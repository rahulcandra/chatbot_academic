import base64
import random
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
    C = {
        "bg":          "#080d18",
        "bg2":         "#0e1525",
        "surface":     "#121c2e",
        "surface2":    "#172236",
        "border":      "#1e3050",
        "primary":     "#4f9eff",
        "primary_bg":  "rgba(79,158,255,0.13)",
        "success":     "#22d3a8",
        "success_bg":  "rgba(34,211,168,0.13)",
        "warning":     "#fbbf24",
        "warning_bg":  "rgba(251,191,36,0.13)",
        "danger":      "#f87171",
        "danger_bg":   "rgba(248,113,113,0.13)",
        "text":        "#e8f0fe",
        "text_muted":  "#7fa8d0",
        "text_faint":  "#3d5875",
    }
else:
    C = {
        "bg":          "#f0f5ff",
        "bg2":         "#ffffff",
        "surface":     "#ffffff",
        "surface2":    "#eef3ff",
        "border":      "#ccd8f0",
        "primary":     "#1a56db",
        "primary_bg":  "#dbeafe",
        "success":     "#059669",
        "success_bg":  "#d1fae5",
        "warning":     "#b45309",
        "warning_bg":  "#fef3c7",
        "danger":      "#dc2626",
        "danger_bg":   "#fee2e2",
        "text":        "#1e2d45",
        "text_muted":  "#4a6080",
        "text_faint":  "#8ca3c0",
    }

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif !important;
}}

/* ── App & Sidebar background ── */
.stApp {{ background: {C['bg']} !important; }}
section[data-testid="stSidebar"] {{
    background: {C['bg2']} !important;
    border-right: 1px solid {C['border']} !important;
}}
.main .block-container {{
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1340px !important;
}}

/* ── Hide default header decoration ── */
.stApp>header, #stDecoration, div[data-testid="stDecoration"] {{ display:none !important; }}
div[data-testid="stHeader"] {{ background:transparent !important; height:0 !important; min-height:0 !important; }}
.main>div:first-child {{ padding-top:0 !important; }}

/* ── Global text color ── */
.stApp p, .stApp span, .stApp label, .stApp li,
.stApp strong, .stApp em, .stApp h1, .stApp h2,
.stApp h3, .stApp h4, .stApp h5,
.stMarkdown, .stMarkdown * {{
    color: {C['text']} !important;
}}

/* ── Chat messages ── */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] code,
[data-testid="stChatMessage"] pre,
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol,
[data-testid="stChatMessage"] a {{
    color: {C['text']} !important;
}}
[data-testid="stChatMessage"] code {{
    background: {C['surface2']} !important;
    color: {C['primary']} !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}}
[data-testid="stCaptionContainer"] p, .stApp small {{
    color: {C['text_muted']} !important;
}}

/* ── Sidebar text (non-gradient) ── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] div {{
    color: {C['text']} !important;
}}

/* ── CRITICAL OVERRIDE: gradient card elements always white ── */
section[data-testid="stSidebar"] [data-white] p,
section[data-testid="stSidebar"] [data-white] span,
section[data-testid="stSidebar"] [data-white] div,
section[data-testid="stSidebar"] [data-white] {{
    color: #ffffff !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] p {{ color: {C['text_muted']} !important; }}
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] p {{ color: {C['text']} !important; }}

/* ── Chat Input ── */
div[data-testid="stChatInput"] textarea {{
    background: {C['surface2']} !important;
    color: {C['text']} !important;
    caret-color: {C['primary']} !important;
}}
div[data-testid="stChatInput"] textarea::placeholder {{
    color: {C['text_faint']} !important; opacity:1 !important;
}}
div[data-testid="stChatInput"]>div {{ background: {C['surface2']} !important; }}
div[data-testid="stChatInput"]>div {{
    border-radius:12px !important;
    border:1.5px solid {C['border']} !important;
    overflow:hidden !important;
}}
div[data-testid="stChatInput"]>div:focus-within {{
    border-color:{C['primary']} !important;
    box-shadow:0 0 0 3px rgba(79,158,255,0.15) !important;
}}
.stChatFloatingInputContainer,
.stChatFloatingInputContainer>div,
.stChatFloatingInputContainer>div>div {{
    background: {C['bg']} !important;
}}

/* ── Chat send button — blue bg, white arrow, NO inner white box ── */
div[data-testid="stChatInput"] button {{
    background-color: {C['primary']} !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    visibility: visible !important;
}}
div[data-testid="stChatInput"] button:hover {{
    background-color: {C['primary']} !important;
    opacity: 0.85 !important;
}}
div[data-testid="stChatInput"] button span,
div[data-testid="stChatInput"] button div {{
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}}
div[data-testid="stChatInput"] button svg {{
    fill: #ffffff !important;
    stroke: none !important;
    border: none !important;
    outline: none !important;
}}
div[data-testid="stChatInput"] button svg rect,
div[data-testid="stChatInput"] button svg path[stroke] {{
    stroke: none !important;
    fill: #ffffff !important;
}}

/* ── Form inputs ── */
.stTextInput input {{
    background: {C['surface2']} !important;
    color: {C['text']} !important;
    border-color: {C['border']} !important;
}}
.stTextInput input::placeholder {{
    color: {C['text_faint']} !important; opacity:1 !important;
}}
.stSelectbox>div>div {{ background:{C['surface2']} !important; color:{C['text']} !important; }}
[data-testid="stSelectbox"] * {{ color:{C['text']} !important; }}

/* ── Buttons ── */
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
}}
button[data-testid="baseButton-primary"] {{
    background-color: {C['primary']} !important;
    border-color: {C['primary']} !important;
    color: white !important;
}}
button[data-testid="baseButton-primary"] p,
button[data-testid="baseButton-primary"] span {{ color:white !important; }}
button[data-testid="baseButton-primary"]:hover {{ opacity:.9 !important; }}

