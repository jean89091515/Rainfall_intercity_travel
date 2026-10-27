<!-- ppt-master-schema: design-spec/v1 -->
# rain_mobility_advisor - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | rain_mobility_advisor（降雨与城际流动·导师交流） |
| Canvas Format | ppt169 (1280×720) |
| Page Count | 21 |
| Primary Language | zh-CN |
| Target Audience | 导师张老师：熟悉标度律、统计物理和复杂系统方法（人类移动、城市科学方向），对 DIMNet-CPC、ERA5-Land 这两个数据和计量里的固定效应回归不一定熟；更关心现象背后的物理图像、可推广的规律，以及值不值得做成一篇方法上有新意的论文。 |
| Communication Intent | 先用较短篇幅说清两个数据和已经做出的实证结果（剂量-响应、距离、气候适应、时间动态、台风、年度损失），再展示用标度律 / 统计物理语言做的三个初探（距离衰减指数、涨落分布、城市“磁化率”），最后把 7 个候选问题摆出来，请老师判断哪些值得做、怎么做。以讨论和征求意见为主，不是答辩。 |
| Desired Audience Outcome | 老师在 30–40 分钟内看懂数据和主要发现，对候选问题给出优先级判断，指出 1–2 个值得深入的方向和对应的方法，并说明还需要补什么数据（如人口、气温、雨量计观测）。 |
| Core Message / Ask / Action | 降雨对城际流动像一个“弱而普遍的外场”：响应平滑、随距离衰减、被本地气候“适应”掉一部分，台风是另一种机制；这些规律有希望用标度律 / 统计物理的语言统一描述——想请老师帮忙挑问题、定方法。 |
| Delivery Context | 主要是一对一当面或线上共享屏幕交流，约 30–40 分钟，由我讲解、边看边讨论；次要是会后发给老师自行翻阅。 |
| Artifact Afterlife | 会后发给老师参考，作为后续选题讨论和组会汇报的底稿。 |
| Reading Mode | balanced |
| Content Strategy | 未指定（balanced 默认）：按 mode 重组素材为叙事，保留全部事实与数字，不引入素材外的事实 |
| Design Style | 学术研讨·问题驱动（custom mode based on pyramid + custom visual style based on swiss-minimal） |
| AI Image Acquisition Path | not applicable（image_usage = provided only） |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — final Stage-2 proactive policy |
| Custom Animations | disabled — final Stage-2 proactive policy |
| Narration Audio | disabled — final Stage-2 proactive policy |
| Created Date | 2026-10-18 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 左 72（含 8px 章节色带与间隔）、右 56、上 44、下 40 |
| Content Area | x 72–1224，y 44–680 |

## III. Visual Theme

### Theme Style

- **Mode**: custom
- **Mode References**: pyramid
- **Mode Behavior**: 以 pyramid 为基底：结果页用结论句做标题，下面是图和 2–3 个关键数字；全稿按“为什么做 → 数据与方法 → 六个实证发现 → 三个统计物理初探 → 七个候选问题 → 请老师把关”推进，每个发现页角落标注它对应的问题编号（Q1–Q7），候选问题部分每页写清“现象与证据 → 可能的物理框架 → 需要的数据或方法”，结尾落到一个让老师给出优先级的决定页。
- **Visual style**: custom
- **Visual Style References**: swiss-minimal
- **Visual Style Behavior**: 以 swiss-minimal 为基底：白底、12 栏网格、左侧一条窄色带标记所在章节；图作为最大的证据平面，结论标题左对齐；关键量（γ≈2.13、Δγ≈0.02、σ≈0.35、9.5 亿人次）用建筑尺度的大数字呈现；细线分隔、直角、无阴影无渐变，强调色只用于降雨效应和问题编号。
- **Theme**: 学术研讨·问题驱动——图是证据平面，结论句做标题，Q 编号贯穿全稿把“实证发现”连到“候选问题”
- **Tone**: 严谨、克制、开放讨论；像组会报告而不是答辩

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #FFFFFF | 页面底色 |
| Secondary background | #F3F5F7 | 数字侧栏、公式框、表格斑马行等浅色面 |
| Primary | #1F3A5F | 标题、章节色带、主结构线、基线/无雨状态 |
| Accent | #D9622B | 降雨效应、问题编号 Q1–Q7、需要老师注意的点（与图中橙色一致） |
| Secondary accent | #2E7FB8 | 第二序列、雨/水相关的辅助标记、链接性标注 |
| Body text | #1D2430 | 正文 |
| Secondary text | #5B6573 | 图注、来源行、页码、注释 |
| Divider | #D5DAE0 | 细线分隔、表格线 |
| Surface | #F3F5F7 | 侧栏/公式框底面（与 secondary_bg 同值，语义为抬升面） |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | neo-grotesque 无衬线，粗细对比 | Microsoft YaHei | Arial | sans-serif |
| Body | neo-grotesque 无衬线，常规 | Microsoft YaHei | Arial | sans-serif |

