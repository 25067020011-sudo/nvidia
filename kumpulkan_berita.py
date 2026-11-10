"""
Bot pengumpul berita skandal Jensen Huang / NVIDIA (Alice Huang, Megaspeed, perselingkuhan).
Target default 10.000 berita: JUDUL, MEDIA, TANGGAL TERBIT, LINK, dan STATUS LINK (dicek satu per satu).

Pasang sekali:
    pip install requests pandas htmldate

Jalankan (contoh):
    python kumpulkan_berita.py                       # target 10.000, 1 Okt - 11 Nov 2026
    python kumpulkan_berita.py --target 1000         # cukup 1.000
    python kumpulkan_berita.py --mulai 2026-10-28 --selesai 2026-11-11
    python kumpulkan_berita.py --tanpa-cek           # lewati pengecekan link (lebih cepat)

Output:
    berita_jensen_huang_<N>.csv   kolom: no, tanggal_terbit, judul, media, url, status_link,
                                  bahasa, negara_sumber, sumber_tanggal, query
    gdelt_mentah.csv              hasil mentah GDELT (cadangan, bisa dilanjutkan)

Catatan jujur:
- Bot berhenti saat target tercapai ATAU saat GDELT tidak punya artikel lagi.
  Kalau total berita unik tentang skandal ini memang < 10.000, hasilnya akan < 10.000
  dan bot memberi tahu. Jangan ditambal dengan berita yang tidak relevan.
- 'tanggal_terbit' diambil dari meta halaman (htmldate). Jika halaman tidak bisa dibuka,
  dipakai 'seendate' GDELT (waktu pertama kali GDELT melihat artikel, biasanya selisih
  menit-jam dari waktu terbit).
"""
import argparse
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

import pandas as pd
import requests

try:
    from htmldate import find_date
except ImportError:
    find_date = None

GDELT = "https://api.gdeltproject.org/api/v2/doc/doc"
JEDA = 6  # GDELT: maks ~1 request / 5 detik
UA = {"User-Agent": "Mozilla/5.0 (riset forensik digital; pengumpul berita)"}

# GDELT memantau berita dalam 65 bahasa dan mencocokkan query ke terjemahan Inggrisnya,
# jadi berita Indonesia, Mandarin, Korea, dll. ikut tertangkap.
QUERIES = [
    '"Jensen Huang" ("Alice Huang" OR Megaspeed OR "Huang Le")',
    '"Jensen Huang" (spy OR espionage OR "intelligence asset" OR "Chinese agent")',
    '"Jensen Huang" (affair OR unfaithful OR mistress OR "independent investigation")',
    '"Jensen Huang" (scandal OR resign OR "board of directors" OR "step down")',
    'Nvidia ("Alice Huang" OR Megaspeed) (Congress OR Moolenaar OR "Select Committee")',
    'Nvidia CEO (spy OR affair OR scandal)',
    'Megaspeed (Singapore OR Malaysia OR smuggling OR export) Nvidia',
    '"Alice Huang" Nvidia',
]


def gdelt(query, start, end):
    params = {
        "query": query, "mode": "artlist", "format": "json", "maxrecords": 250,
        "sort": "datedesc",
        "startdatetime": start.strftime("%Y%m%d%H%M%S"),
        "enddatetime": end.strftime("%Y%m%d%H%M%S"),
    }
    for _ in range(4):
        try:
            r = requests.get(GDELT, params=params, timeout=60, headers=UA)
            if r.status_code == 429:
                time.sleep(30)
                continue
            if not r.text.lstrip().startswith("{"):
                return []
            return r.json().get("articles", [])
        except Exception as e:
            print("   ! GDELT error:", e)
            time.sleep(15)
    return []


def norm(url):
    u = re.sub(r"^https?://(www\.|m\.|amp\.)?", "", str(url)).lower()
    return u.split("?")[0].split("#")[0].replace("/amp/", "/").rstrip("/")


