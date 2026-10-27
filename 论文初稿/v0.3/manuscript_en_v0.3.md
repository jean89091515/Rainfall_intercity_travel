---
title: "Everyday rain, not just storms: Rainfall and intercity travel in China"
---

::: {custom-style="Author"}
[Author 1]^a^, [Author 2]^b^, [Corresponding author]^a,\*^
:::

::: {custom-style="Author"}
^a^ [Affiliation, city, postcode, country]
:::

::: {custom-style="Author"}
^b^ [Affiliation, city, postcode, country]
:::

::: {custom-style="Author"}
\* Corresponding author. E-mail: [address]
:::


# Highlights

- Daily rain cuts intercity flows in China, from −1% (light) to −9% (≥100 mm).

- Rain effects decay with distance; trips under 150 km respond most.

- Cities in drier climates are more sensitive to the same rainfall.

- Typhoon days (2.5% of OD-days) drive most extreme-rainfall disruption.

- Everyday rain, mostly light or moderate, removes 0.7–1.0 billion trips a year.


# Abstract

Research on weather and mobility has focused on travel within cities and on single extreme events. We estimate how daily rainfall affects intercity travel across China, using 28.8 million daily origin–destination (OD) observations on 26,442 stable links among 365 prefecture-level cities in 2023–2025. Flows come from DIMNet-CPC, a calibrated daily intercity mobility dataset; rainfall comes from ERA5-Land totals at 2,385 weather-station locations. Effects are identified from day-to-day rainfall variation within OD links, net of link-by-month, link-by-weekday and date fixed effects, and typhoon-influenced days are separated using IBTrACS tracks. On non-typhoon days, flows fall smoothly with rainfall intensity: by about 1% in light rain at the destination, 2% in moderate rain and 4–6% in rainstorms (50–100 mm). Effects decay with distance: rainstorms cut flows within 150 km by 8.5% but long-haul flows by only 2–7%. Cities in drier climates respond more strongly to the same rainfall, consistent with adaptation. Typhoon days, 2.5% of OD-days, account for most extreme-rainfall disruption; excluding them shrinks the effect of ≥100 mm rain from about −25% to between −6% and −9%. In aggregate, everyday rain removes an estimated 0.7–1.0 billion intercity trips a year, mainly through frequent light and moderate rain rather than rare extremes. Results hold with temperature and antecedent-rainfall controls, finer time fixed effects, Poisson estimation and three-way clustering, and pass placebo tests except for light rain at the origin; region-by-date fixed effects and gauge-based rainfall give somewhat smaller effects. The findings call for adaptation that targets routine rain on short intercity corridors, alongside emergency responses to typhoons.

**Keywords:** Rainfall; Intercity travel; Human mobility; Climate adaptation; Tropical cyclones; China

# 1. Introduction

Rain is the most common weather hazard that travellers face. Unlike heatwaves or floods, it arrives on a large share of days in most of the world's populated regions, and climate change is making heavy precipitation more frequent and more intense (Seneviratne et al., 2021). Transport researchers have long documented that rain changes how people travel within cities: it suppresses walking and cycling, shifts demand toward cars, taxis and ride-hailing, and slows road traffic (Koetse and Rietveld, 2009; Böcker et al., 2013; Gössling et al., 2023). Far less is known about how rain affects travel *between* cities, even though intercity trips sustain labour markets, family ties, tourism and the integration of city regions. In China alone, the stable intercity links we study carry about 48 billion trips a year.

Two strands of evidence bear on this question, but neither answers it. The first studies everyday weather and travel demand, mostly for a single city and a single mode, such as bus ridership in Brisbane (Tao et al., 2018), public transport in Shenzhen (Zhou et al., 2017) or taxis and ride-hailing in New York (Brodeur and Nield, 2018). The second studies the resilience of human mobility to extreme events, typically one storm or flood at a time: Hurricane Sandy (Wang and Taylor, 2014), the 2021 Zhengzhou flood (Tang et al., 2023; Li et al., 2026) Typhoon Mawar in Japan (Yao et al., 2025) or the 2018 heavy rain in Japan (Liu et al., 2026). Recent national-scale work in China has examined how extreme weather and the COVID-19 pandemic jointly suppressed mobility (Liu et al., 2023), and how intercity connectivity helps cities recover from extreme rainfall (Liu and Bai, 2026). The closest study of intercity flows uses toll data from one province's freeway network and finds that rain at both trip ends matters (Yang et al., 2021).

This leaves four gaps. First, the extreme-event literature cannot tell us how much disruption comes from ordinary rain. A rainstorm may cut travel sharply, but light and moderate rain occur on far more days, so their cumulative effect may be larger. Second, aggregate city-level measures cannot separate rain at the origin from rain at the destination, or show how sensitivity varies with trip distance and therefore with transport mode. Third, it is unclear whether the same rainfall matters equally everywhere. If travellers and infrastructure adapt to local climate, as they do to heat (Barreca et al., 2016; Heutel et al., 2021), cities in wet regions should respond less to a given amount of rain. Fourth, in East Asia many of the heaviest rain days are typhoon days, when wind, warnings and service suspensions accompany the rain. Estimates that pool these days attribute typhoon disruption to rainfall.

We address these gaps with a national panel of daily intercity flows. We combine DIMNet-CPC, a newly released dataset of calibrated daily origin–destination (OD) flows among China's prefecture-level cities (Xu et al., 2026), with ERA5-Land rainfall extracted at 2,385 weather-station locations and summed over Beijing-time days (Muñoz-Sabater et al., 2021). The estimation sample covers 26,442 stable directed links observed daily from 2023 to 2025, or 28.8 million link-days. We estimate rainfall dose–response functions for origin and destination rain within OD links, absorbing seasonal, weekly and national shocks with high-dimensional fixed effects, and use IBTrACS cyclone tracks (Knapp et al., 2010) to separate typhoon-influenced days from everyday rain. We also control for daily temperature and re-estimate the model with a gauge-based rainfall analysis.

The paper makes four contributions. (1) It provides the first national estimates of how the full distribution of daily rainfall, not just extremes, affects intercity OD flows, distinguishing origin from destination rain. (2) It shows that the response decays with distance, so short intercity trips bear most of the burden. (3) It documents climate adaptation in intercity travel: cities in drier climates react more strongly to the same rainfall, and the difference narrows, but does not vanish, when rainfall is measured relative to local norms. (4) It separates everyday rain from typhoons and converts effects into trips. Typhoon days explain most of the disruption attributed to extreme rainfall, while everyday rain, mostly light and moderate, removes an estimated 0.7–1.0 billion intercity trips a year.

The rest of the paper proceeds as follows. Section 2 reviews related work. Section 3 describes the data, Section 4 the empirical strategy and Section 5 the results. Section 6 discusses mechanisms, policy implications and limitations, and Section 7 concludes.

# 2. Literature review

## 2.1 Weather and everyday travel

A large body of work links daily weather to travel behaviour. Reviews conclude that precipitation reduces discretionary and active travel, shifts mode choice toward motorised and sheltered modes, and degrades road performance (Koetse and Rietveld, 2009; Böcker et al., 2013; Gössling et al., 2023). Smart-card and trip-record studies quantify these effects at fine time scales. Rain lowers hourly bus ridership in Brisbane, with lagged responses that vary across the network (Tao et al., 2018). Public transport ridership in Shenzhen is likewise weather-sensitive (Zhou et al., 2017). In New York, rainy hours see about 22% more Uber trips and 5% more taxi trips (Brodeur and Nield, 2018), showing that rain redistributes travel as well as suppressing it. Mobile-phone traces show that activity patterns become more dispersed on rainy days (Horanont et al., 2013), and traffic data show congestion rising with hourly rainfall in Beijing, Tianjin and Shijiazhuang, by different amounts in each city (Xiong et al., 2022).

