import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('/home/user/global-bike-growth-analysis/charts', exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = False

# Brand palette
C_NAVY = '#0F172A'
C_BLUE = '#2563EB'
C_LIGHT_BLUE = '#60A5FA'
C_TEAL = '#0D9488'
C_GREEN = '#10B981'
C_AMBER = '#D97706'
C_RED = '#DC2626'
C_GRAY = '#64748B'
C_LIGHT_GRAY = '#E2E8F0'
C_BG = '#F8FAFC'
C_CARD = '#FFFFFF'

# -------------------------------------------------------------
# Chart 1: Annual YoY Revenue & Gross Profit Trajectory (2013–2023)
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(14, 7), facecolor=C_BG)
ax1.set_facecolor(C_BG)

years = np.arange(2013, 2024)
revenue = [7.782, 7.754, 7.854, 7.971, 7.863, 7.596, 7.866, 7.550, 7.672, 7.593, 7.798]
profit =  [2.934, 2.929, 2.964, 3.026, 2.963, 2.867, 2.981, 2.870, 2.895, 2.840, 2.960]

x = np.arange(len(years))
width = 0.38

r1 = ax1.bar(x - width/2, revenue, width, label='Revenue ($M)', color=C_BLUE, zorder=3)
r2 = ax1.bar(x + width/2, profit, width, label='Gross Profit ($M)', color=C_TEAL, zorder=3)

ax1.set_title('11-Year Annual Financial Trajectory: Revenue & Gross Profit (2013–2023)', fontsize=15, fontweight='bold', color=C_NAVY, pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=11, fontweight='bold', color=C_NAVY)
ax1.set_ylabel('$ Millions (USD)', fontsize=12, color=C_GRAY)
ax1.set_ylim(0, 9.5)
ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

# Value annotations
for rect in r1:
    h = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., h + 0.15, f'${h:.2f}M', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_BLUE)

for rect in r2:
    h = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., h + 0.15, f'${h:.2f}M', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_TEAL)

# Peak and Trough highlights
ax1.annotate('Peak Year (2016)\n$7.97M Rev / $3.03M GP', xy=(3 - width/2, 7.971), xytext=(3, 9.0),
             arrowprops=dict(arrowstyle='->', color=C_BLUE, lw=1.5),
             ha='center', fontsize=9.5, fontweight='bold', color=C_BLUE,
             bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=C_BLUE, lw=1))

ax1.annotate('Trough Year (2020)\n$7.55M Rev (-4.0% YoY)', xy=(7 - width/2, 7.550), xytext=(7, 8.8),
             arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.5),
             ha='center', fontsize=9.5, fontweight='bold', color=C_RED,
             bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec=C_RED, lw=1))

ax1.legend(loc='upper right', frameon=True, facecolor=C_CARD, edgecolor=C_LIGHT_GRAY, fontsize=11)
plt.tight_layout(pad=3.0)
plt.savefig('/home/user/global-bike-growth-analysis/charts/01_annual_yoy_revenue_and_profit_trajectory.png', dpi=300, facecolor=C_BG)
plt.close()

# -------------------------------------------------------------
# Chart 2: Gross Profit Margin Stability Corridor (37.4% – 38.0%)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6), facecolor=C_BG)
ax.set_facecolor(C_BG)

margins = [37.7, 37.8, 37.7, 38.0, 37.7, 37.7, 37.9, 38.0, 37.7, 37.4, 38.0]

ax.plot(years, margins, marker='o', color=C_TEAL, linewidth=3, markersize=8, zorder=4, label='Realized Gross Margin %')
ax.axhline(37.8, color=C_BLUE, linestyle='--', linewidth=1.8, label='11-Year Benchmark (37.8%)', zorder=3)
ax.axhspan(37.4, 38.0, color=C_TEAL, alpha=0.12, label='Stability Corridor (37.4% - 38.0%)', zorder=1)

ax.set_title('Exceptional Margin Resilience: 11-Year Gross Margin Stability Corridor', fontsize=15, fontweight='bold', color=C_NAVY, pad=20)
ax.set_xticks(years)
ax.set_xticklabels(years, fontsize=11, fontweight='bold', color=C_NAVY)
ax.set_ylabel('Gross Profit Margin (%)', fontsize=12, color=C_GRAY)
ax.set_ylim(36.0, 39.0)
ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

for i, m in enumerate(margins):
    ax.text(years[i], m + 0.12, f'{m:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold', color=C_NAVY)

ax.legend(loc='lower left', frameon=True, facecolor=C_CARD, edgecolor=C_LIGHT_GRAY, fontsize=10.5)
plt.tight_layout(pad=3.0)
plt.savefig('/home/user/global-bike-growth-analysis/charts/02_gross_margin_resilience_corridor.png', dpi=300, facecolor=C_BG)
plt.close()

# -------------------------------------------------------------
# Chart 3: Monthly Seasonality & Bimodal Demand Curve
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_rev = [7.010, 6.835, 7.351, 7.603, 8.840, 9.044, 5.723, 5.711, 5.842, 5.996, 6.246, 9.097]

