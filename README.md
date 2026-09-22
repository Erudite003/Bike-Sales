# 🚲 Global Bike Sales Performance Analysis (2013–2023)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811.svg)](powerbi_output/)
[![Interactive Dashboard](https://img.shields.io/badge/Web%20Dashboard-Preview-FF5722.svg)](index.html)

A business intelligence portfolio project analyzing **11 years of global bike-sales data (2013–2023)** to understand revenue growth, profitability, product performance, geographic performance, and seasonality.

The analyzed data records **$85.30M in cumulative revenue**, **$32.23M in gross profit**, and a **37.8% blended gross profit margin** across the study period.

---

## 🎯 Business Objective

The project was designed to move beyond a basic sales dashboard and answer practical business questions:

- Is the business growing over time?
- Which periods contribute most strongly to revenue?
- How stable is profitability across years?
- What seasonal patterns appear in the historical sales data?
- Where should management investigate opportunities, risks, or data-quality issues further?

The analysis emphasizes **evidence-based findings**. Where the dataset cannot establish a cause, explanations are treated as hypotheses rather than facts.

---

## 🧰 Tools Used

- **Microsoft Excel** — data validation, PivotTables, financial analysis, and workbook modeling
- **Python** — chart generation, dashboard generation, and reproducible analytical outputs
- **Power BI** — business intelligence outputs and dashboard assets
- **HTML/CSS/JavaScript** — interactive dashboard presentation
- **Generative AI** — assistance with formulas, debugging, documentation, and quality control; outputs were reviewed and corrected against the source data before inclusion

---

## 📊 Executive KPI Summary

| Metric | Result |
|---|---:|
| 11-Year Cumulative Revenue | **$85,298,198** |
| 11-Year Cumulative Gross Profit | **$32,229,951** |
| Blended Gross Profit Margin | **37.8%** |
| Highest Revenue Year | **2016 — $7,971,310** |
| Lowest Revenue Year | **2020 — $7,550,455** |
| 2013–2023 Revenue Net Change | **+$15,870 (+0.2%)** |
| 2013–2023 Gross Profit Net Change | **+$25,889 (+0.9%)** |
| Highest Aggregate Revenue Month | **December — $9,097,070** |
| Mid-Year Aggregate Peak | **June — $9,044,483** |
| Lowest Aggregate Revenue Month | **August — $5,711,193** |
| Annual Gross Margin Range | **37.4%–38.0% (0.6 percentage points)** |

---

## 📅 Annual Year-over-Year Financial Performance

| Year | Revenue ($) | YoY Revenue Growth | Gross Profit ($) | YoY Gross Profit Growth | Gross Margin |
|:---:|---:|---:|---:|---:|---:|
| 2013 | $7,782,163 | — | $2,933,932 | — | 37.7% |
| 2014 | $7,753,872 | -0.4% | $2,929,264 | -0.2% | 37.8% |
| 2015 | $7,853,503 | +1.3% | $2,963,825 | +1.2% | 37.7% |
| 2016 | $7,971,310 | +1.5% | $3,026,307 | +2.1% | 38.0% |
| 2017 | $7,862,502 | -1.4% | $2,963,335 | -2.1% | 37.7% |
| 2018 | $7,595,956 | -3.4% | $2,867,297 | -3.2% | 37.7% |
| 2019 | $7,865,723 | +3.6% | $2,980,984 | +4.0% | 37.9% |
| 2020 | $7,550,455 | -4.0% | $2,870,185 | -3.7% | 38.0% |
| 2021 | $7,671,898 | +1.6% | $2,895,217 | +0.9% | 37.7% |
| 2022 | $7,592,783 | -1.0% | $2,839,784 | -1.9% | 37.4% |
| 2023 | $7,798,033 | +2.7% | $2,959,821 | +4.2% | 38.0% |

### Annual findings

- Annual revenue remained within a relatively narrow range of approximately **$7.55M–$7.97M** over the period.
- The sharpest revenue contraction occurred in **2020 (-4.0%)**.
- The period after 2020 was mixed: revenue increased in 2021, declined slightly in 2022, and increased by **2.7% in 2023**.
- Gross profit margin remained between **37.4% and 38.0%**, indicating limited variation in the reported margin metric across the 11 years.

---

## 🌊 Monthly Seasonality Analysis

The monthly figures below aggregate the same calendar month across the full 2013–2023 period. Month-to-month percentages therefore describe differences between these **aggregate monthly totals**, not a single chronological year.

| Month | Aggregate Revenue ($) | % of Total | Change vs Prior Aggregate Month |
|---|---:|---:|---:|
| January | $7,009,758 | 8.2% | -22.9% |
| February | $6,834,583 | 8.0% | -2.5% |
| March | $7,351,357 | 8.6% | +7.6% |
| April | $7,602,764 | 8.9% | +3.4% |
| May | $8,840,209 | 10.4% | +16.3% |
| June | $9,044,483 | 10.6% | +2.3% |
| July | $5,722,784 | 6.7% | -36.7% |
| August | $5,711,193 | 6.7% | -0.2% |
| September | $5,842,332 | 6.8% | +2.3% |
| October | $5,995,681 | 7.0% | +2.6% |
| November | $6,245,984 | 7.3% | +4.2% |
| December | $9,097,070 | 10.7% | +45.6% |

### Seasonality findings

- The historical data shows two major aggregate revenue peaks: **June ($9.04M)** and **December ($9.10M)**.
- Revenue falls sharply from June to July and remains low in August, with July approximately **36.7% below June** and August approximately **36.9% below June**.
- **August** is the lowest aggregate-revenue month in the dataset.
- These patterns establish historical seasonality, but the dataset alone does not identify the external causes of those changes.
- A practical next step would be to **test targeted promotions during lower-demand periods** and measure their effect on revenue, quantity sold, and gross profit margin before wider implementation.

---

## 📈 Analytical Visualizations (`charts/`)

- `01_annual_yoy_revenue_and_profit_trajectory.png` — annual revenue and gross-profit trajectory
- `02_gross_margin_resilience_corridor.png` — annual gross-margin range
- `03_monthly_seasonality_bimodal_curve.png` — aggregate monthly revenue pattern
- `04_mom_growth_rate_volatility.png` — month-to-month aggregate revenue changes
- `05_demand_cycle_phase_distribution.png` — grouped monthly demand-period visualization

---

## ⚠️ Analytical Limitations

The project intentionally avoids metrics that the available data cannot support reliably.

Key limitations include:

- no unique **Customer ID** for customer-level retention or lifetime-value analysis
- no unique **Order/Transaction ID** for verified order counts, basket analysis, or Average Order Value
- no confirmed realized-return field for calculating actual return rates
- no inventory-balance or stockout data for calculating inventory turnover or stock availability
- historical relationships should not be interpreted as causal without additional evidence
- monthly aggregate patterns show seasonality in the dataset but do not, by themselves, establish why those patterns occurred

---

## 📂 Repository Structure

```text
├── index.html                         # Interactive growth and seasonality dashboard
├── growth_seasonality_dashboard.html # Standalone dashboard output
├── README.md                          # Project documentation
├── LICENSE                            # MIT License
├── Excel Project Dataset.xlsx        # Source workbook included with the project
├── data/
│   └── bike_sales_data_world_2013_2023_Growth_Analysis.csv
├── excel_models/
│   └── bike_sales_growth_and_seasonality_model.xlsx
├── charts/
│   ├── 01_annual_yoy_revenue_and_profit_trajectory.png
│   ├── 02_gross_margin_resilience_corridor.png
│   ├── 03_monthly_seasonality_bimodal_curve.png
│   ├── 04_mom_growth_rate_volatility.png
│   └── 05_demand_cycle_phase_distribution.png
├── scripts/
│   ├── generate_growth_charts.py
│   ├── build_growth_excel.py
│   ├── build_growth_dashboard.py
│   └── generate_powerbi_output.py
└── powerbi_output/
```

---

## 🚀 Reproducing the Outputs

```bash
# Generate charts
python scripts/generate_growth_charts.py

# Build the Excel analytical model
python scripts/build_growth_excel.py

# Generate Power BI-related outputs
python scripts/generate_powerbi_output.py

# Rebuild the interactive dashboard
python scripts/build_growth_dashboard.py
```

---

## 📌 Portfolio Focus

This project demonstrates:

- business-question framing
- Excel-based analysis and validation
- profitability and growth analysis
- seasonal-pattern analysis
- data visualization
- reproducible Python-assisted outputs
- Power BI workflow exposure
- evidence-based business interpretation
- transparent treatment of dataset limitations
- AI-assisted analytical workflow with human validation

---

## 📄 License

MIT License. Copyright (c) 2026.
