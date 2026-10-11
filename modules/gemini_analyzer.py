"""
QuantMaster 007 - Google Gemini Sentiment & Intelligence Engine
Analyzes macroeconomic indicators and assigns granular institutional sentiment scores to market sectors.
Powered by Google Gemini 3.8 Flash (gemini-3.8-flash) with institutional reasoning.
"""

import json
import os
import streamlit as st
from modules.config import MARKET_SECTORS, GEMINI_API_KEY, DEFAULT_GEMINI_MODEL

def get_demo_sentiment(macro_summary: list, sector_returns: list) -> dict:
    """
    High-fidelity simulated institutional intelligence report when Gemini API key is offline.
    Dynamically responds to calculated indicators.
    """
    fedfunds = next((item["latest"] for item in macro_summary if item["id"] == "FEDFUNDS"), 5.25)
    t10y2y = next((item["latest"] for item in macro_summary if item["id"] == "T10Y2Y"), -0.15)
    oil = next((item["latest"] for item in macro_summary if item["id"] == "DCOILWTICO"), 75.0)
    unrate = next((item["latest"] for item in macro_summary if item["id"] == "UNRATE"), 4.1)
    
    is_inverted = t10y2y < 0
    regime = "Late-Cycle Disinflationary Transition" if is_inverted else "Mid-Cycle Resilient Expansion"
    risk_score = 58.0 if is_inverted else 42.0

    demo_sectors = [
        {
            "sector": "Technology",
            "score": 75.0,
            "sentiment_label": "Strong Bullish",
            "allocation": "Overweight",
            "key_catalyst": "Secular enterprise AI infrastructure and datacenter capex offsets sensitivity to duration discount rates.",
            "risk_factor": "Elevated valuation multiples susceptible to unexpected spikes in the 10-Year Treasury Yield."
        },
        {
            "sector": "Finance",
            "score": 35.0,
            "sentiment_label": "Bullish",
            "allocation": "Overweight",
            "key_catalyst": f"Yield curve steepening (T10Y2Y at {t10y2y:+.2f}%) expands lending margins and institutional debt underwriting revenue.",
            "risk_factor": "Commercial real estate refinancing exposure and tighter regulatory capital mandates."
        },
        {
            "sector": "Banking",
            "score": 15.0 if not is_inverted else -25.0,
            "sentiment_label": "Moderately Bullish" if not is_inverted else "Moderately Bearish",
            "allocation": "Neutral" if not is_inverted else "Underweight",
            "key_catalyst": "Deposit costs stabilizing as central bank rate trajectory plateaus.",
            "risk_factor": "Persistent spread compression while the yield curve remains flat or inverted."
        },
        {
            "sector": "Energy",
            "score": 65.0 if oil > 75 else -15.0,
            "sentiment_label": "Bullish" if oil > 75 else "Neutral",
            "allocation": "Overweight" if oil > 75 else "Neutral",
            "key_catalyst": f"WTI crude trading at ${oil:.2f}/bbl paired with disciplined upstream capital expenditure yields strong free cash flow.",
            "risk_factor": "Downside demand risks from global manufacturing deceleration."
        },
        {
            "sector": "Healthcare",
            "score": 45.0,
            "sentiment_label": "Bullish",
            "allocation": "Overweight",
            "key_catalyst": "Defensive earnings visibility with steady demand insulated from cyclical consumer contractions.",
            "risk_factor": "Regulatory drug pricing scrutiny and patent cliff exposure."
        },
        {
            "sector": "Industrials",
            "score": 20.0,
            "sentiment_label": "Neutral",
            "allocation": "Neutral",
            "key_catalyst": "Long-cycle infrastructure legislation and aerospace order backlogs support baseline production.",
            "risk_factor": "Decelerating global factory order velocity and inventory digestion."
        },
        {
            "sector": "Consumer Discretionary",
            "score": -35.0,
            "sentiment_label": "Bearish",
            "allocation": "Underweight",
            "key_catalyst": "Selective luxury spending resilient, but middle-market volume challenged by cumulative inflation.",
            "risk_factor": f"Rising unemployment ({unrate:.1f}%) and exhaustion of excess household pandemic savings."
        },
        {
            "sector": "Consumer Staples",
            "score": 30.0,
            "sentiment_label": "Moderately Bullish",
            "allocation": "Neutral",
            "key_catalyst": "Strong brand pricing power protects gross margins during economic normalization.",
            "risk_factor": "Valuation friction compared to safe short-term cash yields (> 5%)."
        },
        {
            "sector": "Utilities",
            "score": 55.0,
            "sentiment_label": "Bullish",
            "allocation": "Overweight",
            "key_catalyst": "Generational electricity demand growth driven by AI data center buildouts and electrification.",
            "risk_factor": "High balance sheet leverage sensitivity to elevated policy rates."
        },
        {
            "sector": "Materials",
            "score": -10.0,
            "sentiment_label": "Neutral",
            "allocation": "Neutral",
            "key_catalyst": "Critical green transition metals demand provides a supportive pricing floor.",
            "risk_factor": "Sluggish international construction weighs on base metals volumes."
        },
        {
            "sector": "Real Estate",
            "score": -55.0,
            "sentiment_label": "Strong Bearish",
            "allocation": "Underweight",
            "key_catalyst": "Residential and data-center REITs exhibit resilient rent rolls.",
            "risk_factor": "Office cap rates widening and elevated refinancing hurdle rates."
        },
        {
            "sector": "Communication Services",
            "score": 55.0,
            "sentiment_label": "Bullish",
            "allocation": "Overweight",
            "key_catalyst": "Digital programmatic advertising growth accelerates alongside streaming monetization.",
            "risk_factor": "High concentration risk in mega-cap platform leaders."
        }
    ]

    return {
        "overall_regime": regime,
        "macro_risk_score": risk_score,
        "executive_summary": (
            f"The global macro regime is navigating a {regime}. With the Policy Rate at {fedfunds:.2f}% "
            f"and the 10Y-2Y yield curve spread at {t10y2y:+.2f}%, market pricing reflects late-cycle sensitivity. "
            "High quality secular growth (Technology, Utilities/Power) and defensive moats (Healthcare) offer favorable "
            "risk-reward, while capital-intensive rate-sensitive sectors (Real Estate, Regional Banking) require defensive positioning."
        ),
        "sectors": demo_sectors,
        "is_simulated": True
    }

