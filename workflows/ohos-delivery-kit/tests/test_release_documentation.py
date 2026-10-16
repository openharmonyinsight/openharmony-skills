"""Regression checks for the ODK workflow release documentation."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

WORKFLOW_ROOT = Path(__file__).resolve().parents[1]


class ReleaseDocumentationTest(unittest.TestCase):
    def test_current_contract_is_documented(self) -> None:
        readme = (WORKFLOW_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (WORKFLOW_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        provenance = (WORKFLOW_ROOT / "provenance.yaml").read_text(encoding="utf-8")
        source_block = re.search(
            r"^source:\s*$\n(?P<body>(?:^  .*$\n?)+)", provenance, re.MULTILINE
        )
        self.assertIsNotNone(source_block)
        provenance_commit = re.search(
            r"^  commit:\s*([0-9a-f]{40})\s*$",
            source_block.group("body"),
            re.MULTILINE,
        )
        self.assertIsNotNone(provenance_commit)
        skill_count = len(list((WORKFLOW_ROOT / "skills").glob("*/SKILL.md")))

        self.assertIn("## 0.11.0 req-id / design-docs contract change", readme)
        self.assertIn("digits only", readme)
        self.assertIn("codespec/changes/<repo-name>/<req-id>/", readme)
        self.assertIn("metadata_tracking.yaml", readme)
        self.assertIn("requires all five files", " ".join(readme.split()))
        self.assertIn("same final-readiness checks as archive mode", " ".join(readme.split()))
        self.assertIn("owner-qualified signatures", " ".join(readme.split()))
        self.assertIn("optional extension", readme)
        self.assertIn(f"{skill_count} ODK skills", readme)
        self.assertIn("## [0.11.0] - 2026-09-04", changelog)
        source_match = re.search(
            r"^Source: `main@([0-9a-f]{40})`\.$", changelog, re.MULTILINE
        )
        self.assertIsNotNone(source_match)
        self.assertEqual(provenance_commit.group(1), source_match.group(1))
        self.assertIn("Breaking", changelog)
        self.assertIn("optional extension", changelog)
        self.assertIn("per-API specification contract", changelog)
        self.assertIn("archive-equivalent final-readiness checks", changelog)
        self.assertIn("ignores HTML comments and fenced examples", changelog)
        self.assertIn("semantic duplicates", readme)
        self.assertIn("merge_requests", changelog)
        self.assertIn("issue IDs", readme)

    def test_host_specific_command_prefixes_are_not_hard_coded(self) -> None:
        roots = (
            WORKFLOW_ROOT / "skills",
            WORKFLOW_ROOT / "runtime" / "assets" / "templates",
        )
        offenders = []
        for root in roots:
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(WORKFLOW_ROOT).as_posix()
                for line_number, line in enumerate(
                    path.read_text(encoding="utf-8").splitlines(), start=1
                ):
                    if "/odk-" not in line:
                        continue
                    if (
                        relative == "skills/using-odk-bridge/SKILL.md"
                        and "odk-sp-*/odk-ops-*/odk-ms-*" in line
                    ):
                        continue
                    offenders.append(f"{relative}:{line_number}")
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
