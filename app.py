import base64
import streamlit as st
from academic_fsm import AcademicFSM, State

# ── Logo ──────────────────────────────────────────────────────────────────────
def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
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
# SESSION STATE
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
if "ratings" not in st.session_state:
    st.session_state.ratings = {}   # course_key → 1-5
if "catalog_filter_kat" not in st.session_state:
    st.session_state.catalog_filter_kat = "Semua"
if "catalog_filter_sem" not in st.session_state:
    st.session_state.catalog_filter_sem = "Semua"
if "catalog_search" not in st.session_state:
    st.session_state.catalog_search = ""

bot     = st.session_state.bot
is_dark = st.session_state.dark_mode

# ─────────────────────────────────────────────
# THEME CSS
# ─────────────────────────────────────────────
DARK_VARS = """
:root {
    --bg:            #080d18;
    --bg2:           #0e1525;
    --surface:       #121c2e;
    --surface2:      #172236;
    --border:        #1e3050;
    --border-hover:  #3a5a8a;
    --primary:       #4f9eff;
    --primary-dark:  #2563eb;
    --primary-light: rgba(79,158,255,0.14);
    --accent:        #06b6d4;
    --success:       #22d3a8;
    --success-light: rgba(34,211,168,0.13);
    --warning:       #fbbf24;
    --warning-light: rgba(251,191,36,0.13);
    --danger:        #f87171;
    --danger-light:  rgba(248,113,113,0.13);
    --text:          #e8f0fe;
    --text-muted:    #7fa8d0;
    --text-faint:    #3d5875;
    --radius:        12px;
    --shadow:        0 4px 24px rgba(0,0,0,.55);
    --glow:          0 0 20px rgba(79,158,255,0.2);
}
.stApp { background: var(--bg) !important; }
section[data-testid="stSidebar"] { background: var(--bg2) !important; border-right:1px solid var(--border) !important; }
div[data-testid="stChatInput"] textarea { background:#172236 !important; color:#e8f0fe !important; caret-color:#4f9eff !important; }
div[data-testid="stChatInput"] textarea::placeholder { color:#3d5875 !important; opacity:1 !important; }
div[data-testid="stChatInput"] > div { background:#172236 !important; }
.stTextInput input { background:#172236 !important; color:#e8f0fe !important; border-color:#1e3050 !important; }
.stTextInput input::placeholder { color:#3d5875 !important; opacity:1 !important; }
.stSelectbox > div > div { background:#172236 !important; color:#e8f0fe !important; }
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div { color:var(--text) !important; }
label, .stSelectbox label, .stTextInput label { color:var(--text) !important; }
.stTabs [data-baseweb="tab"] { color:var(--text-muted) !important; }
.stTabs [aria-selected="true"] { color:var(--text) !important; }
.stButton > button { background-color:#172236 !important; color:#e8f0fe !important; border:1px solid #1e3050 !important; }
.stButton > button:hover { background-color:#1e3050 !important; border-color:#4f9eff !important; color:#fff !important; }
button[data-testid="baseButton-primary"] { background-color:#1d56db !important; border-color:#1d56db !important; color:white !important; }
button[data-testid="baseButton-primary"]:hover { background-color:#1e40af !important; }
.stChatFloatingInputContainer, .stChatFloatingInputContainer > div, .stChatFloatingInputContainer > div > div { background:#080d18 !important; }
div[data-testid="stAlert"] { background:#172236 !important; color:#e8f0fe !important; border-color:#1e3050 !important; }
pre, code, .stCodeBlock pre, div[data-testid="stCodeBlock"] pre { background:#060e1c !important; color:#7dd3fc !important; border:1px solid #1e3050 !important; border-radius:8px !important; }
.stMarkdown code { background:#060e1c !important; color:#4f9eff !important; border:1px solid #1e3050 !important; padding:2px 6px !important; border-radius:4px !important; }
div[data-testid="stMetricValue"] { color:var(--primary) !important; }
"""

