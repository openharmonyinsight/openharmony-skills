"""Exercise published FMEA gates with delivery documents, without external tools."""

import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "published_dfx_validator", ROOT / "runtime/executables/validate-artifacts-contract.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

MAIN = """## DFX 设计
### DFX 故障模式分析
| 分析对象 | 故障模式 | 故障影响 | 故障原因 | 严酷度 | 恢复措施 | 关键日志 | 大数据打点事件 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cache | timeout | request fails | remote unavailable | high | retry | timeout log | request_failure | demo@1234567:docs/dfx/fmea.yaml#timeout |
"""
DISPOSITION = """### DFX 故障模式处置
| 编号 | 分析对象 | 故障模式 | 处置 | 关联 AC | 验证方式/证据 |
| --- | --- | --- | --- | --- | --- |
| FM-01 | Cache | timeout | 复用 AC | AC-1.1 | Inject a remote timeout |
"""
SPEC = "- **AC-1.1:** Given remote timeout When requesting Then return a timeout error\n"


def plan(*statuses):
    return (
        "## AC 到 Task 追溯\n"
        "| AC | Task | 验证状态（Pass/Fail/Blocked） |\n"
        "| --- | --- | --- |\n"
        + "".join(f"| AC-1.1 | TASK-{i} | {status} |\n" for i, status in enumerate(statuses, 1))
    )


class DfxGateTest(unittest.TestCase):
    def check_gate(self, design, *, archive=False, specification=SPEC, execution_plan=None):
        with tempfile.TemporaryDirectory() as temporary:
            change = Path(temporary)
            (change / "design.md").write_text(design, encoding="utf-8")
            (change / "spec.md").write_text(specification, encoding="utf-8")
            if execution_plan is not None:
                (change / "execution-plan.md").write_text(execution_plan, encoding="utf-8")
            reporter = validator.Reporter()
            with contextlib.redirect_stdout(io.StringIO()):
                validator.validate_dfx_ac_gate(change, reporter, archive)
            return reporter

    def test_missing_disposition_warns_in_draft_and_blocks_archive(self):
        draft = self.check_gate(MAIN)
        self.assertEqual((0, 1), (draft.failed, draft.warned))
        self.assertGreater(self.check_gate(MAIN, archive=True).failed, 0)

    def test_dangling_ac_blocks_draft(self):
        result = self.check_gate(MAIN + DISPOSITION, specification="")
        self.assertTrue(any("not defined in spec.md" in message for message in result.messages))
        self.assertGreater(result.failed, 0)

    def test_all_linked_ac_tasks_must_pass_archive(self):
        for statuses in (("Fail", "Pass"), ("Blocked", "Pass"), ("Pass", "Fail"), ()):
            with self.subTest(statuses=statuses):
                result = self.check_gate(MAIN + DISPOSITION, archive=True, execution_plan=plan(*statuses))
                self.assertGreater(result.failed, 0)
        result = self.check_gate(MAIN + DISPOSITION, archive=True, execution_plan=plan("Pass", "Pass"))
        self.assertEqual(0, result.failed)
        self.assertGreater(result.passed, 0)

    def test_archive_requires_execution_plan(self):
        self.assertGreater(self.check_gate(MAIN + DISPOSITION, archive=True).failed, 0)

    def test_disposition_must_cover_original_fault_mode(self):
        result = self.check_gate(MAIN + DISPOSITION.replace("| Cache | timeout | 复用", "| Cache | crash | 复用"))
        self.assertGreater(result.failed, 0)

    def test_ad_only_analysis_requires_matching_disposition(self):
        design = """## DFX 设计
### 推导条目
| 编号 | 结构元素 | 故障模式 |
| --- | --- | --- |
| AD-01 | Cache | timeout |
"""
        self.assertGreater(self.check_gate(design, archive=True).failed, 0)
        disposition = DISPOSITION.replace("FM-01", "AD-01")
        self.assertEqual(0, self.check_gate(design + disposition).failed)
        self.assertGreater(self.check_gate(design + disposition.replace("| Cache |", "| Other |" )).failed, 0)

    def test_design_constraint_task_requires_pass(self):
        disposition = DISPOSITION.replace("复用 AC | AC-1.1 | Inject a remote timeout", "纳入设计约束 | | D-01 ownership invariant; TASK-1 unit test")
        for status in ("Fail", "Blocked"):
            self.assertGreater(self.check_gate(MAIN + disposition, archive=True, execution_plan=plan(status)).failed, 0)
        self.assertEqual(0, self.check_gate(MAIN + disposition, archive=True, execution_plan=plan("Pass")).failed)

    def test_no_fault_modes_needs_no_disposition(self):
        result = self.check_gate("## DFX 设计\n### DFX 故障模式分析\n不涉及\n", archive=True)
        self.assertEqual((0, 0), (result.failed, result.warned))

    def test_malformed_optional_export_only_warns(self):
        with tempfile.TemporaryDirectory() as temporary:
            change = Path(temporary)
            (change / "design.md").write_text(
                "## DFX 设计\n### 故障模式库导出表格\n| 故障模式 |\n| --- |\n| timeout |\n", encoding="utf-8"
            )
            reporter = validator.Reporter()
            with contextlib.redirect_stdout(io.StringIO()):
                validator.validate_dfx_export_table(change, reporter)
            self.assertEqual((0, 1), (reporter.failed, reporter.warned))


if __name__ == "__main__":
    unittest.main()
