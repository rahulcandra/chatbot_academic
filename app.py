import base64
import os
import random
import requests
import streamlit as st
from academic_fsm import AcademicFSM, State, ACADEMIC_FACTS

# ── Logo ──────────────────────────────────────────────────────────────────────
def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    UPGRIS_LOGO_B64 = get_base64_of_image("logo_upgris.png")
except FileNotFoundError:
    UPGRIS_LOGO_B64 = ""

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

st.set_page_config(
    page_title="SIKRS — Sistem Informasi KRS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True
if "bot" not in st.session_state:
    st.session_state.bot = AcademicFSM()
    st.session_state.bot.step()
    st.session_state.history = [
        {"role": "assistant", "content": st.session_state.bot.get_response()}
    ]

bot     = st.session_state.bot
is_dark = st.session_state.dark_mode

if is_dark:
    COLORS = {
        "bg":           "#080d18",
        "bg2":          "#0e1525",
        "surface":      "#121c2e",
        "surface2":     "#172236",
        "border":       "#1e3050",
        "primary":      "#4f9eff",
        "primary_bg":   "rgba(79,158,255,0.13)",
        "success":      "#22d3a8",
        "success_bg":   "rgba(34,211,168,0.13)",
        "warning":      "#fbbf24",
        "warning_bg":   "rgba(251,191,36,0.13)",
        "danger":       "#f87171",
        "danger_bg":    "rgba(248,113,113,0.13)",
        "text":         "#e8f0fe",
        "text_muted":   "#7fa8d0",
        "text_faint":   "#3d5875",
        # Banner
        "banner_title":  "#ffffff",
        "banner_sub":    "rgba(255,255,255,0.85)",
        "sidebar_title": "#ffffff",
        "sidebar_sub":   "rgba(255,255,255,0.75)",
    }
else:
    COLORS = {
        "bg":           "#f0f5ff",
        "bg2":          "#ffffff",
        "surface":      "#ffffff",
        "surface2":     "#f5f8ff",
        "border":       "#dde7f5",
        "primary":      "#1a56db",
        "primary_bg":   "#dbeafe",
        "success":      "#059669",
        "success_bg":   "#d1fae5",
        "warning":      "#d97706",
        "warning_bg":   "#fef3c7",
        "danger":       "#dc2626",
        "danger_bg":    "#fee2e2",
        "text":         "#1e2d45",
        "text_muted":   "#5a789e",
        "text_faint":   "#9ab3cc",
        # Banner - light mode needs white on gradient background
        "banner_title":  "#ffffff",
        "banner_sub":    "rgba(255,255,255,0.9)",
        "sidebar_title": "#ffffff",
        "sidebar_sub":   "rgba(255,255,255,0.85)",
    }

C = COLORS

DARK_VARS = f"""
:root {{
    --bg:{C['bg']}; --bg2:{C['bg2']}; --surface:{C['surface']}; --surface2:{C['surface2']};
    --border:{C['border']}; --border-hover:#3a5a8a;
    --primary:{C['primary']}; --primary-light:{C['primary_bg']};
    --success:{C['success']}; --success-light:{C['success_bg']};
    --warning:{C['warning']}; --warning-light:{C['warning_bg']};
    --danger:{C['danger']}; --danger-light:{C['danger_bg']};
    --text:{C['text']}; --text-muted:{C['text_muted']}; --text-faint:{C['text_faint']};
    --radius:12px; --shadow:0 4px 24px rgba(0,0,0,.35);
}}
"""

COMMON_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif !important;
    color: {C['text']} !important;
}}
.stApp {{ background: {C['bg']} !important; }}
section[data-testid="stSidebar"] {{
    background: {C['bg2']} !important;
    border-right: 1px solid {C['border']} !important;
}}
.main .block-container {{
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1340px !important;
}}
.stApp>header, #stDecoration, div[data-testid="stDecoration"] {{ display: none !important; }}
div[data-testid="stHeader"] {{ background: transparent !important; height: 0 !important; min-height: 0 !important; }}
.main>div:first-child {{ padding-top: 0 !important; }}

/* ── FORCE ALL TEXT COLOR ── */
.stApp p, .stApp span, .stApp label,
.stApp li, .stApp strong, .stApp em,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
.stMarkdown, .stMarkdown * {{
    color: {C['text']} !important;
}}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong {{
    color: {C['text']} !important;
}}
[data-testid="stCaptionContainer"] p,
.stApp small {{ color: {C['text_muted']} !important; }}

/* ── SIDEBAR text force ── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] div {{ color: {C['text']} !important; }}

/* ── TABS ── */
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] p {{ color: {C['text_muted']} !important; }}
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] p {{ color: {C['text']} !important; }}

/* ── INPUTS ── */
div[data-testid="stChatInput"] textarea {{
    background: {C['surface2']} !important;
    color: {C['text']} !important;
    caret-color: {C['primary']} !important;
}}
div[data-testid="stChatInput"] textarea::placeholder {{ color: {C['text_faint']} !important; opacity: 1 !important; }}
div[data-testid="stChatInput"]>div {{ background: {C['surface2']} !important; }}
.stTextInput input {{
    background: {C['surface2']} !important;
    color: {C['text']} !important;
    border-color: {C['border']} !important;
}}
.stTextInput input::placeholder {{ color: {C['text_faint']} !important; opacity: 1 !important; }}
.stSelectbox>div>div {{ background: {C['surface2']} !important; color: {C['text']} !important; }}
[data-testid="stSelectbox"] * {{ color: {C['text']} !important; }}

