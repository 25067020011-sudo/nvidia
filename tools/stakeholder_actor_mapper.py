#!/usr/bin/env python3
"""
tools/stakeholder_actor_mapper.py
--------------------------------------------------------------------------------
Pemetaan Aktor & Analisis Motif Kepentingan (Multi-Stakeholder Actor Mapping)
Mengklasifikasikan peran, motif yang dilaporkan secara faktual, serta membedakan
antara fakta primer, inferensi analitis, dan klaim tanpa bukti.
"""

import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class StakeholderProfile:
    entity_name: str
    category: str  # 'Corporate_Governance', 'Foreign_Entity', 'Legislative', 'Intelligence_Whistleblower'
    verified_actions: List[str]
    reported_motives: List[str]
    unsupported_conjectures: List[str]
    evidence_sources: List[str]

ACTOR_DATABASE = [
    StakeholderProfile(
        entity_name="Komite Direktur Independen NVIDIA",
        category="Corporate_Governance",
        verified_actions=[
            "Membentuk komite investigasi independen yang didampingi penasihat hukum eksternal",
            "Menegaskan Jensen Huang tetap menjabat sebagai CEO selama proses evaluasi",
            "Melakukan audit kepatuhan tata kelola menjelang rilis kinerja keuangan kuartalan"
        ],
        reported_motives=[
            "Melindungi nilai pemegang saham dari volatilitas pasar",
            "Menanggapi permintaan klarifikasi resmi dari komite legislatif"
        ],
        unsupported_conjectures=[
            "Rencana pencopotan paksa CEO",
            "Pengambilalihan kendali operasional oleh entitas luar"
        ],
        evidence_sources=[
            "Pernyataan Resmi Dewan Direksi NVIDIA Newsroom",
            "Pengungkapan Keterbukaan Informasi Korporasi"
        ]
    ),
    StakeholderProfile(
        entity_name="Entitas Pengawasan Intelijen & Pembocor Anonim",
        category="Intelligence_Whistleblower",
        verified_actions=[
            "Pengawasan terhadap kontak pihak ketiga (Alice Huang) yang telah berjalan sejak era pemerintahan sebelumnya",
            "Penyusunan nota peringatan keamanan terklasifikasi oleh pimpinan diplomasi",
            "Pemberian informasi latar belakang kepada media investigasi arus utama"
        ],
        reported_motives=[
            "Mendorong penegakan regulasi pembatasan ekspor semikonduktor tingkat tinggi",
            "Mengurangi ruang kompromi kebijakan perdagangan teknologi terhadap pesaing strategis"
        ],
        unsupported_conjectures=[
            "Konspirasi politik eksekutif untuk menyita aset perusahaan",
            "Operasi terkoordinasi untuk melumpuhkan fisik eksekutif"
        ],
        evidence_sources=[
            "Liputan Jurnalisme Investigasi New York Times / DNYUZ",
            "Dokumen Analisis Kebijakan Keamanan Nasional"
        ]
    ),
    StakeholderProfile(
        entity_name="Komite Khusus Kongres AS",
        category="Legislative",
        verified_actions=[
            "Meminta pengarahan tertutup (closed-door briefing) dari pimpinan korporasi",
            "Mengevaluasi efektivitas penegakan sanksi perdagangan dan kontrol ekspor AI"
        ],
        reported_motives=[
            "Menilai tingkat risiko keamanan nasional terhadap transfer teknologi kecerdasan buatan"
        ],
        unsupported_conjectures=[
            "Upaya nasionalisasi aset teknologi swasta"
        ],
        evidence_sources=[
            "Pernyataan Resmi Pimpinan Komite Legislatif DPR AS",
            "Laporan Media Kebijakan Publik"
        ]
    ),
    StakeholderProfile(
        entity_name="Entitas Perantara Perdagangan (Megaspeed / Pihak Ketiga)",
        category="Foreign_Entity",
        verified_actions=[
            "Menjalin interaksi bisnis dan komunikasi terkait rantai pasok perangkat keras",
            "Menjadi subjek pemeriksaan aparat pengawas kepatuhan ekspor lintas batas"
        ],
        reported_motives=[
            "Memperoleh wawasan arah lobi regulasi dan akses pasokan komputasi canggih"
        ],
        unsupported_conjectures=[
            "Perencanaan sabotase fisik terhadap eksekutif korporasi"
        ],
        evidence_sources=[
            "Catatan Registrasi Perusahaan Perantara Internasional",
            "Laporan Penegakan Regulasi Perdagangan"
        ]
    )
]

def export_actor_matrix():
    data = [asdict(a) for a in ACTOR_DATABASE]
    output_path = "analisis/matriks_pemetaan_aktor.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[+] Berhasil mengekspor matriks aktor ke: {output_path}")

    print("\n" + "=" * 80)
    print("MATRIKS DEKONSTRUKSI MOTIF PARA PIHAK (FORENSIK INFORMASI)")
    print("=" * 80)
    for a in ACTOR_DATABASE:
        print(f"\n[Aktor]: {a.entity_name} ({a.category})")
        print("  - Tindakan Terverifikasi :", "; ".join(a.verified_actions))
        print("  - Motif yang Dilaporkan  :", "; ".join(a.reported_motives))
        print("  - Dugaan Tanpa Bukti     :", "; ".join(a.unsupported_conjectures))

if __name__ == "__main__":
    export_actor_matrix()

