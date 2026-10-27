# 全国回归：降雨对城际流量的剂量-响应，及其距离、气候、区域异质性与动态。
# 读取 04_构建回归面板.py 的输出；结果逐个模型追加写入 results/全国回归结果.csv。
#
# 依赖：install.packages(c("fixest", "nanoparquet", "data.table"))
# 用法：Rscript 06_全国回归.R            # 全部模型
#       Rscript 06_全国回归.R city M1    # 只跑指定模型
#
# OD 层级 2878 万行。固定效应：OD×年月、OD×星期、日期；标准误按起点、终点城市双向聚类。
# 内存紧张的模型（动态、PPML）用按连接的随机抽样，抽样比例写在模型名里。

suppressPackageStartupMessages({
  library(fixest)
  library(nanoparquet)
  library(data.table)
})
setFixest_notes(FALSE)
setFixest_nthreads(6)

DATA <- Sys.getenv("RM_DATA", "/Volumes/WLSSD990/7-降雨和迁徙数据")
PROC <- file.path(DATA, "processed")
script_dir <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
RES <- Sys.getenv("RM_RESULTS", file.path(script_dir, "results"))
# 主口径（2026-10-23 起）是“日常降雨”：剔除台风日与易降雪日（任一端 CPC 日均气温 <2 °C，列 sn）。
# RM_EVERYDAY=1 时，所有“非台风日”模型（read_ntc 与 T2、T4、T5、T6）改在日常样本上估计，结果写入
# 全国回归结果_日常.csv 与 vcov_日常/；不设时为原口径（非台风日，含易降雪日），写入 全国回归结果.csv。
# RM_SNOW=sn0 / sn4 改用 0 °C / 4 °C 阈值做敏感性，结果文件名带阈值后缀。
EVD <- Sys.getenv("RM_EVERYDAY") == "1"
SNOW <- Sys.getenv("RM_SNOW", "sn")
TAG <- if (!EVD) "" else if (SNOW == "sn") "_日常" else paste0("_日常_", SNOW)
OUT <- file.path(RES, paste0("全国回归结果", TAG, ".csv"))
todo <- commandArgs(trailingOnly = TRUE)
run <- function(name) length(todo) == 0 || name %in% todo

tidy <- function(m, name) {
  ct <- as.data.table(coeftable(m), keep.rownames = "term")
  setnames(ct, 2:5, c("est", "se", "t", "p"))
  ct[, `:=`(model = name, nobs = nobs(m), r2_within = tryCatch(unname(r2(m, "wr2")), error = function(e) NA_real_))]
  ct
}
save <- function(dt) {
  old <- if (file.exists(OUT)) fread(OUT)[!model %in% unique(dt$model)] else NULL
  fwrite(rbind(old, dt, fill = TRUE), OUT, bom = TRUE)
  cat(sprintf("[%s] 已写入 %s\n", format(Sys.time(), "%H:%M:%S"), paste(unique(dt$model), collapse = ", ")))
}
fit_split <- function(fml, data, by, name, ...) {
  out <- list()
  for (g in sort(unique(data[[by]]))) {
    m <- feols(fml, data[data[[by]] == g], ...)
    out[[length(out) + 1]] <- tidy(m, sprintf("%s_%s%s", name, by, g))
  }
  rbindlist(out)
}
od_cols <- function(...) c("ln_flow", "o", "d", "od", "od_ym", "od_dow", "date_id", ...)
read_od <- function(cols, frac = 1) {
  x <- setDT(read_parquet(file.path(PROC, "model_od.parquet"), col_select = unique(cols)))
  if (frac < 1) {
    set.seed(1)
    keep <- sample(unique(x$od), round(frac * uniqueN(x$od)))
    x <- x[od %in% keep]
  }
  x
}
snow_cols <- if (EVD) paste0(SNOW, c("_o", "_d")) else character(0)
no_snow <- function(x) {      # 日常口径：再剔除任一端为易降雪日的连接-日
  if (!EVD) return(x)
  x <- x[x[[snow_cols[1]]] == 0 & x[[snow_cols[2]]] == 0]
  x[, (snow_cols) := NULL][]
}
FE <- "od_ym + od_dow + date_id"
CL <- ~o + d