def kumpulkan(mulai, selesai, target):
    terlihat, rows = set(), []
    for q in QUERIES:
        t = mulai
        while t < selesai:
            # jendela 6 jam: jika penuh (250) dipecah lagi jadi 2 x 3 jam
            jendela = [(t, t + timedelta(hours=6))]
            while jendela:
                s, e = jendela.pop(0)
                arts = gdelt(q, s, e)
                time.sleep(JEDA)
                if len(arts) >= 250 and (e - s) > timedelta(hours=1):
                    tengah = s + (e - s) / 2
                    jendela = [(s, tengah), (tengah, e)] + jendela
                    continue
                baru = 0
                for a in arts:
                    k = norm(a.get("url"))
                    if k in terlihat:
                        continue
                    terlihat.add(k)
                    baru += 1
                    sd = a.get("seendate", "")
                    rows.append({
                        "url": a.get("url"),
                        "judul": (a.get("title") or "").strip(),
                        "media": a.get("domain"),
                        "bahasa": a.get("language"),
                        "negara_sumber": a.get("sourcecountry"),
                        "gdelt_seendate_utc": datetime.strptime(sd, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M") if sd else "",
                        "query": q,
                    })
                print(f"{q[:40]:40} {s:%m-%d %H}h  +{baru:3d}  total unik {len(rows)}", flush=True)
                if baru > 0:
                    pd.DataFrame(rows).to_csv("gdelt_mentah.csv", index=False, encoding="utf-8-sig")
            if len(rows) >= target * 1.15:  # cadangan 15% untuk link yang mati
                return rows
            t += timedelta(hours=6)
        pd.DataFrame(rows).to_csv("gdelt_mentah.csv", index=False, encoding="utf-8-sig")
    return rows


def cek(url):
    """Buka halaman: kembalikan (status_link, tanggal_terbit dari meta halaman)."""
    try:
        r = requests.get(url, headers=UA, timeout=20, allow_redirects=True)
        status = "valid" if r.status_code < 400 else f"HTTP {r.status_code}"
        if r.status_code in (401, 402, 403):
            status = f"terkunci/paywall ({r.status_code})"
        tgl = ""
        if find_date and r.status_code < 400 and r.text:
            try:
                tgl = find_date(r.text, original_date=True, outputformat="%Y-%m-%d") or ""
            except Exception:
                pass
        return status, tgl
    except requests.exceptions.Timeout:
        return "timeout", ""
    except Exception:
        return "tidak bisa dibuka", ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=10000)
    ap.add_argument("--mulai", default="2026-10-01")
    ap.add_argument("--selesai", default="2026-11-11")
    ap.add_argument("--tanpa-cek", action="store_true")
    ap.add_argument("--thread", type=int, default=24)
    a = ap.parse_args()

    mulai = datetime.strptime(a.mulai, "%Y-%m-%d")
    selesai = datetime.strptime(a.selesai, "%Y-%m-%d")
    rows = kumpulkan(mulai, selesai, a.target)

    # gabungkan 300 link kurasi manual jika ada di folder yang sama
    if os.path.exists("berita_skandal_jensen_huang.csv"):
        lama = pd.read_csv("berita_skandal_jensen_huang.csv", encoding="utf-8-sig")
        sudah = {norm(r["url"]) for r in rows}
        for _, r in lama.iterrows():
            if norm(r["url"]) not in sudah:
                rows.append({"url": r["url"], "judul": r["judul_ringkas"], "media": r["media"],
                             "bahasa": r["bahasa"], "negara_sumber": "",
                             "gdelt_seendate_utc": str(r.get("tanggal_terbit") or ""),
                             "query": "kurasi manual"})

    df = pd.DataFrame(rows)
    print(f"\nTotal berita unik terkumpul: {len(df)}")

    if a.tanpa_cek:
        df["status_link"], df["tgl_halaman"] = "belum dicek", ""
    else:
        print(f"Mengecek {len(df)} link + mengambil tanggal terbit ({a.thread} thread)...")
        hasil = {}
        with ThreadPoolExecutor(a.thread) as ex:
            fut = {ex.submit(cek, u): u for u in df["url"]}
            for i, f in enumerate(as_completed(fut), 1):
                hasil[fut[f]] = f.result()
                if i % 200 == 0:
                    print(f"  {i}/{len(df)}")
        df["status_link"] = df["url"].map(lambda u: hasil[u][0])
        df["tgl_halaman"] = df["url"].map(lambda u: hasil[u][1])

    def tanggal(r):
        if r["tgl_halaman"]:
            return pd.Series([r["tgl_halaman"], "meta halaman"])
        if r["gdelt_seendate_utc"] and r["gdelt_seendate_utc"] != "nan":
            return pd.Series([r["gdelt_seendate_utc"][:10], "GDELT seendate (perkiraan)"])
        return pd.Series(["", ""])

    df[["tanggal_terbit", "sumber_tanggal"]] = df.apply(tanggal, axis=1)

    # urutkan: link valid dulu, lalu tanggal; potong sesuai target
    df["_ok"] = df["status_link"].str.startswith(("valid", "terkunci", "belum")).astype(int)
    df = df.sort_values(["_ok", "tanggal_terbit"], ascending=[False, True]).head(a.target)
    df = df.sort_values("tanggal_terbit")
    df.insert(0, "no", range(1, len(df) + 1))
    kolom = ["no", "tanggal_terbit", "judul", "media", "url", "status_link",
             "bahasa", "negara_sumber", "sumber_tanggal", "gdelt_seendate_utc", "query"]
    out = f"berita_jensen_huang_{len(df)}.csv"
    df[kolom].to_csv(out, index=False, encoding="utf-8-sig")

    print(f"\nSelesai -> {out}")
    print(df["status_link"].value_counts().to_string())
    if len(df) < a.target:
        print(f"\nHanya {len(df)} berita unik yang ditemukan GDELT untuk topik ini "
              f"(target {a.target}). Perlebar --mulai/--selesai atau tambah QUERIES.")


if __name__ == "__main__":
    main()

