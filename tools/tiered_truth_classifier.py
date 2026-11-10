#!/usr/bin/env python3
"""
tools/tiered_truth_classifier.py
--------------------------------------------------------------------------------
Sistem Klasifikasi Kebenaran Bertingkat (Tiered Truth Classifier)
Modul untuk menguji dan mengelompokkan klaim viral publik ke dalam 4 kategori:
  1. CONFIRMED (Terkonfirmasi - Bukti primer resmi / SEC / Pengadilan / Kontrol)
  2. REPORTED (Dilaporkan - Investigasi media kredibel / Audit dewan)
  3. UNVERIFIED (Belum Terverifikasi - Spekulasi anonim / Tanpa rekaman)
  4. FABRICATED / DISINFORMATION (Palsu - Terbukti manipulasi deepfake / Distorsi konteks)
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class EvidencePoint:
    source_name: str
    source_type: str  # 'Official_Filing', 'Mainstream_Press', 'Social_Media', 'Forensic_Lab'
    credibility_weight: float  # 0.0 to 1.0
    url_or_ref: str
    claim_support: str  # 'SUPPORTS', 'REFUTES', 'NEUTRAL'

@dataclass
class ClaimEvaluation:
    claim_id: str
    target_subject: str
    claim_statement: str
    incident_date: str
    evidence_list: List[EvidencePoint]
    status_label: Optional[str] = None
    confidence_score: Optional[float] = None
    forensic_rationale: Optional[str] = None

class TieredTruthEngine:
    @staticmethod
    def evaluate(claim: ClaimEvaluation) -> ClaimEvaluation:
        support_score = 0.0
        refute_score = 0.0
        has_official_refutation = False
        has_forensic_debunk = False

        for ev in claim.evidence_list:
            weight = ev.credibility_weight
            if ev.claim_support == 'SUPPORTS':
                support_score += weight
            elif ev.claim_support == 'REFUTES':
                refute_score += weight
                if ev.source_type == 'Official_Filing':
                    has_official_refutation = True
                if ev.source_type == 'Forensic_Lab':
                    has_forensic_debunk = True

        total_weight = support_score + refute_score
        net_ratio = (support_score / total_weight) if total_weight > 0 else 0.5

        # Logika Penentuan Label Kebenaran Bertingkat
        if has_official_refutation or (has_forensic_debunk and refute_score > support_score):
            status = "FABRICATED / DISINFORMATION (Palsu/Distorsi)"
            confidence = min(0.99, 0.70 + (refute_score * 0.1))
            rationale = (
                "Klaim terbantahkan secara definitif oleh data primer resmi dan/atau "
                "analisis laboratorium forensik (bukti distorsi konteks atau rekayasa media)."
            )
        elif support_score >= 1.5 and any(e.source_type == 'Official_Filing' for e in claim.evidence_list if e.claim_support == 'SUPPORTS'):
            status = "CONFIRMED (Terkonfirmasi)"
            confidence = min(0.99, 0.80 + (support_score * 0.1))
            rationale = "Klaim didukung oleh dokumen hukum/korporasi primer resmi."
        elif support_score >= 1.0 and any(e.source_type == 'Mainstream_Press' for e in claim.evidence_list if e.claim_support == 'SUPPORTS'):
            status = "REPORTED (Dilaporkan Media Kredibel)"
            confidence = 0.75
            rationale = "Klaim dilaporkan oleh jurnalisme investigatif kredibel, namun masih dalam proses audit/penyelidikan."
        else:
            status = "UNVERIFIED (Belum Terverifikasi)"
            confidence = 0.40
            rationale = "Tidak ditemukan bukti primer atau liputan kredibel yang dapat memverifikasi klaim."

        claim.status_label = status
        claim.confidence_score = round(confidence, 2)
        claim.forensic_rationale = rationale
        return claim

def run_sample_evaluations():
    """Menguji kasus nyata seputar Jensen Huang (Oktober - November 2026)."""
    # Kasus 1: Klaim Serangan Fisik di Berlin
    c1 = ClaimEvaluation(
        claim_id="CLM-01-BERLIN-PHYSICAL",
        target_subject="Jensen Huang",
        claim_statement="Jensen Huang diserang secara fisik oleh pengunjuk rasa di panggung Keynote Berlin",
        incident_date="2026-10-21",
        evidence_list=[
            EvidencePoint("The Next Web", "Mainstream_Press", 0.9, "https://thenextweb.com/news/huang-gtc-berlin-keynote-protest-nvidia-chips-russian-drones", "REFUTES"),
            EvidencePoint("Rekaman Video Keynote Resmi", "Forensic_Lab", 1.0, "YouTube Official Video Stream", "REFUTES"),
            EvidencePoint("Postingan X Viral Tanpa Sumber", "Social_Media", 0.2, "https://x.com/...", "SUPPORTS")
        ]
    )

    # Kasus 2: Deepfake Siaran Kripto YouTube
    c2 = ClaimEvaluation(
        claim_id="CLM-02-YOUTUBE-DEEPFAKE",
        target_subject="Jensen Huang",
        claim_statement="Siaran YouTube mengumumkan program giveaway kripto resmi oleh Jensen Huang",
        incident_date="2026-10-28",
        evidence_list=[
            EvidencePoint("Tecnoblog", "Mainstream_Press", 0.85, "https://tecnoblog.net/noticias/transmissao-falsa-da-nvidia-engana-milhares-de-pessoas/", "REFUTES"),
            EvidencePoint("Laboratorium Media Forensik", "Forensic_Lab", 0.95, "Analisis Spektral & Lip-sync", "REFUTES"),
            EvidencePoint("NVIDIA Newsroom Official", "Official_Filing", 1.0, "https://nvidianews.nvidia.com", "REFUTES")
        ]
    )

    engine = TieredTruthEngine()
    results = [engine.evaluate(c1), engine.evaluate(c2)]

    print("=" * 80)
    print("HASIL EVALUASI TIERED TRUTH CLASSIFICATION ENGINE")
    print("=" * 80)
    for res in results:
        print(f"\n[ID: {res.claim_id}]")
        print(f"  Pernyataan Klaim : \"{res.claim_statement}\"")
        print(f"  Tanggal          : {res.incident_date}")
        print(f"  Klasifikasi      : {res.status_label}")
        print(f"  Tingkat Keyakinan: {res.confidence_score * 100}%")
        print(f"  Alasan Forensik  : {res.forensic_rationale}")

if __name__ == "__main__":
    run_sample_evaluations()

