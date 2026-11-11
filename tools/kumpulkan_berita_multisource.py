#!/usr/bin/env python3
"""
tools/kumpulkan_berita_multisource.py
--------------------------------------------------------------------------------
Multi-source Live News Collector for Jensen Huang / NVIDIA Ecosystem
Target: 1,000 unique international news articles across multiple languages and media outlets.
Primary Engine: Google News RSS Search API (Multi-language / Multi-region) + Curated Archive Integration
Output: berita_jensen_huang_1000.csv
"""

import sys
import os
import re
import csv
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# List of search queries targeting the Jensen Huang / NVIDIA narrative ecosystem
QUERIES = [
    # Core Investigation & Allegations
    ('"Jensen Huang" "Alice Huang"', "en-US", "US", "en"),
    ('"Jensen Huang" "Chinese spy"', "en-US", "US", "en"),
    ('"Jensen Huang" "foreign intelligence"', "en-US", "US", "en"),
    ('"Jensen Huang" affair scandal', "en-US", "US", "en"),
    ('Nvidia CEO "independent investigation"', "en-US", "US", "en"),
    ('Nvidia board "Stephen Neal" Huang', "en-US", "US", "en"),
    ('Nvidia "Megaspeed" export compliance', "en-US", "US", "en"),
    ('Nvidia Huang FBI investigation', "en-US", "US", "en"),
    ('Trump "Jensen Huang" China trip', "en-US", "US", "en"),
    ('House Republicans subpoena "Jensen Huang"', "en-US", "US", "en"),
    
    # Deepfake & Cyber-Physical Incidents
    ('Jensen Huang deepfake YouTube livestream', "en-US", "US", "en"),
    ('Jensen Huang AI clone scam QR code', "en-US", "US", "en"),
    ('Jensen Huang GTC Berlin protest speech', "en-US", "US", "en"),
    
    # Market & Regulatory Impact
    ('Nvidia stock drops CEO investigation Jensen Huang', "en-US", "US", "en"),
    ('Nvidia internal memo CEO Jensen Huang', "en-US", "US", "en"),
    ('Jensen Huang Blackwell chip China regulations', "en-US", "US", "en"),
    ('Elon Musk Tesla xAI Nvidia GPU purchase', "en-US", "US", "en"),
    
    # Multi-Regional & International Editions (UK, Singapore, Taiwan, Germany, Indonesia)
    ('"Jensen Huang" "Alice Huang"', "en-GB", "GB", "en"),
    ('Nvidia CEO Jensen Huang spy investigation', "en-GB", "GB", "en"),
    ('"Jensen Huang" Megaspeed Singapore Malaysia', "en-SG", "SG", "en"),
    ('Nvidia CEO Jensen Huang scandal', "en-AU", "AU", "en"),
    ('黄仁勋 间谍 调查', "zh-CN", "CN", "zh"),
    ('黄仁勋 Alice Huang 调查', "zh-TW", "TW", "zh"),
    ('輝達 黃仁勳 內部調查 董事會', "zh-TW", "TW", "zh"),
    ('Jensen Huang Spionage Untersuchung Nvidia', "de-DE", "DE", "de"),
    ('Jensen Huang GTC Berlin Protest', "de-DE", "DE", "de"),
    ('Jensen Huang enquête espionnage Nvidia', "fr-FR", "FR", "fr"),
    ('Jensen Huang skandal investigasi Nvidia', "id-ID", "ID", "id"),
    ('CEO Nvidia Jensen Huang isu spionase', "id-ID", "ID", "id"),
    ('ジェンスン・フアン Nvidia スキャンダル 調査', "ja-JP", "JP", "ja"),
    ('젠슨 황 엔비디아 조사 스캔들', "ko-KR", "KR", "ko"),
]

def clean_title(title: str) -> str:
    """Bersihkan judul dari suffix media bawaan RSS Google News (mis. ' - CNBC')."""
    if not title:
        return ""
    title = re.sub(r"\s+-\s+[^-]+$", "", title.strip())
    return title.strip()

def normalize_key(title: str, url: str) -> str:
    """Kunci deduplikasi berbasis kata judul dan host url."""
    t_clean = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]", "", title.lower())[:40]
    return t_clean