/* ── Expander ── */
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
.stExpander > div *, details > div * {{ color:{C['text']} !important; }}
[data-testid="stExpander"] * {{ color:{C['text']} !important; }}

/* ── Alert / Info ── */
div[data-testid="stAlert"] {{
    background: {C['surface2']} !important;
    border-color: {C['border']} !important;
}}
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {{ color:{C['text']} !important; }}

/* ── Metric ── */
div[data-testid="stMetricValue"] {{
    font-family:'JetBrains Mono',monospace !important;
    font-size:22px !important; font-weight:700 !important;
    color:{C['primary']} !important;
}}
div[data-testid="stMetricLabel"] {{
    color:{C['text_muted']} !important; font-size:13px !important;
}}

/* ── Sidebar layout ── */
section[data-testid="stSidebar"]>div {{ padding:1.4rem 1.1rem !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background:{C['bg2']}; }}
::-webkit-scrollbar-thumb {{ background:{C['border']}; border-radius:3px; }}

/* ════════════════════════════════════════════════
   GRADIENT SECTIONS — always white text
   (must come AFTER the global color rules above
   so specificity wins in both dark & light mode)
   ════════════════════════════════════════════════ */

/* ── Sidebar Profile ── */
.sidebar-profile {{
    background: linear-gradient(135deg,#0f2d6e 0%,#1a3a8f 50%,#0ea5e9 100%);
    border-radius:16px; padding:18px 16px 16px; text-align:center;
    margin-bottom:14px; box-shadow:0 4px 24px rgba(26,86,219,.35);
    position:relative; overflow:hidden;
}}
.sidebar-profile,
.sidebar-profile p,
.sidebar-profile span,
.sidebar-profile div,
.sidebar-profile * {{
    color: #ffffff !important;
}}
.sidebar-logo-wrap {{
    width:56px; height:56px; border-radius:14px;
    border:2px solid rgba(255,255,255,.3); background:rgba(255,255,255,.08);
    overflow:hidden; margin:0 auto 10px;
    display:flex; align-items:center; justify-content:center;
}}

/* ── Header Banner ── */
.header-banner {{
    background:linear-gradient(135deg,#0f2d6e 0%,#1a56db 45%,#0ea5e9 100%);
    border-radius:18px; padding:22px 30px; margin-bottom:20px;
    display:flex; align-items:center; gap:18px;
    box-shadow:0 6px 36px rgba(26,86,219,.4);
    position:relative; overflow:hidden;
}}
.header-banner::before {{
    content:''; position:absolute; right:-40px; top:-40px;
    width:220px; height:220px; border-radius:50%;
    background:rgba(255,255,255,0.05); pointer-events:none;
}}
.header-banner,
.header-banner p,
.header-banner span,
.header-banner div,
.header-banner strong,
.header-banner em,
.header-banner * {{
    color: #ffffff !important;
}}
.header-title {{
    font-size:22px; font-weight:800; margin:0; letter-spacing:-.5px;
}}
.header-sub {{
    font-size:12.5px; margin:3px 0 0; opacity:.85;
}}

/* ── Dashboard Card ── */
.dash-card {{
    background: linear-gradient(135deg,#0f2d6e 0%,#1a56db 60%,#0ea5e9 100%);
    border-radius:16px; padding:20px 22px 16px; margin-bottom:10px;
    box-shadow:0 8px 32px rgba(26,86,219,.35);
    position:relative; overflow:hidden;
}}
.dash-card::before {{
    content:''; position:absolute; right:-30px; top:-30px;
    width:160px; height:160px; border-radius:50%;
    background:rgba(255,255,255,0.06); pointer-events:none;
}}
.dash-card,
.dash-card p,
.dash-card span,
.dash-card div,
.dash-card strong,
.dash-card em,
.dash-card * {{
    color: #ffffff !important;
}}
.dash-label {{
    font-size:10px; font-weight:700; letter-spacing:1.8px;
    text-transform:uppercase; opacity:.75; margin-bottom:6px;
}}
.dash-value {{
    font-family:'JetBrains Mono',monospace;
    font-size:42px; font-weight:800; line-height:1; letter-spacing:-2px;
}}
.dash-value span {{ font-size:18px; font-weight:400; opacity:.65; }}
.dash-status {{ font-size:12px; font-weight:600; margin-top:4px; opacity:.85; }}
.dash-bar-wrap {{
    margin:14px 0 12px;
    background:rgba(255,255,255,.18);
    border-radius:999px; height:7px; overflow:hidden;
}}
.dash-bar-inner {{
    height:100%; border-radius:999px;
    background:rgba(255,255,255,.9);
    transition:width .5s cubic-bezier(.4,0,.2,1);
}}
.dash-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }}
.dash-mini {{
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.18);
    border-radius:10px; padding:10px 12px; text-align:center;
}}
.dash-mini-val {{
    font-family:'JetBrains Mono',monospace;
    font-size:22px; font-weight:800; line-height:1;
}}
.dash-mini-lbl {{
    font-size:9px; font-weight:700; letter-spacing:1.2px;
    text-transform:uppercase; opacity:.7; margin-top:3px;
}}

/* ── Sidebar section label ── */
.sbl {{
    font-size:10px; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; color:{C['text_faint']} !important;
    margin:14px 0 8px; display:block;
}}

