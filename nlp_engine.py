import re


class AcademicNLPEngine:
    def __init__(self):
        # ── Database Mata Kuliah (dari jadwal nyata UPGRIS, maks semester 4) ──
        self.course_data = {
            # ── SEMESTER 1 / 2 ──
            "kalkulus_integral": {
                "kode": "MAT102",
                "sks": 2,
                "semester": 2,
                "jadwal": "Jumat 18:30",
                "dosen": "Rizky Esti Utami",
                "ruang": "GP 607",
                "prasyarat": None,
                "emoji": "📐",
                "desc": "Diferensial, integral, dan limit fungsi untuk mahasiswa teknik informatika.",
                "kategori": "Wajib",
                "tips": "Perbanyak latihan soal integral substitusi dan parsial. Gunakan WolframAlpha untuk cek jawaban.",
                "difficulty": 3,
            },
            "sistem_operasi": {
                "kode": "IF202",
                "sks": 2,
                "semester": 2,
                "jadwal": "Rabu 20:10",
                "dosen": "Ramadhan Renaldy",
                "ruang": "GU 301",
                "prasyarat": None,
                "emoji": "🖥️",
                "desc": "Konsep dasar OS, manajemen proses, memori virtual, dan sistem file.",
                "kategori": "Wajib",
                "tips": "Install Linux di VM (VirtualBox/WSL) dan praktikkan command dasar. Sangat membantu pemahaman.",
                "difficulty": 2,
            },
            "struktur_data": {
                "kode": "IF203",
                "sks": 3,
                "semester": 2,
                "jadwal": "Selasa 18:30",
                "dosen": "Ramadhan Renaldy",
                "ruang": "GU 301",
                "prasyarat": None,
                "emoji": "🌲",
                "desc": "Array, linked list, stack, queue, tree, dan graph beserta implementasinya.",
                "kategori": "Wajib",
                "tips": "Visualisasikan struktur data dengan gambar. Situs VisuAlgo.net sangat membantu pemahaman.",
                "difficulty": 3,
            },
            "pemrograman_komputer": {
                "kode": "IF204",
                "sks": 3,
                "semester": 2,
                "jadwal": "Kamis 19:20",
                "dosen": "Nugroho D. S.",
                "ruang": "GU 401",
                "prasyarat": None,
                "emoji": "💻",
                "desc": "Dasar pemrograman prosedural, OOP, dan pemecahan masalah dengan kode.",
                "kategori": "Wajib",
                "tips": "Coding setiap hari minimal 30 menit. Kerjakan latihan di HackerRank atau CodeForces.",
                "difficulty": 2,
            },
            # ── SEMESTER 3 / 4 ──
            "matematika_diskrit": {
                "kode": "MAT301",
                "sks": 3,
                "semester": 4,
                "jadwal": "Rabu 10:00",
                "dosen": "Agung Handayanto",
                "ruang": "GP 607",
                "prasyarat": None,
                "emoji": "🔢",
                "desc": "Logika proposisi, teori himpunan, kombinatorik, dan teori graf.",
                "kategori": "Wajib",
                "tips": "Hafalkan identitas logika dan latihan pembuktian. Soal UAS banyak dari kombinatorik.",
                "difficulty": 3,
            },
            "analisis_perancangan_sistem": {
                "kode": "IF401",
                "sks": 3,
                "semester": 4,
                "jadwal": "Selasa 07:30",
                "dosen": "Bambang Agus Herlambang",
                "ruang": "GP 401",
                "prasyarat": "pemrograman_komputer",
                "emoji": "📊",
                "desc": "DFD, ERD, use case, sequence diagram, dan perancangan sistem informasi.",
                "kategori": "Wajib",
                "tips": "Kuasai tools seperti StarUML atau draw.io. Projek kelompok sangat menentukan nilai akhir.",
                "difficulty": 2,
            },
            "pemrograman_web": {
                "kode": "IF402",
                "sks": 3,
                "semester": 4,
                "jadwal": "Kamis 10:00",
                "dosen": "Aris Tri Joko Harjanto",
                "ruang": "GU 401",
                "prasyarat": "pemrograman_komputer",
                "emoji": "🌐",
                "desc": "HTML, CSS, JavaScript, PHP, dan framework web modern untuk pengembangan aplikasi.",
                "kategori": "Wajib",
                "tips": "Buat portfolio project nyata. Deploy ke GitHub Pages atau Vercel agar bisa ditunjukkan ke HRD.",
                "difficulty": 2,
            },
            "metode_numerik": {
                "kode": "MAT302",
                "sks": 2,
                "semester": 4,
                "jadwal": "Rabu 13:00",
                "dosen": "Agung Handayanto",
                "ruang": "GP 607",
                "prasyarat": "kalkulus_integral",
                "emoji": "🧮",
                "desc": "Solusi numerik persamaan nonlinier, interpolasi, integrasi numerik, dan ODEs.",
                "kategori": "Wajib",
                "tips": "Implementasikan metode dalam Python/MATLAB untuk pemahaman lebih dalam.",
                "difficulty": 4,
            },
            "decission_support_system": {
                "kode": "IF403",
                "sks": 3,
                "semester": 4,
                "jadwal": "Senin 13:00",
                "dosen": "Setyoningsih Wibowo",
                "ruang": "GP 608",
                "prasyarat": "struktur_data",
                "emoji": "🎯",
                "desc": "Model DSS, AHP, TOPSIS, SAW, dan penerapan sistem pendukung keputusan.",
                "kategori": "Pilihan",
                "tips": "Pahami metode pembobotan AHP dan TOPSIS. Banyak dipakai di skripsi mahasiswa TI.",
                "difficulty": 3,
            },
            "teknologi_animasi": {
                "kode": "IF404",
                "sks": 3,
                "semester": 4,
                "jadwal": "Jumat 13:00",
                "dosen": "Febrian Murti Dewanto",
                "ruang": "GU 401",
                "prasyarat": None,
                "emoji": "🎨",
                "desc": "Animasi 2D/3D, motion graphic, dan pengembangan konten multimedia interaktif.",
                "kategori": "Pilihan",
                "tips": "Pelajari Blender (gratis) untuk 3D. Keluruhan karya animasi sangat dinilai di matkul ini.",
                "difficulty": 2,
            },
            "internet_of_things": {
                "kode": "IF405",
                "sks": 3,
                "semester": 4,
                "jadwal": "Senin 08:20",
                "dosen": "Noora Qotrun Nada",
                "ruang": "GP 609",
                "prasyarat": "sistem_operasi",
                "emoji": "📡",
                "desc": "Sensor, mikrokontroler Arduino/ESP32, protokol MQTT, dan cloud IoT platform.",
                "kategori": "Pilihan",
                "tips": "Gunakan simulator Tinkercad sebelum beli hardware. Proyek IoT sederhana sangat diapresiasi.",
                "difficulty": 3,
            },
        }

        self.MAX_SKS = 24

        # ── Alias nama mata kuliah ──
        self.aliases = {
            "kalkulus_integral": ["kalkulus", "kalkulus integral", "mat102", "integral", "calculus"],
            "sistem_operasi": ["sistem operasi", "so", "os", "if202", "operating system"],
            "struktur_data": ["struktur data", "sd", "if203", "strukdat", "data structure"],
            "pemrograman_komputer": ["pemrograman", "pemrograman komputer", "if204", "coding", "prog"],
            "matematika_diskrit": ["matematika diskrit", "matdis", "diskrit", "mat301", "discrete math"],
            "analisis_perancangan_sistem": ["analisis perancangan sistem", "aps", "if401", "analisis sistem", "apsi"],
            "pemrograman_web": ["pemrograman web", "web", "if402", "web programming", "webprog"],
            "metode_numerik": ["metode numerik", "mn", "mat302", "numerik", "numerical method"],
            "decission_support_system": ["decission support system", "dss", "if403", "sistem pendukung keputusan", "spk"],
            "teknologi_animasi": ["teknologi animasi", "animasi", "if404", "animation"],
            "internet_of_things": ["internet of things", "iot", "if405", "arduino", "esp32"],
        }

        # ── Regex intent patterns ──
        self.intent_patterns = {
            "ASK_MENU":      r"\b(menu|daftar|list|kuliah apa|matkul|semua|tersedia|ada apa|katalog|lihat)\b",
            "CHECKOUT":      r"\b(selesai|submit|konfirmasi|krs|kirim|simpan|lanjut|finalisasi)\b",
            "CANCEL_ALL":    r"\b(batalkan semua|hapus semua|kosongkan|reset krs|bersihkan|clear)\b",
            "REMOVE_ITEM":   r"\b(batalkan|hapus|kurangi|drop|tidak jadi|cancel|buang|keluarkan)\b",
            "ASK_SCHEDULE":  r"\b(jadwal|schedule|kapan|jam|hari|waktu|ruang|kelas|tempat)\b",
            "ASK_PREREQ":    r"\b(prasyarat|syarat|prerequisite|wajib lulus|butuh|perlu dulu)\b",
            "ASK_SKS":       r"\b(sks|kredit|bobot|berapa sks|total sks|kapasitas)\b",
            "ASK_LECTURER":  r"\b(dosen|pengajar|pengampu|siapa yang mengajar|instruktur|bu|pak)\b",
            "ASK_TIPS":      r"\b(tips|saran|cara belajar|strategi|kiat|trik|lulus|nilai bagus)\b",
            "ASK_DIFFICULTY":r"\b(susah|sulit|mudah|difficulty|tingkat|level|gampang|berat)\b",
            "ASK_WAJIB":     r"\b(wajib|harus|pilihan|opsional|elective|kategori)\b",
            "RESET_SYSTEM":  r"\b(reset|ulang sistem|mulai ulang|restart)\b",
            "YES":           r"\b(ya|yes|iya|oke|ok|betul|benar|siap|baik|lanjut|setuju|konfirmasi)\b",
            "NO":            r"\b(tidak|enggak|nggak|batal|no|salah|cancel|tidak jadi|mundur)\b",
            "ADD_COURSE":    r"\b(ambil|daftar|tambah|ikut|ikuti|pilih|masukkan|register|mau|ambilkan)\b",
            "GREETING":      r"\b(halo|hi|hello|selamat|pagi|siang|sore|malam|hai|hei)\b",
            "HELP":          r"\b(help|bantuan|tolong|bisa apa|apa saja|fitur|panduan|cara)\b",
            "ASK_REKOMENDASI": r"\b(rekomendasi|saran matkul|rekomen|sarankan|sebaiknya|mana yang|pilihkan)\b",
            "ASK_SUMMARY":   r"\b(ringkasan|summary|review krs|cek krs|lihat krs|krs saya)\b",
        }

    def resolve_course_name(self, text):
        text = text.lower()
        for key, alias_list in self.aliases.items():
            for alias in alias_list:
                if alias in text:
                    return key
        return None

    def parse_courses(self, text):
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
        text = text.lower()
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, text):
                return intent
        return "UNKNOWN"

    def get_course_info_text(self, course_key):
        c = self.course_data[course_key]
        prasyarat_text = c["prasyarat"].replace("_", " ").title() if c["prasyarat"] else "Tidak ada"
        stars = "⭐" * c["difficulty"] + "☆" * (5 - c["difficulty"])
        return (
            f"{c['emoji']} *{course_key.replace('_', ' ').title()}* ({c['kode']})\n"
            f"SKS: {c['sks']} | Semester: {c['semester']} | Tingkat Kesulitan: {stars}\n"
            f"Jadwal: {c['jadwal']} | Ruang: {c['ruang']}\n"
            f"Dosen: {c['dosen']}\n"
            f"Prasyarat: {prasyarat_text}\n"
            f"Kategori: {c['kategori']}\n"
            f"Deskripsi: {c['desc']}\n"
            f"💡 Tips: _{c['tips']}_"
        )

    def get_recommendations(self, cart):
        """Rekomendasi matkul berdasarkan KRS saat ini."""
        in_cart = {c["course_key"] for c in cart}
        recs = []
        for key, data in self.course_data.items():
            if key in in_cart:
                continue
            if data["prasyarat"] and data["prasyarat"] not in in_cart:
                continue
            recs.append((key, data))
        recs.sort(key=lambda x: (x[1]["semester"], x[1]["difficulty"]))
        return recs[:3]