- **Title stack**: "Microsoft YaHei", Arial, sans-serif
- **Body stack**: "Microsoft YaHei", Arial, sans-serif

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 22 |
| Title | 38 |
| Subtitle | 30 |
| Annotation | 18 |
| Lead | 24 |
| Footnote | 14 |
| Hero | 64 |
| Cover title | 48 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: 左上结论标题 → 图（最大证据平面）→ 右侧或下方 2–3 个关键数字 → 角落 Q 编号；眼睛从结论走到证据再走到“这和哪个问题有关”。
- **Composition tendency**: 不对称分栏贴靠网格；超宽图（比例 2.6–2.8）通栏放在标题下方，数字带放在图下；较方的图（地图、剂量-响应）占左侧 7–8 栏，右侧为数字侧栏；候选问题部分以表格和编号格为主。
- **Cross-page continuity**: 左侧 8px 章节色带（第一部分 primary、实证 primary、初探 secondary_accent、问题 accent）；每页右上角统一的 Q 编号标签区；底部统一的来源/页码行。
- **Spacing posture**: 内容较满但网格严格（balanced）；过渡页和封面留白。
- **Spacing anchors**: 页边距 56px（左侧另加色带）、块间距 24px、栏间距 24px、圆角 0px、正文行距 33px

## VI. Icon Usage Specification

- **Primary bundled library**: tabler-outline
- **Stroke Width**: 2

| Icon Path | Suitable Scenarios |
| --- | --- |
| icons/tabler-outline/database.svg | |
| icons/tabler-outline/cloud-rain.svg | |
| icons/tabler-outline/route.svg | |
| icons/tabler-outline/map-2.svg | |
| icons/tabler-outline/clock.svg | |
| icons/tabler-outline/cloud-storm.svg | |
| icons/tabler-outline/atom.svg | |
| icons/tabler-outline/math-function.svg | |
| icons/tabler-outline/target.svg | |
| icons/tabler-outline/ruler-measure.svg | |
| icons/tabler-outline/school.svg | |
| icons/tabler-outline/checklist.svg | |
| icons/tabler-outline/arrow-right.svg | |
| icons/tabler-outline/ripple.svg | |
| icons/tabler-outline/chart-dots.svg | |
| icons/tabler-outline/network.svg | |
| icons/tabler-outline/thermometer.svg | |
| icons/tabler-outline/building-community.svg | |
| icons/tabler-outline/chart-line.svg | |
| icons/tabler-outline/question-mark.svg | |

## VII. Visualization Reference List

| Page | Family | Template | Usage |
| --- | --- | --- | --- |
| P18 | table | comparison_matrix | 候选问题 Q1–Q4 × 现象与证据 / 物理框架 / 数据与方法 的对照 |
| P19 | table | comparison_matrix | 候选问题 Q5–Q7 × 现象与证据 / 物理框架 / 数据与方法 的对照 |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fig1_study_area.png | 1452×1103 | 1.32 | 研究区：365 城按年均降水着色，800 mm 湿润区界线 | Figure | 左侧主图 + 右侧数字侧栏 | no-crop | user | Existing | 论文中文版图 1；含审图号，完整显示 | none | local |
| fig2_dose_response.png | 1416×849 | 1.67 | 非台风日起点/终点降雨的剂量-响应 | Figure | 左侧 2/3 主图 + 右侧数字侧栏 | no-crop | user | Existing | 论文中文版图 2 | none | local |
| fig3_distance.png | 2124×825 | 2.57 | 各雨档效应随距离的变化（a 起点 b 终点） | Figure | 通栏图 + 下方数字带 | no-crop | user | Existing | 论文中文版图 3 | none | local |
| fig4_climate.png | 2244×801 | 2.80 | 气候与区域：绝对分档、本地分位数分档、区域 | Figure | 通栏图 + 下方数字带 | no-crop | user | Existing | 论文中文版图 4 | none | local |
| fig5_dynamics.png | 2124×801 | 2.65 | 降雨前后各日的流量变化（含 ±7 天安慰剂） | Figure | 通栏图 + 下方数字带 | no-crop | user | Existing | 论文中文版图 5 | none | local |
| fig6_losses.png | 2124×777 | 2.73 | 年度损失按雨档、按距离 | Figure | 通栏图 + 上方大数字 | no-crop | user | Existing | 论文中文版图 6 | none | local |
| fig7_typhoon.png | 2124×825 | 2.57 | 全部日 vs 非台风日的剂量-响应对比 | Figure | 通栏图 + 下方数字带 | no-crop | user | Existing | 论文中文版图 7 | none | local |
| scaling_a_distance_decay.png | 2200×836 | 2.63 | 初探 A：距离衰减 γ 与降雨引起的 Δγ | Figure | 通栏图 + 下方公式与大数字 | no-crop | user | Existing | 12_标度律初探.py 图 A | none | local |
| scaling_b_fluctuation.png | 2200×836 | 2.63 | 初探 B：不同雨档下的涨落分布与左尾 | Figure | 通栏图 + 下方大数字 | no-crop | user | Existing | 12_标度律初探.py 图 B | none | local |
| scaling_c_city_susceptibility.png | 2200×836 | 2.63 | 初探 C：城市“磁化率”与规模、气候 | Figure | 通栏图 + 下方大数字 | no-crop | user | Existing | 12_标度律初探.py 图 C | none | local |

