"""把 03 的输出整理成回归用的两张紧凑面板（整数编码，供 06_全国回归.R 读取）。

  model_city.parquet  城市-日：总流出、总流入，本地降雨分档，以及“目的地/来源地加权降雨”控制
  model_od.parquet    OD-日：稳定核心连接的流量，起终点降雨分档（绝对/相对）、前导滞后、距离档、气候背景，
                      以及 02c 的 CPC 观测格点：日均气温分档 tb、雨量计降水分档 abc 与前 7 日累计分档 c7c；
                      v0.2 的安慰剂检验用：小雨前导滞后 m01_*、多期移位降雨分档 pb_*、七大地理区 rg7_o / rg7_d

剔除降雨代表性差的单元：补位站点距单元几何中心 > 100 km（三沙市，约 1094 km）。
"""
import numpy as np
import pandas as pd

from config import ADJUSTED_WORKDAYS, DIST_LABELS, HOLIDAYS, MAIN_END, MAIN_START, PROC, RAIN_BINS, WET_DAY_MM

LAGS = [-7, -3, -2, -1, 0, 1, 2, 3, 7]  # 负数=前导（k 天后的雨），正数=滞后；±7 为安慰剂
# 多期移位安慰剂：k 天前（正）或后（负）的降雨分档；364、728 为一年、两年前的同一星期几（错年同日）
PLACEBO_SHIFTS = [-28, -21, -14, -7, 7, 14, 21, 28, 364, 728]
# 七大地理区（省级代码前两位）：华北 东北 华东 华中 华南 西南 西北，供“大区 × 日期”固定效应
REGION7 = {1: (11, 12, 13, 14, 15), 2: (21, 22, 23), 3: (31, 32, 33, 34, 35, 36, 37), 4: (41, 42, 43),
           5: (44, 45, 46), 6: (50, 51, 52, 53, 54), 7: (61, 62, 63, 64, 65)}
PROV2R7 = {p: r for r, ps in REGION7.items() for p in ps}
# 前 7 日（t-7 至 t-1）累计降水分档，控制连阴雨与湿润期的持续性；第一档 0-10 mm 为参照
CUM7_BINS = [0, 10, 25, 50, 100, np.inf]
# 日均气温分档（°C）：<-10 / -10-0 / 0-10 / 10-15 / 15-20 / 20-25 / 25-30 / ≥30，参照 15-20（代码 4）
TEMP_BINS = [-np.inf, -10, 0, 10, 15, 20, 25, 30, np.inf]
SNOW_TMEAN_C = 2     # 日均气温低于 2 °C 的降水视为可能是雪（常用的雨雪分相气温阈值在 1-2 °C）
MAX_FILL_KM = 100


def day_type(dates: pd.Index) -> pd.Series:
    """1 工作日（含调休上班的周末）/ 2 周末 / 3 节假日（含与假期连休的周末）。"""
    hol = pd.DatetimeIndex(np.concatenate([pd.date_range(a, b) for a, b in HOLIDAYS]))
    d = pd.Series(np.where(dates.dayofweek >= 5, 2, 1), index=dates)
    d[dates.isin(pd.DatetimeIndex(ADJUSTED_WORKDAYS))] = 1
    d[dates.isin(hol)] = 3
    return d.astype("int8")


def tag(k: int) -> str:
    return f"F{-k}" if k < 0 else f"L{k}"


def city_rain(units: pd.DataFrame) -> pd.DataFrame:
    r = pd.read_parquet(PROC / "city_rain.parquet").sort_values(["code", "date"])
    r["ab"] = r["abs_bin"].cat.codes.astype("int8")      # 0 无雨 … 5 大暴雨及以上
    r["rb"] = r["rel_bin"].cat.codes.astype("int8")      # 0 无雨 … 5 >=P99
    g = r.groupby("code")["rain_mm"]
    for k in LAGS:
        s = g.shift(k) if k else r["rain_mm"]
        r[f"m01_{tag(k)}"] = s.between(WET_DAY_MM, 10, inclusive="left").astype("int8")
        r[f"m10_{tag(k)}"] = s.between(10, 25, inclusive="left").astype("int8")
        r[f"m25_{tag(k)}"] = (s >= 25).astype("int8")
    pb = [f"pb_{tag(k)}" for k in PLACEBO_SHIFTS]
    for k, col in zip(PLACEBO_SHIFTS, pb):    # 0 无雨 / 1 小雨 / 2 中雨 / 3 ≥25 mm
        r[col] = pd.cut(g.shift(k), [0, WET_DAY_MM, 10, 25, np.inf], labels=False, right=False)
    cum7 = g.transform(lambda x: x.shift(1).rolling(7, min_periods=7).sum())
    r["cum7_mm"] = cum7.astype("float32")
    r["c7"] = pd.cut(cum7, CUM7_BINS, labels=False, right=False)
    r = r[(r["date"] >= MAIN_START) & (r["date"] <= MAIN_END)]
    # 序列开头 7 天无累计值、移位最远 728 天前与 28 天后，都在降水序列（2019-12 至 2026-10）之内
    r = r.astype({c: "int8" for c in ["c7"] + pb})
    return r.drop(columns=["abs_bin", "rel_bin"])


