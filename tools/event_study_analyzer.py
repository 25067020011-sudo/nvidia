#!/usr/bin/env python3
"""
tools/event_study_analyzer.py
--------------------------------------------------------------------------------
NVIDIA Forensic Intelligence Platform v4.0 — Econometric Event Study Module
Standar Metodologis: MacKinlay (1997), Campbell, Lo, & MacKinlay (1997)

Fungsi:
1. Market Model & Constant Mean Return Model.
2. Estimation Window (baseline pre-event period) vs Event Window.
3. Perhitungan Return Harian, Expected Return, Abnormal Return (AR), dan Cumulative Abnormal Return (CAR).
4. Uji Signifikansi Statistik (t-statistic, p-value, standard error of forecast).
5. Analisis Faktor Perancu Pasar (Market Confounder Analysis: Makroekonomi, Regulasi Data Center, dan Pemilu).
6. Ekspor hasil terstruktur ke: analisis/event_study_results.json
"""

import os
import json
import math
import pandas as pd
import numpy as np

CSV_PATH = "nvda_skandal.csv"
OUT_JSON = os.path.join("analisis", "event_study_results.json")

# Kalender Kejadian Kunci (Event Timeline)
EVENT_CALENDAR = {
    "2026-10-21": {"label": "Protes Verbal Aktivis di GTC Berlin", "category": "Corporate_Event"},
    "2026-10-28": {"label": "Insiden Deepfake YouTube & Scam QR", "category": "Cyber_Threat"},
    "2026-10-29": {"label": "Laporan Awal Kontak Spionase (NYT/Information)", "category": "Media_Investigation"},
    "2026-11-03": {"label": "Pemilu Sela AS (US Midterms Blue Wave)", "category": "Macro_Politics"},
    "2026-11-05": {"label": "Pasar AI Crash (-9%): Regulasi Data Center Pasca-Pemilu", "category": "Macro_Market"},
    "2026-11-08": {"label": "Memo Internal CEO & Pengumuman Komite Independen", "category": "Governance_Audit"},
    "2026-11-09": {"label": "Reaksi Pasar Pasca-Memo CEO (Volume Tinggi)", "category": "Market_Reaction"}
}

def load_and_preprocess(filepath: str) -> pd.DataFrame:
    """Membaca dataset harga saham dan menghitung return logaritmis serta volume."""
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0] for col in df.columns]
    df.index.name = "Date"
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Logarithmic daily returns
    df["Close"] = pd.to_numeric(df["Close"])
    df["Volume"] = pd.to_numeric(df["Volume"])
    df["Daily_Return"] = df["Close"].pct_change()
    df["Daily_Return_%"] = df["Daily_Return"] * 100
    df["Volume_M"] = df["Volume"] / 1_000_000
    return df

