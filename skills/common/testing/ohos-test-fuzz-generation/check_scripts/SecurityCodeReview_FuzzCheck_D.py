#!/usr/bin/env python3
"""
规则D: 文件命名一致性验证
检查文件名与目录名是否一致，FUZZ_PROJECT_NAME是否与目录名一致
"""

import os
import re


def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, UnicodeDecodeError) as e:
        return None


def check_fuzzer_name_format(name):
    """
    检查fuzzer命名是否符合 XxxXxx_fuzzer 格式（驼峰式+下划线+fuzzer后缀）
    允许数字后缀如 XxxXxx_fuzzer1, XxxXxx_fuzzer2
    """
    # 去掉数字后缀
    base_name = re.sub(r"\d+$", "", name)
    # 匹配驼峰式+_fuzzer格式
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*_fuzzer$", base_name))


def check_directory_consistency(filepath):
    """
    规则D: 检查文件命名一致性
    - .cpp/.h 文件名应与目录名一致
    - 命名应符合 XxxXxx_fuzzer 格式
    - 头文件中FUZZ_PROJECT_NAME应与目录名一致

    注意: BUILD.gn中ohos_fuzztest目标名格式由规则G检查，不在本规则范围内
    """
    errors = []
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))

    # 检查目录名是否符合 XxxXxx_fuzzer 格式
    if not check_fuzzer_name_format(dirname):
        errors.append(
            f"规则D: 目录名 '{dirname}' 不符合命名规范，应为 XxxXxx_fuzzer 格式（驼峰式+下划线+fuzzer后缀）"
        )

    if filename.endswith((".cpp", ".h")):
        stem = os.path.splitext(filename)[0]
        if stem != dirname and not re.match(rf"^{re.escape(dirname)}\d*$", stem):
            errors.append(f"规则D: 文件名 '{filename}' 与目录名 '{dirname}' 不一致")
        # 检查文件名是否符合命名规范
        if not check_fuzzer_name_format(stem):
            errors.append(
                f"规则D: 文件名 '{filename}' 不符合命名规范，应为 XxxXxx_fuzzer 格式（驼峰式+下划线+fuzzer后缀）"
            )

    # 检查头文件中的FUZZ_PROJECT_NAME
    if filename.endswith(".h"):
        content = read_file(filepath) or ""
        fuzz_project_match = re.search(
            r'#define\s+FUZZ_PROJECT_NAME\s+"([^"]+)"', content
        )
        if fuzz_project_match:
            project_name = fuzz_project_match.group(1)
            if project_name != dirname:
                errors.append(
                    f"规则D: 头文件中 FUZZ_PROJECT_NAME '{project_name}' 与目录名 '{dirname}' 不一致"
                )

    return errors


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <cpp_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    result = check_fuzzer_name_format(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
