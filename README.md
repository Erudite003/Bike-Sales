# 🚲 Global Bike Sales & Business Intelligence Portfolio (2013–2023)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Power BI Ready](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811.svg)](powerbi_output/)
[![Interactive Dashboard](https://img.shields.io/badge/Web%20Dashboard-Live%20Preview-FF5722.svg)](index.html)

A portfolio-ready business intelligence, financial diagnostic, multi-year YoY trajectory, and cyclical seasonality analytics suite analyzing **11 years of global commercial bicycle sales records** ($85.30M Revenue, $32.23M Gross Profit, 37.8% Gross Margin across 2013–2023).

---

## 📑 Table of Contents
1. [Executive Portfolio KPI Scorecard](#-executive-portfolio-kpi-scorecard)
2. [Multi-Year YoY Growth & Financial Trajectory](#-multi-year-yoy-growth--financial-trajectory)
3. [Monthly Seasonality & Bimodal Demand Curve](#-monthly-seasonality--bimodal-demand-curve)
4. [Gross Margin Resilience Corridor (37.4% – 38.0%)](#-gross-margin-resilience-corridor)
5. [Demand Cycle Phase Classification](#-demand-cycle-phase-classification)
6. [Analytical Visualizations Suite](#-analytical-visualizations-suite)
7. [Power BI & Excel Modeling Assets](#-power-bi--excel-modeling-assets)
8. [Repository Architecture & Directory Structure](#-repository-architecture--directory-structure)
9. [Quickstart & Reproduction Guide](#-quickstart--reproduction-guide)

---

## 🏆 Executive Portfolio KPI Scorecard

```
========================================================================================================
METRIC                          GLOBAL TOTAL          BENCHMARK / STRATEGIC CONTEXT
========================================================================================================
11-Year Cumulative Revenue      $85,298,198.00        $7.75M Annual Average (+0.0% 11-Year CAGR)
11-Year Cumulative Gross Profit $32,229,951.00        37.8% Blended Gross Profit Margin
Peak Revenue Year               $7,971,310.00 (2016)  $3,026,307 Gross Profit (38.0% Margin)
Trough Revenue Year             $7,550,455.00 (2020)  -4.01% YoY Contraction
Annual Margin Stability Band    37.4% – 38.0%         Unbroken ±0.3% Stability Corridor Across 11 Years
Mid-Year Apex Month             $9,044,483.00 (June)  10.6% of Total Global Sales
Summer Slump Impact             -36.7% Contraction    June ($9.04M) ➔ July ($5.72M) & Aug ($5.71M)
Holiday Super Peak              $9,097,070.00 (Dec)   10.7% of Total Global Sales (+45.6% MoM Surge)
========================================================================================================
```

---

## 📅 Multi-Year YoY Growth & Financial Trajectory

| Year | Revenue ($) | Prior Year Rev ($) | YoY Rev Delta ($) | YoY Rev Growth (%) | Gross Profit ($) | Prior Year GP ($) | YoY GP Delta ($) | YoY GP Growth (%) | Gross Margin % | Performance Context |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **2013** | $7,782,163 | — | — | — | $2,933,932 | — | — | — | **37.7%** | Baseline Benchmark Year |
| **2014** | $7,753,872 | $7,782,163 | -$28,291 | -0.4% | $2,929,264 | $2,933,932 | -$4,668 | -0.2% | **37.8%** | Stable (-0.36%) |
| **2015** | $7,853,503 | $7,753,872 | +$99,631 | +1.3% | $2,963,825 | $2,929,264 | +$34,561 | +1.2% | **37.7%** | Expansion (+1.29%) |
| **2016** | $7,971,310 | $7,853,503 | +$117,807 | +1.5% | $3,026,307 | $2,963,825 | +$62,482 | +2.1% | **38.0%** | 🏆 **Peak Year (+1.50%)** |
| **2017** | $7,862,502 | $7,971,310 | -$108,808 | -1.4% | $2,963,335 | $3,026,307 | -$62,972 | -2.1% | **37.7%** | Slight Pullback (-1.36%) |
| **2018** | $7,595,956 | $7,862,502 | -$266,546 | -3.4% | $2,867,297 | $2,963,335 | -$96,038 | -3.2% | **37.7%** | Contraction (-3.39%) |
| **2019** | $7,865,723 | $7,595,956 | +$269,767 | +3.6% | $2,980,984 | $2,867,297 | +$113,687 | +4.0% | **37.9%** | Rebound (+3.55%) |
| **2020** | $7,550,455 | $7,865,723 | -$315,268 | -4.0% | $2,870,185 | $2,980,984 | -$110,799 | -3.7% | **38.0%** | ⚠️ **Trough Year (-4.01%)** |
| **2021** | $7,671,898 | $7,550,455 | +$121,443 | +1.6% | $2,895,217 | $2,870,185 | +$25,032 | +0.9% | **37.7%** | Recovery (+1.61%) |
| **2022** | $7,592,783 | $7,671,898 | -$79,115 | -1.0% | $2,839,784 | $2,895,217 | -$55,433 | -1.9% | **37.4%** | Slight Pullback (-1.03%) |
| **2023** | $7,798,033 | $7,592,783 | +$205,250 | +2.7% | $2,959,821 | $2,839,784 | +$120,037 | +4.2% | **38.0%** | Strong Expansion (+2.70%) |
| **Total** | **$85,298,198** | — | **+$15,870** | **+0.0%** | **$32,229,951** | — | **+$25,889** | **+0.1%** | **37.8%** | **11-Year Cumulative / Avg** |

---

## 🌊 Monthly Seasonality & Bimodal Demand Curve

```text
Month         Revenue ($)      % Total    MoM Delta ($)    MoM Growth (%)    Demand Cycle Phase
---------------------------------------------------------------------------------------------------------
January       $7,009,758.00     8.2%      -$2,087,312.00     -22.9%          Post-Holiday Reset
February      $6,834,583.00     8.0%      -$175,175.00        -2.5%          Late Winter Trough
March         $7,351,357.00     8.6%      +$516,774.00        +7.6%          Spring Ramp-Up
April         $7,602,764.00     8.9%      +$251,407.00        +3.4%          Spring Momentum
May           $8,840,209.00    10.4%      +$1,237,445.00     +16.3%          Early Summer Surge
June          $9,044,483.00    10.6%      +$204,274.00        +2.3%          Mid-Year Apex ($9.04M)
July          $5,722,784.00     6.7%      -$3,321,699.00     -36.7%          Summer Lull (Sharp Drop)
August        $5,711,193.00     6.7%      -$11,591.00         -0.2%          Summer Slump ($5.71M)
September     $5,842,332.00     6.8%      +$131,139.00        +2.3%          Late Q3 Stabilization
October       $5,995,681.00     7.0%      +$153,349.00        +2.6%          Early Q4 Build
November      $6,245,984.00     7.3%      +$250,303.00        +4.2%          Holiday Inflow
December      $9,097,070.00    10.7%      +$2,851,086.00     +45.6%          Annual Super Peak ($9.10M)
---------------------------------------------------------------------------------------------------------
Total / Year  $85,298,198.00   100.0%     —                  —               Full 12-Month Year
```

---

## 📈 Gross Margin Resilience Corridor (37.4% – 38.0%)

Across 11 operating years through economic cycles and pandemic volatility, gross profit margin remained within an ultra-resilient corridor of **37.4% to 38.0%** ($\pm 0.3\%$ maximum variance).

---

## 📊 Analytical Visualizations Suite (`charts/`)

- `01_annual_yoy_revenue_and_profit_trajectory.png`: Grouped YoY bar trajectory with peak/trough annotations.
- `02_gross_margin_resilience_corridor.png`: 11-year margin stability corridor.
- `03_monthly_seasonality_bimodal_curve.png`: 12-month demand curve highlighting the June/December peaks and Summer Slump.
- `04_mom_growth_rate_volatility.png`: Month-over-Month growth rate volatility.
- `05_demand_cycle_phase_distribution.png`: 5-phase operational demand mix doughnut chart.

---

## 📂 Repository Architecture & Directory Structure

```text
├── index.html                                                      # Interactive Executive Growth Dashboard (SPA)
├── growth_seasonality_dashboard.html                               # Standalone Growth & Seasonality Dashboard
├── README.md                                                       # Master Project Documentation
├── LICENSE                                                         # MIT License
├── Excel Project Dataset.xlsx                                      # Original customer project workbook
├── data/
│   └── bike_sales_data_world_2013_2023_Growth_Analysis.csv          # New Growth & Seasonality source dataset
├── excel_models/
│   └── bike_sales_growth_and_seasonality_model.xlsx                # OpenPyXL Dynamic Excel Model with native charts
├── charts/                                                         # 300 DPI Publication-Grade Analytical Visuals
│   ├── 01_annual_yoy_revenue_and_profit_trajectory.png
│   ├── 02_gross_margin_resilience_corridor.png
│   ├── 03_monthly_seasonality_bimodal_curve.png
│   ├── 04_mom_growth_rate_volatility.png
│   └── 05_demand_cycle_phase_distribution.png
├── scripts/
│   ├── generate_growth_charts.py                                   # Python visual chart generator
│   ├── build_growth_excel.py                                       # Dynamic Excel model builder
│   ├── build_growth_dashboard.py                                   # Interactive dashboard generator
│   └── generate_powerbi_output.py                                  # Power BI pipeline generator
└── powerbi_output/                                                 # Generated Power BI deliverables
```

---

## 🚀 Quickstart & Reproduction Guide

```bash
# 1. Regenerate 300 DPI Charts
python scripts/generate_growth_charts.py

# 2. Rebuild Excel Model with Dynamic Native Charts
python scripts/build_growth_excel.py

# 3. Regenerate Power BI deliverables
python scripts/generate_powerbi_output.py
```

---

## 📄 License
MIT License. Copyright (c) 2026.
