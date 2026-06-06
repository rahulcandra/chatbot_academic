import base64
import streamlit as st
from academic_fsm import AcademicFSM, State

# Logo UPGRIS (base64)
def get_base64_of_image(image_path):
    with open(image_path, "rb") as input_file:
        data = input_file.read()
    return base64.b64encode(data).decode()
try:
    UPGRIS_LOGO_B64 = get_base64_of_image("logo_upgris.png")
except FileNotFoundError:
    UPGRIS_LOGO_B64 = ""

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SIKRS — Sistem Informasi KRS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
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

bot = st.session_state.bot
is_dark = st.session_state.dark_mode

# ─────────────────────────────────────────────
# THEME CSS
# ─────────────────────────────────────────────
if is_dark:
    THEME = """
    :root {
        --bg:            #0a0e1a;
        --bg2:           #111827;
        --surface:       #1a2235;
        --surface2:      #1e2a3d;
        --border:        #2d3f5c;
        --border-hover:  #4a6080;
        --primary:       #60a5fa;
        --primary-dark:  #3b82f6;
        --primary-light: rgba(96,165,250,0.18);
        --accent:        #38bdf8;
        --success:       #4ade80;
        --success-light: rgba(74,222,128,0.15);
        --warning:       #fcd34d;
        --warning-light: rgba(252,211,77,0.15);
        --danger:        #f87171;
        --danger-light:  rgba(248,113,113,0.15);
        --text:          #f1f5f9;
        --text-muted:    #94a3b8;
        --text-faint:    #475569;
        --radius:        12px;
        --shadow:        0 2px 12px rgba(0,0,0,.5);
    }
    .stApp { background: var(--bg) !important; }
    section[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border) !important; }
    div[data-testid="stChatInput"] textarea {
        background: #1e2a3d !important;
        color: #f1f5f9 !important;
        caret-color: #60a5fa !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }
    div[data-testid="stChatInput"] > div {
        background: #1e2a3d !important;
    }
    /* Fix all text inputs in dark mode */
    .stTextInput input {
        background: #1e2a3d !important;
        color: #f1f5f9 !important;
        border-color: #2d3f5c !important;
    }
    .stTextInput input::placeholder { color: #64748b !important; opacity: 1 !important; }
    .stSelectbox > div > div { background: #1e2a3d !important; color: #f1f5f9 !important; }
    /* Fix dark mode text visibility */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: var(--text) !important;
    }
    label, .stSelectbox label, .stTextInput label {
        color: var(--text) !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted) !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
    }
    /* Fix ALL buttons background in dark mode */
    .stButton > button {
        background-color: #1a2235 !important;
        color: #f1f5f9 !important;
        border: 1px solid #2d3f5c !important;
    }
    .stButton > button:hover {
        background-color: #1e2d4a !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
    }
    button[data-testid="baseButton-primary"],
    .stButton > button[kind="primary"] {
        background-color: #1a56db !important;
        border-color: #1a56db !important;
        color: white !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        background-color: #1e40af !important;
    }
    button[data-testid="baseButton-secondary"],
    .stButton > button[kind="secondary"] {
        background-color: #1a2235 !important;
        color: #f1f5f9 !important;
        border: 1px solid #2d3f5c !important;
    }
    /* Fix scrollable container and sticky bottom area */
    .stChatFloatingInputContainer,
    .stChatFloatingInputContainer > div,
    .stChatFloatingInputContainer > div > div {
        background: #0a0e1a !important;
    }
    /* Fix white flash on scroll in containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: transparent !important;
    }
    /* Info/success/warning boxes */
    div[data-testid="stAlert"] {
        background: #1a2235 !important;
        color: #f1f5f9 !important;
        border-color: #2d3f5c !important;
    }
    /* Fix code blocks in dark mode */
    pre, code, .stCodeBlock, .stCodeBlock pre,
    div[data-testid="stCodeBlock"],
    div[data-testid="stCodeBlock"] pre,
    div[data-testid="stCodeBlock"] code {
        background: #0d1525 !important;
        color: #a5d6ff !important;
        border: 1px solid #2d3f5c !important;
        border-radius: 8px !important;
    }
    div[data-testid="stCodeBlock"] span {
        color: #a5d6ff !important;
    }
    /* Inline code */
    .stMarkdown code {
        background: #0d1525 !important;
        color: #60a5fa !important;
        border: 1px solid #2d3f5c !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    """
