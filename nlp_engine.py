import re


class AcademicNLPEngine:
    def __init__(self):
        # Database Mata Kuliah
        self.course_data = {
            "kalkulus": {
                "kode": "MAT101",
                "sks": 3,
                "semester": 1,
                "jadwal": "Senin 08.00–10.30",
                "dosen": "Dr. Rina Wijaya",
                "ruang": "GK-201",
                "prasyarat": None,
                "emoji": "📐",
                "desc": "Diferensial, integral, dan limit fungsi.",
                "kategori": "Wajib",
            },
            "fisika_dasar": {
                "kode": "FIS101",
                "sks": 3,
                "semester": 1,
                "jadwal": "Selasa 10.00–12.30",
                "dosen": "Dr. Budi Santoso",
                "ruang": "GK-102",
                "prasyarat": None,
                "emoji": "⚛️",
                "desc": "Mekanika, termodinamika, dan gelombang.",
                "kategori": "Wajib",
            },
            "algoritma": {
                "kode": "IF201",
                "sks": 4,
                "semester": 2,
                "jadwal": "Rabu 13.00–16.20",
                "dosen": "Ir. Candra Putra, M.T.",
                "ruang": "Lab Komputer A",
                "prasyarat": None,
                "emoji": "💻",
                "desc": "Struktur data, kompleksitas, dan pemrograman.",
                "kategori": "Wajib",
            },
            "basis_data": {
                "kode": "IF301",
                "sks": 3,
                "semester": 3,
                "jadwal": "Kamis 08.00–10.30",
                "dosen": "Dr. Dewi Lestari",
                "ruang": "Lab Komputer B",
                "prasyarat": "algoritma",
                "emoji": "🗄️",
                "desc": "ERD, SQL, normalisasi, dan manajemen database.",
                "kategori": "Wajib",
            },
            "kecerdasan_buatan": {
                "kode": "IF401",
                "sks": 3,
                "semester": 5,
                "jadwal": "Jumat 09.00–11.30",
                "dosen": "Prof. Eko Prasetyo",
                "ruang": "GK-305",
                "prasyarat": "algoritma",
                "emoji": "🤖",
                "desc": "Machine learning, neural network, dan NLP.",
                "kategori": "Pilihan",
            },
            "statistika": {
                "kode": "MAT201",
                "sks": 2,
                "semester": 2,
                "jadwal": "Senin 13.00–14.40",
                "dosen": "Dr. Fitri Hapsari",
                "ruang": "GK-203",
                "prasyarat": "kalkulus",
                "emoji": "📊",
                "desc": "Probabilitas, distribusi, dan inferensi statistik.",
                "kategori": "Wajib",
            },
            "jaringan_komputer": {
                "kode": "IF302",
                "sks": 3,
                "semester": 4,
                "jadwal": "Selasa 13.00–15.30",
                "dosen": "Ir. Hendra Kusuma, M.T.",
                "ruang": "Lab Jaringan",
                "prasyarat": "algoritma",
                "emoji": "🌐",
                "desc": "TCP/IP, routing, dan keamanan jaringan.",
                "kategori": "Wajib",
            },
            "bahasa_inggris": {
                "kode": "UNI101",
                "sks": 2,
                "semester": 1,
                "jadwal": "Rabu 08.00–09.40",
                "dosen": "Drs. Agus Ridwan",
                "ruang": "GK-105",
                "prasyarat": None,
                "emoji": "🗣️",
                "desc": "Academic English untuk mahasiswa teknik.",
                "kategori": "Wajib",
            },
        }

        self.MAX_SKS = 24

        # Alias nama mata kuliah
        self.aliases = {
            "kalkulus": ["kalkulus", "calculus", "mat101"],
            "fisika_dasar": ["fisika", "fisika dasar", "fis101", "physics"],
            "algoritma": ["algoritma", "algo", "if201", "pemrograman", "koding"],
            "basis_data": ["basis data", "database", "bd", "if301", "dbms"],
            "kecerdasan_buatan": ["kecerdasan buatan", "ai", "kb", "if401", "machine learning", "ml"],
            "statistika": ["statistika", "statistik", "stat", "mat201"],
            "jaringan_komputer": ["jaringan", "jaringan komputer", "jarkom", "if302", "networking"],
            "bahasa_inggris": ["bahasa inggris", "english", "inggris", "uni101"],
        }

        # Regex intent
        self.intent_patterns = {
            "ASK_MENU": r"\b(menu|daftar|list|kuliah apa|matkul|semua|tersedia|ada apa)\b",
            "CHECKOUT": r"\b(selesai|bayar|submit|konfirmasi|krs|kirim|simpan|daftar|lanjut)\b",
            "CANCEL_ALL": r"\b(batalkan semua|hapus semua|kosongkan|reset krs|bersihkan)\b",
            "REMOVE_ITEM": r"\b(batalkan|hapus|kurangi|drop|tidak jadi|cancel|buang)\b",
            "ASK_SCHEDULE": r"\b(jadwal|schedule|kapan|jam|hari|waktu|ruang|kelas)\b",
            "ASK_PREREQ": r"\b(prasyarat|syarat|prerequisite|wajib lulus|sudah ambil)\b",
            "ASK_SKS": r"\b(sks|kredit|bobot|berapa sks|total)\b",
            "ASK_LECTURER": r"\b(dosen|pengajar|pengampu|siapa yang mengajar|instruktur)\b",
            "RESET_SYSTEM": r"\b(reset|ulang sistem|mulai ulang|restart)\b",
            "YES": r"\b(ya|yes|iya|oke|ok|betul|benar|siap|baik|lanjut|setuju)\b",
            "NO": r"\b(tidak|enggak|nggak|batal|no|salah|cancel|tidak jadi)\b",
            "ADD_COURSE": r"\b(ambil|daftar|tambah|ikut|ikuti|pilih|masukkan|register|mau)\b",
            "GREETING": r"\b(halo|hi|hello|selamat|pagi|siang|sore|malam|hai)\b",
            "HELP": r"\b(help|bantuan|tolong|bisa apa|apa saja|fitur|panduan)\b",
        }

    def resolve_course_name(self, text):
        """Cari nama kunci mata kuliah dari teks."""
        text = text.lower()
        for key, alias_list in self.aliases.items():
            for alias in alias_list:
                if alias in text:
                    return key
        return None

    def parse_courses(self, text):
        """Ekstrak mata kuliah dari teks input."""
        text = text.lower()
        found = []
        for key, alias_list in self.aliases.items():
            for alias in alias_list:
                if alias in text:
                    if key not in [f["course_key"] for f in found]:
                        found.append({"course_key": key, "qty": 1})
                    break
        return found

    def detect_intent(self, text):
        """Deteksi intent utama dari input user."""
        text = text.lower()
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, text):
                return intent
        return "UNKNOWN"

    def get_course_info_text(self, course_key):
        """Teks detail satu mata kuliah."""
        c = self.course_data[course_key]
        prasyarat_text = c["prasyarat"].replace("_", " ").title() if c["prasyarat"] else "Tidak ada"
        return (
            f"{c['emoji']} *{course_key.replace('_', ' ').title()}* ({c['kode']})\n"
            f"SKS: {c['sks']} | Semester: {c['semester']}\n"
            f"Jadwal: {c['jadwal']} | Ruang: {c['ruang']}\n"
            f"Dosen: {c['dosen']}\n"
            f"Prasyarat: {prasyarat_text}\n"
            f"Kategori: {c['kategori']}\n"
            f"Deskripsi: {c['desc']}"
        )