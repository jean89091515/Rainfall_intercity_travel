"""Publication figures for the manuscript, in English or Chinese, at 300 dpi.

用法：python3 10_论文图表.py [en|zh]    # en → results/paper/，zh → results/paper_zh/

Main specification ("everyday rain", 06 with RM_EVERYDAY=1): link-days with no tropical cyclone within 500 km of
either end and no snow-prone end (CPC daily mean temperature below 2 °C), with 7-day antecedent rainfall controls.
Fig. 5 is the dynamic model with light rain (N7); Fig. 6 counts effects up to three days after the rain (09).
Fig. 7 contrasts all days, days without typhoons, and the main sample.

  Fig1_study_area.png    cities shaded by 1991–2020 mean annual precipitation (ERA5-Land), SCS inset
  Fig2_dose_response.png
  Fig3_distance.png
  Fig4_climate.png       (a) absolute bins by origin climate, (b) local-percentile bins, (c) regions
  Fig5_dynamics.png
  Fig6_losses.png
  Fig7_typhoon.png
"""
import os
import sys

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from config import ADMIN_DIR, PROC, RESULTS

LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
OUT = RESULTS / ("paper" if LANG == "en" else "paper_zh")
OUT.mkdir(exist_ok=True)

TXT = {
    "en": dict(
        ylab="Change in OD flow vs. dry day (%)", ylab_dyn="Change in OD flow (%)",
        rain=["None", "Light\n0.1–10", "Moderate\n10–25", "Heavy\n25–50", "Rainstorm\n50–100", "Extreme\n≥100"],
        rain_short=["None", "Light", "Mod.", "Heavy", "Storm", "Extr."], rel_none="None",
        precip="Daily precipitation (mm)", origin="Rain at origin", dest="Rain at destination",
        dist="Origin–destination distance (km)", days=["Workday", "Weekend", "Public holiday"],
        short_o="Rain at origin, links <300 km", short_d="Rain at destination, links <300 km",
        bins={2: "Moderate (10–25 mm)", 3: "Heavy (25–50 mm)", 4: "Rainstorm (50–100 mm)"},
        humid="Humid origin (≥800 mm)", dry="Drier origin (<800 mm)", humid_s="Humid origin", dry_s="Drier origin",
        abs="Absolute bins", rel="Local-percentile bins", region="By region of origin",
        regions=["East", "Central", "West", "Northeast"],
        r25="Rain ≥25 mm", r10="Rain 10–25 mm", r01="Rain 0.1–10 mm", at_o="At origin", at_d="At destination", placebo="(placebo)",
        dyn_x="Days from rain to flow (negative = rain occurs after the flow day)",
        all="All days", ntc="Excluding typhoon days", evd="Excluding typhoon and snow-prone days",
        loss_y="Trips lost per year (million)", loss_scale=100, loss_fmt="{:.0f}",
        loss_bins=["Light\n0.1–10", "Moderate\n10–25", "≥25 mm"],
        loss_t="By rain class, everyday rain (total {:,.0f} million)", share="({:.0%})",
        rate_lab="{:.1f}%\n({:.0%} of loss)", rate_y="Share of counterfactual trips lost (%)",
        rate_t="Loss rate by distance, everyday rain",
        cbar="Mean annual precipitation, 1991–2020 (mm)", humid_line="Humid zone boundary (800 mm)"),
    "zh": dict(
        ylab="相对无雨日的流量变化（%）", ylab_dyn="流量变化（%）",
        rain=["无雨", "小雨\n0.1–10", "中雨\n10–25", "大雨\n25–50", "暴雨\n50–100", "大暴雨及以上\n≥100"],
        rain_short=["无雨", "小雨", "中雨", "大雨", "暴雨", "大暴雨+"], rel_none="无雨",
        precip="日降水量（mm）", origin="起点降雨", dest="终点降雨", dist="起终点距离（km）",
        days=["工作日", "周末", "节假日"], short_o="起点降雨，300 km 以内连接", short_d="终点降雨，300 km 以内连接",
        bins={2: "中雨（10–25 mm）", 3: "大雨（25–50 mm）", 4: "暴雨（50–100 mm）"},
        humid="湿润区起点（≥800 mm）", dry="非湿润区起点（<800 mm）", humid_s="湿润区起点", dry_s="非湿润区起点",
        abs="国标绝对分档", rel="本地分位数分档", region="按起点所在区域", regions=["东部", "中部", "西部", "东北"],
        r25="降雨 ≥25 mm", r10="降雨 10–25 mm", r01="降雨 0.1–10 mm", at_o="起点降雨", at_d="终点降雨", placebo="（安慰剂）",
        dyn_x="流量日相对降雨日的天数（负值表示降雨发生在流量日之后）",
        all="全部日", ntc="剔除台风日", evd="剔除台风日与易降雪日",
        loss_y="年均减少出行（亿人次）", loss_scale=1, loss_fmt="{:.2f}",
        loss_bins=["小雨\n0.1–10", "中雨\n10–25", "≥25 mm"],
        loss_t="日常降雨，按雨档类别（合计 {:.1f} 亿人次）", share="({:.0%})",
        rate_lab="{:.1f}%\n(占损失 {:.0%})", rate_y="损失占无雨反事实出行的比例（%）",
        rate_t="日常降雨，按起终点距离的损失率",
        cbar="1991—2020 年平均年降水量（mm）", humid_line="湿润区界线（800 mm）"),
}[LANG]

