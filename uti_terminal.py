import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="UTI AMC · Institutional Terminal",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --bg:          #0f1117;
  --bg2:         #13161f;
  --glass:       rgba(255,255,255,0.07);
  --glass-hover: rgba(255,255,255,0.11);
  --border:      rgba(255,255,255,0.10);
  --shine:       rgba(255,255,255,0.22);
  --gold:        #e8c97a;
  --gold-dim:    rgba(232,201,122,0.15);
  --gold-border: rgba(232,201,122,0.30);
  --red:         #e05c5c;
  --red-dim:     rgba(224,92,92,0.12);
  --red-border:  rgba(224,92,92,0.28);
  --blue:        #5b9cf6;
  --teal:        #4ecdc4;
  --green:       #52e0a0;
  --t1:          #f0f0f0;
  --t2:          #9ca3af;
  --t3:          #6b7280;
  --mono:        'JetBrains Mono', monospace;
  --sans:        'Sora', sans-serif;
}

html, body, [class*="css"], .stApp {
  font-family: var(--sans);
  background: var(--bg);
  color: var(--t1);
}

/* Animated mesh background */
.stApp {
  background:
    radial-gradient(ellipse 90% 60% at 10% 5%,  rgba(91,156,246,0.09) 0%, transparent 55%),
    radial-gradient(ellipse 70% 50% at 90% 90%, rgba(78,205,196,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 50% 40% at 50% 50%, rgba(232,201,122,0.04) 0%, transparent 60%),
    #0f1117;
}

/* ─── GLASS CARD ──────────────────────────────────── */
.g-card {
  background: var(--glass);
  backdrop-filter: blur(32px) saturate(200%);
  -webkit-backdrop-filter: blur(32px) saturate(200%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 22px 26px;
  margin-bottom: 14px;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.04) inset,
    0 8px 40px rgba(0,0,0,0.45),
    0 1px 0 var(--shine) inset;
}
.g-card::before {
  content: '';
  position: absolute; top: 0; left: 8%; right: 8%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.30) 50%, transparent);
}
.g-card::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 50%);
  pointer-events: none;
}

/* ─── HEADER ──────────────────────────────────────── */
.hdr {
  background: linear-gradient(130deg,
    rgba(91,156,246,0.16) 0%,
    rgba(255,255,255,0.07) 40%,
    rgba(232,201,122,0.08) 100%);
  backdrop-filter: blur(48px) saturate(220%);
  -webkit-backdrop-filter: blur(48px) saturate(220%);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 24px;
  padding: 28px 36px;
  margin-bottom: 18px;
  position: relative; overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.05) inset,
    0 20px 60px rgba(0,0,0,0.50),
    0 1px 0 rgba(255,255,255,0.18) inset;
}
.hdr::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg,
    transparent 0%, rgba(255,255,255,0.35) 35%,
    rgba(232,201,122,0.50) 50%,
    rgba(255,255,255,0.35) 65%, transparent 100%);
}
.hdr::after {
  content: ''; position: absolute;
  top: -80px; right: -60px;
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(232,201,122,0.10) 0%, transparent 65%);
  pointer-events: none;
}

.t-main { font-family: var(--sans); font-weight:700; font-size:27px;
  letter-spacing:-0.5px; color:var(--t1); margin:0 0 3px 0; }
.t-sub  { font-family: var(--mono); font-size:10px; color:var(--t3);
  letter-spacing:2.5px; text-transform:uppercase; margin:0 0 14px 0; }
.price  { font-family: var(--mono); font-size:42px; font-weight:500;
  color:var(--gold); letter-spacing:-1.5px; line-height:1; }
.price-lbl { font-family:var(--mono); font-size:9px; color:var(--t3);
  letter-spacing:2px; text-transform:uppercase; margin-top:4px; }

/* ─── PILLS ───────────────────────────────────────── */
.pill {
  display:inline-block;
  background:rgba(255,255,255,0.07); border:1px solid var(--border);
  border-radius:100px; padding:3px 12px;
  font-family:var(--mono); font-size:9.5px; color:var(--t2);
  margin-right:5px; margin-top:4px;
}
.pill-g { background:rgba(232,201,122,0.12); border-color:var(--gold-border); color:var(--gold); }
.pill-r { background:var(--red-dim); border-color:var(--red-border); color:var(--red); }
.pill-b { background:rgba(91,156,246,0.12); border-color:rgba(91,156,246,0.28); color:var(--blue); }

/* ─── KPI CARDS ───────────────────────────────────── */
.kpi {
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
  border: 1px solid var(--border);
  border-radius: 16px; padding:16px 14px; text-align:center;
  position:relative; overflow:hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.35), 0 1px 0 var(--shine) inset;
}
.kpi::before {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.22),transparent);
}
.kpi-v { font-family:var(--mono); font-size:18px; font-weight:500; color:var(--t1); }
.kpi-l { font-size:9.5px; color:var(--t3); text-transform:uppercase;
  letter-spacing:1.2px; margin-top:5px; }
.kpi-d { font-family:var(--mono); font-size:10px; color:var(--gold); margin-top:3px; }

/* ─── SECTION LABEL ───────────────────────────────── */
.slbl {
  font-family:var(--mono); font-size:9.5px; letter-spacing:3px;
  color:var(--t3); text-transform:uppercase; padding:18px 0 8px 0;
}

/* ─── PILL TABS ───────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.05) !important;
  backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.09) !important;
  border-radius: 100px !important;
  padding: 5px 6px !important;
  gap: 2px !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.40), 0 1px 0 rgba(255,255,255,0.10) inset !important;
  width: fit-content !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 100px !important;
  color: var(--t3) !important;
  font-size: 11.5px !important;
  font-family: var(--sans) !important;
  font-weight: 500 !important;
  padding: 7px 20px !important;
  border: none !important;
  transition: all 0.18s ease !important;
  white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(232,201,122,0.25), rgba(232,201,122,0.12)) !important;
  color: var(--gold) !important;
  border: 1px solid var(--gold-border) !important;
  box-shadow: 0 2px 12px rgba(232,201,122,0.20) !important;
}

/* ─── OVERRIDE STREAMLIT WIDGET TEXT ──────────────── */
/* Make ALL streamlit labels/text visible on dark bg */
label, .stSlider label, p, div, span {
  color: var(--t1) !important;
}
.stSlider .css-1inwz65, .stSlider [data-testid="stWidgetLabel"] * { color: var(--t2) !important; }

/* Slider track & thumb */
.stSlider > div > div > div { background: rgba(255,255,255,0.15) !important; border-radius: 4px !important; }
.stSlider > div > div > div > div { background: var(--gold) !important; }
[data-testid="stThumbValue"] { color: var(--gold) !important; font-family: var(--mono) !important; }

/* Radio buttons — fully styled */
div[role="radiogroup"] { gap: 8px !important; }
div[role="radiogroup"] > label {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 12px !important;
  padding: 10px 16px !important;
  color: var(--t2) !important;
  font-size: 12px !important;
  font-family: var(--sans) !important;
  cursor: pointer !important;
  transition: all 0.15s !important;
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}
div[role="radiogroup"] > label:hover {
  background: rgba(255,255,255,0.10) !important;
  color: var(--t1) !important;
}
div[role="radiogroup"] > label[data-checked="true"],
div[role="radiogroup"] > label:has(input:checked) {
  background: var(--gold-dim) !important;
  border-color: var(--gold-border) !important;
  color: var(--gold) !important;
}
/* Radio circle colour */
div[role="radiogroup"] input[type="radio"] { accent-color: var(--gold) !important; }
div[role="radiogroup"] > label > div:first-child > div {
  border-color: var(--t3) !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 12px !important;
  color: var(--t1) !important;
}
.stSelectbox svg { color: var(--t2) !important; }

