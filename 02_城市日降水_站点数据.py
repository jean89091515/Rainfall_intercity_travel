"""把 ERA5-Land 站点降水（地联社整理，1950-2026，北京时间日）汇总为 DIMNet 366 个单元的逐日降水和气候态。

输入：STATION_RAIN_DIR 下按省/市分文件夹的“站名_站号.csv”，列为 Date_BJT, total_precipitation(mm/day), Remark；
     Remark 前若干行是“键: 值”元信息（stationid、Lat、Lon、县级码、地级、省级等）。
输出：
  processed/station_meta.csv          站点元信息（含所属 DIMNet 单元）
  processed/city_rain_daily.parquet   单元逐日降水（mm），2019-12-01 起，供主分析和前导/滞后项
  processed/city_rain_climate.csv     单元降水气候态（1991-2020）：年降水、湿日分位数、暴雨日数
"""
import csv

import geopandas as gpd
import numpy as np
import pandas as pd

from config import (CITY_SHP, CLIM_END, CLIM_START, PROC, REL_QUANTILES, STATION_RAIN_DIR,
                    UNIT_LOOKUP, WET_DAY_MM)

KEEP_FROM = "1991-01-01"          # 只保留气候态基准期以来的记录，控制内存
PANEL_FROM = "2019-12-01"


def read_station(path):
    """返回 (元信息 dict, 逐日 DataFrame[date, tp])。"""
    meta = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = csv.reader(fh)
        next(rows)
        for i, row in enumerate(rows):
            if i > 40 or len(row) < 3 or not row[2]:
                break
            k, _, v = row[2].partition(":")
            meta[k.strip()] = v.strip()
    d = pd.read_csv(path, encoding="utf-8-sig", usecols=[0, 1], header=0, names=["date", "tp"],
                    dtype={"tp": "float32"})
    d = d[d["date"] >= KEEP_FROM]
    d["date"] = pd.to_datetime(d["date"], format="%Y-%m-%d")
    sid = meta.get("stationid") or path.stem.rsplit("_", 1)[-1]
    meta = {"stationid": int(float(sid)), "name": meta.get("name", path.stem.rsplit("_", 1)[0]),
            "lat": float(meta["Lat"]), "lon": float(meta["Lon"]), "altitude": meta.get("altitude"),
            "county_code": meta.get("县级码"), "prefecture": meta.get("地级"),
            "province": meta.get("省级"), "day_def": meta.get("时间"), "file": str(path)}
    d["stationid"] = meta["stationid"]
    return meta, d