if LANG == "zh":
    for _f in ("/System/Library/Fonts/STHeiti Medium.ttc", "/Library/Fonts/Arial Unicode.ttf"):
        if os.path.exists(_f):
            font_manager.fontManager.addfont(_f)
    FONTS = ["Heiti SC", "Arial Unicode MS"]
else:
    FONTS = ["Arial", "Helvetica", "DejaVu Sans"]
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": FONTS,
                     "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8, "legend.fontsize": 7.5,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.unicode_minus": LANG == "en"})
MM = 1 / 25.4
BLUE, ORANGE, GREY = "#1f4e9c", "#d9622b", "#8c96a3"
R = pd.read_csv(RESULTS / "全国回归结果_日常.csv", encoding="utf-8-sig")      # 主口径
RA = pd.read_csv(RESULTS / "全国回归结果.csv", encoding="utf-8-sig")       # 全部日、剔除台风日（图 7 对照）
REL = [TXT["rel_none"], "<P75", "P75–90", "P90–95", "P95–99", "≥P99"]
DIST = ["<150", "150–300", "300–500", "500–1000", ">1000"]


def bins(model, var, k_max=5, res=None):
    """Percent effects with 95% CI for i(var) levels 1..k_max, plus the reference level 0."""
    res = R if res is None else res
    rows = [(0, 0.0, 0.0, 0.0)]
    for k in range(1, k_max + 1):
        s = res[(res.model == model) & (res.term == f"{var}::{k}")]
        if len(s):
            e, se = s.est.iloc[0], s.se.iloc[0]
            rows.append((k, *(100 * (np.exp(v) - 1) for v in (e, e - 1.96 * se, e + 1.96 * se))))
    return pd.DataFrame(rows, columns=["k", "pct", "lo", "hi"])


def term(model, t):
    s = R[(R.model == model) & (R.term == t)]
    e, se = s.est.iloc[0], s.se.iloc[0]
    return [100 * (np.exp(v) - 1) for v in (e, e - 1.96 * se, e + 1.96 * se)]


def line(ax, d, x, color, label, marker="o", ls="-"):
    ax.errorbar(x, d.pct, yerr=[d.pct - d.lo, d.hi - d.pct], fmt=marker, ls=ls, color=color, ms=3.5, lw=1.2,
                capsize=2, elinewidth=0.9, label=label)


def frame(ax, labels, ylabel=None):
    ax.axhline(0, color="0.6", lw=0.6)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_ylabel(TXT["ylab"] if ylabel is None else ylabel)
    ax.grid(axis="y", color="0.92", lw=0.5)