# ---------- 城市层级：总流出（本地降雨=起点）、总流入（本地降雨=终点） ----------
if (run("city")) {
  city <- setDT(read_parquet(file.path(PROC, "model_city.parquet")))
  city[, `:=`(ln_out = log(outflow), ln_in = log(inflow))]
  cfe <- "| code_ym + code_dow + date_id"
  c1 <- feols(as.formula(paste("ln_out ~ i(ab, ref = 0) + wd_m10 + wd_m25", cfe)), city, cluster = ~code + date_id)
  c2 <- feols(as.formula(paste("ln_in ~ i(ab, ref = 0) + wo_m10 + wo_m25", cfe)), city, cluster = ~code + date_id)
  c3 <- feols(as.formula(paste("ln_out ~ i(rb, ref = 0) + wd_m10 + wd_m25", cfe)), city, cluster = ~code + date_id)
  save(rbind(tidy(c1, "C1_城市流出_绝对"), tidy(c2, "C2_城市流入_绝对"), tidy(c3, "C3_城市流出_相对")))
  rm(city); gc()
}

# ---------- M1 OD 剂量-响应 ----------
if (run("M1")) {
  x <- read_od(od_cols("ab_o", "ab_d"))
  m <- feols(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) |", FE)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "M1_OD绝对分档")); rm(x, m); gc()
}

# ---------- M2 距离：按距离档分样本（每档有自己的日期效应；全交互需约 12 GB 设计矩阵） ----------
if (run("M2")) {
  x <- read_od(od_cols("ab_o", "ab_d", "dband"))
  save(fit_split(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) |", FE)), x, "dband",
                 "M2_距离", cluster = CL, lean = TRUE))
  rm(x); gc()
}

# ---------- M3 气候适应：雨档 × 起终点长期降水（标准化，50% 连接抽样，全样本超过 16 GB）；
#            再按起点干湿分样本（全样本），比较绝对分档与本地分位数分档 ----------
if (run("M3")) {
  x <- read_od(od_cols("ab_o", "ab_d", "clim_o", "clim_d"), frac = 0.5)
  m <- feols(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_o, clim_o, ref = 0) +",
                              "i(ab_d, ref = 0) + i(ab_d, clim_d, ref = 0) |", FE)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "M3_气候交互_抽样50%")); rm(x, m); gc()
  x <- read_od(od_cols("ab_o", "ab_d", "humid_o"))
  save(fit_split(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) |", FE)), x, "humid_o",
                 "M3_绝对", cluster = CL, lean = TRUE))
  rm(x); gc()
  x <- read_od(od_cols("rb_o", "rb_d", "humid_o"))
  save(fit_split(as.formula(paste("ln_flow ~ i(rb_o, ref = 0) + i(rb_d, ref = 0) |", FE)), x, "humid_o",
                 "M3_相对", cluster = CL, lean = TRUE))
  rm(x); gc()
}

# ---------- M4 相对分档（全国） ----------
if (run("M4")) {
  x <- read_od(od_cols("rb_o", "rb_d"))
  m <- feols(as.formula(paste("ln_flow ~ i(rb_o, ref = 0) + i(rb_d, ref = 0) |", FE)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "M4_OD相对分档")); rm(x, m); gc()
}

# ---------- M5 区域：按起点所在四大区域分样本 ----------
if (run("M5")) {
  x <- read_od(od_cols("ab_o", "ab_d", "region_o"))
  save(fit_split(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) |", FE)), x, "region_o",
                 "M5_区域", cluster = CL, lean = TRUE))
  rm(x); gc()
}

