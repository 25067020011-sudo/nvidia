#!/usr/bin/env python3
"""
tools/scrape_nodexl_medsos.py
--------------------------------------------------------------------------------
Social Media & News Scraper for "Jensen Huang" and "NVIDIA"
Compatible with NodeXL Pro Data Format (Edges, Vertices, Groups, Metrics)
Standard: Social Network Analysis (SNA) & Multi-Modal Media Forensics
--------------------------------------------------------------------------------
Generates:
1. data/nodexl_jensen_huang_nvidia.xlsx (Full multi-sheet NodeXL Workbook)
2. data/nodexl_jensen_huang_nvidia_edges.csv (NodeXL Edges standard)
3. data/nodexl_jensen_huang_nvidia_vertices.csv (NodeXL Vertices standard with centrality)
4. data/nodexl_jensen_huang_nvidia_berita.csv (Corpus of news & social posts)
5. analisis/nodexl_network_jensen_huang.png (NodeXL-style network graph)
"""

import os
import sys
import re
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
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

# Query target untuk ekosistem Jensen Huang & NVIDIA
QUERIES = [
    ('"Jensen Huang" NVIDIA', "en-US", "US", "en"),
    ('"Jensen Huang" "Alice Huang"', "en-US", "US", "en"),
    ('NVIDIA "Jensen Huang" China chip export', "en-US", "US", "en"),
    ('"Jensen Huang" Blackwell AI semiconductor', "en-US", "US", "en"),
    ('NVIDIA CEO deepfake scam YouTube', "en-US", "US", "en"),
    ('"Jensen Huang" Computex Taiwan TSMC', "en-US", "US", "en"),
    ('"Jensen Huang" Elon Musk xAI Tesla', "en-US", "US", "en"),
    ('NVIDIA "Megaspeed" Singapore investigation', "en-US", "US", "en"),
    ('"Jensen Huang" GTC keynote AI roadmap', "en-US", "US", "en"),
    ('"Jensen Huang" internal memo employee apology', "en-US", "US", "en")
]

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

def clean_html(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'&quot;', '"', clean)
    clean = re.sub(r'&amp;', '&', clean)
    clean = re.sub(r'&lt;', '<', clean)
    clean = re.sub(r'&gt;', '>', clean)
    clean = re.sub(r'&#39;', "'", clean)
    return clean.strip()

def extract_sentiment(text: str) -> str:
    lower = text.lower()
    negative_words = ["scandal", "spy", "investigation", "affair", "fall", "drop", "subpoena", "probe", "antitrust", "scam", "fraud", "deepfake", "smuggling", "warning"]
    positive_words = ["surge", "record", "triumph", "breakthrough", "leader", "growth", "sovereign ai", "milestone", "innovation", "rally", "partnership", "keynote"]
    
    neg_score = sum(1 for w in negative_words if w in lower)
    pos_score = sum(1 for w in positive_words if w in lower)
    
    if neg_score > pos_score:
        return "Negative"
    elif pos_score > neg_score:
        return "Positive"
    return "Neutral"

def scrape_feed(query_tuple):
    query, hl, gl, ceid = query_tuple
    encoded_q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl={hl}&gl={gl}&ceid={ceid}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    items_data = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            channel = root.find("channel")
            if channel is not None:
                for item in channel.findall("item"):
                    title = clean_html(item.findtext("title", ""))
                    link = item.findtext("link", "")
                    pub_date = item.findtext("pubDate", "")
                    source_elem = item.find("source")
                    source_name = source_elem.text.strip() if source_elem is not None and source_elem.text else "General Media"
                    desc = clean_html(item.findtext("description", ""))
                    
                    if title:
                        items_data.append({
                            "title": title,
                            "link": link,
                            "pub_date": pub_date,
                            "source": source_name,
                            "description": desc,
                            "query": query
                        })
    except Exception as e:
        print(f"[!] Warning fetching '{query}': {e}")
    return items_data

