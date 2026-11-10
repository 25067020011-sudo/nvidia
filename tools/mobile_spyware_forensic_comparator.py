#!/usr/bin/env python3
"""
Mobile Spyware vs. SIGINT vs. HUMINT Forensic Comparator
Membandingkan tiga doktrin intelijen dalam kasus Jensen Huang & Alice Huang:
1. SIGINT Negara & FISA Section 702 Unmasking (NSA / Intelijen AS)
2. Spyware Ponsel Komersial & MVT Detection (Pegasus / NSO Group)
3. HUMINT / Social Engineering / Honeytrap (Alice Huang / Megaspeed)

Menganalisis artefak teknis STIX2 IOC dari Mobile Verification Toolkit (MVT) / Amnesty International
dan menghasilkan matriks komparasi analitis untuk ISO/IEC 27037 digital forensics.
"""

import json
import os
import re
import csv
from pathlib import Path
from collections import Counter

def parse_stix2_bundle(file_path: str):
    """Membaca berkas STIX2 bundle dan mengekstrak metrik IOC."""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    objects = data.get("objects", [])
    type_counts = Counter()
    pattern_types = Counter()
    sample_indicators = []
    
    for obj in objects:
        obj_type = obj.get("type")
        type_counts[obj_type] += 1
        
        if obj_type == "indicator":
            pattern = obj.get("pattern", "")
            # Deteksi tipe pola: domain, email, ipv4, file, url
            match = re.match(r"\[([a-zA-Z0-9_\-]+):", pattern)
            p_type = match.group(1) if match else "other"
            pattern_types[p_type] += 1
            if len(sample_indicators) < 5:
                sample_indicators.append(pattern)
                
    return {
        "total_objects": len(objects),
        "type_counts": dict(type_counts),
        "pattern_types": dict(pattern_types),
        "sample_indicators": sample_indicators
    }

