"""
QuantMaster 007 - Data Loader
Fetches macroeconomic data via FRED API and market sector performance via Yahoo Finance.
Includes offline demo generator for instant plug-and-play testing.
"""

import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import yfinance as yf
from modules.config import FRED_INDICATORS, MARKET_SECTORS, MARKET_BENCHMARKS, FRED_API_KEY

# Cache period: 1 hour for market & macro data
CACHE_TTL = 3600

def generate_mock_macro_series(series_id: str, days: int = 1825) -> pd.Series:
    """Generates realistic synthetic economic time series for offline demo testing."""
    np.random.seed(abs(hash(series_id)) % (2**31 - 1))
    end_date = datetime.now()
    dates = pd.date_range(end=end_date, periods=days, freq='B')
    
    profiles = {
        "FEDFUNDS": (5.33, 0.005, 0.05, 5.5),
        "DGS10": (4.25, 0.015, 0.5, 5.0),
        "T10Y2Y": (-0.15, 0.01, -0.8, 1.2),
        "CPIAUCSL": (314.0, 0.05, 260.0, 320.0),
        "CPILFESL": (320.0, 0.04, 270.0, 325.0),
        "GDPC1": (22800.0, 5.0, 20000.0, 23500.0),
        "INDPRO": (103.5, 0.02, 98.0, 105.0),
        "UNRATE": (4.1, 0.01, 3.4, 6.0),
        "PAYEMS": (158500.0, 20.0, 150000.0, 160000.0),
        "DCOILWTICO": (76.5, 0.4, 55.0, 115.0),
        "STLFSI4": (-0.45, 0.02, -1.2, 1.8),
        "UMCSENT": (69.5, 0.25, 50.0, 95.0),
    }
    
    base_val, step_vol, min_val, max_val = profiles.get(series_id, (100.0, 0.1, 50.0, 150.0))
    steps = np.random.normal(0, step_vol, len(dates))
    values = base_val + np.cumsum(steps)
    values = np.clip(values, min_val, max_val)
    
    series = pd.Series(values, index=dates).ffill()
    return series

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_fred_series(series_id: str, api_key: str = None, lookback_days: int = 1825) -> pd.Series:
    """
    Fetches observations for a FRED series.
    Uses official FRED REST API when key is provided, falls back to demo generator if key is missing or invalid.
    """
    effective_key = (api_key or FRED_API_KEY or os.getenv("FRED_API_KEY", "")).strip()
    if effective_key:
        try:
            start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                "series_id": series_id,
                "api_key": effective_key,
                "file_type": "json",
                "observation_start": start_date,
                "sort_order": "asc"
            }
            resp = requests.get(url, params=params, timeout=8)
            if resp.status_code == 200:
                data = resp.json().get("observations", [])
                if data:
                    dates, values = [], []
                    for obs in data:
                        val = obs.get("value")
                        if val and val != ".":
                            try:
                                values.append(float(val))
                                dates.append(pd.to_datetime(obs.get("date")))
                            except ValueError:
                                pass
                    if values:
                        s = pd.Series(values, index=dates).sort_index()
                        return s
        except Exception:
            pass  # Fall back to synthetic mock data
            
    return generate_mock_macro_series(series_id, days=lookback_days)

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_all_macro_data(api_key: str = None, lookback_days: int = 1825) -> pd.DataFrame:
    """Fetches all registered macroeconomic indicators into an aligned DataFrame."""
    macro_dict = {}
    for sid in FRED_INDICATORS.keys():
        s = fetch_fred_series(sid, api_key=api_key, lookback_days=lookback_days)
        macro_dict[sid] = s
    
    df = pd.DataFrame(macro_dict).ffill().bfill()
    return df

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_sector_market_data(lookback_days: int = 1825) -> pd.DataFrame:
    """
    Fetches daily adjusted close prices for all market sector ETFs and benchmarks using yfinance.
    """
    all_tickers = [sec["etf"] for sec in MARKET_SECTORS.values()] + list(MARKET_BENCHMARKS.keys())
    clean_tickers = [t.strip() for t in all_tickers]
    
    try:
        start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        data = yf.download(clean_tickers, start=start_date, progress=False, auto_adjust=True)
        if isinstance(data.columns, pd.MultiIndex):
            if 'Close' in data.columns.levels[0]:
                prices = data['Close']
            else:
                prices = data.xs(data.columns.levels[0][0], axis=1)
        else:
            prices = data
        prices = prices.ffill().bfill()
        return prices
    except Exception:
        dates = pd.date_range(end=datetime.now(), periods=lookback_days, freq='B')
        mock_data = {}
        np.random.seed(42)
        for t in clean_tickers:
            daily_returns = np.random.normal(0.0004, 0.012, len(dates))
            mock_data[t] = 100 * np.cumprod(1 + daily_returns)
        return pd.DataFrame(mock_data, index=dates)

