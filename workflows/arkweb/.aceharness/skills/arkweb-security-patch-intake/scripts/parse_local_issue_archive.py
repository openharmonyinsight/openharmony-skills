#!/usr/bin/env python3
"""Parse local Chromium issue HTML/MHTML archives into per-issue artifacts."""

from __future__ import annotations

import argparse
import email.policy
import html
import json
import re
import zipfile
from datetime import datetime
from email.parser import BytesParser
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, unquote, urlparse

from archive_paths import validate_project_output_root


ISSUE_RE = re.compile(r"(?:issues/|issue\s*#?|crbug\.com/|chromium:?)(\d{6,})", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>)]+" )
CODE_HOST_RE = re.compile(
    r"(chromium-review\.googlesource\.com|chromium\.googlesource\.com|"
    r"skia-review\.googlesource\.com|skia\.googlesource\.com|"
    r"review\.chromium\.org|crrev\.com|github\.com|chromiumdash\.appspot\.com)",
    re.I,
)
FIX_SIGNALS = re.compile(
    r"(fix(?:ed|es)?|landed|committed|submitted|merged|cherry-?pick|"
    r"review-url|code-review|change-id|following revision refers|revert)",
    re.I,
)
BUG_INTRO_SIGNALS = re.compile(
    r"(culprit|bisect|regression range|introduced by|caused by|regressed in|"
    r"first bad|bad revision|bug-introducing)",
    re.I,
)


def read_html(path: Path) -> str:
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix in {".mhtml", ".mht"}:
        msg = BytesParser(policy=email.policy.default).parsebytes(data)
        parts = msg.walk() if msg.is_multipart() else [msg]
        for part in parts:
            if part.get_content_type() == "text/html":
                content = part.get_content()
                return content if isinstance(content, str) else content.decode("utf-8", "ignore")
        for part in parts:
            if part.get_content_type() == "text/plain":
                content = part.get_content()
                return content if isinstance(content, str) else content.decode("utf-8", "ignore")
    return data.decode("utf-8", "ignore")


