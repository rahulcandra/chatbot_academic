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

    DOSEN_MAP = {
        "bambang": ["basis_data", "analisis_dan_perancangan_sistem", "manajemen_proyek_ti"],
        "beng": ["basis_data", "analisis_dan_perancangan_sistem", "manajemen_proyek_ti"],
        "bambang herlambang": ["basis_data", "analisis_dan_perancangan_sistem", "manajemen_proyek_ti"],
        "pak bambang": ["basis_data", "analisis_dan_perancangan_sistem", "manajemen_proyek_ti"],
        "agung": ["matematika_dasar", "logika_informatika", "matematika_diskrit", "metode_numerik"],
        "agung handayanto": ["matematika_dasar", "logika_informatika", "matematika_diskrit", "metode_numerik"],
        "pak agung": ["matematika_dasar", "logika_informatika", "matematika_diskrit", "metode_numerik"],
        "nugroho": ["algoritma_pemrograman", "pemrograman_komputer"],
        "pak nugroho": ["algoritma_pemrograman", "pemrograman_komputer"],
        "noora": ["pengantar_teknologi_informasi", "jaringan_komputer", "internet_of_things", "workshop_teknologi_informasi", "etika_profesi", "workshop_ti_lanjut", "tugas_akhir"],
        "noora qotrun": ["pengantar_teknologi_informasi", "jaringan_komputer", "internet_of_things", "workshop_teknologi_informasi", "etika_profesi", "workshop_ti_lanjut", "tugas_akhir"],
        "bu noora": ["pengantar_teknologi_informasi", "jaringan_komputer", "internet_of_things", "workshop_teknologi_informasi", "etika_profesi", "workshop_ti_lanjut", "tugas_akhir"],
        "ramadhan": ["sistem_operasi", "struktur_data", "teori_bahasa_dan_otomata"],
        "ramadhan renaldy": ["sistem_operasi", "struktur_data", "teori_bahasa_dan_otomata"],
        "pak re": ["sistem_operasi", "struktur_data", "teori_bahasa_dan_otomata"],
        "rizky": ["kalkulus_integral", "statistika"],
        "rizky esti": ["kalkulus_integral", "statistika"],
        "bu rizky": ["kalkulus_integral", "statistika"],
        "aris": ["pemrograman_berorientasi_objek", "pemrograman_web", "kuliah_kerja_lapangan"],
        "aris tri": ["pemrograman_berorientasi_objek", "pemrograman_web", "kuliah_kerja_lapangan"],
        "pak aris": ["pemrograman_berorientasi_objek", "pemrograman_web", "kuliah_kerja_lapangan"],
        "setyoningsih": ["rekayasa_perangkat_lunak", "decission_support_system", "sistem_informasi_manajemen"],
        "bu setyoningsih": ["rekayasa_perangkat_lunak", "decission_support_system", "sistem_informasi_manajemen"],
        "khoiriya": ["kecerdasan_buatan", "data_science", "big_data"],
        "bu khoiriya": ["kecerdasan_buatan", "data_science", "big_data"],
        "saeful fahmi": ["keamanan_sistem_informasi", "e_business", "cloud_computing"],
        "pak fahmi": ["keamanan_sistem_informasi", "e_business", "cloud_computing"],
        "febrian dewantoro": ["teknologi_animasi", "pemrograman_mobile", "pengembangan_game", "sistem_multimedia_interaktif"],
        "pak anto": ["teknologi_animasi", "pemrograman_mobile", "pengembangan_game", "sistem_multimedia_interaktif"],
        "mega": ["pengolahan_citra", "metodologi_penelitian"],
        "bu mega": ["pengolahan_citra", "metodologi_penelitian"],
        "mega novita": ["pengolahan_citra", "metodologi_penelitian"],
        "sri suciati": ["berbicara"],
        "bu sri": ["berbicara"],
        "hari waluyo": ["ke_pgri_an"],
        "pak hari": ["ke_pgri_an"],
        "siti ulfiyani": ["bahasa_indonesia"],
        "bu siti": ["bahasa_indonesia"],
        "jafar": ["bahasa_inggris"],
        "pak jafar": ["bahasa_inggris"],
        "aryan": ["digital_marketing", "kuliah_kerja_nyata"],
        "pak aryan": ["digital_marketing", "kuliah_kerja_nyata"],
        "dwi": ["studi_kelayakan_bisnis", "manajemen_sdm"],
        "pak dwi": ["studi_kelayakan_bisnis", "manajemen_sdm"],
        "supriyono": ["pendidikan_pancasila"],
        "pak supriyono": ["pendidikan_pancasila"],
    }

    SYNONYMS = {
        "pendidikan_agama":               ["agama", "pend agama", "pendidikan agama"],
        "pendidikan_kewarganegaraan":      ["pkn", "kewarganegaraan", "civics", "pend kewarganegaraan"],
        "matematika_dasar":               ["matdas", "matematika dasar", "mat dasar"],
        "algoritma_pemrograman":           ["algoritma", "algor", "algoprog"],
        "pengantar_teknologi_informasi":   ["pti", "pengantar ti", "pengantar teknologi"],
        "fisika_dasar":                    ["fisika", "fis dasar", "fisika dasar"],
        "kalkulus_integral":              ["kalkulus", "kalkul", "integral", "matkal", "kal int"],
        "sistem_operasi":                 ["sistem operasi", "sismop", "sis op"],
        "struktur_data":                  ["strukdat", "struktur data", "strdat"],
        "pemrograman_komputer":           ["pemkom", "pemrograman komputer", "progkom", "prokom"],
        "berbicara":                      ["berbicara", "speaking bahasa indonesia"],
        "ke_pgri_an":                     ["pgri", "ke-pgri-an", "kepgrian", "kepgri"],
        "bahasa_indonesia":               ["bind", "bahasa indonesia", "b.ind"],
        "bahasa_inggris":                 ["bing", "bahasa inggris", "b.ing", "english"],
        "jaringan_komputer":              ["jarkom", "jaringan komputer", "jaringan"],
        "basis_data":                     ["basdat", "basis data", "database"],
        "pemrograman_berorientasi_objek": ["pbo", "oop", "pemrograman objek", "berorientasi objek"],
        "logika_informatika":             ["logika", "log inf", "logika informatika"],
        "rekayasa_perangkat_lunak":       ["rpl", "rekayasa pl", "software engineering", "softek"],
        "statistika":                     ["statistik", "stats", "stat", "statistika"],
        "matematika_diskrit":             ["matdis", "matematika diskrit", "diskrit", "mat diskrit"],
        "analisis_dan_perancangan_sistem":["aps", "analisis perancangan sistem", "analsis", "anper"],
        "pemrograman_web":                ["pemweb", "progweb", "pemrograman web"],
        "metode_numerik":                 ["numerik", "metnum", "menum", "met numerik"],
        "decission_support_system":       ["dss", "decision support", "spk", "sistem pendukung keputusan"],
        "teknologi_animasi":              ["animasi", "anim", "tekno anim", "teknologi animasi"],
        "internet_of_things":             ["iot", "internet of things", "internet things"],
        "digital_marketing":              ["digmar", "digital marketing", "dig mark", "marketing digital"],
        "studi_kelayakan_bisnis":         ["skb", "studi kelayakan", "kelayakan bisnis"],
        "manajemen_sdm":                  ["msdm", "manajemen sdm", "sdm"],
        "kecerdasan_buatan":              ["kecerdasan buatan", "kb", "artificial intelligence"],
        "pemrograman_mobile":             ["mobile", "android", "ios", "pem mobile"],
        "keamanan_sistem_informasi":      ["keamanan", "ksi", "cybersecurity", "security"],
        "manajemen_proyek_ti":            ["mpti", "manajemen proyek", "project management"],
        "sistem_informasi_manajemen":     ["sim", "sistem informasi manajemen", "erp"],
        "pengolahan_citra":               ["citra", "image processing", "computer vision"],
        "metodologi_penelitian":          ["metpen", "metodologi penelitian", "metodologi", "met pen"],
        "e_business":                     ["ebis", "e-business", "ebusiness", "e business"],
        "data_science":                   ["data science", "datasci", "datascience"],
        "teori_bahasa_dan_otomata":       ["tbo", "teori bahasa", "otomata", "automata"],
        "workshop_teknologi_informasi":   ["workshop ti", "wti", "workshop teknologi"],
        "etika_profesi":                  ["etika", "etpro", "etika profesi"],
        "pendidikan_pancasila":           ["pancasila", "pend pancasila", "ppkn pancasila"],
        "cloud_computing":                ["cloud", "aws", "gcp", "azure", "komputasi awan"],
        "big_data":                       ["bigdata", "hadoop", "spark"],
        "pengembangan_game":              ["gamedev", "pengembangan game", "unity"],
        "kuliah_kerja_lapangan":          ["kkl", "kerja lapangan", "magang", "kuliah kerja lapangan"],
        "kuliah_kerja_nyata":             ["kkn", "kuliah kerja nyata", "pengabdian"],
        "sistem_multimedia_interaktif":   ["multimedia", "smi", "interaktif"],
        "workshop_ti_lanjut":             ["workshop lanjut", "workshop 2", "workshop akhir"],
        "tugas_akhir":                    ["ta", "skripsi", "tugas akhir", "thesis", "sidang"],
    }

    SINGLE_WORD_MAP = {
        "so": "sistem_operasi",
        "os": "sistem_operasi",
        "sd": "struktur_data",
        "ai": "kecerdasan_buatan",
        "web": "pemrograman_web",
        "game": "pengembangan_game",
        "network": "jaringan_komputer",
        "db": "basis_data",
        "ds": "data_science",
        "big data": "big_data",
        "hr": "manajemen_sdm",
        "workshop": "workshop_teknologi_informasi",
    }

    def identify_course(self, text: str):
        text = text.lower()
        best_key = None
        best_len = 0
        for key, aliases in self.SYNONYMS.items():
            for alias in aliases:
                if alias in text and len(alias) > best_len:
                    best_key = key
                    best_len = len(alias)
        if best_key:
            return best_key
        for word, key in self.SINGLE_WORD_MAP.items():
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                return key
        return None

    def identify_dosen(self, text: str):
        t = text.lower()
        best_key = None
        best_len = 0
        for dosen_key in self.DOSEN_MAP:
            if dosen_key in t and len(dosen_key) > best_len:
                best_key = dosen_key
                best_len = len(dosen_key)
        if best_key:
            return best_key, self.DOSEN_MAP[best_key]
        return None, []

    def identify_semester(self, text: str):
        m = re.search(r'semester\s*(\d)', text.lower())
        if m:
            return int(m.group(1))
        for kata, angka in [("satu","1"),("dua","2"),("tiga","3"),("empat","4"),
                             ("lima","5"),("enam","6"),("tujuh","7"),("delapan","8")]:
            if kata in text.lower():
                return int(angka)
        return None

    def parse_intent(self, text: str):
        t = text.lower()

        if re.search(
            r'\b(halo|hai|hello|hi|hey|hei|selamat pagi|selamat siang|selamat sore|selamat malam'
            r'|assalamualaikum|waalaikumsalam|permisi|pagi|siang kak|sore kak|malam kak)\b', t):
            return "GREET"

        if re.search(
            r'(siapa kamu|kamu siapa|lo siapa|ini siapa|kamu itu apa|apa ini|ini apa'
            r'|kamu robot|kamu ai|kamu bot|ini bot|kamu chatbot|ini chatbot'
            r'|namamu siapa|nama kamu apa|dipanggil apa|nama botnya)', t):
            return "IDENTITY"

        if re.search(
            r'\b(terima kasih|makasih|thanks|thx|tengkyu|tq|syukran|nuhun|matur nuwun'
            r'|terimakasih|mksh|trimakasih|arigatou|thank you)\b', t):
            return "THANKS"

        # ════════════════════════════════════════════════════════════
        # FITUR: Ambil semua matkul semester X
        # Harus dicek SEBELUM intent ADD agar tidak salah klasifikasi
        # ════════════════════════════════════════════════════════════
        if re.search(
            r'(ambil semua.*semester|semua matkul.*semester|matkul semester.*semua'
            r'|ambil.*semua.*semester|tambah semua.*semester|daftarkan semua.*semester'
            r'|enroll semua.*semester|masukkan semua.*semester|ikut semua.*semester'
            r'|pilih semua.*semester|semester.*ambil semua|semua matkul di semester'
            r'|mau ambil semua.*semester|pengen ambil semua.*semester'
            r'|ingin ambil semua.*semester|langsung ambil semua.*semester'
            r'|ambil semua matkul semester|tambah semua matkul semester'
            r'|saya mau ambil seluruh.*semester|mau ambil seluruh matkul.*semester'
            r'|ambil seluruh matkul.*semester|seluruh matkul semester.*ambil'
            r'|ambil seluruh.*semester|tambahkan seluruh.*semester'
            r'|daftarkan seluruh.*semester|mau seluruh matkul semester'
            r'|pengen seluruh matkul semester|ingin seluruh matkul semester'
            r'|borong semua.*semester|borong matkul semester|sapu semua.*semester'
            r'|ambil paket semester|ambil satu paket semester|paket lengkap semester'
            r'|full ambil semester|ambil full semester|semester.*ambil semuanya'
            r'|tambahkan semuanya.*semester|semuanya semester.*ambil'
            r'|gas semua.*semester|gaskan semua.*semester)', t):
            return "ADD_ALL_SEMESTER"

        # ════════════════════════════════════════════════════════════
        # FITUR: Lihat semua matkul di semester X ("matkul semester 3 apa saja")
        # Harus dicek SEBELUM intent MENU dan SCHEDULE
        # ════════════════════════════════════════════════════════════
        if re.search(
            r'(matkul semester.*apa saja|mata kuliah semester.*apa saja'
            r'|matkul semester.*apa aja|mata kuliah semester.*apa aja'
            r'|semester.*matkul apa saja|semester.*matkul apa aja'
            r'|semester.*ada matkul apa|semester.*ada mata kuliah apa'
            r'|apa saja matkul semester|apa saja mata kuliah semester'
            r'|apa aja matkul semester|apa aja mata kuliah semester'
            r'|matkul.*semester.*berisi apa|mata kuliah.*semester.*berisi apa'
            r'|isi semester.*apa|semester.*isinya apa|semester.*isi apa'
            r'|daftar matkul semester|daftar mata kuliah semester'
            r'|list matkul semester|list mata kuliah semester'
            r'|semester.*matkulnya apa|semester.*mata kuliahnya apa'
            r'|matkul.*di semester.*apa|mata kuliah.*di semester.*apa'
            r'|ada matkul apa.*semester|ada mata kuliah apa.*semester'
            r'|sebutkan matkul semester|sebutkan mata kuliah semester'
            r'|tampilkan matkul semester|tampilkan mata kuliah semester'
            r'|lihat matkul semester|lihat mata kuliah semester'
            r'|matkul yang ada di semester|mata kuliah yang ada di semester)', t):
            return "LIST_MATKUL_SEMESTER"

        if re.search(
            r'(dosen apa|ngajar apa|mengajar apa|ngampu apa|ampu apa|matkul apa yang diajar'
            r'|mata kuliah apa yang diajar|mengampu apa|dia ngajar apa|beliau ngajar apa'
            r'|pak .+ dosen|bu .+ dosen|mengajar matkul apa|ngajar matkul apa'
            r'|dosen matkul apa|ngajar di mana|mengajar di mana)', t):
            return "DOSEN_NGAJAR_APA"

        if re.search(
            r'(matkul.*gampang|matkul.*mudah|matkul.*ringan|matkul.*santai|yang gampang'
            r'|yang mudah|yang ringan|yang santai|paling gampang|paling mudah|paling ringan'
            r'|gampang.*semester|mudah.*semester|ringan.*semester|semester.*gampang'
            r'|semester.*mudah|semester.*ringan|matkul enak|yang enak diambil'
            r'|matkul yang tidak susah|matkul yang ga susah|yang ga berat|yang tidak berat)', t):
            return "EASY_MATKUL"

        # ════════════════════════════════════════════════════════════
        # FITUR: Rekomendasi matkul gampang ("rekomen matkul gampang semester X")
        # ════════════════════════════════════════════════════════════
        if re.search(
            r'(rekomen.*gampang|rekomen.*mudah|rekomen.*ringan|rekomen.*santai'
            r'|saran.*gampang|saran.*mudah|rekomen.*semester.*gampang'
            r'|rekomen.*gampang.*semester|matkul ringan semester|pilih.*yang.*mudah'
            r'|ambil.*yang.*gampang|pilih.*yang.*gampang|mau.*yang.*santai'
            r'|rekomen.*matkul.*gampang.*semester|rekomendasikan.*matkul.*gampang'
            r'|rekomendasikan.*matkul.*mudah|rekomen mata kuliah.*gampang'
            r'|rekomen mata kuliah.*mudah|rekomen mata kuliah.*ringan'
            r'|rekomendasi matkul gampang|rekomendasi matkul mudah'
            r'|rekomendasi mata kuliah gampang|rekomendasi mata kuliah mudah'
            r'|kasih rekomen.*gampang|kasih rekomendasi.*gampang'
            r'|kasih saran matkul.*gampang|saranin matkul.*gampang'
            r'|saranin matkul.*mudah|carikan matkul gampang|carikan matkul mudah'
            r'|cariin matkul gampang|cariin matkul mudah|tolong rekomen.*gampang'
            r'|tolong rekomendasikan.*gampang|matkul gampang.*rekomen'
            r'|matkul mudah.*rekomen|rekomen.*yang paling gampang'
            r'|rekomen.*yang paling mudah|rekomen.*yang santai.*semester)', t):
            return "REKOMEN_GAMPANG"

        if re.search(
            r'\b(submit|kirim|selesai|konfirmasi|finalisasi|simpan krs|kumpulkan|krs sudah selesai'
            r'|krs-nya sudah|krs nya sudah|udah selesai|udah beres|krs fix|fix krs'
            r'|mau submit|mau kirim|kirim krs|selesaikan krs|akhiri krs|krs selesai)\b', t):
            return "SUBMIT"

        if re.search(
            r'(hapus semua|kosongkan|clear krs|reset krs|buang semua|bersihkan krs'
            r'|mulai dari awal|mulai ulang krs|krs dikosongkan|mau ulang|ulang lagi)', t):
            return "CLEAR"

        if re.search(
            r'\b(ambil|tambah|pilih|daftar|enroll|masukkan|ikut|ikuti|daftarkan'
            r'|mau ambil|pengen ambil|ingin ambil|mau ikut|mau daftar|mau pilih'
            r'|bisa ambil|bisa tambah|tolong ambil|tolong tambah|tolong masukkan'
            r'|coba ambil|langsung ambil|saya mau|aku mau|gue mau|saya ingin|aku ingin'
            r'|mau ngambil|pengen ngambil|rencana ambil|rencana ikut|kayaknya ambil'
            r'|jadiin|masukin|tambahin|ambilkan|pilihkan saja|pilih aja|ambil aja'
            r'|bolehin|boleh ambil|bolehkah ambil|bisakan|bisa ga ambil|bisa gak ambil'
            r'|register|add matkul|add ke krs|masuk ke krs)\b', t):
            return "ADD"

        if re.search(
            r'\b(hapus|buang|batalkan|cancel|remove|keluarkan|drop|tidak jadi|ga jadi|gak jadi'
            r'|jangan ambil|jangan masukin|batal ambil|cabut|tarik|undur|urungkan'
            r'|hapusin|keluarin|buangin|hilangkan|tidak jadi ambil|ga mau lagi'
            r'|gak mau|mau hapus|pengen hapus|ingin hapus|tolong hapus|delete)\b', t):
            return "REMOVE"

        if re.search(
            r'\b(info|detail|jelaskan|tentang|apa itu|keterangan|ceritain|ceritakan'
            r'|gimana|bagaimana|seperti apa|kayak gimana|ngapain aja|isinya apa'
            r'|materinya apa|belajar apa|pelajarannya apa|matkul ini tentang'
            r'|apa yang dipelajari|dipelajari apa|materi apa|konten apa|deskripsi'
            r'|cari tahu|penjelasan|pengen tau|pengen tahu|mau tau|mau tahu'
            r'|tolong jelasin|bisa jelasin|tolong jelaskan|bisa jelaskan)\b', t):
            return "INFO"

        if re.search(
            r'\b(jadwal|schedule|kapan|jam|hari|waktu|ruang|ruangan|di mana|dimana|tempatnya'
            r'|jam berapa|hari apa|kuliah kapan|ada di hari|masuk hari|kelasnya'
            r'|jadwalnya|jadwal kuliah|jadwal matkul|lihat jadwal|cek jadwal|kapan masuk'
            r'|senin|selasa|rabu|kamis|jumat|sabtu|minggu)\b', t):
            return "SCHEDULE"

        if re.search(
            r'\b(tips|cara belajar|strategi belajar|belajar gimana|biar bisa|biar lulus'
            r'|biar nilai|kiat|trik belajar|gimana belajar|supaya lulus|agar lulus'
            r'|supaya bisa|cara biar nilai|cara dapet nilai|cara supaya|cara agar'
            r'|gimana caranya belajar|rekomendasi belajar|saran belajar|bagaimana belajar'
            r'|study tips|belajarnya gimana|tips lulus|cara ngerjain|cara mengerjakan'
            r'|cara nguasain|cara menguasai)\b', t):
            return "TIPS"

        if re.search(
            r'\b(dosen|pengajar|pengampu|instruktur|siapa yang ngajar|siapa yang mengajar'
            r'|diampu siapa|diampu oleh|ngajarnya siapa|dosennya siapa|dosennya apa'
            r'|siapa dosennya|gurunya siapa|yang ngajar siapa|pak siapa|bu siapa'
            r'|nama dosennya|dosen pengampunya|siapa pengajarnya)\b', t):
            return "DOSEN"

        if re.search(
            r'\b(prasyarat|syarat|prerequisite|butuh apa|perlu lulus|harus lulus dulu'
            r'|syaratnya|ada syaratnya|ada prasyarat|perlu apa dulu|harus ambil apa dulu'
            r'|boleh langsung|bisa langsung ambil|syarat ambil|syarat daftar'
            r'|sebelum ambil|matkul sebelumnya|harus selesai apa dulu)\b', t):
            return "PREREQ"

        if re.search(
            r'\b(sulit|susah|mudah|gampang|tingkat|level|difficulty|berat|ringan'
            r'|susah ga|susah gak|susah nggak|gampang ga|gampang gak|gampang nggak'
            r'|berat ga|berat gak|menyulitkan|challenging|susah banget|gampang banget'
            r'|gimana tingkat|seberapa susah|seberapa sulit|seberapa gampang|susahnya'
            r'|gampangnya|mudahnya|susah sih|gampang sih|lumayan susah|lumayan gampang'
            r'|worth it ga|worth it gak|bagus ga|bagus gak)\b', t):
            return "DIFFICULTY"

        if re.search(
            r'\b(rekomen|rekomendasi|saran|suggest|pilihkan|mana yang bagus|apa yang bagus'
            r'|matkul apa yang|enaknya ambil|sebaiknya ambil|sebaiknya pilih|saranin'
            r'|sarankan|kasih saran|mana yang cocok|yang cocok buat|yang bagus buat'
            r'|mana yang enak|mana yang ringan|mana yang asik|mana yang menarik'
            r'|cocok buat saya|yang pas buat|yang kira-kira|kira kira ambil apa'
            r'|ambil apa ya|pilih apa ya|enaknya apa|bagusnya ambil|bagusnya pilih'
            r'|saran dong|rekomendasiin|rekomendasikan|direkomendasikan|saranin dong)\b', t):
            return "RECOMMEND"

        if re.search(
            r'\b(total|jumlah|berapa sks|sks saya|sks aku|sks ku|kapasitas sks|sudah berapa'
            r'|sisa sks|sks tersisa|sks tinggal|tinggal berapa sks|masih bisa berapa sks'
            r'|sks yang diambil|total sks saya|sks yang sudah|sudah berapa sks'
            r'|cek sks|lihat sks|ngecek sks|kuota sks|sks nya berapa|sksnya berapa)\b', t):
            return "TOTAL_SKS"

        if re.search(
            r'\b(krs|daftar matkul|matkul saya|isi krs|krs ku|krs aku|lihat krs|cek krs'
            r'|krs gue|krs gw|krs-ku|review krs|ringkasan krs|matkul yang diambil'
            r'|matkul apa saja yang sudah|sudah ambil apa|udah ambil apa|yang udah diambil'
            r'|daftar yang sudah dipilih|pilihan saya|pilihan saya sekarang'
            r'|matkul dipilih|sudah pilih apa)\b', t):
            return "MY_KRS"

        if re.search(
            r'\b(menu|list|katalog|matkul apa|tersedia|daftar matkul|matkul apa saja'
            r'|ada matkul apa|mau lihat|lihat semua|tampilkan semua|show all'
            r'|matkul tersedia|semua matkul|ada apa aja|ada apa saja|apa saja yang ada'
            r'|pilihan matkul|daftar kuliah|kuliah apa saja|kuliah apa|matkul yang ada'
            r'|tampilkan matkul|lihat daftar|buka menu|show menu)\b', t):
            return "MENU"

        if re.search(
            r'\b(bantuan|help|panduan|cara pakai|petunjuk|tutorial|bingung|ga ngerti'
            r'|gak ngerti|tidak ngerti|nggak ngerti|gimana cara|cara nggunain'
            r'|cara menggunakan|cara pake|fitur apa|bisa apa|apa saja fitur'
            r'|tolong bantu|minta tolong|caranya gimana|cara kerja|cara gunakan'
            r'|gimana cara pake|tidak paham|belum paham|kurang paham)\b', t):
            return "HELP"

        if re.search(
            r'(kamu bisa apa|kamu ngapain|lo bisa apa|bisa bantu apa|fungsi kamu'
            r'|gunanya apa|apa yang bisa kamu lakukan|kamu bisa ngapain'
            r'|kamu bisa bantu apa|apa kemampuan kamu|kamu punya fitur apa)', t):
            return "HELP"

        if re.search(
            r'\b(wajib|harus|pilihan|opsional|elective|kategori|ini wajib|ini pilihan'
            r'|wajib ga|wajib gak|harus ga|harus gak|boleh ga diambil|boleh skip'
            r'|matkul wajib|matkul pilihan|mana yang wajib|mana yang pilihan'
            r'|yang harus diambil|yang boleh dilewati)\b', t):
            return "CATEGORY"

        if re.search(
            r'(berapa sks|sks-nya berapa|sksnya berapa|bobot sks|nilai sks'
            r'|kredit berapa|berapakah sks)', t):
            return "SKS_MATKUL"

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
                return False, (
                    f"🔒 Tidak bisa tambahkan **{key.replace('_',' ').title()}** — "
                    f"prasyarat **{pre_name}** belum ada di KRS kamu.\n\n"
                    f"Ambil dulu matkul prasyaratnya ya!"
                )
        for c in self.cart:
            if c["jadwal"] == data["jadwal"]:
                return False, (
                    f"⏰ Waduh, konflik jadwal! **{key.replace('_',' ').title()}** "
                    f"bentrok dengan **{c['course_key'].replace('_',' ').title()}** "
                    f"di jadwal {data['jadwal']}.\n\nCoba cek jadwal dulu ya!"
                )
        if self.total_sks() + data["sks"] > self.nlp.MAX_SKS:
            return False, (
                f"📊 Tidak bisa tambah! Total SKS kamu akan jadi "
                f"{self.total_sks() + data['sks']} SKS, melebihi batas {self.nlp.MAX_SKS} SKS."
            )
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
            self._notify(f"🗑️ Dihapus: {key.replace('_',' ').title()}")
            return f"🗑️ **{key.replace('_',' ').title()}** berhasil dihapus dari KRS."
        return f"⚠️ **{key.replace('_',' ').title()}** tidak ada di KRS kamu."

    # ════════════════════════════════════════════════════════════════
    # FITUR: add_all_semester
    # Menambahkan semua matkul dari semester X ke KRS sekaligus.
    # Melaporkan mana yang berhasil, duplikat, gagal prereq,
    # gagal jadwal, dan gagal karena SKS penuh.
    # ════════════════════════════════════════════════════════════════
    def add_all_semester(self, semester: int) -> str:
        matkul_semester = [
            (k, v) for k, v in self.nlp.course_data.items()
            if v["semester"] == semester
        ]

        if not matkul_semester:
            return f"❌ Tidak ada mata kuliah untuk semester {semester}."

        berhasil      = []
        gagal_duplikat = []
        gagal_prereq   = []
        gagal_konflik  = []
        gagal_sks      = []

        for key, data in matkul_semester:
            # Sudah ada di KRS
            if any(c["course_key"] == key for c in self.cart):
                gagal_duplikat.append(key)
                continue

            # Cek prasyarat yang belum terpenuhi
            prereq_kurang = [
                p for p in data["prereq"]
                if not any(c["course_key"] == p for c in self.cart)
            ]
            if prereq_kurang:
                gagal_prereq.append((key, prereq_kurang))
                continue

            # Cek konflik jadwal dengan matkul yang sudah ada di KRS
            konflik_dengan = next(
                (c["course_key"] for c in self.cart if c["jadwal"] == data["jadwal"]),
                None
            )
            if konflik_dengan:
                gagal_konflik.append((key, konflik_dengan, data["jadwal"]))
                continue

            # Cek kapasitas SKS
            if self.total_sks() + data["sks"] > self.nlp.MAX_SKS:
                gagal_sks.append((key, data["sks"]))
                continue

            # Semua validasi lolos — tambahkan ke cart
            self.cart.append({
                "course_key": key, "sks": data["sks"],
                "jadwal": data["jadwal"], "ruang": data["ruang"],
                "dosen": data["dosen"], "emoji": data["emoji"],
            })
            self._notify(f"➕ Ditambahkan: {key.replace('_',' ').title()} ({data['sks']} SKS)")
            berhasil.append((key, data))

        # ── Susun laporan hasil ──────────────────────────────────────
        lines = [f"📚 **Hasil tambah semua matkul Semester {semester}:**\n"]

        if berhasil:
            lines.append(f"✅ **Berhasil ditambahkan ({len(berhasil)} matkul):**")
            for key, data in berhasil:
                lines.append(
                    f"  {data['emoji']} {key.replace('_',' ').title()} "
                    f"({data['sks']} SKS) — 📅 {data['jadwal']}"
                )
            lines.append("")

        if gagal_duplikat:
            lines.append(f"⚠️ **Sudah ada di KRS ({len(gagal_duplikat)} matkul):**")
            for key in gagal_duplikat:
                d = self.nlp.course_data[key]
                lines.append(f"  {d['emoji']} {key.replace('_',' ').title()}")
            lines.append("")

        if gagal_prereq:
            lines.append(f"🔒 **Prasyarat belum terpenuhi ({len(gagal_prereq)} matkul):**")
            for key, prereqs in gagal_prereq:
                d = self.nlp.course_data[key]
                pre_names = ", ".join(p.replace("_", " ").title() for p in prereqs)
                lines.append(
                    f"  {d['emoji']} {key.replace('_',' ').title()} — butuh: {pre_names}"
                )
            lines.append("")

        if gagal_konflik:
            lines.append(f"⏰ **Konflik jadwal ({len(gagal_konflik)} matkul):**")
            for key, bentrok, jadwal in gagal_konflik:
                d = self.nlp.course_data[key]
                lines.append(
                    f"  {d['emoji']} {key.replace('_',' ').title()} "
                    f"bentrok dengan {bentrok.replace('_',' ').title()} ({jadwal})"
                )
            lines.append("")

        if gagal_sks:
            lines.append(f"📊 **SKS penuh — tidak bisa masuk ({len(gagal_sks)} matkul):**")
            for key, sks in gagal_sks:
                d = self.nlp.course_data[key]
                lines.append(f"  {d['emoji']} {key.replace('_',' ').title()} ({sks} SKS)")
            lines.append("")

        if not berhasil and not gagal_duplikat and not gagal_prereq and not gagal_konflik and not gagal_sks:
            lines.append("😕 Tidak ada matkul yang diproses.")
        
        lines.append(
            f"📊 **Total SKS sekarang: {self.total_sks()}/{self.nlp.MAX_SKS} SKS**\n\n"
            f"Ketik `krs saya` untuk melihat seluruh isi KRS, "
            f"atau `submit krs` kalau sudah siap!"
        )

        return "\n".join(lines)

    def step(self, user_input: str = ""):
        if not user_input:
            self._resp = self._greeting()
            self.state = State.BROWSING
            return

        intent = self.nlp.parse_intent(user_input)
        course = self.nlp.identify_course(user_input)

        # ── State: DONE ──
        if self.state == State.DONE:
            if re.search(r'\b(reset|mulai ulang|baru|lagi|ulang)\b', user_input.lower()):
                self.cart = []
                self.notifications = []
                self.state = State.BROWSING
                self._resp = "🔄 KRS direset. Silakan susun ulang dari awal!"
            else:
                self._resp = "✅ KRS sudah disubmit. Ketik **reset** untuk mulai ulang."
            return

        # ── State: CONFIRM ──
        if self.state == State.CONFIRM:
            if re.search(
                r'\b(ya|iya|yes|ok|oke|setuju|konfirmasi|lanjut|bener|betul|yep|yoi'
                r'|yup|siap|gas|lanjutkan|benar|fix|deal)\b', user_input.lower()):
                self.state = State.DONE
                self._notify("✅ KRS berhasil disubmit!")
                self._resp = self._done_msg()
            elif re.search(
                r'\b(tidak|batal|no|cancel|belum|nggak|engga|ga|gak|jangan'
                r'|enggak|kagak|nope|batalin|mundur|urungkan)\b', user_input.lower()):
                self.state = State.BROWSING
                self._resp = "↩️ Submit dibatalkan. KRS masih bisa diubah sesuka hati!"
            else:
                self._resp = "❓ Ketik **ya** untuk konfirmasi submit atau **tidak** untuk batal."
            return

        # ══════════════════════════════════════════════════════════════
        # ROUTING INTENT
        # ══════════════════════════════════════════════════════════════

        if intent == "GREET":
            self._resp = self._greet_casual(user_input)

        elif intent == "IDENTITY":
            self._resp = self._identity_msg()

        elif intent == "THANKS":
            self._resp = random.choice([
                "😊 Sama-sama! Kalau ada yang mau ditanyain lagi, bilang aja ya!",
                "🙌 Santai bro! Semoga KRS-nya beres dan semesternya lancar!",
                "😄 No problem! Kalau butuh bantuan lagi, SIKRS siap membantu kapan aja!",
                "👍 Senang bisa bantu! Semangat kuliah semester ini ya!",
                "🤝 Sip sip! Kalau ada pertanyaan lagi langsung tanya aja, nggak usah sungkan!",
            ])

        # ── FITUR: Add All Semester ─────────────────────────────
        elif intent == "ADD_ALL_SEMESTER":
            sem = self.nlp.identify_semester(user_input)
            if sem:
                if sem < 1 or sem > 8:
                    self._resp = "❌ Semester yang tersedia hanya 1 sampai 8."
                else:
                    self._resp = self.add_all_semester(sem)
            else:
                self._resp = (
                    "📚 Mau ambil semua matkul semester berapa?\n\n"
                    "Contoh perintah:\n"
                    "- `ambil semua matkul semester 1`\n"
                    "- `semua matkul semester 3`\n"
                    "- `tambah semua matkul semester 5`\n\n"
                    "Tersedia semester 1 sampai 8."
                )

        # ── FITUR: List Matkul Semester ─────────────────────────
        elif intent == "LIST_MATKUL_SEMESTER":
            sem = self.nlp.identify_semester(user_input)
            if sem:
                if sem < 1 or sem > 8:
                    self._resp = "❌ Semester yang tersedia hanya 1 sampai 8."
                else:
                    self._resp = self._list_matkul_semester(sem)
            else:
                self._resp = (
                    "📚 Mau lihat matkul semester berapa?\n\n"
                    "Contoh: `matkul semester 3 apa saja` atau `mata kuliah semester 5 apa aja`"
                )

        elif intent == "DOSEN_NGAJAR_APA":
            self._resp = self._dosen_ngajar_apa(user_input)

        elif intent == "EASY_MATKUL":
            self._resp = self._easy_matkul(user_input)

        elif intent == "REKOMEN_GAMPANG":
            self._resp = self._rekomen_gampang(user_input)

        elif intent == "ADD":
            if course:
                _, msg = self.add_course(course)
                self._resp = msg
            else:
                self._resp = (
                    "🤔 Mau ambil matkul apa nih? Sebutin nama atau singkatannya dong, contoh:\n\n"
                    "- `ambil matdis`\n"
                    "- `tambah pemweb`\n"
                    "- `mau ambil strukdat`\n"
                    "- `pengen ikut iot`\n\n"
                    "Atau ketik **menu** dulu buat lihat semua pilihan matkul yang tersedia!\n\n"
                    "💡 Mau ambil semua sekaligus? Ketik `ambil semua matkul semester 1`"
                )

        elif intent == "REMOVE":
            if re.search(r'\b(semua|all|hapus semua|clear|semuanya)\b', user_input.lower()):
                self.cart = []
                self._resp = "🗑️ Semua mata kuliah berhasil dihapus dari KRS."
            elif course:
                self._resp = self.remove_course(course)
            else:
                self._resp = (
                    "🤔 Mau hapus matkul yang mana? Sebutin nama atau singkatannya ya, contoh:\n\n"
                    "- `hapus matdis`\n"
                    "- `drop pemweb`\n"
                    "- `batalkan iot`\n\n"
                    "Atau ketik `hapus semua` kalau mau kosongkan semua sekaligus."
                )

        elif intent == "CLEAR":
            self.cart = []
            self._resp = (
                "🗑️ KRS berhasil dikosongkan! Semua matkul sudah dihapus.\n\n"
                "Mau susun ulang dari awal? Ketik **menu** buat lihat pilihan matkul!"
            )

        elif intent == "INFO":
            if course:
                self._resp = self._info_msg(course)
            else:
                self._resp = (
                    "🔍 Mau info matkul apa? Sebutin nama atau singkatannya dong, contoh:\n\n"
                    "- `info matdis`\n"
                    "- `jelaskan pemweb`\n"
                    "- `apa itu iot`\n"
                    "- `ceritain tentang jarkom`"
                )

        elif intent == "SCHEDULE":
            if course:
                d = self.nlp.course_data.get(course, {})
                self._resp = (
                    f"📅 **Jadwal {course.replace('_',' ').title()}:**\n\n"
                    f"- 🕐 Waktu: **{d.get('jadwal','?')}**\n"
                    f"- 📍 Ruangan: **{d.get('ruang','?')}**\n"
                    f"- 👨‍🏫 Dosen: **{d.get('dosen','?')}**"
                )
            else:
                self._resp = self._my_schedule()

        elif intent == "TIPS":
            if course:
                d = self.nlp.course_data.get(course, {})
                self._resp = (
                    f"💡 **Tips belajar {course.replace('_',' ').title()}:**\n\n"
                    f"{d.get('tips','Rajin belajar dan jangan lupa istirahat!')} 💪\n\n"
                    f"Semangat! Kalau ada yang kurang jelas, tanya dosen atau teman ya!"
                )
            else:
                tip = random.choice(ACADEMIC_FACTS)
                self._resp = (
                    f"💡 **Tips belajar umum:**\n\n{tip}\n\n"
                    f"Mau tips spesifik untuk matkul tertentu? Sebutin nama matkul-nya!\n"
                    f"Contoh: `tips belajar matdis` atau `cara belajar kalkulus`"
                )

        elif intent == "DOSEN":
            if course:
                d = self.nlp.course_data.get(course, {})
                self._resp = (
                    f"👨‍🏫 **Dosen {course.replace('_',' ').title()}:**\n\n"
                    f"- Nama: **{d.get('dosen','?')}**\n"
                    f"- Jadwal Kelas: **{d.get('jadwal','?')}**\n"
                    f"- Ruangan: **{d.get('ruang','?')}**"
                )
            else:
                dosen_key, matkul_list = self.nlp.identify_dosen(user_input)
                if dosen_key and matkul_list:
                    self._resp = self._dosen_ngajar_apa_by_key(dosen_key, matkul_list)
                else:
                    self._resp = (
                        "🤔 Mau tanya dosen matkul apa? Sebutin nama matkul-nya dong, contoh:\n\n"
                        "- `dosen matdis`\n"
                        "- `siapa yang ngajar pemweb`\n"
                        "- `dosennya siapa jarkom`\n"
                        "- `pak siapa yang ngajar iot`\n\n"
                        "Atau kalau mau tahu pak/bu dosen ngajar matkul apa:\n"
                        "- `pak bambang ngajar apa`\n"
                        "- `bu noora dosen matkul apa`"
                    )

        elif intent == "PREREQ":
            if course:
                self._resp = self._prereq_msg(course)
            else:
                self._resp = (
                    "🔒 Mau cek prasyarat matkul apa? Sebutin nama matkul-nya, contoh:\n\n"
                    "- `prasyarat jarkom`\n"
                    "- `syarat ambil matdis`\n"
                    "- `bisa langsung ambil iot?`\n"
                    "- `harus lulus apa dulu sebelum ambil basdat`"
                )

        elif intent == "DIFFICULTY":
            if course:
                d = self.nlp.course_data.get(course, {})
                diff = d.get("difficulty", 3)
                stars = "⭐" * diff + "☆" * (5 - diff)
                label = {
                    1: "Sangat Mudah 😄 — cocok buat santai-santai",
                    2: "Mudah 🙂 — masih oke, asal rajin",
                    3: "Sedang 😐 — butuh usaha yang cukup",
                    4: "Sulit 😅 — perlu belajar ekstra",
                    5: "Sangat Sulit 😰 — butuh dedikasi penuh!"
                }.get(diff, "Sedang")
                self._resp = (
                    f"🎯 **Tingkat kesulitan {course.replace('_',' ').title()}:**\n\n"
                    f"{stars} ({diff}/5) — {label}\n\n"
                    f"💡 *Tips: {d.get('tips','')}*"
                )
            else:
                self._resp = (
                    "🎯 Mau tahu tingkat kesulitan matkul apa? Contoh:\n\n"
                    "- `susah ga matdis?`\n"
                    "- `tingkat kesulitan kalkulus`\n"
                    "- `pemweb gampang ga?`\n"
                    "- `seberapa berat iot?`"
                )

        elif intent == "RECOMMEND":
            self._resp = self._recommend()

        elif intent == "SUBMIT":
            if not self.cart:
                self._resp = (
                    "📭 KRS masih kosong nih! Tambahkan dulu beberapa matkul baru bisa di-submit.\n\n"
                    "Ketik **menu** buat lihat daftar matkul yang tersedia!"
                )
            else:
                self.state = State.CONFIRM
                self._resp = self._confirm_msg()

        elif intent == "TOTAL_SKS":
            sks_now = self.total_sks()
            pct = int(sks_now / self.nlp.MAX_SKS * 100) if self.nlp.MAX_SKS else 0
            status = (
                "🔴 Hampir penuh!" if pct >= 90
                else "🟡 Mendekati batas" if pct >= 70
                else "🟢 Masih aman"
            )
            self._resp = (
                f"📊 **Status SKS Kamu:**\n\n"
                f"- Diambil: **{sks_now} SKS**\n"
                f"- Maksimum: **{self.nlp.MAX_SKS} SKS**\n"
                f"- Sisa: **{self.nlp.MAX_SKS - sks_now} SKS** lagi\n"
                f"- Terisi: **{pct}%** — {status}"
            )

        elif intent == "MY_KRS":
            self._resp = self._my_krs()

        elif intent == "MENU":
            self._resp = self._menu_msg()

        elif intent == "HELP":
            self._resp = self._help_msg()

        elif intent == "CATEGORY":
            if course:
                d = self.nlp.course_data.get(course, {})
                kat = d.get("kategori", "?")
                emoji = "⚠️" if kat == "Wajib" else "🎯"
                self._resp = (
                    f"{emoji} **{course.replace('_',' ').title()}** adalah matkul **{kat}**.\n\n"
                    + (
                        "Matkul ini harus diambil dan tidak bisa dilewati."
                        if kat == "Wajib"
                        else "Matkul ini bersifat pilihan, bisa diambil atau dilewati sesuai kebutuhan."
                    )
                )
            else:
                wajib = [k for k, v in self.nlp.course_data.items() if v["kategori"] == "Wajib"]
                pilihan = [k for k, v in self.nlp.course_data.items() if v["kategori"] == "Pilihan"]
                self._resp = (
                    f"📋 **Kategori Mata Kuliah:**\n\n"
                    f"- ⚠️ **Wajib:** {len(wajib)} matkul — harus diambil semua\n"
                    f"- 🎯 **Pilihan:** {len(pilihan)} matkul — bebas dipilih sesuai minat\n\n"
                    f"Ketik **menu** untuk lihat daftar lengkap beserta kategorinya!"
                )

        elif intent == "SKS_MATKUL":
            if course:
                d = self.nlp.course_data.get(course, {})
                self._resp = (
                    f"📊 **{course.replace('_',' ').title()}** memiliki **{d.get('sks','?')} SKS**.\n\n"
                    f"- Semester: {d.get('semester','?')}\n"
                    f"- Kategori: {d.get('kategori','?')}"
                )
            else:
                self._resp = self._total_sks_msg()

        else:
            if course:
                self._resp = self._info_msg(course)
            else:
                self._resp = self._unknown_response(user_input)

    # ══════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════

    def _dosen_ngajar_apa(self, user_input: str) -> str:
        dosen_key, matkul_list = self.nlp.identify_dosen(user_input)
        if not dosen_key or not matkul_list:
            return (
                "🤔 Hmm, saya kurang nangkep nama dosennya. Coba sebutin lebih jelas, contoh:\n\n"
                "- `pak bambang ngajar apa`\n"
                "- `bu noora dosen matkul apa`\n"
                "- `pak agung ngampu apa aja`\n"
                "- `pak ramadhan mengajar apa`\n\n"
                "Nama dosen yang tersedia: Bambang, Agung, Nugroho, Noora, Ramadhan, "
                "Rizky, Aris, Setyoningsih, Khoiriya, Saeful, Febrian, Mega, dll."
            )
        return self._dosen_ngajar_apa_by_key(dosen_key, matkul_list)

    def _dosen_ngajar_apa_by_key(self, dosen_key: str, matkul_list: list) -> str:
        first_data = self.nlp.course_data.get(matkul_list[0], {})
        nama_display = first_data.get("dosen", dosen_key.title())
        lines = [f"👨‍🏫 **{nama_display}** mengampu matkul berikut:\n"]
        for mk in matkul_list:
            d = self.nlp.course_data.get(mk, {})
            if d:
                nama_mk = mk.replace("_", " ").title()
                lines.append(
                    f"- {d['emoji']} **{nama_mk}** (Semester {d['semester']} · {d['sks']} SKS)\n"
                    f"  📅 {d['jadwal']} · 📍 {d['ruang']}"
                )
        lines.append(
            f"\nTotal: **{len(matkul_list)} mata kuliah** yang diampu.\n\n"
            f"Mau info lebih detail salah satu matkul di atas? "
            f"Ketik `info [nama matkul]` ya! 😊"
        )
        return "\n".join(lines)

    # ════════════════════════════════════════════════════════════════
    # FITUR: list_matkul_semester
    # Menampilkan seluruh mata kuliah pada satu semester tertentu.
    # ════════════════════════════════════════════════════════════════
    def _list_matkul_semester(self, semester: int) -> str:
        matkul = [(k, v) for k, v in self.nlp.course_data.items() if v["semester"] == semester]
        if not matkul:
            return f"❌ Tidak ada mata kuliah untuk semester {semester}."
        total_sks = sum(v["sks"] for _, v in matkul)
        lines = [f"📚 **Mata Kuliah Semester {semester}** (total {total_sks} SKS):\n"]
        for k, v in matkul:
            in_krs = "✅" if any(c["course_key"] == k for c in self.cart) else "◻️"
            lines.append(
                f"{in_krs} {v['emoji']} **{k.replace('_',' ').title()}** "
                f"({v['sks']} SKS · {v['kategori']})\n"
                f"   🕐 {v['jadwal']} · 📍 {v['ruang']} · 👨‍🏫 {v['dosen']}"
            )
        lines.append(
            f"\nKetik `ambil [nama matkul]` untuk tambah satu-satu, "
            f"atau `ambil semua matkul semester {semester}` untuk ambil sekaligus!"
        )
        return "\n".join(lines)

    def _easy_matkul(self, user_input: str) -> str:
        sem = self.nlp.identify_semester(user_input)
        if sem:
            matkul_sem = [(k, v) for k, v in self.nlp.course_data.items() if v["semester"] == sem]
            if not matkul_sem:
                return f"😕 Tidak ada data matkul untuk semester {sem}."
            matkul_sem.sort(key=lambda x: x[1]["difficulty"])
            lines = [f"😊 **Matkul Semester {sem} dari yang paling gampang:**\n"]
            for k, v in matkul_sem:
                diff = v["difficulty"]
                stars = "⭐" * diff + "☆" * (5 - diff)
                label = {1:"Santai banget",2:"Gampang",3:"Sedang",4:"Lumayan susah",5:"Berat banget"}.get(diff,"?")
                lines.append(
                    f"- {v['emoji']} **{k.replace('_',' ').title()}** — {stars} *({label})*\n"
                    f"  {v['sks']} SKS · 👨‍🏫 {v['dosen']}"
                )
            easiest = [(k,v) for k,v in matkul_sem if v["difficulty"] <= 2]
            if easiest:
                nama_easy = ", ".join(k.replace("_"," ").title() for k,v in easiest[:2])
                lines.append(f"\n💡 Yang paling santai di semester {sem}: **{nama_easy}**!")
            lines.append(f"Ketik `ambil [nama matkul]` buat langsung masukin ke KRS!")
            lines.append(f"\n💡 Atau ambil semua sekaligus: `ambil semua matkul semester {sem}`")
            return "\n".join(lines)
        else:
            lines = ["😊 **Matkul paling gampang tiap semester:**\n"]
            by_sem = {}
            for k, v in self.nlp.course_data.items():
                by_sem.setdefault(v["semester"], []).append((k, v))
            found_any = False
            for sem_num in sorted(by_sem.keys()):
                easy = [(k,v) for k,v in by_sem[sem_num] if v["difficulty"] <= 2]
                easy.sort(key=lambda x: x[1]["difficulty"])
                if easy:
                    found_any = True
                    lines.append(f"**Semester {sem_num}:**")
                    for k, v in easy[:3]:
                        diff = v["difficulty"]
                        stars = "⭐" * diff + "☆" * (5 - diff)
                        lines.append(f"  {v['emoji']} {k.replace('_',' ').title()} — {stars} ({v['sks']} SKS)")
            if not found_any:
                lines.append("Wah, semua matkul lumayan menantang nih! 😅")
            lines.append("\n💡 Mau filter per semester? Ketik misalnya `matkul gampang semester 2`")
            return "\n".join(lines)

    def _rekomen_gampang(self, user_input: str) -> str:
        sem = self.nlp.identify_semester(user_input)
        taken = {c["course_key"] for c in self.cart}
        taken_jadwal = {c["jadwal"] for c in self.cart}
        if sem:
            candidates = [
                (k, v) for k, v in self.nlp.course_data.items()
                if v["semester"] == sem and k not in taken
                and v["jadwal"] not in taken_jadwal
                and self.total_sks() + v["sks"] <= self.nlp.MAX_SKS
                and all(p in taken for p in v["prereq"])
            ]
            if not candidates:
                return (
                    f"😅 Hmm, tidak ada matkul semester {sem} yang bisa direkomendasikan sekarang.\n\n"
                    f"Kemungkinan:\n- SKS sudah penuh\n- Jadwal bentrok\n- Prasyarat belum terpenuhi\n\n"
                    f"Cek dulu KRS kamu dengan ketik `krs saya`!"
                )
            candidates.sort(key=lambda x: x[1]["difficulty"])
            lines = [f"🎯 **Rekomen matkul gampang semester {sem} buat kamu:**\n"]
            for k, v in candidates[:5]:
                diff = v["difficulty"]
                stars = "⭐" * diff + "☆" * (5 - diff)
                label = {1:"Santai banget 😄",2:"Gampang 🙂",3:"Sedang 😐",4:"Lumayan susah 😅",5:"Berat 😰"}.get(diff,"?")
                lines.append(
                    f"- {v['emoji']} **{k.replace('_',' ').title()}** — {stars} {label}\n"
                    f"  {v['sks']} SKS · 📅 {v['jadwal']} · 👨‍🏫 {v['dosen']}"
                )
            easiest_name = candidates[0][0].replace("_"," ").title()
            lines.append(
                f"\n✨ Paling santai: **{easiest_name}**!\n"
                f"Ketik `ambil {candidates[0][0].replace('_',' ')}` buat masukin ke KRS."
            )
            return "\n".join(lines)
        else:
            candidates = [
                (k, v) for k, v in self.nlp.course_data.items()
                if k not in taken and v["jadwal"] not in taken_jadwal
                and self.total_sks() + v["sks"] <= self.nlp.MAX_SKS
                and all(p in taken for p in v["prereq"]) and v["difficulty"] <= 2
            ]
            if not candidates:
                candidates = [
                    (k, v) for k, v in self.nlp.course_data.items()
                    if k not in taken and v["jadwal"] not in taken_jadwal
                    and self.total_sks() + v["sks"] <= self.nlp.MAX_SKS
                    and all(p in taken for p in v["prereq"])
                ]
            if not candidates:
                return "😅 Tidak ada matkul yang bisa direkomendasikan saat ini.\n\nCek dulu KRS kamu: `krs saya`"
            candidates.sort(key=lambda x: x[1]["difficulty"])
            lines = ["🎯 **Rekomen matkul paling gampang yang bisa kamu ambil sekarang:**\n"]
            for k, v in candidates[:5]:
                diff = v["difficulty"]
                stars = "⭐" * diff + "☆" * (5 - diff)
                label = {1:"Santai banget 😄",2:"Gampang 🙂",3:"Sedang 😐",4:"Lumayan susah 😅",5:"Berat 😰"}.get(diff,"?")
                lines.append(
                    f"- {v['emoji']} **{k.replace('_',' ').title()}** (Sem {v['semester']}) — {stars} {label}\n"
                    f"  {v['sks']} SKS · 📅 {v['jadwal']} · 👨‍🏫 {v['dosen']}"
                )
            lines.append(f"\n💡 Mau spesifik per semester? Ketik: `rekomen matkul gampang semester 3`")
            return "\n".join(lines)

    def _greet_casual(self, text: str) -> str:
        t = text.lower()
        if "pagi" in t:    salam = "Selamat pagi"
        elif "siang" in t: salam = "Selamat siang"
        elif "sore" in t:  salam = "Selamat sore"
        elif "malam" in t: salam = "Selamat malam"
        else:              salam = random.choice(["Halo", "Hai", "Hey"])
        return (
            f"👋 {salam}! Saya **SIKRS**, asisten KRS UPGRIS yang siap bantu kamu!\n\n"
            "Mau ngapain nih? Beberapa hal yang bisa saya bantu:\n\n"
            "- 📚 Lihat daftar matkul → ketik **menu**\n"
            "- ➕ Tambah matkul ke KRS → ketik **ambil [nama matkul]**\n"
            "- 📦 Ambil semua matkul satu semester → ketik **ambil semua matkul semester 1**\n"
            "- 📖 Lihat matkul satu semester → ketik **matkul semester 2 apa saja**\n"
            "- 🎯 Minta rekomendasi matkul → ketik **rekomen**\n"
            "- 😊 Cari matkul yang gampang → ketik **matkul gampang semester 2**\n"
            "- 👨‍🏫 Tanya ngajar apa → ketik **pak bambang ngajar apa**\n"
            "- 📅 Cek jadwal → ketik **jadwal**\n"
            "- 💡 Tips belajar → ketik **tips [nama matkul]**\n"
            "- ❓ Lihat semua fitur → ketik **bantuan**\n\n"
            "Langsung aja tanya atau ketik perintah ya! 😊"
        )

    def _identity_msg(self) -> str:
        return (
            "🤖 Saya **SIKRS** — Sistem Informasi Kartu Rencana Studi!\n\n"
            "Saya adalah chatbot akademik berbasis **Finite State Machine** yang dibuat "
            "untuk membantu mahasiswa **Teknik Informatika UPGRIS** menyusun KRS dengan mudah.\n\n"
            "Yang bisa saya lakukan:\n"
            "- ➕ Tambah/hapus matkul ke KRS\n"
            "- 📦 Ambil semua matkul satu semester sekaligus ✨\n"
            "- 📖 Lihat seluruh matkul satu semester ✨\n"
            "- ⚠️ Validasi prasyarat & konflik jadwal otomatis\n"
            "- 🎯 Rekomendasikan matkul berdasarkan KRS aktif\n"
            "- 😊 Cari matkul gampang per semester\n"
            "- 👨‍🏫 Info dosen ngajar matkul apa\n"
            "- 📅 Tampilkan jadwal kuliah\n"
            "- 💡 Kasih tips belajar per matkul\n"
            "- 🔒 Cek prasyarat matkul\n\n"
            "Ketik **bantuan** untuk panduan lengkap atau **menu** untuk lihat semua matkul!"
        )

    def _unknown_response(self, text: str) -> str:
        return random.choice([
            (
                "🤔 Hmm, saya kurang nangkep maksudnya nih. Coba pakai salah satu perintah ini:\n\n"
                "- `menu` → lihat semua matkul\n"
                "- `ambil [matkul]` → tambah ke KRS\n"
                "- `ambil semua matkul semester 1` → ambil semua sekaligus ✨\n"
                "- `matkul semester 2 apa saja` → lihat isi satu semester ✨\n"
                "- `info [matkul]` → detail matkul\n"
                "- `pak bambang ngajar apa` → info dosen\n"
                "- `matkul gampang semester 2` → cari yang ringan\n"
                "- `rekomen` → rekomendasi matkul\n"
                "- `bantuan` → panduan lengkap"
            ),
            (
                "😅 Waduh, saya belum ngerti yang itu. Mungkin maksudnya:\n\n"
                "- Mau **tambah matkul**? Ketik `ambil [nama matkul]`\n"
                "- Mau **ambil semua satu semester**? Ketik `ambil semua matkul semester 2` ✨\n"
                "- Mau **lihat isi satu semester**? Ketik `mata kuliah semester 4 apa saja` ✨\n"
                "- Mau **lihat jadwal**? Ketik `jadwal`\n"
                "- Mau **info matkul**? Ketik `info [nama matkul]`\n"
                "- Mau **tahu dosen ngajar apa**? Ketik `pak bambang ngajar apa`\n"
                "- Mau **cari matkul gampang**? Ketik `matkul gampang semester 3`\n"
                "- Butuh **bantuan**? Ketik `bantuan`"
            ),
            (
                "🙈 Hmm, saya kurang paham nih. Tapi gapapa, coba ketik salah satu ini:\n\n"
                "- `menu` → lihat daftar matkul\n"
                "- `ambil semua matkul semester 1` → otomatis tambah semua ✨\n"
                "- `matkul semester 5 apa saja` → lihat isi semester tertentu ✨\n"
                "- `rekomen` → minta rekomendasi\n"
                "- `krs saya` → cek KRS sekarang\n"
                "- `bantuan` → lihat semua yang bisa saya lakukan"
            ),
        ])

    def _total_sks_msg(self) -> str:
        sks_now = self.total_sks()
        pct = int(sks_now / self.nlp.MAX_SKS * 100) if self.nlp.MAX_SKS else 0
        return (
            f"📊 **Status SKS Kamu:**\n\n"
            f"- Diambil: **{sks_now} SKS**\n"
            f"- Maksimum: **{self.nlp.MAX_SKS} SKS**\n"
            f"- Sisa: **{self.nlp.MAX_SKS - sks_now} SKS**\n"
            f"- Terisi: **{pct}%**"
        )

    def _greeting(self):
        return (
            "**Selamat datang di SIKRS UPGRIS!**\n\n"
            "Saya akan membantu kamu menyusun Kartu Rencana Studi Semester Genap 2025/2026.\n\n"
            "**Apa yang bisa saya lakukan?**\n"
            "- 📚 Tampilkan daftar mata kuliah\n"
            "- ➕ Tambah/hapus matkul ke KRS\n"
            "- 📦 Ambil semua matkul satu semester sekaligus ✨\n"
            "- 📖 Lihat seluruh matkul satu semester ✨\n"
            "- ⚠️ Validasi prasyarat & konflik jadwal\n"
            "- 🎯 Rekomendasikan matkul\n"
            "- 😊 Cari matkul gampang per semester\n"
            "- 👨‍🏫 Info dosen ngajar matkul apa\n"
            "- 💡 Beri tips belajar per matkul\n\n"
            "Ketik **menu** untuk melihat semua mata kuliah, atau **bantuan** untuk panduan lengkap.\n\n"
            "💡 Cara cepat: ketik `ambil semua matkul semester 1` untuk langsung tambah semua matkul semester 1!"
        )

    def _menu_msg(self):
        lines = ["📚 **Daftar Mata Kuliah Tersedia:**\n"]
        by_sem = {}
        for k, v in self.nlp.course_data.items():
            by_sem.setdefault(v["semester"], []).append((k, v))
        for sem in sorted(by_sem):
            total_sks_sem = sum(v["sks"] for _, v in by_sem[sem])
            lines.append(f"\n**── Semester {sem} ──** *(total {total_sks_sem} SKS · ketik `ambil semua matkul semester {sem}` untuk ambil sekaligus)*")
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
            return (
                f"✅ **{key.replace('_',' ').title()}** tidak punya prasyarat. "
                f"Langsung bisa diambil tanpa syarat apapun!"
            )
        lines = [f"🔒 **Prasyarat {key.replace('_',' ').title()}:**\n"]
        for p in d["prereq"]:
            status = "✅ Sudah di KRS" if any(c["course_key"] == p for c in self.cart) else "❌ Belum diambil"
            lines.append(f"- **{p.replace('_',' ').title()}** → {status}")
        all_met = all(any(c["course_key"] == p for c in self.cart) for p in d["prereq"])
        if all_met:
            lines.append(f"\n✅ Semua prasyarat sudah terpenuhi! Kamu bisa langsung ambil matkul ini.")
        else:
            lines.append(f"\n⚠️ Ada prasyarat yang belum diambil. Ambil dulu matkul di atas ya!")
        return "\n".join(lines)

    def _recommend(self):
        taken = {c["course_key"] for c in self.cart}
        taken_jadwal = {c["jadwal"] for c in self.cart}
        recs = []
        for k, v in self.nlp.course_data.items():
            if k in taken: continue
            if self.total_sks() + v["sks"] > self.nlp.MAX_SKS: continue
            if v["jadwal"] in taken_jadwal: continue
            if all(p in taken for p in v["prereq"]):
                recs.append((k, v))
        if not recs:
            return (
                "🤔 Saat ini tidak ada rekomendasi yang tersedia.\n\n"
                "Kemungkinan penyebabnya:\n"
                "- SKS sudah penuh (maks 24 SKS)\n"
                "- Semua jadwal sudah bentrok\n"
                "- Prasyarat matkul lain belum terpenuhi\n\n"
                "Coba cek KRS kamu dulu dengan ketik `krs saya`!"
            )
        random.shuffle(recs)
        lines = ["🎯 **Rekomendasi Matkul untuk Kamu:**\n"]
        for k, v in recs[:5]:
            diff_label = {1:"Mudah",2:"Mudah",3:"Sedang",4:"Sulit",5:"Sangat Sulit"}.get(v["difficulty"],"?")
            lines.append(
                f"- {v['emoji']} **{k.replace('_',' ').title()}** ({v['sks']} SKS) — {diff_label}\n"
                f"  📅 {v['jadwal']} · 📍 {v['ruang']} · 👨‍🏫 {v['dosen']}"
            )
        lines.append(f"\nKetik `ambil [nama matkul]` untuk menambahkan ke KRS.")
        return "\n".join(lines)

    def _my_schedule(self):
        if not self.cart:
            return "📭 KRS masih kosong. Tambahkan matkul dulu baru bisa lihat jadwal!"
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
            return (
                "📭 KRS masih kosong nih!\n\n"
                "Tambahkan matkul dengan perintah `ambil [nama matkul]` ya!\n"
                "Atau ketik **menu** untuk lihat daftar matkul yang tersedia.\n\n"
                "💡 Cara cepat: ketik `ambil semua matkul semester 1` untuk tambah semua sekaligus!"
            )
        lines = [f"📋 **KRS Kamu ({self.total_sks()}/{self.nlp.MAX_SKS} SKS):**\n"]
        for c in self.cart:
            lines.append(
                f"- {c['emoji']} **{c['course_key'].replace('_',' ').title()}** "
                f"({c['sks']} SKS) — {c['jadwal']}"
            )
        sisa = self.nlp.MAX_SKS - self.total_sks()
        lines.append(f"\n💡 Sisa kapasitas: **{sisa} SKS** lagi.")
        if sisa == 0:
            lines.append("🔴 SKS sudah penuh! Siap untuk di-submit?")
        elif sisa <= 3:
            lines.append("🟡 Hampir penuh, tinggal sedikit lagi!")
        return "\n".join(lines)

    def _confirm_msg(self):
        lines = [f"📋 **Konfirmasi Submit KRS ({self.total_sks()} SKS):**\n"]
        for c in self.cart:
            lines.append(f"- {c['emoji']} {c['course_key'].replace('_',' ').title()} ({c['sks']} SKS)")
        lines.append(f"\n**Total: {self.total_sks()} SKS** dalam {len(self.cart)} mata kuliah.")
        lines.append("\nKetik **ya** untuk submit atau **tidak** untuk batal.")
        return "\n".join(lines)

    def _done_msg(self):
        return (
            "🎉 **KRS berhasil disubmit!**\n\n"
            f"Total: **{self.total_sks()} SKS** dalam **{len(self.cart)} mata kuliah**.\n\n"
            "Semangat belajar semester ini! Semoga nilainya bagus semua! 💪\n\n"
            "Ketik **reset** jika ingin mulai ulang."
        )

    def _help_msg(self):
        return (
            "❓ **Panduan Penggunaan SIKRS:**\n\n"
            "**📋 Mengelola KRS:**\n"
            "- `menu` → daftar semua matkul\n"
            "- `ambil [matkul]` → tambah ke KRS\n"
            "- `ambil semua matkul semester 1` → tambah SEMUA matkul semester 1 sekaligus ✨\n"
            "- `matkul semester 2 apa saja` → lihat seluruh matkul satu semester ✨\n"
            "- `hapus [matkul]` → hapus dari KRS\n"
            "- `hapus semua` → kosongkan KRS\n"
            "- `krs saya` → ringkasan KRS\n"
            "- `total sks` → cek kapasitas SKS\n"
            "- `submit KRS` → finalisasi dan kirim KRS\n\n"
            "**🔍 Informasi Matkul:**\n"
            "- `info [matkul]` → detail lengkap\n"
            "- `jadwal [matkul]` → jadwal & ruangan\n"
            "- `dosen [matkul]` → info dosen\n"
            "- `prasyarat [matkul]` → cek syarat\n"
            "- `tips [matkul]` → tips belajar\n"
            "- `rekomen` → rekomendasi matkul\n"
            "- `susah ga [matkul]` → cek kesulitan\n\n"
            "**👨‍🏫 Tanya Soal Dosen:**\n"
            "- `pak bambang ngajar apa` → dosen ngajar matkul apa\n"
            "- `bu noora dosen matkul apa` → daftar matkul dosen\n"
            "- `pak agung mengampu apa aja` → matkul yang diampu\n\n"
            "**😊 Cari Matkul Gampang:**\n"
            "- `matkul gampang semester 1` → matkul ringan semester tertentu\n"
            "- `rekomen matkul gampang semester 3` → rekomendasi yang santai\n"
            "- `yang paling mudah semester 4` → matkul termudah\n\n"
            "**💬 Contoh kalimat yang dimengerti:**\n"
            "- *'ambil semua matkul semester 1'* ✨\n"
            "- *'mata kuliah semester 3 apa saja'* ✨\n"
            "- *'matkul web itu susah ga?'*\n"
            "- *'pengen ambil iot'*\n"
            "- *'siapa yang ngajar matdis?'*\n"
            "- *'pak bambang herlambang dosen apa?'*\n"
            "- *'jarkom jadwalnya kapan?'*\n"
            "- *'semester 2 matkul yang gampang apa?'*\n"
            "- *'rekomenin matkul santai semester 4 dong'*\n"
            "- *'sisa sks aku berapa?'*\n\n"
        )