Several studies find that weather effects differ across places. In a comparison of Dutch, Norwegian and Swedish city regions, Böcker et al. (2019) attribute regional differences to climate, transport systems and habits. In Germany, precipitation affects cyclists in metropolitan areas less than in peripheral and rural areas (Galich and Nieland, 2023). These comparisons involve a handful of regions, so they cannot separate climate from other local differences.

## 2.2 Extreme rainfall and mobility resilience

A second strand uses mobility big data to study disasters. Wang and Taylor (2014, 2016) show that human mobility during hurricanes and other disasters is perturbed but retains its statistical regularities, up to a limit set by disaster strength. Studies of the 2021 Zhengzhou flood find that pluvial flooding reduced trips while leaving the structure of the mobility network largely intact (Tang et al., 2023), and that intercity outflows and inflows in the Central Plains urban agglomeration fell by roughly 31% and 26% (Li et al., 2026). Yao et al. (2025) report similar patterns at agglomeration and regional scales during Typhoon Mawar in Japan. Liu et al. (2026) find that Japan's 2018 heavy rain cut peak daily cross-city commuting by about 8% and shopping trips by about 20%, and that alternative routes sped recovery. For the Beijing–Tianjin–Hebei region, Zhao et al. (2025) simulate a 100-year rainstorm and estimate that it would reduce the efficiency of the intercity mobility network by about 26%.

Two national studies of China are closest to ours. Liu et al. (2023) show, for 313 cities during the COVID-19 pandemic, that rainfall above 20 mm/day raised the risk that intra- and intercity mobility fell below pre-pandemic levels, with stronger and delayed effects in dense, lower-income cities. Liu and Bai (2026) show for 366 cities that stronger intercity connectivity speeds the recovery of intra-city mobility after extreme rainfall. Yao et al. (2026) combine flood simulations with intercity mobility to project disruption under future climate. These studies treat rainfall as an extreme shock and mobility as a city-level outcome. They do not estimate how intercity OD flows respond to the full range of everyday rainfall, nor do they separate tropical cyclones from other heavy rain.

## 2.3 Intercity travel, distance and climate adaptation

Evidence on weather and intercity travel is sparse. Using freeway toll data for Shandong province, Yang et al. (2021) find that heavy rain and snow reduce OD volumes, that rain at the destination and the origin–destination rainfall difference both matter, and that effects begin about a day before and last about two days after severe weather. A survey in Xi'an shows that weather shifts the choice among air, high-speed rail, conventional rail and coach (Li et al., 2021), and highway volumes in the Greater Bay Area depend jointly on weather and holidays (Lin et al., 2022). Because the shares of road, rail and air travel vary systematically with distance (Xiang et al., 2026), distance is a natural axis along which rain sensitivity may vary. Short trips are more discretionary and more road-based; long trips are more often pre-booked and rail- or air-based. Closest in design to our study, Liang and Wang (2025) use fixed-effects panels to show that heatwaves reduce intra-city trips and inbound intercity trips in Chinese cities, with larger effects in small and less affluent cities.

Methodologically, we draw on the climate-econometrics literature, which treats day-to-day weather as a quasi-random shock conditional on location and time fixed effects and estimates nonlinear dose–response functions with bins (Dell et al., 2014; Hsiang, 2016). This literature also warns that gridded weather products smooth extremes and introduce measurement error (Auffhammer et al., 2013). It has documented adaptation: mortality responses to heat have declined over time and are smaller in hotter places (Barreca et al., 2016; Heutel et al., 2021). We apply the same logic to rainfall and intercity travel, asking whether places that see more rain respond less to it.

# 3. Data

## 3.1 Intercity flows

Intercity flows come from DIMNet-CPC (Xu et al., 2026), which provides directed daily OD flows, in person-trips, among China's 366 prefecture-level and higher administrative units for 2020–2025. The dataset calibrates Baidu Migration's relative intensity indices to national daily passenger statistics. A link's flow is the product of a national daily conversion factor and the link's Baidu relative intensity, $F_{ijt} = k_t\,q_{ijt}$. Because $k_t$ is common to all links on a day, date fixed effects absorb it, so the percentage effects we estimate are identified from the Baidu intensities. The calibration matters for converting those effects into numbers of trips (Section 5.5).

We use 1 January 2023 to 31 December 2025 (1,096 days). This window has no missing dates and no COVID-19 travel restrictions. DIMNet-CPC publishes a link only when it appears in the top-100 origin or destination list of one of its ends. A missing link-day therefore means “not disclosed”, not zero. Rain could push small links below the disclosure threshold, which would bias estimates toward zero if we used every observed record. We therefore restrict the sample to *stable* links that are disclosed on at least 95% of days: 26,442 of the 132,622 directed links ever observed, carrying 98.0% of all disclosed flow. Sansha is excluded because no representative rainfall series exists for it (Section 3.2), leaving 365 cities.

The median stable link carries 709 trips a day (mean 5,003), and the median link distance is 552 km. Short links dominate volumes: links under 150 km are 6% of links but carry half of all flow (Table 1).

## 3.2 Rainfall and temperature

Rainfall is ERA5-Land total precipitation (0.1°, about 9 km), a land-surface reanalysis driven by ERA5 (Muñoz-Sabater et al., 2021). We use a compilation that extracts the series at the locations of 2,421 China Meteorological Administration stations for 1950–2026. Hourly accumulations are de-accumulated and summed over Beijing-time (UTC+8) days, the same day definition as the mobility data. Thirty-six coastal and island stations fall in ERA5-Land ocean grid cells and return series that are zero on every day. We treat these as missing rather than dry and drop them, leaving 2,385 stations. City rainfall is the mean over stations within each city (median six stations). Ten cities with no valid station inside their boundary take the mean of the two nearest valid stations, all within 100 km of the city centroid except for Sansha (1,094 km), which we exclude.

We bin daily rainfall using China's national standard (GB/T 28592-2012): none (<0.1 mm), light (0.1–9.9), moderate (10–24.9), heavy (25–49.9), rainstorm (50–99.9) and extreme (≥100 mm). To measure rainfall relative to local norms, we also bin wet-day rainfall at each city's 1991–2020 75th, 90th, 95th and 99th percentiles. We classify cities with 1991–2020 mean annual precipitation of at least 800 mm as humid; this isohyet roughly follows the Qinling–Huaihe line separating northern and southern China (Fig. 1). Reanalysis rainfall is known to overstate the frequency of light rain and understate extremes over China (Xie et al., 2022), so we also use an independent, gauge-based product.

For temperature and as a check on rainfall, we use two 0.5° gauge-based grids from the NOAA Climate Prediction Center (CPC; unrelated to the DIMNet-CPC flow data): the Global Unified Gauge-Based Analysis of Daily Precipitation, which interpolates rain-gauge reports by optimal interpolation (Xie et al., 2007; Chen et al., 2008), and the CPC Global Daily Temperature analysis of daily maximum and minimum temperature. City values are means over the grid cells that overlap each city, weighted by overlap area, and daily mean temperature is the average of the maximum and minimum. CPC daily totals follow national reporting conventions rather than Beijing-time days, but same-day CPC rainfall matches our series best (correlation of log(1 + rainfall) 0.82, against 0.65 for the previous day and 0.47 for the next), so we use same-day values. The two rainfall series agree on the spatial pattern, with a correlation of about 0.9 in city mean annual rainfall, but not on how often light rain falls: CPC records rain on 49.4% of city-days against 57.7% for ERA5-Land, and 27% of the city-days that ERA5-Land classes as light rain are dry in CPC (Table 1).

## 3.3 Tropical cyclones

Tropical cyclone (TC) tracks are from IBTrACS v04r01 for the western North Pacific (Knapp et al., 2010), at three-hour intervals. We include provisional tracks for 2025, which lack CMA intensities but give positions. A city-day is typhoon-influenced if a TC centre, including decaying remnant lows, passes within 500 km of the city centroid at any time during the Beijing-time day. This radius is standard for attributing rainfall to TCs (Lonfat et al., 2004; Ren et al., 2006); we also report results with a 300 km radius. Between 2023 and 2025, 84 TCs influenced 283 cities on 6,005 city-days (1.5%), and 2.5% of link-days had a TC near at least one end. TCs dominate the heaviest rain: 70% of city-days with ≥100 mm are typhoon-influenced, 75% in humid cities and 20% in drier ones.

