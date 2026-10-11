# QuantMaster 007 ⚡
### Institutional Global Macroeconomic Intelligence & Dynamic Multi-Page Platform

**QuantMaster 007** is an institutional-grade, dynamic multi-page Streamlit application designed for quantitative analysts, portfolio managers, and macro strategists. It ingests live global macroeconomic data (interest rates, yield curves, inflation, labor, energy, consumer confidence) and synthesizes multi-sector market sentiment using **Google Gemini 3.8 Flash (`gemini-3.8-flash`)**.

---

## 🌟 Dynamic Multi-Page Architecture

QuantMaster 007 is structured as a full dynamic quantitative terminal across 7 dedicated pages:

1. **⚡ Global Macro Pulse (`pages/overview.py`)**:
   - Executive macroeconomic regime synthesis and systemic risk score gauge.
   - Interactive live ticker pulse (Fed Funds, 10Y Yield, 10Y-2Y Spread, CPI, WTI Crude, Unemployment) with one-click direct chart exploration.
   - 360° Polar Sentiment Radar snapshot and Overweight/Underweight sector leaderboards.
   - Interactive Action Hub routing to all terminal modules.

2. **🎯 Sector Sentiment Matrix (`pages/sector_sentiment.py`)**:
   - Full 360° radar distribution across all 12 market sectors.
   - Dynamic filters by sector category (*Growth & Secular, Cyclical & Financials, Defensive Quality, Commodity, Rate-Sensitive*).
   - Interactive sector cards with sentiment scores (-100 to +100), allocation tags, transmission channels, top constituent stocks, and clickable drill-down buttons.

3. **🏢 Sector Drill-Down & Comps (`pages/sector_deep_dive.py`)**:
   - Dedicated single-sector deep dive with moving averages (50-SMA & 200-SMA), 52-week trading ranges, and 30-day realized volatility.
   - Empirical macro factor beta sensitivities (Rates, Inflation, Oil, Yield Curve).
   - Dominant index constituents (comps).
   - Real-time institutional strategic memo synthesized by **Gemini 3.8 Flash**.

4. **📈 Macro & Market Explorer (`pages/macro_explorer.py`)**:
   - Dual-axis interactive overlay: Plot any FRED indicator against any sector ETF or market benchmark (`SPY`, `QQQ`, `^VIX`, `GLD`, `UUP`).
   - Rebased multi-asset cumulative return comparison (Base = 100).
   - Cross-asset Pearson correlation heatmap.
   - Yield curve inversion tracking with historical recession warning thresholds.

5. **🧪 Scenario Stress-Tester & Simulation Lab (`pages/stress_tester.py`)**:
   - Interactive shock sliders (Fed Funds Rate ±200 bps, Crude Oil ±$40, Yield Curve Spread ±1.5%, Inflation ±4.0%).
   - One-click historical crisis presets (*1970s Stagflation, 2008 Credit Crunch, Aggressive Easing, AI Capex Supercycle*).
   - Baseline vs. Simulated post-shock sentiment bar charts with winner/loser breakdowns.
   - **Gemini 3.8 Flash** Chief Risk Officer (CRO) stress assessment memo.

6. **🤖 Gemini AI Strategy Copilot (`pages/ai_copilot.py`)**:
   - Institutional macro strategist powered by **Google Gemini 3.8 Flash (`gemini-3.8-flash`)**.
   - Instant prompt library with one-click chips for rapid macro inquiry.
   - Conversational terminal with chat memory, transcript export, and grounded economic context.

7. **📋 Economic Registry & Data Hub (`pages/economic_registry.py`)**:
   - Comprehensive directory of tracked FRED series with 1-month and 1-year momentum.
   - Single-indicator time-series inspector with historical range statistics and transmission pathways.
   - One-click CSV export of historical macroeconomic data and sector sentiment matrices.

---

## 🔑 Automated API Configurations

All API keys are loaded seamlessly from `.env` in the background with zero UI clutter:
- **Federal Reserve Economic Data (FRED)**: Live API key configured in `.env`.
- **Google Gemini AI**: Default model set to `gemini-3.8-flash`.

---

## 🚀 Getting Started

### 1. Launch the Application
Run the Streamlit application using the provided virtual environment:
```powershell
.\quantmaster\Scripts\python.exe -m streamlit run app.py
```

### 2. Navigate and Interact
- Use the sidebar navigation menu or the top quick-jump action bar to switch between pages.
- Click **"Drill Down"**, **"Explore Chart"**, or **"Stress Test"** on any card to jump directly to dedicated analytical pages.
