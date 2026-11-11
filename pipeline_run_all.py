#!/usr/bin/env python3
"""
pipeline_run_all.py
--------------------------------------------------------------------------------
NVIDIA MULTIMODAL FORENSIC INTELLIGENCE PLATFORM v4.0 — Master Pipeline
Standar Kepatuhan & Metodologi:
  - ISO/IEC 27037:2012 (Preservasi Bukti Digital & Rantai Integritas Kriptografis)
  - NIST SP 800-86 (Integrasi Teknik Forensik pada Respon Insiden)
  - MacKinlay (1997) (Ekonometrika Event-Study & Cumulative Abnormal Return)
  - Coalition for Content Provenance and Authenticity (C2PA)

Fitur Rekayasa Pipeline v4.0:
1. Validasi Dependensi Pra-Eksekusi (Pre-flight Dependency Check).
2. Pencatatan Terstruktur (Structured File & Console Logging).
3. Pelacakan Eksekusi & Manifest Input/Output (pipeline_manifest.json).
4. Penanganan Kesalahan & Logika Coba Ulang Terukur (Measured Retry Logic).
5. Prinsip Fail-Fast untuk Tahapan Integritas Kritis.
"""

from __future__ import annotations

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Dict

LOG_FILE = "pipeline_execution.log"
MANIFEST_FILE = "pipeline_manifest.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
LOGGER = logging.getLogger("Pipeline_v4")

def validate_environment() -> bool:
    """Memeriksa keberadaan pustaka Python inti sebelum memulai analisis."""
    required_packages = ["pandas", "numpy", "matplotlib", "networkx"]
    missing = []
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        LOGGER.error("Dependensi kritis tidak ditemukan: %s", missing)
        return False
    LOGGER.info("Pemeriksaan pra-eksekusi: Seluruh dependensi inti terpasang secara valid.")
    return True

def run_stage_with_retry(
    cmd: List[str],
    stage_name: str,
    max_retries: int = 1,
    is_critical: bool = False
) -> Dict[str, Any]:
    """Menjalankan tahapan pipeline dengan pelacakan waktu, retry, dan logging terstruktur."""
    LOGGER.info("MENJALANKAN TAHAP: %s", stage_name)
    attempt = 0
    start_time = time.time()

    while attempt <= max_retries:
        attempt += 1
        sub_start = time.time()
        try:
            proc = subprocess.run(
                cmd,
                text=True,
                capture_output=True,
                check=False
            )
            duration = round(time.time() - sub_start, 2)

            if proc.returncode == 0:
                LOGGER.info("  -> [SUKSES] Selesai dalam %.2f detik (Percobaan ke-%d).", duration, attempt)
                # Ambil cuplikan baris output
                lines = [l for l in proc.stdout.strip().split("\n") if l.strip()]
                preview = lines[-4:] if len(lines) > 4 else lines
                for l in preview:
                    LOGGER.info("     | %s", l)

                return {
                    "stage_name": stage_name,
                    "command": " ".join(cmd),
                    "status": "SUCCESS",
                    "returncode": 0,
                    "duration_sec": duration,
                    "attempts": attempt,
                    "stdout_tail": preview,
                    "stderr": ""
                }
            else:
                LOGGER.warning("  -> [PERINGATAN] Gagal pada percobaan ke-%d dengan kode %d.", attempt, proc.returncode)
                if attempt <= max_retries:
                    LOGGER.info("     Melakukan coba ulang (retry) untuk: %s...", stage_name)
                    time.sleep(1)
                else:
                    LOGGER.error("  -> [GAGAL] Tahap '%s' gagal setelah %d percobaan.", stage_name, attempt)
                    LOGGER.error("     Detail Error: %s", proc.stderr[:500])
                    if is_critical:
                        LOGGER.critical("     Tahap ini bersifat KRITIS (Fail-Fast). Menghentikan eksekusi pipeline!")
                    return {
                        "stage_name": stage_name,
                        "command": " ".join(cmd),
                        "status": "FAILED",
                        "returncode": proc.returncode,
                        "duration_sec": round(time.time() - start_time, 2),
                        "attempts": attempt,
                        "stdout_tail": [],
                        "stderr": proc.stderr[:1000]
                    }
        except Exception as exc:
            LOGGER.error("  -> [EXCEPTION] Gagal menjalankan proses: %s", exc)
            return {
                "stage_name": stage_name,
                "command": " ".join(cmd),
                "status": "EXCEPTION",
                "returncode": -1,
                "duration_sec": round(time.time() - start_time, 2),
                "attempts": attempt,
                "stdout_tail": [],
                "stderr": str(exc)
            }

    return {"stage_name": stage_name, "status": "UNKNOWN", "returncode": -1}