![Fig. 1. Study area: cities shaded by 1991–2020 mean annual precipitation (ERA5-Land); red line, 800 mm humid-zone boundary; grey, outside the sample. Base map GS(2024)0650.](../results/paper/Fig1_study_area.png){width=16cm}

**Table 1.** Descriptive statistics, 2023–2025.

| Variable | Value |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Cities (prefecture level and above) | 365 |
| Stable directed links (share of disclosed flow) | 26,442 (98.0%) |
| Days | 1,096 |
| Link-days: all / non-typhoon | 28,777,077 / 28,072,836 |
| Daily trips per link: median (mean) | 709 (5,003) |
| Link distance, km: median (mean) | 552 (713) |
| Links under 150 km: share of links / share of flow | 6.0% / 49.9% |
| Stations used after quality control | 2,385 |
| City-days by rain bin, ERA5-Land, %: none / light / moderate / heavy / rainstorm / extreme | 42.3 / 48.7 / 6.8 / 1.8 / 0.38 / 0.04 |
| City-days by rain bin, CPC gauge analysis, %: none / light / moderate / heavy / rainstorm / extreme | 50.6 / 40.2 / 6.6 / 2.1 / 0.52 / 0.06 |
| Daily mean temperature, °C: mean (5th–95th percentile) | 14.9 (−7.1 to 29.6) |
| Mean annual precipitation 1991–2020, mm: mean (range) | 1,125 (38–2,342) |
| Humid cities (≥800 mm) | 225 |
| Typhoon-influenced city-days (≤500 km) | 6,005 (1.5%) |

# 4. Empirical strategy

## 4.1 Baseline model

For link ij (origin i, destination j) on day t, we estimate

$$\ln F_{ijt} = \sum_{b=1}^{5} \beta^{O}_{b}\,\mathbf{1}[R_{it} \in b] + \sum_{b=1}^{5} \beta^{D}_{b}\,\mathbf{1}[R_{jt} \in b] + \sum_{c=1}^{4} \left(\gamma^{O}_{c}\,\mathbf{1}[A_{it} \in c] + \gamma^{D}_{c}\,\mathbf{1}[A_{jt} \in c]\right) + \mu_{ij,m(t)} + \eta_{ij,w(t)} + \lambda_{t} + \varepsilon_{ijt}$$

where R is daily rainfall in the five non-zero bins of Section 3.2, with dry days as the reference. A is rainfall accumulated over the previous seven days (t−7 to t−1), binned at 10, 25, 50 and 100 mm. Wet days cluster in wet spells, and the seven days before a ≥25 mm day average 60–76 mm against 10 mm before a dry day. Without this control, the rain coefficients would partly capture the effect of a wet period. The fixed effects μ (link × year-month) absorb each link's seasonality and trend; η (link × day-of-week) absorbs weekly rhythms such as commuting and weekend travel; and λ (date) absorbs national shocks, including public holidays, the Spring Festival travel season and DIMNet's daily conversion factor $k_t$. We report effects as percentage changes, 100 × (exp(β) − 1).

Identification rests on the standard assumption in weather studies: conditional on a link's month and weekday and on the national date effect, day-to-day rainfall is as good as random (Dell et al., 2014; Hsiang, 2016). The coefficients are reduced-form total effects. They include travellers' own responses and any operator responses, such as service changes, that rain triggers.

The main specification uses non-typhoon link-days, those with no TC within 500 km of either end (28.07 million observations). Typhoon days combine rain with wind, warnings and pre-emptive suspensions, so we analyse them separately. We compare all days with non-typhoon days and estimate a model in which each rain bin is interacted with a typhoon indicator at the same end. We estimate all models in R with fixest (Bergé, 2018), which handles the roughly 950,000 link × year-month and 185,000 link × weekday fixed effects.

## 4.2 Inference

Standard errors are clustered two-way by origin and destination city. Large weather systems hit many cities on the same day, so we also cluster three-way by origin, destination and date. Three-way clustering of all 28 million observations exceeds available memory, so we compute both sets of standard errors on the same 30% random sample of links. We treat the three-way results as the conservative basis for inference (Cameron et al., 2011; Cameron and Miller, 2015).

## 4.3 Heterogeneity and dynamics

To study distance, we split links into five great-circle distance bands between city centroids (<150, 150–300, 300–500, 500–1,000 and >1,000 km) and re-estimate the model in each band. Each band then has its own date effects. To study climate, we split links by whether the origin is humid (≥800 mm). We also interact the rain bins with the origin's standardised log mean annual precipitation, re-estimate with local-percentile bins, and split by the four official regions (East, Central, West, Northeast).

To study timing, we replace the rain bins with indicators for 10–25 mm and ≥25 mm at each end on days t−3 to t+3 relative to the flow day, plus t−7 and t+7 as placebos. Rain seven days *after* the flow day cannot plausibly cause it, so a non-zero coefficient there signals residual confounding. A second version adds light rain (0.1–10 mm) on the same days. To gauge the size of such spurious associations more generally, we also add to the main model rainfall shifted by ±7, ±14, ±21 or ±28 days, or by 364 or 728 days (the same weekday one and two years earlier), binned as none, light, moderate and ≥25 mm, one shift at a time. None of these can affect travel on the flow day, so their coefficients describe the noise against which the actual effects should be judged.

We also estimate city-level models for total outflow and inflow summed over stable links. These control for the flow-weighted share of a city's destinations (or origins) experiencing moderate or heavy rain, with city × year-month, city × weekday and date fixed effects.

## 4.4 Robustness

We re-estimate the main model with Poisson pseudo-maximum likelihood on flow levels (Santos Silva and Tenreyro, 2006; Correia et al., 2020), replace link × year-month with link × week fixed effects, and narrow the typhoon radius to 300 km. To absorb regional shocks, such as provincial school holidays and regional events, we replace the national date fixed effects with origin-region × date and destination-region × date fixed effects for China's seven geographic regions. We also add daily mean temperature at both ends in eight bins (below −10, −10 to 0, 0–10, 10–15, 15–20, 20–25, 25–30 and at least 30 °C), with 15–20 °C as the reference. With these 14 extra regressors the model exceeds available memory on the full sample, so we estimate it on a 50% random sample of links and compare it with the main model on the same sample. We do the same for the distance-band and dry–humid splits. Finally, we replace ERA5-Land rainfall, both on the day and in the antecedent-rainfall control, with the CPC gauge analysis, binned in the same way.

## 4.5 Converting effects into trips

To express effects in trips, we compute each link-day's counterfactual dry-day flow as $F_{ijt}/\exp(\hat\beta^{O}_{b(i,t)} + \hat\beta^{D}_{b(j,t)})$ and sum the difference from observed flow. On non-typhoon days we use the distance-band estimates, because short links carry most flow and respond most. On typhoon days we use the interaction model's rain coefficients. Antecedent rainfall is held at its observed level. Because only stable links are counted, the totals are lower bounds. To show how sensitive they are to specification, we recompute them with distance-band coefficients from the region-by-date and gauge-based models, with coefficients net of the mean placebo coefficient, and with the light-rain effect set to zero.

# 5. Results

## 5.1 Dose–response

On non-typhoon days, intercity flows fall steadily as rainfall rises (Fig. 2, Table 2). Rain at the origin reduces a link's flow by 0.6% in light rain, 1.9% in moderate rain, 2.3% in heavy rain and 4.0% in a rainstorm. Destination rain matters slightly more: −1.0%, −1.8%, −3.1% and −6.0%. Of these estimates, the origin light-rain effect is the least robust; it does not clear the placebo noise (Section 5.4). For extreme rain (≥100 mm) the destination effect is −8.8%; the origin estimate (−5.5%) is imprecise because only 50 non-typhoon city-days reach this level. Under three-way clustering every coefficient except the origin extreme bin remains significant at the 5% level. City-level totals confirm the pattern. A city's total outflow falls by 1.9% in light rain and 6.3% in a rainstorm, and its inflow by 1.8% and 6.5%. Measured relative to local norms, rain above a city's 99th percentile reduces flows by 4.0% (origin) and 5.5% (destination).

