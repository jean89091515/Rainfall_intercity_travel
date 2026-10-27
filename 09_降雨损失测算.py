"""降雨造成的城际出行减少量（年均，亿人次），按三类天气分别核算，并给出日常降雨损失的区间与置信区间。

日常降雨（主口径，非台风且两端都不是易降雪日）：用 N7d（含小雨的动态模型，按距离档，日常样本）计入当天至
  3 天后（L0-L3）的效应。按小雨 / 中雨 / ≥25 mm 分解时，每类单独去掉、其余照旧，各类之和与合计略有出入。
易降雪日（非台风，任一端 CPC 日均气温 <2 °C）：用 S1（非台风日的降水分相模型）的系数，只计当天。
台风日：用 T3（雨档 × 台风交互）的“基础 + 台风额外”系数，只计当天，只算降雨部分、不含台风本身（无雨）的效应。
日常降雨的其他口径（均按距离档）：动态模型只算当天；动态模型且起点小雨记零；静态 T5（只算当天）及其
  大区×日期 FE（R7）、CPC 雨量计降水（G5）、扣除移位安慰剂（P_）、起点小雨记零、小雨记零。
置信区间：按各距离档模型的聚类协方差（results/vcov_日常/）做 1,000 次参数模拟，取 2.5% 与 97.5% 分位数。
反事实：起终点都不下雨、其余不变时的流量 = 观测流量 / exp(降雨效应)。只覆盖稳定核心连接（占已披露流量的 98%），因此是下限。

输出：
  results/全国_降雨损失分解.csv   按雨档类别 × 天气类型
  results/全国_降雨损失_距离.csv  日常降雨按距离档的损失率、占比与损失量
  results/全国_降雨损失区间.csv   日常降雨在各口径下的合计与 95% 置信区间
"""
import numpy as np
import pandas as pd

from config import DIST_LABELS, PROC, RESULTS

RE = pd.read_csv(RESULTS / "全国回归结果_日常.csv", encoding="utf-8-sig")   # 日常口径（06 的 RM_EVERYDAY=1）
RA = pd.read_csv(RESULTS / "全国回归结果.csv", encoding="utf-8-sig")        # 全部日、非台风日口径（S1、T3）
VC = RESULTS / "vcov_日常"
PB = ["F28", "F21", "F14", "F7", "L7", "L14", "L21", "L28", "L364", "L728"]
CLASS = np.array([0, 1, 2, 3, 3, 3])      # 雨档 0-5 → 0 无雨 / 1 小雨 / 2 中雨 / 3 ≥25 mm
CLASS_LABELS = ["小雨", "中雨", "≥25 mm"]
LAGS = ["L0", "L1", "L2", "L3"]
YEARS, DRAWS = 3, 1000
rng = np.random.default_rng(1)


def est(model, R=RE):
    m = R[R["model"] == model].set_index("term")["est"]
    if m.empty:
        raise SystemExit(f"缺少模型 {model}，先运行 06")
    return m


def vcov(model, terms):
    v = pd.read_csv(VC / f"{model}.csv", encoding="utf-8-sig", index_col=0)
    return v.reindex(index=terms, columns=terms).fillna(0).to_numpy()


def coefs(model, var, side, R=RE, suffix=""):
    m = est(model, R)
    return np.r_[0.0, [m.get(f"{var}_{side}::{k}{suffix}", 0.0) for k in range(1, 6)]]


cols = ["flow", "ab_o", "ab_d", "abc_o", "abc_d", "dband", "tc500_o", "tc500_d", "sn_o", "sn_d"] + \
       [f"{v}_{t}_{e}" for v in ("m01", "m10", "m25") for t in LAGS for e in ("o", "d")]
x = pd.read_parquet(PROC / "model_od.parquet", columns=cols)
tc = (x["tc500_o"].to_numpy() + x["tc500_d"].to_numpy()) > 0
sn = ~tc & ((x["sn_o"].to_numpy() + x["sn_d"].to_numpy()) > 0)
ev = ~tc & ~sn
e = x[ev]
flow_e, band_e = e["flow"].to_numpy(), e["dband"].to_numpy()

# ---------- 日常降雨：静态口径（只算当天） ----------
T5 = "T5_剔除台风日_距离_dband"