def build_nodexl_network(raw_items):
    edges = []
    berita_records = []
    
    seen_titles = set()
    unique_items = []
    for it in raw_items:
        clean_t = re.sub(r'\s+', ' ', it["title"].lower()).strip()
        if clean_t not in seen_titles:
            seen_titles.add(clean_t)
            unique_items.append(it)
            
    print(f"[*] Berhasil memproses {len(unique_items)} berita/postingan unik dari live feeds.")
    
    for idx, item in enumerate(unique_items, start=1):
        source = item["source"]
        title = item["title"]
        pub_date = item["pub_date"]
        link = item["link"]
        desc = item["description"]
        sentiment = extract_sentiment(title + " " + desc)
        
        # Ekstrak entitas target
        found_targets = []
        lower_t = (title + " " + desc).lower()
        for kw, entity in ENTITIES_MAPPING.items():
            if kw in lower_t:
                found_targets.append(entity)
        
        # Default target
        if not found_targets:
            if "jensen" in lower_t:
                found_targets.append("@JensenHuang")
            else:
                found_targets.append("@NVIDIA")
        else:
            if "@JensenHuang" not in found_targets and "jensen" in lower_t:
                found_targets.append("@JensenHuang")
            if "@NVIDIA" not in found_targets and "nvidia" in lower_t:
                found_targets.append("@NVIDIA")

        # Buat edges standar NodeXL
        for tgt in found_targets:
            rel = "Mentions"
            if "investigation" in lower_t or "probe" in lower_t:
                rel = "Reports Investigation"
            elif "interview" in lower_t or "keynote" in lower_t:
                rel = "Broadcasts Keynote"
            elif "scam" in lower_t or "deepfake" in lower_t:
                rel = "Exploits Brand"
            elif "stock" in lower_t or "shares" in lower_t:
                rel = "Analyzes Market Impact"

            edges.append({
                "Vertex 1": source,
                "Vertex 2": tgt,
                "Relationship": rel,
                "Relationship Date": pub_date,
                "Tweet / Headline": title,
                "URLs in Tweet": link,
                "Sentiment": sentiment,
                "Topic Query": item["query"]
            })
            
        berita_records.append({
            "id_berita": f"NXL-{idx:04d}",
            "judul": title,
            "media_sumber": source,
            "tanggal_rilis": pub_date,
            "sentimen": sentiment,
            "target_entitas": ", ".join(found_targets),
            "url_sumber": link,
            "ringkasan": desc[:200] + "..." if len(desc) > 200 else desc
        })
        
    df_edges = pd.DataFrame(edges)
    df_berita = pd.DataFrame(berita_records)
    
    # Hitung Graf SNA dengan NetworkX
    G = nx.DiGraph()
    for _, row in df_edges.iterrows():
        u = str(row["Vertex 1"])
        v = str(row["Vertex 2"])
        if G.has_edge(u, v):
            G[u][v]["weight"] += 1
        else:
            G.add_edge(u, v, weight=1)
            
    # Metrik Sentralitas NodeXL
    betweenness = nx.betweenness_centrality(G, weight="weight")
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    try:
        pagerank = nx.pagerank(G, weight="weight")
    except Exception:
        pagerank = {n: 0.0 for n in G.nodes()}
        
    # Deteksi Kluster Komunitas (Modularity)
    undirected_G = G.to_undirected()
    try:
        communities = list(nx.community.greedy_modularity_communities(undirected_G))
        cluster_map = {}
        for c_idx, comm in enumerate(communities, start=1):
            for node in comm:
                cluster_map[node] = f"G{c_idx}"
    except Exception:
        cluster_map = {n: "G1" for n in G.nodes()}

    vertices = []
    for node in G.nodes():
        node_type = "Media Outlet" if not node.startswith(("@", "#")) and "_" not in node else "Central Entity / Topic"
        vertices.append({
            "Vertex": node,
            "Cluster": cluster_map.get(node, "G1"),
            "In-Degree": in_degrees.get(node, 0),
            "Out-Degree": out_degrees.get(node, 0),
            "Degree": in_degrees.get(node, 0) + out_degrees.get(node, 0),
            "Betweenness Centrality": round(betweenness.get(node, 0.0), 5),
            "PageRank": round(pagerank.get(node, 0.0), 5),
            "Vertex Type": node_type
        })
        
    df_vertices = pd.DataFrame(vertices).sort_values(by="Betweenness Centrality", ascending=False)
    
    # Summary Metrics NodeXL
    metrics = [{
        "Metric": "Total Vertices (Nodes)", "Value": G.number_of_nodes()
    }, {
        "Metric": "Total Edges (Relationships)", "Value": G.number_of_edges()
    }, {
        "Metric": "Total Unique Articles/Posts Scraped", "Value": len(unique_items)
    }, {
        "Metric": "Connected Components", "Value": nx.number_weakly_connected_components(G)
    }, {
        "Metric": "Average Degree", "Value": round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2)
    }, {
        "Metric": "Network Density", "Value": round(nx.density(G), 4)
    }, {
        "Metric": "Top Bridge Influencer", "Value": df_vertices.iloc[0]["Vertex"] if not df_vertices.empty else "N/A"
    }]
    df_metrics = pd.DataFrame(metrics)
    
    return df_edges, df_vertices, df_berita, df_metrics, G

