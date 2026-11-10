# PRD & KERANGKA PENELITIAN FORENSIK TERPADU (VERSI 2.0)
## Cyber-Physical & Behavioral Digital Forensics: Investigasi Serangan Konvergen (Fisik dan Digital) Berbasis Rekayasa Sosial dan Deepfake

---

| Parameter Dokumen | Spesifikasi Teknis |
| :--- | :--- |
| **Kode Proyek** | `PRD-CPBF-HYBRID-02` |
| **Versi Dokumen** | `2.0 (Cyber-Physical Convergence Release)` |
| **Klasifikasi** | *Defensive Security, Physical Security & Digital Forensic Research* |
| **Fokus Utama** | *Konvergensi Serangan Fisik (On-site/Human), Digital (Deepfake/Network), dan Kognitif (Layer 8)* |
| **Standar Acuan** | CISA Converged Security, ASIS International, ISO/IEC 27037, NIST SP 800-86 |

---

## DAFTAR ISI (17 BAGIAN LENGKAP)
1. [Latar Belakang & Urgensi Konvergensi Siber-Fisik](#1-latar-belakang--urgensi-konvergensi-siber-fisik)
2. [Fakta Kasus & Dekonstruksi Serangan Hibrida (Fisik & Digital)](#2-fakta-kasus--dekonstruksi-serangan-hibrida-fisik--digital)
3. [Research Questions (RQ) & Hipotesis Penelitian](#3-research-questions-rq--hipotesis-penelitian)
4. [Ruang Lingkup & Batasan Masalah (Scope & Limitations)](#4-ruang-lingkup--batasan-masalah-scope--limitations)
5. [Model Rantai Serangan Hibrida (Cyber-Physical Attack Chain)](#5-model-rantai-serangan-hibrida-cyber-physical-attack-chain)
6. [Kerangka Keilmuan: Cyber-Physical & Behavioral Forensics](#6-kerangka-keilmuan-cyber-physical--behavioral-forensics)
7. [Metodologi Penelitian Tiga Fase Terpadu](#7-metodologi-penelitian-tiga-fase-terpadu)
8. [Arsitektur Sistem Investigasi & Mesin Korelasi Dual-Vektor](#8-arsitektur-sistem-investigasi--mesin-korelasi-dual-vektor)
9. [Etika Penelitian, Kepatuhan Hukum & Aturan Atribusi Ketat](#9-etika-penelitian-kepatuhan-hukum--aturan-atribusi-ketat)
10. [Manajemen Risiko & Mitigasi Penyelidikan Siber-Fisik](#10-manajemen-risiko--mitigasi-penyelidikan-siber-fisik)
11. [Functional Requirements (FR) & Non-Functional Requirements (NFR)](#11-functional-requirements-fr--non-functional-requirements-nfr)
12. [Deliverables & Artefak Output Penelitian](#12-deliverables--artefak-output-penelitian)
13. [Metrik Evaluasi & Key Performance Indicators (KPIs)](#13-metrik-evaluasi--key-performance-indicators-kpis)
14. [Rencana Eksperimen & Validasi Data Forensik Konvergen](#14-rencana-eksperimen--validasi-data-forensik-konvergen)
15. [Linimasa Proyek 14 Minggu (W1 - W14)](#15-linimasa-proyek-14-minggu-w1---w14)
16. [Rencana Diseminasi & Publikasi Ilmiah](#16-rencana-diseminasi--publikasi-ilmiah)
17. [Daftar Pustaka & Standar Regulasi](#17-daftar-pustaka--standar-regulasi)

---

### 1. Latar Belakang & Urgensi Konvergensi Siber-Fisik

Dalam lanskap ancaman modern, pemisahan tradisional antara **Keamanan Fisik** (gedung, gerbang akses, CCTV, kehadiran fisik manusia) dan **Keamanan Siber** (firewall, enkripsi, deteksi intrusi jaringan) telah runtuh. Pelaku kejahatan tingkat lanjut (*advanced threat actors*) tidak lagi menyerang sistem secara terisolasi. Mereka mengeksekusi **Serangan Konvergen (Cyber-Physical Hybrid Attacks)**:

1. **Vektor Fisik (The Physical Plane)**: Mengeksploitasi kehadiran fisik manusia di lokasi acara (venue konferensi, lobi gedung, ruang pameran), sabotase perangkat keras, penempelan stiker kode QR palsu di area fisik (*phygital attacks / quishing*), atau penyamaran langsung di tempat.
2. **Vektor Digital (The Digital Plane)**: Mengeksploitasi kanal siaran online, sintesis suara dan wajah berbasis AI (*deepfake audio-visual*), pembajakan akun live-streaming, serta transaksi blockchain.
3. **Vektor Kognitif (Layer 8 - The Human Factor)**: Memanfaatkan kerentanan psikologis korban (rasa percaya pada figur otoritas, kepanikan, rasa urgensi, dan bukti sosial) untuk menjembatani aksi fisik dan digital.

Urgensi penelitian ini bertumpu pada ketiadaan protokol investigasi digital forensik terpadu yang mampu merekonstruksi garis waktu (*timeline*) ketika sebuah serangan berpindah bolak-balik antara ranah fisik dan ranah digital.

---

### 2. Fakta Kasus & Dekonstruksi Serangan Hibrida (Fisik & Digital)

Studi kasus berfokus pada dinamika insiden seputar konferensi teknologi berskala internasional (seperti ajang **NVIDIA GTC**):

```mermaid
flowchart TD
    subgraph RANAH FISIK [Ranah Fisik: Venue & Lingkungan Nyata]
        P1["Keynote Panggung & Kehadiran Fisik Tokoh (Jensen Huang)"]
        P2["Peserta Konferensi & Pengunjung Booth Pameran Fisik"]
        P3["Distribusi Material Fisik / Stiker QR Code di Lokasi Acara"]
    end

    subgraph RANAH KOGNITIF [Layer 8: Eksploitasi Faktor Manusia]
        H1["Bias Otoritas Tokoh & Bukti Sosial Keramaian"]
        H2["FOMO: Iming-iming Giveaway Khusus Peserta Acara"]
    end

    subgraph RANAH DIGITAL [Ranah Digital: Siber & Media Sintetis]
        D1["Kanal Tiruan 'NVIDIA Live' Membajak Siaran"]
        D2["Deepfake AI Wajah & Suara Jensen Huang"]
        D3["Aliran Transaksi Wallet Kripto & Pencucian Aset"]
    end

    P1 -.->|Eksploitasi Waktu & Momentum| D1
    D2 -->|Manipulasi Otoritas| H1
    P3 -->|Phygital Gateway (Quishing)| D3
    H1 & H2 -->|Aksi Korban: Scan & Transfer| D3
```

#### 2.1 Dekonstruksi Dua Sisi Serangan
- **Dimensi Fisik**:
  - Penyelenggaraan acara fisik di pusat konvensi menjadi penentu waktu (*time-anchor*).
  - Kehadiran fisik audiens di lokasi menciptakan asumsi kelayakan (*inherent trust*) bahwa semua materi yang menyandang nama acara adalah resmi.
  - Vektor fisik mencakup manipulasi kode QR fisik (*quishing sticker overlay*) di tempat umum atau materi cetak tidak resmi.
- **Dimensi Digital**:
  - Pemanfaatan siaran langsung digital (*live stream spoofing*) yang memanipulasi algoritma metrik semu (~95.000 bot viewers).
  - Pemalsuan biometrik digital menggunakan deepfake suara (*audio cloning*) dan sinkronisasi bibir (*lip-sync synthesis*).
  - Pengalihan dana melalui smart contract atau wallet kripto anonim.

---

### 3. Research Questions (RQ) & Hipotesis Penelitian

#### 3.1 Pertanyaan Penelitian (Research Questions)
- **RQ-1 (Korelasi Forensik Siber-Fisik)**: Bagaimana merancang metode sinkronisasi bukti digital (log stream, audio-visual hash, ledger kripto) dengan bukti fisik (log akses venue, rekaman CCTV lingkungan, materi phygital QR) untuk menyusun garis waktu investigasi yang tidak terputus?
- **RQ-2 (Dinamika Layer 8 Hibrida)**: Apakah kombinasi rangsangan fisik (suasana acara konferensi) dan manipulasi digital (deepfake siaran) meningkatkan tingkat kerentanan kognitif korban secara signifikan dibanding serangan murni digital?
- **RQ-3 (Deteksi & Pencegahan Terpadu)**: Bagaimana arsitektur pertahanan konvergen (*Converged SOC/GSOC*) dapat mendeteksi indikasi awal serangan hibrida sebelum terjadi kerugian finansial atau fisik?

#### 3.2 Hipotesis Penelitian
- **H-1**: Korelasi silang berbasis *temporal event mapping* antara log aktivitas digital dan log pengawasan fisik mampu memangkas waktu atribusi insiden (*Incident Reconstruction Time*) hingga $>40\%$ dibandingkan investigasi terpisah.
- **H-2**: Tingkat kepatuhan korban untuk memindai kode QR (*quishing conversion rate*) meningkat $\ge 3\times$ lipat jika dipadukan dengan kehadiran momentum fisik resmi dan video deepfake figur otoritas.

---

### 4. Ruang Lingkup & Batasan Masalah (Scope & Limitations)

#### 4.1 Ruang Lingkup (In-Scope)
- Investigasi forensik terhadap artefak digital: rekaman deepfake, spektrum audio sintetis, metadata siaran, dan aliran transaksi blockchain publik.
- Investigasi forensik terhadap artefak fisik/phygital: analisis integritas visual stiker/banner QR fisik, log akses kontrol venue, dan rekaman pengawasan (CCTV).
- Pemodelan kognitif korban dalam konteks lingkungan fisik-digital gabungan.
- Perancangan purwarupa sistem korelasi siber-fisik (*Cyber-Physical Forensic Correlation Engine*).

#### 4.2 Batasan Masalah (Out-of-Scope & Limitations)
- Penelitian **tidak melakukan pengujian penetrasi fisik tanpa izin (*unauthorized physical break-in*)** ke fasilitas riil.
- Penelitian **tidak mengekspos identitas pribadi audiens atau staf keamanan** tanpa proses penyensoran (redaksi data pribadi/GDPR/UU PDP).
- Penelitian berfokus pada metodologi pertahanan (*blue team / forensic defense*) dan tidak menghasilkan alat eksploitasi fisik aktif.

---

### 5. Model Rantai Serangan Hibrida (Cyber-Physical Attack Chain)

Model serangan ini memperluas rantai pembunuhan siber konvensional menjadi **7 Fase Konvergen**:

```
+-------------------------------------------------------------------------------------------------+
| FASE 1: RECONNAISSANCE SIBER-FISIK                                                              |
| - Fisik  : Survei tata letak gedung pameran, lokasi booth resmi, titik buta keamanan fisik      |
| - Siber  : Pemindaian jadwal streaming resmi, struktur tim publikasi, akun media sosial eksekutif|
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| FASE 2: WEAPONIZATION GABUNGAN                                                                  |
| - Fisik  : Pencetakan stiker QR code berbahaya yang menyerupai branding resmi acara fisik       |
| - Siber  : Pelatihan model deepfake suara & wajah CEO (Jensen Huang) menggunakan korpus video   |
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| FASE 3: INFILTRASI & PENEMPATAN VEKTOR (DEPLOYMENT)                                             |
| - Fisik  : Pemasangan stiker QR di meja lobi / pembagian selebaran fisik palsu                  |
| - Siber  : Penyiapan kanal stream YouTube bajakan berlabel 'Official Live'                      |
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| FASE 4: EKSPLOITASI LAYER 8 & PENGKONDISIAN KOGNITIF                                            |
| - Pemanfaatan bias otoritas (CEO berpidato di video)                                            |
| - Eksploitasi urgensi fisik ("Hanya berlaku untuk pengunjung sesi keynote hari ini!")           |
| - Amplifikasi bukti sosial semu (95.000 bot penonton online)                                    |
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| FASE 5: AKSI SIBER-FISIK TERKOORDINASI (CONVERGED EXECUTION)                                    |
| - Korban di lokasi fisik atau daring memindai QR code via smartphone pribadi                    |
| - Smartphone mengeksekusi payload phishing / koneksi web3 wallet penguras aset                  |
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| FASE 6: MONETISASI & SABOTASE REPUTASI                                                          |
| - Transaksi aset kripto masuk ke wallet sindikat penipu                                         |
| - Kekacauan reputasi acara fisik dan gangguan ketertiban umum di venue acara                    |
+-------------------------------------------------------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| FASE 7: PENGHAPUSAN JEJAK JEJAK FISIK-DIGITAL (ANTI-FORENSICS)                                  |
| - Fisik  : Pelepasan stiker QR / pelaku fisik meninggalkan venue sebelum acara berakhir        |
| - Siber  : Penghapusan kanal live stream, crypto mixing, dan pergantian alamat IP/VPN           |
+-------------------------------------------------------------------------------------------------+
```

---

### 6. Kerangka Keilmuan: Cyber-Physical & Behavioral Forensics

Penyelidikan forensik memerlukan integrasi tiga pilar ilmu:

```
                            [ INVESTIGASI KONVERGEN ]
                                        |
        +-------------------------------+-------------------------------+
        |                               |                               |
        v                               v                               v
[ FORENSIK DIGITAL ]          [ FORENSIK FISIK ]            [ BEHAVIORAL & KOGNITIF ]
- Artefak Deepfake (Audio/Video)- Rekaman CCTV & Waktu Nyata - Profil Aktor Siber-Fisik
- Log Jaringan & Server Stream - Log Tap Kartu RFID / Pintu  - Psikologi Kerentanan Korban
- Ledger Blockchain & Smart Cont- Bukti Fisik Stiker QR Code - Analisis Rekayasa Sosial
```

- **Forensik Digital**: Mengamankan bukti elektromagnetik, komputasi awan, dan algoritma AI sintetis.
- **Forensik Fisik**: Memperlakukan materi cetak, rekaman sensor lingkungan, dan kartu akses dengan prinsip rantai pengawasan fisik (*Physical Chain of Custody*).
- **Behavioral & Cognitive Forensics**: Menghubungkan motif dan keputusan manusia di kedua lingkungan tersebut.

---

### 7. Metodologi Penelitian Tiga Fase Terpadu

```mermaid
flowchart LR
    subgraph FASE 1 [Fase 1: Triangulasi Bukti Bukti]
        E1["Pengumpulan Bukti Digital Stream & Blockchain"]
        E2["Akuisisi Log Fisik (CCTV, Kartu Akses, Materi Cetak)"]
        E1 & E2 --> E3["Penyelarasan Stempel Waktu (Timestamp Synchronization)"]
    end

    subgraph FASE 2 [Fase 2: Korelasi & Analisis Eksperimental]
        C1["Uji Anomali Media Deepfake (Audio/Visual)"]
        C2["Analisis Jejak Phygital (QR Code / Quishing)"]
        C3["Pemodelan Eksploitasi Kognitif Korban"]
        C1 & C2 & C3 --> C4["Pemetaan Garis Waktu Hibrida Terpadu"]
    end

    subgraph FASE 3 [Fase 3: Mitigasi & Standarisasi Pertahanan]
        M1["Perumusan Kerangka GSOC Terpadu"]
        M2["SOP Tanggap Darurat Insiden Siber-Fisik"]
        M3["Penyusunan Modul Deteksi Multi-Vektor"]
    end

    FASE 1 --> FASE 2 --> FASE 3
```

---

### 8. Arsitektur Sistem Investigasi & Mesin Korelasi Dual-Vektor

Arsitektur mesin korelasi forensik (*Cyber-Physical Forensic Engine*) dirancang untuk menyatukan log heterogen ke dalam basis data terpadu:

```
[ Sensor Lingkungan Fisik ]                [ Sensor Jaringan & Media Digital ]
  - Log RFID / Badge Tap                     - NetFlow & CDN Stream Logs
  - Video Feed CCTV (Timecoded)              - Deepfake Audio-Visual Spectrogram
  - Physical QR Code Scan Reports            - Blockchain Transaction Ledger
            |                                           |
            +---------------------+---------------------+
                                  |
                                  v
                [ Unified Forensic Ingestion Pipeline ]
                     (ISO/IEC 27037 Compliance)
                                  |
                                  v
              +---------------------------------------+
              | CYBER-PHYSICAL CORRELATION ENGINE     |
              | 1. Timestamp Normalizer (UTC Offset)  |
              | 2. Geolocation & BSSID/BLE Mapper     |
              | 3. Layer 8 Cognitive Pattern Matcher  |
              | 4. Cross-Vector Anomaly Scoring       |
              +---------------------------------------+
                                  |
                                  v
              +---------------------------------------+
              | OUTPUT INVESTIGASI:                   |
              | - Unified Hybrid Timeline Visualization|
              | - Attributed TTPs & Threat Actor Dossier
              | - Converged Incident Response Actions |
              +---------------------------------------+
```

---

### 9. Etika Penelitian, Kepatuhan Hukum & Aturan Atribusi Ketat

#### 9.1 Verification Gate & Perlindungan Identitas Tokoh Nyata
1. **Status Korban Mutlak**: Jensen Huang, jajaran pimpinan eksekutif, dan NVIDIA Corporation secara hukum diidentifikasi sebagai **korban eksploitasi identitas, imitasi tanpa hak, dan pencemaran reputasi**. Tidak ada dokumen yang boleh menuduh atau mengindikasikan keterlibatan mereka sebagai pelaku.
2. **Atribusi Pelaku**: Aktor kejahatan wajib ditulis dengan nomenklatur netral forensik: *"Kelompok Ancaman Hibrida Tak Teridentifikasi (UNC-CP-01)"* atau *"Operator Sindikat Phygital-Kripto"*.
3. **Penyensoran Privasi Rekaman CCTV**: Seluruh wajah individu dalam rekaman fisik atau log kartu pegawai yang digunakan dalam eksperimen wajib di-blur (*anonymized*) untuk memenuhi kepatuhan UU Pelindungan Data Pribadi (UU PDP) dan kaidah etika penelitian institusional.

---

### 10. Manajemen Risiko & Mitigasi Penyelidikan Siber-Fisik

| ID | Kategori Risiko | Deskripsi Dampak | Strategi Mitigasi Terstruktur |
| :--- | :--- | :--- | :--- |
| **RS-01** | *Desinkronisasi Waktu* | Perbedaan jam internal server digital dan NVR CCTV menyebabkan kesalahan urutan kejadian | Menerapkan normalisasi berbasis sumber waktu terpusat (PTP/NTP Clock Drift Adjustment) |
| **RS-02** | *Kerusakan Bukti Fisik* | Stiker QR fisik rusak, terlepas, atau terhapus sidik jarinya | Melakukan fotografi makro forensik beresolusi tinggi dan preservasi dalam kantong anti-statis |
| **RS-03** | *Penyusupan Fisik Liar* | Risiko bahaya keamanan personil saat menginspeksi lokasi acara publik | Investigasi fisik hanya dilakukan melalui kerja sama resmi dengan otoritas keamanan venue/GSOC |
| **RS-04** | *Bias Interpretasi AI* | Modul deteksi deepfake menghasilkan False Positive pada video terkompresi | Verifikasi ganda (*dual-analyst peer verification*) sebelum penetapan status bukti |

---

### 11. Functional Requirements (FR) & Non-Functional Requirements (NFR)

#### 11.1 Functional Requirements (FR)
- **FR-01 (Akuisisi Bukti Terpadu)**: Sistem mampu mengimpor data stream video digital, log access control fisik (.csv/.syslog), dan metadata transaksi blockchain.
- **FR-02 (Korelasi Waktu Otomatis)**: Mesin korelasi mampu mencocokkan event fisik (misal: orang berdiri di depan booth pada 14:02:10) dengan event digital (lonjakan trafik live stream atau pembuatan QR pada 14:02:15).
- **FR-03 (Analisis Integritas QR Phygital)**: Modul OCR dan pengurai URL mampu membedakan tautan resmi acara dengan domain *typosquatting* penipuan.
- **FR-04 (Peringkat Eksploitasi Kognitif)**: Sistem menghitung nilai *Cognitive Pressure Index* (skala 1–10) berdasarkan kombinasi faktor urgensi dan kehadiran figur otoritas.

#### 11.2 Non-Functional Requirements (NFR)
- **NFR-01 (Integritas Rantai Bukti)**: Seluruh artefak fisik dan digital harus memiliki catatan riwayat pemindahan (*Chain of Custody*) yang memenuhi standar ISO/IEC 27037.
- **NFR-02 (Auditability)**: Setiap tahap rekonstruksi garis waktu harus dapat diuji ulang secara independen (*reproducible forensic trail*).

---

### 12. Deliverables & Artefak Output Penelitian

```
artifacts/
├── 01_Unified_Research_Paper/
│   ├── Cyber_Physical_Behavioral_Forensics_Manuscript.pdf
│   └── Multi_Vector_Event_Correlation_Matrix.xlsx
├── 02_Forensic_Dossier_Hybrid/
│   ├── Physical_Evidence_Chain_of_Custody.pdf
│   ├── Deepfake_Media_Forensic_Analysis.pdf
│   └── Phygital_Quishing_Lab_Report.pdf
├── 03_Forensic_Toolkits/
│   ├── time_sync_correlator.py
│   ├── phygital_qr_inspector.py
│   └── deepfake_spectral_evaluator.py
└── 04_Enterprise_Standard/
    └── Converged_GSOC_Incident_Response_Playbook.pdf
```

---

### 13. Metrik Evaluasi & Key Performance Indicators (KPIs)

1. **Akurasi Rekonstruksi Garis Waktu Hibrida**:
   - Tingkat korelasi yang benar antara event fisik dan digital $\ge 95\%$ pada data uji terkontrol.
2. **Efektivitas Deteksi Deepfake & Quishing**:
   - $\text{F1-Score} \ge 0.91$ pada deteksi video deepfake kompresi rendah/menengah.
   - $\text{Recall} \ge 98\%$ pada identifikasi URL phishing dari kode QR fisik.
3. **Reduksi Waktu Tanggap Insiden Konvergen (*MTTD / MTTR*)**:
   - Penurunan waktu deteksi insiden hibrida hingga $\le 15\text{ menit}$ melalui buku panduan GSOC terpadu.

---

### 14. Rencana Eksperimen & Validasi Data Forensik Konvergen

#### 14.1 Eksperimen Laboratorium Simulasi Siber-Fisik
- Membangun lingkungan simulasi terkontrol yang meniru lobi konferensi:
  - Dipasang monitor siaran (menampilkan stream kontrol vs stream deepfake).
  - Ditempatkan poster materi acara dengan kode QR resmi vs kode QR quishing.
  - Dipasang sistem pembaca badge RFID dan kamera pengawas waktu riil.
- Menguji efektivitas instrumen *time_sync_correlator.py* dalam menyatukan 1.000 log transaksi fisik dan digital secara akurat.

---

### 15. Linimasa Proyek 14 Minggu (W1 - W14)

| Periode | Fokus Pekerjaan | Capaian Utama |
| :--- | :--- | :--- |
| **W1 - W2** | Kajian pustaka konvergensi siber-fisik, perumusan metodologi, setup lab forensik | *Dokumen Metodologi & Registri Bukti* |
| **W3 - W5** | Ekstraksi artefak digital (deepfake audio/visual, metadata stream) | *Laporan Analisis Media Forensik* |
| **W6 - W7** | Analisis artefak fisik (log kontrol akses venue, phygital QR, CCTV) | *Laporan Forensik Fisik & Lingkungan* |
| **W8 - W9** | Pembangunan dan pengujian mesin korelasi waktu siber-fisik | *Software Prototype Korelasi Dual-Vektor* |
| **W10 - W11**| Eksperimen simulasi Layer 8 & validasi metrik reseptivitas korban | *Data Hasil Uji Validasi Kognitif* |
| **W12** | Penyusunan Converged Security Playbook untuk tim keamanan korporasi | *Enterprise Incident Response Playbook* |
| **W13 - W14**| Penulisan naskah akhir, peer-review pakar, finalisasi arsip kode | *Manuskrip Publikasi & Dokumen Lengkap* |

---

### 16. Rencana Diseminasi & Publikasi Ilmiah

- **Target Jurnal Ilmiah**:
  - *Journal of Information Security and Applications (Elsevier)*
  - *Forensic Science International: Digital Investigation*
  - *IEEE Transactions on Dependable and Secure Computing*
- **Diseminasi Praktisi Keamanan**:
  - Presentasi di forum keamanan industri (ASIS Chapter, Black Hat Briefings, FIRST Incident Response Symposium).

---

### 17. Daftar Pustaka & Standar Regulasi

1. CISA. (2020). *Cybersecurity and Physical Security Convergence Guide*. Cybersecurity and Infrastructure Security Agency.
2. ASIS International. (2019). *Enterprise Security Risk Management (ESRM) Guideline*.
3. NIST SP 800-86. (2020). *Guide to Integrating Forensic Techniques into Incident Response*. National Institute of Standards and Technology.
4. ISO/IEC 27037:2012. *Guidelines for identification, collection, acquisition, and preservation of digital evidence*.
5. Casey, E. (2011). *Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet*. Academic Press.
6. Cialdini, R. B. (2021). *Influence: The Psychology of Persuasion*. Harper Business.
7. Rossler, A., et al. (2019). *FaceForensics++: Learning to Detect Manipulated Facial Images*. ICCV.

