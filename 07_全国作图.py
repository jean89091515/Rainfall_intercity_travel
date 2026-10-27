"""根据 results/全国回归结果.csv 绘制全国结果图（系数换算为相对无雨日的百分比变化，竖线为 95% 置信区间）。

主口径：非台风日（起终点 500 km 内均无热带气旋），含前 7 日累计降水控制。图 6 对照全部日。

  全国_图1_剂量响应.png   起点降雨与终点降雨的剂量-响应（OD 层级）
  全国_图2_距离.png       各雨档效应随距离档的变化
  全国_图3_气候适应.png   湿润区与非湿润区：绝对分档 vs 本地分位数分档
  全国_图4_区域.png       按起点四大区域
  全国_图5_动态.png       ≥25 mm 降雨的前导与滞后
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

from config import DIST_LABELS, RAIN_LABELS, REL_LABELS, RESULTS

for _f in ("/System/Library/Fonts/STHeiti Medium.ttc", "/Library/Fonts/Arial Unicode.ttf"):
    if os.path.exists(_f):
        font_manager.fontManager.addfont(_f)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Heiti SC", "Arial Unicode MS", "Source Han Sans", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

R = pd.read_csv(RESULTS / "全国回归结果.csv", encoding="utf-8-sig")
MAIN = {"dose": "T2_剔除台风日500km", "dist": "T5_剔除台风日_距离_dband{}", "abs": "T4_剔除台风日_干湿_humid_o{}",
        "rel": "N3r_非台风_相对_干湿_humid_o{}", "region": "N5_非台风_区域_region_o{}",
        "dyn": "N6_非台风_动态_抽样30%_三向聚类"}
R["pct"] = 100 * (np.exp(R["est"]) - 1)
R["lo"] = 100 * (np.exp(R["est"] - 1.96 * R["se"]) - 1)
R["hi"] = 100 * (np.exp(R["est"] + 1.96 * R["se"]) - 1)


def bins(model: str, var: str) -> pd.DataFrame:
    """取出 i(var) 的各档系数，补上参照档 0。"""
    s = R[(R["model"] == model) & R["term"].str.fullmatch(fr"{var}::\d")].copy()
    s["k"] = s["term"].str.extract(r"::(\d)")[0].astype(int)
    ref = pd.DataFrame({"k": [0], "pct": [0.0], "lo": [0.0], "hi": [0.0]})
    return pd.concat([ref, s[["k", "pct", "lo", "hi"]]]).sort_values("k")


def errline(ax, s, x, label, color, marker="o"):
    ax.errorbar(x, s["pct"], yerr=[s["pct"] - s["lo"], s["hi"] - s["pct"]], fmt=f"{marker}-",
                capsize=3, color=color, label=label, lw=1.5, ms=5)


def finish(ax, labels, ylabel="相对无雨日的流量变化（%）"):
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(range(len(labels)), labels, fontsize=9)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, fontsize=9)


def fig1():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = np.arange(len(RAIN_LABELS))
    errline(ax, bins(MAIN["dose"], "ab_o"), x - 0.06, "起点降雨", "#1f4e9c")
    errline(ax, bins(MAIN["dose"], "ab_d"), x + 0.06, "终点降雨", "#e07b39")
    finish(ax, RAIN_LABELS)
    ax.set_title("非台风日降雨对城际 OD 流量的剂量-响应（26,442 条稳定连接，2023—2025）")
    fig.tight_layout()
    fig.savefig(RESULTS / "全国_图1_剂量响应.png", dpi=200)


def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    cmap = plt.cm.Blues
    for ax, var, title in zip(axes, ("ab_o", "ab_d"), ("起点降雨", "终点降雨")):
        for k in range(2, 6):
            rows = []
            for b in range(5):
                s = bins(MAIN["dist"].format(b), var)
                rows.append(s[s.k == k].assign(b=b))
            s = pd.concat(rows)
            errline(ax, s, s["b"] + (k - 3.5) * 0.06, RAIN_LABELS[k], cmap(0.35 + 0.17 * (k - 2)))
        finish(ax, [f"{d} km" for d in DIST_LABELS])
        ax.set_title(title)
        ax.set_xlabel("OD 距离")
    fig.suptitle("非台风日：各雨档效应随出行距离的变化")
    fig.tight_layout()
    fig.savefig(RESULTS / "全国_图2_距离.png", dpi=200)


def fig3():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, kind, labels in zip(axes, ("绝对", "相对"), (RAIN_LABELS, REL_LABELS)):
        var = "ab_o" if kind == "绝对" else "rb_o"
        x = np.arange(len(labels))
        key = "abs" if kind == "绝对" else "rel"
        errline(ax, bins(MAIN[key].format(1), var), x - 0.06, "起点在湿润区（年降水 ≥800 mm）", "#1f4e9c")
        errline(ax, bins(MAIN[key].format(0), var), x + 0.06, "起点在非湿润区（<800 mm）", "#c0504d", "s")
        finish(ax, labels)
        ax.set_title("国标绝对分档" if kind == "绝对" else "本地分位数分档")
    fig.suptitle("非台风日：同样的雨量，非湿润区反应更强（起点降雨）")
    fig.tight_layout()
    fig.savefig(RESULTS / "全国_图3_气候适应.png", dpi=200)


def fig4():
    names = {1: "东部", 2: "中部", 3: "西部", 4: "东北"}
    colors = {1: "#1f4e9c", 2: "#4f9a5b", 3: "#c0504d", 4: "#8064a2"}
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = np.arange(len(RAIN_LABELS))
    for i, (g, n) in enumerate(names.items()):
        m = MAIN["region"].format(g)
        if (R["model"] == m).any():
            errline(ax, bins(m, "ab_o"), x + (i - 1.5) * 0.07, n, colors[g])
    finish(ax, RAIN_LABELS)
    ax.set_title("非台风日起点降雨效应：按起点所在区域")
    fig.tight_layout()
    fig.savefig(RESULTS / "全国_图4_区域.png", dpi=200)


def fig5():
    """动态（非台风日）：OD×年月 FE，30% 连接抽样，起点+终点+日期三向聚类；±7 天为安慰剂。"""
    tags = ["F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7"]
    x = np.array([-7, -3, -2, -1, 0, 1, 2, 3, 7])
    m = R[R["model"] == MAIN["dyn"]]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for end, lab, col, off in (("o", "起点 ≥25 mm", "#1f4e9c", -0.1), ("d", "终点 ≥25 mm", "#e07b39", 0.1)):
        s = m.set_index("term").reindex([f"m25_{t}_{end}" for t in tags])
        errline(ax, s, x + off, lab, col)
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(0, color="grey", lw=0.6, ls="--")
    # 横轴是“流量日相对降雨日”：前导项 F1（次日才下雨）画在 −1，滞后项 L1（前一天下过雨）画在 +1
    ax.set_xticks(x, ["雨前7天\n(安慰剂)", "雨前3天", "雨前2天", "雨前1天", "雨当天", "雨后1天", "雨后2天", "雨后3天",
                      "雨后7天\n(安慰剂)"], fontsize=8.5)
    ax.set_xlabel("流量日相对降雨日")
    ax.set_ylabel("流量变化（%）")
    ax.legend(frameon=False)
    ax.set_title("非台风日 ≥25 mm 降雨的动态影响（三向聚类 95% 置信区间）")
    fig.tight_layout()
    fig.savefig(RESULTS / "全国_图5_动态.png", dpi=200)


def fig6():
    """台风：全部日 vs 剔除任一端台风日（500 km），均含前 7 日累计降水控制。"""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    x = np.arange(len(RAIN_LABELS))
    for ax, var, title in zip(axes, ("ab_o", "ab_d"), ("起点降雨", "终点降雨")):
        errline(ax, bins("M1c_OD绝对分档_含7日累计", var), x - 0.06, "全部日", "#9aa5b1", "s")
        errline(ax, bins("T2_剔除台风日500km", var), x + 0.06, "剔除台风日", "#1f4e9c")
        finish(ax, RAIN_LABELS)
        ax.set_title(title)
    fig.suptitle("剔除台风影响日后，极端降雨的效应大幅缩小")
    fig.tight_layout()
    fig.savefig(RESULTS / "全国_图6_台风.png", dpi=200)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6):
        try:
            f()
        except Exception as e:          # 某个模型尚未跑完时跳过对应的图
            print(f"{f.__name__} 跳过：{e}")
    print("图已写入", RESULTS)