/* ─── INSIGHT BOX ─────────────────────────────────── */
.insight {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  border-radius: 0 14px 14px 0;
  padding: 13px 18px;
  font-size: 12.5px; color: var(--t2); line-height: 1.80;
  margin: 10px 0;
}

/* ─── VAL BOX ─────────────────────────────────────── */
.vbox {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(32px); -webkit-backdrop-filter: blur(32px);
  border: 1px solid var(--border);
  border-radius: 20px; padding:26px; text-align:center;
  box-shadow: 0 8px 40px rgba(0,0,0,0.45), 0 1px 0 var(--shine) inset;
  margin-bottom: 10px;
}

/* ─── TICKER ──────────────────────────────────────── */
.ticker {
  background: rgba(78,205,196,0.06);
  border: 1px solid rgba(78,205,196,0.18);
  border-radius: 12px; padding:12px 20px;
  font-family:var(--mono); font-size:11px; color:var(--teal);
  text-align:center; letter-spacing:0.5px; margin-bottom:14px;
}

/* ─── COHERENCE ROW ───────────────────────────────── */
.coh-row {
  display:flex; align-items:flex-start; gap:12px;
  padding:11px 14px; margin-bottom:7px;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:12px;
}

/* ─── 4P CARD ─────────────────────────────────────── */
.p4 {
  padding:14px 16px; margin-bottom:10px;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.07);
  border-left:3px solid var(--gold);
  border-radius:0 12px 12px 0;
}

/* ─── STP CARD ────────────────────────────────────── */
.stp {
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.09);
  border-radius:16px; padding:16px 18px;
  height:100%;
}

/* ─── FOOTER ──────────────────────────────────────── */
.footer {
  margin-top:40px; border-top:1px solid rgba(255,255,255,0.07);
  padding-top:16px; font-family:var(--mono); font-size:9px;
  color:var(--t3); text-align:center; line-height:2.2;
}

.block-container { padding:2rem 2.5rem 4rem; max-width:1440px; }
div[data-testid="stVerticalBlock"] > div { gap:0.4rem; }
</style>
""", unsafe_allow_html=True)

# ── HELPERS ────────────────────────────────────────────────────────────────────
PBG  = "rgba(0,0,0,0)"
GRID = "rgba(255,255,255,0.06)"
FC   = "#9ca3af"
FM   = "JetBrains Mono, monospace"
FS   = "Sora, sans-serif"

CG = "#e8c97a"   # gold
CR = "#e05c5c"   # red
CB = "#5b9cf6"   # blue
CT = "#4ecdc4"   # teal
CK = "#f0f0f0"   # near-white
CM = "#6b7280"   # muted

def rgba(h, a):
    r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
    return f"rgba({r},{g},{b},{a})"

def BL(**kw):
    d = dict(
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(color=FC, family=FM, size=10),
        xaxis=dict(gridcolor=GRID, zeroline=False, showline=False,
                   tickfont=dict(size=9, color="#6b7280")),
        yaxis=dict(gridcolor=GRID, zeroline=False, showline=False,
                   tickfont=dict(size=9, color="#6b7280")),
        legend=dict(bgcolor="rgba(255,255,255,0.04)", bordercolor="rgba(255,255,255,0.08)",
                    borderwidth=1, font=dict(size=9, color="#9ca3af")),
        margin=dict(t=42, b=32, l=10, r=10),
    )
    d.update(kw)
    return d

# ── DATA ──────────────────────────────────────────────────────────────────────
YR  = ["FY21","FY22","FY23","FY24","FY25"]
REV = [1168.52,1319.08,1266.86,1736.96,1851.09]
EBT = [410.15, 661.17, 594.01, 728.89, 761.35]
NI  = [489.85, 526.95, 438.69, 549.73, 576.11]
PBT = [578.57, 771.29, 606.46, 871.00,1041.35]
TAX = [88.72,  244.34, 167.77, 321.27, 465.24]
LIQ = [3078.62,3376.50,3605.11,4748.31,5091.45]
FIX = [566.46, 578.51, 566.98, 483.42, 398.22]
EQT = [3230.12,3450.20,3631.58,3867.84,4141.06]
DBT = [102.45, 110.12, 122.45, 142.11,  89.80]
CFO = [312.45, 450.12, 398.74, 512.33, 545.67]
CFI = [-150.11,-120.45,-85.22,-92.11,-110.45]
CFF = [-111.09,-241.86,-294.78,-513.74,-643.60]
NTC = [51.25,  87.81,  18.74,-93.52,-208.38]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
    <div>
      <p class="t-main">UTI Asset Management</p>
      <p class="t-sub">Institutional Terminal · FY21–FY25 · Historical Audit + Phase-2 Valuation</p>
      <div>
        <span class="pill pill-b">NSE: UTIAMC</span>
        <span class="pill pill-b">BSE: 543238</span>
        <span class="pill pill-g">Financials / AMC</span>
        <span class="pill">Tier-1 Institutional</span>
        <span class="pill">Feb 25, 2026</span>
      </div>
    </div>
    <div style="text-align:right;">
      <p class="price">₹874.76</p>
      <p class="price-lbl">Intrinsic Value / Share</p>
      <span class="pill pill-g">DCF · WACC 13.05% · TGR 6.0%</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI STRIP ─────────────────────────────────────────────────────────────────
for col,(v,l,d) in zip(st.columns(6), [
    ("₹1,851 Cr","FY25 Revenue","+58.4% CAGR 12.1%"),
    ("41.1%","EBIT Margin","+600 bps over 5yr"),
    ("14.9%","Return on Capital","from 12.4% FY21"),
    ("105.6%","Dividend Payout","FY25 peak"),
    ("82%","Digital Txns","from 55% FY21"),
    ("₹21L Cr+","Group AUM","FY25 peak"),
]):
    with col:
        st.markdown(f"""<div class="kpi">
          <div class="kpi-v">{v}</div>
          <div class="kpi-l">{l}</div>
          <div class="kpi-d">{d}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
T = st.tabs(["Financials","What-If Engine","B30 Moat",
             "Digital Metamorphosis","Ansoff Matrix",
             "Shareholder Yield","Marketing Strategy"])

