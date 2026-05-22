#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 OpenHarmony 存量测试用例脚本

功能：
1. 分析指定目录下的测试用例文件
2. 提取命名规范、注释风格、测试模式
3. 关联宏与@tc注释
4. 输出"建议采用的本地风格"

使用方式：
    python analyze-existing-tests.py <test_directory> [--output report.md] [--encoding utf-8] [--verbose]

示例：
    python analyze-existing-tests.py //base/telephony/test --output telephony_test_report.md
    python analyze-existing-tests.py ./tests --verbose --encoding gbk
"""

import os
import re
import sys
import time
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional, DefaultDict, Any


def extract_test_body(content: str, start_pos: int) -> str:
    """从 start_pos 开始匹配完整的测试函数体（支持嵌套大括号）

    Args:
        content: 文件完整内容
        start_pos: 第一个 '{' 所在的位置

    Returns:
        从 start_pos 到匹配的 '}' 之间的完整字符串（含首尾大括号），
        如果不匹配则返回空字符串。
    """
    depth = 0
    i = start_pos
    while i < len(content):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                return content[start_pos : i + 1]
        i += 1
    return ""


class TestCaseInfo:
    """单个测试用例的信息"""

    def __init__(self):
        self.macro_type: str = ""
        self.test_suite: str = ""
        self.test_name: str = ""
        self.test_level: str = ""
        self.thread_count: Optional[int] = None
        self.tc_name: str = ""
        self.tc_desc: str = ""
        self.tc_type: str = ""
        self.tc_require: str = ""
        self.file_path: str = ""
        self.line_number: int = 0


class StyleRecommendation:
    """风格建议"""

    def __init__(self):
        self.macro_recommendation: str = ""
        self.level_recommendation: str = ""
        self.naming_recommendation: str = ""
        self.comment_recommendation: str = ""
        self.setup_teardown_recommendation: str = ""
        self.detected_patterns: Dict[str, Any] = {}


class TestAnalyzer:
    """测试用例分析器"""

    def __init__(self, encoding: str = "utf-8", verbose: bool = False) -> None:
        self.encoding = encoding
        self.verbose = verbose
        self.test_cases: List[TestCaseInfo] = []
        self.total_files: int = 0
        self.total_test_cases: int = 0
        self.test_macros: DefaultDict[str, int] = defaultdict(int)
        self.test_levels: DefaultDict[str, int] = defaultdict(int)
        self.tc_types: DefaultDict[str, int] = defaultdict(int)
        self.functions_tested: Set[str] = set()
        self.naming_patterns: Counter = Counter()
        self.comment_patterns: Counter = Counter()
        self.suite_names: Counter = Counter()
        self.level_formats: Counter = Counter()
        self.examples: Dict[str, List[str]] = {
            "hwtest": [],
            "hwtest_f": [],
            "hwmtest_f": [],
            "hwtest_p": [],
            "setup_teardown": [],
            "test_class": [],
        }

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[VERBOSE] {msg}")

    def analyze_file(self, filepath: str) -> None:
        try:
            with open(filepath, "r", encoding=self.encoding, errors="ignore") as f:
                content = f.read()
            self._log(f"Analyzing file: {filepath} ({len(content)} bytes)")
            self._extract_info(content, filepath)
            self.total_files += 1
        except UnicodeDecodeError as e:
            print(f"Encoding error reading {filepath} with {self.encoding}: {e}")
        except OSError as e:
            print(f"OS error reading {filepath}: {e}")
        except Exception as e:
            print(f"Unexpected error reading {filepath}: {e}")

    def _extract_info(self, content: str, filepath: str) -> None:
        self._extract_all_test_macros(content, filepath)
        self._extract_test_class(content)
        self._extract_setup_teardown(content)

    def _find_tc_comments_before(self, content: str, position: int) -> Dict[str, str]:
        """在指定位置之前查找 @tc 注释块"""
        tc_info = {
            "tc_name": "",
            "tc_desc": "",
            "tc_type": "",
            "tc_require": "",
        }

        search_start = max(0, position - 1000)
        search_content = content[search_start:position]

        comment_pattern = r"/\*\s*\n((?:\s*\*.*\n)+)\s*\*/"
        comment_match = re.search(comment_pattern, search_content, re.MULTILINE)

        if comment_match:
            comment_body = comment_match.group(1)

            tc_name_match = re.search(r"@tc\.name:\s*(.+)", comment_body)
            if tc_name_match:
                tc_info["tc_name"] = tc_name_match.group(1).strip()

            tc_desc_match = re.search(r"@tc\.desc:\s*(.+)", comment_body)
            if tc_desc_match:
                tc_info["tc_desc"] = tc_desc_match.group(1).strip()

            tc_type_match = re.search(r"@tc\.type:\s*(\w+)", comment_body)
            if tc_type_match:
                tc_info["tc_type"] = tc_type_match.group(1).strip()

            tc_require_match = re.search(r"@tc\.require:\s*(.+)", comment_body)
            if tc_require_match:
                tc_info["tc_require"] = tc_require_match.group(1).strip()

        return tc_info

    def _extract_all_test_macros(self, content: str, filepath: str) -> None:
        """提取所有测试宏调用，并关联 @tc 注释"""
        param_pattern = r"(\w+(?:\.\w+)?)"

        macro_patterns: Dict[str, str] = {
            "HWTEST": r"HWTEST\s*\(\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*\)",
            "HWTEST_F": r"HWTEST_F\s*\(\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*\)",
            "HWMTEST_F": r"HWMTEST_F\s*\(\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*,\s*(\d+)\s*\)",
            "HWTEST_P": r"HWTEST_P\s*\(\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*,\s*"
            + param_pattern
            + r"\s*\)",
        }

        for macro_type, pattern in macro_patterns.items():
            for match in re.finditer(pattern, content):
                tc_info = TestCaseInfo()
                tc_info.macro_type = macro_type
                tc_info.file_path = filepath

                line_num = content[: match.start()].count("\n") + 1
                tc_info.line_number = line_num

                groups = match.groups()

                if macro_type == "HWMTEST_F":
                    tc_info.test_suite = groups[0]
                    tc_info.test_name = groups[1]
                    tc_info.test_level = self._normalize_level(groups[2])
                    tc_info.thread_count = int(groups[3])
                    original_level = groups[2]
                else:
                    tc_info.test_suite = groups[0]
                    tc_info.test_name = groups[1]
                    tc_info.test_level = self._normalize_level(groups[2])
                    original_level = groups[2]

                tc_comments = self._find_tc_comments_before(content, match.start())
                tc_info.tc_name = tc_comments["tc_name"]
                tc_info.tc_desc = tc_comments["tc_desc"]
                tc_info.tc_type = tc_comments["tc_type"]
                tc_info.tc_require = tc_comments["tc_require"]

                self.test_cases.append(tc_info)

                self.test_macros[macro_type] += 1
                self.total_test_cases += 1
                self.test_levels[tc_info.test_level] += 1
                self.suite_names[tc_info.test_suite] += 1
                self.naming_patterns[tc_info.test_name] += 1

                if tc_info.tc_type:
                    self.tc_types[tc_info.tc_type] += 1

                if tc_info.tc_require:
                    self.comment_patterns[tc_info.tc_require] += 1

                self.level_formats[original_level] += 1

                func_match = re.match(r"(\w+)_\d{3}", tc_info.test_name)
                if func_match:
                    self.functions_tested.add(func_match.group(1))

                self._log(
                    f"  Found {macro_type}({tc_info.test_suite}, {tc_info.test_name}, {tc_info.test_level}) at line {line_num}"
                )

    def _normalize_level(self, level_str: str) -> str:
        """标准化测试等级字符串"""
        if level_str.startswith("TestSize."):
            return level_str.split(".")[-1]
        return level_str

    def _extract_test_class(self, content: str) -> None:
        """提取测试类定义"""
        class_pattern = r"class\s+(\w+)\s*:\s*public\s+testing::Test\s*\{"
        matches = re.findall(class_pattern, content)
        for class_name in matches:
            self._log(f"  Found test class: {class_name}")

        class_match = re.search(
            r"class\s+\w+\s*:\s*public\s+testing::Test\s*\{[^}]*public:[^}]*\}", content
        )
        if class_match:
            self.examples["test_class"].append(class_match.group(0)[:300])

    def _extract_setup_teardown(self, content: str) -> None:
        """提取 SetUp/TearDown 示例"""
        setup_patterns = [
            r"void\s+\w+::SetUpTestCase\(\)\s*\{",
            r"void\s+\w+::SetUp\(\)\s*\{",
            r"static\s+void\s+SetUpTestCase\(\)\s*;",
        ]

        for pattern in setup_patterns:
            setup_match = re.search(pattern, content)
            if setup_match:
                brace_pos = setup_match.end() - 1
                body = extract_test_body(content, brace_pos)
                if body:
                    full_setup = (
                        content[setup_match.start() : setup_match.end() - 1] + body
                    )
                    self.examples["setup_teardown"].append(full_setup[:200])
                    self._log(f"  Extracted SetUp example ({len(full_setup)} chars)")
                    break

        teardown_patterns = [
            r"void\s+\w+::TearDownTestCase\(\)\s*\{",
            r"void\s+\w+::TearDown\(\)\s*\{",
        ]

        for pattern in teardown_patterns:
            teardown_match = re.search(pattern, content)
            if teardown_match:
                brace_pos = teardown_match.end() - 1
                body = extract_test_body(content, brace_pos)
                if body:
                    full_teardown = (
                        content[teardown_match.start() : teardown_match.end() - 1]
                        + body
                    )
                    self.examples["setup_teardown"].append(full_teardown[:200])
                    self._log(
                        f"  Extracted TearDown example ({len(full_teardown)} chars)"
                    )
                    break

    def _generate_style_recommendation(self) -> StyleRecommendation:
        """根据分析结果生成风格建议"""
        recommendation = StyleRecommendation()

        if self.test_macros:
            most_common_macro = max(self.test_macros.items(), key=lambda x: x[1])
            total_macros = sum(self.test_macros.values())
            percentage = (
                (most_common_macro[1] / total_macros * 100) if total_macros > 0 else 0
            )

            if most_common_macro[0] == "HWTEST_F":
                recommendation.macro_recommendation = (
                    f"**推荐使用 HWTEST_F**（占比 {percentage:.1f}%）：\n"
                    f"本地代码库主要使用 HWTEST_F，适合需要 SetUp/TearDown 的测试场景。\n"
                    f"如果测试不需要初始化/清理，可使用 HWTEST。"
                )
            elif most_common_macro[0] == "HWTEST":
                recommendation.macro_recommendation = (
                    f"**推荐使用 HWTEST**（占比 {percentage:.1f}%）：\n"
                    f"本地代码库主要使用 HWTEST，适合简单独立的测试场景。"
                )
            else:
                recommendation.macro_recommendation = (
                    f"**推荐使用 {most_common_macro[0]}**（占比 {percentage:.1f}%）"
                )

            recommendation.detected_patterns["macro_distribution"] = dict(
                self.test_macros
            )

        if self.test_levels:
            most_used_levels = sorted(self.test_levels.items(), key=lambda x: -x[1])[:2]

            recommendation.level_recommendation = (
                f"**推荐测试等级**：\n"
                f"本地最常用等级：{', '.join([l[0] for l in most_used_levels])}\n"
                f"- Level1：基础功能测试（占比最高）\n"
                f"- Level2：异常处理、边界条件\n"
                f"- Level0：冒烟测试（门禁）\n"
                f"建议：新功能正常场景用 Level1，异常/边界场景用 Level2。"
            )

            testsize_count = sum(
                v for k, v in self.level_formats.items() if k.startswith("TestSize.")
            )
            plain_count = sum(
                v
                for k, v in self.level_formats.items()
                if not k.startswith("TestSize.")
            )
            if testsize_count > plain_count:
                recommendation.level_recommendation += f"\n\n**等级格式**：推荐使用完整格式 `TestSize.Level1`（{testsize_count} 次）。"
            else:
                recommendation.level_recommendation += (
                    f"\n\n**等级格式**：推荐使用简化格式 `Level1`（{plain_count} 次）。"
                )

        if self.naming_patterns:
            valid_patterns = [
                p for p in self.naming_patterns.keys() if re.match(r"\w+_\d{3}", p)
            ]
            invalid_patterns = [
                p for p in self.naming_patterns.keys() if not re.match(r"\w+_\d{3}", p)
            ]

            valid_ratio = (
                len(valid_patterns) / len(self.naming_patterns) * 100
                if self.naming_patterns
                else 0
            )

            recommendation.naming_recommendation = (
                f"**命名规范建议**：\n"
                f"- 符合规范：{len(valid_patterns)} 个（{valid_ratio:.1f}%）\n"
                f"- 不符合规范：{len(invalid_patterns)} 个\n"
                f"- **推荐格式**：`TestSuite_FunctionName_001`\n"
                f"- 序号使用3位数字（001-999）\n"
                f"- 使用 CamelCase 风格"
            )

            if invalid_patterns:
                invalid_list = list(invalid_patterns)[:3]
                recommendation.naming_recommendation += (
                    f"\n\n**不合规示例**：`{', '.join(invalid_list)}`"
                )

        if self.tc_types:
            most_common_type = max(self.tc_types.items(), key=lambda x: x[1])
            recommendation.comment_recommendation = (
                f"**注释风格建议**：\n"
                f"- @tc.type 最常用：{most_common_type[0]}（{most_common_type[1]} 次）\n"
                f"- **推荐注释格式**：\n"
                f"```\n"
                f"/*\n"
                f" * @tc.name: TestSuite_FunctionName_001\n"
                f" * @tc.desc: 验证xxx功能xxx场景\n"
                f" * @tc.type: FUNC\n"
                f" * @tc.require: issueIxxxxx\n"
                f" */\n"
                f"```\n"
            )

        if self.examples["setup_teardown"]:
            recommendation.setup_teardown_recommendation = (
                f"**SetUp/TearDown 建议**：\n"
                f"本地代码库使用 SetUp/TearDown 模式。\n"
                f"- SetUp()：每个测试前初始化\n"
                f"- TearDown()：每个测试后清理\n"
                f"- SetUpTestCase()：所有测试前一次性初始化\n"
                f"- TearDownTestCase()：所有测试后一次性清理"
            )

        return recommendation

    def analyze_directory(self, directory: str) -> None:
        """分析目录下所有测试文件"""
        directory = os.path.normpath(directory)

        if not os.path.exists(directory):
            print(f"Error: Directory does not exist: {directory}")
            sys.exit(1)

        if not os.path.isdir(directory):
            print(f"Error: Path is not a directory: {directory}")
            sys.exit(1)

        test_suffixes: Tuple[str, ...] = ("Test.cpp", "_test.cpp", "test.cpp")

        file_count = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(test_suffixes):
                    filepath = os.path.join(root, file)
                    self.analyze_file(filepath)
                    file_count += 1

        if file_count == 0:
            print(f"Warning: No test files found in directory: {directory}")
            print(f"  (Looking for files matching *Test.cpp, *_test.cpp, or *test.cpp)")

        self._log(f"Total files processed: {file_count}")

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """生成分析报告"""
        report = self._build_report()

        if output_path:
            output_path = os.path.normpath(output_path)
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                self._log(f"Created output directory: {output_dir}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report saved to: {output_path}")
        else:
            print(report)

        return report

    def _build_report(self) -> str:
        """构建报告内容"""
        recommendation = self._generate_style_recommendation()

        lines: List[str] = [
            "# OpenHarmony 测试用例分析报告",
            "",
            "## 统计概览",
            "",
            f"- 分析文件数: {self.total_files}",
            f"- 测试用例总数: {self.total_test_cases}",
            f"- 被测函数数: {len(self.functions_tested)}",
            f"- 测试套/类数: {len(self.suite_names)}",
            "",
            "---",
            "",
            "# 本地风格建议",
            "",
            "根据存量代码分析，建议新编写的测试用例遵循以下风格：",
            "",
        ]

        if recommendation.macro_recommendation:
            lines.extend(
                [
                    "## 1. 测试宏选择",
                    "",
                    recommendation.macro_recommendation,
                    "",
                ]
            )

        if recommendation.level_recommendation:
            lines.extend(
                [
                    "## 2. 测试等级设置",
                    "",
                    recommendation.level_recommendation,
                    "",
                ]
            )

        if recommendation.naming_recommendation:
            lines.extend(
                [
                    "## 3. 命名规范",
                    "",
                    recommendation.naming_recommendation,
                    "",
                ]
            )

        if recommendation.comment_recommendation:
            lines.extend(
                [
                    "## 4. 注释风格",
                    "",
                    recommendation.comment_recommendation,
                    "",
                ]
            )

        if recommendation.setup_teardown_recommendation:
            lines.extend(
                [
                    "## 5. SetUp/TearDown 模式",
                    "",
                    recommendation.setup_teardown_recommendation,
                    "",
                ]
            )

        lines.extend(
            [
                "---",
                "",
                "# 详细统计",
                "",
                "## 测试宏使用分布",
                "",
            ]
        )

        for macro, count in sorted(self.test_macros.items()):
            percentage = (
                (count / self.total_test_cases * 100)
                if self.total_test_cases > 0
                else 0
            )
            lines.append(f"- {macro}: {count} ({percentage:.1f}%)")

        lines.extend(
            [
                "",
                "## 测试等级分布",
                "",
            ]
        )

        for level in ["Level0", "Level1", "Level2", "Level3", "Level4"]:
            count = self.test_levels.get(level, 0)
            if count > 0:
                percentage = (
                    (count / self.total_test_cases * 100)
                    if self.total_test_cases > 0
                    else 0
                )
                lines.append(f"- {level}: {count} ({percentage:.1f}%)")

        lines.extend(
            [
                "",
                "## 测试等级格式分布",
                "",
                "（记录原始格式，未标准化）",
                "",
            ]
        )

        for format_str, count in sorted(self.level_formats.items()):
            lines.append(f"- `{format_str}`: {count}")

        lines.extend(
            [
                "",
                "## 测试类型分布 (@tc.type)",
                "",
            ]
        )

        for tc_type, count in sorted(self.tc_types.items()):
            lines.append(f"- {tc_type}: {count}")

        lines.extend(
            [
                "",
                "## 测试套/类分布",
                "",
            ]
        )

        top_suites = sorted(self.suite_names.items(), key=lambda x: -x[1])[:10]
        for suite, count in top_suites:
            lines.append(f"- {suite}: {count}")

        if len(self.suite_names) > 10:
            lines.append(f"- ... 还有 {len(self.suite_names) - 10} 个")

        lines.extend(
            [
                "",
                "## 常见命名模式",
                "",
            ]
        )

        top_names = sorted(self.naming_patterns.items(), key=lambda x: -x[1])[:10]
        for name, count in top_names:
            lines.append(f"- `{name}`: {count} 次")

        lines.extend(
            [
                "",
                "## @tc.require 常见格式",
                "",
            ]
        )

        top_requires = sorted(self.comment_patterns.items(), key=lambda x: -x[1])[:10]
        for req, count in top_requires:
            lines.append(f"- `{req}`: {count} 次")

        lines.extend(
            [
                "",
                "## 被测函数列表",
                "",
            ]
        )

        for func in sorted(self.functions_tested)[:20]:
            lines.append(f"- {func}")

        if len(self.functions_tested) > 20:
            lines.append(f"- ... 还有 {len(self.functions_tested) - 20} 个函数")

        if self.examples["test_class"]:
            lines.extend(
                [
                    "",
                    "## 测试类定义示例",
                    "",
                    "```cpp",
                    self.examples["test_class"][0],
                    "```",
                ]
            )

        if self.examples["setup_teardown"]:
            lines.extend(
                [
                    "",
                    "## SetUp/TearDown 示例",
                    "",
                    "```cpp",
                ]
            )
            for example in self.examples["setup_teardown"][:3]:
                lines.append(example)
            lines.append("```")

        typical_cases = [tc for tc in self.test_cases if tc.tc_name and tc.tc_desc][:3]
        if typical_cases:
            lines.extend(
                [
                    "",
                    "## 典型测试用例示例（含注释）",
                    "",
                ]
            )
            for tc in typical_cases:
                lines.extend(
                    [
                        f"**{tc.macro_type}({tc.test_suite}, {tc.test_name}, {tc.test_level})**",
                        "",
                        f"@tc.name: {tc.tc_name}",
                        f"@tc.desc: {tc.tc_desc}",
                        f"@tc.type: {tc.tc_type}",
                        f"@tc.require: {tc.tc_require}",
                        f"文件: `{os.path.basename(tc.file_path)}` 行 {tc.line_number}",
                        "",
                    ]
                )

        return "\n".join(lines)


def main() -> None:
    """脚本入口函数"""
    parser = argparse.ArgumentParser(
        description="分析 OpenHarmony 存量测试用例，输出本地风格建议"
    )
    parser.add_argument("directory", help="测试用例目录路径")
    parser.add_argument("--output", "-o", help="输出报告文件路径（可选）")
    parser.add_argument(
        "--encoding", "-e", default="utf-8", help="文件读取编码（默认: utf-8）"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", default=False, help="输出详细调试信息"
    )

    args = parser.parse_args()

    start_time = time.time()

    analyzer = TestAnalyzer(encoding=args.encoding, verbose=args.verbose)
    analyzer.analyze_directory(args.directory)
    analyzer.generate_report(args.output)

    elapsed = time.time() - start_time

    print(f"")
    print(f"--- 分析统计 ---")
    print(f"总文件数: {analyzer.total_files}")
    print(f"总用例数: {analyzer.total_test_cases}")
    print(f"分析耗时: {elapsed:.2f} 秒")


if __name__ == "__main__":
    main()