def render_nodexl_chart(G, df_vertices, output_path):
    plt.figure(figsize=(14, 10), dpi=300)
    plt.style.use("default")
    
    pos = nx.spring_layout(G, k=0.55, seed=42)
    
    # Ukuran simpul berdasarkan degree
    degrees = dict(G.degree())
    node_sizes = [max(120, degrees.get(n, 1) * 75) for n in G.nodes()]
    
    # Warna simpul: Target Utama vs Media
    node_colors = []
    for n in G.nodes():
        if n in ["@JensenHuang", "@NVIDIA"]:
            node_colors.append("#2ca02c") # Hijau khas Nvidia
        elif n.startswith(("@", "#")):
            node_colors.append("#d62728") # Merah Aktor/Isu
        else:
            node_colors.append("#1f77b4") # Biru Media
            
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.88, edgecolors="white", linewidths=1.2)
    nx.draw_networkx_edges(G, pos, edge_color="#7f7f7f", alpha=0.35, arrows=True, arrowsize=10, width=0.8)
    
    # Label hanya untuk top 20 simpul berpengaruh
    top_nodes = set(df_vertices.head(22)["Vertex"])
    labels = {n: n for n in G.nodes() if n in top_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight="bold", font_family="sans-serif")
    
    plt.title("NodeXL Social Network Analysis: Ekosistem Berita & Medsos 'Jensen Huang' & 'NVIDIA'\n"
              "Pemetaan Struktur Polarisasi Informasi, Aktor Pengaruh, dan Saluran Penyebaran",
              fontsize=13, fontweight="bold", pad=16)
    plt.axis("off")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"[+] Visualisasi graf jaringan NodeXL tersimpan di: {output_path}")

def main():
    print("=" * 80)
    print("🌐 NODEXL LIVE MEDIA SCRAPER & NETWORK GENERATOR")
    print("Query: 'Jensen Huang' & 'NVIDIA'")
    print("=" * 80)
    
    all_items = []
    for q_tup in QUERIES:
        print(f"--> Scraping live feed: {q_tup[0]}...")
        items = scrape_feed(q_tup)
        all_items.extend(items)
        time.sleep(0.3)
        
    if not all_items:
        print("[!] Gagal mengumpulkan data live feed.")
        sys.exit(1)
        
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ANALISIS_DIR.mkdir(parents=True, exist_ok=True)
    
    df_edges, df_vertices, df_berita, df_metrics, G = build_nodexl_network(all_items)
    
    # 1. Simpan CSV
    csv_edges = DATA_DIR / "nodexl_jensen_huang_nvidia_edges.csv"
    csv_vertices = DATA_DIR / "nodexl_jensen_huang_nvidia_vertices.csv"
    csv_berita = DATA_DIR / "nodexl_jensen_huang_nvidia_berita.csv"
    
    df_edges.to_csv(csv_edges, index=False, encoding="utf-8-sig")
    df_vertices.to_csv(csv_vertices, index=False, encoding="utf-8-sig")
    df_berita.to_csv(csv_berita, index=False, encoding="utf-8-sig")
    
    # 2. Simpan Multi-Sheet Excel (NodeXL Pro Standard Format)
    excel_path = DATA_DIR / "nodexl_jensen_huang_nvidia.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_edges.to_excel(writer, sheet_name="Edges", index=False)
        df_vertices.to_excel(writer, sheet_name="Vertices", index=False)
        df_metrics.to_excel(writer, sheet_name="Overall Metrics", index=False)
        df_berita.to_excel(writer, sheet_name="Feed Berita Medsos", index=False)
    print(f"[+] Workbook NodeXL berhasil diekspor ke: {excel_path.relative_to(REPO_ROOT)}")
    
    # 3. Render Chart
    chart_path = ANALISIS_DIR / "nodexl_network_jensen_huang.png"
    render_nodexl_chart(G, df_vertices, str(chart_path))
    
    print("\n" + "=" * 80)
    print("📊 RINGKASAN HASIL SCRAPING NODEXL:")
    print("=" * 80)
    for _, row in df_metrics.iterrows():
        print(f"  • {row['Metric']:<35}: {row['Value']}")
    print("-" * 80)
    print("Top 5 Influencer / Vertex Berpengaruh:")
    for idx, row in df_vertices.head(5).iterrows():
        print(f"    {row['Vertex']:<26} | Betweenness: {row['Betweenness Centrality']:<8} | Degree: {row['Degree']}")
    print("=" * 80)

if __name__ == "__main__":
    main()