![Fig. 2. Change in OD flow relative to a dry day, by rainfall at the origin and destination, non-typhoon days, 2023–2025. Bars are 95% confidence intervals, clustered by origin and destination.](../results/paper/Fig2_dose_response.png){width=16cm}

**Table 2.** Main estimates, non-typhoon days (percentage change relative to a dry day).

| Rain bin | OD flow \[95% CI\] | Three-way clustered p | PPML (30% of links) | City total outflow | City total inflow |
| -------------------------------------------- | ---------------------------------------------------- | ------------------------ | ------------------------ | ---------------------------- | ---------------------------- |
| *Origin rain* |  |  |  |  |  |
| Light (0.1–10 mm) | −0.6\*\*\* \[−0.9, −0.3\] | 0.011 | −0.8\*\* | −1.9\*\*\* |  |
| Moderate (10–25) | −1.9\*\*\* \[−2.2, −1.5\] | <0.001 | −3.1\*\*\* | −3.2\*\*\* |  |
| Heavy (25–50) | −2.3\*\*\* \[−2.8, −1.7\] | <0.001 | −4.3\*\*\* | −4.7\*\*\* |  |
| Rainstorm (50–100) | −4.0\*\*\* \[−5.0, −3.0\] | <0.001 | −5.2\*\*\* | −6.3\*\*\* |  |
| Extreme (≥100) | −5.5 \[−11.7, 1.2\] | 0.20 | −16.0 | −14.7\*\*\* |  |
| *Destination rain* |  |  |  |  |  |
| Light (0.1–10 mm) | −1.0\*\*\* \[−1.2, −0.8\] | <0.001 | −1.1\*\*\* |  | −1.8\*\*\* |
| Moderate (10–25) | −1.8\*\*\* \[−2.2, −1.5\] | <0.001 | −2.3\*\*\* |  | −2.8\*\*\* |
| Heavy (25–50) | −3.1\*\*\* \[−3.7, −2.6\] | <0.001 | −3.5\*\*\* |  | −3.6\*\*\* |
| Rainstorm (50–100) | −6.0\*\*\* \[−7.2, −4.8\] | <0.001 | −5.9\*\*\* |  | −6.5\*\*\* |
| Extreme (≥100) | −8.8\*\*\* \[−12.9, −4.6\] | 0.009 | −3.2 |  | −10.9\*\*\* |
| Observations | 28,072,836 | 8.4 million | 8,421,805 | 393,986 | 393,979 |

::: {custom-style="Table Note"}
*Notes: All models control for 7-day antecedent rainfall at both ends. OD models include link × year-month, link × weekday and date fixed effects; city models include city × year-month, city × weekday and date fixed effects and the flow-weighted share of partner cities with moderate or heavy rain. Confidence intervals and stars (\* p<0.05, \*\* p<0.01, \*\*\* p<0.001) use two-way clustering by origin and destination (city models: city and date). Column 3 reports p-values with three-way clustering by origin, destination and date on a 30% random sample of links.*
:::

## 5.2 Distance

Sensitivity to rain declines with distance (Fig. 3). Rain at the origin cuts flows on links under 150 km by 4.1% in moderate rain and 8.4% in a rainstorm, against 0.8% and 2.0% on links over 1,000 km. Destination rain follows the same gradient up to 1,000 km: from −4.2% to −0.7% in moderate rain and from −8.5% to −4.3% in a rainstorm. Beyond 1,000 km, destination effects tick up slightly (−1.4% and −6.7%) but remain smaller than on short links. Extreme rain, omitted from Fig. 3 because of wide intervals, shows the same decline at the origin, from −21.3% under 150 km to −1.9% (not significant) at 500–1,000 km. Adding temperature controls, estimated on half of the links, changes the light-rain to rainstorm coefficients in each band by at most 0.4 percentage points (0.1 on average) and leaves the gradient intact (origin moderate rain: −4.1% under 150 km against −0.8% beyond 1,000 km).

Because short links both respond most and carry most flow, they bear most of the loss. Everyday rain removes 2.5% of counterfactual trips on links under 150 km, 1.8% at 150–300 km, 1.2% at 300–500 km, 0.8% at 500–1,000 km and 0.5% beyond (Section 5.5). Links under 300 km account for 89% of the non-typhoon loss.

![Fig. 3. Change in OD flow by rainfall bin and origin–destination distance, estimated separately for each distance band, non-typhoon days. (a) Rain at the origin; (b) rain at the destination. Bars are 95% confidence intervals.](../results/paper/Fig3_distance.png){width=16cm}

## 5.3 Climate adaptation and regional differences

The same rainfall matters more where rain is less common (Fig. 4a). For origins in drier climates (<800 mm a year), flows fall by 1.2% in light rain, 3.0% in moderate rain, 4.2% in heavy rain and 6.0% in a rainstorm. For humid origins the corresponding effects are 0.0%, −1.4%, −1.5% and −3.3%. The continuous interaction gives the same answer: each standard deviation of higher long-run precipitation at the origin shrinks the effect of light, moderate, heavy and rainstorm rain by 1.4, 1.9, 2.3 and 3.5 percentage points. Effects of extreme rain do not differ by climate (−4.7% and −5.4%, both imprecise). Temperature does not explain the gap. Drier cities also tend to be colder, so the gap could in principle reflect rain on cold days. With temperature controls, estimated on half of the links, the dry and humid coefficients change by at most 0.3 percentage points, and the origin gap widens slightly, from 1.6 to 1.8 percentage points in moderate rain and from 2.6 to 3.0 points in a rainstorm.

Measuring rain relative to local norms narrows but does not close the gap (Fig. 4b). Rain between the local 95th and 99th percentiles reduces flows by 1.4% from humid origins and 3.4% from drier ones. Part of the north–south difference therefore reflects how unusual a given rainfall is locally, and part reflects other differences, such as road conditions, mode mix and habits. By region, the Northeast (−8.3% in a rainstorm) and the West (−5.2%) are most sensitive and the East (−3.6%) and Centre (−2.5%) least (Fig. 4c). In light rain, eastern origins show no response at all.

![Fig. 4. Rain at the origin, non-typhoon days. (a) Absolute bins by origin climate; (b) local-percentile bins by origin climate; (c) absolute bins by region of origin. Bars are 95% confidence intervals.](../results/paper/Fig4_climate.png){width=16cm}

## 5.4 Timing and placebo tests

Rain reduces travel on the day it falls and the next day, and the lost trips are not made up later (Fig. 5). After ≥25 mm of rain at the origin, flows fall by 1.6% on the day and 2.2% the following day, then return to normal with no rebound over the next two days. Destination rain of ≥25 mm reduces flows by 2.6% on the day and 1.6% the next day, with small negative effects persisting to day 3. Flows to a destination fall slightly (−0.8%, p = 0.06) the day before heavy rain arrives, consistent with travellers responding to forecasts. Moderate rain shows the same pattern at about half the size. Because no positive lagged effects appear, the reductions look like cancelled trips rather than trips shifted to a later day within the window.

The ±7-day placebo tests are clean for moderate rain: rain seven days before or after the flow day has effects within ±0.3% and none is significant. For ≥25 mm they are not fully clean. Heavy origin rain seven days after the flow day is associated with 1.2% higher flows (p = 0.001), and heavy destination rain seven days before with 1.1% lower flows (p = 0.01). Adding light rain to the dynamic model shows that its ±7-day placebos are small: +0.2% and +0.1% at the origin, and +0.4% (p = 0.04) and 0.0% at the destination. Light rain at the destination lowers flows by 0.7% on the day and 1.1% the next day. At the origin the effect appears mainly on the next day (−0.9%), and the same-day effect (−0.4%) is not significant.

