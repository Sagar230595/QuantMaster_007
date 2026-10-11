"""
QuantMaster 007 - Interactive Visualizations
Institutional-grade Plotly charts: Radar charts, Dual-axis macro vs sector plots,
Correlation heatmaps, Risk gauges, Technical charts, Factor Betas, and Normalized Comparisons.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Dark Theme Layout Configuration
DARK_LAYOUT = dict(
    paper_bgcolor='rgba(11, 14, 20, 0.85)',
    plot_bgcolor='rgba(15, 19, 28, 0.7)',
    font=dict(family="Inter, sans-serif", color="#CBD5E1", size=12),
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(
        bgcolor='rgba(19, 24, 34, 0.85)',
        bordercolor='rgba(255, 255, 255, 0.1)',
        borderwidth=1,
        font=dict(size=11, color="#E2E8F0")
    ),
    hoverlabel=dict(
        bgcolor="#1E293B",
        bordercolor="#00F0FF",
        font=dict(family="JetBrains Mono, monospace", size=12, color="#FFFFFF")
    )
)

def create_sector_radar_chart(sentiment_data: list) -> go.Figure:
    """
    Creates a 360-degree polar radar chart displaying sentiment scores across market sectors.
    """
    if not sentiment_data:
        return go.Figure()
        
    sectors = [item["sector"] for item in sentiment_data]
    scores = [item["score"] for item in sentiment_data]
    
    sectors_closed = sectors + [sectors[0]]
    scores_closed = scores + [scores[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[0] * len(sectors_closed),
        theta=sectors_closed,
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.25)', dash='dash', width=1),
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=sectors_closed,
        fill='toself',
        fillcolor='rgba(0, 240, 255, 0.18)',
        line=dict(color='#00F0FF', width=2.5),
        marker=dict(
            size=7,
            color=['#00E676' if s > 15 else ('#FF1744' if s < -15 else '#FFD600') for s in scores_closed],
            symbol='circle'
        ),
        name="Sentiment Score",
        hovertemplate="<b>%{theta}</b><br>Sentiment Score: %{r:+.1f}<extra></extra>"
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-100, 100],
                tickvals=[-80, -40, 0, 40, 80],
                ticktext=["-80 (Bearish)", "-40", "0 (Neutral)", "+40", "+80 (Bullish)"],
                gridcolor='rgba(255, 255, 255, 0.08)',
                color='#94A3B8',
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.12)',
                color='#F1F5F9',
                tickfont=dict(size=11, family="Inter, sans-serif")
            ),
            bgcolor='rgba(15, 19, 28, 0.6)'
        ),
        title=dict(
            text="<b>Global Macro Sector Sentiment Radar</b>",
            font=dict(size=16, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        showlegend=False,
        height=480
    )
    return fig

def create_macro_vs_sector_chart(macro_series: pd.Series, sector_series: pd.Series, 
                                 macro_name: str, sector_name: str) -> go.Figure:
    """
    Creates an interactive dual-axis chart comparing an economic indicator to a sector ETF.
    """
    df = pd.DataFrame({"Macro": macro_series, "Sector": sector_series}).dropna()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Macro"],
        name=macro_name,
        line=dict(color='#00F0FF', width=2.2),
        yaxis='y1',
        hovertemplate="<b>" + macro_name + "</b>: %{y:.2f}<br>%{x|%Y-%m-%d}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Sector"],
        name=sector_name,
        line=dict(color='#FF9100', width=2.2),
        yaxis='y2',
        hovertemplate="<b>" + sector_name + "</b>: $%{y:.2f}<br>%{x|%Y-%m-%d}<extra></extra>"
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text=f"<b>Macro Overlay: {macro_name} vs {sector_name}</b>",
            font=dict(size=15, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8',
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            title=dict(text=macro_name, font=dict(color='#00F0FF')),
            tickfont=dict(color='#00F0FF'),
            gridcolor='rgba(255, 255, 255, 0.06)',
            side='left'
        ),
        yaxis2=dict(
            title=dict(text=sector_name, font=dict(color='#FF9100')),
            tickfont=dict(color='#FF9100'),
            overlaying='y',
            side='right',
            gridcolor='rgba(0, 0, 0, 0)'
        ),
        height=450,
        hovermode="x unified"
    )
    return fig

def create_correlation_heatmap(macro_df: pd.DataFrame, sector_prices: pd.DataFrame) -> go.Figure:
    """
    Computes Pearson correlation matrix between economic indicators and sector returns.
    """
    merged = pd.concat([macro_df, sector_prices], axis=1).dropna()
    pct_changes = merged.pct_change(periods=22).dropna()
    
    macro_cols = [c for c in macro_df.columns if c in pct_changes.columns]
    sector_cols = [c for c in sector_prices.columns if c in pct_changes.columns]
    
    if not macro_cols or not sector_cols:
        return go.Figure()
        
    corr_matrix = pct_changes.corr().loc[sector_cols, macro_cols]
    
    fig = px.imshow(
        corr_matrix,
        labels=dict(x="Macroeconomic Indicator", y="Sector / Benchmark", color="Correlation"),
        x=macro_cols,
        y=sector_cols,
        color_continuous_scale=[
            [0.0, "#FF1744"],
            [0.5, "#1E293B"],
            [1.0, "#00E676"]
        ],
        zmin=-1,
        zmax=1,
        aspect="auto"
    )
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text="<b>Cross-Asset Correlation Matrix (Macro vs Sector Returns)</b>",
            font=dict(size=15, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(color='#94A3B8', tickangle=-30),
        yaxis=dict(color='#94A3B8'),
        coloraxis_colorbar=dict(
            title="Correlation",
            tickvals=[-1, -0.5, 0, 0.5, 1],
            tickfont=dict(color="#CBD5E1")
        ),
        height=480
    )
    return fig

def create_macro_risk_gauge(risk_score: float) -> go.Figure:
    """
    Creates a semicircular institutional risk gauge for overall macroeconomic fragility.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Macro Risk Index</b>", 'font': {'size': 18, 'color': '#F8FAFC'}},
        number={'suffix': "/100", 'font': {'size': 32, 'family': 'JetBrains Mono', 'color': '#FFFFFF'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8", 'tickfont': {'color': "#94A3B8"}},
            'bar': {'color': "#00F0FF", 'thickness': 0.28},
            'bgcolor': "rgba(19, 24, 34, 0.8)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(0, 230, 118, 0.2)'},
                {'range': [30, 70], 'color': 'rgba(255, 214, 0, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(255, 23, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#FF1744", 'width': 3},
                'thickness': 0.8,
                'value': 75
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(11, 14, 20, 0.85)',
        font=dict(family="Inter, sans-serif", color="#CBD5E1"),
        margin=dict(l=30, r=30, t=50, b=30),
        height=260
    )
    return fig

def create_sector_performance_bar(sector_returns_df: pd.DataFrame, period: str = "1M %") -> go.Figure:
    """
    Horizontal bar chart of sector returns color-coded by positive/negative return.
    """
    if sector_returns_df.empty or period not in sector_returns_df.columns:
        return go.Figure()
        
    df = sector_returns_df.sort_values(by=period, ascending=True)
    colors = ['#00E676' if x >= 0 else '#FF1744' for x in df[period]]
    
    fig = go.Figure(go.Bar(
        x=df[period],
        y=df["Sector"],
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(255, 255, 255, 0.15)', width=1)),
        text=[f"{x:+.2f}%" for x in df[period]],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=11, color="#F8FAFC"),
        hovertemplate="<b>%{y}</b>: %{x:+.2f}%<extra></extra>"
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text=f"<b>Sector Performance Leaderboard ({period})</b>",
            font=dict(size=15, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(
            title=f"Return ({period})",
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.3)'
        ),
        yaxis=dict(color='#F1F5F9'),
        height=420
    )
    return fig

def create_yield_curve_chart(yield_curve_series: pd.Series) -> go.Figure:
    """
    Historical 10Y-2Y yield curve spread chart highlighting inversion recession danger zones.
    """
    s = yield_curve_series.dropna()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=s.index,
        y=s.values,
        name="10Y - 2Y Spread (%)",
        line=dict(color='#00F0FF', width=2),
        hovertemplate="<b>Spread</b>: %{y:+.2f}%<br>%{x|%Y-%m-%d}<extra></extra>"
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="#FF1744", annotation_text="Inversion Zero Threshold", 
                  annotation_position="bottom right", annotation_font_color="#FF1744")
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text="<b>US Treasury Yield Curve Spread (10Y minus 2Y)</b>",
            font=dict(size=15, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.06)', color='#94A3B8'),
        yaxis=dict(
            title="Spread (%)",
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8'
        ),
        height=320
    )
    return fig

