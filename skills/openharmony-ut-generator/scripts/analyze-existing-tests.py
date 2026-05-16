#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 OpenHarmony 存量测试用例脚本

功能：
1. 分析指定目录下的测试用例文件
2. 提取命名规范、注释风格、测试模式
3. 输出统计报告供 Skill 学习参考

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
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional, DefaultDict


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
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[start_pos:i + 1]
        i += 1
    return ""


class TestAnalyzer:
    """测试用例分析器

    分析 OpenHarmony 测试目录中的 C++ 测试文件，提取测试宏使用情况、
    测试等级、命名规范、注释风格等信息，并生成 Markdown 格式的统计报告。
    """

    def __init__(self, encoding: str = 'utf-8', verbose: bool = False) -> None:
        """初始化分析器

        Args:
            encoding: 文件读取编码，默认 utf-8
            verbose: 是否输出详细调试信息
        """
        self.encoding = encoding
        self.verbose = verbose
        self.stats: Dict[str, object] = {
            'total_files': 0,
            'total_test_cases': 0,
            'test_macros': defaultdict(int),
            'test_levels': defaultdict(int),
            'tc_types': defaultdict(int),
            'functions_tested': set(),
            'naming_patterns': [],
            'comment_patterns': [],
        }
        self.examples: Dict[str, List[str]] = {
            'hwtest': [],
            'hwtest_f': [],
            'hwmtest_f': [],
            'setup_teardown': [],
        }

    def _log(self, msg: str) -> None:
        """仅在 verbose 模式下打印调试信息"""
        if self.verbose:
            print(f"[VERBOSE] {msg}")

    def analyze_file(self, filepath: str) -> None:
        """分析单个测试文件

        Args:
            filepath: 测试文件路径
        """
        try:
            with open(filepath, 'r', encoding=self.encoding, errors='ignore') as f:
                content = f.read()
            self._log(f"Analyzing file: {filepath} ({len(content)} bytes)")
            self._extract_info(content, filepath)
            self.stats['total_files'] += 1
        except UnicodeDecodeError as e:
            print(f"Encoding error reading {filepath} with {self.encoding}: {e}")
        except OSError as e:
            print(f"OS error reading {filepath}: {e}")
        except Exception as e:
            print(f"Unexpected error reading {filepath}: {e}")

    def _extract_info(self, content: str, filepath: str) -> None:
        """从文件内容提取信息

        Args:
            content: 文件内容字符串
            filepath: 文件路径（用于调试）
        """
        self._extract_test_macros(content)
        self._extract_tc_comments(content)
        self._extract_test_levels(content)
        self._extract_test_functions(content)
        self._extract_examples(content)

    def _extract_test_macros(self, content: str) -> None:
        """提取测试宏使用情况

        识别 HWTEST、HWTEST_F、HWMTEST_F、HWTEST_P 等宏调用。
        """
        patterns: Dict[str, str] = {
            'HWTEST': r'HWTEST\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)',
            'HWTEST_F': r'HWTEST_F\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)',
            'HWMTEST_F': r'HWMTEST_F\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*,\s*(\d+)',
            'HWTEST_P': r'HWTEST_P\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)',
        }

        for macro, pattern in patterns.items():
            matches = re.findall(pattern, content)
            count = len(matches)
            self.stats['test_macros'][macro] += count
            self.stats['total_test_cases'] += count
            if count > 0:
                self._log(f"  Found {count} {macro} macro(s)")

    def _extract_tc_comments(self, content: str) -> None:
        """提取 @tc 注释"""
        tc_type_pattern = r'@tc\.type:\s*(\w+)'
        tc_types = re.findall(tc_type_pattern, content)
        for tc_type in tc_types:
            self.stats['tc_types'][tc_type] += 1

        tc_require_pattern = r'@tc\.require:\s*(\S+)'
        tc_requires = re.findall(tc_require_pattern, content)
        self.stats['comment_patterns'].extend(tc_requires[:5])  # 保存前5个示例

    def _extract_test_levels(self, content: str) -> None:
        """提取测试等级"""
        level_pattern = r'TestSize\.Level(\d)'
        levels = re.findall(level_pattern, content)
        for level in levels:
            self.stats['test_levels'][f'Level{level}'] += 1

    def _extract_test_functions(self, content: str) -> None:
        """提取测试函数名"""
        pattern = r'HWTEST_F\s*\(\s*\w+\s*,\s*(\w+)\s*,'
        names = re.findall(pattern, content)

        for name in names:
            func_match = re.match(r'(\w+)_\d{3}', name)
            if func_match:
                self.stats['functions_tested'].add(func_match.group(1))
            self.stats['naming_patterns'].append(name)

    def _extract_examples(self, content: str) -> None:
        """提取示例代码片段

        使用大括号计数法提取包含嵌套结构的完整测试函数体，
        解决正则 [^}]+ 无法匹配嵌套 if/for/while 大括号的问题。
        """
        # 提取 HWTEST_F 示例（包含 @tc 注释的完整测试）
        # 第一步：用正则匹配注释 + 宏签名部分（不含函数体）
        example_header_pattern = (
            r'/\*\s*\n'                          # /* 换行
            r'\s*\*\s*@tc\.name:[^\n]+\n'        # @tc.name 行
            r'\s*\*\s*@tc\.desc:[^\n]+\n'        # @tc.desc 行
            r'\s*\*\s*@tc\.type:[^\n]+\n'        # @tc.type 行
            r'\s*\*\s*@tc\.require:[^\n]+\n'     # @tc.require 行
            r'\s*\*/\s*\n'                       # */ 结束注释
            r'(HWTEST_F\s*\([^)]*\)\s*\{)'       # 宏签名直到第一个 {
        )
        header_match = re.search(example_header_pattern, content, re.MULTILINE)
        if header_match:
            brace_pos = header_match.end() - 1  # 最后一个字符是 '{'
            body = extract_test_body(content, brace_pos)
            if body:
                full_example = content[header_match.start():header_match.end() - 1] + body
                self.examples['hwtest_f'].append(full_example[:500])  # 保存前500字符
                self._log(f"  Extracted HWTEST_F example ({len(full_example)} chars)")

        # 提取 SetUp/TearDown 示例（同样使用大括号计数法）
        setup_pattern = r'void\s+\w+::SetUp\(\)\s*\{'
        setup_header_match = re.search(setup_pattern, content)
        if setup_header_match:
            brace_pos = setup_header_match.end() - 1  # '{' 的位置
            body = extract_test_body(content, brace_pos)
            if body:
                full_setup = content[setup_header_match.start():setup_header_match.end() - 1] + body
                self.examples['setup_teardown'].append(full_setup)
                self._log(f"  Extracted SetUp example ({len(full_setup)} chars)")

        # 同样处理 TearDown
        teardown_pattern = r'void\s+\w+::TearDown\(\)\s*\{'
        teardown_header_match = re.search(teardown_pattern, content)
        if teardown_header_match:
            brace_pos = teardown_header_match.end() - 1
            body = extract_test_body(content, brace_pos)
            if body:
                full_teardown = content[teardown_header_match.start():teardown_header_match.end() - 1] + body
                self.examples['setup_teardown'].append(full_teardown)
                self._log(f"  Extracted TearDown example ({len(full_teardown)} chars)")

    def analyze_directory(self, directory: str) -> None:
        """分析目录下所有测试文件

        Args:
            directory: 测试用例目录路径

        Raises:
            SystemExit: 目录不存在时退出
        """
        directory = os.path.normpath(directory)

        if not os.path.exists(directory):
            print(f"Error: Directory does not exist: {directory}")
            sys.exit(1)

        if not os.path.isdir(directory):
            print(f"Error: Path is not a directory: {directory}")
            sys.exit(1)

        # 匹配测试文件的扩展名
        test_suffixes: Tuple[str, ...] = ('Test.cpp', '_test.cpp')

        file_count = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(test_suffixes):
                    filepath = os.path.join(root, file)
                    self.analyze_file(filepath)
                    file_count += 1

        if file_count == 0:
            print(f"Warning: No test files found in directory: {directory}")
            print(f"  (Looking for files matching *Test.cpp or *_test.cpp)")

        self._log(f"Total files processed: {file_count}")

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """生成分析报告

        Args:
            output_path: 报告输出文件路径，为 None 时仅打印到终端

        Returns:
            生成的报告内容字符串
        """
        report = self._build_report()

        if output_path:
            output_path = os.path.normpath(output_path)
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                self._log(f"Created output directory: {output_dir}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {output_path}")
        else:
            print(report)

        return report

    def _build_report(self) -> str:
        """构建报告内容

        Returns:
            Markdown 格式的报告字符串
        """
        lines: List[str] = [
            "# OpenHarmony 测试用例分析报告",
            "",
            "## 统计概览",
            "",
            f"- 分析文件数: {self.stats['total_files']}",
            f"- 测试用例总数: {self.stats['total_test_cases']}",
            f"- 被测函数数: {len(self.stats['functions_tested'])}",
            "",
            "## 测试宏使用分布",
            "",
        ]

        for macro, count in sorted(self.stats['test_macros'].items()):
            lines.append(f"- {macro}: {count}")

        lines.extend([
            "",
            "## 测试等级分布",
            "",
        ])

        for level, count in sorted(self.stats['test_levels'].items()):
            lines.append(f"- {level}: {count}")

        lines.extend([
            "",
            "## 测试类型分布",
            "",
        ])

        for tc_type, count in sorted(self.stats['tc_types'].items()):
            lines.append(f"- {tc_type}: {count}")

        lines.extend([
            "",
            "## 被测函数列表",
            "",
        ])

        for func in sorted(self.stats['functions_tested'])[:20]:  # 只显示前20个
            lines.append(f"- {func}")

        if len(self.stats['functions_tested']) > 20:
            lines.append(f"- ... 还有 {len(self.stats['functions_tested']) - 20} 个函数")

        lines.extend([
            "",
            "## 命名规范示例",
            "",
        ])

        # 分析命名模式
        naming_patterns = self.stats['naming_patterns'][:10]
        for pattern in naming_patterns:
            lines.append(f"- `{pattern}`")

        # 检查命名规范
        valid_patterns = [p for p in self.stats['naming_patterns'] if re.match(r'\w+_\d{3}', p)]
        invalid_patterns = [p for p in self.stats['naming_patterns'] if not re.match(r'\w+_\d{3}', p)]

        lines.extend([
            "",
            "## 命名规范统计",
            "",
            f"- 符合规范: {len(valid_patterns)}",
            f"- 不符合规范: {len(invalid_patterns)}",
        ])

        if invalid_patterns:
            lines.append("")
            lines.append("### 不符合规范的示例")
            lines.append("")
            for pattern in invalid_patterns[:5]:
                lines.append(f"- `{pattern}`")

        lines.extend([
            "",
            "## @tc.require 格式示例",
            "",
        ])

        for req in self.stats['comment_patterns'][:10]:
            lines.append(f"- `{req}`")

        # 添加示例代码
        if self.examples['hwtest_f']:
            lines.extend([
                "",
                "## 测试用例示例",
                "",
                "```cpp",
                self.examples['hwtest_f'][0][:300],
                "```",
            ])

        if self.examples['setup_teardown']:
            lines.extend([
                "",
                "## SetUp/TearDown 示例",
                "",
                "```cpp",
            ])
            for example in self.examples['setup_teardown'][:2]:
                lines.append(example)
            lines.append("```")

        return '\n'.join(lines)


def main() -> None:
    """脚本入口函数"""
    parser = argparse.ArgumentParser(
        description='分析 OpenHarmony 存量测试用例'
    )
    parser.add_argument(
        'directory',
        help='测试用例目录路径'
    )
    parser.add_argument(
        '--output', '-o',
        help='输出报告文件路径（可选）'
    )
    parser.add_argument(
        '--encoding', '-e',
        default='utf-8',
        help='文件读取编码（默认: utf-8）'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        help='输出详细调试信息'
    )

    args = parser.parse_args()

    start_time = time.time()

    analyzer = TestAnalyzer(encoding=args.encoding, verbose=args.verbose)
    analyzer.analyze_directory(args.directory)
    analyzer.generate_report(args.output)

    elapsed = time.time() - start_time
    total_files = analyzer.stats['total_files']
    total_cases = analyzer.stats['total_test_cases']

    print(f"")
    print(f"--- 分析统计 ---")
    print(f"总文件数: {total_files}")
    print(f"总用例数: {total_cases}")
    print(f"分析耗时: {elapsed:.2f} 秒")


if __name__ == '__main__':
    main()
