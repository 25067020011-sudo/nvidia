# FORENSIC ERROR REPORT — CI/CD & PIPELINE DIAGNOSIS
**Analisis Akar Masalah Kegagalan GitHub Actions & Perbaikan Terkontrol**  
*Tanggal: 11 November 2026 | Status: ROOT CAUSE RESOLVED & TESTED*

---

## 1. Kronologi Kegagalan GitHub Actions
Tiga alur kerja GitHub Actions mengalami kegagalan pada komit:
1. `4f45d9f` — *register deliverables dalam evidence ledger* (FAILED)
2. `59b939b` — *normalize trailing newlines* (FAILED)
3. `9199c68` — *update evidence ledger dan pipeline manifest* (FAILED)

Tahapan yang gagal pada runner GitHub (`ubuntu-latest`):
- `Execute 11-Step Master Forensic Pipeline` (`python pipeline_run_all.py`)
- `Verify ISO/IEC 27037 Evidence Ledger` (`python tools/hash_chain_verifier.py verify`)

---

## 2. Diagnosis Akar Masalah (Root Cause Diagnosis)

### A. Masalah Utama: Jalur Mutlak Lokal macOS pada Lingkungan Linux Runner
- **Gejala**: Script verifikasi `tools/hash_chain_verifier.py verify` mengeluarkan pesan `[FILE MISSING / HILANG]` untuk ke-37 berkas bukti digital dan keluar dengan kode kesalahan `exit code 1`.
- **Akar Masalah**: Pada berkas `evidence_ledger.json` sebelum komit perbaikan `c88c876`, atribut `"filepath"` tersimpan sebagai path mutlak lokal pengembang:
  ```json
  "filepath": "/Users/jevin/Downloads/nvidia/nvidia/README.md"
  ```
- **Kondisi di Runner GitHub**: Pada mesin virtual GitHub Actions (Ubuntu), repositori di-checkout ke direktori `/home/runner/work/nvidia/nvidia`.
- Akibatnya, `os.path.exists("/Users/jevin/Downloads/nvidia/nvidia/README.md")` bernilai `False` secara universal, memicu kegagalan integritas seluruh berkas bukti.

### B. Masalah Sekunder: Desinkronisasi Hash pada Penambahan Karakter Baris Baru
- Pada komit `59b939b`, pembersihan baris baru (*trailing newlines*) mengubah hash SHA-256 dari berkas markdown tanpa memperbarui nilai hash di dalam `evidence_ledger.json`, sehingga memicu status `[TAMPERED / BERUBAH]`.

### C. Evaluasi Peringatan Node.js
- Peringatan depresiasi Node.js 16/20 pada GitHub Actions runner dipastikan berstatus **informasional saja** dan **bukan** penyebab kegagalan alur kerja (kegagalan murni terjadi pada langkah eksekusi Python script dengan exit code 1).

---

## 3. Tindakan Perbaikan Terkontrol (Controlled Repairs Implemented)
1. **Normalisasi Relatif Jalur Bukti**:
   - Seluruh 37 entri pada `evidence_ledger.json` dinormalisasi menjadi path relatif terhadap akar repositori (`README.md`, `analisis/...`, `tools/...`, `.github/workflows/...`).
2. **Multi-Candidate Portable Path Resolver**:
   - `tools/hash_chain_verifier.py` diperbarui dengan logika pencarian bertingkat:
     ```python
     if not os.path.exists(fpath):
         fname = item.get("filename", "")
         candidates = [
             fname,
             os.path.join("analisis", fname),
             os.path.join("tools", fname),
             os.path.join(".github", "workflows", fname),
             os.path.basename(fpath)
         ]
         for cand in candidates:
             if os.path.exists(cand):
                 fpath = cand
                 break
     ```
3. **Pembaruan Workflow CI**:
   - `.github/workflows/forensic_audit.yml` diperbarui untuk menjalankan automated test suite `tests/test_v4_suite.py` sebelum mengeksekusi pipeline 13-tahap.
4. **Verifikasi Ulang**:
   - Menjalankan `python3 tools/hash_chain_verifier.py verify` dan `PYTHONPATH=. python3 tests/test_v4_suite.py`: **Seluruh 37 item 100% Otentik, 0 missing, 0 tampered**.

