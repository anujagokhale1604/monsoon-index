"""
=============================================================================
MONSOON INDEX — Global Inflation Transmission Dashboard
Streamlit App

Author: Anuja A. Gokhale
        MA Applied Economics, NUS (Merit Scholar)
        ssrn.com/abstract=6514338

HOW TO RUN:
  1. Run monsoon_index_pipeline.py first to generate the CSV files
  2. pip install streamlit plotly pandas numpy statsmodels
  3. streamlit run monsoon_app.py

OR on Google Colab:
  !pip install streamlit plotly pyngrok
  # Then follow Colab tunnel instructions
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Monsoon Index — Global Inflation Tracker",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --cream:#faf6f0; --parch:#f3ede3; --border:#d4c4a8;
  --navy:#1B2A4A; --rust:#c4522e; --gold:#b8860b;
  --sage:#4a6741; --mid:#333; --lite:#666;
}
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;background:var(--cream);color:var(--navy)}
.stApp{background:var(--cream)}
.stTabs [data-baseweb="tab"]{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#1B2A4A !important}
.stTabs [aria-selected="true"]{color:#c4522e !important;font-weight:700}
.stTabs [data-baseweb="tab-list"]{border-bottom:2px solid #d4c4a8}
/* Force markdown text to be visible on light backgrounds */
.stMarkdown p, .stMarkdown li, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown strong,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{color:#333333 !important}
/* Checkbox labels */
.stCheckbox label, .stCheckbox span, .stCheckbox p{color:#1B2A4A !important}
/* Selectbox and slider labels */
.stSelectbox label, .stSlider label, .stSelectSlider label,
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p{color:#1B2A4A !important}
/* Dataframe text */
.stDataFrame, .dataframe{color:#333333 !important}
/* Caption */
.stCaption, .stCaption p{color:#666666 !important}
/* Footer area */
footer, .reportview-container .main footer{color:#666666 !important}
.stApp footer{background:var(--parch) !important;color:#666 !important}
/* General paragraphs — but NOT inside dark boxes */
p:not(.finding-text):not(.signal-val):not(.masthead-title):not(.masthead-sub){color:#333333}
/* Plotly legend text */
.legendtext{fill:#333333 !important}

.masthead{border-top:5px solid var(--navy);padding:28px 0 20px}
.masthead-kicker{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:3px;color:var(--rust);text-transform:uppercase;margin-bottom:8px}
.masthead-title{font-family:'Playfair Display',serif;font-size:44px;font-weight:700;color:var(--navy) !important;line-height:1.1;margin-bottom:6px}
.masthead-sub{font-family:'Playfair Display',serif;font-size:15px;font-style:italic;color:#555 !important;margin-bottom:10px}
.masthead-byline{font-family:'IBM Plex Mono',monospace;font-size:9px;color:#666 !important;letter-spacing:1px}

.signal-panel{border:2px solid var(--navy);background:white;padding:16px 20px;text-align:center;min-height:100px;display:flex;flex-direction:column;justify-content:center}
.signal-label{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:3px;color:#666;text-transform:uppercase;margin-bottom:6px}
.signal-val{font-family:'Playfair Display',serif;font-size:24px;font-weight:700;line-height:1.1;word-break:break-word}
.signal-note{font-family:'IBM Plex Sans',sans-serif;font-size:10px;color:#555;margin-top:5px;line-height:1.4}
.sv-active{color:var(--rust)}
.sv-marginal{color:var(--gold)}
.sv-quiet{color:var(--sage)}
.sv-navy{color:var(--navy)}

.sec-hdr{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:3px;color:var(--rust);text-transform:uppercase;border-bottom:2px solid var(--navy);padding-bottom:5px;margin:24px 0 14px}
.finding-box{background:var(--navy);border-radius:8px;padding:20px 24px;margin:12px 0}
.finding-text{font-family:'Playfair Display',serif;font-size:15px;font-style:italic;color:#FFFFFF !important;line-height:1.65;border-left:3px solid rgba(255,255,255,0.3);padding-left:14px}
.finding-box p, .finding-box span, .finding-box div{color:#FFFFFF !important}

.country-card{background:white;border:1px solid var(--border);border-radius:8px;padding:14px 16px;margin:4px 0}
.country-name{font-family:'IBM Plex Sans',sans-serif;font-size:13px;font-weight:600;color:var(--navy) !important}
.country-cpi{font-family:'Playfair Display',serif;font-size:22px;font-weight:700}
.country-role{font-family:'IBM Plex Mono',monospace;font-size:9px;color:#888 !important;letter-spacing:1px;text-transform:uppercase}

.pair-card{background:white;border-left:3px solid var(--navy);padding:10px 14px;margin:4px 0}
.pair-sig{border-left-color:var(--rust)}
.pair-name{font-size:12px;font-weight:600;color:var(--navy) !important}
.pair-p{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#555 !important}

#MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}
.block-container{padding-top:1rem;max-width:1200px}
.watch-box{border:2px solid var(--rust);background:white;padding:20px 24px;text-align:left}
.watch-label{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:3px;color:var(--rust);text-transform:uppercase;margin-bottom:8px}
.watch-title{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:var(--navy);margin-bottom:6px;line-height:1.2}
.watch-note{font-family:'IBM Plex Sans',sans-serif;font-size:11px;color:#555;line-height:1.5}
.watch-country{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--rust);margin-top:6px}

/* White text inside navy backgrounds */
[style*="background:var(--navy)"] *, [style*="background:#1B2A4A"] *,
.finding-box *, .finding-box p, .finding-box div{color:#FFFFFF !important}
/* Soften all black dataframe backgrounds */
.stDataFrame thead tr th{background-color:var(--navy) !important;color:white !important}
.stDataFrame tbody tr td{background-color:#FAFAF7 !important;color:#333333 !important}
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ──────────────────────────────────────────────────────────────
COUNTRIES = {
    'IND': {'name': 'India',         'role': 'upstream',   'flag': '🇮🇳'},
    'CHN': {'name': 'China',         'role': 'upstream',   'flag': '🇨🇳'},
    'VNM': {'name': 'Vietnam',       'role': 'upstream',   'flag': '🇻🇳'},
    'IDN': {'name': 'Indonesia',     'role': 'upstream',   'flag': '🇮🇩'},
    'THA': {'name': 'Thailand',      'role': 'upstream',   'flag': '🇹🇭'},
    'BRA': {'name': 'Brazil',        'role': 'upstream',   'flag': '🇧🇷'},
    'ZAF': {'name': 'South Africa',  'role': 'upstream',   'flag': '🇿🇦'},
    'MEX': {'name': 'Mexico',        'role': 'upstream',   'flag': '🇲🇽'},
    'SGP': {'name': 'Singapore',     'role': 'relay',      'flag': '🇸🇬'},
    'KOR': {'name': 'South Korea',   'role': 'relay',      'flag': '🇰🇷'},
    'GBR': {'name': 'United Kingdom','role': 'downstream', 'flag': '🇬🇧'},
    'USA': {'name': 'United States', 'role': 'downstream', 'flag': '🇺🇸'},
    'DEU': {'name': 'Germany',       'role': 'downstream', 'flag': '🇩🇪'},
    'FRA': {'name': 'France',        'role': 'downstream', 'flag': '🇫🇷'},
    'JPN': {'name': 'Japan',         'role': 'downstream', 'flag': '🇯🇵'},
}

ROLE_COLORS = {'upstream': '#C0392B', 'relay': '#1B2A4A', 'downstream': '#27AE60'}

@st.cache_data
def load_data():
    # Try loading pre-generated CSVs first
    try:
        cpi     = pd.read_csv('monsoon_data.csv',    index_col=0, parse_dates=True)
        granger = pd.read_csv('monsoon_granger.csv', parse_dates=['date'])
        signal  = pd.read_csv('monsoon_signal.csv',  index_col=0, parse_dates=True)
        # Ensure p_values are proper floats not rounded to 0
        granger['p_value'] = granger['p_value'].clip(lower=0.0001)
        return cpi, granger, signal
    except FileNotFoundError:
        st.error("Data files not found. Upload monsoon_data.csv, monsoon_granger.csv, monsoon_signal.csv to your GitHub repo.")
        st.stop()

cpi, granger, signal = load_data()

latest_date   = cpi.index[-1]
latest_cpi    = cpi.iloc[-1]
latest_signal = signal.iloc[-1]
latest_regime = latest_signal['regime']

# India→Singapore latest p-value
ind_sg = granger[(granger['cause']=='IND') & (granger['effect']=='SGP')]
ind_sg_p = ind_sg.iloc[-1]['p_value'] if len(ind_sg) > 0 else np.nan

regime_class = {'ACTIVE': 'sv-active', 'MARGINAL': 'sv-marginal', 'QUIET': 'sv-quiet'}[latest_regime]
regime_note  = {
    'ACTIVE':   'Upstream EM pressure is elevated and transmitting. Watch downstream CPI.',
    'MARGINAL': 'Transmission signals present but not dominant. Monitor closely.',
    'QUIET':    'No significant upstream transmission detected. Cycles appear decoupled.',
}[latest_regime]

FONT = dict(family="IBM Plex Sans", size=12, color="#1B2A4A")
LAYOUT = dict(
    plot_bgcolor="white", paper_bgcolor="#FAF6F0",
    font=FONT, hovermode="x unified"
)

# ── MASTHEAD ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="masthead">
  <div class="masthead-kicker">Live Research Tool · Gokhale (2026)</div>
  <div class="masthead-title">🌧️ The Monsoon Index</div>
  <div class="masthead-sub">Global Inflation Transmission Tracker — Where Is the Next Surge Coming From?</div>
  <div class="masthead-byline">
    ssrn.com/abstract=6514338 &nbsp;·&nbsp;
    Rolling VAR(4) Granger causality &nbsp;·&nbsp;
    15 economies &nbsp;·&nbsp;
    Data through {latest_date.strftime('%B %Y')}
  </div>
</div>
""", unsafe_allow_html=True)

