"""
QuantMaster 007 - Gemini AI Strategy Copilot
Institutional quantitative macroeconomic strategist powered by Google Gemini 3.8 Flash.
Synthesizes regime briefings, answers complex transmission questions, and generates tactical asset allocations.
"""

import streamlit as st
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import GEMINI_API_KEY, DEFAULT_GEMINI_MODEL
from modules.gemini_analyzer import ask_gemini_copilot

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Gemini AI Strategy Copilot • Powered by Google Gemini 3.8 Flash")
render_quick_navigation(active_page="ai_copilot")
render_sidebar()

# ==========================================
# 1. EXECUTIVE MACRO BRIEFING CARD
# ==========================================
regime = report.get('overall_regime', 'Economic Transition')
exec_summary = report.get('executive_summary', 'Synthesizing live macroeconomic indicators...')

briefing_html = f"""<div class="qm-metric-card" style="margin-bottom: 20px; border-left: 4px solid #C084FC;">
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
<div style="font-size: 1.25rem; font-weight: 700; color: #00F0FF;">Executive Macro Intelligence Briefing: {regime}</div>
<span class="qm-badge qm-badge-ai">● GEMINI 3.8 FLASH VERIFIED</span>
</div>
<p style="font-size: 0.95rem; color: #E2E8F0; line-height: 1.65; margin-top: 12px; margin-bottom: 0;">{exec_summary}</p>
</div>"""
st.html(briefing_html)

# ==========================================
# 2. PROMPT SUGGESTION CHIPS
# ==========================================
st.markdown("##### 💡 **Instant Institutional Prompt Library**")
st.caption("Click any prompt to instantly query Gemini 3.8 Flash with live macroeconomic groundings:")

preset_queries = [
    "How does a Fed rate pause affect Regional Banks vs Megacap Tech?",
    "What is the transmission of high crude oil on Consumer Discretionary?",
    "Analyze recession risk and timeline based on current 10Y-2Y yield curve spread.",
    "Recommend a 3-month tactical asset allocation across all 12 sectors.",
    "Compare defensive characteristics of Utilities vs Healthcare in late-cycle."
]

chip_cols = st.columns(len(preset_queries))
clicked_chip_prompt = None

for idx, q in enumerate(preset_queries):
    with chip_cols[idx]:
        short_label = q[:35] + "..."
        if st.button(f"🔍 {short_label}", key=f"chip_{idx}", use_container_width=True, type="secondary"):
            clicked_chip_prompt = q

# Check if navigated with preloaded prompt
if "chat_prompt" in st.session_state and st.session_state.chat_prompt:
    clicked_chip_prompt = st.session_state.chat_prompt
    st.session_state.chat_prompt = None

st.markdown("---")

# ==========================================
# 3. INTERACTIVE CHAT INTERFACE
# ==========================================
st.markdown("#### 💬 **Conversational Strategy Terminal**")

chat_box = st.container()
with chat_box:
    if not st.session_state.chat_history:
        st.info("👋 **Welcome to QuantMaster Copilot.** Ask any question about interest rates, inflation, sector rotations, or macroeconomic transmission channels.")
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                user_bubble = f'<div class="qm-chat-bubble-user">👤 <b>Quantitative Portfolio Manager:</b><br>{msg["content"]}</div>'
                st.html(user_bubble)
            else:
                assistant_bubble = f'<div class="qm-chat-bubble-assistant">🤖 <b>Gemini 3.8 Flash Copilot:</b><br>{msg["content"]}</div>'
                st.html(assistant_bubble)

# Handle user input from text box or prompt chips
user_q = st.chat_input("Ask Gemini 3.8 Flash about interest rates, inflation, sector rotations, or asset allocation...")

target_query = clicked_chip_prompt or user_q

if target_query:
    st.session_state.chat_history.append({"role": "user", "content": target_query})
    with st.spinner("Gemini 3.8 Flash is analyzing macroeconomic transmission channels..."):
        ans = ask_gemini_copilot(
            question=target_query,
            macro_summary=macro_summary,
            chat_history=st.session_state.chat_history,
            api_key=GEMINI_API_KEY,
            model_name=DEFAULT_GEMINI_MODEL
        )
    st.session_state.chat_history.append({"role": "assistant", "content": ans})
    st.rerun()

st.html("<div style='margin-bottom: 20px;'></div>")

# Utilities: Clear chat and export
c_clear, c_export, c_nav = st.columns([1.5, 2, 2.5])
with c_clear:
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

with c_export:
    transcript = "\n\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in st.session_state.chat_history])
    st.download_button(
        "📥 Download Chat Briefing (TXT)",
        data=transcript.encode("utf-8"),
        file_name="quantmaster_gemini_briefing.txt",
        mime="text/plain",
        use_container_width=True
    )

with c_nav:
    if st.button("🎯 Return to Sector Sentiment Matrix ➜", use_container_width=True):
        st.switch_page("pages/sector_sentiment.py")
