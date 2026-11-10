# Riset Forensik Digital & Verifikasi Klaim: Kasus Ekosistem Narasi Jensen Huang (NVIDIA)

Repositori ini memuat kerangka penelitian (*Research PRD*), metodologi pengujian, korpus dataset, serta instrumen forensik digital untuk memverifikasi klaim viral seputar **serangan fisik vs. serangan digital (deepfake & disinformasi)** yang menargetkan figur publik pimpinan teknologi global (Jensen Huang / NVIDIA).

---

## 📌 Dokumen Penelitian Utama

| Versi Dokumen | Nama Dokumen | Fokus Utama | Tautan Berkas |
| :--- | :--- | :--- | :--- |
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
1. **Verifikasi Media Multimodal**: InVID-WeVerify, FotoForensics (Error Level Analysis), ExifTool.
2. **Benchmark Deepfake**: FaceForensics++, DFDC, Celeb-DF v2, FakeAVCeleb.
3. **Data Primer & Pelacakan Narasi**: SEC EDGAR (Form 8-K), GDELT Project, Media Cloud, Wayback Machine, X API (SNA).
