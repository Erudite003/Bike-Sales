# Bike Sales Project - Power BI Output

## What was carried out

The Excel workbook was converted into a reproducible, Power BI-ready output package in `powerbi_output/`.

Generated assets:

- `data/bike_buyers_clean.csv` - clean flat table for Power BI import.
- `data/data_quality_report.csv` - data-quality checks and duplicate-removal audit.
- `summary_tables/*.csv` - prebuilt KPI and segment summary exports.
- `powerbi_assets/Power_Query_BikeSales.m` - reproducible Power Query cleaning script.
- `powerbi_assets/Bike_Sales_DAX_Measures.dax` - DAX measures for the semantic model.
- `powerbi_assets/Bike_Sales_PowerBI_Theme.json` - report theme.
- `powerbi_assets/Power_BI_Report_Build_Guide.md` - visual layout guide for Power BI Desktop.
- `report/Bike_Sales_PowerBI_Output.html` - static Power-BI-style dashboard output.
- `BikeSalesPowerBI/` - lightweight PBIP/TMDL scaffold for Power BI Desktop validation.

## Current results

| Metric | Result |
|---|---:|
| Raw rows | 1,026 |
| Raw duplicate rows removed | 26 |
| Clean customer rows | 1,000 |
| Clean duplicate customer IDs | 0 |
| Clean missing values | 0 |
| Bike buyers | 481 |
| Purchase rate | 48.1% |
| Average income | $56,360 |
| Average age | 44.2 |

## Key findings

- The overall purchase rate is **48.1%**.
- `Pacific` is the strongest region with a **58.9%** purchase rate.
- Customers commuting `2-5 Miles` show the strongest commute-distance purchase rate at **58.6%**.
- `Middle Age` customers are the strongest age bracket at **54.0%**.
- Customers commuting `More than 10 miles` are much less likely to purchase, with a **29.7%** purchase rate.

## What could be improved in the original project

1. **Make cleaning reproducible** - the Excel workbook contains manual/implicit steps. Keep Power Query or a script as the source of truth.
2. **Remove raw duplicates before analysis** - the raw sheet has **26** full duplicate rows / duplicate customer IDs.
3. **Fix naming and documentation** - `Workind Sheet` should be `Working Sheet`; add a data dictionary and README.
4. **Use explicit measures instead of implicit pivots** - Power BI DAX measures make KPIs consistent across visuals.
5. **Add sort columns for ordered categories** - commute distance, age bracket, and income band need numeric sort fields.
6. **Track data-quality checks** - duplicate count, missing count, row count, and accepted value checks should be visible in every refresh.
7. **Move from binary-only assets to Git-friendly outputs** - CSV, M, DAX, JSON theme, and PBIP/TMDL files are reviewable in source control.
8. **Add richer business data if available** - purchase date, bike type, price, channel, marketing source, store, and repeat purchases would support revenue, trend, and campaign analysis.

## Rebuild

Run:

```bash
python scripts/generate_powerbi_output.py
```
