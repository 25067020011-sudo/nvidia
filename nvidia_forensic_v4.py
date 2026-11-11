#!/usr/bin/env python3
"""
NVIDIA FORENSIC INTELLIGENCE v4.0 — Repository Audit Orchestrator

Usage:
  python3 nvidia_forensic_v4.py --repo .
  python3 nvidia_forensic_v4.py --repo . --create-branch

Safety:
- Read-only audit of repository files; writes reports under audit_v4/.
- Does not delete or overwrite source files.
- Branch creation is opt-in.
- Never commits or pushes.
- SHA-256 manifest hashes files as found; this does not establish authenticity.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "4.0"
REPORT_DIR_NAME = "audit_v4"
SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".mypy_cache", ".pytest_cache", "dist", "build",
}
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".ini", ".cfg",
    ".tex", ".bib", ".sh", ".dockerfile", ".html", ".css", ".js",
}
DATA_EXTENSIONS = {".csv", ".json", ".jsonl"}
SECRET_PATTERNS = [
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Potential API token", re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,})\b")),
    ("Hardcoded credential assignment", re.compile(
        r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\b"
        r"\s*[:=]\s*['\"][^'\"]{6,}['\"]"
    )),
]
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger("nvidia_forensic_v4")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_command(args: list[str], cwd: Path, timeout: int = 60) -> dict[str, Any]:
    """Run a command without shell interpolation and capture result."""
    try:
        proc = subprocess.run(
            args, cwd=str(cwd), text=True, capture_output=True,
            timeout=timeout, check=False,
        )
        return {
            "command": args,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-12000:],
            "stderr": proc.stderr[-12000:],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": args, "returncode": None,
            "stdout": str(exc.stdout or "")[-4000:],
            "stderr": str(exc.stderr or "")[-4000:],
            "timed_out": True,
        }
    except FileNotFoundError as exc:
        return {
            "command": args, "returncode": None, "stdout": "",
            "stderr": str(exc), "timed_out": False,
        }


def iter_files(repo: Path):
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = Path(root) / name
            if path.is_file():
                yield path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def collect_inventory(repo: Path, files: list[Path]) -> dict[str, Any]:
    ext_counts: dict[str, int] = {}
    total_bytes = 0
    entries = []
    for path in files:
        rel = path.relative_to(repo).as_posix()
        ext = path.suffix.lower() or "[no extension]"
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
        try:
            size = path.stat().st_size
        except OSError:
            size = -1
        total_bytes += max(size, 0)
        entries.append({"path": rel, "size_bytes": size, "extension": ext})
    return {
        "generated_at": utc_now(),
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "extension_counts": dict(sorted(ext_counts.items())),
        "files": entries,
    }


def audit_python(files: list[Path], repo: Path) -> dict[str, Any]:
    syntax_errors = []
    import_summary = []
    for path in files:
        if path.suffix != ".py":
            continue
        source = safe_read_text(path)
        rel = path.relative_to(repo).as_posix()
        try:
            tree = ast.parse(source, filename=rel)
        except SyntaxError as exc:
            syntax_errors.append({
                "file": rel, "line": exc.lineno, "column": exc.offset,
                "message": exc.msg,
            })
            continue
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        import_summary.append({"file": rel, "imports": sorted(set(imports))})
    return {
        "python_files_checked": len(import_summary) + len(syntax_errors),
        "syntax_errors": syntax_errors,
        "imports": import_summary,
    }


def audit_secrets(files: list[Path], repo: Path) -> dict[str, Any]:
    findings = []
    for path in files:
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name.lower() != "dockerfile":
            continue
        text = safe_read_text(path)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            # Skip common example placeholders to reduce false positives.
            if any(placeholder in line.lower() for placeholder in
                   ("your_api_key", "example_secret", "changeme", "placeholder")):
                continue
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append({
                        "file": path.relative_to(repo).as_posix(),
                        "line": line_number,
                        "finding": label,
                        "snippet_redacted": "[REDACTED: potential sensitive value]",
                    })
    return {
        "method": "pattern-based static scan; results require manual triage",
        "finding_count": len(findings),
        "findings": findings,
    }


def audit_data_files(files: list[Path], repo: Path) -> dict[str, Any]:
    results = []
    for path in files:
        suffix = path.suffix.lower()
        if suffix not in DATA_EXTENSIONS:
            continue
        rel = path.relative_to(repo).as_posix()
        item: dict[str, Any] = {"file": rel, "format": suffix, "status": "UNKNOWN"}
        try:
            if suffix == ".json":
                parsed = json.loads(path.read_text(encoding="utf-8"))
                item.update(status="VALID", top_level_type=type(parsed).__name__)
            elif suffix == ".jsonl":
                count = 0
                with path.open(encoding="utf-8") as handle:
                    for line_no, line in enumerate(handle, start=1):
                        if line.strip():
                            json.loads(line)
                            count += 1
                item.update(status="VALID", records=count)
            elif suffix == ".csv":
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.reader(handle)
                    rows = list(reader)
                headers = rows[0] if rows else []
                widths = [len(row) for row in rows[1:]]
                item.update(
                    status="VALID",
                    row_count=max(len(rows) - 1, 0),
                    column_count=len(headers),
                    headers=headers[:100],
                    inconsistent_row_widths=sum(1 for width in widths if width != len(headers)),
                    duplicate_rows=max(0, len(rows) - len(set(tuple(r) for r in rows))),
                )
        except Exception as exc:
            item.update(status="INVALID", error=f"{type(exc).__name__}: {exc}")
        results.append(item)
    return {"checked_files": len(results), "results": results}


def create_hash_manifest(files: list[Path], repo: Path, output_path: Path) -> dict[str, Any]:
    entries = []
    for path in files:
        try:
            entries.append({
                "path": path.relative_to(repo).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            })
        except OSError as exc:
            entries.append({
                "path": path.relative_to(repo).as_posix(),
                "error": str(exc),
            })
    manifest = {
        "generated_at": utc_now(),
        "algorithm": "SHA-256",
        "note": "Hashes identify file bytes at audit time; they do not prove source authenticity or chain of custody.",
        "entries": entries,
    }
    write_report(output_path, json.dumps(manifest, indent=2, ensure_ascii=False))
    return manifest


def git_audit(repo: Path) -> dict[str, Any]:
    status = run_command(["git", "status", "--short", "--branch"], repo)
    branch = run_command(["git", "branch", "--show-current"], repo)
    log = run_command(["git", "log", "-5", "--oneline"], repo)
    is_repo = status["returncode"] == 0
    return {"is_git_repository": is_repo, "status": status, "branch": branch, "recent_commits": log}


def create_branch(repo: Path, branch_name: str) -> dict[str, Any]:
    status = run_command(["git", "status", "--porcelain"], repo)
    if status["returncode"] != 0:
        return {"created": False, "reason": "git status failed", "details": status}
    if status["stdout"].strip():
        return {
            "created": False,
            "reason": "Working tree is not clean; refusing to create branch automatically.",
            "status": status["stdout"],
        }
    existing = run_command(["git", "branch", "--list", branch_name], repo)
    if existing["stdout"].strip():
        return {"created": False, "reason": f"Branch already exists: {branch_name}"}
    result = run_command(["git", "switch", "-c", branch_name], repo)
    return {"created": result["returncode"] == 0, "details": result}


def markdown_report(title: str, sections: list[tuple[str, str]]) -> str:
    out = [f"# {title}", "", f"Generated: {utc_now()}", ""]
    for heading, body in sections:
        out.extend([f"## {heading}", "", body.strip() or "_No findings/data._", ""])
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="NVIDIA Forensic Intelligence v4.0 repository audit")
    parser.add_argument("--repo", required=True, help="Path to a local clone of the repository")
    parser.add_argument("--create-branch", action="store_true", help="Create feature branch if working tree is clean")
    parser.add_argument("--branch-name", default="feature/nvidia-forensic-intelligence-v4")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        LOGGER.error("Repository path is not a directory: %s", repo)
        return 2

    report_dir = repo / REPORT_DIR_NAME
    report_dir.mkdir(parents=True, exist_ok=True)

    LOGGER.info("Enumerating repository files...")
    files = list(iter_files(repo))
    # Avoid auditing outputs created by this script on repeated runs.
    files = [p for p in files if REPORT_DIR_NAME not in p.relative_to(repo).parts]

    inventory = collect_inventory(repo, files)
    py_audit = audit_python(files, repo)
    secret_audit = audit_secrets(files, repo)
    data_audit = audit_data_files(files, repo)
    git_report = git_audit(repo)

    inventory_path = report_dir / "repository_inventory.json"
    write_report(inventory_path, json.dumps(inventory, indent=2, ensure_ascii=False))
    write_report(report_dir / "python_syntax_import_audit.json",
                 json.dumps(py_audit, indent=2, ensure_ascii=False))
    write_report(report_dir / "security_pattern_scan.json",
                 json.dumps(secret_audit, indent=2, ensure_ascii=False))
    write_report(report_dir / "data_quality_audit.json",
                 json.dumps(data_audit, indent=2, ensure_ascii=False))
    write_report(report_dir / "git_audit.json",
                 json.dumps(git_report, indent=2, ensure_ascii=False))

    hash_manifest = create_hash_manifest(files, repo, report_dir / "evidence_sha256_manifest.json")

    syntax_body = (
        f"Python files checked: {py_audit['python_files_checked']}\n\n"
        f"Syntax errors: {len(py_audit['syntax_errors'])}\n\n"
        + "\n".join(
            f"- {e['file']}:{e['line']} — {e['message']}"
            for e in py_audit["syntax_errors"]
        )
    )
    inventory_body = (
        f"Files: {inventory['file_count']}\n"
        f"Total bytes: {inventory['total_bytes']}\n\n"
        "Extension counts:\n"
        + "\n".join(f"- {ext}: {count}" for ext, count in inventory["extension_counts"].items())
    )
    security_body = (
        f"Potential pattern findings: {secret_audit['finding_count']}\n\n"
        "This is a heuristic scan; false positives and false negatives are possible.\n"
        + "\n".join(
            f"- {item['file']}:{item['line']} — {item['finding']}"
            for item in secret_audit["findings"]
        )
    )
    data_body = "\n".join(
        f"- {r['file']}: {r['status']}"
        + (f" (rows={r.get('row_count')}, columns={r.get('column_count')}, "
           f"inconsistent widths={r.get('inconsistent_row_widths')}, duplicates={r.get('duplicate_rows')})"
           if r.get("format") == ".csv" and r.get("status") == "VALID" else "")
        + (f" — {r.get('error')}" if r.get("status") == "INVALID" else "")
        for r in data_audit["results"]
    )
    write_report(report_dir / "AUDIT_V4.md", markdown_report(
        "NVIDIA Repository Audit v4.0",
        [("Inventory", inventory_body), ("Python Syntax", syntax_body),
         ("Data Files", data_body), ("Audit Limitations",
          "This script performs static, local checks. It does not establish factual truth of news claims, "
          "run all project tests, validate deepfake models, assess event-study correctness, or certify "
          "compliance with ISO/NIST standards.")],
    ))
    write_report(report_dir / "SECURITY_AUDIT_V4.md", markdown_report(
        "Security Audit v4.0",
        [("Pattern Scan", security_body),
         ("Limitations", "No penetration testing or external exploitation was performed. "
          "Review findings manually and use a trusted dependency scanner in a controlled environment.")],
    ))
    write_report(report_dir / "DATA_QUALITY_REPORT_V4.md", markdown_report(
        "Data Quality Report v4.0",
        [("CSV/JSON Validation", data_body),
         ("SHA-256 Manifest", f"Hashed entries: {len(hash_manifest['entries'])}. "
          "The manifest is generated locally and is not a trusted timestamp or external attestation.")],
    ))
    write_report(report_dir / "TEST_REPORT_V4.md", markdown_report(
        "Test Report v4.0",
        [("Executed", f"- Python AST syntax check: {len(py_audit['syntax_errors'])} syntax error(s) detected.\n"
          f"- CSV/JSON parsing: {data_audit['checked_files']} file(s) inspected.\n"
          "- Security pattern scan completed."),
         ("Not Executed", "- Project unit/integration tests\n- Streamlit startup\n- Docker build\n"
          "- Full pipeline run\n- Dependency vulnerability scan\n- Deepfake model validation")],
    ))
    write_report(report_dir / "REPRODUCIBILITY_V4.md", markdown_report(
        "Reproducibility Protocol v4.0",
        [("Protocol", "Record commit SHA, Python version, OS, dependency lockfile, dataset provenance, "
          "collection timestamps, parameters, random seeds, model versions, and artifact hashes. "
          "Use immutable raw data snapshots and documented transformations."),
         ("Limitations", "The current script records local inventory and hashes only; additional experiment-specific "
          "metadata and test automation must be implemented for complete reproducibility.")],
    ))
    write_report(report_dir / "CHANGELOG_V4.md", markdown_report(
        "Changelog v4.0",
        [("Audit Orchestrator", "Added local inventory, AST syntax checks, heuristic secret scan, "
          "CSV/JSON validation, SHA-256 manifest, and audit documentation generation.")],
    ))
    write_report(report_dir / "README_V4.md", markdown_report(
        "NVIDIA Forensic Intelligence v4.0 — Audit Outputs",
        [("Run", "```bash\npython3 nvidia_forensic_v4.py --repo /path/to/nvidia\n```"),
         ("Outputs", "Reports are written to `audit_v4/`. Source files are not modified by this script.")],
    ))

    branch_result = None
    if args.create_branch:
        branch_result = create_branch(repo, args.branch_name)
        write_report(report_dir / "branch_creation_result.json",
                     json.dumps(branch_result, indent=2, ensure_ascii=False))

    LOGGER.info("Audit complete. Reports: %s", report_dir)
    LOGGER.info("Files inventoried: %d", inventory["file_count"])
    LOGGER.info("Python syntax errors: %d", len(py_audit["syntax_errors"]))
    LOGGER.info("Potential secret patterns: %d", secret_audit["finding_count"])
    LOGGER.info("Data files checked: %d", data_audit["checked_files"])
    if branch_result:
        LOGGER.info("Branch creation result: %s", branch_result)
    LOGGER.info("No commit or push was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