def station_to_unit(stations: pd.DataFrame) -> pd.DataFrame:
    units = pd.read_excel(UNIT_LOOKUP)
    units.columns = ["unit_name", "code", "en"]
    city = gpd.read_file(CITY_SHP)[["市代码", "geometry"]]
    city["code"] = city["市代码"].astype(int)
    city = city[city["code"].isin(units["code"])].to_crs(3857)

    pts = gpd.GeoDataFrame(stations, geometry=gpd.points_from_xy(stations.lon, stations.lat),
                           crs=4326).to_crs(3857)
    inside = gpd.sjoin(pts, city[["code", "geometry"]], predicate="within", how="left")
    # 海岸、边界附近落在面外的站点，归到最近的单元（10 km 以内）
    out = inside[inside["code"].isna()].drop(columns=["code", "index_right"])
    near = gpd.sjoin_nearest(out, city[["code", "geometry"]], max_distance=10_000, how="left")
    m = pd.concat([inside[inside["code"].notna()], near])[["stationid", "code"]].dropna()
    m["code"] = m["code"].astype(int)
    m["how"] = "within"

    # 没有站点的单元：用离单元几何中心最近的 2 个站点补位（只在站点覆盖全国时启用，否则会把远处站点硬塞给它们）
    covered_prov = set(m["code"] // 10000)
    empty = city[~city["code"].isin(m["code"]) & (city["code"] // 10000).isin(covered_prov)].copy()
    if len(empty):
        cent = empty.set_geometry(empty.geometry.centroid)
        for _, r in cent.iterrows():
            d = pts.distance(r.geometry).nsmallest(2)
            m = pd.concat([m, pd.DataFrame({"stationid": stations.loc[d.index, "stationid"].values,
                                            "code": r["code"], "how": "nearest",
                                            "fill_km": (d.values / 1000).round(1)})])
        print(f"{len(empty)} 个单元内无有效站点，已用最近 2 站补位（距几何中心 km）:")
        print(m[m["how"] == "nearest"].groupby("code")["fill_km"].max().to_string())
    return m.merge(units[["code", "unit_name"]], on="code")


def climate(daily: pd.DataFrame) -> pd.DataFrame:
    base = daily[(daily["date"] >= CLIM_START) & (daily["date"] <= CLIM_END)]
    nyear = base["date"].dt.year.nunique()
    wet = base[base["rain_mm"] >= WET_DAY_MM]
    q = wet.groupby("code")["rain_mm"].quantile(REL_QUANTILES).unstack()
    q.columns = [f"p{int(x * 100)}" for x in REL_QUANTILES]
    g = base.groupby("code")["rain_mm"]
    return q.assign(
        annual_mm=g.sum() / nyear,
        wet_days=(base["rain_mm"] >= WET_DAY_MM).groupby(base["code"]).sum() / nyear,
        days_ge50=(base["rain_mm"] >= 50).groupby(base["code"]).sum() / nyear,
    ).reset_index()


if __name__ == "__main__":
    # 移动硬盘（exFAT）上 macOS 会为每个文件生成“._”开头的影子文件，必须跳过
    files = sorted(f for f in STATION_RAIN_DIR.rglob("*_*.csv")
                   if not any(part.startswith(".") for part in f.relative_to(STATION_RAIN_DIR).parts))
    if not files:
        raise SystemExit(f"未找到站点降水文件：{STATION_RAIN_DIR}")
    metas, parts = [], []
    for i, f in enumerate(files, 1):
        m, d = read_station(f)
        metas.append(m)
        parts.append(d)
        if i % 200 == 0:
            print(f"  已读 {i}/{len(files)} 站")
    stations = pd.DataFrame(metas)
    raw = pd.concat(parts, ignore_index=True).drop_duplicates(["stationid", "date"])
    raw.loc[raw["tp"] < 0, "tp"] = 0          # 去累计后偶见极小负值
    print(f"{len(stations)} 站，{len(raw):,} 条日记录，{raw['date'].min().date()} 至 {raw['date'].max().date()}；"
          f"日界线：{stations['day_def'].unique()}")

    # 质控：站点坐标落在 ERA5-Land 海洋格点时，提供方把缺测填成了 0，整条序列全为 0（如深圳、舟山、
    # 金山、汉沽等 36 站）。这些站不能当作“无雨”参与平均，剔除后所在单元改由其他站或最近有效站代表。
    total = raw.groupby("stationid")["tp"].sum()
    stations["valid"] = stations["stationid"].map(total).gt(0)
    bad = stations.loc[~stations["valid"], "name"].tolist()
    print(f"质控剔除全零站 {len(bad)} 个：{'、'.join(bad)}")
    raw = raw[raw["stationid"].isin(stations.loc[stations["valid"], "stationid"])]

    smap = station_to_unit(stations.loc[stations["valid"]].drop(columns="file").reset_index(drop=True))
    stations.merge(smap, on="stationid", how="left").to_csv(PROC / "station_meta.csv", index=False)
    per = smap.groupby("code").size()
    print(f"覆盖 {per.size} 个单元；每单元站点数 中位 {per.median():.0f}，最少 {per.min()}，最多 {per.max()}")

    # 站点等权平均得到单元降水。缺失值保持缺失，不补 0
    daily = (raw.merge(smap[["stationid", "code"]], on="stationid")
                .groupby(["code", "date"], as_index=False)["tp"].mean()
                .rename(columns={"tp": "rain_mm"}))
    climate(daily).to_csv(PROC / "city_rain_climate.csv", index=False)
    daily[daily["date"] >= PANEL_FROM].to_parquet(PROC / "city_rain_daily.parquet", index=False)
    print("完成:", PROC)