## IX. Content Outline

### Part 1: 开场

#### Slide 01 - 封面

- **Audience move**: 老师知道这次是什么题目、我想要什么 → 带着“雨天少走 9.5 亿人次、能不能用物理语言描述”的好奇进入
- **Relationships**: none
- **Layout**: 大面积留白；左侧 primary 色块或粗色带；一个建筑尺度的“9.5 亿”作为钩子，完整标题作为原生文字
- **Title**: 降雨与中国城际人口流动
- **Core message**: 日常降雨每年让中国城际出行少约 9.5 亿人次——这种“弱而普遍的外场”能否用标度律 / 统计物理的语言描述？
- **Content**: 副标题：初步结果，以及想请教张老师的标度律 / 统计物理问题 · 钩子数字：9.5 亿人次 / 年（非台风日、稳定连接、下限）· 汇报人：[姓名] · 2026 年 10 月
- **Cover impact**: 以“9.5 亿人次 / 年”大数字为钩子（binding），构图为左侧大数字 + 右侧标题的不对称分割（Reference）

#### Slide 02 - 今天想聊的三件事

- **Audience move**: 不清楚汇报结构 → 知道三段内容和最后要老师做的判断
- **Relationships**: order: 数据与结果 → 统计物理初探 → 候选问题与请教（三段顺序推进，最后一段是请求）
- **Layout**: 三个编号区块横向排开，第三块用 accent 强调“需要老师判断”；下方一行时间分配
- **Title**: 今天想和老师聊三件事
- **Core message**: 先快速过数据和结果，再看三个物理视角的初探，重点是请老师挑问题
- **Content**: ① 两个数据与六个实证发现（约 12 分钟）· ② 用标度律 / 统计物理语言做的三个初探（约 8 分钟）· ③ 七个候选问题，请老师判断优先级与方法（约 15 分钟）· 背景：之前微信说过“整理后再详细汇报”

### Part 2: 为什么做与数据

#### Slide 03 - 研究缺口

- **Audience move**: 不清楚这个题目的位置 → 看到两类已有研究各缺什么，以及本研究补哪里
- **Relationships**: contrast: 已有研究 A（日常天气 × 城内出行）与 B（极端事件 × 移动韧性）各自的局限；membership: 四个缺口同属“城际 × 日常降雨”空白
- **Layout**: 左右两栏对照已有研究，下方横跨一条“缺口”带列四点
- **Title**: 降雨如何影响“城市之间”的出行，还缺全国证据
- **Core message**: 已有研究要么只看城内、要么一次只看一个极端事件；城际 × 日常降雨是空白
- **Content**: 研究 A：日常天气与城内出行（公交、出租、骑行；多为单城市单方式）· 研究 B：极端事件下的移动韧性（飓风 Sandy、2021 郑州暴雨、台风“玛娃”，一次一个事件）· 缺口：普通小雨中雨的累计影响 / 起点雨与终点雨 / 远近与交通方式 / 南北气候差异 / 台风与普通降雨未分开 · 窗口：DIMNet-CPC 2026 年 9 月刚发表

#### Slide 04 - 两个数据加一个辅助数据

