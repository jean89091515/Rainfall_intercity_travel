"""标度律 / 统计物理视角的初探（给导师交流用，非论文主结果）。只用非台风日。

  A 引力模型：稳定连接上 ln 平均流量 = 起点 FE + 终点 FE − γ ln 距离；
    降雨对距离衰减的改变 Δγ = 各距离档降雨效应对 ln 距离的斜率（T5 系数，按 1/se² 加权）。
  B 涨落分布：去掉连接×年月均值、全国日期均值、连接×星期均值后的逐日对数偏差 ε，
    按两端最大雨档分组，看均值平移、方差和左尾。
  C 城市“磁化率”：城市总流出的对数偏差在 ≥25 mm 日与无雨日之差，随城市流动规模、气候的变化。

输出 results/scaling/：图_A_距离衰减.png、图_B_涨落分布.png、图_C_城市敏感度.png、summary.json
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

from config import PROC, RESULTS

OUT = RESULTS / "scaling"
OUT.mkdir(exist_ok=True)
for _f in ("/System/Library/Fonts/STHeiti Medium.ttc", "/Library/Fonts/Arial Unicode.ttf"):
    if os.path.exists(_f):
        font_manager.fontManager.addfont(_f)
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Heiti SC", "Arial Unicode MS"],
                     "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.unicode_minus": False})
BLUE, ORANGE, GREY = "#1f4e9c", "#d9622b", "#8c96a3"
R = pd.read_csv(RESULTS / "全国回归结果.csv", encoding="utf-8-sig")
S = {}


# ---------- A 引力模型与降雨对距离衰减指数的改变 ----------
def two_way_fe(y, a, b, x, iters=200):
    """y = FE_a + FE_b + g·x，交替投影求 g。"""
    ya, xa = y.copy(), x.copy()
    for _ in range(iters):
        for g in (a, b):
            ya = ya - pd.Series(ya).groupby(g).transform("mean").to_numpy()
            xa = xa - pd.Series(xa).groupby(g).transform("mean").to_numpy()
    return (xa @ ya) / (xa @ xa), xa, ya


e = pd.read_parquet(PROC / "edges.parquet")
e = e[e.core & (e.dist_km > 0)].copy()
lnd = np.log(e.dist_km.to_numpy())
g, xr, yr = two_way_fe(np.log(e.mean_flow.to_numpy()), e.o.to_numpy(), e.d.to_numpy(), lnd)
S["gamma_fe"] = -g
mass_o = e.groupby("o").mean_flow.sum()
mass_d = e.groupby("d").mean_flow.sum()
X = np.c_[np.ones(len(e)), np.log(e.o.map(mass_o)), np.log(e.d.map(mass_d)), lnd]
coef = np.linalg.lstsq(X, np.log(e.mean_flow.to_numpy()), rcond=None)[0]
S["gravity_mass"] = {"alpha_o": coef[1], "beta_d": coef[2], "gamma": -coef[3]}

band_d = e.groupby("dist_band").dist_km.median().reindex(["<150", "150-300", "300-500", "500-1000", ">1000"])
S["band_median_km"] = band_d.round(0).to_dict()
names = {2: "中雨", 3: "大雨", 4: "暴雨"}
dg = {}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
# 分箱散点：去掉两端固定效应后的 ln 流量 vs ln 距离
q = pd.qcut(xr, 30)
bx = pd.Series(xr + lnd.mean()).groupby(q).mean()
by = pd.Series(yr).groupby(q).mean()
a1.scatter(np.exp(bx), np.exp(by), s=14, color=BLUE)
xx = np.linspace(bx.min() - lnd.mean(), bx.max() - lnd.mean(), 50)
a1.plot(np.exp(xx + lnd.mean()), np.exp(g * xx), color=ORANGE, lw=1.2, label=f"γ = {-g:.2f}")
a1.set_xscale("log"); a1.set_yscale("log")
a1.set_xlabel("起终点距离（km，对数轴）"); a1.set_ylabel("流量（去掉起终点固定效应，相对值）")
a1.set_title("a  稳定连接的距离衰减：F ∝ d^−γ", loc="left")
a1.legend(frameon=False)
cols = {2: "#9ecae1", 3: "#4292c6", 4: "#08306b"}
for side, mk in (("d", "o"), ("o", "s")):
    for k in (2, 3, 4):
        rows = []
        for b in range(5):
            s = R[(R.model == f"T5_剔除台风日_距离_dband{b}") & (R.term == f"ab_{side}::{k}")]
            rows.append((np.log(band_d.iloc[b]), s.est.iloc[0], s.se.iloc[0]))
        x, y, se = map(np.array, zip(*rows))
        w = 1 / se ** 2
        slope = np.polyfit(x, y, 1, w=np.sqrt(w))
        dg[f"{side}_{names[k]}"] = slope[0]
        if side == "d":
            a2.errorbar(np.exp(x), 100 * (np.exp(y) - 1), yerr=196 * se, fmt=mk, color=cols[k], ms=4, capsize=2,
                        label=f"终点{names[k]}：Δγ = {slope[0]:+.3f}")
            a2.plot(np.exp(x), 100 * (np.exp(np.polyval(slope, x)) - 1), color=cols[k], lw=0.9)
a2.set_xscale("log")
a2.axhline(0, color="0.6", lw=0.6)
a2.set_xlabel("起终点距离（km，对数轴，各档中位数）"); a2.set_ylabel("相对无雨日的流量变化（%）")
a2.set_title("b  降雨让距离衰减变平：γ_雨 = γ − Δγ", loc="left")
a2.legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "图_A_距离衰减.png", dpi=220); plt.close(fig)
S["delta_gamma"] = dg

# ---------- B 涨落分布 ----------
cols_b = ["ln_flow", "od_ym", "od_dow", "date_id", "ab_o", "ab_d", "tc500_o", "tc500_d"]
x = pd.read_parquet(PROC / "model_od.parquet", columns=cols_b)
x = x[(x.tc500_o == 0) & (x.tc500_d == 0)]
eps = x.ln_flow.to_numpy() - x.groupby("od_ym").ln_flow.transform("mean").to_numpy()
for key in ("date_id", "od_dow", "date_id"):
    eps = eps - pd.Series(eps, index=x.index).groupby(x[key]).transform("mean").to_numpy()
cls = np.minimum(np.maximum(x.ab_o.to_numpy(), x.ab_d.to_numpy()), 4)
lab = ["两端无雨", "小雨", "中雨", "大雨", "暴雨及以上"]
colors = ["#7f7f7f", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]
stat = {}
fig, (b1, b2) = plt.subplots(1, 2, figsize=(10, 3.8))
edges = np.linspace(-1.0, 0.6, 161)
for k in range(5):
    v = eps[cls == k]
    h, _ = np.histogram(v, edges, density=True)
    b1.plot((edges[1:] + edges[:-1]) / 2, h, color=colors[k], lw=1.3, label=lab[k])
    t = np.sort(-v)
    xs = np.linspace(0.05, 1.0, 60)
    ccdf = 1 - np.searchsorted(t, xs) / len(t)
    b2.plot(xs, ccdf, color=colors[k], lw=1.3, label=lab[k])
    stat[lab[k]] = {"n": int(len(v)), "mean": float(v.mean()), "sd": float(v.std()),
                    "p05": float(np.quantile(v, 0.05)), "P_drop_gt_30pct": float((v < np.log(0.7)).mean())}
b1.set_xlim(-0.8, 0.5); b1.set_yscale("log"); b1.set_ylim(1e-3, None)
b1.set_xlabel("逐日对数偏差 ε（去掉连接×年月、日期、连接×星期均值）"); b1.set_ylabel("概率密度（对数轴）")
b1.set_title("a  不同雨档下的涨落分布", loc="left"); b1.legend(frameon=False, fontsize=8)
b2.set_yscale("log"); b2.set_xlabel("下降幅度 −ε"); b2.set_ylabel("P(−ε > x)")
b2.set_title("b  左尾：降雨增加 10%–45% 的下降，更大的下降多来自其他冲击", loc="left"); b2.legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "图_B_涨落分布.png", dpi=220); plt.close(fig)
S["fluctuation"] = stat
del x, eps

# ---------- C 城市敏感度 vs 规模、气候 ----------
c = pd.read_parquet(PROC / "model_city.parquet", columns=["code", "outflow", "ab", "tc500", "code_ym", "code_dow",
                                                          "date_id"])
c = c[(c.tc500 == 0) & (c.outflow > 0)].copy()
c["y"] = np.log(c.outflow)
r = c.y - c.groupby("code_ym").y.transform("mean")
for key in ("date_id", "code_dow", "date_id"):
    r = r - r.groupby(c[key]).transform("mean")
c["r"] = r
u = pd.read_parquet(PROC / "units.parquet").set_index("code")
g = c[["code", "r", "ab", "outflow"]].groupby("code")
sens = pd.DataFrame({"dry": g[["r", "ab"]].apply(lambda d: d.r[d.ab == 0].mean()),
                     "heavy": g[["r", "ab"]].apply(lambda d: d.r[d.ab >= 3].mean()),
                     "n_heavy": g["ab"].apply(lambda s: int((s >= 3).sum())),
                     "mass": g.outflow.mean()})
sens = sens[sens.n_heavy >= 10].join(u[["name", "annual_mm", "region4"]])
sens["chi"] = 100 * (np.exp(sens.heavy - sens.dry) - 1)
fit_m = np.polyfit(np.log10(sens.mass), sens.chi, 1)
fit_p = np.polyfit(np.log10(sens.annual_mm), sens.chi, 1)
X = np.c_[np.ones(len(sens)), np.log10(sens.mass), np.log10(sens.annual_mm)]
both = np.linalg.lstsq(X, sens.chi.to_numpy(), rcond=None)[0]
S["city_sensitivity"] = {"n_cities": int(len(sens)), "median_chi_pct": float(sens.chi.median()),
                         "slope_per_decade_mass": float(fit_m[0]), "slope_per_decade_precip": float(fit_p[0]),
                         "joint": {"per_decade_mass": float(both[1]), "per_decade_precip": float(both[2])},
                         "corr_mass_precip": float(np.corrcoef(np.log(sens.mass), np.log(sens.annual_mm))[0, 1])}
fig, (c1, c2) = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
reg_col = {"东部": BLUE, "中部": "#4f9a5b", "西部": ORANGE, "东北": "#8064a2"}
for ax, var, fit, xl in ((c1, "mass", fit_m, "城市日均总流出（人次，对数轴）"),
                         (c2, "annual_mm", fit_p, "1991—2020 年平均年降水量（mm，对数轴）")):
    for reg, col in reg_col.items():
        s = sens[sens.region4 == reg]
        ax.scatter(s[var], s.chi, s=10, color=col, alpha=0.7, label=reg)
    xs = np.logspace(np.log10(sens[var].min()), np.log10(sens[var].max()), 20)
    ax.plot(xs, np.polyval(fit, np.log10(xs)), color="k", lw=1)
    ax.set_xscale("log"); ax.axhline(0, color="0.6", lw=0.6); ax.set_xlabel(xl)
    ax.text(0.02, 0.04, f"每增加 10 倍：{fit[0]:+.1f} 个百分点", transform=ax.transAxes, fontsize=8)
c1.set_ylabel("≥25 mm 日相对无雨日的总流出变化（%）")
c1.set_title("a  城市“磁化率”与流动规模", loc="left"); c2.set_title("b  城市“磁化率”与气候", loc="left")
c1.legend(frameon=False, fontsize=8, ncol=2)
fig.tight_layout(); fig.savefig(OUT / "图_C_城市敏感度.png", dpi=220); plt.close(fig)
sens.round(4).to_csv(OUT / "城市敏感度.csv", encoding="utf-8-sig")

(OUT / "summary.json").write_text(json.dumps(S, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
print(json.dumps(S, ensure_ascii=False, indent=1, default=float))
