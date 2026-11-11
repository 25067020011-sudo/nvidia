#!/usr/bin/env python3
"""
tools/sna_centrality_analyzer.py
--------------------------------------------------------------------------------
Social Network Analysis (SNA) & Rekonstruksi Garis Waktu Kemunculan Pertama
Menganalisis:
1. Kronologi Multi-Tahap Kemunculan Pertama (Platform, Tanggal, Pelopor, Isi)
2. Analisis Sentralitas Jejaring (Betweenness Centrality, Degree, PageRank)
   untuk 20 Aktor Utama dan 10 Media Teratas.
3. Visualisasi Graf Jejaring Komunikasi Informasi (07_network_graph_betweenness.png)
"""

import os
import json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = "analisis"

def generate_first_appearance_timeline():
    """Menyusun berkas '01_timeline_kemunculan_pertama.csv'."""
    os.makedirs(OUT_DIR, exist_ok=True)
    out_csv = os.path.join(OUT_DIR, "01_timeline_kemunculan_pertama.csv")

    stages = [
        {
            "tahap": "1. Media Sosial (Foto Tanpa Isu)",
            "tanggal": "Juni 2024",
            "platform_dan_lokasi": "LinkedIn (Taipei, Taiwan - Bar)",
            "pelopor_pertama": "Akun Resmi Perusahaan NetThunder",
            "muatan_informasi": "Foto santai Alice Huang duduk bersebelahan dengan Jensen Huang; Alice diperkenalkan sebagai MegaSpeed Chairwoman Alice Wong. Belum ada isu apa pun.",
            "status_klaim": "FAKTA DOKUMENTASI (FOTO ASLI)"
        },
        {
            "tahap": "1b. Media Sosial (Promosi Personal)",
            "tanggal": "2024 - 2025 (Periodik)",
            "platform_dan_lokasi": "Akun Media Sosial Pribadi Alice Huang",
            "pelopor_pertama": "Alice Huang (Huang Le)",
            "muatan_informasi": "Mengunggah foto bersama Jensen Huang untuk membanggakan relasi dekat guna menghimpun dana investasi bisnis.",
            "status_klaim": "FAKTA LAPANGAN (NETWORKING BIZ)"
        },
        {
            "tahap": "2. Media Massa (Penyebutan Kedekatan Bisnis)",
            "tanggal": "09 Oktober 2025",
            "platform_dan_lokasi": "The New York Times (AS)",
            "pelopor_pertama": "Jurnalis Investigasi NYT",
            "muatan_informasi": "Artikel mengenai penyelidikan ekspor Megaspeed; menyebut Alice Huang dan Jensen Huang adalah teman dekat. Belum ada tuduhan spionase.",
            "status_klaim": "LAPORAN PERS INVESTIGATIF"
        },
        {
            "tahap": "3. Media Massa (Tuduhan Spionase)",
            "tanggal": "29 Oktober 2026",
            "platform_dan_lokasi": "The Information (lalu disusul NYT)",
            "pelopor_pertama": "The Information (Briefing), disusul NYT",
            "muatan_informasi": "The Information mempublikasikan tajuk 'Nvidia CEO Reportedly Targeted By Suspected Chinese Informant', disusul laporan mendalam NYT.",
            "status_klaim": "TUDUHAN INTELIJEN SEDANG DIAUDIT"
        },
        {
            "tahap": "3b. Media Sosial (Amplifikasi Wartawan)",
            "tanggal": "29 Oktober 2026",
            "platform_dan_lokasi": "Platform X (Twitter)",
            "pelopor_pertama": "Paul Mozur (Wartawan Investigasi NYT)",
            "muatan_informasi": "Cuitan analisis bahwa laporan tersebut adalah babak baru penyelidikan penyelundupan chip di Singapura dan dugaan kontak intelijen.",
            "status_klaim": "AMPLIFIKASI MEDIA SOSIAL RESMI"
        },
        {
            "tahap": "4. Media Massa (Relasi Personal / Intim)",
            "tanggal": "06 - 07 November 2026",
            "platform_dan_lokasi": "Financial Times (London, Inggris)",
            "pelopor_pertama": "Financial Times (FT)",
            "muatan_informasi": "FT untuk pertama kalinya melaporkan hubungan tersebut bersifat intim/romantis (sebelumnya NYT hanya menyebut 'teman dekat'). Memicu sirkulasi foto di medsos.",
            "status_klaim": "LAPORAN INVESTIGASI PERSONAL"
        },
        {
            "tahap": "5. Pengakuan & Tata Kelola Dewan",
            "tanggal": "08 November 2026",
            "platform_dan_lokasi": "Memo Internal NVIDIA (dibocorkan ke Axios/FT) & Rilis Resmi Dewan",
            "pelopor_pertama": "Jensen Huang (Memo) & Dewan Direksi NVIDIA",
            "muatan_informasi": "Jensen Huang mengakui hubungan personal lewat memo internal; Dewan Direksi NVIDIA mengumumkan pembentukan komite independen.",
            "status_klaim": "DOKUMEN PRIMER TERKONFIRMASI"
        }
    ]

    df = pd.DataFrame(stages)
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"[+] Berhasil membuat kronologi kemunculan pertama: {out_csv}")
    return df

