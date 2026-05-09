#!/usr/bin/env python3
"""
规则A: 头文件格式验证
检查.h文件的格式规范（必需系统头文件、保护宏、FUZZ_PROJECT_NAME宏）
"""

import re
import os


def check_header_file(filename, dirname, content):
    """
    规则A: 检查头文件格式
    - 必需的系统头文件
    - #ifndef/#define/#endif 保护宏
    - FUZZ_PROJECT_NAME 宏定义
    - 不定义命名空间
    """
    errors = []
    # 定义必需的头文件组（C++风格和C风格都接受）
    required_header_groups = [
        ["<cstdint>", "<stdint.h>"],  # 整数类型
        ["<unistd.h>"],  # Unix标准（只有C风格）
        ["<climits>", "<limits.h>"],  # 限制宏
        ["<cstdio>", "<stdio.h>"],  # 标准IO
        ["<cstdlib>", "<stdlib.h>"],  # 标准库
        ["<fcntl.h>"],  # 文件控制（只有C风格）
    ]

    missing = []
    for header_group in required_header_groups:
        # 检查该组中是否有任何一个头文件被包含
        if not any(f"#include {h}" in content for h in header_group):
            # 如果没有，报告缺少该组的第一个（推荐）头文件
            missing.append(header_group[0])

    if missing:
        errors.append(f"规则A: 头文件缺少必需的系统头文件: {', '.join(missing)}")

    if not (
        re.search(r"#ifndef\s+\w+", content)
        and "#define" in content
        and "#endif" in content
    ):
        errors.append("规则A: 头文件缺少 #ifndef/#define/#endif 保护宏")

    fuzz_project_match = re.search(r'#define\s+FUZZ_PROJECT_NAME\s+"([^"]+)"', content)
    if not fuzz_project_match:
        errors.append("规则A: 头文件未定义 FUZZ_PROJECT_NAME 宏")
    else:
        project_name = fuzz_project_match.group(1)
        if project_name != dirname:
            errors.append(
                f"规则A: FUZZ_PROJECT_NAME '{project_name}' 与目录名 '{dirname}' 不一致"
            )

    # 检查不定义命名空间
    if re.search(r"\bnamespace\s+\w+", content):
        errors.append("规则A: 头文件不应定义命名空间")

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
    
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))
    result = check_header_file(filename, dirname, content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
