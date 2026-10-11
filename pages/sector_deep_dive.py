"""
QuantMaster 007 - Sector Drill-Down & Financial Comps
Granular single-sector analytics terminal page.
Provides moving average technicals, macro factor beta attribution, constituent stock comps,
and institutional research memos powered by Google Gemini 3.8 Flash.
"""

import streamlit as st
import pandas as pd
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import MARKET_SECTORS, GEMINI_API_KEY, DEFAULT_GEMINI_MODEL
from modules.data_loader import calculate_sector_technicals
from modules.visualizations import (
    create_sector_technicals_chart,
    create_factor_sensitivity_bar
)
from modules.gemini_analyzer import analyze_sector_deep_dive

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Granular Sector Drill-Down, Factor Sensitivities & Comps")
render_quick_navigation(active_page="sector_deep_dive")
render_sidebar()

# ==========================================
# 1. SECTOR SELECTOR & PROFILE HEADER
# ==========================================
sector_list = list(MARKET_SECTORS.keys())
curr_sector = st.session_state.get("selected_sector", "Technology")
if curr_sector not in sector_list:
    curr_sector = "Technology"

c_sel, c_back = st.columns([4, 1.5])
with c_sel:
    selected_sector = st.selectbox(
        "Select Sector to Drill Down",
        options=sector_list,
        index=sector_list.index(curr_sector),
        format_func=lambda x: f"{x} ({MARKET_SECTORS[x]['etf']}) — {MARKET_SECTORS[x]['category']}"
    )
    st.session_state.selected_sector = selected_sector

with c_back:
    st.html("<div style='margin-top: 28px;'></div>")
    if st.button("⬅ Back to Sector Matrix", use_container_width=True, type="secondary"):
        st.switch_page("pages/sector_sentiment.py")

sector_info = MARKET_SECTORS[selected_sector]
ticker = sector_info["etf"]

# Find sector sentiment from report
sector_sent = next((s for s in report.get("sectors", []) if s["sector"] == selected_sector), {
    "score": 50.0, "sentiment_label": "Bullish", "allocation": "Overweight", 
    "key_catalyst": "Strong momentum", "risk_factor": "Discount rate volatility"
})

# Find returns
ret_row = sector_returns_df[sector_returns_df["Sector"] == selected_sector]
ret_dict = ret_row.iloc[0].to_dict() if not ret_row.empty else {}

# Calculate technicals
technicals = calculate_sector_technicals(sector_prices_df, ticker)

# Color badge
score = sector_sent.get("score", 0.0)
score_color = "#00E676" if score > 15 else ("#FF1744" if score < -15 else "#FFD600")

# Sector KPI Ribbon
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    card1 = f"""<div class="qm-metric-card">
<div class="qm-metric-label">ETF Benchmark</div>
<div class="qm-metric-value">{ticker}</div>
<div style="font-size:0.8rem; color:#94A3B8; margin-top:4px;">{sector_info['name']}</div>
</div>"""
    st.html(card1)
    
with kpi2:
    price_val = technicals.get("latest", ret_dict.get("Price", 0.0))
    card2 = f"""<div class="qm-metric-card">
<div class="qm-metric-label">Latest Price</div>
<div class="qm-metric-value">${price_val:.2f}</div>
<div style="font-size:0.8rem; color:#94A3B8; margin-top:4px;">Adjusted Close</div>
</div>"""
    st.html(card2)

with kpi3:
    card3 = f"""<div class="qm-metric-card">
<div class="qm-metric-label">Quant Sentiment</div>
<div class="qm-metric-value" style="color: {score_color};">{score:+.1f}</div>
<div style="font-size:0.8rem; color:{score_color}; margin-top:4px;">{sector_sent.get('sentiment_label', 'Neutral')}</div>
</div>"""
    st.html(card3)

with kpi4:
    alloc = sector_sent.get('allocation', 'Neutral').upper()
    card4 = f"""<div class="qm-metric-card">
<div class="qm-metric-label">Recommended Stance</div>
<div class="qm-metric-value" style="font-size:1.4rem; color:#00F0FF;">{alloc}</div>
<div style="font-size:0.8rem; color:#94A3B8; margin-top:4px;">Tactical Allocation</div>
</div>"""
    st.html(card4)

with kpi5:
    ret_1m = ret_dict.get("1M %", 0.0)
    delta_class = "qm-metric-delta-pos" if ret_1m >= 0 else "qm-metric-delta-neg"
    arrow = "▲" if ret_1m >= 0 else "▼"
    card5 = f"""<div class="qm-metric-card">
<div class="qm-metric-label">1-Month Return</div>
<div class="qm-metric-value">{ret_1m:+.2f}%</div>
<div class="{delta_class}">{arrow} 1Y: {ret_dict.get('1Y %', 0.0):+.1f}%</div>
</div>"""
    st.html(card5)

st.html("<div style='margin-bottom: 20px;'></div>")

# ==========================================
# 2. PRICE TECHNICIANS & MOVING AVERAGES
# ==========================================
col_chart, col_side = st.columns([2.2, 1])

with col_chart:
    tech_fig = create_sector_technicals_chart(sector_prices_df, ticker, selected_sector)
    st.plotly_chart(tech_fig, use_container_width=True)

