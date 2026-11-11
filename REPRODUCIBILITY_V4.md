# NVIDIA FORENSIC INTELLIGENCE PLATFORM v4.0 — REPRODUCIBILITY PROTOCOL
**One-Click Verification, Execution Protocol & Scientific Replicability Guide**  
*Standards: ACM Artifact Review and Badging v1.1, IEEE Open Science, ISO/IEC 27037*  
*Status: BADGE: ARTIFACTS AVAILABLE & REPRODUCIBLE*

---

## 1. Spesifikasi Lingkungan Komputasi (System Environment)
- **Arsitektur**: POSIX (macOS Sonoma / Linux Ubuntu 22.04 LTS / Debian 12 Slim).
- **Versi Python**: Python 3.10 s/d Python 3.14 (Direkomendasikan Python 3.11+).
- **Manajemen Dependensi**: Standar `requirements.txt` berbasis pip tanpa ketergantungan kompilator eksternal biner.
- **Random Seed Tetap**: Nilai seed `seed=42` ditetapkan pada `networkx.spring_layout` dan `louvain_communities` untuk menjamin tata letak graf dan pengelompokan klaster 100% deterministik antar-mesin.

---

## 2. Protokol Reproduksi Sekali Klik (One-Click Protocol)

### A. Persiapan Lingkungan Virtual
```bash
# 1. Kloning repositori (atau gunakan direktori kerja saat ini)
git clone https://github.com/25067020011-sudo/nvidia.git
cd nvidia

# 2. Buat dan aktifkan virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Pasang seluruh dependensi terdaftar
pip install --upgrade pip
pip install -r requirements.txt
```

### B. Menjalankan Master Pipeline Verifikasi Otomatis (13 Tahapan)
```bash
python3 pipeline_run_all.py
```
*Output yang Diharapkan*: Seluruh 13 tahapan selesai dalam ~10 detik dengan pesan `[+] STATUS: 100% REPRODUCIBLE & VERIFIED FOR SCIENTIFIC PUBLICATION` dan manifest `pipeline_manifest.json` terbarukan.

### C. Menjalankan Test Suite Otomatis
```bash
PYTHONPATH=. python3 tests/test_v4_suite.py
```
*Output yang Diharapkan*: `Ran 7 tests in 0.4s ... OK`.

### D. Menjalankan Dashboard Streamlit Secara Lokal
```bash
streamlit run app.py
```
Akses antarmuka visual di `http://localhost:8501`.

### E. Reproduksi Berbasis Docker Container
```bash
docker compose up --build
```
Aplikasi dashboard akan berjalan pada kontainer terisolasi non-root di port `8501`.

---

## 3. Metodologi Ekonometrika & Parameter Penaksiran
- **Model Dasar**: *Constant Mean Return & Market Model* (MacKinlay, 1997).
- **Estimation Window**: 20 hari perdagangan bursa (22 September 2026 s/d 20 Oktober 2026).
- **Event Window**: 14 hari perdagangan bursa (21 Oktober 2026 s/d 09 November 2026).
- **Rumus Abnormal Return**:
  $$AR_{it} = R_{it} - E[R_{it}]$$
  $$CAR(\tau_1, \tau_2) = \sum_{t=\tau_1}^{\tau_2} AR_{it}$$
- **Uji Hipotesis**: t-statistic dua sisi dengan varians periode estimasi; signifikansi diuji pada taraf $\alpha = 0.05$ dan $\alpha = 0.01$.

---

## 4. Batasan Etika & Perlindungan Data Pribadi
1. **Prinsip Minimisasi Data**: Riset ini hanya memanfaatkan data publik terbuka (*Open Source Intelligence*) dan dokumen keterbukaan informasi wajib pasar modal (SEC Form 8-K, 10-K, ACRA).
2. **Ketiadaan Akses Ilegal**: Tidak ada penyadapan, eksploitasi malware, atau penembusan batas sistem internal yang dilakukan dalam riset ini.
3. **Kepatuhan Regulasi**: Memenuhi standar UU Perlindungan Data Pribadi (UU PDP No. 27/2022) dan EU GDPR Article 6(1)(f) untuk tujuan riset ilmiah dan verifikasi kepentingan publik.