/* ── BUTTONS ── */
.stButton>button {{
    background-color: {C['surface2']} !important;
    color: {C['text']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Sora', sans-serif !important;
    transition: all .15s !important;
}}
.stButton>button:hover {{
    background-color: {C['border']} !important;
    border-color: {C['primary']} !important;
    color: {C['text']} !important;
}}
button[data-testid="baseButton-primary"] {{
    background-color: {C['primary']} !important;
    border-color: {C['primary']} !important;
    color: white !important;
}}
button[data-testid="baseButton-primary"] p,
button[data-testid="baseButton-primary"] span {{
    color: white !important;
}}
button[data-testid="baseButton-primary"]:hover {{ opacity: .9 !important; }}

/* ── EXPANDER ── */
.stExpander {{
    background: {C['surface']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
.stExpander summary, .stExpander summary *,
details summary, details summary * {{
    color: {C['text']} !important;
    background: {C['surface']} !important;
}}
.stExpander > div *, details > div * {{ color: {C['text']} !important; }}
[data-testid="stExpander"] * {{ color: {C['text']} !important; }}

/* ── ALERTS ── */
div[data-testid="stAlert"] {{
    background: {C['surface2']} !important;
    border-color: {C['border']} !important;
}}
div[data-testid="stAlert"] p, div[data-testid="stAlert"] span {{ color: {C['text']} !important; }}

/* ── METRICS ── */
div[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: {C['primary']} !important;
}}
div[data-testid="stMetricLabel"] {{ color: {C['text_muted']} !important; font-size: 13px !important; }}

/* ── CHAT INPUT ── */
div[data-testid="stChatInput"]>div {{
    border-radius: 12px !important;
    border: 1.5px solid {C['border']} !important;
    overflow: hidden !important;
}}
div[data-testid="stChatInput"]>div:focus-within {{
    border-color: {C['primary']} !important;
    box-shadow: 0 0 0 3px rgba(79,158,255,0.15) !important;
}}
.stChatFloatingInputContainer,
.stChatFloatingInputContainer>div,
.stChatFloatingInputContainer>div>div {{ background: {C['bg']} !important; }}

/* ── SIDEBAR padding ── */
section[data-testid="stSidebar"]>div {{ padding: 1.4rem 1.1rem !important; }}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {C['bg2']}; }}
::-webkit-scrollbar-thumb {{ background: {C['border']}; border-radius: 3px; }}

/* ── SKS BAR ── */
.sks-bar-bg {{ background: {C['border']}; border-radius: 999px; height: 10px; margin: 8px 0 4px; overflow: hidden; }}
.sks-bar-fill {{ height: 100%; border-radius: 999px; transition: width .4s ease; }}

/* ── SIDEBAR PROFILE ── */
.sidebar-profile {{
    background: linear-gradient(135deg,#0f2d6e 0%,#1a3a8f 50%,#0ea5e9 100%);
    border-radius: 16px; padding: 18px 16px 16px; text-align: center;
    margin-bottom: 14px; position: relative; overflow: hidden;
    box-shadow: 0 4px 24px rgba(26,86,219,.35);
}}
.sidebar-profile-title {{ font-size: 14px; font-weight: 700; color: #ffffff !important; margin: 0; }}
.sidebar-profile-sub {{ font-size: 11px; color: rgba(255,255,255,0.85) !important; margin: 3px 0 0; }}
.sidebar-profile * {{ color: #ffffff !important; }}
.sidebar-logo-wrap {{
    width: 56px; height: 56px; border-radius: 14px;
    border: 2px solid rgba(255,255,255,.3); background: rgba(255,255,255,.08);
    overflow: hidden; margin: 0 auto 10px;
    display: flex; align-items: center; justify-content: center;
}}

/* ── SIDEBAR SECTION LABEL ── */
.sidebar-section-label {{
    font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: {C['text_muted']} !important;
    margin: 14px 0 8px; padding-left: 2px;
    display: block;
}}
section[data-testid="stSidebar"] .sidebar-section-label {{
    color: {C['text_muted']} !important;
}}

/* ── SKS DASHBOARD ── */
.sks-dashboard {{
    background: {C['surface']}; border: 1px solid {C['border']};
    border-radius: 12px; padding: 14px; margin-bottom: 10px;
}}
.sks-dash-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
.sks-dash-val {{ font-family: 'JetBrains Mono',monospace; font-size: 28px; font-weight: 800; color: {C['primary']}; line-height: 1; }}
.sks-dash-label {{ font-size: 11px; color: {C['text_muted']}; font-weight: 600; letter-spacing: .5px; text-transform: uppercase; }}
.sks-dash-pct {{ font-size: 13px; font-weight: 700; font-family: 'JetBrains Mono',monospace; }}
.sks-dash-mini {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 10px; }}
.sks-mini-card {{ background: {C['surface2']}; border-radius: 8px; padding: 8px 10px; text-align: center; border: 1px solid {C['border']}; }}
.sks-mini-val {{ font-size: 17px; font-weight: 700; font-family: 'JetBrains Mono',monospace; color: {C['text']}; }}
.sks-mini-lbl {{ font-size: 10px; color: {C['text_muted']}; margin-top: 2px; font-weight: 600; }}

/* ── KRS ITEMS ── */
.krs-item-v2 {{
    display: flex; align-items: center; gap: 9px;
    padding: 8px 11px; border-radius: 10px;
    background: {C['surface']}; border: 1px solid {C['border']};
    margin-bottom: 7px;
}}
.krs-emoji-box {{
    width: 34px; height: 34px; border-radius: 8px;
    background: {C['surface2']}; border: 1px solid {C['border']};
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; flex-shrink: 0;
}}
.krs-text {{ flex: 1; min-width: 0; }}
.krs-item-name-v2 {{ font-size: 12.5px; font-weight: 700; color: {C['text']}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.krs-item-code {{ font-size: 10.5px; color: {C['text_muted']}; font-family: 'JetBrains Mono',monospace; margin-top: 1px; }}
.krs-sks-badge {{ background: {C['primary_bg']}; color: {C['primary']}; border-radius: 6px; padding: 3px 7px; font-size: 11.5px; font-weight: 700; font-family: 'JetBrains Mono',monospace; flex-shrink: 0; }}

/* ── NOTIF ITEMS ── */
.notif-item-v2 {{
    display: flex; align-items: flex-start; gap: 8px; padding: 7px 10px;
    border-radius: 8px; background: {C['surface']}; border: 1px solid {C['border']};
    margin-bottom: 5px; font-size: 12px; color: {C['text_muted']};
}}
.notif-pip {{ width: 6px; height: 6px; border-radius: 50%; background: {C['primary']}; flex-shrink: 0; margin-top: 3px; }}

/* ── HEADER BANNER — teks selalu putih karena background gelap ── */
.header-banner {{
    background: linear-gradient(135deg,#0f2d6e 0%,#1a56db 45%,#0ea5e9 100%);
    border-radius: 18px; padding: 22px 30px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 6px 36px rgba(26,86,219,.4); position: relative; overflow: hidden;
}}
.header-banner::before {{
    content: ''; position: absolute; right: -40px; top: -40px;
    width: 220px; height: 220px; border-radius: 50%;
    background: rgba(255,255,255,0.05); pointer-events: none;
}}
.header-banner * {{ color: white !important; }}
.header-title {{ font-size: 22px; font-weight: 800; color: white !important; margin: 0; letter-spacing: -.5px; }}
.header-sub {{ color: rgba(255,255,255,0.85) !important; font-size: 12.5px; margin: 3px 0 0; }}

/* ── LANDING ── */
.landing-hero {{
    min-height: 44vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 2.5rem 2rem 1rem; position: relative;
}}
.landing-logo {{
    width: 160px; height: 160px; object-fit: contain;
    border-radius: 0; border: none; background: transparent; padding: 0;
    filter: drop-shadow(0 6px 24px rgba(79,158,255,.3)); margin-bottom: 22px;
    animation: floatLogo 4s ease-in-out infinite alternate;
}}
@keyframes floatLogo {{ from {{ transform: translateY(0) rotate(-1deg); }} to {{ transform: translateY(-12px) rotate(1deg); }} }}
.landing-title {{ font-size: clamp(28px,4vw,54px); font-weight: 800; color: {C['text']} !important; line-height: 1.08; letter-spacing: -2px; margin: 0 0 14px; }}
.landing-title span.blue {{ color: {C['primary']}; }}
.landing-title span.teal {{ color: #22d3a8; }}
.landing-sub {{ font-size: 15px; color: {C['text_muted']} !important; max-width: 540px; margin: 0 auto 22px; line-height: 1.75; }}
.landing-tags {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 28px; }}
.landing-tag {{ background: {C['surface']}; border: 1px solid {C['border']}; color: {C['text_muted']}; border-radius: 999px; padding: 5px 12px; font-size: 12px; font-weight: 600; }}

/* ── STAT CARD ── */
.dark-stat-card {{ text-align: center; padding: 20px 10px; background: {C['surface']}; border-radius: 14px; border: 1px solid {C['border']}; }}
.dark-stat-val {{ font-size: 32px; font-weight: 800; color: {C['primary']}; font-family: 'JetBrains Mono',monospace; }}
.dark-stat-lbl {{ font-size: 13px; color: {C['text_muted']}; margin-top: 4px; }}

/* ── CARD ── */
.card {{ background: {C['surface']}; border-radius: var(--radius); padding: 18px 20px; border: 1px solid {C['border']}; margin-bottom: 14px; }}

/* ── CATALOG TIGHT BUTTON ── */
.catalog-btn-wrap {{ margin-top: 0 !important; padding-top: 0 !important; }}
"""

st.markdown(f"<style>{DARK_VARS}{COMMON_CSS}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: render catalog card sebagai st.markdown (tanpa iframe)
# ─────────────────────────────────────────────
def render_catalog_card(key, data, in_krs):
    nama = key.replace("_", " ").title()
    krs_badge = ""
    if in_krs:
        krs_badge = (
            f'<span style="background:{C["success_bg"]};color:{C["success"]};'
            f'border-radius:6px;padding:2px 10px;font-size:11px;font-weight:700;'
            f'white-space:nowrap;">✅ Di KRS</span>'
        )
    kat_color = C["warning"] if data["kategori"] == "Wajib" else C["success"]
    kat_bg    = C["warning_bg"] if data["kategori"] == "Wajib" else C["success_bg"]
    tag_style = (
        f'display:inline-block;border-radius:6px;padding:3px 8px;font-size:11px;'
        f'font-weight:600;margin:2px 2px 0 0;background:{C["surface2"]};color:{C["text_muted"]};'
    )
    return f"""
<div style="background:{C['surface']};border-radius:14px;padding:14px 16px;
     border:1px solid {C['border']};box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:6px;">
  <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:8px;">
    <span style="font-size:26px;line-height:1.1;flex-shrink:0;">{data['emoji']}</span>
    <div style="flex:1;min-width:0;">
      <div style="font-size:14px;font-weight:700;color:{C['text']};">{nama}</div>
      <div style="font-size:11px;color:{C['text_muted']};margin-top:2px;">Semester {data['semester']} · {data['kode']}</div>
    </div>
    {krs_badge}
  </div>
  <div style="font-size:12px;color:{C['text_muted']};margin-bottom:8px;line-height:1.55;">{data['desc']}</div>
  <div>
    <span style="{tag_style}background:{C['primary_bg']};color:{C['primary']};">{data['sks']} SKS</span>
    <span style="{tag_style}background:{kat_bg};color:{kat_color};">{data['kategori']}</span>
    <span style="{tag_style}">🕐 {data['jadwal']}</span>
    <span style="{tag_style}">📍 {data['ruang']}</span>
    <span style="{tag_style}">👨‍🏫 {data['dosen']}</span>
  </div>
</div>"""


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    if UPGRIS_LOGO_B64:
        logo_inner = f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" style="width:48px;height:48px;object-fit:contain;" alt="UPGRIS"/>'
    else:
        logo_inner = '<span style="font-size:28px;">🎓</span>'

    st.markdown(f"""
    <div class="sidebar-profile">
        <div class="sidebar-logo-wrap">{logo_inner}</div>
        <p class="sidebar-profile-title">SIKRS · UPGRIS</p>
        <p class="sidebar-profile-sub">Sistem Informasi KRS 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-section-label">🎨 Tema Tampilan</div>', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("🌙 Gelap", use_container_width=True, key="btn_dark",
                     type="primary" if is_dark else "secondary"):
            st.session_state.dark_mode = True; st.rerun()
    with col_t2:
        if st.button("☀️ Terang", use_container_width=True, key="btn_light",
                     type="primary" if not is_dark else "secondary"):
            st.session_state.dark_mode = False; st.rerun()

    st.markdown(f'<div class="sidebar-section-label">🧭 Navigasi</div>', unsafe_allow_html=True)
    if st.session_state.show_landing:
        if st.button("🚀 Masuk ke Aplikasi", use_container_width=True, type="primary"):
            st.session_state.show_landing = False; st.rerun()
    else:
        if st.button("🏠 Kembali ke Beranda", use_container_width=True):
            st.session_state.show_landing = True; st.rerun()

    if not st.session_state.show_landing:
        total_sks = bot.total_sks()
        max_sks   = bot.nlp.MAX_SKS
        pct       = int(total_sks / max_sks * 100)
        bar_color = "#f87171" if pct >= 90 else "#fbbf24" if pct >= 70 else "#4f9eff"
        status_emoji = "🔴" if pct >= 90 else "🟡" if pct >= 70 else "🟢"
        status_txt   = "Hampir Penuh" if pct >= 90 else "Mendekati Batas" if pct >= 70 else "Aman"

        st.markdown(f'<div class="sidebar-section-label">📊 Dashboard KRS</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sks-dashboard">
            <div class="sks-dash-header">
                <div>
                    <div class="sks-dash-label">Total SKS</div>
                    <div class="sks-dash-val" style="color:{bar_color};">{total_sks}<span style="font-size:14px;color:{C['text_muted']};font-weight:400;">/{max_sks}</span></div>
                </div>
                <div style="text-align:right;">
                    <div class="sks-dash-pct" style="color:{bar_color};">{pct}%</div>
                    <div style="font-size:11px;color:{C['text_muted']};">{status_emoji} {status_txt}</div>
                </div>
            </div>
            <div class="sks-bar-bg">
                <div class="sks-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
            </div>
            <div class="sks-dash-mini">
                <div class="sks-mini-card">
                    <div class="sks-mini-val" style="color:{bar_color};">{total_sks}</div>
                    <div class="sks-mini-lbl">DIAMBIL</div>
                </div>
                <div class="sks-mini-card">
                    <div class="sks-mini-val">{max_sks - total_sks}</div>
                    <div class="sks-mini-lbl">TERSISA</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if bot.notifications:
            st.markdown(f'<div class="sidebar-section-label">🔔 Notifikasi Terbaru</div>', unsafe_allow_html=True)
            for n in reversed(bot.notifications[-3:]):
                st.markdown(f'<div class="notif-item-v2"><div class="notif-pip"></div><span style="color:{C["text_muted"]}">{n}</span></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="sidebar-section-label">🗂️ Mata Kuliah Dipilih</div>', unsafe_allow_html=True)
        if bot.cart:
            for c in bot.cart:
                nama = c["course_key"].replace("_", " ").title()
                st.markdown(f"""
                <div class="krs-item-v2">
                    <div class="krs-emoji-box">{c['emoji']}</div>
                    <div class="krs-text">
                        <div class="krs-item-name-v2">{nama}</div>
                        <div class="krs-item-code">{c['kode']}</div>
                    </div>
                    <span class="krs-sks-badge">{c['sks']} SKS</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🗑️ Kosongkan KRS", use_container_width=True, type="secondary"):
                bot.cart = []
                st.session_state.history.append({"role": "assistant", "content": "🗑️ KRS berhasil dikosongkan."})
                st.rerun()
        else:
            st.info("Belum ada matkul dipilih.", icon="📭")

        st.markdown(f'<div class="sidebar-section-label">⚙️ Sistem</div>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔄 Reset", use_container_width=True):
                dark_backup = st.session_state.dark_mode
                st.session_state.clear()
                st.session_state.dark_mode    = dark_backup
                st.session_state.show_landing = False
                st.rerun()
        with cb:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.history = []
                st.rerun()

    st.markdown("---")
    st.caption("SIKRS 2026 · Universitas PGRI Semarang\nPowered by Rahul Candra")


# ═════════════════════════════════════════════
# LANDING PAGE
# ═════════════════════════════════════════════
if st.session_state.show_landing:
    logo_html = (
        f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" class="landing-logo" alt="Logo UPGRIS" />'
        if UPGRIS_LOGO_B64
        else '<div style="font-size:100px;margin-bottom:20px;">🎓</div>'
    )

    st.markdown(f"""
    <div class="landing-hero">
        {logo_html}
        <h1 class="landing-title">Susun KRS Lebih<br><span class="blue">Cerdas</span> & <span class="teal">Cepat</span></h1>
        <p class="landing-sub">
            SIKRS adalah chatbot akademik berbasis <strong>Finite State Machine</strong>
            yang membantu mahasiswa Teknik Informatika UPGRIS menyusun KRS dengan data jadwal
            real, validasi prasyarat, deteksi konflik jadwal, dan tips belajar otomatis.
        </p>
        <div class="landing-tags">
            <span class="landing-tag">🤖 NLP Engine</span>
            <span class="landing-tag">⚡ Validasi Real-time</span>
            <span class="landing-tag">📅 Data Jadwal Resmi</span>
            <span class="landing-tag">🎯 Rekomendasi Cerdas</span>
            <span class="landing-tag">🔔 Notifikasi Live</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_matkul = len(bot.nlp.course_data)
    s1, s2, s3, s4 = st.columns(4)
    for col, (val, lbl) in zip([s1, s2, s3, s4], [(str(total_matkul),"Mata Kuliah"),("24","Maks SKS"),("4","State FSM"),("9","Fitur Utama")]):
        with col:
            st.markdown(f'<div class="dark-stat-card"><div class="dark-stat-val">{val}</div><div class="dark-stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<h3 style="color:{C["text"]};">✨ Fitur Unggulan SIKRS</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{C["text_muted"]};font-size:14px;margin-bottom:16px;">Klik setiap fitur untuk melihat detail</p>', unsafe_allow_html=True)

    features = [
        ("🤖","Chatbot NLP Pintar","Pahami perintah natural bahasa Indonesia","Baru",
         "Ketik perintah seperti <b>'ambil struktur data'</b> atau <b>'rekomen matkul'</b>. NLP Engine berbasis Regex mengenali sinonim dan variasi penulisan nama matkul secara otomatis."),
        ("⚠️","Validasi Real-time","Cek prasyarat, konflik jadwal & batas 24 SKS","Wajib",
         "Sistem otomatis memeriksa prasyarat, bentrokan jadwal, dan kapasitas SKS setiap kali Anda menambah mata kuliah."),
        ("💡","Tips Belajar Spesifik","Tips personal untuk setiap mata kuliah","Wajib",
         "Setiap matkul dilengkapi tips belajar spesifik dari rekomendasi tools hingga strategi ujian."),
        ("🔔","Panel Notifikasi","Riwayat 5 perubahan KRS terakhir di sidebar","Pilihan",
         "Setiap aksi tambah/hapus matkul dan submit KRS dicatat sebagai notifikasi real-time di sidebar."),
        ("🎯","Rekomendasi Cerdas","Saran matkul berdasarkan KRS aktif Anda","Baru",
         "Sistem menganalisis pilihan matkul Anda dan merekomendasikan matkul lain yang prasyaratnya sudah terpenuhi."),
        ("📅","Jadwal Visual per Hari","Tampilan jadwal terurut Senin–Sabtu + submit","Wajib",
         "Tab Jadwal menampilkan semua matkul KRS terurut per hari dalam card rapi, lengkap ruangan, dosen, dan jam."),
        ("🎨","Tema Gelap & Terang","Ganti tema kapan saja tanpa kehilangan data","Pilihan",
         "Dark mode untuk coding malam dan light mode untuk siang hari. Ganti via sidebar kapan saja."),
    ]
    badge_styles = {
        "Baru":    (C["primary"],    C["primary_bg"]),
        "Wajib":   (C["success"],    C["success_bg"]),
        "Pilihan": (C["text_muted"], C["surface2"]),
    }
    for row_start in range(0, len(features), 3):
        row  = features[row_start:row_start+3]
        cols = st.columns(3)
        for col, (icon, name, short, badge, detail) in zip(cols, row):
            bc, bb = badge_styles.get(badge, (C["text_muted"], C["surface2"]))
            with col:
                with st.expander(f"{icon} **{name}**"):
                    st.markdown(
                        f'<div style="padding:4px 0 10px;">'
                        f'<span style="background:{bb};color:{bc};border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700;display:inline-block;margin-bottom:10px;">{badge}</span>'
                        f'<p style="color:{C["text_muted"]};font-style:italic;font-size:13px;margin:0 0 8px;">{short}</p>'
                        f'<p style="color:{C["text"]};font-size:13.5px;line-height:1.75;margin:0;">{detail}</p>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    st.markdown("---")
    cta2 = st.columns([1, 2, 1])
    with cta2[1]:
        if st.button("🚀 Mulai Sekarang!", use_container_width=True, type="primary"):
            st.session_state.show_landing = False; st.rerun()

    st.markdown(
        f'<div style="text-align:center;color:{C["text_faint"]};font-size:12px;margin-top:28px;line-height:2;">'
        f'SIKRS 2026 · Universitas PGRI Semarang<br>'
        f'Powered by <strong style="color:{C["primary"]};">Rahul Candra</strong> · Teknik Informatika</div>',
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════
# HALAMAN APLIKASI UTAMA
# ═════════════════════════════════════════════
else:
    logo_img = (
        f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" '
        f'style="width:80px;height:80px;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));" alt="UPGRIS" />'
        if UPGRIS_LOGO_B64
        else '<div style="font-size:46px;">🎓</div>'
    )

    # Header — teks putih karena gradient selalu gelap
    st.markdown(f"""
    <div class="header-banner">
        {logo_img}
        <div>
            <p class="header-title">SIKRS — Chatbot Akademik UPGRIS</p>
            <p class="header-sub">Sistem Informasi Kartu Rencana Studi · Teknik Informatika · Universitas PGRI Semarang</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_chat, tab_catalog, tab_schedule, tab_tips, tab_about = st.tabs([
        "💬 Chatbot KRS", "📚 Katalog Matkul", "📅 Jadwal Saya", "💡 Tips & Fakta", "ℹ️ Panduan",
    ])

    # ═══════════════════════════════
    # TAB 1 — CHATBOT FSM
    # ═══════════════════════════════
    with tab_chat:
        chat_col, _ = st.columns([3, 0.01])
        with chat_col:
            chat_container = st.container(height=520)
            with chat_container:
                for msg in st.session_state.history:
                    avatar = "🎓" if msg["role"] == "assistant" else "🧑‍🎓"
                    with st.chat_message(msg["role"], avatar=avatar):
                        st.markdown(msg["content"])

            prompt = st.chat_input("Contoh: ambil struktur data / info matdis / rekomen / tips web")
            if prompt:
                st.session_state.history.append({"role": "user", "content": prompt})
                bot.step(prompt)
                st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                st.rerun()

            st.markdown(f'<p style="color:{C["text"]};font-weight:700;font-size:14px;margin-bottom:8px;">⚡ Aksi Cepat:</p>', unsafe_allow_html=True)
            q1, q2, q3, q4, q5, q6 = st.columns(6)
            quick_actions = [
                ("📚 Menu", "menu"), ("🎯 Rekomen", "rekomen"), ("📅 Jadwal", "jadwal"),
                ("📊 SKS", "total sks saya"), ("📤 Submit", "submit KRS"), ("❓ Bantuan", "bantuan"),
            ]
            for col, (label, cmd) in zip([q1, q2, q3, q4, q5, q6], quick_actions):
                with col:
                    if st.button(label, use_container_width=True, key=f"qa_{cmd}"):
                        st.session_state.history.append({"role": "user", "content": cmd})
                        bot.step(cmd)
                        st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                        st.rerun()

    # ═══════════════════════════════
    # TAB 2 — KATALOG
    # Tombol mepet langsung di bawah card
    # ═══════════════════════════════
    with tab_catalog:
        st.markdown(f'<h3 style="color:{C["text"]};">📚 Katalog Mata Kuliah</h3>', unsafe_allow_html=True)
        st.caption("Data jadwal real UPGRIS Semester Genap 2025/2026")
        st.markdown("---")

        fc1, fc2, fc3 = st.columns([1, 1, 2])
        with fc1: filter_kat = st.selectbox("Kategori", ["Semua", "Wajib", "Pilihan"])
        with fc2: filter_sem = st.selectbox("Semester", ["Semua", "2", "4", "6", "8"])
        with fc3: search_q   = st.text_input("🔍 Cari matkul atau dosen...", placeholder="contoh: web, Ramadhan, IoT")

        st.markdown("---")

        filtered = []
        for key, data in bot.nlp.course_data.items():
            nama = key.replace("_", " ").title()
            if filter_kat != "Semua" and data["kategori"] != filter_kat: continue
            if filter_sem != "Semua" and str(data["semester"]) != filter_sem: continue
            if search_q:
                sq = search_q.lower()
                if not any(sq in x for x in [key, data["kode"].lower(), data["dosen"].lower(), nama.lower()]):
                    continue
            filtered.append((key, data))

        if not filtered:
            st.info("Tidak ada matkul yang sesuai filter.", icon="🔍")
        else:
            for i in range(0, len(filtered), 2):
                pair = filtered[i:i+2]
                cols = st.columns(2)
                for col_idx, (key, data) in enumerate(pair):
                    nama   = key.replace("_", " ").title()
                    in_krs = any(c["course_key"] == key for c in bot.cart)
                    with cols[col_idx]:
                        with st.container():
                            st.markdown(render_catalog_card(key, data, in_krs), unsafe_allow_html=True)
                            if in_krs:
                                if st.button(
                                    f"🗑️ Hapus dari KRS",
                                    key=f"rem_{key}",
                                    use_container_width=True,
                                ):
                                    msg = bot.remove_course(key)
                                    st.session_state.history.append({"role": "assistant", "content": msg})
                                    st.rerun()
                            else:
                                if st.button(
                                    f"➕ Tambah ke KRS",
                                    key=f"add_{key}",
                                    use_container_width=True,
                                    type="primary",
                                ):
                                    success, msg = bot.add_course(key)
                                    st.session_state.history.append({"role": "user", "content": f"ambil {nama}"})
                                    st.session_state.history.append({"role": "assistant", "content": msg})
                                    st.rerun()
                st.markdown("---")

    # ═══════════════════════════════
    # TAB 3 — JADWAL
    # ═══════════════════════════════
    with tab_schedule:
        st.markdown(f'<h3 style="color:{C["text"]};">📅 Jadwal Kuliah Saya</h3>', unsafe_allow_html=True)
        st.markdown("---")

        if not bot.cart:
            st.info("Belum ada mata kuliah dalam KRS.\nTambahkan dari **Katalog** atau via **Chat**.", icon="📭")
        else:
            days_order = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
            by_day = {d: [] for d in days_order}
            for c in bot.cart:
                for day in days_order:
                    if day in c["jadwal"]:
                        by_day[day].append(c); break

            for day in days_order:
                if not by_day[day]: continue
                st.markdown(f"#### 📆 {day}")
                for c in by_day[day]:
                    nama = c["course_key"].replace("_", " ").title()
                    jam  = c["jadwal"].split(" ", 1)[1] if " " in c["jadwal"] else c["jadwal"]
                    cl1, cl2, cl3, cl4 = st.columns([0.4, 2.2, 2, 1])
                    with cl1:
                        st.markdown(f'<div style="font-size:26px;text-align:center">{c["emoji"]}</div>', unsafe_allow_html=True)
                    with cl2:
                        st.markdown(f"**{nama}**")
                        st.caption(f"⏰ {jam}")
                    with cl3:
                        st.markdown(f"📍 {c['ruang']}")
                        st.caption(f"👨‍🏫 {c['dosen']}")
                    with cl4:
                        st.markdown(f"""<div style="background:{C['primary_bg']};color:{C['primary']};
border-radius:8px;padding:7px 12px;text-align:center;font-weight:700;
font-family:'JetBrains Mono',monospace;">{c['sks']} SKS</div>""", unsafe_allow_html=True)
                st.markdown("---")

            pct = int(bot.total_sks() / bot.nlp.MAX_SKS * 100)
            bar_color = "#f87171" if pct >= 90 else "#fbbf24" if pct >= 70 else "#4f9eff"
            st.markdown(f"**Total: {bot.total_sks()} SKS** dari maksimum {bot.nlp.MAX_SKS} SKS")
            st.markdown(f"""
<div class="sks-bar-bg" style="max-width:400px;">
    <div class="sks-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
</div>
<div style="font-size:12px;color:{C['text_muted']};">{pct}% terisi</div>
""", unsafe_allow_html=True)

            if bot.state == State.BROWSING:
                st.markdown("")
                if st.button("📤 Submit KRS Sekarang", type="primary"):
                    bot.step("submit KRS")
                    st.session_state.history.append({"role": "user", "content": "submit KRS"})
                    st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                    st.rerun()

    # ═══════════════════════════════
    # TAB 4 — TIPS & FAKTA
    # ═══════════════════════════════
    with tab_tips:
        st.markdown(f'<h3 style="color:{C["text"]};">💡 Tips Belajar & Fakta Akademik</h3>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown(f'<h4 style="color:{C["text"]};">🧠 Fakta & Strategi Belajar</h4>', unsafe_allow_html=True)
        fact_cols = st.columns(2)
        for i, fact in enumerate(ACADEMIC_FACTS):
            with fact_cols[i % 2]:
                st.markdown(f"""
<div class="card" style="border-left:3px solid {C['primary']};">
    <div style="font-size:14px;line-height:1.7;color:{C['text']};">{fact}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f'<h4 style="color:{C["text"]};">📚 Tips Per Mata Kuliah</h4>', unsafe_allow_html=True)
        for key, data in bot.nlp.course_data.items():
            nama  = key.replace("_", " ").title()
            stars = "⭐" * data["difficulty"] + "☆" * (5 - data["difficulty"])
            with st.expander(f"{data['emoji']} {nama} — Tips Belajar"):
                st.markdown(
                    f'<div style="padding:6px 0;">'
                    f'<p style="color:{C["text"]};margin:0 0 6px;"><strong>Tingkat Kesulitan:</strong> {stars} ({data["difficulty"]}/5)</p>'
                    f'<p style="color:{C["text"]};margin:0 0 6px;"><strong>Dosen:</strong> {data["dosen"]}</p>'
                    f'<p style="color:{C["text"]};margin:0 0 10px;"><strong>Jadwal:</strong> {data["jadwal"]} · {data["ruang"]}</p>'
                    f'<div style="background:{C["primary_bg"]};border-left:3px solid {C["primary"]};'
                    f'border-radius:0 8px 8px 0;padding:10px 14px;font-size:13.5px;'
                    f'color:{C["text_muted"]};font-style:italic;line-height:1.7;">💡 {data["tips"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown(f'<h4 style="color:{C["text"]};">🏆 Perbandingan Kesulitan Matkul</h4>', unsafe_allow_html=True)
        for nama, diff in sorted(
            {k.replace("_", " ").title(): d["difficulty"] for k, d in bot.nlp.course_data.items()}.items(),
            key=lambda x: -x[1],
        ):
            bar = "█" * diff + "░" * (5 - diff)
            st.markdown(f"`{bar}` {nama} ({diff}/5)")

    # ═══════════════════════════════
    # TAB 5 — PANDUAN
    # ═══════════════════════════════
    with tab_about:
        st.markdown(f'<h3 style="color:{C["text"]};">ℹ️ Panduan & Informasi Sistem</h3>', unsafe_allow_html=True)
        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"""
<div style="color:{C['text']};">

#### 🤖 Tentang SIKRS
Chatbot ini menggunakan **Finite State Machine (FSM)** dengan **NLP Engine berbasis Regex** untuk membantu mahasiswa Teknik Informatika **UPGRIS** menyusun KRS.

**State FSM:**

| State | Ikon | Keterangan |
|-------|------|-----------|
| Browsing | 🟢 | Menjelajah & menambah matkul |
| Konfirmasi | 🟠 | Verifikasi sebelum submit |
| Selesai | 🔵 | KRS berhasil disubmit |

---
#### ✨ Fitur Lengkap
1. 💬 **Chatbot KRS** — FSM-based, perintah natural bahasa Indonesia
2. 📚 **Katalog Interaktif** — Filter semester, kategori, pencarian
3. 🛒 **Manajemen KRS** — Tambah/hapus via chat atau tombol
4. ⚠️ **Validasi Otomatis** — Prasyarat, konflik jadwal, batas SKS
5. 🎯 **Rekomendasi AI** — Saran matkul berdasarkan KRS aktif
6. 💡 **Tips Belajar** — Tips spesifik per matkul
7. 🔔 **Notifikasi** — Panel riwayat perubahan KRS
8. 📅 **Jadwal Visual** — Tersusun per hari + submit langsung
9. 🎨 **Tema Gelap/Terang** — Ganti tema kapan saja
</div>
""", unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
<div style="color:{C['text']};">

#### 💬 Contoh Perintah Chat
```
menu                    → lihat semua matkul
ambil matdis            → tambah ke KRS
hapus sistem operasi    → hapus dari KRS
hapus semua             → kosongkan KRS
jadwal                  → lihat jadwal
total sks               → cek kapasitas SKS
info pemrograman web    → detail matkul
prasyarat aps           → cek syarat
dosen iot               → info dosen + jadwal
susah matdis            → tingkat kesulitan
tips web                → tips belajar
rekomen                 → rekomendasi matkul
krs saya                → ringkasan KRS
submit KRS              → konfirmasi & kirim
reset                   → mulai ulang
bantuan                 → panduan ini
```

#### 📋 Aturan KRS
- **Maksimum SKS:** 24 SKS per semester
- **Prasyarat:** Beberapa matkul butuh matkul lain di KRS
- **Konflik:** Jadwal yang sama tidak bisa diambil bersamaan
- **Data jadwal:** Real dari UPGRIS Sem. Genap 2025/2026
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
<div style='text-align:center;color:{C["text_muted"]};font-size:13px;padding:10px;'>
SIKRS 2026 · Dikembangkan oleh <b>Rahul Candra</b><br>
Finite State Machine + NLP Engine<br>
Program Studi Teknik Informatika · <b>Universitas PGRI Semarang</b>
</div>
""", unsafe_allow_html=True)