# Bike Sales Power BI Build Guide

This folder contains a Power BI-ready project output generated from `Excel Project Dataset.xlsx`.

## 1. Import data

Recommended quick import:

1. Open Power BI Desktop.
2. Get data > Text/CSV.
3. Select `powerbi_output/data/bike_buyers_clean.csv`.
4. Name the table `Bike Buyers`.
5. Set data types as listed in `powerbi_output/powerbi_assets/Bike_Sales_Model_Spec.json`.

Alternative source import:

- Use `powerbi_output/powerbi_assets/Power_Query_BikeSales.m` in Power Query Advanced Editor to reproduce the cleaning directly from the source Excel workbook.

## 2. Sort columns

In Model view, apply these sort-by-column settings:

- `Age Bracket` -> sort by `Age Bracket Sort`
- `Commute Distance` -> sort by `Commute Distance Sort`
- `Income Band` -> sort by `Income Band Sort`

Then hide the three sort columns plus `Purchase Flag`.

## 3. Add measures

Create the measures in `powerbi_output/powerbi_assets/Bike_Sales_DAX_Measures.dax`.

Minimum required measures:

- `Total Customers`
- `Bike Buyers`
- `Non-Buyers`
- `Bike Purchase Rate`
- `Average Income`
- `Average Age`
- `Purchase Rate Delta vs Overall`

## 4. Apply theme

Import `powerbi_output/powerbi_assets/Bike_Sales_PowerBI_Theme.json` from View > Themes > Browse for themes.

## 5. Recommended report page

Canvas: 16:9, one executive page.

Top row KPI cards:

- Total Customers: **1,000**
- Bike Buyers: **481**
- Purchase Rate: **48.1%**
- Average Income: **$56,360**
- Average Age: **44.2**

Visual layout:

1. Clustered bar chart: `Commute Distance` by `Bike Purchase Rate`.
2. Clustered bar chart: `Age Bracket` by `Bike Purchase Rate`.
3. Clustered bar chart or treemap: `Region` by `Bike Buyers` and `Bike Purchase Rate` tooltip.
4. Stacked bar chart: `Occupation` on axis, `Purchased Bike` on legend, `Total Customers` as value.
5. Matrix: `Marital Status` rows, `Gender` columns, `Bike Purchase Rate` values.
6. Slicers: `Region`, `Gender`, `Marital Status`, `Education`.

## 6. Main findings to call out

- Overall bike purchase rate is **48.1%**.
- Pacific customers have the highest regional purchase rate: **58.9%**.
- The strongest commute segment is `2-5 Miles` at **58.6%**.
- `Middle Age` customers convert best by age bracket at **54.0%**.
- Longer commutes have materially lower conversion: `More than 10 miles` is **29.7%**.

## 7. Suggested dashboard title

**Bike Buyer Profile & Purchase Propensity Dashboard**