- **Audience move**: 不熟悉数据 → 知道流量怎么来、降雨怎么来、台风怎么定义，以及各自的坑
- **Relationships**: membership: 三个数据源共同构成面板；link: k_t 被日期固定效应吸收 → 百分比效应由百度相对强度识别
- **Layout**: 三栏数据卡（DIMNet-CPC 最宽），每栏一个图标、要点和一个“注意”行；公式放在 DIMNet 栏
- **Title**: 两个主数据：逐日 OD 流量 + 站点位置的再分析降水
- **Core message**: 流量是校准后的百度迁徙强度，降雨是 ERA5-Land 站点提取；两者都是北京时日
- **Content**: DIMNet-CPC：Xu et al. 2026 Sci Data，366 个地级及以上单元，2020—2025，逐日有向 OD（人次），把百度迁徙相对强度校准到全国逐日旅客统计；只披露前 100 名流出/流入地，缺失 = 未披露 · ERA5-Land（地联社整理）：2421 站位置提取，0.1°≈9 km，1950—2026，北京时日累加；36 个沿海/海岛站全为 0 剔除，保留 2385 站；城市取站点均值（中位 6 站）；高估小雨频率、低估极端 · IBTrACS：西北太平洋路径，3 小时一个位置；气旋中心（含残余低压）距城市 ≤500 km 记为台风日（300 km 稳健性）
- **Mathematical content**: F_{ijt} = k_t \, q_{ijt}

#### Slide 05 - 样本

- **Audience move**: 不知道样本有多大 → 记住 26,442 条稳定连接、2878 万连接-日、短连接承载一半流量
- **Relationships**: parent: 132,622 条曾出现连接 → 26,442 条稳定连接（≥95% 天数披露）；contrast: <150 km 连接占 6% 数量却占 49.9% 流量
- **Layout**: 左侧研究区地图（完整显示），右侧数字侧栏 4–5 个关键数
- **Title**: 2.6 万条稳定连接承载了 98% 的流量
- **Core message**: 用“稳定连接”避开披露门槛造成的截断偏误，样本仍覆盖几乎全部流量
- **Content**: 2023-01-01 至 2025-12-31，1096 天，无缺失、无疫情管控 · 365 城（剔除三沙）· 26,442 条稳定有向连接，占 98.0% 流量 · 2878 万连接-日 · <150 km：6% 的连接、49.9% 的流量 · 连接日流量中位数 709 人次，距离中位数 552 km · 湿润区（年降水 ≥800 mm）225 城，大致秦岭—淮河以南
- **Images**: fig1_study_area.png 完整显示，作为左侧主图

#### Slide 06 - 识别策略

- **Audience move**: 不熟悉固定效应回归 → 理解“同一条连接在不同日子之间比较”这一识别思路和主口径
- **Relationships**: link: 每类固定效应吸收一种干扰（季节/周内/全国冲击）；order: 全部日 → 剔除台风日 = 主口径
- **Layout**: 上方公式框（secondary_bg）通栏；下方三栏解释：降雨分档 / 固定效应吸收什么 / 推断与稳健性
- **Title**: 识别：同一条连接，下雨的日子和不下雨的日子比
- **Core message**: 用高维固定效应吸收季节、周内和全国冲击，剩下的逐日降雨变化近似随机
- **Content**: 降雨分档（GB/T 28592-2012）：无雨 / 小雨 0.1–10 / 中雨 10–25 / 大雨 25–50 / 暴雨 50–100 / ≥100 mm；另有本地 P75/P90/P95/P99 分档 · 前 7 日累计降水分档控制“连阴雨”· 连接×年月：季节与趋势；连接×星期：通勤与周末；日期：节假日、春运、k_t · 主口径：非台风日（两端 500 km 内无气旋），2807 万观测 · 起点+终点双向聚类；30% 连接样本上加日期三向聚类 · 稳健性：PPML、连接×周 FE、台风半径 300 km、去掉前期降水
- **Mathematical content**: \ln F_{ijt} = \sum_{b=1}^{5}\beta^{O}_{b}\,\mathbf{1}[R_{it}\in b] + \sum_{b=1}^{5}\beta^{D}_{b}\,\mathbf{1}[R_{jt}\in b] + \sum_{c}\gamma_{c}\,\mathbf{1}[A_{it},A_{jt}\in c] + \mu_{ij,m(t)} + \eta_{ij,w(t)} + \lambda_{t} + \varepsilon_{ijt}

### Part 3: 六个实证发现

#### Slide 07 - 剂量-响应

