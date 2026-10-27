"""北京试点：在只有北京降水的情况下，先估计北京降雨对进出北京城际流量的影响。

识别：只有一个城市的降雨时，日期固定效应会吸收它。因此用两端都距北京 800 km 以上的稳定连接作对照组
（同日降雨与北京几乎不相关），由它们识别日期固定效应；北京出发、到达北京的连接为处理组。
  ln F_ij,t = Σ_k β_k^out·1[i=北京]·1[北京雨档=k] + Σ_k β_k^in·1[j=北京]·1[北京雨档=k]
              + 北京连接 × 节假日窗口 + μ_ij,ym + η_ij,dow + λ_t + ε
标准误按“年-周”聚类（处理只随日期变化，需允许同一周内的序列相关）。

依赖 pyfixest。用法：python 05_北京试点.py
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf
from matplotlib import font_manager

from config import PROC, RESULTS

for _f in ("/System/Library/Fonts/STHeiti Medium.ttc", "/Library/Fonts/Arial Unicode.ttf"):
    if os.path.exists(_f):
        font_manager.fontManager.addfont(_f)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Heiti SC", "Arial Unicode MS", "Source Han Sans", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

BJ = 110000
CONTROL_KM = 800
CONTROL_N = 2000          # 对照连接随机抽样数：全部约 1.5 万条会让内存超过 40 GB；日期效应用 2000 条足够估计
SEED = int(os.environ.get("RM_SEED", 1))
# 北京 2023-2025 年仅 7 个暴雨日，试点把大雨和暴雨合并为“≥25 mm”
BINS = [0, 0.1, 10, 25, np.inf]
LABELS = ["无雨", "小雨 0.1-10", "中雨 10-25", "大雨及以上 ≥25"]
FE = "od_ym + od_dow + date"
VCOV = {"CRV1": "week"}

# 国务院办公厅公布的放假日期（含调休后的连续假期）
HOLIDAYS = [("2022-12-31", "2023-01-02"), ("2023-01-21", "2023-01-27"), ("2023-04-05", "2023-04-05"),
            ("2023-04-29", "2023-05-03"), ("2023-06-22", "2023-06-24"), ("2023-09-29", "2023-10-06"),
            ("2023-12-30", "2024-01-01"), ("2024-02-10", "2024-02-17"), ("2024-04-04", "2024-04-06"),
            ("2024-05-01", "2024-05-05"), ("2024-06-08", "2024-06-10"), ("2024-09-15", "2024-09-17"),
            ("2024-10-01", "2024-10-07"), ("2025-01-01", "2025-01-01"), ("2025-01-28", "2025-02-04"),
            ("2025-04-04", "2025-04-06"), ("2025-05-01", "2025-05-05"), ("2025-05-31", "2025-06-02"),
            ("2025-10-01", "2025-10-08")]
CHUNYUN = [("2023-01-07", "2023-02-15"), ("2024-01-26", "2024-03-05"), ("2025-01-14", "2025-02-22")]


def date_flags(dates: pd.Series) -> pd.DataFrame:
    """假期前 2 天、假期中、假期后 2 天，以及春运 40 天。"""
    out = pd.DataFrame(index=dates.index)
    for k in ("hol_pre", "hol_in", "hol_post", "chunyun"):
        out[k] = 0
    for a, b in HOLIDAYS:
        a, b = pd.Timestamp(a), pd.Timestamp(b)
        out.loc[dates.between(a - pd.Timedelta(days=2), a - pd.Timedelta(days=1)), "hol_pre"] = 1
        out.loc[dates.between(a, b), "hol_in"] = 1
        out.loc[dates.between(b + pd.Timedelta(days=1), b + pd.Timedelta(days=2)), "hol_post"] = 1
    for a, b in CHUNYUN:
        out.loc[dates.between(pd.Timestamp(a), pd.Timestamp(b)), "chunyun"] = 1
    return out.astype("int8")


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * np.arcsin(np.sqrt(a))


def build() -> pd.DataFrame:
    u = pd.read_parquet(PROC / "units.parquet").set_index("code")
    km_bj = pd.Series(haversine_km(u.lat, u.lon, u.at[BJ, "lat"], u.at[BJ, "lon"]), index=u.index)
    e = pd.read_parquet(PROC / "edges.parquet")
    e = e[e.core]
    far = e[e["o"].map(km_bj).ge(CONTROL_KM) & e["d"].map(km_bj).ge(CONTROL_KM)]
    ctrl = far.sample(min(CONTROL_N, len(far)), random_state=SEED)
    keep = pd.concat([e[(e.o == BJ) | (e.d == BJ)], ctrl])[["o", "d", "dist_km"]]
    print(f"处理组：北京出发 {(keep.o == BJ).sum()} 条、到达北京 {(keep.d == BJ).sum()} 条；"
          f"对照组从 {len(far)} 条远距离连接中抽 {len(ctrl)} 条（种子 {SEED}）", flush=True)

    p = pd.read_parquet(PROC / "od_panel.parquet").rename(columns={"Date": "date"}).merge(keep, on=["o", "d"])
    r = pd.read_parquet(PROC / "city_rain.parquet").query("code == @BJ").sort_values("date")
    r["bin"] = pd.cut(r["rain_mm"], BINS, labels=False, right=False).astype(int)
    r["ge10"] = (r["rain_mm"] >= 10).astype(int)
    r["ge25"] = (r["rain_mm"] >= 25).astype(int)
    r["m10"] = r["rain_mm"].between(10, 25, inclusive="left").astype(int)
    for k in (-3, -2, -1, 1, 2, 3, 7):
        tag = f"F{-k}" if k < 0 else f"L{k}"
        r[f"m10_{tag}"] = r["m10"].shift(k)
        r[f"ge25_{tag}"] = r["ge25"].shift(k)
    p = p.merge(r.drop(columns=["code", "abs_bin", "rel_bin"], errors="ignore"), on="date", how="left")

    p["out"] = (p.o == BJ).astype("int8")
    p["inn"] = (p.d == BJ).astype("int8")
    p = pd.concat([p, date_flags(p["date"])], axis=1)
    for g in ("out", "inn"):
        for k in (1, 2, 3):
            p[f"{g}_b{k}"] = p[g] * (p["bin"] == k)
        for f in ("hol_pre", "hol_in", "hol_post", "chunyun"):
            p[f"{g}_{f}"] = p[g] * p[f]
    p["dgrp"] = pd.cut(p["dist_km"], [0, 500, 1000, np.inf], labels=["<500", "500-1000", ">1000"]).astype(str)
    p["ln_flow"] = np.log(p["flow"])
    od = p["o"].astype("int64") * 1_000_000 + p["d"]
    p["od_ym"] = od * 10_000 + p["date"].dt.year * 100 + p["date"].dt.month
    p["od_dow"] = od * 10 + p["date"].dt.dayofweek
    iso = p["date"].dt.isocalendar()
    p["week"] = iso["year"].astype(int) * 100 + iso["week"].astype(int)
    return p


def tidy(fit, name):
    t = fit.tidy().reset_index().rename(columns={"Coefficient": "term"})
    t.insert(0, "model", name)
    t["pct"] = 100 * (np.exp(t["Estimate"]) - 1)            # 对数系数换算为百分比变化
    t["pct_lo"] = 100 * (np.exp(t["2.5%"]) - 1)
    t["pct_hi"] = 100 * (np.exp(t["97.5%"]) - 1)
    return t


def plot_distance(out: pd.DataFrame):
    """北京出发流量：各距离组在各雨档下相对无雨日的变化（95% 置信区间）。"""
    groups = [("P3_距离<500", "<500 km"), ("P3_距离500-1000", "500–1000 km"), ("P3_距离>1000", ">1000 km")]
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for i, (m, lab) in enumerate(groups):
        s = out[(out.model == m) & out.term.str.match(r"out_b\d$")].sort_values("term")
        x = np.arange(1, 4) + (i - 1) * 0.18
        ax.errorbar(x, s["pct"], yerr=[s["pct"] - s["pct_lo"], s["pct_hi"] - s["pct"]], fmt="o", capsize=3,
                    color=plt.cm.Blues(0.9 - 0.25 * i), label=lab)
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks([1, 2, 3], LABELS[1:])
    ax.set_ylabel("北京出发流量相对无雨日的变化（%）")
    ax.set_title("北京降雨对出京流量的影响随距离递减")
    ax.legend(title="目的地距离", frameon=False)
    fig.tight_layout()
    fig.savefig(RESULTS / "北京试点_距离梯度.png", dpi=200)
    plt.close(fig)


HOLCTRL = " + ".join(f"{g}_{f}" for g in ("out", "inn") for f in ("hol_pre", "hol_in", "hol_post", "chunyun"))

if __name__ == "__main__":
    p = build()
    print(f"面板 {len(p):,} 行，{p['date'].nunique()} 天", flush=True)
    res = []

    # P1 剂量-响应
    rhs = " + ".join(f"{g}_b{k}" for g in ("out", "inn") for k in (1, 2, 3))
    m1 = pf.feols(f"ln_flow ~ {rhs} + {HOLCTRL} | {FE}", data=p, vcov=VCOV)
    res.append(tidy(m1, "P1_剂量响应"))

    # P2 剔除春运与节假日窗口
    calm = p[(p.chunyun == 0) & (p.hol_pre + p.hol_in + p.hol_post == 0)]
    res.append(tidy(pf.feols(f"ln_flow ~ {rhs} | {FE}", data=calm, vcov=VCOV), "P2_剔除节假日春运"))

    # P3 距离：北京连接按距离分组，对照组共用
    for g in ("<500", "500-1000", ">1000"):
        sub = p[((p.out == 0) & (p.inn == 0)) | (p.dgrp == g)]
        res.append(tidy(pf.feols(f"ln_flow ~ {rhs} + {HOLCTRL} | {FE}", data=sub, vcov=VCOV), f"P3_距离{g}"))

    # P4 动态：前导（预报）与滞后（补回）；L7 为安慰剂
    lags = ["F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7"]
    p["m10_L0"], p["ge25_L0"] = p["m10"], p["ge25"]
    dyn = " + ".join(f"{g}_{v}_{t}" for g in ("out", "inn") for v in ("m10", "ge25") for t in lags)
    for g in ("out", "inn"):
        for v in ("m10", "ge25"):
            for t in lags:
                p[f"{g}_{v}_{t}"] = p[g] * p[f"{v}_{t}"]
    pd_ = p.dropna(subset=[f"m10_{t}" for t in lags if t != "L0"])
    res.append(tidy(pf.feols(f"ln_flow ~ {dyn} + {HOLCTRL} | {FE}", data=pd_, vcov=VCOV), "P4_动态"))

    out = pd.concat(res, ignore_index=True)
    out.to_csv(RESULTS / "北京试点_回归结果.csv", index=False, encoding="utf-8-sig")
    plot_distance(out)
    show = out[out.term.str.match(r"(out|inn)_b\d$")][["model", "term", "Estimate", "Std. Error", "pct", "Pr(>|t|)"]]
    print(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("结果已写入", RESULTS)
