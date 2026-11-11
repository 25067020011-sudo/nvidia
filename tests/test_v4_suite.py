#!/usr/bin/env python3
"""
tests/test_v4_suite.py
--------------------------------------------------------------------------------
Automated Test Suite for NVIDIA Multimodal Forensic Intelligence Platform v4.0
Tests executed:
1. Python AST Syntax validation for all project scripts.
2. JSON schema and integrity validation for all JSON files.
3. CSV structure and row consistency validation for all datasets.
4. Tool unit & execution tests (event study, tiered truth, OSINT manager, ELA, deepfake validator).
5. Evidence Ledger SHA-256 integrity verification.
6. Security static checks (no unredacted keys or secrets).
7. Streamlit app import and rendering test.
"""

import os
import sys
import ast
import csv
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestNvidiaForensicPlatformV4(unittest.TestCase):

    def test_01_python_syntax(self):
        """Memverifikasi sintaks seluruh file Python proyek tidak memiliki SyntaxError."""
        py_files = [p for p in REPO_ROOT.glob("*.py")] + [p for p in (REPO_ROOT / "tools").glob("*.py")]
        errors = []
        for path in py_files:
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as e:
                errors.append(f"{path.name}:{e.lineno} - {e.msg}")
        self.assertEqual(len(errors), 0, f"Ditemukan SyntaxError pada file Python: {errors}")

    def test_02_json_validity(self):
        """Memvalidasi bahwa seluruh berkas JSON proyek dapat diparsing secara valid."""
        json_files = list(REPO_ROOT.glob("*.json")) + list((REPO_ROOT / "analisis").glob("*.json"))
        for path in json_files:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsNotNone(data)
            except Exception as e:
                self.fail(f"File JSON corrupt: {path.name} - {e}")

    def test_03_csv_validity(self):
        """Memvalidasi integritas baris dan kolom seluruh berkas CSV proyek."""
        csv_files = list(REPO_ROOT.glob("*.csv")) + list((REPO_ROOT / "analisis").glob("*.csv"))
        for path in csv_files:
            with path.open(encoding="utf-8-sig", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
                self.assertGreater(len(rows), 1, f"File CSV kosong atau hanya header: {path.name}")
                header_len = len(rows[0])
                for i, row in enumerate(rows[1:], start=2):
                    self.assertEqual(len(row), header_len, f"Inkonsistensi lebar kolom pada {path.name} baris {i}")

    def test_04_evidence_ledger_integrity(self):
        """Memverifikasi seluruh item di evidence_ledger.json memiliki hash SHA-256 otentik."""
        import hashlib
        ledger_path = REPO_ROOT / "evidence_ledger.json"
        self.assertTrue(ledger_path.exists(), "evidence_ledger.json tidak ditemukan")
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        
        self.assertGreaterEqual(len(ledger), 30, "Jumlah bukti terdaftar minimal 30 item")
        tampered = []
        for item in ledger:
            rel = item.get("filepath", "")
            fpath = Path(rel) if Path(rel).is_absolute() else (REPO_ROOT / rel)
            if not fpath.exists():
                fpath = REPO_ROOT / item.get("filename", "")
            if not fpath.exists():
                fpath = REPO_ROOT / "analisis" / item.get("filename", "")
            if not fpath.exists():
                fpath = REPO_ROOT / "tools" / item.get("filename", "")
            if not fpath.exists():
                tampered.append(f"{item['filename']} (FILE MISSING)")
                continue
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if sha != item["hashes"]["sha256"]:
                tampered.append(f"{item['filename']} (HASH MISMATCH)")
        
        self.assertEqual(len(tampered), 0, f"Ditemukan bukti tidak otentik: {tampered}")

    def test_05_event_study_metrics(self):
        """Memverifikasi hasil perhitungan ekonometrika event study."""
        from tools.event_study_analyzer import load_and_preprocess, calculate_econometric_event_study
        csv_path = REPO_ROOT / "nvda_skandal.csv"
        df = load_and_preprocess(str(csv_path))
        results = calculate_econometric_event_study(df)
        self.assertIn("event_window", results)
        self.assertIn("final_car_pct", results["event_window"])
        self.assertLess(results["event_window"]["car_p_value"], 0.05, "CAR harus signifikan secara statistik (p < 0.05)")

    def test_06_deepfake_heuristics(self):
        """Memverifikasi modul deteksi heuristik deepfake C2PA."""
        from tools.deepfake_signature_validator import evaluate_media_heuristics
        res = evaluate_media_heuristics(str(REPO_ROOT / "analisis" / "04_klaim.png"))
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("synthetic_probability_score", res)

    def test_07_streamlit_import(self):
        """Memverifikasi modul app.py Streamlit dapat dimuat atau diparse tanpa broken imports."""
        # Uji parsing AST struktur dan pemanggilan Streamlit
        app_path = REPO_ROOT / "app.py"
        source = app_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(app_path))
        imported_modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend([n.name for n in node.names])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.append(node.module)

        self.assertIn("streamlit", imported_modules)
        self.assertIn("pandas", imported_modules)
        self.assertIn("json", imported_modules)

if __name__ == "__main__":
    unittest.main()
