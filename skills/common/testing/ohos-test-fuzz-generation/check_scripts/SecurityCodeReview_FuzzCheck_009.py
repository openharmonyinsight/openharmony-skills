#!/usr/bin/env python3
"""
规则009: FUZZ Driver引入bug
检查内存安全、资源管理等Driver自身引入的安全问题
"""

import re
import os


def check_buffer_overflow(content):
    """
    规则009: 检查FUZZ Driver引入的安全问题
    - 内存安全类：堆溢出、栈溢出、数组越界、空指针解引用
    - 资源管理类：内存泄漏（new/delete不匹配）
    - 逻辑安全类：整数溢出/下溢、超大内存分配
    - 构造合理性问题：未初始化指针、未释放资源
    """
    errors = []
    # 1) 检测是否使用 data/size 进行 memcpy/memset 等可能堆溢出的操作
    dangerous_funcs = ["memcpy", "memset", "memmove", "strcpy", "strncpy"]
    for func in dangerous_funcs:
        if re.search(rf"\b{func}\s*\(", content):
            if "data" in content or "size" in content:
                errors.append(
                    f"规则009[高危]: 发现 {func}() 操作，若目标缓冲区大小小于 source 长度可能导致堆溢出，"
                    "请确保目标缓冲区大小与复制长度严格匹配"
                )
                break

    # 2) 检测 ConsumeBytes / ConsumeRandomLengthString 是否使用了极大的无限制长度
    large_bytes = re.findall(r"ConsumeBytes<\w+>\(\s*(\d{6,})\s*\)", content)
    for val in large_bytes:
        errors.append(
            f"规则009[高危]: ConsumeBytes() 使用了极大长度 {val}，可能导致内存占用过高或堆溢出，"
            "建议限制在合理范围（如 ≤ 65535）"
        )

    # 2.1) 检测未限制大小的内存分配
    alloc_patterns = [
        r"make_unique\<\s*\w+\s*\[]\>\s*\(([^)]+)\)",
        r"make_shared\<\s*\w+\s*\[]\>\s*\(([^)]+)\)",
        r"new\s+\w+\s*\[([^\]]+)\]",
    ]
    for pattern in alloc_patterns:
        for match in re.finditer(pattern, content):
            arg = match.group(1).strip()
            is_from_fdp = "fdp." in arg
            if not is_from_fdp and re.match(r"^\w+$", arg):
                var_def_pattern = rf"\b{re.escape(arg)}\s*=\s*fdp\."
                if re.search(var_def_pattern, content):
                    is_from_fdp = True

            if is_from_fdp:
                alloc_pos = match.start()
                nearby_content = content[max(0, alloc_pos - 200) : alloc_pos + 200]
                if not re.search(r"%\s*\d+", nearby_content):
                    errors.append(
                        "规则009[高危]: 发现未限制大小的内存分配（如 make_unique<Type[]>(fdp数据)），"
                        "可能分配超大内存导致卡住，应添加 % 限制大小（如 % 65536）"
                    )

    # 3) 检测数组越界访问（无范围校验的数组索引）
    array_access = re.search(
        r"(\w+)\s+\w+\s*\[\s*(\d+)\s*\]\s*;[^}]*?\w+\s*\[\s*\w+\s*\]\s*=",
        content,
        re.DOTALL,
    )
    if array_access:
        array_size = array_access.group(2)
        if not re.search(r"if\s*\([^)]*[<>]=?\s*" + array_size + r"[^)]*\)", content):
            errors.append(
                f"规则009[高危]: 发现数组访问未做范围校验（数组大小 {array_size}），可能导致数组越界，"
                f"应添加 if (index >= 0 && index < {array_size}) 检查"
            )

    # 4) 检测空指针解引用（将 nullptr 传给接口）
    if re.search(r"\w+\s*=\s*nullptr\s*;", content):
        null_vars = re.findall(r"(\w+)\s*=\s*nullptr\s*;", content)
        for var in null_vars:
            if re.search(
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var)}\b[^)]*\)", content
            ):
                errors.append(
                    f"规则009[高危]: 将 nullptr 变量 {var} 传给接口调用，可能导致空指针解引用，"
                    f"应构造有效对象而非传递 nullptr"
                )

    # 4.1) 检测未初始化的指针使用
    uninitialized_ptr = re.search(
        r"(\w+)\s*\*\s*(\w+)\s*;(?![^}]*?=)",
        content,
    )
    if uninitialized_ptr:
        ptr_var = uninitialized_ptr.group(2)
        if re.search(
            rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(ptr_var)}\b[^)]*\)", content
        ):
            errors.append(
                f"规则009[高危]: 发现未初始化的指针 {ptr_var} 被使用，可能导致未定义行为，"
                f"应使用 make_unique/make_shared 或 new 初始化"
            )

    # 5) 检测整数下溢（减法未做保护）
    sub_patterns = re.findall(
        r"(\w+)\s*=\s*(\w+)\s*-\s*(\w+)\s*;",
        content,
    )
    for result, left, right in sub_patterns:
        if re.search(rf"{re.escape(left)}\s*=\s*fdp\.", content):
            if not re.search(
                rf"if\s*\([^)]*{re.escape(left)}\s*[><]=?\s*{re.escape(right)}[^)]*\)",
                content,
            ):
                errors.append(
                    f"规则009[高危]: 发现整数减法 {result} = {left} - {right} 未做下溢保护，"
                    f"当 {left} < {right} 时会发生下溢，应添加 if ({left} >= {right}) 检查"
                )

    # 5.1) 检测整数溢出（乘法未做保护）
    mul_patterns = re.findall(
        r"(\w+)\s*=\s*(\w+)\s*\*\s*(\w+)\s*;",
        content,
    )
    for result, left, right in mul_patterns:
        if re.search(rf"{re.escape(left)}\s*=\s*fdp\.", content) or re.search(
            rf"{re.escape(right)}\s*=\s*fdp\.", content
        ):
            if not re.search(
                rf"if\s*\([^)]*{re.escape(result)}\s*[<>][^)]*\)", content
            ):
                errors.append(
                    f"规则009[高危]: 发现整数乘法 {result} = {left} * {right} 未做溢出保护，"
                    f"可能发生整数溢出，应添加范围检查"
                )

    # 5.2) 检测除零风险
    div_patterns = re.findall(
        r"(\w+)\s*/\s*(\w+)",
        content,
    )
    for left, right in div_patterns:
        if re.search(rf"{re.escape(right)}\s*=\s*fdp\.", content):
            if not re.search(
                rf"if\s*\([^)]*{re.escape(right)}\s*[!=]=\s*0[^)]*\)", content
            ) and not re.search(
                rf"if\s*\([^)]*{re.escape(right)}\s*[<>][^)]*\)", content
            ):
                errors.append(
                    f"规则009[高危]: 发现除法 {left} / {right}，除数来自 fdp 且未做除零保护，"
                    f"应添加 if ({right} != 0) 检查"
                )

    # 6) 检测长度判断与实际读取不匹配
    size_check = re.search(
        r"if\s*\(\s*(\w+)\s*<\s*(\d+)\s*\)\s*\{\s*return",
        content,
    )
    if size_check:
        var_name = size_check.group(1)
        checked_size = int(size_check.group(2))
        check_pos = size_check.end()
        remaining = content[check_pos:]
        byte_consumes = {
            "int8_t": 1,
            "uint8_t": 1,
            "int16_t": 2,
            "uint16_t": 2,
            "int32_t": 4,
            "uint32_t": 4,
            "int64_t": 8,
            "uint64_t": 8,
            "bool": 1,
            "float": 4,
            "double": 8,
        }
        total_bytes = 0
        for type_name, size in byte_consumes.items():
            count = len(
                re.findall(
                    rf"fdp\.ConsumeIntegral<{re.escape(type_name)}>\s*\(", remaining
                )
            )
            total_bytes += count * size
        bool_count = len(re.findall(r"fdp\.ConsumeBool\s*\(", remaining))
        total_bytes += bool_count
        float_count = len(
            re.findall(r"fdp\.ConsumeFloatingPoint<float>\s*\(", remaining)
        )
        total_bytes += float_count * 4
        double_count = len(
            re.findall(r"fdp\.ConsumeFloatingPoint<double>\s*\(", remaining)
        )
        total_bytes += double_count * 8
        if total_bytes > checked_size:
            errors.append(
                f"规则009[高危]: 长度检查不足: {var_name} 只检查了 {checked_size} 字节，"
                f"但后续读取了约 {total_bytes} 字节，可能导致堆溢出"
            )

    # 7) 检测内存泄漏（new 后没有 delete）
    new_allocations = re.findall(
        r"(\w+)\s*\*\s*(\w+)\s*=\s*new\s+\w+",
        content,
    )
    for type_name, var_name in new_allocations:
        if not re.search(rf"delete\s+{re.escape(var_name)}", content) and not re.search(
            rf"delete\[\]\s+{re.escape(var_name)}", content
        ):
            errors.append(
                f"规则009[高危]: 发现内存泄漏: 使用 new 分配了 {var_name} 但未释放，"
                f"应使用 delete/delete[] 释放或使用智能指针（make_unique/make_shared）"
            )

    # 8) 检测 malloc 后没有 free
    malloc_allocations = re.findall(
        r"(\w+)\s*\*\s*(\w+)\s*=\s*\(\s*\w+\s*\*\s*\)\s*malloc",
        content,
    )
    for type_name, var_name in malloc_allocations:
        if not re.search(rf"free\s*\(\s*{re.escape(var_name)}\s*\)", content):
            errors.append(
                f"规则009[高危]: 发现内存泄漏: 使用 malloc 分配了 {var_name} 但未释放，"
                f"应使用 free 释放或使用智能指针"
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
    
    result = check_buffer_overflow(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