else:
    THEME = """
    :root {
        --bg:            #f0f4ff;
        --bg2:           #ffffff;
        --surface:       #ffffff;
        --surface2:      #f8faff;
        --border:        #e2e8f0;
        --border-hover:  #cbd5e1;
        --primary:       #1a56db;
        --primary-dark:  #1e40af;
        --primary-light: #dbeafe;
        --accent:        #0ea5e9;
        --success:       #16a34a;
        --success-light: #dcfce7;
        --warning:       #d97706;
        --warning-light: #fef3c7;
        --danger:        #dc2626;
        --danger-light:  #fee2e2;
        --text:          #1e293b;
        --text-muted:    #64748b;
        --text-faint:    #94a3b8;
        --radius:        12px;
        --shadow:        0 1px 3px rgba(0,0,0,.08), 0 4px 16px rgba(26,86,219,.06);
    }
    .stApp { background: var(--bg) !important; }
    section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
    """

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text) !important;
}
.main .block-container { padding: 1.5rem 2rem 2rem !important; max-width: 1300px !important; }
/* Remove white top bar */
.stApp > header { background: transparent !important; display: none !important; }
.stApp { margin-top: 0 !important; }
#stDecoration { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stToolbar"] { background: transparent !important; }
div[data-testid="stHeader"] { background: transparent !important; height: 0 !important; min-height: 0 !important; }
.main > div:first-child { padding-top: 0 !important; }
header[data-testid="stHeader"] { background-color: transparent !important; height: 0 !important; }

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #1a56db 0%, #2563eb 40%, #0ea5e9 100%);
    border-radius: 16px; padding: 24px 32px; margin-bottom: 22px;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 4px 28px rgba(26,86,219,.35);
}
.header-title { font-size: 24px; font-weight: 800; color: white !important; margin: 0; letter-spacing: -0.5px; }
.header-sub { color: rgba(255,255,255,.8) !important; font-size: 13px; margin: 3px 0 0; }
.header-badge {
    margin-left: auto; background: rgba(255,255,255,.18); color: white;
    border: 1px solid rgba(255,255,255,.3); border-radius: 8px;
    padding: 5px 13px; font-size: 12px; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

/* Cards */
.card {
    background: var(--surface); border-radius: var(--radius);
    padding: 18px 20px; border: 1px solid var(--border);
    box-shadow: var(--shadow); margin-bottom: 14px;
}
.matkul-card {
    background: var(--surface); border-radius: var(--radius);
    padding: 18px 20px; border: 1px solid var(--border);
    box-shadow: var(--shadow); margin-bottom: 14px;
    transition: border-color .2s, box-shadow .2s;
}
.matkul-card:hover { border-color: var(--primary); box-shadow: 0 2px 16px rgba(96,165,250,.2); }
.matkul-name { font-size: 15px; font-weight: 700; color: var(--text); }
.matkul-kode { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted); margin-top: 2px; }
.matkul-desc { font-size: 13px; color: var(--text-muted); margin: 8px 0 10px; line-height: 1.55; }
.matkul-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px; }
.meta-tag { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 3px 9px; font-size: 12px; color: var(--text-muted); }
.meta-tag.sks  { background: var(--primary-light); color: var(--primary); border-color: transparent; font-weight: 700; }
.meta-tag.wajib { background: var(--warning-light); color: var(--warning); border-color: transparent; }
.meta-tag.pilihan { background: var(--success-light); color: var(--success); border-color: transparent; }
.prereq-tag { background: var(--danger-light); color: var(--danger); border-radius: 6px; padding: 3px 9px; font-size: 12px; font-weight: 600; display: inline-block; margin-top: 2px; }

