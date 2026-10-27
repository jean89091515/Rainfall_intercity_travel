<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: 导师张老师，熟悉标度律与统计物理，不熟悉这两个数据和固定效应回归
- objective: 简要汇报数据与六个实证发现，展示三个统计物理初探，摆出七个候选问题，让老师在 30–40 分钟内给出优先级、1–2 个值得深入的方向、方法建议和需补的数据
- core_message: 降雨对城际流动像一个弱而普遍的外场——响应平滑、随距离衰减、被本地气候适应，台风是另一种机制；想请老师帮忙挑问题、定方法
- consumption_mode: balanced

## mode
- mode: custom
- mode_references: pyramid
- mode_behavior: 以 pyramid 为基底：结果页用结论句做标题，下面是图和 2–3 个关键数字；全稿按“为什么做 → 数据与方法 → 六个实证发现 → 三个统计物理初探 → 七个候选问题 → 请老师把关”推进，每个发现页角落标注它对应的问题编号（Q1–Q7），候选问题部分每页写清“现象与证据 → 可能的物理框架 → 需要的数据或方法”，结尾落到一个让老师给出优先级的决定页。

## visual_style
- visual_style: custom
- visual_style_references: swiss-minimal
- visual_style_behavior: 以 swiss-minimal 为基底：白底、12 栏网格、左侧一条窄色带标记所在章节；图作为最大的证据平面，结论标题左对齐；关键量（γ≈2.13、Δγ≈0.02、σ≈0.35、9.5 亿人次）用建筑尺度的大数字呈现；细线分隔、直角、无阴影无渐变，强调色只用于降雨效应和问题编号。

## colors
- background: #FFFFFF
- secondary_bg: #F3F5F7
- primary: #1F3A5F
- accent: #D9622B
- secondary_accent: #2E7FB8
- body_text: #1D2430
- secondary_text: #5B6573
- divider: #D5DAE0
- surface: #F3F5F7

## typography
- font_family: "Microsoft YaHei", Arial, sans-serif
- title_family: "Microsoft YaHei", Arial, sans-serif
- body_family: "Microsoft YaHei", Arial, sans-serif
- body: 22
- title: 38
- subtitle: 30
- annotation: 18
- lead: 24
- footnote: 14
- hero: 64
- cover_title: 48

## icons
- library: tabler-outline
- stroke_width: 2
- inventory: tabler-outline/database, tabler-outline/cloud-rain, tabler-outline/route, tabler-outline/map-2, tabler-outline/clock, tabler-outline/cloud-storm, tabler-outline/atom, tabler-outline/math-function, tabler-outline/target, tabler-outline/ruler-measure, tabler-outline/school, tabler-outline/checklist, tabler-outline/arrow-right, tabler-outline/ripple, tabler-outline/chart-dots, tabler-outline/network, tabler-outline/thermometer, tabler-outline/building-community, tabler-outline/chart-line, tabler-outline/question-mark

## images
- p05: images/fig1_study_area.png | source=user | crop=no-crop
- p07: images/fig2_dose_response.png | source=user | crop=no-crop
- p08: images/fig3_distance.png | source=user | crop=no-crop
- p09: images/fig4_climate.png | source=user | crop=no-crop
- p10: images/fig5_dynamics.png | source=user | crop=no-crop
- p12: images/fig6_losses.png | source=user | crop=no-crop
- p11: images/fig7_typhoon.png | source=user | crop=no-crop
- p14: images/scaling_a_distance_decay.png | source=user | crop=no-crop
- p15: images/scaling_b_fluctuation.png | source=user | crop=no-crop
- p16: images/scaling_c_city_susceptibility.png | source=user | crop=no-crop

## page_rhythm
- P01: anchor
- P02: breathing
- P03: dense
- P04: dense
- P05: dense
- P06: dense
- P07: dense
- P08: dense
- P09: dense
- P10: dense
- P11: dense
- P12: anchor
- P13: breathing
- P14: dense
- P15: dense
- P16: dense
- P17: dense
- P18: dense
- P19: dense
- P20: anchor
- P21: breathing

## page_visualizations
- P18: table/comparison_matrix
- P19: table/comparison_matrix

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
