# 🛡️ NVIDIA MULTIMODAL FORENSIC INTELLIGENCE PLATFORM v4.0
**Pusat Riset Forensik Digital, Dekonstruksi Disinformasi & Ekonometrika Tata Kelola Korporasi**  
*Studi Kasus: Ekosistem Narasi Jensen Huang & NVIDIA Corporation (Oktober–November 2026)*

[![Master Pipeline](https://img.shields.io/badge/Pipeline-13%2F13%20Passed-brightgreen)](pipeline_run_all.py)
[![ISO/IEC 27037](https://img.shields.io/badge/Evidence%20Ledger-37%20Items%20SHA--256-blue)](evidence_ledger.json)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit%20Cloud-Live%20Dashboard-orange)](https://nvidia-jasonhuang.streamlit.app/)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-100%25%20Verified-success)](REPRODUCIBILITY_V4.md)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 📌 Ringkasan Eksekutif Platform
**NVIDIA Forensic Intelligence Platform v4.0** adalah platform riset terpadu yang menggabungkan teknik forensik digital multimodal (*audio, visual, metadata EXIF/ELA, C2PA*), analisis jejaring sosial (*SNA*), dan pemodelan ekonometrika *event-study* (MacKinlay 1997) untuk mengaudit kebenaran klaim viral, ancaman siber hibrida, serta respon pasar modal terkait CEO NVIDIA Jensen Huang pada kuartal akhir 2026.

Platform ini mematuhi standar internasional:
- **ISO/IEC 27037:2012**: Preservasi dan integritas bukti digital menggunakan rantai hash ganda SHA-256 & MD5.
- **NIST SP 800-86 & NIST SP 800-61 Rev. 2**: Kerangka kerja integrasi teknik forensik pada manajemen insiden siber.
- **C2PA (Coalition for Content Provenance and Authenticity)**: Pengujian tanda tangan kriptografis media sintetis.

---

## 🏛️ Arsitektur 10 Modul Intelijen (Platform Components)
1. **OSINT Intelligence**: Pengelolaan dan verifikasi 11 artefak data terbuka (LinkedIn, ACRA Singapore, X, press briefing, memo dewan).
2. **AI Fact Checking (5-Tier Truth Engine)**: Mesin klasifikasi bertingkat (`VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `DISPUTED`, `HYPOTHESIS`).
3. **Digital Evidence Ledger**: Pencatatan 37 artefak bukti digital dengan audit integritas kriptografis mandiri.
4. **Deepfake Analysis & ELA**: Deteksi anomali kompresi JPEG (Error Level Analysis), inspeksi metadata EXIF/IPTC, dan deteksi vocoder Wav2Lip.
5. **Social Network Analysis (SNA)**: Pemodelan graf terarah 20 aktor dan 10 media (Betweenness Centrality, Degree, PageRank, dan deteksi komunitas Louvain).
6. **Temporal Intelligence**: Garis waktu kronologis multi-tahap pelopor kemunculan narasi dari media sosial hingga sindikasi pers global.
7. **NVDA Econometric Event Study**: Penaksiran Abnormal Return ($AR$) dan Cumulative Abnormal Return ($CAR$) dengan uji signifikansi statistik ($t$-stat, $p < 0.01$) serta dekomposisi faktor perancu makro vs tata kelola.
8. **Reportica Intelligence Reporting**: Pembangkit laporan intelijen otomatis berbasis mesin (JSON) dan ringkasan eksekutif C-Suite (Markdown).
9. **Streamlit Intelligence Dashboard**: Dashboard interaktif berbasis Streamlit (`app.py` & `streamlit_app.py`) dengan visualisasi dark-theme profesional.
10. **Academic Research Export**: Penyediaan artefak siap publikasi jurnal internasional (LaTeX IEEEtran, BibTeX, CodeMeta v2.0, CITATION.cff).

---

## 🚀 Panduan Mulai Cepat (Quickstart Guide)

### 1. Instalasi Dependensi
```bash
git clone https://github.com/25067020011-sudo/nvidia.git
cd nvidia
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Eksekusi Master Pipeline (One-Click)
```bash
python3 pipeline_run_all.py
```
*Pipeline akan mengeksekusi 13 tahapan verifikasi secara otomatis, mencatat log terstruktur di `pipeline_execution.log`, dan menghasilkan manifest di `pipeline_manifest.json`.*

### 3. Menjalankan Automated Test Suite
```bash
PYTHONPATH=. python3 tests/test_v4_suite.py
```

### 4. Menjalankan Dashboard Streamlit
```bash
streamlit run app.py
```
Akses antarmuka visual di: `http://localhost:8501` atau kunjungi versi cloud di:  
👉 **[https://nvidia-jasonhuang.streamlit.app/](https://nvidia-jasonhuang.streamlit.app/)**

### 5. Menjalankan via Docker
```bash
docker compose up --build
```

---

## 📊 Temuan Kunci Riset Empiris
1. **0% Bukti Serangan Fisik**: Dari korpus 300 artikel berita (212 media internasional, 15 bahasa), **tidak ada satupun laporan serangan fisik**. Kejadian sesungguhnya di GTC Berlin (21 Okt) adalah interupsi verbal damai aktivis energi.
2. **Serangan Kloning Deepfake Nyata**: Siaran langsung YouTube (28 Okt) terbukti merupakan kampanye penipuan siber menggunakan media sintetis generatif tanpa manifest C2PA, disertai manipulasi ~100.000 penonton bot untuk mempromosikan penipuan kripto ber-QR code.
3. **Pemisahan Risiko Saham**: Penurunan tajam saham NVDA (-12.14% pada 05 Nov) dipicu oleh sentimen makro regulasi energi/data center pasca-pemilu sela AS, sedangkan memo dewan (09 Nov) hanya menyumbang -1.61% dengan lonjakan volume transaksi 459M lembar saham ($CAR = -14.502\%, p = 0.0087$).
4. **Pembantahan Teori Dalang Elon Musk**: Saling ketergantungan modal ekonomi riil (Tesla belanja $10 Miliar chip NVIDIA; xAI komitmen $20 Miliar superkomputer Colossus 2) secara rasional membantah keterlibatan Musk sebagai perancang krisis. Pihak yang secara faktual memperoleh keuntungan lobi adalah faksi *China-hawks* di Kongres AS.

---

## 📑 Dokumentasi Audit Lengkap (v4.0)
- [`AUDIT_V4.md`](AUDIT_V4.md): Audit teknis menyeluruh kode sumber dan pipeline.
- [`SECURITY_AUDIT_V4.md`](SECURITY_AUDIT_V4.md): Audit keamanan, SAST scan, dan hardening kontainer Docker.
- [`DATA_QUALITY_REPORT_V4.md`](DATA_QUALITY_REPORT_V4.md): Laporan kualitas data, kurasi korpus $N=300$, dan integritas SHA-256.
- [`TEST_REPORT_V4.md`](TEST_REPORT_V4.md): Laporan eksekusi unit test dan end-to-end pipeline.
- [`REPRODUCIBILITY_V4.md`](REPRODUCIBILITY_V4.md): Protokol reproduksi ilmiah lengkap.
- [`CHANGELOG_V4.md`](CHANGELOG_V4.md): Riwayat pembaruan arsitektural platform v4.0.

---

## ⚖️ Etika & Lisensi
Riset ini diselenggarakan untuk tujuan verifikasi kebenaran informasi publik, riset keamanan siber, dan analisis tata kelola korporasi dengan mematuhi prinsip etika riset akademis, UU Perlindungan Data Pribadi (UU PDP No. 27/2022), dan GDPR.  
Didistribusikan di bawah Lisensi **MIT**.