- **Audience move**: 不知道效应多大 → 记住“小雨约 −1%、暴雨 −4%~−6%，终点雨略强”
- **Relationships**: order: 雨档由小到大对应效应单调变大；contrast: 起点降雨 vs 终点降雨
- **Layout**: 左侧剂量-响应图，右侧数字侧栏；右上角 Q 标签 Q3·Q4
- **Title**: 流量随雨强平滑下降，终点下雨影响略大
- **Core message**: 非台风日，降雨对城际流量是一条平滑的剂量-响应曲线
- **Content**: 起点：小雨 −0.6% · 中雨 −1.9% · 大雨 −2.3% · 暴雨 −4.0% · ≥100 mm −5.5%（不显著，仅 50 个非台风城市-日）· 终点：−1.0% · −1.8% · −3.1% · −6.0% · −8.8% · 城市总流出：小雨 −1.9%，暴雨 −6.3% · 三向聚类下除起点 ≥100 mm 外均在 5% 水平显著 · 物理视角：一条光滑的响应函数 → Q3、Q4
- **Images**: fig2_dose_response.png 完整显示

#### Slide 08 - 距离

- **Audience move**: 以为远近一样 → 看到短途最敏感、损失集中在 300 km 以内
- **Relationships**: order: 距离档由近到远效应递减；contrast: <150 km vs >1000 km
- **Layout**: 通栏图，下方数字带三格；Q 标签 Q2
- **Title**: 越短的出行越怕雨：损失的 89% 在 300 km 以内
- **Core message**: 降雨效应随距离衰减，短途连接既最敏感又承载最多流量
- **Content**: 起点暴雨：<150 km −8.4%，>1000 km −2.0%；起点中雨：−4.1% vs −0.8% · 终点暴雨：<150 km −8.5%，500–1000 km −4.3%；>1000 km 略回升 · 300 km 以内连接承担非台风日损失的 89% · 物理视角：降雨改变了距离衰减的形状 → Q2
- **Images**: fig3_distance.png 通栏完整显示

#### Slide 09 - 气候适应

- **Audience move**: 以为同样的雨影响相同 → 看到越干的地方越敏感，且重标度后差距缩小但不消失
- **Relationships**: contrast: 湿润区起点 vs 非湿润区起点；link: 改用本地分位数（重标度）→ 差距缩小；membership: 四大区域
- **Layout**: 通栏三联图，下方数字带；Q 标签 Q3·Q1
- **Title**: 同样的雨，越干的地方越敏感
- **Core message**: 存在气候适应；用本地气候尺度重标度后差距缩小但不消失
- **Content**: 非湿润区起点：小雨 −1.2% · 中雨 −3.0% · 大雨 −4.2% · 暴雨 −6.0%；湿润区：0.0% · −1.4% · −1.5% · −3.3% · 本地 P95–P99：湿润区 −1.4%，非湿润区 −3.4% · 区域（暴雨）：东北 −8.3%、西部 −5.2%、东部 −3.6%、中部 −2.5% · 物理视角：部分“数据塌缩” → Q3
- **Images**: fig4_climate.png 通栏完整显示

#### Slide 10 - 时间动态

- **Audience move**: 以为只是改期 → 看到出行被取消，1–2 天恢复且无反弹
- **Relationships**: order: 雨前 → 当天 → 次日 → 之后；contrast: 中雨安慰剂干净 vs ≥25 mm 有约 1 个百分点残余
- **Layout**: 通栏图，下方数字带；Q 标签 Q6
- **Title**: 下雨取消出行，而不是推迟
- **Core message**: 扰动后 1–2 天恢复，没有补偿性反弹
- **Content**: 起点 ≥25 mm：当天 −1.6%，次日 −2.2%，之后恢复无反弹 · 终点 ≥25 mm：当天 −2.6%，次日 −1.6% · 雨前一天流向目的地 −0.8%（p = 0.06），像在看天气预报 · ±7 天安慰剂：中雨干净；≥25 mm 有约 1 个百分点残余（小雨结论需谨慎）· 物理视角：弛豫函数 → Q6
- **Images**: fig5_dynamics.png 通栏完整显示

#### Slide 11 - 台风

- **Audience move**: 以为极端降雨效应就是降雨效应 → 看到台风日是另一种机制（供给侧停运）
- **Relationships**: contrast: 全部日 vs 非台风日；link: 台风日 → 预警、停运 → 额外下降
- **Layout**: 通栏对比图，下方数字带；Q 标签 Q5·Q7
- **Title**: 台风日只占 2.5%，却制造了“极端降雨”的大部分效应
- **Core message**: 剔除台风日后，≥100 mm 的效应从约 −25% 缩到 −6%~−9%；台风是供给侧冲击
- **Content**: ≥100 mm 的城市-日中 70% 是台风日（湿润区 75%，较干城市 20%）· 全部日：≥100 mm 起点 −22.4%、终点 −27.1% → 剔除台风日：−5.5%、−8.8% · 同样的雨在台风日额外再降 24%（起点）/ 32%（终点）；台风影响下终点小雨也额外 −6.5% · 混在一起会制造两个假象：长途也大降、湿润区反而更敏感 · 物理视角：强而空间相关的扰动 → Q5、Q7
- **Images**: fig7_typhoon.png 通栏完整显示

