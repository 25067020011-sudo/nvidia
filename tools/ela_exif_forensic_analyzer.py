#!/usr/bin/env python3
"""
tools/ela_exif_forensic_analyzer.py
--------------------------------------------------------------------------------
Toolkit Forensik Digital: Error Level Analysis (ELA) & Audit Metadata EXIF/IPTC
Standar Kepatuhan: ISO/IEC 27037:2012 (Preservasi & Uji Keaslian Bukti Visual)

Fungsi Utama:
1. Error Level Analysis (ELA):
   - Menganalisis perbedaan tingkat kompresi JPEG antar-area gambar.
   - Mengidentifikasi elemen manipulasi komposit (image splicing), penempelan wajah,
     atau rekayasa digital pada artefak media sosial.
2. Audit Metadata EXIF & Provenance:
   - Mengekstrak stempel waktu pengambilan asli (DateTimeOriginal), kamera, dan koordinat.
   - Mendeteksi jejak software editor (Photoshop, GIMP, Canva) atau artefak generator AI.
"""

import os
import sys
import json
import io
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS

def perform_ela(image_path: str, output_path: str = None, quality: int = 90, scale: int = 15) -> dict:
    """
    Melakukan pengujian Error Level Analysis (ELA) pada berkas gambar.
    """
    if not os.path.exists(image_path):
        return {"status": "ERROR", "message": f"Berkas '{image_path}' tidak ditemukan."}

    # Buka gambar asli
    orig_img = Image.open(image_path).convert("RGB")
    width, height = orig_img.size

    # Simpan sementara dalam buffer JPEG pada tingkat kualitas tertentu
    buffer = io.BytesIO()
    orig_img.save(buffer, "JPEG", quality=quality)
    buffer.seek(0)
    recompressed_img = Image.open(buffer)

    # Hitung selisih absolut antar-piksel
    diff_img = ImageChops.difference(orig_img, recompressed_img)

    # Skalakan selisih agar terlihat jelas oleh mata manusia
    extrema = diff_img.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    multiplier = scale if scale else int(255.0 / max_diff)
    
    enhancer = ImageEnhance.Brightness(diff_img)
    ela_img = enhancer.enhance(multiplier)

    # Hitung metrik statistik anomali
    diff_arr = np.array(diff_img, dtype=float)
    mean_error = float(np.mean(diff_arr))
    std_error = float(np.std(diff_arr))
    max_error = float(np.max(diff_arr))

    # Tentukan output path jika tidak diberikan
    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_ela.jpg"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    ela_img.save(output_path, "JPEG")

    # Interpretasi Forensik ELA
    if std_error > 8.5:
        verdict = "ANOMALI TINGGI: Terindikasi penyuntingan komposit / percampuran multi-kompresi (splicing)"
    elif std_error > 5.0:
        verdict = "ANOMALI MODERAT: Variasi tekstur normal atau kompresi ulang parsial"
    else:
        verdict = "SERAGAM / OTENTIK: Tingkat error merata, tidak terdeteksi manipulasi penempelan digital"

    return {
        "status": "SUCCESS",
        "image_path": image_path,
        "output_ela_path": output_path,
        "dimensions": f"{width}x{height}",
        "quality_recompression": quality,
        "scale_multiplier": multiplier,
        "mean_error": round(mean_error, 3),
        "std_error": round(std_error, 3),
        "max_error": round(max_error, 3),
        "forensic_verdict": verdict
    }

