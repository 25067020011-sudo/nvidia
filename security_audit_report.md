# SECURITY AUDIT REPORT — NVIDIA FORENSIC INTELLIGENCE PLATFORM
**Evaluasi Keamanan Statis, Pemindaian Rahasia, dan Pengerasan Kontainer**  
*Standar: NIST SP 800-61 Rev. 2, OWASP Top 10, CWE / SANS Top 25*  
*Tanggal: 11 November 2026 | Status Keamanan: SECURE & HARDENED*

---

## 1. Pemindaian Kredensial & Rahasia Statis
- **Metode**: Pemindaian ekspresi reguler berbasis pola terhadap kunci privat RSA/EC, token API (`sk-`, `ghp_`, `gho_`), dan penetapan kredensial teks biasa.
- **Temuan**:
  - Direktori Inti Proyek (`tools/`, `analisis/`, `app.py`, `pipeline_run_all.py`, dataset, dokumentasi): **0 Kredensial Ditemukan (100% Bersih)**.
  - Direktori Pihak Ketiga (`mvt/tests/`): Ditemukan 8 penanda kata sandi tiruan (*mock dummy passwords* untuk pengujian parser backup telepon). Tidak ada data kredensial nyata.
- **Tindakan Pencegahan**: Berkas `.env.example` telah dibuat sebagai panduan konfigurasi aman, dan berkas `.gitignore` telah ditambahkan aturan pengabaian `.env` dan `*.env`.

---

## 2. Keamanan Eksekusi Subproses (CWE-78)
- Seluruh pemanggilan proses eksternal pada `pipeline_run_all.py` menggunakan format berbasis daftar argumen:
  `subprocess.run([python_bin, "tools/event_study_analyzer.py"], ...)`
- Penggunaan `shell=True` dengan interpolasi string masukan ditiadakan secara menyeluruh, menghilangkan risiko serangan *Command Injection*.

---

## 3. Keamanan Path Traversal & Manipulasi Berkas (CWE-22)
- Pembacaan dan penulisan berkas pada modul analitis dibatasi pada direktori terotentikasi (`analisis/`, `audit_v4/`).
- Validasi keberadaan berkas menggunakan `os.path.exists()` tanpa resolusi path traversal arbitrer (`../`).

---

## 4. Pengerasan Kontainer Docker
- `Dockerfile` menerapkan prinsip hak akses terendah (*Principle of Least Privilege*):
  - Pengguna terbatas non-root dibuat dengan ID `appuser` (UID: 1001).
  - Kontainer dialihkan menggunakan direktif `USER appuser`.
  - Pengecekan kesehatan kontainer terintegrasi via port 8501.