LIGHT_VARS = """
:root {
    --bg:            #f0f5ff;
    --bg2:           #ffffff;
    --surface:       #ffffff;
    --surface2:      #f5f8ff;
    --border:        #dde7f5;
    --border-hover:  #b8cfee;
    --primary:       #1a56db;
    --primary-dark:  #1e40af;
    --primary-light: #dbeafe;
    --accent:        #0ea5e9;
    --success:       #059669;
    --success-light: #d1fae5;
    --warning:       #d97706;
    --warning-light: #fef3c7;
    --danger:        #dc2626;
    --danger-light:  #fee2e2;
    --text:          #1e2d45;
    --text-muted:    #5a789e;
    --text-faint:    #9ab3cc;
    --radius:        12px;
    --shadow:        0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(26,86,219,.07);
    --glow:          0 0 20px rgba(26,86,219,0.1);
}
.stApp { background:var(--bg) !important; }
section[data-testid="stSidebar"] { background:var(--surface) !important; border-right:1px solid var(--border) !important; }
"""

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family:'Sora',sans-serif !important; color:var(--text) !important; }
.main .block-container { padding:1.5rem 2rem 2rem !important; max-width:1340px !important; }
.stApp > header, #stDecoration, div[data-testid="stDecoration"] { display:none !important; }
div[data-testid="stHeader"] { background:transparent !important; height:0 !important; min-height:0 !important; }
.main > div:first-child { padding-top:0 !important; }

/* ── Header ── */
.header-banner {
    background: linear-gradient(135deg,#0f2d6e 0%,#1a56db 45%,#0ea5e9 100%);
    border-radius:18px; padding:22px 30px; margin-bottom:20px;
    display:flex; align-items:center; gap:18px;
    box-shadow:0 6px 36px rgba(26,86,219,.4);
    position:relative; overflow:hidden;
}
.header-banner::before {
    content:''; position:absolute; right:-40px; top:-40px;
    width:220px; height:220px; border-radius:50%;
    background:rgba(255,255,255,0.05); pointer-events:none;
}
.header-title { font-size:22px; font-weight:800; color:white !important; margin:0; letter-spacing:-.5px; }
.header-sub { color:rgba(255,255,255,.75) !important; font-size:12.5px; margin:3px 0 0; }
.header-badge {
    margin-left:auto; background:rgba(255,255,255,.18); color:white;
    border:1px solid rgba(255,255,255,.3); border-radius:8px;
    padding:5px 14px; font-size:12px; font-weight:600;
    font-family:'JetBrains Mono',monospace; white-space:nowrap;
}

/* ── Cards ── */
.card {
    background:var(--surface); border-radius:var(--radius);
    padding:18px 20px; border:1px solid var(--border);
    box-shadow:var(--shadow); margin-bottom:14px;
}
.matkul-card {
    background:var(--surface); border-radius:14px;
    padding:18px 20px; border:1px solid var(--border);
    box-shadow:var(--shadow); margin-bottom:14px;
    transition:border-color .2s, box-shadow .2s, transform .2s;
}
.matkul-card:hover {
    border-color:var(--primary); transform:translateY(-2px);
    box-shadow:0 4px 24px rgba(79,158,255,.18);
}
.matkul-name { font-size:15px; font-weight:700; color:var(--text); }
.matkul-kode { font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-muted); margin-top:2px; }
.matkul-desc { font-size:13px; color:var(--text-muted); margin:8px 0 10px; line-height:1.6; }
.matkul-meta { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:8px; }
.meta-tag { background:var(--surface2); border:1px solid var(--border); border-radius:6px; padding:3px 9px; font-size:12px; color:var(--text-muted); }
.meta-tag.sks     { background:var(--primary-light); color:var(--primary); border-color:transparent; font-weight:700; }
.meta-tag.wajib   { background:var(--warning-light); color:var(--warning); border-color:transparent; }
.meta-tag.pilihan { background:var(--success-light); color:var(--success); border-color:transparent; }
.prereq-tag { background:var(--danger-light); color:var(--danger); border-radius:6px; padding:3px 9px; font-size:12px; font-weight:600; display:inline-block; margin-top:4px; }
.tips-box { background:var(--primary-light); border-left:3px solid var(--primary); border-radius:0 8px 8px 0; padding:8px 12px; margin-top:8px; font-size:12.5px; color:var(--text-muted); font-style:italic; }

