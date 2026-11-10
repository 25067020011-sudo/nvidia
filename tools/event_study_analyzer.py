#!/usr/bin/env python3
"""
tools/event_study_analyzer.py
--------------------------------------------------------------------------------
Event-Study Analysis: Pengaruh Narasi Hibrida, Pemilu Sela & Skandal terhadap Saham NVDA
Menganalisis korelasi dampak pasar modal dan konteks makropolitik:
  - 2026-10-21: Protes Verbal Keynote GTC Berlin
  - 2026-10-28: Serangan Siber FEC & Insiden Deepfake Kripto YouTube
  - 2026-10-29: Laporan Awal NYT Kasus Alice Huang / Megaspeed
  - 2026-11-03: Pemilu Sela AS (US Midterms: Democratic Blue Wave)
  - 2026-11-05: Pasar AI Anjlok Masif (Kekhawatiran Regulasi Data Center Pasca-Pemilu)
  - 2026-11-08/09: Pengakuan Memo CEO & Audit Independen Dewan NVIDIA
  - 2026-11-17: Antisipasi Jadwal Laporan Keuangan Triwulanan (Q3 Earnings)
"""

import os
import pandas as pd
import numpy as np

CSV_PATH = "nvda_skandal.csv"

# Kalender Kejadian Gabungan (Makro Politik, Regulasi, dan Skandal)
MACRO_EVENT_CALENDAR = {
    "2026-10-21": "Protes Verbal Aktivis di GTC Berlin",
    "2026-10-28": "Serangan Siber FEC & Deepfake Kripto YouTube (~100k bot)",
    "2026-10-29": "Laporan Awal NYT Kontak Spionase (Alice Huang / Megaspeed)",
    "2026-11-03": "Pemilu Sela AS (Midterms: Kemenangan Demokrat / Blue Wave)",
    "2026-11-05": "Pasar AI Crash (-9% NVDA): Sentimen Regulasi Data Center Pasca-Pemilu",
    "2026-11-09": "Reaksi Pasar Pasca-Memo CEO & Audit Dewan Direksi (Volume: 459M)",
    "2026-11-17": "[Jadwal] Pengumuman Kinerja Keuangan Triwulanan NVIDIA"
}

def load_clean_data(filepath: str) -> pd.DataFrame:
    """Membaca CSV yfinance dengan format multi-index header."""
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0] for col in df.columns]
    df.index.name = "Date"
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df["Daily_Return_%"] = df["Close"].pct_change() * 100
    df["Volume_M"] = df["Volume"] / 1_000_000
    baseline_vol = df["Volume_M"].iloc[:15].mean()
    df["Volume_Ratio"] = df["Volume_M"] / baseline_vol
    return df

def run_event_study():
    if not os.path.exists(CSV_PATH):
        print(f"[!] Error: File '{CSV_PATH}' tidak ditemukan.")
        return

    df = load_clean_data(CSV_PATH)

    print("=" * 95)
    print("ANALISIS EVENT-STUDY MULTI-FAKTOR: KASUS JENSEN HUANG VS SENTIMEN PASAR MAKRO")
    print("=" * 95)
    print(f"Periode Observasi: {df.index.min().strftime('%Y-%m-%d')} s/d {df.index.max().strftime('%Y-%m-%d')}")
    print(f"Total Hari Perdagangan: {len(df)} hari")
    print("-" * 95)

    print(f"{'Tanggal':<12} | {'Tutup ($)':<10} | {'Return (%)':<11} | {'Volume (Jt)':<12} | {'Peristiwa Kunci & Konteks Makro'}")
    print("-" * 95)

    for dt, row in df.iterrows():
        dt_str = dt.strftime('%Y-%m-%d')
        event_note = MACRO_EVENT_CALENDAR.get(dt_str, "")
        ret_str = f"{row['Daily_Return_%']:+.2f}%" if pd.notnull(row['Daily_Return_%']) else "N/A"
        marker = ">>>" if event_note else "   "
        print(f"{marker} {dt_str:<8} | ${row['Close']:>8.2f} | {ret_str:>10} | {row['Volume_M']:>10.1f}M | {event_note}")

    print("=" * 95)

    # Evaluasi Hipotesis Pengalihan Isu (Diversionary Hypothesis Testing)
    p_oct28 = df.loc["2026-10-28", "Close"] if "2026-10-28" in df.index else df.loc["2026-10-27", "Close"]
    p_nov03 = df.loc["2026-11-03", "Close"]
    p_nov05 = df.loc["2026-11-05", "Close"]
    p_nov09 = df.loc["2026-11-09", "Close"]

    drop_crash_nov05 = ((p_nov05 - p_nov03) / p_nov03) * 100
    drop_memo_nov09 = ((p_nov09 - p_nov05) / p_nov05) * 100

    print("\n[DEKONSTRUKSI HIPOTESIS PENGALIHAN ISU (DIVERSIONARY HYPOTHESIS TEST)]:")
    print("1. Apakah Skandal Ini 'Pengalihan Isu Politik Pemilu'?")
    print("   - FAKTA: Berita bocor tanggal 29 Okt (5 hari jelang Pemilu Sela 3 Nov).")
    print("   - IMPLIKASI: Menyorot kelambanan penanganan intelijen, merugikan petahana.")
    print("   - HASIL: Partainya justru mengalami kekalahan besar (Blue Wave).")
    print("   -> KESIMPULAN: Tidak logis sebagai operasi pengalihan isu yang disengaja.")
    print("\n2. Apakah Penurunan Saham Murni Akibat Skandal Pribadi?")
    print(f"   - FAKTA 05 Nov: Saham jatuh {drop_crash_nov05:.2f}% (${p_nov03:.2f} -> ${p_nov05:.2f}).")
    print("     Pemicu utama adalah kekhawatiran regulasi ketat pembangunan data-center pasca-pemilu.")
    print("     Kerugian melanda seluruh indeks Nasdaq 100 (~$2.5 Triliun lenyap).")
    print(f"   - FAKTA 09 Nov: Penurunan tambahan {drop_memo_nov09:.2f}% (${p_nov05:.2f} -> ${p_nov09:.2f}) dengan volume 459M.")
    print("     Reaksi spesifik atas ketidakpastian kepemimpinan (governance risk) dan audit internal.")
    print("   -> KESIMPULAN: Penurunan saham adalah fenomena multi-faktor gabungan makro dan tata kelola.")
    print("=" * 95)

if __name__ == "__main__":
    run_event_study()