ax.plot(months, monthly_rev, marker='s', color=C_BLUE, linewidth=3.5, markersize=9, zorder=4, label='Monthly Aggregate Revenue ($M)')
ax.fill_between(months, monthly_rev, color=C_BLUE, alpha=0.15, zorder=2)

# Highlight zones
ax.axvspan(4.5, 5.5, color=C_GREEN, alpha=0.15, label='Mid-Year Apex (June $9.04M / 10.6%)', zorder=1)
ax.axvspan(5.5, 7.5, color=C_RED, alpha=0.18, label='Summer Slump (Jul–Aug $5.71M, -36.7% drop)', zorder=1)
ax.axvspan(10.5, 11.5, color=C_AMBER, alpha=0.2, label='Holiday Super Peak (Dec $9.10M / 10.7%)', zorder=1)

ax.set_title('Bimodal Seasonality Curve: June & December Super-Peaks vs. July–August Summer Slump', fontsize=15, fontweight='bold', color=C_NAVY, pad=20)
ax.set_ylabel('Total Revenue ($ Millions USD)', fontsize=12, color=C_GRAY)
ax.set_ylim(4.5, 10.5)
ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

for i, val in enumerate(monthly_rev):
    color = C_RED if i in [6, 7] else (C_GREEN if i == 5 else (C_AMBER if i == 11 else C_NAVY))
    offset = 12 if i not in [6, 7] else -20
    ax.annotate(f'${val:.2f}M', (months[i], val), textcoords="offset points", xytext=(0, offset),
                ha='center', fontsize=10, fontweight='bold', color=color)

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=True, facecolor=C_CARD, edgecolor=C_LIGHT_GRAY, fontsize=10)
plt.tight_layout(pad=3.0)
plt.savefig('/home/user/global-bike-growth-analysis/charts/03_monthly_seasonality_bimodal_curve.png', dpi=300, facecolor=C_BG)
plt.close()

# -------------------------------------------------------------
# Chart 4: Month-over-Month (MoM) Growth & Delta Waterfall
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6.5), facecolor=C_BG)
ax.set_facecolor(C_BG)

mom_growth = [-22.9, -2.5, 7.6, 3.4, 16.3, 2.3, -36.7, -0.2, 2.3, 2.6, 4.2, 45.6]
colors = [C_GREEN if g > 0 else C_RED for g in mom_growth]

bars = ax.bar(months, mom_growth, color=colors, width=0.55, zorder=3)
ax.axhline(0, color=C_NAVY, linewidth=1.2, zorder=4)

ax.set_title('Month-over-Month (MoM) Growth % Volatility: The July Crash (-36.7%) vs. Dec Surge (+45.6%)', fontsize=14, fontweight='bold', color=C_NAVY, pad=20)
ax.set_ylabel('MoM Growth Rate (%)', fontsize=12, color=C_GRAY)
ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

for bar in bars:
    h = bar.get_height()
    va = 'bottom' if h >= 0 else 'top'
    y_pos = h + 1.2 if h >= 0 else h - 2.5
    ax.text(bar.get_x() + bar.get_width()/2., y_pos, f'{h:+.1f}%', ha='center', va=va, fontsize=9.5, fontweight='bold', color=C_NAVY)

plt.tight_layout(pad=3.0)
plt.savefig('/home/user/global-bike-growth-analysis/charts/04_mom_growth_rate_volatility.png', dpi=300, facecolor=C_BG)
plt.close()

# -------------------------------------------------------------
# Chart 5: Demand Cycle Phases & Operational Revenue Mix
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

phases = [
    'Mid-Year & Holiday Super Peaks\n(May, Jun, Dec - $26.98M)',
    'Spring Ramp-Up & Momentum\n(Mar, Apr - $14.95M)',
    'Post-Holiday & Winter Reset\n(Jan, Feb - $13.84M)',
    'Fall Inflow & Q4 Build\n(Sep, Oct, Nov - $18.08M)',
    'Summer Slump Trough\n(Jul, Aug - $11.43M)'
]
phase_shares = [31.63, 17.53, 16.23, 21.20, 13.41]
phase_colors = [C_GREEN, C_BLUE, C_GRAY, C_AMBER, C_RED]

wedges, texts, autotexts = ax.pie(
    phase_shares,
    labels=phases,
    autopct='%1.1f%%',
    startangle=140,
    colors=phase_colors,
    wedgeprops=dict(width=0.45, edgecolor=C_CARD, linewidth=2),
    pctdistance=0.75
)

for t in texts:
    t.set_fontsize(10.5)
    t.set_color(C_NAVY)
    t.set_fontweight('bold')

for at in autotexts:
    at.set_fontsize(11)
    at.set_color('#FFFFFF')
    at.set_fontweight('bold')

ax.set_title('Operational Demand Phase Distribution (% of 11-Year Total Sales)', fontsize=15, fontweight='bold', color=C_NAVY, pad=20)
plt.tight_layout(pad=3.0)
plt.savefig('/home/user/global-bike-growth-analysis/charts/05_demand_cycle_phase_distribution.png', dpi=300, facecolor=C_BG)
plt.close()

print('All 5 Growth & Seasonality charts successfully generated in /home/user/global-bike-growth-analysis/charts/')
