# PRD & KERANGKA PENELITIAN FORENSIK DIGITAL (VERSI 1.0)
## Behavioral Digital Forensics pada Serangan Layer 8: Analisis Kasus Deepfake Keynote Jensen Huang (NVIDIA GTC)

---

| Parameter Dokumen | Keterangan |
| :--- | :--- |
| **Kode Dokumen** | `PRD-BDF-L8-NV01` |
| **Versi Dokumen** | `1.0 (Comprehensive Release)` |
| **Klasifikasi** | *Defensive Security & Digital Forensic Research* |
| **Fokus Utama** | *Integrated Behavioral Forensics & Deepfake Media Forensics* |
| **Status Dokumen** | Disetujui untuk Eksekusi Riset |

---

## DAFTAR ISI (17 BAGIAN UTAMA)
1. [Latar Belakang & Urgensi Masalah](#1-latar-belakang--urgensi-masalah)
2. [Fakta Kasus & Dekonstruksi Kejadian (Jensen Huang Deepfake GTC)](#2-fakta-kasus--dekonstruksi-kejadian-jensen-huang-deepfake-gtc)
3. [Research Questions (RQ) & Hipotesis Penelitian](#3-research-questions-rq--hipotesis-penelitian)
4. [Ruang Lingkup & Batasan Penelitian (Scope & Limitations)](#4-ruang-lingkup--batasan-penelitian-scope--limitations)
5. [Model Rantai Serangan Layer 8 (Layer 8 Attack Chain)](#5-model-rantai-serangan-layer-8-layer-8-attack-chain)
6. [Kerangka Keilmuan: Integrasi Behavioral Forensics & Media Forensics](#6-kerangka-keilmuan-integrasi-behavioral-forensics--media-forensics)
7. [Metodologi Penelitian Tiga Fase (3-Phase Methodology)](#7-metodologi-penelitian-tiga-fase-3-phase-methodology)
8. [Arsitektur Teknis & Komponen Deteksi (FR-07: Media & NLP Analysis)](#8-arsitektur-teknis--komponen-deteksi-fr-07-media--nlp-analysis)
9. [Etika Penelitian, Kepatuhan Hukum & Aturan Atribusi Ketat](#9-etika-penelitian-kepatuhan-hukum--aturan-atribusi-ketat)
10. [Manajemen Risiko & Mitigasi Penyelidikan](#10-manajemen-risiko--mitigasi-penyelidikan)
11. [Functional Requirements (FR) & Non-Functional Requirements (NFR)](#11-functional-requirements-fr--non-functional-requirements-nfr)
12. [Deliverables & Artefak Output Penelitian](#12-deliverables--artefak-output-penelitian)
13. [Metrik Evaluasi & Key Performance Indicators (KPIs)](#13-metrik-evaluasi--key-performance-indicators-kpis)
14. [Rencana Eksperimen & Validasi Data Forensik](#14-rencana-eksperimen--validasi-data-forensik)
15. [Linimasa Riset 14 Minggu (W1 - W14)](#15-linimasa-riset-14-minggu-w1---w14)
16. [Rencana Diseminasi & Publikasi Ilmiah](#16-rencana-diseminasi--publikasi-ilmiah)
17. [Daftar Pustaka & Referensi Awal](#17-daftar-pustaka--referensi-awal)

---

### 1. Latar Belakang & Urgensi Masalah

Dalam model referensi Open Systems Interconnection (OSI) 7-layer, sistem keamanan informasi tradisional memusatkan fokus pada pertahanan perimeter teknis (Layer 1 hingga Layer 7). Namun, para pakar keamanan siber sepakat mengakui keberadaan de-facto **Layer 8**, yaitu **Faktor Manusia (The Human Layer)**. Lapisan ini mencakup psikologi kognitif pengguna, bias keputusan, kepatuhan prosedural, dan kerentanan terhadap manipulasi sosial.

Perkembangan mutakhir dalam teknologi *Generative Artificial Intelligence* (Gen-AI)—khususnya *audio cloning* berbasis diffusion/neural vocoder dan sintesis video *high-fidelity face-swap*—telah secara radikal menurunkan biaya pembuatan deepfake berkualitas tinggi. Hal ini melahirkan taktik eksploitasi baru: **AI-Powered Impersonation & Social Engineering**.

Urgensi penelitian ini lahir dari fenomena di mana perimeter keamanan kriptografis dan jaringan tidak ditembus, melainkan dieksploitasi melalui manipulasi kognitif target menggunakan figur otoritas industri (*Authority Bias*). Ketika bukti forensik multimedia sintetis digabungkan dengan manipulasi perilaku, investigasi digital forensik konvensional (berbasis disk/network artifact) tidak lagi memadai tanpa melibatkan **Behavioral Digital Forensics** dan **Forensic Cyberpsychology**.

---

### 2. Fakta Kasus & Dekonstruksi Kejadian (Jensen Huang Deepfake GTC)

#### 2.1 Kronologi dan Ringkasan Kasus
Pada saat perhelatan keynote konferensi resmi NVIDIA (GTC DC), terjadi insiden serangan rekayasa sosial masif yang mengeksploitasi momentum siaran langsung (*live-streaming event*):

```mermaid
flowchart LR
    A["Event Resmi: NVIDIA GTC Keynote"] --> B["Aktor Membajak/Membuat Kanal 'NVIDIA Live'"]
    B --> C["Siaran Stream Deepfake Jensen Huang (AI Voice + Face)"]
    C --> D["Manipulasi Tampilan: Overlay QR Code + Promo Giveaway Kripto"]
    D --> E["Algoritma & Botting: Mencapai 95.000+ Penonton"]
    E --> F["Eksploitasi Layer 8: Korban Melakukan Scan QR & Transaksi Wallet"]
```

#### 2.2 Data Komparatif Lapangan
- **Kanal Resmi**: Siaran resmi NVIDIA mengumpulkan audiens terverifikasi sekitar 12.000 hingga 20.000 penonton langsung.
- **Kanal Sindikat Palsu**: Siaran tiruan bertajuk *"NVIDIA Live / Official"* mencatat rentang penonton sekitar 85.000 hingga 100.000+ penonton bersamaan (*concurrent viewers*). Tingginya angka ini dicapai melalui kombinasi teknik *view-botting*, manipulasi algoritma rekomendasi YouTube, dan eksploitasi kata kunci tren (*search hijacking*).
- **Vektor Monetisasi**: Overlay kode QR dinamis di layar yang mengarahkan korban ke landing page penipuan skema *crypto-doubling* (misal: "Kirim 1 BTC/ETH, dapatkan 2x kembali").

#### 2.3 Relevansi Fakta ke Layer 8
1. **Bias Otoritas (*Authority Bias*)**: Jensen Huang diposisikan sebagai figur pionir komputasi AI global. Kehadirannya memberikan legitimasi instan terhadap klaim teknologi dan promosi yang disampaikan.
2. **Social Proof Asimetris**: Korban melihat angka 95.000 penonton aktif, yang secara psikologis meyakinkan korban bahwa siaran tersebut sah dan aman.
3. **Pemanfaatan Urgensi (*Time-Sensitive Scarcity*)**: Skema penipuan menggunakan hitung mundur (*countdown timer*) yang menekan fungsi kognitif analitis korban, memicu keputusan impulsif.

---

### 3. Research Questions (RQ) & Hipotesis Penelitian

#### 3.1 Pertanyaan Penelitian (Research Questions)
- **RQ-1 (Teknis Media)**: Indikator artefak digital dan akustik forensik apa yang paling persisten dan reliabel untuk membedakan video siaran langsung asli Jensen Huang dari video sintetis (deepfake) yang dikompresi oleh platform streaming?
- **RQ-2 (Perilaku & Kognitif)**: Bagaimana rantai serangan Layer 8 mengeksploitasi bias kognitif manusia (*authority bias*, *social proof*, dan *FOMO*) dalam kasus deepfake siaran langsung berskala besar?
- **RQ-3 (Investigasi & Atribusi)**: Bagaimana kerangka kerja *Behavioral Digital Forensics* dapat memetakan taktik, teknik, dan prosedur (TTPs) aktor penipuan multimodal tanpa mengorbankan integritas etika dan batas atribusi legal?

#### 3.2 Hipotesis Penelitian
- **H-1**: Ekstraksi fitur multimodal (inkonsistensi mikrografik perioral/lip-sync error dan diskontinuitas spektral frekuensi tinggi pada audio vocoder) mampu mendeteksi manipulasi deepfake dengan akurasi $\ge 92\%$ meskipun mengalami kompresi video streaming H.264/VP9.
- **H-2**: Persepsi kredibilitas korban pada siaran palsu dipengaruhi secara signifikan oleh metrik sosial semu (*view counts* dan *live chat engagement*) lebih dominan daripada kualitas visual deepfake itu sendiri.
- **H-3**: Integrasi pemetaan TTP berbasis MITRE ATT&CK dengan matriks eksploitasi kognitif Layer 8 mempercepat waktu rekonstruksi insiden (*Mean Time to Understand/MTTU*) pada tim respon forensik.

---

### 4. Ruang Lingkup & Batasan Penelitian (Scope & Limitations)

#### 4.1 Ruang Lingkup (In-Scope)
- Analisis rekaman video dan audio kasus deepfake Jensen Huang pada insiden YouTube Live.
- Analisis forensik artefak digital: metadata stream, jejak kompresi, sinyal biometrik wajah buatan, dan artefak audio sintetik.
- Dekonstruksi rantai serangan Layer 8 dan psikologi rekayasa sosial.
- Pembangunan purwarupa modul deteksi NLP untuk pesan rekayasa sosial berbahasa Indonesia dan Inggris.
- Perumusan kerangka kerja mitigasi *Human Risk Management (HRM)* dan pedoman investigasi insiden (*SOP Forensik*).

#### 4.2 Batasan Masalah (Out-of-Scope & Limitations)
- Penelitian **tidak melakukan peretasan aktif (*offensive counter-attack*)** terhadap infrastruktur pelaku.
- Penelitian **tidak merilis kode sumber untuk membuat deepfake yang dapat dieksploitasi (*no weaponized code generation*)**.
- Analisis transaksi blockchain wallet pelaku dibatasi pada *passive ledger intelligence* (eksplorasi buku besar publik) tanpa de-anonimisasi paksa di luar data publik.
- Keterbatasan data asli rekaman stream yang mungkin telah dihapus oleh platform; rekonstruksi mengandalkan korpus arsip digital forensik (*forensic mirrors, archival dumps, and technical report captures*).

---

### 5. Model Rantai Serangan Layer 8 (Layer 8 Attack Chain)

Serangan Layer 8 pada kasus ini memodifikasi *Cyber Kill Chain* konvensional menjadi rantai manipulasi manusia terpadu:

```
+-----------------------------------------------------------------------------------+
| 1. RECONNAISSANCE & TARGETING                                                     |
|    - Pemantauan jadwal keynote resmi NVIDIA (GTC).                                |
|    - Pemanfaatan momentum hype pasar AI & GPU.                                    |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| 2. WEAPONIZATION (SYNTHETIC GENERATION)                                           |
|    - Pemanenan korpus suara & video resolusi tinggi Jensen Huang dari keynote lama|
|    - Pelatihan/inferensi neural voice model & latent face diffusion model         |
|    - Pembuatan video broadcast master loop dengan promo giveaway kripto           |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| 3. INFRASTRUCTURE & CHANNEL HIJACKING                                             |
|    - Kompromi akun YouTube terverifikasi atau pendaftaran kanal 'NVIDIA Live'     |
|    - Modifikasi identitas kanal (avatar, banner resmi NVIDIA, deskripsi)          |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| 4. DELIVERY & SOCIAL PROOF AMPLIFICATION                                          |
|    - Peluncuran live stream bersamaan dengan keynote resmi                        |
|    - Pengerahan view-botting (~95.000 concurrent bot-viewers)                     |
|    - Pembungkaman chat kritis melalui moderasi bot kata kunci                     |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| 5. COGNITIVE EXPLOITATION (LAYER 8 COMPROMISE)                                    |
|    - Aktivasi Authority Bias (figur CEO Jensen Huang)                             |
|    - Rekayasa Scarcity & FOMO (hitungan mundur promo promo 2x)                    |
|    - Dorongan Call to Action melalui overlay QR Code                              |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| 6. ACTION ON OBJECTIVES & MONETIZATION                                            |
|    - Korban mentransfer aset kripto (BTC/ETH/USDT) ke wallet pelaku               |
|    - Aktor mencuci dana menggunakan mixing service atau decentralized exchange    |
+-----------------------------------------------------------------------------------+
```

---

### 6. Kerangka Keilmuan: Integrasi Behavioral Forensics & Media Forensics

Penelitian ini memadukan tiga pilar disiplin ilmu forensik modern:

```
                      +-----------------------------------+
                      | INTEGRATED FORENSIC INVESTIGATION |
                      +-----------------+-----------------+
                                        |
       +--------------------------------+--------------------------------+
       |                                |                                |
       v                                v                                v
+----------------------+     +----------------------+     +----------------------+
|  DEEPFAKE / MEDIA    |     |  BEHAVIORAL DIGITAL  |     | FORENSIC CYBER-      |
|      FORENSICS       |     |      FORENSICS       |     |     PSYCHOLOGY       |
+----------------------+     +----------------------+     +----------------------+
| - Analisis Lip-Sync  |     | - Rekonstruksi TTP   |     | - Eksploitasi Kognisi|
| - Spektrogram Audio  |     | - Jejak Operasi Akun |     | - Profil Kerentanan  |
| - Deteksi Frame/Blur |     | - Aliran Dana Kripto |     | - Bias Keputusan     |
| - Anomali Kedipan    |     | - Profil Aktor Siber |     | - Reseptivitas Korban|
+----------------------+     +----------------------+     +----------------------+
```

1. **Deepfake Media Forensics**: Menguji integritas berkas multimedia murni secara matematis dan sinyal pemrosesan digital (DSP).
2. **Behavioral Digital Forensics**: Menganalisis jejak perilaku komputasi pelaku, kebiasaan waktu siaran (*operational tempo*), pola teks penipuan, dan interaksi bot.
3. **Forensic Cyberpsychology**: Menginvestigasi mengapa kontrol logika pengguna runtuh di hadapan stimulus video palsu berotoritas tinggi.

---

### 7. Metodologi Penelitian Tiga Fase (3-Phase Methodology)

```mermaid
flowchart TD
    subgraph Fase 1: Akuisisi & Forensik Teknis
        P1A["Preservasi Video & Audio Stream"] --> P1B["Ekstraksi Artefak Kompresi & Metadata"]
        P1B --> P1C["Analisis Spektral Akustik & Visual Deepfake"]
    end

    subgraph Fase 2: Analisis Perilaku & Kognitif
        P2A["Katalogisasi Manipulasi Kognitif Layer 8"] --> P2B["Analisis Pola Pesan & Rekayasa Teks"]
        P2B --> P2C["Pemodelan Reseptivitas Korban & Social Proof"]
    end

    subgraph Fase 3: Sintesis Atribusi & Mitigasi Defensif
        P3A["Pemetaan TTP & Threat Actor Profiling"] --> P3B["Perumusan Framework SOP Forensik"]
        P3B --> P3C["Pengembangan Model Deteksi & Panduan HRM"]
    end

    Fase 1 --> Fase 2
    Fase 2 --> Fase 3
```

#### Fase 1: Preservasi Bukti & Analisis Media Forensik (Minggu 1 - 5)
- Pengumpulan sampel video bukti siaran langsung deepfake dan video kontrol (keynote resmi).
- Ekstraksi frame-by-frame untuk mengukur *Eye Blinking Rate* (EAR), diskontinuitas tekstur kulit, dan koherensi pencahayaan wajah.
- Analisis audio: Mel-Frequency Cepstral Coefficients (MFCC) dan visualisasi spektrogram untuk mengidentifikasi artefak sintesis suara.

#### Fase 2: Behavioral Forensics & Analisis Manipulasi Layer 8 (Minggu 6 - 9)
- Dekonstruksi transkrip percakapan dan pesan siaran menggunakan teknik linguistik forensik.
- Analisis interaksi live chat: identifikasi sentimen semu, bot-seeding, dan pembersihan pesan peringatan dari penonton asli.
- Pemetaan vektor eksploitasi psikologis berdasarkan matriks Cialdini (*Authority, Social Proof, Scarcity*).

#### Fase 3: Threat Profiling & Desain Pertahanan Terpadu (Minggu 10 - 14)
- Sintesis profil ancaman (*Threat Actor Profile*) berdasarkan infrastruktur teknis dan modus psikologis.
- Evaluasi modul NLP pendeteksi pesan manipulatif berbahasa Indonesia & Inggris.
- Penyusunan buku putih pertahanan (*Whitepaper / Defense Playbook*) dan kerangka kesiapsiagaan insiden Layer 8 bagi korporasi.

---

### 8. Arsitektur Teknis & Komponen Deteksi (FR-07: Media & NLP Analysis)

Arsitektur sistem dirancang untuk memproses berkas stream masuk (*input stream*) melalui dua pipa verifikasi (*dual verification pipeline*):

```
                                [ Incoming Live Stream / Video ]
                                               |
                     +-------------------------+-------------------------+
                     |                                                   |
                     v                                                   v
         [ Pipeline 1: Media Forensics ]                     [ Pipeline 2: NLP & Layer 8 ]
                     |                                                   |
        +------------+------------+                         +------------+------------+
        |                         |                         |                         |
        v                         v                         v                         v
  [Visual Artifact]        [Audio Spectral]         [Transcript OCR/STT]      [Context & Urgency]
  - Lip-sync error         - Vocoder artifact       - Deteksi giveaway        - Scarcity score
  - Facial warping         - Formant shift          - QR Code content         - Authority claim
        |                         |                         |                         |
        +------------+------------+                         +------------+------------+
                     |                                                   |
                     +-------------------------+-------------------------+
                                               |
                                               v
                                [ Forensic Correlation Engine ]
                                               |
                                               v
                        +---------------------------------------------+
                        | OUTPUT:                                     |
                        | 1. Deepfake Probability Score (0 - 100%)    |
                        | 2. Layer 8 Manipulation Index (0 - 10)      |
                        | 3. Forensic Evidence Dossier & Audit Log    |
                        +---------------------------------------------+
```

#### Spesifikasi Fitur NLP Berbahasa Indonesia & Multilingual:
- **Speech-to-Text (STT) Normalizer**: Mentranskripsi audio stream secara near real-time.
- **Manipulative Pattern Matcher**: Mendeteksi pola frasa rekayasa sosial spesifik:
  - *Authority Claims*: "NVIDIA secara resmi membagikan...", "Jensen Huang mengumumkan program hadiah..."
  - *Scarcity / Urgency Triggers*: "Hanya berlaku selama keynote berlangsung", "Tersisa 100 slot partisipasi".
  - *Financial Lures*: "Kirim 0.5 ETH, dapatkan 1.0 ETH instan".

---

### 9. Etika Penelitian, Kepatuhan Hukum & Aturan Atribusi Ketat

#### 9.1 Verification Gate & Aturan Atribusi Entitas Nyata (Wajib Dipatuhi)
1. **Status Korban**: Jensen Huang dan NVIDIA Corporation adalah **korban pencemaran nama baik, imitasi tanpa izin (*unauthorized impersonation*), dan pelanggaran hak cipta visual**. Dalam keadaan apa pun, publikasi tidak boleh menuliskan Jensen Huang atau NVIDIA sebagai subjek pelaku kejahatan.
2. **Penyebutan Pelaku**: Sebelum ada penetapan hukum berkekuatan tetap atau rilis atribusi resmi dari otoritas penegak hukum (misal: FBI / INTERPOL / Bareskrim Polri), pihak penyerang **wajib secara konsisten disebut sebagai: *"Operator Kanal Belum Teridentifikasi"* atau *"Aktor Ancaman Sindikat Kripto (UNC-XXXX)"***.
3. **Penyensoran Informasi Pribadi (PII Redaction)**: Alamat wallet korban yang terekam atau nama pengguna publik yang muncul di live chat wajib disamarkan (*anonymized/hashed*) untuk melindungi privasi individu.

#### 9.2 Kepatuhan Yuridis
- Riset tunduk pada prinsip *Ethical Security Research*, tidak melanggar ketentuan UU ITE (Indonesia) terkait distribusi materi manipulatif terlarang, serta mematuhi prinsip *Fair Use* untuk investigasi akademis.

---

### 10. Manajemen Risiko & Mitigasi Penyelidikan

| No | Risiko Potensial | Tingkat Dampak | Probabilitas | Rencana Mitigasi Terstruktur |
| :--- | :--- | :--- | :--- | :--- |
| **R-1** | Sampel video asli di-takedown dari platform streaming | Tinggi | Sangat Tinggi | Membuat *local forensic mirror* secara *air-gapped* menggunakan *cryptographic hashing* (SHA-256) sesaat setelah bukti ditemukan. |
| **R-2** | Tuntutan hukum pencemaran nama baik akibat salah atribusi | Sangat Tinggi | Rendah | Mengunci Bagian 9.1: atribusi netral pada aktor tak dikenal dan validasi peer-review sebelum rilis publik. |
| **R-3** | Risiko bias subjektivitas dalam asesmen kognitif korban | Sedang | Sedang | Menggunakan kuesioner terstandarisasi berbasis metrik psikometri tervalidasi (*Likert scale 7-point, cognitive load metrics*). |
| **R-4** | Salah klasifikasi (*False Positive*) pada model deteksi NLP | Sedang | Sedang | Menerapkan *ensemble thresholding*: keputusan peringatan hanya terpicu jika korelasi media dan teks sama-sama melampaui batas batas kritis ($\ge 0.85$). |

---

### 11. Functional Requirements (FR) & Non-Functional Requirements (NFR)

#### 11.1 Functional Requirements (FR)
- **FR-01 (Akuisisi Bukti)**: Sistem harus mampu memvalidasi keaslian hash SHA-256 dari setiap artefak video yang dikaji.
- **FR-02 (Ekstraksi Landmark Wajah)**: Modul harus mampu melacak 68–468 titik landmark wajah per frame untuk mendeteksi distorsi geometris.
- **FR-03 (Analisis Integritas Audio)**: Sistem harus mengekstraksi spektrogram frekuensi tinggi ($>16\text{ kHz}$) untuk menguji jejak rekonstruksi neural vocoder.
- **FR-04 (Pemetaan Layer 8)**: Modul harus mengklasifikasikan setiap tahapan serangan ke dalam 6 tahapan Rantai Serangan Layer 8.
- **FR-05 (Deteksi NLP Manipulatif)**: Sistem harus mengenali minimal 15 pola leksikal manipulasi urgensi dan iming-iming finansial (Bahasa Indonesia & Inggris).
- **FR-06 (Katalogisasi TTP)**: Sistem harus memetakan temuan ke dalam taksonomi MITRE ATT&CK for Enterprise & Social Engineering matrix.

#### 11.2 Non-Functional Requirements (NFR)
- **NFR-01 (Integritas Forensik)**: Setiap pemrosesan bukti harus mematuhi standar ISO/IEC 27037 (*Guidelines for identification, collection, acquisition, and preservation of digital evidence*).
- **NFR-02 (Reproducibility)**: Setiap script ekstraksi fitur dan kode analisis data harus terdokumentasi dan dapat direproduksi dalam lingkungan virtual terisolasi (*Docker container*).
- **NFR-03 (Security)**: Semua artefak data penipuan disimpan dalam direktori terenkripsi (AES-256) dengan akses terbatas.

---

### 12. Deliverables & Artefak Output Penelitian

```
artifacts/
├── 01_Research_Paper/
│   ├── Main_Manuscript_Behavioral_Digital_Forensics.pdf
│   └── Supplementary_Statistical_Data.xlsx
├── 02_Forensic_Evidence_Dossier/
│   ├── Chain_of_Custody_Log.md
│   ├── Media_Artifact_Analysis_Report.pdf
│   └── Blockchain_Ledger_Traces.csv
├── 03_Detection_Toolkits/
│   ├── audio_spectral_analyzer.py
│   ├── nlp_urgency_classifier.py
│   └── requirements.txt
└── 04_Enterprise_Playbook/
    └── Layer8_Executive_Defense_SOP.pdf
```

---

### 13. Metrik Evaluasi & Key Performance Indicators (KPIs)

1. **Akurasi Deteksi Media Forensik**:
   $$\text{Precision} \ge 90\%, \quad \text{Recall} \ge 88\%, \quad \text{F1-Score} \ge 0.89$$
2. **Kinerja Model Deteksi Pesan Rekayasa Sosial (NLP)**:
   - Area Under the ROC Curve (AUC-ROC) $\ge 0.92$ pada dataset uji pesan berbahasa Indonesia.
3. **Chain of Custody Completeness**:
   - $100\%$ artefak digital memiliki catatan *hash verification*, *timestamp*, dan sumber penarikan yang valid secara forensik.
4. **Kejelasan Rekonstruksi TTP**:
   - $100\%$ tahapan serangan terpetakan dengan referensi mitigasi defensif yang dapat diimplementasikan (*actionable*).

---

### 14. Rencana Eksperimen & Validasi Data Forensik

#### 14.1 Pengujian Media Forensik (Deepfake Verification)
- **Dataset Kontrol**: 50 segmen video asli keynote resmi NVIDIA GTC (resolusi 1080p).
- **Dataset Uji**: 50 segmen video siaran deepfake penipuan yang berhasil dipreservasi.
- **Metode Pengujian**:
  1. Pengujian diskontinuitas frekuensi temporal (*Optical Flow Anomaly*).
  2. Pengujian inkonsistensi spektral audio menggunakan model pra-terlatih (*ResNet / RawNet2*).
  3. Matriks evaluasi: Confusion Matrix ($TP, FP, TN, FN$).

#### 14.2 Validasi Kognitif Layer 8 & Reseptivitas Korban
- **Metode**: Simulasi eksperimental terkontrol (*Controlled Perception Experiment*) dengan $\approx 100$ responden terbagi dalam 2 grup (A/B testing):
  - *Grup A*: Diberikan tayangan video stream tanpa metrik penonton (tanpa angka 95.000 penonton).
  - *Grup B*: Diberikan tayangan video stream lengkap dengan metrik semu 95.000 penonton dan bot chat.
- **Tujuan**: Membuktikan secara empiris sejauh mana *social proof metric* memengaruhi kepercayaan korban terhadap keabsahan siaran.

---

### 15. Linimasa Riset 14 Minggu (W1 - W14)

| Fase | Minggu (W) | Fokus Aktivitas Utama | Output Kunci |
| :--- | :--- | :--- | :--- |
| **Inisiasi & Preservasi** | W1 - W2 | Pengumpulan artefak, validasi rantai bukti (Chain of Custody), telaah literatur | *Evidence Archive & Hash Registry* |
| **Forensik Media** | W3 - W5 | Ekstraksi fitur visual, analisis spektrogram audio, identifikasi model sintesis | *Deepfake Media Technical Report* |
| **Analisis Layer 8** | W6 - W7 | Analisis transkrip, psikologi penipuan, dekonstruksi botting & live chat | *Cognitive Vulnerability Matrix* |
| **Rekayasa NLP** | W8 - W9 | Pelatihan & tuning modul NLP deteksi pesan rekayasa sosial (ID & EN) | *Trained NLP Classification Model* |
| **Eksperimen & Validasi** | W10 - W11 | Eksekusi eksperimen komparatif, evaluasi metrik F1-score & AUC | *Experiment Validation Results* |
| **Penyusunan Playbook** | W12 | Perumusan SOP mitigasi korporasi & Human Risk Management | *Defensive Action Playbook* |
| **Finalisasi & Diseminasi**| W13 - W14 | Penulisan manuskrip jurnal/laporan riset lengkap, peer-review internal | *Final Research Paper & PRD Complete* |

---

### 16. Rencana Diseminasi & Publikasi Ilmiah

- **Target Jurnal / Konferensi Ilmiah**:
  - *IEEE Transactions on Information Forensics and Security (TIFS)* / *Computers & Security (Elsevier)*.
  - Konferensi bidang Cyber Security: *IEEE S&P, ACM CCS Workshop on Fake Media*, atau *Jurnal Nasional Terakreditasi SINTA 1/2*.
- **Target Praktisi Industri & Regulasi**:
  - *Security Briefing Paper* untuk asosiasi keamanan informasi dan tim tanggap insiden (CSIRT / SOC).
  - Panduan pencegahan penipuan deepfake finansial untuk edukasi publik.

---

### 17. Daftar Pustaka & Referensi Awal

1. Cialdini, R. B. (2021). *Influence, New and Expanded: The Psychology of Persuasion*. Harper Business.
2. Rossler, A., et al. (2019). *FaceForensics++: Learning to Detect Manipulated Facial Images*. IEEE International Conference on Computer Vision (ICCV).
3. Korshunov, P., & Marcel, S. (2022). *Deepfake Defense: Biometrics and Countermeasures in Voice and Video Clones*. ACM Computing Surveys.
4. Hadnagy, C. (2018). *Social Engineering: The Science of Human Hacking*. John Wiley & Sons.
5. MITRE ATT&CK Framework. (2024). *Techniques: Impersonation (T1656) & Phishing (T1566)*. MITRE Corporation.
6. Casey, E. (2011). *Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet*. Academic Press.
7. ISO/IEC 27037:2012. *Information technology — Security techniques — Guidelines for identification, collection, acquisition, and preservation of digital evidence*.

