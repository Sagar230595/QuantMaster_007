"""
QuantMaster 007 - Sector Sentiment Matrix
Comprehensive 360° institutional sentiment distribution across all key market sectors.
Interactive cards enable instant drill-down routing into deep-dive financials and scenario stress testing.
"""

import streamlit as st
import pandas as pd
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import MARKET_SECTORS
from modules.visualizations import create_sector_radar_chart, create_macro_risk_gauge

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Sector Sentiment Matrix & Strategic Allocations")
render_quick_navigation(active_page="sector_sentiment")
render_sidebar()

all_sectors_data = report.get("sectors", [])

# ==========================================
# 1. RADAR & REGIME SYNTHESIS
# ==========================================
col_radar, col_gauge = st.columns([2, 1.1])

with col_radar:
    radar_fig = create_sector_radar_chart(all_sectors_data)
    st.plotly_chart(radar_fig, use_container_width=True)

with col_gauge:
    risk_gauge = create_macro_risk_gauge(report.get("macro_risk_score", 45.0))
    st.plotly_chart(risk_gauge, use_container_width=True)
    
    regime = report.get('overall_regime', 'Economic Transition')
    st.markdown(f"""
    <div class="qm-metric-card" style="margin-top: 10px;">
        <div class="qm-metric-label">Macroeconomic Cycle Regime</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #00F0FF; margin-top: 4px;">
            {regime}
        </div>
        <div style="font-size: 0.85rem; color: #CBD5E1; margin-top: 6px; line-height: 1.45;">
            {report.get('executive_summary', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 2. DYNAMIC FILTERS & CONTROLS
# ==========================================
st.markdown("#### ⚡ **Interactive Sector Sentiment Breakdown**")
st.caption("Filter and sort sectors. Click 'Drill Down' on any card to navigate directly into its dedicated analytics page.")

f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
with f_col1:
    categories = ["All Categories"] + sorted(list(set([info.get("category", "General") for info in MARKET_SECTORS.values()])))
    selected_category = st.selectbox("Filter by Category", options=categories, index=0)
    
with f_col2:
    sort_option = st.selectbox(
        "Sort Sectors By",
        options=["Sentiment (Highest to Lowest)", "Sentiment (Lowest to Highest)", "Sector Name (A-Z)"],
        index=0
    )

with f_col3:
    alloc_filter = st.multiselect(
        "Allocation Stance",
        options=["Overweight", "Neutral", "Underweight"],
        default=["Overweight", "Neutral", "Underweight"]
    )

# Filter logic
filtered_list = all_sectors_data.copy()

if selected_category != "All Categories":
    filtered_list = [
        s for s in filtered_list 
        if MARKET_SECTORS.get(s["sector"], {}).get("category") == selected_category
    ]

if alloc_filter:
    filtered_list = [s for s in filtered_list if s.get("allocation") in alloc_filter]

# Sorting logic
if sort_option == "Sentiment (Highest to Lowest)":
    filtered_list = sorted(filtered_list, key=lambda x: x["score"], reverse=True)
elif sort_option == "Sentiment (Lowest to Highest)":
    filtered_list = sorted(filtered_list, key=lambda x: x["score"])
else:
    filtered_list = sorted(filtered_list, key=lambda x: x["sector"])

# ==========================================
# 3. INTERACTIVE SECTOR CARDS WITH MULTIPAGE ROUTING
# ==========================================
card_cols = st.columns(3)
for idx, s in enumerate(filtered_list):
    sector_name = s["sector"]
    score = s["score"]
    label = s["sentiment_label"]
    alloc = s["allocation"]
    catalyst = s["key_catalyst"]
    risk = s["risk_factor"]
    
    sec_info = MARKET_SECTORS.get(sector_name, {})
    etf = sec_info.get("etf", "ETF")
    category = sec_info.get("category", "")
    holdings = sec_info.get("top_holdings", [])[:4]
    
    if score > 15:
        card_class = "qm-sector-bullish"
        score_color = "#00E676"
    elif score < -15:
        card_class = "qm-sector-bearish"
        score_color = "#FF1744"
    else:
        card_class = "qm-sector-neutral"
        score_color = "#FFD600"
        
    alloc_class = (
        "qm-alloc-overweight" if alloc.lower() == "overweight" else
        ("qm-alloc-underweight" if alloc.lower() == "underweight" else "qm-alloc-neutral")
    )
    
    with card_cols[idx % 3]:
        holdings_html = " ".join([f"<span class='qm-holding-pill'>{h}</span>" for h in holdings])
        st.markdown(f"""
        <div class="qm-sector-card {card_class}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">{sector_name}</div>
                    <div style="font-size: 0.8rem; color: #94A3B8; font-family: 'JetBrains Mono';">{etf} • {category}</div>
                </div>
                <span class="{alloc_class}">{alloc.upper()}</span>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 14px 0 6px 0;">
                <span style="font-size: 0.78rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Sentiment Score</span>
                <span style="font-size: 1.45rem; font-weight: 800; font-family: 'JetBrains Mono'; color: {score_color};">{score:+.1f}</span>
            </div>
            
            <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; margin-bottom: 12px;">
                <div style="width: {(score + 100) / 2}%; height: 100%; background: {score_color}; border-radius: 3px;"></div>
            </div>
            
            <div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.45; margin-bottom: 8px;">
                <strong style="color: #00F0FF;">Key Catalyst:</strong> {catalyst}
            </div>
            <div style="font-size: 0.80rem; color: #94A3B8; line-height: 1.4; margin-bottom: 12px;">
                <strong style="color: #FF5252;">Watch Risk:</strong> {risk}
            </div>
            
            <div style="margin-top: 10px; margin-bottom: 14px;">
                <span style="font-size: 0.74rem; color: #64748B; text-transform: uppercase; font-weight: 600;">Top Holdings:</span><br>
                {holdings_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button(f"🔍 Drill Down ➜", key=f"mat_dive_{sector_name}", use_container_width=True):
                st.session_state.selected_sector = sector_name
                st.switch_page("pages/sector_deep_dive.py")
        with btn_c2:
            if st.button(f"🧪 Stress Test ➜", key=f"mat_stress_{sector_name}", use_container_width=True, type="secondary"):
                st.session_state.stress_sector = sector_name
                st.switch_page("pages/stress_tester.py")
