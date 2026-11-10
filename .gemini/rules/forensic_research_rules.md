---
description: Aturan Baku Riset Forensik Digital, Etika Atribusi, dan Integritas Rantai Bukti ISO/IEC 27037
globs: ["*"]
---

# ATURAN BAKU RISET FORENSIK DIGITAL & TATA KELOLA REPOSITORI (WORKSPACE RULES)

Setiap agen AI yang bekerja di dalam repositori ini **WAJIB MEMATUHI** aturan-aturan berikut:

---

## 1. ATURAN ATRIBUSI ENTITAS NYATA (STRICT ATTRIBUTION GATE)
1. **Status Korban**: Jensen Huang dan NVIDIA Corporation adalah **korban imitasi tanpa hak (*unauthorized impersonation*) dan rekayasa deepfake**. Dalam keadaan apa pun, dilarang menuliskan Jensen Huang atau NVIDIA sebagai subjek pelaku penipuan siber.
2. **Nomenklatur Pelaku**: Pihak penyerang siaran YouTube Live palsu atau pembuat kampanye penipuan kripto wajib disebut secara netral forensik: *"Operator Kanal Belum Teridentifikasi"* atau *"Aktor Ancaman Siber (UNC-CP-01)"*.
3. **Penyensoran Privasi (PII Redaction)**: Identitas pribadi non-publik (alamat dompet kripto audiens, nama akun live chat, atau pihak ketiga non-korporasi) wajib disamarkan (*anonymized*) sesuai prinsip UU PDP dan GDPR.

---

## 2. PRINSIP RUANG LINGKUP PENELITIAN
1. **Fokus pada Integritas Informasi**: Riset ini berfokus pada **verifikasi klaim viral publik, rekayasa media sintetis (deepfake audio/visual), dan manipulasi kognitif Layer 8**.
2. **Tidak Melakukan Penyelidikan Kehidupan Pribadi**: Peneliti dan agen dilarang menyelidiki kehidupan pribadi individu. Dokumen memo internal hanya dianalisis sebatas dokumen korporasi yang memengaruhi tata kelola pasar (*corporate governance*) dan evaluasi dewan direksi.

---

## 3. TAKSONOMI KEBENARAN BERTINGKAT (TIERED TRUTH SYSTEM)
Setiap analisis klaim wajib menggunakan 4 label standar:
- **CONFIRMED (Terkonfirmasi)**: Didukung dokumen primer resmi (SEC EDGAR Form 10-K/8-K, siaran resmi, dokumen hukum).
- **REPORTED (Dilaporkan)**: Diliput media jurnalisme investigatif kredibel, namun masih dalam proses audit independen.
- **UNVERIFIED / SPECULATIVE (Belum Terverifikasi)**: Beredar di ruang publik atau media sosial tanpa dokumen penguat (termasuk teori konspirasi politik).
- **FABRICATED / DISINFORMATION (Palsu/Distorsi Total)**: Terbukti merupakan distorsi konteks total (misal: klaim "serangan fisik") atau manipulasi sintetis (deepfake).

---

## 4. INTEGRITAS RANTAI BUKTI DIGITAL (ISO/IEC 27037:2012)
1. **Pendaftaran Hash Kriptografis**: Setiap berkas dataset baru (`.csv`), naskah publikasi (`.md`), atau laporan audit (`.json`) wajib didaftarkan ke dalam `evidence_ledger.json` menggunakan skrip `tools/hash_chain_verifier.py`.
2. **Audit Periodik**: Sebelum melakukan `git commit` atau mempublikasikan hasil temuan, jalankan verifikasi integritas:
   ```bash
   python tools/hash_chain_verifier.py verify
   ```
   Seluruh berkas bukti harus berstatus `[VERIFIED / OTENTIK]` (100% utuh).

---

## 5. ORIENTASI DEFENSIF MURNI (DEFENSIVE SECURITY ONLY)
- Repositori ini berorientasi pada **forensik pertahanan (*blue team defense*)**, pemulihan reputasi, dan perlindungan eksekutif (*Executive CSOC Defense Playbook*).
- Dilarang membuat, memodifikasi, atau membagikan skrip pembuatan deepfake yang dapat dieksploitasi untuk penipuan aktif (*no weaponized code generation*).

