"""用 IBTrACS 西北太平洋路径标识 2023-2025 年各单元的“台风影响日”。

数据：NOAA IBTrACS v04r01（ibtracs.WP.list.v04r01.csv，公共领域），3 小时间隔，时间为 UTC。
引用：Knapp et al. 2010, BAMS 91: 363-376；Gahtan et al. 2024, IBTrACS v04r01, NOAA NCEI。
2025 年多数台风仍为 US-PROVISIONAL（尚无中国气象局数值），位置已足够判断距离，因此一并纳入。

定义（按北京时间日）：当天任一时次热带气旋中心（含减弱后的残余低压）与单元几何中心的大圆距离
  tc500 ≤ 500 km：常用于把降水归因于热带气旋的半径（主口径；能覆盖 2023 年杜苏芮残余与京津冀 23·7 暴雨）
  tc300 ≤ 300 km：大风直接影响半径（稳健性）
输出：processed/city_typhoon.parquet（code, date, tc300, tc500, min_km, storms）
"""
import numpy as np
import pandas as pd

from config import DATA, MAIN_END, MAIN_START, PROC

TRACKS = DATA / "台风" / "ibtracs.WP.list.v04r01.csv"
KEEP_TYPES = ["main", "US-PROVISIONAL", "PROVISIONAL"]     # 不含 spur（分支重复路径）


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * np.arcsin(np.sqrt(a))


if __name__ == "__main__":
    t = pd.read_csv(TRACKS, skiprows=[1], low_memory=False, na_values=[" ", ""],
                    usecols=["SID", "SEASON", "NAME", "ISO_TIME", "NATURE", "LAT", "LON", "TRACK_TYPE"])
    t = t[t["SEASON"].between(2022, 2026) & t["TRACK_TYPE"].isin(KEEP_TYPES)].dropna(subset=["LAT", "LON"])
    t = t.drop_duplicates(["SID", "ISO_TIME"])
    t["date"] = (pd.to_datetime(t["ISO_TIME"]) + pd.Timedelta(hours=8)).dt.normalize()     # UTC → 北京时间日
    t = t[(t["date"] >= MAIN_START) & (t["date"] <= MAIN_END)]
    print(f"2023-2025 年路径点 {len(t):,} 个，{t['SID'].nunique()} 个热带气旋")

    u = pd.read_parquet(PROC / "units.parquet")[["code", "name", "lat", "lon"]]
    # 路径点 × 单元 的距离矩阵（约 5000 × 366）
    d = haversine_km(t["LAT"].to_numpy()[:, None], t["LON"].to_numpy()[:, None],
                     u["lat"].to_numpy()[None, :], u["lon"].to_numpy()[None, :])
    near = np.argwhere(d <= 500)
    hit = pd.DataFrame({"code": u["code"].to_numpy()[near[:, 1]],
                        "date": t["date"].to_numpy()[near[:, 0]],
                        "km": d[near[:, 0], near[:, 1]],
                        "storm": (t["NAME"] + "_" + t["SEASON"].astype(str)).to_numpy()[near[:, 0]]})
    out = hit.groupby(["code", "date"]).agg(min_km=("km", "min"),
                                            storms=("storm", lambda s: ",".join(sorted(set(s))))).reset_index()
    out["tc500"] = np.int8(1)
    out["tc300"] = (out["min_km"] <= 300).astype("int8")
    out.to_parquet(PROC / "city_typhoon.parquet", index=False)

    n_cd = len(u) * pd.date_range(MAIN_START, MAIN_END).size
    print(f"台风影响城市-日：500 km 内 {len(out):,}（{len(out) / n_cd:.2%}），300 km 内 {out['tc300'].sum():,}")
    print("受影响城市数：", out["code"].nunique(), "；按年：",
          out.groupby(out["date"].dt.year).size().to_dict())
    print("影响城市-日最多的台风：")
    print(hit.groupby("storm")[["code", "date"]].apply(lambda x: len(x.drop_duplicates())).nlargest(10).to_string())
