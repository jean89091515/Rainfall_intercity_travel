"""把 NOAA CPC 全球逐日观测格点（0.5°，由气象站观测插值）汇总为 366 个单元的面平均逐日降水与气温。

免账号，替代需要 GEE 认证的 02b，用于：
  1. 气温控制：日最高、最低气温，日均取两者平均；
  2. 降水稳健性：CPC 降水由雨量计插值而来，独立于 ERA5-Land。
数据：NOAA PSL 的 CPC Global Unified Gauge-Based Analysis of Daily Precipitation 与 CPC Global Daily Temperature，
每年每个变量一个 netCDF（约 65-82 MB），首次运行自动下载 2022-2025 年共 12 个文件（约 0.9 GB）到 CPC_DIR。
引用 Chen et al. (2008, JGR) 与 Xie et al. (2007, JHM)，并致谢 "CPC data provided by the NOAA PSL, Boulder, Colorado, USA"。

注意：CPC 的日界线按各国报告惯例定义，不是北京时间 00-24 时。脚本最后与 02 的站点降水（北京时间日）比较 CPC 平移
-1/0/+1 天的相关，回归时按相关最高的平移对齐。

输出：processed/city_cpc_daily.parquet  code, date, rain_cpc_mm, tmax_c, tmin_c, tmean_c（2022-12-24 至 2025-12-31）
"""
import shutil
import ssl
import urllib.request

import certifi
import geopandas as gpd
import netCDF4
import numpy as np
import pandas as pd
from shapely.geometry import box

from config import CITY_SHP, CPC_DIR, PROC, UNIT_LOOKUP, WET_DAY_MM

BASE = "https://downloads.psl.noaa.gov/Datasets"
VARS = {"precip": "cpc_global_precip", "tmax": "cpc_global_temp", "tmin": "cpc_global_temp"}
YEARS = range(2022, 2026)
START, END = "2022-12-24", "2025-12-31"    # 比 7 日累计所需多留一天，便于按对齐结果平移
HALF = 0.25                                # 半个格距（度）
EQUAL_AREA = "+proj=aea +lat_1=25 +lat_2=47 +lon_0=105 +datum=WGS84"   # 中国 Albers 等积投影


def download():
    """缺哪个下哪个；先写 .part 再改名，中断后重跑不会留下半截文件。"""
    CPC_DIR.mkdir(exist_ok=True)
    ctx = ssl.create_default_context(cafile=certifi.where())   # python.org 版 Python 不带系统根证书
    for var, folder in VARS.items():
        for y in YEARS:
            f = CPC_DIR / f"{var}.{y}.nc"
            if not f.exists():
                print("下载", f.name)
                with urllib.request.urlopen(f"{BASE}/{folder}/{f.name}", context=ctx) as r, \
                        open(f.with_suffix(".part"), "wb") as fh:
                    shutil.copyfileobj(r, fh)
                f.with_suffix(".part").rename(f)


def load_units():
    units = pd.read_excel(UNIT_LOOKUP)
    units.columns = ["name", "code", "en"]
    city = gpd.read_file(CITY_SHP)
    city["code"] = city["市代码"].astype(int)
    city = city[city["code"].isin(units["code"])][["code", "geometry"]].reset_index(drop=True)
    city["geometry"] = city.geometry.simplify(0.005)
    return city


def read_box(var, y, bounds):
    """读一年一个变量，裁到单元外包框外扩 1°。返回 (日期, 纬度, 经度, 数组[日, 纬, 经])，缺测为 NaN。"""
    x0, y0, x1, y1 = bounds
    with netCDF4.Dataset(CPC_DIR / f"{var}.{y}.nc") as ds:
        lat, lon = np.asarray(ds["lat"][:]), np.asarray(ds["lon"][:])
        i = np.where((lat >= y0 - 1) & (lat <= y1 + 1))[0]
        j = np.where((lon >= x0 - 1) & (lon <= x1 + 1))[0]
        ri, rj = slice(i.min(), i.max() + 1), slice(j.min(), j.max() + 1)
        t = ds["time"]
        dates = pd.to_datetime(netCDF4.num2date(t[:], t.units, only_use_cftime_datetimes=False)).normalize()
        arr = np.ma.filled(ds[var][:, ri, rj].astype("float32"), np.nan)
    return dates, lat[ri], lon[rj], arr


def area_weights(city, lat, lon):
    """单元 × 格点的相交面积（km²），格点按 lat 外层、lon 内层展平，与 arr.reshape(日, -1) 一致。"""
    cells = gpd.GeoDataFrame({"cell": np.arange(lat.size * lon.size)}, crs=4326,
                             geometry=[box(x - HALF, y - HALF, x + HALF, y + HALF) for y in lat for x in lon])
    ov = gpd.overlay(city.to_crs(EQUAL_AREA), cells.to_crs(EQUAL_AREA), how="intersection")
    row = ov["code"].map(pd.Series(city.index, index=city["code"]))
    w = np.zeros((len(city), len(cells)))
    np.add.at(w, (row.to_numpy(), ov["cell"].to_numpy()), ov.area.to_numpy() / 1e6)
    return w