# ═════════════════════════════════════════
# TAB 1 — FINANCIALS
# ═════════════════════════════════════════
with T[0]:
    st.markdown('<p class="slbl">Income Statement · FY21–FY25</p>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="g-card">', unsafe_allow_html=True)
        f = go.Figure()
        f.add_trace(go.Bar(x=YR,y=REV,name="Revenue",
                           marker_color=rgba(CB,0.35),marker_line_color=CB,marker_line_width=1))
        f.add_trace(go.Bar(x=YR,y=EBT,name="EBIT",
                           marker_color=rgba(CG,0.35),marker_line_color=CG,marker_line_width=1))
        f.add_trace(go.Scatter(x=YR,y=[e/r*100 for e,r in zip(EBT,REV)],
                               name="EBIT Margin %",mode="lines+markers",yaxis="y2",
                               line=dict(color=CG,width=2.5),
                               marker=dict(size=7,color=CG,line=dict(color=PBG,width=1.5))))
        f.update_layout(**BL(title=dict(text="Revenue · EBIT · Margin",
                                        font=dict(size=11,color="#c0c8d8",family=FS)),
                             barmode="group",height=310,
                             yaxis2=dict(overlaying="y",side="right",showgrid=False,
                                         ticksuffix="%",tickfont=dict(size=9,color="#6b7280")),
                             margin=dict(t=42,b=32,l=10,r=48)))
        st.plotly_chart(f,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="g-card">', unsafe_allow_html=True)
        f2 = go.Figure()
        f2.add_trace(go.Scatter(x=YR,y=NI,name="Net Income",fill="tozeroy",
                                fillcolor=rgba(CK,0.04),line=dict(color=CK,width=2.5),
                                marker=dict(size=7,color=CK,line=dict(color=PBG,width=1.5))))
        f2.add_trace(go.Scatter(x=YR,y=PBT,name="PBT",
                                line=dict(color=CT,width=1.5,dash="dot"),
                                marker=dict(size=5,color=CT)))
        f2.add_trace(go.Bar(x=YR,y=TAX,name="Tax",
                            marker_color=rgba(CR,0.30),marker_line_color=CR,marker_line_width=1))
        f2.update_layout(**BL(title=dict(text="PBT · Net Income · Tax",
                                         font=dict(size=11,color="#c0c8d8",family=FS)),height=310))
        st.plotly_chart(f2,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<p class="slbl">Balance Sheet · Cash Flows</p>',unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        f3=go.Figure()
        f3.add_trace(go.Bar(x=YR,y=LIQ,name="Liquid",
                            marker_color=rgba(CB,0.30),marker_line_color=CB,marker_line_width=1))
        f3.add_trace(go.Bar(x=YR,y=FIX,name="Fixed",
                            marker_color=rgba(CT,0.30),marker_line_color=CT,marker_line_width=1))
        f3.add_trace(go.Scatter(x=YR,y=EQT,name="Equity",mode="lines+markers",yaxis="y2",
                                line=dict(color=CG,width=2),
                                marker=dict(size=6,color=CG,line=dict(color=PBG,width=1.5))))
        f3.add_trace(go.Scatter(x=YR,y=DBT,name="Debt",mode="lines+markers",yaxis="y2",
                                line=dict(color=CR,width=1.5,dash="dot"),
                                marker=dict(size=5,color=CR)))
        f3.update_layout(**BL(title=dict(text="Balance Sheet · ₹ Cr",
                                         font=dict(size=11,color="#c0c8d8",family=FS)),
                              barmode="stack",height=310,
                              yaxis2=dict(overlaying="y",side="right",showgrid=False,
                                          tickfont=dict(size=9,color="#6b7280")),
                              margin=dict(t=42,b=32,l=10,r=48)))
        st.plotly_chart(f3,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        f4=go.Figure()
        f4.add_trace(go.Bar(x=YR,y=CFO,name="CFO",
                            marker_color=rgba(CG,0.40),marker_line_color=CG,marker_line_width=1))
        f4.add_trace(go.Bar(x=YR,y=CFI,name="CFI",
                            marker_color=rgba(CM,0.35),marker_line_color=CM,marker_line_width=1))
        f4.add_trace(go.Bar(x=YR,y=CFF,name="CFF",
                            marker_color=rgba(CR,0.35),marker_line_color=CR,marker_line_width=1))
        f4.add_trace(go.Scatter(x=YR,y=NTC,name="Net Δ Cash",mode="lines+markers",
                                line=dict(color=CB,width=2),
                                marker=dict(size=6,color=CB,line=dict(color=PBG,width=1.5))))
        f4.update_layout(**BL(title=dict(text="Cash Flow Waterfall · ₹ Cr",
                                         font=dict(size=11,color="#c0c8d8",family=FS)),
                              barmode="group",height=310))
        st.plotly_chart(f4,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("""<div class="insight">
    <strong style="color:#e8c97a;">5-Year Snapshot</strong> — Revenue CAGR 12.1% · ₹1,168→₹1,851 Cr.
    EBIT margin +600 bps to 41.1%. Equity grew ₹3,230→₹4,141 Cr, virtually debt-free.
    Record CFF outflows in FY24–25 reflect the 105.6% dividend payout.
    </div>""",unsafe_allow_html=True)

# ═════════════════════════════════════════
# TAB 2 — WHAT-IF ENGINE
# ═════════════════════════════════════════
with T[1]:
    st.markdown('<p class="slbl">Live DCF Sensitivity Terminal</p>',unsafe_allow_html=True)
    cs,co = st.columns([1,1])
    with cs:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:14px;">Adjust Assumptions</p>',unsafe_allow_html=True)
        tgr   = st.slider("Terminal Growth Rate (%)",   3.0, 9.0, 6.0,0.1)
        margin= st.slider("EBIT Margin — Year 5 (%)", 28.0,52.0,41.0,0.5)
        coe   = st.slider("WACC / Cost of Equity (%)",10.0,17.0,13.05,0.05)
        rev_g = st.slider("Revenue CAGR — Yr 1–5 (%)", 4.0,15.0, 6.0,0.5)
        reinv = st.slider("Reinvestment Rate (%)",      5.0,40.0,17.0,1.0)
        st.markdown("""<div style="margin-top:14px;padding:12px 14px;
                       background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                       border-radius:10px;font-family:'JetBrains Mono',monospace;
                       font-size:10px;color:#6b7280;line-height:2.2;">
        Base Rev ₹1,851 Cr &nbsp;·&nbsp; Shares 12.8 Cr<br>
        Net Cash ₹3,100 Cr &nbsp;·&nbsp; Tax 44.7%<br>
        Beta 1.1 &nbsp;·&nbsp; Risk-free 7.0%
        </div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with co:
        BR=1851.09;TR=0.447;SH=12.8;NC=3100.0
        revs =[BR*(1+rev_g/100)**t for t in range(1,6)]
        nops =[r*(margin/100)*(1-TR) for r in revs]
        fcffs=[n*(1-reinv/100) for n in nops]
        pv_f =sum(f/(1+coe/100)**t for t,f in enumerate(fcffs,1))
        tv   =(fcffs[-1]*(1+tgr/100))/((coe/100)-(tgr/100)) if coe/100>tgr/100 else 0
        pv_tv=tv/(1+coe/100)**5
        price=(pv_f+pv_tv+NC)/SH
        delta=(price-874.76)/874.76*100
        pc=CG if price>=874.76 else CR
        sg="▲" if delta>=0 else "▼"

        st.markdown(f"""<div class="vbox">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;
                      color:#6b7280;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px;">
            Computed Intrinsic Value</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:52px;
                      font-weight:500;color:{pc};letter-spacing:-2px;line-height:1;">
            ₹{price:,.2f}</div>
          <div style="font-size:12.5px;color:{pc};margin-top:10px;font-family:'JetBrains Mono',monospace;">
            {sg} {abs(delta):.1f}% vs base ₹874.76</div>
        </div>""",unsafe_allow_html=True)

        m1,m2,m3=st.columns(3)
        for col,val,lbl in zip([m1,m2,m3],
            [f"₹{pv_f:,.0f}Cr",f"₹{pv_tv:,.0f}Cr",f"₹{(pv_f+pv_tv):,.0f}Cr"],
            ["PV FCFFs","PV Terminal","Enterprise Val"]):
            with col:
                st.markdown(f"""<div class="kpi" style="margin-bottom:8px;">
                  <div class="kpi-v" style="font-size:14px;">{val}</div>
                  <div class="kpi-l">{lbl}</div></div>""",unsafe_allow_html=True)

        st.markdown('<div class="g-card" style="margin-top:10px;">',unsafe_allow_html=True)
        fcb=go.Figure(go.Bar(x=[f"Y{i}" for i in range(1,6)],y=fcffs,
                             marker_color=[rgba(CG,0.20+i*0.10) for i in range(5)],
                             marker_line_color=CG,marker_line_width=1,
                             text=[f"₹{v:.0f}" for v in fcffs],textposition="outside",
                             textfont=dict(size=9,color=FC)))
        fcb.update_layout(**BL(title=dict(text="Projected FCFF · ₹ Cr",
                                           font=dict(size=11,color="#c0c8d8",family=FS)),
                               height=200,margin=dict(t=38,b=28,l=10,r=10)))
        st.plotly_chart(fcb,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<p class="slbl">WACC × Terminal Growth Rate · Price Sensitivity Heatmap</p>',unsafe_allow_html=True)
    st.markdown('<div class="g-card">',unsafe_allow_html=True)
    wr=np.arange(10.0,17.5,0.5); gr=np.arange(3.0,9.5,0.5)
    heat=[]
    for w in wr:
        row=[]
        for g in gr:
            if w/100<=g/100: row.append(None); continue
            fb=nops[-1]*(1-reinv/100)
            _tv=(fb*(1+g/100))/((w/100)-(g/100))
            row.append(round((sum(f/(1+w/100)**t for t,f in enumerate(fcffs,1))+_tv/(1+w/100)**5+NC)/SH,1))
        heat.append(row)
    df_h=pd.DataFrame(heat,index=[f"{w:.1f}%" for w in wr],columns=[f"{g:.1f}%" for g in gr])
    fh=go.Figure(go.Heatmap(z=df_h.values,x=df_h.columns,y=df_h.index,
        colorscale=[[0,"rgba(20,20,30,0.9)"],[0.3,"rgba(80,30,30,0.9)"],
                    [0.6,"rgba(30,60,120,0.9)"],[0.85,"rgba(91,156,246,0.9)"],
                    [1.0,"rgba(232,201,122,1)"]],
        text=[[f"₹{v:.0f}" if v else "" for v in row] for row in df_h.values],
        texttemplate="%{text}",textfont=dict(size=8,color="rgba(255,255,255,0.82)"),
        showscale=True,
        colorbar=dict(title=dict(text="₹/sh",font=dict(color=FC,size=10)),
                      tickfont=dict(color=FC,size=8),bgcolor=PBG,borderwidth=0)))
    fh.update_layout(**BL(
        title=dict(text="Share Price · WACC (Y) × Terminal Growth Rate (X)",
                   font=dict(size=11,color="#c0c8d8",family=FS)),
        xaxis=dict(title="Terminal Growth Rate",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
        yaxis=dict(title="WACC",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
        height=390,margin=dict(t=45,b=50,l=60,r=20)))
    st.plotly_chart(fh,use_container_width=True)
    st.markdown("""<p style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#4b5563;
        text-align:center;margin-top:-6px;">
        Base: WACC 13.05% · TGR 6.0% → ₹874.76 · Cells where WACC ≤ TGR excluded
        </p></div>""",unsafe_allow_html=True)

# ═════════════════════════════════════════
# TAB 3 — B30 MOAT
# ═════════════════════════════════════════
with T[2]:
    st.markdown('<p class="slbl">Competitive Moat · B30 Geographic Strategy</p>',unsafe_allow_html=True)
    cl,cr=st.columns(2)
    with cl:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        cities={"Mumbai":(72.88,19.07,45,"T30"),"Delhi":(77.21,28.61,42,"T30"),
                "Bengaluru":(77.59,12.97,38,"T30"),"Chennai":(80.27,13.08,30,"T30"),
                "Hyderabad":(78.47,17.38,29,"T30"),"Pune":(73.86,18.52,25,"T30"),
                "Patna":(85.14,25.59,18,"B30"),"Lucknow":(80.95,26.85,16,"B30"),
                "Jaipur":(75.79,26.91,15,"B30"),"Bhopal":(77.41,23.26,14,"B30"),
                "Indore":(75.86,22.72,14,"B30"),"Surat":(72.83,21.17,13,"B30"),
                "Nagpur":(79.09,21.15,12,"B30"),"Kanpur":(80.35,26.46,11,"B30"),
                "Varanasi":(82.97,25.32,9,"B30"),"Agra":(78.01,27.18,9,"B30")}
        shown={"T30":False,"B30":False}
        fm=go.Figure()
        for city,(lon,lat,aum,tier) in cities.items():
            cc=CG if tier=="B30" else CB
            fm.add_trace(go.Scatter(x=[lon],y=[lat],mode="markers+text",
                marker=dict(size=aum*0.65+6,color=cc,opacity=0.85 if tier=="B30" else 0.50,
                            line=dict(color="rgba(255,255,255,0.30)",width=1.5)),
                text=[city],textposition="top center",textfont=dict(size=7.5,color="#6b7280"),
                name=tier,legendgroup=tier,showlegend=not shown[tier],
                hovertemplate=f"<b>{city}</b><br>Tier:{tier}<br>AUM:{aum}<extra></extra>"))
            shown[tier]=True
        fm.update_layout(**BL(
            title=dict(text="Geographic Footprint (Bubble = Relative AUM)",font=dict(size=11,color="#c0c8d8",family=FS)),
            xaxis=dict(range=[68,92],gridcolor=GRID,tickfont=dict(size=8,color="#4b5563")),
            yaxis=dict(range=[8,34], gridcolor=GRID,tickfont=dict(size=8,color="#4b5563")),height=380))
        st.plotly_chart(fm,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        BY2=["FY21","FY22","FY23","FY24","FY25"]
        fsp=go.Figure()
        fsp.add_trace(go.Scatter(x=BY2,y=[14.2,16.8,17.5,18.9,18.0],name="Core MFs",
                                 fill="tozeroy",fillcolor=rgba(CB,0.07),
                                 line=dict(color=CB,width=2),marker=dict(size=5,color=CB)))
        fsp.add_trace(go.Scatter(x=BY2,y=[1.2,1.55,1.85,2.15,2.5],name="UTI Pension",
                                 fill="tozeroy",fillcolor=rgba(CG,0.08),
                                 line=dict(color=CG,width=2.5),marker=dict(size=6,color=CG),yaxis="y2"))
        fsp.add_trace(go.Scatter(x=BY2,y=[0.08,0.14,0.22,0.35,0.52],name="UTI Alts",
                                 line=dict(color=CR,width=2,dash="dash"),
                                 marker=dict(size=6,color=CR),yaxis="y2"))
        fsp.update_layout(**BL(
            title=dict(text="Speedboat AUM Tracker · ₹ Trillion",font=dict(size=11,color="#c0c8d8",family=FS)),
            yaxis=dict(gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
            yaxis2=dict(overlaying="y",side="right",showgrid=False,tickfont=dict(size=8,color="#6b7280")),
            height=220,margin=dict(t=42,b=32,l=10,r=48)))
        st.plotly_chart(fsp,use_container_width=True)
        fmx=go.Figure()
        fmx.add_trace(go.Bar(x=BY2,y=[42,48,50,51,52],name="Equity",
                             marker_color=rgba(CB,0.50),marker_line_color=CB,marker_line_width=1))
        fmx.add_trace(go.Bar(x=BY2,y=[40,35,32,30,28],name="Debt",
                             marker_color=rgba(CM,0.40),marker_line_color=CM,marker_line_width=1))
        fmx.add_trace(go.Bar(x=BY2,y=[18,17,18,19,20],name="ETF/Others",
                             marker_color=rgba(CG,0.40),marker_line_color=CG,marker_line_width=1))
        fmx.update_layout(**BL(barmode="stack",
                               yaxis=dict(ticksuffix="%",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                               height=175,margin=dict(t=10,b=30,l=10,r=10)))
        st.plotly_chart(fmx,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("""<div class="insight">
    <strong style="color:#e8c97a;">B30 Structural Moat</strong> — B30 investors stay invested 2.5× longer than T30.
    India Stack reduced CAC by ~40% over 5 years. Digital-first expansion = zero branch capex.
    </div>""",unsafe_allow_html=True)

# ═════════════════════════════════════════
# TAB 4 — DIGITAL METAMORPHOSIS
# ═════════════════════════════════════════
with T[3]:
    st.markdown("""<div class="ticker">
    ✦ &nbsp; PAPERLESS → ₹45 CRORE SAVED ANNUALLY · SINCE FY23 &nbsp;|&nbsp;
    AUM-PER-EMPLOYEE ↑ +35% &nbsp;|&nbsp; DIGITAL TRANSACTIONS 82% (FY25)
    </div>""",unsafe_allow_html=True)
    cd1,cd2=st.columns(2)
    BY3=["FY21","FY22","FY23","FY24","FY25"]
    with cd1:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        fd=go.Figure()
        fd.add_trace(go.Bar(x=BY3,y=[55,63,71,77,82],name="Digital Txn %",
                            marker_color=[rgba(CB,0.22+i*0.10) for i in range(5)],
                            marker_line_color=CB,marker_line_width=1,
                            text=["55%","63%","71%","77%","82%"],textposition="outside",
                            textfont=dict(size=9,color=FC)))
        fd.add_trace(go.Scatter(x=BY3,y=[200,196,190,182,175],name="Branches",
                                mode="lines+markers",yaxis="y2",
                                line=dict(color=CR,width=1.5,dash="dot"),
                                marker=dict(size=5,color=CR)))
        fd.update_layout(**BL(
            title=dict(text="Digital Txn % vs Branch Rationalisation",font=dict(size=11,color="#c0c8d8",family=FS)),
            yaxis=dict(range=[0,102],ticksuffix="%",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
            yaxis2=dict(overlaying="y",side="right",showgrid=False,tickfont=dict(size=8,color="#6b7280")),
            height=285,margin=dict(t=42,b=30,l=10,r=48)))
        st.plotly_chart(fd,use_container_width=True)
        fe=go.Figure(go.Scatter(x=BY3,y=[100,108,116,127,135],fill="tozeroy",
                                fillcolor=rgba(CT,0.07),line=dict(color=CT,width=2.5),
                                marker=dict(size=7,color=CT,line=dict(color=PBG,width=1.5)),
                                text=["100","108","116","127","135"],textposition="top center",
                                textfont=dict(size=9,color=FC)))
        fe.update_layout(**BL(title=dict(text="AUM-per-Employee Index (FY21=100)",
                                          font=dict(size=11,color="#c0c8d8",family=FS)),
                              yaxis=dict(range=[85,145],gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                              height=195,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(fe,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with cd2:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        fs=go.Figure()
        fs.add_trace(go.Scatter(x=BY3,y=[0.36,0.38,0.39,0.41,0.43],
                                mode="lines+markers+text",fill="tozeroy",fillcolor=rgba(CG,0.07),
                                line=dict(color=CG,width=2.5),
                                marker=dict(size=9,color=CG,line=dict(color=PBG,width=1.5)),
                                text=["0.36×","0.38×","0.39×","0.41×","0.43×"],
                                textposition="top center",textfont=dict(size=9,color=CG)))
        fs.add_hline(y=0.43,line_dash="dot",line_color=CK,
                     annotation_text="FY25: 0.43×",annotation_font=dict(color=CK,size=9))
        fs.update_layout(**BL(title=dict(text="Sales-to-Capital Ratio",
                                          font=dict(size=11,color="#c0c8d8",family=FS)),
                              yaxis=dict(range=[0.30,0.50],gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                              height=248,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(fs,use_container_width=True)
        paper=[0,0,45,90,135]
        fp=go.Figure(go.Bar(x=BY3,y=paper,
                            marker_color=[rgba(CG,0.55) if v else rgba(CM,0.15) for v in paper],
                            marker_line_color=[CG if v else CM for v in paper],marker_line_width=1,
                            text=[f"₹{v}Cr" if v else "—" for v in paper],
                            textposition="outside",textfont=dict(size=9,color=FC)))
        fp.update_layout(**BL(title=dict(text="Paperless Cumulative Savings · ₹ Cr",
                                          font=dict(size=11,color="#c0c8d8",family=FS)),
                              height=215,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(fp,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ═════════════════════════════════════════
# TAB 5 — ANSOFF MATRIX
# ═════════════════════════════════════════
with T[4]:
    st.markdown('<p class="slbl">Strategic Positioning · Ansoff Matrix + Fee Stress Test</p>',unsafe_allow_html=True)
    ca,cb=st.columns([1.15,0.85])

    with ca:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:14px;">Select a quadrant to explore:</p>',unsafe_allow_html=True)

        options = [
            "★  Market Development  ← UTI Primary Strategy",
            "   Market Penetration (T30 Deepening)",
            "   Product Development (Passive / ETF)",
            "   Diversification (Alternatives + Pension)",
        ]
        sel = st.radio("quadrant", options, index=0, label_visibility="collapsed")

        # Visual Ansoff grid
        quad_colors = {
            "★  Market Development  ← UTI Primary Strategy":   [rgba(CG,0.08), rgba(CG,0.08), rgba(CM,0.05), rgba(CG,0.28)],
            "   Market Penetration (T30 Deepening)":            [rgba(CM,0.05), rgba(CM,0.05), rgba(CB,0.25), rgba(CM,0.05)],
            "   Product Development (Passive / ETF)":           [rgba(CT,0.25), rgba(CM,0.05), rgba(CM,0.05), rgba(CM,0.05)],
            "   Diversification (Alternatives + Pension)":      [rgba(CM,0.05), rgba(CR,0.25), rgba(CM,0.05), rgba(CM,0.05)],
        }
        ql = quad_colors[sel]

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;
                    gap:8px;margin:4px 0 16px 0;height:200px;">
          <div style="background:{ql[2]};border:1px solid rgba(255,255,255,0.10);
                      border-radius:14px;padding:12px;display:flex;align-items:center;
                      justify-content:center;text-align:center;">
            <div>
              <div style="font-size:10px;font-weight:600;color:#9ca3af;margin-bottom:3px;">Product Development</div>
              <div style="font-size:9px;color:#6b7280;">New Products · Existing Markets</div>
            </div>
          </div>
          <div style="background:{ql[1]};border:1px solid rgba(255,255,255,0.10);
                      border-radius:14px;padding:12px;display:flex;align-items:center;
                      justify-content:center;text-align:center;">
            <div>
              <div style="font-size:10px;font-weight:600;color:#9ca3af;margin-bottom:3px;">Diversification</div>
              <div style="font-size:9px;color:#6b7280;">New Products · New Markets</div>
            </div>
          </div>
          <div style="background:{ql[3]};border:1px solid rgba(255,255,255,0.12);
                      border-radius:14px;padding:12px;display:flex;align-items:center;
                      justify-content:center;text-align:center;">
            <div>
              <div style="font-size:11px;font-weight:600;color:#e8c97a;margin-bottom:3px;">★ Market Development</div>
              <div style="font-size:9px;color:#9ca3af;">Existing Products · New B30 Markets</div>
              <div style="margin-top:6px;"><span style="background:rgba(232,201,122,0.18);
                border:1px solid rgba(232,201,122,0.35);border-radius:100px;
                padding:2px 10px;font-size:9px;color:#e8c97a;">UTI Primary</span></div>
            </div>
          </div>
          <div style="background:{ql[0]};border:1px solid rgba(255,255,255,0.10);
                      border-radius:14px;padding:12px;display:flex;align-items:center;
                      justify-content:center;text-align:center;">
            <div>
              <div style="font-size:10px;font-weight:600;color:#9ca3af;margin-bottom:3px;">Market Penetration</div>
              <div style="font-size:9px;color:#6b7280;">Existing Products · Existing Markets</div>
            </div>
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;
                    font-family:'JetBrains Mono',monospace;font-size:9px;color:#4b5563;
                    margin-bottom:10px;">
          <span>← Existing Products</span><span>New Products →</span>
        </div>
        """, unsafe_allow_html=True)

        det = {
            "★  Market Development  ← UTI Primary Strategy":
                (CG, "Market Development — B30 Digital Expansion",
                 "Existing trusted products pushed into new B30 geographies. Capital-light, digital-first, zero branch capex. B30 investors retain 2.5× longer. India Stack cut CAC by ~40%. Low reinvestment (17%) because growth comes from distribution reach, not product R&D."),
            "   Market Penetration (T30 Deepening)":
                (CB, "Market Penetration — T30 Retention",
                 "Defend HNI and corporate treasury AUM in T30 metros through institutional pedigree. Not a price war — UTI is a Differentiator, not a cost leader. 25% NPS private-sector market share is the key battle line."),
            "   Product Development (Passive / ETF)":
                (CT, "Product Development — Passive/ETF Hedge",
                 "UTI International launched global passive products for sovereign mandates. Passive fees (0.05–0.20%) are far below active (0.7–1.5%) — volume must compensate rate compression. Hedge strategy against fee compression, not the growth engine."),
            "   Diversification (Alternatives + Pension)":
                (CR, "Diversification — The Speedboats",
                 "UTI Alternatives: management fees 1.5–2.0%, far above MF TERs. UTI Pension: ₹2.5T AUM, NPS private-sector market leader. Highest risk-reward quadrant — already at critical mass by FY25."),
        }
        bc,title,body = det[sel]
        st.markdown(f"""<div class="insight" style="border-left-color:{bc};">
        <strong style="color:{bc};">{title}</strong><br>{body}
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:10px;">Fee Compression Scenario</p>',unsafe_allow_html=True)
        sc_name=st.selectbox("Scenario",["Base Case — 6% growth, passive 20% mix",
                                          "Bear Case — Passive accelerates to 35%",
                                          "Bull Case — Active premium holds, B30 surge"],
                             label_visibility="collapsed")
        sc_map={"Base Case — 6% growth, passive 20% mix":
                    ([1851,1963,2081,2206,2338,2478],CK,"₹874.76","0.0%"),
                "Bear Case — Passive accelerates to 35%":
                    ([1851,1917,1985,2055,2128,2203],CR,"₹612.40","−30.0%"),
                "Bull Case — Active premium holds, B30 surge":
                    ([1851,2073,2322,2600,2912,3261],CG,"₹1,140.20","+30.4%")}
        sc_r,sc_c,sc_p,sc_pct=sc_map[sc_name]
        sy=["FY25","FY26E","FY27E","FY28E","FY29E","FY30E"]
        fsc=go.Figure()
        fsc.add_trace(go.Bar(x=sy,y=sc_r,name="Revenue",
                             marker_color=rgba(sc_c,0.22),marker_line_color=sc_c,marker_line_width=1.5))
        fsc.add_trace(go.Scatter(x=sy,y=[r*0.411*(1-0.447) for r in sc_r],name="Net Income",
                                 mode="lines+markers",line=dict(color=sc_c,width=2.5),
                                 marker=dict(size=7,color=sc_c,line=dict(color=PBG,width=1.5))))
        fsc.update_layout(**BL(title=dict(text="Revenue + Net Income Projection · ₹ Cr",
                                           font=dict(size=11,color="#c0c8d8",family=FS)),
                               height=255,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(fsc,use_container_width=True)
        st.markdown(f"""<div class="vbox" style="padding:20px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#6b7280;
                      letter-spacing:3px;text-transform:uppercase;margin-bottom:8px;">
            Scenario Intrinsic Value</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:38px;
                      font-weight:500;color:{sc_c};letter-spacing:-1px;">{sc_p}</div>
          <div style="color:{sc_c};font-size:12px;font-family:'JetBrains Mono',monospace;
                      margin-top:6px;">{sc_pct} vs base ₹874.76</div>
        </div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ═════════════════════════════════════════
# TAB 6 — SHAREHOLDER YIELD
# ═════════════════════════════════════════
with T[5]:
    st.markdown('<p class="slbl">Capital Discipline · Dividend + ROC Analysis</p>',unsafe_allow_html=True)
    cg,ch=st.columns(2)
    BY4=["FY21","FY22","FY23","FY24","FY25"]
    with cg:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        fpay=go.Figure()
        fpay.add_trace(go.Bar(x=BY4,y=[8.8,17.0,22.0,36.0,48.0],name="DPS (₹)",
                              marker_color=[rgba(CB,0.22+i*0.10) for i in range(5)],
                              marker_line_color=CB,marker_line_width=1,
                              text=["₹8.8","₹17","₹22","₹36","₹48"],textposition="outside",
                              textfont=dict(size=9,color=FC)))
        fpay.add_trace(go.Scatter(x=BY4,y=[18.1,32.5,51.2,72.4,105.6],name="Payout %",
                                  mode="lines+markers",yaxis="y2",
                                  line=dict(color=CG,width=2.5),
                                  marker=dict(size=7,color=CG,line=dict(color=PBG,width=1.5))))
        fpay.add_hline(y=100,yref="y2",line_dash="dot",line_color=CR,
                       annotation_text="100%",annotation_font=dict(color=CR,size=9))
        fpay.update_layout(**BL(title=dict(text="DPS + Payout Ratio Evolution",
                                            font=dict(size=11,color="#c0c8d8",family=FS)),
                               yaxis=dict(title="₹",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                               yaxis2=dict(overlaying="y",side="right",showgrid=False,
                                           ticksuffix="%",tickfont=dict(size=8,color="#6b7280")),
                               height=275,margin=dict(t=42,b=30,l=10,r=48)))
        st.plotly_chart(fpay,use_container_width=True)
        fdo=go.Figure(go.Pie(values=[83,17],labels=["Returned to Shareholders","Retained"],hole=0.68,
                             marker=dict(colors=[CG,rgba(CK,0.07)],line=dict(color=PBG,width=0)),
                             textfont=dict(size=10,color="#9ca3af")))
        fdo.add_annotation(text="83%",x=0.5,y=0.5,showarrow=False,
                           font=dict(size=22,color=CG,family=FM))
        fdo.update_layout(paper_bgcolor=PBG,font=dict(color=FC,family=FM),
                          legend=dict(bgcolor="rgba(255,255,255,0.03)",font=dict(size=9,color="#9ca3af")),
                          title=dict(text="FY25 — ₹57.35 EPS → ₹48 DPS",
                                     font=dict(size=11,color="#c0c8d8",family=FS)),
                          height=240,margin=dict(t=42,b=10,l=10,r=10))
        st.plotly_chart(fdo,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with ch:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        roc=[12.4,12.9,12.1,13.7,14.9]; wcc=[8.5]*5
        froc=go.Figure()
        froc.add_trace(go.Scatter(x=BY4,y=roc,name="ROC",fill="tozeroy",
                                  fillcolor=rgba(CB,0.07),line=dict(color=CB,width=2.5),
                                  marker=dict(size=7,color=CB,line=dict(color=PBG,width=1.5))))
        froc.add_trace(go.Scatter(x=BY4,y=wcc,name="WACC",fill="tonexty",
                                  fillcolor=rgba(CG,0.07),line=dict(color=CR,width=1.5,dash="dot"),
                                  marker=dict(size=5,color=CR)))
        for i,(yr,sp) in enumerate(zip(BY4,[r-w for r,w in zip(roc,wcc)])):
            froc.add_annotation(x=yr,y=(roc[i]+wcc[i])/2,text=f"+{sp:.1f}%",showarrow=False,
                                font=dict(size=9,color=CG,family=FM))
        froc.update_layout(**BL(title=dict(text="ROC vs WACC — Value Creation Spread",
                                            font=dict(size=11,color="#c0c8d8",family=FS)),
                               yaxis=dict(ticksuffix="%",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                               height=280,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(froc,use_container_width=True)
        fbs=go.Figure(go.Bar(x=["Liquid Assets","Fixed Assets","Equity","Debt+Leases"],
                             y=[5091,398,4141,90],
                             marker_color=[rgba(CB,0.35),rgba(CT,0.30),rgba(CG,0.35),rgba(CR,0.35)],
                             marker_line_color=[CB,CT,CG,CR],marker_line_width=1.5,
                             text=["₹5,091","₹398","₹4,141","₹90"],
                             textposition="outside",textfont=dict(size=9,color=FC)))
        fbs.update_layout(**BL(title=dict(text="Balance Sheet Health · FY25 · ₹ Cr",
                                           font=dict(size=11,color="#c0c8d8",family=FS)),
                               height=230,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(fbs,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("""<div class="insight">
    <strong style="color:#e8c97a;">Why UTI Returns So Much Cash</strong> — ROC–WACC spread +5.8% to +6.2% proves UTI
    earns well above cost of capital. No high-quality reinvestment opportunities exist at these elevated returns — hence 80–105% payout.
    Net cash ₹3,100+ Cr (~₹242/share) = ~28% of ₹874.76 intrinsic value.
    </div>""",unsafe_allow_html=True)

# ═════════════════════════════════════════
# TAB 7 — MARKETING STRATEGY
# ═════════════════════════════════════════
with T[6]:
    st.markdown('<p class="slbl">Marketing Strategy · Positioning · Lifecycle · STP · 4Ps</p>',unsafe_allow_html=True)

    r1a,r1b = st.columns(2)

    with r1a:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:12px;">Company Life Cycle — Mature Growth Stage</p>',unsafe_allow_html=True)
        stages=["Start-Up","Growth","Mature Growth","Mature","Decline"]
        flc=go.Figure()
        flc.add_trace(go.Scatter(x=stages,y=[5,35,75,90,55],name="Revenue Growth",
                                 fill="tozeroy",fillcolor=rgba(CB,0.07),
                                 line=dict(color=CB,width=2.5),
                                 marker=dict(size=8,color=CB,line=dict(color=PBG,width=1.5))))
        flc.add_trace(go.Scatter(x=stages,y=[-20,15,45,38,10],name="ROI / Returns",
                                 line=dict(color=CG,width=2,dash="dot"),
                                 marker=dict(size=7,color=CG,line=dict(color=PBG,width=1.5))))
        flc.add_vline(x=2,line_dash="solid",line_color=CG,line_width=2.5,
                      annotation_text="◀ UTI NOW",
                      annotation_font=dict(color=CG,size=10,family=FM))
        flc.add_vrect(x0=1.75,x1=2.25,fillcolor=rgba(CG,0.08),
                      line_color=rgba(CG,0.20),line_width=1)
        flc.update_layout(**BL(title=dict(text="UTI Life Cycle Position",
                                           font=dict(size=11,color="#c0c8d8",family=FS)),
                               yaxis=dict(gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                               height=270,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(flc,use_container_width=True)
        st.markdown("""<div class="insight">UTI is in <strong style="color:#e8c97a;">Mature Growth</strong> —
        past frantic expansion but the Indian investor base is still in its infancy.
        Revenue stabilises at 6% CAGR, margins expand, and the ROC–WACC spread remains healthy.
        The 80–105% payout is the classic signature of a company that has "arrived."
        </div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with r1b:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:12px;">Porter\'s 5 Forces — Competitive Intensity</p>',unsafe_allow_html=True)
        forces=["Threat of<br>New Entrants","Buyer<br>Power","Supplier<br>Power","Threat of<br>Substitutes","Competitive<br>Rivalry"]
        scores=[3,4,2,4,3]
        fp5=go.Figure(go.Bar(x=forces,y=scores,
                             marker_color=[rgba(CR,0.20+s*0.08) for s in scores],
                             marker_line_color=[CR if s>=4 else CM for s in scores],
                             marker_line_width=1.5,
                             text=["Low","Medium","Low","High","Medium"],
                             textposition="outside",textfont=dict(size=9,color=FC)))
        fp5.add_hline(y=3.5,line_dash="dot",line_color=CR,
                      annotation_text="High-risk threshold",
                      annotation_font=dict(color=CR,size=9))
        fp5.update_layout(**BL(title=dict(text="Force Intensity (1=Low · 5=Very High)",
                                           font=dict(size=11,color="#c0c8d8",family=FS)),
                               yaxis=dict(range=[0,6],gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                               xaxis=dict(tickfont=dict(size=9,color="#9ca3af")),
                               height=270,margin=dict(t=42,b=40,l=10,r=10)))
        st.plotly_chart(fp5,use_container_width=True)
        st.markdown("""<div class="insight"><strong style="color:#e05c5c;">Key competitive risks</strong> —
        Buyer power and substitutes (passive ETFs) are the two high forces. UTI's defence: brand trust
        in B30, NPS pension anchor, and digital moat that new fintechs cannot easily replicate.
        </div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    # STP
    st.markdown('<p class="slbl">Segmentation · Targeting · Positioning</p>',unsafe_allow_html=True)
    s1,s2,s3 = st.columns(3)
    stp_data = [
        ("Segmentation", CG, [
            ("Geographic","T30 vs B30 cities — B30 is the growth frontier with lower competition"),
            ("Demographic","First-time investors (B30) · HNIs (metro) · Corporates (treasury)"),
            ("Behavioural","SIP savers vs lump-sum · Active vs passive preference"),
            ("B30 Priority","2.5× longer retention · India Stack cuts CAC by 40%"),
        ]),
        ("Targeting", CB, [
            ("Primary","B30 first-time retail investors via SIP — digital-first acquisition"),
            ("Secondary","Corporate/HNI in T30 — institutional mandates and treasury"),
            ("Pension","Govt and private-sector NPS subscribers via UTI Pension Fund"),
            ("Global","Sovereign wealth funds via ESG-screened equity mandates"),
        ]),
        ("Positioning", CR, [
            ("Core Claim","India's Most Trusted Asset Manager — institutional pedigree"),
            ("Differentiator","B30 physical + digital reach that private AMCs cannot match"),
            ("Not a","Price leader — avoids fee wars with pure-passive players"),
            ("Bundle Strategy","Passive as hook → migrate investors to high-margin thematic funds"),
        ]),
    ]
    for col,(title,color,items) in zip([s1,s2,s3], stp_data):
        with col:
            rows="".join([f"""<div style="padding:9px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
              <div style="font-size:9.5px;font-family:'JetBrains Mono',monospace;
                          color:{color};margin-bottom:2px;text-transform:uppercase;letter-spacing:1px;">
                {k}</div>
              <div style="font-size:11.5px;color:#9ca3af;line-height:1.55;">{v}</div>
            </div>""" for k,v in items])
            st.markdown(f"""<div class="g-card">
              <div style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:12px;
                          padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.08);">
                {title}</div>
              {rows}
            </div>""",unsafe_allow_html=True)

    # 4Ps + Coherence
    st.markdown('<p class="slbl">The 4Ps + Strategic Coherence Audit</p>',unsafe_allow_html=True)
    p1,p2 = st.columns([1.2,0.8])

    with p1:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:14px;">Marketing Mix — 4Ps</p>',unsafe_allow_html=True)
        ps4 = [
            ("Product", CG, ["Equity, Debt, Hybrid MFs — the core trusted range",
                              "Thematic & ESG funds for HNI and global mandates",
                              "NPS pension anchor (₹2.5T AUM) — UTI Pension Fund",
                              "ETF/Index funds — passive hedge against fee compression",
                              "Alternatives platform (1.5–2.0% fees) — UTI Alts"]),
            ("Price", CB, ["Active equity TER ~0.7–1.5% — industry standard, not discounted",
                            "Passive/ETF at 0.05–0.20% — volume play, not margin play",
                            "Alternatives 1.5–2.0% + carry — premium pricing justified by returns",
                            "Bundle: use low-fee passive to retain investors in UTI ecosystem",
                            "No price wars — differentiation is the primary defence"]),
            ("Place", CT, ["B30 digital-first: 82% transactions digital by FY25",
                            "175 physical branches for trust in Tier-3 cities",
                            "India Stack: e-KYC + UPI reduced CAC by ~40% over 5 years",
                            "Global: Singapore and UK offices for sovereign wealth mandates",
                            "Partnership with post offices and regional banks for B30 reach"]),
            ("Promotion", CR, ["Brand positioning: 'Nobody ever got fired for buying UTI'",
                                "SIP education campaigns in B30 heartland — trust-first",
                                "ESG credential marketing → sovereign wealth fund pitch",
                                "NPS brand as safety and trust anchor in retirement planning",
                                "Low paid-media spend — brand trust is organic and earned"]),
        ]
        for pname,pcolor,items in ps4:
            items_html="".join([f"<li style='margin-bottom:5px;font-size:11.5px;color:#9ca3af;'>{i}</li>" for i in items])
            st.markdown(f"""<div class="p4" style="border-left-color:{pcolor};">
              <div style="font-size:11px;font-weight:600;color:{pcolor};margin-bottom:7px;
                          font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:1px;">
                {pname}</div>
              <ul style="margin:0;padding-left:16px;list-style:disc;">{items_html}</ul>
            </div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="g-card">',unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f0f0;margin-bottom:14px;">Strategic Coherence Audit</p>',unsafe_allow_html=True)
        checks=[
            ("✓","Lifecycle → Dividend",CG,"Mature stage justifies 80–105% payout. Only reinvest where ROC > WACC."),
            ("✓","Lifecycle → Pricing", CG,"Mature company avoids price wars. Defends margin through differentiation."),
            ("✓","Ansoff → Capex",      CG,"Market Development funded by digital spend, not branch expansion."),
            ("✓","B30 → CAC",           CG,"India Stack + digital model cuts CAC 40%. B30 strategy is feasible."),
            ("✓","NPS → Moat",          CG,"25% NPS market share is structural. Trust-based switching costs are very high."),
            ("✓","ESG → Global",        CG,"100% ESG-screened AUM positions UTI for sovereign wealth mandates."),
            ("⚠","Passive Growth Risk", CR,"If passive hits 35%+ of mix, margin compression outpaces B30 volume gains."),
        ]
        for tick,item,col,desc in checks:
            st.markdown(f"""<div class="coh-row">
              <div style="font-size:17px;color:{col};flex-shrink:0;line-height:1.3;">{tick}</div>
              <div>
                <div style="font-size:11px;font-weight:600;color:{col};
                            font-family:'JetBrains Mono',monospace;margin-bottom:2px;">{item}</div>
                <div style="font-size:11px;color:#6b7280;line-height:1.55;">{desc}</div>
              </div>
            </div>""",unsafe_allow_html=True)
        st.markdown("""<div class="insight" style="margin-top:12px;">
        <strong style="color:#e8c97a;">Verdict</strong> — Strategy is internally coherent across all 6 dimensions.
        Single identified risk: passive fee compression. If passive exceeds 35% of AUM mix,
        EBIT margin compression will outpace B30 volume growth.
        Monitor passive mix % as the leading risk indicator.
        </div>""",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    # Revenue attribution
    st.markdown('<p class="slbl">Revenue Mix · Fee Margin by Segment · FY25</p>',unsafe_allow_html=True)
    st.markdown('<div class="g-card">',unsafe_allow_html=True)
    ra,rb=st.columns(2)
    with ra:
        cats=["Active Equity","Debt/Liquid","ETF/Passive","UTI Pension","UTI Alts","International"]
        vals=[42,18,9,16,8,7]
        pie_colors=[rgba(CB,0.80),rgba(CM,0.70),rgba(CG,0.50),rgba(CG,0.80),rgba(CR,0.80),rgba(CT,0.70)]
        fpie=go.Figure(go.Pie(labels=cats,values=vals,hole=0.55,
                              marker=dict(colors=pie_colors,line=dict(color=PBG,width=2)),
                              textfont=dict(size=10,color="#c0c8d8"),textposition="outside"))
        fpie.add_annotation(text="FY25<br>Mix",x=0.5,y=0.5,showarrow=False,
                            font=dict(size=13,color=FC,family=FM))
        fpie.update_layout(paper_bgcolor=PBG,font=dict(color=FC,family=FM),
                           legend=dict(bgcolor="rgba(255,255,255,0.03)",font=dict(size=9,color="#9ca3af")),
                           title=dict(text="Revenue Attribution by Segment (%)",
                                      font=dict(size=11,color="#c0c8d8",family=FS)),
                           height=320,margin=dict(t=42,b=10,l=10,r=10))
        st.plotly_chart(fpie,use_container_width=True)
    with rb:
        segs=["Active Equity","Debt/Liquid","ETF/Passive","Pension","Alternatives"]
        fees=[1.10,0.35,0.12,0.08,1.75]
        fb2=go.Figure(go.Bar(x=segs,y=fees,
                             marker_color=[rgba(CG,0.20+i*0.12) for i in range(5)],
                             marker_line_color=CG,marker_line_width=1.5,
                             text=[f"{v:.2f}%" for v in fees],textposition="outside",
                             textfont=dict(size=9,color=FC)))
        fb2.update_layout(**BL(title=dict(text="Average Management Fee by Segment (%)",
                                           font=dict(size=11,color="#c0c8d8",family=FS)),
                               yaxis=dict(ticksuffix="%",gridcolor=GRID,tickfont=dict(size=8,color="#6b7280")),
                               height=320,margin=dict(t=42,b=30,l=10,r=10)))
        st.plotly_chart(fb2,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""<div class="footer">
  UTI Asset Management Company Limited — Institutional Terminal · Feb 25, 2026<br>
  Historical Institutional Audit (FY21–FY25) · Phase-2 Valuation Report (FY25)<br>
  Confidential — Academic / Institutional Use · FCFF DCF · WACC 13.05% · TGR 6.0% · 12.8 Cr Shares
</div>""",unsafe_allow_html=True)