#### Slide 12 - 年度损失

- **Audience move**: 以为暴雨最要紧 → 看到频繁的小雨中雨才是损失大头
- **Relationships**: membership: 年度损失按雨档分解；contrast: 中雨（2.36 亿）vs 暴雨+≥100 mm（0.37 亿）
- **Layout**: 上方大数字“9.5 亿”与分解数字，下方通栏损失图；Q 标签 Q7
- **Title**: 日常降雨每年少走约 9.5 亿人次，大头是小雨和中雨
- **Core message**: 损失来自频繁的小扰动，而不是少数大扰动
- **Content**: 非台风日 9.54 亿 + 台风日降雨 1.27 亿 = 10.8 亿人次 / 年，占无雨反事实 2.2%（稳定连接，下限）· 小雨 5.77 亿（61%）· 中雨 2.36 亿（25%）· 暴雨 + ≥100 mm 0.37 亿（4%）· 仅中雨就是暴雨+大暴雨的约 6 倍 · 论文进展：英文 TR Part D 初稿 + 中英文 Word 已完成；待补气温、雨量计稳健性 · 物理视角：频率-强度-损失 → Q7
- **Images**: fig6_losses.png 通栏完整显示

### Part 4: 用统计物理语言重看

#### Slide 13 - 换一种语言

- **Audience move**: 只看到计量结果 → 看到每个结果在统计物理里对应什么概念
- **Relationships**: link: 计量结果 → 统计物理概念 的一一对应（五对）
- **Layout**: 过渡页：左侧一句核心判断（大字），右侧五行“计量语言 → 物理语言”对照，用箭头连接；secondary_accent 色带
- **Title**: 换一种语言：把降雨看成一个弱而普遍的外场
- **Core message**: 同一组结果可以用响应函数、标度指数、数据塌缩、弛豫和相关扰动来描述
- **Content**: 剂量-响应曲线 → 响应函数 / 磁化率 χ · 效应随距离衰减 → 距离衰减指数 γ 被外场改变 · 本地分位数分档 → 重标度与数据塌缩 · 当天/次日/恢复 → 弛豫函数 · 台风 → 强而空间相关的扰动 · 定义：外场 h = 降雨强度，响应 = ⟨ln F⟩ 的变化
- **Mathematical content**: \chi = \partial \langle \ln F \rangle / \partial h

#### Slide 14 - 初探 A：距离衰减

- **Audience move**: 不知道降雨与引力模型的关系 → 记住 γ≈2.13，雨天 Δγ≈+0.02，以及 >1000 km 的交叉
- **Relationships**: link: 降雨效应对 ln d 的斜率 = Δγ；contrast: 晴天 γ vs 雨天 γ − Δγ
- **Layout**: 通栏双联图，下方左公式框、右三个大数字；Q 标签 Q2
- **Title**: 初探 A：雨天，距离衰减变平
- **Core message**: F ∝ d^−γ 中 γ≈2.13；降雨使 γ 减小约 0.02–0.03，且 >1000 km 处存在交叉
- **Content**: 稳定连接，去掉起终点固定效应：γ ≈ 2.13 · 用流动“质量”替代：F ∝ M_i^0.59 M_j^0.58 d^−1.51 · Δγ（终点）：中雨 +0.014、大雨 +0.017、暴雨 +0.018；起点暴雨 +0.030 · >1000 km 衰减变平，像存在交叉尺度（高铁 / 航空接管？）· 未经推敲的初探
- **Mathematical content**: F_{ij} \propto M_i^{\alpha} M_j^{\beta} d_{ij}^{-\gamma}, \quad \gamma_{\mathrm{rain}} = \gamma - \Delta\gamma
- **Images**: scaling_a_distance_decay.png 通栏完整显示

#### Slide 15 - 初探 B：涨落分布

