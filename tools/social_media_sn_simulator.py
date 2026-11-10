#!/usr/bin/env python3
"""
tools/social_media_sn_simulator.py
--------------------------------------------------------------------------------
Simulator Propagasi Media Sosial (X / Twitter & YouTube Live Chat)
Menghasilkan korpus 10.000 interaksi media sosial untuk memodelkan bagaimana
narasi "Jensen Huang diserang fisik" diamplifikasi dari 'Patient Zero' (protes Berlin)
hingga menjadi viral melalui akun botting dan bias kognitif Layer 8.

Keluaran:
  - analisis/dataset_medsos_10000.csv (10.000 baris)
  - analisis/06_propagasi_medsos_sna.png (Visualisasi jejaring penyebaran)
"""

import os
import random
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

OUT_DIR = "analisis"
OUTPUT_CSV = os.path.join(OUT_DIR, "dataset_medsos_10000.csv")

def generate_social_media_10k():
    print("[*] Mensintesis dataset propagasi media sosial (Target: 10.000 baris)...")
    os.makedirs(OUT_DIR, exist_ok=True)

    # 4 Kategori Akun
    account_types = ["Bot_Amplifier", "Netizen_Organik", "Tech_Influencer", "Media_Agregator"]
    account_weights = [0.55, 0.35, 0.05, 0.05]  # 55% Bot, 35% Organik

    # Kategori Konten Postingan
    content_templates = {
        "KLAIM_SERANGAN_FISIK": [
            "BREAKING: Jensen Huang physically attacked on stage in Berlin keynote?! Watch before deleted!",
            "OMG did someone just assault the Nvidia CEO during the live event?",
            "Jensen Huang diserang orang di panggung Berlin, gila parah banget!",
            "Report: Physical confrontation on stage targeting Nvidia CEO Jensen Huang in Germany",
            "Video shows Nvidia CEO rushed on stage, attacked over AI chips controversy"
        ],
        "KLARIFIKASI_PROTES_VERBAL": [
            "Fact check: Huang was NOT physically assaulted. Activists only heckled verbally about drone chips.",
            "Tidak ada serangan fisik, itu cuma interupsi suara pengunjuk rasa di Berlin GTC.",
            "Stop spreading fake news, watch the full official stream, Jensen wasn't touched at all."
        ],
        "DEEPFAKE_CRYPTO_SPAM": [
            "Nvidia official live stream giving away 50,000 ETH! Scan QR code on screen now!",
            "Jensen Huang announces surprise crypto doubling event during keynote! Claim your BTC",
            "Giveaway resmi Nvidia Live, scan QR di layar untuk dapat 2x crypto!"
        ],
        "SENTIMEN_SAHAM_DAN_REGULASI": [
            "Nvidia stock diving after election results and data center regulation fears $NVDA",
            "Massive selloff in AI stocks, Nasdaq down $2.5T, Nvidia drops 9%",
            "Panic selling on NVDA as board opens independent governance inquiry"
        ]
    }

    start_date = datetime(2026, 10, 21, 8, 0, 0)  # Hari Keynote Berlin
    end_date = datetime(2026, 11, 10, 23, 59, 59)
    total_seconds = int((end_date - start_date).total_seconds())

    rows = []
    # Seed generator untuk konsistensi eksperimen
    random.seed(42)
    np.random.seed(42)

    for i in range(1, 10001):
        post_id = f"POST-{i:06d}"
        platform = random.choice(["X (Twitter)", "YouTube Live Chat", "Reddit", "Telegram Channel"])
        acc_type = random.choices(account_types, weights=account_weights)[0]
        
        # Probabilitas kategori konten
        # 45% Bot giveaway deepfake, 30% Klaim viral serangan fisik, 15% Sentimen pasar, 10% Klarifikasi
        cat = random.choices(
            ["DEEPFAKE_CRYPTO_SPAM", "KLAIM_SERANGAN_FISIK", "SENTIMEN_SAHAM_DAN_REGULASI", "KLARIFIKASI_PROTES_VERBAL"],
            weights=[0.45, 0.30, 0.15, 0.10]
        )[0]
        
        text = random.choice(content_templates[cat])
        
        # Penjadwalan waktu posting berbasis lonjakan peristiwa
        if cat in ["KLAIM_SERANGAN_FISIK", "KLARIFIKASI_PROTES_VERBAL"]:
            # Terkonsentrasi di 21-23 Oktober (Insiden Berlin)
            delta = random.randint(0, 3 * 86400)
        elif cat == "DEEPFAKE_CRYPTO_SPAM":
            # Terkonsentrasi di 28-30 Oktober (Insiden YouTube Live)
            delta = random.randint(7 * 86400, 10 * 86400)
        else:
            # Terkonsentrasi di 4-9 November (Crash saham & memo)
            delta = random.randint(14 * 86400, 19 * 86400)

        post_time = start_date + timedelta(seconds=delta)
        retweets = random.randint(0, 500) if acc_type != "Bot_Amplifier" else random.randint(50, 2500)
        likes = retweets * random.randint(2, 6)

        rows.append({
            "post_id": post_id,
            "timestamp_utc": post_time.strftime("%Y-%m-%d %H:%M:%S"),
            "platform": platform,
            "account_type": acc_type,
            "category": cat,
            "text": text,
            "reposts_retweets": retweets,
            "likes_upvotes": likes,
            "is_bot_generated": acc_type == "Bot_Amplifier"
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp_utc").reset_index(drop=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[+] Berhasil membuat dataset media sosial: {OUTPUT_CSV} ({len(df):,} baris)")

    # Visualisasi Propagasi Media Sosial (06_propagasi_medsos_sna.png)
    df["date"] = pd.to_datetime(df["timestamp_utc"]).dt.date
    daily_cat = df.groupby(["date", "category"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    daily_cat.plot(kind="area", stacked=True, alpha=0.8, ax=ax,
                   color=["#E7298A", "#D95F02", "#1B9E77", "#7570B3"])
    ax.set_title("Propagasi Narasi Media Sosial (N=10.000 Postingan): Dekonstruksi Hoaks & Botting", fontsize=12, pad=12)
    ax.set_ylabel("Frekuensi Postingan / Hari", fontsize=11)
    ax.set_xlabel("Garis Waktu Peristiwa (Oktober - November 2026)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(title="Kategori Narasi", loc="upper left", fontsize=9)

    out_img = os.path.join(OUT_DIR, "06_propagasi_medsos_sna.png")
    fig.tight_layout()
    fig.savefig(out_img, dpi=200)
    plt.close(fig)
    print(f"[+] Grafik propagasi medsos tersimpan di: {out_img}")

if __name__ == "__main__":
    generate_social_media_10k()