def loss_static(prefix, var="ab", adjust=None):
    bo, bd = e[f"{var}_o"].to_numpy(), e[f"{var}_d"].to_numpy()
    eff = np.zeros(len(e))
    for b in range(5):
        i = band_e == b
        co, cd = coefs(f"{prefix}{b}", var, "o"), coefs(f"{prefix}{b}", var, "d")
        if adjust:
            co, cd = adjust("o", co), adjust("d", cd)
        eff[i] = co[bo[i]] + cd[bd[i]]
    return (flow_e / np.exp(eff) - flow_e).sum() / YEARS / 1e8


def ci_static(prefix, adjust=None):
    cell = e.groupby(["dband", "ab_o", "ab_d"])["flow"].sum().reset_index()
    tot = np.zeros(DRAWS)
    for b in range(5):
        model = f"{prefix}{b}"
        terms = [f"ab_{s}::{k}" for s in ("o", "d") for k in range(1, 6)]
        draws = rng.multivariate_normal(est(model).reindex(terms).fillna(0).to_numpy(), vcov(model, terms), DRAWS)
        c = cell[cell["dband"] == b]
        ao, ad, f = c["ab_o"].to_numpy(), c["ab_d"].to_numpy(), c["flow"].to_numpy()
        for d in range(DRAWS):
            co, cd = np.r_[0.0, draws[d, :5]], np.r_[0.0, draws[d, 5:]]
            if adjust:
                co, cd = adjust("o", co), adjust("d", cd)
            tot[d] += (f * (np.exp(-(co[ao] + cd[ad])) - 1)).sum()
    return np.percentile(tot / YEARS / 1e8, [2.5, 97.5])


def placebo_bias(side):
    """10 个移位安慰剂系数的均值（日常样本），按类别 0-3。"""
    m = RE[RE["model"].isin([f"P_{k}_抽样30%" for k in PB])]
    return np.r_[0.0, [m.loc[m["term"].isin([f"pb_{k}_{side}::{c}" for k in PB]), "est"].mean() for c in (1, 2, 3)]]


# ---------- 日常降雨：动态口径（N7d） ----------
cls = {f"{t}_{s}": (e[f"m01_{t}_{s}"].to_numpy() + 2 * e[f"m10_{t}_{s}"].to_numpy() + 3 * e[f"m25_{t}_{s}"].to_numpy()).astype("int8")
       for t in LAGS for s in ("o", "d")}
dyn = pd.DataFrame({"dband": band_e, "flow": flow_e, **cls}).groupby(["dband", *cls])["flow"].sum().reset_index()
DTERMS = [f"{v}_{t}_{s}" for t in LAGS for s in ("o", "d") for v in ("m01", "m10", "m25")]


def loss_dynamic(lags=LAGS, zero_origin_light=False, only_class=None, draws=0, by_band=False):
    """年均损失（亿人次）。only_class 只去掉该类降雨；draws>0 返回模拟分布；by_band 返回各距离档损失。"""
    out = np.zeros((5, max(draws, 1)))
    for b in range(5):
        model = f"N7d_非台风_动态含小雨_距离_抽样50%_dband{b}"
        mu = est(model).reindex(DTERMS).fillna(0).to_numpy()
        B = rng.multivariate_normal(mu, vcov(model, DTERMS), draws) if draws else mu[None, :]
        B = B.reshape(len(B), len(LAGS), 2, 3)                       # 抽样 × 滞后 × 端 × 类别
        if zero_origin_light:
            B[:, :, 0, 0] = 0.0
        if only_class is not None:
            B[:, :, :, [k for k in range(3) if k != only_class - 1]] = 0.0
        B = np.concatenate([np.zeros(B.shape[:3] + (1,)), B], axis=3)
        c = dyn[dyn["dband"] == b]
        eff = np.zeros((len(B), len(c)))
        for li, t in enumerate(LAGS):
            if t in lags:
                for si, s in enumerate(("o", "d")):
                    eff += B[:, li, si, :][:, c[f"{t}_{s}"].to_numpy()]
        out[b] = (c["flow"].to_numpy()[None, :] * (np.exp(-eff) - 1)).sum(axis=1)
    out = out / YEARS / 1e8
    if by_band:
        return out[:, 0]
    tot = out.sum(axis=0)
    return tot if draws else tot[0]


