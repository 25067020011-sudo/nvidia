# PANDUAN SIMULASI LATIHAN TANGGAP INSIDEN KRISIS (TABLETOP DRILL / TTX)
## Skenario Uji Kesiapan CSOC, Legal, & PR dalam Menghadapi Ancaman Hibrida (Deepfake, Disinformasi Fisik, & Isu Regulasi)
**Standar Acuan**: NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide), ISO/IEC 27035, ISO/IEC 27037

---

### TUJUAN LATIHAN
Menguji koordinasi lintas fungsi antara **Converged Security Operations Center (CSOC)**, **Tim Legal & Kepatuhan**, **Hubungan Masyarakat (Corporate Communications / PR)**, dan **Executive Protection** dalam merespons krisis informasi hibrida berlapis waktu nyata (*near real-time*).

---

### SKENARIO 1: PEMBAJAKAN KANAL & SIARAN LANGSUNG DEEPFAKE EKSEKUTIF
* **Waktu Latihan**: $T+0$ hingga $T+60$ menit.
* **Situasi Injeksi**:
  - Akun YouTube bajakan bernama "NVIDIA Live" menyiarkan video deepfake AI Jensen Huang mengumumkan program penggandaan mata uang kripto dengan kode QR dinamis.
  - Penonton dimanipulasi mencapai 100.000 bot bersamaan untuk mengeksploitasi bias otoritas (*Authority Bias*).
* **Tindakan yang Diuji**:
  1. *Deteksi (Menit 0–15)*: Pemantauan brand abuse oleh tim CTI, verifikasi ketiadaan tanda tangan kriptografis C2PA pada media stream.
  2. *Mitigasi (Menit 15–30)*: Koordinasi takedown darurat melalui kanal eskalasi resmi YouTube Trust & Safety dan abuse report Google.
  3. *Komunikasi Publik (Menit 30–45)*: Penerbitan peringatan penipuan (*scam alert*) di media sosial resmi dan newsroom resmi korporasi untuk memutus siklus korban quishing.
  4. *Preservasi Bukti (Menit 45–60)*: Perekaman bukti digital (URL, dompet kripto tujuan, metadata stream) dengan hash SHA-256 sesuai ISO/IEC 27037.

---

### SKENARIO 2: DISTORSI INSIDEN FISIK PANGGUNG MENJADI HOAKS "SERANGAN FISIK"
* **Waktu Latihan**: $T+0$ hingga $T+120$ menit.
* **Situasi Injeksi**:
  - Di sebuah konferensi industri (misal: Computex/GTC), terjadi interupsi verbal (*heckling*) selama 30 detik oleh aktivis.
  - Dalam waktu 45 menit, klip video tanpa suara beredar di X dan TikTok dengan takarir viral: *"CEO DISERANG SECARA FISIK DI PANGGUNG OLEH PENYUSUP"*.
  - Saham korporasi mulai mengalami tekanan volatilitas di sesi perdagangan pre-market.
* **Tindakan yang Diuji**:
  1. *Konfirmasi Lapangan (Menit 0–10)*: Tim pengamanan fisik eksekutif mengonfirmasi tidak ada kontak fisik, cedera, atau senjata.
  2. *Pencegahan Kekosongan Informasi (Menit 10–30)*: Tim PR segera merilis pernyataan klarifikasi faktual 1 paragraf (*Fact-Check Dispatch*) sebelum rumor masuk ke terminal berita finansial (Bloomberg/Reuters).
  3. *Rilis Klip Utuh Bersegel C2PA (Menit 30–60)*: Merilis video rekaman resmi sudut lebar (*wide-angle*) dengan audio utuh yang memperlihatkan aktivis dikawal keluar tanpa kontak fisik.

---

### SKENARIO 3: PEMBOCORAN MEMO INTERNAL & PENYELIDIKAN REGULASI EKSPOR
* **Waktu Latihan**: $T+0$ hingga $T+24$ jam.
* **Situasi Injeksi**:
  - Media investigasi merilis laporan bahwa distributor pihak ketiga sedang diperiksa intelijen terkait ekspor chip canggih, dan kontak CEO tersadap insidental.
  - Sebuah memo personal internal bocor ke outlet media finansial 5 hari menjelang pengumuman laporan keuangan kuartalan (*earnings call*).
* **Tindakan yang Diuji**:
  1. *Aktivasi Komite Independen Dewan (Jam 0–4)*: Dewan komisaris membentuk komite khusus independen dibantu penasihat hukum luar untuk menjamin kepatuhan fidusia pemegang saham.
  2. *Keterbukaan Informasi Pasar (Jam 4–12)*: Menilai materialitas pengungkapan di bawah SEC Regulation FD dan menyiapkan pengarsipan Form 8-K transparan untuk meredam diskon tata kelola (*governance discount*).
  3. *Komunikasi Internal Karyawan (Jam 12–24)*: Menyampaikan arahan tegas kepada seluruh pimpinan divisi mengenai kepatuhan kerahasiaan dagang dan kesinambungan roadmap teknologi.

---

### INDIKATOR KEBERHASILAN LATIHAN (KPI METRICS)
1. **Mean Time to Detect (MTTD)**: Deteksi siaran palsu $< 15$ menit.
2. **Mean Time to Takedown (MTTT)**: Pemutusan siaran jahat $< 45$ menit.
3. **Truth Pre-emption Ratio**: Keberhasilan merilis klarifikasi fakta sebelum rumor masuk ke sindikasi media arus utama.

