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

Mengekspor hasil evaluasi komprehensif ke: analisis/02_status_klaim.csv
"""

import os
import csv
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class EvidencePoint:
    source_name: str
    source_type: str  # 'Official_Filing', 'Mainstream_Press', 'Social_Media', 'Forensic_Lab', 'Economic_Data'
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
                if ev.source_type in ['Forensic_Lab', 'Economic_Data']:
                    has_forensic_debunk = True

        total_weight = support_score + refute_score

        # Logika Penentuan Label Kebenaran Bertingkat
        if has_official_refutation or (has_forensic_debunk and refute_score > support_score) or (refute_score >= 2.0 and support_score <= 0.5):
            status = "FABRICATED / DISINFORMATION (Palsu/Distorsi)"
            confidence = min(0.99, 0.75 + (refute_score * 0.08))
            rationale = (
                "Klaim terbantahkan secara definitif oleh data primer resmi, data ekonomi riil, "
                "dan/atau analisis laboratorium forensik (terbukti distorsi konteks, rekayasa, atau spekulasi tanpa dasar)."
            )
        elif support_score >= 1.5 and any(e.source_type == 'Official_Filing' for e in claim.evidence_list if e.claim_support == 'SUPPORTS'):
            status = "CONFIRMED (Terkonfirmasi Dokumen Resmi)"
            confidence = min(0.99, 0.80 + (support_score * 0.1))
            rationale = "Klaim didukung penuh oleh dokumen hukum/korporasi primer resmi."
        elif support_score >= 1.0 and any(e.source_type == 'Mainstream_Press' for e in claim.evidence_list if e.claim_support == 'SUPPORTS'):
            status = "REPORTED (Dilaporkan Media Kredibel)"
            confidence = 0.75
            rationale = "Klaim dilaporkan oleh jurnalisme investigatif kredibel, namun masih dalam proses audit/penyelidikan dewan."
        else:
            status = "UNVERIFIED / SPECULATIVE (Belum Terverifikasi)"
            confidence = 0.40
            rationale = "Tidak ditemukan bukti primer atau liputan kredibel yang dapat memverifikasi klaim."

        claim.status_label = status
        claim.confidence_score = round(confidence, 2)
        claim.forensic_rationale = rationale
        return claim

def get_all_claim_evaluations() -> List[ClaimEvaluation]:
    """Menghimpun seluruh kasus klaim kunci seputar Jensen Huang (Oktober - November 2026)."""
    # Klaim 1: Serangan Fisik di Berlin
    c1 = ClaimEvaluation(
        claim_id="CLM-01-BERLIN-PHYSICAL",
        target_subject="Jensen Huang",
        claim_statement="Jensen Huang diserang secara fisik oleh pengunjuk rasa di panggung Keynote GTC Berlin",
        incident_date="2026-10-21",
        evidence_list=[
            EvidencePoint("The Next Web", "Mainstream_Press", 0.9, "https://thenextweb.com/news/huang-gtc-berlin-keynote-protest-nvidia-chips-russian-drones", "REFUTES"),
            EvidencePoint("Rekaman Video Keynote Resmi", "Forensic_Lab", 1.0, "YouTube Official Video Stream", "REFUTES"),
            EvidencePoint("Postingan X Viral Tanpa Sumber", "Social_Media", 0.2, "Klaim viral menghilangkan kata 'verbal'", "SUPPORTS")
        ]
    )

    # Klaim 2: Deepfake Siaran Kripto YouTube
    c2 = ClaimEvaluation(
        claim_id="CLM-02-YOUTUBE-DEEPFAKE",
        target_subject="Jensen Huang",
        claim_statement="Siaran YouTube mengumumkan program giveaway kripto resmi yang dibawakan langsung oleh Jensen Huang",
        incident_date="2026-10-28",
        evidence_list=[
            EvidencePoint("Tecnoblog", "Mainstream_Press", 0.85, "https://tecnoblog.net/noticias/transmissao-falsa-da-nvidia-engana-milhares-de-pessoas/", "REFUTES"),
            EvidencePoint("Laboratorium Media Forensik", "Forensic_Lab", 0.95, "Analisis Spektral & Lip-sync Wav2Lip", "REFUTES"),
            EvidencePoint("NVIDIA Newsroom Official", "Official_Filing", 1.0, "https://nvidianews.nvidia.com", "REFUTES")
        ]
    )

    # Klaim 3: Teori Konspirasi "Trump Dalang Penjebakan / Pengambilalihan NVIDIA"
    c3 = ClaimEvaluation(
        claim_id="CLM-03-TRUMP-TAKEOVER-CONSPIRACY",
        target_subject="Jensen Huang & Donald Trump",
        claim_statement="Donald Trump mendalangi penjebakan intelijen terhadap Jensen Huang untuk mengambil alih kendali/saham NVIDIA",
        incident_date="2026-11-08",
        evidence_list=[
            EvidencePoint("The Daily Beast", "Mainstream_Press", 0.90, "Penyelidikan Alice Huang sudah berjalan sejak era Biden", "REFUTES"),
            EvidencePoint("The Hill / NYT", "Mainstream_Press", 0.90, "Trump telah di-briefing setahun lalu tapi pasif dan tidak bertindak", "REFUTES"),
            EvidencePoint("Crypto Briefing / ABC7", "Mainstream_Press", 0.95, "Trump secara terbuka membela Huang dan menyebutnya brilliant", "REFUTES"),
            EvidencePoint("DNYUZ / NYT", "Mainstream_Press", 0.85, "Inisiator memo adalah Menlu Marco Rubio & faksi China hawks, bukan Trump", "REFUTES"),
            EvidencePoint("Klaim Spekulatif Anonim Media Sosial", "Social_Media", 0.25, "Analogi spekulatif pengambilalihan 10% saham Intel 2025", "SUPPORTS")
        ]
    )

    # Klaim 4: Teori Konspirasi "Elon Musk Dalang Penjatuhan Jensen Huang"
    c4 = ClaimEvaluation(
        claim_id="CLM-04-MUSK-MASTERMIND-CONSPIRACY",
        target_subject="Jensen Huang & Elon Musk",
        claim_statement="Elon Musk mendalangi atau menggerakkan skandal intelijen untuk menjatuhkan Jensen Huang demi keuntungan pribadi xAI/Tesla",
        incident_date="2026-11-08",
        evidence_list=[
            EvidencePoint("AOL / Bloomberg - Data Belanja Tesla", "Economic_Data", 0.95, "Tesla menganggarkan belanja kumulatif $10 Miliar chip NVIDIA hingga akhir 2026", "REFUTES"),
            EvidencePoint("roic.ai - Kesepakatan Infrastruktur xAI", "Economic_Data", 0.95, "xAI menandatangani kemitraan cluster $20 Miliar untuk superkomputer Colossus 2", "REFUTES"),
            EvidencePoint("Pernyataan Resmi Rekor Publik Jensen Huang", "Official_Filing", 0.90, "Huang memuji Musk sebagai 'the ultimate GPU' dan mitra terdekat", "REFUTES"),
            EvidencePoint("Analisis Rasionalitas Ekonomi Industri AI", "Forensic_Lab", 0.95, "Logika terbalik: Musk bergantung 100% pada chip NVIDIA untuk Grok & FSD; jatuhnya Huang melumpuhkan roadmap Musk", "REFUTES"),
            EvidencePoint("Unggahan X 23 Okt 2025", "Social_Media", 0.30, "Unggahan 'If she's a 10, you're an asset' adalah komentar sinis tanpa menyebut subjek dan tanpa kaitan operasional", "SUPPORTS")
        ]
    )

    return [c1, c2, c3, c4]

def export_claims_csv(evaluations: List[ClaimEvaluation], output_path: str):
    """Mengekspor matriks status klaim ke berkas CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []
    for c in evaluations:
        rows.append({
            "claim_id": c.claim_id,
            "target_subject": c.target_subject,
            "claim_statement": c.claim_statement,
            "incident_date": c.incident_date,
            "status_label": c.status_label,
            "confidence_score": c.confidence_score,
            "forensic_rationale": c.forensic_rationale,
            "total_evidence_sources": len(c.evidence_list)
        })
        
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "claim_id", "target_subject", "claim_statement", "incident_date",
            "status_label", "confidence_score", "forensic_rationale", "total_evidence_sources"
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[+] Berhasil mengekspor {len(rows)} evaluasi klaim ke: {output_path}")

def main():
    engine = TieredTruthEngine()
    claims = get_all_claim_evaluations()
    results = [engine.evaluate(c) for c in claims]

    print("=" * 85)
    print("HASIL EVALUASI TIERED TRUTH CLASSIFICATION ENGINE")
    print("=" * 85)
    for res in results:
        print(f"\n[ID: {res.claim_id}]")
        print(f"  Subjek Target    : {res.target_subject}")
        print(f"  Pernyataan Klaim : \"{res.claim_statement}\"")
        print(f"  Tanggal          : {res.incident_date}")
        print(f"  Klasifikasi      : {res.status_label}")
        print(f"  Tingkat Keyakinan: {res.confidence_score * 100:.0f}%")
        print(f"  Alasan Forensik  : {res.forensic_rationale}")

    csv_out = "analisis/02_status_klaim.csv"
    export_claims_csv(results, csv_out)
    print("=" * 85)

if __name__ == "__main__":
    main()
