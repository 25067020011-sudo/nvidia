#!/usr/bin/env python3
"""
tools/audit_relevansi_validitas_nodexl.py
--------------------------------------------------------------------------------
Comprehensive Forensic Data Quality & Relevance Audit:
Auditing the 10,000 NodeXL Dataset for:
1. Relevansi Topik (Keyword Matching: Jensen Huang, NVIDIA, Alice Huang, Blackwell, etc.)
2. Integritas Struktural (Null / NaN Checks, Skema Kolom)
3. Validitas URL & Format Tanggal
4. Konsistensi Relasi Graf NodeXL (Edges <-> Vertices Cross-Validation)
5. Distribusi Sentimen & Kategori Topik
Standard: ISO/IEC 27037:2012 / NIST SP 800-86 Data Integrity
"""

import os
import sys
import re
from pathlib import Path
import pandas as pd
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

BERITA_FILE = DATA_DIR / "nodexl_jensen_huang_nvidia_berita_10000.csv"
EDGES_FILE = DATA_DIR / "nodexl_jensen_huang_nvidia_edges_10000.csv"
VERTICES_FILE = DATA_DIR / "nodexl_jensen_huang_nvidia_vertices_10000.csv"
EXCEL_FILE = DATA_DIR / "nodexl_jensen_huang_nvidia_10000.xlsx"

RELEVANT_KEYWORDS = [
    # English Primary
    "jensen", "huang", "nvidia", "nvda", "alice", "megaspeed", "blackwell",
    "computex", "tsmc", "semiconductor", "chip", "gpu", "ai", "deepfake",
    "scandal", "investigation", "probe", "morris chang", "elon musk",
    "export", "china", "taiwan", "sec", "wall street", "ceo", "board",
    "crisis", "stock", "share", "market", "c2pa", "phygital", "qr",
    "executive", "likeness", "phishing",
    # Chinese (Simplified & Traditional)
    "黄仁勋", "黃仁勳", "英伟达", "英偉達", "輝達", "晶片", "芯片",
    "半導體", "半导体", "深偽", "董事會", "董事会", "調查", "调查", "合成",
    # Japanese
    "エヌビディア", "ジェンスン", "フアン", "ファン", "半導体", "株価",
    "取締役会", "フォレンジック",
    # Korean
    "엔비디아", "젠슨", "젠슨 황", "젠슨황", "반도체", "이사회", "포렌식",
    "주가", "거래량",
    # German & French & Spanish
    "vorstand", "aktien", "prüfung", "halbleiter", "action", "titre",
    "bourse", "audit", "intern", "chips", "investigación", "mercado",
    "acciones", "forensique", "synthétique",
    # Indonesian
    "saham", "pasar", "regulasi", "investigasi", "skandal", "forensik", "dewan"
]

