#!/usr/bin/env python3
"""
规则006: 单文件测试接口过多
检查TARGET_SIZE、测试函数调用数量、switch-case分支数量等
"""

import re
import os


def check_target_size(content):
    """
    规则006: 检查单文件测试接口数量是否超过10个
    支持多种模式：
    1. TARGET_SIZE 常量定义
    2. 串行调用测试函数
    3. switch-case 分支
    """
    errors = []

    # 1. 检查 TARGET_SIZE 常量（支持const和constexpr）
    target_size_matches = re.findall(
        r"(?:const|constexpr)\s+\w+\s+TARGET_SIZE\s*=\s*(\d+)", content
    )
    if target_size_matches:
        target_size = int(target_size_matches[0])
        if target_size > 10:
            errors.append(
                f"规则006[中危]: TARGET_SIZE={target_size} 超过10，单文件接口过多会导致数据变异性差，建议拆分为多个fuzzer文件"
            )
            return errors

    # 2. 检查串行调用的测试函数数量（接收FuzzedDataProvider参数的函数调用）
    serial_calls = re.findall(r"\b(\w+)\s*\(\s*\w+\s*\)", content)
    fdp_func_names = set(
        re.findall(r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider", content)
    )
    test_calls = [c for c in serial_calls if c in fdp_func_names]
    unique_test_calls = list(dict.fromkeys(test_calls))
    if len(unique_test_calls) > 10:
        errors.append(
            f"规则006[中危]: 发现 {len(unique_test_calls)} 个串行调用的测试函数，超过10个会导致数据变异性差，"
            f"建议拆分为多个fuzzer文件或使用switch-case模式"
        )
        return errors

    # 3. 检查 switch-case 分支数量
    switch_pattern = re.compile(
        r"switch\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}", re.DOTALL
    )
    for switch_match in switch_pattern.finditer(content):
        switch_body = switch_match.group(1)
        case_count = len(re.findall(r"\bcase\s+", switch_body))
        if case_count > 10:
            errors.append(
                f"规则006[中危]: switch-case 模式中有 {case_count} 个分支，超过10个会导致数据变异性差，"
                f"建议拆分为多个fuzzer文件"
            )
            return errors

    # 4. 检查 if-else if 链式调用
    if_chain = re.findall(
        r"\bif\s*\([^)]*\)\s*\{[^}]*\}\s*(?:else\s+if\s*\([^)]*\)\s*\{[^}]*\}\s*)*",
        content,
        re.DOTALL,
    )
    for chain in if_chain:
        if_count = len(re.findall(r"\bif\s*\(", chain))
        if if_count > 10:
            errors.append(
                f"规则006[中危]: if-else if 链式调用中有 {if_count} 个分支，超过10个会导致数据变异性差，"
                f"建议拆分为多个fuzzer文件"
            )
            return errors

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
    
    result = check_target_size(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
