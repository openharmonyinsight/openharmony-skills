"""Regression checks for the published ODK runtime contract validators."""

from __future__ import annotations

import importlib.util
import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module(
    "published_odk_validator",
    WORKFLOW_ROOT / "runtime" / "executables" / "validate-artifacts-contract.py",
)
odk_yaml = load_module(
    "published_odk_yaml",
    WORKFLOW_ROOT / "runtime" / "executables" / "lib" / "odk_yaml.py",
)


class RuntimeContractRegressionTest(unittest.TestCase):
    def validate_api_documents(self, proposal: str, spec: str) -> str:
        with tempfile.TemporaryDirectory() as temporary:
            change_dir = Path(temporary)
            (change_dir / "proposal.md").write_text(proposal, encoding="utf-8")
            (change_dir / "spec.md").write_text(spec, encoding="utf-8")
            reporter = validator.Reporter()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                validator.validate_api_spec_contract(change_dir, reporter)
        self.assertGreater(reporter.failed, 0)
        return output.getvalue()

    def test_contract_sections_preserve_all_duplicate_matches(self) -> None:
        text = "## API 规格定义\nfirst\n## API 规格定义\nsecond"
        self.assertEqual(["first", "second"], validator.section_texts(text, "API 规格定义"))
        self.assertEqual("", validator.section_text(text, "API 规格定义"))

    def test_contract_tables_preserve_all_duplicate_matches(self) -> None:
        text = """\
| 规格项 | 值 |
| --- | --- |
| 返回值 | ok |

| 规格项 | 值 |
| --- | --- |
| 返回值 | conflicting |
"""
        self.assertEqual(2, len(validator.tables_with_columns(text, ["规格项", "值"])))
        self.assertEqual([], validator.table_with_columns(text, ["规格项", "值"]))
        self.assertIsNone(validator.unique_table_with_columns(text, ["规格项", "值"]))

    def test_duplicate_top_level_api_section_is_rejected(self) -> None:
        proposal = """\
## 不涉及项确认

| 维度 | 是否涉及 |
| --- | --- |
| API/SDK | 是 |
"""
        spec = "## API 规格定义\nfirst\n## API 规格定义\nsecond"
        output = self.validate_api_documents(proposal, spec)
        self.assertIn("API 规格定义 section must appear exactly once", output)

    def test_duplicate_common_subsection_and_table_are_rejected(self) -> None:
        proposal = """\
## 不涉及项确认

| 维度 | 是否涉及 |
| --- | --- |
| API/SDK | 是 |
"""
        duplicate_subsection = """\
## API 规格定义
### 公共规格属性
first
### 公共规格属性
second
### 逐 API 规格
"""
        output = self.validate_api_documents(proposal, duplicate_subsection)
        self.assertIn("公共规格属性 subsection must appear exactly once", output)

        duplicate_table = """\
## API 规格定义
### 公共规格属性
| 规格项 | 值 |
| --- | --- |
| API 类型 | Public |

| 规格项 | 值 |
| --- | --- |
| API 类型 | System |
### 逐 API 规格
"""
        output = self.validate_api_documents(proposal, duplicate_table)
        self.assertIn("must contain exactly one specification table", output)

    def test_invalid_arkts_type_expressions_are_rejected(self) -> None:
        for value in (
            "string number",
            "Foo + Bar",
            "Foo-Bar",
            "Foo / Bar",
            "Foo * Bar",
            "Foo = Bar",
            "Foo: Bar",
            "Foo; Bar",
            "Foo => Bar",
            "Promise<(value: string) =>>",
            "(callback: (value: string) =>) => void",
            "{ cb: (value: string) => }",
        ):
            with self.subTest(value=value):
                self.assertFalse(validator._api_type_complete(value, language="ArkTS"))
        self.assertFalse(
            validator.api_signature_complete(
                "PaymentCallback.onSuccess(transactionId: string number): void",
                language="ArkTS",
            )
        )

    def test_valid_arkts_type_expressions_are_accepted(self) -> None:
        for value in (
            "Foo | Bar",
            "Promise<Record<string, number>>",
            "(value: string) => number",
            "readonly Foo[]",
            "keyof Foo",
            "T extends U ? X : Y",
            "(callback: (value: string) => number) => void",
            "Promise<(value: string) => number>",
            "T extends U ? X : V extends W ? Y : Z",
        ):
            with self.subTest(value=value):
                self.assertTrue(validator._api_type_complete(value, language="ArkTS"))

    def test_valid_c_type_specifier_combinations_are_accepted(self) -> None:
        for value in (
            "const char *",
            "unsigned long long",
            "struct PaymentResult *",
            "void (*)(const char *)",
            "int (*)(unsigned long, const char *)",
        ):
            with self.subTest(value=value):
                self.assertTrue(validator._api_type_complete(value, language="C"))

    def test_invalid_c_type_specifier_combinations_are_rejected(self) -> None:
        for value in (
            "signed unsigned int",
            "long float",
            "void int",
            "Foo Bar",
            "Foo | Bar",
            "Foo: Bar",
            "Foo.Bar",
            "Foo * Bar",
            "Foo, Bar",
            "Foo; Bar",
        ):
            with self.subTest(value=value):
                self.assertFalse(validator._api_type_complete(value, language="C"))

    def test_c_function_pointer_signature_is_accepted(self) -> None:
        self.assertTrue(
            validator.api_signature_complete(
                "OH_RegisterCallback(callback: void (*)(const char *)): int",
                name_style="free",
                language="C",
            )
        )

    def test_c_function_pointer_empty_parameter_is_rejected(self) -> None:
        for type_name in ("int (*)(int,,int)", "int (*)(void (*)(int,,int))"):
            with self.subTest(type=type_name):
                self.assertFalse(validator.api_signature_complete(
                    f"OH_call1(value: {type_name}): int", name_style="free", language="C"))

    def test_c_qualified_function_pointer_is_accepted(self) -> None:
        for type_name in ("void (* const)(const char *)", "void (* volatile)(const char *)"):
            with self.subTest(type=type_name):
                self.assertTrue(validator.api_signature_complete(
                    f"OH_call1(value: {type_name}): int", name_style="free", language="C"))

    def test_c_callback_named_parameters_are_accepted(self) -> None:
        for type_name in ("void (*)(int code)", "void (*)(const char *message)",
                          "void (*)(void (*cb)(int code))"):
            with self.subTest(type=type_name):
                self.assertTrue(validator.api_signature_complete(
                    f"OH_call1(value: {type_name}): int", name_style="free", language="C"))

    def test_arkts_callback_empty_parameters_are_rejected(self) -> None:
        for type_name in ("(value: string,, other: number) => void",
                          "Promise<(value: string,, other: number) => void>"):
            with self.subTest(type=type_name):
                self.assertFalse(validator.api_signature_complete(
                    f"Example.on(cb: {type_name}): void", language="ArkTS"))

    def test_arkts_callback_tuple_parameters_are_accepted(self) -> None:
        for type_name in ("(value: [string, number]) => void",
                          "Promise<(value: [string, number]) => void>", "(value: []) => void"):
            with self.subTest(type=type_name):
                self.assertTrue(validator.api_signature_complete(
                    f"Example.on(cb: {type_name}): void", language="ArkTS"))

    def test_supported_device_decisions_are_validated(self) -> None:
        valid = [{"设备类型": "手机", "起始版本": "6.0", "是否支持": "是"}]
        self.assertEqual([], validator.supported_device_table_issues(valid))
        invalid = [
            {"设备类型": "手机", "起始版本": "banana", "是否支持": "maybe"},
            {"设备类型": "手机", "起始版本": "6.0", "是否支持": "是"},
        ]
        issues = validator.supported_device_table_issues(invalid)
        self.assertTrue(any("must state 是 or 否" in issue for issue in issues))
        self.assertTrue(any("invalid starting version" in issue for issue in issues))
        self.assertTrue(any("duplicate supported device" in issue for issue in issues))

    def test_design_docs_commit_is_full_sha_and_matches_current_head(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            change_dir = Path(temporary) / "codespec" / "changes" / "arkui_ace_engine" / "123"
            change_dir.mkdir(parents=True)
            (change_dir / "proposal.md").write_text(
                "---\nreq: '123'\ntarget_release: '7.1'\n---\n",
                encoding="utf-8",
            )
            metadata = change_dir / "metadata_tracking.yaml"
            template = """\
req_id: "123"
target_release: "7.1"
repos:
  - repo: "openharmony/arkui_ace_engine"
    pull_requests:
      - url: "https://gitcode.com/openharmony/arkui_ace_engine/pulls/351"
        title: "Implement contract"
        state: "open"
        commit: "{commit}"
"""

            def validate(commit: str) -> tuple[int, str]:
                metadata.write_text(template.format(commit=commit), encoding="utf-8")
                reporter = validator.Reporter()
                output = io.StringIO()
                with (
                    mock.patch.object(
                        validator,
                        "repository_origin_url",
                        return_value="https://gitcode.com/openharmony/arkui_ace_engine.git",
                    ),
                    mock.patch.object(validator, "repository_head_commit", return_value="a" * 40),
                    contextlib.redirect_stdout(output),
                ):
                    validator.validate_metadata_tracking(change_dir, reporter, required=True)
                return reporter.failed, output.getvalue()

            failed, output = validate("deadbee")
            self.assertGreater(failed, 0)
            self.assertIn("full 40-digit hex SHA", output)

            failed, output = validate("b" * 40)
            self.assertGreater(failed, 0)
            self.assertIn("must match git rev-parse HEAD", output)

            failed, output = validate("a" * 40)
            self.assertEqual(0, failed, output)

    def test_duplicate_resource_proposal_section_is_rejected(self) -> None:
        templates = WORKFLOW_ROOT / "runtime" / "assets" / "templates" / "ai"
        contract = WORKFLOW_ROOT / "runtime" / "assets" / "contracts" / "artifacts.yaml"
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "templates"
            shutil.copytree(templates, copied)
            proposal = copied / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8")
                + "\n## 资源开销审视\n\n"
                + "| 维度 | 状态 | 信号/依据 | 确认人/理由/范围 |\n"
                + "| --- | --- | --- | --- |\n",
                encoding="utf-8",
            )
            issues = odk_yaml.validate_resource_templates(str(contract), str(copied))
        self.assertTrue(any("resource heading must appear exactly once" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
