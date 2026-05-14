#!/usr/bin/env python3
"""
规则G: BUILD.gn ohos_fuzztest目标名格式
检查BUILD.gn中ohos_fuzztest目标名是否符合规范
"""

import re


def check_fuzztest_target_name_format(target_name):
    """
    检查 ohos_fuzztest 目标名是否符合 XxxXxxFuzzTest 格式
    - 必须以 FuzzTest 结尾（可跟数字，如 FuzzTest1, FuzzTest2）
    - 必须是驼峰式命名（不含下划线）
    """
    # 匹配模式: XxxXxxFuzzTest 或 XxxXxxFuzzTest1, XxxXxxFuzzTest2 等
    if not re.match(r"^[A-Z][A-Za-z0-9]*FuzzTest\d*$", target_name):
        if not target_name.endswith("FuzzTest") and not re.search(
            r"FuzzTest\d+$", target_name
        ):
            return False, f"目标名 '{target_name}' 不以 'FuzzTest' 结尾"
        if "_" in target_name:
            return False, f"目标名 '{target_name}' 包含下划线，应为驼峰式命名"
        if not target_name[0].isupper():
            return False, f"目标名 '{target_name}' 首字母应大写"
        return False, f"目标名 '{target_name}' 格式不正确"

    return True, None


def check_build_gn_target_name(filepath, content=None):
    """
    规则G: 检查 BUILD.gn 中 ohos_fuzztest 目标名格式
    - 目标名必须以 FuzzTest 结尾
    - 目标名必须为驼峰式命名
    - group("fuzztest") 中的 deps 必须引用正确的目标名
    """
    errors = []
    filename = filepath if not content else None

    if filename:
        import os

        if os.path.basename(filename) != "BUILD.gn":
            return errors
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
        except (IOError, UnicodeDecodeError):
            return errors

    if not content:
        return errors

    # 检查 ohos_fuzztest 目标名
    target_matches = re.findall(r'ohos_fuzztest\("([^"]+)"\)', content)
    for target_name in target_matches:
        is_valid, error_msg = check_fuzztest_target_name_format(target_name)
        if not is_valid:
            errors.append(f"规则G: {error_msg}")

    # 检查 group("fuzztest") 中的 deps 是否引用了 ohos_fuzztest 目标名
    group_pattern = r'group\("fuzztest"\)\s*\{[^}]*deps\s*=\s*\[([^\]]*)\]'
    group_match = re.search(group_pattern, content, re.DOTALL)
    if group_match:
        deps_content = group_match.group(1)
        deps = re.findall(r'":([^"]+)"', deps_content)

        for dep in deps:
            is_valid, error_msg = check_fuzztest_target_name_format(dep)
            if not is_valid:
                errors.append(f'规则G: group("fuzztest") deps 中的 {error_msg}')

    return errors


if __name__ == "__main__":
    import os
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <BUILD.gn>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    result = check_build_gn_target_name(filepath)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
