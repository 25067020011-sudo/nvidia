# STANDAR OPERASIONAL PROSEDUR (SOP) TANGGAP DARURAT INSIDEN
## Penanganan Disinformasi Figur Publik, Impersonasi Deepfake AI, dan Rekayasa Sosial Layer 8
**Standar Acuan:** NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide) & ISO/IEC 27035

---

| Dokumen SOP | Keterangan Teknis |
| :--- | :--- |
| **Nomor Dokumen** | `SOP-CSOC-L8-001` |
| **Klasifikasi** | *Enterprise Defense & Incident Response Playbook* |
| **Sasaran Pengguna** | Tim Keamanan Informasi (CSOC), Legal Counsel, Hubungan Masyarakat (PR/IR) |
| **Versi** | `1.0 (Operasional)` |

---

## 1. TUJUAN & RUANG LINGKUP

SOP ini mengatur tata cara penanganan terkoordinasi ketika pimpinan eksekutif korporasi atau figur publik organisasi menjadi target dari:
1. **Disinformasi Viral Insiden Fisik** (klaim penyerangan, kekerasan, atau cedera fisik di ruang publik/konferensi).
2. **Impersonasi Media Sintetis (Deepfake)** (kloning suara, video palsu panggung, atau rekayasa siaran langsung / *live streaming*).
3. **Rekayasa Sosial Terpadu (Layer 8 / Phygital)** (skema quishing QR code, penipuan finansial, atau manipulasi opini pasar).

---

## 2. MATRIKS TINGKAT KEGAWATAN INSIDEN (*SEVERITY MATRIX*)

| Tingkat Kegawatan | Kriteria Indikator | Waktu Tanggap Maksimal (SLA) | Penanggung Jawab Tindakan |
| :--- | :--- | :---: | :--- |
| **LEVEL 1 (Kritis)** | - Video deepfake siaran langsung disaksikan $>10.000$ audiens aktif.<br>- Penipuan finansial / QR code aktif memakan korban.<br>- Narasi serangan fisik memicu volatilitas harga saham $>5\%$. | $\le 15\text{ Menit}$ | *Incident Commander*, CISO, General Counsel, Head of IR |
| **LEVEL 2 (Tinggi)** | - Beredar potongan klip manipulatif audio/video di media sosial.<br>- Pelaporan sepihak oleh media pers independen tanpa konfirmasi resmi.<br>- Munculnya isu pelanggaran hukum/etik personal eksekutif. | $\le 1\text{ Jam}$ | Tim CSOC, Legal Specialist, Media Relations Officer |
| **LEVEL 3 (Sedang)** | - Interupsi fisik minor (protes verbal di panggung tanpa kekerasan).<br>- Rumor awal di forum daring sebelum diliput media arus utama. | $\le 4\text{ Jam}$ | Tim Keamanan Fisik Venue, Intelijen Ancaman Siber (CTI) |

---

## 3. ALUR KERJA TANGGAP DARURAT 4 FASE (INCIDENT WORKFLOW)

```
[ FASE 1: DETEKSI & TRIAGE ] 
  - Monitoring media sosial & sinyal CTI (alerting deepfake/quishing)
  - Klasifikasi kegawatan insiden (Level 1 / 2 / 3)
                   |
                   v
[ FASE 2: ISOLASI & PRESERVASI BUKTI ]
  - Perekaman streaming mentah & penguncian hash SHA-256 (ISO/IEC 27037)
  - Notifikasi takedown darurat ke tim keamanan platform (YouTube/X/Meta)
                   |
                   v
[ FASE 3: VERIFIKASI MULTIMODAL & ATRIBUSI ]
  - Uji laboratorium spektrum audio & inkonsistensi biometrik wajah
  - Pencocokan terhadap arsip rekaman kontrol resmi organisasi
                   |
                   v
[ FASE 4: KOMUNIKASI PUBLIK & PEMULIHAN ]
  - Rilis pernyataan pers resmi dan pengungkapan regulator (SEC Form 8-K)
  - Pelaporan aparat penegak hukum & evaluasi pasca-insiden (PIR)
```

---

## 4. INSTRUKSI KERJA TEKNIS DETAIL

### 4.1 Langkah Triage & Penghentian Cepat (*Rapid Containment*)
1. **Penghentian Aliran Trafik Palsu**:
   - Kirimkan permintaan *Emergency Copyright / Impersonation Takedown* melalui kanal prioritas platform penyedia siaran (*Trust & Safety Escalate Channel*).
   - Lampirkan sertifikat hash berkas resmi keynote asli sebagai bukti kepemilikan hak cipta (*Ground Truth Verification*).
2. **Penanganan Vektor Finansial / Phygital**:
   - Jika terdapat kode QR atau wallet penipuan, lakukan penandaan (*flagging*) alamat dompet kripto ke penyedia analitik blockchain (*Chainalysis, Elliptic, TRM Labs*) sebagai *Fraudulent Scam Wallet*.

### 4.2 Prosedur Komunikasi Publik & Pasar Modal
1. **Prinsip *"Single Source of Truth"***:
   - Hanya satu kanal resmi (Newsroom Korporasi / Investor Relations) yang berhak mengeluarkan bantahan atau klarifikasi.
   - Jangan membagikan ulang (*re-tweet/re-post*) video deepfake penyerang karena justru memperluas jangkauan algoritma.
2. **Klarifikasi Narasi Distorsi Fisik**:
   - Publikasikan rekaman utuh panggung tanpa suntingan (*unedited continuous master clip*) yang membuktikan subjek dalam kondisi aman dan tidak mengalami kekerasan fisik.

### 4.3 Evaluasi Pasca-Insiden (*Post-Incident Review - PIR*)
- Dalam waktu maksimal $3 \times 24\text{ jam}$ pasca-penutupan insiden, tim gabungan wajib menerbitkan:
  1. *Forensic Timeline Reconstruction Report*.
  2. Perhitungan taksiran dampak reputasi dan finansial.
  3. Pembaruan kamus deteksi pada modul pemantauan intelijen media (*Threat Intelligence Feed*).

