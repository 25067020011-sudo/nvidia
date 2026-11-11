#!/usr/bin/env python3
"""
tools/generate_nodexl_10000.py
--------------------------------------------------------------------------------
Build Full 10,000 Social Media & News NodeXL Network Dataset for Jensen Huang / NVIDIA
Compatible with NodeXL Pro Standard (Edges, Vertices, Groups, Metrics)
Standard: ISO/IEC 27037:2012, Social Network Analysis (SNA)
--------------------------------------------------------------------------------
Outputs:
1. data/nodexl_jensen_huang_nvidia_10000.xlsx (Multi-sheet NodeXL workbook)
2. data/nodexl_jensen_huang_nvidia_edges_10000.csv
3. data/nodexl_jensen_huang_nvidia_vertices_10000.csv
4. data/nodexl_jensen_huang_nvidia_berita_10000.csv
5. analisis/nodexl_network_10000.png
"""

import os
import sys
import re
from pathlib import Path
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
ANALISIS_DIR = REPO_ROOT / "analisis"

ENTITIES_MAPPING = {
    "alice huang": "@AliceHuang",
    "alice wong": "@AliceHuang",
    "megaspeed": "@MegaspeedSolutions",
    "elon musk": "@ElonMusk",
    "blackwell": "#Blackwell_Architecture",
    "tsmc": "@TSMC_Official",
    "morris chang": "@MorrisChang_TSMC",
    "computex": "#ComputexTaipei",
    "china": "China_Regulators",
    "taiwan": "Taiwan_Gov",
    "sec": "@SEC_Enforcement",
    "commerce": "@CommerceGov_BIS",
    "deepfake": "Deepfake_Actor_Bot",
    "scam": "Crypto_Fraud_Ring",
    "internal memo": "NVIDIA_Employees",
    "wall street": "WallStreet_Analysts",
    "ftc": "@FTC_Antitrust",
    "doj": "@DOJ_Antitrust"
}

def extract_sentiment(text: str, tier: str = "") -> str:
    lower = str(text).lower()
    if tier == "VERIFIED_FALSE":
        return "Negative"
    elif tier == "VERIFIED_TRUE":
        return "Positive"
        
    neg_words = ["scandal", "spy", "investigation", "affair", "fall", "drop", "subpoena", "probe", "antitrust", "scam", "fraud", "deepfake", "smuggling", "warning", "crisis", "disastrous", "lawsuit", "sued"]
    pos_words = ["surge", "record", "triumph", "breakthrough", "leader", "growth", "sovereign", "milestone", "innovation", "rally", "partnership", "keynote", "advance", "support", "rebound"]
    
    neg = sum(1 for w in neg_words if w in lower)
    pos = sum(1 for w in pos_words if w in lower)
    if neg > pos:
        return "Negative"
    elif pos > neg:
        return "Positive"
    return "Neutral"

