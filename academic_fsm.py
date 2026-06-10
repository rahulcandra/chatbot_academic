import re
import random
from enum import Enum, auto

ACADEMIC_FACTS = [
    "Teknik Pomodoro: 25 menit belajar, 5 menit istirahat — terbukti meningkatkan fokus hingga 40%.",
    "Spaced Repetition: Mengulang materi di interval tertentu jauh lebih efektif daripada belajar sekaligus.",
    "Menulis catatan tangan meningkatkan retensi memori lebih baik dibanding mengetik.",
    "Belajar kelompok efektif untuk matkul berbasis konsep; belajar mandiri lebih baik untuk coding.",
    "Tidur cukup 7-8 jam setelah belajar membantu konsolidasi memori jangka panjang.",
    "Mulai dengan matkul tersulit di pagi hari saat energi dan fokus masih optimal.",
    "Mode fokus (matikan notif) terbukti meningkatkan produktivitas belajar hingga 23%.",
    "Mengajarkan materi ke orang lain (Feynman Technique) adalah cara paling efektif memahami konsep.",
]

class State(Enum):
    GREETING   = auto()
    BROWSING   = auto()
    CONFIRM    = auto()
    DONE       = auto()

class NLPEngine:
    MAX_SKS = 24

    course_data = {
        # ── SEMESTER 1 ──
        "pendidikan_agama": {
            "sks": 2, "semester": 1,
            "emoji": "🕌", "kategori": "Wajib",
            "desc": "Nilai-nilai keagamaan, akhlak mulia, dan pembentukan karakter mahasiswa.",
            "jadwal": "Senin 07:30", "ruang": "GP 601",
            "dosen": "TBD",
            "prereq": [], "difficulty": 1,
            "tips": "Aktif dalam diskusi kelas dan kaitkan nilai agama dengan etika profesi IT."
        },
        "pendidikan_kewarganegaraan": {
            "sks": 2, "semester": 1,
            "emoji": "🇮🇩", "kategori": "Wajib",
            "desc": "Wawasan kebangsaan, demokrasi, hak asasi manusia, dan bela negara.",
            "jadwal": "Selasa 07:30", "ruang": "GP 601",
            "dosen": "TBD",
            "prereq": [], "difficulty": 1,
            "tips": "Kaitkan wawasan kebangsaan dengan isu digital dan keamanan siber nasional."
        },
        "matematika_dasar": {
            "sks": 3, "semester": 1,
            "emoji": "➕", "kategori": "Wajib",
            "desc": "Aljabar, fungsi, trigonometri, dan dasar-dasar matematika untuk teknik.",
            "jadwal": "Rabu 07:30", "ruang": "GP 607",
            "dosen": "Agung Handayanto",
            "prereq": [], "difficulty": 2,
            "tips": "Latihan soal setiap hari. Manfaatkan Khan Academy untuk materi yang belum paham."
        },
        "algoritma_pemrograman": {
            "sks": 3, "semester": 1,
            "emoji": "🔄", "kategori": "Wajib",
            "desc": "Logika algoritma, flowchart, pseudocode, dan pengantar pemrograman terstruktur.",
            "jadwal": "Kamis 07:30", "ruang": "GU 401",
            "dosen": "Nugroho D. S.",
            "prereq": [], "difficulty": 2,
            "tips": "Latih flowchart manual dulu sebelum coding. Gunakan draw.io untuk visualisasi algoritma."
        },
        "pengantar_teknologi_informasi": {
            "sks": 2, "semester": 1,
            "emoji": "💡", "kategori": "Wajib",
            "desc": "Pengenalan hardware, software, jaringan, dan perkembangan teknologi informasi.",
            "jadwal": "Jumat 07:30", "ruang": "GP 608",
            "dosen": "Noora Qotrun Nada",
            "prereq": [], "difficulty": 1,
            "tips": "Baca berita teknologi terkini di TechCrunch atau IDN Times Tech untuk konteks nyata."
        },
        "fisika_dasar": {
            "sks": 2, "semester": 1,
            "emoji": "⚛️", "kategori": "Wajib",
            "desc": "Mekanika, listrik, magnet, dan gelombang untuk dasar ilmu teknik.",
            "jadwal": "Senin 10:00", "ruang": "GP 607",
            "dosen": "TBD",
            "prereq": [], "difficulty": 2,
            "tips": "Hubungkan konsep fisika dengan elektronika dan IoT yang akan dipelajari di semester selanjutnya."
        },

        # ── SEMESTER 2 ──
        "kalkulus_integral": {
            "sks": 2, "semester": 2,
            "emoji": "📐", "kategori": "Wajib",
            "desc": "Diferensial, integral, dan limit fungsi untuk mahasiswa teknik informatika.",
            "jadwal": "Jumat 18:30", "ruang": "GP 607",
            "dosen": "Rizky Esti Utami",
            "prereq": [], "difficulty": 4,
            "tips": "Latihan soal minimal 10 soal per hari. Gunakan Wolfram Alpha untuk cek jawaban."
        },
        "sistem_operasi": {
            "sks": 2, "semester": 2,
            "emoji": "🖥️", "kategori": "Wajib",
            "desc": "Konsep OS, manajemen proses, memori, dan sistem file.",
            "jadwal": "Rabu 20:10", "ruang": "GU 301",
            "dosen": "Ramadhan Renaldy",
            "prereq": [], "difficulty": 3,
            "tips": "Praktikkan di Linux/VirtualBox. Baca 'Operating System Concepts' oleh Silberschatz."
        },
        "struktur_data": {
            "sks": 3, "semester": 2,
            "emoji": "🗂️", "kategori": "Wajib",
            "desc": "Array, linked list, stack, queue, tree, graph, dan algoritma sorting/searching.",
            "jadwal": "Selasa 18:30", "ruang": "GU 301",
            "dosen": "Ramadhan Renaldy",
            "prereq": [], "difficulty": 4,
            "tips": "Visualisasikan struktur data dengan VisuAlgo. Implementasikan sendiri dari nol."
        },
        "pemrograman_komputer": {
            "sks": 3, "semester": 2,
            "emoji": "💻", "kategori": "Wajib",
            "desc": "Dasar pemrograman prosedural, OOP, dan pemecahan masalah komputasi.",
            "jadwal": "Kamis 19:20", "ruang": "GU 401",
            "dosen": "Nugroho D. S.",
            "prereq": [], "difficulty": 3,
            "tips": "Kerjakan minimal 1 program latihan per hari. Manfaatkan LeetCode untuk latihan."
        },
        "berbicara": {
            "sks": 2, "semester": 2,
            "emoji": "🗣️", "kategori": "Wajib",
            "desc": "Keterampilan berbicara efektif dalam konteks akademik dan profesional.",
            "jadwal": "Senin 09:10", "ruang": "A.307",
            "dosen": "Sri Suciati",
            "prereq": [], "difficulty": 2,
            "tips": "Latih public speaking di depan cermin. Rekam diri sendiri untuk evaluasi."
        },
        "ke_pgri_an": {
            "sks": 2, "semester": 2,
            "emoji": "🏫", "kategori": "Wajib",
            "desc": "Wawasan sejarah, visi, misi, dan nilai-nilai Universitas PGRI Semarang.",
            "jadwal": "Jumat 20:10", "ruang": "GD 412",
            "dosen": "Hari Waluyo",
            "prereq": [], "difficulty": 1,
            "tips": "Pahami sejarah PGRI dan UPGRIS. Ikuti kegiatan kemahasiswaan untuk nilai plus."
        },
        "bahasa_indonesia": {
            "sks": 2, "semester": 2,
            "emoji": "🇮🇩", "kategori": "Wajib",
            "desc": "Kaidah bahasa Indonesia baku untuk keperluan akademik dan penulisan ilmiah.",
            "jadwal": "Kamis 07:30", "ruang": "GP 601",
            "dosen": "Siti Ulfiyani",
            "prereq": [], "difficulty": 2,
            "tips": "Baca KBBI dan EYD. Latih menulis esai ilmiah minimal 1 per minggu."
        },
        "bahasa_inggris": {
            "sks": 2, "semester": 2,
            "emoji": "🇬🇧", "kategori": "Wajib",
            "desc": "Bahasa Inggris untuk komunikasi teknik dan membaca literatur ilmiah.",
            "jadwal": "Kamis 16:20", "ruang": "B 504",
            "dosen": "Jafar Sodiq",
            "prereq": [], "difficulty": 2,
            "tips": "Biasakan membaca dokumentasi teknis dalam bahasa Inggris. Gunakan Duolingo harian."
        },

        # ── SEMESTER 3 ──
        "jaringan_komputer": {
            "sks": 3, "semester": 3,
            "emoji": "🌐", "kategori": "Wajib",
            "desc": "Arsitektur jaringan, protokol TCP/IP, routing, switching, dan keamanan jaringan dasar.",
            "jadwal": "Senin 10:00", "ruang": "GP 609",
            "dosen": "Noora Qotrun Nada",
            "prereq": ["sistem_operasi"], "difficulty": 3,
            "tips": "Praktikkan dengan Cisco Packet Tracer (gratis). Sertifikasi CCNA sangat berharga di industri."
        },
        "basis_data": {
            "sks": 3, "semester": 3,
            "emoji": "🗄️", "kategori": "Wajib",
            "desc": "Perancangan database, SQL, normalisasi, dan sistem manajemen basis data.",
            "jadwal": "Rabu 08:20", "ruang": "GU 301",
            "dosen": "Bambang Agus Herlambang",
            "prereq": ["struktur_data"], "difficulty": 3,
            "tips": "Kuasai SQL dengan SQLZoo atau Mode Analytics. Praktikkan normalisasi pada studi kasus nyata."
        },
        "pemrograman_berorientasi_objek": {
            "sks": 3, "semester": 3,
            "emoji": "🧩", "kategori": "Wajib",
            "desc": "Konsep OOP: class, inheritance, polymorphism, encapsulation, dan design patterns.",
            "jadwal": "Selasa 10:00", "ruang": "GU 401",
            "dosen": "Aris Tri Joko Harjanto",
            "prereq": ["pemrograman_komputer"], "difficulty": 3,
            "tips": "Buat minimal 3 proyek OOP. Pelajari design patterns dari refactoring.guru."
        },
        "logika_informatika": {
            "sks": 2, "semester": 3,
            "emoji": "🧮", "kategori": "Wajib",
            "desc": "Logika proposisi, predikat, inferensi, dan aplikasi logika dalam pemrograman.",
            "jadwal": "Kamis 08:20", "ruang": "GP 607",
            "dosen": "Agung Handayanto",
            "prereq": ["matematika_dasar"], "difficulty": 3,
            "tips": "Latihan soal pembuktian logika setiap hari. Gunakan tabel kebenaran untuk visualisasi."
        },
        "rekayasa_perangkat_lunak": {
            "sks": 3, "semester": 3,
            "emoji": "⚙️", "kategori": "Wajib",
            "desc": "SDLC, metodologi Agile/Scrum, dokumentasi perangkat lunak, dan quality assurance.",
            "jadwal": "Jumat 10:00", "ruang": "GP 608",
            "dosen": "Setyoningsih Wibowo",
            "prereq": ["pemrograman_komputer"], "difficulty": 3,
            "tips": "Pelajari Git flow dan manajemen proyek Agile. Buat proyek tim dengan GitHub Projects."
        },
        "statistika": {
            "sks": 2, "semester": 3,
            "emoji": "📊", "kategori": "Wajib",
            "desc": "Statistika deskriptif, probabilitas, distribusi, uji hipotesis, dan regresi.",
            "jadwal": "Senin 13:00", "ruang": "GP 607",
            "dosen": "Rizky Esti Utami",
            "prereq": ["matematika_dasar"], "difficulty": 3,
            "tips": "Gunakan R atau Python (pandas, scipy) untuk praktik statistika. Kaggle menyediakan dataset gratis."
        },

        # ── SEMESTER 4 ──
        "matematika_diskrit": {
            "sks": 3, "semester": 4,
            "emoji": "🔢", "kategori": "Wajib",
            "desc": "Logika, himpunan, relasi, fungsi, kombinatorik, graf, dan teori bilangan.",
            "jadwal": "Rabu 10:00", "ruang": "GP 607",
            "dosen": "Agung Handayanto",
            "prereq": ["kalkulus_integral"], "difficulty": 4,
            "tips": "Buat mind map untuk setiap topik. Latihan soal logika dan graf setiap hari."
        },
        "analisis_dan_perancangan_sistem": {
            "sks": 3, "semester": 4,
            "emoji": "📋", "kategori": "Wajib",
            "desc": "Metodologi pengembangan sistem, DFD, ERD, dan dokumentasi analisis kebutuhan.",
            "jadwal": "Selasa 07:30", "ruang": "GP 401",
            "dosen": "Bambang Agus Herlambang",
            "prereq": ["pemrograman_komputer"], "difficulty": 3,
            "tips": "Pelajari tools seperti draw.io dan Lucidchart. Buat studi kasus nyata."
        },
        "pemrograman_web": {
            "sks": 3, "semester": 4,
            "emoji": "🌐", "kategori": "Wajib",
            "desc": "HTML, CSS, JavaScript, PHP, dan framework web modern untuk pengembangan aplikasi.",
            "jadwal": "Kamis 10:00", "ruang": "GU 401",
            "dosen": "Aris Tri Joko Harjanto",
            "prereq": ["pemrograman_komputer"], "difficulty": 3,
            "tips": "Buat portofolio web pribadi. Ikuti tutorial di freeCodeCamp dan MDN Web Docs."
        },
        "metode_numerik": {
            "sks": 2, "semester": 4,
            "emoji": "🔬", "kategori": "Wajib",
            "desc": "Algoritma numerik untuk penyelesaian persamaan, interpolasi, dan integrasi numerik.",
            "jadwal": "Rabu 13:00", "ruang": "GP 607",
            "dosen": "Agung Handayanto",
            "prereq": ["kalkulus_integral"], "difficulty": 4,
            "tips": "Implementasikan algoritma dalam Python/MATLAB. Gunakan NumPy untuk verifikasi."
        },
        "decission_support_system": {
            "sks": 3, "semester": 4,
            "emoji": "🎯", "kategori": "Wajib",
            "desc": "Sistem pendukung keputusan, metode TOPSIS, AHP, SAW, dan fuzzy logic.",
            "jadwal": "Senin 13:00", "ruang": "GP 608",
            "dosen": "Setyoningsih Wibowo",
            "prereq": ["struktur_data"], "difficulty": 3,
            "tips": "Implementasikan metode DSS dalam studi kasus nyata. Buat perbandingan antar metode."
        },
        "teknologi_animasi": {
            "sks": 3, "semester": 4,
            "emoji": "🎬", "kategori": "Wajib",
            "desc": "Prinsip animasi, 2D/3D animation, motion graphics, dan tools animasi digital.",
            "jadwal": "Jumat 13:00", "ruang": "GU 401",
            "dosen": "Febrian Murti Dewanto",
            "prereq": [], "difficulty": 3,
            "tips": "Kuasai Adobe Animate atau Blender. Buat portofolio animasi pendek sebagai latihan."
        },
        "internet_of_things": {
            "sks": 3, "semester": 4,
            "emoji": "📡", "kategori": "Wajib",
            "desc": "Arsitektur IoT, sensor, aktuator, protokol komunikasi, dan platform IoT.",
            "jadwal": "Senin 08:20", "ruang": "GP 609",
            "dosen": "Noora Qotrun Nada",
            "prereq": ["pemrograman_komputer"], "difficulty": 4,
            "tips": "Praktikkan dengan Arduino/Raspberry Pi. Ikuti komunitas IoT Indonesia di Telegram."
        },
        "digital_marketing": {
            "sks": 2, "semester": 4,
            "emoji": "📢", "kategori": "Pilihan",
            "desc": "Strategi pemasaran digital, SEO, SEM, media sosial, dan analitik web.",
            "jadwal": "Kamis 09:10", "ruang": "A.303",
            "dosen": "Aryan Eka Prastya Nugraha",
            "prereq": [], "difficulty": 2,
            "tips": "Buat akun Google Analytics dan Google Search Console. Praktikkan kampanye kecil."
        },
        "studi_kelayakan_bisnis": {
            "sks": 2, "semester": 4,
            "emoji": "📋", "kategori": "Pilihan",
            "desc": "Analisis kelayakan bisnis dari aspek teknis, finansial, pasar, dan organisasi.",
            "jadwal": "Rabu 13:00", "ruang": "A.LAB EKONOMI",
            "dosen": "Dwi Prastiyo Hadi",
            "prereq": [], "difficulty": 2,
            "tips": "Pelajari template business plan. Analisis kasus startup lokal sebagai latihan."
        },
        "manajemen_sdm": {
            "sks": 2, "semester": 4,
            "emoji": "👥", "kategori": "Pilihan",
            "desc": "Perencanaan SDM, rekrutmen, pengembangan, kompensasi, dan hubungan industrial.",
            "jadwal": "Selasa 14:40", "ruang": "A.303",
            "dosen": "Dwi Prastiyo Hadi",
            "prereq": [], "difficulty": 2,
            "tips": "Hubungkan konsep MSDM dengan praktik di perusahaan teknologi seperti Google atau Tokopedia."
        },

        # ── SEMESTER 5 ──
        "kecerdasan_buatan": {
            "sks": 3, "semester": 5,
            "emoji": "🤖", "kategori": "Wajib",
            "desc": "Konsep AI, searching, knowledge representation, machine learning dasar, dan neural network.",
            "jadwal": "Senin 10:00", "ruang": "GU 401",
            "dosen": "Khoiriya Latifah",
            "prereq": ["matematika_diskrit"], "difficulty": 4,
            "tips": "Kuasai Python untuk AI. Ikuti kursus Andrew Ng di Coursera sebagai tambahan."
        },
        "pemrograman_mobile": {
            "sks": 3, "semester": 5,
            "emoji": "📱", "kategori": "Wajib",
            "desc": "Pengembangan aplikasi mobile Android/iOS menggunakan framework modern.",
            "jadwal": "Selasa 13:00", "ruang": "GU 401",
            "dosen": "Febrian Murti Dewanto",
            "prereq": ["pemrograman_berorientasi_objek"], "difficulty": 3,
            "tips": "Buat minimal 2 aplikasi mobile untuk portofolio. Publish ke Google Play Store."
        },
        "keamanan_sistem_informasi": {
            "sks": 3, "semester": 5,
            "emoji": "🔐", "kategori": "Wajib",
            "desc": "Kriptografi, keamanan jaringan, ethical hacking, dan manajemen risiko keamanan informasi.",
            "jadwal": "Rabu 10:00", "ruang": "GP 608",
            "dosen": "Saeful Fahmi",
            "prereq": ["jaringan_komputer"], "difficulty": 4,
            "tips": "Ikuti CTF (Capture The Flag) online. Platform TryHackMe dan HackTheBox sangat direkomendasikan."
        },
        "manajemen_proyek_ti": {
            "sks": 2, "semester": 5,
            "emoji": "📊", "kategori": "Wajib",
            "desc": "Perencanaan proyek, manajemen risiko, Agile, Scrum, dan tools manajemen proyek.",
            "jadwal": "Kamis 13:00", "ruang": "GP 608",
            "dosen": "Bambang Agus Herlambang",
            "prereq": ["rekayasa_perangkat_lunak"], "difficulty": 2,
            "tips": "Pelajari Jira, Trello, dan MS Project. Sertifikasi PMP/Scrum Master sangat dihargai industri."
        },
        "sistem_informasi_manajemen": {
            "sks": 3, "semester": 5,
            "emoji": "🏢", "kategori": "Wajib",
            "desc": "Sistem informasi untuk pengambilan keputusan manajemen, ERP, CRM, dan SCM.",
            "jadwal": "Jumat 10:00", "ruang": "GP 609",
            "dosen": "Setyoningsih Wibowo",
            "prereq": ["basis_data", "analisis_dan_perancangan_sistem"], "difficulty": 3,
            "tips": "Pelajari SAP Business One atau Odoo untuk simulasi ERP. Sangat relevan di dunia kerja."
        },
        "pengolahan_citra": {
            "sks": 3, "semester": 5,
            "emoji": "🖼️", "kategori": "Pilihan",
            "desc": "Teknik pengolahan citra digital, segmentasi, deteksi tepi, dan klasifikasi gambar.",
            "jadwal": "Senin 13:00", "ruang": "GU 301",
            "dosen": "Mega Novita",
            "prereq": ["matematika_diskrit"], "difficulty": 4,
            "tips": "Kuasai OpenCV dan PIL di Python. Ikuti kompetisi computer vision di Kaggle."
        },

        # ── SEMESTER 6 ──
        "metodologi_penelitian": {
            "sks": 2, "semester": 6,
            "emoji": "🔍", "kategori": "Wajib",
            "desc": "Metode penelitian ilmiah, penulisan proposal, tinjauan pustaka, dan analisis data.",
            "jadwal": "Rabu 10:50", "ruang": "GP 608",
            "dosen": "Mega Novita",
            "prereq": [], "difficulty": 3,
            "tips": "Gunakan Mendeley untuk manajemen referensi. Baca minimal 5 jurnal internasional per minggu."
        },
        "e_business": {
            "sks": 3, "semester": 6,
            "emoji": "🛒", "kategori": "Wajib",
            "desc": "Model bisnis digital, e-commerce, payment gateway, keamanan transaksi online.",
            "jadwal": "Senin 10:00", "ruang": "GU 401",
            "dosen": "Saeful Fahmi",
            "prereq": ["pemrograman_web"], "difficulty": 3,
            "tips": "Pelajari Shopify, WooCommerce, dan Midtrans. Analisis model bisnis marketplace Indonesia."
        },
        "data_science": {
            "sks": 3, "semester": 6,
            "emoji": "📈", "kategori": "Wajib",
            "desc": "Analisis data, machine learning dasar, visualisasi data, dan Python untuk data science.",
            "jadwal": "Senin 13:00", "ruang": "GU 401",
            "dosen": "Khoiriya Latifah",
            "prereq": ["matematika_diskrit"], "difficulty": 5,
            "tips": "Kuasai Python (Pandas, NumPy, Scikit-learn). Ikuti Kaggle competition untuk pengalaman nyata."
        },
        "teori_bahasa_dan_otomata": {
            "sks": 3, "semester": 6,
            "emoji": "⚙️", "kategori": "Wajib",
            "desc": "Automata, grammar formal, regular expression, pushdown automata, dan mesin Turing.",
            "jadwal": "Jumat 09:10", "ruang": "GP 607",
            "dosen": "Ramadhan Renaldy",
            "prereq": ["matematika_diskrit"], "difficulty": 5,
            "tips": "Visualisasikan automata dengan JFLAP. Buat implementasi regex engine sederhana."
        },
        "workshop_teknologi_informasi": {
            "sks": 3, "semester": 6,
            "emoji": "🛠️", "kategori": "Wajib",
            "desc": "Workshop praktis pengembangan proyek teknologi informasi secara tim.",
            "jadwal": "Jumat 17:10", "ruang": "GP 609",
            "dosen": "Noora Qotrun Nada",
            "prereq": ["pemrograman_web", "analisis_dan_perancangan_sistem"], "difficulty": 4,
            "tips": "Gunakan Git/GitHub untuk kolaborasi tim. Dokumentasikan setiap sprint dengan baik."
        },
        "etika_profesi": {
            "sks": 2, "semester": 6,
            "emoji": "⚖️", "kategori": "Wajib",
            "desc": "Etika profesi IT, kode etik programmer, hak kekayaan intelektual, dan cyberlaw.",
            "jadwal": "Jumat 20:10", "ruang": "GP 608",
            "dosen": "Noora Qotrun Nada",
            "prereq": [], "difficulty": 2,
            "tips": "Baca IEEE Code of Ethics dan UU ITE. Kaitkan dengan kasus nyata di dunia teknologi."
        },
        "pendidikan_pancasila": {
            "sks": 2, "semester": 6,
            "emoji": "🦅", "kategori": "Wajib",
            "desc": "Nilai-nilai Pancasila, implementasi dalam kehidupan berbangsa dan bernegara.",
            "jadwal": "Rabu 10:50", "ruang": "GP 601",
            "dosen": "Supriyono PS",
            "prereq": [], "difficulty": 1,
            "tips": "Kaitkan nilai Pancasila dengan etika dalam pengembangan teknologi dan AI."
        },

        # ── SEMESTER 7 ──
        "cloud_computing": {
            "sks": 3, "semester": 7,
            "emoji": "☁️", "kategori": "Pilihan",
            "desc": "Arsitektur cloud, layanan AWS/GCP/Azure, containerisasi Docker, dan Kubernetes.",
            "jadwal": "Senin 10:00", "ruang": "GP 609",
            "dosen": "Saeful Fahmi",
            "prereq": ["jaringan_komputer", "sistem_operasi"], "difficulty": 4,
            "tips": "Manfaatkan AWS Free Tier atau GCP Free Credits. Kejar sertifikasi AWS Cloud Practitioner."
        },
        "big_data": {
            "sks": 3, "semester": 7,
            "emoji": "🗄️", "kategori": "Pilihan",
            "desc": "Arsitektur big data, Hadoop, Spark, data pipeline, dan analitik skala besar.",
            "jadwal": "Rabu 13:00", "ruang": "GU 401",
            "dosen": "Khoiriya Latifah",
            "prereq": ["data_science"], "difficulty": 5,
            "tips": "Pelajari Apache Spark dan Kafka. Ikuti program Bangkit Academy untuk hands-on experience."
        },
        "pengembangan_game": {
            "sks": 3, "semester": 7,
            "emoji": "🎮", "kategori": "Pilihan",
            "desc": "Game design, game mechanics, pengembangan menggunakan Unity/Unreal, dan monetisasi.",
            "jadwal": "Selasa 10:00", "ruang": "GU 401",
            "dosen": "Febrian Murti Dewanto",
            "prereq": ["teknologi_animasi", "pemrograman_berorientasi_objek"], "difficulty": 4,
            "tips": "Mulai dengan game sederhana di Unity (gratis). Publish ke itch.io untuk portofolio."
        },
        "kuliah_kerja_lapangan": {
            "sks": 2, "semester": 7,
            "emoji": "🏭", "kategori": "Wajib",
            "desc": "Praktik kerja lapangan di perusahaan atau instansi terkait bidang teknologi informasi.",
            "jadwal": "Jumat 20:10", "ruang": "Balairung",
            "dosen": "Aris Tri Joko Harjanto",
            "prereq": [], "difficulty": 2,
            "tips": "Cari tempat KKL yang sesuai minat karir. Manfaatkan untuk membangun koneksi profesional."
        },
        "kuliah_kerja_nyata": {
            "sks": 4, "semester": 7,
            "emoji": "🌍", "kategori": "Wajib",
            "desc": "Pengabdian masyarakat dengan menerapkan ilmu teknologi informasi di lingkungan nyata.",
            "jadwal": "Sabtu 07:30", "ruang": "A.201",
            "dosen": "Aryan Eka Prastya Nugraha",
            "prereq": [], "difficulty": 2,
            "tips": "Buat program IT yang berkelanjutan untuk masyarakat. Dokumentasikan dengan baik untuk laporan."
        },

        # ── SEMESTER 8 ──
        "sistem_multimedia_interaktif": {
            "sks": 3, "semester": 8,
            "emoji": "🎮", "kategori": "Pilihan",
            "desc": "Desain multimedia interaktif, game development dasar, AR/VR, dan UX/UI.",
            "jadwal": "Selasa 10:00", "ruang": "GU 401",
            "dosen": "Febrian Murti Dewanto",
            "prereq": ["teknologi_animasi"], "difficulty": 4,
            "tips": "Kuasai Unity atau Godot untuk game. Pelajari prinsip UX dari Google Material Design."
        },
        "workshop_ti_lanjut": {
            "sks": 2, "semester": 8,
            "emoji": "🛠️", "kategori": "Wajib",
            "desc": "Workshop lanjut pengembangan proyek TI, persiapan tugas akhir, dan presentasi karya.",
            "jadwal": "Sabtu 10:00", "ruang": "GU 401",
            "dosen": "Noora Qotrun Nada",
            "prereq": ["workshop_teknologi_informasi"], "difficulty": 3,
            "tips": "Fokus pada proyek yang bisa dikembangkan menjadi skripsi. Mulai kumpulkan referensi jurnal."
        },
        "tugas_akhir": {
            "sks": 6, "semester": 8,
            "emoji": "🎓", "kategori": "Wajib",
            "desc": "Penelitian mandiri, pengembangan sistem/aplikasi, penulisan skripsi, dan sidang akhir.",
            "jadwal": "Sabtu 08:20", "ruang": "GP 401",
            "dosen": "Noora Qotrun Nada",
            "prereq": ["metodologi_penelitian"], "difficulty": 5,
            "tips": "Pilih topik yang sesuai passion dan relevan industri. Mulai dari semester 7. Konsultasi rutin dengan dosen pembimbing."
        },
    }

    SYNONYMS = {
        # Semester 1
        "pendidikan_agama":               ["agama", "pend agama", "pendidikan agama"],
        "pendidikan_kewarganegaraan":      ["pkn", "kewarganegaraan", "civics", "pend kewarganegaraan"],
        "matematika_dasar":               ["matdas", "matematika dasar", "mat dasar"],
        "algoritma_pemrograman":           ["algoritma", "algor", "algoprog"],
        "pengantar_teknologi_informasi":   ["pti", "pengantar ti", "pengantar teknologi"],
        "fisika_dasar":                    ["fisika", "fis dasar", "fisika dasar"],
        # Semester 2
        "kalkulus_integral":              ["kalkulus", "kalkul", "integral", "matkal", "kal int"],
        "sistem_operasi":                 ["so", "sistem operasi", "os", "sismop", "sis op"],
        "struktur_data":                  ["strukdat", "struktur data", "sd", "strdat"],
        "pemrograman_komputer":           ["pemkom", "pemrograman komputer", "progkom", "prokom"],
        "berbicara":                      ["berbicara", "speaking bahasa indonesia"],
        "ke_pgri_an":                     ["pgri", "ke-pgri-an", "kepgrian", "kepgri"],
        "bahasa_indonesia":               ["bind", "bahasa indonesia", "b.ind", "b ind"],
        "bahasa_inggris":                 ["bing", "bahasa inggris", "b.ing", "english"],
        # Semester 3
        "jaringan_komputer":              ["jarkom", "jaringan komputer", "jaringan", "network"],
        "basis_data":                     ["basdat", "basis data", "database", "db"],
        "pemrograman_berorientasi_objek": ["pbo", "oop", "pemrograman objek", "berorientasi objek"],
        "logika_informatika":             ["logika", "log inf", "logika informatika"],
        "rekayasa_perangkat_lunak":       ["rpl", "rekayasa pl", "software engineering", "softek"],
        "statistika":                     ["statistik", "stats", "stat", "statistika"],
        # Semester 4
        "matematika_diskrit":             ["matdis", "matematika diskrit", "diskrit", "mat diskrit"],
        "analisis_dan_perancangan_sistem":["aps", "analisis perancangan sistem", "analsis", "anper"],
        "pemrograman_web":                ["web", "pemweb", "progweb", "pemrograman web"],
        "metode_numerik":                 ["numerik", "metnum", "menum", "met numerik"],
        "decission_support_system":       ["dss", "decision support", "spk", "sistem pendukung keputusan"],
        "teknologi_animasi":              ["animasi", "anim", "tekno anim", "teknologi animasi"],
        "internet_of_things":             ["iot", "internet of things", "internet things"],
        "digital_marketing":              ["digmar", "digital marketing", "dig mark", "marketing digital"],
        "studi_kelayakan_bisnis":         ["skb", "studi kelayakan", "kelayakan bisnis"],
        "manajemen_sdm":                  ["msdm", "manajemen sdm", "sdm", "hr"],
        # Semester 5
        "kecerdasan_buatan":              ["ai", "kecerdasan buatan", "kb", "artificial intelligence"],
        "pemrograman_mobile":             ["mobile", "android", "ios", "pem mobile"],
        "keamanan_sistem_informasi":      ["keamanan", "ksi", "cybersecurity", "security"],
        "manajemen_proyek_ti":            ["mpti", "manajemen proyek", "project management"],
        "sistem_informasi_manajemen":     ["sim", "sistem informasi manajemen", "erp"],
        "pengolahan_citra":               ["citra", "image processing", "computer vision"],
        # Semester 6
        "metodologi_penelitian":          ["metpen", "metodologi penelitian", "metodologi", "met pen"],
        "e_business":                     ["ebis", "e-business", "ebusiness", "e business"],
        "data_science":                   ["ds", "data science", "datasci", "datascience"],
        "teori_bahasa_dan_otomata":       ["tbo", "teori bahasa", "otomata", "automata"],
        "workshop_teknologi_informasi":   ["workshop ti", "wti", "workshop teknologi", "workshop"],
        "etika_profesi":                  ["etika", "etpro", "etika profesi"],
        "pendidikan_pancasila":           ["pancasila", "pend pancasila", "ppkn pancasila"],
        # Semester 7
        "cloud_computing":                ["cloud", "aws", "gcp", "azure", "komputasi awan"],
        "big_data":                       ["big data", "bigdata", "hadoop", "spark"],
        "pengembangan_game":              ["game", "gamedev", "pengembangan game", "unity"],
        "kuliah_kerja_lapangan":          ["kkl", "kerja lapangan", "magang", "kuliah kerja lapangan"],
        "kuliah_kerja_nyata":             ["kkn", "kuliah kerja nyata", "pengabdian"],
        # Semester 8
        "sistem_multimedia_interaktif":   ["multimedia", "smi", "interaktif", "game dev"],
        "workshop_ti_lanjut":             ["workshop lanjut", "workshop 2", "workshop akhir"],
        "tugas_akhir":                    ["ta", "skripsi", "tugas akhir", "thesis", "sidang"],
    }

    def identify_course(self, text: str):
        text = text.lower()
        for key, aliases in self.SYNONYMS.items():
            for alias in aliases:
                if alias in text:
                    return key
        return None

    def parse_intent(self, text: str):
        t = text.lower()
        if re.search(r'\b(ambil|tambah|pilih|daftar|enroll|add|masukkan|mau)\b', t):
            return "ADD"
        if re.search(r'\b(hapus|buang|batalkan|cancel|remove|keluarkan|drop)\b', t):
            return "REMOVE"
        if re.search(r'\b(info|detail|jelaskan|tentang|apa itu|keterangan)\b', t):
            return "INFO"
        if re.search(r'\b(jadwal|schedule|waktu|kapan|jam)\b', t):
            return "SCHEDULE"
        if re.search(r'\b(tips|cara belajar|strategi|belajar)\b', t):
            return "TIPS"
        if re.search(r'\b(dosen|siapa pengajar|pengajar|siapa yang)\b', t):
            return "DOSEN"
        if re.search(r'\b(prasyarat|syarat|prerequisite|butuh)\b', t):
            return "PREREQ"
        if re.search(r'\b(sulit|susah|mudah|tingkat|level|difficulty)\b', t):
            return "DIFFICULTY"
        if re.search(r'\b(rekomen|rekomendasi|saran|suggest|pilihkan)\b', t):
            return "RECOMMEND"
        if re.search(r'\b(submit|kirim|selesai|konfirmasi|finalisasi)\b', t):
            return "SUBMIT"
        if re.search(r'\b(total|jumlah|berapa sks|sks saya)\b', t):
            return "TOTAL_SKS"
        if re.search(r'\b(krs|daftar matkul|matkul saya|isi krs)\b', t):
            return "MY_KRS"
        if re.search(r'\b(hapus semua|kosongkan|clear|reset krs)\b', t):
            return "CLEAR"
        if re.search(r'\b(menu|list|katalog|matkul apa|tersedia|daftar matkul)\b', t):
            return "MENU"
        if re.search(r'\b(bantuan|help|panduan|cara|petunjuk)\b', t):
            return "HELP"
        if re.search(r'\b(halo|hai|hello|hi|selamat|pagi|siang|malam)\b', t):
            return "GREET"
        return "UNKNOWN"


