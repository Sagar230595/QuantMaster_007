"""
QuantMaster 007 - Macro & Market Explorer
Quantitative exploration of macroeconomic indicators against sector performance.
Dual-axis overlay plots, cross-asset correlation heatmaps, and yield curve recession dynamics.
"""

import streamlit as st
import pandas as pd
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import FRED_INDICATORS, MARKET_SECTORS, MARKET_BENCHMARKS
from modules.visualizations import (
    create_macro_vs_sector_chart,
    create_correlation_heatmap,
    create_yield_curve_chart,
    create_sector_performance_bar,
    create_normalized_comparison_chart
)

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Macro & Market Explorer: Dual-Axis Overlays & Correlations")
render_quick_navigation(active_page="macro_explorer")
render_sidebar()

# ==========================================
# 1. DUAL-AXIS MACRO VS SECTOR OVERLAY
# ==========================================
st.markdown("#### 📈 **Dual-Axis Macro vs Sector Analysis**")
st.caption("Overlay macroeconomic series directly against sector ETF historical prices to detect regime inflection points.")

# Determine preselected values from session state
default_macro = st.session_state.get("selected_macro_id", "FEDFUNDS")
if default_macro not in FRED_INDICATORS:
    default_macro = "FEDFUNDS"
default_sector = st.session_state.get("selected_sector_key", "Technology")

exp_col1, exp_col2 = st.columns(2)
with exp_col1:
    chosen_macro_id = st.selectbox(
        "Select Economic Indicator (Left Axis)",
        options=list(FRED_INDICATORS.keys()),
        index=list(FRED_INDICATORS.keys()).index(default_macro),
        format_func=lambda x: f"{FRED_INDICATORS[x]['name']} ({x}) — {FRED_INDICATORS[x]['category']}"
    )
    st.session_state.selected_macro_id = chosen_macro_id

with exp_col2:
    all_ticker_options = list(MARKET_SECTORS.keys()) + list(MARKET_BENCHMARKS.keys())
    sec_idx = all_ticker_options.index(default_sector) if default_sector in all_ticker_options else 0
    chosen_sector_key = st.selectbox(
        "Select Sector or Benchmark (Right Axis)",
        options=all_ticker_options,
        index=sec_idx,
        format_func=lambda x: f"{x} ({MARKET_SECTORS.get(x, {}).get('etf', x)})"
    )
    
chosen_ticker = MARKET_SECTORS.get(chosen_sector_key, {}).get("etf", chosen_sector_key)

if chosen_macro_id in macro_df.columns and chosen_ticker in sector_prices_df.columns:
    fig_overlay = create_macro_vs_sector_chart(
        macro_series=macro_df[chosen_macro_id],
        sector_series=sector_prices_df[chosen_ticker],
        macro_name=FRED_INDICATORS[chosen_macro_id]["name"],
        sector_name=f"{chosen_sector_key} ({chosen_ticker})"
    )
    st.plotly_chart(fig_overlay, use_container_width=True)

# Indicator Quick Insight
macro_meta = FRED_INDICATORS.get(chosen_macro_id, {})
st.html(f"""<div class="qm-callout">
<strong style="color: #00F0FF;">Economic Transmission Channel:</strong> {macro_meta.get('impact', '')}
</div>""")

st.markdown("---")

# ==========================================
# 2. REBASED ASSET COMPARISON
# ==========================================
st.markdown("#### 📊 **Rebased Multi-Asset Performance Comparison**")
st.caption("Compare cumulative returns normalized to base 100 over the selected lookback horizon.")

comp_multiselect = st.multiselect(
    "Choose Sectors & Benchmarks to Compare",
    options=list(MARKET_SECTORS.keys()) + list(MARKET_BENCHMARKS.keys()),
    default=["Technology", "Finance", "Energy", "SPY", "QQQ"]
)

if comp_multiselect:
    comp_tickers = {MARKET_SECTORS.get(k, {}).get("etf", k): k for k in comp_multiselect}
    norm_fig = create_normalized_comparison_chart(sector_prices_df, comp_tickers)
    st.plotly_chart(norm_fig, use_container_width=True)

st.markdown("---")

# ==========================================
# 3. CROSS-ASSET CORRELATION MATRIX & YIELD SPREAD
# ==========================================
col_corr, col_yield = st.columns(2)

with col_corr:
    corr_fig = create_correlation_heatmap(macro_df, sector_prices_df)
    st.plotly_chart(corr_fig, use_container_width=True)

with col_yield:
    if "T10Y2Y" in macro_df.columns:
        yield_fig = create_yield_curve_chart(macro_df["T10Y2Y"])
        st.plotly_chart(yield_fig, use_container_width=True)
    
    st.markdown("##### ⏱️ **Sector Performance By Period**")
    perf_period = st.radio("Select Return Window", ["1W %", "1M %", "3M %", "1Y %"], horizontal=True, index=1)
    perf_fig = create_sector_performance_bar(sector_returns_df, period=perf_period)
    st.plotly_chart(perf_fig, use_container_width=True)

st.markdown("---")

# Next Steps Navigation
act1, act2 = st.columns(2)
with act1:
    if st.button("🧪 Simulate Shocks on These Assets in Stress-Tester ➜", use_container_width=True):
        st.switch_page("pages/stress_tester.py")
with act2:
    if st.button("🤖 Ask Gemini Copilot About Macro Correlations ➜", use_container_width=True):
        st.session_state.chat_prompt = f"Explain the correlation between {chosen_macro_id} and {chosen_sector_key}."
        st.switch_page("pages/ai_copilot.py")