def text_from_html(raw: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>", " ", raw)
    text = re.sub(r"(?is)<style.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_mhtml_text(raw: str) -> str:
    return re.sub(r"=\r?\n", "", raw)


def clean_url(url: str) -> str:
    url = html.unescape(unquote(url)).rstrip(".,;]")
    url = re.sub(r"[\"'>]+$", "", url)
    parsed = urlparse(url)
    if parsed.netloc.endswith("google.com") and parsed.path == "/url":
        target = parse_qs(parsed.query).get("q", [""])[0]
        if target:
            url = html.unescape(unquote(target)).rstrip(".,;]")
    url = re.sub(r"#.*$", "", url)
    return url


def infer_issue_id(path: Path, raw: str, text: str) -> str:
    for candidate in (path.stem, path.parent.name, raw, text):
        match = ISSUE_RE.search(candidate)
        if match:
            return match.group(1)
    digits = re.search(r"\d{6,}", path.stem)
    return digits.group(0) if digits else path.stem


def extract_title(raw: str, text: str, issue_id: str) -> str:
    for pattern in (
        r"(?is)<title[^>]*>(.*?)</title>",
        rf"([^.\n]{{8,220}}\[{re.escape(issue_id)}\][^.\n]{{0,80}})",
        rf"(Issue\s+{re.escape(issue_id)}[^.\n]{{0,180}})",
    ):
        match = re.search(pattern, raw if "<" in pattern else text)
        if match:
            title = re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()
            title = re.sub(r"\s+-\s+Chromium.*$", " - Chromium", title)
            if title:
                return title[:240]
    return f"Issue {issue_id}"


def extract_field(text: str, names: Iterable[str]) -> str:
    for name in names:
        match = re.search(rf"\b{name}\b\s*[:：]?\s*([A-Za-z0-9_.+-]+)", text, re.I)
        if match:
            return match.group(1)
    return "unknown"


def extract_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    summary_match = re.search(
        r"Resources\s*\(\d+\)\s+([A-Za-z]+)\s+([A-Za-z]+)\s+(P\d)\b",
        text,
        re.I,
    )
    if summary_match:
        metadata["Issue状态"] = summary_match.group(1)
        metadata["Issue类型"] = summary_match.group(2)
        metadata["Priority"] = summary_match.group(3)

    reporter_match = re.search(
        r"([A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+)\s+created issue #1\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s+\d{2}:\d{2}[AP]M)",
        text,
    )
    if reporter_match:
        metadata["reporter"] = reporter_match.group(1)
        metadata["created_time"] = reporter_match.group(2)

    owner_match = re.search(
        r"Assigned to\s+([A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+)",
        text,
        re.I,
    )
    if owner_match:
        metadata["owner"] = owner_match.group(1)

    severity_match = re.search(r"\bS([0-4])\b", text)
    if severity_match:
        metadata["Issue严重程度"] = f"S{severity_match.group(1)}"

    milestone_match = re.search(r"\bM(?:erged-)?(\d{2,3})\b", text, re.I)
    if milestone_match:
        metadata["Milestone"] = milestone_match.group(1)

    return metadata


def extract_commit_hash(context: str, url: str) -> str:
    commit = re.search(r"\bHash:\s*([0-9a-f]{7,40})\b", context, re.I)
    if commit:
        return commit.group(1)
    if "-review.googlesource.com" in url:
        return ""
    commit = re.search(r"/\+/([0-9a-f]{7,40})(?:[/?#]|$)", url, re.I)
    return commit.group(1) if commit else ""


def infer_subject(context: str) -> str:
    bug_split = re.split(r"\b(?:Bug|Fixed|Change-Id):", context, maxsplit=1)
    head = bug_split[0].strip()
    if head:
        head = re.sub(r"\s+", " ", head)
        head = re.sub(r"^[^A-Za-z\"\[]+", "", head)
        if 12 <= len(head) <= 180 and "http" not in head and "Issue Tracker" not in head:
            return head
    for pattern in (
        r'(Reland "[^"]+")',
        r'(Revert "[^"]+")',
        r'([A-Z][A-Za-z0-9][^.\n]{12,160})',
    ):
        match = re.search(pattern, context)
        if match:
            subject = re.sub(r"\s+", " ", match.group(1)).strip(" -")
            if "http" not in subject and "Issue Tracker" not in subject:
                return subject[:180]
    return ""


def build_fix_entry(item: dict[str, str]) -> dict[str, str]:
    url = item["url"]
    context = item["context"]
    cl_match = re.search(
        r"(?:chromium-review|skia-review)\.googlesource\.com/(?:c/[^?#]+/\+/|changes/[^?#]*~)?(\d+)(?:[/?#]|$)",
        url,
        re.I,
    )
    change_id = re.search(r"\bChange-Id:\s*(I[a-f0-9]{8,40})\b", context, re.I)
    commit_hash = extract_commit_hash(context, url)
    item_type = "unknown"
    if cl_match:
        item_type = "gerrit_cl"
    elif "github.com" in url and "/pull/" in url:
        item_type = "github_pr"
    elif "googlesource.com" in url and commit_hash:
        item_type = "gitiles_commit"
    elif "review.chromium.org" in url or "crrev.com" in url:
        item_type = "chromium_review"

    status = "merged" if re.search(r"(Cr-Commit-Position|Hash:|Committed|Landed|Merged)", context, re.I) else "unknown"
    confidence = "high" if status == "merged" else "medium"
    return {
        "type": item_type,
        "url": url,
        "cl_number": cl_match.group(1) if cl_match else "",
        "commit_hash": commit_hash,
        "change_id": change_id.group(1) if change_id else "",
        "subject": infer_subject(context),
        "status": status,
        "source_comment_id": item["comment_id"],
        "confidence": confidence,
    }


def classify_links(raw: str) -> list[dict[str, str]]:
    audits: list[dict[str, str]] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(raw):
        url = clean_url(match.group(0))
        if url in seen or not CODE_HOST_RE.search(url):
            continue
        seen.add(url)
        start = max(0, match.start() - 600)
        end = min(len(raw), match.end() + 600)
        context = text_from_html(raw[start:end])
        is_intro = bool(BUG_INTRO_SIGNALS.search(context))
        is_fix = bool(FIX_SIGNALS.search(context))
        semantic_type = "code link without fix semantics"
        if is_fix and not is_intro:
            decision = "accepted"
            if re.search(r"\bReland\b", context, re.I):
                semantic_type = "relanded fix"
            elif re.search(r"\bRevert\b", context, re.I):
                semantic_type = "revert event"
            else:
                semantic_type = "upstream fix"
            reason = "surrounding text has committed/fixed/merged/review semantics"
        elif is_intro and not is_fix:
            decision = "rejected"
            semantic_type = "bug-introducing candidate"
            reason = "surrounding text points to culprit/regression source"
        elif is_fix and is_intro:
            decision = "review"
            semantic_type = "mixed fix/root-cause signal"
            reason = "context contains both fix and bug-introducing signals"
        else:
            decision = "rejected"
            semantic_type = "code link without fix semantics"
            reason = "no nearby committed/fixed/merged signal"
        audits.append(
            {
                "comment_id": f"link{len(audits) + 1}",
                "decision": decision,
                "semantic_type": semantic_type,
                "url": url,
                "reason": reason,
                "context": context[:500],
            }
        )
    return audits


def dedupe_fix_links(audits: list[dict[str, str]]) -> list[dict[str, str]]:
    by_key: dict[str, dict[str, str]] = {}
    for item in audits:
        if item["decision"] != "accepted":
            continue
        key = item["url"]
        cl = re.search(
            r"(?:chromium-review|skia-review)\.googlesource\.com/(?:c/[^?#]+/\+/|changes/[^?#]*~)?(\d+)(?:[/?#]|$)",
            key,
        )
        if cl:
            key = f"cl:{cl.group(1)}"
        commit = re.search(r"/\+/([0-9a-f]{7,40})(?:[/?#]|$)", item["url"], re.I)
        if commit and "googlesource.com" in item["url"] and "-review.googlesource.com" not in item["url"]:
            key = f"commit:{commit.group(1)}"
        existing = by_key.get(key)
        if existing and ("/c/" not in item["url"] or "/c/" in existing["url"]):
            continue
        by_key[key] = build_fix_entry(item)
    return list(by_key.values())


def parse_one(path: Path, output_root: Path) -> dict[str, object]:
    raw = normalize_mhtml_text(read_html(path))
    text = text_from_html(raw)
    issue_id = infer_issue_id(path, raw, text)
    title = extract_title(raw, text, issue_id)
    audits = classify_links(raw)
    fixes = dedupe_fix_links(audits)
    metadata = extract_metadata(text)
    issue_dir = output_root / issue_id
    issue_dir.mkdir(parents=True, exist_ok=True)

    labels = sorted(set(re.findall(r"\b(?:Type|Pri|Security|FoundIn|FixedIn|Merge|Merged|Milestone)[-_][A-Za-z0-9_.+-]+", text)))
    related_links = sorted({item["url"] for item in audits})
    confidence = "high" if fixes else ("medium" if audits else "low")
    data = {
        "IssueID": issue_id,
        "Issue链接": f"https://issues.chromium.org/issues/{issue_id}" if issue_id.isdigit() else "",
        "Issue状态": metadata.get("Issue状态", extract_field(text, ["Status"])),
        "Issue类型": metadata.get("Issue类型", "Vulnerability" if re.search(r"vulnerability|security|cve|external_security_report", text, re.I) else "unknown"),
        "Issue标题": title,
        "Issue原始标题": title,
        "Issue原始描述": text[:5000],
        "Milestone": metadata.get("Milestone", extract_field(text, ["Milestone", "Target"])),
        "Issue严重程度": metadata.get("Issue严重程度", extract_field(text, ["Severity", "Security_Severity"])),
        "Priority": metadata.get("Priority", extract_field(text, ["Priority", "Pri"])),
        "Labels": labels,
        "reporter": metadata.get("reporter", "unknown"),
        "owner": metadata.get("owner", "unknown"),
        "created_time": metadata.get("created_time", "unknown"),
        "related_links": related_links,
        "可信度": confidence,
        "是否可继续自动抓取patch": bool(fixes),
        "upstream_fix_prs": fixes,
        "fix_event_audit": audits,
        "Issue概述": "基于本地 HTML/MHTML 解析的初步漏洞或缺陷线索，已提取基础字段并审计修复事件，后续阶段继续抓取 patch 与做 ArkWeb 影响判定。",
        "Issue提交信息概述": f"提取到代码相关链接 {len(audits)} 条，接受为修复线索 {len(fixes)} 条；仅 accepted 且具备 fix 语义的链接进入 upstream_fix_prs。",
        "信息缺口": [] if fixes else ["未从本地归档中确认具备明确修复语义的上游 CL/commit 链接"],
        "source_archive_file": str(path),
    }
    (issue_dir / "01_issue_analysis.json").write_text(
        json.dumps({"issues": [data]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# 01 Issue Analysis",
        "",
        "## Basic information",
        f"- Issue ID: {issue_id}",
        f"- Issue URL: {data['Issue链接']}",
        f"- Original title: {title}",
        f"- Chinese title: 待补充",
        f"- Status: {data['Issue状态']}",
        f"- Type: {data['Issue类型']}",
        f"- Priority: {data['Priority']}",
        f"- Severity: {data['Issue严重程度']}",
        f"- Milestone: {data['Milestone']}",
        f"- Reporter: {data['reporter']}",
        f"- Owner: {data['owner']}",
        f"- Created: {data['created_time']}",
        f"- Source archive: {path}",
        f"- Confidence: {confidence}",
        "",
        "## Original issue summary",
        f"- Description snapshot: {text[:1000]}",
        f"- Labels: {', '.join(labels) if labels else 'none'}",
        f"- Related links found: {len(related_links)}",
        "",
        "## Vulnerability or defect summary",
        f"- Problem summary: {title}",
        f"- Initial assessment: {'安全问题或上游安全修复线索明确' if data['Issue类型'].lower() == 'vulnerability' else '缺陷类型待进一步确认'}",
        "",
        "## Upstream fix PR/CL extraction",
        f"- Patch fetch ready: {'yes' if fixes else 'no'}",
    ]
    if fixes:
        lines.extend(
            [
                "",
                "| Type | URL | CL | Commit | Change-Id | Subject | Status | Source Comment | Confidence |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in fixes:
            lines.append(
                f"| {item['type']} | {item['url']} | {item['cl_number'] or '-'} | {item['commit_hash'] or '-'} | {item['change_id'] or '-'} | {item['subject'] or '-'} | {item['status']} | {item['source_comment_id']} | {item['confidence']} |"
            )
    else:
        lines.extend(
            [
                "",
                "- No confirmed upstream fix PR/CL was found in the local archive.",
            ]
        )
    lines.extend(
        [
            "",
            "## Link audit",
            "",
            "| Comment ID | Decision | Semantic Type | URL | Reason |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in audits:
        lines.append(f"| {item['comment_id']} | {item['decision']} | {item['semantic_type']} | {item['url']} | {item['reason']} |")
    if not audits:
        lines.append("| n/a | rejected | none |  | no code review or commit links found |")
    lines.extend(
        [
            "",
            "## Gaps and next step",
            f"- Information gaps: {', '.join(data['信息缺口']) if data['信息缺口'] else 'none'}",
            f"- Can continue automatic patch fetch: {'yes' if data['是否可继续自动抓取patch'] else 'no'}",
        ]
    )
    (issue_dir / "01_issue_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "issue_id": issue_id,
        "file": path.name,
        "fix": len(fixes),
        "audit": len(audits),
        "confidence": confidence,
        "output_dir": str(issue_dir),
    }


def candidate_files(archive_dir: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in ("**/*.mhtml", "**/*.mht", "**/*.html", "**/*.htm"):
        files.extend(path for path in archive_dir.glob(pattern) if path.is_file())
    return sorted(set(files))


def extract_zip_inputs(archive_dir: Path, temp_dir: Path) -> list[Path]:
    extracted: list[Path] = []
    for zip_path in archive_dir.glob("**/*.zip"):
        target_root = temp_dir / zip_path.stem
        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                if info.is_dir() or not info.filename.lower().endswith((".mhtml", ".mht", ".html", ".htm")):
                    continue
                target = target_root / info.filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(info))
                extracted.append(target)
    return extracted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--temp-dir", type=Path)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    archive_dir = args.archive_dir.resolve()
    output_root, _project_root = validate_project_output_root(args.output_root, args.project_root)
    if not archive_dir.is_dir():
        raise SystemExit(f"archive dir not found: {archive_dir}")
    output_root.mkdir(parents=True, exist_ok=True)
    temp_dir = args.temp_dir or (output_root / ".tmp_issue_zip")

    files = candidate_files(archive_dir) + extract_zip_inputs(archive_dir, temp_dir)
    if args.limit > 0:
        files = files[: args.limit]

    results = [parse_one(path, output_root) for path in files]
    summary = {
        "generated_at": datetime.now().isoformat(),
        "archive_dir": str(archive_dir),
        "output_root": str(output_root),
        "issue_count": len(results),
        "issues": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
