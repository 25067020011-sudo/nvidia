# REKAYASA & PERBAIKAN LOG (CHANGE LOG) v4.0
**Proyek:** NVIDIA Multimodal Forensic Intelligence Platform  
**Rilis:** v4.0 (Autonomous Engineering & Controlled Repair)  
**Tanggal:** 2026-11-11  
**Repositori:** `https://github.com/25067020011-sudo/nvidia` (Branch: `main`)  
**Metodologi:** ISO/IEC 27037:2012, NIST SP 800-86, GitOps, Zero Trust  

---

## 1. Ikhtisar Perubahan

Rilis ini menyelesaikan investigasi akar penyebab kegagalan CI/CD GitHub Actions pada commit `9199c68`, `59b939b`, dan `4f45d9f`, menormalkan format bukti forensik, memperkuat keamanan kontainer dan repository, memvalidasi 100% integritas bukti SHA-256, serta menyusun automated test suite dan dokumentasi audit standar publikasi.

---

## 2. Rincian Perubahan per Komponen

### A. CI/CD & GitHub Actions Workflow (`.github/workflows/forensic_audit.yml`)
- **Perbaikan**: Mengganti step eksekusi pipeline lama dari script statis ke Master 13-Step Automated Pipeline (`pipeline_run_all.py`).
- **Verifikasi Kriptografis Otomatis**: Menambahkan step verifikasi hash chain ISO/IEC 27037 (`tools/hash_chain_verifier.py verify`).
- **Unit Test Runner**: Menambahkan step eksekusi test suite otomatis (`python3 -m unittest discover tests`).
- **Robust Path Resolution**: Memastikan CI runner Ubuntu Linux (`/home/runner/work/nvidia/nvidia`) dapat mengeksekusi pipeline dan validasi ledger tanpa kegagalan path macOS lokal.

### B. Evidence Ledger (`evidence_ledger.json`)
- **Normalisasi Path Absolut ke Relatif**: 
  - Masalah: File sebelumnya menyimpan path absolut lokal host (`/Users/jevin/Downloads/...`), menyebabkan `os.path.exists` bernilai `False` pada GitHub Actions runner.
  - Perbaikan: Semua 37 entri file dinormalkan menjadi path relatif terhadap root repositori (misalnya `analisis/nvda_skandal.csv`, `tools/event_study_analyzer.py`).
- **Verifikasi SHA-256 100%**: 
  - Mengonfirmasi seluruh 37 hash SHA-256 yang tersimpan cocok secara biner dengan berkas fisik repositori.

### C. Hash Chain Verifier (`tools/hash_chain_verifier.py`)
- **Multi-Candidate Path Resolution Engine**:
  - Ditambahkan fallback cerdas untuk mencari lokasi berkas pada:
    1. `REPO_ROOT / filepath` (jalur relatif resmi)
    2. `REPO_ROOT / filename` (root repositori)
    3. `REPO_ROOT / 'analisis' / filename`
    4. `REPO_ROOT / 'tools' / filename`
- **Toleransi Cross-Platform**: Mencegah kegagalan verifikasi akibat perbedaan format direktori di Windows, macOS, dan Linux.

### D. Keamanan & Konfigurasi Lingkungan (`Dockerfile`, `.env.example`, `.gitignore`)
- **Docker Hardening**:
  - `Dockerfile` dikonfigurasi dengan user non-root `appuser` (UID 1001, GID 1001).
  - Ditambahkan direktori konfigurasi eksplisit `MPLCONFIGDIR=/tmp/matplotlib` untuk mencegah crash permission pada runtime tanpa hak tulis root.
  - Membatasi surface attack kontainer sesuai prinsip Least Privilege (NIST SP 800-190).
- **Secret Management**:
  - Menambahkan template konfigurasi lingkungan `.env.example`.
  - Memperbarui `.gitignore` dengan aturan isolasi secret `.env`, `*.env`, `.venv/`, `.pytest_cache/`, `*.pyc`.

### E. Automated Test Suite (`tests/`)
- **Pembuatan Suite Pengujian Mandiri**:
  - `tests/test_v4_suite.py`: 7 skenario pengujian komprehensif (Syntax AST, JSON Schema, CSV Structure, Evidence Ledger Hash, Event Study Math, Deepfake Heuristics, Streamlit Import).
  - `tests/step4_audit.py`: Skrip audit kriptografis ISO/IEC 27037.
  - `tests/step5_dataset_audit.py`: Skrip validasi struktural dataset.
  - `tests/step8_dashboard_test.py`: Skrip validasi integrasi data loader dashboard.

### F. Pelaporan Mutu & Kesiapan Publikasi (Quality Gate Reports)
- `audit_report.md`: Laporan audit komprehensif arsitektur repositori, dependensi, dan kualitas ilmiah.
- `forensic_error_report.md`: Analisis investigatif kegagalan CI/CD GitHub Actions commit `9199c68`, `59b939b`, `4f45d9f`.
- `evidence_integrity_report.json`: Manifest digital verifikasi kriptografis 37 bukti ISO/IEC 27037:2012.
- `security_audit_report.md`: Laporan audit postur keamanan siber, pemindaian kredensial, dan mitigasi kontainer.
- `test_results.md`: Laporan eksekusi pengujian 100% lulus.
- `change_log.md`: Berkas pencatatan riwayat rekayasa dan perbaikan teknis.

---

## 3. Komparasi Status Sebelum & Sesudah Audit

| Parameter | Kondisi Awal (v3.0 / Commit `9199c68`) | Kondisi Terkini (v4.0 Terverifikasi) |
|---|---|---|
| **Status CI/CD GitHub Actions** | GAGAL (Exit Code 1 di Ubuntu Runner) | **LULUS (Jalur relatif & verifier cerdas)** |
| **Pathing Evidence Ledger** | Path absolut lokal macOS | **Path relatif portabel cross-platform** |
| **Otentisitas SHA-256 Bukti** | Terancam broken path di CI | **100% Terverifikasi (37/37 Berkas)** |
| **Test Suite Otomatis** | Tidak ada file pengujian unit | **Lengkap (`unittest discover tests` lulus)** |
| **Izin Kontainer Docker** | Default Root | **Non-root `appuser` (UID 1001)** |
| **Penanganan Kredensial** | Tidak ada template `.env` | **`.env.example` & `.gitignore` terproteksi** |
| **Reproducibility Pipeline** | Manual per sub-skrip | **13-Tahap otomatis via `pipeline_run_all.py`** |

