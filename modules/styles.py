"""
QuantMaster 007 - Styling & CSS System
Institutional dark quantitative terminal styling with glassmorphism, responsive grids, and modern UI components.
"""

TERMINAL_CSS = """
<style>
/* Import Inter / JetBrains Mono typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #E2E8F0;
}

code, kbd, samp, pre {
    font-family: 'JetBrains Mono', monospace;
}

/* Base background glow */
.stApp {
    background-color: #07090E;
    background-image: 
        radial-gradient(circle at 10% 15%, rgba(0, 240, 255, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 90% 85%, rgba(124, 77, 255, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.5) 0%, transparent 100%);
    background-attachment: fixed;
}

/* Hide default streamlit clutter */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sleek Header Banner */
.qm-header-container {
    background: linear-gradient(135deg, rgba(19, 24, 34, 0.9) 0%, rgba(11, 14, 20, 0.98) 100%);
    border: 1px solid rgba(0, 240, 255, 0.22);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(14px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.qm-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #FFFFFF 20%, #00F0FF 80%, #7000FF 120%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.1;
}

.qm-subtitle {
    color: #94A3B8;
    font-size: 0.92rem;
    font-weight: 400;
    margin-top: 5px;
    letter-spacing: 0.01em;
}

/* Quant Status Badges */
.qm-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.qm-badge-live {
    background: rgba(0, 230, 118, 0.12);
    color: #00E676;
    border: 1px solid rgba(0, 230, 118, 0.35);
}

.qm-badge-demo {
    background: rgba(255, 214, 0, 0.12);
    color: #FFD600;
    border: 1px solid rgba(255, 214, 0, 0.3);
}

.qm-badge-ai {
    background: rgba(124, 77, 255, 0.15);
    color: #C084FC;
    border: 1px solid rgba(168, 85, 247, 0.4);
}

/* Glassmorphism Metric Cards */
.qm-metric-card {
    background: rgba(19, 24, 34, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, border-color 0.2s ease;
    height: 100%;
}

.qm-metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 240, 255, 0.38);
}

.qm-metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

.qm-metric-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #F8FAFC;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
}

.qm-metric-delta-pos {
    color: #00E676;
    font-size: 0.82rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 4px;
}

.qm-metric-delta-neg {
    color: #FF1744;
    font-size: 0.82rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 4px;
}

/* Action Cards for Multipage Dynamic Exploration */
.qm-action-card {
    background: linear-gradient(145deg, rgba(19, 24, 34, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    height: 100%;
}

.qm-action-card:hover {
    border-color: #00F0FF;
    transform: translateY(-3px);
    box-shadow: 0 10px 30px -10px rgba(0, 240, 255, 0.25);
}

.qm-action-icon {
    font-size: 1.8rem;
    margin-bottom: 10px;
}

.qm-action-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 6px;
}

.qm-action-desc {
    font-size: 0.84rem;
    color: #94A3B8;
    line-height: 1.5;
}

/* Sector Card Grid */
.qm-sector-card {
    background: linear-gradient(145deg, rgba(19, 24, 34, 0.88) 0%, rgba(15, 19, 28, 0.96) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.qm-sector-card:hover {
    border-color: rgba(0, 240, 255, 0.45);
    box-shadow: 0 8px 30px -8px rgba(0, 240, 255, 0.18);
    transform: translateY(-2px);
}

.qm-sector-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
}

.qm-sector-bullish::before {
    background: #00E676;
    box-shadow: 0 0 10px #00E676;
}

.qm-sector-bearish::before {
    background: #FF1744;
    box-shadow: 0 0 10px #FF1744;
}

.qm-sector-neutral::before {
    background: #FFD600;
    box-shadow: 0 0 10px #FFD600;
}

/* Pill allocation badges */
.qm-alloc-overweight {
    background: rgba(0, 230, 118, 0.15);
    color: #00E676;
    border: 1px solid rgba(0, 230, 118, 0.4);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

.qm-alloc-underweight {
    background: rgba(255, 23, 68, 0.15);
    color: #FF5252;
    border: 1px solid rgba(255, 23, 68, 0.4);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

.qm-alloc-neutral {
    background: rgba(255, 214, 0, 0.15);
    color: #FFD600;
    border: 1px solid rgba(255, 214, 0, 0.4);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

/* Constituent Stock Holding Pills */
.qm-holding-pill {
    display: inline-block;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #E2E8F0;
    padding: 3px 10px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 3px 4px 3px 0;
}

/* Quick Jump Navigation Bar */
.qm-nav-bar {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    background: rgba(19, 24, 34, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 24px;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #0B0E14 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00F0FF 0%, #0099FF 100%);
    color: #07090E !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 14px rgba(0, 240, 255, 0.22);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0, 240, 255, 0.4);
    color: #000000 !important;
}

/* Secondary outline button */
.stButton > button[kind="secondary"] {
    background: rgba(19, 24, 34, 0.8) !important;
    color: #CBD5E1 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: #00F0FF !important;
    color: #00F0FF !important;
}

/* Chat bubble styling */
.qm-chat-bubble-user {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px 12px 2px 12px;
    padding: 12px 16px;
    margin-bottom: 12px;
    margin-left: 15%;
    color: #F1F5F9;
    font-size: 0.92rem;
}

.qm-chat-bubble-assistant {
    background: linear-gradient(145deg, rgba(19, 24, 34, 0.92) 0%, rgba(15, 23, 42, 0.92) 100%);
    border: 1px solid rgba(0, 240, 255, 0.25);
    border-radius: 12px 12px 12px 2px;
    padding: 16px 20px;
    margin-bottom: 16px;
    margin-right: 10%;
    color: #E2E8F0;
    font-size: 0.92rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}

/* Callout Note Boxes */
.qm-callout {
    background: rgba(15, 23, 42, 0.65);
    border-left: 3px solid #00F0FF;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    margin: 14px 0;
    font-size: 0.88rem;
    color: #CBD5E1;
}
</style>
"""

def inject_styles():
    """Returns CSS string for embedding in Streamlit markdown."""
    return TERMINAL_CSS
