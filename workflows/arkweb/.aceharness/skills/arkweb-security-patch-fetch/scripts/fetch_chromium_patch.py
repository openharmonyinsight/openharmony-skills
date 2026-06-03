#!/usr/bin/env python3
"""Fetch Chromium Gerrit/Gitiles patches from 01_issue_analysis.json files."""

from __future__ import annotations

import argparse
import base64
import hashlib
import email
import json
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from archive_paths import validate_project_output_root


def strip_xssi(data: bytes) -> bytes:
    return re.sub(rb"^\)\]\}'\n", b"", data)


def http_get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ACEHarness arkweb-security-patch-fetch"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def parse_gerrit_url(url: str) -> dict[str, str] | None:
    patterns = [
        r"(?P<host>[a-z0-9.-]+review\.googlesource\.com)/c/(?P<project>.+?)/\+/(?P<cl>\d+)(?:/(?P<patchset>\d+))?",
        r"(?P<host>[a-z0-9.-]+review\.googlesource\.com)/q/(?P<cl>\d+)",
        r"(?P<host>[a-z0-9.-]+review\.googlesource\.com)/changes/(?P<change>[^/?#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if not match:
            continue
        info = {k: v for k, v in match.groupdict().items() if v}
        if "change" in info:
            change = info["change"]
            info["change_id"] = change
            cl_match = re.search(r"~(\d+)$", change)
            if cl_match:
                info["cl"] = cl_match.group(1)
        elif "project" in info and "cl" in info:
            project = info["project"].replace("/", "%2F")
            info["change_id"] = f"{project}~{info['cl']}"
        return info
    return None


def extract_bug_ids(text: str) -> list[str]:
    return sorted(set(re.findall(r"\b(?:Bug|Fixed):\s*([A-Za-z0-9_./-]+)", text)))


def patch_header_metadata(data: bytes) -> dict[str, str]:
    text = data.decode("utf-8", "ignore")
    info: dict[str, str] = {}
    match = re.search(r"^From ([0-9a-f]{7,40}) ", text, re.M)
    if match:
        info["commit_hash"] = match.group(1)
    match = re.search(r"^From:\s*(.+)$", text, re.M)
    if match:
        info["author"] = match.group(1).strip()
    match = re.search(r"^Date:\s*(.+)$", text, re.M)
    if match:
        info["commit_time"] = match.group(1).strip()
    match = re.search(r"^Subject:\s*(?:\[PATCH\]\s*)?(.+)$", text, re.M)
    if match:
        info["subject"] = match.group(1).strip()
    return info


def validate_patch_bytes(data: bytes) -> tuple[bool, str, str]:
    text = data[:4096].decode("utf-8", "ignore")
    low = text.lower().lstrip()
    first = text.splitlines()[0] if text.splitlines() else ""
    if not data:
        return False, "empty patch artifact", first
    if low.startswith("<!doctype html") or low.startswith("<html") or "not found" in low[:300]:
        return False, "invalid artifact: html/error page", first
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


def decode_gerrit_patch(data: bytes) -> bytes:
    raw = strip_xssi(data).strip()
    try:
        decoded = base64.b64decode(raw, validate=True)
    except Exception:
        return data
    return decoded or data


def gitiles_patch_url(url: str) -> str | None:
    if "googlesource.com" not in url:
        return None
    base = re.sub(r"([?#].*)$", "", url)
    if base.endswith(".patch"):
        return base
    if "/+/" in base:
        return f"{base}.patch"
    return None


def fetch_gerrit(info: dict[str, str], issue_dir: Path, source_url: str) -> dict[str, Any]:
    change_id = info.get("change_id")
    if not change_id:
        raise RuntimeError("cannot derive Gerrit change id")
    host = info.get("host")
    if not host:
        raise RuntimeError("cannot derive Gerrit host")
    encoded = change_id.replace("/", "%2F")
    detail_url = f"https://{host}/changes/{encoded}/detail"
    files_url = f"https://{host}/changes/{encoded}/revisions/current/files"
    patch_url = f"https://{host}/changes/{encoded}/revisions/current/patch?download"

    detail = json.loads(strip_xssi(http_get(detail_url)).decode("utf-8"))
    files = json.loads(strip_xssi(http_get(files_url)).decode("utf-8"))
    patch_data = decode_gerrit_patch(http_get(patch_url))

    patch_dir = issue_dir / "patches"
    patch_dir.mkdir(exist_ok=True)
    patch_name = f"{info.get('cl') or re.sub(r'[^A-Za-z0-9_.-]+', '_', change_id)}.patch"
    patch_path = patch_dir / patch_name
    patch_path.write_bytes(patch_data)
    valid, reason, first = validate_patch_bytes(patch_data)
    patch_meta = patch_header_metadata(patch_data)
    modified = []
    for name, meta in files.items():
        if name == "/COMMIT_MSG":
            continue
        modified.append(
            {
                "path": name,
                "status": {
                    "A": "added",
                    "D": "deleted",
                    "R": "renamed",
                    "C": "copied",
                    "W": "modified",
                    "M": "modified",
                }.get(str(meta.get("status", "M")), "unknown"),
                "old_path": meta.get("old_path", ""),
                "language": "",
                "component_hint": "",
            }
        )
    revision = detail.get("current_revision", "")
    current = detail.get("revisions", {}).get(revision, {}) if isinstance(detail.get("revisions"), dict) else {}
    commit = current.get("commit", {}) if isinstance(current, dict) else {}
    message = commit.get("message", "") if isinstance(commit, dict) else ""
    reviewers = []
    for reviewer in detail.get("reviewers", {}).get("REVIEWER", []):
        if isinstance(reviewer, dict) and reviewer.get("email"):
            reviewers.append(reviewer["email"])
    cr_commit_position = ""
    match = re.search(r"Cr-Commit-Position:\s*(.+)", message)
    if match:
        cr_commit_position = match.group(1).strip()

    return {
        "selected_fix": {
            "url": source_url,
            "cl_number": str(detail.get("_number") or info.get("cl", "")),
            "change_id": detail.get("change_id", ""),
            "commit_hash": revision or patch_meta.get("commit_hash", ""),
            "subject": detail.get("subject", "") or patch_meta.get("subject", ""),
            "author": (commit.get("author") or {}).get("email", "") or patch_meta.get("author", ""),
            "commit_time": (commit.get("committer") or {}).get("date", "") or patch_meta.get("commit_time", ""),
            "reviewers": reviewers,
            "cr_commit_position": cr_commit_position,
            "bug_ids": extract_bug_ids(message),
        },
        "modified_files": modified,
        "patch_files": [
            {
                "path": str(patch_path),
                "source_url": patch_url,
                "format": "patch",
                "sha256": hashlib.sha256(patch_data).hexdigest(),
                "content_valid": valid,
                "validation_reason": reason,
                "first_line_signature": first,
            }
        ],
        "fetch_commands": [
            f"curl -fsSL '{detail_url}'",
            f"curl -fsSL '{files_url}'",
            f"curl -fsSL '{patch_url}' | base64 -d > {patch_path}",
        ],
        "blocking_issues": [] if valid else ["selected patch artifact failed content validation"],
    }


def fetch_gitiles(url: str, issue_dir: Path) -> dict[str, Any]:
    patch_url = gitiles_patch_url(url)
    if not patch_url:
        raise RuntimeError("unsupported Gitiles URL")
    patch_data = http_get(patch_url)
    patch_dir = issue_dir / "patches"
    patch_dir.mkdir(exist_ok=True)
    commit = re.search(r"/\+/([0-9a-f]{7,40})", patch_url, re.I)
    patch_path = patch_dir / f"{commit.group(1) if commit else 'gitiles_commit'}.patch"
    patch_path.write_bytes(patch_data)
    valid, reason, first = validate_patch_bytes(patch_data)
    patch_meta = patch_header_metadata(patch_data)
    modified = sorted(set(re.findall(rb"^\+\+\+ b/(.+)$", patch_data, re.M)))
    text = patch_data.decode("utf-8", "ignore")
    subject_match = re.search(r"^Subject:\s*(.+)$", text, re.M)
    return {
        "selected_fix": {
            "url": url,
            "commit_hash": commit.group(1) if commit else patch_meta.get("commit_hash", ""),
            "subject": subject_match.group(1).strip() if subject_match else patch_meta.get("subject", ""),
            "reviewers": [],
            "author": patch_meta.get("author", ""),
            "commit_time": patch_meta.get("commit_time", ""),
            "cr_commit_position": "",
            "bug_ids": extract_bug_ids(text),
        },
        "modified_files": [{"path": m.decode("utf-8", "ignore"), "status": "modified", "old_path": "", "language": "", "component_hint": ""} for m in modified],
        "patch_files": [
            {
                "path": str(patch_path),
                "source_url": patch_url,
                "format": "patch",
                "sha256": hashlib.sha256(patch_data).hexdigest(),
                "content_valid": valid,
                "validation_reason": reason,
                "first_line_signature": first,
            }
        ],
        "fetch_commands": [f"curl -fsSL '{patch_url}' > {patch_path}"],
        "blocking_issues": [] if valid else ["selected patch artifact failed content validation"],
    }


def fetch_github_pr(url: str, issue_dir: Path) -> dict[str, Any]:
    patch_url = f"{url}.patch"
    patch_data = http_get(patch_url)
    patch_dir = issue_dir / "patches"
    patch_dir.mkdir(exist_ok=True)
    pr_match = re.search(r"/pull/(\d+)", url)
    patch_path = patch_dir / f"github_pr_{pr_match.group(1) if pr_match else 'patch'}.patch"
    patch_path.write_bytes(patch_data)
    valid, reason, first = validate_patch_bytes(patch_data)
    patch_meta = patch_header_metadata(patch_data)
    text = patch_data.decode("utf-8", "ignore")
    msg = email.message_from_string(text)
    subject = msg.get("Subject", "")
    author = msg.get("From", "")
    modified = sorted(set(re.findall(r"^\+\+\+ b/(.+)$", text, re.M)))
    return {
        "selected_fix": {
            "url": url,
            "cl_number": "",
            "change_id": "",
            "commit_hash": patch_meta.get("commit_hash", ""),
            "subject": subject or patch_meta.get("subject", ""),
            "author": author or patch_meta.get("author", ""),
            "commit_time": patch_meta.get("commit_time", ""),
            "reviewers": [],
            "cr_commit_position": "",
            "bug_ids": extract_bug_ids(text),
        },
        "modified_files": [{"path": path, "status": "modified", "old_path": "", "language": "", "component_hint": ""} for path in modified],
        "patch_files": [
            {
                "path": str(patch_path),
                "source_url": patch_url,
                "format": "patch",
                "sha256": hashlib.sha256(patch_data).hexdigest(),
                "content_valid": valid,
                "validation_reason": reason,
                "first_line_signature": first,
            }
        ],
        "fetch_commands": [f"curl -fsSL '{patch_url}' > {patch_path}"],
        "blocking_issues": [] if valid else ["selected patch artifact failed content validation"],
    }


def process_issue(issue_json: Path, offline: bool) -> dict[str, Any]:
    issue_dir = issue_json.parent
    issue_meta = json.loads(issue_json.read_text(encoding="utf-8"))
    if isinstance(issue_meta, dict) and isinstance(issue_meta.get("issues"), list) and issue_meta["issues"]:
        issue = issue_meta["issues"][0]
    else:
        issue = issue_meta
    issue_id = str(issue.get("IssueID") or issue_dir.name)
    candidates = issue.get("upstream_fix_prs") or []
    result: dict[str, Any] = {
        "IssueID": issue_id,
        "selected_fix": {},
        "modified_files": [],
        "patch_files": [],
        "fetch_commands": [],
        "excluded_candidates": [],
        "blocking_issues": [],
        "generated_at": datetime.now().isoformat(),
    }
    if not candidates:
        result["blocking_issues"].append("01_issue_analysis.json has no upstream_fix_prs[]")
    else:
        if offline:
            selected = candidates[0]
            url = selected.get("url", "") if isinstance(selected, dict) else str(selected)
            result["selected_fix"] = {"url": url}
            result["fetch_commands"] = reproducible_commands(url)
            result["excluded_candidates"] = [
                {"url": item.get("url", ""), "reason": "non-primary candidate; kept excluded per single-main-fix rule"}
                for item in candidates[1:]
                if isinstance(item, dict)
            ]
            result["blocking_issues"].append("offline mode: patch not downloaded")
        else:
            fetched_candidates: list[dict[str, Any]] = []
            for idx, candidate in enumerate(candidates):
                url = candidate.get("url", "") if isinstance(candidate, dict) else str(candidate)
                try:
                    if "review.googlesource.com" in url:
                        parsed = parse_gerrit_url(url)
                        if not parsed:
                            raise RuntimeError("unsupported Gerrit URL")
                        fetched = fetch_gerrit(parsed, issue_dir, url)
                    elif "googlesource.com" in url:
                        fetched = fetch_gitiles(url, issue_dir)
                    elif "github.com" in url and "/pull/" in url:
                        fetched = fetch_github_pr(url, issue_dir)
                    else:
                        raise RuntimeError("unsupported upstream fix URL")
                    fetched["_idx"] = idx
                    fetched["_url"] = url
                    fetched["_err"] = ""
                    fetched["_source_candidate"] = candidate if isinstance(candidate, dict) else {"url": url}
                except (urllib.error.URLError, TimeoutError, RuntimeError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
                    fetched = {
                        "_idx": idx,
                        "_url": url,
                        "_err": str(exc),
                        "_source_candidate": candidate if isinstance(candidate, dict) else {"url": url},
                        "selected_fix": {"url": url},
                        "modified_files": [],
                        "patch_files": [],
                        "fetch_commands": reproducible_commands(url),
                        "blocking_issues": [f"candidate fetch failed: {exc}"],
                    }
                fetched_candidates.append(fetched)
                result["fetch_commands"].extend(fetched.get("fetch_commands", []))
            selected = choose_primary(fetched_candidates)
            result.update({k: v for k, v in selected.items() if not k.startswith("_")})
            result["excluded_candidates"] = [
                {"url": item.get("_url", ""), "reason": exclusion_reason(item), "bug_introducing": False}
                for item in fetched_candidates
                if item is not selected
            ]
            if selected.get("_err"):
                result["blocking_issues"].append(f"selected fix fetch failed: {selected['_err']}")

    write_outputs(issue_dir, result)
    return result


def choose_primary(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[int]] = {}
    reverted_subjects: set[str] = set()
    for candidate in candidates:
        source = candidate.get("_source_candidate", {})
        change_id = str(source.get("change_id") or candidate.get("selected_fix", {}).get("change_id") or "")
        if change_id:
            groups.setdefault(change_id, []).append(int(candidate.get("_idx", 0)))
        subject = str(candidate.get("selected_fix", {}).get("subject") or source.get("subject") or "")
        revert_match = re.search(r'^Revert "(.+)"$', subject)
        if revert_match:
            reverted_subjects.add(revert_match.group(1).strip().lower())

    def score(candidate: dict[str, Any]) -> float:
        selected = candidate.get("selected_fix", {})
        source = candidate.get("_source_candidate", {})
        subject = str(selected.get("subject") or source.get("subject") or "").lower()
        patch_files = candidate.get("patch_files", [])
        valid_patch = any(item.get("content_valid") for item in patch_files)
        value = 0.0
        url = str(candidate.get("_url", ""))
        change_id = str(source.get("change_id") or selected.get("change_id") or "")
        duplicate_idxs = groups.get(change_id, []) if change_id else []
        if candidate.get("_err"):
            value -= 50
        if "revert" in subject:
            value -= 20
        if "reland" in subject:
            value += 8
        if subject and subject in reverted_subjects:
            value -= 18
        if "test" in subject and len(candidate.get("modified_files", [])) <= 3:
            value -= 6
        if "chromiumdash.appspot.com/commit/" in url:
            value -= 12
        if "review.googlesource.com/c/" in url:
            value += 3
        if "github.com" in url and "/pull/" in url:
            value -= 2
        if valid_patch:
            value += 4
        if candidate.get("modified_files"):
            value += 2
        if duplicate_idxs:
            if int(candidate.get("_idx", 0)) == max(duplicate_idxs):
                value += 6
            else:
                value -= 4
        status = str(source.get("status", "") or "").lower()
        if status == "merged":
            value += 1
        value -= float(candidate.get("_idx", 0)) * 0.01
        return value

    return sorted(candidates, key=score, reverse=True)[0]


def exclusion_reason(candidate: dict[str, Any]) -> str:
    source = candidate.get("_source_candidate", {})
    subject = str(candidate.get("selected_fix", {}).get("subject") or source.get("subject") or "").lower()
    url = str(candidate.get("_url", ""))
    if candidate.get("_err"):
        return f"excluded because fetch failed: {candidate['_err']}"
    if "revert" in subject:
        return "excluded as revert candidate, not selected main fix"
    if "reland" in subject:
        return "excluded as reland/secondary candidate, not selected main fix"
    if "test" in subject and len(candidate.get("modified_files", [])) <= 3:
        return "excluded as likely test-only/auxiliary candidate, not selected main fix"
    if "chromiumdash.appspot.com/commit/" in url:
        return "excluded as commit mirror link; preferred direct review or patch source"
    if "github.com" in url and "/pull/" in url:
        return "excluded as non-primary GitHub candidate after selecting a more direct upstream patch source"
    return "non-primary candidate; kept excluded per single-main-fix rule"


def reproducible_commands(url: str) -> list[str]:
    info = parse_gerrit_url(url) if "review.googlesource.com" in url else None
    if info and info.get("change_id") and info.get("host"):
        encoded = info["change_id"].replace("/", "%2F")
        return [
            f"curl -fsSL 'https://{info['host']}/changes/{encoded}/detail'",
            f"curl -fsSL 'https://{info['host']}/changes/{encoded}/revisions/current/files'",
            f"curl -fsSL 'https://{info['host']}/changes/{encoded}/revisions/current/patch?download' | base64 -d > patches/{info.get('cl', 'change')}.patch",
        ]
    if "github.com" in url and "/pull/" in url:
        return [f"curl -fsSL '{url}.patch' > patches/github_pr.patch"]
    patch_url = gitiles_patch_url(url)
    return [f"curl -fsSL '{patch_url or url}' > patches/upstream.patch"]


def write_outputs(issue_dir: Path, result: dict[str, Any]) -> None:
    (issue_dir / "02_patch_fetch.json").write_text(
        json.dumps({"issues": [result]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    valid_count = sum(1 for item in result.get("patch_files", []) if item.get("content_valid"))
    lines = [
        "# 02 Patch Fetch",
        "",
        f"- IssueID: {result['IssueID']}",
        f"- Selected fix: {result.get('selected_fix', {}).get('url', '')}",
        f"- Valid patch files: {valid_count}",
        "",
        "## Selected upstream fix",
        "",
        f"- CL: {result.get('selected_fix', {}).get('cl_number', '')}",
        f"- Commit: {result.get('selected_fix', {}).get('commit_hash', '')}",
        f"- Change-Id: {result.get('selected_fix', {}).get('change_id', '')}",
        f"- Subject: {result.get('selected_fix', {}).get('subject', '')}",
        f"- Author: {result.get('selected_fix', {}).get('author', '')}",
        f"- Reviewers: {', '.join(result.get('selected_fix', {}).get('reviewers', []))}",
        f"- Commit time: {result.get('selected_fix', {}).get('commit_time', '')}",
        f"- Cr-Commit-Position: {result.get('selected_fix', {}).get('cr_commit_position', '')}",
        f"- Bug IDs: {', '.join(result.get('selected_fix', {}).get('bug_ids', []))}",
        "",
        "## Modified files",
    ]
    for item in result.get("modified_files", []):
        lines.append(f"- {item.get('path', '')} [{item.get('status', 'unknown')}]")
    lines.extend(["", "## Patch files", "", "| Path | Source URL | Valid | Reason |", "| --- | --- | --- | --- |"])
    for item in result.get("patch_files", []):
        lines.append(f"| {item.get('path', '')} | {item.get('source_url', '')} | {item.get('content_valid', False)} | {item.get('validation_reason', '')} |")
    lines.extend(["", "## Excluded candidates"])
    for item in result.get("excluded_candidates", []):
        lines.append(f"- {item.get('url', '')}: {item.get('reason', '')}")
    lines.extend(["", "## Fetch commands"])
    for cmd in result.get("fetch_commands", []):
        lines.append(f"- `{cmd}`")
    if result.get("blocking_issues"):
        lines.extend(["", "## Blocking issues"])
        for item in result["blocking_issues"]:
            lines.append(f"- {item}")
    (issue_dir / "02_patch_fetch.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_issue_jsons(output_root: Path, issue_id: str | None) -> list[Path]:
    if issue_id:
        return [output_root / issue_id / "01_issue_analysis.json"]
    return sorted(output_root.glob("*/01_issue_analysis.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--issue-id")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    output_root, _project_root = validate_project_output_root(args.output_root, args.project_root)
    issue_jsons = [path for path in find_issue_jsons(output_root, args.issue_id) if path.is_file()]
    results = [process_issue(path, args.offline) for path in issue_jsons]
    print(json.dumps({"processed": len(results), "issues": results}, ensure_ascii=False, indent=2))
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