def tag(ax, s):
    ax.text(-0.12, 1.04, s, transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")


def fig1():
    u = pd.read_parquet(PROC / "units.parquet")[["code", "annual_mm"]]
    city = gpd.read_file(ADMIN_DIR / "市.shp")
    city["code"] = city["市代码"].astype(int)
    city = city.merge(u, on="code", how="left")
    prov = gpd.read_file(ADMIN_DIR / "省.shp")
    nine = gpd.read_file(ADMIN_DIR / "十段线.shp")
    crs = "+proj=aea +lat_1=25 +lat_2=47 +lon_0=105 +datum=WGS84"
    city, prov, nine = city.to_crs(crs), prov.to_crs(crs), nine.to_crs(crs)
    city.loc[city["code"] == 460300, "annual_mm"] = np.nan        # 三沙市：无代表性降水，不参与分析
    edges = [0, 200, 400, 800, 1200, 1600, 2400]
    cmap = plt.get_cmap("YlGnBu", len(edges) - 1)
    norm = BoundaryNorm(edges, cmap.N)
    fig, ax = plt.subplots(figsize=(140 * MM, 110 * MM))
    city.plot(ax=ax, column="annual_mm", cmap=cmap, norm=norm, edgecolor="white", linewidth=0.15,
              missing_kwds={"color": "0.85", "edgecolor": "white", "linewidth": 0.15})
    city[city["annual_mm"] >= 800].dissolve().boundary.plot(ax=ax, color="#b2182b", linewidth=0.9)
    prov.boundary.plot(ax=ax, color="0.35", linewidth=0.3)
    xmin, ymin, xmax, ymax = city.loc[city["code"] != 460300].total_bounds     # 大陆与海南，南海诸岛见插图
    ax.set_xlim(xmin - 1e5, xmax + 1e5)
    ax.set_ylim(ymin - 1e5, ymax + 1e5)
    ax.set_axis_off()
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax, fraction=0.03, pad=0.01, ticks=edges)
    cb.set_label(TXT["cbar"])
    ax.plot([], [], color="#b2182b", lw=0.9, label=TXT["humid_line"])
    ax.legend(loc="lower left", frameon=False)
    ax.text(0.99, -0.02, "GS(2024)0650", transform=ax.transAxes, ha="right", va="top", fontsize=6, color="0.4")
    ins = inset_axes(ax, width="18%", height="28%", loc="lower right", borderpad=0.6)
    city.plot(ax=ins, column="annual_mm", cmap=cmap, norm=norm, edgecolor="white", linewidth=0.1,
              missing_kwds={"color": "0.85"})
    nine.plot(ax=ins, color="0.3", linewidth=0.6)
    sx = nine.total_bounds
    ins.set_xlim(sx[0] - 1e5, sx[2] + 1e5)
    ins.set_ylim(sx[1] - 1e5, sx[3] + 1e5)
    ins.set_xticks([]); ins.set_yticks([])
    for sp in ins.spines.values():
        sp.set_visible(True); sp.set_linewidth(0.5)
    fig.savefig(OUT / "Fig1_study_area.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(120 * MM, 72 * MM))
    x = np.arange(6)
    line(ax, bins("T2_剔除台风日500km", "ab_o"), x - 0.07, BLUE, TXT["origin"])
    line(ax, bins("T2_剔除台风日500km", "ab_d"), x + 0.07, ORANGE, TXT["dest"], "s")
    frame(ax, TXT["rain"])
    ax.set_xlabel(TXT["precip"])
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "Fig2_dose_response.png", dpi=300)
    plt.close(fig)


