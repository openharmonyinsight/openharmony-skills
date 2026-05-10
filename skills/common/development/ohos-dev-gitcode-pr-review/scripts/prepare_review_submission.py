#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_draft(summary: dict[str, object], draft: dict[str, object]) -> list[str]:
    errors: list[str] = []
    files = summary.get("files", [])
    valid_paths = {item["path"] for item in files if isinstance(item, dict) and "path" in item}
    valid_lines = {
        item["path"]: set(item.get("commentable_lines", []))
        for item in files
        if isinstance(item, dict) and "path" in item
    }

    if "summary" in draft and not isinstance(draft["summary"], str):
        errors.append("draft.summary must be a string")
    if "approve" in draft and not isinstance(draft["approve"], bool):
        errors.append("draft.approve must be a boolean")

    line_comments = draft.get("line_comments", [])
    if line_comments is None:
        line_comments = []
    if not isinstance(line_comments, list):
        errors.append("draft.line_comments must be a list")
        return errors

    for index, comment in enumerate(line_comments):
        if not isinstance(comment, dict):
            errors.append(f"line_comments[{index}] must be an object")
            continue
        path = comment.get("path")
        line = comment.get("line")
        body = comment.get("body")
        if not isinstance(path, str) or not path:
            errors.append(f"line_comments[{index}].path must be a non-empty string")
            continue
        if path not in valid_paths:
            errors.append(f"line_comments[{index}].path is not part of the collected diff: {path}")
        if not isinstance(line, int):
            errors.append(f"line_comments[{index}].line must be an integer")
        elif path in valid_lines and line not in valid_lines[path]:
            errors.append(f"line_comments[{index}] line {line} is not commentable for {path}")
        if not isinstance(body, str) or not body.strip():
            errors.append(f"line_comments[{index}].body must be a non-empty string")

    return errors


def build_commands(pr: dict[str, object], draft: dict[str, object]) -> list[list[str]]:
    number = str(pr["number"])
    repo = pr.get("repo")
    repo_args = ["--repo", str(repo)] if repo else []

    commands: list[list[str]] = []
    summary_text = draft.get("summary")
    if isinstance(summary_text, str) and summary_text.strip():
        commands.append(["oh-gc", "pr:comment", number, "--body", summary_text, *repo_args])

    for comment in draft.get("line_comments", []) or []:
        commands.append(
            [
                "oh-gc",
                "pr:comment",
                number,
                "--body",
                str(comment["body"]),
                "--path",
                str(comment["path"]),
                "--line",
                str(comment["line"]),
                *repo_args,
            ]
        )

    if draft.get("approve") is True:
        commands.append(["oh-gc", "pr:review", number, *repo_args])
    return commands


def execute(commands: list[list[str]]) -> list[dict[str, object]]:
    results = []
    for command in commands:
        proc = subprocess.run(command, capture_output=True, text=True)
        results.append(
            {
                "command": command,
                "exit_code": proc.returncode,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
        )
        if proc.returncode != 0:
            break
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and optionally submit GitCode PR review comments.")
    parser.add_argument("--context-dir", required=True, help="Directory produced by collect_pr_context.py")
    parser.add_argument("--draft", required=True, help="Draft review JSON file")
    parser.add_argument("--execute", action="store_true", help="Execute generated oh-gc commands")
    args = parser.parse_args()

    context_dir = Path(args.context_dir)
    summary = load_json(context_dir / "summary.json")
    draft = load_json(Path(args.draft))

    if not isinstance(summary, dict) or summary.get("ok") is not True:
        print(json.dumps({"ok": False, "error": "summary.json is missing or invalid"}, ensure_ascii=False, indent=2))
        return 1
    if not isinstance(draft, dict):
        print(json.dumps({"ok": False, "error": "draft file must be a JSON object"}, ensure_ascii=False, indent=2))
        return 1

    errors = validate_draft(summary, draft)
    commands = build_commands(summary["pr"], draft) if not errors else []

    response: dict[str, object] = {
        "ok": not errors,
        "errors": errors,
        "command_count": len(commands),
        "commands": commands,
    }

    if errors or not args.execute:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return 1 if errors else 0

    results = execute(commands)
    response["results"] = results
    response["ok"] = all(item["exit_code"] == 0 for item in results) and len(results) == len(commands)
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0 if response["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
