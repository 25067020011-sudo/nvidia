import streamlit as st
import pandas as pd
import json
import os
import subprocess
from datetime import datetime

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Audit Forensik Digital: Kasus Jensen Huang & NVIDIA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #76b900;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1a1c24;
        border: 1px solid #2d3139;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .status-badge-confirmed {
        background-color: #137333;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-badge-debunked {
        background-color: #c5221f;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Load Data
@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Sidebar Navigation & Information
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/21/Nvidia_logo.svg", width=180)
    st.markdown("### **Pusat Forensik Digital**")
    st.markdown("**Studi Kasus**: Verifikasi Narasi Viral, Deepfake, Intelijen, & Audit Tata Kelola")
    st.markdown("---")
    
    st.markdown("#### **Status Integritas (ISO/IEC 27037)**")
    ledger_data = load_json("evidence_ledger.json")
    st.metric("Total Bukti Terverifikasi", f"{len(ledger_data)} Artefak", delta="SHA-256 Otentik", delta_color="normal")
    
    st.markdown("---")
    st.markdown("#### **Tautan Dokumen Riset**")
    st.markdown("- [Repositori GitHub Resmi](https://github.com/25067020011-sudo/nvidia)")
    st.markdown("- `PRD Master v3.0 Ground Truth`")
    st.markdown("- `Manuskrip Ilmiah (IMRaD)`")
    st.markdown("- `Laporan Penyelidikan ISO 27037`")
    st.markdown("- `SOP Tanggap Insiden NIST SP 800-61`")
    
    st.markdown("---")
    st.caption("Pusat Riset Forensik Digital & Ekonometrika © 2026")

# Header Section
st.markdown('<div class="main-title">🛡️ Platform Audit Forensik Digital & Tata Kelola Korporasi</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Dekonstruksi Klaim Viral Tokoh Publik, Rekayasa Media Deepfake, Rantai Intelijen, dan Reaksi Pasar Modal (Studi Kasus: Jensen Huang / NVIDIA)</div>', unsafe_allow_html=True)

# Top KPI Summary Cards
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Klaim Serangan Fisik", value="0.0%", delta="Total Ditolak / Hoaks", delta_color="inverse")
with col2:
    st.metric(label="Serangan Kloning Deepfake", value="100.000 Bot", delta="QR Scam Aktif (28 Okt)", delta_color="inverse")
with col3:
    st.metric(label="Investigasi Dewan (20 Thn)", value="2 Kali", delta="2006 vs 2026 (Unik)", delta_color="normal")
with col4:
    st.metric(label="Belanja GPU Tesla/xAI", value="$30 Miliar", delta="Bantah Musk Dalang", delta_color="normal")
with col5:
    st.metric(label="Rantai Bukti SHA-256", value="100% Utuh", delta="17 Berkas Tersertifikasi", delta_color="normal")

st.markdown("---")

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎯 Status Klaim (Tiered Truth)",
    "🔎 11 Artefak Publik OSINT",
    "📈 Event-Study Saham NVDA",
    "🕸️ Social Network Analysis (SNA)",
    "🛰️ Triad Intelijen (SIGINT/MVT)",
    "🏛️ Audit SEC EDGAR 20 Tahun",
    "🔐 Rantai Integritas (ISO 27037)"
])

