"""用 Google Earth Engine 按北京时间自然日计算 366 个单元的面平均降水与气温，供气温控制和降水稳健性检验。

两套数据，均为单元面平均、北京时间 00-24 时：
  1. ERA5-Land 小时数据（ECMWF/ERA5_LAND/HOURLY）：日降水、06-22 时白天降水、日均/最高/最低气温；
  2. GPM IMERG V07 半小时数据（NASA/GPM_L3/IMERG_V07）：日降水。卫星与雨量计融合，独立于 ERA5，
     用来检验 ERA5-Land 小雨偏多、极端偏少的问题。2025-09-30 以后只有临时版（provisional），imerg_perm 记录正式版的半小时数。

时段 2022-12-25 至 2025-12-31：主样本从 2023-01-01 开始，前 7 天用于 7 日累计降水。

用法（先按 README 完成 GEE 认证，并接上移动硬盘）：
  python3 02b_城市日降水气温_GEE.py test [YYYY-MM-DD]   交互试算一天（默认 2023-07-31），并核对 ERA5-Land 的计时约定
  python3 02b_城市日降水气温_GEE.py export              按年提交 4 个导出任务（CSV 到 Google Drive 的 GEE_FOLDER）
  python3 02b_城市日降水气温_GEE.py status              查看导出任务进度
导出完成后把 Drive 里的 CSV 下载到 config.GEE_DIR。
Cloud 项目用 `earthengine set_project` 设的默认值，或环境变量 GEE_PROJECT。
"""
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)   # google-auth 对 Python 3.9 的停更提示

import ee
import geopandas as gpd
import pandas as pd

from config import CITY_SHP, UNIT_LOOKUP

START, END = "2022-12-25", "2025-12-31"
TZ = "Asia/Shanghai"
GEE_FOLDER = "rain_mobility"
SCALE = 11132           # 两套数据都是 0.1° 网格
# ERA5-Land 累积量按时段末计时：时间戳 T 的 total_precipitation_hourly 是 (T-1h, T] 的降水，
# 所以北京时间 00-24 时取时间戳 01:00 至次日 00:00。`test` 会核对这一约定，不对时改成 0。
ERA5_ACC_LAG_H = 1
COLUMNS = ["code", "date", "rain_era5_mm", "rain_era5_day_mm", "rain_imerg_mm",
           "tmean_c", "tmax_c", "tmin_c", "era5_n", "imerg_n", "imerg_perm"]

ee.Initialize(project=os.environ.get("GEE_PROJECT"))   # 未设环境变量时用默认项目
era5 = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")
imerg = ee.ImageCollection("NASA/GPM_L3/IMERG_V07")


def unit_fc():
    """366 个单元的简化边界（约 1 km 容差，对 0.1° 面平均影响可忽略）。"""
    units = pd.read_excel(UNIT_LOOKUP)
    units.columns = ["name", "code", "en"]
    city = gpd.read_file(CITY_SHP)
    city["code"] = city["市代码"].astype(int)
    city = city[city["code"].isin(units["code"])][["code", "geometry"]]
    city["geometry"] = city.geometry.simplify(0.01)
    return ee.FeatureCollection(json.loads(city.to_json()))


def or_masked(coll, img):
    """当天有数据就返回 img，否则返回全掩膜图像（导出为空值），以免缺一天让整年的任务失败。"""
    return ee.Image(ee.Algorithms.If(coll.size().gt(0), img, ee.Image.constant(0).updateMask(0)))


def day_stats(d, fc):
    """北京时间 d 当日（ee.Date，北京时间零点）各单元的面平均降水（mm）与气温（°C）。"""
    acc = era5.filterDate(d.advance(ERA5_ACC_LAG_H, "hour"), d.advance(24 + ERA5_ACC_LAG_H, "hour")) \
              .select("total_precipitation_hourly")
    acc_day = era5.filterDate(d.advance(6 + ERA5_ACC_LAG_H, "hour"), d.advance(22 + ERA5_ACC_LAG_H, "hour")) \
                  .select("total_precipitation_hourly")
    temp = era5.filterDate(d, d.advance(1, "day")).select("temperature_2m")   # 瞬时值，取 00-23 时
    hh = imerg.filterDate(d, d.advance(1, "day")).select("precipitation")      # mm/h，时间戳为半小时起点
    img = ee.Image.cat(
        or_masked(acc, acc.sum().multiply(1000)).rename("rain_era5_mm"),
        or_masked(acc_day, acc_day.sum().multiply(1000)).rename("rain_era5_day_mm"),
        or_masked(hh, hh.sum().multiply(0.5)).rename("rain_imerg_mm"),
        or_masked(temp, temp.mean().subtract(273.15)).rename("tmean_c"),
        or_masked(temp, temp.max().subtract(273.15)).rename("tmax_c"),
        or_masked(temp, temp.min().subtract(273.15)).rename("tmin_c"),
    )
    props = {"date": d.format("YYYY-MM-dd", TZ), "era5_n": acc.size(), "imerg_n": hh.size(),
             "imerg_perm": hh.filter(ee.Filter.eq("status", "permanent")).size()}
    return img.reduceRegions(collection=fc, reducer=ee.Reducer.mean(), scale=SCALE, tileScale=2) \
              .map(lambda f: f.set(props).setGeometry(None))


