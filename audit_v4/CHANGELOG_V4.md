# CHANGELOG — NVIDIA FORENSIC INTELLIGENCE PLATFORM

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.0.0] — 2026-11-11
### Major Architecture & Intelligence Platform Upgrade (v4.0)

#### Added
- **Econometric Event-Study Engine (`tools/event_study_analyzer.py`)**:
  - Implementasi formal model MacKinlay (1997) dengan jendela estimasi 20 hari bursa dan jendela peristiwa 14 hari bursa.
  - Perhitungan Abnormal Return ($AR$), Cumulative Abnormal Return ($CAR$), standard error, t-statistic, dan p-value ($p = 0.0087 < 0.01$).
  - Dekomposisi faktor perancu makro (guncangan regulasi izin data center pasca-pemilu 05 Nov: -12.14%) vs risiko tata kelola dewan (09 Nov: -1.61%).
- **Social Network Analysis Enhancements (`tools/sna_centrality_analyzer.py`)**:
  - Penambahan metrik Degree Centrality, In-Degree, Out-Degree, Closeness, dan PageRank untuk 20 aktor dan 10 media.
  - Implementasi algoritma deteksi komunitas Louvain / Modularity Clustering.
  - Perhitungan densitas graf global ($D$) dan timbal balik (*reciprocity*).
  - Ekspor edge list terarah (`analisis/sna_edgelist.csv`) dan ringkasan topologi (`analisis/sna_metrics_summary.json`).
- **5-Tier Truth Classification Taxonomy (`tools/tiered_truth_classifier.py`)**:
  - Transisi taksonomi menuju standar ontologi ilmiah: `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `DISPUTED`, dan `HYPOTHESIS`.
  - Penilaian bobot kredibilitas sumber primer resmi vs media massa vs media sosial.
- **Reportica Intelligence Reporting Module (`tools/reportica_intelligence_generator.py`)**:
  - Otomasi agregasi seluruh artefak menjadi laporan terpadu: `analisis/REPORTICA_INTELLIGENCE_BRIEF_V4.json` dan `analisis/REPORTICA_EXECUTIVE_SUMMARY_V4.md`.
- **Master Pipeline Rekayasa Ulang (`pipeline_run_all.py`)**:
  - Peningkatan menjadi 13 tahapan otomatis dengan penanganan eksepsi dan retry terukur.
  - Pencatatan terstruktur ganda: konsol dan berkas log permanen `pipeline_execution.log`.
  - Pelacakan eksekusi otomatis dengan luaran manifest JSON `pipeline_manifest.json`.
- **Automated Test Suite (`tests/test_v4_suite.py`)**:
  - 7 pengujian otomatis mencakup validasi sintaks AST Python, schema JSON, konsistensi CSV, integritas ledger SHA-256, model ekonometrika, dan heuristik deepfake.
- **Audit Dokumen Lengkap v4.0**:
  - `AUDIT_V4.md`, `SECURITY_AUDIT_V4.md`, `DATA_QUALITY_REPORT_V4.md`, `TEST_REPORT_V4.md`, `REPRODUCIBILITY_V4.md`, `CHANGELOG_V4.md`, dan `README_V4.md`.
- **Keamanan Docker Non-Root**:
  - Pembuatan akun terbatas `appuser` (UID 1001) pada `Dockerfile` untuk mematuhi prinsip least privilege.

#### Changed
- **Streamlit Dashboard (`app.py` & `streamlit_app.py`)**:
  - Desain antarmuka gelap (*dark intelligence theme*) modern cybersecurity.
  - Ekspansi dari 7 tab menjadi 9 tab modul komprehensif.
  - Perbaikan pemanggilan kolom DataFrame matriks SNA untuk mencegah KeyError.
  - Sinkronisasi instan dengan Streamlit Cloud.
- **Evidence Ledger (`evidence_ledger.json`)**:
  - Pembaruan ledger menjadi 37 item bukti digital dengan verifikasi SHA-256 100% utuh.

#### Fixed
- Memperbaiki peringatan submodule git tertanam `nvidia/` dengan menghapusnya dari index tracking (`git rm --cached nvidia`).
- Menambahkan modul `json` yang terlewat pada `tools/sna_centrality_analyzer.py`.
- Memperbaiki penanganan path file dan permission Streamlit saat diuji di lingkungan sandboxed.
