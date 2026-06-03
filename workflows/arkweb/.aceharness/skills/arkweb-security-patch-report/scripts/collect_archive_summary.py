#!/usr/bin/env python3
"""Collect per-issue archive workflow outputs and print a summary JSON."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from archive_paths import validate_project_output_root


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def first_issue(meta: dict) -> dict:
    issues = meta.get("issues") if isinstance(meta, dict) else None
    if isinstance(issues, list) and issues and isinstance(issues[0], dict):
        return issues[0]
    return meta if isinstance(meta, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()
    output_root, _project_root = validate_project_output_root(args.output_root, args.project_root)

    issues = []
    for issue_dir in sorted(path for path in output_root.iterdir() if path.is_dir()):
        issue = first_issue(load_json(issue_dir / "01_issue_analysis.json"))
        patch = first_issue(load_json(issue_dir / "02_patch_fetch.json"))
        impact = first_issue(load_json(issue_dir / "03_impact_decision.json"))
        issue_id = str(issue.get("IssueID") or patch.get("IssueID") or impact.get("IssueID") or issue_dir.name)
        issues.append(
            {
                "issue_id": issue_id,
                "title": issue.get("Issue标题", ""),
                "fix_count": len(issue.get("upstream_fix_prs") or []),
                "valid_patch_count": sum(1 for item in patch.get("patch_files", []) if item.get("content_valid")),
                "arkweb_impact": impact.get("arkweb_impact") or impact.get("ArkWeb结论") or impact.get("impact", "unknown"),
                "merge_policy": impact.get("merge_policy", {"force_merge": False, "impact_mode": "normal", "reason": ""}),
                "risk": impact.get("risk_level") or impact.get("风险等级", "unknown"),
                "issue_dir": str(issue_dir),
            }
        )

    summary = {"generated_at": datetime.now().isoformat(), "output_root": str(output_root), "issue_count": len(issues), "issues": issues}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
