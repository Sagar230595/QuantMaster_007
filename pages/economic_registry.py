"""
QuantMaster 007 - Economic Registry & Data Hub
Institutional reference library of Federal Reserve economic series.
Provides time-series inspector, momentum stats, transmission analysis, and CSV data export.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import FRED_INDICATORS
from modules.visualizations import create_single_indicator_chart

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Federal Reserve Economic Registry & Time-Series Inspector")
render_quick_navigation(active_page="economic_registry")
render_sidebar()

# ==========================================
# 1. SEARCHABLE REGISTRY TABLE
# ==========================================
st.markdown("#### 📋 **Global Economic Indicator Registry**")
st.caption("Registry of tracked Federal Reserve Economic Data (FRED) series with latest observations, momentum, and transmission pathways.")

cat_options = ["All Categories"] + sorted(list(set([info["category"] for info in FRED_INDICATORS.values()])))
sel_cat = st.selectbox("Filter Indicators by Category", options=cat_options, index=0)

summary_df = pd.DataFrame(macro_summary)
if sel_cat != "All Categories":
    summary_df = summary_df[summary_df["category"] == sel_cat]

display_df = summary_df[[
    "name", "id", "category", "latest", "unit", "change_1m", "pct_1m", "pct_1y", "trend"
]].rename(columns={
    "name": "Indicator Name",
    "id": "FRED Series ID",
    "category": "Category",
    "latest": "Latest Observation",
    "unit": "Unit",
    "change_1m": "1M Abs Change",
    "pct_1m": "1M % Change",
    "pct_1y": "1Y % Change",
    "trend": "Trend"
})

st.dataframe(
    display_df.style.format({
        "Latest Observation": "{:,.2f}",
        "1M Abs Change": "{:+,.2f}",
        "1M % Change": "{:+,.2f}%",
        "1Y % Change": "{:+,.2f}%"
    }),
    use_container_width=True
)

st.markdown("---")

# ==========================================
# 2. TIME-SERIES INSPECTOR & TRANSMISSION
# ==========================================
st.markdown("#### 🔍 **Individual Series Inspector**")
st.caption("Inspect granular historical observations, trendlines, and economic transmission channels for any indicator.")

default_inspect = st.session_state.get("selected_macro_id", "FEDFUNDS")
if default_inspect not in FRED_INDICATORS:
    default_inspect = "FEDFUNDS"

inspect_id = st.selectbox(
    "Select Indicator to Inspect",
    options=list(FRED_INDICATORS.keys()),
    index=list(FRED_INDICATORS.keys()).index(default_inspect),
    format_func=lambda x: f"{FRED_INDICATORS[x]['name']} ({x}) — {FRED_INDICATORS[x]['category']}"
)
st.session_state.selected_macro_id = inspect_id

ind_info = FRED_INDICATORS[inspect_id]

col_chart, col_meta = st.columns([2.2, 1])

with col_chart:
    if inspect_id in macro_df.columns:
        fig_single = create_single_indicator_chart(
            series=macro_df[inspect_id],
            name=ind_info["name"],
            unit=ind_info["unit"]
        )
        st.plotly_chart(fig_single, use_container_width=True)

with col_meta:
    series_s = macro_df[inspect_id].dropna() if inspect_id in macro_df.columns else pd.Series()
    latest_val = series_s.iloc[-1] if not series_s.empty else 0.0
    mean_val = series_s.mean() if not series_s.empty else 0.0
    hi_val = series_s.max() if not series_s.empty else 0.0
    lo_val = series_s.min() if not series_s.empty else 0.0

    meta_html = f"""<div class="qm-metric-card" style="margin-bottom: 12px;">
<div class="qm-metric-label">{ind_info['name']}</div>
<div class="qm-metric-value">{latest_val:,.2f} <span style="font-size:0.85rem; color:#94A3B8;">{ind_info['unit']}</span></div>
<div style="font-size:0.82rem; color:#00F0FF; margin-top:4px;">Frequency: <b>{ind_info['frequency']}</b></div>
</div>
<div class="qm-metric-card" style="margin-bottom: 12px;">
<div class="qm-metric-label">Historical Range Statistics</div>
<div style="font-size:0.85rem; color:#CBD5E1; line-height:1.7;">
• Maximum: <b style="font-family:'JetBrains Mono'; color:#FFFFFF;">{hi_val:,.2f}</b><br>
• Minimum: <b style="font-family:'JetBrains Mono'; color:#FFFFFF;">{lo_val:,.2f}</b><br>
• Mean: <b style="font-family:'JetBrains Mono'; color:#FFFFFF;">{mean_val:,.2f}</b>
</div>
</div>
<div class="qm-metric-card">
<div class="qm-metric-label">Economic Role & Rationale</div>
<div style="font-size:0.82rem; color:#CBD5E1; line-height:1.5;">{ind_info['description']}</div>
</div>"""
    st.html(meta_html)

callout_html = f"""<div class="qm-callout">
<strong style="color: #00F0FF;">Market Impact & Transmission Pathway:</strong> {ind_info['impact']}
</div>"""
st.html(callout_html)

if st.button(f"📈 Overlay {ind_info['name']} with Sector ETFs in Macro Explorer ➜", use_container_width=True):
    st.session_state.selected_macro_id = inspect_id
    st.switch_page("pages/macro_explorer.py")

st.markdown("---")

# ==========================================
# 3. DATA EXPORT HUB
# ==========================================
st.markdown("#### 📥 **Institutional Data Export Hub**")
st.caption("Download clean, time-aligned CSV files for quantitative modeling in Python, R, or Excel.")

dl_col1, dl_col2 = st.columns(2)
with dl_col1:
    csv_macro = macro_df.to_csv().encode('utf-8')
    st.download_button(
        "📥 Download Historical Macro Data (CSV)",
        data=csv_macro,
        file_name=f"quantmaster_macro_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with dl_col2:
    all_sectors = report.get("sectors", [])
    csv_sentiment = pd.DataFrame(all_sectors).to_csv().encode('utf-8')
    st.download_button(
        "📥 Download Sector Sentiment Matrix (CSV)",
        data=csv_sentiment,
        file_name=f"quantmaster_sentiment_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
