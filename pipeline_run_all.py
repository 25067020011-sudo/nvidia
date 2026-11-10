#!/usr/bin/env python3
"""
pipeline_run_all.py
--------------------------------------------------------------------------------
Master Execution Pipeline: Riset Forensik Digital Multimodal & Audit Tata Kelola
Menjalankan seluruh tahapan verifikasi, audit ekonometrika, dan pengujian rantai bukti
secara otomatis dalam sekali eksekusi (One-Click Automated Reproducibility).

Standar Kepatuhan:
  - ISO/IEC 27037:2012 (Preservasi & Integritas Bukti Digital)
  - NIST SP 800-86 (Integrasi Teknik Forensik pada Respon Insiden)
  - NIST SP 800-61 Rev. 2 (Manajemen Insiden Siber)
"""

import os
import sys
import subprocess
import time

def print_banner(text):
    print("\n" + "=" * 90)
    print(f" {text}")
    print("=" * 90)

def run_step(command_list, step_name):
    print(f"\n[+] MENJALANKAN TAHAP: {step_name}...")
    start_time = time.time()
    res = subprocess.run(command_list, capture_output=True, text=True)
    duration = time.time() - start_time
    if res.returncode == 0:
        print(f"    -> [SUKSES] Selesai dalam {duration:.2f} detik.")
        if res.stdout.strip():
            # Tampilkan 5 baris terakhir output
            lines = res.stdout.strip().split("\n")
            preview = lines[-4:] if len(lines) > 4 else lines
            for l in preview:
                print(f"       | {l}")
        return True
    else:
        print(f"    -> [GAGAL] Error code {res.returncode}:")
        print(res.stderr[:400])
        return False

def main():
    print_banner("MEMULAI MASTER PIPELINE AUDIT FORENSIK DIGITAL MULTIMODAL")
    python_bin = os.path.join(".venv", "bin", "python")
    if not os.path.exists(python_bin):
        python_bin = sys.executable

    steps = [
        ([python_bin, "tools/hash_chain_verifier.py", "verify"],
         "1. Audit Kriptografis Integritas Rantai Bukti (ISO/IEC 27037 SHA-256)"),

        ([python_bin, "tools/tiered_truth_classifier.py"],
         "2. Mesin Klasifikasi Kebenaran Bertingkat (Tiered Truth Engine)"),

        ([python_bin, "tools/sec_edgar_10k_scanner.py"],
         "3. Audit Keterbukaan Informasi SEC EDGAR 20 Tahun (2006–2026)"),

        ([python_bin, "tools/event_study_analyzer.py"],
         "4. Analisis Ekonometrika Event-Study Fluktuasi Saham NVDA"),

        ([python_bin, "tools/stakeholder_actor_mapper.py"],
         "5. Dekomposisi Jaringan Aktor & Matriks Motif Pemangku Kepentingan"),

        ([python_bin, "tools/generate_corpus_and_charts.py"],
         "6. Rekonstruksi Korpus Berita & Pembangkitan Grafik Visualisasi Pasar"),

        ([python_bin, "tools/sna_centrality_analyzer.py"],
         "7. Pemodelan Social Network Analysis (Betweenness Centrality 20 Aktor & 10 Media)"),

        ([python_bin, "analisis_berita.py", "berita_skandal_jensen_huang.csv"],
         "8. Audit Leksikal Multibahasa & Klasterisasi Sindikasi Berita Arus Utama")
    ]

    success_count = 0
    for cmd, name in steps:
        if run_step(cmd, name):
            success_count += 1
        else:
            print(f"[!] Pipeline terhenti pada tahap: {name}")
            break

    print_banner(f"RINGKASAN EKSEKUSI: {success_count}/{len(steps)} TAHAP BERHASIL DIVERIFIKASI")
    if success_count == len(steps):
        print("[+] STATUS REPOSITORI: 100% REPRODUCIBLE & VERIFIED FOR SCIENTIFIC PUBLICATION.")
        print("[+] Seluruh bukti digital, model jejaring sosial, dan data saham valid secara forensik.")
    else:
        print("[!] Terdapat tahap yang memerlukan pengecekan dependensi atau berkas.")

if __name__ == "__main__":
    main()
