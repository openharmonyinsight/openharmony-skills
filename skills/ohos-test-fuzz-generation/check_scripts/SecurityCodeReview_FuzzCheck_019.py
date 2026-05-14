#!/usr/bin/env python3
"""
规则019: 全局变量初始化检查
检查全局指针是否在LLVMFuzzerInitialize中正确初始化
"""

import re
import os


def check_global_initialization(content):
    """
    规则019: 检查全局指针初始化

    检测策略:
    1. 查找全局指针声明（如 RSScreenManager* g_manager = nullptr;）
    2. 检查是否存在 LLVMFuzzerInitialize 函数
    3. 检查全局指针是否在 LLVMFuzzerInitialize 中被赋值为有效对象
    """
    errors = []

    # 1. 查找全局指针声明
    global_ptr_pattern = re.compile(
        r"^(\w+(?:\s*::\s*\w+)*)\s*\*\s*(g_\w+)\s*=\s*nullptr\s*;", re.MULTILINE
    )

    global_ptrs = []
    for match in global_ptr_pattern.finditer(content):
        ptr_type = match.group(1).strip()
        ptr_name = match.group(2)
        global_ptrs.append((ptr_type, ptr_name))

    if not global_ptrs:
        # 没有全局指针，无需检查
        return errors

    # 2. 检查是否存在 LLVMFuzzerInitialize 函数
    init_match = re.search(
        r'extern\s+"C"\s+int\s+LLVMFuzzerInitialize\s*\(\s*int\*\s*\w+\s*,\s*char\*\*\*\s*\w+\s*\)',
        content,
    )

    if not init_match:
        errors.append(
            "规则019[高危]: 发现全局指针但未找到 LLVMFuzzerInitialize 函数，"
            "全局指针可能未初始化，建议添加初始化函数"
        )
        return errors

    # 3. 提取 LLVMFuzzerInitialize 函数体
    init_start = init_match.end()
    brace_count = 0
    init_body_start = None
    init_body_end = None

    for i in range(init_start, len(content)):
        if content[i] == "{":
            if brace_count == 0:
                init_body_start = i + 1
            brace_count += 1
        elif content[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                init_body_end = i
                break

    if init_body_start is None or init_body_end is None:
        errors.append("规则019[高危]: 无法解析 LLVMFuzzerInitialize 函数体")
        return errors

    init_body = content[init_body_start:init_body_end]

    # 4. 检查每个全局指针是否在初始化函数中被赋值
    for ptr_type, ptr_name in global_ptrs:
        # 检查是否在初始化函数中被赋值为有效对象
        # 支持命名空间路径: &Class::GetInstance(), &Namespace::Class::GetInstance() 等
        assignment_pattern = re.compile(
            rf"\b{re.escape(ptr_name)}\s*=\s*(?:&(?:\w+::)+GetInstance\(\)|new\s+\w+|std::make_shared<[^>]+>|\w+)\s*;"
        )

        if not assignment_pattern.search(init_body):
            # 检查是否被赋值为 nullptr
            null_assignment = re.search(
                rf"\b{re.escape(ptr_name)}\s*=\s*nullptr\s*;", init_body
            )

            if null_assignment:
                errors.append(
                    f"规则019[高危]: 全局指针 {ptr_name} 在 LLVMFuzzerInitialize 中被赋值为 nullptr，"
                    f"应使用 &{ptr_type}::GetInstance() 或 new {ptr_type}() 初始化"
                )
            else:
                errors.append(
                    f"规则019[高危]: 全局指针 {ptr_name} 未在 LLVMFuzzerInitialize 中初始化，"
                    f"可能导致空指针解引用"
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
    
    result = check_global_initialization(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
