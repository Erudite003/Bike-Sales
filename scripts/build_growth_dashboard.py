import base64
import os

charts_dir = '/home/user/global-bike-growth-analysis/charts'
chart_files = [
    ('01_annual_yoy_revenue_and_profit_trajectory.png', '11-Year Annual YoY Revenue & Profit Trajectory (2013–2023)', 'Annual revenue remained tightly stabilized between $7.55M (2020) and $7.97M (2016), averaging $7.75M annually (+0.0% CAGR). Gross profit followed an identical stable pattern ($2.84M to $3.03M).'),
    ('02_gross_margin_resilience_corridor.png', 'Gross Profit Margin Resilience Corridor (37.4% – 38.0%)', 'Unbroken 11-year stability: realized gross margins varied by only ±0.3% around the 37.8% benchmark across economic cycles and pandemic volatility.'),
    ('03_monthly_seasonality_bimodal_curve.png', 'Bimodal Monthly Demand Curve & Summer Slump', 'Pronounced demand peaks in June ($9.04M / 10.6%) and December ($9.10M / 10.7%) contrasted with an immediate -36.7% drop into the July–August slump ($5.71M).'),
    ('04_mom_growth_rate_volatility.png', 'Month-over-Month (MoM) Growth Rate Volatility', 'High seasonal acceleration in May (+16.3%) and December (+45.6%), counterbalanced by severe post-peak resets in January (-22.9%) and July (-36.7%).'),
    ('05_demand_cycle_phase_distribution.png', 'Operational Demand Cycle Phase Mix', 'Super Peak months drive 31.6% ($26.98M) of sales, while the Summer Slump accounts for 13.4% ($11.43M), requiring tailored inventory and marketing playbooks.')
]