def parse_rss_feed(query: str, hl: str, gl: str, lang: str):
    encoded_q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl={hl}&gl={gl}&ceid={gl}:{lang}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    )
    items_out = []
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            tree = ET.fromstring(content)
            for it in tree.findall(".//item"):
                t_el = it.find("title")
                l_el = it.find("link")
                d_el = it.find("pubDate")
                s_el = it.find("source")
                
                title = t_el.text.strip() if t_el is not None and t_el.text else ""
                link = l_el.text.strip() if l_el is not None and l_el.text else ""
                pub_date = d_el.text.strip() if d_el is not None and d_el.text else ""
                source_name = s_el.text.strip() if s_el is not None and s_el.text else ""
                
                if not source_name and " - " in title:
                    source_name = title.split(" - ")[-1]
                
                # Format pubDate ke YYYY-MM-DD
                tgl_iso = ""
                if pub_date:
                    try:
                        # Contoh: Tue, 10 Nov 2026 19:36:37 GMT
                        dt = datetime.strptime(pub_date[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                        tgl_iso = dt.strftime("%Y-%m-%d")
                    except Exception:
                        try:
                            # Fallback parsing
                            dt = datetime.strptime(pub_date[:16].strip(), "%a, %d %b %Y")
                            tgl_iso = dt.strftime("%Y-%m-%d")
                        except Exception:
                            tgl_iso = pub_date[:10]
                
                if title and link:
                    items_out.append({
                        "judul": clean_title(title),
                        "media": source_name or "Portal Berita",
                        "url": link,
                        "tanggal_terbit": tgl_iso or datetime.utcnow().strftime("%Y-%m-%d"),
                        "bahasa": lang,
                        "status_link": "valid"
                    })
    except Exception as e:
        print(f"   [!] Gagal query '{query}' ({hl}): {e}", file=sys.stderr)
    return items_out

def main():
    target = 1000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        target = int(sys.argv[1])
        
    print(f"[*] Memulai pengumpulan {target} berita ekosistem Jensen Huang / NVIDIA...")
    collected = []
    seen = set()
    
    # 1. Muat korpus yang sudah ada (jika ada) untuk menjaga kesinambungan riset
    curated_csv = REPO_ROOT / "berita_skandal_jensen_huang.csv"
    if curated_csv.exists():
        with open(curated_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                k = normalize_key(r.get("judul", ""), r.get("url", ""))
                if k and k not in seen:
                    seen.add(k)
                    collected.append({
                        "tanggal_terbit": r.get("tanggal_terbit", "2026-10-29"),
                        "judul": r.get("judul", ""),
                        "media": r.get("media", "Tech Media"),
                        "url": r.get("url", ""),
                        "bahasa": r.get("bahasa", "en"),
                        "status_link": r.get("status_link", "valid")
                    })
        print(f"[+] Memuat {len(collected)} artikel terkurasi dari dataset awal.")
    
    # 2. Lakukan crawling multi-sumber via RSS Search
    for i, (q, hl, gl, lang) in enumerate(QUERIES, start=1):
        if len(collected) >= target:
            break
        print(f"--> [{i}/{len(QUERIES)}] Mencari: '{q}' ({hl})...", flush=True)
        items = parse_rss_feed(q, hl, gl, lang)
        added = 0
        for it in items:
            k = normalize_key(it["judul"], it["url"])
            if k and k not in seen:
                seen.add(k)
                collected.append(it)
                added += 1
                if len(collected) >= target:
                    break
        print(f"    Ditemukan {len(items)} | Ditambahkan: {added} unik | Total: {len(collected)}")
        time.sleep(1.0) # Rate limiter santun
    
    # 3. Jika target belum tercapai, tambahkan pencarian relasi industri AI/semikonduktor
    additional_terms = [
        "Nvidia US-China export controls", "Jensen Huang Computex keynote AI",
        "Nvidia AI enterprise server demand", "Huang Le Alice Huang investigation",
        "Nvidia SEC Form 8-K audit committee", "Taiwan Semiconductor TSMC Nvidia Huang",
        "Jensen Huang White House AI meeting", "Nvidia quantum computing AI chips"
    ]
    if len(collected) < target:
        for term in additional_terms:
            if len(collected) >= target:
                break
            print(f"--> [Ekspansi] Mencari: '{term}'...", flush=True)
            items = parse_rss_feed(term, "en-US", "US", "en")
            for it in items:
                k = normalize_key(it["judul"], it["url"])
                if k and k not in seen:
                    seen.add(k)
                    collected.append(it)
                    if len(collected) >= target:
                        break
            time.sleep(1.0)
    
    # Batasi tepat target
    final_dataset = collected[:target]
    
    # 4. Tulis hasil ke CSV
    out_csv = REPO_ROOT / f"berita_jensen_huang_{len(final_dataset)}.csv"
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["no", "tanggal_terbit", "judul", "media", "url", "bahasa", "status_link"])
        for idx, row in enumerate(final_dataset, start=1):
            writer.writerow([
                idx,
                row["tanggal_terbit"],
                row["judul"],
                row["media"],
                row["url"],
                row["bahasa"],
                row["status_link"]
            ])
            
    print(f"\n[+] BERHASIL: {len(final_dataset)} berita unik berhasil disimpan di: {out_csv.name}")
    
    # Statistik bahasa dan media
    languages = {}
    media_counts = {}
    for r in final_dataset:
        l = r["bahasa"]
        m = r["media"]
        languages[l] = languages.get(l, 0) + 1
        media_counts[m] = media_counts.get(m, 0) + 1
        
    print(f"[i] Distribusi Bahasa: {languages}")
    print(f"[i] Total Media Unik : {len(media_counts)} portal media")

if __name__ == "__main__":
    main()

