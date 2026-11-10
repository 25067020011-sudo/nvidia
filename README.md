# Riset Forensik Digital & Verifikasi Klaim: Kasus Ekosistem Narasi Jensen Huang (NVIDIA)

Repositori ini memuat kerangka penelitian (*Research PRD*), metodologi pengujian, korpus dataset, serta instrumen forensik digital untuk memverifikasi klaim viral seputar **serangan fisik vs. serangan digital (deepfake & disinformasi)** yang menargetkan figur publik pimpinan teknologi global (Jensen Huang / NVIDIA).

---

## 📌 Dokumen Penelitian Utama

| Versi Dokumen | Nama Dokumen | Fokus Utama | Tautan Berkas |
| :--- | :--- | :--- | :--- |
| **SOP Tanggap Insiden** | **Playbook Penanganan Insiden Layer 8 & Deepfake** | Panduan operasional standar (NIST SP 800-61 / ISO 27035) untuk CSOC, Legal, dan PR dalam menangani disinformasi fisik, deepfake siaran langsung, dan penipuan phygital. | [`SOP_PENANGANAN_INSIDEN_LAYER8_DEEPFAKE.md`](./SOP_PENANGANAN_INSIDEN_LAYER8_DEEPFAKE.md) |
| **Laporan Investigasi** | **Laporan Resmi Penyelidikan Forensik Digital & Audit** | Laporan formal komprehensif (Executive Summary, Ground Truth Matrix, Audit Keterbukaan SEC 20 Tahun, Hasil Korpus 300 Berita, Event-Study Saham, Rekomendasi CSOC). | [`LAPORAN_HASIL_INVESTIGASI_FORENSIK.md`](./LAPORAN_HASIL_INVESTIGASI_FORENSIK.md) |
| **Slide Eksekutif** | **Presentasi Hasil Riset Forensik (Deck)** | Ringkasan 9 slide siap saji untuk sidang skripsi/tesis, presentasi dewan, atau konferensi ilmiah (latar belakang, metodologi, temuan empiris, event study, dan rekomendasi). | [`PRESENTASI_HASIL_RISET_FORENSIK.md`](./PRESENTASI_HASIL_RISET_FORENSIK.md) |
| **Manuskrip Ilmiah** | **Naskah Draft Artikel Jurnal (IMRaD)** | Format baku artikel ilmiah (Abstrak, Pendahuluan, Metodologi, Hasil Empiris 300 Berita, Event-Study Saham, dan Pembahasan). Siap untuk diseminasi akademis/tesis. | [`MANUSCRIPT_VERIFIKASI_KLAIM_JENSEN_HUANG.md`](./MANUSCRIPT_VERIFIKASI_KLAIM_JENSEN_HUANG.md) |
| **Versi 3.0 (Master)** | **Multi-Modal Forensics & Fact-Checking Framework** | *Ground truth verification*, dekonstruksi klaim serangan fisik (protes verbal Berlin) vs. serangan digital nyata (deepfake siaran YouTube), analisis propagasi jejaring sosial (SNA), dan korpus data primer. | [`PRD_MULTI_MODAL_FORENSICS_VERIFIKASI_KLAIM_JENSEN_HUANG.md`](./PRD_MULTI_MODAL_FORENSICS_VERIFIKASI_KLAIM_JENSEN_HUANG.md) |
| **Versi 2.0** | **Cyber-Physical & Behavioral Forensics** | Kerangka konvergensi keamanan fisik dan siber (CISA/ASIS standard), analisis phygital (QR quishing), dan mesin korelasi stempel waktu (*temporal alignment*). | [`PRD_CYBER_PHYSICAL_BEHAVIORAL_FORENSICS.md`](./PRD_CYBER_PHYSICAL_BEHAVIORAL_FORENSICS.md) |
| **Versi 1.0** | **Behavioral Digital Forensics Layer 8** | Analisis psikologi rekayasa sosial, eksploitasi bias otoritas (*authority bias*), dan rantai serangan manipulasi kognitif korban. | [`PRD_BEHAVIORAL_DIGITAL_FORENSICS_LAYER8_NVIDIA.md`](./PRD_BEHAVIORAL_DIGITAL_FORENSICS_LAYER8_NVIDIA.md) |

---

## 🔍 Matriks Fakta Lapangan (*Ground Truth Matrix*)