def fig3():
    fig, axes = plt.subplots(2, 2, figsize=(180 * MM, 132 * MM))
    shades = {2: "#9ecae1", 3: "#4292c6", 4: "#08306b"}
    for ax, side, title, t in zip(axes[0], "od", (TXT["origin"], TXT["dest"]), "ab"):
        for k in (2, 3, 4):
            d = pd.DataFrame([term(f"T5_剔除台风日_距离_dband{b}", f"ab_{side}::{k}") for b in range(5)],
                             columns=["pct", "lo", "hi"])
            line(ax, d, np.arange(5) + (k - 3) * 0.08, shades[k], TXT["bins"][k])
        frame(ax, DIST, TXT["ylab"] if side == "o" else "")
        ax.set_xlabel(TXT["dist"])
        ax.set_title(title)
        tag(ax, t)
    axes[0, 0].legend(frameon=False, loc="lower right")
    x = np.arange(5)
    for ax, side, title, t in zip(axes[1], "od", (TXT["short_o"], TXT["short_d"]), "cd"):     # 日类型：300 km 以内连接
        for g, (lab, col, mk) in enumerate(zip(TXT["days"], (BLUE, ORANGE, GREY), "os^"), start=1):
            line(ax, bins(f"H5_非台风_300km内_日类型_dtype{g}", f"ab_{side}", 4), x + (g - 2) * 0.08, col, lab, mk)
        frame(ax, TXT["rain"][:5], TXT["ylab"] if side == "o" else "")
        ax.set_xlabel(TXT["precip"])
        ax.set_title(title)
        tag(ax, t)
    axes[1, 0].legend(frameon=False, loc="lower left")
    ymin = min(a.get_ylim()[0] for a in axes.flat)
    for a in axes.flat:
        a.set_ylim(ymin, 1)
    fig.tight_layout()
    fig.savefig(OUT / "Fig3_distance.png", dpi=300)
    plt.close(fig)


def fig4():
    fig, axes = plt.subplots(1, 3, figsize=(190 * MM, 68 * MM))
    x = np.arange(6)
    a, b, c = axes
    line(a, bins("T4_剔除台风日_干湿_humid_o1", "ab_o"), x - 0.07, BLUE, TXT["humid"])
    line(a, bins("T4_剔除台风日_干湿_humid_o0", "ab_o"), x + 0.07, ORANGE, TXT["dry"], "s")
    frame(a, TXT["rain_short"])
    a.set_title(TXT["abs"])
    a.legend(frameon=False, loc="lower left")
    line(b, bins("N3r_非台风_相对_干湿_humid_o1", "rb_o"), x - 0.07, BLUE, TXT["humid_s"])
    line(b, bins("N3r_非台风_相对_干湿_humid_o0", "rb_o"), x + 0.07, ORANGE, TXT["dry_s"], "s")
    frame(b, REL, "")
    b.tick_params(axis="x", labelrotation=35)
    b.set_title(TXT["rel"])
    colors = ["#1f4e9c", "#4f9a5b", "#c0504d", "#8064a2"]
    for i, (n, col) in enumerate(zip(TXT["regions"], colors)):
        d = bins(f"N5_非台风_区域_region_o{i + 1}", "ab_o", 4)
        line(c, d, np.arange(len(d)) + (i - 1.5) * 0.07, col, n)
    frame(c, TXT["rain_short"][:5], "")
    c.set_title(TXT["region"])
    c.legend(frameon=False, loc="lower left", ncol=2)
    for ax, t in zip(axes, "abc"):
        tag(ax, t)
    fig.tight_layout()
    fig.savefig(OUT / "Fig4_climate.png", dpi=300)
    plt.close(fig)


def fig5():
    tags = ["F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7"]
    x = np.array([-7, -3, -2, -1, 0, 1, 2, 3, 7])
    m = "N7_非台风_动态含小雨_抽样30%_三向聚类"
    minus = "−" if LANG == "en" else "-"
    fig, axes = plt.subplots(1, 3, figsize=(190 * MM, 66 * MM), sharey=True)
    for ax, v, title, t in zip(axes, ("m25", "m10", "m01"), (TXT["r25"], TXT["r10"], TXT["r01"]), "abc"):
        for side, col, lab, off in (("o", BLUE, TXT["at_o"], -0.12), ("d", ORANGE, TXT["at_d"], 0.12)):
            d = pd.DataFrame([term(m, f"{v}_{tg}_{side}") for tg in tags], columns=["pct", "lo", "hi"])
            line(ax, d, x + off, col, lab, "o" if side == "o" else "s")
        ax.axhline(0, color="0.6", lw=0.6)
        ax.axvline(0, color="0.75", lw=0.6, ls="--")
        ax.axvspan(-7.6, -6.4, color="0.94"); ax.axvspan(6.4, 7.6, color="0.94")
        ax.set_xticks(x, [f"{minus}7\n{TXT['placebo']}", f"{minus}3", f"{minus}2", f"{minus}1", "0", "1", "2", "3",
                          f"7\n{TXT['placebo']}"], fontsize=6.5)
        ax.set_title(title)
        ax.grid(axis="y", color="0.92", lw=0.5)
        tag(ax, t)
    axes[0].set_ylabel(TXT["ylab_dyn"])
    axes[0].legend(frameon=False, loc="lower left")
    fig.supxlabel(TXT["dyn_x"], fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "Fig5_dynamics.png", dpi=300)
    plt.close(fig)


