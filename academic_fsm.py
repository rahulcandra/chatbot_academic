from enum import Enum, auto
from nlp_engine import AcademicNLPEngine
import random


class State(Enum):
    IDLE         = auto()
    BROWSING     = auto()
    CONFIRMATION = auto()
    SUBMITTED    = auto()


# Fakta / trivia akademik yang ditampilkan secara random
ACADEMIC_FACTS = [
    "💡 Mahasiswa yang tidur 7–8 jam semalam sebelum ujian rata-rata mendapat nilai 15% lebih tinggi.",
    "📚 Metode Pomodoro (25 menit belajar, 5 menit istirahat) terbukti meningkatkan fokus hingga 40%.",
    "🧠 Belajar dengan mengajari orang lain (Feynman Technique) adalah cara paling efektif menguasai materi.",
    "⏰ Puncak konsentrasi otak manusia terjadi antara pukul 09.00–11.00 dan 14.00–16.00.",
    "🎯 Membuat rangkuman tulis tangan meningkatkan retensi ingatan 3× lebih baik dari mengetik.",
    "☕ Kafein meningkatkan fokus jangka pendek, tapi tidur berkualitas jauh lebih efektif jangka panjang.",
]


class AcademicFSM:
    def __init__(self):
        self.state          = State.IDLE
        self.nlp            = AcademicNLPEngine()
        self.cart           = []
        self.response       = ""
        self.submitted_krs  = None
        self.notifications  = []   # antrian notifikasi
        self.session_count  = 0    # jumlah interaksi
        self.ratings        = {}   # course_key → int(1‑5)

    # ── helpers ──────────────────────────────────────────────────────────────

    def get_response(self):
        return self.response

    def total_sks(self):
        return sum(c["sks"] for c in self.cart)

    def get_catalog_text(self):
        lines = ["📚 *Katalog Mata Kuliah Tersedia:*\n"]
        semester_now = None
        for key, data in self.nlp.course_data.items():
            if data["semester"] != semester_now:
                semester_now = data["semester"]
                lines.append(f"\n*── Semester {semester_now} ──*")
            nama = key.replace("_", " ").title()
            stars = "⭐" * data["difficulty"]
            lines.append(
                f"{data['emoji']} *{nama}* ({data['kode']}) "
                f"— {data['sks']} SKS | {data['kategori']} | {stars}\n"
                f"   _{data['desc']}_\n"
                f"   🕐 {data['jadwal']} · 👨‍🏫 {data['dosen']}\n"
            )
        lines.append(
            "💡 Ketik *'ambil [nama matkul]'* untuk mendaftarkan, "
            "atau *'info [nama matkul]'* untuk detail lengkap."
        )
        return "\n".join(lines)

    def get_schedule_text(self):
        if not self.cart:
            return "📅 Belum ada mata kuliah di KRS Anda."
        days_order = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        by_day = {d: [] for d in days_order}
        for c in self.cart:
            for day in days_order:
                if day in c["jadwal"]:
                    by_day[day].append(c)
                    break
        lines = ["📅 *Jadwal Kuliah Anda:*\n"]
        for day in days_order:
            if not by_day[day]:
                continue
            lines.append(f"*{day}*")
            for c in by_day[day]:
                nama = c["course_key"].replace("_", " ").title()
                jam  = c["jadwal"].split(" ", 1)[1] if " " in c["jadwal"] else c["jadwal"]
                lines.append(
                    f"  {c['emoji']} {nama} — {jam}\n"
                    f"     📍 {c['ruang']} · 👨‍🏫 {c['dosen']}"
                )
            lines.append("")
        return "\n".join(lines)

    def check_conflict(self, new_course_key):
        new = self.nlp.course_data[new_course_key]
        for c in self.cart:
            existing = self.nlp.course_data[c["course_key"]]
            if existing["jadwal"] == new["jadwal"]:
                return c["course_key"]
        return None

    def add_course(self, course_key):
        data = self.nlp.course_data[course_key]
        nama = course_key.replace("_", " ").title()

        if any(c["course_key"] == course_key for c in self.cart):
            return False, f"⚠️ *{nama}* sudah ada di KRS Anda."

        if self.total_sks() + data["sks"] > self.nlp.MAX_SKS:
            sisa = self.nlp.MAX_SKS - self.total_sks()
            return False, (
                f"❌ Tidak bisa menambahkan *{nama}* ({data['sks']} SKS).\n"
                f"Sisa kapasitas SKS: {sisa} dari {self.nlp.MAX_SKS} SKS."
            )

        if data["prasyarat"]:
            pr_key  = data["prasyarat"]
            in_cart = any(c["course_key"] == pr_key for c in self.cart)
            pr_nama = pr_key.replace("_", " ").title()
            if not in_cart:
                return False, (
                    f"❌ *{nama}* memerlukan prasyarat: *{pr_nama}*.\n"
                    f"Silakan tambahkan *{pr_nama}* terlebih dahulu."
                )

        conflict = self.check_conflict(course_key)
        if conflict:
            conflict_nama = conflict.replace("_", " ").title()
            return False, (
                f"❌ Jadwal *{nama}* bentrok dengan *{conflict_nama}*!\n"
                f"Keduanya dijadwalkan pada: {data['jadwal']}."
            )

        self.cart.append({
            "course_key": course_key,
            "kode":       data["kode"],
            "sks":        data["sks"],
            "jadwal":     data["jadwal"],
            "ruang":      data["ruang"],
            "dosen":      data["dosen"],
            "emoji":      data["emoji"],
            "difficulty": data["difficulty"],
            "tips":       data["tips"],
        })
        self.push_notification(f"✅ {nama} ditambahkan ke KRS")
        return True, (
            f"✅ *{nama}* ({data['sks']} SKS) berhasil ditambahkan!\n"
            f"📊 Total SKS: {self.total_sks()}/{self.nlp.MAX_SKS}\n"
            f"💡 Tips: _{data['tips']}_"
        )

    def remove_course(self, course_key):
        nama   = course_key.replace("_", " ").title()
        before = len(self.cart)
        self.cart = [c for c in self.cart if c["course_key"] != course_key]
        if len(self.cart) < before:
            self.push_notification(f"🗑️ {nama} dihapus dari KRS")
            return f"🗑️ *{nama}* berhasil dihapus dari KRS."
        return f"⚠️ *{nama}* tidak ditemukan di KRS Anda."

    def get_krs_summary(self):
        if not self.cart:
            return "📋 KRS Anda masih kosong."
        lines = ["📋 *Ringkasan KRS Anda:*\n"]
        total_diff = 0
        for c in self.cart:
            nama = c["course_key"].replace("_", " ").title()
            stars = "⭐" * c.get("difficulty", 2)
            lines.append(f"{c['emoji']} {nama} ({c['kode']}) — {c['sks']} SKS {stars}")
            total_diff += c.get("difficulty", 2)
        avg_diff = total_diff / len(self.cart) if self.cart else 0
        diff_label = "Ringan 😊" if avg_diff < 2.5 else "Sedang 🤔" if avg_diff < 3.5 else "Berat 😤"
        lines.append(f"\n📊 *Total SKS: {self.total_sks()} dari {self.nlp.MAX_SKS} SKS*")
        lines.append(f"🎚️ *Beban belajar rata-rata: {diff_label}*")
        return "\n".join(lines)

    def push_notification(self, msg):
        self.notifications.append(msg)
        if len(self.notifications) > 5:
            self.notifications.pop(0)

    def get_notifications(self):
        if not self.notifications:
            return "🔔 Tidak ada notifikasi baru."
        lines = ["🔔 *Notifikasi Terbaru:*\n"]
        for n in reversed(self.notifications):
            lines.append(f"• {n}")
        return "\n".join(lines)

    # ── main FSM step ─────────────────────────────────────────────────────────

    def step(self, user_input=""):
        user_input       = user_input.strip()
        self.session_count += 1

        # Sapa pertama kali
        if user_input == "" and self.state == State.IDLE:
            self.state    = State.BROWSING
            fact          = random.choice(ACADEMIC_FACTS)
            self.response = (
                "*Selamat datang di SIKRS — Chatbot KRS UPGRIS! 👋*\n\n"
                "Saya siap membantu Anda menyusun Kartu Rencana Studi "
                "dengan data jadwal resmi semester ini.\n\n"
                "Yang bisa saya bantu:\n"
                "• Lihat daftar matkul → ketik *'menu'*\n"
                "• Tambah matkul → ketik *'ambil [nama matkul]'*\n"
                "• Tips belajar → ketik *'tips [nama matkul]'*\n"
                "• Rekomendasi matkul → ketik *'rekomen'*\n"
                "• Lihat jadwal → ketik *'jadwal'*\n"
                "• Submit KRS → ketik *'submit KRS'*\n\n"
                f"📌 *Fakta Akademik Hari Ini:*\n{fact}\n\n"
                "Ketik *'bantuan'* untuk panduan lengkap."
            )
            return

        intent = self.nlp.detect_intent(user_input)

        # ── intent global (semua state) ───────────────────────────────────────
        if intent == "RESET_SYSTEM":
            dark_mode = getattr(self, "_dark_mode", True)
            self.__init__()
            self.state    = State.BROWSING
            self.response = "🔄 Sistem direset. Ketik *'menu'* untuk mulai."
            return

        if intent == "GREETING":
            greetings = [
                f"👋 Halo! Siap bantu susun KRS Anda. Ketik *'menu'* untuk lihat daftar matkul.",
                f"😊 Hai! Ada yang bisa saya bantu? Coba ketik *'rekomendasi'* untuk saran matkul.",
                f"🎓 Halo! Ingat, batas SKS semester ini {self.nlp.MAX_SKS} SKS. Ketik *'menu'* untuk mulai!",
            ]
            self.response = random.choice(greetings)
            return

        if intent == "HELP":
            self.response = (
                "📖 *Panduan Lengkap SIKRS:*\n\n"
                "🔍 *Informasi Matkul:*\n"
                "• `menu` — Daftar semua matkul\n"
                "• `info web` — Detail matkul pemrograman web\n"
                "• `prasyarat aps` — Cek prasyarat APS\n"
                "• `tips iot` — Tips belajar IoT\n"
                "• `dosen matdis` — Info dosen Matematika Diskrit\n"
                "• `susah matdis` — Tingkat kesulitan matkul\n\n"
                "➕ *Kelola KRS:*\n"
                "• `ambil struktur data` — Tambah ke KRS\n"
                "• `hapus sistem operasi` — Hapus dari KRS\n"
                "• `hapus semua` — Kosongkan KRS\n"
                "• `krs saya` — Ringkasan KRS\n\n"
                "🤖 *Fitur Cerdas:*\n"
                "• `rekomen` — Rekomendasi matkul untukmu\n"
                "• `notifikasi` — Lihat notifikasi terbaru\n"
                "• `total sks` — Cek kapasitas SKS\n\n"
                "📤 *Submit:*\n"
                "• `submit KRS` — Konfirmasi & kirim KRS\n"
                "• `reset` — Mulai ulang dari awal"
            )
            return

        # ── STATE: BROWSING ───────────────────────────────────────────────────
        if self.state == State.BROWSING:

            if intent == "ASK_MENU":
                self.response = self.get_catalog_text()

            elif intent == "ASK_SCHEDULE":
                self.response = self.get_schedule_text()

            elif intent == "ASK_SKS":
                pct    = int(self.total_sks() / self.nlp.MAX_SKS * 100)
                status = "🔴 Hampir penuh!" if pct >= 90 else "🟡 Mendekati batas." if pct >= 70 else "🟢 Masih aman."
                self.response = (
                    f"📊 SKS diambil: *{self.total_sks()} SKS* {status}\n"
                    f"Kapasitas: *{self.nlp.MAX_SKS} SKS*\n"
                    f"Sisa: *{self.nlp.MAX_SKS - self.total_sks()} SKS*\n"
                    f"Progres: [{('█' * (pct // 10)).ljust(10, '░')}] {pct}%"
                )

            elif intent == "ASK_PREREQ":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    data    = self.nlp.course_data[course_key]
                    nama    = course_key.replace("_", " ").title()
                    if data["prasyarat"]:
                        pr_nama = data["prasyarat"].replace("_", " ").title()
                        in_cart = any(c["course_key"] == data["prasyarat"] for c in self.cart)
                        status  = "✅ Sudah ada di KRS Anda!" if in_cart else "⚠️ Belum ada di KRS."
                        self.response = f"📋 Prasyarat *{nama}*: *{pr_nama}*\n{status}"
                    else:
                        self.response = f"✅ *{nama}* tidak memiliki prasyarat. Bisa langsung diambil!"
                else:
                    self.response = "Matkul apa yang ingin dicek prasyaratnya?\nContoh: *'prasyarat web'*"

            elif intent == "ASK_LECTURER":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    data = self.nlp.course_data[course_key]
                    nama = course_key.replace("_", " ").title()
                    self.response = (
                        f"👨‍🏫 Dosen *{nama}*: *{data['dosen']}*\n"
                        f"📅 Jadwal: {data['jadwal']} | 📍 Ruang: {data['ruang']}"
                    )
                else:
                    self.response = "Matkul apa yang ingin dicek dosennya?\nContoh: *'dosen matdis'*"

            elif intent == "ASK_TIPS":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    data = self.nlp.course_data[course_key]
                    nama = course_key.replace("_", " ").title()
                    self.response = f"💡 *Tips belajar {nama}:*\n\n_{data['tips']}_"
                else:
                    self.response = f"💡 *Tips Akademik:*\n\n{random.choice(ACADEMIC_FACTS)}"

            elif intent == "ASK_DIFFICULTY":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    data   = self.nlp.course_data[course_key]
                    nama   = course_key.replace("_", " ").title()
                    stars  = "⭐" * data["difficulty"] + "☆" * (5 - data["difficulty"])
                    labels = {1: "Sangat mudah", 2: "Mudah", 3: "Sedang", 4: "Sulit", 5: "Sangat sulit"}
                    self.response = (
                        f"🎚️ Tingkat kesulitan *{nama}*:\n"
                        f"{stars} — {labels[data['difficulty']]} ({data['difficulty']}/5)\n\n"
                        f"💡 _{data['tips']}_"
                    )
                else:
                    lines = ["🎚️ *Peringkat Kesulitan Matkul:*\n"]
                    sorted_courses = sorted(
                        self.nlp.course_data.items(),
                        key=lambda x: -x[1]["difficulty"]
                    )
                    for key, data in sorted_courses:
                        nama  = key.replace("_", " ").title()
                        stars = "⭐" * data["difficulty"]
                        lines.append(f"{data['emoji']} {nama} — {stars}")
                    self.response = "\n".join(lines)

            elif intent == "ASK_WAJIB":
                wajib   = [(k, d) for k, d in self.nlp.course_data.items() if d["kategori"] == "Wajib"]
                pilihan = [(k, d) for k, d in self.nlp.course_data.items() if d["kategori"] == "Pilihan"]
                lines   = ["📚 *Kategori Mata Kuliah:*\n\n*Wajib:*"]
                for k, d in wajib:
                    lines.append(f"  {d['emoji']} {k.replace('_', ' ').title()} ({d['sks']} SKS)")
                lines.append("\n*Pilihan:*")
                for k, d in pilihan:
                    lines.append(f"  {d['emoji']} {k.replace('_', ' ').title()} ({d['sks']} SKS)")
                self.response = "\n".join(lines)

            elif intent == "ASK_REKOMENDASI":
                recs = self.nlp.get_recommendations(self.cart)
                if not recs:
                    self.response = "🎉 Semua matkul yang tersedia sudah ada di KRS Anda!"
                else:
                    lines = ["🤖 *Rekomendasi Matkul untuk Anda:*\n"]
                    for key, data in recs:
                        nama = key.replace("_", " ").title()
                        stars = "⭐" * data["difficulty"]
                        lines.append(
                            f"{data['emoji']} *{nama}* ({data['sks']} SKS) — {stars}\n"
                            f"   {data['jadwal']} · {data['dosen']}\n"
                            f"   💡 _{data['tips']}_\n"
                        )
                    lines.append("Ketik *'ambil [nama matkul]'* untuk mendaftarkan.")
                    self.response = "\n".join(lines)

            elif intent == "ASK_SUMMARY":
                self.response = self.get_krs_summary()

            elif user_input.lower() in ("notifikasi", "notif", "notification"):
                self.response = self.get_notifications()

            elif intent == "CANCEL_ALL":
                self.cart     = []
                self.push_notification("🗑️ Semua matkul dihapus dari KRS")
                self.response = "🗑️ Semua mata kuliah berhasil dihapus dari KRS."

            elif intent == "REMOVE_ITEM":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    self.response = self.remove_course(course_key)
                else:
                    self.response = "Matkul apa yang ingin dihapus?\nContoh: *'hapus matdis'*"

            elif intent == "CHECKOUT":
                if not self.cart:
                    self.response = "🛒 KRS kosong. Silakan tambahkan matkul terlebih dahulu."
                else:
                    self.state    = State.CONFIRMATION
                    self.response = (
                        f"{self.get_krs_summary()}\n\n"
                        f"❓ Yakin ingin men-submit KRS ini? Ketik *Ya* atau *Tidak*."
                    )

            elif intent in ("ADD_COURSE", "UNKNOWN"):
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    if intent == "UNKNOWN":
                        self.response  = self.nlp.get_course_info_text(course_key)
                        nama           = course_key.replace("_", " ").title()
                        self.response += f"\n\n💡 Ketik *'ambil {nama}'* untuk menambahkan ke KRS."
                    else:
                        success, msg   = self.add_course(course_key)
                        self.response  = msg
                        if success and self.session_count % 3 == 0:
                            self.response += f"\n\n{random.choice(ACADEMIC_FACTS)}"
                else:
                    self.response = (
                        "❓ Saya tidak mengerti perintah itu. Coba:\n"
                        "• *'menu'* — lihat daftar matkul\n"
                        "• *'rekomen'* — rekomendasi matkul\n"
                        "• *'bantuan'* — panduan lengkap"
                    )

            else:
                self.response = (
                    "❓ Perintah tidak dikenali.\n"
                    "Ketik *'bantuan'* untuk panduan, atau *'menu'* untuk lihat matkul."
                )

        # ── STATE: CONFIRMATION ───────────────────────────────────────────────
        elif self.state == State.CONFIRMATION:
            if intent == "YES":
                self.state        = State.SUBMITTED
                self.submitted_krs = list(self.cart)
                self.push_notification("📤 KRS berhasil disubmit!")
                self.response = (
                    f"🎉 *KRS Berhasil Disubmit!*\n\n"
                    f"{self.get_krs_summary()}\n\n"
                    f"📨 Konfirmasi dikirim ke email mahasiswa Anda.\n"
                    f"Verifikasi akademik dalam 1×24 jam.\n\n"
                    f"{random.choice(ACADEMIC_FACTS)}\n\n"
                    f"Ketik *'reset'* untuk memulai sesi baru."
                )
                self.cart = []
            elif intent == "NO":
                self.state    = State.BROWSING
                self.response = "↩️ Dibatalkan. Silakan ubah pilihan matkul Anda."
            else:
                self.response = "Ketik *'Ya'* untuk konfirmasi submit, atau *'Tidak'* untuk kembali."

        # ── STATE: SUBMITTED ──────────────────────────────────────────────────
        elif self.state == State.SUBMITTED:
            self.response = (
                "✅ KRS sudah disubmit!\n"
                f"{random.choice(ACADEMIC_FACTS)}\n\n"
                "Ketik *'reset'* untuk memulai sesi baru."
            )