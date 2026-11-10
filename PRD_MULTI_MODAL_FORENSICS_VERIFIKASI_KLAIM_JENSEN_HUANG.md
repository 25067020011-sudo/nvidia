# PRD & KERANGKA PENELITIAN FORENSIK DIGITAL (VERSI 3.0 - GROUND TRUTH RELEASE)
## Verifikasi Forensik Digital Klaim Viral Tokoh Publik: Dekonstruksi Klaim "Serangan Fisik", Manipulasi Deepfake, dan Rantai Narasi Digital (Studi Kasus: Jensen Huang / NVIDIA)

---

| Parameter Dokumen | Spesifikasi Teknis |
| :--- | :--- |
| **Kode Dokumen** | `PRD-FDC-JH-03` |
| **Versi Dokumen** | `3.0 (Ground Truth & Fact-Verification Edition)` |
| **Fokus Keilmuan** | *Multi-Modal Digital Forensics, OSINT Verification, & Social Media Network Analysis* |
| **Orientasi Etika** | *Verifikasi Klaim Viral Tokoh Publik & Integritas Informasi (Bukan Investigasi Privasi)* |
| **Sistem Kebenaran** | *Tiered Truth Labeling System (Terkonfirmasi, Dilaporkan, Belum Terverifikasi, Palsu)* |

---

## 1. Matriks Verifikasi Fakta Lapangan (*Ground Truth Verification Matrix*)

Untuk mencegah misinformasi dan menjaga integritas akademis, penelitian ini menggunakan sistem label kebenaran 4-tingkat:

```
[ KLAIM VIRAL MASUK ]
          |
          +---> [ TERKONFIRMASI ]        : Didukung bukti primer resmi (SEC 8-K, siaran resmi, dokumen peradilan)
          +---> [ DILAPORKAN ]           : Diliput media pers kredibel, investigasi dewan/otoritas sedang berjalan
          +---> [ BELUM TERVERIFIKASI ]  : Beredar di ruang publik tanpa bukti rekaman otentik / data pengadilan
          +---> [ PALSU / FABRIKASI ]    : Terbukti rekayasa sintetis (deepfake), distorsi konteks, atau disinformasi
```

### Tabel Rangkuman Insiden Terverifikasi (Oktober - November 2026)