def run_sna_centrality_analysis():
    """Menghitung metrik sentralitas jejaring SNA untuk 20 aktor dan 10 media."""
    print("[*] Menjalankan pemodelan Social Network Analysis (SNA)...")

    # 20 Aktor Utama dalam Ekosistem Kasus
    actors = [
        "Jensen Huang (CEO)", "Alice Huang (Megaspeed)", "Dewan Direksi NVIDIA",
        "Komite Audit Independen", "Paul Mozur (Jurnalis NYT)", "Marco Rubio (Menlu AS)",
        "John Moolenaar (Ketua Komite Kongres)", "Pejabat Intelijen Anonim",
        "Komite Khusus DPR AS", "Kepolisian Singapura (Megaspeed Probe)",
        "Pengunjuk Rasa Berlin (Aktivis)", "NetThunder (Uploader LinkedIn)",
        "Operator Kanal Deepfake (UNC-CP-01)", "Investor / Pemegang Saham NVDA",
        "Analis Pasar Wall Street", "Elon Musk (Komentator X)",
        "Departemen Perdagangan AS (BIS)", "Penasihat Hukum Luar NVIDIA",
        "Auditor Eksternal Independen", "Komisi Pemilihan Umum AS (FEC)"
    ]

    # 10 Media Teratas
    top_media = [
        "The New York Times", "The Information", "Financial Times",
        "Tech Insider", "Crypto Briefing", "Axios",
        "NVIDIA Newsroom (Primer)", "Business Standard", "The Daily Beast", "The Next Web"
    ]

    # Inisialisasi Graf Terarah (DiGraph)
    G = nx.DiGraph()

    for a in actors:
        G.add_node(a, node_type="Aktor")
    for m in top_media:
        G.add_node(m, node_type="Media")

    # Tambahkan Relasi Informasi & Aliran Kutipan (Edges dengan Bobot Relasi)
    edges = [
        ("NetThunder (Uploader LinkedIn)", "Alice Huang (Megaspeed)"),
        ("Alice Huang (Megaspeed)", "Jensen Huang (CEO)"),
        ("Pejabat Intelijen Anonim", "The New York Times"),
        ("Pejabat Intelijen Anonim", "The Information"),
        ("The Information", "Tech Insider"),
        ("The New York Times", "Paul Mozur (Jurnalis NYT)"),
        ("Paul Mozur (Jurnalis NYT)", "Investor / Pemegang Saham NVDA"),
        ("Marco Rubio (Menlu AS)", "Komite Khusus DPR AS"),
        ("Komite Khusus DPR AS", "John Moolenaar (Ketua Komite Kongres)"),
        ("John Moolenaar (Ketua Komite Kongres)", "Business Standard"),
        ("Financial Times", "Jensen Huang (CEO)"),
        ("Jensen Huang (CEO)", "Dewan Direksi NVIDIA"),
        ("Jensen Huang (CEO)", "Axios"),
        ("Axios", "Crypto Briefing"),
        ("Dewan Direksi NVIDIA", "NVIDIA Newsroom (Primer)"),
        ("Dewan Direksi NVIDIA", "Komite Audit Independen"),
        ("Komite Audit Independen", "Penasihat Hukum Luar NVIDIA"),
        ("Pengunjuk Rasa Berlin (Aktivis)", "The Next Web"),
        ("The Next Web", "Investor / Pemegang Saham NVDA"),
        ("Operator Kanal Deepfake (UNC-CP-01)", "Investor / Pemegang Saham NVDA"),
        ("The Daily Beast", "Jensen Huang (CEO)"),
        ("Analis Pasar Wall Street", "Investor / Pemegang Saham NVDA"),
        ("Kepolisian Singapura (Megaspeed Probe)", "The New York Times"),
        ("Departemen Perdagangan AS (BIS)", "Komite Khusus DPR AS"),
        ("Elon Musk (Komentator X)", "Investor / Pemegang Saham NVDA"),
        ("The New York Times", "Financial Times"),
        ("NVIDIA Newsroom (Primer)", "The New York Times"),
        ("Crypto Briefing", "Investor / Pemegang Saham NVDA")
    ]

    G.add_edges_from(edges)

    # Perhitungan Metrik Sentralitas
    betweenness = nx.betweenness_centrality(G, normalized=True)
    in_degree = nx.in_degree_centrality(G)
    out_degree = nx.out_degree_centrality(G)
    degree_all = nx.degree_centrality(G)
    pagerank = nx.pagerank(G, alpha=0.85)
    closeness = nx.closeness_centrality(G)

    # Deteksi Komunitas (Louvain / Modularity Clustering pada Undirected Projection)
    G_undir = G.to_undirected()
    try:
        from networkx.algorithms.community import louvain_communities
        communities = louvain_communities(G_undir, seed=42)
    except Exception:
        from networkx.algorithms.community import greedy_modularity_communities
        communities = greedy_modularity_communities(G_undir)

    community_map = {}
    for c_id, comm in enumerate(communities, start=1):
        for node in comm:
            community_map[node] = c_id

    # Metrik Topologi Graf Global
    network_density = nx.density(G)
    reciprocity = nx.reciprocity(G)
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    # Ekspor Edge List dengan Tipe Hubungan & Bobot
    edge_records = []
    for u, v in G.edges():
        edge_records.append({
            "source": u,
            "target": v,
            "source_type": G.nodes[u].get("node_type", "Unknown"),
            "target_type": G.nodes[v].get("node_type", "Unknown"),
            "relation": "Information_Flow"
        })
    df_edges = pd.DataFrame(edge_records)
    df_edges.to_csv(os.path.join(OUT_DIR, "sna_edgelist.csv"), index=False, encoding="utf-8-sig")

    # 1. Matriks 20 Aktor
    actor_data = []
    for a in actors:
        actor_data.append({
            "Aktor": a,
            "Betweenness_Centrality": round(betweenness.get(a, 0.0), 4),
            "Degree_Centrality": round(degree_all.get(a, 0.0), 4),
            "In_Degree_Centrality": round(in_degree.get(a, 0.0), 4),
            "Out_Degree_Centrality": round(out_degree.get(a, 0.0), 4),
            "PageRank": round(pagerank.get(a, 0.0), 4),
            "Closeness_Centrality": round(closeness.get(a, 0.0), 4),
            "Community_Cluster": community_map.get(a, 0)
        })
    df_actors = pd.DataFrame(actor_data).sort_values("Betweenness_Centrality", ascending=False).reset_index(drop=True)
    df_actors.insert(0, "Ranking", range(1, len(df_actors) + 1))
    actor_csv = os.path.join(OUT_DIR, "matriks_sna_20_aktor.csv")
    if not os.path.exists(actor_csv):
        df_actors.to_csv(actor_csv, index=False, encoding="utf-8-sig")

    # 2. Matriks 10 Media Teratas
    media_data = []
    for m in top_media:
        media_data.append({
            "Media": m,
            "Betweenness_Centrality": round(betweenness.get(m, 0.0), 4),
            "Degree_Centrality": round(degree_all.get(m, 0.0), 4),
            "In_Degree_Centrality": round(in_degree.get(m, 0.0), 4),
            "Out_Degree_Centrality": round(out_degree.get(m, 0.0), 4),
            "PageRank": round(pagerank.get(m, 0.0), 4),
            "Closeness_Centrality": round(closeness.get(m, 0.0), 4),
            "Community_Cluster": community_map.get(m, 0)
        })
    df_media = pd.DataFrame(media_data).sort_values("Betweenness_Centrality", ascending=False).reset_index(drop=True)
    df_media.insert(0, "Ranking", range(1, len(df_media) + 1))
    media_csv = os.path.join(OUT_DIR, "matriks_sna_10_media.csv")
    if not os.path.exists(media_csv):
        df_media.to_csv(media_csv, index=False, encoding="utf-8-sig")

    # Ringkasan Topologi Graf
    topology_summary = {
        "nodes_count": num_nodes,
        "edges_count": num_edges,
        "network_density": round(float(network_density), 4),
        "reciprocity": round(float(reciprocity), 4),
        "total_communities_detected": len(communities),
        "clustering_method": "Louvain / Greedy Modularity",
        "top_information_gatekeeper": df_actors.iloc[0]["Aktor"],
        "top_media_conduit": df_media.iloc[0]["Media"]
    }
    with open(os.path.join(OUT_DIR, "sna_metrics_summary.json"), "w", encoding="utf-8") as f:
        json.dump(topology_summary, f, indent=2, ensure_ascii=False)

    print(f"[+] Matriks SNA 20 Aktor tersimpan di: {actor_csv}")
    print(f"[+] Matriks SNA 10 Media tersimpan di: {media_csv}")

    # Visualisasi Graf Jejaring Betweenness (07_network_graph_betweenness.png)
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.55, seed=42)

    # Ukuran node proporsional terhadap Betweenness Centrality
    node_sizes = [(betweenness[n] * 6000) + 400 for n in G.nodes()]
    node_colors = ["#3B6EA8" if G.nodes[n].get("node_type") == "Aktor" else "#D95F02" for n in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.88, edgecolors="white", linewidths=1.5)
    nx.draw_networkx_edges(G, pos, edge_color="#999999", alpha=0.6, arrows=True, arrowsize=14, width=1.2)
    nx.draw_networkx_labels(G, pos, font_size=8.5, font_family="sans-serif", font_weight="bold")

    plt.title("Social Network Analysis (SNA): Peta Sentralitas Perantara (Betweenness Centrality)\nAliran Informasi Kasus Jensen Huang & NVIDIA (20 Aktor & 10 Media Teratas)", fontsize=13, pad=15)
    plt.axis("off")
    plt.tight_layout()

    graph_img = os.path.join(OUT_DIR, "07_network_graph_betweenness.png")
    plt.savefig(graph_img, dpi=200)
    plt.close()
    print(f"[+] Visualisasi graf SNA tersimpan di: {graph_img}")

    # Tampilkan Ringkasan ke Terminal
    print("\n" + "=" * 80)
    print("TOP 10 AKTOR DENGAN BETWEENNESS CENTRALITY TERTINGGI (JEMBATAN INFORMASI)")
    print("=" * 80)
    print(df_actors[["Ranking", "Aktor", "Betweenness_Centrality", "PageRank"]].head(10).to_string(index=False))

    print("\n" + "=" * 80)
    print("TOP 10 MEDIA BERDASARKAN BETWEENNESS CENTRALITY (JARINGAN PEMBERITAAN)")
    print("=" * 80)
    print(df_media[["Ranking", "Media", "Betweenness_Centrality", "PageRank"]].to_string(index=False))

if __name__ == "__main__":
    generate_first_appearance_timeline()
    run_sna_centrality_analysis()