def build_10000_dataset():
    print("=" * 80)
    print("🚀 MEMBANGUN 10.000 DATASET NODEXL UNGGAPAN & ANALISIS JEJARING SOSIAL LENGKAP")
    print("Topik: 'Jensen Huang' & 'NVIDIA'")
    print("=" * 80)

    # 1. Ambil data live feed yang sudah discrape
    live_file = DATA_DIR / "nodexl_jensen_huang_nvidia_berita.csv"
    live_items = []
    if live_file.exists():
        df_live = pd.read_csv(live_file)
        for _, row in df_live.iterrows():
            live_items.append({
                "judul": str(row["judul"]),
                "media": str(row["media_sumber"]),
                "tanggal": str(row["tanggal_rilis"]),
                "url": str(row["url_sumber"]),
                "sentimen": str(row.get("sentimen", "Neutral")),
                "kategori": "Live_OSINT_Feed"
            })
    print(f"[*] Berhasil memuat {len(live_items)} unggahan live feed aktual.")

    # 2. Ambil dari korpus benchmark 10.000 untuk melengkapi hingga genap 10.000
    target_count = 10000
    needed = target_count - len(live_items)
    
    corpus_file = REPO_ROOT / "berita_jensen_huang_10000.csv"
    if not corpus_file.exists():
        print(f"[!] Berkas '{corpus_file.name}' tidak ditemukan.")
        sys.exit(1)
        
    df_corpus = pd.read_csv(corpus_file)
    print(f"[*] Mengambil {needed} artikel dari benchmark corpus terverifikasi...")
    
    selected_corpus = df_corpus.head(needed)
    all_10000_records = []
    
    # Masukkan live items lebih dulu
    for idx, it in enumerate(live_items, start=1):
        all_10000_records.append({
            "id_unggahan": f"NXL-10K-{idx:05d}",
            "judul": it["judul"],
            "media_sumber": it["media"],
            "tanggal_rilis": it["tanggal"],
            "sentimen": it["sentimen"],
            "kategori_topik": it["kategori"],
            "url_sumber": it["url"]
        })
        
    start_idx = len(live_items) + 1
    for _, row in selected_corpus.iterrows():
        t_sent = extract_sentiment(str(row["judul"]), str(row.get("tier_kebenaran", "")))
        all_10000_records.append({
            "id_unggahan": f"NXL-10K-{start_idx:05d}",
            "judul": str(row["judul"]),
            "media_sumber": str(row["media"]),
            "tanggal_rilis": str(row["tanggal_terbit"]),
            "sentimen": t_sent,
            "kategori_topik": str(row["kategori_topik"]),
            "url_sumber": str(row["url"])
        })
        start_idx += 1
        
    df_berita_10000 = pd.DataFrame(all_10000_records)
    print(f"[+] Total berkas berita/unggahan: {len(df_berita_10000):,} data.")

    # 3. Bentuk Tabel Edges (Relasi NodeXL)
    print("[*] Mengonstruksi relasi jaringan Edges (NodeXL format)...")
    edges_records = []
    
    for _, row in df_berita_10000.iterrows():
        source = row["media_sumber"]
        title = row["judul"]
        date = row["tanggal_rilis"]
        url = row["url_sumber"]
        sent = row["sentimen"]
        lower = title.lower()
        
        found_targets = []
        for kw, entity in ENTITIES_MAPPING.items():
            if kw in lower:
                found_targets.append(entity)
                
        if not found_targets:
            if "jensen" in lower:
                found_targets.append("@JensenHuang")
            else:
                found_targets.append("@NVIDIA")
        else:
            if "@JensenHuang" not in found_targets and "jensen" in lower:
                found_targets.append("@JensenHuang")
            if "@NVIDIA" not in found_targets and "nvidia" in lower:
                found_targets.append("@NVIDIA")

        for tgt in found_targets:
            rel = "Mentions"
            if any(w in lower for w in ["investigation", "probe", "subpoena"]):
                rel = "Reports Investigation"
            elif any(w in lower for w in ["keynote", "speech", "ces", "gtc"]):
                rel = "Broadcasts Keynote"
            elif any(w in lower for w in ["scam", "deepfake", "clone"]):
                rel = "Exploits Brand"
            elif any(w in lower for w in ["stock", "shares", "drop", "surge", "valuation"]):
                rel = "Analyzes Market Impact"
            elif any(w in lower for w in ["regulation", "export", "license"]):
                rel = "Examines Geopolitical Policy"
                
            edges_records.append({
                "Vertex 1": source,
                "Vertex 2": tgt,
                "Relationship": rel,
                "Relationship Date": date,
                "Tweet / Headline": title,
                "URLs in Tweet": url,
                "Sentiment": sent,
                "Topic Category": row["kategori_topik"]
            })
            
    df_edges_10000 = pd.DataFrame(edges_records)
    print(f"[+] Total relasi Edges terkonstruksi: {len(df_edges_10000):,} baris.")

    # 4. Bangun Graf SNA & Metrik Vertices
    print("[*] Menghitung metrik sentralitas SNA (Betweenness, Degree, PageRank, Modularity)...")
    G = nx.DiGraph()
    for _, r in df_edges_10000.iterrows():
        u = str(r["Vertex 1"])
        v = str(r["Vertex 2"])
        if G.has_edge(u, v):
            G[u][v]["weight"] += 1
        else:
            G.add_edge(u, v, weight=1)
            
    in_deg = dict(G.in_degree())
    out_deg = dict(G.out_degree())
    
    # Hitung Betweenness Centrality (sample untuk performa tinggi)
    betweenness = nx.betweenness_centrality(G, weight="weight", k=min(120, len(G.nodes())))
    try:
        pagerank = nx.pagerank(G, weight="weight", max_iter=100)
    except Exception:
        pagerank = {n: 0.0 for n in G.nodes()}

    undirected_G = G.to_undirected()
    try:
        communities = list(nx.community.greedy_modularity_communities(undirected_G))
        cluster_map = {}
        for c_idx, comm in enumerate(communities, start=1):
            for n in comm:
                cluster_map[n] = f"G{c_idx}"
    except Exception:
        cluster_map = {n: "G1" for n in G.nodes()}

    vertices_records = []
    for node in G.nodes():
        node_type = "Media Outlet" if not node.startswith(("@", "#")) and "_" not in node else "Central Entity / Topic"
        vertices_records.append({
            "Vertex": node,
            "Cluster": cluster_map.get(node, "G1"),
            "In-Degree": in_deg.get(node, 0),
            "Out-Degree": out_deg.get(node, 0),
            "Degree": in_deg.get(node, 0) + out_deg.get(node, 0),
            "Betweenness Centrality": round(betweenness.get(node, 0.0), 6),
            "PageRank": round(pagerank.get(node, 0.0), 6),
            "Vertex Type": node_type
        })
        
    df_vertices_10000 = pd.DataFrame(vertices_records).sort_values(by="Degree", ascending=False)
    print(f"[+] Total simpul Vertices terhitung: {len(df_vertices_10000)} simpul.")

    # 5. Buat Ringkasan Metrik
    df_metrics_10000 = pd.DataFrame([
        {"Metric": "Total Data Unggahan (Berita/Medsos)", "Value": len(df_berita_10000)},
        {"Metric": "Total Edges (Relasi)", "Value": len(df_edges_10000)},
        {"Metric": "Total Vertices (Simpul)", "Value": len(df_vertices_10000)},
        {"Metric": "Jumlah Kluster Komunitas (Groups)", "Value": len(set(df_vertices_10000['Cluster']))},
        {"Metric": "Average Degree", "Value": round(sum(dict(G.degree()).values()) / len(G.nodes()), 2)},
        {"Metric": "Network Density", "Value": round(nx.density(G), 5)},
        {"Metric": "Aktor Paling Sentral (Highest In-Degree)", "Value": df_vertices_10000.iloc[0]["Vertex"]},
        {"Metric": "Media Paling Prolifik (Highest Out-Degree)", "Value": df_vertices_10000[df_vertices_10000['Vertex Type'] == 'Media Outlet'].iloc[0]["Vertex"]}
    ])

    # 6. Ekspor Berkas
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ANALISIS_DIR.mkdir(parents=True, exist_ok=True)
    
    excel_path = DATA_DIR / "nodexl_jensen_huang_nvidia_10000.xlsx"
    print(f"[*] Menulis berkas Excel multi-sheet: {excel_path.name}...")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_edges_10000.to_excel(writer, sheet_name="Edges", index=False)
        df_vertices_10000.to_excel(writer, sheet_name="Vertices", index=False)
        df_metrics_10000.to_excel(writer, sheet_name="Overall Metrics", index=False)
        df_berita_10000.to_excel(writer, sheet_name="Feed Berita Medsos 10000", index=False)

    df_berita_10000.to_csv(DATA_DIR / "nodexl_jensen_huang_nvidia_berita_10000.csv", index=False, encoding="utf-8-sig")
    df_edges_10000.to_csv(DATA_DIR / "nodexl_jensen_huang_nvidia_edges_10000.csv", index=False, encoding="utf-8-sig")
    df_vertices_10000.to_csv(DATA_DIR / "nodexl_jensen_huang_nvidia_vertices_10000.csv", index=False, encoding="utf-8-sig")

    # 7. Render Visualisasi Jaringan Resolusi Tinggi
    chart_path = ANALISIS_DIR / "nodexl_network_10000.png"
    print(f"[*] Merender grafik jaringan NodeXL 10.000 ke: {chart_path.name}...")
    plt.figure(figsize=(18, 14), dpi=300)
    pos = nx.spring_layout(G, k=0.40, seed=42)
    
    degrees = dict(G.degree())
    node_sizes = [min(2000, max(80, degrees.get(n, 1) * 2)) for n in G.nodes()]
    
    node_colors = []
    for n in G.nodes():
        if n in ["@JensenHuang", "@NVIDIA"]:
            node_colors.append("#2ca02c") # Hijau khas Nvidia
        elif n.startswith(("@", "#")):
            node_colors.append("#d62728") # Merah Entitas/Isu
        else:
            node_colors.append("#1f77b4") # Biru Media
            
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.82, edgecolors="white", linewidths=0.8)
    nx.draw_networkx_edges(G, pos, edge_color="#999999", alpha=0.18, arrows=True, arrowsize=8, width=0.5)
    
    top_35_nodes = set(df_vertices_10000.head(32)["Vertex"])
    labels = {n: n for n in G.nodes() if n in top_35_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight="bold", font_family="sans-serif")
    
    plt.title("NodeXL Social Network Analysis (10.000 Dataset Benchmark)\n"
              "Pemetaan Skala Penuh Struktur Polarisasi Informasi, Aktor Pengaruh, & Saluran Berita 'Jensen Huang' - 'NVIDIA'",
              fontsize=15, fontweight="bold", pad=18)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    print("\n" + "=" * 80)
    print("✅ SELESAI! SEMUA BERKAS NODEXL 10.000 DATA BERHASIL DIBUAT:")
    print("=" * 80)
    print(f"1. Excel Workbook : data/nodexl_jensen_huang_nvidia_10000.xlsx ({os.path.getsize(excel_path):,} bytes)")
    print(f"2. CSV Berita     : data/nodexl_jensen_huang_nvidia_berita_10000.csv")
    print(f"3. CSV Edges      : data/nodexl_jensen_huang_nvidia_edges_10000.csv ({len(df_edges_10000):,} baris)")
    print(f"4. CSV Vertices   : data/nodexl_jensen_huang_nvidia_vertices_10000.csv ({len(df_vertices_10000)} simpul)")
    print(f"5. Grafik PNG     : analisis/nodexl_network_10000.png")
    print("=" * 80)

if __name__ == "__main__":
    build_10000_dataset()

