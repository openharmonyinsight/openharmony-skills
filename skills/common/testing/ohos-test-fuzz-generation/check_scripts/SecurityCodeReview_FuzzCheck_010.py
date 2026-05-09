#!/usr/bin/env python3
"""
规则010: size当作变异数据
检查size参数是否被用于业务逻辑而非仅用于边界检查和FuzzedDataProvider初始化
"""

import re
import os


def _extract_func_body(content, start_pos):
    """提取函数体"""
    brace_count = 0
    body_start = -1
    for i in range(start_pos, len(content)):
        if content[i] == "{":
            brace_count += 1
            if brace_count == 1:
                body_start = i + 1
        elif content[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                return content[body_start:i]
    return ""


def check_size_as_fuzz_data(content):
    """
    规则010: 检查size是否被当作变异数据使用

    检测以下模式：
    1. 将size直接传给被测API
    2. 用size做业务分支判断
    3. 用size作为循环次数
    4. size参与算术运算后作为参数
    """
    errors = []

    if not re.search(r"LLVMFuzzerTestOneInput", content):
        return errors

    # 检查LLVMFuzzerTestOneInput函数体
    func_match = re.search(
        r"extern\s+\"C\"\s+int\s+LLVMFuzzerTestOneInput\s*\([^)]*\)\s*\{", content
    )
    if not func_match:
        return errors

    func_body = _extract_func_body(content, func_match.end() - 1)

    # 1. 检查将size直接传给被测API
    # 匹配: g_instance->Method(..., size, ...) 或 g_instance->Method(size)
    api_calls = re.finditer(r"(\w+)\s*->\s*(\w+)\s*\(([^)]*)\)", func_body)

    for match in api_calls:
        obj_name = match.group(1)
        method_name = match.group(2)
        args_str = match.group(3)

        # 排除FuzzedDataProvider构造
        if obj_name == "FuzzedDataProvider" or "FuzzedDataProvider" in args_str:
            continue

        # 检查参数中是否包含size
        if re.search(r"\bsize\b", args_str):
            # 排除: if (size < N) return 0; 这样的边界检查
            # 获取这行之前的代码
            line_start = func_body.rfind("\n", 0, match.start()) + 1
            context = func_body[line_start : match.start()]

            # 如果前面有return 0，可能是边界检查后的代码
            if not re.search(r"return\s+0", context):
                errors.append(
                    f"规则010[高危]: 将size参数直接传给 {method_name}()，"
                    f"size由fuzz引擎决定不代表业务输入，应通过fdp.ConsumeIntegral<T>()提取"
                )

    # 2. 检查用size做业务分支判断
    # 匹配: if (size ...) { ...->...(...) }
    branch_matches = re.finditer(
        r"if\s*\([^)]*\bsize\b[^)]*\)\s*\{[^}]*\w+\s*->\s*\w+\s*\(", func_body
    )

    for match in branch_matches:
        branch_text = match.group(0)
        # 排除: if (size < N) return 0;
        if re.search(r"return\s+0", branch_text):
            continue
        # 排除: if (size < N) { return 0; }
        if re.search(r"if\s*\(\s*size\s*[<>]=?\s*\d+\s*\)\s*\{?\s*return", branch_text):
            continue

        errors.append(
            "规则010[高危]: 用size参数做业务分支判断，"
            "size仅用于边界检查，业务分支条件应通过fdp.ConsumeBool()或fdp.ConsumeIntegral()提取"
        )

    # 3. 检查用size作为循环次数
    loop_patterns = [
        r"for\s*\([^)]*\bsize\b[^)]*\)",
        r"while\s*\([^)]*\bsize\b[^)]*\)",
    ]

    for pattern in loop_patterns:
        for match in re.finditer(pattern, func_body):
            loop_text = match.group(0)
            # 排除: for (size_t i = 0; i < min(size, N); i++)
            if re.search(r"size\s*[<>]=?\s*\d+", loop_text):
                continue
            errors.append(
                "规则010[高危]: 用size参数作为循环次数，"
                "循环次数应通过fdp.ConsumeIntegralInRange<T>(min, max)提取"
            )

    # 4. 检查size参与算术运算后作为参数
    # 匹配: var = ...size...;
    arithmetic_matches = re.finditer(r"(\w+)\s*=\s*[^;]*\bsize\b[^;]*;", func_body)

    for match in arithmetic_matches:
        var_name = match.group(1)
        expr = match.group(0)

        # 排除: if (size < N) return 0; 中的size
        if re.search(r"size\s*[<>]=?\s*\d+", expr):
            continue
        # 排除: FuzzedDataProvider fdp(data, size);
        if "FuzzedDataProvider" in expr:
            continue

        # 检查该变量是否被用于API调用
        api_usage = re.search(
            rf"\w+\s*->\s*(\w+)\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)",
            func_body[match.end() :],
        )

        if api_usage:
            method_name = api_usage.group(1)
            errors.append(
                f"规则010[高危]: size参数参与算术运算后作为参数传给 {method_name}()，"
                f"size由fuzz引擎决定，业务参数应通过fdp.ConsumeIntegral<T>()提取"
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
    
    result = check_size_as_fuzz_data(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