class AcademicFSM:
    def __init__(self):
        self.state   = State.GREETING
        self.cart    = []
        self.nlp     = NLPEngine()
        self._resp   = ""
        self.notifications = []

    def _notify(self, msg):
        self.notifications.append(msg)
        if len(self.notifications) > 5:
            self.notifications.pop(0)

    def total_sks(self):
        return sum(c["sks"] for c in self.cart)

    def get_response(self):
        return self._resp

    def add_course(self, key: str):
        data = self.nlp.course_data.get(key)
        if not data:
            return False, "❌ Mata kuliah tidak ditemukan."
        if any(c["course_key"] == key for c in self.cart):
            return False, f"⚠️ **{key.replace('_',' ').title()}** sudah ada di KRS kamu."
        for pre in data["prereq"]:
            if not any(c["course_key"] == pre for c in self.cart):
                pre_name = pre.replace("_", " ").title()
                return False, f"🔒 Tidak bisa menambahkan **{key.replace('_',' ').title()}** — prasyarat **{pre_name}** belum diambil."
        for c in self.cart:
            if c["jadwal"] == data["jadwal"]:
                return False, f"⏰ Konflik jadwal! **{key.replace('_',' ').title()}** bentrok dengan **{c['course_key'].replace('_',' ').title()}** di jadwal {data['jadwal']}."
        if self.total_sks() + data["sks"] > self.nlp.MAX_SKS:
            return False, f"📊 Tidak bisa tambah! Total SKS akan melebihi batas maksimum {self.nlp.MAX_SKS} SKS."
        self.cart.append({
            "course_key": key, "sks": data["sks"],
            "jadwal": data["jadwal"], "ruang": data["ruang"],
            "dosen": data["dosen"], "emoji": data["emoji"],
        })
        self._notify(f"➕ Ditambahkan: {key.replace('_',' ').title()} ({data['sks']} SKS)")
        return True, (
            f"{data['emoji']} **{key.replace('_',' ').title()}** berhasil ditambahkan ke KRS!\n\n"
            f"- 📅 Jadwal: {data['jadwal']}\n"
            f"- 📍 Ruang: {data['ruang']}\n"
            f"- 👨‍🏫 Dosen: {data['dosen']}\n"
            f"- 📊 SKS: {data['sks']} | Total sekarang: **{self.total_sks()} SKS**\n\n"
            f"💡 *Tips: {data['tips']}*"
        )

    def remove_course(self, key: str):
        before = len(self.cart)
        self.cart = [c for c in self.cart if c["course_key"] != key]
        if len(self.cart) < before:
            self._notify(f"🗑️ Dihapus: {key.replace('_','  ').title()}")
            return f"🗑️ **{key.replace('_',' ').title()}** berhasil dihapus dari KRS."
        return f"⚠️ **{key.replace('_',' ').title()}** tidak ada di KRS kamu."

    def step(self, user_input: str = ""):
        if not user_input:
            self._resp = self._greeting()
            self.state = State.BROWSING
            return

        intent = self.nlp.parse_intent(user_input)
        course = self.nlp.identify_course(user_input)

        if self.state == State.DONE:
            if re.search(r'\b(reset|mulai ulang|baru|lagi)\b', user_input.lower()):
                self.cart = []
                self.notifications = []
                self.state = State.BROWSING
                self._resp = "🔄 KRS direset. Silakan susun ulang dari awal!"
            else:
                self._resp = "✅ KRS sudah disubmit. Ketik **reset** untuk mulai ulang."
            return

        if self.state == State.CONFIRM:
            if re.search(r'\b(ya|iya|yes|ok|setuju|konfirmasi|lanjut)\b', user_input.lower()):
                self.state = State.DONE
                self._notify("✅ KRS berhasil disubmit!")
                self._resp = self._done_msg()
            elif re.search(r'\b(tidak|batal|no|cancel|belum)\b', user_input.lower()):
                self.state = State.BROWSING
                self._resp = "↩️ Submit dibatalkan. KRS masih bisa diubah."
            else:
                self._resp = "❓ Ketik **ya** untuk konfirmasi submit atau **tidak** untuk batal."
            return

        if intent == "ADD" and course:
            _, msg = self.add_course(course)
            self._resp = msg
        elif intent == "REMOVE" and course:
            if re.search(r'\b(semua|all|hapus semua|clear)\b', user_input.lower()):
                self.cart = []
                self._resp = "🗑️ Semua mata kuliah dihapus dari KRS."
            else:
                self._resp = self.remove_course(course)
        elif intent == "CLEAR":
            self.cart = []
            self._resp = "🗑️ KRS dikosongkan."
        elif intent == "INFO" and course:
            self._resp = self._info_msg(course)
        elif intent == "SCHEDULE" and course:
            d = self.nlp.course_data.get(course, {})
            self._resp = f"📅 Jadwal **{course.replace('_',' ').title()}**: {d.get('jadwal','?')} di {d.get('ruang','?')}"
        elif intent == "SCHEDULE":
            self._resp = self._my_schedule()
        elif intent == "TIPS" and course:
            d = self.nlp.course_data.get(course, {})
            self._resp = f"💡 Tips **{course.replace('_',' ').title()}**:\n{d.get('tips','Rajin belajar!')}"
        elif intent == "DOSEN" and course:
            d = self.nlp.course_data.get(course, {})
            self._resp = f"👨‍🏫 Dosen **{course.replace('_',' ').title()}**: {d.get('dosen','?')} | Jadwal: {d.get('jadwal','?')}"
        elif intent == "PREREQ" and course:
            self._resp = self._prereq_msg(course)
        elif intent == "DIFFICULTY" and course:
            d = self.nlp.course_data.get(course, {})
            stars = "⭐" * d.get("difficulty", 3)
            self._resp = f"🎯 Tingkat kesulitan **{course.replace('_',' ').title()}**: {stars} ({d.get('difficulty',3)}/5)"
        elif intent == "RECOMMEND":
            self._resp = self._recommend()
        elif intent == "SUBMIT":
            if not self.cart:
                self._resp = "📭 KRS masih kosong! Tambahkan dulu beberapa mata kuliah."
            else:
                self.state = State.CONFIRM
                self._resp = self._confirm_msg()
        elif intent == "TOTAL_SKS":
            self._resp = f"📊 Total SKS kamu: **{self.total_sks()}** dari maksimum **{self.nlp.MAX_SKS} SKS** ({int(self.total_sks()/self.nlp.MAX_SKS*100)}% terisi)"
        elif intent == "MY_KRS":
            self._resp = self._my_krs()
        elif intent == "MENU":
            self._resp = self._menu_msg()
        elif intent == "HELP":
            self._resp = self._help_msg()
        elif intent == "GREET":
            self._resp = "👋 Halo! Saya SIKRS, asisten KRS kamu. Ketik **menu** untuk lihat daftar mata kuliah atau **bantuan** untuk panduan lengkap."
        else:
            self._resp = (
                "🤔 Maaf, saya kurang paham. Coba perintah seperti:\n"
                "- `ambil [nama matkul]`\n- `hapus [nama matkul]`\n- `info [nama matkul]`\n"
                "- `rekomen` / `jadwal` / `submit KRS` / `bantuan`"
            )

    def _greeting(self):
        return (
            "**Selamat datang di SIKRS UPGRIS!**\n\n"
            "Saya akan membantu kamu menyusun Kartu Rencana Studi Semester Genap 2025/2026.\n\n"
            "**Apa yang bisa saya lakukan?**\n"
            "- 📚 Tampilkan daftar mata kuliah\n"
            "- ➕ Tambah/hapus matkul ke KRS\n"
            "- ⚠️ Validasi prasyarat & konflik jadwal\n"
            "- 🎯 Rekomendasikan matkul\n"
            "- 💡 Beri tips belajar per matkul\n\n"
            "Ketik **menu** untuk melihat semua mata kuliah, atau **bantuan** untuk panduan lengkap."
        )

    def _menu_msg(self):
        lines = ["📚 **Daftar Mata Kuliah Tersedia:**\n"]
        by_sem = {}
        for k, v in self.nlp.course_data.items():
            by_sem.setdefault(v["semester"], []).append((k, v))
        for sem in sorted(by_sem):
            lines.append(f"\n**── Semester {sem} ──**")
            for k, v in by_sem[sem]:
                in_krs = "✅" if any(c["course_key"] == k for c in self.cart) else "◻️"
                kat_tag = "Wajib" if v["kategori"] == "Wajib" else "Pilihan"
                lines.append(
                    f"\n{in_krs} {v['emoji']} **{k.replace('_',' ').title()}**\n"
                    f"   {v['sks']} SKS · {kat_tag}\n"
                    f"   🕐 {v['jadwal']} · 📍 {v['ruang']}"
                )
        lines.append(f"\n\n📊 **Total SKS kamu: {self.total_sks()}/{self.nlp.MAX_SKS} SKS**")
        lines.append("Ketik `ambil [nama matkul]` untuk menambahkan ke KRS.")
        return "\n".join(lines)

    def _info_msg(self, key):
        d = self.nlp.course_data.get(key)
        if not d:
            return "❌ Matkul tidak ditemukan."
        pre = ", ".join(p.replace("_"," ").title() for p in d["prereq"]) or "Tidak ada"
        stars = "⭐" * d["difficulty"] + "☆" * (5 - d["difficulty"])
        return (
            f"{d['emoji']} **{key.replace('_',' ').title()}**\n\n"
            f"📖 {d['desc']}\n\n"
            f"- 📅 Jadwal: {d['jadwal']}\n"
            f"- 📍 Ruang: {d['ruang']}\n"
            f"- 👨‍🏫 Dosen: {d['dosen']}\n"
            f"- 📊 SKS: {d['sks']} | Semester: {d['semester']}\n"
            f"- 🏷️ Kategori: {d['kategori']}\n"
            f"- 🔒 Prasyarat: {pre}\n"
            f"- 🎯 Kesulitan: {stars}\n"
            f"- 💡 Tips: *{d['tips']}*"
        )

    def _prereq_msg(self, key):
        d = self.nlp.course_data.get(key)
        if not d:
            return "❌ Matkul tidak ditemukan."
        if not d["prereq"]:
            return f"✅ **{key.replace('_',' ').title()}** tidak punya prasyarat."
        lines = [f"🔒 Prasyarat **{key.replace('_',' ').title()}**:"]
        for p in d["prereq"]:
            status = "✅ Sudah diambil" if any(c["course_key"] == p for c in self.cart) else "❌ Belum diambil"
            lines.append(f"- {p.replace('_',' ').title()} → {status}")
        return "\n".join(lines)

    def _recommend(self):
        taken = {c["course_key"] for c in self.cart}
        taken_jadwal = {c["jadwal"] for c in self.cart}
        recs = []
        for k, v in self.nlp.course_data.items():
            if k in taken:
                continue
            if self.total_sks() + v["sks"] > self.nlp.MAX_SKS:
                continue
            if v["jadwal"] in taken_jadwal:
                continue
            prereq_ok = all(p in taken for p in v["prereq"])
            if prereq_ok:
                recs.append((k, v))
        if not recs:
            return "🤔 Tidak ada rekomendasi tersedia saat ini (SKS penuh atau semua prasyarat belum terpenuhi)."
        random.shuffle(recs)
        lines = ["🎯 **Rekomendasi Mata Kuliah untuk Kamu:**\n"]
        for k, v in recs[:5]:
            lines.append(
                f"- {v['emoji']} **{k.replace('_',' ').title()}** ({v['sks']} SKS)\n"
                f"  📅 {v['jadwal']} · 📍 {v['ruang']} · 👨‍🏫 {v['dosen']}"
            )
        lines.append(f"\nKetik `ambil [nama matkul]` untuk menambahkan ke KRS.")
        return "\n".join(lines)

    def _my_schedule(self):
        if not self.cart:
            return "📭 KRS masih kosong."
        days = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"]
        by_day = {d: [] for d in days}
        for c in self.cart:
            for d in days:
                if d in c["jadwal"]:
                    by_day[d].append(c); break
        lines = ["📅 **Jadwal KRS Kamu:**\n"]
        for d in days:
            if by_day[d]:
                lines.append(f"**{d}:**")
                for c in by_day[d]:
                    jam = c["jadwal"].split(" ",1)[1] if " " in c["jadwal"] else c["jadwal"]
                    lines.append(f"  {c['emoji']} {c['course_key'].replace('_',' ').title()} — {jam} | {c['ruang']}")
        return "\n".join(lines)

    def _my_krs(self):
        if not self.cart:
            return "📭 KRS masih kosong. Tambahkan matkul dengan perintah `ambil [nama matkul]`."
        lines = [f"📋 **KRS Kamu ({self.total_sks()}/{self.nlp.MAX_SKS} SKS):**\n"]
        for c in self.cart:
            lines.append(f"- {c['emoji']} **{c['course_key'].replace('_',' ').title()}** ({c['sks']} SKS) — {c['jadwal']}")
        return "\n".join(lines)

    def _confirm_msg(self):
        lines = [f"📋 **Konfirmasi Submit KRS ({self.total_sks()} SKS):**\n"]
        for c in self.cart:
            lines.append(f"- {c['emoji']} {c['course_key'].replace('_',' ').title()} ({c['sks']} SKS)")
        lines.append("\nKetik **ya** untuk submit atau **tidak** untuk batal.")
        return "\n".join(lines)

    def _done_msg(self):
        return (
            "🎉 **KRS berhasil disubmit!**\n\n"
            f"Total: **{self.total_sks()} SKS** dalam {len(self.cart)} mata kuliah.\n\n"
            "Semangat belajar semester ini! 💪\n"
            "Ketik **reset** jika ingin mulai ulang."
        )

    def _help_msg(self):
        return (
            "❓ **Panduan Penggunaan SIKRS:**\n\n"
            "**Mengelola KRS:**\n"
            "- `menu` → daftar semua matkul\n"
            "- `ambil [matkul]` → tambah ke KRS\n"
            "- `hapus [matkul]` → hapus dari KRS\n"
            "- `hapus semua` → kosongkan KRS\n"
            "- `krs saya` → ringkasan KRS\n"
            "- `total sks` → cek kapasitas SKS\n"
            "- `submit KRS` → finalisasi dan kirim KRS\n\n"
            "**Informasi Matkul:**\n"
            "- `info [matkul]` → detail lengkap\n"
            "- `jadwal [matkul]` → jadwal & ruangan\n"
            "- `dosen [matkul]` → info dosen\n"
            "- `prasyarat [matkul]` → cek syarat\n"
            "- `tips [matkul]` → tips belajar\n"
            "- `rekomen` → rekomendasi matkul\n"
        )