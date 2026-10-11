"""
QuantMaster 007 - Global Macro Pulse & Intelligence Overview
Executive quantitative dashboard displaying macroeconomic regime, live ticker pulse,
sector sentiment summary, and interactive routing into dedicated analytics pages.
"""

import streamlit as st
import pandas as pd
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import FRED_INDICATORS, MARKET_SECTORS
from modules.visualizations import create_sector_radar_chart, create_macro_risk_gauge

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Global Macroeconomic Pulse & Command Center")
render_quick_navigation(active_page="overview")
render_sidebar()

# ==========================================
# 1. LIVE MACROECONOMIC TICKER PULSE
# ==========================================
st.markdown("##### 🌐 **Global Macroeconomic Ticker Pulse**")
st.caption("Click 'Chart [Indicator]' under any card to jump straight into its historical dual-axis correlation analysis.")

key_ticker_ids = [
    ("FEDFUNDS", "Fed Funds Rate", "%"),
    ("DGS10", "10Y Treasury", "%"),
    ("T10Y2Y", "10Y-2Y Spread", "%"),
    ("CPIAUCSL", "CPI Inflation", "Index"),
    ("DCOILWTICO", "Crude Oil (WTI)", "$/bbl"),
    ("UNRATE", "Unemployment", "%")
]

ticker_cols = st.columns(6)
for i, (sid, label, unit) in enumerate(key_ticker_ids):
    item = next((m for m in macro_summary if m["id"] == sid), None)
    with ticker_cols[i]:
        if item:
            val = item["latest"]
            chg = item["change_1m"]
            pct = item["pct_1m"]
            delta_class = "qm-metric-delta-pos" if chg >= 0 else "qm-metric-delta-neg"
            arrow = "▲" if chg >= 0 else "▼"
            metric_html = f"""<div class="qm-metric-card">
<div class="qm-metric-label">{label}</div>
<div class="qm-metric-value">{val:.2f} <span style="font-size:0.85rem; color:#94A3B8;">{unit}</span></div>
<div class="{delta_class}">{arrow} {abs(chg):.2f} (1M: {pct:+.1f}%)</div>
</div>"""
            st.html(metric_html)
            
            if st.button(f"📈 Chart {label}", key=f"pulse_btn_{sid}", use_container_width=True, type="secondary"):
                st.session_state.selected_macro_id = sid
                st.switch_page("pages/macro_explorer.py")
        else:
            metric_html = f"""<div class="qm-metric-card">
<div class="qm-metric-label">{label}</div>
<div class="qm-metric-value">--</div>
</div>"""
            st.html(metric_html)

st.html("<div style='margin-bottom: 24px;'></div>")

# ==========================================
# 2. MACRO REGIME & RISK OVERVIEW
# ==========================================
col_risk, col_regime = st.columns([1, 2.2])

with col_risk:
    risk_score = report.get("macro_risk_score", 45.0)
    risk_fig = create_macro_risk_gauge(risk_score)
    st.plotly_chart(risk_fig, use_container_width=True)

with col_regime:
    regime_name = report.get("overall_regime", "Late-Cycle Disinflationary Transition")
    exec_summary = report.get("executive_summary", "Synthesizing macroeconomic transmission indicators...")
    
    regime_html = f"""<div class="qm-metric-card" style="padding: 24px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
<div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Macroeconomic Regime Synthesis</div>
<span class="qm-badge qm-badge-live">● GEMINI 3.8 FLASH VERIFIED</span>
</div>
<div style="font-size: 1.45rem; font-weight: 800; color: #00F0FF; margin-bottom: 10px;">{regime_name}</div>
<div style="font-size: 0.94rem; color: #CBD5E1; line-height: 1.6; margin-bottom: 18px;">{exec_summary}</div>
</div>"""
    st.html(regime_html)
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.button("🤖 Ask Gemini Copilot About This Regime ➜", use_container_width=True):
            st.switch_page("pages/ai_copilot.py")
    with sub_col2:
        if st.button("🧪 Stress-Test Macro Shock Scenarios ➜", use_container_width=True, type="secondary"):
            st.switch_page("pages/stress_tester.py")

st.html("<div style='margin-bottom: 24px;'></div>")

# ==========================================
# 3. SECTOR SENTIMENT SNAPSHOT & QUICK DRILL-DOWN
# ==========================================
col_radar, col_leaderboard = st.columns([1.5, 1.2])

all_sectors = report.get("sectors", [])
filtered_sectors = [s for s in all_sectors if s["sector"] in st.session_state.get("selected_sectors_filter", [])]
if not filtered_sectors:
    filtered_sectors = all_sectors

with col_radar:
    radar_fig = create_sector_radar_chart(filtered_sectors)
    st.plotly_chart(radar_fig, use_container_width=True)
    if st.button("🎯 Open Full Sector Sentiment Matrix ➜", use_container_width=True):
        st.switch_page("pages/sector_sentiment.py")