# ---------- M6 动态：起终点中雨、≥25 mm 的前导与滞后（50% 连接抽样） ----------
if (run("M6")) {
  tags <- c("F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- read_od(od_cols(vv), frac = 0.5)
  m <- feols(as.formula(paste("ln_flow ~", paste(vv, collapse = " + "), "|", FE)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "M6_动态_抽样50%")); rm(x, m); gc()
}

# ---------- R1 PPML（水平值，30% 连接抽样） ----------
if (run("R1")) {
  x <- read_od(c(od_cols("ab_o", "ab_d"), "flow"), frac = 0.3)
  m <- fepois(as.formula(paste("flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) |", FE)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "R1_PPML_抽样30%")); rm(x, m); gc()
}
# ---------- 加入前 7 日累计降水控制（c7：0-10 / 10-25 / 25-50 / 50-100 / ≥100 mm，参照 0-10） ----------
C7 <- "i(c7_o, ref = 0) + i(c7_d, ref = 0)"
if (run("Cc")) {
  city <- setDT(read_parquet(file.path(PROC, "model_city.parquet")))
  city[, `:=`(ln_out = log(outflow), ln_in = log(inflow))]
  cfe <- "| code_ym + code_dow + date_id"
  c1 <- feols(as.formula(paste("ln_out ~ i(ab, ref = 0) + i(c7, ref = 0) + wd_m10 + wd_m25", cfe)), city, cluster = ~code + date_id)
  c2 <- feols(as.formula(paste("ln_in ~ i(ab, ref = 0) + i(c7, ref = 0) + wo_m10 + wo_m25", cfe)), city, cluster = ~code + date_id)
  save(rbind(tidy(c1, "C1c_城市流出_含7日累计"), tidy(c2, "C2c_城市流入_含7日累计")))
  rm(city); gc()
}
if (run("M1c")) {
  x <- read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d"))
  m <- feols(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) +", C7, "|", FE)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "M1c_OD绝对分档_含7日累计")); rm(x, m); gc()
}
if (run("M2c")) {
  x <- read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "dband"))
  save(fit_split(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) +", C7, "|", FE)), x, "dband",
                 "M2c_距离_含7日累计", cluster = CL, lean = TRUE))
  rm(x); gc()
}
if (run("M3c")) {
  x <- read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "humid_o"))
  save(fit_split(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) +", C7, "|", FE)), x, "humid_o",
                 "M3c_绝对_含7日累计", cluster = CL, lean = TRUE))
  rm(x); gc()
}
# 动态：增加 7 天后降雨（F7）作为更干净的安慰剂；M6b 不含累计控制，M6c 再加入累计控制。
# 两者用同一 30% 连接抽样以便对比（50% 抽样加累计控制时超过 16 GB）
if (run("M6b") || run("M6c")) {
  tags <- c("F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- read_od(od_cols(vv, "c7_o", "c7_d"), frac = 0.3)
  dyn <- paste(vv, collapse = " + ")
  if (run("M6b")) {
    save(tidy(feols(as.formula(paste("ln_flow ~", dyn, "|", FE)), x, cluster = CL, lean = TRUE), "M6b_动态含F7_抽样30%"))
    gc()
  }
  if (run("M6c")) save(tidy(feols(as.formula(paste("ln_flow ~", dyn, "+", C7, "|", FE)), x, cluster = CL, lean = TRUE),
                            "M6c_动态含F7与7日累计_抽样30%"))
  rm(x); gc()
}
# ---------- 更细的时间固定效应：OD×周（替代 OD×年月），吸收月内季节性；检验 ±7 天安慰剂是否因此归零 ----------
# date_id=1 为 2023-01-01（周日）；按周一起算的周序号 = (date_id + 5) %/% 7
FEW <- "od_wk + od_dow + date_id"
add_wk <- function(x) x[, od_wk := od * 200L + (date_id + 5L) %/% 7L][]
if (run("M1w")) {
  x <- add_wk(read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d")))
  m <- feols(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) +", C7, "|", FEW)), x, cluster = CL, lean = TRUE)
  save(tidy(m, "M1w_OD绝对分档_OD周FE_含7日累计")); rm(x, m); gc()
}
if (run("M6w")) {
  tags <- c("F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- add_wk(read_od(od_cols(vv), frac = 0.3))
  save(tidy(feols(as.formula(paste("ln_flow ~", paste(vv, collapse = " + "), "|", FEW)), x, cluster = CL, lean = TRUE),
            "M6w_动态含F7_OD周FE_抽样30%"))
  rm(x); gc()
}
# ---------- 推断稳健性：再按日期聚类（起点 + 终点 + 日期三向）。大尺度天气系统同日覆盖多个城市，
#            只按城市聚类会低估标准误 ----------
CL3 <- ~o + d + date_id
# 全样本三向聚类超过 16 GB，故在同一 30% 连接抽样上拟合一次，分别计算双向与三向聚类标准误
if (run("M1c3")) {
  x <- read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d"), frac = 0.3)
  m <- feols(as.formula(paste("ln_flow ~ i(ab_o, ref = 0) + i(ab_d, ref = 0) +", C7, "|", FE)), x, cluster = CL)
  save(rbind(tidy(m, "M1c_抽样30%_双向聚类"), tidy(summary(m, cluster = CL3), "M1c_抽样30%_三向聚类")))
  rm(x, m); gc()
}
if (run("M6b3")) {
  tags <- c("F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- read_od(od_cols(vv), frac = 0.3)
  m <- feols(as.formula(paste("ln_flow ~", paste(vv, collapse = " + "), "|", FE)), x, cluster = CL)
  save(tidy(summary(m, cluster = CL3), "M6b_动态含F7_抽样30%_三向聚类"))
  rm(x, m); gc()
}
# ---------- 台风：tc500 = 当天热带气旋中心（含残余）距单元 ≤500 km（08_台风日标识.py） ----------
# T1 控制台风日；T2 剔除任一端台风日；T2b 改用 300 km；T3 雨档 × 台风交互（50% 抽样）；
# T4 / T5 / T6 为剔除台风日后的干湿分样本、距离分样本与城市层级
B <- paste("i(ab_o, ref = 0) + i(ab_d, ref = 0) +", C7)
if (run("T1")) {     # 20 个回归元，全样本超过 16 GB，用 50% 连接抽样
  x <- read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "tc500_o", "tc500_d"), frac = 0.5)
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "+ tc500_o + tc500_d |", FE)), x, cluster = CL, lean = TRUE),
            "T1_控制台风日_抽样50%"))
  rm(x); gc()
}
for (r in c(500, 300)) {
  name <- if (r == 500) "T2" else "T2b"
  if (!run(name)) next
  x <- read_od(c(od_cols("ab_o", "ab_d", "c7_o", "c7_d", paste0("tc", r, "_o"), paste0("tc", r, "_d")), snow_cols))
  keep <- x[[paste0("tc", r, "_o")]] == 0 & x[[paste0("tc", r, "_d")]] == 0
  x <- x[keep]; x[, (paste0("tc", r, c("_o", "_d"))) := NULL]; x <- no_snow(x); gc()
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "|", FE)), x, cluster = CL, lean = TRUE),
            sprintf("%s_剔除台风日%dkm", name, r)))
  rm(x); gc()
}
if (run("T3")) {
  x <- read_od(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "tc500_o", "tc500_d"), frac = 0.5)
  m <- feols(as.formula(paste("ln_flow ~", B, "+ i(ab_o, tc500_o, ref = 0) + i(ab_d, tc500_d, ref = 0) + tc500_o + tc500_d |", FE)),
             x, cluster = CL, lean = TRUE)
  save(tidy(m, "T3_雨档x台风_抽样50%")); rm(x, m); gc()
}
if (run("T4") || run("T5")) {
  x <- read_od(c(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "tc500_o", "tc500_d", "humid_o", "dband"), snow_cols))
  x <- no_snow(x[tc500_o == 0 & tc500_d == 0][, c("tc500_o", "tc500_d") := NULL]); gc()
  if (run("T4")) save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x, "humid_o", "T4_剔除台风日_干湿",
                                cluster = CL, lean = TRUE))
  gc()
  if (run("T5")) save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x, "dband", "T5_剔除台风日_距离",
                                cluster = CL, lean = TRUE))
  rm(x); gc()
}
if (run("T6")) {
  city <- setDT(read_parquet(file.path(PROC, "model_city.parquet")))[tc500 == 0]
  if (EVD) city <- city[get(SNOW) == 0]
  city[, `:=`(ln_out = log(outflow), ln_in = log(inflow))]
  cfe <- "| code_ym + code_dow + date_id"
  c1 <- feols(as.formula(paste("ln_out ~ i(ab, ref = 0) + i(c7, ref = 0) + wd_m10 + wd_m25", cfe)), city, cluster = ~code + date_id)
  c2 <- feols(as.formula(paste("ln_in ~ i(ab, ref = 0) + i(c7, ref = 0) + wo_m10 + wo_m25", cfe)), city, cluster = ~code + date_id)
  save(rbind(tidy(c1, "T6_城市流出_剔除台风日"), tidy(c2, "T6_城市流入_剔除台风日")))
  rm(city); gc()
}
# ---------- 主口径：非台风日（起终点 500 km 内均无热带气旋），含前 7 日累计降水控制 ----------
# 已有：T2（剂量-响应）、T4（干湿）、T5（距离）、T6（城市）。以下补齐其余分析。
read_ntc <- function(cols, frac = 1) {
  x <- read_od(c(cols, "tc500_o", "tc500_d", snow_cols), frac = frac)
  x <- no_snow(x[tc500_o == 0 & tc500_d == 0][, c("tc500_o", "tc500_d") := NULL])
  gc(); x
}
if (run("N3r")) {
  x <- read_ntc(od_cols("rb_o", "rb_d", "c7_o", "c7_d", "humid_o"))
  save(fit_split(as.formula(paste("ln_flow ~ i(rb_o, ref = 0) + i(rb_d, ref = 0) +", C7, "|", FE)), x, "humid_o",
                 "N3r_非台风_相对_干湿", cluster = CL, lean = TRUE))
  rm(x); gc()
}
if (run("N4")) {
  x <- read_ntc(od_cols("rb_o", "rb_d", "c7_o", "c7_d"))
  save(tidy(feols(as.formula(paste("ln_flow ~ i(rb_o, ref = 0) + i(rb_d, ref = 0) +", C7, "|", FE)), x, cluster = CL, lean = TRUE),
            "N4_非台风_相对分档")); rm(x); gc()
}
if (run("N5")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "region_o"))
  save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x, "region_o", "N5_非台风_区域", cluster = CL, lean = TRUE))
  rm(x); gc()
}
if (run("N3i")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "clim_o", "clim_d"), frac = 0.5)
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "+ i(ab_o, clim_o, ref = 0) + i(ab_d, clim_d, ref = 0) |", FE)),
                  x, cluster = CL, lean = TRUE), "N3i_非台风_气候交互_抽样50%"))
  rm(x); gc()
}
if (run("N1c3")) {      # 同一 30% 抽样上的双向与三向聚类
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d"), frac = 0.3)
  m <- feols(as.formula(paste("ln_flow ~", B, "|", FE)), x, cluster = CL)
  save(rbind(tidy(m, "N1_非台风_抽样30%_双向聚类"), tidy(summary(m, cluster = CL3), "N1_非台风_抽样30%_三向聚类")))
  rm(x, m); gc()
}
if (run("N1w")) {
  x <- add_wk(read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d")))
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "|", FEW)), x, cluster = CL, lean = TRUE), "N1w_非台风_OD周FE"))
  rm(x); gc()
}
if (run("N6")) {
  tags <- c("F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- read_ntc(od_cols(vv), frac = 0.3)
  m <- feols(as.formula(paste("ln_flow ~", paste(vv, collapse = " + "), "|", FE)), x, cluster = CL)
  save(rbind(tidy(m, "N6_非台风_动态_抽样30%_双向聚类"), tidy(summary(m, cluster = CL3), "N6_非台风_动态_抽样30%_三向聚类")))
  rm(x, m); gc()
}
if (run("NR1")) {
  x <- read_ntc(c(od_cols("ab_o", "ab_d", "c7_o", "c7_d"), "flow"), frac = 0.3)
  save(tidy(fepois(as.formula(paste("flow ~", B, "|", FE)), x, cluster = CL, lean = TRUE), "NR1_非台风_PPML_抽样30%"))
  rm(x); gc()
}
# ---------- 气温控制与雨量计稳健性（02c 的 NOAA CPC 观测格点，非台风日） ----------
# tb 日均气温分档，参照 15-20 °C（代码 4）；abc、c7c 为 CPC 雨量计降水的当日与前 7 日累计分档，口径同 ab、c7。
# Q：加气温后 32 个回归元，全样本超过 16 GB，故在同一 50% 连接抽样上拟合不加气温（Q0）、加气温（Q1）、
#    CPC 降水加气温（Q2），三者可直接比较；G1：CPC 降水替换 ERA5-Land（18 个回归元，全样本，对照 T2）。
TB <- "i(tb_o, ref = 4) + i(tb_d, ref = 4)"
BC <- "i(abc_o, ref = 0) + i(abc_d, ref = 0) + i(c7c_o, ref = 0) + i(c7c_d, ref = 0)"
if (run("Q")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "tb_o", "tb_d", "abc_o", "abc_d", "c7c_o", "c7c_d"), frac = 0.5)
  for (s in list(c("Q0_非台风_抽样50%", B), c("Q1_非台风_含气温_抽样50%", paste(B, "+", TB)),
                 c("Q2_非台风_CPC降水_含气温_抽样50%", paste(BC, "+", TB)))) {
    save(tidy(feols(as.formula(paste("ln_flow ~", s[2], "|", FE)), x, cluster = CL, lean = TRUE), s[1]))
    gc()
  }
  rm(x); gc()
}
if (run("G1")) {
  x <- read_ntc(od_cols("abc_o", "abc_d", "c7c_o", "c7c_d"))
  save(tidy(feols(as.formula(paste("ln_flow ~", BC, "|", FE)), x, cluster = CL, lean = TRUE), "G1_非台风_CPC降水"))
  rm(x); gc()
}
# ---------- v0.2 安慰剂与区域冲击（非台风日） ----------
# FER：起点、终点所在七大地理区 × 日期固定效应替代全国日期效应，吸收寒暑假、区域性活动等区域冲击
FER <- "od_ym + od_dow + rg7_o^date_id + rg7_d^date_id"
# N7：小雨（0.1-10 mm）也进入动态模型，3 档 × 9 期 × 两端 = 54 个回归元（30% 连接抽样），F7、L7 为安慰剂；
#     N7r 为同一样本上的大区 × 日期固定效应版本
if (run("N7")) {
  tags <- c("F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m01_", "m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- read_ntc(od_cols(vv, "rg7_o", "rg7_d"), frac = 0.3)
  f <- paste("ln_flow ~", paste(vv, collapse = " + "), "|")
  m <- feols(as.formula(paste(f, FE)), x, cluster = CL)
  save(rbind(tidy(m, "N7_非台风_动态含小雨_抽样30%_双向聚类"), tidy(summary(m, cluster = CL3), "N7_非台风_动态含小雨_抽样30%_三向聚类")))
  rm(m); gc()
  m <- feols(as.formula(paste(f, FER)), x, cluster = CL)
  save(rbind(tidy(m, "N7r_非台风_动态含小雨_大区日期FE_抽样30%_双向聚类"),
             tidy(summary(m, cluster = CL3), "N7r_非台风_动态含小雨_大区日期FE_抽样30%_三向聚类")))
  rm(x, m); gc()
}
# P：多期移位安慰剂。在主模型上再加入 t+k 天的降雨分档（0 无雨 / 1 小雨 / 2 中雨 / 3 ≥25 mm），
#    k = ±7、±14、±21、±28 天与一年、两年前的同一星期几；全国日期效应（P_）与大区 × 日期（Pr_）各一遍，30% 连接抽样
PB <- c("F28", "F21", "F14", "F7", "L7", "L14", "L21", "L28", "L364", "L728")
if (run("P")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "rg7_o", "rg7_d", paste0("pb_", PB, "_o"), paste0("pb_", PB, "_d")), frac = 0.3)
  for (k in PB) {
    f <- paste("ln_flow ~", B, sprintf("+ i(pb_%s_o, ref = 0) + i(pb_%s_d, ref = 0) |", k, k))
    save(rbind(tidy(feols(as.formula(paste(f, FE)), x, cluster = CL, lean = TRUE), sprintf("P_%s_抽样30%%", k)),
               tidy(feols(as.formula(paste(f, FER)), x, cluster = CL, lean = TRUE), sprintf("Pr_%s_大区日期FE_抽样30%%", k))))
    gc()
  }
  rm(x); gc()
}
# R7：主口径（T2）与距离分样本（T5）改用大区 × 日期固定效应（全样本）；G5：CPC 雨量计降水的距离分样本。供损失区间
if (run("R7")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "rg7_o", "rg7_d", "dband"))
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "|", FER)), x, cluster = CL, lean = TRUE), "R7_非台风_大区日期FE"))
  gc()
  save(fit_split(as.formula(paste("ln_flow ~", B, "|", FER)), x, "dband", "R7_非台风_大区日期FE_距离", cluster = CL, lean = TRUE))
  rm(x); gc()
}
if (run("G5")) {
  x <- read_ntc(od_cols("abc_o", "abc_d", "c7c_o", "c7c_d", "dband"))
  save(fit_split(as.formula(paste("ln_flow ~", BC, "|", FE)), x, "dband", "G5_非台风_CPC降水_距离", cluster = CL, lean = TRUE))
  rm(x); gc()
}
# T45t：干湿（T4）与距离（T5）分样本加气温控制。与 Q 相同的 50% 连接抽样，同一样本上分别拟合不加气温（T4q、T5q）
#       与加气温（T4t、T5t），两两可直接比较
if (run("T45t")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "tb_o", "tb_d", "humid_o", "dband"), frac = 0.5)
  for (s in list(c("humid_o", "T4q_非台风_干湿_抽样50%", B), c("humid_o", "T4t_非台风_干湿_含气温_抽样50%", paste(B, "+", TB)),
                 c("dband", "T5q_非台风_距离_抽样50%", B), c("dband", "T5t_非台风_距离_含气温_抽样50%", paste(B, "+", TB)))) {
    save(fit_split(as.formula(paste("ln_flow ~", s[3], "|", FE)), x, s[1], s[2], cluster = CL, lean = TRUE))
    gc()
  }
  rm(x); gc()
}
# ---------- v0.4：降雪与滞后损失（非台风日） ----------
# 协方差矩阵另存 results/vcov/<模型名>.csv，供 09b 用参数模拟给损失置信区间
save_vcov <- function(m, name) {
  dir.create(file.path(RES, paste0("vcov", TAG)), showWarnings = FALSE)
  v <- as.matrix(unclass(m$cov.scaled))   # 估计时已按 cluster 算好的协方差；fixest_vcov 类直接转 data.table 会无限递归
  fwrite(data.table(term = rownames(v), as.data.table(v)), file.path(RES, paste0("vcov", TAG), paste0(name, ".csv")), bom = TRUE)
}
# W：只用 5-9 月（基本无降雪），重估剂量-响应（W1）与干湿分样本（W4）。date_id = 1 为 2023-01-01
if (run("W")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "humid_o"))
  x <- x[month(as.IDate("2022-12-31") + date_id) %in% 5:9]; gc()
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "|", FE)), x, cluster = CL, lean = TRUE), "W1_非台风_5至9月"))
  gc()
  save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x, "humid_o", "W4_非台风_5至9月_干湿", cluster = CL, lean = TRUE))
  rm(x); gc()
}
# S：全年降水分相。日均气温 <2 °C 的易降雪日（sn）的降水单独分档（abs），其余为降雨（abw）；
#    同时控制易降雪日本身（sn）。参数翻倍，50% 连接抽样；S4 为干湿分样本
if (run("S")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "sn_o", "sn_d", "humid_o"), frac = 0.5)
  x[, `:=`(abw_o = ab_o * (1L - sn_o), abs_o = ab_o * sn_o, abw_d = ab_d * (1L - sn_d), abs_d = ab_d * sn_d)]
  fs <- as.formula(paste("ln_flow ~ i(abw_o, ref = 0) + i(abs_o, ref = 0) + i(abw_d, ref = 0) + i(abs_d, ref = 0) + sn_o + sn_d +",
                         C7, "|", FE))
  save(tidy(feols(fs, x, cluster = CL, lean = TRUE), "S1_非台风_降水分相_抽样50%"))
  gc()
  save(fit_split(fs, x, "humid_o", "S4_非台风_降水分相_干湿_抽样50%", cluster = CL, lean = TRUE))
  rm(x); gc()
}
# N7d：含小雨的动态模型按距离档分样本（50% 连接抽样），供计入滞后效应的损失；T5v：主口径 T5 重跑一遍只为保存协方差
if (run("N7d")) {
  tags <- c("F7", "F3", "F2", "F1", "L0", "L1", "L2", "L3", "L7")
  v <- as.vector(outer(c("m01_", "m10_", "m25_"), tags, paste0))
  vv <- c(paste0(v, "_o"), paste0(v, "_d"))
  x <- read_ntc(od_cols(vv, "dband"), frac = 0.5)
  for (g in 0:4) {
    nm <- sprintf("N7d_非台风_动态含小雨_距离_抽样50%%_dband%d", g)
    m <- feols(as.formula(paste("ln_flow ~", paste(vv, collapse = " + "), "|", FE)), x[dband == g], cluster = CL, lean = TRUE)
    save(tidy(m, nm)); save_vcov(m, nm); rm(m); gc()
  }
  rm(x); gc()
}
# H：按日类型分样本（dtype：1 工作日 / 2 周末 / 3 节假日，04 依国务院放假安排生成），检验随意性出行更多的日子是否更敏感；
#    H5 再在 300 km 以内的短连接上分日类型
if (run("H")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "dtype", "dband"))
  save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x, "dtype", "H_非台风_日类型", cluster = CL, lean = TRUE))
  gc()
  save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x[dband <= 1], "dtype", "H5_非台风_300km内_日类型", cluster = CL, lean = TRUE))
  rm(x); gc()
}
# X：OD 占比的机械溢出（盲审意见 2）。若 OD 流量 = 起点规模 × 目的地占比，终点下雨压低本连接占比时，
#    同一起点其余连接的占比会被动抬高，对照组受正向溢出。加入起点其余目的地、终点其余来源地当天小雨、中雨、
#    ≥25 mm 的流量加权份额（04 的 wdx_*、wox_*，不含本连接的另一端）。溢出存在时这些系数为正，且起终点系数
#    应明显变小；与同一样本的 T2 比较
if (run("X")) {
  sp <- as.vector(outer(c("wdx_", "wox_"), c("m01", "m10", "m25"), paste0))
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", sp))
  save(tidy(feols(as.formula(paste("ln_flow ~", B, "+", paste(sp, collapse = " + "), "|", FE)), x, cluster = CL, lean = TRUE),
            "X1_非台风_伙伴降雨溢出"))
  rm(x); gc()
}
# V：沿线降水（盲审意见 5）。距离衰减也可能来自路径暴露：长途时两端降雨只覆盖路程的一小段。
#    在 300 km 以上的连接上加入两端连线中点最近城市（100 km 内、不含两端）的降雨分档 ab_m，按距离档分样本；
#    同一样本上先跑不含中点降雨的 V0 作对照。日常口径下再剔除中点为易降雪日的连接-日
if (run("V")) {
  x <- read_ntc(c(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "dband", "ab_m"), if (EVD) paste0(SNOW, "_m")))
  x <- x[dband >= 2 & ab_m >= 0]
  if (EVD) x <- x[get(paste0(SNOW, "_m")) == 0]
  gc()
  save(fit_split(as.formula(paste("ln_flow ~", B, "|", FE)), x, "dband", "V0_非台风_中点样本", cluster = CL, lean = TRUE))
  gc()
  save(fit_split(as.formula(paste("ln_flow ~", B, "+ i(ab_m, ref = 0) |", FE)), x, "dband", "V1_非台风_含中点降雨",
                 cluster = CL, lean = TRUE))
  rm(x); gc()
}
if (run("T5v")) {
  x <- read_ntc(od_cols("ab_o", "ab_d", "c7_o", "c7_d", "dband"))
  for (g in 0:4) {
    m <- feols(as.formula(paste("ln_flow ~", B, "|", FE)), x[dband == g], cluster = CL, lean = TRUE)
    save_vcov(m, sprintf("T5_剔除台风日_距离_dband%d", g)); rm(m); gc()
  }
  rm(x); gc()
}
cat("完成\n")