Shifted-rain placebos give a fuller picture of the noise (Table 3). Across the ten shifts, placebo coefficients alternate in sign and average close to zero (−0.05% to +0.16%), so they do not point to a systematic bias. Their typical absolute size is about 0.3 percentage points for light rain, 0.4–0.5 for moderate rain and 0.5–0.7 for ≥25 mm, and region-by-date fixed effects shrink it by 27–44%. Against this noise, destination effects are about four to six times the typical placebo at every intensity, including light rain (−1.0%), and origin effects of moderate and heavier rain are more than three times. The origin light-rain effect (−0.6%) is only about twice the typical placebo, lies within the placebo range, and falls to −0.2% with region-by-date fixed effects. We therefore do not treat it as established.

![Fig. 5. Change in OD flow on days around rainfall at the origin and destination, non-typhoon days. Negative values on the horizontal axis mean the rain falls after the flow day; ±7 are placebo days. Estimated on a 30% sample of links; bars are 95% confidence intervals with three-way clustering.](../results/paper/Fig5_dynamics.png){width=16cm}

**Table 3.** Placebo tests with shifted rainfall, non-typhoon days (percentage change relative to a dry day).

| Rain | Effect on the day | Placebo mean | Mean absolute placebo | Placebo range | Significant placebos (of 10) |
| ------------------------------------ | ---------------- | ------------ | ---------------- | ---------------- | ---------------- |
| *A. National date fixed effects* |  |  |  |  |  |
| Origin, light | −0.6\*\*\* | 0.04 | 0.29 | −0.9 to 0.4 | 4 |
| Origin, moderate | −1.9\*\*\* | −0.05 | 0.51 | −1.2 to 0.7 | 7 |
| Origin, ≥25 mm | −2.3\*\*\* | 0.13 | 0.69 | −1.6 to 1.4 | 6 |
| Destination, light | −1.0\*\*\* | 0.14 | 0.26 | −0.3 to 0.7 | 3 |
| Destination, moderate | −1.8\*\*\* | 0.14 | 0.40 | −0.8 to 0.8 | 6 |
| Destination, ≥25 mm | −3.1\*\*\* | 0.16 | 0.53 | −0.7 to 1.1 | 5 |
| *B. Region × date fixed effects* |  |  |  |  |  |
| Origin, light | −0.2\* | 0.04 | 0.16 | −0.4 to 0.3 | 3 |
| Origin, moderate | −1.3\*\*\* | 0.01 | 0.32 | −0.6 to 0.6 | 5 |
| Origin, ≥25 mm | −1.7\*\*\* | 0.17 | 0.51 | −0.8 to 1.0 | 4 |
| Destination, light | −0.7\*\*\* | 0.11 | 0.16 | −0.2 to 0.3 | 3 |
| Destination, moderate | −1.5\*\*\* | 0.15 | 0.27 | −0.4 to 0.5 | 4 |
| Destination, ≥25 mm | −2.6\*\*\* | 0.18 | 0.38 | −0.6 to 0.9 | 3 |

::: {custom-style="Table Note"}
*Notes: Effect on the day is from the main model (Panel A) or from the model with origin-region × date and destination-region × date fixed effects for seven regions (Panel B), on all non-typhoon link-days; for ≥25 mm it is the heavy-rain bin (25–50 mm), the smallest effect above 25 mm. Placebo statistics summarise ten regressions on a 30% random sample of links, each adding to the main model rainfall shifted by ±7, ±14, ±21 or ±28 days, or by 364 or 728 days. Significant placebos have p < 0.05 with two-way clustering by origin and destination. \* p<0.05, \*\* p<0.01, \*\*\* p<0.001.*
:::

## 5.5 Annual losses

In the main estimates, everyday rain removes about 954 million intercity trips a year on non-typhoon days, and rain on typhoon days removes another 127 million. Together that is 1.08 billion trips, or 2.2% of counterfactual dry-weather travel on the stable links. Most of the non-typhoon loss comes from frequent, modest rain (Fig. 6a). Light rain accounts for 577 million trips (61%) and moderate rain for 236 million (25%). Rainstorms and extreme rain together account for only 37 million (4%).

The total is sensitive to specification, mainly through light rain (Table 4). With region-by-date fixed effects the non-typhoon loss is 680 million trips, with gauge-based rainfall 775 million, and with coefficients net of the mean placebo 1.0 billion; light rain accounts for 56–61% in each case. We therefore report the everyday loss as 0.7–1.0 billion trips a year. Moderate and heavier rain account for 297–386 million in every specification, and even under the most conservative assumption, that light rain has no effect at all, everyday rain removes 334 million trips a year. In the main estimates, moderate rain alone causes about six times as much annual loss as rainstorms and extreme rain combined.

![Fig. 6. Annual intercity trips lost to rain on non-typhoon days, main estimates, 2023–2025 average. (a) By rainfall bin, with share of total in parentheses; (b) share of counterfactual trips lost by distance band, with share of total loss in parentheses.](../results/paper/Fig6_losses.png){width=16cm}

**Table 4.** Annual intercity trips lost to rain on non-typhoon days under alternative specifications (million trips, 2023–2025 average).

| Specification | Light | Moderate | ≥25 mm | Total | Light share |
| ------------------------------------ | -------------- | -------------- | -------------- | -------------- | -------------- |
| Main estimates | 577 | 236 | 141 | 954 | 61% |
| Region × date fixed effects | 382 | 179 | 119 | 680 | 56% |
| Gauge-based rainfall (NOAA CPC) | 451 | 194 | 130 | 775 | 58% |
| Net of mean placebo coefficient | 616 | 241 | 145 | 1,002 | 61% |
| Light-rain effect set to zero | 0 | 198 | 135 | 334 | 0% |

::: {custom-style="Table Note"}
*Notes: All rows use coefficients estimated separately by distance band. Losses are classified by the heavier rain bin of the two ends; when the light-rain effect is set to zero, link-days with light rain at one end and moderate rain at the other also lose less, so the moderate column falls too. The gauge-based row classifies days by CPC rainfall.*
:::

## 5.6 Typhoon days

Typhoon days behave very differently from ordinary rainy days (Fig. 7). Pooling all days, extreme rain cuts flows by 22.4% at the origin and 27.1% at the destination, and rainstorms by 7.5% and 10.1%. Removing the 2.5% of link-days near a tropical cyclone shrinks these effects to −5.5%, −8.8%, −4.0% and −6.0%, while light and moderate effects barely change. When rain bins are interacted with a typhoon indicator, the same rainfall on a typhoon day lowers flows by an additional 24% (origin) and 32% (destination) at ≥100 mm. Even light rain at a typhoon-affected destination lowers flows by an extra 6.5%, suggesting that warnings and service suspensions depress travel beyond the rain itself. At the city level, total outflow on days with ≥100 mm falls by 31.8% when typhoon days are included and by 14.7% when they are excluded.

Typhoon days also produce two patterns that would otherwise be misread as features of rainfall. With all days pooled, destination rain of ≥100 mm cuts long-haul flows (>1,000 km) by 27.8%, almost as much as short-haul flows; on non-typhoon days the long-haul effect is −5.9%. With all days pooled, humid origins appear more sensitive than drier ones to ≥100 mm (−23.6% versus −8.4%), the opposite of the adaptation pattern. That reversal disappears once typhoon days are removed. Typhoon days contribute 127 million lost trips a year, 12% of the total, and about half of all losses from rainstorms and extreme rain.

![Fig. 7. Change in OD flow by rainfall bin, all days versus non-typhoon days (no tropical cyclone within 500 km of either end). (a) Rain at the origin; (b) rain at the destination. Bars are 95% confidence intervals.](../results/paper/Fig7_typhoon.png){width=16cm}

## 5.7 Robustness

