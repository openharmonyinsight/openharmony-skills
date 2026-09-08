"""Regression checks for the ODK workflow release documentation."""

from __future__ import annotations

from pathlib import Path
import unittest


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]


class ReleaseDocumentationTest(unittest.TestCase):
    def test_current_contract_is_documented(self) -> None:
        readme = (WORKFLOW_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (WORKFLOW_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
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
        self.assertIn("500c0063d9a532e5e64caa01a262e302c976fea1", changelog)
        self.assertIn("Breaking", changelog)
        self.assertIn("optional extension", changelog)
        self.assertIn("per-API specification contract", changelog)
        self.assertIn("archive-equivalent final-readiness checks", changelog)


if __name__ == "__main__":
    unittest.main()