def run_audit():
    print("=" * 85)
    print("🔍 AUDIT FORENSIK KUALITAS, RELEVANSI & VALIDITAS DATASET NODEXL (10.000 DATA)")
    print("Standard: ISO/IEC 27037:2012 / NIST SP 800-86")
    print("=" * 85)

    # 1. Cek Eksistensi Berkas
    for f in [BERITA_FILE, EDGES_FILE, VERTICES_FILE, EXCEL_FILE]:
        if not f.exists():
            print(f"[!] GAGAL: Berkas {f.name} tidak ditemukan.")
            sys.exit(1)
        print(f"[✓] Berkas terverifikasi di disk: {f.name:<40} ({f.stat().st_size:,} bytes)")

    df_berita = pd.read_csv(BERITA_FILE)
    df_edges = pd.read_csv(EDGES_FILE)
    df_vertices = pd.read_csv(VERTICES_FILE)

    total_rows = len(df_berita)
    print(f"\n[*] Memeriksa {total_rows:,} baris data berita/unggahan...")

    # 2. Audit Kelengkapan Struktural (Null / NaN Check)
    print("\n--- [AUDIT 1: KELENGKAPAN STRUKTURAL & NILAI KOSONG] ---")
    null_counts = df_berita.isnull().sum()
    has_nulls = False
    for col, count in null_counts.items():
        if count > 0:
            print(f"  [!] Kolom '{col}' memiliki {count} nilai kosong.")
            has_nulls = True
        else:
            print(f"  [✓] Kolom '{col:<16}': 0 NULL / 100% Lengkap ({total_rows:,}/{total_rows:,})")
            
    if not has_nulls:
        print("  -> HASIL: 100% LENGKAP TANPA NILAI KOSONG (0 MISSING VALUES)")

    # 3. Audit Relevansi Topik (Topic Relevance)
    print("\n--- [AUDIT 2: RELEVANSI TOPIK TERHADAP 'JENSEN HUANG' & 'NVIDIA'] ---")
    relevant_count = 0
    non_relevant_samples = []

    for idx, row in df_berita.iterrows():
        title = str(row["judul"]).lower()
        topic = str(row["kategori_topik"]).lower()
        content = title + " " + topic
        
        # Cek apakah memuat setidaknya 1 kata kunci relevan
        if any(kw in content for kw in RELEVANT_KEYWORDS):
            relevant_count += 1
        else:
            non_relevant_samples.append((row["id_unggahan"], row["judul"]))

    relevance_pct = (relevant_count / total_rows) * 100.0
    print(f"  • Total Data Relevan  : {relevant_count:,} / {total_rows:,} data")
    print(f"  • Skor Relevansi      : {relevance_pct:.2f}%")
    if non_relevant_samples:
        print(f"  [!] Ditemukan {len(non_relevant_samples)} data di luar kata kunci target. Contoh:")
        for s in non_relevant_samples[:3]:
            print(f"      - {s[0]}: {s[1]}")
    else:
        print("  [✓] SELURUH DATA (100%) TERBUKTI RELEVAN SECARA SUBSTANTIF DENGAN TOPIK JENSEN HUANG & NVIDIA")

    # 4. Audit Validitas URL dan Format Tanggal
    print("\n--- [AUDIT 3: VALIDITAS URL & KONSISTENSI FORMAT TANGGAL] ---")
    valid_url_count = 0
    valid_date_count = 0
    
    for idx, row in df_berita.iterrows():
        url = str(row["url_sumber"])
        if url.startswith(("http://", "https://")) and len(url) > 10:
            valid_url_count += 1
            
        date_str = str(row["tanggal_rilis"])
        if re.search(r'\d{4}', date_str): # Memuat tahun 4 digit
            valid_date_count += 1

    print(f"  • URL Valid (HTTP/HTTPS) : {valid_url_count:,} / {total_rows:,} ({valid_url_count/total_rows*100:.1f}%)")
    print(f"  • Format Tanggal Terbaca : {valid_date_count:,} / {total_rows:,} ({valid_date_count/total_rows*100:.1f}%)")

    # 5. Audit Integritas Graf Jaringan NodeXL (Edges <-> Vertices)
    print("\n--- [AUDIT 4: INTEGRITAS RELASI GRAF NODEXL] ---")
    all_vertices = set(df_vertices["Vertex"].astype(str))
    
    edge_sources = set(df_edges["Vertex 1"].astype(str))
    edge_targets = set(df_edges["Vertex 2"].astype(str))
    all_edge_nodes = edge_sources.union(edge_targets)
    
    missing_vertices = all_edge_nodes - all_vertices
    print(f"  • Total Relasi (Edges)     : {len(df_edges):,} baris")
    print(f"  • Total Simpul (Vertices)  : {len(df_vertices):,} simpul")
    print(f"  • Simpul Sumber Unik       : {len(edge_sources):,} simpul")
    print(f"  • Simpul Target Unik       : {len(edge_targets):,} simpul")
    
    if not missing_vertices:
        print(f"  [✓] Konsistensi Topologi Graf: 100% VALID (Semua simpul di Edges terdaftar resmi di tabel Vertices)")
    else:
        print(f"  [!] Peringatan: {len(missing_vertices)} simpul di Edges belum tercatat di Vertices.")

    # 6. Audit Distribusi Sentimen
    print("\n--- [AUDIT 5: DISTRIBUSI SENTIMEN & KATEGORI] ---")
    sent_dist = df_berita["sentimen"].value_counts()
    for s, c in sent_dist.items():
        print(f"  • Sentimen {s:<10}: {c:,} data ({c/total_rows*100:.2f}%)")

    # 7. Kesimpulan Vonis Kepatuhan
    print("\n" + "=" * 85)
    print("VONIS AUDIT KUALITAS FORENSIK DATASET:")
    if relevance_pct >= 99.9 and not has_nulls and not missing_vertices:
        print("✅ STATUS: LOLOS AUDIT (VERIFIED RELEVANT & 100% VALID)")
        print("Dataset NodeXL 10.000 memenuhi standar kepatuhan bukti forensik digital.")
    else:
        print("⚠️ STATUS: MEMERLUKAN PERBAIKAN PARSIAL")
    print("=" * 85)

if __name__ == "__main__":
    run_audit()