Table 5 shows that the main estimates are stable across specifications. Replacing link × month with link × week fixed effects, which absorb seasonality within months, changes the moderate-rain and rainstorm coefficients by at most 1.4 percentage points. Poisson estimation on flow levels gives similar or slightly larger effects, except in the sparsely populated extreme bin. Three-way clustering inflates standard errors by 1.5–2 times but leaves the moderate, heavy and rainstorm effects significant at p < 0.001. Narrowing the typhoon radius to 300 km barely moves the estimates. Adding or omitting the antecedent-rainfall control changes estimates by at most 0.2 points.

Temperature does not account for the rainfall effects. Adding temperature bins at both ends changes no rain coefficient by more than 0.2 percentage points (Table 5, comparing the two rows estimated on the same 50% of links), and by no more than 0.4 points in the distance-band and dry–humid splits (Sections 5.2 and 5.3). Temperature itself matters: relative to a 15–20 °C day, flows fall by 12.9% when the origin's daily mean is below −10 °C and by 3.4% at 0–10 °C, with smaller effects at the destination (−8.6% and −2.8%) and little change on warm days. With CPC gauge-based rainfall, light- and moderate-rain effects are almost identical to the main estimates (origin −0.6% and −1.4%, destination −1.0% and −1.7%). Effects of heavier rain are smaller, especially at the destination (rainstorm −3.4% against −6.0%; extreme −5.3% against −8.8%). This is consistent with the 0.5° grid smoothing local downpours, so that a city's heaviest rain days are identified less sharply. The smooth dose–response and the size of light- and moderate-rain effects therefore hold with either rainfall source, while the size of rainstorm effects is best read as a range of about 3.5–6%.

Region-by-date fixed effects make the estimates smaller but leave their pattern intact (Table 5). They shrink the moderate-rain to rainstorm effects by 16–31% (origin moderate rain −1.3%, destination rainstorm −4.9%) and the origin light-rain effect by 60%, to −0.2%; the dose–response and the decline with distance remain. Part of this shrinkage is likely attenuation. With these fixed effects, effects are identified only from rainfall differences between cities in the same region on the same day, so rain systems that cover a whole region no longer contribute and measurement error weighs more. We therefore keep national date effects in the main specification and use the region-by-date estimates as the lower end of the loss range.

**Table 5.** Robustness: selected coefficients (percentage change relative to a dry day).

| Specification | Origin moderate | Origin rainstorm | Origin extreme | Dest. moderate | Dest. rainstorm | Dest. extreme |
| -------------------------------------------------------- | ------------------------ | ------------------------ | ------------------------ | ------------------------ | ------------------------ | ------------------------ |
| Main: non-typhoon days, link × month FE | −1.9\*\*\* | −4.0\*\*\* | −5.5 | −1.8\*\*\* | −6.0\*\*\* | −8.8\*\*\* |
| Link × week FE | −1.7\*\*\* | −4.7\*\*\* | −6.6\* | −1.6\*\*\* | −4.6\*\*\* | −6.9\*\*\* |
| PPML, 30% of links | −3.1\*\*\* | −5.2\*\*\* | −16.0 | −2.3\*\*\* | −5.9\*\*\* | −3.2 |
| Three-way clustering, 30% of links | −1.9\*\*\* | −4.1\*\*\* | −5.4 | −1.9\*\*\* | −6.4\*\*\* | −8.1\*\* |
| Typhoon radius 300 km | −1.9\*\*\* | −4.3\*\*\* | −6.3 | −1.9\*\*\* | −6.3\*\*\* | −8.6\*\*\* |
| Region × date fixed effects (7 regions) | −1.3\*\*\* | −3.2\*\*\* | −5.1 | −1.5\*\*\* | −4.9\*\*\* | −5.8\*\* |
| Main model, 50% of links | −1.9\*\*\* | −3.9\*\*\* | −5.9 | −1.9\*\*\* | −6.3\*\*\* | −8.6\*\*\* |
| Adding temperature bins, 50% of links | −1.7\*\*\* | −3.7\*\*\* | −5.3 | −1.8\*\*\* | −6.3\*\*\* | −8.6\*\*\* |
| Gauge-based rainfall (NOAA CPC) | −1.4\*\*\* | −3.5\*\*\* | −1.9 | −1.7\*\*\* | −3.4\*\*\* | −5.3\*\*\* |
| Gauge-based rainfall and temperature, 50% of links | −1.4\*\*\* | −3.3\*\*\* | −0.7 | −1.7\*\*\* | −3.7\*\*\* | −5.2\*\*\* |
| All days, including typhoon days | −2.0\*\*\* | −7.5\*\*\* | −22.4\*\*\* | −2.0\*\*\* | −10.1\*\*\* | −27.1\*\*\* |
| All days, no antecedent-rain control | −2.0\*\*\* | −7.6\*\*\* | −22.6\*\*\* | −2.0\*\*\* | −10.2\*\*\* | −27.1\*\*\* |

::: {custom-style="Table Note"}
*Notes: \* p<0.05, \*\* p<0.01, \*\*\* p<0.001. Clustering by origin and destination except in the three-way row. Rows marked “50% of links” use the same random half of links; temperature enters as eight daily-mean bins at each end (reference 15–20 °C). Gauge-based rows replace both daily and antecedent rainfall with the NOAA CPC gauge analysis. The region × date row replaces date fixed effects with origin-region × date and destination-region × date fixed effects.*
:::

# 6. Discussion

## 6.1 Two channels: everyday demand and typhoon supply shocks

The results point to two distinct ways in which rain reduces intercity travel. On ordinary rainy days the response is smooth, modest and concentrated on short trips, and the lost trips are not recovered within three days. This pattern fits a demand channel. Short intercity trips are more discretionary, such as visiting family, shopping or leisure, and are mostly made by car, coach or conventional rail, so rain raises their generalised cost through slower roads, worse access to stations and less pleasant activities at the destination. Travellers respond by cancelling rather than postponing. Long trips are more often pre-booked, purpose-bound and made by high-speed rail or air, which ordinary rain barely affects. That destination rain matters slightly more than origin rain suggests that conditions at the place of activity weigh more heavily than conditions at departure, consistent with Yang et al. (2021).

Typhoon days follow a different logic. The same rainfall depresses flows several times more; long-haul trips into an affected city fall almost as much as short ones; and even light rain at a typhoon-affected destination reduces travel by 6.5%. These are the signatures of a supply channel: pre-emptive suspension of flights, high-speed rail and ferries, expressway closures and official warnings. Pooled estimates mix the two channels, and attributing typhoon disruption to rainfall overstates how much heavy rain alone disrupts travel. It also produces misleading patterns, such as apparent long-haul sensitivity and an apparent reversal of adaptation in humid regions.

## 6.2 Adaptation

Cities in drier climates respond more strongly to the same rainfall, mirroring the adaptation found for heat and mortality (Barreca et al., 2016; Heutel et al., 2021). Part of the gap closes when rain is measured relative to local norms, so rarity itself matters: a 25 mm day is routine in Guangzhou but unusual in Lanzhou. The remainder may reflect durable investments and habits, such as drainage capacity, road and vehicle preparedness, and travellers' familiarity with rain. This has a forward-looking implication. Heavy precipitation is projected to intensify across much of the world (Seneviratne et al., 2021). Where rain is becoming more frequent in regions that are not adapted to it, the intercity travel response may initially be larger than in historically wet regions.

## 6.3 Policy implications

Three implications follow. First, adaptation for intercity travel should not focus only on extremes. On non-typhoon days, moderate rain alone causes about six times as much annual loss as rainstorms and extreme rain combined in the main estimates, and links under 300 km account for 89% of the loss. Improving the rain resilience of short corridors could therefore address most of the everyday loss. Relevant measures include drainage and surface quality on expressways and national roads, sheltered access to intercity bus and rail stations, and timely travel information. Second, the larger response in drier regions argues for prioritising adaptation where rain is unfamiliar and where projected increases in heavy rain are concentrated. Third, typhoon disruptions are large, concentrated and partly policy-driven, so they warrant a separate emergency-management lens. Coordinated suspension and resumption decisions, flexible rebooking and clear communication may reduce lost travel without compromising safety.