/* ── Difficulty bar ── */
.diff-bar { display:flex; align-items:center; gap:6px; margin-top:6px; }
.diff-pip { width:16px; height:6px; border-radius:3px; display:inline-block; }
.diff-pip.filled { background:var(--primary); }
.diff-pip.empty  { background:var(--border); }

/* ── KRS items ── */
.krs-item {
    display:flex; align-items:center; gap:8px;
    padding:7px 10px; border-radius:8px;
    background:var(--surface2); border:1px solid var(--border);
    margin-bottom:6px; font-size:13px;
}
.krs-item-name { font-weight:600; flex:1; color:var(--text); }
.krs-badge { background:var(--primary-light); color:var(--primary); border-radius:6px; padding:2px 8px; font-size:12px; font-weight:700; font-family:'JetBrains Mono',monospace; }

/* ── SKS bar ── */
.sks-bar-bg { background:var(--border); border-radius:999px; height:10px; margin:8px 0 4px; overflow:hidden; }
.sks-bar-fill { height:100%; border-radius:999px; transition:width .4s ease; }

/* ── Notif badge ── */
.notif-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--danger); margin-left:6px; vertical-align:middle; animation:pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.4;} }

/* ── Stat cards ── */
.dark-stat-card { text-align:center; padding:20px 10px; background:var(--surface); border-radius:14px; border:1px solid var(--border); box-shadow:var(--shadow); }
.dark-stat-val { font-size:32px; font-weight:800; color:var(--primary); font-family:'JetBrains Mono',monospace; text-shadow:var(--glow); }
.dark-stat-lbl { font-size:13px; color:var(--text-muted); margin-top:4px; }

/* ── Landing ── */
.landing-hero { min-height:86vh; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:3rem 2rem; }
.landing-logo { width:280px; height:auto; object-fit:contain; filter:drop-shadow(0 8px 28px rgba(79,158,255,.4)); margin-bottom:24px; animation:floatLogo 4s ease-in-out infinite alternate; }
@keyframes floatLogo { from{transform:translateY(0);} to{transform:translateY(-10px);} }
.landing-title { font-size:clamp(34px,5.5vw,68px); font-weight:800; color:var(--text) !important; line-height:1.08; letter-spacing:-2px; margin:0 0 18px; }
.landing-title span { color:var(--primary); }
.landing-sub { font-size:16.5px; color:var(--text-muted) !important; max-width:560px; margin:0 auto 36px; line-height:1.75; }
.feature-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:40px 0; max-width:840px; width:100%; }
.feature-item { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:22px 18px; text-align:left; transition:border-color .2s,transform .2s; }
.feature-item:hover { border-color:var(--primary); transform:translateY(-3px); }
.feature-icon { font-size:26px; margin-bottom:10px; }
.feature-name { font-size:14px; font-weight:700; color:var(--text); margin-bottom:5px; }
.feature-desc { font-size:12.5px; color:var(--text-muted); line-height:1.55; }

/* ── Rating stars ── */
.star-row { display:flex; gap:4px; margin:6px 0 2px; }
.star { font-size:18px; cursor:pointer; transition:transform .1s; line-height:1; }
.star:hover { transform:scale(1.2); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:var(--bg2); }
::-webkit-scrollbar-thumb { background:var(--border-hover); border-radius:3px; }

