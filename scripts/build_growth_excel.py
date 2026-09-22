import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, DoughnutChart, Reference, Series
from openpyxl.drawing.image import Image
import os

wb = openpyxl.Workbook()
wb.remove(wb.active)

# Styles
navy_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
blue_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
card_fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
alert_fill = PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid")

header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
title_font = Font(name="Calibri", size=16, bold=True, color="0F172A")
subtitle_font = Font(name="Calibri", size=11, italic=True, color="64748B")
card_title_font = Font(name="Calibri", size=9, bold=True, color="2563EB")
card_num_font = Font(name="Calibri", size=18, bold=True, color="0F172A")
bold_font = Font(name="Calibri", size=11, bold=True, color="0F172A")
regular_font = Font(name="Calibri", size=11, color="0F172A")

thin_border = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1")
)
double_bottom_border = Border(
    top=Side(style="thin", color="94A3B8"),
    bottom=Side(style="double", color="0F172A")
)

# -------------------------------------------------------------
# Sheet 1: YoY Annual Financial Trajectory
# -------------------------------------------------------------
ws1 = wb.create_sheet("Annual YoY Trajectory")
ws1.views.sheetView[0].showGridLines = True

ws1["A1"] = "GLOBAL BIKE SALES - ANNUAL YEAR-OVER-YEAR (YoY) FINANCIAL TRAJECTORY (2013–2023)"
ws1["A1"].font = title_font
ws1["A2"] = "Multi-year revenue, gross profit, margin resilience, and growth rate analysis"
ws1["A2"].font = subtitle_font

# Summary Cards
kpis = [
    ("11-YEAR REVENUE", "$85,298,198", "Annual Avg: $7.75M (+0.0% CAGR)"),
    ("11-YEAR GROSS PROFIT", "$32,229,951", "37.8% Blended Gross Margin"),
    ("PEAK PERFORMANCE", "$7,971,310 (2016)", "Gross Profit: $3,026,307 (38.0%)"),
    ("TROUGH YEAR", "$7,550,455 (2020)", "-4.01% YoY Contraction"),
    ("MARGIN BAND", "37.4% – 38.0%", "Unbroken 11-Year Stability Corridor")
]

col_offsets = [1, 3, 5, 7, 9]
for i, (title, val, sub) in enumerate(kpis):
    col = col_offsets[i]
    ws1.cell(row=4, column=col, value=title).font = card_title_font
    ws1.cell(row=5, column=col, value=val).font = card_num_font
    ws1.cell(row=6, column=col, value=sub).font = Font(name="Calibri", size=9, italic=True, color="64748B")
    for r in range(4, 7):
        for c in range(col, col+2):
            ws1.cell(row=r, column=c).fill = card_fill
            ws1.cell(row=r, column=c).border = thin_border
    ws1.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col+1)
    ws1.merge_cells(start_row=5, start_column=col, end_row=5, end_column=col+1)
    ws1.merge_cells(start_row=6, start_column=col, end_row=6, end_column=col+1)

# Table Header
headers_yoy = [
    "Operating Year", "Revenue ($)", "Prior Year Rev ($)", "YoY Rev Delta ($)", "YoY Rev Growth (%)",
    "Gross Profit ($)", "Prior Year GP ($)", "YoY GP Delta ($)", "YoY GP Growth (%)", "Gross Margin (%)", "Context & Trajectory"
]

for col_num, h in enumerate(headers_yoy, 1):
    c = ws1.cell(row=9, column=col_num, value=h)
    c.font = header_font
    c.fill = navy_fill
    c.alignment = Alignment(horizontal="center" if col_num in [1, 5, 9, 10] else "left", vertical="center")

yoy_rows = [
    [2013, 7782163.0, None, None, None, 2933932.0, None, None, None, 0.3770, "Baseline Year"],
    [2014, 7753872.0, 7782163.0, -28291.0, -0.0036, 2929264.0, 2933932.0, -4668.0, -0.0016, 0.3778, "Stable (-0.36%)"],
    [2015, 7853503.0, 7753872.0, 99631.0, 0.0129, 2963825.0, 2929264.0, 34561.0, 0.0118, 0.3774, "Growth (+1.29%)"],
    [2016, 7971310.0, 7853503.0, 117807.0, 0.0150, 3026307.0, 2963825.0, 62482.0, 0.0211, 0.3797, "Peak Year (+1.50%)"],
    [2017, 7862502.0, 7971310.0, -108808.0, -0.0136, 2963335.0, 3026307.0, -62972.0, -0.0208, 0.3769, "Slight Pullback (-1.36%)"],
    [2018, 7595956.0, 7862502.0, -266546.0, -0.0339, 2867297.0, 2963335.0, -96038.0, -0.0324, 0.3775, "Decline (-3.39%)"],
    [2019, 7865723.0, 7595956.0, 269767.0, 0.0355, 2980984.0, 2867297.0, 113687.0, 0.0396, 0.3790, "Rebound (+3.55%)"],
    [2020, 7550455.0, 7865723.0, -315268.0, -0.0401, 2870185.0, 2980984.0, -110799.0, -0.0372, 0.3801, "Trough Year (-4.01%)"],
    [2021, 7671898.0, 7550455.0, 121443.0, 0.0161, 2895217.0, 2870185.0, 25032.0, 0.0087, 0.3774, "Recovery (+1.61%)"],
    [2022, 7592783.0, 7671898.0, -79115.0, -0.0103, 2839784.0, 2895217.0, -55433.0, -0.0191, 0.3740, "Slight Contraction (-1.03%)"],
    [2023, 7798033.0, 7592783.0, 205250.0, 0.0270, 2959821.0, 2839784.0, 120037.0, 0.0423, 0.3796, "Strong Expansion (+2.70%)"]
]

