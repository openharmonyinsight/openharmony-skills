#!/usr/bin/env python3
"""Generate bounded ArkWeb security patch code-review artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git_diff_names(repo: Path, files: list[str]) -> list[str]:
    if not files:
        return []
    cmd = ["git", "-C", str(repo), "diff", "--name-only", "--", *files]
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def has_conflict_marker(repo: Path, files: list[str]) -> bool:
    for rel in files:
        p = repo / rel
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            stripped = line.strip()
            if any(stripped.startswith(marker) for marker in CONFLICT_MARKERS):
                return True
    return False


def issue_record(batch: dict[str, Any], issue_id: str) -> dict[str, Any] | None:
    for item in batch.get("issues", []):
        if str(item.get("issue_id")) == str(issue_id):
            return item
    return None


def read_issue_merge_result(run_root: Path, issue_id: str) -> dict[str, Any] | None:
    path = run_root / "issues" / issue_id / "06_merge_result.json"
    if not path.exists():
        return None
    return read_json(path)


def issue_verdict(
    item: dict[str, Any],
    merge_result: dict[str, Any] | None,
    diff_names: list[str],
    conflict: bool,
    issue_md_exists: bool,
    root_md_exists: bool,
) -> tuple[str, list[str]]:
    blockers: list[str] = []
    if item.get("stage_status") not in ("ready_for_next", "pending_current_stage"):
        blockers.append(f"stage_status_not_active:{item.get('stage_status')}")
    semantic_landed = item.get("semantic_landed")
    if semantic_landed is None and merge_result is not None:
        semantic_landed = merge_result.get("semantic_landed")
    if not semantic_landed:
        blockers.append("semantic_landed_false")
    final_changed_files = item.get("final_changed_files")
    if final_changed_files is None and merge_result is not None:
        final_changed_files = merge_result.get("final_changed_files")
    if not final_changed_files:
        blockers.append("empty_final_changed_files")
    if conflict:
        blockers.append("unresolved_conflict_marker")
    if final_changed_files and not diff_names:
        blockers.append("empty_current_issue_diff")
    if not root_md_exists or not issue_md_exists:
        blockers.append("artifact_missing:06_merge_result")
    return ("fail" if blockers else "pass", blockers)


def write_issue_md(run_root: Path, issue_id: str, item: dict[str, Any], status: str, blockers: list[str], diff_names: list[str], conflict: bool) -> None:
    issue_dir = run_root / "issues" / issue_id
    issue_dir.mkdir(parents=True, exist_ok=True)
    files = item.get("final_changed_files", [])
    lines = [
        f"# 08 Code Review - {issue_id}",
        "",
        "## Scope",
        f"- issue_id: `{issue_id}`",
        f"- target_subrepo: `{item.get('target_git_subrepo') or item.get('target_subrepo', '')}`",
        f"- stage_status: `{item.get('stage_status', '')}`",
        f"- changed_count: `{len(files)}`",
        "",
        "## Result",
        f"- verdict: `{status}`",
        f"- semantic_landed: `{str(bool(item.get('semantic_landed'))).lower()}`",
        f"- apply_ok: `{str(bool(item.get('apply_ok'))).lower()}`",
        f"- manual_applied: `{str(bool(item.get('manual_applied'))).lower()}`",
        f"- current_issue_diff_files: `{len(diff_names)}`",
        f"- conflict_markers: `{str(conflict).lower()}`",
        "",
        "## Blockers",
    ]
    if blockers:
        lines.extend(f"- `{b}`" for b in blockers)
    else:
        lines.append("- None.")
    lines.extend(["", "## Files"])
    lines.extend(f"- `{f}`" for f in files)
    (issue_dir / "08_code_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True)
    args = parser.parse_args()

    run_root = Path(args.run_root).resolve()
    batch = read_json(run_root / "batch_status.json")
    root_merge_md = run_root / "06_merge_result.md"
    active = [str(x) for x in batch.get("active_batch", [])]
    ready = [str(x) for x in batch.get("ready_for_next", [])]
    pending = [str(x) for x in batch.get("pending_current_stage", [])]
    terminal = [str(x) for x in batch.get("terminal_failed", [])]
    deferred = [str(x) for x in batch.get("deferred_for_archive", [])]

    issue_results: list[dict[str, Any]] = []
    blocked: list[dict[str, str]] = []
    review_ids = active or ready or pending
    for issue_id in review_ids:
        item = issue_record(batch, issue_id)
        if item is None:
            blocked.append({"issue_id": issue_id, "reason": "missing_issue_in_batch_status"})
            continue
        merge_result = read_issue_merge_result(run_root, issue_id)
        issue_merge_md = run_root / "issues" / issue_id / "06_merge_result.md"
        repo = Path(
            str(
                item.get("target_git_subrepo")
                or item.get("target_subrepo")
                or (merge_result or {}).get("target_git_subrepo")
                or (merge_result or {}).get("target_subrepo")
                or batch.get("project_root")
                or "."
            )
        ).resolve()
        files = [str(x) for x in item.get("final_changed_files", [])]
        if not files and merge_result:
            files = [str(x) for x in merge_result.get("final_changed_files", [])]
        diff_names = run_git_diff_names(repo, files)
        conflict = has_conflict_marker(repo, files)
        status, blockers = issue_verdict(
            item,
            merge_result,
            diff_names,
            conflict,
            issue_merge_md.exists(),
            root_merge_md.exists(),
        )
        write_issue_md(run_root, issue_id, item, status, blockers, diff_names, conflict)
        result = {
            "issue_id": issue_id,
            "status": status,
            "target_subrepo": str(repo),
            "changed_count": len(files),
            "current_issue_diff_count": len(diff_names),
            "blockers": blockers,
        }
        issue_results.append(result)
        for blocker in blockers:
            blocked.append({"issue_id": issue_id, "reason": blocker})

    verdict = "pass" if not blocked and not pending and ready else "fail"
    next_state = "编译验证" if verdict == "pass" else "冲突解决"
    issues = [
        {
            "type": "implementation",
            "severity": "major",
            "description": f"{b['issue_id']}: {b['reason']}",
        }
        for b in blocked
    ]

    summary = {
        "verdict": verdict,
        "next_state": next_state,
        "issues": issues,
        "summary": "active batch 代码审查通过，可进入编译验证。" if verdict == "pass" else "active batch 存在 patch 未真实合入证据，需回到冲突解决。",
        "active_batch": active,
        "ready_for_next": ready,
        "pending_current_stage": pending,
        "terminal_failed": terminal,
        "deferred_for_archive": deferred,
        "issue_results": issue_results,
    }

    md = [
        "# 08 Code Review",
        "",
        "## Summary",
        f"- verdict: `{verdict}`",
        f"- next_state: `{next_state}`",
        f"- active_batch: `{', '.join(active)}`",
        f"- ready_for_next: `{', '.join(ready)}`",
        f"- pending_current_stage: `{', '.join(pending)}`",
        "",
        "## Active Issue Results",
    ]
    for item in issue_results:
        md.append(
            f"- `{item['issue_id']}`: `{item['status']}`, changed={item['changed_count']}, "
            f"current_diff={item['current_issue_diff_count']}, blockers={len(item['blockers'])}"
        )
    md.extend(["", "## Archived Or Deferred"])
    for issue_id in terminal:
        item = issue_record(batch, issue_id) or {}
        reason = "; ".join(str(x) for x in item.get("blockers", [])) or "terminal_failed"
        md.append(f"- `{issue_id}`: terminal_failed, {reason}")
    for issue_id in deferred:
        md.append(f"- `{issue_id}`: deferred_for_archive")
    md.extend(["", "## State Machine JSON", "```json", json.dumps({k: summary[k] for k in ("verdict", "next_state", "issues", "summary")}, ensure_ascii=False, indent=2), "```"])

    (run_root / "08_code_review.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (run_root / "08_code_review.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("verdict", "next_state", "issues", "summary")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
