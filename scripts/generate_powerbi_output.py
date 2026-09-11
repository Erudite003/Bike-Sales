#!/usr/bin/env python3
"""Generate Power BI-ready outputs for the Bike Sales project.

This script intentionally uses only the Python standard library so it can run in
minimal environments. It reads the source Excel workbook, exports a clean CSV,
creates summary tables, writes Power Query/DAX assets, and builds a static
Power-BI-style HTML dashboard for quick review.
"""

from __future__ import annotations

import csv
import html
import json
import math
import re
import statistics
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_XLSX = ROOT / "Excel Project Dataset.xlsx"
OUT = ROOT / "powerbi_output"
DATA_DIR = OUT / "data"
SUMMARY_DIR = OUT / "summary_tables"
POWERBI_DIR = OUT / "powerbi_assets"
REPORT_DIR = OUT / "report"

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS = f"{{{MAIN_NS}}}"
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

COMMUTE_ORDER = {
    "0-1 Miles": 1,
    "1-2 Miles": 2,
    "2-5 Miles": 3,
    "5-10 Miles": 4,
    "More than 10 miles": 5,
}
AGE_BRACKET_ORDER = {"Adult": 1, "Middle Age": 2, "Old": 3}
INCOME_BANDS = [
    (0, 39999, "Under $40k", 1),
    (40000, 59999, "$40k-$59k", 2),
    (60000, 79999, "$60k-$79k", 3),
    (80000, 99999, "$80k-$99k", 4),
    (100000, math.inf, "$100k+", 5),
]

CLEAN_FIELDS = [
    "Customer ID",
    "Marital Status",
    "Gender",
    "Income",
    "Income Band",
    "Income Band Sort",
    "Children",
    "Education",
    "Occupation",
    "Home Owner",
    "Cars",
    "Commute Distance",
    "Commute Distance Sort",
    "Region",
    "Age",
    "Age Bracket",
    "Age Bracket Sort",
    "Purchased Bike",
    "Purchase Flag",
]