for row_idx, row_val in enumerate(yoy_rows, 10):
    fill = zebra_fill if row_idx % 2 == 0 else PatternFill(fill_type=None)
    for col_idx, val in enumerate(row_val, 1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=val)
        cell.font = regular_font
        cell.fill = fill
        cell.border = thin_border
        if col_idx in [2, 3, 4, 6, 7, 8]:
            cell.number_format = "$#,##0"
        elif col_idx in [5, 9, 10]:
            cell.number_format = "+0.0%;-0.0%;0.0%" if col_idx != 10 else "0.0%"

# Total / Average Row
tot_r = 21
ws1.cell(row=tot_r, column=1, value="Total / Avg").font = bold_font
ws1.cell(row=tot_r, column=2, value="=SUM(B10:B20)").number_format = "$#,##0"
ws1.cell(row=tot_r, column=3, value="-").alignment = Alignment(horizontal="center")
ws1.cell(row=tot_r, column=4, value="=AVERAGE(D11:D20)").number_format = "$#,##0"
ws1.cell(row=tot_r, column=5, value="=AVERAGE(E11:E20)").number_format = "+0.0%;-0.0%;0.0%"
ws1.cell(row=tot_r, column=6, value="=SUM(F10:F20)").number_format = "$#,##0"
ws1.cell(row=tot_r, column=7, value="-").alignment = Alignment(horizontal="center")
ws1.cell(row=tot_r, column=8, value="=AVERAGE(H11:H20)").number_format = "$#,##0"
ws1.cell(row=tot_r, column=9, value="=AVERAGE(I11:I20)").number_format = "+0.0%;-0.0%;0.0%"
ws1.cell(row=tot_r, column=10, value="=F21/B21").number_format = "0.0%"
ws1.cell(row=tot_r, column=11, value="11-Year Cumulative Baseline").font = bold_font

for c in range(1, 12):
    ws1.cell(row=tot_r, column=c).font = bold_font
    ws1.cell(row=tot_r, column=c).border = double_bottom_border

# Add Chart
chart1 = BarChart()
chart1.type = "col"
chart1.style = 10
chart1.title = "Annual Revenue vs. Gross Profit (2013–2023)"
chart1.y_axis.title = "USD ($)"
chart1.x_axis.title = "Operating Year"
data1 = Reference(ws1, min_col=2, min_row=9, max_row=20)
cats1 = Reference(ws1, min_col=1, min_row=10, max_row=20)
chart1.add_data(data1, titles_from_data=True)
chart1.set_categories(cats1)
chart1.width = 16
chart1.height = 7.5
ws1.add_chart(chart1, "A24")

# Embed chart image
if os.path.exists('/home/user/global-bike-growth-analysis/charts/01_annual_yoy_revenue_and_profit_trajectory.png'):
    img = Image('/home/user/global-bike-growth-analysis/charts/01_annual_yoy_revenue_and_profit_trajectory.png')
    img.width = 620
    img.height = 310
    ws1.add_image(img, "L4")

for col in ws1.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    ws1.column_dimensions[col_letter].width = max(max_len + 4, 13)

# -------------------------------------------------------------
# Sheet 2: Monthly Seasonality & Demand Cycle
# -------------------------------------------------------------
ws2 = wb.create_sheet("Monthly Seasonality")
ws2.views.sheetView[0].showGridLines = True

ws2["A1"] = "MONTHLY SEASONALITY & DEMAND CYCLE DISTRIBUTION (AGGREGATE 2013–2023)"
ws2["A1"].font = title_font
ws2["A2"] = "12-month seasonality curves, MoM velocity, demand cycle classification, and operational playbooks"
ws2["A2"].font = subtitle_font

headers_season = [
    "Month", "Aggregate Revenue ($)", "% of Total Sales", "MoM Delta ($)", "MoM Growth (%)", "Demand Cycle Phase", "Operational & Commercial Impact"
]

for col_num, h in enumerate(headers_season, 1):
    c = ws2.cell(row=5, column=col_num, value=h)
    c.font = header_font
    c.fill = navy_fill
    c.alignment = Alignment(horizontal="center" if col_num in [1, 3, 5] else "left", vertical="center")

