# PEER-REVIEW SUBMISSION & REPRODUCIBILITY CHECKLIST
## Scientific Artifacts and Computational Verification Standard
**Target Venues**: IEEE Transactions on Information Forensics and Security, ACM CCS, USENIX Security, IEEE S&P  
**Standard**: ACM Artifact Review and Badging v1.1 / IEEE Reproducibility Guidelines

---

### 1. REPRODUCIBILITY & ARTIFACT AVAILABILITY
- [x] **Complete Computational Pipeline**: Automated 1-click execution via `pipeline_run_all.py` (11 sequential verification steps).
- [x] **Cryptographic Evidence Ledger**: All 27+ evidence files registered with dual hash (SHA-256 and MD5) in `evidence_ledger.json` complying with ISO/IEC 27037:2012.
- [x] **Containerization Support**: `Dockerfile` and `docker-compose.yml` provided for environment-agnostic execution on Linux/macOS/Windows.
- [x] **Continuous Integration (CI)**: GitHub Actions workflow (`.github/workflows/forensic_audit.yml`) automatically executes and verifies the entire pipeline on every push.
- [x] **Live Interactive Dashboard**: Publicly hosted web application running on Streamlit Community Cloud (`app.py` / `streamlit_app.py`).

---

### 2. DATASETS & OPEN SCIENCE STANDARDS
- [x] **News Corpus Integrity**: 300 verified international articles (`berita_skandal_jensen_huang.csv`) spanning 212 media outlets and 15 languages with uniform keyword categorization.
- [x] **Financial Market Data**: Complete OHLCV time-series for NVDA (`nvda_skandal.csv`) spanning Sep 22 – Nov 11, 2026.
- [x] **Social Network Analysis Matrices**: Betweenness, In-Degree, PageRank, and Closeness centrality metrics for 20 actors and 10 media outlets.
- [x] **OSINT Catalog**: 11 public artifacts (`analisis/09_osint_artefak.csv`) with verified provenance, EXIF/ELA status, and primary reporting URLs.
- [x] **Open Science Citation Metadata**: `CITATION.cff` and `codemeta.json` configured for Zenodo/DOI registration.

---

### 3. METHODOLOGICAL & ETHICAL COMPLIANCE
- [x] **Strict Attribution Gate**: CEO Jensen Huang and NVIDIA Corporation consistently framed as victims of impersonation, synthetic media quishing, and narrative distortion.
- [x] **No Private Data Intrusion**: OSINT strictly confined to public artifacts, government corporate registries (Singapore ACRA), and mainstream media records without probing private communications.
- [x] **Double-Blind Review Compatibility**: LaTeX manuscript (`manuscript.tex`) and Markdown draft structured for easy anonymization upon request.
- [x] **Theoretical Alignment**: Integrated recent communications scholarship on the *Branding Iceberg* and *Silent Authority* paradigm (Sari, Prasetio, & Subroto, IPSSJ 2026).