| Tanggal Kejadian | Peristiwa / Narasi Viral | Klaim yang Beredar di Publik | Hasil Verifikasi Forensik Lapangan | Status Kebenaran | Sumber Rujukan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **21 Okt 2026** | **Protes Keynote GTC Berlin** | *"Jensen Huang diserang secara fisik di atas panggung"* | **Distorsi Konteks.** Terjadi interupsi protes verbal (*heckling*) terkait isu penggunaan chip di drone perang. **Tidak ada kontak fisik atau serangan kekerasan.** | `PALSU (Klaim Fisik)` / `TERKONFIRMASI (Protes Verbal)` | [The Next Web](https://thenextweb.com/news/huang-gtc-berlin-keynote-protest-nvidia-chips-russian-drones) |
| **28 Okt 2026** | **Siaran Deepfake Kripto YouTube** | *"NVIDIA Live menyiarkan promo giveaway kripto resmi"* | **Serangan Digital Murni.** Akun YouTube dibajak/dibuat tiruan menyiarkan video deepfake AI Jensen Huang. Mencapai ~100.000 concurrent bot-viewers dengan overlay QR code penipuan. | `TERKONFIRMASI (Serangan Deepfake)` | [Tecnoblog](https://tecnoblog.net/noticias/transmissao-falsa-da-nvidia-engana-milhares-de-pessoas/) |
| **29 Okt 2026** | **Isu Spionase & Kontak Eksekutif** | *"Huang terlibat operasi spionase asing"* | **Tuduhan Intelijen Sedang Berjalan.** Otoritas memeriksa interaksi dengan eksekutif pihak ketiga (Alice Huang). NVIDIA secara resmi membantah anomali interaksi. | `DILAPORKAN` | [SiliconANGLE](https://siliconangle.com/?p=852455), [TweakTown](https://www.tweaktown.com/news/114387/nvidia-pushes-back-against-report-linking-ceo-jensen-huang-to-suspected-chinese-intelligence-asset/index.html) |
| **08 Nov 2026** | **Memo Internal & Evaluasi Dewan** | *"CEO mengakui perselingkuhan lewat memo internal"* | **Pengakuan Internal.** Memo pengakuan hubungan personal telah diedarkan; aspek implikasi keamanan nasional masih dalam audit dewan komisaris (*board of directors*). | `DILAPORKAN / TERKONFIRMASI (Memo)` | [Crypto Briefing](https://cryptobriefing.com/nvidia-ceo-jensen-huang-admits-infidelity-memo/) |
| **08 Nov 2026** | **Teori Konspirasi "Trump Dalang"** | *"Trump menjebak Huang untuk mengambil alih saham/kendali NVIDIA"* | **Spekulasi Tanpa Bukti (Disinformation/Conspiracy).** Penyelidikan terhadap Alice Huang telah dimulai sejak era Biden; Trump telah diberi taklimat setahun sebelumnya namun pasif. Trump justru secara terbuka membela Huang ("brilliant"). Inisiator isu adalah Menlu Marco Rubio dan faksi *China hawks*. | `BELUM TERVERIFIKASI / SPEKULATIF` | [The Daily Beast](https://www.thedailybeast.com/trumps-billionaire-pal-jensen-huang-targeted-in-mystery-woman-spy-plot), [The Hill](https://thehill.com/policy/technology/6181938-nvidia-huang-china-intelligence-report/amp/), [Crypto Briefing](https://cryptobriefing.com/trump-backs-nvidia-ceo-huang-china-spy-report/), [DNYUZ](https://dnyuz.com/2026/11/08/rubio-warned-officials-about-nvidia-chiefs-entanglement-with-chinese-spy/) |

---

## 2. Latar Belakang & Nilai Kebaruan Riset (*Research Novelty*)

### 2.1 Mengapa Klaim "Serangan Fisik" Menjadi Pintu Masuk Riset yang Sangat Kuat?
Fenomena beredarnya klaim *"Jensen Huang diserang fisik"* menunjukkan pola tipikal **Piramida Disinformasi Modern**:
1. **Benih Kejadian Riil (*Physical Trigger*)**: Protes verbal nyata di GTC Berlin (21 Okt).
2. **Amplifikasi Algoritma & Clickbait**: Akun media sosial mengeklaim terjadinya "serangan" tanpa kata "verbal".
3. **Konvergensi dengan Manipulasi Digital**: Munculnya video deepfake di platform video dan potongan gambar yang dimanipulasi (*out of context keyframes*).
4. **Hasil Akhir**: Opini publik mengonsumsi narasi fiktif bahwa telah terjadi serangan fisik terhadap pimpinan korporasi.

Penelitian ini membedah **bagaimana sebuah insiden fisik minor (protes verbal) ditransformasikan menjadi narasi serangan hibrida** melalui saluran digital, serta bagaimana alat forensik digital dapat membuktikannya secara matematis dan prosedural.

### 2.2 Dekomposisi Jaringan Aktor & Analisis Motif Kepentingan
Untuk menjaga objektivitas ilmiah dan mencegah atribusi spekulatif, dinamika kasus didekonstruksi ke dalam 4 kuadran pemangku kepentingan:
1. **Komite Direktur Independen NVIDIA**: Menjalankan mekanisme kepatuhan tata kelola luar biasa (*extraordinary event-driven action*) yang dibantu penasihat hukum eksternal independen. Berdasarkan audit historis SEC EDGAR 20 tahun (2006–2026), investigasi tingkat dewan hanya terjadi 2 kali (2006 terkait akuntansi opsi saham, dan 2026 terkait perilaku pribadi CEO). CEO tetap menjabat penuh selama evaluasi berlangsung.
2. **Aparatur Intelijen & Pembocor Anonim**: Pengawasan terhadap perantara perdagangan luar negeri telah berlangsung lintas periode kepresidenan. Pembocoran memo kepada media investigasi dipicu oleh perbedaan pandangan kebijakan terkait penegakan batas ekspor chip canggih, bukan konspirasi pengambilalihan korporasi.
3. **Komite Pengawasan Legislatif (Kongres AS)**: Menjalankan fungsi pengawasan keamanan nasional terkait rantai pasok dan transfer teknologi kecerdasan buatan.
4. **Entitas Perantara Perdagangan**: Berfokus pada dinamika akses pasokan teknologi dan arah kebijakan pembatasan semikonduktor.

*Pedoman Metodologis*: Aspek-aspek tanpa atribusi publik resmi (seperti identitas spesifik pembocor dokumen internal) wajib diklasifikasikan sebagai variabel anonim/tidak terverifikasi, bukan diisi dengan spekulasi konspiratif.

### 2.3 Uji Hipotesis Distraksi / Pengalihan Isu (*Diversionary Hypothesis Test*)
Munculnya spekulasi bahwa insiden ini merupakan "rekayasa pengalihan isu" (*false flag / distraction tactic*) diuji secara empiris melalui analisis garis waktu multi-faktor:
1. **Disinsentif Elektoral**: Laporan bocor ke publik pada 29 Oktober 2026 (hanya lima hari menjelang Pemilu Sela AS 3 November). Muatan laporan justru menyorot kelemahan penanganan keamanan pihak eksekutif petahana, yang berujung pada kekalahan elektoral besar ("Blue Wave"). Merancang pengalihan isu yang merugikan posisi politik sendiri menjelang hari pemungutan suara tidak memiliki rasionalitas operasional.
2. **Karakteristik Penurunan Pasar Modal (5 Nov vs. 9 Nov)**:
   - *5 November 2026*: Kejatuhan saham NVDA (-9.26%) dan indeks Nasdaq 100 (kehilangan $\approx \$2.5\text{ Triliun}$) merupakan respon makro terhadap ekspektasi regulasi pembatasan pembangunan pusat data AI dan pengembangan model kecerdasan buatan pasca-kemenangan legislatif Demokrat.
   - *9 November 2026*: Reaksi pasar pasca-pengakuan memo personal Jensen Huang ditandai lonjakan volume transaksi masif (459,1 Juta lembar) yang mencerminkan kekhawatiran atas risiko tata kelola kepemimpinan (*executive governance risk*) menjelang rilis laporan keuangan 17 November.
3. **Kesimpulan Empiris**: Kasus ini bukan pengalihan isu rekayasa tunggal, melainkan bagian dari pertarungan strategis jangka panjang seputar kontrol ekspor teknologi semikonduktor canggih dan friksi kebijakan luar negeri.

---

## 3. Rumusan Masalah (Research Questions) & Hipotesis

- **RQ-1 (Verifikasi Multimodal Media)**: Bagaimana kombinasi teknik ekstraksi *Keyframe Error Level Analysis (ELA)*, spektrum audio vocoder, dan analisis ketidaksesuaian temporal mampu membuktikan kepalsuan video deepfake siaran langsung dan potongan klip viral?
- **RQ-2 (Jejaring Propagasi Narasi)**: Bagaimana pola penyebaran klaim viral (dari protes verbal menjadi hoaks serangan fisik) di platform media sosial (X/YouTube/TikTok) saat dipetakan menggunakan analisis jejaring sosial (*Social Network Analysis - SNA*)?
- **RQ-3 (Rantai Integritas Bukti - Chain of Custody)**: Bagaimana merancang kerangka kerja verifikasi bukti terbuka (*Open-Source Fact-Checking Framework*) yang memenuhi standar integritas forensik ISO/IEC 27037 tanpa melanggar privasi subjek penelitian?

---

## 4. Sumber Data & Korpus Penelitian (*Forensic Datasets & Ground Truth*)

```
                                  [ KORPUS DATASET PENELITIAN ]
                                                |
        +-----------------------+---------------+-----------------------+
        |                       |                                       |
        v                       v                                       v
[ 1. DATA PRIMER RESMI ]  [ 2. MEDIA & ARSIP SEJARAH ]    [ 3. DATA SOSIAL MEDIA ]
- SEC EDGAR (Form 8-K)    - GDELT Project BigQuery        - X (Twitter) Historical API
- Newsroom Resmi NVIDIA   - Media Cloud Narrative DB      - YouTube Data API v3
- Transkrip Resmi Keynote - Wayback Machine & Archive.today- TikTok Research API
        |                       |                                       |
        +-----------------------+---------------+-----------------------+
                                                |
                                                v
                        +-----------------------------------------------+
                        | 4. BENCHMARK DEEPFAKE & PEMBANDING KONTROL    |
                        | - Kontrol Asli : Keynote resmi YouTube NVIDIA |
                        | - Dataset Latih: FaceForensics++, DFDC,       |
                        |   Celeb-DF v2, DeeperForensics, FakeAVCeleb   |
                        +-----------------------------------------------+
```

### Peralatan & Toolkit Forensik yang Digunakan:
1. **InVID-WeVerify**: Ekstraksi keyframe video, reverse image search multi-mesin (Google Lens, TinEye, Yandex).
2. **ExifTool**: Audit metadata EXIF, encoding profile, dan integritas kontainer video.
3. **FotoForensics**: Error Level Analysis (ELA) untuk mendeteksi penempelan/komposisi elemen visual palsu.
4. **Spectral Audio Analyzer (Python/Librosa)**: Visualisasi spektrogram MFCC untuk mendeteksi *neural vocoder artifacts*.
5. **Gephi / NetworkX**: Analisis graf jaringan aktor penyebar hoaks pertama (*patient zero analysis*).

---

## 5. Taksonomi Metodologi Penelitian

```mermaid
flowchart TD
    subgraph Tahap 1: Ekstraksi Ground Truth & Preservasi
        A1["Koleksi Pengumuman Resmi SEC EDGAR & Newsroom"] --> A2["Penetapan SHA-256 Hash Setiap Bukti Mentah"]
        A2 --> A3["Pengarsipan via Wayback Machine / Archive.today"]
    end

    subgraph Tahap 2: Verifikasi Forensik Multimodal
        B1["Uji Video Deepfake YouTube (FaceForensics++/FakeAVCeleb)"] --> B2["Analisis ELA Foto/Tangkapan Layar Klip Viral"]
        B2 --> B3["Audit Spektrum Suara Keynote Asli vs Video Kloning"]
    end

    subgraph Tahap 3: Analisis Propagasi & Rekonstruksi Narasi
        C1["Query GDELT & Media Cloud (Framing Berita)"] --> C2["SNA di X/YouTube API: Pelacakan Sumber Pertama (Patient Zero)"]
        C3["Koreksi Fakta Bertingkat (Tiered Truth Classification)"]
    end

    Tahap 1 --> Tahap 2 --> Tahap 3
```

---

## 6. Batasan Etika Penelitian & Aturan Atribusi Ketat

1. **Prinsip *"Public Claim Verification, Not Personal Life Probe"***:
   - Penelitian **hanya menguji kebenaran klaim viral dan manipulasi informasi teknis**.
   - Penelitian **tidak melakukan investigasi terhadap ranah kehidupan pribadi, keluarga, atau perselingkuhan subjek**. Data memo hanya dirujuk sebatas dokumen resmi yang memengaruhi tata kelola korporasi (*corporate governance*) dan verifikasi klaim dewan.
2. **Chain of Custody & Immutability**:
   - Seluruh artefak (video, tangkapan layar, tweet) wajib disimpan bersama nilai hash SHA-256 dan timestamp akuisisi untuk memastikan keabsahan di hadapan peer-reviewer akademis.
3. **Perlindungan Terhadap Pihak yang Disebutkan**:
   - Nama individu non-publik yang muncul dalam live chat atau komentar publik disamarkan (*anonymized*).

---

## 7. Rencana Kerja & Deliverables Repositori

```
nvidia/
├── README.md                                          # Panduan Navigasi Repositori
├── PRD_MULTI_MODAL_FORENSICS_VERIFIKASI_KLAIM_JENSEN_HUANG.md # PRD Master v3.0
├── PRD_CYBER_PHYSICAL_BEHAVIORAL_FORENSICS.md         # Kerangka Cyber-Physical v2.0
├── PRD_BEHAVIORAL_DIGITAL_FORENSICS_LAYER8_NVIDIA.md  # Kerangka Layer 8 v1.0
└── tools/                                             # Skrip Forensik & Verifikasi
    ├── hash_verifier.py                               # Preservasi SHA-256
    └── spectral_deepfake_check.py                     # Skrip Analisis Spektrogram
```

