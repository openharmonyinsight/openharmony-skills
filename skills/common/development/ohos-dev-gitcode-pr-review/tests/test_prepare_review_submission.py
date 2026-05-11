#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "prepare_review_submission.py"


class PrepareReviewSubmissionFindingsTest(unittest.TestCase):
    def write_context(self, root: Path) -> Path:
        context_dir = root / "context"
        context_dir.mkdir()
        summary = {
            "ok": True,
            "pr": {"number": 123, "repo": "openharmony/example", "source_ref": "123"},
            "files": [
                {
                    "path": "src/example.cpp",
                    "commentable_lines": [10, 11, 12],
                    "hunks": [{"commentable_lines": [10, 11, 12]}],
                }
            ],
        }
        (context_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
        return context_dir

    def run_script(self, root: Path, findings: object, *extra_args: str) -> subprocess.CompletedProcess[str]:
        context_dir = self.write_context(root)
        findings_path = root / "findings.json"
        findings_path.write_text(json.dumps(findings), encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--context-dir",
                str(context_dir),
                "--findings",
                str(findings_path),
                *extra_args,
            ],
            capture_output=True,
            text=True,
        )

    def test_existing_draft_input_still_previews_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context_dir = self.write_context(root)
            draft_path = root / "review-draft.json"
            draft_path.write_text(
                json.dumps(
                    {
                        "summary": "整体评论。",
                        "line_comments": [
                            {"path": "src/example.cpp", "line": 10, "body": "已有 draft 入口仍可用。"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--context-dir",
                    str(context_dir),
                    "--draft",
                    str(draft_path),
                ],
                capture_output=True,
                text=True,
            )

        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command_count"], 2)

    def test_findings_generate_valid_line_comment_commands(self) -> None:
        findings = {
            "summary": "发现 1 个问题。",
            "findings": [
                {
                    "id": "F001",
                    "severity": "medium",
                    "status": "draft",
                    "comment_target": "line",
                    "path": "src/example.cpp",
                    "line": 11,
                    "body": "**中** `src/example.cpp:11`\n\n这里会破坏旧调用方。\n\n建议：补充兼容分支。",
                },
                {
                    "id": "F002",
                    "severity": "low",
                    "status": "skipped",
                    "comment_target": "line",
                    "path": "src/example.cpp",
                    "line": 12,
                    "body": "跳过的问题不应提交。",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_script(Path(tmp), findings)

        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command_count"], 2)
        self.assertEqual(payload["commands"][0][:3], ["oh-gc", "pr:comment", "123"])
        self.assertIn("--path", payload["commands"][1])
        self.assertIn("--line", payload["commands"][1])
        self.assertIn("11", payload["commands"][1])
        self.assertNotIn("跳过的问题", json.dumps(payload, ensure_ascii=False))

    def test_findings_reject_non_commentable_line(self) -> None:
        findings = {
            "findings": [
                {
                    "id": "F001",
                    "severity": "medium",
                    "status": "draft",
                    "comment_target": "line",
                    "path": "src/example.cpp",
                    "line": 99,
                    "body": "这行不在可评论范围内。",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_script(Path(tmp), findings)

        self.assertNotEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        self.assertIn("not commentable", "\n".join(payload["errors"]))

    def test_findings_can_write_draft_file(self) -> None:
        findings = {
            "findings": [
                {
                    "id": "F001",
                    "severity": "medium",
                    "status": "draft",
                    "comment_target": "line",
                    "path": "src/example.cpp",
                    "line": 10,
                    "body": "可以提交的问题。",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "review-draft.json"
            proc = self.run_script(Path(tmp), findings, "--write-draft", str(draft_path))
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            draft = json.loads(draft_path.read_text(encoding="utf-8"))

        self.assertEqual(draft["line_comments"][0]["path"], "src/example.cpp")
        self.assertEqual(draft["line_comments"][0]["line"], 10)


if __name__ == "__main__":
    unittest.main()