- **Audience move**: 以为降雨是主导因素 → 看到它在很大的自发涨落里只是很弱的位移
- **Relationships**: contrast: 自发涨落 σ≈0.35 vs 暴雨平均位移 ≈ −0.04；order: 雨档增大 → 左尾 10%–45% 段加厚
- **Layout**: 通栏双联图，下方三个大数字（σ、位移、信噪比）；Q 标签 Q4
- **Title**: 初探 B：降雨是一个很弱的外场
- **Core message**: 信噪比约 0.1：降雨让分布整体左移、增加中等幅度的下降，而最大的下降多来自节假日等其他冲击
- **Content**: 去掉连接×年月、日期、连接×星期均值后的逐日对数偏差 ε · σ ≈ 0.35；暴雨及以上平均位移 ≈ −0.04 · 分布中心呈指数型尾部（对数坐标近似三角形）· P(下降 > 30%)：两端无雨 10.3% → 暴雨及以上 12.5% · 更大的下降（> 45%）在无雨日一样多
- **Images**: scaling_b_fluctuation.png 通栏完整显示

#### Slide 16 - 初探 C：城市“磁化率”

- **Audience move**: 以为大城市更稳或更脆 → 看到敏感度几乎不随规模变、强烈随气候变
- **Relationships**: contrast: 规模斜率 +0.8 vs 气候斜率 +12.7（每 10 倍）；link: 长期外场强度 → 响应被“适应”掉
- **Layout**: 通栏双联散点图，下方两个大数字对比；Q 标签 Q1·Q3
- **Title**: 初探 C：城市“磁化率”取决于气候，不取决于规模
- **Core message**: 没有明显的规模标度，但有很强的“气候标度”
- **Content**: χ_i：≥25 mm 日相对无雨日的城市总流出变化（非台风日，≥10 个大雨日，270 城），中位数 −5.1% · 规模每增加 10 倍：+0.8 个百分点（几乎不变）· 年降水每增加 10 倍：敏感度减弱 12.7 个百分点；同时放入：规模 +1.6、降水 +13.2 · 解读：系统对外场的响应被它长期经历的外场强度“适应”掉
- **Mathematical content**: \chi_i = \exp\left(\bar{\varepsilon}_{i,\ge 25\,\mathrm{mm}} - \bar{\varepsilon}_{i,\mathrm{dry}}\right) - 1
- **Images**: scaling_c_city_susceptibility.png 通栏完整显示

### Part 5: 想请教老师的问题

#### Slide 17 - 七个候选问题总览

- **Audience move**: 看过证据 → 一眼看到七个问题分三组，以及各自的证据页
- **Relationships**: membership: 标度与模型（Q1、Q2）/ 普适性与响应（Q3、Q4）/ 网络与动力学（Q5、Q6、Q7）；link: 每个问题 → 对应证据页
- **Layout**: 三组分栏，每个问题一个编号格（Q 编号 accent），格内一句话问题 + 证据页码
- **Title**: 七个候选问题，分三组
- **Core message**: 从实证结果自然引出七个标度律 / 统计物理问题
- **Content**: Q1 城市标度律：雨天 Y ∝ N^β 的 β 变不变？（P16）· Q2 引力 vs 辐射模型：降雨改的是 γ、质量项还是交叉尺度？（P08、P14）· Q3 数据塌缩：用本地气候尺度重标度后能否塌缩到一条主曲线？（P09、P16）· Q4 线性响应与涨落：自发涨落与敏感度有无类似涨落-耗散的关系？（P07、P15）· Q5 空间关联与网络：相关扰动下的网络渗流与级联？（P11）· Q6 弛豫动力学：恢复是指数型还是幂律型？（P10）· Q7 频率-强度统计：损失分布有无幂律尾？（P12）

#### Slide 18 - 候选问题详解（一）

- **Audience move**: 只知道问题名 → 清楚 Q1–Q4 各自的证据、可能的物理框架和所需数据
- **Relationships**: membership: Q1–Q4 各自的三项属性（证据 / 框架 / 数据）
- **Layout**: 对照表通栏，问题编号列 accent
- **Title**: 候选问题详解（一）：标度、模型、塌缩、响应
- **Core message**: Q1–Q4 都能用现有数据起步，Q1 需补人口
- **Content**: Q1 现象：敏感度几乎与流动规模无关 / 框架：城市标度律 Y ∝ N^β，比较雨天与晴天的 β / 需要：七普人口 · Q2 现象：效应随距离衰减、Δγ≈0.02、>1000 km 交叉 / 框架：引力模型与辐射模型（中间机会），降雨是否缩小“有效机会半径” / 需要：机制模型推出 Δγ 量级 · Q3 现象：本地分位数重标度后差距缩小但不消失 / 框架：重标度变量（P99、重现期、标准化距平）下的数据塌缩 / 需要：选择合适的标度变量 · Q4 现象：σ≈0.35 远大于平均响应 / 框架：线性响应、涨落-耗散类比、敏感度分布是否重尾 / 需要：连接层面的响应估计
- **Visualization**: questions-1 = 4 行 × 4 列对照表（问题 | 现象与已有证据 | 可能的物理框架 | 需要的数据或方法）
- **Native-ready**: questions-1=yes