season_rows = [
    ["January", 7009758.0, 0.0822, -2087312.0, -0.2294, "Post-Holiday Reset", "Moderate baseline demand following year-end peak."],
    ["February", 6834583.0, 0.0801, -175175.0, -0.0250, "Late Winter Trough", "Annual trough month; prime window for inventory build."],
    ["March", 7351357.0, 0.0862, 516774.0, 0.0756, "Spring Ramp-Up", "Outdoor cycling interest accelerates across NA & Europe."],
    ["April", 7602764.0, 0.0891, 251407.0, 0.0342, "Spring Momentum", "Broad-based expansion across all bike categories."],
    ["May", 8840209.0, 0.1036, 1237445.0, 0.1628, "Early Summer Surge", "Pre-summer accessories and apparel purchasing surge."],
    ["June", 9044483.0, 0.1060, 204274.0, 0.0231, "Mid-Year Peak ($9.04M)", "First major annual sales apex; peak riding season."],
    ["July", 5722784.0, 0.0671, -3321699.0, -0.3673, "Summer Lull (Sharp Drop)", "Sudden -36.7% drop due to mid-summer European vacations."],
    ["August", 5711193.0, 0.0670, -11591.0, -0.0020, "Summer Slump ($5.71M)", "Lowest revenue month of the operational calendar."],
    ["September", 5842332.0, 0.0685, 131139.0, 0.0230, "Late Q3 Stabilization", "Demand stabilizes with fall commuting and clearance."],
    ["October", 5995681.0, 0.0703, 153349.0, 0.0262, "Early Q4 Build", "Pre-holiday stocking and promotional campaigns launch."],
    ["November", 6245984.0, 0.0732, 250303.0, 0.0417, "Holiday Inflow", "Black Friday / Cyber Week shopping initiates peak."],
    ["December", 9097070.0, 0.1066, 2851086.0, 0.4565, "Annual Super Peak ($9.10M)", "Highest grossing month driven by holiday gift orders."]
]

for row_idx, row_val in enumerate(season_rows, 6):
    is_trough = row_idx in [12, 13]
    is_peak = row_idx in [11, 17]
    fill = alert_fill if is_trough else (card_fill if is_peak else (zebra_fill if row_idx % 2 == 0 else PatternFill(fill_type=None)))
    for col_idx, val in enumerate(row_val, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=val)
        cell.font = regular_font
        cell.fill = fill
        cell.border = thin_border
        if col_idx in [2, 4]:
            cell.number_format = "$#,##0"
        elif col_idx in [3, 5]:
            cell.number_format = "0.0%" if col_idx == 3 else "+0.0%;-0.0%;0.0%"

# Total Row
tot_s = 18
ws2.cell(row=tot_s, column=1, value="Total / Year").font = bold_font
ws2.cell(row=tot_s, column=2, value="=SUM(B6:B17)").number_format = "$#,##0"
ws2.cell(row=tot_s, column=3, value=1.0).number_format = "0.0%"
ws2.cell(row=tot_s, column=4, value="-").alignment = Alignment(horizontal="center")
ws2.cell(row=tot_s, column=5, value="-").alignment = Alignment(horizontal="center")
ws2.cell(row=tot_s, column=6, value="Full 12-Month Total").font = bold_font
ws2.cell(row=tot_s, column=7, value="Aggregated multi-year baseline volume").font = regular_font

for c in range(1, 8):
    ws2.cell(row=tot_s, column=c).font = bold_font
    ws2.cell(row=tot_s, column=c).border = double_bottom_border

# Add Line Chart
chart2 = LineChart()
chart2.title = "Monthly Seasonality Curve: Bimodal Demand ($M)"
chart2.y_axis.title = "USD ($)"
chart2.x_axis.title = "Month"
data2 = Reference(ws2, min_col=2, min_row=5, max_row=17)
cats2 = Reference(ws2, min_col=1, min_row=6, max_row=17)
chart2.add_data(data2, titles_from_data=True)
chart2.set_categories(cats2)
chart2.width = 16
chart2.height = 7.5
ws2.add_chart(chart2, "A21")

# Embed chart image
if os.path.exists('/home/user/global-bike-growth-analysis/charts/03_monthly_seasonality_bimodal_curve.png'):
    img2 = Image('/home/user/global-bike-growth-analysis/charts/03_monthly_seasonality_bimodal_curve.png')
    img2.width = 620
    img2.height = 290
    ws2.add_image(img2, "I5")

for col in ws2.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    ws2.column_dimensions[col_letter].width = max(max_len + 4, 14)

wb.save('/home/user/global-bike-growth-analysis/bike_sales_growth_and_seasonality_model.xlsx')
print('Growth & Seasonality Excel workbook saved: /home/user/global-bike-growth-analysis/bike_sales_growth_and_seasonality_model.xlsx')