chart_b64 = {}
for fname, title, desc in chart_files:
    fpath = os.path.join(charts_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            chart_b64[fname] = {'b64': b64, 'title': title, 'desc': desc}

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Bike Sales | Multi-Year Growth & Seasonality Analytics (2013–2023)</title>
    <style>
        :root {{
            --bg: #0B132B;
            --surface: #1C2541;
            --surface-card: #222F55;
            --border: #3A506B;
            --text: #F8FAFC;
            --text-muted: #94A3B8;
            --primary: #3B82F6;
            --primary-light: #60A5FA;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
            --accent: #8B5CF6;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background: var(--bg); color: var(--text); padding: 24px; line-height: 1.5; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{ margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; border-bottom: 1px solid var(--border); padding-bottom: 20px; }}
        .title h1 {{ font-size: 26px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px; }}
        .title p {{ font-size: 14px; color: var(--text-muted); margin-top: 4px; }}
        .badge {{ background: rgba(59, 130, 246, 0.2); color: var(--primary-light); border: 1px solid var(--primary); padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block; }}
        
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; position: relative; overflow: hidden; }}
        .kpi-card::before {{ content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--primary); }}
        .kpi-card.green::before {{ background: var(--success); }}
        .kpi-card.purple::before {{ background: var(--accent); }}
        .kpi-card.amber::before {{ background: var(--warning); }}
        .kpi-card.red::before {{ background: var(--danger); }}
        .kpi-label {{ font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--text-muted); letter-spacing: 0.5px; }}
        .kpi-val {{ font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 6px 0; }}
        .kpi-sub {{ font-size: 12px; color: var(--text-muted); }}

        .nav-tabs {{ display: flex; gap: 8px; border-bottom: 1px solid var(--border); margin-bottom: 24px; overflow-x: auto; padding-bottom: 4px; }}
        .tab-btn {{ background: transparent; border: none; color: var(--text-muted); padding: 10px 18px; font-size: 14px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.05); color: #FFF; }}
        .tab-btn.active {{ background: var(--primary); color: #FFF; }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        .panel {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 24px; }}
        .panel-header {{ font-size: 17px; font-weight: 700; color: #FFFFFF; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }}
        
        .chart-container {{ text-align: center; margin-bottom: 30px; }}
        .chart-img {{ width: 100%; max-height: 480px; object-fit: contain; border-radius: 8px; border: 1px solid var(--border); }}
        .chart-desc {{ font-size: 13px; color: var(--text-muted); margin-top: 8px; text-align: left; }}

        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{ background: rgba(11, 19, 43, 0.9); color: var(--text-muted); font-weight: 700; text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--border); text-transform: uppercase; font-size: 11px; }}
        td {{ padding: 12px 14px; border-bottom: 1px solid rgba(58, 80, 107, 0.4); color: var(--text); }}
        tr:hover td {{ background: rgba(255, 255, 255, 0.03); }}
        .tag {{ padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; display: inline-block; }}
        .tag-pos {{ background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid var(--success); }}
        .tag-neg {{ background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid var(--danger); }}
        .tag-neutral {{ background: rgba(148, 163, 184, 0.2); color: #CBD5E1; border: 1px solid var(--border); }}

        .phase-badge {{ padding: 4px 10px; border-radius: 6px; font-size: 11.5px; font-weight: 700; display: inline-block; }}
        .phase-peak {{ background: rgba(16, 185, 129, 0.2); color: #A7F3D0; border: 1px solid var(--success); }}
        .phase-slump {{ background: rgba(239, 68, 68, 0.25); color: #FECACA; border: 1px solid var(--danger); }}
        .phase-ramp {{ background: rgba(59, 130, 246, 0.2); color: #BFDBFE; border: 1px solid var(--primary); }}
        .phase-build {{ background: rgba(245, 158, 11, 0.2); color: #FDE68A; border: 1px solid var(--warning); }}
        .phase-reset {{ background: rgba(139, 92, 246, 0.2); color: #DDD6FE; border: 1px solid var(--accent); }}

        .calc-box {{ background: var(--surface-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }}
        .calc-row {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; }}
        .calc-field {{ flex: 1; min-width: 220px; }}
        .calc-field label {{ font-size: 12px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 6px; }}
        .calc-field input, .calc-field select {{ width: 100%; background: #0B132B; border: 1px solid var(--border); color: #FFF; padding: 10px 12px; border-radius: 6px; font-size: 14px; outline: none; }}
        .calc-result {{ background: #0B132B; border: 1px solid var(--border); border-radius: 8px; padding: 18px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 16px; }}
    </style>
</head>
<body>

<div class="container">
    <header>
        <div class="title">
            <h1>GLOBAL BIKE SALES (2013–2023)</h1>
            <p>Comprehensive Multi-Year YoY Growth Trajectory, Cyclical Patterns & Monthly Seasonality Analytics</p>
        </div>
        <div>
            <span class="badge">11-Year Growth Diagnostic Suite</span>
        </div>
    </header>

    <!-- KPI Grid -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Cumulative 11-Yr Revenue</div>
            <div class="kpi-val">$85,298,198</div>
            <div class="kpi-sub">$7.75M Annual Average (+0.0% CAGR)</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Cumulative Gross Profit</div>
            <div class="kpi-val">$32,229,951</div>
            <div class="kpi-sub">37.8% Blended Gross Margin</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">Margin Stability Corridor</div>
            <div class="kpi-val">37.4% – 38.0%</div>
            <div class="kpi-sub">±0.3% Maximum Variance Across 11 Yrs</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Peak Performance Year</div>
            <div class="kpi-val">$7.97M (2016)</div>
            <div class="kpi-sub">$3.03M Gross Profit (38.0% Margin)</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Summer Slump Impact</div>
            <div class="kpi-val">-36.7%</div>
            <div class="kpi-sub">July Drop from June ($9.04M $\rightarrow$ $5.72M)</div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('tab-charts')">📊 Analytical Visualizations</button>
        <button class="tab-btn" onclick="switchTab('tab-yoy')">📅 Annual YoY Trajectory</button>
        <button class="tab-btn" onclick="switchTab('tab-season')">🌊 Monthly Seasonality & Cycles</button>
        <button class="tab-btn" onclick="switchTab('tab-insights')">💡 Strategic Findings & Playbook</button>
        <button class="tab-btn" onclick="switchTab('tab-simulator')">🎛️ Seasonal Margin Simulator</button>
    </div>

    <!-- TAB 1: Visual Charts Deck -->
    <div id="tab-charts" class="tab-content active">
        <div class="panel">
            <div class="panel-header">Publication-Grade Growth & Seasonality Visual Deck (300 DPI)</div>
'''

for fname, title, desc in chart_files:
    if fname in chart_b64:
        item = chart_b64[fname]
        html_content += f'''
            <div class="chart-container">
                <h3 style="color: #FFF; font-size: 16px; text-align: left; margin-bottom: 8px;">{item['title']}</h3>
                <img src="data:image/png;base64,{item['b64']}" class="chart-img" alt="{item['title']}">
                <p class="chart-desc">{item['desc']}</p>
            </div>
        '''

html_content += '''
        </div>
    </div>

    <!-- TAB 2: Annual YoY Trajectory -->
    <div id="tab-yoy" class="tab-content">
        <div class="panel">
            <div class="panel-header">Annual Year-over-Year (YoY) Financial Performance Ledger (2013–2023)</div>
            <table>
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Revenue ($)</th>
                        <th>Prior Year Rev ($)</th>
                        <th>YoY Rev Delta ($)</th>
                        <th>YoY Rev Growth (%)</th>
                        <th>Gross Profit ($)</th>
                        <th>Prior Year GP ($)</th>
                        <th>YoY GP Delta ($)</th>
                        <th>YoY GP Growth (%)</th>
                        <th>Gross Margin %</th>
                        <th>Performance Context</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>2013</strong></td>
                        <td>$7,782,163</td>
                        <td>-</td>
                        <td>-</td>
                        <td><span class="tag tag-neutral">Baseline</span></td>
                        <td>$2,933,932</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                        <td><strong>37.7%</strong></td>
                        <td>Baseline Benchmark Year</td>
                    </tr>
                    <tr>
                        <td><strong>2014</strong></td>
                        <td>$7,753,872</td>
                        <td>$7,782,163</td>
                        <td>-$28,291</td>
                        <td><span class="tag tag-neg">-0.4%</span></td>
                        <td>$2,929,264</td>
                        <td>$2,933,932</td>
                        <td>-$4,668</td>
                        <td>-0.2%</td>
                        <td><strong>37.8%</strong></td>
                        <td>Stable (-0.36%)</td>
                    </tr>
                    <tr>
                        <td><strong>2015</strong></td>
                        <td>$7,853,503</td>
                        <td>$7,753,872</td>
                        <td>+$99,631</td>
                        <td><span class="tag tag-pos">+1.3%</span></td>
                        <td>$2,963,825</td>
                        <td>$2,929,264</td>
                        <td>+$34,561</td>
                        <td>+1.2%</td>
                        <td><strong>37.7%</strong></td>
                        <td>Growth Expansion (+1.29%)</td>
                    </tr>
                    <tr style="background: rgba(59, 130, 246, 0.08);">
                        <td><strong>2016</strong></td>
                        <td>$7,971,310</td>
                        <td>$7,853,503</td>
                        <td>+$117,807</td>
                        <td><span class="tag tag-pos">+1.5%</span></td>
                        <td>$3,026,307</td>
                        <td>$2,963,825</td>
                        <td>+$62,482</td>
                        <td>+2.1%</td>
                        <td><strong style="color:var(--success);">38.0%</strong></td>
                        <td>🏆 11-Year Peak Revenue & Profit</td>
                    </tr>
                    <tr>
                        <td><strong>2017</strong></td>
                        <td>$7,862,502</td>
                        <td>$7,971,310</td>
                        <td>-$108,808</td>
                        <td><span class="tag tag-neg">-1.4%</span></td>
                        <td>$2,963,335</td>
                        <td>$3,026,307</td>
                        <td>-$62,972</td>
                        <td>-2.1%</td>
                        <td><strong>37.7%</strong></td>
                        <td>Slight Pullback (-1.36%)</td>
                    </tr>
                    <tr>
                        <td><strong>2018</strong></td>
                        <td>$7,595,956</td>
                        <td>$7,862,502</td>
                        <td>-$266,546</td>
                        <td><span class="tag tag-neg">-3.4%</span></td>
                        <td>$2,867,297</td>
                        <td>$2,963,335</td>
                        <td>-$96,038</td>
                        <td>-3.2%</td>
                        <td><strong>37.7%</strong></td>
                        <td>Contraction (-3.39%)</td>
                    </tr>
                    <tr>
                        <td><strong>2019</strong></td>
                        <td>$7,865,723</td>
                        <td>$7,595,956</td>
                        <td>+$269,767</td>
                        <td><span class="tag tag-pos">+3.6%</span></td>
                        <td>$2,980,984</td>
                        <td>$2,867,297</td>
                        <td>+$113,687</td>
                        <td>+4.0%</td>
                        <td><strong>37.9%</strong></td>
                        <td>Rebound Surge (+3.55%)</td>
                    </tr>
                    <tr style="background: rgba(239, 68, 68, 0.08);">
                        <td><strong>2020</strong></td>
                        <td>$7,550,455</td>
                        <td>$7,865,723</td>
                        <td>-$315,268</td>
                        <td><span class="tag tag-neg">-4.0%</span></td>
                        <td>$2,870,185</td>
                        <td>$2,980,984</td>
                        <td>-$110,799</td>
                        <td>-3.7%</td>
                        <td><strong style="color:var(--success);">38.0%</strong></td>
                        <td>⚠️ Trough Year (-4.01% Pandemic Trough)</td>
                    </tr>
                    <tr>
                        <td><strong>2021</strong></td>
                        <td>$7,671,898</td>
                        <td>$7,550,455</td>
                        <td>+$121,443</td>
                        <td><span class="tag tag-pos">+1.6%</span></td>
                        <td>$2,895,217</td>
                        <td>$2,870,185</td>
                        <td>+$25,032</td>
                        <td>+0.9%</td>
                        <td><strong>37.7%</strong></td>
                        <td>Recovery (+1.61%)</td>
                    </tr>
                    <tr>
                        <td><strong>2022</strong></td>
                        <td>$7,592,783</td>
                        <td>$7,671,898</td>
                        <td>-$79,115</td>
                        <td><span class="tag tag-neg">-1.0%</span></td>
                        <td>$2,839,784</td>
                        <td>$2,895,217</td>
                        <td>-$55,433</td>
                        <td>-1.9%</td>
                        <td><strong>37.4%</strong></td>
                        <td>Slight Pullback (-1.03%)</td>
                    </tr>
                    <tr style="background: rgba(16, 185, 129, 0.08);">
                        <td><strong>2023</strong></td>
                        <td>$7,798,033</td>
                        <td>$7,592,783</td>
                        <td>+$205,250</td>
                        <td><span class="tag tag-pos">+2.7%</span></td>
                        <td>$2,959,821</td>
                        <td>$2,839,784</td>
                        <td>+$120,037</td>
                        <td>+4.2%</td>
                        <td><strong style="color:var(--success);">38.0%</strong></td>
                        <td>Strong Expansion (+2.70%)</td>
                    </tr>
                    <tr style="font-weight: 800; background: rgba(59, 130, 246, 0.15);">
                        <td>Total / Avg</td>
                        <td>$85,298,198</td>
                        <td>-</td>
                        <td>+$15,870</td>
                        <td>+0.0%</td>
                        <td>$32,229,951</td>
                        <td>-</td>
                        <td>+$25,889</td>
                        <td>+0.1%</td>
                        <td>37.8%</td>
                        <td>11-Year Cumulative Baseline</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 3: Monthly Seasonality -->
    <div id="tab-season" class="tab-content">
        <div class="panel">
            <div class="panel-header">12-Month Seasonality, MoM Deltas & Demand Cycle Phases</div>
            <table>
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Aggregate Revenue ($)</th>
                        <th>% Total Sales</th>
                        <th>MoM Delta ($)</th>
                        <th>MoM Growth (%)</th>
                        <th>Demand Cycle Phase</th>
                        <th>Operational & Commercial Playbook</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>January</strong></td>
                        <td>$7,009,758</td>
                        <td>8.2%</td>
                        <td>-$2,087,312</td>
                        <td><span class="tag tag-neg">-22.9%</span></td>
                        <td><span class="phase-badge phase-reset">Post-Holiday Reset</span></td>
                        <td>Moderate baseline demand following year-end peak; cycle warehouse maintenance.</td>
                    </tr>
                    <tr>
                        <td><strong>February</strong></td>
                        <td>$6,834,583</td>
                        <td>8.0%</td>
                        <td>-$175,175</td>
                        <td><span class="tag tag-neg">-2.5%</span></td>
                        <td><span class="phase-badge phase-reset">Late Winter Trough</span></td>
                        <td>Annual trough month; prime window for early season inventory procurement.</td>
                    </tr>
                    <tr>
                        <td><strong>March</strong></td>
                        <td>$7,351,357</td>
                        <td>8.6%</td>
                        <td>+$516,774</td>
                        <td><span class="tag tag-pos">+7.6%</span></td>
                        <td><span class="phase-badge phase-ramp">Spring Ramp-Up</span></td>
                        <td>Outdoor cycling interest accelerates across North America & Europe.</td>
                    </tr>
                    <tr>
                        <td><strong>April</strong></td>
                        <td>$7,602,764</td>
                        <td>8.9%</td>
                        <td>+$251,407</td>
                        <td><span class="tag tag-pos">+3.4%</span></td>
                        <td><span class="phase-badge phase-ramp">Spring Momentum</span></td>
                        <td>Broad-based expansion across all bike categories and apparel.</td>
                    </tr>
                    <tr>
                        <td><strong>May</strong></td>
                        <td>$8,840,209</td>
                        <td>10.4%</td>
                        <td>+$1,237,445</td>
                        <td><span class="tag tag-pos">+16.3%</span></td>
                        <td><span class="phase-badge phase-peak">Early Summer Surge</span></td>
                        <td>Pre-summer accessories and apparel purchasing acceleration.</td>
                    </tr>
                    <tr style="background: rgba(16, 185, 129, 0.08);">
                        <td><strong>June</strong></td>
                        <td>$9,044,483</td>
                        <td>10.6%</td>
                        <td>+$204,274</td>
                        <td><span class="tag tag-pos">+2.3%</span></td>
                        <td><span class="phase-badge phase-peak">Mid-Year Apex ($9.04M)</span></td>
                        <td>First major annual sales apex; peak summer riding season demand.</td>
                    </tr>
                    <tr style="background: rgba(239, 68, 68, 0.08);">
                        <td><strong>July</strong></td>
                        <td>$5,722,784</td>
                        <td>6.7%</td>
                        <td>-$3,321,699</td>
                        <td><span class="tag tag-neg">-36.7%</span></td>
                        <td><span class="phase-badge phase-slump">Summer Lull (Sharp Drop)</span></td>
                        <td>Sudden -36.7% drop due to mid-summer European vacations and heatwaves.</td>
                    </tr>
                    <tr style="background: rgba(239, 68, 68, 0.08);">
                        <td><strong>August</strong></td>
                        <td>$5,711,193</td>
                        <td>6.7%</td>
                        <td>-$11,591</td>
                        <td><span class="tag tag-neg">-0.2%</span></td>
                        <td><span class="phase-badge phase-slump">Summer Slump ($5.71M)</span></td>
                        <td>Lowest revenue month of the operational calendar; test clearance discounting.</td>
                    </tr>
                    <tr>
                        <td><strong>September</strong></td>
                        <td>$5,842,332</td>
                        <td>6.8%</td>
                        <td>+$131,139</td>
                        <td><span class="tag tag-pos">+2.3%</span></td>
                        <td><span class="phase-badge phase-build">Late Q3 Stabilization</span></td>
                        <td>Demand stabilizes with fall commuting and late-season clearance.</td>
                    </tr>
                    <tr>
                        <td><strong>October</strong></td>
                        <td>$5,995,681</td>
                        <td>7.0%</td>
                        <td>+$153,349</td>
                        <td><span class="tag tag-pos">+2.6%</span></td>
                        <td><span class="phase-badge phase-build">Early Q4 Build</span></td>
                        <td>Pre-holiday stocking and initial promotional campaigns launch.</td>
                    </tr>
                    <tr>
                        <td><strong>November</strong></td>
                        <td>$6,245,984</td>
                        <td>7.3%</td>
                        <td>+$250,303</td>
                        <td><span class="tag tag-pos">+4.2%</span></td>
                        <td><span class="phase-badge phase-build">Holiday Inflow</span></td>
                        <td>Black Friday / Cyber Week shopping initiates peak demand window.</td>
                    </tr>
                    <tr style="background: rgba(245, 158, 11, 0.08);">
                        <td><strong>December</strong></td>
                        <td>$9,097,070</td>
                        <td>10.7%</td>
                        <td>+$2,851,086</td>
                        <td><span class="tag tag-pos">+45.6%</span></td>
                        <td><span class="phase-badge phase-peak">Annual Super Peak ($9.10M)</span></td>
                        <td>Highest grossing month driven by holiday gift orders and bike purchases.</td>
                    </tr>
                    <tr style="font-weight: 800; background: rgba(59, 130, 246, 0.15);">
                        <td>Total / Year</td>
                        <td>$85,298,198</td>
                        <td>100.0%</td>
                        <td>-</td>
                        <td>-</td>
                        <td>Full 12-Month Total</td>
                        <td>Aggregated 11-year operational demand volume.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 4: Strategic Findings -->
    <div id="tab-insights" class="tab-content">
        <div class="panel">
            <div class="panel-header">Core Strategic Findings & Executive Action Playbook</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: var(--surface-card); padding: 18px; border-radius: 8px; border: 1px solid var(--border);">
                    <h3 style="color: var(--primary-light); font-size: 15px; margin-bottom: 10px;">📈 Long-Term Growth Trajectory Findings</h3>
                    <p style="font-size: 13.5px; color: var(--text); margin-bottom: 8px;">
                        • <strong>Mature Market Equilibrium</strong>: Annual revenue has stabilized tightly between $7.55M (2020) and $7.97M (2016), demonstrating an 11-year CAGR of +0.0%.
                    </p>
                    <p style="font-size: 13.5px; color: var(--text); margin-bottom: 8px;">
                        • <strong>Exceptional Margin Resilience</strong>: Realized gross profit margins remained between 37.4% and 38.0% across all 11 operating years, illustrating price discipline and robust cost-pass-through mechanics.
                    </p>
                    <p style="font-size: 13.5px; color: var(--text);">
                        • <strong>Post-Pandemic Expansion</strong>: Following the 2020 contraction (-4.01%), revenue rebounded strongly to $7.80M by 2023 (+2.70% YoY), with gross profit reaching $2.96M (+4.23% YoY).
                    </p>
                </div>

                <div style="background: var(--surface-card); padding: 18px; border-radius: 8px; border: 1px solid var(--border);">
                    <h3 style="color: var(--warning); font-size: 15px; margin-bottom: 10px;">🌊 Seasonality & Cyclical Playbook</h3>
                    <p style="font-size: 13.5px; color: var(--text); margin-bottom: 8px;">
                        • <strong>Bifurcated Apexes</strong>: Demand concentrates around two distinct apexes: June ($9.04M / 10.6%) and December ($9.10M / 10.7%).
                    </p>
                    <p style="font-size: 13.5px; color: var(--text); margin-bottom: 8px;">
                        • <strong>Summer Slump Vulnerability</strong>: The -36.7% plunge from June ($9.04M) to July ($5.72M) and August ($5.71M) represents the single largest working capital risk in the business.
                    </p>
                    <p style="font-size: 13.5px; color: var(--text);">
                        • <strong>Targeted Playbook</strong>: Protect margins in May–June and Nov–Dec; deploy off-peak seasonal campaigns and accessory bundles during July–August to smooth demand volatility.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 5: Seasonal Simulator -->
    <div id="tab-simulator" class="tab-content">
        <div class="panel">
            <div class="panel-header">Interactive Seasonal Campaign & Slump Smoothing Simulator</div>
            <div class="calc-box">
                <div class="calc-row">
                    <div class="calc-field">
                        <label>Target Season / Phase</label>
                        <select id="sim-season" onchange="runSeasonSim()">
                            <option value="summer">Summer Slump (Jul–Aug: $11.43M combined)</option>
                            <option value="spring">Spring Ramp-Up (Mar–Apr: $14.95M combined)</option>
                            <option value="fall">Fall Build (Sep–Nov: $18.08M combined)</option>
                            <option value="peak">Super Peaks (May, Jun, Dec: $26.98M combined)</option>
                            <option value="full">Full 12-Month Year ($85.30M)</option>
                        </select>
                    </div>
                    <div class="calc-field">
                        <label>Promotional Price Adjustment (%): <span id="sim-p-val">0%</span></label>
                        <input type="range" id="sim-p" min="-15" max="15" value="0" step="1" oninput="runSeasonSim()">
                    </div>
                    <div class="calc-field">
                        <label>Projected Volume Demand Lift (%): <span id="sim-v-val">0%</span></label>
                        <input type="range" id="sim-v" min="-20" max="40" value="0" step="2" oninput="runSeasonSim()">
                    </div>
                </div>

                <div class="calc-result">
                    <div>
                        <div class="kpi-label">Projected Seasonal Revenue</div>
                        <div id="sres-rev" style="font-size: 22px; font-weight: 800; color: #FFF; margin-top: 4px;">$11,433,977</div>
                        <div id="sres-rev-diff" class="kpi-sub" style="color: var(--text-muted);">Baseline: $11.43M</div>
                    </div>
                    <div>
                        <div class="kpi-label">Projected Gross Profit</div>
                        <div id="sres-profit" style="font-size: 22px; font-weight: 800; color: var(--success); margin-top: 4px;">$4,322,043</div>
                        <div id="sres-profit-diff" class="kpi-sub" style="color: var(--text-muted);">Baseline: $4.32M</div>
                    </div>
                    <div>
                        <div class="kpi-label">Projected Realized Margin</div>
                        <div id="sres-margin" style="font-size: 22px; font-weight: 800; color: var(--primary-light); margin-top: 4px;">37.8%</div>
                        <div class="kpi-sub">Baseline: 37.8%</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    function switchTab(tabId) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        event.target.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    }

    const seasonData = {
        summer: { rev: 11433977, cost: 7111934, profit: 4322043 },
        spring: { rev: 14954121, cost: 9301463, profit: 5652658 },
        fall: { rev: 18083997, cost: 11248246, profit: 6835751 },
        peak: { rev: 26981762, cost: 16782656, profit: 10199106 },
        full: { rev: 85298198, cost: 53068247, profit: 32229951 }
    };

    function runSeasonSim() {
        const s = document.getElementById('sim-season').value;
        const p = parseFloat(document.getElementById('sim-p').value) / 100;
        const v = parseFloat(document.getElementById('sim-v').value) / 100;

        document.getElementById('sim-p-val').innerText = (p > 0 ? '+' : '') + (p * 100).toFixed(0) + '%';
        document.getElementById('sim-v-val').innerText = (v > 0 ? '+' : '') + (v * 100).toFixed(0) + '%';

        const base = seasonData[s];
        const newRev = base.rev * (1 + p) * (1 + v);
        const newCost = base.cost * (1 + v);
        const newProfit = newRev - newCost;
        const newMargin = (newProfit / newRev) * 100;

        const revDiff = newRev - base.rev;
        const profitDiff = newProfit - base.profit;

        document.getElementById('sres-rev').innerText = '$' + newRev.toLocaleString('en-US', {maximumFractionDigits: 0});
        document.getElementById('sres-rev-diff').innerHTML = (revDiff >= 0 ? '<span style="color:var(--success)">+$' : '<span style="color:var(--danger)">-$') + Math.abs(revDiff).toLocaleString('en-US', {maximumFractionDigits: 0}) + ' vs baseline</span>';

        document.getElementById('sres-profit').innerText = '$' + newProfit.toLocaleString('en-US', {maximumFractionDigits: 0});
        document.getElementById('sres-profit-diff').innerHTML = (profitDiff >= 0 ? '<span style="color:var(--success)">+$' : '<span style="color:var(--danger)">-$') + Math.abs(profitDiff).toLocaleString('en-US', {maximumFractionDigits: 0}) + ' vs baseline</span>';

        document.getElementById('sres-margin').innerText = newMargin.toFixed(1) + '%';
    }
</script>
</body>
</html>
'''

with open('/home/user/global-bike-growth-analysis/index.html', 'w') as f:
    f.write(html_content)

with open('/home/user/global-bike-growth-analysis/dashboard.html', 'w') as f:
    f.write(html_content)

print('Growth & Seasonality Dashboard created: /home/user/global-bike-growth-analysis/index.html')
