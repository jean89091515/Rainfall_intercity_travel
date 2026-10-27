"""构建分析用的四张表（降水数据未到位时只生成流动部分）：

  units.parquet       单元属性：代码、名称、省、四大区域、几何中心经纬度、降水气候态与干湿分区
  edges.parquet       主样本内出现过的全部有向连接：距离、距离档、出现比例、是否稳定核心
  od_panel.parquet    稳定核心连接 × 主样本日期的流量（Date, o, d, flow）
  city_flow.parquet   单元逐日总流出、总流入（只汇总稳定核心连接，避免截断带来的口径变化）
  city_rain.parquet   单元逐日降水与绝对/相对分档（需先运行 02 或 02b）
"""
from typing import Optional

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from config import (CITY_SHP, CORE_SHARE, DIMNET_PARQUET, DIST_BINS, DIST_LABELS,
                    MAIN_END, MAIN_START, PROC, RAIN_BINS, RAIN_LABELS, REL_LABELS,
                    REL_QUANTILES, UNIT_LOOKUP, WET_DAY_MM)

REGION4 = {**dict.fromkeys([11, 12, 13, 31, 32, 33, 35, 37, 44, 46], "东部"),
           **dict.fromkeys([14, 34, 36, 41, 42, 43], "中部"),
           **dict.fromkeys([15, 45, 50, 51, 52, 53, 54, 61, 62, 63, 64, 65], "西部"),
           **dict.fromkeys([21, 22, 23], "东北")}
# 中国干湿分区的经典年降水界线；800 mm 等降水量线大致与秦岭—淮河一致
DRYWET_BINS = [0, 200, 400, 800, np.inf]
DRYWET_LABELS = ["干旱区", "半干旱区", "半湿润区", "湿润区"]


def build_units() -> pd.DataFrame:
    lk = pd.read_excel(UNIT_LOOKUP)
    lk.columns = ["name", "code", "en"]
    city = gpd.read_file(CITY_SHP)
    city["code"] = city["市代码"].astype(int)
    city = city[city["code"].isin(lk["code"])]
    # 在等积投影里取几何中心再转回经纬度；以后可换成政府驻地坐标
    cen = city.to_crs("+proj=aea +lat_1=25 +lat_2=47 +lon_0=105 +datum=WGS84").centroid.to_crs(4326)
    u = lk.merge(pd.DataFrame({"code": city["code"].values, "lon": cen.x.values, "lat": cen.y.values}),
                 on="code")
    u["prov"] = u["code"] // 10000
    u["region4"] = u["prov"].map(REGION4)
    clim = PROC / "city_rain_climate.csv"
    if clim.exists():
        u = u.merge(pd.read_csv(clim), on="code", how="left")
        u["drywet"] = pd.cut(u["annual_mm"], DRYWET_BINS, labels=DRYWET_LABELS)
    return u


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * np.arcsin(np.sqrt(a))


def load_flows(units: pd.DataFrame) -> pd.DataFrame:
    """全表 1.02 亿行；只读主样本年份，城市名与日期按字典编码读入，内存约 1 GB。"""
    lo, hi = MAIN_START.replace("-", ""), MAIN_END.replace("-", "")     # 文件里 Date 为 YYYYMMDD 字符串
    t = pq.read_table(DIMNET_PARQUET, filters=[("Date", ">=", lo), ("Date", "<=", hi)],
                      read_dictionary=["Date", "Origin", "Destination"])
    f = t.to_pandas()
    f["Date"] = f["Date"].cat.rename_categories(pd.to_datetime(f["Date"].cat.categories, format="%Y%m%d"))
    f["Date"] = f["Date"].astype("datetime64[ns]")
    code = dict(zip(units["name"], units["code"]))
    for end, col in (("o", "Origin"), ("d", "Destination")):
        cats = f[col].cat.categories
        bad = [c for c in cats if c not in code]
        if bad:
            print(f"警告：{col} 有 {len(bad)} 个名称未匹配 Unit_Lookup，例如 {bad[:5]}")
        lut = np.array([code.get(c, -1) for c in cats], dtype="int32")
        f[end] = lut[f[col].cat.codes.to_numpy()]
    f = f[(f["o"] > 0) & (f["d"] > 0)]
    return f[["Date", "o", "d", "Flow"]].rename(columns={"Flow": "flow"}).reset_index(drop=True)


def build_edges(f: pd.DataFrame, units: pd.DataFrame) -> pd.DataFrame:
    ndays = f["Date"].nunique()
    e = f.groupby(["o", "d"]).agg(ndays=("flow", "size"), mean_flow=("flow", "mean")).reset_index()
    e["share"] = e["ndays"] / ndays
    e["core"] = e["share"] >= CORE_SHARE
    xy = units.set_index("code")[["lat", "lon"]]
    o, d = xy.loc[e["o"]].to_numpy(), xy.loc[e["d"]].to_numpy()
    e["dist_km"] = haversine_km(o[:, 0], o[:, 1], d[:, 0], d[:, 1])
    e["dist_band"] = pd.cut(e["dist_km"], DIST_BINS, labels=DIST_LABELS, right=False)
    print(f"主样本 {ndays} 天；出现过的有向连接 {len(e):,} 条，其中稳定核心 {e['core'].sum():,} 条，"
          f"占主样本总流量 {e.loc[e.core, 'mean_flow'].mul(e.loc[e.core, 'ndays']).sum() / f['flow'].sum():.1%}")
    return e


def build_city_rain(units: pd.DataFrame) -> Optional[pd.DataFrame]:
    path = PROC / "city_rain_daily.parquet"
    if not path.exists():
        print("尚无降水数据（先运行 02 或 02b），跳过 city_rain")
        return None
    r = pd.read_parquet(path)
    r["abs_bin"] = pd.cut(r["rain_mm"], RAIN_BINS, labels=RAIN_LABELS, right=False)
    qcols = [f"p{int(x * 100)}" for x in REL_QUANTILES]
    if not set(qcols) <= set(units.columns):
        print("缺少降水气候态（相对分位数），只生成绝对分档")
        return r
    edges = units.set_index("code")[qcols].reindex(r["code"]).to_numpy()
    wet = r["rain_mm"].to_numpy() >= WET_DAY_MM
    level = (r["rain_mm"].to_numpy()[:, None] >= edges).sum(axis=1)     # 0-4：超过了几个分位数
    r["rel_bin"] = pd.Categorical(np.where(wet, np.array(REL_LABELS[1:])[level], REL_LABELS[0]),
                                  categories=REL_LABELS, ordered=True)
    return r


if __name__ == "__main__":
    units = build_units()
    units.to_parquet(PROC / "units.parquet", index=False)

    flows = load_flows(units)
    edges = build_edges(flows, units)
    edges.to_parquet(PROC / "edges.parquet", index=False)

    core = flows.merge(edges.loc[edges.core, ["o", "d"]], on=["o", "d"])
    core.to_parquet(PROC / "od_panel.parquet", index=False)

    out = core.groupby(["o", "Date"])["flow"].sum().rename("outflow")
    inn = core.groupby(["d", "Date"])["flow"].sum().rename("inflow")
    out.index.names = inn.index.names = ["code", "Date"]
    pd.concat([out, inn], axis=1).reset_index().to_parquet(PROC / "city_flow.parquet", index=False)

    rain = build_city_rain(units)
    if rain is not None:
        rain.to_parquet(PROC / "city_rain.parquet", index=False)
    print("完成:", PROC)