with col_side:
    st.markdown("##### 📐 **Technical & Volatility Health**")
    
    sma50 = technicals.get("sma_50", 0)
    sma200 = technicals.get("sma_200", 0)
    vol = technicals.get("volatility_annualized", 15.0)
    hi52 = technicals.get("high_52w", 0)
    lo52 = technicals.get("low_52w", 0)
    pct_hi = technicals.get("pct_from_high", 0)
    
    trend_state = "Bullish Uptrend (Above 50 & 200 SMA)" if technicals.get("above_sma_50") and technicals.get("above_sma_200") else (
        "Bearish Downtrend (Below Moving Averages)" if not technicals.get("above_sma_50") and not technicals.get("above_sma_200") else
        "Consolidation / Mixed Trend"
    )
    trend_color = "#00E676" if "Bullish" in trend_state else ("#FF1744" if "Bearish" in trend_state else "#FFD600")

    side_html = f"""<div class="qm-metric-card" style="margin-bottom: 12px;">
<div class="qm-metric-label">Trend Alignment</div>
<div style="font-weight: 700; color: {trend_color}; font-size: 0.95rem;">{trend_state}</div>
<div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">50-SMA: <b>${sma50:.2f}</b> | 200-SMA: <b>${sma200:.2f}</b></div>
</div>
<div class="qm-metric-card" style="margin-bottom: 12px;">
<div class="qm-metric-label">52-Week Trading Range</div>
<div style="font-size: 1.15rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #FFFFFF;">${lo52:.2f} — ${hi52:.2f}</div>
<div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">Distance from 52W High: <b style="color: {'#00E676' if pct_hi > -5 else '#FF1744'}">{pct_hi:+.1f}%</b></div>
</div>
<div class="qm-metric-card">
<div class="qm-metric-label">30-Day Realized Volatility</div>
<div style="font-size: 1.45rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #C084FC;">{vol:.1f}%</div>
<div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">Annualized Standard Deviation</div>
</div>"""
    st.html(side_html)

st.html("<div style='margin-bottom: 20px;'></div>")

# ==========================================
# 3. MACRO FACTOR SENSITIVITY & TOP HOLDINGS
# ==========================================
col_sens, col_holdings = st.columns([1.4, 1.4])

with col_sens:
    st.markdown("##### 📡 **Macroeconomic Factor Sensitivities**")
    st.caption("Empirical betas determining how this sector performs when interest rates, crude oil, or GDP shift.")
    sens_fig = create_factor_sensitivity_bar(sector_info.get("macro_sensitivities", {}), selected_sector)
    st.plotly_chart(sens_fig, use_container_width=True)

with col_holdings:
    st.markdown("##### 🏛️ **Top Constituent Holdings & Comps**")
    st.caption("Key mega-cap companies driving sector earnings, cash flows, and index weighting.")
    
    holdings = sector_info.get("top_holdings", [])
    holdings_pills = "".join([f"<span class='qm-holding-pill' style='font-size:0.95rem; padding: 6px 14px;'>{h}</span>" for h in holdings])
    
    holdings_card = f"""<div class="qm-metric-card" style="margin-bottom: 14px;">
<div class="qm-metric-label">Dominant Index Constituents</div>
<div style="margin-top: 10px; margin-bottom: 10px;">{holdings_pills}</div>
<div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.5; margin-top: 8px;">{sector_info.get('description', '')}</div>
</div>"""
    st.html(holdings_card)
    
    st.markdown("##### 🔑 **Core Economic Drivers**")
    for d in sector_info.get("key_drivers", []):
        st.markdown(f"- ⚡ <span style='color: #00F0FF; font-weight: 600;'>{d}</span>", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 4. GEMINI 3.8 FLASH INSTITUTIONAL MEMO
# ==========================================
st.markdown("#### 🤖 **Gemini 3.8 Flash Institutional Sector Briefing**")
st.caption(f"Real-time quantitative thesis and factor attribution synthesized specifically for {selected_sector}.")

memo_cache_key = f"memo_{selected_sector}"
if memo_cache_key not in st.session_state:
    with st.spinner(f"Gemini 3.8 Flash is drafting strategic memo for {selected_sector}..."):
        memo_content = analyze_sector_deep_dive(
            sector_name=selected_sector,
            sector_info=sector_info,
            macro_summary=macro_summary,
            returns_info=ret_dict,
            api_key=GEMINI_API_KEY,
            model_name=DEFAULT_GEMINI_MODEL
        )
        st.session_state[memo_cache_key] = memo_content
else:
    memo_content = st.session_state[memo_cache_key]

memo_header = f"""<div style="background: rgba(19, 24, 34, 0.9); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 12px 12px 0 0; padding: 18px 22px; display:flex; justify-content:space-between; align-items:center;">
<span style="font-size:1.15rem; font-weight:700; color:#00F0FF;">{selected_sector} Institutional Strategic Memo</span>
<span class="qm-badge qm-badge-ai">● GEMINI 3.8 FLASH SYNTHESIZED</span>
</div>"""
st.html(memo_header)

st.markdown(f"""
<div style="background: rgba(15, 19, 28, 0.9); border: 1px solid rgba(0, 240, 255, 0.15); border-top: none; border-radius: 0 0 12px 12px; padding: 22px; color: #E2E8F0; line-height: 1.7; font-size: 0.94rem;">

{memo_content}

</div>
""", unsafe_allow_html=True)

st.html("<div style='margin-bottom: 20px;'></div>")

# Navigation Buttons
act_col1, act_col2, act_col3 = st.columns(3)
with act_col1:
    if st.button(f"🧪 Stress-Test {selected_sector} ➜", use_container_width=True):
        st.session_state.stress_sector = selected_sector
        st.switch_page("pages/stress_tester.py")
with act_col2:
    if st.button(f"📈 Overlay {selected_sector} with Macro Data ➜", use_container_width=True):
        st.session_state.selected_sector_key = selected_sector
        st.switch_page("pages/macro_explorer.py")
with act_col3:
    if st.button(f"💬 Chat with Copilot about {selected_sector} ➜", use_container_width=True):
        st.session_state.chat_prompt = f"What is your high-conviction outlook on {selected_sector} given current policy rates and growth?"
        st.switch_page("pages/ai_copilot.py")