/* KRS items */
.krs-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 10px; border-radius: 8px;
    background: var(--surface2); border: 1px solid var(--border);
    margin-bottom: 6px; font-size: 13.5px;
}
.krs-item-name { font-weight: 600; flex: 1; color: var(--text); }
.krs-badge { background: var(--primary-light); color: var(--primary); border-radius: 6px; padding: 2px 8px; font-size: 12px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }

/* SKS bar */
.sks-bar-bg { background: var(--border); border-radius: 999px; height: 10px; margin: 8px 0 4px; overflow: hidden; }
.sks-bar-fill { height: 100%; border-radius: 999px; transition: width .4s ease; }

/* Streamlit overrides */
div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 22px !important; font-weight: 700 !important; color: var(--primary) !important; }
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; transition: all .15s !important; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,.2) !important; }
div[data-testid="stTabs"] button { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important; }
div[data-testid="stChatInput"] > div { border-radius: 12px !important; border: 1.5px solid var(--border) !important; overflow: hidden !important; }
div[data-testid="stChatInput"] > div:focus-within { border-color: var(--primary) !important; box-shadow: 0 0 0 3px rgba(96,165,250,0.15) !important; }
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem !important; }
div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 13px !important; }

/* Landing page */
.landing-hero {
    min-height: 88vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center; text-align: center;
    padding: 3rem 2rem; position: relative;
}
.landing-logo {
    width: 300px; height: 250px; object-fit: contain;
    filter: drop-shadow(0 8px 24px rgba(96,165,250,0.35));
    margin-bottom: 24px;
    animation: floatLogo 4s ease-in-out infinite;
}
@keyframes floatLogo {
    0%, 100% { transform: translateY(0px); }
    100% { transform: translateY(-8px); }
}
.landing-badge {
    display: inline-block; background: var(--primary-light); color: var(--primary);
    border: 1px solid var(--primary); border-radius: 999px;
    padding: 5px 18px; font-size: 12.5px; font-weight: 700;
    letter-spacing: .5px; margin-bottom: 28px; text-transform: uppercase;
}
.landing-title {
    font-size: clamp(36px, 6vw, 72px); font-weight: 800;
    color: var(--text) !important; line-height: 1.08;
    letter-spacing: -2px; margin: 0 0 20px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}
.landing-title span { color: var(--primary); }
.landing-sub {
    font-size: 17px; color: var(--text-muted) !important;
    max-width: 560px; margin: 0 auto 42px; line-height: 1.7;
}
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 48px 0; max-width: 820px; width: 100%; }
.feature-item {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 22px 18px; text-align: left;
    transition: border-color .2s, transform .2s;
}
.feature-item:hover { border-color: var(--primary); transform: translateY(-3px); }
.feature-icon { font-size: 26px; margin-bottom: 10px; }
.feature-name { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 5px; }
.feature-desc { font-size: 12.5px; color: var(--text-muted); line-height: 1.5; }
.landing-footer { color: var(--text-faint) !important; font-size: 12px; margin-top: 32px; }
.divider-dot { color: var(--border); margin: 0 8px; }