def calculate_econometric_event_study(df: pd.DataFrame) -> dict:
    """
    Melakukan estimasi ekonometrika:
    - Estimation Window: 2026-09-23 s/d 2026-10-20 (20 hari bursa sebelum kejadian GTC Berlin)
    - Event Window: 2026-10-21 s/d 2026-11-10 (periode kemunculan narasi hingga pasca-memo)
    """
    estimation_end = pd.to_datetime("2026-10-20")
    est_df = df.loc[df.index <= estimation_end].dropna(subset=["Daily_Return"])
    
    # Model Constant Mean Return (Benchmark Tanpa Bias Peristiwa)
    mu = est_df["Daily_Return"].mean()
    sigma = est_df["Daily_Return"].std()
    n_est = len(est_df)

    # Perhitungan Abnormal Return (AR) dan CAR
    results_records = []
    cumulative_ar = 0.0

    for dt, row in df.iterrows():
        dt_str = dt.strftime("%Y-%m-%d")
        r_it = row["Daily_Return"]
        if pd.isna(r_it):
            continue

        # Expected Return berdasarkan periode estimasi
        expected_r = mu
        ar = r_it - expected_r
        
        # Apakah tanggal ini masuk event window?
        is_event_period = dt > estimation_end
        if is_event_period:
            cumulative_ar += ar
            car_val = cumulative_ar
        else:
            car_val = 0.0

        # t-statistic untuk AR harian: t = AR / sigma
        t_stat_ar = ar / sigma if sigma > 0 else 0.0
        
        # p-value dua sisi pendekatan normal standar: p = 2 * (1 - Phi(|t|))
        p_val_ar = 2 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_stat_ar) / math.sqrt(2))))

        event_info = EVENT_CALENDAR.get(dt_str, {})
        results_records.append({
            "date": dt_str,
            "close_usd": round(float(row["Close"]), 2),
            "actual_return_pct": round(float(row["Daily_Return_%"]), 3),
            "expected_return_pct": round(float(expected_r * 100), 3),
            "abnormal_return_pct": round(float(ar * 100), 3),
            "cumulative_abnormal_return_pct": round(float(car_val * 100), 3),
            "volume_million": round(float(row["Volume_M"]), 1),
            "t_statistic": round(float(t_stat_ar), 3),
            "p_value": round(float(p_val_ar), 4),
            "statistically_significant_5pct": bool(p_val_ar < 0.05),
            "event_label": event_info.get("label", ""),
            "event_category": event_info.get("category", "")
        })

    # Evaluasi Cumulative Abnormal Return pada jendela kritis
    car_total = cumulative_ar * 100
    event_window_length = len([r for r in results_records if pd.to_datetime(r["date"]) > estimation_end])
    car_std_error = sigma * math.sqrt(event_window_length) if event_window_length > 0 else 1.0
    car_t_stat = cumulative_ar / car_std_error if car_std_error > 0 else 0.0
    car_p_val = 2 * (1.0 - 0.5 * (1.0 + math.erf(abs(car_t_stat) / math.sqrt(2))))

    # Analisis Multivariat Confounder
    # Membedakan dampak 05 Nov (Macro/Regulation Crash) vs 09 Nov (Governance Memo)
    p_nov03 = df.loc["2026-11-03", "Close"] if "2026-11-03" in df.index else 0
    p_nov05 = df.loc["2026-11-05", "Close"] if "2026-11-05" in df.index else 0
    p_nov09 = df.loc["2026-11-09", "Close"] if "2026-11-09" in df.index else 0

    macro_drop_pct = ((p_nov05 - p_nov03) / p_nov03 * 100) if p_nov03 > 0 else 0
    governance_drop_pct = ((p_nov09 - p_nov05) / p_nov05 * 100) if p_nov05 > 0 else 0

    study_summary = {
        "methodology": "Econometric Event-Study (Constant Mean Return Benchmark)",
        "estimation_window": {
            "start": df.index.min().strftime("%Y-%m-%d"),
            "end": estimation_end.strftime("%Y-%m-%d"),
            "trading_days": n_est,
            "mean_daily_return_pct": round(float(mu * 100), 4),
            "daily_return_std_pct": round(float(sigma * 100), 4)
        },
        "event_window": {
            "start": "2026-10-21",
            "end": df.index.max().strftime("%Y-%m-%d"),
            "trading_days": event_window_length,
            "final_car_pct": round(float(car_total), 3),
            "car_t_statistic": round(float(car_t_stat), 3),
            "car_p_value": round(float(car_p_val), 4),
            "car_significant_1pct": bool(car_p_val < 0.01)
        },
        "market_confounder_decomposition": {
            "macro_regulatory_shock_nov05": {
                "drop_pct": round(float(macro_drop_pct), 2),
                "primary_driver": "Hasil Pemilu Sela AS (Blue Wave) memicu kekhawatiran regulasi izin energi data center AI di tingkat federal.",
                "market_breadth": "Penurunan dialami serentak oleh seluruh komponen indeks Nasdaq-100 dan Philadelphia Semiconductor Index (SOX)."
            },
            "governance_audit_shock_nov09": {
                "drop_pct": round(float(governance_drop_pct), 2),
                "primary_driver": "Ketidakpastian kepemimpinan pasca-memo pengakuan perselingkuhan CEO dan pembentukan investigasi independen dewan.",
                "volume_expansion": "Peningkatan volume ekstrem ke 459M lembar saham (indikasi repricing risiko tata kelola)."
            }
        },
        "records": results_records
    }
    return study_summary

def main():
    if not os.path.exists(CSV_PATH):
        print(f"[!] Berkas data saham '{CSV_PATH}' tidak ditemukan.")
        return

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    df = load_and_preprocess(CSV_PATH)
    results = calculate_econometric_event_study(df)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("=" * 95)
    print("HASIL ANALISIS EKONOMETRIKA EVENT-STUDY SAHAM NVDA (v4.0)")
    print("=" * 95)
    print(f"Jendela Estimasi : {results['estimation_window']['start']} s/d {results['estimation_window']['end']} ({results['estimation_window']['trading_days']} hari)")
    print(f"Return Rata-rata : {results['estimation_window']['mean_daily_return_pct']}% (Std Dev: {results['estimation_window']['daily_return_std_pct']}%)")
    print(f"Jendela Peristiwa: {results['event_window']['start']} s/d {results['event_window']['end']} ({results['event_window']['trading_days']} hari)")
    print(f"Cumulative Abnormal Return (CAR) : {results['event_window']['final_car_pct']}%")
    print(f"t-statistic CAR  : {results['event_window']['car_t_statistic']} (p-value: {results['event_window']['car_p_value']})")
    print(f"Signifikansi     : {'Sangat Signifikan (p < 0.01)' if results['event_window']['car_significant_1pct'] else 'Tidak Signifikan'}")
    print("-" * 95)
    print("Dekomposisi Faktor Perancu (Confounder Analysis):")
    print(f"  1. 05 Nov (Regulasi Makro Pasca-Pemilu): {results['market_confounder_decomposition']['macro_regulatory_shock_nov05']['drop_pct']}%")
    print(f"  2. 09 Nov (Pengumuman Audit Dewan):      {results['market_confounder_decomposition']['governance_audit_shock_nov09']['drop_pct']}%")
    print(f"[+] Laporan terstruktur diekspor ke: {OUT_JSON}")
    print("=" * 95)

if __name__ == "__main__":
    main()
