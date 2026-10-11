"""
QuantMaster 007 - Common UI & State Management
Provides shared terminal state, navigation bars, header banners, and sidebar controls.
Ensures seamless multi-page interactivity, zero API-key prompt clutter, and clean HTML rendering.
"""

import os
import streamlit as st
import pandas as pd
from modules.config import (
    FRED_API_KEY,
    GEMINI_API_KEY,
    DEFAULT_GEMINI_MODEL,
    MARKET_SECTORS
)
from modules.data_loader import get_terminal_data
from modules.gemini_analyzer import analyze_macro_sentiment
from modules.styles import inject_styles

def init_app_state():
    """Initializes global terminal state."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "sentiment_report" not in st.session_state:
        st.session_state.sentiment_report = None
    if "selected_sector" not in st.session_state:
        st.session_state.selected_sector = "Technology"
    if "selected_macro_id" not in st.session_state:
        st.session_state.selected_macro_id = "FEDFUNDS"
    if "lookback_days" not in st.session_state:
        st.session_state.lookback_days = 365
    if "selected_sectors_filter" not in st.session_state:
        st.session_state.selected_sectors_filter = list(MARKET_SECTORS.keys())
    if "stress_preset" not in st.session_state:
        st.session_state.stress_preset = None

def get_shared_data():
    """Loads and caches macro and sector terminal datasets."""
    init_app_state()
    lookback = st.session_state.get("lookback_days", 365)
    macro_df, sector_prices_df, macro_summary, sector_returns_df = get_terminal_data(lookback_days=lookback)
    
    # Generate sentiment report via gemini-3.8-flash if not cached
    if st.session_state.sentiment_report is None:
        with st.spinner("Synthesizing institutional sector sentiment via gemini-3.8-flash..."):
            report = analyze_macro_sentiment(
                macro_summary=macro_summary,
                sector_returns=sector_returns_df.to_dict(orient="records"),
                api_key=GEMINI_API_KEY,
                model_name=DEFAULT_GEMINI_MODEL
            )
            st.session_state.sentiment_report = report
            
    return macro_df, sector_prices_df, macro_summary, sector_returns_df, st.session_state.sentiment_report

def render_terminal_header(subtitle: str = "Global Macroeconomic Intelligence & Sector Sentiment Terminal"):
    """Renders the institutional top header with live credentials and regime badges using native st.html."""
    st.markdown(inject_styles(), unsafe_allow_html=True)
    report = st.session_state.get("sentiment_report", {})
    regime = report.get("overall_regime", "EXPANSION") if report else "EXPANSION"
    
    # Credential badges
    fred_badge = '<span class="qm-badge qm-badge-live">● FRED LIVE API</span>' if FRED_API_KEY else '<span class="qm-badge qm-badge-demo">● FRED DEMO MODE</span>'
    gemini_badge = f'<span class="qm-badge qm-badge-ai">● {DEFAULT_GEMINI_MODEL.upper()} ACTIVE</span>' if GEMINI_API_KEY else '<span class="qm-badge qm-badge-demo">● GEMINI DEMO MODE</span>'
    regime_badge = f'<span class="qm-badge qm-badge-live">REGIME: {regime.upper()}</span>'

    header_html = f"""<div class="qm-header-container">