def calculate_macro_summary(macro_df: pd.DataFrame) -> list:
    """
    Computes latest values, 1-month changes, 1-year changes, and momentum signals
    for each macroeconomic indicator.
    """
    summary = []
    for sid, info in FRED_INDICATORS.items():
        if sid in macro_df.columns:
            series = macro_df[sid].dropna()
            if len(series) >= 2:
                latest_val = series.iloc[-1]
                idx_1m = max(0, len(series) - 22)
                val_1m = series.iloc[idx_1m]
                chg_1m = latest_val - val_1m
                pct_1m = ((latest_val - val_1m) / abs(val_1m) * 100) if val_1m != 0 else 0
                
                idx_1y = max(0, len(series) - 252)
                val_1y = series.iloc[idx_1y]
                pct_1y = ((latest_val - val_1y) / abs(val_1y) * 100) if val_1y != 0 else 0
                
                trend = "↗" if chg_1m > 0 else ("↘" if chg_1m < 0 else "→")
                
                summary.append({
                    "id": sid,
                    "name": info["name"],
                    "category": info["category"],
                    "latest": latest_val,
                    "unit": info["unit"],
                    "change_1m": chg_1m,
                    "pct_1m": pct_1m,
                    "pct_1y": pct_1y,
                    "trend": trend,
                    "description": info["description"],
                    "impact": info["impact"]
                })
    return summary

def calculate_sector_returns(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates returns across various windows (1W, 1M, 3M, 6M, 1Y) for each sector.
    """
    records = []
    for sector_name, info in MARKET_SECTORS.items():
        etf = info["etf"]
        if etf in prices_df.columns:
            s = prices_df[etf].dropna()
            if len(s) >= 5:
                latest = s.iloc[-1]
                ret_1w = ((latest - s.iloc[max(0, len(s) - 5)]) / s.iloc[max(0, len(s) - 5)]) * 100
                ret_1m = ((latest - s.iloc[max(0, len(s) - 22)]) / s.iloc[max(0, len(s) - 22)]) * 100
                ret_3m = ((latest - s.iloc[max(0, len(s) - 66)]) / s.iloc[max(0, len(s) - 66)]) * 100
                ret_1y = ((latest - s.iloc[max(0, len(s) - 252)]) / s.iloc[max(0, len(s) - 252)]) * 100
                
                records.append({
                    "Sector": sector_name,
                    "ETF": etf,
                    "Category": info.get("category", "General"),
                    "Price": round(latest, 2),
                    "1W %": round(ret_1w, 2),
                    "1M %": round(ret_1m, 2),
                    "3M %": round(ret_3m, 2),
                    "1Y %": round(ret_1y, 2),
                    "Name": info["name"]
                })
    return pd.DataFrame(records)

def calculate_sector_technicals(prices_df: pd.DataFrame, ticker: str) -> dict:
    """
    Computes technical metrics (SMA 50, SMA 200, 52W Range, 30D Volatility) for a sector ETF.
    """
    if ticker not in prices_df.columns:
        return {}
    s = prices_df[ticker].dropna()
    if len(s) < 10:
        return {}
        
    latest = s.iloc[-1]
    sma_50 = s.rolling(50).mean().iloc[-1] if len(s) >= 50 else latest
    sma_200 = s.rolling(200).mean().iloc[-1] if len(s) >= 200 else latest
    
    # 52 week range (approx 252 days)
    lookback_52w = min(len(s), 252)
    s_52w = s.iloc[-lookback_52w:]
    high_52w = s_52w.max()
    low_52w = s_52w.min()
    
    # 30D Annualized Volatility
    pct_changes = s.pct_change().dropna()
    vol_30d = (pct_changes.iloc[-30:].std() * np.sqrt(252) * 100) if len(pct_changes) >= 30 else 15.0
    
    # Distance from 52W High
    pct_from_high = ((latest - high_52w) / high_52w * 100) if high_52w else 0.0

    return {
        "latest": round(latest, 2),
        "sma_50": round(sma_50, 2),
        "sma_200": round(sma_200, 2),
        "above_sma_50": latest >= sma_50,
        "above_sma_200": latest >= sma_200,
        "high_52w": round(high_52w, 2),
        "low_52w": round(low_52w, 2),
        "pct_from_high": round(pct_from_high, 2),
        "volatility_annualized": round(vol_30d, 2)
    }

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_terminal_data(lookback_days: int = 1825):
    """
    Unified cached data loader returning all core data objects for the terminal.
    """
    macro_df = fetch_all_macro_data(lookback_days=lookback_days)
    sector_prices_df = fetch_sector_market_data(lookback_days=lookback_days)
    macro_summary = calculate_macro_summary(macro_df)
    sector_returns_df = calculate_sector_returns(sector_prices_df)
    return macro_df, sector_prices_df, macro_summary, sector_returns_df
