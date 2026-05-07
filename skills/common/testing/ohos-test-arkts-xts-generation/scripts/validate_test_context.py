#!/usr/bin/env python3
"""
测试文件生成上下文检查工具

自动执行 Phase 7 步骤 A 中的可编程检查项：
  A.1 Apache 2.0 许可证头
  A.2 @ohos/hypium 导入
  A.3 被测模块导入
  A.7 禁止 as any
  A.8 设计文档一致性（每个 @tc.number 有对应条目）

用法：
    python scripts/validate_test_context.py \\
        --file path/to/TestFile.test.ets \\
        --expected-module "@ohos.multimedia.media" \\
        --design-doc path/to/TestFile.test.design.md
"""

import argparse
import json
import os
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ISSUES = []


def issue(check_id, severity, message, line=None):
    ISSUES.append({
        'check': check_id,
        'severity': severity,
        'message': message,
        'line': line
    })


def check_license_header(lines):
    text = '\n'.join(lines[:15])
    if 'Apache License' not in text or 'Version 2.0' not in text:
        issue('A.1', 'error', 'Missing Apache 2.0 license header in file top 15 lines')
        return False
    if 'Copyright' not in text:
        issue('A.1', 'warning', 'Copyright line missing or incomplete in license header')
    print('  [PASS] A.1 License header')
    return True


def check_hypium_import(lines):
    hypium_pattern = re.compile(r"import\s*\{[^}]*}\s*from\s*['\"]@ohos/hypium['\"]")
    found = False
    for i, line in enumerate(lines, 1):
        if hypium_pattern.search(line):
            found = True
            symbols = re.search(r'\{([^}]*)\}', line)
            if symbols:
                syms = [s.strip() for s in symbols.group(1).split(',') if s.strip()]
                required = {'describe', 'it', 'expect'}
                missing = required - set(syms)
                if missing:
                    issue('A.2', 'warning', f'Commonly needed symbols not imported: {missing}', line=i)
            break

    if not found:
        issue('A.2', 'error', "Missing import from '@ohos/hypium'")
        return False

    print('  [PASS] A.2 hypium import')
    return True


def check_module_import(lines, expected_module):
    if not expected_module:
        print('  [SKIP] A.3 Module import check (no --expected-module specified)')
        return True

    pattern = re.compile(
        r"import\s*.*\s*from\s*['\"]" + re.escape(expected_module) + r"['\"]"
    )
    for i, line in enumerate(lines, 1):
        if pattern.search(line):
            print(f'  [PASS] A.3 Module import ({expected_module})')
            return True

    relaxed = expected_module.replace('@ohos.', '').replace('@kit.', '')
    for i, line in enumerate(lines, 1):
        if relaxed in line and 'import' in line:
            print(f'  [PASS] A.3 Module import (relaxed match at line {i})')
            return True

    issue('A.3', 'error', f"Missing import for expected module: '{expected_module}'")
    return False


def check_no_as_any(lines):
    pattern = re.compile(r'\bas\s+any\b')
    found_issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*'):
            continue
        if pattern.search(line):
            found_issues.append(i)

    if found_issues:
        for ln in found_issues:
            issue('A.7', 'error', f"'as any' found at line {ln}: {lines[ln-1].strip()}", line=ln)
        return False

    print('  [PASS] A.7 No as any')
    return True


def check_design_doc_consistency(lines, design_doc_path):
    tc_numbers = []
    tc_pattern = re.compile(r'@tc\.number\s+(\S+)')
    for i, line in enumerate(lines, 1):
        m = tc_pattern.search(line)
        if m:
            tc_numbers.append((m.group(1), i))

    if not tc_numbers:
        issue('A.8', 'warning', 'No @tc.number annotations found in test file')
        return True

    if not design_doc_path or not os.path.exists(design_doc_path):
        print(f'  [SKIP] A.8 Design doc check (no --design-doc or file not found)')
        return True

    with open(design_doc_path, 'r', encoding='utf-8') as f:
        design_content = f.read()

    missing = []
    for tc_num, line_num in tc_numbers:
        if tc_num not in design_content:
            missing.append((tc_num, line_num))

    if missing:
        for tc_num, line_num in missing:
            issue('A.8', 'error', f'@tc.number {tc_num} (line {line_num}) not found in design doc', line=line_num)
        return False

    print(f'  [PASS] A.8 Design doc consistency ({len(tc_numbers)} test cases verified)')
    return True


def main():
    parser = argparse.ArgumentParser(description='Validate test file generation context')
    parser.add_argument('--file', required=True, help='Path to the test file (.ets)')
    parser.add_argument('--expected-module', default=None,
                        help='Expected module import (e.g. @ohos.multimedia.media)')
    parser.add_argument('--design-doc', default=None,
                        help='Path to the design doc (.design.md) for A.8 check')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'[ERROR] File not found: {args.file}')
        return 1

    with open(args.file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f'[CHECK] {args.file} ({len(lines)} lines)')

    all_pass = True
    all_pass &= check_license_header(lines)
    all_pass &= check_hypium_import(lines)
    all_pass &= check_module_import(lines, args.expected_module)
    all_pass &= check_no_as_any(lines)
    all_pass &= check_design_doc_consistency(lines, args.design_doc)

    print()

    if ISSUES:
        print(f'[ISSUES] {len(ISSUES)} issue(s) found:')
        for iss in ISSUES:
            line_info = f" (line {iss['line']})" if iss['line'] else ''
            print(f"  [{iss['severity'].upper()}] {iss['check']}: {iss['message']}{line_info}")

        report_path = os.path.join(os.path.dirname(args.file), 'validate_context_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({'file': args.file, 'issues': ISSUES, 'total': len(ISSUES)}, f, indent=2, ensure_ascii=False)
        print(f'\n  Report saved to: {report_path}')
        return 1
    else:
        print('[PASS] All checks passed')
        return 0


if __name__ == '__main__':
    sys.exit(main())
