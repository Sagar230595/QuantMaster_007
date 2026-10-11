"""
QuantMaster 007 - Scenario Stress-Tester & Simulation Lab
Simulates macroeconomic shock scenarios (Fed rate adjustments, crude oil spikes, inflation shocks)
and computes real-time sector sentiment shifts and asset reallocation recommendations.
Powered by factor sensitivity matrices and Google Gemini 3.8 Flash.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from modules.common_ui import (
    get_shared_data,
    render_terminal_header,
    render_quick_navigation,
    render_sidebar
)
from modules.config import MARKET_SECTORS, GEMINI_API_KEY, DEFAULT_GEMINI_MODEL
from modules.gemini_analyzer import analyze_stress_scenario_ai

# Load shared data
macro_df, sector_prices_df, macro_summary, sector_returns_df, report = get_shared_data()

# Render Header & Navigation
render_terminal_header(subtitle="Macroeconomic Scenario Stress-Tester & Simulation Lab")
render_quick_navigation(active_page="stress_tester")
render_sidebar()

all_sectors_data = report.get("sectors", [])

st.markdown("#### 🧪 **Interactive Macroeconomic Stress-Tester**")
st.caption("Apply macroeconomic shocks to observe how institutional sector sentiment and allocation recommendations react in real-time.")

# ==========================================
# 1. CRISIS PRESET SCENARIOS
# ==========================================
st.markdown("##### ⚡ **One-Click Historical Crisis Presets**")
p_cols = st.columns(5)

# Manage presets in session state
if "fed_shift" not in st.session_state:
    st.session_state.fed_shift = 0
if "oil_shift" not in st.session_state:
    st.session_state.oil_shift = 0
if "yield_curve_shift" not in st.session_state:
    st.session_state.yield_curve_shift = 0.0
if "cpi_shock" not in st.session_state:
    st.session_state.cpi_shock = 0.0
if "scenario_title" not in st.session_state:
    st.session_state.scenario_title = "Custom Stress Scenario"

with p_cols[0]:
    if st.button("🚨 1970s Stagflation", use_container_width=True):
        st.session_state.fed_shift = 100
        st.session_state.oil_shift = 30
        st.session_state.yield_curve_shift = -0.5
        st.session_state.cpi_shock = 3.0
        st.session_state.scenario_title = "1970s Stagflationary Oil Spike"
        st.rerun()

with p_cols[1]:
    if st.button("📉 2008 Credit Crunch", use_container_width=True):
        st.session_state.fed_shift = -100
        st.session_state.oil_shift = -30
        st.session_state.yield_curve_shift = -0.8
        st.session_state.cpi_shock = -2.0
        st.session_state.scenario_title = "2008 Financial Stress & Liquidity Shock"
        st.rerun()

with p_cols[2]:
    if st.button("🕊️ Aggressive Fed Easing", use_container_width=True):
        st.session_state.fed_shift = -150
        st.session_state.oil_shift = 5
        st.session_state.yield_curve_shift = 0.8
        st.session_state.cpi_shock = -0.5
        st.session_state.scenario_title = "Aggressive Fed Rate Cutting Cycle"
        st.rerun()

with p_cols[3]:
    if st.button("🚀 AI Capex Supercycle", use_container_width=True):
        st.session_state.fed_shift = -25
        st.session_state.oil_shift = -10
        st.session_state.yield_curve_shift = 0.3
        st.session_state.cpi_shock = 0.0
        st.session_state.scenario_title = "Productivity Boom & Capex Supercycle"
        st.rerun()

with p_cols[4]:
    if st.button("🔄 Reset Baseline", use_container_width=True, type="secondary"):
        st.session_state.fed_shift = 0
        st.session_state.oil_shift = 0
        st.session_state.yield_curve_shift = 0.0
        st.session_state.cpi_shock = 0.0
        st.session_state.scenario_title = "Baseline Neutral Conditions"
        st.rerun()

st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

# ==========================================
# 2. INTERACTIVE SHOCK SLIDERS
# ==========================================
s_c1, s_c2, s_c3, s_c4 = st.columns(4)

with s_c1:
    fed_shift = st.slider(
        "Fed Funds Rate Shock (bps)",
        min_value=-200, max_value=+200,
        value=st.session_state.fed_shift, step=25,
        help="Higher rates compress valuation multiples for high-duration assets."
    )
    st.session_state.fed_shift = fed_shift

with s_c2:
    oil_shift = st.slider(
        "Crude Oil Shock ($/bbl)",
        min_value=-40, max_value=+40,
        value=st.session_state.oil_shift, step=5,
        help="Directly affects energy producers vs consumer spending and transport costs."
    )
    st.session_state.oil_shift = oil_shift

with s_c3:
    yield_curve_shift = st.slider(
        "10Y-2Y Spread Shift (%)",
        min_value=-1.5, max_value=+1.5,
        value=st.session_state.yield_curve_shift, step=0.1,
        help="Steepening expands bank net interest margins; inversion raises recession risk."
    )
    st.session_state.yield_curve_shift = yield_curve_shift

with s_c4:
    cpi_shock = st.slider(
        "Inflation Shock (YoY %)",
        min_value=-3.0, max_value=+4.0,
        value=st.session_state.cpi_shock, step=0.25,
        help="Sticky inflation reduces real disposable income and triggers hawkish central banks."
    )
    st.session_state.cpi_shock = cpi_shock

# ==========================================
# 3. COMPUTE SHOCK IMPACT ON SECTORS
# ==========================================
sim_results = []
for s_name, s_info in MARKET_SECTORS.items():
    base_s = next((item["score"] for item in all_sectors_data if item["sector"] == s_name), 0.0)
    sens = s_info.get("macro_sensitivities", {})
    
    delta_score = 0.0
    delta_score += (fed_shift / 25.0) * sens.get("FEDFUNDS", 0.0) * 4.0
    delta_score += (oil_shift / 5.0) * sens.get("DCOILWTICO", 0.0) * 3.5
    delta_score += (yield_curve_shift / 0.2) * sens.get("T10Y2Y", 0.0) * 5.0
    delta_score += (cpi_shock / 0.5) * sens.get("CPIAUCSL", 0.0) * 4.0
    
    new_score = float(np.clip(base_s + delta_score, -100.0, 100.0))
    
    new_alloc = "Overweight" if new_score > 20 else ("Underweight" if new_score < -20 else "Neutral")
    
    sim_results.append({
        "sector": s_name,
        "base_score": base_s,
        "sim_score": new_score,
        "delta": new_score - base_s,
        "allocation": new_alloc,
        "etf": s_info["etf"],
        "category": s_info.get("category", "")
    })

sim_df = pd.DataFrame(sim_results).sort_values(by="sim_score", ascending=False)

st.markdown(f"##### 📊 **Simulated Sector Sensitivity Results: {st.session_state.scenario_title}**")

# Grouped Bar Plot
fig_sim = go.Figure()
fig_sim.add_trace(go.Bar(
    name="Baseline Sentiment",
    x=sim_df["sector"],
    y=sim_df["base_score"],
    marker_color="rgba(148, 163, 184, 0.45)"
))
fig_sim.add_trace(go.Bar(
    name="Post-Shock Simulated Sentiment",
    x=sim_df["sector"],
    y=sim_df["sim_score"],
    marker_color=["#00E676" if x > 15 else ("#FF1744" if x < -15 else "#FFD600") for x in sim_df["sim_score"]]
))

fig_sim.update_layout(
    paper_bgcolor='rgba(11, 14, 20, 0.85)',
    plot_bgcolor='rgba(15, 19, 28, 0.7)',
    font=dict(family="Inter, sans-serif", color="#CBD5E1"),
    barmode='group',
    height=420,
    title=dict(text="<b>Baseline vs Simulated Sector Sentiment Impact</b>", font=dict(color="#F8FAFC")),
    yaxis=dict(title="Sentiment Score (-100 to +100)", range=[-100, 100], gridcolor="rgba(255,255,255,0.06)"),
    xaxis=dict(color="#94A3B8"),
    legend=dict(bgcolor="rgba(19, 24, 34, 0.8)")
)
st.plotly_chart(fig_sim, use_container_width=True)

# Winners & Losers Summary
top_winner = sim_df.sort_values(by="delta", ascending=False).iloc[0]
top_loser = sim_df.sort_values(by="delta", ascending=True).iloc[0]

res_c1, res_c2, res_c3 = st.columns(3)
with res_c1:
    st.markdown(f"""
    <div class="qm-metric-card">
        <div class="qm-metric-label">Top Shock Beneficiary</div>
        <div class="qm-metric-value" style="color: #00E676;">{top_winner['sector']}</div>
        <div style="font-size:0.85rem; color:#00E676; margin-top:4px;">
            Score Shift: <b>{top_winner['delta']:+.1f} pts</b> ({top_winner['sim_score']:+.1f})
        </div>
    </div>
    """, unsafe_allow_html=True)

with res_c2:
    st.markdown(f"""
    <div class="qm-metric-card">
        <div class="qm-metric-label">Most Vulnerable Sector</div>
        <div class="qm-metric-value" style="color: #FF5252;">{top_loser['sector']}</div>
        <div style="font-size:0.85rem; color:#FF5252; margin-top:4px;">
            Score Shift: <b>{top_loser['delta']:+.1f} pts</b> ({top_loser['sim_score']:+.1f})
        </div>
    </div>
    """, unsafe_allow_html=True)

with res_c3:
    ov_count = len(sim_df[sim_df['allocation'] == 'Overweight'])
    un_count = len(sim_df[sim_df['allocation'] == 'Underweight'])
    st.markdown(f"""
    <div class="qm-metric-card">
        <div class="qm-metric-label">Recommended Rebalancing</div>
        <div class="qm-metric-value" style="color: #00F0FF;">{ov_count} Over / {un_count} Under</div>
        <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">
            Post-Shock Portfolio Stance
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Detailed Table
st.dataframe(
    sim_df.rename(columns={
        "sector": "Sector",
        "etf": "ETF",
        "category": "Category",
        "base_score": "Base Score",
        "sim_score": "Shocked Score",
        "delta": "Score Change",
        "allocation": "Post-Shock Stance"
    })[["Sector", "ETF", "Category", "Base Score", "Shocked Score", "Score Change", "Post-Shock Stance"]].style.format({
        "Base Score": "{:+.1f}",
        "Shocked Score": "{:+.1f}",
        "Score Change": "{:+.1f}"
    }),
    use_container_width=True
)