/* Dark mode specific improvements */
.dark-stat-card {
    text-align:center; padding:20px 10px;
    background: var(--surface);
    border-radius:14px; border:1px solid var(--border);
    box-shadow: var(--shadow);
}
.dark-stat-val {
    font-size:32px; font-weight:800;
    color: var(--primary);
    font-family:'JetBrains Mono',monospace;
    text-shadow: 0 0 20px rgba(96,165,250,0.4);
}
.dark-stat-lbl {
    font-size:13px; color: var(--text-muted); margin-top:4px;
}
"""

st.markdown(f"<style>{THEME}{COMMON_CSS}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎨 Tema")
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        if st.button("🌙 Gelap", use_container_width=True, key="btn_dark"):
            st.session_state.dark_mode = True
            st.rerun()
    with col_t2:
        if st.button("☀️ Terang", use_container_width=True, key="btn_light"):
            st.session_state.dark_mode = False
            st.rerun()

    tema_label = "🌙 Tema Gelap" if is_dark else "☀️ Tema Terang"
    st.caption(f"Aktif tema saat ini: **{tema_label}**")
    st.markdown("---")

    st.markdown("### 🧭 Navigasi")
    if st.session_state.show_landing:
        if st.button("Masuk ke Aplikasi", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.rerun()
    else:
        if st.button("Kembali ke Beranda", use_container_width=True):
            st.session_state.show_landing = True
            st.rerun()

    if not st.session_state.show_landing:
        st.markdown("---")
        st.markdown("### 📊 Dashboard KRS")

        total_sks = bot.total_sks()
        max_sks = bot.nlp.MAX_SKS
        pct = int(total_sks / max_sks * 100)
        bar_color = "#f87171" if pct >= 90 else "#fbbf24" if pct >= 70 else "#60a5fa"

        c1, c2 = st.columns(2)
        with c1:
            st.metric("SKS Diambil", f"{total_sks}")
        with c2:
            st.metric("Sisa SKS", f"{max_sks - total_sks}")

        st.markdown(f"""
        <div class="sks-bar-bg">
            <div class="sks-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
        </div>
        <div style="text-align:right;font-size:12px;color:var(--text-muted);">{pct}% dari {max_sks} SKS</div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🗂️ Mata Kuliah Dipilih")
        if bot.cart:
            for c in bot.cart:
                nama = c["course_key"].replace("_", " ").title()
                st.markdown(f"""
                <div class="krs-item">
                    <span>{c['emoji']}</span>
                    <span class="krs-item-name">{nama}</span>
                    <span class="krs-badge">{c['sks']} SKS</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🗑️ Kosongkan KRS", use_container_width=True, type="secondary"):
                bot.cart = []
                st.session_state.history.append({"role": "assistant", "content": "🗑️ KRS berhasil dikosongkan."})
                st.rerun()
        else:
            st.info("Belum ada matkul dipilih.", icon="📭")

        st.markdown("---")
        st.markdown("### ⚙️ Sistem")
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔄 Reset Chat", use_container_width=True):
                dark_backup = st.session_state.dark_mode
                st.session_state.clear()
                st.session_state.dark_mode = dark_backup
                st.session_state.show_landing = False
                st.rerun()
        with cb:
            if st.button("🗑️ Bersihkan Chat", use_container_width=True):
                st.session_state.history = []
                st.rerun()

    st.markdown("---")
    st.caption("SIKRS 2026 · Universitas PGRI Semarang · Powered by Rahul Candra")


# ═════════════════════════════════════════════
# LANDING PAGE
# ═════════════════════════════════════════════
if st.session_state.show_landing:

    st.markdown(f"""
    <div class="landing-hero">
        <img src="data:image/png;base64,{UPGRIS_LOGO_B64}" style="width: 150px; height: auto;" class="landing-logo" alt="Logo UPGRIS" />
        <h1 class="landing-title">
            Susun KRS Lebih<br><span>Cerdas &amp; Cepat</span>
        </h1>
        <p class="landing-sub">
            SIKRS adalah chatbot akademik berbasis <strong>Finite State Machine</strong>
            yang membantu mahasiswa Teknik Informatika untuk menyusun Kartu Rencana Studi dengan validasi
            prasyarat, deteksi konflik jadwal, dan batas SKS secara otomatis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cta_col = st.columns([1, 2, 1])
    with cta_col[1]:
        if st.button("Mulai Susun KRS Sekarang!", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.rerun()

    st.markdown("""
    <div style="display:flex;justify-content:center;margin-top:10px;">
    <div class="feature-grid">
        <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <div class="feature-name">Chatbot</div>
            <div class="feature-desc">Ketik perintah natural seperti "saya ambil algoritma" atau "jadwal saya hari ini".</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">⚠️</div>
            <div class="feature-name">Validasi Otomatis</div>
            <div class="feature-desc">Cek prasyarat, konflik jadwal, dan batas 24 SKS secara real-time.</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📅</div>
            <div class="feature-name">Tampilan Jadwal</div>
            <div class="feature-desc">Lihat jadwal kuliah yang sudah dipilih terurut per hari dalam seminggu.</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📚</div>
            <div class="feature-name">Katalog Interaktif</div>
            <div class="feature-desc">Filter dan cari mata kuliah berdasarkan kategori, semester, atau nama.</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📤</div>
            <div class="feature-name">Submit KRS</div>
            <div class="feature-desc">Alur konfirmasi berlapis sebelum KRS dikirim ke sistem akademik.</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🎨</div>
            <div class="feature-name">Tema</div>
            <div class="feature-desc">Ganti tema kapan saja dari sidebar berlaku di seluruh halaman.</div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("8", "Mata Kuliah"),
        ("24", "Maks SKS"),
        ("3", "State FSM"),
        ("6", "Fitur Utama"),
    ]
    for col, (val, lbl) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="dark-stat-card">
                <div class="dark-stat-val">{val}</div>
                <div class="dark-stat-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="landing-footer" style="text-align:center;margin-top:40px;">
        SIKRS 2026
        <span class="divider-dot">·</span>
        Universitas PGRI Semarang
        <span class="divider-dot">·</span>
        Powered by Rahul Candra
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════
# HALAMAN APLIKASI UTAMA
# ═════════════════════════════════════════════
else:
    state_labels = {
        State.IDLE:         ("🟡", "Idle"),
        State.BROWSING:     ("🟢", "Aktif"),
        State.CONFIRMATION: ("🟠", "Konfirmasi"),
        State.SUBMITTED:    ("🔵", "Selesai"),
    }
    s_icon, s_label = state_labels.get(bot.state, ("⚪", "—"))

    st.markdown(f"""
    <div class="header-banner">
        <img src="data:image/png;base64,{UPGRIS_LOGO_B64}" style="width:100px;height:100px;object-fit:contain;filter:drop-shadow(0 2px 6px rgba(0,0,0,.3));" alt="UPGRIS" />
        <div>
            <p class="header-title">SIKRS - Chatbot Akademik UPGRIS</p>
            <p class="header-sub">Sistem Informasi Kartu Rencana Studi · Program Studi Teknik Informatika · Universitas PGRI Semarang</p>
        </div>
        <div class="header-badge">{s_icon} {s_label}</div>
    </div>
    """, unsafe_allow_html=True)

    tab_chat, tab_catalog, tab_schedule, tab_about = st.tabs([
        "💬 Chatbot",
        "📚 Katalog Matkul",
        "📅 Jadwal Saya",
        "ℹ️ Panduan",
    ])

    # ══════════════════════════════════════════
    # TAB 1: CHAT
    # ══════════════════════════════════════════
    with tab_chat:
        chat_col, _ = st.columns([3, 0.01])
        with chat_col:
            chat_container = st.container(height=520)
            with chat_container:
                for msg in st.session_state.history:
                    avatar = "🎓" if msg["role"] == "assistant" else "🧑‍🎓"
                    with st.chat_message(msg["role"], avatar=avatar):
                        st.markdown(msg["content"])

            prompt = st.chat_input("Contoh: saya ingin mengambbil mata kuliah algoritma dan struktur data")
            if prompt:
                st.session_state.history.append({"role": "user", "content": prompt})
                bot.step(prompt)
                st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                st.rerun()

            st.markdown("**⚡ Aksi Cepat:**")
            qcols = st.columns(5)
            quick_actions = [
                ("📚 Menu", "menu"),
                ("📅 Jadwal", "jadwal"),
                ("📊 Info SKS", "total sks saya"),
                ("📤 Submit KRS", "submit KRS"),
                ("❓ Bantuan", "bantuan"),
            ]
            for i, (label, cmd) in enumerate(quick_actions):
                with qcols[i]:
                    if st.button(label, use_container_width=True, key=f"qa_{i}"):
                        st.session_state.history.append({"role": "user", "content": cmd})
                        bot.step(cmd)
                        st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                        st.rerun()

    # ══════════════════════════════════════════
    # TAB 2: KATALOG
    # ══════════════════════════════════════════
    with tab_catalog:
        st.markdown("### 📚 Katalog Mata Kuliah")
        st.caption("Klik tombol **Tambah ke KRS** untuk langsung mendaftarkan mata kuliah.")
        st.markdown("---")

        fc1, fc2, fc3 = st.columns([1, 1, 2])
        with fc1:
            filter_kat = st.selectbox("Kategori", ["Semua", "Wajib", "Pilihan"])
        with fc2:
            filter_sem = st.selectbox("Semester", ["Semua"] + [str(i) for i in range(1, 9)])
        with fc3:
            search_q = st.text_input("🔍 Cari mata kuliah...", placeholder="Nama, kode, atau dosen")

        st.markdown("---")
        cols = st.columns(2)
        idx = 0

        for key, data in bot.nlp.course_data.items():
            nama = key.replace("_", " ").title()
            if filter_kat != "Semua" and data["kategori"] != filter_kat:
                continue
            if filter_sem != "Semua" and str(data["semester"]) != filter_sem:
                continue
            if search_q:
                sq = search_q.lower()
                if sq not in key and sq not in data["kode"].lower() and sq not in data["dosen"].lower() and sq not in nama.lower():
                    continue

            in_krs = any(c["course_key"] == key for c in bot.cart)
            kat_class = "wajib" if data["kategori"] == "Wajib" else "pilihan"
            prereq_html = (
                f'<span class="prereq-tag">🔒 Prasyarat: {data["prasyarat"].replace("_"," ").title()}</span>'
                if data["prasyarat"] else ""
            )

            with cols[idx % 2]:
                st.markdown(f"""
                <div class="matkul-card">
                    <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:8px;">
                        <div style="font-size:28px;line-height:1.2;">{data["emoji"]}</div>
                        <div>
                            <div class="matkul-name">{nama}</div>
                            <div class="matkul-kode">{data["kode"]} · Sem. {data["semester"]}</div>
                        </div>
                    </div>
                    <div class="matkul-desc">{data["desc"]}</div>
                    <div class="matkul-meta">
                        <span class="meta-tag sks">{data["sks"]} SKS</span>
                        <span class="meta-tag {kat_class}">{data["kategori"]}</span>
                        <span class="meta-tag">🕐 {data["jadwal"]}</span>
                        <span class="meta-tag">📍 {data["ruang"]}</span>
                        <span class="meta-tag">👨‍🏫 {data["dosen"]}</span>
                    </div>
                    {prereq_html}
                </div>
                """, unsafe_allow_html=True)

                if in_krs:
                    st.success("✅ Sudah ada di KRS")
                else:
                    if st.button("➕ Tambah ke KRS", key=f"add_{key}", use_container_width=True):
                        success, msg = bot.add_course(key)
                        st.session_state.history.append({"role": "user", "content": f"ambil {nama}"})
                        st.session_state.history.append({"role": "assistant", "content": msg})
                        st.rerun()

            idx += 1

        if idx == 0:
            st.info("Tidak ada mata kuliah yang sesuai filter.", icon="🔍")

    # ══════════════════════════════════════════
    # TAB 3: JADWAL
    # ══════════════════════════════════════════
    with tab_schedule:
        st.markdown("### 📅 Jadwal Kuliah Saya")
        st.markdown("---")

        if not bot.cart:
            st.info("Belum ada mata kuliah dalam KRS Anda.\nTambahkan dari Tab **Katalog** atau via **Chat**.", icon="📭")
        else:
            days_order = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
            by_day = {d: [] for d in days_order}
            for c in bot.cart:
                for day in days_order:
                    if day in c["jadwal"]:
                        by_day[day].append(c)
                        break

            for day in days_order:
                if not by_day[day]:
                    continue
                st.markdown(f"#### 📆 {day}")
                for c in by_day[day]:
                    nama = c["course_key"].replace("_", " ").title()
                    jam  = c["jadwal"].split(" ", 1)[1] if " " in c["jadwal"] else c["jadwal"]
                    c1, c2, c3, c4 = st.columns([0.4, 2, 2, 1.2])
                    with c1:
                        st.markdown(f"<div style='font-size:24px;text-align:center'>{c['emoji']}</div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"**{nama}** `{c['kode']}`")
                        st.caption(f"⏰ {jam}")
                    with c3:
                        st.markdown(f"📍 {c['ruang']}")
                        st.caption(f"👨‍🏫 {c['dosen']}")
                    with c4:
                        st.markdown(f"""
                        <div style="background:var(--primary-light);color:var(--primary);
                        border-radius:8px;padding:7px 12px;text-align:center;
                        font-weight:700;font-family:'JetBrains Mono',monospace;">{c['sks']} SKS</div>
                        """, unsafe_allow_html=True)
                st.markdown("---")

            st.markdown(f"**Total: {bot.total_sks()} SKS** dari maksimum {bot.nlp.MAX_SKS} SKS")
            if bot.state == State.BROWSING:
                if st.button("📤 Submit KRS Sekarang", type="primary"):
                    bot.step("submit KRS")
                    st.session_state.history.append({"role": "user", "content": "submit KRS"})
                    st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                    st.rerun()

    # ══════════════════════════════════════════
    # TAB 4: PANDUAN
    # ══════════════════════════════════════════
    with tab_about:
        st.markdown("### ℹ️ Panduan & Informasi Sistem")
        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
#### 🤖 Tentang Chatbot
Chatbot ini menggunakan **Finite State Machine (FSM)** dengan engine **NLP berbasis regex** untuk membantu mahasiswa Teknik Informatika **Universitas PGRI Semarang** menyusun KRS.

**State yang tersedia:**
| State | Keterangan |
|-------|-----------|
| 🟢 Browsing | Menjelajah & menambah matkul |
| 🟠 Konfirmasi | Verifikasi sebelum submit |
| 🔵 Selesai | KRS berhasil disubmit |

---
#### ✨ Fitur Utama
1. **📚 Katalog Interaktif** — Filter semua mata kuliah
2. **🛒 Manajemen KRS** — Tambah/hapus via chat atau tombol
3. **⚠️ Validasi Otomatis** — Prasyarat, batas SKS, & konflik jadwal
4. **📅 Tampilan Jadwal** — Jadwal terurut per hari
5. **📤 Submit KRS** — Alur konfirmasi sebelum pengiriman
6. **🎨 Tema Gelap/Terang** — Ganti tema dari sidebar kapan saja
            """)

        with col_b:
            st.markdown("""
#### 💬 Contoh Perintah Chat
```
menu                    → lihat semua matkul
ambil algoritma         → tambah ke KRS
hapus kalkulus          → hapus dari KRS
hapus semua             → kosongkan KRS
jadwal                  → lihat jadwal saya
total sks               → cek total SKS
prasyarat basis data    → cek prasyarat
dosen kecerdasan buatan → info pengajar
submit KRS              → konfirmasi & submit
reset                   → mulai ulang sistem
bantuan                 → panduan lengkap
```

---
#### 📋 Aturan KRS
- **Maksimum SKS:** 24 SKS per semester
- **Prasyarat:** Beberapa matkul mengharuskan matkul tertentu ada di KRS
- **Konflik jadwal:** Matkul dengan jadwal sama tidak bisa diambil bersamaan
            """)

        st.markdown("---")
        st.markdown(f"""
        <div style='text-align:center;color:var(--text-muted);font-size:13px;padding:10px;'>
        SIKRS 2026 · Dikembangkan oleh <b>Rahul Candra<br>
        Mengimplementasikan <b>Finite State Machine</b> & <b>NLP Engine</b>
        · Program Studi Teknik Informatika<br>
        <b>Universitas PGRI Semarang</b>
        </div>
        """, unsafe_allow_html=True)