/* ── KRS Items in sidebar ── */
.krs-item {{
    display:flex; align-items:center; gap:9px;
    padding:8px 11px; border-radius:10px;
    background:{C['surface']}; border:1px solid {C['border']};
    margin-bottom:7px;
}}
.krs-emoji-box {{
    width:34px; height:34px; border-radius:8px;
    background:{C['surface2']}; border:1px solid {C['border']};
    display:flex; align-items:center; justify-content:center;
    font-size:17px; flex-shrink:0;
}}
.krs-text {{ flex:1; min-width:0; }}
.krs-name {{
    font-size:12.5px; font-weight:700; color:{C['text']};
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.krs-code {{
    font-size:10.5px; color:{C['text_muted']};
    font-family:'JetBrains Mono',monospace; margin-top:1px;
}}
.krs-sks-badge {{
    background:{C['primary_bg']}; color:{C['primary']};
    border-radius:6px; padding:3px 7px; font-size:11.5px;
    font-weight:700; font-family:'JetBrains Mono',monospace; flex-shrink:0;
}}

/* ── Notifications ── */
.notif-item {{
    display:flex; align-items:flex-start; gap:8px; padding:7px 10px;
    border-radius:8px; background:{C['surface']}; border:1px solid {C['border']};
    margin-bottom:5px; font-size:12px; color:{C['text_muted']};
}}
.notif-pip {{
    width:6px; height:6px; border-radius:50%; background:{C['primary']};
    flex-shrink:0; margin-top:3px;
}}

/* ── Landing ── */
.landing-hero {{
    min-height:44vh; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    text-align:center; padding:2.5rem 2rem 1rem;
}}
.landing-logo {{
    width:300px; height:200px; object-fit:contain;
    filter:drop-shadow(0 6px 24px rgba(79,158,255,.3));
    margin-bottom:22px;
    animation:floatLogo 4s ease-in-out infinite alternate;
}}
@keyframes floatLogo {{
    from {{ transform:translateY(0) rotate(-1deg); }}
    to   {{ transform:translateY(-12px) rotate(1deg); }}
}}
.landing-tag {{
    background:{C['surface']}; border:1px solid {C['border']};
    color:{C['text_muted']}; border-radius:999px;
    padding:5px 12px; font-size:12px; font-weight:600;
    display:inline-block; margin:4px;
}}
.stat-card {{
    text-align:center; padding:20px 10px;
    background:{C['surface']}; border-radius:14px;
    border:1px solid {C['border']};
}}
.stat-val {{
    font-size:32px; font-weight:800; color:{C['primary']};
    font-family:'JetBrains Mono',monospace;
}}
.stat-lbl {{ font-size:13px; color:{C['text_muted']}; margin-top:4px; }}

/* ── Catalog card ── */
.catalog-card {{
    background:{C['surface']}; border-radius:14px; padding:14px 16px;
    border:1px solid {C['border']}; margin-bottom:6px;
}}

/* ── SKS bar (jadwal tab) ── */
.sks-bar-bg {{
    background:{C['border']}; border-radius:999px;
    height:8px; margin:8px 0 4px; overflow:hidden;
}}
.sks-bar-fill {{ height:100%; border-radius:999px; transition:width .4s ease; }}

/* ── Fact card (Tips tab) ── */
.fact-card {{
    background:{C['surface']};
    border:1px solid {C['border']};
    border-left:4px solid {C['primary']};
    border-radius:12px;
    padding:14px 16px;
    margin-bottom:12px;
    display:flex; align-items:flex-start; gap:12px;
}}
.fact-icon {{ font-size:22px; flex-shrink:0; line-height:1.3; }}
.fact-text {{ font-size:13.5px; line-height:1.75; color:{C['text']}; font-weight:500; }}

/* ── Matkul tip card (Tips tab) ── */
.mtcard {{
    background:{C['surface2']};
    border:1px solid {C['border']};
    border-radius:12px;
    padding:14px 16px;
    margin-bottom:10px;
}}
.mtcard-header {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
.mtcard-emoji {{ font-size:26px; line-height:1; flex-shrink:0; }}
.mtcard-name {{ font-size:13.5px; font-weight:700; color:{C['text']}; }}
.mtcard-meta {{
    font-size:11px; color:{C['text_muted']};
    font-family:'JetBrains Mono',monospace; margin-top:2px;
}}
.mtcard-tip {{
    background:{C['surface']};
    border-left:3px solid {C['primary']};
    border-radius:0 8px 8px 0;
    padding:10px 14px;
    font-size:13px; color:{C['text_muted']};
    font-style:italic; line-height:1.7;
    margin-top:8px;
}}
.tbadge {{
    display:inline-block; border-radius:20px;
    padding:3px 10px; font-size:11px; font-weight:700;
    margin:2px 3px 2px 0;
}}

/* ── Command list (Panduan tab) ── */
.cmd-table {{
    background:{C['surface2']};
    border:1px solid {C['border']};
    border-radius:12px;
    padding:16px 20px;
    font-family:'JetBrains Mono',monospace;
    font-size:12.5px;
    line-height:1.9;
}}
.cmd-row {{ display:flex; gap:8px; margin-bottom:2px; }}
.cmd-key {{ color:{C['primary']}; font-weight:700; min-width:200px; flex-shrink:0; }}
.cmd-desc {{ color:{C['text_muted']}; }}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: render catalog card
# ─────────────────────────────────────────────
def render_catalog_card(key, data, in_krs):
    nama = key.replace("_", " ").title()
    krs_badge = (
        f'<span style="background:{C["success_bg"]};color:{C["success"]};'
        f'border-radius:6px;padding:2px 10px;font-size:11px;font-weight:700;">✅ Di KRS</span>'
    ) if in_krs else ""
    kat_color = C["warning"] if data["kategori"] == "Wajib" else C["success"]
    kat_bg    = C["warning_bg"] if data["kategori"] == "Wajib" else C["success_bg"]
    ts = f'display:inline-block;border-radius:6px;padding:3px 8px;font-size:11px;font-weight:600;margin:2px 2px 0 0;background:{C["surface2"]};color:{C["text_muted"]};'
    return f"""
<div class="catalog-card">
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
    <span style="{ts}background:{C['primary_bg']};color:{C['primary']};">{data['sks']} SKS</span>
    <span style="{ts}background:{kat_bg};color:{kat_color};">{data['kategori']}</span>
    <span style="{ts}">🕐 {data['jadwal']}</span>
    <span style="{ts}">📍 {data['ruang']}</span>
    <span style="{ts}">👨‍🏫 {data['dosen']}</span>
  </div>
</div>"""


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    logo_inner = (
        f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" style="width:48px;height:48px;object-fit:contain;" alt="UPGRIS"/>'
        if UPGRIS_LOGO_B64 else '<span style="font-size:28px;">🎓</span>'
    )
    st.markdown(f"""
    <div data-white style="background:linear-gradient(135deg,#0f2d6e 0%,#1a3a8f 50%,#0ea5e9 100%);
                border-radius:16px;padding:18px 16px 16px;text-align:center;
                margin-bottom:14px;box-shadow:0 4px 24px rgba(26,86,219,.35);
                position:relative;overflow:hidden;">
        <div data-white style="width:56px;height:56px;border-radius:14px;
                    border:2px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);
                    overflow:hidden;margin:0 auto 10px;
                    display:flex;align-items:center;justify-content:center;">
            {logo_inner}
        </div>
        <p data-white style="font-size:14px;font-weight:700;margin:0;color:#ffffff;">SIKRS · UPGRIS</p>
        <p data-white style="font-size:11px;opacity:.85;margin:3px 0 0;color:#ffffff;">Sistem Informasi KRS 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sbl">🎨 Tema Tampilan</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌙 Gelap", use_container_width=True, key="btn_dark",
                     type="primary" if is_dark else "secondary"):
            st.session_state.dark_mode = True; st.rerun()
    with c2:
        if st.button("☀️ Terang", use_container_width=True, key="btn_light",
                     type="primary" if not is_dark else "secondary"):
            st.session_state.dark_mode = False; st.rerun()

    st.markdown('<span class="sbl">🧭 Navigasi</span>', unsafe_allow_html=True)
    if st.session_state.show_landing:
        if st.button("Masuk ke Aplikasi", use_container_width=True, type="primary"):
            st.session_state.show_landing = False; st.rerun()
    else:
        if st.button("Kembali ke Beranda", use_container_width=True):
            st.session_state.show_landing = True; st.rerun()

    if not st.session_state.show_landing:
        total_sks = bot.total_sks()
        max_sks   = bot.nlp.MAX_SKS
        pct       = int(total_sks / max_sks * 100) if max_sks else 0
        if pct >= 90:
            status_emoji, status_txt = "🔴", "Hampir Penuh"
        elif pct >= 70:
            status_emoji, status_txt = "🟡", "Mendekati Batas"
        else:
            status_emoji, status_txt = "🟢", "Aman"

        st.markdown('<span class="sbl">📊 Dashboard KRS</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div data-white style="background:linear-gradient(135deg,#0f2d6e 0%,#1a56db 60%,#0ea5e9 100%);
                    border-radius:16px;padding:20px 22px 16px;margin-bottom:10px;
                    box-shadow:0 8px 32px rgba(26,86,219,.35);position:relative;overflow:hidden;">
            <div data-white style="font-size:10px;font-weight:700;letter-spacing:1.8px;
                        text-transform:uppercase;opacity:.75;margin-bottom:6px;color:#ffffff;">
                Total SKS Diambil
            </div>
            <div data-white style="font-family:'JetBrains Mono',monospace;font-size:42px;font-weight:800;
                        line-height:1;letter-spacing:-2px;color:#ffffff;">
                {total_sks}<span data-white style="font-size:18px;font-weight:400;opacity:.65;color:#ffffff;"> / {max_sks} SKS</span>
            </div>
            <div data-white style="font-size:12px;font-weight:600;margin-top:4px;opacity:.85;color:#ffffff;">
                {status_emoji} {status_txt} · {pct}% terisi
            </div>
            <div data-white style="margin:14px 0 12px;background:rgba(255,255,255,.18);
                        border-radius:999px;height:7px;overflow:hidden;">
                <div data-white style="width:{pct}%;height:100%;border-radius:999px;
                            background:rgba(255,255,255,.9);"></div>
            </div>
            <div data-white style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div data-white style="background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);
                            border-radius:10px;padding:10px 12px;text-align:center;">
                    <div data-white style="font-family:'JetBrains Mono',monospace;font-size:22px;
                                font-weight:800;line-height:1;color:#ffffff;">{total_sks}</div>
                    <div data-white style="font-size:9px;font-weight:700;letter-spacing:1.2px;
                                text-transform:uppercase;opacity:.7;margin-top:3px;color:#ffffff;">Diambil</div>
                </div>
                <div data-white style="background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);
                            border-radius:10px;padding:10px 12px;text-align:center;">
                    <div data-white style="font-family:'JetBrains Mono',monospace;font-size:22px;
                                font-weight:800;line-height:1;color:#ffffff;">{max_sks - total_sks}</div>
                    <div data-white style="font-size:9px;font-weight:700;letter-spacing:1.2px;
                                text-transform:uppercase;opacity:.7;margin-top:3px;color:#ffffff;">Tersisa</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if bot.notifications:
            st.markdown('<span class="sbl">🔔 Notifikasi Terbaru</span>', unsafe_allow_html=True)
            for n in reversed(bot.notifications[-3:]):
                st.markdown(f'<div class="notif-item"><div class="notif-pip"></div><span>{n}</span></div>',
                            unsafe_allow_html=True)

        st.markdown('<span class="sbl">🗂️ Mata Kuliah Dipilih</span>', unsafe_allow_html=True)
        if bot.cart:
            for c in bot.cart:
                nama = c["course_key"].replace("_", " ").title()
                st.markdown(f"""
                <div class="krs-item">
                    <div class="krs-emoji-box">{c['emoji']}</div>
                    <div class="krs-text">
                        <div class="krs-name">{nama}</div>
                        <div class="krs-code">{c['kode']}</div>
                    </div>
                    <span class="krs-sks-badge">{c['sks']} SKS</span>
                </div>""", unsafe_allow_html=True)
            st.markdown("")
            if st.button("🗑️ Kosongkan KRS", use_container_width=True):
                bot.cart = []
                st.session_state.history.append({"role": "assistant", "content": "🗑️ KRS berhasil dikosongkan."})
                st.rerun()
        else:
            st.info("Belum ada matkul dipilih.", icon="📭")

        st.markdown('<span class="sbl">⚙️ Sistem</span>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔄 Reset Chat", use_container_width=True):
                dark_bak = st.session_state.dark_mode
                st.session_state.clear()
                st.session_state.dark_mode    = dark_bak
                st.session_state.show_landing = False
                st.rerun()
        with cb:
            if st.button("🗑️ Hapus Chat", use_container_width=True):
                st.session_state.history = []
                st.rerun()

    st.markdown("---")
    st.caption("SIKRS 2026 · Powered by Rahul Candra · Universitas PGRI Semarang")


# ══════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════
if st.session_state.show_landing:
    logo_html = (
        f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" class="landing-logo" alt="Logo UPGRIS"/>'
        if UPGRIS_LOGO_B64 else '<div style="font-size:80px;margin-bottom:20px;">🎓</div>'
    )
    st.markdown(f"""
    <div class="landing-hero">
        {logo_html}
        <h1 style="font-size:clamp(28px,4vw,54px);font-weight:800;color:{C['text']};
                   line-height:1.08;letter-spacing:-2px;margin:0 0 14px;">
            Susun KRS Lebih<br>
            <span style="color:{C['primary']};">Cerdas</span> &amp;
            <span style="color:#22d3a8;">Cepat</span>
        </h1>
        <p style="font-size:15px;color:{C['text_muted']};max-width:540px;margin:0 auto 22px;line-height:1.75;">
            SIKRS adalah chatbot akademik berbasis <strong>Finite State Machine</strong>
            yang membantu mahasiswa Program Studi Teknik Informatika UPGRIS menyusun KRS
            dengan data jadwal real, validasi prasyarat, deteksi konflik jadwal, dan tips belajar otomatis.
        </p>
        <div>
            <span class="landing-tag">🤖 Chatbot NLP Engine</span>
            <span class="landing-tag">⚡ Validasi Real-time</span>
            <span class="landing-tag">📅 Data Jadwal Resmi</span>
            <span class="landing-tag">🎯 Rekomendasi Cerdas</span>
            <span class="landing-tag">🔔 Notifikasi Live</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_matkul = len(bot.nlp.course_data)
    s1, s2, s3, s4 = st.columns(4)
    for col, (val, lbl) in zip([s1,s2,s3,s4], [
        (str(total_matkul),"Mata Kuliah"),("24","Maks SKS"),("4","State FSM"),("9","Fitur Utama")
    ]):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div>'
                        f'<div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<h3 style="color:{C["text"]};">✨ Fitur Unggulan SIKRS</h3>', unsafe_allow_html=True)
    st.caption("Klik setiap fitur untuk melihat detail keunggulan chatbot ini!")

    features = [
        ("🤖","Chatbot NLP","Pahami perintah natural bahasa Indonesia","Baru",
         "Ketik perintah seperti 'ambil struktur data' atau 'rekomen matkul'. NLP Engine berbasis Regex mengenali sinonim dan variasi penulisan nama matkul secara otomatis."),
        ("⚠️","Validasi Real-time","Cek prasyarat, konflik jadwal & batas 24 SKS","Wajib",
         "Sistem otomatis memeriksa prasyarat, bentrokan jadwal, dan kapasitas SKS setiap kali Anda menambah mata kuliah."),
        ("💡","Tips Belajar Spesifik","Tips personal untuk setiap mata kuliah","Wajib",
         "Setiap matkul dilengkapi tips belajar spesifik dari rekomendasi tools hingga strategi ujian."),
        ("🔔","Panel Notifikasi","Riwayat perubahan KRS di sidebar","Pilihan",
         "Setiap aksi tambah/hapus matkul dicatat sebagai notifikasi real-time di sidebar."),
        ("🎯","Rekomendasi Cerdas","Saran matkul berdasarkan KRS aktif Anda","Baru",
         "Sistem menganalisis KRS Anda dan merekomendasikan matkul lain yang prasyaratnya sudah terpenuhi."),
        ("📅","Jadwal Visual per Hari","Tampilan jadwal terurut Senin–Sabtu","Wajib",
         "Tab Jadwal menampilkan matkul KRS terurut per hari lengkap ruangan, dosen, dan jam."),
        ("🎨","Tema Gelap & Terang","Ganti tema kapan saja tanpa kehilangan data","Pilihan",
         "Dark mode untuk coding malam dan light mode untuk siang hari. Ganti via sidebar kapan saja."),
    ]
    badge_map = {
        "Baru":    (C["primary"],   C["primary_bg"]),
        "Wajib":   (C["success"],   C["success_bg"]),
        "Pilihan": (C["text_muted"],C["surface2"]),
    }
    for row_start in range(0, len(features), 3):
        row  = features[row_start:row_start+3]
        cols = st.columns(3)
        for col, (icon, name, short, badge, detail) in zip(cols, row):
            bc, bb = badge_map.get(badge, (C["text_muted"], C["surface2"]))
            with col:
                with st.expander(f"{icon} **{name}**"):
                    st.markdown(
                        f'<span style="background:{bb};color:{bc};border-radius:6px;'
                        f'padding:3px 10px;font-size:11px;font-weight:700;display:inline-block;'
                        f'margin-bottom:10px;">{badge}</span>', unsafe_allow_html=True)
                    st.caption(short)
                    st.markdown(detail)

    st.markdown("---")
    cta = st.columns([1, 2, 1])
    with cta[1]:
        if st.button("Mulai Sekarang!", use_container_width=True, type="primary"):
            st.session_state.show_landing = False; st.rerun()

    st.markdown(
        f'<div style="text-align:center;color:{C["text_faint"]};font-size:12px;margin-top:28px;line-height:2;">'
        f'SIKRS 2026 · Universitas PGRI Semarang<br>'
        f'Powered by <strong style="color:{C["primary"]};">Rahul Candra</strong> · Teknik Informatika</div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HALAMAN APLIKASI UTAMA
# ══════════════════════════════════════════════
else:
    logo_img = (
        f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" '
        f'style="width:80px;height:80px;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));" alt="UPGRIS"/>'
        if UPGRIS_LOGO_B64 else '<div style="font-size:46px;">🎓</div>'
    )
    st.markdown(f"""
    <div class="header-banner">
        {logo_img}
        <div>
            <p class="header-title" style="color:#ffffff !important;">SIKRS — Chatbot Akademik UPGRIS</p>
            <p class="header-sub" style="color:#ffffff !important;">Sistem Informasi Kartu Rencana Studi · Teknik Informatika · Universitas PGRI Semarang</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_chat, tab_catalog, tab_schedule, tab_tips, tab_about = st.tabs([
        "💬 Chatbot KRS", "📚 Katalog Matkul", "📅 Jadwal Saya", "💡 Tips & Fakta", "ℹ️ Panduan",
    ])

    # ═══ TAB 1 — CHATBOT ═══
    with tab_chat:
        chat_col, _ = st.columns([3, 0.01])
        with chat_col:
            chat_container = st.container(height=520)
            with chat_container:
                for msg in st.session_state.history:
                    if msg["role"] == "assistant":
                        avatar = f"data:image/png;base64,{UPGRIS_LOGO_B64}" if UPGRIS_LOGO_B64 else "🎓"
                    else:
                        avatar = "🧑‍🎓"
                    with st.chat_message(msg["role"], avatar=avatar):
                        st.markdown(msg["content"])

            prompt = st.chat_input("Contoh: ambil matkul / info matkul / rekomen matkul / jadwal kuliah")
            if prompt:
                st.session_state.history.append({"role": "user", "content": prompt})
                bot.step(prompt)
                st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                st.rerun()

            st.markdown(f'<p style="color:{C["text"]};font-weight:700;font-size:14px;margin-bottom:8px;">⚡ Aksi Cepat:</p>',
                        unsafe_allow_html=True)
            q1,q2,q3,q4,q5,q6 = st.columns(6)
            quick_actions = [
                ("📚 Menu","menu"),("🎯 Rekomen","rekomen"),("📅 Jadwal","jadwal"),
                ("📊 SKS","total sks saya"),("📤 Submit","submit KRS"),("❓ Bantuan","bantuan"),
            ]
            for col, (label, cmd) in zip([q1,q2,q3,q4,q5,q6], quick_actions):
                with col:
                    if st.button(label, use_container_width=True, key=f"qa_{cmd}"):
                        st.session_state.history.append({"role":"user","content":cmd})
                        bot.step(cmd)
                        st.session_state.history.append({"role":"assistant","content":bot.get_response()})
                        st.rerun()

    # ═══ TAB 2 — KATALOG ═══
    with tab_catalog:
        st.markdown(f'<h3 style="color:{C["text"]};">📚 Katalog Mata Kuliah</h3>', unsafe_allow_html=True)
        st.caption("Data jadwal real UPGRIS Semester Genap 2025/2026")
        st.markdown("---")

        fc1, fc2, fc3 = st.columns([1,1,2])
        with fc1: filter_kat = st.selectbox("Kategori", ["Semua","Wajib","Pilihan"])
        with fc2: filter_sem = st.selectbox("Semester", ["Semua","1","2","3","4","5","6","7","8"])
        with fc3: search_q  = st.text_input("🔍 Cari matkul atau dosen...", placeholder="contoh: web, Ramadhan, IoT")

        st.markdown("---")
        filtered = []
        for key, data in bot.nlp.course_data.items():
            nama = key.replace("_"," ").title()
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
                    nama   = key.replace("_"," ").title()
                    in_krs = any(c["course_key"] == key for c in bot.cart)
                    with cols[col_idx]:
                        st.markdown(render_catalog_card(key, data, in_krs), unsafe_allow_html=True)
                        if in_krs:
                            if st.button("🗑️ Hapus dari KRS", key=f"rem_{key}", use_container_width=True):
                                msg = bot.remove_course(key)
                                st.session_state.history.append({"role":"assistant","content":msg})
                                st.rerun()
                        else:
                            if st.button("➕ Tambah ke KRS", key=f"add_{key}", use_container_width=True, type="primary"):
                                success, msg = bot.add_course(key)
                                st.session_state.history.append({"role":"user","content":f"ambil {nama}"})
                                st.session_state.history.append({"role":"assistant","content":msg})
                                st.rerun()
                st.markdown("---")

    # ═══ TAB 3 — JADWAL ═══
    with tab_schedule:
        st.markdown(f'<h3 style="color:{C["text"]};">📅 Jadwal Kuliah Saya</h3>', unsafe_allow_html=True)
        st.markdown("---")

        if not bot.cart:
            st.info("Belum ada mata kuliah dalam KRS.\nTambahkan dari **Katalog** atau via **Chat**.", icon="📭")
        else:
            days_order = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"]
            by_day = {d:[] for d in days_order}
            for c in bot.cart:
                for d in days_order:
                    if d in c["jadwal"]:
                        by_day[d].append(c); break

            for day in days_order:
                if not by_day[day]: continue
                st.markdown(f"#### 📆 {day}")
                for c in by_day[day]:
                    nama = c["course_key"].replace("_"," ").title()
                    jam  = c["jadwal"].split(" ",1)[1] if " " in c["jadwal"] else c["jadwal"]
                    cl1,cl2,cl3,cl4 = st.columns([0.4,2.2,2,1])
                    with cl1:
                        st.markdown(f'<div style="font-size:26px;text-align:center;">{c["emoji"]}</div>',
                                    unsafe_allow_html=True)
                    with cl2:
                        st.markdown(f"**{nama}**"); st.caption(f"⏰ {jam}")
                    with cl3:
                        st.markdown(f"📍 {c['ruang']}"); st.caption(f"👨‍🏫 {c['dosen']}")
                    with cl4:
                        st.markdown(
                            f'<div style="background:{C["primary_bg"]};color:{C["primary"]};'
                            f'border-radius:8px;padding:7px 12px;text-align:center;font-weight:700;'
                            f'font-family:JetBrains Mono,monospace;">{c["sks"]} SKS</div>',
                            unsafe_allow_html=True)
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
                    st.session_state.history.append({"role":"user","content":"submit KRS"})
                    st.session_state.history.append({"role":"assistant","content":bot.get_response()})
                    st.rerun()

    # ═══ TAB 4 — TIPS & FAKTA ═══
    with tab_tips:
        st.markdown(f'<h3 style="color:{C["text"]};">💡 Tips Belajar & Fakta Akademik</h3>', unsafe_allow_html=True)
        st.caption("Strategi dan tips belajar yang terbukti efektif untuk mahasiswa Teknik Informatika.")
        st.markdown("---")

        st.markdown(f'<h4 style="color:{C["text"]};margin-bottom:14px;">🧠 Strategi Belajar Efektif</h4>',
                    unsafe_allow_html=True)
        fact_icons = ["⏱️","🔁","✏️","👥","😴","🌅","📵","🗣️"]
        fc1, fc2 = st.columns(2)
        for i, fact in enumerate(ACADEMIC_FACTS):
            icon = fact_icons[i] if i < len(fact_icons) else "💡"
            with (fc1 if i % 2 == 0 else fc2):
                st.markdown(f"""
<div class="fact-card">
  <div class="fact-icon">{icon}</div>
  <div class="fact-text">{fact}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f'<h4 style="color:{C["text"]};margin-bottom:6px;">📚 Tips Belajar Per Mata Kuliah</h4>',
                    unsafe_allow_html=True)
        st.caption("Klik semester untuk membuka daftar mata kuliah beserta tips belajarnya.")

        by_sem = {}
        for k, v in bot.nlp.course_data.items():
            by_sem.setdefault(v["semester"], []).append((k, v))

        for sem in sorted(by_sem.keys()):
            matkul_list = by_sem[sem]
            with st.expander(f"📖 Semester {sem}  —  {len(matkul_list)} mata kuliah", expanded=(sem <= 2)):
                for k, v in matkul_list:
                    nama = k.replace("_"," ").title()
                    diff = v["difficulty"]
                    stars = "⭐" * diff + "☆" * (5 - diff)
                    diff_label = "Mudah" if diff <= 2 else "Sedang" if diff <= 3 else "Sulit"

                    if diff <= 2:
                        diff_c, diff_bg = C["success"], C["success_bg"]
                    elif diff <= 3:
                        diff_c, diff_bg = C["warning"], C["warning_bg"]
                    else:
                        diff_c, diff_bg = C["danger"], C["danger_bg"]

                    kat_c  = C["warning"] if v["kategori"] == "Wajib" else C["success"]
                    kat_bg = C["warning_bg"] if v["kategori"] == "Wajib" else C["success_bg"]

                    in_krs = any(c["course_key"] == k for c in bot.cart)

                    st.markdown("---")
                    col_emoji, col_info = st.columns([0.08, 0.92])
                    with col_emoji:
                        st.markdown(f"## {v['emoji']}")
                    with col_info:
                        krs_tag = "  ✅ *Di KRS*" if in_krs else ""
                        st.markdown(f"**{nama}**{krs_tag}")
                        st.caption(f"{v['kode']} · Semester {v['semester']} · {v['sks']} SKS · 👨‍🏫 {v['dosen']} · 🕐 {v['jadwal']}")

                    badge_col1, badge_col2, badge_col3 = st.columns([1,1,3])
                    with badge_col1:
                        st.markdown(
                            f'<span class="tbadge" style="background:{diff_bg};color:{diff_c};">'
                            f'{stars} {diff_label}</span>',
                            unsafe_allow_html=True)
                    with badge_col2:
                        st.markdown(
                            f'<span class="tbadge" style="background:{kat_bg};color:{kat_c};">'
                            f'{v["kategori"]}</span>',
                            unsafe_allow_html=True)

                    st.info(f"💡 {v['tips']}", icon=None)

        st.markdown("---")

        st.markdown(f'<h4 style="color:{C["text"]};margin-bottom:14px;">📊 Ringkasan Katalog</h4>',
                    unsafe_allow_html=True)
        total_matkul  = len(bot.nlp.course_data)
        total_wajib   = sum(1 for v in bot.nlp.course_data.values() if v["kategori"] == "Wajib")
        total_pilihan = sum(1 for v in bot.nlp.course_data.values() if v["kategori"] == "Pilihan")
        avg_diff      = sum(v["difficulty"] for v in bot.nlp.course_data.values()) / total_matkul if total_matkul else 0

        sc1,sc2,sc3,sc4 = st.columns(4)
        for col,(val,lbl,icon,col_c,col_bg) in zip(
            [sc1,sc2,sc3,sc4],
            [
                (str(total_matkul), "Total Matkul",       "📚", C["primary"], C["primary_bg"]),
                (str(total_wajib),  "Matkul Wajib",       "✅", C["warning"], C["warning_bg"]),
                (str(total_pilihan),"Matkul Pilihan",     "🎯", C["success"], C["success_bg"]),
                (f"{avg_diff:.1f}/5","Rata-rata Kesulitan","⭐", C["danger"],  C["danger_bg"]),
            ]
        ):
            with col:
                st.markdown(f"""
<div style="background:{col_bg};border:1px solid {C['border']};border-radius:14px;
padding:18px 14px;text-align:center;">
  <div style="font-size:24px;margin-bottom:6px;">{icon}</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:800;color:{col_c};">{val}</div>
  <div style="font-size:12px;color:{C['text_muted']};margin-top:4px;font-weight:600;">{lbl}</div>
</div>""", unsafe_allow_html=True)

    # ═══ TAB 5 — PANDUAN ═══
    with tab_about:
        st.markdown(f'<h3 style="color:{C["text"]};">ℹ️ Panduan & Informasi Sistem</h3>', unsafe_allow_html=True)
        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### 🤖 Tentang SIKRS")
            st.markdown(
                f"Chatbot ini menggunakan **Finite State Machine (FSM)** dengan **NLP Engine berbasis Regex** "
                f"untuk membantu mahasiswa Teknik Informatika **UPGRIS** menyusun KRS."
            )
            st.markdown("**State FSM:**")
            st.markdown("""
| State | Ikon | Keterangan |
|-------|------|-----------|
| Browsing | 🟢 | Menjelajah & menambah matkul |
| Konfirmasi | 🟠 | Verifikasi sebelum submit |
| Selesai | 🔵 | KRS berhasil disubmit |
""")
            st.markdown("---")
            st.markdown("#### ✨ Fitur Lengkap")
            fitur = [
                "💬 **Chatbot KRS** — FSM-based, perintah natural bahasa Indonesia",
                "📚 **Katalog Interaktif** — Filter semester, kategori, pencarian",
                "🛒 **Manajemen KRS** — Tambah/hapus via chat atau tombol",
                "⚠️ **Validasi Otomatis** — Prasyarat, konflik jadwal, batas SKS",
                "🎯 **Rekomendasi** — Saran matkul berdasarkan KRS aktif",
                "💡 **Tips Belajar** — Tips spesifik per matkul",
                "🔔 **Notifikasi** — Panel riwayat perubahan KRS",
                "📅 **Jadwal Visual** — Tersusun per hari + submit langsung",
                "🎨 **Tema Gelap/Terang** — Ganti tema kapan saja",
            ]
            for f in fitur:
                st.markdown(f"- {f}")

        with col_b:
            st.markdown("#### 💬 Contoh Perintah Chat")
            commands = [
                ("menu",                 "lihat semua matkul"),
                ("ambil matdis",         "tambah ke KRS"),
                ("hapus sistem operasi", "hapus dari KRS"),
                ("hapus semua",          "kosongkan KRS"),
                ("jadwal",               "lihat jadwal"),
                ("total sks",            "cek kapasitas SKS"),
                ("info pemrograman web", "detail matkul"),
                ("prasyarat aps",        "cek syarat"),
                ("dosen iot",            "info dosen + jadwal"),
                ("susah matdis",         "tingkat kesulitan"),
                ("tips web",             "tips belajar"),
                ("rekomen",              "rekomendasi matkul"),
                ("krs saya",             "ringkasan KRS"),
                ("submit KRS",           "konfirmasi & kirim"),
                ("reset",                "mulai ulang"),
                ("bantuan",              "panduan ini"),
            ]
            rows = "".join(
                f'<div class="cmd-row">'
                f'<span class="cmd-key">{cmd}</span>'
                f'<span class="cmd-desc">→ {desc}</span>'
                f'</div>'
                for cmd, desc in commands
            )
            st.markdown(f'<div class="cmd-table">{rows}</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 📋 Aturan KRS")
            aturan = [
                "**Maksimum SKS:** 24 SKS per semester",
                "**Prasyarat:** Beberapa matkul butuh matkul lain di KRS",
                "**Konflik:** Jadwal yang sama tidak bisa diambil bersamaan",
                "**Data jadwal:** Real dari UPGRIS Sem. Genap 2025/2026",
                "**Semester tersedia:** 1 hingga 8",
            ]
            for a in aturan:
                st.markdown(f"- {a}")

        st.markdown("---")
        st.markdown(
            f'<div style="text-align:center;color:{C["text_muted"]};font-size:13px;padding:10px;">'
            f'SIKRS 2026 · Dikembangkan oleh <b>Rahul Candra</b><br>'
            f'Finite State Machine + NLP Engine<br>'
            f'Program Studi Teknik Informatika · <b>Universitas PGRI Semarang</b>'
            f'</div>', unsafe_allow_html=True)