def nearest_if_empty(w, arr, city, lat, lon):
    """只保留有值格点的权重；单元内全是无值格点（海岛、沿海小单元）时，改用离单元最近的有值格点。"""
    has = ~np.isnan(arr.reshape(len(arr), -1)).all(axis=0)
    w = w * has
    empty = np.where(w.sum(axis=1) == 0)[0]
    if len(empty):
        glat, glon = np.repeat(lat, lon.size)[has], np.tile(lon, lat.size)[has]
        pts = city.geometry.iloc[empty].representative_point()
        for r, p in zip(empty, pts):
            k = np.argmin((glat - p.y) ** 2 + ((glon - p.x) * np.cos(np.radians(p.y))) ** 2)
            w[r, np.flatnonzero(has)[k]] = 1.0
        print(f"  {len(empty)} 个单元没有覆盖有值格点，用最近格点：", city["code"].iloc[empty].tolist())
    return w


def city_mean(arr, w):
    """面积加权平均；某天个别格点缺测时按其余格点的权重重新归一。"""
    x = arr.reshape(len(arr), -1)
    num = np.nan_to_num(x) @ w.T
    den = (~np.isnan(x)).astype("float64") @ w.T
    with np.errstate(invalid="ignore", divide="ignore"):
        return num / den


def build(city):
    out = {}
    for var in VARS:
        parts, w = [], None
        for y in YEARS:
            dates, lat, lon, arr = read_box(var, y, city.total_bounds)
            if w is None:   # 各年格点与陆地掩膜相同，权重每个变量算一次
                print(f"{var}：格点 {lat.size}×{lon.size}，计算与单元的相交面积")
                grid = (lat, lon)
                w = nearest_if_empty(area_weights(city, lat, lon), arr, city, lat, lon)
            assert np.array_equal(grid[0], lat) and np.array_equal(grid[1], lon), f"{var}.{y} 格点与前一年不同"
            parts.append(pd.DataFrame(city_mean(arr, w), index=dates, columns=city["code"]))
        out[var] = pd.concat(parts).stack()
    df = pd.concat(out, axis=1).rename_axis(["date", "code"]).reset_index()
    df = df.rename(columns={"precip": "rain_cpc_mm", "tmax": "tmax_c", "tmin": "tmin_c"})
    df["tmean_c"] = (df["tmax_c"] + df["tmin_c"]) / 2
    return df[df["date"].between(START, END)].sort_values(["code", "date"]).reset_index(drop=True)


def check_alignment(df):
    """与 02 的北京时间日站点降水（ERA5-Land）比：CPC 平移几天相关最高，以及两者的雨量与湿日频率差异。"""
    path = PROC / "city_rain_daily.parquet"
    if not path.exists():
        print("没有 city_rain_daily.parquet（先运行 02），跳过对齐检查")
        return
    st = pd.read_parquet(path, columns=["code", "date", "rain_mm"])
    cpc = df.pivot(index="date", columns="code", values="rain_cpc_mm")
    era = st.pivot(index="date", columns="code", values="rain_mm").reindex(index=cpc.index, columns=cpc.columns)
    for k in (-1, 0, 1):
        a, b = np.log1p(era.to_numpy()), np.log1p(cpc.shift(-k).to_numpy())
        ok = ~np.isnan(a) & ~np.isnan(b)
        print(f"CPC 第 t{k:+d} 天 vs 北京时间第 t 天：log(1+雨量) 相关 {np.corrcoef(a[ok], b[ok])[0, 1]:.3f}")
    print(f"日均雨量 ERA5-Land 站点 {np.nanmean(era):.2f} mm，CPC {np.nanmean(cpc):.2f} mm；"
          f"湿日（≥{WET_DAY_MM} mm）占比 ERA5-Land {np.nanmean(era >= WET_DAY_MM):.1%}，CPC {np.nanmean(cpc >= WET_DAY_MM):.1%}")


if __name__ == "__main__":
    download()
    city = load_units()
    df = build(city)
    df.to_parquet(PROC / "city_cpc_daily.parquet", index=False)
    print(f"city_cpc_daily.parquet：{df['code'].nunique()} 个单元，{df['date'].min():%Y-%m-%d} 至 {df['date'].max():%Y-%m-%d}，"
          f"{len(df):,} 行；缺测占比", df[["rain_cpc_mm", "tmax_c", "tmin_c"]].isna().mean().round(4).to_dict())
    check_alignment(df)
