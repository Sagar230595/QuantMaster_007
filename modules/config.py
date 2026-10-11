"""
QuantMaster 007 - Configuration & Indicator Definitions
Defines global macroeconomic indicators, sector mappings, and benchmark parameters.
Loads environment credentials with defaults for high-speed terminal operation.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Path to project root .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load environment variables from .env file
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

# API Credentials - securely retrieved from .env or environment variables
FRED_API_KEY = os.getenv("FRED_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

# Supported Google Gemini Models (Defaulting to gemini-3.8-flash)
GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]

# FRED Macroeconomic Indicators Registry
# Free API Registration: https://fredaccount.stlouisfed.org/apikeys
FRED_INDICATORS = {
    # Monetary Policy & Interest Rates
    "FEDFUNDS": {
        "name": "Federal Funds Effective Rate",
        "category": "Monetary Policy",
        "unit": "%",
        "frequency": "Monthly",
        "description": "Core interest rate targeted by the Federal Reserve, dictating interbank lending costs.",
        "impact": "Higher rates increase borrowing costs, squeeze valuations, but expand bank lending spreads if yield curve is steep."
    },
    "DGS10": {
        "name": "10-Year Treasury Yield",
        "category": "Interest Rates",
        "unit": "%",
        "frequency": "Daily",
        "description": "Global risk-free rate benchmark for equity discount rates and long-term borrowing.",
        "impact": "Rising yields compress high-duration growth/tech valuations; benefit cash-rich institutions."
    },
    "T10Y2Y": {
        "name": "10Y - 2Y Treasury Yield Spread",
        "category": "Recession Indicator",
        "unit": "%",
        "frequency": "Daily",
        "description": "Yield curve slope. An inverted spread (< 0) is a historically reliable leading indicator of recessions.",
        "impact": "Inversion hurts banking net interest margins (borrow short, lend long); un-inverting signals late-cycle turning point."
    },
    # Inflation Metrics
    "CPIAUCSL": {
        "name": "Consumer Price Index (CPI)",
        "category": "Inflation",
        "unit": "Index (1982-84=100)",
        "frequency": "Monthly",
        "description": "Headline inflation measuring the cost of a basket of urban consumer goods and services.",
        "impact": "High inflation triggers tighter central bank policies and erodes discretionary purchasing power."
    },
    "CPILFESL": {
        "name": "Core CPI (Ex Food & Energy)",
        "category": "Inflation",
        "unit": "Index (1982-84=100)",
        "frequency": "Monthly",
        "description": "Underlying structural inflation excluding volatile food and energy sectors.",
        "impact": "Primary stickiness metric monitored by the Fed to determine terminal rates."
    },
    # Economic Growth & Activity
    "GDPC1": {
        "name": "Real Gross Domestic Product",
        "category": "Growth",
        "unit": "Billion Chained 2017 $",
        "frequency": "Quarterly",
        "description": "Inflation-adjusted total economic output of goods and services.",
        "impact": "Expanding GDP supports corporate earnings across cyclical sectors (Industrials, Discretionary)."
    },
    "INDPRO": {
        "name": "Industrial Production Index",
        "category": "Growth",
        "unit": "Index (2017=100)",
        "frequency": "Monthly",
        "description": "Real output for manufacturing, mining, and electric/gas utilities.",
        "impact": "Direct proxy for real business cycle activity and capital expenditure."
    },
    # Labor Market
    "UNRATE": {
        "name": "Civilian Unemployment Rate",
        "category": "Labor Market",
        "unit": "%",
        "frequency": "Monthly",
        "description": "Percentage of the civilian labor force actively seeking work.",
        "impact": "Low unemployment sustains consumer spending; sharp uptick (Sahm Rule) signals recession onset."
    },
    "PAYEMS": {
        "name": "Total Nonfarm Payrolls",
        "category": "Labor Market",
        "unit": "Thousands",
        "frequency": "Monthly",
        "description": "Net monthly job creation across all nonfarm commercial and government sectors.",
        "impact": "Leading gauge of economic momentum and wage-push inflation risks."
    },
    # Commodities & Energy
    "DCOILWTICO": {
        "name": "Crude Oil Prices: WTI",
        "category": "Energy & Commodities",
        "unit": "$ / Barrel",
        "frequency": "Daily",
        "description": "Benchmark price for West Texas Intermediate light sweet crude oil.",
        "impact": "High oil prices directly drive Energy sector cash flows while increasing operating costs for airlines, consumer goods, and logistics."
    },
    # Market Stress & Sentiment
    "STLFSI4": {
        "name": "St. Louis Fed Financial Stress Index",
        "category": "Financial Stress",
        "unit": "Index (0 = Normal)",
        "frequency": "Weekly",
        "description": "Composite measure of liquidity, credit spreads, and market volatility. Zero represents normal financial conditions.",
        "impact": "Values above 0 indicate elevated financial stress and banking distress."
    },
    "UMCSENT": {
        "name": "U. of Michigan Consumer Sentiment",
        "category": "Sentiment",
        "unit": "Index (1966=100)",
        "frequency": "Monthly",
        "description": "Survey of consumer attitudes on personal finances, business conditions, and buying climates.",
        "impact": "Directly correlates with Consumer Discretionary spending and durable goods purchases."
    }
}

# Sectors & Representative ETF Proxies with Extended Institutional Metadata
MARKET_SECTORS = {
    "Technology": {
        "etf": "XLK",
        "name": "Technology Select Sector SPDR",
        "category": "Growth & Secular",
        "top_holdings": ["NVDA", "MSFT", "AAPL", "AVGO", "AMD", "CRM"],
        "description": "Semiconductors, enterprise software, AI compute, and cloud platforms.",
        "key_drivers": ["10-Year Discount Rate", "AI Infrastructure Capex", "Enterprise Software Demand", "FX Strength"],
        "macro_sensitivities": {"DGS10": -0.60, "GDPC1": 0.50, "STLFSI4": -0.45}
    },
    "Finance": {
        "etf": "XLF",
        "name": "Financial Select Sector SPDR",
        "category": "Cyclical & Financials",
        "top_holdings": ["BRK.B", "JPM", "V", "MA", "BAC", "GS"],
        "description": "Diversified banks, investment banking, asset management, and payment rails.",
        "key_drivers": ["Yield Curve Steepness", "Credit Spreads", "Net Interest Margins", "AUM Growth"],
        "macro_sensitivities": {"T10Y2Y": 0.65, "FEDFUNDS": 0.45, "STLFSI4": -0.70}
    },
    "Banking": {
        "etf": "KRE",
        "name": "SPDR S&P Regional Banking ETF",
        "category": "Cyclical & Financials",
        "top_holdings": ["FITB", "HBAN", "RF", "CFG", "KEY", "MTB"],
        "description": "US regional commercial lenders with exposure to real estate and local business deposits.",
        "key_drivers": ["Deposit Costs", "Commercial Real Estate", "Loan Demand", "10Y-2Y Spread"],
        "macro_sensitivities": {"T10Y2Y": 0.85, "FEDFUNDS": 0.20, "STLFSI4": -0.80}
    },
    "Energy": {
        "etf": "XLE",
        "name": "Energy Select Sector SPDR",
        "category": "Commodity & Cyclical",
        "top_holdings": ["XOM", "CVX", "COP", "EOG", "SLB", "MPC"],
        "description": "Integrated oil & gas majors, upstream exploration, refining, and energy infrastructure.",
        "key_drivers": ["Crude Oil WTI", "Global Refinery Margins", "OPEC+ Policy", "Inflation Expectations"],
        "macro_sensitivities": {"DCOILWTICO": 0.90, "CPIAUCSL": 0.55, "GDPC1": 0.40}
    },
    "Healthcare": {
        "etf": "XLV",
        "name": "Health Care Select Sector SPDR",
        "category": "Defensive Quality",
        "top_holdings": ["LLY", "UNH", "JNJ", "ABBV", "MRK", "TMO"],
        "description": "Pharmaceuticals, managed care, biotech, medical devices, and diagnostics.",
        "key_drivers": ["Defensive Capital Flows", "Demographic Aging", "Drug Pricing Policy", "Clinical Approvals"],
        "macro_sensitivities": {"GDPC1": 0.15, "STLFSI4": 0.35, "UNRATE": 0.20}
    },
    "Industrials": {
        "etf": "XLI",
        "name": "Industrial Select Sector SPDR",
        "category": "Cyclical & CapEx",
        "top_holdings": ["GE", "CAT", "UNP", "RTX", "HON", "BA"],
        "description": "Aerospace & defense, heavy machinery, transportation, logistics, and building products.",
        "key_drivers": ["Global Manufacturing PMI", "Infrastructure Capex", "Supply Chain Velocity", "Defense Budgets"],
        "macro_sensitivities": {"INDPRO": 0.75, "GDPC1": 0.70, "DCOILWTICO": -0.30}
    },
    "Consumer Discretionary": {
        "etf": "XLY",
        "name": "Consumer Discretionary SPDR",
        "category": "Cyclical & Consumer",
        "top_holdings": ["AMZN", "TSLA", "HD", "MCD", "NKE", "BKNG"],
        "description": "E-commerce, automotive, home improvement, restaurants, and experiential retail.",
        "key_drivers": ["Consumer Sentiment", "Real Disposable Income", "Gasoline Prices", "Credit Card Delinquencies"],
        "macro_sensitivities": {"UMCSENT": 0.80, "CPIAUCSL": -0.65, "UNRATE": -0.55}
    },
    "Consumer Staples": {
        "etf": "XLP",
        "name": "Consumer Staples Select SPDR",
        "category": "Defensive Quality",
        "top_holdings": ["PG", "COST", "WMT", "KO", "PEP", "PM"],
        "description": "Essential household products, discount retail, food & beverage, and tobacco.",
        "key_drivers": ["Pricing Power", "Input Cost Inflation", "Defensive Flight-to-Safety", "Dividend Yield"],
        "macro_sensitivities": {"STLFSI4": 0.40, "GDPC1": 0.10, "CPIAUCSL": -0.20}
    },
    "Utilities": {
        "etf": "XLU",
        "name": "Utilities Select Sector SPDR",
        "category": "Defensive & Power Infrastructure",
        "top_holdings": ["NEE", "SO", "DUK", "CEG", "AEP", "SRE"],
        "description": "Regulated electric utilities, nuclear power providers, and clean grid infrastructure.",
        "key_drivers": ["Bond Yield Proxy", "Data Center Clean Power", "Regulated Rate Base", "Debt Financing Cost"],
        "macro_sensitivities": {"DGS10": -0.75, "FEDFUNDS": -0.60, "STLFSI4": 0.30}
    },
    "Materials": {
        "etf": "XLB",
        "name": "Materials Select Sector SPDR",
        "category": "Commodity & Cyclical",
        "top_holdings": ["LIN", "SHW", "FCX", "ECL", "NEM", "APD"],
        "description": "Industrial chemicals, copper, gold mining, packaging, and construction aggregates.",
        "key_drivers": ["Global Commodity Cycle", "China Industrial Demand", "US Dollar Strength", "Construction Activity"],
        "macro_sensitivities": {"INDPRO": 0.65, "CPIAUCSL": 0.40, "GDPC1": 0.55}
    },
    "Real Estate": {
        "etf": "XLRE",
        "name": "Real Estate Select Sector SPDR",
        "category": "Rate-Sensitive & Yield",
        "top_holdings": ["PLD", "AMT", "EQIX", "WELL", "PSA", "O"],
        "description": "Industrial logistics warehouses, cell towers, data centers, and healthcare REITs.",
        "key_drivers": ["Mortgage & Borrowing Rates", "Occupancy Rates", "Commercial Refinancing Wall", "Cap Rates"],
        "macro_sensitivities": {"DGS10": -0.80, "FEDFUNDS": -0.65, "T10Y2Y": 0.30}
    },
    "Communication Services": {
        "etf": "XLC",
        "name": "Communication Services SPDR",
        "category": "Growth & Digital",
        "top_holdings": ["GOOGL", "META", "NFLX", "DIS", "TMUS", "CMCSA"],
        "description": "Digital advertising, interactive media platforms, streaming entertainment, and telco.",
        "key_drivers": ["Digital Advertising Spend", "Streaming Subscriptions", "Telco Broadband CapEx"],
        "macro_sensitivities": {"GDPC1": 0.45, "UMCSENT": 0.50, "DGS10": -0.40}
    }
}

# Market Benchmarks
MARKET_BENCHMARKS = {
    "SPY": "S&P 500 Index ETF",
    "QQQ": "Nasdaq-100 ETF",
    "^VIX": "CBOE Volatility Index",
    "GLD": "SPDR Gold Shares",
    "UUP": "Invesco DB US Dollar Bullish Fund"
}