def city_cpc():
    """02c 的 CPC 观测格点：日均气温分档 tb，雨量计降水当日分档 abc 与前 7 日累计分档 c7c（口径同 ab、c7），
    以及易降雪日 sn（日均气温低于 SNOW_TMEAN_C，当天降水可能是雪或雨夹雪）。"""
    path = PROC / "city_cpc_daily.parquet"
    if not path.exists():
        return None
    c = pd.read_parquet(path).sort_values(["code", "date"])
    c["tb"] = pd.cut(c["tmean_c"], TEMP_BINS, labels=False, right=False)
    c["abc"] = pd.cut(c["rain_cpc_mm"], RAIN_BINS, labels=False, right=False)
    cum7 = c.groupby("code")["rain_cpc_mm"].transform(lambda x: x.shift(1).rolling(7, min_periods=7).sum())
    c["c7c"] = pd.cut(cum7, CUM7_BINS, labels=False, right=False)
    c["sn"] = (c["tmean_c"] < SNOW_TMEAN_C).astype("int8")
    c["sn0"] = (c["tmean_c"] < 0).astype("int8")        # 阈值敏感性：0 °C 与 4 °C
    c["sn4"] = (c["tmean_c"] < 4).astype("int8")
    c = c[(c["date"] >= MAIN_START) & (c["date"] <= MAIN_END)]
    return c[["code", "date", "tb", "abc", "c7c", "sn", "sn0", "sn4"]].astype({"tb": "int8", "abc": "int8", "c7c": "int8"})


def add_typhoon(df: pd.DataFrame, key: str, suffix: str = "") -> pd.DataFrame:
    """并入 08_台风日标识.py 的台风影响日（tc500 / tc300，未受影响记 0）。"""
    path = PROC / "city_typhoon.parquet"
    if not path.exists():
        return df
    ty = pd.read_parquet(path)[["code", "date", "tc500", "tc300"]]
    ty = ty.rename(columns={"code": key, "tc500": f"tc500{suffix}", "tc300": f"tc300{suffix}"})
    df = df.merge(ty, on=[key, "date"], how="left")
    for v in ("tc500", "tc300"):
        df[f"{v}{suffix}"] = df[f"{v}{suffix}"].fillna(0).astype("int8")
    return df


