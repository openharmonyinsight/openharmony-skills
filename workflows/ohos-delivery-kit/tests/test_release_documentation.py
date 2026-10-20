"""Regression checks for the ODK workflow release documentation."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

WORKFLOW_ROOT = Path(__file__).resolve().parents[1]


class ReleaseDocumentationTest(unittest.TestCase):
    def test_manifest_registers_every_shipped_skill_and_command(self) -> None:
        manifest = (WORKFLOW_ROOT / "plugin.yaml").read_text(encoding="utf-8")
        registered = re.findall(r"(?:path: | - )(skills/[^\s]+/SKILL\.md)", manifest)
        shipped = {
            path.relative_to(WORKFLOW_ROOT).as_posix()
            for path in (WORKFLOW_ROOT / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(shipped, set(registered))
        self.assertEqual(len(registered), len(set(registered)))
        commands = re.findall(r"^    - skill: (\S+)$", manifest, re.MULTILINE)
        public = {Path(path).parent.name for path in shipped} - {"using-odk", "using-odk-bridge"}
        self.assertEqual(public, set(commands))
        self.assertEqual(len(commands), len(set(commands)))

    def test_release_version_matches_provenance(self) -> None:
        manifest = (WORKFLOW_ROOT / "plugin.yaml").read_text(encoding="utf-8")
        provenance = (WORKFLOW_ROOT / "provenance.yaml").read_text(encoding="utf-8")
        version = re.search(r"^version: (\S+)$", manifest, re.MULTILINE).group(1)
        source_version = re.search(r"^  sourceVersion: (\S+)$", provenance, re.MULTILINE).group(1)
        self.assertEqual(source_version, version)
        changelog = (WORKFLOW_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(version, re.search(r"^## \[([^]]+)\]", changelog, re.MULTILINE).group(1))

    def test_shared_skill_references_resolve_to_declared_assets(self) -> None:
        manifest = (WORKFLOW_ROOT / "plugin.yaml").read_text(encoding="utf-8")
        asset_root = WORKFLOW_ROOT / re.search(r"^  ASSET_ROOT: (\S+)$", manifest, re.MULTILINE).group(1)
        references = 0
        for skill in (WORKFLOW_ROOT / "skills").glob("*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("{{PLUGIN_ROOT}}", text)
            self.assertNotRegex(text, r"`(?:templates|contracts|profiles|rules|adapters)/")
            for target in re.findall(r"`\{\{ASSET_ROOT\}\}/([^`\n]+)`", text):
                if "<" in target or "*" in target:
                    continue  # Runtime-selected phase/profile, not a literal file.
                references += 1
                self.assertTrue((asset_root / target.split("#", 1)[0]).exists(), f"{skill}: {target}")
        self.assertGreater(references, 0)
        contract = (asset_root / "contracts/artifacts.yaml").read_text(encoding="utf-8")
        for target in re.findall(r'^    template: "([^"]+)"$', contract, re.MULTILINE):
            self.assertTrue((asset_root / target).is_file(), target)

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

        self.assertIn("## 0.12.0 proposal ID / delivery handoff", readme)
        self.assertIn("digits only", readme)
        self.assertIn("codespec/changes/<repo-name>/<proposal-id>/", readme)
        self.assertIn("metadata_tracking.yaml", readme)
        self.assertIn("requires all five files", " ".join(readme.split()))
        self.assertIn("same final-readiness checks as archive mode", " ".join(readme.split()))
        self.assertIn("owner-qualified signatures", " ".join(readme.split()))
        self.assertIn("optional extension", readme)
        self.assertIn(f"{skill_count} ODK skills", readme)
        self.assertIn("## [0.11.0] - 2026-09-04", changelog)
        self.assertIn("## [0.12.0] - 2026-09-24", changelog)
        self.assertIn("MIGRATION-0.12.0.md", readme)
        self.assertTrue((WORKFLOW_ROOT / "MIGRATION-0.12.0.md").is_file())
        self.assertIn("repository_url", readme)
        self.assertIn("odk-link-proposal", readme)
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
