# LAPORAN AUDIT KEPATUHAN ETIKA PENELITIAN & PELINDUNGAN DATA PRIBADI (PDP)
## Kepatuhan Hukum, Batasan Etis Riset Forensik Digital, dan Prinsip Minimisasi Data
**Dasar Hukum**:
1. Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP).
2. General Data Protection Regulation (GDPR) Regulation (EU) 2016/679 (Article 6 & Article 9).
3. ACM Code of Ethics and Professional Conduct & IEEE Code of Ethics.

---

### 1. PRINSIP DASAR ETIKA RISET KASUS TOKOH PUBLIK
Penyelidikan forensik digital ini dirancang dengan prinsip **keterbukaan ilmiah tanpa intrusi privasi (*non-intrusive public fact-checking*)**:
- **Objek Penelitian**: Klaim viral di media massa dan media sosial, siaran video bajakan di YouTube, pergerakan harga saham di pasar modal, dan keterbukaan informasi bursa resmi (SEC EDGAR).
- **Subjek Tokoh Publik**: CEO korporasi terbuka (Jensen Huang) diperlakukan sebagai pimpinan entitas publik dengan kewajiban keterbukaan material (*fiduciary public figure*).
- **Atribusi Sebagai Korban**: Korporasi dan figur CEO secara eksplisit diposisikan sebagai **korban kejahatan siber (*impersonation & quishing target*)** dan **korban distorsi narasi publik**, bukan sebagai pelaku kejahatan.

---

### 2. KEPATUHAN TERHADAP UNDANG-UNDANG PDP NO. 27 TAHUN 2022 (INDONESIA)

| Prinsip UU PDP (Pasal 16 & 20) | Penerapan dalam Riset Ini | Status Kepatuhan |
| :--- | :--- | :---: |
| **Tujuan Spesifik & Sah** | Penelitian dilakukan murni untuk kepentingan pendidikan, sains, dan metodologi forensik digital penangkal disinformasi. | **PATUH PENUH** |
| **Prinsip Minimisasi Data** | Tidak menghimpun data privat non-relevan (alamat rumah, nomor rekening, percakapan telepon pribadi). | **PATUH PENUH** |
| **Data yang Terbuka untuk Umum** | Seluruh 11 artefak OSINT dan 300 berita diperoleh dari ranah publik yang sudah dipublikasikan secara terbuka oleh media massa atau badan registrasi resmi pemerintah (ACRA Singapura). | **PATUH PENUH** |
| **Keamanan & Integritas Kriptografis** | Seluruh data disimpan dan diverifikasi dengan enkripsi hash SHA-256 (ISO/IEC 27037) untuk mencegah manipulasi data sepihak. | **PATUH PENUH** |

---

### 3. KEPATUHAN TERHADAP GDPR (EROPA)
1. **Legitimate Interest (Article 6(1)(f))**: Riset forensik atas manipulasi deepfake dan verifikasi disinformasi publik memenuhi syarat kepentingan ilmiah publik yang sah (*academic research exception*).
2. **Ketiadaan Data Kategori Khusus (Article 9)**: Riset ini tidak memproses data biometrik privat untuk pengawasan massal, melainkan hanya menguji file video YouTube publik untuk membuktikan manipulasi deepfake tiruan.

---

### 4. BATASAN FORENSIK TEGAS: MENGAPA SPYWARE PEGASUS TIDAK DIPERGUNAKAN
- Riset ini **secara tegas menolak penggunaan software eksploitasi ofensif (spyware peretas ponsel)**.
- Repositori MVT (Mobile Verification Toolkit) yang disertakan dalam penelitian hanya memuat instrumen **deteksi defensif konsensual** dan pustaka indikator kompromi terbuka (*AmnestyTech STIX2 database*), yang digunakan untuk membuktikan bahwa ponsel subjek **bersih dari malware**.

---

### KESIMPULAN AUDITOR ETIKA
Penelitian ini memenuhi 100% kaidah etika penelitian akademis internasional dan regulasi pelindungan data pribadi. Repositori ini aman, sah secara hukum, dan layak untuk diseminasi akademis di tingkat nasional maupun internasional.