def main():
    u = pd.read_parquet(PROC / "units.parquet")
    meta = pd.read_csv(PROC / "station_meta.csv")
    fill = meta.groupby("code")["fill_km"].max() if "fill_km" in meta else pd.Series(dtype=float)
    u["rain_ok"] = ~u["code"].map(fill).gt(MAX_FILL_KM)
    print("剔除降雨代表性差的单元:", u.loc[~u.rain_ok, "name"].tolist())
    z = np.log(u["annual_mm"])
    u["clim_z"] = (z - z.mean()) / z.std()                  # 长期降水（对数）标准化：每 1 个标准差
    u["humid"] = (u["annual_mm"] >= 800).astype("int8")      # 800 mm 等雨量线≈秦岭—淮河
    u["region"] = u["region4"].map({"东部": 1, "中部": 2, "西部": 3, "东北": 4}).astype("int8")
    ok = set(u.loc[u.rain_ok, "code"])
    rain = city_rain(u)
    rain = rain[rain["code"].isin(ok)]
    cpc = city_cpc()
    if cpc is not None:
        rain = rain.merge(cpc, on=["code", "date"], how="left")
        print("CPC 缺测单元日:", int(rain[["tb", "abc", "c7c"]].isna().any(axis=1).sum()))
    dates = pd.Index(sorted(rain["date"].unique()))
    did = pd.Series(np.arange(1, len(dates) + 1, dtype="int32"), index=dates)

    # ---------- OD-日 ----------
    p = pd.read_parquet(PROC / "od_panel.parquet").rename(columns={"Date": "date"})
    p = p[p["o"].isin(ok) & p["d"].isin(ok)]
    e = pd.read_parquet(PROC / "edges.parquet")[["o", "d", "dist_km", "dist_band"]]
    p = p.merge(e, on=["o", "d"])
    p["dband"] = p["dist_band"].cat.codes.astype("int8")     # 0 <150 … 4 >1000
    keep = (["code", "date", "rain_mm", "ab", "rb", "c7", "cum7_mm"]
            + [c for c in rain.columns if c.startswith(("m01_", "m10_", "m25_", "pb_"))]
            + [c for c in ("tb", "abc", "c7c", "sn", "sn0", "sn4") if c in rain.columns])
    for end in ("o", "d"):
        x = rain[keep].rename(columns={c: f"{c}_{end}" for c in keep if c not in ("code", "date")})
        p = p.merge(x.rename(columns={"code": end}), on=[end, "date"])
    for end in ("o", "d"):
        p = add_typhoon(p, end, f"_{end}")
    ua = u.set_index("code")
    for end in ("o", "d"):
        p[f"clim_{end}"] = p[end].map(ua["clim_z"]).astype("float32")
        p[f"humid_{end}"] = p[end].map(ua["humid"]).astype("int8")
    p["region_o"] = p["o"].map(ua["region"]).astype("int8")
    for end in ("o", "d"):
        p[f"rg7_{end}"] = (p[end] // 10000).map(PROV2R7).astype("int8")
    p["ln_flow"] = np.log(p["flow"]).astype("float64")
    od = pd.factorize(p["o"].astype("int64") * 1_000_000 + p["d"])[0]
    p["od"] = (od + 1).astype("int32")
    p["od_ym"] = (pd.factorize(od.astype("int64") * 1000 + (p["date"].dt.year - 2020) * 12 + p["date"].dt.month)[0] + 1).astype("int32")
    p["od_dow"] = (pd.factorize(od.astype("int64") * 10 + p["date"].dt.dayofweek)[0] + 1).astype("int32")
    p["date_id"] = p["date"].map(did).astype("int32")
    p["dtype"] = p["date"].map(day_type(dates)).astype("int8")
    p = p.drop(columns=["date", "dist_band"]).astype({c: "float32" for c in ("rain_mm_o", "rain_mm_d", "dist_km", "cum7_mm_o", "cum7_mm_d")})
    p.to_parquet(PROC / "model_od.parquet", index=False)
    print(f"model_od: {len(p):,} 行，{p['od'].nunique():,} 条连接；距离档行数：",
          dict(zip(DIST_LABELS, np.bincount(p["dband"], minlength=5))))

    # ---------- 城市-日 ----------
    c = pd.read_parquet(PROC / "city_flow.parquet").rename(columns={"Date": "date"})
    c = add_typhoon(c[c["code"].isin(ok)].merge(rain, on=["code", "date"]), "code")
    # 目的地加权降雨：i 的出行目的地按主样本平均流量加权，当天处于中雨、≥25 mm 的份额（流入同理按来源地加权）
    core = pd.read_parquet(PROC / "od_panel.parquet")
    core = core[core["o"].isin(ok) & core["d"].isin(ok)]
    w = core.groupby(["o", "d"])["flow"].mean().rename("w").reset_index()
    for side, other, name in (("o", "d", "wd"), ("d", "o", "wo")):
        ww = w.assign(w=w["w"] / w.groupby(side)["w"].transform("sum"))
        for v in ("m10_L0", "m25_L0"):
            pv = rain.pivot(index="date", columns="code", values=v)
            W = ww.pivot(index=other, columns=side, values="w").reindex(index=pv.columns).fillna(0)
            share = pd.DataFrame(pv.fillna(0).to_numpy() @ W.to_numpy(), index=pv.index, columns=W.columns)
            s = share.stack().rename(f"{name}_{v[:3]}").reset_index().rename(columns={side: "code"})
            c = c.merge(s, on=["date", "code"], how="left")
    c["code_ym"] = (pd.factorize(c["code"].astype("int64") * 1000 + (c["date"].dt.year - 2020) * 12 + c["date"].dt.month)[0] + 1).astype("int32")
    c["code_dow"] = (pd.factorize(c["code"].astype("int64") * 10 + c["date"].dt.dayofweek)[0] + 1).astype("int32")
    c["date_id"] = c["date"].map(did).astype("int32")
    c["clim"] = c["code"].map(ua["clim_z"]).astype("float32")
    c["humid"] = c["code"].map(ua["humid"]).astype("int8")
    c["region"] = c["code"].map(ua["region"]).astype("int8")
    c = c.drop(columns=["date"])
    c.to_parquet(PROC / "model_city.parquet", index=False)
    print(f"model_city: {len(c):,} 行，{c['code'].nunique()} 个城市")


if __name__ == "__main__":
    main()
