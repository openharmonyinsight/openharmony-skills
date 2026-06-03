#!/usr/bin/env python3
"""Generate per-issue 04_final_archive and summary files for archive workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from archive_paths import validate_project_output_root


REQUIRED = [
    "01_issue_analysis.md",
    "01_issue_analysis.json",
    "02_patch_fetch.md",
    "02_patch_fetch.json",
    "03_impact_decision.md",
    "03_impact_decision.json",
    "patches",
]


def first_issue(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        meta = json.loads(path.read_text(encoding="utf-8"))
        issues = meta.get("issues") if isinstance(meta, dict) else None
        return issues[0] if isinstance(issues, list) and issues else meta
    except Exception:
        return {}


def process_issue(issue_dir: Path, issue_archive_root: Path) -> dict:
    missing = []
    for name in REQUIRED:
        path = issue_dir / name
        if name == "patches":
            if not path.is_dir() or not any(path.iterdir()):
                missing.append(name)
        elif not path.is_file():
            missing.append(name)

    issue = first_issue(issue_dir / "01_issue_analysis.json")
    patch = first_issue(issue_dir / "02_patch_fetch.json")
    impact = first_issue(issue_dir / "03_impact_decision.json")
    issue_id = issue_dir.name
    selected = patch.get("selected_fix", {})
    patch_files = patch.get("patch_files", [])
    source_files = [str(path) for path in (issue_archive_root / issue_id).glob(f"{issue_id}.mh*")]
    result = "failed" if not issue or not patch or not impact else ("partial" if missing else "success")
    final_json = {
        "archive_result": result,
        "issue_archive_dir": str(issue_archive_root),
        "processed_issue_files": source_files,
        "patches_found": [
            {"url": selected.get("url", ""), "commit": selected.get("commit_hash", ""), "change_id": selected.get("change_id", ""), "local_patch": item.get("path", "")}
            for item in patch_files
        ],
        "impact": impact.get("arkweb_impact", "unknown"),
        "merge_policy": impact.get("merge_policy", {"force_merge": False, "impact_mode": "normal", "reason": ""}),
        "archive_dirs": [
            str(issue_dir / "01_issue_analysis.md"),
            str(issue_dir / "01_issue_analysis.json"),
            str(issue_dir / "02_patch_fetch.md"),
            str(issue_dir / "02_patch_fetch.json"),
            str(issue_dir / "03_impact_decision.md"),
            str(issue_dir / "03_impact_decision.json"),
            str(issue_dir / "patches"),
            str(issue_dir / "04_final_archive.md"),
            str(issue_dir / "04_final_archive.json"),
            str(issue_dir / "summary.md"),
            str(issue_dir / "summary.json"),
        ],
        "missing_artifacts": missing,
        "report_path": str(issue_dir / "04_final_archive.md"),
    }
    md = [
        "# ArkWeb本地Issue补丁分析归档报告",
        "",
        "## 1. 基础信息",
        f"- issue_id: {issue_id}",
        f"- issue_title: {issue.get('Issue标题', 'unknown')}",
        f"- issue_archive_dir: {issue_archive_root}",
        f"- processed_issue_files: {source_files}",
        "",
        "## 2. 漏洞/缺陷解析摘要",
        f"- 漏洞/缺陷摘要: {issue.get('Issue概述', 'unknown')}",
        f"- Milestone: {issue.get('Milestone', 'unknown')}",
        f"- 状态: {issue.get('Issue状态', 'unknown')}",
        "",
        "## 3. Patch获取结果",
        f"- selected_fix_url: {selected.get('url', '')}",
        f"- commit_hash: {selected.get('commit_hash', '')}",
        f"- change_id: {selected.get('change_id', '')}",
        f"- patch_files: {[item.get('path', '') for item in patch_files]}",
        f"- modified_files_count: {len(patch.get('modified_files', []))}",
        "",
        "## 4. 影响判定",
        f"- impact: {impact.get('arkweb_impact', 'unknown')}",
        f"- merge_policy: {impact.get('merge_policy', {'force_merge': False, 'impact_mode': 'normal', 'reason': ''})}",
        f"- risk_level: {impact.get('风险评估级别', 'unknown')}",
        f"- 安全专项摘要: {impact.get('security_impact', {})}",
        "",
        "## 5. 责任田与质量维度",
        f"- 归属团队: {impact.get('归属团队', 'unknown')}",
        f"- 影响特性: {impact.get('影响的特性', [])}",
        f"- 是否建议保留: {impact.get('是否建议保留', 'unknown')}",
        f"- 是否需要测试: {impact.get('是否需要测试', 'unknown')}",
        f"- 测试建议: {impact.get('测试建议', '')}",
        "",
        "## 6. 未解决问题与人工核查建议",
        f"- missing_artifacts: {missing}",
        "- 后续工作建议: 自动合入、编译验证、提交上库由本集成工作流后续状态继续执行。",
        "",
        "## 7. JSON摘要",
        "```json",
        json.dumps(final_json, ensure_ascii=False, indent=2),
        "```",
    ]
    (issue_dir / "04_final_archive.json").write_text(json.dumps(final_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (issue_dir / "04_final_archive.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    mini = {
        "issue_id": issue_id,
        "title": issue.get("Issue标题", "unknown"),
        "impact": impact.get("arkweb_impact", "unknown"),
        "merge_policy": impact.get("merge_policy", {"force_merge": False, "impact_mode": "normal", "reason": ""}),
        "risk": impact.get("风险评估级别", "unknown"),
        "team": impact.get("归属团队", "unknown"),
        "feature_paths": impact.get("影响的特性", []),
        "selected_fix": selected.get("url", ""),
        "patch_count": len(patch_files),
        "missing_artifacts": missing,
        "archive_result": result,
    }
    (issue_dir / "summary.json").write_text(json.dumps(mini, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (issue_dir / "summary.md").write_text("\n".join(f"- {k}: {v}" for k, v in mini.items()) + "\n", encoding="utf-8")
    return mini


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--issue-archive-root", required=True, type=Path)
    args = parser.parse_args()
    output_root, _project_root = validate_project_output_root(args.output_root, args.project_root)
    summaries = [process_issue(path, args.issue_archive_root) for path in sorted(output_root.iterdir()) if path.is_dir()]
    print(json.dumps({"processed": len(summaries), "issues": summaries}, ensure_ascii=False, indent=2))
    return 0 if summaries else 1


if __name__ == "__main__":
    raise SystemExit(main())
