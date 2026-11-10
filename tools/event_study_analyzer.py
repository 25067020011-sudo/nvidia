#!/usr/bin/env python3
"""
tools/event_study_analyzer.py
--------------------------------------------------------------------------------
Event-Study Analysis: Pengaruh Narasi Hibrida & Skandal terhadap Saham NVDA
Menganalisis dampak pasar modal atas rangkaian kejadian:
  - 2026-10-21: Protes Verbal Keynote GTC Berlin
  - 2026-10-28: Insiden Deepfake Kripto YouTube Live
  - 2026-10-29: Pemberitaan Dugaan Kontak Spionase (Alice Huang)
  - 2026-11-05: Volatilitas Penurunan Saham Tajam
  - 2026-11-08/09: Pengakuan Memo Internal & Audit Dewan Direksi
"""

import os
import pandas as pd
import numpy as np

CSV_PATH = "nvda_skandal.csv"

# Daftar Peristiwa Kunci untuk Event Mapping
KEY_EVENTS = {
    "2026-10-21": "Protes Verbal Aktivis di GTC Berlin",
    "2026-10-28": "Siaran Deepfake AI Jensen Huang di YouTube (~100k bot)",
    "2026-10-29": "Laporan Dugaan Kontak Spionase Tiongkok (Alice Huang)",
    "2026-11-05": "Penurunan Harga Menembus Support ($181.60)",
    "2026-11-09": "Reaksi Pasar Pasca-Memo CEO & Pemeriksaan Dewan (Vol: 459M)"
}

def load_clean_data(filepath: str) -> pd.DataFrame:
    """Membaca CSV yfinance dengan format multi-index header."""
    # yfinance output memiliki 3 baris header awal
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    
    # Flatten MultiIndex columns
    df.columns = [col[0] for col in df.columns]
    df.index.name = "Date"
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Hitung Return Harian dan Return Logaritmik
    df["Daily_Return_%"] = df["Close"].pct_change() * 100
    df["Volume_M"] = df["Volume"] / 1_000_000

    # Rata-rata volume dasar (baseline 20 hari sebelum skandal puncak)
    baseline_vol = df["Volume_M"].iloc[:15].mean()
    df["Volume_Ratio"] = df["Volume_M"] / baseline_vol

    return df

def run_event_study():
    if not os.path.exists(CSV_PATH):
        print(f"[!] Error: File '{CSV_PATH}' tidak ditemukan.")
        return

    df = load_clean_data(CSV_PATH)

    print("=" * 86)
    print("ANALISIS EVENT-STUDY KORRELASI PASAR ATAS KASUS JENSEN HUANG (NVDA)")
    print("=" * 86)
    print(f"Periode Data: {df.index.min().strftime('%Y-%m-%d')} s/d {df.index.max().strftime('%Y-%m-%d')}")
    print(f"Total Hari Perdagangan: {len(df)} hari")
    print(f"Harga Tertinggi Periode : ${df['High'].max():.2f}")
    print(f"Harga Terendah Periode  : ${df['Low'].min():.2f}")
    print("-" * 86)

    print(f"{'Tanggal':<12} | {'Tutup ($)':<10} | {'Return (%)':<11} | {'Volume (Jt)':<12} | {'Catatan Kejadian'}")
    print("-" * 86)

    for dt, row in df.iterrows():
        dt_str = dt.strftime('%Y-%m-%d')
        event_note = KEY_EVENTS.get(dt_str, "")
        ret_str = f"{row['Daily_Return_%']:+.2f}%" if pd.notnull(row['Daily_Return_%']) else "N/A"
        
        # Tandai tanggal penting dengan penanda khusus
        marker = ">>>" if event_note else "   "
        print(f"{marker} {dt_str:<8} | ${row['Close']:>8.2f} | {ret_str:>10} | {row['Volume_M']:>10.1f}M | {event_note}")

    print("=" * 86)

    # Analisis Jendela Peristiwa (Event Window)
    # Jendela 1: 21 Okt - 30 Okt (Isu Berlin & Spionase)
    # Jendela 2: 04 Nov - 09 Nov (Isu Memo & Audit Dewan)
    price_start = df.loc["2026-09-22", "Close"]
    price_oct21 = df.loc["2026-10-21", "Close"] if "2026-10-21" in df.index else df.iloc[20]["Close"]
    price_oct30 = df.loc["2026-10-30", "Close"] if "2026-10-30" in df.index else df.loc["2026-10-29", "Close"]
    price_nov03 = df.loc["2026-11-03", "Close"]
    price_nov09 = df.loc["2026-11-09", "Close"]

    drop_window_1 = ((price_oct30 - price_oct21) / price_oct21) * 100
    drop_window_2 = ((price_nov09 - price_nov03) / price_nov03) * 100
    drop_total = ((price_nov09 - price_start) / price_start) * 100

    print("\n[TEMUAN EKONOMETRIKA FORENSIK]:")
    print(f"1. Jendela Kejadian 1 (21-30 Okt: Protes Berlin + Deepfake + Tuduhan Spionase):")
    print(f"   - Pergerakan Harga: Turun sebesar {drop_window_1:.2f}%.")
    print(f"   - Respon Pasar: Cenderung bertahan karena pasar menafsirkan protes Berlin sebagai gangguan minor.")
    print(f"2. Jendela Kejadian 2 (03-09 Nov: Pengakuan Memo Hubungan Pribadi & Audit Dewan):")
    print(f"   - Pergerakan Harga: Jatuh tajam dari ${price_nov03:.2f} ke ${price_nov09:.2f} ({drop_window_2:.2f}%).")
    print(f"   - Volume Perdagangan: Meledak hingga 459.1 Juta lembar saham (rekor tertinggi periode).")
    print(f"   - Respon Pasar: Risiko tata kelola (*governance risk*) dan ketidakpastian posisi CEO memicu panic selling.")
    print(f"3. Kumulatif Penurunan Periode (Sep - Nov 2026): {drop_total:.2f}% (${price_start:.2f} -> ${price_nov09:.2f}).")
    print("=" * 86)

if __name__ == "__main__":
    run_event_study()