# ---------- 易降雪日与台风日（只计当天） ----------
def loss_snow():
    s1 = "S1_非台风_降水分相_抽样50%"
    z = x[sn]
    eff = np.zeros(len(z))
    for side in ("o", "d"):
        w, s = coefs(s1, "abw", side, RA), coefs(s1, "abs", side, RA)
        b, cold = z[f"ab_{side}"].to_numpy(), z[f"sn_{side}"].to_numpy() == 1
        eff += np.where(cold, s[b], w[b])
    l = z["flow"].to_numpy() / np.exp(eff) - z["flow"].to_numpy()
    k = CLASS[np.maximum(z["ab_o"].to_numpy(), z["ab_d"].to_numpy())]
    return pd.Series(l).groupby(k).sum().reindex([1, 2, 3], fill_value=0).to_numpy() / YEARS / 1e8


def loss_typhoon():
    t3 = "T3_雨档x台风_抽样50%"
    z = x[tc]
    eff = np.zeros(len(z))
    for side in ("o", "d"):
        b, on = z[f"ab_{side}"].to_numpy(), z[f"tc500_{side}"].to_numpy()
        eff += coefs(t3, "ab", side, RA)[b] + on * coefs(t3, "ab", side, RA, f":tc500_{side}")[b]
    l = z["flow"].to_numpy() / np.exp(eff) - z["flow"].to_numpy()
    k = CLASS[np.maximum(z["ab_o"].to_numpy(), z["ab_d"].to_numpy())]
    return pd.Series(l).groupby(k).sum().reindex([1, 2, 3], fill_value=0).to_numpy() / YEARS / 1e8


if __name__ == "__main__":
    by_class = np.array([loss_dynamic(only_class=k) for k in (1, 2, 3)])
    tab = pd.DataFrame({"日常降雨（计入滞后）": by_class, "易降雪日（当天）": loss_snow(), "台风日（当天）": loss_typhoon()},
                       index=CLASS_LABELS)
    tab.loc["合计"] = tab.sum()
    tab.round(4).to_csv(RESULTS / "全国_降雨损失分解.csv", encoding="utf-8-sig")
    print("按天气类型与雨档类别（亿人次/年）：\n", tab.round(2).to_string())

    lb = loss_dynamic(by_band=True)
    fb = pd.Series(flow_e).groupby(band_e).sum().to_numpy() / YEARS / 1e8
    dist = pd.DataFrame({"损失率": lb / (fb + lb), "损失占比": lb / lb.sum(), "年损失_亿人次": lb}, index=DIST_LABELS)
    dist.round(4).to_csv(RESULTS / "全国_降雨损失_距离.csv", encoding="utf-8-sig")
    print("日常降雨按距离档：\n", dist.round(3).to_string())

    bias = {s: placebo_bias(s) for s in ("o", "d")}
    adj_placebo = lambda s, c: c - bias[s][CLASS]
    adj_light0 = lambda s, c: np.where(CLASS == 1, 0.0, c)
    adj_olight0 = lambda s, c: np.where((CLASS == 1) & (s == "o"), 0.0, c)
    rows = {}
    for name, kw in (("动态：计入滞后（主估计）", {}), ("动态：只算当天", {"lags": ["L0"]}),
                     ("动态：计入滞后、起点小雨记零", {"zero_origin_light": True})):
        rows[name] = [loss_dynamic(**kw), *np.percentile(loss_dynamic(draws=DRAWS, **kw), [2.5, 97.5])]
    for name, adj in (("静态：只算当天", None), ("静态：起点小雨记零", adj_olight0), ("静态：小雨记零", adj_light0),
                      ("静态：扣除移位安慰剂", adj_placebo)):
        rows[name] = [loss_static(T5, adjust=adj), *ci_static(T5, adj)]
    rows["静态：大区×日期固定效应"] = [loss_static("R7_非台风_大区日期FE_距离_dband"), np.nan, np.nan]
    rows["静态：雨量计降水（CPC）"] = [loss_static("G5_非台风_CPC降水_距离_dband", "abc"), np.nan, np.nan]
    rng_tab = pd.DataFrame(rows, index=["合计", "95%下限", "95%上限"]).T
    rng_tab.round(4).to_csv(RESULTS / "全国_降雨损失区间.csv", encoding="utf-8-sig")
    print("日常降雨损失的口径与置信区间（亿人次/年）：\n", rng_tab.round(2).to_string())
    print(f"连接-日：日常 {ev.mean():.1%}，易降雪日 {sn.mean():.1%}，台风日 {tc.mean():.1%}")
