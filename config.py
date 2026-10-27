"""项目路径与研究设计常量。所有脚本都从这里读取，改口径只改这一处。"""
import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
# 原始数据与中间结果放在移动硬盘（本机剩余空间约 11 GB）。环境变量 RM_DATA 可改指别处，如模拟数据测试。
DATA = Path(os.environ.get("RM_DATA", "/Volumes/WLSSD990/7-降雨和迁徙数据"))
PROC = DATA / "processed"
RESULTS = Path(os.environ.get("RM_RESULTS", PROJECT / "results"))   # 回归表和图很小，留在项目里
if not DATA.exists():
    raise SystemExit(f"找不到数据目录 {DATA}，请先接上移动硬盘")
for p in (PROC, RESULTS):
    p.mkdir(parents=True, exist_ok=True)

# ---------- 输入数据 ----------
# DIMNet-CPC（Figshare, CC BY 4.0）: https://doi.org/10.6084/m9.figshare.33154163
DIMNET_DIR = DATA / "迁徙数据"
DIMNET_FILES = {
    "DIMNet-CPC_2020-2025v1.0.parquet": "https://ndownloader.figshare.com/files/67241432",
    "Unit_Lookup.xlsx": "https://ndownloader.figshare.com/files/67241324",
    "DIMNet-CPC_Metadata_and_Validation.xlsx": "https://ndownloader.figshare.com/files/68107297",
    "README.txt": "https://ndownloader.figshare.com/files/68107294",
}
DIMNET_PARQUET = DIMNET_DIR / "DIMNet-CPC_2020-2025v1.0.parquet"
UNIT_LOOKUP = DIMNET_DIR / "Unit_Lookup.xlsx"

# 地联社 ERA5-Land 站点降水：按省/市分文件夹，每站一个“站名_站号.csv”（Date_BJT, total_precipitation(mm/day), Remark）。
# Remark 前 18 行是元信息：经纬度、所属县/地/省。已注明“北京时间 BJT, UTC+8”，由去累积的小时值求和，日界线与百度迁徙一致。
STATION_RAIN_DIR = DATA / "232-全国各省气象站1950-2026年逐日总降水量（Tp）"   # 31 省 + 3 个海上平台站，共 2421 站

# 02b 从 GEE 导出的单元面平均逐日气象（ERA5-Land 降水与气温、GPM IMERG 降水，北京时间日），从 Google Drive 下载后放这里
GEE_DIR = DATA / "GEE_城市逐日气象"
# 02c 下载的 NOAA CPC 全球逐日观测格点（降水、最高/最低气温，0.5°，免账号）
CPC_DIR = DATA / "CPC观测格点"

# 2024 版省市县行政区划（审图号 GS(2024)0650），366 个 DIMNet 单元全部能按“市代码”匹配
ADMIN_DIR = Path("/Users/liangwang/12-数据/49-2024年省市县三级行政区划数据（审图号：GS（2024）0650号）2024年5月更新")
CITY_SHP = ADMIN_DIR / "市.shp"

# ---------- 研究设计 ----------
MAIN_START, MAIN_END = "2023-01-01", "2025-12-31"   # 主样本：无缺失日、无疫情管控
CLIM_START, CLIM_END = "1991-01-01", "2020-12-31"   # 降水气候态基准期（WMO 标准期）
CORE_SHARE = 0.95       # 稳定核心连接：主样本可用日期中出现比例 >= 该值
WET_DAY_MM = 0.1        # 湿日阈值

# 国标 GB/T 28592-2012 24 小时降水等级（mm），左闭右开；第一档 0 为“无雨”参照组
RAIN_BINS = [0, 0.1, 10, 25, 50, 100, float("inf")]
RAIN_LABELS = ["无雨", "小雨", "中雨", "大雨", "暴雨", "大暴雨及以上"]

# 相对阈值：本地基准期湿日降水的分位数
REL_QUANTILES = [0.75, 0.90, 0.95, 0.99]
REL_LABELS = ["无雨", "<P75", "P75-P90", "P90-P95", "P95-P99", ">=P99"]

# 距离档（km，政府驻地或几何中心之间的大圆距离）
DIST_BINS = [0, 150, 300, 500, 1000, float("inf")]
DIST_LABELS = ["<150", "150-300", "300-500", "500-1000", ">1000"]

# 法定节假日（含与假期连休的周末）与调休上班日，依据国务院办公厅 2023、2024、2025 年部分节假日安排的通知
# （国办发明电〔2022〕16 号、〔2023〕7 号、〔2024〕12 号）。日类型：1 工作日（含调休上班的周末）/ 2 周末 / 3 节假日
HOLIDAYS = [("2023-01-01", "2023-01-02"), ("2023-01-21", "2023-01-27"), ("2023-04-05", "2023-04-05"),
            ("2023-04-29", "2023-05-03"), ("2023-06-22", "2023-06-24"), ("2023-09-29", "2023-10-06"),
            ("2023-12-30", "2024-01-01"), ("2024-02-10", "2024-02-17"), ("2024-04-04", "2024-04-06"),
            ("2024-05-01", "2024-05-05"), ("2024-06-08", "2024-06-10"), ("2024-09-15", "2024-09-17"),
            ("2024-10-01", "2024-10-07"), ("2025-01-01", "2025-01-01"), ("2025-01-28", "2025-02-04"),
            ("2025-04-04", "2025-04-06"), ("2025-05-01", "2025-05-05"), ("2025-05-31", "2025-06-02"),
            ("2025-10-01", "2025-10-08")]
ADJUSTED_WORKDAYS = ["2023-01-28", "2023-01-29", "2023-04-23", "2023-05-06", "2023-06-25", "2023-10-07", "2023-10-08",
                     "2024-02-04", "2024-02-18", "2024-04-07", "2024-04-28", "2024-05-11", "2024-09-14", "2024-09-29",
                     "2024-10-12", "2025-01-26", "2025-02-08", "2025-04-27", "2025-09-28", "2025-10-11"]
DAY_TYPES = ["工作日", "周末", "节假日"]
