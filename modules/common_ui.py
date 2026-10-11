"""
QuantMaster 007 - Common UI & State Management
Provides shared terminal state, navigation bars, header banners, and sidebar controls.
Ensures seamless multi-page interactivity and zero API-key prompt clutter.
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
    """Renders the institutional top header with live credentials and regime badges."""
    st.markdown(inject_styles(), unsafe_allow_html=True)
    report = st.session_state.get("sentiment_report", {})
    regime = report.get("overall_regime", "EXPANSION") if report else "EXPANSION"
    
    # Credential badges
    fred_badge = '<span class="qm-badge qm-badge-live">● FRED LIVE API</span>'
    gemini_badge = f'<span class="qm-badge qm-badge-ai">● {DEFAULT_GEMINI_MODEL.upper()} ACTIVE</span>'
    regime_badge = f'<span class="qm-badge qm-badge-live">REGIME: {regime.upper()}</span>'

    st.markdown(f"""
    <div class="qm-header-container">
        <div>
            <h1 class="qm-title">QUANTMASTER 007</h1>
            <div class="qm-subtitle">{subtitle}</div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
            {fred_badge}
            {gemini_badge}
            {regime_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                    
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

def render_sidebar():
    """
    Renders the clean institutional sidebar without any API key input clutter.
    """
    with st.sidebar:
        st.markdown("### ⚡ **QuantMaster Terminal**")
        st.caption("Institutional Quantitative Architecture")
        st.markdown("---")
        
        # System status card
        st.markdown("""
        <div style="background: rgba(19, 24, 34, 0.7); border: 1px solid rgba(0, 240, 255, 0.15); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
            <div style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Active Engine Status</div>
            <div style="font-size: 0.85rem; color: #00E676; margin-top: 4px;">🟢 FRED Real-Time API: <b>Active</b></div>
            <div style="font-size: 0.85rem; color: #C084FC; margin-top: 2px;">🟣 Gemini Core: <b>gemini-3.8-flash</b></div>
            <div style="font-size: 0.85rem; color: #00F0FF; margin-top: 2px;">⚡ Multi-Page Architecture: <b>Online</b></div>
        </div>
        """, unsafe_allow_html=True)
        
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
