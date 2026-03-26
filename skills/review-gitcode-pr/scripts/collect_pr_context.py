#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from urllib.parse import urlparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = Path.cwd() / ".review-gitcode-pr"


def run_command(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def normalize_ref(ref: str) -> dict[str, object]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "normalize_pr_ref.py"), ref],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout.strip() or proc.stderr.strip() or "normalize_pr_ref failed")
    return json.loads(proc.stdout)


def parse_repo_from_remote_url(remote_url: str) -> str | None:
    remote_url = remote_url.strip()
    if not remote_url:
        return None
    if remote_url.startswith("git@"):
        match = re.match(r"git@[^:]+:([^/]+)/(.+?)(?:\.git)?$", remote_url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return None

    parsed = urlparse(remote_url)
    if not parsed.netloc or "gitcode.com" not in parsed.netloc:
        return None
    path = parsed.path.strip("/")
    if not path:
        return None
    parts = path.split("/")
    if len(parts) < 2:
        return None
    repo = parts[1][:-4] if parts[1].endswith(".git") else parts[1]
    return f"{parts[0]}/{repo}"


def resolve_repo_from_git_remotes() -> str | None:
    code, stdout, _ = run_command(["git", "config", "--get-regexp", r"^remote\..*\.url$"])
    if code != 0:
        return None
    for line in stdout.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
        repo = parse_repo_from_remote_url(parts[1])
        if repo:
            return repo
    return None


def parse_name_only(text: str) -> list[str]:
    paths: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # `oh-gc pr:diff --name-only` may prefix each entry with a status marker
        # such as "? ". Normalize those lines back to repository-relative paths.
        match = re.match(r"^(?:\?\??|[ACDMRTUXB])\s+(.+)$", line)
        if match:
            line = match.group(1).strip()

        paths.append(line)
    return paths


def parse_unified_diff(diff_text: str) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    old_line = None
    new_line = None

    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

    for raw_line in diff_text.splitlines():
        if raw_line.startswith("diff --git "):
            parts = raw_line.split()
            path = parts[3][2:] if len(parts) >= 4 and parts[3].startswith("b/") else None
            current = {
                "path": path,
                "commentable_lines": [],
                "hunks": [],
            }
            files.append(current)
            old_line = None
            new_line = None
            continue

        if current is None:
            continue

        if raw_line.startswith("+++ "):
            target = raw_line[4:].strip()
            if target.startswith("b/"):
                current["path"] = target[2:]
            elif target != "/dev/null":
                current["path"] = target
            continue

        match = hunk_re.match(raw_line)
        if match:
            old_line = int(match.group(1))
            new_line = int(match.group(3))
            current["hunks"].append(
                {
                    "header": raw_line,
                    "old_start": old_line,
                    "old_count": int(match.group(2) or "1"),
                    "new_start": new_line,
                    "new_count": int(match.group(4) or "1"),
                    "commentable_lines": [],
                }
            )
            continue

        if old_line is None or new_line is None or not current["hunks"]:
            continue

        last_hunk = current["hunks"][-1]
        if not raw_line:
            continue

        prefix = raw_line[0]
        if prefix == "+":
            last_hunk["commentable_lines"].append(new_line)
            current["commentable_lines"].append(new_line)
            new_line += 1
        elif prefix == " ":
            last_hunk["commentable_lines"].append(new_line)
            current["commentable_lines"].append(new_line)
            old_line += 1
            new_line += 1
        elif prefix == "-":
            old_line += 1

    deduped: list[dict[str, object]] = []
    for item in files:
        path = item.get("path")
        if not path:
            continue
        item["commentable_lines"] = sorted(set(item["commentable_lines"]))
        for hunk in item["hunks"]:
            hunk["commentable_lines"] = sorted(set(hunk["commentable_lines"]))
        deduped.append(item)
    return deduped


def extract_files_from_diff_json(payload: object) -> list[str]:
    if isinstance(payload, list):
        values = payload
    elif isinstance(payload, dict):
        for key in ("files", "changes", "diffs", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                values = value
                break
        else:
            values = []
    else:
        values = []

    paths: list[str] = []
    for item in values:
        if not isinstance(item, dict):
            continue
        for key in ("new_path", "newPath", "path", "file_path", "filePath", "filename"):
            value = item.get(key)
            if isinstance(value, str) and value and value != "/dev/null":
                paths.append(value)
                break
    return sorted(set(paths))


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def maybe_parse_json(text: str) -> object | None:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect GitCode PR metadata, diff, and comments.")
    parser.add_argument("ref", help="PR number or URL")
    parser.add_argument("--repo", help="OWNER/REPO override")
    parser.add_argument("--out-dir", help="Artifact directory. Defaults to .review-gitcode-pr/pr-<n>")
    parser.add_argument("--comments-limit", type=int, default=100, help="How many comments to fetch per type")
    args = parser.parse_args()

    normalized = normalize_ref(args.ref)
    number = int(normalized["number"])
    repo = args.repo or normalized.get("repo") or resolve_repo_from_git_remotes()

    out_dir = Path(args.out_dir) if args.out_dir else (DEFAULT_ROOT / f"pr-{number}")
    out_dir.mkdir(parents=True, exist_ok=True)

    commands = {
        "pr-view.json": ["oh-gc", "pr:view", str(number), "--json"],
        "pr-diff.json": ["oh-gc", "pr:diff", str(number), "--json"],
        "pr-diff-name-only.txt": ["oh-gc", "pr:diff", str(number), "--name-only"],
        "pr-diff.txt": ["oh-gc", "pr:diff", str(number), "--color", "never"],
        "pr-comments.json": [
            "oh-gc",
            "pr:comments",
            str(number),
            "--json",
            "--comment-type",
            "pr_comment",
            "--limit",
            str(args.comments_limit),
        ],
        "pr-diff-comments.json": [
            "oh-gc",
            "pr:comments",
            str(number),
            "--json",
            "--comment-type",
            "diff_comment",
            "--limit",
            str(args.comments_limit),
        ],
    }

    if repo:
        for command in commands.values():
            command.extend(["--repo", str(repo)])

    results: dict[str, object] = {}
    failures: list[dict[str, object]] = []
    for filename, command in commands.items():
        code, stdout, stderr = run_command(command)
        write_text(out_dir / filename, stdout)
        if stderr:
            write_text(out_dir / f"{filename}.stderr", stderr)
        results[filename] = {"command": command, "exit_code": code}
        if code != 0:
            failures.append({"file": filename, "command": command, "stderr": stderr.strip()})

    if failures:
        write_json(out_dir / "summary.json", {"error": "one or more oh-gc commands failed", "failures": failures})
        print(json.dumps({"ok": False, "out_dir": str(out_dir), "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    diff_text = (out_dir / "pr-diff.txt").read_text(encoding="utf-8")
    diff_json = maybe_parse_json((out_dir / "pr-diff.json").read_text(encoding="utf-8"))
    changed_files = parse_name_only((out_dir / "pr-diff-name-only.txt").read_text(encoding="utf-8"))
    parsed_files = parse_unified_diff(diff_text)

    if not changed_files:
        changed_files = extract_files_from_diff_json(diff_json)

    parsed_by_path = {item["path"]: item for item in parsed_files}
    file_summaries: list[dict[str, object]] = []
    for path in changed_files:
        parsed = parsed_by_path.get(path, {"path": path, "commentable_lines": [], "hunks": []})
        file_summaries.append(parsed)

    summary = {
        "ok": True,
        "pr": {
            "number": number,
            "repo": repo,
            "source_ref": normalized.get("source"),
        },
        "artifacts": results,
        "files": file_summaries,
    }
    write_json(out_dir / "summary.json", summary)
    print(json.dumps({"ok": True, "out_dir": str(out_dir), "files": len(file_summaries)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
