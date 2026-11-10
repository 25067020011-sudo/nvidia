"""
Analisis forensik-media atas CSV berita skandal Jensen Huang.
Bisa dipakai untuk CSV 300 link (berita_skandal_jensen_huang.csv) maupun hasil bot
(berita_jensen_huang_<N>.csv).

    pip install pandas matplotlib
    python analisis_berita.py berita_jensen_huang_10000.csv

Output di folder analisis/:
    ringkasan.md                 temuan utama (siap dikutip di laporan)
    01_timeline.png              jumlah berita per hari
    02_media_teratas.png         20 media paling banyak memberitakan
    03_bahasa.png                sebaran bahasa
    04_klaim.png                 klaim apa yang muncul di judul
    klaim_per_berita.csv         label klaim per baris
    klaster_sindikasi.csv        judul-judul yang hampir identik (berita yang sama dimuat ulang)
"""
import os
import re
import sys
from collections import Counter
from difflib import SequenceMatcher

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUT = "analisis"

# Kamus klaim multibahasa (EN, ID, ZH, KO, DE, ES). Dicocokkan pada judul + URL.
KLAIM = {
    "Spionase / Alice Huang": r"spy|espionage|intelligence|alice huang|agent|mata-mata|intelijen|间谍|情报|黄乐|스파이|간첩|spion|espía",
    "Megaspeed / ekspor chip": r"megaspeed|export|smuggl|ekspor|selundup|走私|出口|수출|밀수",
    "Perselingkuhan": r"affair|unfaithful|mistress|selingkuh|婚外|外遇|不忠|불륜|외도|affäre|aventura",
    "Investigasi / Kongres / dewan": r"congress|committee|moolenaar|investigat|probe|board|senat|kongres|penyelidik|国会|调查|董事会|의회|조사|이사회|untersuch",
    "Kubu Garis Keras / Rubio / Hawkish": r"rubio|moolenaar|hawk|hardline|select committee|national security memo",
    "Spekulasi Politik / Dalang Trump": r"trump (?:takeover|oust|trap|plot|scheme|puppet|dalang|jebak|rebut|kuasai|ambil ?alih)",
    "Saham / pasar": r"stock|share|market|investor|saham|股价|股票|주가|aktie|acciones",
    "Bantahan NVIDIA / Huang": r"deni|reject|push(?:es)? back|respond|statement|bantah|tanggap|否认|回应|부in|반박|dementi|niega",
    "SERANGAN FISIK": r"assault|attack(?:ed)? (?:on|by)|stab|shot|physically|injur|diserang|dipukul|ditusuk|luka|袭击|遇袭|受伤|폭행|피습|angriff|agresi[oó]n",
    "Serangan siber / peretasan": r"hack|breach|cyber ?attack|ransomware|leak|retas|bocor|黑客|入侵|해킹|유출",
}


def baca(path):
    d = pd.read_csv(path, encoding="utf-8-sig")
    if "judul" not in d.columns and "judul_ringkas" in d.columns:
        d = d.rename(columns={"judul_ringkas": "judul"})
    d["judul"] = d["judul"].fillna("").astype(str)
    d["tanggal_terbit"] = pd.to_datetime(d.get("tanggal_terbit"), errors="coerce")
    return d


def label_klaim(d):
    teks = (d["judul"] + " " + d["url"].astype(str)).str.lower()
    for k, pola in KLAIM.items():
        d[k] = teks.str.contains(pola, regex=True)
    return d


def klaster_sindikasi(d, ambang=0.85):
    """Kelompokkan judul yang hampir sama (berita yang sama dimuat ulang media lain)."""
    j = d["judul"].str.lower().str.replace(r"[^\w\s]", " ", regex=True).str.split().str.join(" ")
    idx = [i for i in d.index if len(j[i]) > 25]
    klaster, sudah = [], set()
    # bucket per 3 kata pertama agar tetap cepat untuk 10.000 baris
    bucket = {}
    for i in idx:
        bucket.setdefault(" ".join(j[i].split()[:3]), []).append(i)
    for anggota in bucket.values():
        for a in anggota:
            if a in sudah:
                continue
            grup = [a]
            for b in anggota:
                if b != a and b not in sudah and SequenceMatcher(None, j[a], j[b]).ratio() >= ambang:
                    grup.append(b)
            if len(grup) > 1:
                sudah.update(grup)
                klaster.append(grup)
    rows = []
    for n, g in enumerate(sorted(klaster, key=len, reverse=True), 1):
        for i in g:
            rows.append({"klaster": n, "ukuran": len(g), "judul": d.at[i, "judul"],
                         "media": d.at[i, "media"], "url": d.at[i, "url"]})
    return pd.DataFrame(rows)


def simpan_bar(series, judul, file, warna="#3B6EA8", horizontal=True):
    fig, ax = plt.subplots(figsize=(9, max(3, 0.32 * len(series) + 1)))
    if horizontal:
        series[::-1].plot.barh(ax=ax, color=warna)
        ax.set_xlabel("jumlah berita")
    else:
        series.plot.bar(ax=ax, color=warna)
        ax.set_ylabel("jumlah berita")
    ax.set_title(judul, loc="left", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, file), dpi=150)
    plt.close(fig)