# ── SIGNAL PANELS ─────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    regime_short = {
    'ACTIVE':   'Upstream pressure transmitting downstream.',
    'MARGINAL': 'Transmission present, not dominant.',
    'QUIET':    'No significant transmission detected.',
}[latest_regime]
st.markdown(f"""<div class="signal-panel">
      <div class="signal-label">Monsoon Regime</div>
      <div class="signal-val {regime_class}">{latest_regime}</div>
      <div class="signal-note">{regime_short}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    ind_cpi = latest_cpi.get('IND', np.nan)
    ind_col = "sv-active" if ind_cpi > 5 else "sv-marginal" if ind_cpi > 3 else "sv-quiet"
    st.markdown(f"""<div class="signal-panel">
      <div class="signal-label">🇮🇳 India CPI</div>
      <div class="signal-val {ind_col}">{ind_cpi:.1f}%</div>
      <div class="signal-note">Upstream driver</div>
    </div>""", unsafe_allow_html=True)
with c3:
    sg_cpi = latest_cpi.get('SGP', np.nan)
    sg_col = "sv-active" if sg_cpi > 4 else "sv-marginal" if sg_cpi > 2 else "sv-quiet"
    st.markdown(f"""<div class="signal-panel">
      <div class="signal-label">🇸🇬 Singapore CPI</div>
      <div class="signal-val {sg_col}">{sg_cpi:.1f}%</div>
      <div class="signal-note">Transmission relay</div>
    </div>""", unsafe_allow_html=True)
with c4:
    em_gap = latest_signal.get('em_dm_gap', np.nan)
    gap_col = "sv-active" if em_gap > 2 else "sv-marginal" if em_gap > 0 else "sv-quiet"
    st.markdown(f"""<div class="signal-panel">
      <div class="signal-label">EM–DM Gap</div>
      <div class="signal-val {gap_col}">{em_gap:+.1f}pp</div>
      <div class="signal-note">Upstream pressure gauge</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown(f"""<div class="signal-panel">
      <div class="signal-label">India→SG p-value</div>
      <div class="signal-val sv-navy">p = {ind_sg_p:.3f}</div>
      <div class="signal-note">Gokhale (2026): p=0.028</div>
    </div>""", unsafe_allow_html=True)


# ── NEXT SURGE WATCH ─────────────────────────────────────────────────────────
# Find upstream countries with elevated CPI AND active transmission signals
em_countries = [c for c, v in COUNTRIES.items() if v['role'] == 'upstream']
dm_avg_now   = np.mean([latest_cpi.get(c, 0)
                        for c, v in COUNTRIES.items() if v['role'] == 'downstream'])

# Score each upstream country: CPI above DM avg + significant outbound transmission
watch_scores = []
for em in em_countries:
    em_cpi = latest_cpi.get(em, 0)
    if np.isnan(em_cpi):
        continue
    # Count significant outbound pairs
    outbound = granger.sort_values('date').groupby(['cause','effect']).last().reset_index()
    sig_out  = outbound[(outbound['cause']==em) & (outbound['p_value']<0.05)]
    score    = (em_cpi - dm_avg_now) + len(sig_out) * 0.5
    if em_cpi > dm_avg_now:
        watch_scores.append((em, em_cpi, len(sig_out), score))

watch_scores.sort(key=lambda x: -x[3])
top_watch = watch_scores[:3]

if top_watch:
    watch_countries = ', '.join(
        f"{COUNTRIES[c]['flag']} {COUNTRIES[c]['name']} ({cpi:.1f}%)"
        for c, cpi, _, _ in top_watch
    )
    top_name  = COUNTRIES[top_watch[0][0]]['name']
    top_cpi   = top_watch[0][1]
    top_sigs  = top_watch[0][2]
    watch_msg = (
        f"{top_name} leads the watch list at {top_cpi:.1f}% with "
        f"{top_sigs} active downstream transmission pair{'s' if top_sigs != 1 else ''}. "
        f"{'Downstream CPI pressure expected in 2–3 months.' if top_sigs > 0 else 'Monitor for emerging transmission.'}"
    )
else:
    watch_countries = "No upstream economies elevated above DM average"
    watch_msg = "All upstream economies currently tracking below or near DM inflation levels. Surge risk is low."

# Next Surge Watch box — full width below panels
st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
st.markdown(f"""<div class="watch-box">
  <div class="watch-label">🌧️ Next Surge Watch — Answering the Question Above</div>
  <div class="watch-title">{watch_msg}</div>
  <div class="watch-country">Elevated upstream economies: {watch_countries}</div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
# ── NEXT SURGE WATCH ─────────────────────────────────────────────────────────
# Find upstream countries with elevated CPI AND active transmission signals
em_countries = [c for c, v in COUNTRIES.items() if v['role'] == 'upstream']
dm_avg_now   = np.mean([latest_cpi.get(c, 0)
                        for c, v in COUNTRIES.items() if v['role'] == 'downstream'])

# Score each upstream country: CPI above DM avg + significant outbound transmission
watch_scores = []
for em in em_countries:
    em_cpi = latest_cpi.get(em, 0)
    if np.isnan(em_cpi):
        continue
    # Count significant outbound pairs
    outbound = granger.sort_values('date').groupby(['cause','effect']).last().reset_index()
    sig_out  = outbound[(outbound['cause']==em) & (outbound['p_value']<0.05)]
    score    = (em_cpi - dm_avg_now) + len(sig_out) * 0.5
    if em_cpi > dm_avg_now:
        watch_scores.append((em, em_cpi, len(sig_out), score))

watch_scores.sort(key=lambda x: -x[3])
top_watch = watch_scores[:3]

if top_watch:
    watch_countries = ', '.join(
        f"{COUNTRIES[c]['flag']} {COUNTRIES[c]['name']} ({cpi:.1f}%)"
        for c, cpi, _, _ in top_watch
    )
    top_name  = COUNTRIES[top_watch[0][0]]['name']
    top_cpi   = top_watch[0][1]
    top_sigs  = top_watch[0][2]
    watch_msg = (
        f"{top_name} leads the watch list at {top_cpi:.1f}% with "
        f"{top_sigs} active downstream transmission pair{'s' if top_sigs != 1 else ''}. "
        f"{'Downstream CPI pressure expected in 2–3 months.' if top_sigs > 0 else 'Monitor for emerging transmission.'}"
    )
else:
    watch_countries = "No upstream economies elevated above DM average"
    watch_msg = "All upstream economies currently tracking below or near DM inflation levels. Surge risk is low."

t1, t2, t3, t4, t5 = st.tabs([
    "🗺️ Transmission Map",
    "📈 CPI Trajectories",
    "🌧️ Monsoon Signal",
    "🔍 Country Deep Dive",
    "📑 Methodology"
])

# ── TAB 1: TRANSMISSION MAP ───────────────────────────────────────────────────
with t1:
    st.markdown('<div class="sec-hdr">Live Global Inflation Transmission Map</div>',
                unsafe_allow_html=True)

    st.markdown("""<div class="finding-box"><div class="finding-text">
        "Dark crimson (thick) = highly significant (p &lt; 0.01). Coral red (medium) = significant (p &lt; 0.05).
        Dashed orange = marginal (p &lt; 0.10). Use the slider to adjust the threshold.
        Based on Gokhale (2026): India → Singapore → UK is the documented core chain."
    </div></div>""", unsafe_allow_html=True)

    sig_threshold = st.select_slider(
        "Map significance threshold",
        options=[0.001, 0.005, 0.01, 0.025, 0.05],
        value=0.005,
        format_func=lambda x: f"p < {x}"
    )

    # Get latest p-value matrix
    latest_g = granger.sort_values('date').groupby(
        ['cause','effect']).last().reset_index()

    # Network layout — position countries by role
    positions = {
        # Upstream (left cluster)
        'IND': (-2.5,  0.8), 'CHN': (-2.5, -0.8),
        'BRA': (-3.2,  1.8), 'ZAF': (-3.2, -1.8),
        'IDN': (-1.8,  2.0), 'VNM': (-1.8, -2.0),
        'THA': (-3.0,  0.0), 'MEX': (-3.8,  0.0),
        # Relay (middle)
        'SGP': ( 0.0,  0.8), 'KOR': ( 0.0, -0.8),
        # Downstream (right cluster)
        'GBR': ( 2.5,  1.5), 'USA': ( 2.5,  0.5),
        'DEU': ( 2.5, -0.5), 'FRA': ( 2.5, -1.5),
        'JPN': ( 3.2,  0.0),
    }

    fig_map = go.Figure()

    # Draw edges for significant pairs — cap at top 20 pairs by p-value
    sig_pairs = latest_g[latest_g['p_value'] < sig_threshold]
    for _, row in sig_pairs.iterrows():
        c, e = row['cause'], row['effect']
        if c not in positions or e not in positions:
            continue
        x0, y0 = positions[c]
        x1, y1 = positions[e]
        alpha  = max(0.15, 1 - row['p_value'] * 10)
        width  = max(0.5, (1 - row['p_value']) * 4)
        color  = f"rgba(196,82,46,{alpha:.2f})"

        # Arrow midpoint
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2

        fig_map.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(color=color, width=width),
            hovertemplate=f"{COUNTRIES[c]['name']} → {COUNTRIES[e]['name']}<br>"
                          f"p = {row['p_value']:.3f}<extra></extra>",
            showlegend=False
        ))

    # Draw marginal edges (0.05 < p < 0.10)
    marg_pairs = latest_g[(latest_g['p_value'] >= 0.05) & (latest_g['p_value'] < 0.10)]
    for _, row in marg_pairs.iterrows():
        c, e = row['cause'], row['effect']
        if c not in positions or e not in positions:
            continue
        x0, y0 = positions[c]
        x1, y1 = positions[e]
        fig_map.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(color="rgba(196,122,0,0.55)", width=1.2, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Draw nodes
    for code, info in COUNTRIES.items():
        if code not in positions:
            continue
        x, y  = positions[code]
        role  = info['role']
        color = ROLE_COLORS[role]
        cpi_val = latest_cpi.get(code, np.nan)
        size  = 20 + (cpi_val * 2 if not np.isnan(cpi_val) else 10)
        size  = min(max(size, 16), 45)

        fig_map.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=size, color=color,
                line=dict(color='white', width=2)
            ),
            text=[f"{info['flag']}<br>{code}"],
            textposition='bottom center',
            textfont=dict(size=9, color='#1B2A4A'),
            hovertemplate=(
                f"<b>{info['flag']} {info['name']}</b><br>"
                f"CPI: {cpi_val:.1f}%<br>"
                f"Role: {role}<extra></extra>"
            ),
            showlegend=False
        ))

    # Role labels
    for label, x, color in [
        ("← UPSTREAM", -3.0, "#C0392B"),
        ("RELAY →", 0.0, "#1B2A4A"),
        ("← DOWNSTREAM", 2.8, "#27AE60")
    ]:
        fig_map.add_annotation(
            x=x, y=2.8, text=label, showarrow=False,
            font=dict(size=9, color=color, family='IBM Plex Mono'),
            xanchor='center'
        )

    fig_map.update_layout(
        **LAYOUT,
        paper_bgcolor="#F3EDE3",
        plot_bgcolor="#F3EDE3",
        height=520,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                   range=[-4.5, 4.0]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                   range=[-3.0, 3.2]),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.caption(
        "Node size = current CPI level. Red edges = significant transmission (p<0.05). "
        "Dashed gold = marginal (p<0.10). Rolling 36-month window."
    )

    # Significant pairs table
    st.markdown('<div class="sec-hdr">Active Transmission Pairs (p < 0.05)</div>',
                unsafe_allow_html=True)

    # Show all significant pairs in table but sorted by p-value
    sig_display = latest_g[latest_g['p_value'] < sig_threshold].nsmallest(30, 'p_value').copy()
    sig_display['Cause'] = sig_display['cause'].map(
        lambda x: f"{COUNTRIES[x]['flag']} {COUNTRIES[x]['name']}" if x in COUNTRIES else x)
    sig_display['Effect'] = sig_display['effect'].map(
        lambda x: f"{COUNTRIES[x]['flag']} {COUNTRIES[x]['name']}" if x in COUNTRIES else x)
    sig_display['p-value'] = sig_display['p_value'].apply(lambda x: f'{x:.4f}')
    sig_display['Lag (M)'] = sig_display['lag']
    sig_display['Direction'] = sig_display['cause'].map(
        lambda x: COUNTRIES[x]['role'] if x in COUNTRIES else '') + ' → ' + \
        sig_display['effect'].map(
        lambda x: COUNTRIES[x]['role'] if x in COUNTRIES else '')

    st.dataframe(
        sig_display[['Cause','Effect','p-value','Lag (M)','Direction']]
        .sort_values('p-value')
        .style
        .set_properties(**{'background-color': '#FAF6F0', 'color': '#333333'})
        .set_table_styles([
            {'selector': 'thead tr th',
             'props': [('background-color', '#1B2A4A'),
                       ('color', 'white'),
                       ('font-family', 'IBM Plex Mono'),
                       ('font-size', '11px')]},
            {'selector': 'tbody tr:nth-child(even) td',
             'props': [('background-color', '#F3EDE3')]},
            {'selector': 'tbody tr:nth-child(odd) td',
             'props': [('background-color', '#FAF6F0')]},
            {'selector': 'td',
             'props': [('color', '#333333'),
                       ('font-family', 'IBM Plex Sans'),
                       ('font-size', '12px'),
                       ('border-color', '#D4C4A8')]},
        ]),
        use_container_width=True,
        hide_index=True
    )

# ── TAB 2: CPI TRAJECTORIES ───────────────────────────────────────────────────
with t2:
    st.markdown('<div class="sec-hdr">Consumer Price Index — All 15 Economies</div>',
                unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 3])
    with col_left:
        st.markdown("**Filter by role:**")
        show_upstream   = st.checkbox("Upstream EM", True)
        show_relay      = st.checkbox("Relay", True)
        show_downstream = st.checkbox("Downstream DM", True)

        selected = [c for c, v in COUNTRIES.items()
                    if (v['role']=='upstream'   and show_upstream)
                    or (v['role']=='relay'       and show_relay)
                    or (v['role']=='downstream'  and show_downstream)]

        yr_start = st.select_slider(
            "Start date",
            options=cpi.index.strftime("%Y-%m").tolist(),
            value=cpi.index.strftime("%Y-%m").tolist()[0],
            label_visibility="collapsed"
        )

    with col_right:
        df_plot = cpi.loc[yr_start:][selected]
        fig2 = go.Figure()

        for code in selected:
            if code not in df_plot.columns:
                continue
            info  = COUNTRIES[code]
            color = ROLE_COLORS[info['role']]
            dash  = 'solid' if info['role'] != 'downstream' else 'dash'

            fig2.add_trace(go.Scatter(
                x=df_plot.index.strftime("%Y-%m-%d"),
                y=df_plot[code],
                name=f"{info['flag']} {info['name']}",
                line=dict(color=color, width=2, dash=dash),
                opacity=0.85,
                hovertemplate=f"<b>{info['name']}</b><br>%{{x|%b %Y}}: %{{y:.1f}}%<extra></extra>"
            ))

        # MAS tightening verticals
        for d in ["2021-10-01","2022-01-01","2022-04-01","2022-07-01","2022-10-01"]:
            if d[:7] >= yr_start:
                fig2.add_vline(x=d, line=dict(color="#1B2A4A", width=1, dash="dot"))

        fig2.add_annotation(
            x="2022-04-01", y=1.05, yref="paper",
            text="MAS tightening cycle", showarrow=False,
            font=dict(size=9, color="#1B2A4A"), xanchor="center"
        )
        fig2.update_layout(
            **LAYOUT, height=420,
            margin=dict(l=0, r=0, t=30, b=60),
            yaxis=dict(title="CPI YoY (%)", gridcolor="#EEEEEE",
                       zeroline=True, zerolinecolor="#CCCCCC",
                       tickfont=dict(color="#1B2A4A")),
            xaxis=dict(gridcolor="#EEEEEE", tickfont=dict(color="#1B2A4A")),
            legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center",
                        bgcolor="rgba(0,0,0,0)", font=dict(size=10, color='#333333'))
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Current CPI snapshot
    st.markdown('<div class="sec-hdr">Current CPI Snapshot</div>',
                unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (code, info) in enumerate(COUNTRIES.items()):
        with cols[i % 5]:
            val   = latest_cpi.get(code, np.nan)
            color = ROLE_COLORS[info['role']]
            trend = "↑" if val > 3 else ("→" if val > 1.5 else "↓")
            st.markdown(f"""<div class="country-card">
              <div class="country-role">{info['role']}</div>
              <div class="country-name">{info['flag']} {info['name']}</div>
              <div class="country-cpi" style="color:{color}">{val:.1f}% {trend}</div>
            </div>""", unsafe_allow_html=True)

# ── TAB 3: MONSOON SIGNAL ─────────────────────────────────────────────────────
with t3:
    st.markdown('<div class="sec-hdr">Monsoon Index — Rolling Transmission Signal</div>',
                unsafe_allow_html=True)

    st.markdown("""<div class="finding-box"><div class="finding-text">
        "The Monsoon Index is a composite signal tracking whether upstream emerging market
        supply dynamics are currently transmitting to advanced economy inflation. When the
        signal is ACTIVE, history suggests downstream CPI will follow in 2-3 months.
        Named for India's monsoon cycles, the original upstream driver in Gokhale (2026)."
    </div></div>""", unsafe_allow_html=True)

    # Regime over time
    regime_colors = {'ACTIVE': '#C0392B', 'MARGINAL': '#b8860b', 'QUIET': '#4a6741'}
    signal_plot = signal.copy()

    fig3 = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.4, 0.35, 0.25],
        subplot_titles=("EM–DM Inflation Gap (Upstream Pressure)",
                        "India → Singapore Rolling p-value",
                        "Monsoon Regime")
    )

    # Panel 1: EM-DM gap
    fig3.add_trace(go.Scatter(
        x=signal_plot.index.strftime("%Y-%m-%d"),
        y=signal_plot['em_dm_gap'],
        name="EM-DM gap",
        line=dict(color="#C0392B", width=2),
        fill="tozeroy",
        fillcolor="rgba(192,57,43,0.08)",
        hovertemplate="%{x|%b %Y}: %{y:+.1f}pp<extra>EM-DM Gap</extra>"
    ), row=1, col=1)
    fig3.add_hline(y=0, line=dict(color="#CCCCCC", width=1), row=1, col=1)
    fig3.add_hline(y=1.5, line=dict(color="#C0392B", width=1, dash="dot"), row=1, col=1)

    # Panel 2: India→SG rolling p-value
    ind_sg_rolling = granger[
        (granger['cause']=='IND') & (granger['effect']=='SGP')
    ].set_index('date').sort_index()

    fig3.add_hrect(
        y0=0, y1=0.05, row=2, col=1,
        fillcolor="rgba(192,57,43,0.06)", line_width=0,
        annotation_text="Significant (p<0.05)",
        annotation_position="right",
        annotation_font_size=9,
        annotation_font_color="#C0392B"
    )
    fig3.add_trace(go.Scatter(
        x=ind_sg_rolling.index.strftime("%Y-%m-%d"),
        y=ind_sg_rolling['p_value'],
        name="India→SG p-value",
        line=dict(color="#1B2A4A", width=2),
        fill="tozeroy",
        fillcolor="rgba(27,42,74,0.07)",
        hovertemplate="%{x|%b %Y}: p=%{y:.3f}<extra>India→Singapore</extra>"
    ), row=2, col=1)
    fig3.add_hline(
        y=0.05, line=dict(color="#C0392B", width=1.5, dash="dash"),
        row=2, col=1
    )

    # Panel 3: Regime bar
    regime_num = signal_plot['regime'].map(
        {'ACTIVE': 1, 'MARGINAL': 0.5, 'QUIET': 0}
    )
    regime_color_list = signal_plot['regime'].map(regime_colors).tolist()

    fig3.add_trace(go.Bar(
        x=signal_plot.index.strftime("%Y-%m-%d"),
        y=regime_num,
        name="Regime",
        marker_color=regime_color_list,
        hovertemplate="%{x|%b %Y}: %{customdata}<extra></extra>",
        customdata=signal_plot['regime']
    ), row=3, col=1)

    fig3.update_layout(
        **LAYOUT, height=600,
        margin=dict(l=0, r=80, t=40, b=40),
        showlegend=False
    )
    fig3.update_yaxes(gridcolor="#EEEEEE", tickfont=dict(color="#1B2A4A"))
    fig3.update_xaxes(gridcolor="#EEEEEE", tickfont=dict(color="#1B2A4A"))
    fig3.update_annotations(font=dict(color="#1B2A4A", size=11))

    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "EM-DM gap = average EM CPI minus average DM CPI. "
        "Above red dotted line (+1.5pp) = elevated upstream pressure. "
        "Rolling 36-month window for p-value calculation."
    )

    # Regime history summary
    st.markdown('<div class="sec-hdr">Regime History</div>', unsafe_allow_html=True)
    regime_counts = signal_plot['regime'].value_counts()
    c1, c2, c3 = st.columns(3)
    for col, regime, color in [
        (c1, 'ACTIVE', '#C0392B'),
        (c2, 'MARGINAL', '#b8860b'),
        (c3, 'QUIET', '#4a6741')
    ]:
        count = regime_counts.get(regime, 0)
        pct   = count / len(signal_plot) * 100 if len(signal_plot) > 0 else 0
        with col:
            st.markdown(f"""<div class="signal-panel">
              <div class="signal-label">{regime}</div>
              <div class="signal-val" style="color:{color}">{count} months</div>
              <div class="signal-note">{pct:.0f}% of sample period</div>
            </div>""", unsafe_allow_html=True)

# ── TAB 4: COUNTRY DEEP DIVE ──────────────────────────────────────────────────
with t4:
    st.markdown('<div class="sec-hdr">Country Deep Dive — Full Transmission Profile</div>',
                unsafe_allow_html=True)

    col_sel, col_main = st.columns([1, 3])
    with col_sel:
        focus = st.selectbox(
            "Select country",
            options=list(COUNTRIES.keys()),
            format_func=lambda x: f"{COUNTRIES[x]['flag']} {COUNTRIES[x]['name']}",
            index=list(COUNTRIES.keys()).index('IND')
        )

        info  = COUNTRIES[focus]
        val   = latest_cpi.get(focus, np.nan)
        color = ROLE_COLORS[info['role']]

        st.markdown(f"""<div class="signal-panel" style="margin-top:12px">
          <div class="signal-label">{info['role']}</div>
          <div class="signal-val" style="color:{color}">{val:.1f}%</div>
          <div class="signal-note">{info['flag']} {info['name']} CPI</div>
        </div>""", unsafe_allow_html=True)

        # Countries this one causes
        st.markdown("**Granger-causes (p<0.05):**")
        causes = granger.sort_values('date').groupby(
            ['cause','effect']).last().reset_index()
        outbound = causes[
            (causes['cause']==focus) & (causes['p_value']<0.05)
        ].sort_values('p_value')

        if len(outbound) > 0:
            for _, row in outbound.iterrows():
                e    = row['effect']
                ename = COUNTRIES[e]['name'] if e in COUNTRIES else e
                eflag = COUNTRIES[e]['flag'] if e in COUNTRIES else ''
                st.markdown(f"""<div class="pair-card pair-sig">
                  <div class="pair-name">{eflag} {ename}</div>
                  <div class="pair-p">p = {row['p_value']:.3f} · lag {row['lag']}M</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("No significant outbound transmission")

        # Countries causing this one
        st.markdown("**Caused by (p<0.05):**")
        inbound = causes[
            (causes['effect']==focus) & (causes['p_value']<0.05)
        ].sort_values('p_value')

        if len(inbound) > 0:
            for _, row in inbound.iterrows():
                c    = row['cause']
                cname = COUNTRIES[c]['name'] if c in COUNTRIES else c
                cflag = COUNTRIES[c]['flag'] if c in COUNTRIES else ''
                st.markdown(f"""<div class="pair-card">
                  <div class="pair-name">{cflag} {cname}</div>
                  <div class="pair-p">p = {row['p_value']:.3f} · lag {row['lag']}M</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("No significant inbound transmission")

    with col_main:
        # CPI trajectory
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=cpi.index.strftime("%Y-%m-%d"),
            y=cpi[focus] if focus in cpi.columns else [],
            name=f"{info['name']} CPI",
            line=dict(color=color, width=2.5),
            hovertemplate=f"<b>{info['name']}</b><br>%{{x|%b %Y}}: %{{y:.1f}}%<extra></extra>"
        ))

        # Overlay key comparison countries
        compare = {'IND': ('India', '#C0392B'), 'SGP': ('Singapore', '#1B2A4A'),
                   'GBR': ('UK', '#27AE60')}
        for code, (name, col2) in compare.items():
            if code != focus and code in cpi.columns:
                fig4.add_trace(go.Scatter(
                    x=cpi.index.strftime("%Y-%m-%d"),
                    y=cpi[code],
                    name=name,
                    line=dict(color=col2, width=1.2, dash='dot'),
                    opacity=0.5,
                    hovertemplate=f"<b>{name}</b><br>%{{x|%b %Y}}: %{{y:.1f}}%<extra></extra>"
                ))

        fig4.update_layout(
            **LAYOUT, height=250,
            margin=dict(l=0, r=0, t=20, b=40),
            yaxis=dict(title="CPI YoY (%)", gridcolor="#EEEEEE",
                       tickfont=dict(color="#1B2A4A")),
            xaxis=dict(gridcolor="#EEEEEE", tickfont=dict(color="#1B2A4A")),
            legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center",
                        bgcolor="rgba(0,0,0,0)", font=dict(size=10))
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Rolling p-value for focus → Singapore and India → focus
        fig5 = make_subplots(rows=1, cols=2,
            subplot_titles=(
                f"{info['name']} → Singapore (rolling p-value)",
                f"India → {info['name']} (rolling p-value)"
            ))

        for col_idx, (cause, effect) in enumerate([
            (focus, 'SGP'), ('IND', focus)
        ]):
            sub = granger[
                (granger['cause']==cause) & (granger['effect']==effect)
            ].set_index('date').sort_index()

            if len(sub) > 0:
                fig5.add_hrect(
                    y0=0, y1=0.05, row=1, col=col_idx+1,
                    fillcolor="rgba(192,57,43,0.06)", line_width=0
                )
                fig5.add_trace(go.Scatter(
                    x=sub.index.strftime("%Y-%m-%d"),
                    y=sub['p_value'],
                    line=dict(color="#1B2A4A", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(27,42,74,0.07)",
                    showlegend=False,
                    hovertemplate="%{x|%b %Y}: p=%{y:.3f}<extra></extra>"
                ), row=1, col=col_idx+1)
                fig5.add_hline(
                    y=0.05,
                    line=dict(color="#C0392B", width=1.5, dash="dash"),
                    row=1, col=col_idx+1
                )

        fig5.update_layout(
            **LAYOUT, height=220,
            margin=dict(l=0, r=80, t=30, b=20),
            showlegend=False
        )
        fig5.update_yaxes(gridcolor="#EEEEEE", range=[0, 0.6],
                          tickfont=dict(color="#1B2A4A"))
        fig5.update_xaxes(gridcolor="#EEEEEE", tickfont=dict(color="#1B2A4A"))
        fig5.update_annotations(font=dict(color="#1B2A4A", size=10))
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("Below red dashed line = statistically significant Granger causality (p<0.05). Rolling 36-month window.")

# ── TAB 5: METHODOLOGY ────────────────────────────────────────────────────────
with t5:
    st.markdown('<div class="sec-hdr">Research Basis</div>', unsafe_allow_html=True)
    st.markdown("""
**Gokhale, Anuja A. (2026). "Cross-Country Macroeconomic Dynamics: Inflation, Growth,
and Monetary Policy — India, Singapore, and the United Kingdom." SSRN Working Paper.**

[ssrn.com/abstract=6514338](https://ssrn.com/abstract=6514338)

This dashboard is the live, global-scale implementation of the paper's core empirical framework,
extended to 15 economies across three roles: upstream EM supply originators, relay small open
economies, and downstream advanced economy recipients.
    """)

    st.markdown('<div class="sec-hdr">Methodology</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
**Data**
- World Bank annual CPI YoY% (via GitHub datasets API)
- Cubic spline interpolation to monthly frequency
- FRED monthly data where API key provided
- 15 economies, Jan 2012 – present

**Rolling Granger Causality**
- 36-month rolling window, updated monthly
- VAR lag length: 1–4 quarters (best p-value)
- Significance threshold: p < 0.05
- 210 country pairs computed simultaneously
        """)
    with c2:
        st.markdown("""
**Monsoon Index Construction**
- EM-DM gap: average EM CPI minus average DM CPI
- Key pair p-values: IND→SGP, IND→GBR, SGP→GBR, CHN→KOR, CHN→DEU
- Regime: ACTIVE (min_p<0.05 AND gap>1.5pp), MARGINAL (p<0.10), QUIET (otherwise)

**Core Finding (Gokhale 2026)**
- India Granger-causes Singapore: p=0.028, lag 2M
- Singapore Granger-causes UK: p=0.039
- Neither reverse direction significant
- S$NEER framework outperformed rate-based frameworks in 2022
        """)

    st.markdown('<div class="sec-hdr">Country Classification</div>', unsafe_allow_html=True)
    roles_df = pd.DataFrame([
        {'Country': f"{v['flag']} {v['name']}", 'Role': v['role'].title(),
         'Rationale': {
             'upstream':   'EM commodity/food supplier — originates supply shocks',
             'relay':      'Small open economy — transmits upstream pressure downstream',
             'downstream': 'Advanced economy — receives transmitted inflation'
         }[v['role']]}
        for v in COUNTRIES.values()
    ])
    st.dataframe(
        roles_df
        .style
        .set_properties(**{'background-color': '#FAF6F0', 'color': '#333333'})
        .set_table_styles([
            {'selector': 'thead tr th',
             'props': [('background-color', '#1B2A4A'),
                       ('color', 'white'),
                       ('font-family', 'IBM Plex Mono'),
                       ('font-size', '11px')]},
            {'selector': 'tbody tr:nth-child(even) td',
             'props': [('background-color', '#F3EDE3')]},
            {'selector': 'tbody tr:nth-child(odd) td',
             'props': [('background-color', '#FAF6F0')]},
            {'selector': 'td',
             'props': [('color', '#333333'),
                       ('font-family', 'IBM Plex Sans'),
                       ('font-size', '12px'),
                       ('border-color', '#D4C4A8')]},
        ]),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.caption(
        "Built by Anuja A. Gokhale · MA Applied Economics, NUS · Merit Scholar · "
        "anujagokhale1604@gmail.com · ssrn.com/abstract=6514338"
    )