## 6.4 Limitations

Several limitations qualify these findings. First, the flows are model-based estimates. DIMNet-CPC calibrates Baidu location data to national totals, so our percentage effects inherit any differences between Baidu users and the travelling population, and we observe only disclosed links. Restricting to stable links avoids truncation bias for 98% of flows but leaves the smallest links unstudied. Second, rainfall in the main analysis comes from a reanalysis at station locations rather than from rain gauges. ERA5-Land overstates the frequency of light rain and understates extremes over China (Xie et al., 2022). A gauge-based analysis reproduces the light- and moderate-rain effects but gives smaller effects for rainstorms and extreme rain, and its 0.5° grid is coarse for small cities, so the size of the heaviest-rain effects remains uncertain by a few percentage points. Third, we add temperature only in robustness checks on half of the links, and other weather, such as wind and visibility, is not controlled; temperature leaves the national, distance-band and dry–humid estimates essentially unchanged. Fourth, placebo coefficients, though centred on zero, are typically 0.3–0.7 percentage points, enough to leave the origin light-rain effect unconfirmed, and region-by-date fixed effects shrink all effects; this is why we report the everyday loss as a range rather than a point estimate. Fifth, our distance-based typhoon definition misses cyclone-related rain far from the storm centre, as in the 2023 Beijing rainstorm linked to Typhoon Doksuri, so the typhoon contribution is, if anything, understated. Finally, we observe distance but not mode, and our period, 2023–2025, follows the pandemic, so behaviour may differ in other periods.

# 7. Conclusions

Using 28 million daily observations of intercity flows among 365 Chinese cities, this paper estimates how rainfall shapes travel between cities. On ordinary days, rain reduces intercity flows by about 1% in light rain at the destination, 2% in moderate rain and 4–6% in a rainstorm. Effects are larger at the destination than the origin, larger on short trips than long ones, and larger in drier climates than in humid ones. Lost trips are cancelled rather than postponed. Typhoon days are a distinct phenomenon: they account for most of the disruption usually attributed to extreme rainfall and reach long-distance travel that ordinary rain leaves almost untouched.

The central message is that the burden of rain on intercity mobility lies mostly in the everyday. Because modest rain is so common, it removes far more trips each year, an estimated 0.7–1.0 billion on the stable links studied here, than the rare storms that dominate the resilience literature. Planning for climate-resilient regional transport should therefore pair emergency responses to typhoons with routine improvements that keep short intercity corridors working in ordinary rain, especially in regions where heavy rain is becoming more common but remains unfamiliar.

Future work should pin down the effects of heavy rain with denser gauge or radar data, observe transport modes directly, and study the mechanisms of typhoon disruption, including warnings and service suspensions, in their own right.

# Declarations