#### Slide 19 - 候选问题详解（二）

- **Audience move**: 继续 → 清楚 Q5–Q7 的证据、框架和难点
- **Relationships**: membership: Q5–Q7 各自的三项属性（证据 / 框架 / 数据）
- **Layout**: 对照表通栏，问题编号列 accent
- **Title**: 候选问题详解（二）：网络、弛豫、频率-强度
- **Core message**: Q5–Q7 方法上更“物理”，但需要更多建模工作
- **Content**: Q5 现象：降雨场空间相关强，同一天很多城市同时下雨；台风是强相关扰动 / 框架：网络上的相关扰动、渗流与巨连通分量、向第三方城市的级联 / 需要：逐日网络重构、空间相关长度估计 · Q6 现象：扰动后 1–2 天恢复、无反弹 / 框架：弛豫函数形式（指数 vs 幂律），联系 Wang & Taylor 关于扰动下移动规律保持的结论 / 需要：事件对齐的恢复曲线 · Q7 现象：小雨中雨占损失 86%，台风是少数大扰动 / 框架：类 G-R 律的“强度—频率—损失”统一描述，损失分布是否有幂律尾 / 需要：事件层面的损失分布
- **Visualization**: questions-2 = 3 行 × 4 列对照表（问题 | 现象与已有证据 | 可能的物理框架 | 需要的数据或方法）
- **Native-ready**: questions-2=yes

#### Slide 20 - 请老师把关

- **Audience move**: 看完问题 → 老师按价值 × 可行性给出排序，并回答四件事
- **Relationships**: contrast: 研究价值 × 可行性 两个维度；membership: 四件请教事项
- **Layout**: 左侧 2×2 优先级矩阵（横轴可行性、纵轴价值），Q1–Q7 圆标按我的初步判断摆放并注明“请老师修正”；右侧四件请教事项编号列表
- **Title**: 想请老师帮我判断：先做哪一两个？
- **Core message**: 我的初步判断是 Q2、Q3 价值高且现有数据能做，但最终想听老师意见
- **Content**: 矩阵初步摆放（我的判断，非数据）：高价值高可行 Q2、Q3；高价值中可行 Q4；高价值低可行 Q5；中价值高可行 Q6、Q7；中价值需补数据 Q1 · 请教 1：哪一两个问题最值得做成统计物理 / 复杂系统风格的论文？和 TR-D 实证稿怎么分工？· 请教 2：固定效应给的是平均响应，统计物理的做法该怎么补（分布、标度、塌缩、模型）？· 请教 3：需要补哪些数据（人口、气温、雨量计、交通方式）？· 请教 4：投稿方向的建议
- **Data class**: scenario — 矩阵中 Q1–Q7 的位置是汇报人的主观初步判断，不是数据

### Part 6: 收尾

#### Slide 21 - 下一步

- **Audience move**: 讨论结束 → 知道我接下来会做什么、什么时候再汇报
- **Relationships**: order: 近期（完善 TR-D 稿）→ 按老师意见挑 1–2 个问题做最小可行分析 → 再定论文定位
- **Layout**: 左侧核心信息复述（大字），右侧三步时间线
- **Title**: 下一步
- **Core message**: 实证稿继续推进；物理视角的论文按老师意见先做最小可行分析
- **Content**: 近期：补气温控制和雨量计数据稳健性，完善 TR Part D 稿 · 按老师意见挑 1–2 个标度律 / 统计物理问题，先做最小可行分析 · 再定论文定位与投稿方向，下次组会汇报 · 复述：降雨是一个弱而普遍的外场——想把它的规律用物理语言讲清楚
- **Closing impact**: 以核心信息复述 + 三步计划收尾（binding takeaway）；构图为左大字右时间线（Reference）

## X. Speaker Notes Requirements

- **Generation**: enabled
- **Filename**: match each SVG filename under `notes/`
- **Content**: 依据每页最终 SVG 和素材 `sources/导师交流_素材.md` 写讲稿；数字与素材一致，不引入素材外的事实；初探部分要说明“未经推敲”
- **Total duration**: 约 35 分钟（第一段约 12 分钟、第二段约 8 分钟、第三段约 15 分钟）
- **Notes style**: 口语化但严谨，像跟导师当面讲；每页先说结论，再讲 1–2 个数字，最后一句过渡到下一页或对应的问题
- **Presentation purpose**: 汇报数据与实证结果，展示三个统计物理初探，请老师判断候选问题的优先级与方法
