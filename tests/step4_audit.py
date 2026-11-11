import json
import hashlib
import os
import sys

LEDGER_PATH = "evidence_ledger.json"
with open(LEDGER_PATH, "r", encoding="utf-8") as f:
    ledger = json.load(f)

print(f"Total entries in ledger: {len(ledger)}")

report = {
    "audit_timestamp_utc": "2026-11-11T08:28:40Z",
    "total_registered_items": len(ledger),
    "verified_authentic_count": 0,
    "tampered_or_mismatched_count": 0,
    "missing_files_count": 0,
    "duplicated_evidence_ids": [],
    "duplicated_hashes": [],
    "items": []
}

seen_ids = set()
seen_hashes = set()

for item in ledger:
    eid = item.get("evidence_id")
    fname = item.get("filename")
    fpath = item.get("filepath")
    expected_sha = item.get("hashes", {}).get("sha256")
    expected_md5 = item.get("hashes", {}).get("md5")

    # Check duplicates
    if eid in seen_ids:
        report["duplicated_evidence_ids"].append(eid)
    seen_ids.add(eid)

    if expected_sha in seen_hashes:
        report["duplicated_hashes"].append(expected_sha)
    seen_hashes.add(expected_sha)

    # Resolve file path
    actual_path = fpath
    if not os.path.exists(actual_path):
        for cand in [fname, os.path.join("analisis", fname), os.path.join("tools", fname), os.path.join(".github", "workflows", fname)]:
            if os.path.exists(cand):
                actual_path = cand
                break

    if not os.path.exists(actual_path):
        report["missing_files_count"] += 1
        report["items"].append({
            "evidence_id": eid,
            "filename": fname,
            "status": "FILE_MISSING",
            "resolved_path": None
        })
        continue

    # Hash calculation
    sha = hashlib.sha256()
    md5 = hashlib.md5()
    with open(actual_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            sha.update(chunk)
            md5.update(chunk)
    actual_sha = sha.hexdigest()
    actual_md5 = md5.hexdigest()
    actual_size = os.path.getsize(actual_path)

    sha_match = (actual_sha == expected_sha)
    md5_match = (actual_md5 == expected_md5)

    if sha_match:
        report["verified_authentic_count"] += 1
        status = "AUTHENTIC"
    else:
        report["tampered_or_mismatched_count"] += 1
        status = "HASH_MISMATCH"

    report["items"].append({
        "evidence_id": eid,
        "filename": fname,
        "resolved_path": actual_path,
        "filesize_bytes": actual_size,
        "expected_sha256": expected_sha,
        "actual_sha256": actual_sha,
        "sha256_match": sha_match,
        "md5_match": md5_match,
        "status": status
    })

with open("evidence_integrity_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"AUTHENTIC: {report['verified_authentic_count']}/{len(ledger)}")
print(f"MISMATCH : {report['tampered_or_mismatched_count']}")
print(f"MISSING  : {report['missing_files_count']}")
print("Wrote evidence_integrity_report.json successfully.")