def test(day, fc):
    """交互试算一天：打印降水最多的 10 个单元，再用当天雨最大的单元核对 ERA5-Land 的计时约定。"""
    rows = day_stats(ee.Date(day, TZ), fc).getInfo()["features"]
    df = pd.DataFrame([r["properties"] for r in rows]).reindex(columns=COLUMNS)
    print(f"{day}：{len(df)} 个单元，ERA5 小时数 {df.era5_n.iloc[0]}，"
          f"IMERG 半小时数 {df.imerg_n.iloc[0]}（正式版 {df.imerg_perm.iloc[0]}）")
    print(df.sort_values("rain_era5_mm", ascending=False).head(10).round(1).to_string(index=False))
    print(df[COLUMNS[2:8]].describe().round(1).to_string())

    # total_precipitation 自 UTC 0 时起累积、0 时清零。时段末计时下，UTC 次日 0 时的累积值 = 当日时间戳 01-24 时的小时值之和。
    code = int(df.loc[df.rain_era5_mm.idxmax(), "code"])
    geom = fc.filter(ee.Filter.eq("code", code)).geometry()
    u = ee.Date(day)   # UTC 零点

    def mm(img, band):
        return ee.Number(ee.Image(img).select(band).reduceRegion(ee.Reducer.mean(), geom, SCALE).get(band)).multiply(1000)

    def hourly_sum(lag):
        return mm(era5.filterDate(u.advance(lag, "hour"), u.advance(24 + lag, "hour"))
                  .select("total_precipitation_hourly").sum(), "total_precipitation_hourly")

    def cum_at(hour):
        return mm(era5.filterDate(u.advance(hour, "hour"), u.advance(hour + 1, "hour")).first(), "total_precipitation")

    v = ee.Dictionary({"lag1": hourly_sum(1), "lag0": hourly_sum(0),
                       "cum24": cum_at(24), "cum23": cum_at(23)}).getInfo()
    print(f"\n计时核对（单元 {code}，UTC {day}，mm）：", {k: round(x, 2) for k, x in v.items()})
    if abs(v["cum24"] - v["lag1"]) <= 0.01 + 0.01 * v["lag1"]:
        print("时段末计时，ERA5_ACC_LAG_H = 1 正确")
    elif abs(v["cum23"] - v["lag0"]) <= 0.01 + 0.01 * v["lag0"]:
        print("时段起点计时，请把 ERA5_ACC_LAG_H 改成 0")
    else:
        print("无法判定计时约定，先不要导出")


def export(fc):
    """按年提交导出任务，每年一个 CSV。"""
    for y in range(int(START[:4]), int(END[:4]) + 1):
        s, e = max(START, f"{y}-01-01"), min(END, f"{y}-12-31")
        n = (pd.Timestamp(e) - pd.Timestamp(s)).days + 1
        start = ee.Date(s, TZ)
        days = ee.List.sequence(0, n - 1).map(lambda i: start.advance(i, "day"))
        table = ee.FeatureCollection(days.map(lambda d: day_stats(ee.Date(d), fc))).flatten()
        task = ee.batch.Export.table.toDrive(
            collection=table, description=f"city_weather_bjt_{y}", folder=GEE_FOLDER,
            fileFormat="CSV", selectors=COLUMNS)
        task.start()
        print(f"已提交 city_weather_bjt_{y}：{s} 至 {e}，{n} 天，任务 {task.id}")


def status():
    for op in ee.data.listOperations():
        m = op.get("metadata", {})
        if m.get("description", "").startswith("city_weather_bjt"):
            err = op.get("error", {}).get("message", "")
            print(m["description"], m.get("state"), f"{m.get('progress', 0):.0%}", m.get("updateTime", ""), err)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "status":
        status()
    elif mode == "export":
        export(unit_fc())
    elif mode == "test":
        test(sys.argv[2] if len(sys.argv) > 2 else "2023-07-31", unit_fc())
    else:
        raise SystemExit(__doc__)