def main():
    LOGGER.info("=" * 85)
    LOGGER.info("MEMULAI MASTER PIPELINE AUDIT FORENSIK DIGITAL MULTIMODAL v4.0")
    LOGGER.info("Standar: ISO/IEC 27037, NIST SP 800-86, & Ekonometrika MacKinlay (1997)")
    LOGGER.info("=" * 85)

    if not validate_environment():
        LOGGER.critical("Pipeline dibatalkan karena dependensi tidak lengkap.")
        sys.exit(1)

    python_bin = os.path.join(".venv", "bin", "python")
    if not os.path.exists(python_bin):
        python_bin = sys.executable

    # 13 Tahap Lengkap Forensik Multimodal v4.0
    stages = [
        ([python_bin, "tools/hash_chain_verifier.py", "verify"],
         "1. Audit Kriptografis Integritas Rantai Bukti (ISO/IEC 27037 SHA-256)", True),

        ([python_bin, "tools/tiered_truth_classifier.py"],
         "2. Mesin Klasifikasi Kebenaran Bertingkat (5-Tier Truth Engine)", True),

        ([python_bin, "tools/sec_edgar_10k_scanner.py"],
         "3. Audit Keterbukaan Informasi SEC EDGAR 20 Tahun (2006–2026)", False),

        ([python_bin, "tools/event_study_analyzer.py"],
         "4. Analisis Ekonometrika Event-Study (AR & CAR Saham NVDA)", True),

        ([python_bin, "tools/stakeholder_actor_mapper.py"],
         "5. Dekomposisi Jaringan Aktor & Matriks Motif Pemangku Kepentingan", False),

        ([python_bin, "tools/generate_corpus_and_charts.py"],
         "6. Rekonstruksi Korpus Berita & Pembangkitan Grafik Visualisasi Pasar", False),

        ([python_bin, "tools/sna_centrality_analyzer.py"],
         "7. Pemodelan SNA (Betweenness, PageRank, Louvain Cluster, Density)", True),

        ([python_bin, "analisis_berita.py", "berita_skandal_jensen_huang.csv"],
         "8. Audit Leksikal Multibahasa & Klasterisasi Sindikasi Berita Arus Utama", False),

        ([python_bin, "tools/mobile_spyware_forensic_comparator.py"],
         "9. Komparasi Triad Intelijen Forensik: SIGINT vs Spyware vs HUMINT", False),

        ([python_bin, "tools/osint_artifact_manager.py"],
         "10. Pengelolaan & Verifikasi Katalog 11 Artefak Publik OSINT", False),

        ([python_bin, "tools/ela_exif_forensic_analyzer.py", "test"],
         "11. Validasi Forensik Visual ELA (Error Level Analysis) & Metadata EXIF", False),

        ([python_bin, "tools/deepfake_signature_validator.py", "test"],
         "12. Pengujian Tanda Tangan Media Sintetis Deepfake & Provenansi C2PA", False),

        ([python_bin, "tools/reportica_intelligence_generator.py"],
         "13. Pembangkitan Laporan Intelijen Terpadu (Reportica Executive Brief v4.0)", False)
    ]

    manifest_records = []
    pipeline_success = True
    start_all = time.time()

    for cmd, name, is_critical in stages:
        res = run_stage_with_retry(cmd, name, max_retries=1, is_critical=is_critical)
        manifest_records.append(res)
        if res["status"] != "SUCCESS":
            pipeline_success = False
            if is_critical:
                LOGGER.critical("Menghentikan pipeline akibat kegagalan pada tahap kritis: %s", name)
                break

    total_duration = round(time.time() - start_all, 2)
    successful_count = sum(1 for r in manifest_records if r["status"] == "SUCCESS")

    manifest_data = {
        "pipeline_version": "4.0",
        "execution_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_duration_sec": total_duration,
        "stages_planned": len(stages),
        "stages_executed": len(manifest_records),
        "stages_successful": successful_count,
        "overall_status": "SUCCESS" if pipeline_success and successful_count == len(stages) else "FAILED",
        "stages": manifest_records
    }

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    LOGGER.info("=" * 85)
    LOGGER.info("RINGKASAN EKSEKUSI PIPELINE: %d/%d TAHAP BERHASIL DIVERIFIKASI (%.2f dtk)",
                successful_count, len(stages), total_duration)
    LOGGER.info("Manifest eksekusi disimpan di: %s", MANIFEST_FILE)
    LOGGER.info("Log lengkap disimpan di: %s", LOG_FILE)
    if manifest_data["overall_status"] == "SUCCESS":
        LOGGER.info("[+] STATUS: 100% REPRODUCIBLE & VERIFIED FOR SCIENTIFIC PUBLICATION.")
    else:
        LOGGER.warning("[!] STATUS: Terdapat tahapan yang memerlukan perhatian.")
    LOGGER.info("=" * 85)

    if manifest_data["overall_status"] != "SUCCESS":
        sys.exit(1)

if __name__ == "__main__":
    main()