/* metric */
div[data-testid="stMetricValue"] { font-family:'JetBrains Mono',monospace !important; font-size:22px !important; font-weight:700 !important; color:var(--primary) !important; }
div[data-testid="stMetricLabel"] { color:var(--text-muted) !important; font-size:13px !important; }
.stButton > button { border-radius:8px !important; font-weight:600 !important; font-family:'Sora',sans-serif !important; transition:all .15s !important; }
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 4px 14px rgba(0,0,0,.2) !important; }
div[data-testid="stChatInput"] > div { border-radius:12px !important; border:1.5px solid var(--border) !important; overflow:hidden !important; }
div[data-testid="stChatInput"] > div:focus-within { border-color:var(--primary) !important; box-shadow:0 0 0 3px rgba(79,158,255,0.15) !important; }
section[data-testid="stSidebar"] > div { padding:1.4rem 1.1rem !important; }
"""

st.markdown(f"<style>{DARK_VARS if is_dark else LIGHT_VARS}{COMMON_CSS}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Logo kecil
    if UPGRIS_LOGO_B64:
        st.markdown(
            f'<div style="text-align:center;margin-bottom:12px;">'
            f'<img src="data:image/png;base64,{UPGRIS_LOGO_B64}" style="width:72px;opacity:.9;" /></div>',
            unsafe_allow_html=True
        )

    st.markdown("### 🎨 Tema")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("🌙 Gelap", use_container_width=True, key="btn_dark"):
            st.session_state.dark_mode = True; st.rerun()
    with col_t2:
        if st.button("☀️ Terang", use_container_width=True, key="btn_light"):
            st.session_state.dark_mode = False; st.rerun()
    st.caption(f"Tema aktif: **{'🌙 Gelap' if is_dark else '☀️ Terang'}**")

    st.markdown("---")
    st.markdown("### 🧭 Navigasi")
    if st.session_state.show_landing:
        if st.button("Masuk ke Aplikasi", use_container_width=True, type="primary"):
            st.session_state.show_landing = False; st.rerun()
    else:
        if st.button("Kembali ke Beranda", use_container_width=True):
            st.session_state.show_landing = True; st.rerun()

    if not st.session_state.show_landing:
        st.markdown("---")
        st.markdown("### 📊 Dashboard KRS")

        total_sks = bot.total_sks()
        max_sks   = bot.nlp.MAX_SKS
        pct       = int(total_sks / max_sks * 100)
        bar_color = "#f87171" if pct >= 90 else "#fbbf24" if pct >= 70 else "#4f9eff"

        c1, c2 = st.columns(2)
        with c1: st.metric("SKS Diambil", f"{total_sks}")
        with c2: st.metric("Sisa SKS",    f"{max_sks - total_sks}")

        st.markdown(f"""
        <div class="sks-bar-bg">
            <div class="sks-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
        </div>
        <div style="text-align:right;font-size:12px;color:var(--text-muted);">{pct}% dari {max_sks} SKS</div>
        """, unsafe_allow_html=True)

        # Notifikasi
        if bot.notifications:
            st.markdown("---")
            notif_count = len(bot.notifications)
            st.markdown(f"### 🔔 Notifikasi <span class='notif-dot'></span>", unsafe_allow_html=True)
            for n in reversed(bot.notifications[-3:]):
                st.caption(n)

        st.markdown("---")
        st.markdown("### 🗂️ Mata Kuliah Dipilih")
        if bot.cart:
            for c in bot.cart:
                nama = c["course_key"].replace("_", " ").title()
                diff_html = "".join([
                    f'<span class="diff-pip {"filled" if i < c.get("difficulty",2) else "empty"}"></span>'
                    for i in range(5)
                ])
                st.markdown(f"""
                <div class="krs-item">
                    <span>{c['emoji']}</span>
                    <div style="flex:1">
                        <span class="krs-item-name">{nama}</span>
                        <div class="diff-bar">{diff_html}</div>
                    </div>
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
            if st.button("🔄 Reset", use_container_width=True):
                dark_backup = st.session_state.dark_mode
                st.session_state.clear()
                st.session_state.dark_mode     = dark_backup
                st.session_state.show_landing  = False
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
    st.markdown(f"""
    <div class="landing-hero">
        <img src="data:image/png;base64,{UPGRIS_LOGO_B64}" class="landing-logo" alt="Logo UPGRIS" />
        <h1 class="landing-title">Susun KRS Lebih<br><span>Cerdas &amp; Cepat</span></h1>
        <p class="landing-sub">
            SIKRS adalah chatbot akademik berbasis <strong>Finite State Machine</strong>
            yang membantu mahasiswa Teknik Informatika UPGRIS menyusun KRS dengan data jadwal
            real, validasi prasyarat, deteksi konflik jadwal, dan tips belajar otomatis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cta_col = st.columns([1, 2, 1])
    with cta_col[1]:
        if st.button("🚀 Mulai Susun KRS Sekarang!", use_container_width=True, type="primary"):
            st.session_state.show_landing = False; st.rerun()

    st.markdown("""
    <div style="display:flex;justify-content:center;margin-top:10px;">
    <div class="feature-grid">
        <div class="feature-item"><div class="feature-icon">🤖</div><div class="feature-name">Chatbot Pintar</div><div class="feature-desc">Ketik perintah natural. Chatbot memahami nama matkul, dosen, dan jadwal real UPGRIS.</div></div>
        <div class="feature-item"><div class="feature-icon">⚠️</div><div class="feature-name">Validasi Real-time</div><div class="feature-desc">Cek prasyarat, konflik jadwal, dan batas 24 SKS secara otomatis.</div></div>
        <div class="feature-item"><div class="feature-icon">💡</div><div class="feature-name">Tips Belajar</div><div class="feature-desc">Setiap matkul dilengkapi tips belajar spesifik agar nilai optimal.</div></div>
        <div class="feature-item"><div class="feature-icon">🎚️</div><div class="feature-name">Rating Kesulitan</div><div class="feature-desc">Lihat dan bandingkan tingkat kesulitan setiap matkul sebelum mendaftar.</div></div>
        <div class="feature-item"><div class="feature-icon">🔔</div><div class="feature-name">Notifikasi</div><div class="feature-desc">Pantau perubahan KRS Anda lewat panel notifikasi di sidebar.</div></div>
        <div class="feature-item"><div class="feature-icon">⭐</div><div class="feature-name">Rating Matkul</div><div class="feature-desc">Beri rating bintang untuk setiap matkul sebagai referensi semester depan.</div></div>
        <div class="feature-item"><div class="feature-icon">🤖</div><div class="feature-name">Rekomendasi AI</div><div class="feature-desc">Dapat rekomendasi matkul berdasarkan KRS yang sudah dipilih.</div></div>
        <div class="feature-item"><div class="feature-icon">📅</div><div class="feature-name">Jadwal Visual</div><div class="feature-desc">Jadwal terurut per hari dan bisa langsung submit KRS dari tab jadwal.</div></div>
        <div class="feature-item"><div class="feature-icon">🎨</div><div class="feature-name">Tema Gelap/Terang</div><div class="feature-desc">Ganti tema kapan saja dari sidebar untuk kenyamanan belajar Anda.</div></div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, (val, lbl) in zip([s1,s2,s3,s4], [("11","Mata Kuliah"),("24","Maks SKS"),("4","State FSM"),("9","Fitur Utama")]):
        with col:
            st.markdown(f'<div class="dark-stat-card"><div class="dark-stat-val">{val}</div><div class="dark-stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;color:var(--text-faint);font-size:12px;margin-top:36px;">SIKRS 2026 · Universitas PGRI Semarang · Powered by Rahul Candra</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════
# HALAMAN APLIKASI UTAMA
# ═════════════════════════════════════════════
else:
    state_labels = {
        State.IDLE:         ("🟡","Idle"),
        State.BROWSING:     ("🟢","Aktif"),
        State.CONFIRMATION: ("🟠","Konfirmasi"),
        State.SUBMITTED:    ("🔵","Selesai"),
    }
    s_icon, s_label = state_labels.get(bot.state, ("⚪","—"))

    st.markdown(f"""
    <div class="header-banner">
        <img src="data:image/png;base64,{UPGRIS_LOGO_B64}" style="width:90px;height:90px;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));" alt="UPGRIS" />
        <div>
            <p class="header-title">SIKRS — Chatbot Akademik UPGRIS</p>
            <p class="header-sub">Sistem Informasi Kartu Rencana Studi · Teknik Informatika · Universitas PGRI Semarang</p>
        </div>
        <div class="header-badge">{s_icon} {s_label}</div>
    </div>
    """, unsafe_allow_html=True)

    tab_chat, tab_catalog, tab_schedule, tab_tips, tab_about = st.tabs([
        "💬 Chatbot",
        "📚 Katalog Matkul",
        "📅 Jadwal Saya",
        "💡 Tips & Fakta",
        "ℹ️ Panduan",
    ])

    # ═══════════════════════════════
    # TAB 1: CHAT
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
                st.session_state.history.append({"role":"user","content":prompt})
                bot.step(prompt)
                st.session_state.history.append({"role":"assistant","content":bot.get_response()})
                st.rerun()

            st.markdown("**⚡ Aksi Cepat:**")
            q1, q2, q3, q4, q5, q6 = st.columns(6)
            quick_actions = [
                ("📚 Menu",       "menu"),
                ("🤖 Rekomen",    "rekomen"),
                ("📅 Jadwal",     "jadwal"),
                ("📊 SKS",        "total sks saya"),
                ("📤 Submit",     "submit KRS"),
                ("❓ Bantuan",    "bantuan"),
            ]
            for col, (label, cmd) in zip([q1,q2,q3,q4,q5,q6], quick_actions):
                with col:
                    if st.button(label, use_container_width=True, key=f"qa_{cmd}"):
                        st.session_state.history.append({"role":"user","content":cmd})
                        bot.step(cmd)
                        st.session_state.history.append({"role":"assistant","content":bot.get_response()})
                        st.rerun()

    # ═══════════════════════════════
    # TAB 2: KATALOG
    # ═══════════════════════════════
    with tab_catalog:
        st.markdown("### 📚 Katalog Mata Kuliah")
        st.caption("Data jadwal real dari UPGRIS Semester Genap 2025/2026 · Klik **Tambah ke KRS** atau beri ⭐ rating.")
        st.markdown("---")

        fc1, fc2, fc3 = st.columns([1,1,2])
        with fc1: filter_kat = st.selectbox("Kategori", ["Semua","Wajib","Pilihan"])
        with fc2: filter_sem = st.selectbox("Semester",  ["Semua","2","4"])
        with fc3: search_q   = st.text_input("🔍 Cari matkul, dosen, kode...", placeholder="contoh: web, Ramadhan, IF203")

        st.markdown("---")
        cols = st.columns(2)
        idx  = 0

        for key, data in bot.nlp.course_data.items():
            nama = key.replace("_", " ").title()
            if filter_kat != "Semua" and data["kategori"] != filter_kat: continue
            if filter_sem != "Semua" and str(data["semester"]) != filter_sem: continue
            if search_q:
                sq = search_q.lower()
                if not any(sq in x for x in [key, data["kode"].lower(), data["dosen"].lower(), nama.lower()]): continue

            in_krs    = any(c["course_key"] == key for c in bot.cart)
            kat_class = "wajib" if data["kategori"] == "Wajib" else "pilihan"
            prereq_html = (
                f'<span class="prereq-tag">🔒 Prasyarat: {data["prasyarat"].replace("_"," ").title()}</span>'
                if data["prasyarat"] else ""
            )
            diff_pips = "".join([
                f'<span class="diff-pip {"filled" if i < data["difficulty"] else "empty"}"></span>'
                for i in range(5)
            ])
            user_rating = st.session_state.ratings.get(key, 0)
            stars_display = "⭐" * user_rating + "☆" * (5 - user_rating) if user_rating else "☆☆☆☆☆"

            with cols[idx % 2]:
                st.markdown(f"""
                <div class="matkul-card">
                    <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:8px;">
                        <div style="font-size:28px;line-height:1.2;">{data["emoji"]}</div>
                        <div style="flex:1">
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
                    <div style="margin:6px 0 4px;">
                        <span style="font-size:12px;color:var(--text-muted);">Kesulitan:</span>
                        <div class="diff-bar">{diff_pips}</div>
                    </div>
                    {prereq_html}
                    <div class="tips-box">💡 {data["tips"]}</div>
                </div>
                """, unsafe_allow_html=True)

                # Rating
                rating_cols = st.columns([2, 3])
                with rating_cols[0]:
                    if in_krs:
                        st.success("✅ Di KRS")
                    else:
                        if st.button("➕ Tambah ke KRS", key=f"add_{key}", use_container_width=True):
                            success, msg = bot.add_course(key)
                            st.session_state.history.append({"role":"user","content":f"ambil {nama}"})
                            st.session_state.history.append({"role":"assistant","content":msg})
                            st.rerun()
                with rating_cols[1]:
                    new_rating = st.select_slider(
                        f"Rating {data['emoji']}",
                        options=[0,1,2,3,4,5],
                        value=user_rating,
                        format_func=lambda x: "☆☆☆☆☆" if x==0 else "⭐"*x+"☆"*(5-x),
                        key=f"rating_{key}",
                        label_visibility="collapsed"
                    )
                    if new_rating != user_rating:
                        st.session_state.ratings[key] = new_rating
                        st.rerun()
                    if user_rating:
                        st.caption(f"Rating Anda: {'⭐'*user_rating}")

            idx += 1

        if idx == 0:
            st.info("Tidak ada matkul yang sesuai filter.", icon="🔍")

    # ═══════════════════════════════
    # TAB 3: JADWAL
    # ═══════════════════════════════
    with tab_schedule:
        st.markdown("### 📅 Jadwal Kuliah Saya")
        st.markdown("---")

        if not bot.cart:
            st.info("Belum ada mata kuliah dalam KRS.\nTambahkan dari **Katalog** atau via **Chat**.", icon="📭")
        else:
            days_order = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"]
            by_day = {d: [] for d in days_order}
            for c in bot.cart:
                for day in days_order:
                    if day in c["jadwal"]:
                        by_day[day].append(c); break

            for day in days_order:
                if not by_day[day]: continue
                st.markdown(f"#### 📆 {day}")
                for c in by_day[day]:
                    nama = c["course_key"].replace("_"," ").title()
                    jam  = c["jadwal"].split(" ",1)[1] if " " in c["jadwal"] else c["jadwal"]
                    diff_pips = "".join([
                        f'<span class="diff-pip {"filled" if i < c.get("difficulty",2) else "empty"}"></span>'
                        for i in range(5)
                    ])
                    cl1,cl2,cl3,cl4 = st.columns([0.4,2.2,2,1])
                    with cl1: st.markdown(f'<div style="font-size:26px;text-align:center">{c["emoji"]}</div>', unsafe_allow_html=True)
                    with cl2:
                        st.markdown(f"**{nama}** `{c['kode']}`")
                        st.caption(f"⏰ {jam}")
                    with cl3:
                        st.markdown(f"📍 {c['ruang']}")
                        st.caption(f"👨‍🏫 {c['dosen']}")
                    with cl4:
                        st.markdown(f"""<div style="background:var(--primary-light);color:var(--primary);
                        border-radius:8px;padding:7px 12px;text-align:center;
                        font-weight:700;font-family:'JetBrains Mono',monospace;">{c['sks']} SKS</div>
                        <div class="diff-bar" style="justify-content:center;margin-top:6px;">{diff_pips}</div>
                        """, unsafe_allow_html=True)
                st.markdown("---")

            pct = int(bot.total_sks() / bot.nlp.MAX_SKS * 100)
            bar_color = "#f87171" if pct>=90 else "#fbbf24" if pct>=70 else "#4f9eff"
            st.markdown(f"""
            **Total: {bot.total_sks()} SKS** dari maksimum {bot.nlp.MAX_SKS} SKS
            <div class="sks-bar-bg" style="max-width:400px;">
                <div class="sks-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
            </div>
            <div style="font-size:12px;color:var(--text-muted);">{pct}% terisi</div>
            """, unsafe_allow_html=True)

            if bot.state == State.BROWSING:
                st.markdown("")
                if st.button("📤 Submit KRS Sekarang", type="primary"):
                    bot.step("submit KRS")
                    st.session_state.history.append({"role":"user","content":"submit KRS"})
                    st.session_state.history.append({"role":"assistant","content":bot.get_response()})
                    st.rerun()

    # ═══════════════════════════════
    # TAB 4: TIPS & FAKTA
    # ═══════════════════════════════
    with tab_tips:
        st.markdown("### 💡 Tips Belajar & Fakta Akademik")
        st.markdown("---")

        # Fakta akademik
        from academic_fsm import ACADEMIC_FACTS
        st.markdown("#### 🧠 Fakta & Strategi Belajar")
        fact_cols = st.columns(2)
        for i, fact in enumerate(ACADEMIC_FACTS):
            with fact_cols[i % 2]:
                st.markdown(f"""
                <div class="card" style="border-left:3px solid var(--primary);">
                    <div style="font-size:14px;line-height:1.7;color:var(--text);">{fact}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📚 Tips Per Mata Kuliah")
        for key, data in bot.nlp.course_data.items():
            nama = key.replace("_"," ").title()
            with st.expander(f"{data['emoji']} {nama} — Tips Belajar"):
                stars = "⭐" * data["difficulty"] + "☆" * (5 - data["difficulty"])
                st.markdown(f"**Tingkat Kesulitan:** {stars} ({data['difficulty']}/5)")
                st.markdown(f"**Dosen:** {data['dosen']}")
                st.markdown(f"**Jadwal:** {data['jadwal']} · {data['ruang']}")
                st.info(data["tips"], icon="💡")

        st.markdown("---")
        st.markdown("#### 🏆 Perbandingan Kesulitan Matkul")
        import json
        diff_data = {key.replace("_"," ").title(): data["difficulty"] for key, data in bot.nlp.course_data.items()}
        chart_rows = []
        for nama, diff in sorted(diff_data.items(), key=lambda x: -x[1]):
            bar = "█" * diff + "░" * (5 - diff)
            chart_rows.append(f"`{bar}` {nama} ({diff}/5)")
        st.markdown("\n\n".join(chart_rows))

    # ═══════════════════════════════
    # TAB 5: PANDUAN
    # ═══════════════════════════════
    with tab_about:
        st.markdown("### ℹ️ Panduan & Informasi Sistem")
        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
#### 🤖 Tentang SIKRS
Chatbot ini menggunakan **Finite State Machine (FSM)** dengan **NLP Engine berbasis Regex** untuk membantu mahasiswa Teknik Informatika **UPGRIS** menyusun KRS. Data matkul dan jadwal diambil dari data resmi UPGRIS Semester Genap 2025/2026.

**State FSM:**
| State | Ikon | Keterangan |
|-------|------|-----------|
| Browsing | 🟢 | Menjelajah & menambah matkul |
| Konfirmasi | 🟠 | Verifikasi sebelum submit |
| Selesai | 🔵 | KRS berhasil disubmit |

---
#### ✨ Fitur Lengkap
1. 💬 **Chatbot NLP** — Pahami perintah natural bahasa Indonesia
2. 📚 **Katalog Interaktif** — Filter semester, kategori, pencarian
3. 🛒 **Manajemen KRS** — Tambah/hapus via chat atau tombol
4. ⚠️ **Validasi Otomatis** — Prasyarat, konflik jadwal, batas SKS
5. 🤖 **Rekomendasi AI** — Saran matkul berdasarkan KRS aktif
6. 💡 **Tips Belajar** — Tips spesifik per matkul
7. 🎚️ **Rating Kesulitan** — Indikator tingkat kesulitan visual
8. ⭐ **Rating User** — Beri bintang untuk setiap matkul
9. 🔔 **Notifikasi** — Panel riwayat perubahan KRS
10. 📅 **Jadwal Visual** — Tersusun per hari + submit langsung
11. 🎨 **Tema Gelap/Terang** — Ganti tema kapan saja
            """)

        with col_b:
            st.markdown("""
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
notifikasi              → riwayat perubahan
submit KRS              → konfirmasi & kirim
reset                   → mulai ulang
bantuan                 → panduan ini
```

---
#### 📋 Aturan KRS
- **Maksimum SKS:** 24 SKS per semester
- **Prasyarat:** Beberapa matkul butuh matkul lain di KRS
- **Konflik:** Jadwal yang sama tidak bisa diambil bersamaan
- **Data jadwal:** Real dari UPGRIS Sem. Genap 2025/2026
            """)

        st.markdown("---")
        st.markdown(f"""
        <div style='text-align:center;color:var(--text-muted);font-size:13px;padding:10px;'>
        SIKRS 2026 · Dikembangkan oleh <b>Rahul Candra</b><br>
        Mengimplementasikan <b>Finite State Machine</b> &amp; <b>NLP Engine</b><br>
        Program Studi Teknik Informatika · <b>Universitas PGRI Semarang</b>
        </div>
        """, unsafe_allow_html=True)