**Data availability.** Intercity flows: DIMNet-CPC v1.0, Figshare, CC BY 4.0 ([doi:10.6084/m9.figshare.33154163](https://doi.org/10.6084/m9.figshare.33154163)). Rainfall: ERA5-Land hourly data, Copernicus Climate Change Service ([doi:10.24381/cds.e2161bac](https://doi.org/10.24381/cds.e2161bac)), extracted at weather-station locations by a third-party compilation \[describe source and licence\]. Tropical cyclone tracks: IBTrACS v04r01, NOAA National Centers for Environmental Information. Gauge-based precipitation and temperature: NOAA CPC Global Unified Gauge-Based Analysis of Daily Precipitation and CPC Global Daily Temperature, provided by the NOAA Physical Sciences Laboratory (PSL), Boulder, Colorado, USA (<https://psl.noaa.gov>). The city-level daily rainfall and temperature series and typhoon flags derived for this study will be made available \[repository and DOI to be added\].

**Code availability.** Processing and estimation code (Python and R) will be deposited at \[repository to be added\].

**CRediT authorship contribution statement.** \[Author 1\]: Conceptualization, Methodology, Formal analysis, Writing – original draft. \[Author 2\]: \[roles\]. \[To be completed.\]

**Declaration of competing interest.** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Funding.** \[To be completed.\]

**Acknowledgements.** CPC data provided by the NOAA PSL, Boulder, Colorado, USA, from their website at <https://psl.noaa.gov>. \[Other acknowledgements to be completed.\]

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the authors used Claude (Anthropic) to assist with literature search, data processing code, statistical analysis and drafting of the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication. \[Authors to confirm and adapt.\]

# References

::: {custom-style="Reference List"}
Auffhammer, M., Hsiang, S.M., Schlenker, W., Sobel, A., 2013. Using weather data and climate model output in economic analyses of climate change. Review of Environmental Economics and Policy 7(2), 181–198. <https://doi.org/10.1093/reep/ret016>

Barreca, A., Clay, K., Deschênes, O., Greenstone, M., Shapiro, J.S., 2016. Adapting to climate change: The remarkable decline in the US temperature-mortality relationship over the twentieth century. Journal of Political Economy 124(1), 105–159. <https://doi.org/10.1086/684582>

Bergé, L., 2018. Efficient estimation of maximum likelihood models with multiple fixed-effects: The R package FENmlm. CREA Discussion Papers 13, University of Luxembourg.

Böcker, L., Dijst, M., Prillwitz, J., 2013. Impact of everyday weather on individual daily travel behaviours in perspective: A literature review. Transport Reviews 33(1), 71–91. <https://doi.org/10.1080/01441647.2012.747114>

Böcker, L., Uteng, T.P., Liu, C., Dijst, M., 2019. Weather and daily mobility in international perspective: A cross-comparison of Dutch, Norwegian and Swedish city regions. Transportation Research Part D 77, 491–505. <https://doi.org/10.1016/j.trd.2019.07.012>

Brodeur, A., Nield, K., 2018. An empirical analysis of taxi, Lyft and Uber rides: Evidence from weather shocks in NYC. Journal of Economic Behavior & Organization 152, 1–16. <https://doi.org/10.1016/j.jebo.2018.06.004>

Cameron, A.C., Gelbach, J.B., Miller, D.L., 2011. Robust inference with multiway clustering. Journal of Business & Economic Statistics 29(2), 238–249. <https://doi.org/10.1198/jbes.2010.07136>

Cameron, A.C., Miller, D.L., 2015. A practitioner's guide to cluster-robust inference. Journal of Human Resources 50(2), 317–372. <https://doi.org/10.3368/jhr.50.2.317>

Chen, M., Shi, W., Xie, P., Silva, V.B.S., Kousky, V.E., Higgins, R.W., Janowiak, J.E., 2008. Assessing objective techniques for gauge-based analyses of global daily precipitation. Journal of Geophysical Research: Atmospheres 113(D4), D04110. <https://doi.org/10.1029/2007JD009132>

Correia, S., Guimarães, P., Zylkin, T., 2020. Fast Poisson estimation with high-dimensional fixed effects. Stata Journal 20(1), 95–115. <https://doi.org/10.1177/1536867X20909691>

Dell, M., Jones, B.F., Olken, B.A., 2014. What do we learn from the weather? The new climate-economy literature. Journal of Economic Literature 52(3), 740–798. <https://doi.org/10.1257/jel.52.3.740>

Galich, A., Nieland, S., 2023. The impact of weather conditions on mode choice in different spatial areas. Future Transportation 3(3), 1007–1028. <https://doi.org/10.3390/futuretransp3030056>

Gössling, S., Neger, C., Steiger, R., Bell, R., 2023. Weather, climate change, and transport: A review. Natural Hazards 118, 1341–1360. <https://doi.org/10.1007/s11069-023-06054-2>

Heutel, G., Miller, N.H., Molitor, D., 2021. Adaptation and the mortality effects of temperature across U.S. climate regions. Review of Economics and Statistics, advance online publication. <https://doi.org/10.1162/rest_a_00936>

Horanont, T., Phithakkitnukoon, S., Leong, T.W., Sekimoto, Y., Shibasaki, R., 2013. Weather effects on the patterns of people's everyday activities: A study using GPS traces of mobile phone users. PLoS ONE 8(12), e81153. <https://doi.org/10.1371/journal.pone.0081153>

Hsiang, S., 2016. Climate econometrics. Annual Review of Resource Economics 8, 43–75. <https://doi.org/10.1146/annurev-resource-100815-095343>

Knapp, K.R., Kruk, M.C., Levinson, D.H., Diamond, H.J., Neumann, C.J., 2010. The International Best Track Archive for Climate Stewardship (IBTrACS). Bulletin of the American Meteorological Society 91(3), 363–376. <https://doi.org/10.1175/2009BAMS2755.1>

Koetse, M.J., Rietveld, P., 2009. The impact of climate change and weather on transport: An overview of empirical findings. Transportation Research Part D 14(3), 205–221. <https://doi.org/10.1016/j.trd.2008.12.004>

Li, T., Wei, S., Sun, Y., Du, F., Wang, J., 2026. Quantifying the impact of extreme weather event on intercity mobility in urban agglomerations: A Bayesian structural time series analysis. Transport Policy 176, 103925. <https://doi.org/10.1016/j.tranpol.2025.103925>

Li, X., Ma, Q., Wang, W., Wang, B., 2021. Influence of weather conditions on the intercity travel mode choice: A case of Xi'an. Computational Intelligence and Neuroscience 2021, 9969322. <https://doi.org/10.1155/2021/9969322>

Liang, Y., Wang, D., 2025. Heatwaves reduce intra- and intercity human mobility in China. Environmental Research Letters 20, 124027. <https://doi.org/10.1088/1748-9326/ae1e13>

Lin, P., He, Y., Pei, M., Yang, R., 2022. Data-driven spatial-temporal analysis of highway traffic volume considering weather and festival impacts. Travel Behaviour and Society 29, 95–112. <https://doi.org/10.1016/j.tbs.2022.06.001>

Liu, H., Bai, X., 2026. Intercity connectivity enhances urban mobility resilience to extreme rainfall. Nature Climate Change 16, 1037–1044. <https://doi.org/10.1038/s41558-026-02713-x>

Liu, H., Wang, J., Liu, J., Ge, Y., Wang, X., Zhang, C., 2023. Combined and delayed impacts of epidemics and extreme weather on urban mobility recovery. Sustainable Cities and Society 99, 104872. <https://doi.org/10.1016/j.scs.2023.104872>

Liu, H., Kajitani, Y., Yang, Y., Yamaguchi, K., Tatano, H., 2026. Unraveling the impacts of heavy rainfall on cross-city human mobility. Transportation Research Part D 158, 105446. <https://doi.org/10.1016/j.trd.2026.105446>

Lonfat, M., Marks, F.D., Chen, S.S., 2004. Precipitation distribution in tropical cyclones using the Tropical Rainfall Measuring Mission (TRMM) Microwave Imager: A global perspective. Monthly Weather Review 132(7), 1645–1660. [https://doi.org/10.1175/1520-0493(2004)132<1645:PDITCU>2.0.CO;2](<https://doi.org/10.1175/1520-0493(2004)132%3C1645:PDITCU%3E2.0.CO;2>)

Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., et al., 2021. ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. Earth System Science Data 13(9), 4349–4383. <https://doi.org/10.5194/essd-13-4349-2021>

Ren, F., Wu, G., Dong, W., Wang, X., Wang, Y., Ai, W., Li, W., 2006. Changes in tropical cyclone precipitation over China. Geophysical Research Letters 33(20), L20702. <https://doi.org/10.1029/2006GL027951>

Santos Silva, J.M.C., Tenreyro, S., 2006. The log of gravity. Review of Economics and Statistics 88(4), 641–658. <https://doi.org/10.1162/rest.88.4.641>

Seneviratne, S.I., Zhang, X., Adnan, M., Badi, W., et al., 2021. Weather and climate extreme events in a changing climate. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge University Press, pp. 1513–1766. <https://doi.org/10.1017/9781009157896.013>

Tang, J., Zhao, P., Gong, Z., Zhao, H., et al., 2023. Resilience patterns of human mobility in response to extreme urban floods. National Science Review 10(8), nwad097. <https://doi.org/10.1093/nsr/nwad097>

Tao, S., Corcoran, J., Rowe, F., Hickman, M., 2018. To travel or not to travel: ‘Weather’ is the question. Modelling the effect of local weather conditions on bus ridership. Transportation Research Part C 86, 147–167. <https://doi.org/10.1016/j.trc.2017.11.005>

Wang, Q., Taylor, J.E., 2014. Quantifying human mobility perturbation and resilience in Hurricane Sandy. PLoS ONE 9(11), e112608. <https://doi.org/10.1371/journal.pone.0112608>

Wang, Q., Taylor, J.E., 2016. Patterns and limitations of urban human mobility resilience under the influence of multiple types of natural disaster. PLoS ONE 11(1), e0147299. <https://doi.org/10.1371/journal.pone.0147299>

Xiang, Y., Zeng, T., Yu, W., et al., 2026. Distance-dependent patterns of intercity passenger mode share: A multiscale analysis of socioeconomic and spatiotemporal heterogeneity. PLoS ONE 21(9), e0352112. <https://doi.org/10.1371/journal.pone.0352112>

Xie, P., Chen, M., Yang, S., Yatagai, A., Hayasaka, T., Fukushima, Y., Liu, C., 2007. A gauge-based analysis of daily precipitation over East Asia. Journal of Hydrometeorology 8(3), 607–626. <https://doi.org/10.1175/JHM583.1>

Xie, W., Yi, S., Leng, C., Xia, D., Li, M., Zhong, Z., Ye, J., 2022. The evaluation of IMERG and ERA5-Land daily precipitation over China with considering the influence of gauge data bias. Scientific Reports 12, 8085. <https://doi.org/10.1038/s41598-022-12307-0>

Xiong, M., Han, Z., Lu, B., et al., 2022. Effects of rainfall on the weekday traffic flow in major cities of the Beijing–Tianjin–Hebei region, China, in 2021. Advances in Climate Change Research 13(6), 858–867. <https://doi.org/10.1016/j.accre.2022.11.009>

Xu, Z., Zheng, H., Xu, G., Ma, J., 2026. Daily intercity human mobility estimates across Chinese cities from 2020 to 2025. Scientific Data. <https://doi.org/10.1038/s41597-026-08296-8>

Yang, X., Yue, X., Sun, H., Gao, Z., Wang, W., 2021. Impact of weather on freeway origin-destination volume in China. Transportation Research Part A 143, 30–47. <https://doi.org/10.1016/j.tra.2020.11.007>

Yao, Q., Lu, C., Li, M., Zhai, W., Lin, J., Xu, H., 2026. Climate change-induced floods disrupt intercity mobility in China: A national-scale assessment. Travel Behaviour and Society 42, 101132. <https://doi.org/10.1016/j.tbs.2025.101132>

Yao, Y., Liang, L., Zhang, Y., Wang, Y., Hu, Z., Fan, Y., 2025. Resilience patterns of multiscale human mobility under extreme rainfall events using massive individual trajectory data. Annals of the American Association of Geographers 115, 578–602. <https://doi.org/10.1080/24694452.2024.2435927>

Zhao, N., Zhang, Y., Chen, X., Xiao, J., Lu, Y., Zhai, W., Zhai, G., 2025. Resilience measurement and enhancement of population mobility network in Beijing-Tianjin-Hebei urban agglomeration under extreme rainfall impact. Journal of Transport Geography 126, 104253. <https://doi.org/10.1016/j.jtrangeo.2025.104253>

Zhou, M., Wang, D., Li, Q., Yue, Y., et al., 2017. Impacts of weather on public transport ridership: Results from mining data from different sources. Transportation Research Part C 75, 17–29. <https://doi.org/10.1016/j.trc.2016.12.001>
:::