with col_leaderboard:
    st.markdown("#### ⚡ **Institutional Sector Sentiment Leaders**")
    st.caption("Click on any sector to inspect its detailed financials, top holdings, and factor sensitivities.")
    
    sorted_sectors = sorted(filtered_sectors, key=lambda x: x["score"], reverse=True)
    top_3 = sorted_sectors[:3]
    bottom_3 = sorted_sectors[-3:]
    
    st.html("<span style='color: #00E676; font-weight: 700; font-size: 0.85rem;'>▲ TOP OVERWEIGHT SECTORS</span>")
    for s in top_3:
        sec_name = s["sector"]
        score = s["score"]
        etf = MARKET_SECTORS.get(sec_name, {}).get("etf", "ETF")
        
        c_left, c_right = st.columns([3, 2])
        with c_left:
            row_html = f"""<div style="padding: 6px 0;">
<b style="color: #FFFFFF; font-size: 0.95rem;">{sec_name}</b> 
<span style="color: #94A3B8; font-family: 'JetBrains Mono'; font-size: 0.8rem;">({etf})</span>
<span style="color: #00E676; font-family: 'JetBrains Mono'; font-weight: 700; margin-left: 8px;">{score:+.1f}</span>
</div>"""
            st.html(row_html)
        with c_right:
            if st.button(f"Drill Down ➜", key=f"top_dive_{sec_name}", use_container_width=True, type="secondary"):
                st.session_state.selected_sector = sec_name
                st.switch_page("pages/sector_deep_dive.py")
                
    st.html("<div style='margin-top: 14px;'></div><span style='color: #FF5252; font-weight: 700; font-size: 0.85rem;'>▼ TOP UNDERWEIGHT SECTORS</span>")
    for s in bottom_3:
        sec_name = s["sector"]
        score = s["score"]
        etf = MARKET_SECTORS.get(sec_name, {}).get("etf", "ETF")
        
        c_left, c_right = st.columns([3, 2])
        with c_left:
            row_html = f"""<div style="padding: 6px 0;">
<b style="color: #FFFFFF; font-size: 0.95rem;">{sec_name}</b> 
<span style="color: #94A3B8; font-family: 'JetBrains Mono'; font-size: 0.8rem;">({etf})</span>
<span style="color: #FF5252; font-family: 'JetBrains Mono'; font-weight: 700; margin-left: 8px;">{score:+.1f}</span>
</div>"""
            st.html(row_html)
        with c_right:
            if st.button(f"Drill Down ➜", key=f"bot_dive_{sec_name}", use_container_width=True, type="secondary"):
                st.session_state.selected_sector = sec_name
                st.switch_page("pages/sector_deep_dive.py")

st.markdown("---")

# ==========================================
# 4. MULTIPAGE TERMINAL MODULES HUB
# ==========================================
st.markdown("#### 🚀 **QuantMaster Interactive Command Hub**")
st.caption("Explore dedicated pages for deep sector drill-downs, cross-asset correlations, stress testing, and real-time AI reasoning.")

hub_c1, hub_c2, hub_c3 = st.columns(3)

with hub_c1:
    action1_html = """<div class="qm-action-card">
<div class="qm-action-icon">🎯</div>
<div class="qm-action-title">Sector Sentiment Matrix</div>
<div class="qm-action-desc">Complete 360° radar distribution across all 12 S&P sectors with real-time sentiment scores, institutional catalyst channels, and allocation gauges.</div>
</div>"""
    st.html(action1_html)
    if st.button("Open Sector Matrix ➜", key="hub_btn_matrix", use_container_width=True):
        st.switch_page("pages/sector_sentiment.py")

with hub_c2:
    action2_html = """<div class="qm-action-card">
<div class="qm-action-icon">🏢</div>
<div class="qm-action-title">Sector Drill-Down & Comps</div>
<div class="qm-action-desc">Granular single-sector terminal page with technical moving averages, 52-week ranges, macro factor betas, top constituent stocks, and Gemini memos.</div>
</div>"""
    st.html(action2_html)
    if st.button("Open Sector Drill-Down ➜", key="hub_btn_dive", use_container_width=True):
        st.switch_page("pages/sector_deep_dive.py")

with hub_c3:
    action3_html = """<div class="qm-action-card">
<div class="qm-action-icon">📈</div>
<div class="qm-action-title">Macro & Market Explorer</div>
<div class="qm-action-desc">Overlay any FRED economic series with sector ETFs. Inspect cross-asset correlation heatmaps and Treasury yield curve recession inversions.</div>
</div>"""
    st.html(action3_html)
    if st.button("Open Macro Explorer ➜", key="hub_btn_explorer", use_container_width=True):
        st.switch_page("pages/macro_explorer.py")

hub_c4, hub_c5, hub_c6 = st.columns(3)

with hub_c4:
    action4_html = """<div class="qm-action-card">
<div class="qm-action-icon">🧪</div>
<div class="qm-action-title">Scenario Stress-Tester</div>
<div class="qm-action-desc">Simulate Fed policy rate shocks, crude oil spikes, and yield curve shifts. Test historical crisis scenarios (1970s stagflation, 2008 crunch).</div>
</div>"""
    st.html(action4_html)
    if st.button("Open Scenario Lab ➜", key="hub_btn_stress", use_container_width=True):
        st.switch_page("pages/stress_tester.py")

with hub_c5:
    action5_html = """<div class="qm-action-card">
<div class="qm-action-icon">🤖</div>
<div class="qm-action-title">Gemini AI Strategy Copilot</div>
<div class="qm-action-desc">Institutional macro strategist powered by Gemini 3.8 Flash. Ask complex transmission questions, generate asset allocations, and debate policy.</div>
</div>"""
    st.html(action5_html)
    if st.button("Open AI Copilot ➜", key="hub_btn_copilot", use_container_width=True):
        st.switch_page("pages/ai_copilot.py")

with hub_c6:
    action6_html = """<div class="qm-action-card">
<div class="qm-action-icon">📋</div>
<div class="qm-action-title">Economic Registry & Data Hub</div>
<div class="qm-action-desc">Complete reference library of all tracked FRED series with historical observations, momentum metrics, transmission pathways, and CSV export.</div>
</div>"""
    st.html(action6_html)
    if st.button("Open Data Registry ➜", key="hub_btn_registry", use_container_width=True):
        st.switch_page("pages/economic_registry.py")
