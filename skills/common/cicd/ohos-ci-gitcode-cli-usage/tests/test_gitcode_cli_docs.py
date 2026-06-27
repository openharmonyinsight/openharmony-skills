import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTENDED_COMMANDS = ROOT / "references" / "extended-commands.md"
SKILL = ROOT / "SKILL.md"


def user_section() -> str:
    text = EXTENDED_COMMANDS.read_text(encoding="utf-8")
    match = re.search(r"## User\n\n```bash\n(?P<body>.*?)\n```\n", text, re.DOTALL)
    if match is None:
        raise AssertionError("extended-commands.md must contain a fenced bash block under ## User")
    return match.group("body")


class GitCodeCliExtendedDocsTest(unittest.TestCase):
    def test_user_issues_documents_pagination_and_time_filters(self):
        section = user_section()

        self.assertIn("oh-gc user issues --per-page 100", section)
        self.assertIn("oh-gc user issues --per-page 50 --page 2", section)
        self.assertIn("--since: 按更新时间过滤", section)
        self.assertIn('oh-gc user issues --since "2024-01-01T00:00:00Z"', section)
        self.assertIn("--created-at: 按创建时间范围过滤，格式为 START..END（两端必填）", section)
        self.assertIn('oh-gc user issues --created-at "2024-01-01..2025-12-31"', section)
        self.assertIn('oh-gc user issues --state closed --finished-at "2025-01-01..2025-12-31"', section)

    def test_skill_reminds_agents_to_use_help_for_unfamiliar_commands(self):
        skill = SKILL.read_text(encoding="utf-8")

        self.assertIn("When a needed command or flag is unfamiliar, run the command with `--help` first", skill)


if __name__ == "__main__":
    unittest.main()