def create_sector_technicals_chart(prices_df: pd.DataFrame, ticker: str, sector_name: str) -> go.Figure:
    """
    Interactive price chart with 50-day and 200-day moving averages and volume/bands.
    """
    if ticker not in prices_df.columns:
        return go.Figure()
        
    s = prices_df[ticker].dropna()
    sma_50 = s.rolling(50).mean()
    sma_200 = s.rolling(200).mean()
    
    fig = go.Figure()
    
    # Area gradient under price
    fig.add_trace(go.Scatter(
        x=s.index,
        y=s.values,
        name=f"{sector_name} ({ticker})",
        line=dict(color='#00F0FF', width=2.4),
        fill='tozeroy',
        fillcolor='rgba(0, 240, 255, 0.05)',
        hovertemplate="<b>Price</b>: $%{y:.2f}<br>%{x|%Y-%m-%d}<extra></extra>"
    ))
    
    # SMA 50
    fig.add_trace(go.Scatter(
        x=sma_50.index,
        y=sma_50.values,
        name="50-Day Moving Average",
        line=dict(color='#FFD600', width=1.5, dash='solid'),
        hovertemplate="<b>50-SMA</b>: $%{y:.2f}<extra></extra>"
    ))
    
    # SMA 200
    fig.add_trace(go.Scatter(
        x=sma_200.index,
        y=sma_200.values,
        name="200-Day Moving Average",
        line=dict(color='#B388FF', width=1.5, dash='dash'),
        hovertemplate="<b>200-SMA</b>: $%{y:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text=f"<b>{sector_name} ({ticker}) Historical Price & Trend Technicians</b>",
            font=dict(size=16, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8',
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            title="Price ($)",
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8'
        ),
        height=450,
        hovermode="x unified"
    )
    return fig

def create_factor_sensitivity_bar(sensitivities: dict, sector_name: str) -> go.Figure:
    """
    Horizontal bar chart showing positive & negative macroeconomic factor betas for a sector.
    """
    if not sensitivities:
        return go.Figure()
        
    factors = list(sensitivities.keys())
    values = list(sensitivities.values())
    colors = ['#00E676' if v >= 0 else '#FF1744' for v in values]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=factors,
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(255, 255, 255, 0.15)', width=1)),
        text=[f"{v:+.2f}" for v in values],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=11, color="#F8FAFC"),
        hovertemplate="<b>%{y}</b>: %{x:+.2f} Beta<extra></extra>"
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text=f"<b>Macro Factor Beta Sensitivities ({sector_name})</b>",
            font=dict(size=14, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(
            title="Beta Sensitivity (-1.0 to +1.0)",
            range=[-1.0, 1.0],
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.3)'
        ),
        yaxis=dict(color='#CBD5E1'),
        height=300
    )
    return fig