def fig6():
    lb = pd.read_csv(RESULTS / "全国_降雨损失分解.csv", encoding="utf-8-sig", index_col=0)
    ld = pd.read_csv(RESULTS / "全国_降雨损失_距离.csv", encoding="utf-8-sig", index_col=0)
    total = pd.read_csv(RESULTS / "全国_降雨损失区间.csv", encoding="utf-8-sig", index_col=0).loc["动态：计入滞后（主估计）", "合计"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(180 * MM, 66 * MM))
    v = lb.loc[["小雨", "中雨", "≥25 mm"], "日常降雨（计入滞后）"].to_numpy() * TXT["loss_scale"]   # 英文版 ×100 = 百万人次
    a.bar(range(3), v, color=[BLUE, BLUE, GREY], width=0.6)
    for i, (val, sh) in enumerate(zip(v, v / v.sum())):
        a.text(i, val + v.max() * 0.015, TXT["loss_fmt"].format(val) + "\n" + TXT["share"].format(sh),
               ha="center", va="bottom", fontsize=7)
    a.set_xticks(range(3), TXT["loss_bins"])
    a.set_ylabel(TXT["loss_y"])
    a.set_ylim(0, v.max() * 1.25)
    a.set_title(TXT["loss_t"].format(total * TXT["loss_scale"]))     # 合计为同时去掉各类降雨的估计，各类单独去掉之和略小
    b.bar(range(5), ld["损失率"] * 100, color=BLUE, width=0.6)
    for i, (r, s) in enumerate(zip(ld["损失率"] * 100, ld["损失占比"])):
        b.text(i, r + 0.05, TXT["rate_lab"].format(r, s), ha="center", va="bottom", fontsize=7)
    b.set_xticks(range(5), DIST)
    b.set_xlabel(TXT["dist"])
    b.set_ylabel(TXT["rate_y"])
    b.set_ylim(0, ld["损失率"].max() * 100 * 1.35)
    b.set_title(TXT["rate_t"])
    for ax, t in zip((a, b), "ab"):
        tag(ax, t)
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="0.92", lw=0.5)
    fig.tight_layout()
    fig.savefig(OUT / "Fig6_losses.png", dpi=300)
    plt.close(fig)


def fig7():
    fig, axes = plt.subplots(1, 2, figsize=(180 * MM, 70 * MM), sharey=True)
    x = np.arange(6)
    for ax, side, title, t in zip(axes, "od", (TXT["origin"], TXT["dest"]), "ab"):
        line(ax, bins("M1c_OD绝对分档_含7日累计", f"ab_{side}", res=RA), x - 0.1, GREY, TXT["all"], "s", "--")
        line(ax, bins("T2_剔除台风日500km", f"ab_{side}", res=RA), x, "#7fa7d9", TXT["ntc"], "^", ":")
        line(ax, bins("T2_剔除台风日500km", f"ab_{side}"), x + 0.1, BLUE, TXT["evd"])
        frame(ax, TXT["rain"], TXT["ylab"] if side == "o" else "")
        ax.set_title(title)
        tag(ax, t)
    axes[0].legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "Fig7_typhoon.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        f()
        print(LANG, "done", f.__name__)
