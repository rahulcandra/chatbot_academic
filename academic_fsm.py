from enum import Enum, auto
from nlp_engine import AcademicNLPEngine


class State(Enum):
    IDLE = auto()
    BROWSING = auto()       # Melihat & menambah mata kuliah
    CONFIRMATION = auto()   # Konfirmasi KRS sebelum submit
    SUBMITTED = auto()      # KRS sudah disubmit


class AcademicFSM:
    def __init__(self):
        self.state = State.IDLE
        self.nlp = AcademicNLPEngine()
        self.cart = []          # Mata kuliah yang dipilih
        self.response = ""
        self.submitted_krs = None

    def get_response(self):
        return self.response

    def total_sks(self):
        return sum(c["sks"] for c in self.cart)

    def get_catalog_text(self):
        lines = ["📚 *Katalog Mata Kuliah yang Tersedia:*\n"]
        for key, data in self.nlp.course_data.items():
            nama = key.replace("_", " ").title()
            lines.append(
                f"{data['emoji']} *{nama}* ({data['kode']}) "
                f"— {data['sks']} SKS | {data['kategori']}\n"
                f"   _{data['desc']}_\n"
                f"   🕐 {data['jadwal']}\n"
            )
        lines.append(
            "\n💡 Ketik nama mata kuliah untuk info detail, "
            "atau *'ambil [nama matkul]'* untuk mendaftarkan."
        )
        return "\n".join(lines)

    def get_schedule_text(self):
        if not self.cart:
            return "📅 Belum ada mata kuliah di KRS Anda."
        lines = ["📅 *Jadwal Kuliah Anda:*\n"]
        for c in self.cart:
            nama = c["course_key"].replace("_", " ").title()
            lines.append(
                f"{c['emoji']} *{nama}* — {c['jadwal']}\n"
                f"   📍 {c['ruang']} | 👨‍🏫 {c['dosen']}"
            )
        return "\n".join(lines)

    def check_conflict(self, new_course_key):
        """Cek konflik jadwal dengan matkul yang sudah ada di keranjang."""
        new = self.nlp.course_data[new_course_key]
        for c in self.cart:
            existing = self.nlp.course_data[c["course_key"]]
            if existing["jadwal"] == new["jadwal"]:
                return c["course_key"]
        return None

    def add_course(self, course_key):
        """Tambah mata kuliah ke KRS. Return (success, message)."""
        data = self.nlp.course_data[course_key]
        nama = course_key.replace("_", " ").title()

        # Sudah ada?
        if any(c["course_key"] == course_key for c in self.cart):
            return False, f"⚠️ *{nama}* sudah ada di KRS Anda."

        # Cek batas SKS
        if self.total_sks() + data["sks"] > self.nlp.MAX_SKS:
            sisa = self.nlp.MAX_SKS - self.total_sks()
            return False, (
                f"❌ Tidak bisa menambahkan *{nama}* ({data['sks']} SKS).\n"
                f"Sisa kapasitas SKS: {sisa} SKS dari maksimum {self.nlp.MAX_SKS} SKS."
            )

        # Cek prasyarat
        if data["prasyarat"]:
            prasyarat_key = data["prasyarat"]
            in_cart = any(c["course_key"] == prasyarat_key for c in self.cart)
            prasyarat_nama = prasyarat_key.replace("_", " ").title()
            if not in_cart:
                return False, (
                    f"❌ *{nama}* memerlukan prasyarat: *{prasyarat_nama}*.\n"
                    f"Silakan tambahkan *{prasyarat_nama}* terlebih dahulu."
                )

        # Cek konflik jadwal
        conflict = self.check_conflict(course_key)
        if conflict:
            conflict_nama = conflict.replace("_", " ").title()
            return False, (
                f"❌ Jadwal *{nama}* bentrok dengan *{conflict_nama}*!\n"
                f"Keduanya di jadwal: {data['jadwal']}."
            )

        # Tambahkan
        self.cart.append({
            "course_key": course_key,
            "kode": data["kode"],
            "sks": data["sks"],
            "jadwal": data["jadwal"],
            "ruang": data["ruang"],
            "dosen": data["dosen"],
            "emoji": data["emoji"],
        })
        return True, (
            f"✅ *{nama}* ({data['sks']} SKS) berhasil ditambahkan!\n"
            f"Total SKS: {self.total_sks()}/{self.nlp.MAX_SKS}"
        )

    def remove_course(self, course_key):
        """Hapus mata kuliah dari KRS."""
        nama = course_key.replace("_", " ").title()
        before = len(self.cart)
        self.cart = [c for c in self.cart if c["course_key"] != course_key]
        if len(self.cart) < before:
            return f"🗑️ *{nama}* berhasil dihapus dari KRS."
        return f"⚠️ *{nama}* tidak ditemukan di KRS Anda."

    def get_krs_summary(self):
        if not self.cart:
            return "📋 KRS Anda masih kosong."
        lines = ["📋 *Ringkasan KRS Anda:*\n"]
        for c in self.cart:
            nama = c["course_key"].replace("_", " ").title()
            lines.append(f"{c['emoji']} {nama} ({c['kode']}) — {c['sks']} SKS")
        lines.append(f"\n📊 *Total SKS: {self.total_sks()} dari {self.nlp.MAX_SKS} SKS*")
        return "\n".join(lines)

    def step(self, user_input=""):
        user_input = user_input.strip()

        # Pertama kali (IDLE tanpa input)
        if user_input == "" and self.state == State.IDLE:
            self.state = State.BROWSING
            self.response = (
                "*Selamat datang di Sistem KRS Akademik! 👋*\n\n"
                "Saya akan membantu Anda menyusun Kartu Rencana Studi.\n\n"
                "Yang bisa saya bantu:\n"
                "• Lihat daftar mata kuliah → ketik *'menu'*\n"
                "• Tambah matkul → ketik *'ambil [nama matkul]'*\n"
                "• Cek jadwal → ketik *'jadwal'*\n"
                "• Info prasyarat → ketik *'prasyarat [nama matkul]'*\n"
                "• Submit KRS → ketik *'submit KRS'*\n\n"
                "Ketik *'bantuan'* untuk panduan lengkap."
            )
            return

        intent = self.nlp.detect_intent(user_input)

        # RESET SISTEM
        if intent == "RESET_SYSTEM":
            self.__init__()
            self.state = State.BROWSING
            self.response = "🔄 Sistem direset. Selamat datang kembali! Ketik *'menu'* untuk mulai."
            return

        # GREETING
        if intent == "GREETING":
            self.response = (
                "👋 Halo! Saya asisten KRS Anda.\n"
                "Ketik *'menu'* untuk melihat daftar mata kuliah, "
                "atau *'bantuan'* untuk panduan."
            )
            return

        # HELP
        if intent == "HELP":
            self.response = (
                "📖 *Panduan Penggunaan Chatbot KRS:*\n\n"
                "🔍 *Melihat Informasi:*\n"
                "• `menu` — Lihat semua mata kuliah\n"
                "• `jadwal` — Lihat jadwal yang sudah dipilih\n"
                "• `prasyarat algoritma` — Cek syarat suatu matkul\n"
                "• `info kalkulus` — Detail lengkap satu matkul\n\n"
                "➕ *Mengelola KRS:*\n"
                "• `ambil algoritma` — Tambah ke KRS\n"
                "• `hapus kalkulus` — Hapus dari KRS\n"
                "• `hapus semua` — Kosongkan KRS\n\n"
                "📤 *Submit:*\n"
                "• `submit KRS` atau `selesai` — Konfirmasi & kirim\n\n"
                "🔁 *Lainnya:*\n"
                "• `reset` — Mulai ulang dari awal"
            )
            return

        # ========================
        # STATE: BROWSING
        # ========================
        if self.state == State.BROWSING:

            if intent == "ASK_MENU":
                self.response = self.get_catalog_text()

            elif intent == "ASK_SCHEDULE":
                self.response = self.get_schedule_text()

            elif intent == "ASK_SKS":
                self.response = (
                    f"📊 Total SKS yang diambil: *{self.total_sks()} SKS*\n"
                    f"Kapasitas maksimum: *{self.nlp.MAX_SKS} SKS*\n"
                    f"Sisa kapasitas: *{self.nlp.MAX_SKS - self.total_sks()} SKS*"
                )

            elif intent == "ASK_PREREQ":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    data = self.nlp.course_data[course_key]
                    nama = course_key.replace("_", " ").title()
                    if data["prasyarat"]:
                        pr_nama = data["prasyarat"].replace("_", " ").title()
                        self.response = f"📋 Prasyarat *{nama}*: harus lulus *{pr_nama}* terlebih dahulu."
                    else:
                        self.response = f"✅ *{nama}* tidak memiliki prasyarat. Dapat langsung diambil!"
                else:
                    self.response = "Mata kuliah apa yang ingin dicek prasyaratnya?\nContoh: *'prasyarat basis data'*"

            elif intent == "ASK_LECTURER":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    data = self.nlp.course_data[course_key]
                    nama = course_key.replace("_", " ").title()
                    self.response = f"👨‍🏫 Dosen pengampu *{nama}*: *{data['dosen']}*"
                else:
                    self.response = "Mata kuliah apa yang ingin dicek dosennya?\nContoh: *'dosen algoritma'*"

            elif intent == "CANCEL_ALL":
                self.cart = []
                self.response = "🗑️ Semua mata kuliah berhasil dihapus dari KRS."

            elif intent == "REMOVE_ITEM":
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    self.response = self.remove_course(course_key)
                else:
                    self.response = "Mata kuliah apa yang ingin dihapus?\nContoh: *'hapus kalkulus'*"

            elif intent == "CHECKOUT":
                if not self.cart:
                    self.response = "🛒 KRS Anda masih kosong. Silakan tambahkan mata kuliah terlebih dahulu."
                else:
                    self.state = State.CONFIRMATION
                    self.response = (
                        f"{self.get_krs_summary()}\n\n"
                        f"❓ Yakin ingin men-submit KRS ini? Ketik *Ya* atau *Tidak*."
                    )

            elif intent in ("ADD_COURSE", "UNKNOWN"):
                # Coba deteksi nama matkul langsung
                course_key = self.nlp.resolve_course_name(user_input)
                if course_key:
                    # Jika hanya info (tidak ada kata kerja ambil)
                    if intent == "UNKNOWN":
                        self.response = self.nlp.get_course_info_text(course_key)
                        nama = course_key.replace("_", " ").title()
                        self.response += f"\n\n💡 Ketik *'ambil {nama}'* untuk menambahkan ke KRS."
                    else:
                        # Tambahkan ke KRS
                        success, msg = self.add_course(course_key)
                        self.response = msg
                else:
                    self.response = (
                        "❓ Saya tidak mengerti. Coba:\n"
                        "• *'menu'* — lihat daftar matkul\n"
                        "• *'ambil algoritma'* — tambah ke KRS\n"
                        "• *'bantuan'* — panduan lengkap"
                    )

            else:
                self.response = (
                    "❓ Saya tidak mengerti perintah itu.\n"
                    "Ketik *'bantuan'* untuk panduan."
                )

        # ========================
        # STATE: CONFIRMATION
        # ========================
        elif self.state == State.CONFIRMATION:
            if intent == "YES":
                self.state = State.SUBMITTED
                self.submitted_krs = list(self.cart)
                self.response = (
                    f"🎉 *KRS Berhasil Disubmit!*\n\n"
                    f"{self.get_krs_summary()}\n\n"
                    f"📨 Konfirmasi telah dikirim ke email mahasiswa Anda.\n"
                    f"Silakan tunggu verifikasi dari akademik dalam 1×24 jam.\n\n"
                    f"Ketik *'reset'* untuk memulai sesi baru."
                )
                self.cart = []
            elif intent == "NO":
                self.state = State.BROWSING
                self.response = "↩️ Dibatalkan. Silakan ubah pilihan mata kuliah Anda."
            else:
                self.response = "Ketik *'Ya'* untuk konfirmasi submit, atau *'Tidak'* untuk kembali edit."

        # ========================
        # STATE: SUBMITTED
        # ========================
        elif self.state == State.SUBMITTED:
            self.response = (
                "✅ KRS Anda sudah disubmit!\n"
                "Ketik *'reset'* jika ingin memulai sesi baru."
            )