def main(path):
    os.makedirs(OUT, exist_ok=True)
    d = label_klaim(baca(path))
    n = len(d)

    # 1. timeline
    ber_tgl = d.dropna(subset=["tanggal_terbit"])
    lama = ber_tgl[ber_tgl["tanggal_terbit"] < "2026-10-01"]  # berita konteks (Megaspeed lama dll.)
    ber_tgl = ber_tgl[ber_tgl["tanggal_terbit"] >= "2026-10-01"]
    per_hari = ber_tgl.groupby(ber_tgl["tanggal_terbit"].dt.date).size()
    if len(per_hari):
        fig, ax = plt.subplots(figsize=(10, 4))
        per_hari.plot(ax=ax, marker="o", color="#3B6EA8")
        for tgl, ket in (("2026-10-29", "Laporan NYT\n(Alice Huang)"), ("2026-11-08", "Huang akui\nperselingkuhan")):
            t = pd.Timestamp(tgl).date()
            if per_hari.index.min() <= t <= per_hari.index.max():
                ax.axvline(t, color="#C0504D", ls="--", lw=1)
                ax.text(t, ax.get_ylim()[1] * 0.92, " " + ket, color="#C0504D", fontsize=8, va="top")
        ax.set_title(f"Jumlah berita per hari (n bertanggal = {len(ber_tgl)})", loc="left")
        ax.set_xlabel("")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig(os.path.join(OUT, "01_timeline.png"), dpi=150)
        plt.close(fig)

    # 2-3. media & bahasa
    media = d["media"].value_counts().head(20)
    simpan_bar(media, "20 media teratas", "02_media_teratas.png")
    bahasa = d["bahasa"].fillna("?").value_counts()
    simpan_bar(bahasa.head(15), "Sebaran bahasa", "03_bahasa.png", warna="#6A9C59")

    # 4. klaim
    klaim = pd.Series({k: int(d[k].sum()) for k in KLAIM}).sort_values(ascending=False)
    simpan_bar(klaim, "Klaim yang muncul di judul/URL", "04_klaim.png", warna="#8064A2")
    d[["url", "media", "judul", "tanggal_terbit"] + list(KLAIM)].to_csv(
        os.path.join(OUT, "klaim_per_berita.csv"), index=False, encoding="utf-8-sig")

    # 5. sindikasi
    sind = klaster_sindikasi(d)
    sind.to_csv(os.path.join(OUT, "klaster_sindikasi.csv"), index=False, encoding="utf-8-sig")
    n_salinan = int(sind.groupby("klaster").size().sub(1).sum()) if len(sind) else 0

    fisik = d[d["SERANGAN FISIK"]]
    status = d["status_link"].value_counts().to_dict() if "status_link" in d else {}

    md = [
        f"# Ringkasan analisis berita — {os.path.basename(path)}",
        "",
        f"- **Total berita:** {n}",
        f"- **Bertanggal:** {len(ber_tgl)} ({len(ber_tgl)/n:.0%})"
        + (f", rentang {per_hari.index.min()} s.d. {per_hari.index.max()}" if len(per_hari) else ""),
        f"- **Berita konteks sebelum Okt 2026 (tidak masuk timeline):** {len(lama)}",
        f"- **Media unik:** {d['media'].nunique()} | **Bahasa:** {d['bahasa'].nunique()}",
        f"- **Salinan sindikasi (judul hampir identik):** {n_salinan} berita dalam {sind['klaster'].nunique() if len(sind) else 0} klaster "
        f"-> sumber independen efektif sekitar {n - n_salinan}",
    ]
    if status:
        md.append("- **Status link:** " + ", ".join(f"{k}: {v}" for k, v in status.items()))
    if len(per_hari):
        md.append(f"- **Puncak pemberitaan:** {per_hari.idxmax()} ({per_hari.max()} berita)")
    md += ["", "## Klaim di judul/URL", "", "| Klaim | Jumlah | % |", "|---|---:|---:|"]
    md += [f"| {k} | {v} | {v/n:.1%} |" for k, v in klaim.items()]
    md += ["", "## Verifikasi klaim \"Jensen Huang diserang fisik\"", ""]
    if len(fisik):
        md.append(f"{len(fisik)} judul cocok dengan kata kunci serangan fisik. Periksa manual (bisa jadi kiasan, "
                  "mis. 'attack on Nvidia's reputation'):")
        md += [f"- {r.media}: {r.judul} — {r.url}" for r in fisik.head(30).itertuples()]
    else:
        md.append("Tidak ada satu pun judul yang memuat klaim serangan fisik. Narasi \"diserang\" yang beredar "
                  "tidak didukung pemberitaan media dalam korpus ini; isu yang sebenarnya adalah dugaan spionase "
                  "(Alice Huang/Megaspeed) dan perselingkuhan.")
    md += ["", "## 20 media teratas", ""] + [f"{i}. {m} — {c}" for i, (m, c) in enumerate(media.items(), 1)]
    md += ["", "_Label klaim berbasis kata kunci, bukan pembacaan isi artikel. Gunakan sebagai penyaring awal, lalu "
           "validasi sampel secara manual (mis. 100 baris acak) dan laporkan presisinya._"]
    open(os.path.join(OUT, "ringkasan.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "berita_skandal_jensen_huang.csv")