<div>
<h1 class="qm-title">QUANTMASTER 007</h1>
<div class="qm-subtitle">{subtitle}</div>
</div>
<div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
{fred_badge}
{gemini_badge}
{regime_badge}
</div>
</div>"""
    st.html(header_html)

def render_quick_navigation(active_page: str = "overview"):
    """
    Renders top interactive action pills allowing instant navigation between pages.
    """
    cols = st.columns(7)
    nav_items = [
        ("⚡ Overview", "pages/overview.py", "overview"),
        ("🎯 Sector Matrix", "pages/sector_sentiment.py", "sector_sentiment"),
        ("🏢 Sector Deep Dive", "pages/sector_deep_dive.py", "sector_deep_dive"),
        ("📈 Macro Explorer", "pages/macro_explorer.py", "macro_explorer"),
        ("🧪 Stress Tester", "pages/stress_tester.py", "stress_tester"),
        ("🤖 AI Copilot", "pages/ai_copilot.py", "ai_copilot"),
        ("📋 Data Hub", "pages/economic_registry.py", "economic_registry")
    ]
    
    for i, (label, path, key_name) in enumerate(nav_items):
        with cols[i]:
            is_active = (active_page == key_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_top_{key_name}", use_container_width=True, type=btn_type):
                if not is_active:
                    st.switch_page(path)
                    
    st.html("<div style='margin-bottom: 16px;'></div>")

def render_sector_card(s: dict):
    """
    Renders an institutional sector card with zero markdown indentation issues using st.html.
    """
    sector_name = s.get("sector", "")
    score = s.get("score", 0.0)
    label = s.get("sentiment_label", "Neutral")
    alloc = s.get("allocation", "Neutral")
    catalyst = s.get("key_catalyst", "")
    risk = s.get("risk_factor", "")
    
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
    
    holdings_pills = "".join([f'<span class="qm-holding-pill">{h}</span>' for h in holdings])
    progress_pct = max(0.0, min(100.0, (score + 100.0) / 2.0))
    
    card_html = f"""<div class="qm-sector-card {card_class}">
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
<div style="width: {progress_pct:.1f}%; height: 100%; background: {score_color}; border-radius: 3px;"></div>
</div>
<div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.45; margin-bottom: 8px;">
<strong style="color: #00F0FF;">Key Catalyst:</strong> {catalyst}
</div>
<div style="font-size: 0.80rem; color: #94A3B8; line-height: 1.4; margin-bottom: 12px;">
<strong style="color: #FF5252;">Watch Risk:</strong> {risk}
</div>
<div style="margin-top: 10px; margin-bottom: 14px;">
<span style="font-size: 0.74rem; color: #64748B; text-transform: uppercase; font-weight: 600;">Top Holdings:</span><br>
{holdings_pills}
</div>
</div>"""
    st.html(card_html)

def render_sidebar():
    """
    Renders the clean institutional sidebar without any API key input clutter.
    """
    with st.sidebar:
        st.markdown("### ⚡ **QuantMaster Terminal**")
        st.caption("Institutional Quantitative Architecture")
        st.markdown("---")
        
        # System status card
        fred_status = '<div style="font-size: 0.85rem; color: #00E676; margin-top: 4px;">🟢 FRED Real-Time API: <b>Active</b></div>' if FRED_API_KEY else '<div style="font-size: 0.85rem; color: #FFD600; margin-top: 4px;">🟡 FRED Real-Time API: <b>Demo Mode</b></div>'
        gemini_status = f'<div style="font-size: 0.85rem; color: #C084FC; margin-top: 2px;">🟣 Gemini Core: <b>{DEFAULT_GEMINI_MODEL}</b></div>' if GEMINI_API_KEY else '<div style="font-size: 0.85rem; color: #FFD600; margin-top: 2px;">🟡 Gemini Core: <b>Simulation Mode</b></div>'
        
        status_html = f"""<div style="background: rgba(19, 24, 34, 0.7); border: 1px solid rgba(0, 240, 255, 0.15); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
<div style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Active Engine Status</div>
{fred_status}
{gemini_status}
<div style="font-size: 0.85rem; color: #00F0FF; margin-top: 2px;">⚡ Multi-Page Architecture: <b>Online</b></div>
</div>"""
        st.html(status_html)
        
        st.markdown("#### ⚙️ **Horizon & Universe**")
        lookback_options = ["6 Months", "1 Year", "3 Years", "5 Years"]
        curr_lookback = "1 Year"
        if st.session_state.get("lookback_days") == 180:
            curr_lookback = "6 Months"
        elif st.session_state.get("lookback_days") == 1095:
            curr_lookback = "3 Years"
        elif st.session_state.get("lookback_days") == 1825:
            curr_lookback = "5 Years"
            
        selected_lb = st.selectbox(
            "Lookback Horizon",
            options=lookback_options,
            index=lookback_options.index(curr_lookback)
        )
        days_map = {"6 Months": 180, "1 Year": 365, "3 Years": 1095, "5 Years": 1825}
        if days_map[selected_lb] != st.session_state.get("lookback_days"):
            st.session_state.lookback_days = days_map[selected_lb]
            st.cache_data.clear()
            st.session_state.sentiment_report = None
            st.rerun()
            
        selected_sec = st.multiselect(
            "Filter Sectors",
            options=list(MARKET_SECTORS.keys()),
            default=st.session_state.get("selected_sectors_filter", list(MARKET_SECTORS.keys()))
        )
        st.session_state.selected_sectors_filter = selected_sec
        
        st.markdown("---")
        if st.button("🔄 Refresh Data Feeds", use_container_width=True):
            st.cache_data.clear()
            st.session_state.sentiment_report = None
            st.rerun()
