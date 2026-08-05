import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RUNNER = Path(__file__).resolve().parents[1] / "run_skill_evals.py"
USER_GUIDE_ROOT = RUNNER.parents[1]


class RunSkillEvalsTest(unittest.TestCase):
    def test_grades_programmatic_assertions_and_marks_llm_judge_manual(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            evals = workspace / "evals.json"
            output = workspace / "output.txt"
            result = workspace / "grading.json"

            evals.write_text(
                json.dumps(
                    {
                        "skill_name": "demo-skill",
                        "evals": [
                            {
                                "id": 1,
                                "name": "demo",
                                "prompt": "generate output",
                                "assertions": [
                                    {"type": "contains", "text": "status: Clarified"},
                                    {"type": "not_contains", "tokens": ["TBD", "待确认"]},
                                    {"type": "regex", "pattern": r"RR-\d{4}-\d{4}-\d{3}"},
                                    {"type": "llm_judge", "text": "输出满足业务语义"},
                                ],
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            output.write_text(
                "rr_id: RR-2026-0512-003\nstatus: Clarified\n",
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "grade",
                    "--evals",
                    str(evals),
                    "--output",
                    str(output),
                    "--eval-id",
                    "1",
                    "--result",
                    str(result),
                ],
                check=True,
            )

            data = json.loads(result.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["passed"], 3)
            self.assertEqual(data["summary"]["manual"], 1)
            self.assertEqual(data["summary"]["failed"], 0)

    def test_collects_benchmark_summary_from_user_guide(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "benchmark.json"
            root = Path(__file__).resolve().parents[1].parent

            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "collect",
                    "--root",
                    str(root),
                    "--benchmark-json",
                    str(out),
                ],
                check=True,
            )

            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertGreaterEqual(data["summary"]["total_cases"], 29)
            self.assertGreaterEqual(data["summary"]["programmatic_assertions"], 40)
            self.assertEqual(
                data["summary"]["total_assertions"],
                data["summary"]["programmatic_assertions"]
                + data["summary"]["manual_assertions"]
                + data["summary"]["unsupported_assertions"],
            )
            self.assertIn("ohos-req-requirement-intake", data["skills"])

    def test_not_contains_tokens_fail_on_forbidden_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            evals = workspace / "evals.json"
            output = workspace / "output.txt"
            result = workspace / "grading.json"

            evals.write_text(
                json.dumps(
                    {
                        "skill_name": "demo-skill",
                        "evals": [
                            {
                                "id": "placeholder",
                                "assertions": [
                                    {"type": "not_contains", "tokens": ["TBD", "待确认"]},
                                ],
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            output.write_text("当前风险：TBD\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "grade",
                    "--evals",
                    str(evals),
                    "--output",
                    str(output),
                    "--eval-id",
                    "placeholder",
                    "--result",
                    str(result),
                ],
                check=True,
            )

            data = json.loads(result.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["failed"], 1)

    def test_real_regex_assertion_uses_pattern_not_description_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            output = workspace / "output.txt"
            result = workspace / "grading.json"
            output.write_text("```mermaid\nflowchart TD\n  A --> B\n```\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "grade",
                    "--evals",
                    str(USER_GUIDE_ROOT / "ohos-req-feasibility-analysis/evals/evals.json"),
                    "--output",
                    str(output),
                    "--eval-id",
                    "1",
                    "--result",
                    str(result),
                ],
                check=True,
            )

            data = json.loads(result.read_text(encoding="utf-8"))
            regex_result = [item for item in data["expectations"] if item["type"] == "regex"][0]
            self.assertEqual(regex_result["status"], "passed")

    def test_real_not_contains_assertion_uses_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            output = workspace / "output.txt"
            result = workspace / "grading.json"
            output.write_text("status: Draft-NeedsClarification\n遗留字段：TBD\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "grade",
                    "--evals",
                    str(USER_GUIDE_ROOT / "ohos-req-requirement-intake/evals/evals.json"),
                    "--output",
                    str(output),
                    "--eval-id",
                    "1",
                    "--result",
                    str(result),
                ],
                check=True,
            )

            data = json.loads(result.read_text(encoding="utf-8"))
            not_contains_result = [item for item in data["expectations"] if item["type"] == "not_contains"][0]
            self.assertEqual(not_contains_result["status"], "failed")

    def test_all_repo_programmatic_assertions_have_machine_fields(self):
        for evals_path in USER_GUIDE_ROOT.glob("ohos-req-*/evals/evals.json"):
            data = json.loads(evals_path.read_text(encoding="utf-8"))
            for case in data.get("evals", []):
                for assertion in case.get("assertions", []) or []:
                    kind = assertion.get("type", "llm_judge")
                    if kind == "regex":
                        self.assertTrue(
                            assertion.get("pattern") or assertion.get("patterns"),
                            f"{evals_path}:{case.get('id')} regex requires pattern(s)",
                        )
                    if kind == "not_contains":
                        self.assertTrue(
                            assertion.get("tokens") or assertion.get("patterns"),
                            f"{evals_path}:{case.get('id')} not_contains requires tokens/patterns",
                        )


if __name__ == "__main__":
    unittest.main()
