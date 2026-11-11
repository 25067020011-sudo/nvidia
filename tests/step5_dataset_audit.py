import csv
import json
import os
import sys

DATASETS = [
    ("berita_skandal_jensen_huang.csv", "csv", 300),
    ("nvda_skandal.csv", "csv", 35),
    ("analisis/01_timeline_kemunculan_pertama.csv", "csv", 7),
    ("analisis/02_status_klaim.csv", "csv", 4),
    ("analisis/08_komparasi_metode_intelijen.csv", "csv", 9),
    ("analisis/09_osint_artefak.csv", "csv", 11),
    ("analisis/matriks_sna_20_aktor.csv", "csv", 20),
    ("analisis/matriks_sna_10_media.csv", "csv", 10),
    ("analisis/audit_historis_sec_20tahun.json", "json", None),
    ("analisis/event_study_results.json", "json", None),
    ("analisis/sna_metrics_summary.json", "json", None)
]

print("=== STEP 5: DATASET & REPRODUCIBILITY AUDIT ===")
all_valid = True

for path, ftype, min_rows in DATASETS:
    if not os.path.exists(path):
        print(f"[FAIL] Missing dataset: {path}")
        all_valid = False
        continue

    try:
        if ftype == "csv":
            with open(path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
            if not rows:
                print(f"[FAIL] Empty CSV: {path}")
                all_valid = False
                continue
            header = rows[0]
            widths = [len(r) for r in rows[1:]]
            inconsistent = [i+2 for i, w in enumerate(widths) if w != len(header)]
            if inconsistent:
                print(f"[FAIL] {path} has inconsistent column widths at rows: {inconsistent[:5]}")
                all_valid = False
            else:
                row_count = len(rows) - 1
                print(f"[PASS] {path}: {row_count} rows, {len(header)} cols, 100% consistent schema.")
        elif ftype == "json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"[PASS] {path}: valid JSON ({type(data).__name__}).")
    except Exception as e:
        print(f"[FAIL] {path}: parse error {e}")
        all_valid = False

if all_valid:
    print("ALL DATASETS VALIDATED SUCCESSFULLY.")
else:
    sys.exit(1)