| Tanggal | Peristiwa Lapangan | Status Verifikasi | Catatan Forensik |
| :--- | :--- | :--- | :--- |
| **21 Okt 2026** | Protes Keynote GTC Berlin | `PALSU (Serangan Fisik)` / `TERKONFIRMASI (Protes Verbal)` | Protes verbal aktivis terkait chip drone; **tidak ada serangan fisik**. |
| **28 Okt 2026** | Siaran Kloning AI di YouTube | `TERKONFIRMASI (Serangan Deepfake)` | Kanal bajakan menyiarkan video deepfake AI dengan ~100k penonton bot & QR penipuan. |
| **29 Okt 2026** | Isu Kontak & Spionase | `DILAPORKAN (Dalam Audit Dewan)` | Laporan dugaan spionase; NVIDIA membantah anomali interaksi. |
| **08 Nov 2026** | Memo Internal Perusahaan | `TERKONFIRMASI (Memo)` | Memo internal pimpinan korporasi beredar dan diakui. |

---

## 🛠️ Toolkit & Korpus Verifikasi
1. **Master Pipeline Otomatis**: Jalankan seluruh rangkaian audit & analisis dalam 1 klik via [`pipeline_run_all.py`](./pipeline_run_all.py).
2. **Verifikasi Media Multimodal**: InVID-WeVerify, FotoForensics (Error Level Analysis), ExifTool.
3. **Benchmark Deepfake**: FaceForensics++, DFDC, Celeb-DF v2, FakeAVCeleb.
4. **Data Primer & Pelacakan Narasi**: SEC EDGAR (Form 8-K / 10-K), GDELT Project, Media Cloud, Wayback Machine, X API (SNA).

---

## 📊 Visualisasi Analisis Forensik Media & Ekonometrika
- [`analisis/01_timeline.png`](./analisis/01_timeline.png): Garis waktu volume pemberitaan harian (puncak 30 Oktober 2026).
- [`analisis/02_media_teratas.png`](./analisis/02_media_teratas.png): 20 media teratas yang mempublikasikan isu skandal.
- [`analisis/03_bahasa.png`](./analisis/03_bahasa.png): Distribusi bahasa artikel berita internasional.
- [`analisis/04_klaim.png`](./analisis/04_klaim.png): Sebaran kategori klaim di judul dan URL berita.
- [`analisis/05_saham_event_study.png`](./analisis/05_saham_event_study.png): Analisis event-study fluktuasi saham NVDA vs. kalender peristiwa makro.
- [`analisis/07_network_graph_betweenness.png`](./analisis/07_network_graph_betweenness.png): Peta Social Network Analysis (SNA) sentralitas perantara (*Betweenness Centrality*) 20 aktor & 10 media teratas.
- [`analisis/01_timeline_kemunculan_pertama.csv`](./analisis/01_timeline_kemunculan_pertama.csv): Matriks kronologi kemunculan pertama lintas platform (Juni 2024 - Nov 2026).
- [`analisis/02_status_klaim.csv`](./analisis/02_status_klaim.csv): Matriks evaluasi klaim kunci via Tiered Truth Engine (Serangan Fisik, Deepfake YouTube, Teori Trump Dalang, Teori Musk Dalang).
- [`analisis/matriks_sna_20_aktor.csv`](./analisis/matriks_sna_20_aktor.csv): Skor Betweenness, In-Degree, PageRank, dan Closeness untuk 20 aktor utama.
- [`analisis/matriks_sna_10_media.csv`](./analisis/matriks_sna_10_media.csv): Skor Betweenness Centrality untuk 10 media arus utama.
- [`analisis/08_komparasi_metode_intelijen.csv`](./analisis/08_komparasi_metode_intelijen.csv): Komparasi 9 dimensi ontologis intelijen: SIGINT Unmasking (FISA 702) vs Spyware Komersial (Pegasus / MVT) vs HUMINT (Honeytrap/Social Engineering).
- [`analisis/09_osint_artefak.csv`](./analisis/09_osint_artefak.csv): Katalog 11 artefak publik OSINT lengkap dengan status verifikasi, metodologi forensik, dan pemetaan tool spesifik.
- [`evidence_ledger.json`](./evidence_ledger.json): Manifest rantai integritas bukti digital berstandar ISO/IEC 27037:2012 (17 item terverifikasi SHA-256).
