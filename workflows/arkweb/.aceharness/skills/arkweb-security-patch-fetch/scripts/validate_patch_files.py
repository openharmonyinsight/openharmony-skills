#!/usr/bin/env python3
"""Validate patch_files[] entries under 02_patch_fetch.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from archive_paths import validate_project_output_root


def validate_patch_bytes(data: bytes) -> tuple[bool, str, str]:
    text = data[:4096].decode("utf-8", "ignore")
    low = text.lower().lstrip()
    first = text.splitlines()[0] if text.splitlines() else ""
    if not data:
        return False, "empty patch artifact", first
    if low.startswith("<!doctype html") or low.startswith("<html") or "http error" in low[:300]:
        return False, "invalid artifact: html/http error page", first
    if low.startswith(")]}'") or low.startswith("{"):
        return False, "invalid artifact: metadata json", first
    if (
        "diff --git" in text
        or "Index:" in text
        or ("--- a/" in text and "+++ b/" in text)
        or (re.search(r"^From [0-9a-f]{7,40}", text, re.M) and "Subject:" in text)
    ):
        return True, "standard diff/patch signature found", first
    return False, "missing standard diff signature", first


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()
    output_root, _project_root = validate_project_output_root(args.output_root, args.project_root)

    results = []
    for meta_path in sorted(output_root.glob("*/02_patch_fetch.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        issues = meta.get("issues") if isinstance(meta, dict) else None
        issue_records = issues if isinstance(issues, list) and issues else [meta]
        for record in issue_records:
            if not isinstance(record, dict):
                continue
            for item in record.get("patch_files", []):
                path = Path(item.get("path", ""))
                if not path.is_absolute():
                    path = meta_path.parent / path
                if not path.is_file():
                    results.append({"issue_id": meta_path.parent.name, "path": str(path), "valid": False, "reason": "missing file"})
                    continue
                valid, reason, first = validate_patch_bytes(path.read_bytes())
                results.append({"issue_id": meta_path.parent.name, "path": str(path), "valid": valid, "reason": reason, "first_line": first})
    print(json.dumps({"patch_files": results}, ensure_ascii=False, indent=2))
    return 0 if all(item["valid"] for item in results) and results else 1


if __name__ == "__main__":
    raise SystemExit(main())