def extract_exif(image_path: str) -> dict:
    """
    Mengekstrak dan mengaudit metadata EXIF, IPTC, dan penanda software editor.
    """
    if not os.path.exists(image_path):
        return {"status": "ERROR", "message": f"Berkas '{image_path}' tidak ditemukan."}

    img = Image.open(image_path)
    info = img._getexif()

    exif_data = {}
    software_flag = None
    ai_generation_flag = False

    if info:
        for tag_id, value in info.items():
            tag_name = TAGS.get(tag_id, tag_id)
            # Konversi bytes ke string jika perlu
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8", errors="ignore").strip()
                except Exception:
                    value = str(value)
            exif_data[tag_name] = value

        # Cek Software Editor
        software = exif_data.get("Software", "")
        if software:
            known_editors = ["photoshop", "gimp", "canva", "lightroom", "midjourney", "stable diffusion", "dall-e"]
            for ed in known_editors:
                if ed in software.lower():
                    software_flag = f"Penyunting Terdeteksi: {software}"
                    if ed in ["midjourney", "stable diffusion", "dall-e"]:
                        ai_generation_flag = True
    else:
        exif_data["Notice"] = "Tidak ditemukan metadata EXIF header (kemungkinan terkompresi platform media sosial)."

    # Cek metadata bawaan format PNG/JPEG jika ada text chunk
    if hasattr(img, "text") and img.text:
        exif_data["PNG_Text_Chunks"] = dict(img.text)
        for k, v in img.text.items():
            if any(term in str(v).lower() for term in ["prompt", "negative prompt", "steps", "sampler", "midjourney", "c2pa"]):
                ai_generation_flag = True

    return {
        "status": "SUCCESS",
        "image_path": image_path,
        "format": img.format,
        "mode": img.mode,
        "size": f"{img.width}x{img.height}",
        "has_exif": info is not None,
        "software_signature": software_flag or "Tidak ada jejak software editor komersial",
        "ai_synthesis_flag": ai_generation_flag,
        "metadata_tags": exif_data
    }

def main():
    if len(sys.argv) < 2:
        print("=" * 75)
        print("TOOLKIT FORENSIK DIGITAL: ERROR LEVEL ANALYSIS (ELA) & EXIF AUDIT")
        print("=" * 75)
        print("Penggunaan:")
        print("  1. Uji ELA (Deteksi Splicing/Manipulasi Gambar):")
        print("     python tools/ela_exif_forensic_analyzer.py ela <path_gambar> [output_path]")
        print("  2. Ekstraksi Metadata EXIF & Deteksi Software/AI:")
        print("     python tools/ela_exif_forensic_analyzer.py exif <path_gambar>")
        print("  3. Audit Forensik Lengkap (ELA + EXIF):")
        print("     python tools/ela_exif_forensic_analyzer.py audit <path_gambar>")
        print("  4. Uji Mandiri / Demo Testing:")
        print("     python tools/ela_exif_forensic_analyzer.py test")
        print("=" * 75)
        sys.exit(0)

    mode = sys.argv[1].lower()

    if mode == "test":
        print("\n[*] Menjalankan Demo Pengujian ELA pada Artefak Gambar Proyek...")
        test_img = "analisis/04_klaim.png"
        if os.path.exists(test_img):
            ela_res = perform_ela(test_img, "analisis/04_klaim_ela_test.jpg")
            exif_res = extract_exif(test_img)
            print("\n[+] HASIL UJI ELA (ERROR LEVEL ANALYSIS):")
            print(json.dumps(ela_res, indent=2, ensure_ascii=False))
            print("\n[+] HASIL AUDIT METADATA EXIF:")
            print(json.dumps(exif_res, indent=2, ensure_ascii=False))
        else:
            print(f"[!] Berkas uji '{test_img}' tidak ditemukan.")

    elif mode == "ela" and len(sys.argv) >= 3:
        target = sys.argv[2]
        out_path = sys.argv[3] if len(sys.argv) >= 4 else None
        res = perform_ela(target, out_path)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif mode == "exif" and len(sys.argv) >= 3:
        target = sys.argv[2]
        res = extract_exif(target)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif mode == "audit" and len(sys.argv) >= 3:
        target = sys.argv[2]
        ela_res = perform_ela(target)
        exif_res = extract_exif(target)
        combined = {
            "forensic_ela": ela_res,
            "forensic_exif": exif_res
        }
        print(json.dumps(combined, indent=2, ensure_ascii=False))
    else:
        print("[!] Parameter tidak valid. Jalankan tanpa argumen untuk bantuan.")

if __name__ == "__main__":
    main()