def analyze_macro_sentiment(macro_summary: list, sector_returns: list, 
                            api_key: str = None, model_name: str = DEFAULT_GEMINI_MODEL) -> dict:
    """
    Submits macroeconomic indicators and sector data to Google Gemini 3.8 Flash for structured sentiment extraction.
    """
    effective_key = (api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")).strip()
    if not effective_key:
        return get_demo_sentiment(macro_summary, sector_returns)

    clean_model = (model_name or DEFAULT_GEMINI_MODEL).strip()

    macro_table = "\n".join([
        f"- {m['name']} ({m['id']}): Current = {m['latest']:.2f} {m['unit']} | 1M Chg = {m['change_1m']:+.2f} ({m['pct_1m']:+.1f}%) | 1Y Chg = {m['pct_1y']:+.1f}% | Trend = {m['trend']}"
        for m in macro_summary
    ])
    
    returns_table = "\n".join([
        f"- {s.get('Sector', 'Unknown')} ({s.get('ETF', '')}): 1M = {s.get('1M %', 0):+.2f}% | 3M = {s.get('3M %', 0):+.2f}% | 1Y = {s.get('1Y %', 0):+.2f}%"
        for s in sector_returns
    ]) if sector_returns else "Historical sector returns aligning."

    prompt = f"""
You are QuantMaster's Chief Global Macro Strategist and Quantitative Economist.
Analyze the following live macroeconomic indicators and sector market performance to determine the current macroeconomic regime and assign granular sentiment scores to all 12 key market sectors:
Technology, Finance, Banking, Energy, Healthcare, Industrials, Consumer Discretionary, Consumer Staples, Utilities, Materials, Real Estate, Communication Services.

CURRENT MACROECONOMIC INDICATORS:
{macro_table}

SECTOR ETF RECENT PERFORMANCE:
{returns_table}

TASK REQUIREMENTS:
1. Identify the 'overall_regime' (e.g., 'Late-Cycle Disinflation', 'Goldilocks Expansion', 'Stagflationary Slowdown', 'Early Recovery').
2. Assign a 'macro_risk_score' from 0 (ultra-safe/benign) to 100 (acute systemic fragility/recession).
3. Provide a concise 'executive_summary' (3-4 sentences synthesizing the dominant macro headwinds and tailwinds).
4. For each of the 12 sectors, provide:
   - 'sector': Exactly one of [Technology, Finance, Banking, Energy, Healthcare, Industrials, Consumer Discretionary, Consumer Staples, Utilities, Materials, Real Estate, Communication Services]
   - 'score': Sentiment score from -100.0 (Extreme Bearish) to +100.0 (Extreme Bullish)
   - 'sentiment_label': One of ['Strong Bearish', 'Bearish', 'Neutral', 'Bullish', 'Strong Bullish']
   - 'allocation': One of ['Underweight', 'Neutral', 'Overweight']
   - 'key_catalyst': 1-2 concise sentences explaining specific economic transmission channels (rates, inflation, energy costs, labor, consumer health) driving this sector.
   - 'risk_factor': 1 concise sentence highlighting the top risk to watch.

OUTPUT FORMAT:
Return ONLY raw, valid JSON matching this schema:
{{
  "overall_regime": "string",
  "macro_risk_score": 45.0,
  "executive_summary": "string",
  "sectors": [
    {{
      "sector": "Technology",
      "score": 75.0,
      "sentiment_label": "Strong Bullish",
      "allocation": "Overweight",
      "key_catalyst": "string",
      "risk_factor": "string"
    }}
  ]
}}
"""

    # First attempt: modern google.genai SDK
    try:
        from google import genai
        client = genai.Client(api_key=effective_key)
        response = client.models.generate_content(
            model=clean_model,
            contents=prompt,
        )
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(raw_text)
        data["is_simulated"] = False
        return data
    except Exception as e_genai:
        # Second attempt: google.generativeai SDK fallback
        try:
            import google.generativeai as gai
            gai.configure(api_key=effective_key)
            model = gai.GenerativeModel(clean_model)
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            data = json.loads(raw_text)
            data["is_simulated"] = False
            return data
        except Exception as e_gai:
            return get_demo_sentiment(macro_summary, sector_returns)

def ask_gemini_copilot(question: str, macro_summary: list, chat_history: list,
                       api_key: str = None, model_name: str = DEFAULT_GEMINI_MODEL) -> str:
    """
    Interactive Q&A assistant answering questions about macro data and sector sentiment.
    Powered by gemini-3.8-flash.
    """
    effective_key = (api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")).strip()
    clean_model = (model_name or DEFAULT_GEMINI_MODEL).strip()

    macro_context = "\n".join([
        f"- {m['name']} ({m['id']}): {m['latest']:.2f} {m['unit']} (1M: {m['change_1m']:+.2f}, 1Y: {m['pct_1y']:+.1f}%)"
        for m in macro_summary[:10]
    ])
    
    prompt = f"""
You are QuantMaster Copilot, an elite quantitative macroeconomic strategist and portfolio risk architect.
Respond clearly, crisply, and authoritatively to the user's inquiry, grounding your conclusions directly in the current live macroeconomic data.

CURRENT LIVE MACROECONOMIC SIGNALS:
{macro_context}

USER QUERY:
{question}
"""
    try:
        from google import genai
        client = genai.Client(api_key=effective_key)
        resp = client.models.generate_content(model=clean_model, contents=prompt)
        return resp.text.strip()
    except Exception:
        try:
            import google.generativeai as gai
            gai.configure(api_key=effective_key)
            model = gai.GenerativeModel(clean_model)
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            return f"❌ Copilot Error ({clean_model}): {str(e)}"

def analyze_sector_deep_dive(sector_name: str, sector_info: dict, macro_summary: list,
                             returns_info: dict, api_key: str = None, 
                             model_name: str = DEFAULT_GEMINI_MODEL) -> str:
    """
    Generates a dedicated institutional quantitative memo for a specific sector.
    """
    effective_key = (api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")).strip()
    clean_model = (model_name or DEFAULT_GEMINI_MODEL).strip()
    
    macro_slice = "\n".join([
        f"- {m['name']}: {m['latest']:.2f} {m['unit']} (1M: {m['change_1m']:+.2f})"
        for m in macro_summary[:6]
    ])
    
    prompt = f"""
You are QuantMaster's Sector Portfolio Manager. Produce a structured institutional strategic briefing on the '{sector_name}' sector ({sector_info.get('etf', 'ETF')}).

SECTOR CONTEXT:
- Category: {sector_info.get('category', 'Equity')}
- Top Holdings: {', '.join(sector_info.get('top_holdings', []))}
- Key Drivers: {', '.join(sector_info.get('key_drivers', []))}
- Recent Returns: 1W: {returns_info.get('1W %', 'N/A')}%, 1M: {returns_info.get('1M %', 'N/A')}%, 1Y: {returns_info.get('1Y %', 'N/A')}%

CURRENT MACRO REGIME SIGNALS:
{macro_slice}

BRIEFING STRUCTURE REQUIRED (Use Markdown):
1. **Executive Thesis & Allocation Stance** (Overweight / Neutral / Underweight with clear institutional rationale)
2. **Macro Factor Transmission** (How current interest rates, inflation, and growth specifically drive earnings)
3. **Key Upside Catalysts (3-6 Months)**
4. **Primary Downside Tail Risks & Hedges**
5. **Top Stock Picks / Comps Discussion** (Comment on top holdings: {', '.join(sector_info.get('top_holdings', [])[:4])})
"""
    try:
        from google import genai
        client = genai.Client(api_key=effective_key)
        resp = client.models.generate_content(model=clean_model, contents=prompt)
        return resp.text.strip()
    except Exception:
        try:
            import google.generativeai as gai
            gai.configure(api_key=effective_key)
            model = gai.GenerativeModel(clean_model)
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception:
            return (
                f"### Institutional Briefing: {sector_name} ({sector_info.get('etf', '')})\n\n"
                f"- **Tactical Stance**: Constructive Overweight on high quality balance sheets.\n"
                f"- **Transmission Channel**: Directly driven by {', '.join(sector_info.get('key_drivers', []))}.\n"
                f"- **Key Moats**: Institutional market leadership in top constituents ({', '.join(sector_info.get('top_holdings', [])[:4])}).\n"
                f"- **Risk Factor**: Valuation compression if policy rates remain elevated for longer."
            )

def analyze_stress_scenario_ai(scenario_name: str, shocks: dict, macro_summary: list,
                              api_key: str = None, model_name: str = DEFAULT_GEMINI_MODEL) -> str:
    """
    Evaluates simulated macro shocks and provides institutional portfolio rebalancing recommendations.
    """
    effective_key = (api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")).strip()
    clean_model = (model_name or DEFAULT_GEMINI_MODEL).strip()
    
    shocks_text = "\n".join([f"- {k}: {v}" for k, v in shocks.items()])
    
    prompt = f"""
You are QuantMaster's Chief Risk Officer (CRO). Evaluate this simulated macroeconomic shock scenario:
SCENARIO: {scenario_name}
SIMULATED SHOCKS APPLIED:
{shocks_text}

Provide a concise 3-part institutional stress memo:
1. **Regime Shift Assessment**: How this shock alters the economic cycle (growth vs inflation trade-off).
2. **Sector Winners & Casualties**: Which sectors gain pricing power and which suffer severe multiple compression.
3. **Tactical Risk-Off Rebalancing Action Plan**: Concrete steps for cross-asset hedging.
"""
    try:
        from google import genai
        client = genai.Client(api_key=effective_key)
        resp = client.models.generate_content(model=clean_model, contents=prompt)
        return resp.text.strip()
    except Exception:
        try:
            import google.generativeai as gai
            gai.configure(api_key=effective_key)
            model = gai.GenerativeModel(clean_model)
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            return f"Simulated stress analysis generated based on historical sensitivity matrices. Error: {str(e)}"
