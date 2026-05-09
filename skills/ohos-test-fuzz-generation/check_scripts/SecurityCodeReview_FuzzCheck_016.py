#!/usr/bin/env python3
"""
规则016: 赋值数据类型不正确
检查fdp生成类型与变量声明类型不匹配的问题
"""

import re
import os


def check_type_mismatch(content):
    """
    规则016: 检查类型不匹配问题
    - fdp生成类型与变量声明类型不一致
    - 小字节类型赋值给大字节类型
    - 有符号/无符号混用
    - 整数与浮点混用
    - 指针与整数混用
    """
    errors = []

    # 1. 检查 data 强转为 char*
    if re.search(r"char\s*\*\s*\w+\s*=\s*\(\s*char\s*\*\s*\)\s*data", content):
        errors.append(
            "规则016[高危]: 将 data 强转为 char*，二进制数据不等于字符串，应使用 fdp.ConsumeRandomLengthString()"
        )

    # 2. 检查 fdp 生成类型与变量声明类型不一致
    type_mismatch_patterns = [
        (
            r"uint8_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<uint(?:16|32|64)_t>",
            "uint8_t",
            "uint16/32/64_t",
        ),
        (
            r"int8_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int(?:16|32|64)_t>",
            "int8_t",
            "int16/32/64_t",
        ),
        (
            r"uint16_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<uint(?:32|64)_t>",
            "uint16_t",
            "uint32/64_t",
        ),
        (
            r"int16_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int(?:32|64)_t>",
            "int16_t",
            "int32/64_t",
        ),
        (
            r"uint32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<uint64_t>",
            "uint32_t",
            "uint64_t",
        ),
        (r"int32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int64_t>", "int32_t", "int64_t"),
        (r"float\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<\w+>", "float", "整数类型"),
        (r"double\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<\w+>", "double", "整数类型"),
    ]

    for pattern, var_type, fdp_type in type_mismatch_patterns:
        mismatches = re.findall(pattern, content)
        for var_name in mismatches:
            errors.append(
                f"规则016[高危]: 变量 {var_name} 声明为 {var_type}，但使用 fdp.ConsumeIntegral<{fdp_type}>() 赋值，"
                f"类型不匹配可能导致数据截断或精度丢失，应使用匹配的类型"
            )

    # 3. 检查小类型赋值给大类型（零填充失真）
    type_sizes = {
        "uint8_t": 1,
        "int8_t": 1,
        "uint16_t": 2,
        "int16_t": 2,
        "uint32_t": 4,
        "int32_t": 4,
        "uint64_t": 8,
        "int64_t": 8,
    }
    # 匹配所有基本类型变量从fdp提取
    all_fdp_vars = re.findall(
        r"(uint8_t|int8_t|uint16_t|int16_t|uint32_t|int32_t|uint64_t|int64_t)\s+(\w+)\s*=\s*fdp\.Consume",
        content,
    )
    for src_type, var_name in all_fdp_vars:
        src_size = type_sizes.get(src_type, 0)
        # 检查该变量是否被赋值给更大类型的变量
        large_assign = re.findall(
            r"(uint8_t|int8_t|uint16_t|int16_t|uint32_t|int32_t|uint64_t|int64_t)\s+\w+\s*=\s*"
            + re.escape(var_name)
            + r"\b",
            content,
        )
        for dst_type in large_assign:
            dst_size = type_sizes.get(dst_type, 0)
            if dst_size > src_size:
                errors.append(
                    f"规则016[高危]: 将 {src_size} 字节变量 {var_name}（{src_type}）赋值给 {dst_type}（{dst_size} 字节），"
                    f"零填充导致变异空间受限，应直接用 fdp.ConsumeIntegral<{dst_type}>() 提取"
                )
                break

    # 4. 检查有符号/无符号混用
    signed_types = {"int8_t", "int16_t", "int32_t", "int64_t"}
    unsigned_types = {"uint8_t", "uint16_t", "uint32_t", "uint64_t", "size_t"}
    for src_type, var_name in all_fdp_vars:
        if src_type not in signed_types:
            continue
        # 检查是否被赋值给无符号类型
        unsigned_assign = re.findall(
            r"(uint8_t|uint16_t|uint32_t|uint64_t|size_t)\s+\w+\s*=\s*"
            + re.escape(var_name)
            + r"\b",
            content,
        )
        for dst_type in unsigned_assign:
            errors.append(
                f"规则016[高危]: 有符号变量 {var_name}（{src_type}）赋值给无符号类型 {dst_type}，"
                f"负数会被解释为超大正数，应使用匹配的类型"
            )
            break

    # 5. 检查整数与浮点混用
    int_to_float_patterns = [
        (
            r"int32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int32_t>",
            r"float\s+\w+\s*=\s*static_cast<float>\s*\(\s*\w+\s*\)",
        ),
        (
            r"int64_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int64_t>",
            r"double\s+\w+\s*=\s*static_cast<double>\s*\(\s*\w+\s*\)",
        ),
    ]

    for int_pattern, float_pattern in int_to_float_patterns:
        int_vars = re.findall(int_pattern, content)
        for var_name in int_vars:
            if re.search(
                rf"float\s+\w+\s*=\s*static_cast<float>\s*\(\s*{re.escape(var_name)}\s*\)",
                content,
            ):
                errors.append(
                    f"规则016[高危]: 将整数变量 {var_name} 转为 float，会丢失小数部分，应使用 fdp.ConsumeFloatingPoint<float>()"
                )

    # 6. 检查指针与整数混用
    if re.search(r"uintptr_t\s+\w+\s*=\s*fdp\.ConsumeIntegral<uintptr_t>", content):
        if re.search(r"reinterpret_cast<void\*>\s*\(\s*\w+\s*\)", content):
            errors.append(
                "规则016[高危]: 将整数 reinterpret_cast 为指针，随机地址可能无效，应通过合法 API 构造对象"
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
    
    result = check_type_mismatch(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