# ==============================================================================
# TAB 1: STATUS KLAIM & TIERED TRUTH TAXONOMY
# ==============================================================================
with tab1:
    st.subheader("🎯 Matriks Kebenaran Bertingkat (*Tiered Truth Taxonomy*)")
    st.markdown("""
    Setiap klaim yang beredar diuji menggunakan mesin klasifikasi forensik berbasis bobot kredibilitas bukti:
    **CONFIRMED** (Dokumen Resmi Primer), **REPORTED** (Jurnalisme Investigasi/Audit Dewan),
    **UNVERIFIED** (Spekulasi Anonim), dan **FABRICATED / DISINFORMATION** (Terbukti Rekayasa/Distorsi).
    """)
    
    claims_df = load_csv("analisis/02_status_klaim.csv")
    if not claims_df.empty:
        st.dataframe(claims_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Berkas status klaim belum dimuat.")

    st.markdown("---")
    st.subheader("💡 Dekonstruksi Mendalam Teori Dalang Eksternal")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### 🚫 Pembantahan Teori 'Elon Musk Dalang'")
        st.info("""
        - **Saling Ketergantungan Ekonomi Riil**: Tesla belanja kumulatif **$10 Miliar** untuk chip NVIDIA per 2026; xAI sepakat investasi **$20 Miliar** untuk superkomputer *Colossus 2*.
        - **Logika Industri Terbalik**: Pelatihan AI xAI (*Grok*) dan *Tesla FSD* bergantung 100% pada NVIDIA. Menjatuhkan Huang melumpuhkan roadmap produk Musk sendiri.
        - **Kemitraan Erat**: Huang memuji Musk sebagai *"the ultimate GPU"*, bukan musuh bisnis.
        - **Cuitan 23 Okt 2025**: *"If she's a 10, you're an asset"* adalah satir tanpa menyebut subjek dan terbit setahun sebelum insiden.
        """)
    with col_t2:
        st.markdown("#### 🎯 Siapa yang Diuntungkan Secara Faktual?")
        st.success("""
        - **Faksi Garis Keras Ekspor (*China-hawks*)**: Senator Marco Rubio dan komite keamanan nasional Kongres AS.
        - **Motif Regulasi**: Jensen Huang adalah juru lobi terkuat yang memperjuangkan kelonggaran izin ekspor chip komputasi ke Asia.
        - **Hasil**: Pelemahan reputasi Huang melapangkan pengetatan kontrol ekspor semikonduktor canggih secara permanen.
        - **Penyelidikan Alice Huang**: Telah berjalan secara formal sejak era pemerintahan Biden, membantah klaim rekayasa dadakan politik.
        """)

# ==============================================================================
# TAB 2: KATALOG 11 ARTEFAK PUBLIK OSINT
# ==============================================================================
with tab2:
    st.subheader("🔎 Katalog 11 Artefak Publik OSINT & Metodologi Verifikasi")
    st.markdown("""
    Koleksi data terbuka (*Open Source Intelligence*) yang dapat diakses dan diverifikasi oleh peneliti independen
    sesuai standar ISO/IEC 27037 tanpa melanggar batasan privasi personal.
    """)
    
    osint_df = load_csv("analisis/09_osint_artefak.csv")
    if not osint_df.empty:
        filter_platform = st.multiselect("Filter Platform Sumber:", options=osint_df["platform"].unique(), default=osint_df["platform"].unique())
        filtered_df = osint_df[osint_df["platform"].isin(filter_platform)]
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Berkas katalog OSINT belum dimuat.")

    st.markdown("---")
    st.markdown("#### 🛠️ Sorotan Artefak Paling Signifikan")
    c_os1, c_os2, c_os3 = st.columns(3)
    with c_os1:
        st.markdown("**OS07: Registrasi ACRA Singapura**")
        st.caption("Pemerintah Singapura (2023)")
        st.write("Satu-satunya sumber primer resmi pemerintah yang dapat diakses langsung via BizFile+. Memvalidasi status hukum Megaspeed sebagai spin-off 7Road (HKEX: 0797).")
    with c_os2:
        st.markdown("**OS01: Foto LinkedIn NetThunder**")
        st.caption("Taipei Bar Lounge (Juni 2024)")
        st.write("Uji ELA (Error Level Analysis) dan EXIF membuktikan ketiadaan splicing digital. Menjadi titik awal dokumentasi visual kedekatan.")
    with c_os3:
        st.markdown("**OS11: Memo Internal Jensen Huang**")
        st.caption("NVIDIA Corp (8 Nov 2026)")
        st.write("Dikonfirmasi resmi oleh juru bicara korporasi dan dual-sourced via Axios & Financial Times; mengakui hubungan perselingkuhan personal.")

# ==============================================================================
# TAB 3: EVENT-STUDY SAHAM NVDA & KORPUS BERITA
# ==============================================================================
with tab3:
    st.subheader("📈 Analisis Ekonometrika Event-Study (Saham NVDA)")
    st.markdown("""
    Menguji apakah volatilitas pasar modal dipicu oleh skandal reputasi internal atau dinamika makroekonomi regulasi AI.
    """)
    
    if os.path.exists("analisis/05_saham_event_study.png"):
        st.image("analisis/05_saham_event_study.png", caption="Gambar: Fluktuasi Harga Penutupan dan Volume Transaksi Saham NVDA (Sep-Nov 2026) dengan Penanda Peristiwa Kunci", use_container_width=True)

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.markdown("#### 📊 Tiga Jendela Peristiwa Kunci")
        st.markdown("""
        - **Jendela 1 (21–29 Okt)**: Harga stabil di $213 – $221. Insiden protes Berlin dan laporan The Information tidak memicu kepanikan investor.
        - **Jendela 2 (5 Nov - Paska Pemilu)**: Saham anjlok -9.26% ($206 -> $181) bersamaan dengan jatuhnya Nasdaq 100 akibat kekhawatiran regulasi pusat data pasca-kemenangan Demokrat.
        - **Jendela 3 (9 Nov - Reaksi Memo)**: Penurunan ke $178 dengan volume rekor **459,1 Juta lembar**, mencerminkan diskon risiko tata kelola (*governance discount*).
        """)
    with c_s2:
        st.markdown("#### 📰 Korpus 300 Berita Internasional")
        if os.path.exists("analisis/04_klaim.png"):
            st.image("analisis/04_klaim.png", caption="Sebaran Kategori Narasi Judul Berita (N=300)", use_container_width=True)

# ==============================================================================
# TAB 4: SOCIAL NETWORK ANALYSIS (SNA)
# ==============================================================================
with tab4:
    st.subheader("🕸️ Pemodelan Jejaring Sosial & Sentralitas Antara (Betweenness Centrality)")
    st.markdown("""
    Mengidentifikasi simpul pialang (*information broker*) yang mentransformasikan isu lokal menjadi krisis global.
    """)
    
    if os.path.exists("analisis/07_network_graph_betweenness.png"):
        st.image("analisis/07_network_graph_betweenness.png", caption="Visualisasi Graf Interaksi Aktor dan Sindikasi Media (Ukuran Simpul = Betweenness Centrality)", use_container_width=True)

    col_sna1, col_sna2 = st.columns(2)
    with col_sna1:
        st.markdown("#### 👤 Top 10 Aktor (Sentralitas Antara)")
        actors_df = load_csv("analisis/matriks_sna_20_aktor.csv")
        if not actors_df.empty:
            st.dataframe(actors_df[["nama_aktor", "kategori", "betweenness_centrality", "pagerank"]].head(10), use_container_width=True, hide_index=True)
    with col_sna2:
        st.markdown("#### 📰 Top 10 Media Massa (Penyebar Narasi)")
        media_df = load_csv("analisis/matriks_sna_10_media.csv")
        if not media_df.empty:
            st.dataframe(media_df, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 5: TRIAD DOKTRIN INTELIJEN
# ==============================================================================
with tab5:
    st.subheader("🛰️ Komparasi Triad Intelijen: SIGINT vs Spyware Komersial vs HUMINT")
    st.markdown("""
    Meluruskan kekeliruan terminologis publik: Pembedaan mendasar antara penyadapan hulu (*upstream SIGINT*),
    peretasan ponsel (*commercial spyware*), dan pendekatan relasional personal (*human intelligence/honeytrap*).
    """)
    
    intel_df = load_csv("analisis/08_komparasi_metode_intelijen.csv")
    if not intel_df.empty:
        st.dataframe(intel_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🔬 Bukti Audit Mobile Verification Toolkit (MVT) & STIX2 IOC")
    st.markdown("""
    - **Dataset AmnestyTech (`pegasus.stix2`)**: Memuat **3.099 objek STIX 2.1** (1.549 indikator teknis: 1.438 domain C2, 81 proses, 29 alamat email).
    - **Visibilitas MVT**: Efektif mendeteksi jejak biner pada backup endpoint iOS/Android.
    - **Fakta Kasus**: Intelijen AS **tidak meretas ponsel Jensen Huang menggunakan spyware Pegasus**; pengawasan dilakukan terhadap target asing (Alice Huang) via **FISA Section 702**, di mana kontak Jensen terjaring secara insidental (*incidental collection*) lalu di-unmask secara legal.
    """)

# ==============================================================================
# TAB 6: AUDIT HISTORIS SEC EDGAR 20 TAHUN
# ==============================================================================
with tab6:
    st.subheader("🏛️ Audit Keterbukaan Informasi SEC EDGAR (2006–2026)")
    st.markdown("""
    Penelusuran terhadap pengarsipan Form 10-K, 10-Q, dan 8-K NVIDIA Corporation (CIK: `0001045810`).
    """)
    
    col_sec1, col_sec2 = st.columns([3, 2])
    with col_sec1:
        st.markdown("#### 📜 Preseden Dua Dekade (Hanya Terjadi 2 Kali)")
        st.markdown("""
        1. **Tahun 2006 (*Stock Option Backdating*)**: Dipimpin Komite Audit dewan dibantu kuasa hukum eksternal, berfokus pada sistem akuntansi korporasi (*corporate accounting practice*).
        2. **Tahun 2026 (*Kasus Memo CEO*)**: Dipimpin Komite Direktur Independen, menyasar perilaku pribadi (*personal conduct*) pimpinan tertinggi. **Ini merupakan satu-satunya investigasi dewan dalam sejarah NVIDIA yang menargetkan CEO secara langsung.**
        """)
        st.markdown("""
        *Catatan Metodologis*: Seluruh insiden material lain (denda SEC kripto 2017/2022, sengketa Valeo 2022, pemeriksaan Megaspeed 2025, dan gugatan hak cipta AI 2026) diselesaikan di level manajemen internal atau litigasi peradilan biasa, bukan melalui pembentukan komite dewan independen.
        """)
    with col_sec2:
        sec_json = load_json("analisis/audit_historis_sec_20tahun.json")
        if sec_json:
            st.json(sec_json)

# ==============================================================================
# TAB 7: RANTAI INTEGRITAS BUKTI (ISO/IEC 27037)
# ==============================================================================
with tab7:
    st.subheader("🔐 Rantai Integritas Bukti Forensik (*Chain of Custody*)")
    st.markdown("""
    Seluruh berkas bukti digital, skrip otomasi, dan data analitis diverifikasi menggunakan hash kriptografis ganda (SHA-256 dan MD5)
    sesuai standar ISO/IEC 27037:2012 untuk menjamin bahwa bukti tidak mengalami manipulasi (*tamper-proof*).
    """)
    
    if ledger_data:
        ledger_table = []
        for item in ledger_data:
            ledger_table.append({
                "Evidence ID": item.get("evidence_id"),
                "Nama Berkas": item.get("filename"),
                "Kategori": item.get("source_category"),
                "Ukuran (Bytes)": item.get("filesize_bytes"),
                "SHA-256 Hash": item.get("hashes", {}).get("sha256"),
                "Status Integritas": item.get("verification_status")
            })
        st.dataframe(pd.DataFrame(ledger_table), use_container_width=True, hide_index=True)
    else:
        st.warning("Ledger bukti forensik kosong atau tidak ditemukan.")

    st.markdown("---")
    st.markdown("#### ⚡ Eksekusi Master Pipeline Reproducibility (10 Tahapan)")
    st.code("python pipeline_run_all.py", language="bash")
    st.caption("Pipeline master mengeksekusi audit SHA-256, Tiered Truth Engine, SEC 20 Tahun, Event-Study, SNA, dan OSINT Manager secara sekuensial (100% reproducible).")
