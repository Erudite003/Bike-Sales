# Bike Sales

This repository contains a customer bike-purchase dataset and a generated Power BI-ready output package.

## Main files

- `Excel Project Dataset.xlsx` - original workbook.
- `scripts/generate_powerbi_output.py` - reproducible generator for the cleaned data, summaries, and Power BI assets.
- `powerbi_output/` - generated Power BI-ready deliverables.

Open `powerbi_output/report/Bike_Sales_PowerBI_Output.html` for a static dashboard preview, then use `powerbi_output/powerbi_assets/Power_BI_Report_Build_Guide.md` to recreate the report in Power BI Desktop.

## Regenerate outputs

```bash
python scripts/generate_powerbi_output.py
```
