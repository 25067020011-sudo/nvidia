#!/usr/bin/env python3
"""
tools/hash_chain_verifier.py
--------------------------------------------------------------------------------
Forensic Chain of Custody & SHA-256 Evidence Hasher
Standar Kepatuhan: ISO/IEC 27037:2012 (Digital Evidence Preservation)

Fungsi:
1. Menghitung nilai hash kriptografis ganda (SHA-256 dan MD5) untuk setiap berkas bukti.
2. Menghasilkan metadata waktu akuisisi berpresisi mikrodetik (UTC).
3. Mencatat dan memperbarui berkas manifest chain of custody (evidence_ledger.json).
4. Melakukan verifikasi integritas berkas bukti secara berkala.
"""

import os
import sys

# Deteksi otomatis eksekusi via Streamlit Cloud
try:
    import streamlit as st
    if hasattr(st, "runtime") and st.runtime.exists():
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        app_file = os.path.join(parent_dir, "app.py")
        if os.path.exists(app_file):
            os.chdir(parent_dir)
            with open(app_file, "r", encoding="utf-8") as _f:
                _code = compile(_f.read(), app_file, "exec")
            exec(_code, globals())
            sys.exit(0)
except SystemExit:
    raise
except Exception:
    pass

import json
import hashlib
from datetime import datetime, timezone

LEDGER_PATH = "evidence_ledger.json"

def calculate_hashes(filepath: str, block_size: int = 65536) -> dict:
    """Menghitung SHA-256 dan MD5 secara streaming untuk efisiensi memori."""
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256.update(block)
            md5.update(block)
            
    return {
        "sha256": sha256.hexdigest(),
        "md5": md5.hexdigest()
    }

def ingest_evidence(filepath: str, source_category: str, description: str, collector: str = "Forensic_Analyst"):
    """Mendaftarkan berkas bukti baru ke dalam log Chain of Custody."""
    if not os.path.exists(filepath):
        print(f"[!] Error: Berkas '{filepath}' tidak ditemukan.")
        return False

    stat = os.stat(filepath)
    hashes = calculate_hashes(filepath)
    utc_now = datetime.now(timezone.utc).isoformat()

    record = {
        "evidence_id": f"EVD-{hashes['sha256'][:8].upper()}",
        "filename": os.path.basename(filepath),
        "filepath": os.path.abspath(filepath),
        "filesize_bytes": stat.st_size,
        "source_category": source_category,  # e.g., 'Primary_Official', 'Social_Media', 'Media_Artifact'
        "description": description,
        "collector": collector,
        "acquisition_timestamp_utc": utc_now,
        "hashes": hashes,
        "verification_status": "AUTHENTIC"
    }

    # Muat ledger yang ada atau buat baru
    ledger = []
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        except Exception:
            ledger = []

    # Cek apakah berkas sudah ada dalam ledger (update jika berubah)
    found_idx = -1
    for idx, item in enumerate(ledger):
        if item.get("filepath") == os.path.abspath(filepath) or item.get("filename") == os.path.basename(filepath):
            found_idx = idx
            break

    if found_idx != -1:
        if ledger[found_idx].get("hashes", {}).get("sha256") == hashes["sha256"]:
            print(f"[*] Berkas sudah terdaftar dengan ID identik: {ledger[found_idx]['evidence_id']}")
            return True
        else:
            ledger[found_idx] = record
            print(f"[+] Memperbarui integritas bukti yang dimodifikasi:")
    else:
        ledger.append(record)
        print(f"[+] Berhasil mendaftarkan bukti forensik baru:")
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

    print(f"    - ID       : {record['evidence_id']}")
    print(f"    - File     : {record['filename']}")
    print(f"    - SHA-256  : {record['hashes']['sha256']}")
    print(f"    - Timestamp: {record['acquisition_timestamp_utc']}")
    return True

def verify_all_evidence():
    """Memverifikasi integritas seluruh berkas yang tercatat dalam ledger."""
    if not os.path.exists(LEDGER_PATH):
        print(f"[!] Belum ada ledger bukti '{LEDGER_PATH}'.")
        return

    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    print(f"[*] Memulai audit integritas bukti ({len(ledger)} item terdaftar)...")
    tampered_count = 0

    for item in ledger:
        fpath = item["filepath"]
        print(f"--> Memeriksa {item['evidence_id']} ({item['filename']})...", end=" ")
        
        if not os.path.exists(fpath):
            print("[FILE MISSING / HILANG]")
            tampered_count += 1
            continue

        curr_hashes = calculate_hashes(fpath)
        if curr_hashes["sha256"] == item["hashes"]["sha256"]:
            print("[VERIFIED / OTENTIK]")
        else:
            print("[TAMPERED / BERUBAH]")
            tampered_count += 1

    if tampered_count == 0:
        print("[+] Seluruh bukti forensik memiliki integritas SHA-256 yang valid (100% Utuh).")
        return 0
    else:
        print(f"[!] PERINGATAN: Ditemukan {tampered_count} berkas yang rusak/hilang dari rantai bukti!")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan:")
        print("  1. Ingest bukti baru:")
        print("     python hash_chain_verifier.py ingest <path_file> <kategori> <deskripsi>")
        print("  2. Verifikasi seluruh bukti:")
        print("     python hash_chain_verifier.py verify")
        sys.exit(0)

    mode = sys.argv[1].lower()
    if mode == "ingest" and len(sys.argv) >= 5:
        ingest_evidence(sys.argv[2], sys.argv[3], sys.argv[4])
    elif mode == "verify":
        verify_all_evidence()
    else:
        print("[!] Parameter tidak valid. Gunakan 'ingest' atau 'verify'.")