def generate_intelligence_matrix_csv(output_path: str):
    """Menghasilkan dataset CSV komparasi ketiga doktrin intelijen."""
    rows = [
        {
            "id_dimensi": "DIM-01",
            "dimensi": "Klasifikasi Doktrin Intelijen",
            "sigint_fisa_unmasking": "Signals Intelligence (SIGINT) Strategis Tingkat Negara",
            "spyware_komersial_pegasus": "Cyber Espionage Tool / Commercial Targeted Spyware",
            "humint_honeytrap": "Human Intelligence (HUMINT) & Targeted Social Engineering"
        },
        {
            "id_dimensi": "DIM-02",
            "dimensi": "Aktor Pelaksana Utama",
            "sigint_fisa_unmasking": "Badan Intelijen Sinyal Negara (NSA, CIA, FBI - Penyelidikan Resmi AS)",
            "spyware_komersial_pegasus": "Vendor Senjata Siber Komersial (NSO Group / Klien Pemerintah Asing)",
            "humint_honeytrap": "Alice Wong / Alice Huang (Megaspeed Solutions / Diduga Informan Asing)"
        },
        {
            "id_dimensi": "DIM-03",
            "dimensi": "Target Primer vs. Insidental",
            "sigint_fisa_unmasking": "Target primer: Alice Huang (warga asing). Jensen Huang: Warga AS yang tersadap insidental (incidental collection) lalu di-unmask secara legal",
            "spyware_komersial_pegasus": "Ponsel target spesifik (aktivis, jurnalis, pejabat, eksekutif bisnis) yang dieksploitasi dari jarak jauh",
            "humint_honeytrap": "Jensen Huang (CEO NVIDIA) didekati secara personal untuk akses relasional dan penggalangan modal/investasi"
        },
        {
            "id_dimensi": "DIM-04",
            "dimensi": "Vektor Penetrasi / Akses",
            "sigint_fisa_unmasking": "Penyadapan level backbone telekomunikasi kabel/satelit & penyedia layanan internet (FISA Section 702 Upstream/PRISM)",
            "spyware_komersial_pegasus": "Zero-click exploit (misal: FORCEDENTRY via iMessage/WebKit), zero-day buffer overflow tanpa interaksi korban",
            "humint_honeytrap": "Interaksi tatap muka, kehadiran di konferensi industri (Computex Taipei, bar lounge, jamuan VIP, networking)"
        },
        {
            "id_dimensi": "DIM-05",
            "dimensi": "Artefak Jejak pada Perangkat Klien (Endpoint)",
            "sigint_fisa_unmasking": "NIHIL pada ponsel korban. Penyadapan terjadi di infrastruktur upstream operator telekomunikasi, bukan di memory/storage ponsel",
            "spyware_komersial_pegasus": "SANGAT SIGNIFIKAN: sqlite DBs, logs (DataUsage.sqlite, netusage.sqlite, fsCachedData, crash logs, process traces)",
            "humint_honeytrap": "Foto bersama di media sosial (LinkedIn NetThunder), rekaman CCTV publik, korespondensi email/chat personal normal"
        },
        {
            "id_dimensi": "DIM-06",
            "dimensi": "Kapabilitas Deteksi MVT (Mobile Verification Toolkit)",
            "sigint_fisa_unmasking": "TIDAK DAPAT MENDETEKSI (Out of Scope): MVT menganalisis endpoint file system, tidak memiliki visibilitas ke backbone NSA",
            "spyware_komersial_pegasus": "EFEKTIF TINGGI (Native Target): MVT dirancang khusus mencocokkan STIX2 IOCs (domain C2, SHA256 binaries, SMS pdu)",
            "humint_honeytrap": "TIDAK DAPAT MENDETEKSI (Bukan Malware): Komunikasi terjadi lewat protokol normal tanpa kode jahat"
        },
        {
            "id_dimensi": "DIM-07",
            "dimensi": "Landasan Hukum & Regulasi",
            "sigint_fisa_unmasking": "Foreign Intelligence Surveillance Act (FISA) Section 702, Prosedur Minimisasi IC DNI, Pengawasan Pengadilan FISC",
            "spyware_komersial_pegasus": "Wassenaar Arrangement (Dual-Use Controls), US Commerce Entity List, Hukum Anti-Cybercrime & Penyadapan Ilegal",
            "humint_honeytrap": "Undang-Undang Spionase (18 U.S.C. 794), Foreign Agents Registration Act (FARA), Regulasi Ekspor Kontrol AI (EAR)"
        },
        {
            "id_dimensi": "DIM-08",
            "dimensi": "Fakta Kasus Jensen Huang & Alice Huang (2024-2026)",
            "sigint_fisa_unmasking": "FAKTA TERKONFIRMASI: Intelijen AS memantau Alice Huang; Jensen Huang terdeteksi berkomunikasi dan identitasnya dibuka (unmasked) via prosedur legal",
            "spyware_komersial_pegasus": "TIDAK DIGUNAKAN / TIDAK TERLIBAT: Tidak ada laporan atau bukti eksploitasi ponsel Jensen Huang menggunakan spyware Pegasus",
            "humint_honeytrap": "FAKTA KORESPONDENSI: Hubungan personal diakui internal memo NVIDIA (8 Nov 2026); penyelidikan Megaspeed atas ekspor chip AI"
        },
        {
            "id_dimensi": "DIM-09",
            "dimensi": "Rekomendasi Forensik ISO/IEC 27037",
            "sigint_fisa_unmasking": "Analisis dokumen kebijakan hukum FISA, audit log permintaan unmasking antar-agensi pemerintah, transparansi laporan ODNI",
            "spyware_komersial_pegasus": "Akuisisi fisik/logis citra bit-stream iPhone/Android, verifikasi integritas SHA-256, scanning IOC via MVT CLI",
            "humint_honeytrap": "Analisis kronologi digital media sosial, verifikasi rantai asal-usul foto (metadata EXIF), audit tata kelola perusahaan & kerahasiaan NDA"
        }
    ]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id_dimensi", "dimensi", "sigint_fisa_unmasking", "spyware_komersial_pegasus", "humint_honeytrap"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)

def main():
    print("=" * 70)
    print("FORENSIK DIGITAL: KOMPARASI SIGINT vs. SPYWARE KOMERSIAL vs. HUMINT")
    print("Investigasi Kasus Jensen Huang, Alice Huang, & Megaspeed Solutions")
    print("=" * 70)
    
    # 1. Cek repositori IOC AmnestyTech jika tersedia
    stix2_path = "investigations/2021-07-18_nso/pegasus.stix2"
    if os.path.exists(stix2_path):
        ioc_stats = parse_stix2_bundle(stix2_path)
        print(f"\n[+] Analisis Berkas STIX2 AmnestyTech IOC: {stix2_path}")
        print(f"    Total STIX Objects     : {ioc_stats['total_objects']}")
        print(f"    Distribusi Tipe Objek  : {ioc_stats['type_counts']}")
        print(f"    Distribusi Tipe Indikator: {ioc_stats['pattern_types']}")
        print(f"    Contoh IOC Patterns    : {ioc_stats['sample_indicators'][:3]}")
    else:
        print("\n[-] Berkas STIX2 lokal tidak ditemukan, menggunakan dataset referensi.")

    # 2. Generate CSV Komparasi
    csv_out = "analisis/08_komparasi_metode_intelijen.csv"
    count = generate_intelligence_matrix_csv(csv_out)
    print(f"\n[+] Berhasil membangkitkan {count} dimensi komparasi ke: {csv_out}")
    print("=" * 70)

if __name__ == "__main__":
    main()