def ensure_dirs() -> None:
    for directory in [OUT, DATA_DIR, SUMMARY_DIR, POWERBI_DIR, REPORT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def col_to_idx(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    number = 0
    for char in match.group(1):
        number = number * 26 + ord(char) - 64
    return number - 1


def load_shared_strings(zip_file: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zip_file.namelist():
        return []
    root = ET.fromstring(zip_file.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for si in root.findall(NS + "si"):
        values.append("".join(t.text or "" for t in si.iter(NS + "t")))
    return values


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "s":
        v = cell.find(NS + "v")
        return shared_strings[int(v.text)] if v is not None and v.text else ""
    if cell_type == "inlineStr":
        inline = cell.find(NS + "is")
        return "".join(t.text or "" for t in inline.iter(NS + "t")) if inline is not None else ""
    if cell_type == "str":
        v = cell.find(NS + "v")
        return v.text if v is not None and v.text else ""
    if cell_type == "b":
        v = cell.find(NS + "v")
        return "TRUE" if v is not None and v.text == "1" else "FALSE"
    v = cell.find(NS + "v")
    return v.text if v is not None and v.text else ""


def workbook_sheet_map(zip_file: ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(zip_file.read("xl/workbook.xml"))
    rels = ET.fromstring(zip_file.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: "xl/" + rel.attrib["Target"] for rel in rels}
    return {sheet.attrib["name"]: rel_map[sheet.attrib[RID]] for sheet in workbook.find(NS + "sheets")}


def read_xlsx_sheet(workbook_path: Path, sheet_name: str) -> list[list[str]]:
    with ZipFile(workbook_path) as zip_file:
        shared_strings = load_shared_strings(zip_file)
        sheet_map = workbook_sheet_map(zip_file)
        if sheet_name not in sheet_map:
            raise ValueError(f"Sheet {sheet_name!r} not found. Available sheets: {', '.join(sheet_map)}")
        root = ET.fromstring(zip_file.read(sheet_map[sheet_name]))
        rows: list[list[str]] = []
        max_col = 0
        for row in root.find(NS + "sheetData").findall(NS + "row"):
            values: list[str] = []
            for cell in row.findall(NS + "c"):
                idx = col_to_idx(cell.attrib["r"])
                while len(values) <= idx:
                    values.append("")
                values[idx] = cell_value(cell, shared_strings)
                max_col = max(max_col, idx + 1)
            rows.append(values)
        for row in rows:
            row.extend([""] * (max_col - len(row)))
        return rows


def to_int(value: str) -> int:
    return int(float(value))


def income_band(income: int) -> tuple[str, int]:
    for low, high, label, sort in INCOME_BANDS:
        if low <= income <= high:
            return label, sort
    raise ValueError(f"Income is out of expected range: {income}")


def load_records() -> tuple[list[dict[str, object]], dict[str, object]]:
    raw_rows = read_xlsx_sheet(SOURCE_XLSX, "bike_buyers")
    working_rows = read_xlsx_sheet(SOURCE_XLSX, "Workind Sheet")

    raw_headers = raw_rows[0]
    raw_records = [dict(zip(raw_headers, row)) for row in raw_rows[1:] if any(row)]
    raw_id_count = Counter(str(record.get("ID", "")) for record in raw_records)
    raw_full_count = Counter(tuple(record.get(header, "") for header in raw_headers) for record in raw_records)

    headers = working_rows[0]
    records: list[dict[str, object]] = []
    for row in working_rows[1:]:
        if not any(row):
            continue
        original = dict(zip(headers, row))
        income = to_int(original["Income"])
        age = to_int(original["Age"])
        band, band_sort = income_band(income)
        normalized = {
            "Customer ID": to_int(original["ID"]),
            "Marital Status": original["Marital Status"],
            "Gender": original["Gender"],
            "Income": income,
            "Income Band": band,
            "Income Band Sort": band_sort,
            "Children": to_int(original["Children"]),
            "Education": original["Education"],
            "Occupation": original["Occupation"],
            "Home Owner": original["Home Owner"],
            "Cars": to_int(original["Cars"]),
            "Commute Distance": original["Commute Distance"],
            "Commute Distance Sort": COMMUTE_ORDER.get(original["Commute Distance"], 999),
            "Region": original["Region"],
            "Age": age,
            "Age Bracket": original["Age Bracket"],
            "Age Bracket Sort": AGE_BRACKET_ORDER.get(original["Age Bracket"], 999),
            "Purchased Bike": original["Purchased Bike"],
            "Purchase Flag": 1 if original["Purchased Bike"] == "Yes" else 0,
        }
        records.append(normalized)

    missing_by_column = {
        field: sum(1 for record in records if record[field] in ("", None)) for field in CLEAN_FIELDS
    }

    quality = {
        "source_workbook": SOURCE_XLSX.name,
        "raw_rows": len(raw_records),
        "raw_duplicate_customer_ids": sum(count - 1 for count in raw_id_count.values() if count > 1),
        "raw_full_duplicate_rows": sum(count - 1 for count in raw_full_count.values() if count > 1),
        "clean_rows": len(records),
        "clean_duplicate_customer_ids": len(records) - len({record["Customer ID"] for record in records}),
        "clean_missing_values": sum(missing_by_column.values()),
        "missing_by_column": missing_by_column,
    }
    return records, quality


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def safe_mean(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def pct(value: float) -> str:
    return f"{value:.1%}"


def money(value: float) -> str:
    return f"${value:,.0f}"


def number(value: float) -> str:
    return f"{value:,.0f}"


def metric_rows(records: list[dict[str, object]]) -> list[dict[str, object]]:
    buyers = sum(int(r["Purchase Flag"]) for r in records)
    total = len(records)
    non_buyers = total - buyers
    return [
        {"Metric": "Total Customers", "Value": total, "Display Value": number(total)},
        {"Metric": "Bike Buyers", "Value": buyers, "Display Value": number(buyers)},
        {"Metric": "Non-Buyers", "Value": non_buyers, "Display Value": number(non_buyers)},
        {"Metric": "Bike Purchase Rate", "Value": buyers / total if total else 0, "Display Value": pct(buyers / total if total else 0)},
        {"Metric": "Average Income", "Value": round(safe_mean([float(r["Income"]) for r in records]), 2), "Display Value": money(safe_mean([float(r["Income"]) for r in records]))},
        {"Metric": "Average Age", "Value": round(safe_mean([float(r["Age"]) for r in records]), 2), "Display Value": f"{safe_mean([float(r['Age']) for r in records]):.1f}"},
        {"Metric": "Median Income", "Value": statistics.median([float(r["Income"]) for r in records]), "Display Value": money(statistics.median([float(r["Income"]) for r in records]))},
    ]


def summarize_by(records: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    groups: dict[object, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        groups[record[field]].append(record)
    rows: list[dict[str, object]] = []
    for segment, group in groups.items():
        customers = len(group)
        buyers = sum(int(r["Purchase Flag"]) for r in group)
        non_buyers = customers - buyers
        rate = buyers / customers if customers else 0
        rows.append(
            {
                field: segment,
                "Customers": customers,
                "Bike Buyers": buyers,
                "Non-Buyers": non_buyers,
                "Purchase Rate": round(rate, 6),
                "Purchase Rate Display": pct(rate),
                "Average Income": round(safe_mean([float(r["Income"]) for r in group]), 2),
                "Average Age": round(safe_mean([float(r["Age"]) for r in group]), 2),
            }
        )

    sort_field = f"{field} Sort"
    if field == "Commute Distance":
        rows.sort(key=lambda row: COMMUTE_ORDER.get(str(row[field]), 999))
    elif field == "Age Bracket":
        rows.sort(key=lambda row: AGE_BRACKET_ORDER.get(str(row[field]), 999))
    elif field == "Income Band":
        rows.sort(key=lambda row: next(sort for _, _, label, sort in INCOME_BANDS if label == row[field]))
    elif sort_field in records[0]:
        rows.sort(key=lambda row: row.get(sort_field, 999))
    else:
        rows.sort(key=lambda row: str(row[field]))
    return rows


def write_summary_tables(records: list[dict[str, object]], quality: dict[str, object]) -> dict[str, list[dict[str, object]]]:
    write_csv(DATA_DIR / "bike_buyers_clean.csv", records, CLEAN_FIELDS)

    quality_rows = [
        {"Metric": "Source workbook", "Value": quality["source_workbook"]},
        {"Metric": "Raw rows", "Value": quality["raw_rows"]},
        {"Metric": "Raw duplicate customer IDs", "Value": quality["raw_duplicate_customer_ids"]},
        {"Metric": "Raw full duplicate rows", "Value": quality["raw_full_duplicate_rows"]},
        {"Metric": "Clean rows", "Value": quality["clean_rows"]},
        {"Metric": "Clean duplicate customer IDs", "Value": quality["clean_duplicate_customer_ids"]},
        {"Metric": "Clean missing values", "Value": quality["clean_missing_values"]},
    ]
    for column, missing_count in quality["missing_by_column"].items():
        quality_rows.append({"Metric": f"Missing values - {column}", "Value": missing_count})
    write_csv(DATA_DIR / "data_quality_report.csv", quality_rows, ["Metric", "Value"])

    summary: dict[str, list[dict[str, object]]] = {"kpis": metric_rows(records)}
    write_csv(SUMMARY_DIR / "key_metrics.csv", summary["kpis"])

    for field in [
        "Region",
        "Commute Distance",
        "Age Bracket",
        "Income Band",
        "Occupation",
        "Education",
        "Gender",
        "Marital Status",
        "Home Owner",
        "Cars",
        "Children",
    ]:
        rows = summarize_by(records, field)
        summary[field] = rows
        filename = "purchase_rate_by_" + field.lower().replace(" ", "_").replace("-", "_") + ".csv"
        write_csv(SUMMARY_DIR / filename, rows)

    return summary


def write_dax_measures() -> None:
    dax = """// Bike Sales Power BI measures
// Table name assumed: 'Bike Buyers'

Total Customers = COUNTROWS('Bike Buyers')

Bike Buyers =
CALCULATE(
    [Total Customers],
    'Bike Buyers'[Purchased Bike] = "Yes"
)

Non-Buyers = [Total Customers] - [Bike Buyers]

Bike Purchase Rate = DIVIDE([Bike Buyers], [Total Customers])

Average Income = AVERAGE('Bike Buyers'[Income])

Average Age = AVERAGE('Bike Buyers'[Age])

Median Income = MEDIAN('Bike Buyers'[Income])

Average Income - Buyers =
CALCULATE(
    [Average Income],
    'Bike Buyers'[Purchased Bike] = "Yes"
)

Average Income - Non-Buyers =
CALCULATE(
    [Average Income],
    'Bike Buyers'[Purchased Bike] = "No"
)

Purchase Rate Delta vs Overall =
[Bike Purchase Rate]
    - CALCULATE([Bike Purchase Rate], ALL('Bike Buyers'))

High-Propensity Customers =
CALCULATE(
    [Total Customers],
    'Bike Buyers'[Age Bracket] = "Middle Age",
    'Bike Buyers'[Cars] <= 1
)

High-Propensity Buyers =
CALCULATE(
    [Bike Buyers],
    'Bike Buyers'[Age Bracket] = "Middle Age",
    'Bike Buyers'[Cars] <= 1
)

High-Propensity Purchase Rate =
DIVIDE([High-Propensity Buyers], [High-Propensity Customers])
"""
    (POWERBI_DIR / "Bike_Sales_DAX_Measures.dax").write_text(dax, encoding="utf-8")


def write_power_query() -> None:
    # Power Query uses a relative-path parameter pattern when the workbook is stored next to the report.
    m = r'''// Bike Sales Power Query M
// Option A: update ExcelWorkbookPath to the local path of "Excel Project Dataset.xlsx".
// Option B: use the generated CSV in powerbi_output/data/bike_buyers_clean.csv and skip this query.

let
    ExcelWorkbookPath = "C:\Path\To\Excel Project Dataset.xlsx",
    Source = Excel.Workbook(File.Contents(ExcelWorkbookPath), null, true),
    RawSheet = Source{[Item="bike_buyers", Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(RawSheet, [PromoteAllScalars=true]),
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"ID", Int64.Type},
            {"Marital Status", type text},
            {"Gender", type text},
            {"Income", Int64.Type},
            {"Children", Int64.Type},
            {"Education", type text},
            {"Occupation", type text},
            {"Home Owner", type text},
            {"Cars", Int64.Type},
            {"Commute Distance", type text},
            {"Region", type text},
            {"Age", Int64.Type},
            {"Purchased Bike", type text}
        }
    ),
    ExpandedMaritalStatus = Table.ReplaceValue(TypedColumns, "M", "Married", Replacer.ReplaceText, {"Marital Status"}),
    ExpandedMaritalStatus2 = Table.ReplaceValue(ExpandedMaritalStatus, "S", "Single", Replacer.ReplaceText, {"Marital Status"}),
    ExpandedGender = Table.ReplaceValue(ExpandedMaritalStatus2, "F", "Female", Replacer.ReplaceText, {"Gender"}),
    ExpandedGender2 = Table.ReplaceValue(ExpandedGender, "M", "Male", Replacer.ReplaceText, {"Gender"}),
    RemovedDuplicates = Table.Distinct(ExpandedGender2, {"ID"}),
    AddedAgeBracket = Table.AddColumn(
        RemovedDuplicates,
        "Age Bracket",
        each if [Age] < 31 then "Adult" else if [Age] <= 54 then "Middle Age" else "Old",
        type text
    ),
    AddedAgeBracketSort = Table.AddColumn(
        AddedAgeBracket,
        "Age Bracket Sort",
        each if [Age Bracket] = "Adult" then 1 else if [Age Bracket] = "Middle Age" then 2 else 3,
        Int64.Type
    ),
    AddedCommuteSort = Table.AddColumn(
        AddedAgeBracketSort,
        "Commute Distance Sort",
        each
            if [Commute Distance] = "0-1 Miles" then 1
            else if [Commute Distance] = "1-2 Miles" then 2
            else if [Commute Distance] = "2-5 Miles" then 3
            else if [Commute Distance] = "5-10 Miles" then 4
            else 5,
        Int64.Type
    ),
    AddedIncomeBand = Table.AddColumn(
        AddedCommuteSort,
        "Income Band",
        each
            if [Income] < 40000 then "Under $40k"
            else if [Income] < 60000 then "$40k-$59k"
            else if [Income] < 80000 then "$60k-$79k"
            else if [Income] < 100000 then "$80k-$99k"
            else "$100k+",
        type text
    ),
    AddedIncomeBandSort = Table.AddColumn(
        AddedIncomeBand,
        "Income Band Sort",
        each
            if [Income Band] = "Under $40k" then 1
            else if [Income Band] = "$40k-$59k" then 2
            else if [Income Band] = "$60k-$79k" then 3
            else if [Income Band] = "$80k-$99k" then 4
            else 5,
        Int64.Type
    ),
    AddedPurchaseFlag = Table.AddColumn(
        AddedIncomeBandSort,
        "Purchase Flag",
        each if [Purchased Bike] = "Yes" then 1 else 0,
        Int64.Type
    ),
    RenamedID = Table.RenameColumns(AddedPurchaseFlag, {{"ID", "Customer ID"}}),
    ReorderedColumns = Table.ReorderColumns(
        RenamedID,
        {
            "Customer ID", "Marital Status", "Gender", "Income", "Income Band", "Income Band Sort",
            "Children", "Education", "Occupation", "Home Owner", "Cars", "Commute Distance",
            "Commute Distance Sort", "Region", "Age", "Age Bracket", "Age Bracket Sort",
            "Purchased Bike", "Purchase Flag"
        }
    )
in
    ReorderedColumns
'''
    (POWERBI_DIR / "Power_Query_BikeSales.m").write_text(m, encoding="utf-8")


def write_theme() -> None:
    theme = {
        "name": "Bike Sales Executive Theme",
        "dataColors": ["#00A878", "#304FFE", "#FFB000", "#E84855", "#7B2CBF", "#0F8B8D", "#F9844A"],
        "background": "#F7F9FC",
        "foreground": "#1D2733",
        "tableAccent": "#00A878",
        "visualStyles": {
            "*": {
                "*": {
                    "title": [{"fontColor": {"solid": {"color": "#1D2733"}}, "fontSize": 12}],
                    "background": [{"color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}],
                    "border": [{"show": True, "color": {"solid": {"color": "#E5EAF2"}}, "radius": 8}],
                }
            }
        },
    }
    (POWERBI_DIR / "Bike_Sales_PowerBI_Theme.json").write_text(json.dumps(theme, indent=2), encoding="utf-8")


def write_model_spec() -> None:
    spec = {
        "table_name": "Bike Buyers",
        "source_file": "powerbi_output/data/bike_buyers_clean.csv",
        "grain": "One row per unique customer/customer survey response",
        "columns": [
            {"name": "Customer ID", "type": "Whole number", "summarize_by": "Do not summarize"},
            {"name": "Marital Status", "type": "Text"},
            {"name": "Gender", "type": "Text"},
            {"name": "Income", "type": "Whole number", "format": "$#,0"},
            {"name": "Income Band", "type": "Text", "sort_by": "Income Band Sort"},
            {"name": "Income Band Sort", "type": "Whole number", "hide": True},
            {"name": "Children", "type": "Whole number"},
            {"name": "Education", "type": "Text"},
            {"name": "Occupation", "type": "Text"},
            {"name": "Home Owner", "type": "Text"},
            {"name": "Cars", "type": "Whole number"},
            {"name": "Commute Distance", "type": "Text", "sort_by": "Commute Distance Sort"},
            {"name": "Commute Distance Sort", "type": "Whole number", "hide": True},
            {"name": "Region", "type": "Text"},
            {"name": "Age", "type": "Whole number"},
            {"name": "Age Bracket", "type": "Text", "sort_by": "Age Bracket Sort"},
            {"name": "Age Bracket Sort", "type": "Whole number", "hide": True},
            {"name": "Purchased Bike", "type": "Text"},
            {"name": "Purchase Flag", "type": "Whole number", "hide": True},
        ],
        "recommended_measures_file": "powerbi_output/powerbi_assets/Bike_Sales_DAX_Measures.dax",
        "recommended_theme_file": "powerbi_output/powerbi_assets/Bike_Sales_PowerBI_Theme.json",
    }
    (POWERBI_DIR / "Bike_Sales_Model_Spec.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")


def write_build_guide(summary: dict[str, list[dict[str, object]]]) -> None:
    build_guide = f"""# Bike Sales Power BI Build Guide

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

- Total Customers: **{summary['kpis'][0]['Display Value']}**
- Bike Buyers: **{summary['kpis'][1]['Display Value']}**
- Purchase Rate: **{summary['kpis'][3]['Display Value']}**
- Average Income: **{summary['kpis'][4]['Display Value']}**
- Average Age: **{summary['kpis'][5]['Display Value']}**

Visual layout:

1. Clustered bar chart: `Commute Distance` by `Bike Purchase Rate`.
2. Clustered bar chart: `Age Bracket` by `Bike Purchase Rate`.
3. Clustered bar chart or treemap: `Region` by `Bike Buyers` and `Bike Purchase Rate` tooltip.
4. Stacked bar chart: `Occupation` on axis, `Purchased Bike` on legend, `Total Customers` as value.
5. Matrix: `Marital Status` rows, `Gender` columns, `Bike Purchase Rate` values.
6. Slicers: `Region`, `Gender`, `Marital Status`, `Education`.

## 6. Main findings to call out

- Overall bike purchase rate is **{summary['kpis'][3]['Display Value']}**.
- Pacific customers have the highest regional purchase rate: **{next(r for r in summary['Region'] if r['Region'] == 'Pacific')['Purchase Rate Display']}**.
- The strongest commute segment is `2-5 Miles` at **{next(r for r in summary['Commute Distance'] if r['Commute Distance'] == '2-5 Miles')['Purchase Rate Display']}**.
- `Middle Age` customers convert best by age bracket at **{next(r for r in summary['Age Bracket'] if r['Age Bracket'] == 'Middle Age')['Purchase Rate Display']}**.
- Longer commutes have materially lower conversion: `More than 10 miles` is **{next(r for r in summary['Commute Distance'] if r['Commute Distance'] == 'More than 10 miles')['Purchase Rate Display']}**.

## 7. Suggested dashboard title

**Bike Buyer Profile & Purchase Propensity Dashboard**
"""
    (POWERBI_DIR / "Power_BI_Report_Build_Guide.md").write_text(build_guide, encoding="utf-8")


def svg_bar_chart(rows: list[dict[str, object]], category: str, value: str, title: str, value_type: str = "pct") -> str:
    width = 720
    bar_area = 430
    left = 190
    top = 52
    row_h = 42
    height = top + row_h * len(rows) + 24
    max_value = max(float(row[value]) for row in rows) or 1
    if value_type == "pct":
        max_value = max(max_value, 0.65)
    svg = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">']
    svg.append(f'<text x="0" y="24" class="chart-title">{html.escape(title)}</text>')
    svg.append(f'<line x1="{left}" y1="{top-18}" x2="{left+bar_area}" y2="{top-18}" class="axis" />')
    for i, row in enumerate(rows):
        y = top + i * row_h
        val = float(row[value])
        bar_w = max(2, (val / max_value) * bar_area)
        label = str(row[category])
        display = pct(val) if value_type == "pct" else number(val)
        svg.append(f'<text x="0" y="{y+18}" class="axis-label">{html.escape(label)}</text>')
        svg.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="24" rx="6" class="bar" />')
        svg.append(f'<text x="{left+bar_w+10:.1f}" y="{y+18}" class="value-label">{html.escape(display)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def svg_stacked_buyers(rows: list[dict[str, object]], category: str, title: str) -> str:
    width = 720
    bar_area = 430
    left = 190
    top = 62
    row_h = 42
    height = top + row_h * len(rows) + 44
    max_total = max(float(row["Customers"]) for row in rows) or 1
    svg = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">']
    svg.append(f'<text x="0" y="24" class="chart-title">{html.escape(title)}</text>')
    svg.append(f'<rect x="{left}" y="36" width="14" height="14" class="bar yes" /><text x="{left+20}" y="48" class="legend">Buyers</text>')
    svg.append(f'<rect x="{left+90}" y="36" width="14" height="14" class="bar no" /><text x="{left+110}" y="48" class="legend">Non-buyers</text>')
    for i, row in enumerate(rows):
        y = top + i * row_h
        buyers = float(row["Bike Buyers"])
        non_buyers = float(row["Non-Buyers"])
        total = buyers + non_buyers
        buyer_w = (buyers / max_total) * bar_area
        non_w = (non_buyers / max_total) * bar_area
        label = str(row[category])
        svg.append(f'<text x="0" y="{y+18}" class="axis-label">{html.escape(label)}</text>')
        svg.append(f'<rect x="{left}" y="{y}" width="{buyer_w:.1f}" height="24" rx="6" class="bar yes" />')
        svg.append(f'<rect x="{left+buyer_w:.1f}" y="{y}" width="{non_w:.1f}" height="24" rx="6" class="bar no" />')
        svg.append(f'<text x="{left+buyer_w+non_w+10:.1f}" y="{y+18}" class="value-label">{int(total):,} total</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def html_table(rows: list[dict[str, object]], columns: list[str], title: str) -> str:
    head = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    body_rows = []
    for row in rows:
        cells = []
        for col in columns:
            value = row[col]
            if col == "Purchase Rate":
                rendered = pct(float(value))
            elif col == "Average Income":
                rendered = money(float(value))
            elif isinstance(value, float):
                rendered = f"{value:,.2f}"
            else:
                rendered = str(value)
            cells.append(f"<td>{html.escape(rendered)}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"""
    <section class="card wide">
      <h2>{html.escape(title)}</h2>
      <table>
        <thead><tr>{head}</tr></thead>
        <tbody>{''.join(body_rows)}</tbody>
      </table>
    </section>
    """


def write_html_dashboard(summary: dict[str, list[dict[str, object]]], quality: dict[str, object]) -> None:
    kpis = {row["Metric"]: row["Display Value"] for row in summary["kpis"]}
    cards = [
        ("Total Customers", kpis["Total Customers"], "Unique customer records"),
        ("Bike Buyers", kpis["Bike Buyers"], "Purchased Bike = Yes"),
        ("Purchase Rate", kpis["Bike Purchase Rate"], "Buyers / total customers"),
        ("Avg Income", kpis["Average Income"], "Across all customers"),
        ("Avg Age", kpis["Average Age"], "Customer age"),
    ]
    card_html = "\n".join(
        f'<div class="kpi"><div class="kpi-label">{html.escape(label)}</div><div class="kpi-value">{html.escape(value)}</div><div class="kpi-note">{html.escape(note)}</div></div>'
        for label, value, note in cards
    )

    commute = summary["Commute Distance"]
    age = summary["Age Bracket"]
    region_rate = sorted(summary["Region"], key=lambda row: float(row["Purchase Rate"]), reverse=True)
    occupation = sorted(summary["Occupation"], key=lambda row: int(row["Customers"]), reverse=True)
    income_band = summary["Income Band"]

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bike Sales Power BI Output</title>
  <style>
    :root {{
      --bg: #f6f8fb;
      --panel: #ffffff;
      --ink: #1d2733;
      --muted: #667085;
      --green: #00a878;
      --blue: #304ffe;
      --amber: #ffb000;
      --red: #e84855;
      --border: #e5eaf2;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: "Segoe UI", Arial, sans-serif; }}
    .wrap {{ max-width: 1260px; margin: 0 auto; padding: 28px; }}
    header {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; margin-bottom: 20px; }}
    h1 {{ margin: 0; font-size: 30px; letter-spacing: -0.02em; }}
    .subtitle {{ margin-top: 8px; color: var(--muted); line-height: 1.45; }}
    .badge {{ background: #eaf8f2; color: #067a59; border: 1px solid #bbebd8; padding: 8px 12px; border-radius: 999px; font-size: 13px; white-space: nowrap; }}
    .kpis {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 14px; margin-bottom: 16px; }}
    .kpi, .card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 16px; box-shadow: 0 8px 22px rgba(16, 24, 40, 0.06); }}
    .kpi {{ padding: 18px; }}
    .kpi-label {{ color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .kpi-value {{ font-size: 32px; font-weight: 750; margin-top: 10px; }}
    .kpi-note {{ color: var(--muted); font-size: 13px; margin-top: 8px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    .card {{ padding: 18px; overflow: hidden; }}
    .wide {{ grid-column: 1 / -1; }}
    h2 {{ margin: 0 0 14px; font-size: 18px; }}
    .insights {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin: 16px 0; }}
    .insight {{ padding: 16px; background: #102a43; color: white; border-radius: 16px; }}
    .insight strong {{ display: block; font-size: 24px; margin-bottom: 4px; }}
    .insight span {{ color: #d9e7f5; font-size: 13px; line-height: 1.4; }}
    svg {{ width: 100%; height: auto; display: block; }}
    .chart-title {{ font-size: 18px; font-weight: 700; fill: var(--ink); }}
    .axis {{ stroke: var(--border); stroke-width: 1; }}
    .axis-label {{ font-size: 13px; fill: var(--ink); }}
    .value-label, .legend {{ font-size: 13px; fill: var(--muted); }}
    .bar {{ fill: var(--green); }}
    .bar.yes {{ fill: var(--green); }}
    .bar.no {{ fill: #d0d8e8; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); text-align: left; }}
    th {{ background: #f0f4f9; color: #344054; font-weight: 700; }}
    tr:last-child td {{ border-bottom: 0; }}
    .footer {{ color: var(--muted); font-size: 13px; margin-top: 18px; line-height: 1.5; }}
    code {{ background: #eef2f7; padding: 2px 5px; border-radius: 5px; }}
    @media (max-width: 980px) {{ .kpis, .grid, .insights {{ grid-template-columns: 1fr; }} header {{ display: block; }} .badge {{ display: inline-block; margin-top: 12px; }} }}
  </style>
</head>
<body>
  <main class="wrap">
    <header>
      <div>
        <h1>Bike Buyer Profile & Purchase Propensity Dashboard</h1>
        <div class="subtitle">Static Power-BI-style output generated from the cleaned customer survey data. Use the accompanying CSV, Power Query, DAX, and theme files to recreate this in Power BI Desktop.</div>
      </div>
      <div class="badge">Clean rows: {quality['clean_rows']:,} | Raw duplicate rows removed: {quality['raw_full_duplicate_rows']}</div>
    </header>

    <section class="kpis">{card_html}</section>

    <section class="insights">
      <div class="insight"><strong>{next(r for r in region_rate if r['Region'] == 'Pacific')['Purchase Rate Display']}</strong><span>Pacific is the strongest region by bike purchase rate.</span></div>
      <div class="insight"><strong>{next(r for r in commute if r['Commute Distance'] == '2-5 Miles')['Purchase Rate Display']}</strong><span>Customers commuting 2-5 miles are the strongest commute-distance segment.</span></div>
      <div class="insight"><strong>{next(r for r in age if r['Age Bracket'] == 'Middle Age')['Purchase Rate Display']}</strong><span>Middle Age customers convert best among age brackets.</span></div>
    </section>

    <section class="grid">
      <div class="card">{svg_bar_chart(commute, 'Commute Distance', 'Purchase Rate', 'Bike Purchase Rate by Commute Distance')}</div>
      <div class="card">{svg_bar_chart(age, 'Age Bracket', 'Purchase Rate', 'Bike Purchase Rate by Age Bracket')}</div>
      <div class="card">{svg_bar_chart(region_rate, 'Region', 'Purchase Rate', 'Bike Purchase Rate by Region')}</div>
      <div class="card">{svg_stacked_buyers(occupation, 'Occupation', 'Buyer / Non-Buyer Mix by Occupation')}</div>
      <div class="card wide">{svg_bar_chart(income_band, 'Income Band', 'Purchase Rate', 'Bike Purchase Rate by Income Band')}</div>
      {html_table(region_rate, ['Region', 'Customers', 'Bike Buyers', 'Purchase Rate', 'Average Income'], 'Regional Summary')}
    </section>

    <p class="footer">Files generated in <code>powerbi_output</code>: clean CSV, summary tables, Power Query M, DAX measures, model specification, theme JSON, report build guide, and this HTML dashboard.</p>
  </main>
</body>
</html>
"""
    (REPORT_DIR / "Bike_Sales_PowerBI_Output.html").write_text(html_doc, encoding="utf-8")


def write_pbip_scaffold() -> None:
    """Create a lightweight PBIP/TMDL scaffold for source-control-friendly Power BI work.

    The scaffold is intentionally conservative: it defines the project structure,
    semantic model metadata, and measures. Power BI Desktop may still need to bind
    the local CSV path on first open because this environment cannot refresh a
    native Power BI model.
    """
    project = OUT / "BikeSalesPowerBI"
    semantic = project / "BikeSalesPowerBI.SemanticModel" / "definition"
    tables = semantic / "tables"
    report = project / "BikeSalesPowerBI.Report" / "definition" / "pages" / "ReportSectionOverview"
    tables.mkdir(parents=True, exist_ok=True)
    report.mkdir(parents=True, exist_ok=True)

    (project / "BikeSalesPowerBI.pbip").write_text(
        json.dumps(
            {
                "version": "1.0",
                "artifacts": [{"report": {"path": "BikeSalesPowerBI.Report"}}],
                "settings": {"enableAutoRecovery": True},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (project / "BikeSalesPowerBI.SemanticModel" / "definition.pbism").write_text(
        json.dumps({"version": "1.0", "datasetReference": {"byPath": None, "byConnection": None}}, indent=2),
        encoding="utf-8",
    )
    (semantic / "database.tmdl").write_text("database 'BikeSalesPowerBI'\n\tcompatibilityLevel: 1567\n", encoding="utf-8")
    (semantic / "model.tmdl").write_text(
        "model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tdiscourageImplicitMeasures: true\n\tsourceQueryCulture: en-US\n",
        encoding="utf-8",
    )
    (semantic / "relationships.tmdl").write_text("", encoding="utf-8")
    (semantic / "expressions.tmdl").write_text(
        'expression CsvPath = "../data/bike_buyers_clean.csv" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n',
        encoding="utf-8",
    )
    table_tmdl = """table 'Bike Buyers'

	partition 'Bike Buyers' = m
		mode: import
		source =
			let
				Source = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Columns=19, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
				#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
				#"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"Customer ID", Int64.Type}, {"Marital Status", type text}, {"Gender", type text}, {"Income", Int64.Type}, {"Income Band", type text}, {"Income Band Sort", Int64.Type}, {"Children", Int64.Type}, {"Education", type text}, {"Occupation", type text}, {"Home Owner", type text}, {"Cars", Int64.Type}, {"Commute Distance", type text}, {"Commute Distance Sort", Int64.Type}, {"Region", type text}, {"Age", Int64.Type}, {"Age Bracket", type text}, {"Age Bracket Sort", Int64.Type}, {"Purchased Bike", type text}, {"Purchase Flag", Int64.Type}})
			in
				#"Changed Type"

	measure 'Total Customers' = COUNTROWS('Bike Buyers')
		formatString: #,##0

	measure 'Bike Buyers' = CALCULATE([Total Customers], 'Bike Buyers'[Purchased Bike] = "Yes")
		formatString: #,##0

	measure 'Non-Buyers' = [Total Customers] - [Bike Buyers]
		formatString: #,##0

	measure 'Bike Purchase Rate' = DIVIDE([Bike Buyers], [Total Customers])
		formatString: 0.0%

	measure 'Average Income' = AVERAGE('Bike Buyers'[Income])
		formatString: $#,##0

	measure 'Average Age' = AVERAGE('Bike Buyers'[Age])
		formatString: 0.0

	column 'Customer ID'
		dataType: int64
		sourceColumn: "Customer ID"
		summarizeBy: none

	column 'Marital Status'
		dataType: string
		sourceColumn: "Marital Status"
		summarizeBy: none

	column Gender
		dataType: string
		sourceColumn: Gender
		summarizeBy: none

	column Income
		dataType: int64
		sourceColumn: Income
		summarizeBy: sum
		formatString: $#,##0

	column 'Income Band'
		dataType: string
		sourceColumn: "Income Band"
		summarizeBy: none

	column 'Income Band Sort'
		dataType: int64
		isHidden
		sourceColumn: "Income Band Sort"
		summarizeBy: none

	column Children
		dataType: int64
		sourceColumn: Children
		summarizeBy: sum

	column Education
		dataType: string
		sourceColumn: Education
		summarizeBy: none

	column Occupation
		dataType: string
		sourceColumn: Occupation
		summarizeBy: none

	column 'Home Owner'
		dataType: string
		sourceColumn: "Home Owner"
		summarizeBy: none

	column Cars
		dataType: int64
		sourceColumn: Cars
		summarizeBy: sum

	column 'Commute Distance'
		dataType: string
		sourceColumn: "Commute Distance"
		summarizeBy: none

	column 'Commute Distance Sort'
		dataType: int64
		isHidden
		sourceColumn: "Commute Distance Sort"
		summarizeBy: none

	column Region
		dataType: string
		sourceColumn: Region
		summarizeBy: none

	column Age
		dataType: int64
		sourceColumn: Age
		summarizeBy: average

	column 'Age Bracket'
		dataType: string
		sourceColumn: "Age Bracket"
		summarizeBy: none

	column 'Age Bracket Sort'
		dataType: int64
		isHidden
		sourceColumn: "Age Bracket Sort"
		summarizeBy: none

	column 'Purchased Bike'
		dataType: string
		sourceColumn: "Purchased Bike"
		summarizeBy: none

	column 'Purchase Flag'
		dataType: int64
		isHidden
		sourceColumn: "Purchase Flag"
		summarizeBy: sum
"""
    (tables / "Bike Buyers.tmdl").write_text(table_tmdl, encoding="utf-8")

    (project / "BikeSalesPowerBI.Report" / "definition.pbir").write_text(
        json.dumps(
            {
                "version": "1.0",
                "datasetReference": {
                    "byPath": {"path": "../BikeSalesPowerBI.SemanticModel"},
                    "byConnection": None,
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (project / "BikeSalesPowerBI.Report" / "definition" / "version.json").write_text(
        json.dumps({"version": "1.0.0"}, indent=2), encoding="utf-8"
    )
    (project / "BikeSalesPowerBI.Report" / "definition" / "report.json").write_text(
        json.dumps(
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
                "themeCollection": {
                    "baseTheme": {"name": "CY24SU06", "reportVersionAtImport": "5.55", "type": "SharedResources"}
                },
                "config": {"version": 5, "defaultDrillFilterOtherVisuals": True},
                "objects": {},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (project / "BikeSalesPowerBI.Report" / "definition" / "pages" / "pages.json").write_text(
        json.dumps({"pageOrder": ["ReportSectionOverview"], "activePageName": "ReportSectionOverview"}, indent=2),
        encoding="utf-8",
    )
    (report / "page.json").write_text(
        json.dumps(
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
                "name": "ReportSectionOverview",
                "displayName": "Bike Sales Overview",
                "displayOption": "FitToPage",
                "height": 720,
                "width": 1280,
                "objects": {},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (report / "visuals").mkdir(exist_ok=True)
    (project / "README.md").write_text(
        """# Bike Sales Power BI PBIP Scaffold

This is a source-control-friendly Power BI project scaffold. The semantic model TMDL defines the `Bike Buyers` table, columns, and core measures. Because this Linux sandbox cannot run Power BI Desktop, validate/open `BikeSalesPowerBI.pbip` in Power BI Desktop and update the `CsvPath` parameter if prompted.

For a finished visual layout, use `../powerbi_assets/Power_BI_Report_Build_Guide.md` and the static dashboard at `../report/Bike_Sales_PowerBI_Output.html`.
""",
        encoding="utf-8",
    )


def write_project_readme(summary: dict[str, list[dict[str, object]]], quality: dict[str, object]) -> None:
    readme = f"""# Bike Sales Project - Power BI Output

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
| Raw rows | {quality['raw_rows']:,} |
| Raw duplicate rows removed | {quality['raw_full_duplicate_rows']:,} |
| Clean customer rows | {quality['clean_rows']:,} |
| Clean duplicate customer IDs | {quality['clean_duplicate_customer_ids']:,} |
| Clean missing values | {quality['clean_missing_values']:,} |
| Bike buyers | {summary['kpis'][1]['Display Value']} |
| Purchase rate | {summary['kpis'][3]['Display Value']} |
| Average income | {summary['kpis'][4]['Display Value']} |
| Average age | {summary['kpis'][5]['Display Value']} |

## Key findings

- The overall purchase rate is **{summary['kpis'][3]['Display Value']}**.
- `Pacific` is the strongest region with a **{next(r for r in summary['Region'] if r['Region'] == 'Pacific')['Purchase Rate Display']}** purchase rate.
- Customers commuting `2-5 Miles` show the strongest commute-distance purchase rate at **{next(r for r in summary['Commute Distance'] if r['Commute Distance'] == '2-5 Miles')['Purchase Rate Display']}**.
- `Middle Age` customers are the strongest age bracket at **{next(r for r in summary['Age Bracket'] if r['Age Bracket'] == 'Middle Age')['Purchase Rate Display']}**.
- Customers commuting `More than 10 miles` are much less likely to purchase, with a **{next(r for r in summary['Commute Distance'] if r['Commute Distance'] == 'More than 10 miles')['Purchase Rate Display']}** purchase rate.

## What could be improved in the original project

1. **Make cleaning reproducible** - the Excel workbook contains manual/implicit steps. Keep Power Query or a script as the source of truth.
2. **Remove raw duplicates before analysis** - the raw sheet has **{quality['raw_full_duplicate_rows']}** full duplicate rows / duplicate customer IDs.
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
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def write_root_readme() -> None:
    root_readme = """# Bike Sales

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
"""
    (ROOT / "README.md").write_text(root_readme, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    records, quality = load_records()
    summary = write_summary_tables(records, quality)
    write_dax_measures()
    write_power_query()
    write_theme()
    write_model_spec()
    write_build_guide(summary)
    write_html_dashboard(summary, quality)
    write_pbip_scaffold()
    write_project_readme(summary, quality)
    write_root_readme()
    print(f"Generated Power BI output in {OUT.relative_to(ROOT)}")
    print(f"Clean rows: {quality['clean_rows']:,}; raw full duplicate rows removed: {quality['raw_full_duplicate_rows']}")


if __name__ == "__main__":
    main()