st.markdown("---")

# ==========================================
# 4. GEMINI 3.8 FLASH STRESS MEMO
# ==========================================
st.markdown("#### 🤖 **Gemini 3.8 Flash Stress Test Risk Assessment**")
st.caption("Generate institutional risk evaluation and cross-asset hedging strategy for this exact simulated scenario.")

if st.button("⚡ Generate AI Stress Memo with Gemini 3.8 Flash ➜", use_container_width=True):
    shocks_dict = {
        "Federal Reserve Policy Rate": f"{fed_shift:+} bps",
        "Crude Oil WTI Shock": f"${oil_shift:+} / bbl",
        "10Y-2Y Yield Curve Spread": f"{yield_curve_shift:+.2f} %",
        "Inflation (CPI) Shock": f"{cpi_shock:+.2f} %"
    }
    with st.spinner("Gemini 3.8 Flash is simulating transmission channels..."):
        ai_memo = analyze_stress_scenario_ai(
            scenario_name=st.session_state.scenario_title,
            shocks=shocks_dict,
            macro_summary=macro_summary,
            api_key=GEMINI_API_KEY,
            model_name=DEFAULT_GEMINI_MODEL
        )
        st.session_state.last_stress_memo = ai_memo

if "last_stress_memo" in st.session_state:
    st.markdown(f"""
    <div class="qm-metric-card" style="padding: 22px; border-left: 4px solid #C084FC;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="font-size:1.15rem; font-weight:700; color:#C084FC;">Chief Risk Officer (CRO) Stress Memo: {st.session_state.scenario_title}</span>
            <span class="qm-badge qm-badge-ai">● GEMINI 3.8 FLASH</span>
        </div>
        <div style="color: #E2E8F0; line-height: 1.7; font-size: 0.94rem;">
            {st.session_state.last_stress_memo}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💬 Discuss this Stress Test with Gemini Copilot ➜", use_container_width=True, type="secondary"):
        st.session_state.chat_prompt = f"Let's discuss portfolio hedges for our stress test: {st.session_state.scenario_title} (Fed: {fed_shift}bps, Oil: ${oil_shift})."
        st.switch_page("pages/ai_copilot.py")
