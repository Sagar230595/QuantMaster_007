"""
QuantMaster 007 - Global Macro & Sector Sentiment Intelligence Platform
Master Multipage Entrypoint & Navigation Controller
Institutional quantitative terminal architecture powered by Federal Reserve Economic Data and Google Gemini 3.8 Flash.
"""

import streamlit as st

# Page configuration - must be the first Streamlit command in the entrypoint
st.set_page_config(
    page_title="QuantMaster 007 | Institutional Quantitative Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define Multipage Navigation Hierarchy
pages = {
    "Macro Pulse & Overview": [
        st.Page("pages/overview.py", title="Global Macro Pulse", icon="⚡", default=True),
    ],
    "Sector Intelligence": [
        st.Page("pages/sector_sentiment.py", title="Sector Sentiment Matrix", icon="🎯"),
        st.Page("pages/sector_deep_dive.py", title="Sector Drill-Down & Comps", icon="🏢"),
    ],
    "Quantitative Lab": [
        st.Page("pages/macro_explorer.py", title="Macro & Market Explorer", icon="📈"),
        st.Page("pages/stress_tester.py", title="Scenario Stress-Tester", icon="🧪"),
    ],
    "AI Strategy & Data Hub": [
        st.Page("pages/ai_copilot.py", title="Gemini AI Strategy Copilot", icon="🤖"),
        st.Page("pages/economic_registry.py", title="Economic Registry & Hub", icon="📋"),
    ]
}

# Run Streamlit Navigation
pg = st.navigation(pages)
pg.run()
