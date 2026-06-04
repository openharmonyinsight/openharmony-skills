#!/usr/bin/env python3
"""Generate bounded ArkWeb security patch risk-assessment artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def read_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def parse_build_gate(run_root: Path) -> dict[str, Any]:
    data = read_json(run_root / "09_build_verification.json", {})
    if isinstance(data, dict) and data:
        status = str(data.get("build_status") or "unknown")
        exit_code = data.get("exit_code")
        try:
            exit_code = int(exit_code) if exit_code is not None else None
        except (TypeError, ValueError):
            exit_code = None
        return {
            "build_completed": bool(data.get("build_completed")),
            "build_status": status,
            "exit_code": exit_code,
            "nonblocking_unrelated_build_failure": bool(data.get("nonblocking_unrelated_build_failure")),
            "submit_eligible": bool(data.get("submit_eligible")),
        }

    text = (run_root / "09_build_verification.md").read_text(encoding="utf-8", errors="ignore") if (run_root / "09_build_verification.md").is_file() else ""

    def bool_field(name: str, default: bool = False) -> bool:
        m = re.search(rf"{re.escape(name)}:\s*`?(true|false)`?", text, re.I)
        return (m.group(1).lower() == "true") if m else default

    def str_field(name: str, default: str = "unknown") -> str:
        m = re.search(rf"{re.escape(name)}:\s*`?([^`\n]+)`?", text)
        return m.group(1).strip() if m else default

    def int_field(name: str, default: int | None = None) -> int | None:
        m = re.search(rf"{re.escape(name)}:\s*`?(-?\d+)`?", text)
        return int(m.group(1)) if m else default

    return {
        "build_completed": bool_field("build_completed"),
        "build_status": str_field("build_status"),
        "exit_code": int_field("exit_code"),
        "nonblocking_unrelated_build_failure": bool_field("nonblocking_unrelated_build_failure"),
        "submit_eligible": bool_field("submit_eligible"),
    }


def detect_force_merge(run_root: Path, batch: dict[str, Any]) -> dict[str, Any]:
    policy = batch.get("merge_policy") or {}
    if policy:
        return policy
    return {
        "force_merge": False,
        "impact_mode": "normal",
        "source": "default",
        "reason": "未检测到强制合入策略。",
    }


def first_issue_payload(data: Any) -> dict[str, Any]:
    if isinstance(data, dict) and isinstance(data.get("issues"), list) and data["issues"]:
        return data["issues"][0] if isinstance(data["issues"][0], dict) else {}
    return data if isinstance(data, dict) else {}


def issue_record(batch: dict[str, Any], issue_id: str) -> dict[str, Any]:
    for item in batch.get("issues", []):
        if str(item.get("issue_id")) == str(issue_id):
            return item
    return {"issue_id": issue_id}


def impact_for(run_root: Path, issue_id: str) -> dict[str, Any]:
    direct = read_json(run_root / issue_id / "03_impact_decision.json", {})
    return first_issue_payload(direct)


def write_issue(run_root: Path, issue_id: str, result: dict[str, Any]) -> None:
    issue_dir = run_root / "issues" / issue_id
    issue_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# 11 Risk Assessment - {issue_id}",
        "",
        "## Summary",
        f"- submit_decision: `{result['submit_decision']}`",
        f"- real_impact: `{result.get('real_impact', 'unknown')}`",
        f"- risk_level: `{result.get('risk_level', '中')}`",
        f"- build_completed: `{str(result['build_gate']['build_completed']).lower()}`",
        f"- build_status: `{result['build_gate']['build_status']}`",
        f"- exit_code: `{result['build_gate']['exit_code']}`",
        f"- submit_eligible: `{str(result['build_gate']['submit_eligible']).lower()}`",
        "",
        "## Non-blocking Tracking",
        "- 风险项只作为提交背景记录，不作为本阶段阻塞项。",
        "- 回滚建议：按 issue 独立回退对应提交。",
    ]
    (issue_dir / "11_risk_assessment.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (issue_dir / "11_risk_assessment.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True)
    args = parser.parse_args()

    run_root = Path(args.run_root).resolve()
    batch = read_json(run_root / "batch_status.json", {})
    build_gate = parse_build_gate(run_root)
    policy = detect_force_merge(run_root, batch)
    ready = [str(x) for x in batch.get("ready_for_next", [])]
    active = [str(x) for x in batch.get("active_batch", [])]
    pending = [str(x) for x in batch.get("pending_current_stage", [])]
    terminal = [str(x) for x in batch.get("terminal_failed", [])]
    deferred = [str(x) for x in batch.get("deferred_for_archive", [])]
    candidates = [x for x in ready if x in set(active)] or ready

    submit_gate_ok = (
        build_gate["build_completed"]
        and build_gate["submit_eligible"]
        and (
            build_gate["exit_code"] == 0
            or build_gate["build_status"] in ("success", "completed")
            or build_gate["nonblocking_unrelated_build_failure"]
        )
    )

    issue_results: list[dict[str, Any]] = []
    blocking_issues: list[dict[str, str]] = []
    for issue_id in candidates:
        item = issue_record(batch, issue_id)
        impact = impact_for(run_root, issue_id)
        decision = "allow_submit" if submit_gate_ok and item.get("semantic_landed", True) else "block_submit"
        result = {
            "issue_id": issue_id,
            "stage_status": item.get("stage_status", "ready_for_next"),
            "real_impact": impact.get("arkweb_impact") or item.get("arkweb_impact") or "unknown",
            "merge_policy": policy,
            "responsibility_area": impact.get("responsibility_area") or impact.get("责任田") or "",
            "feature_tree": impact.get("feature_tree") or impact.get("影响特性") or "",
            "risk_level": impact.get("risk_level") or "中",
            "build_gate": build_gate,
            "submit_eligible": bool(submit_gate_ok),
            "submit_decision": decision,
            "semantic_landed": bool(item.get("semantic_landed", True)),
            "final_changed_files": item.get("final_changed_files", []),
        }
        write_issue(run_root, issue_id, result)
        issue_results.append(result)
        if decision != "allow_submit":
            blocking_issues.append({"issue_id": issue_id, "reason": "submit_gate_not_satisfied"})

    archive_only = []
    for issue_id in terminal:
        item = issue_record(batch, issue_id)
        archive_only.append({
            "issue_id": issue_id,
            "stage_status": "terminal_failed",
            "reason": "; ".join(str(x) for x in item.get("blockers", [])) or "terminal_failed",
        })
    for issue_id in deferred:
        archive_only.append({"issue_id": issue_id, "stage_status": "deferred_for_archive", "reason": "deferred_for_archive"})

    verdict = "pass" if not blocking_issues and submit_gate_ok and candidates else "fail"
    next_state = "提交上库" if verdict == "pass" else "结果归档"
    issues = [
        {"type": "implementation", "severity": "major", "description": f"{x['issue_id']}: {x['reason']}"}
        for x in blocking_issues
    ]
    state_json = {
        "verdict": verdict,
        "next_state": next_state,
        "issues": issues,
        "summary": "active batch 已合入并通过编译，风险仅作非阻塞记录，可进入提交上库。" if verdict == "pass" else "提交门槛未满足，进入结果归档。",
    }
    summary = {
        "stage": "风险评估",
        "archive_run_id": run_root.name,
        "merge_policy": policy,
        "build_gate": build_gate,
        "active_batch": active,
        "ready_for_next": ready,
        "pending_current_stage": pending,
        "archive_only_issues": archive_only,
        "issues": issue_results,
        **state_json,
    }

    md = [
        "# 11 Risk Assessment",
        "",
        "## Summary",
        f"- verdict: `{verdict}`",
        f"- next_state: `{next_state}`",
        f"- force_merge: `{str(bool(policy.get('force_merge'))).lower()}`",
        f"- build_completed: `{str(build_gate['build_completed']).lower()}`",
        f"- build_status: `{build_gate['build_status']}`",
        f"- exit_code: `{build_gate['exit_code']}`",
        f"- submit_eligible: `{str(build_gate['submit_eligible']).lower()}`",
        "",
        "## Submit Candidates",
    ]
    for item in issue_results:
        md.append(f"- `{item['issue_id']}`: `{item['submit_decision']}`, impact=`{item['real_impact']}`, risk=`{item['risk_level']}`")
    md.extend(["", "## Archive Only"])
    if archive_only:
        md.extend(f"- `{x['issue_id']}`: `{x['stage_status']}`, {x['reason']}" for x in archive_only)
    else:
        md.append("- None.")
    md.extend(["", "## State Machine JSON", "```json", json.dumps(state_json, ensure_ascii=False, indent=2), "```"])

    (run_root / "11_risk_assessment.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (run_root / "11_risk_assessment.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state_json, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