def create_normalized_comparison_chart(prices_df: pd.DataFrame, tickers_dict: dict) -> go.Figure:
    """
    Indexed normalized returns rebased to 100 for side-by-side relative performance comparison.
    """
    valid_cols = [t for t in tickers_dict.keys() if t in prices_df.columns]
    if not valid_cols:
        return go.Figure()
        
    df = prices_df[valid_cols].dropna()
    normalized = (df / df.iloc[0]) * 100
    
    colors = ['#00F0FF', '#7C4DFF', '#00E676', '#FF9100', '#FF1744', '#FFD600', '#00E5FF', '#E040FB']
    
    fig = go.Figure()
    for idx, col in enumerate(valid_cols):
        fig.add_trace(go.Scatter(
            x=normalized.index,
            y=normalized[col],
            name=tickers_dict.get(col, col),
            line=dict(color=colors[idx % len(colors)], width=2),
            hovertemplate="<b>" + tickers_dict.get(col, col) + "</b>: %{y:.1f}<extra></extra>"
        ))
        
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text="<b>Rebased Performance Comparison (Base = 100)</b>",
            font=dict(size=15, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.06)', color='#94A3B8'),
        yaxis=dict(
            title="Indexed Value (Base 100)",
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8'
        ),
        height=450,
        hovermode="x unified"
    )
    return fig

def create_single_indicator_chart(series: pd.Series, name: str, unit: str) -> go.Figure:
    """
    Plots an individual macroeconomic indicator with clean trendline and 30-day moving average.
    """
    s = series.dropna()
    sma = s.rolling(22).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=s.index,
        y=s.values,
        name=name,
        line=dict(color='#00F0FF', width=2),
        hovertemplate=f"<b>{name}</b>: %{{y:.2f}} {unit}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=sma.index,
        y=sma.values,
        name="1-Month Moving Average",
        line=dict(color='#FFD600', width=1.5, dash='dash'),
        hovertemplate=f"<b>1M SMA</b>: %{{y:.2f}} {unit}<extra></extra>"
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=dict(
            text=f"<b>{name} Historical Trend</b>",
            font=dict(size=15, color="#F8FAFC"),
            x=0.02, y=0.96
        ),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.06)', color='#94A3B8'),
        yaxis=dict(
            title=f"{name} ({unit})",
            gridcolor='rgba(255, 255, 255, 0.06)',
            color='#94A3B8'
        ),
        height=380,
        hovermode="x unified"
    )
    return fig
