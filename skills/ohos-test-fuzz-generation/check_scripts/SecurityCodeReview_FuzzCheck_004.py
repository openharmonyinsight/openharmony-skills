#!/usr/bin/env python3
"""
规则004: 重复使用变异数据
避免同一变量用于多个接口调用
"""

import re
import os


def _extract_fuzzer_func_body(content, func_name, start_pos):
    """从函数名后的 '{' 开始提取完整函数体"""
    brace_count = 0
    end = start_pos
    for i in range(start_pos, len(content)):
        if content[i] == "{":
            brace_count += 1
        elif content[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end = i
                break
    return content[start_pos + 1 : end]


def check_reused_data(content):
    """
    规则004: 检查在同一个函数体内，从fdp提取的变量是否被重复用于多个接口调用。
    """
    errors = []

    pattern = re.compile(r"\b(?:void|extern\s+\"C\"\s+int)\s+(\w+)\s*\([^)]*\)\s*\{")

    for m in pattern.finditer(content):
        func_name = m.group(1)
        start = m.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        if not re.search(r"fdp\.", body):
            continue

        var_pattern = re.compile(
            r"(?:const\s+)?(?:[\w:]+\s+)?(?:\*?\s*)?(\w+)\s*=\s*fdp\.(Consume\w+)"
        )

        var_usage = {}

        for var_match in var_pattern.finditer(body):
            var_name = var_match.group(1)
            if var_name not in var_usage:
                var_usage[var_name] = {
                    "consume_type": var_match.group(2),
                    "methods": [],
                }

        method_call_pattern = re.compile(
            r"(?:(?:g_\w+|\w+)\s*->\s*(\w+)|(\w+)\s*->\s*(\w+)|(\w+)::(\w+))\s*\(([^)]*)\)"
        )

        for call_match in method_call_pattern.finditer(body):
            method_name = (
                call_match.group(1) or call_match.group(3) or call_match.group(5)
            )
            args_str = call_match.group(6)

            for var_name in var_usage:
                if re.search(rf"\b{re.escape(var_name)}\b", args_str):
                    if method_name not in var_usage[var_name]["methods"]:
                        var_usage[var_name]["methods"].append(method_name)

        # 也检查直接函数调用: MethodName(args)
        direct_call_pattern = re.compile(r"(\w+)\s*\(([^)]*)\)")
        for call_match in direct_call_pattern.finditer(body):
            method_name = call_match.group(1)
            args_str = call_match.group(2)
            # 跳过fdp调用、控制流、类型转换等
            if method_name in (
                "if",
                "for",
                "while",
                "switch",
                "return",
                "static_cast",
                "dynamic_cast",
                "reinterpret_cast",
                "const_cast",
            ):
                continue
            if method_name.startswith("Consume") or method_name == "fdp":
                continue
            for var_name in var_usage:
                if re.search(rf"\b{re.escape(var_name)}\b", args_str):
                    if method_name not in var_usage[var_name]["methods"]:
                        var_usage[var_name]["methods"].append(method_name)

        reused_vars = []
        for var_name, info in var_usage.items():
            if len(info["methods"]) >= 2:
                # 豁免场景1: 同一个变量在同一个API的多次调用中使用
                unique_methods = list(dict.fromkeys(info["methods"]))
                if len(unique_methods) == 1:
                    continue
                # 豁免场景2: 回调函数中重复使用（lambda/函数对象内部使用外部变量）
                if re.search(r"\[.*&.*\].*->", body) and len(unique_methods) <= 2:
                    continue
                reused_vars.append({"var": var_name, "methods": unique_methods})

        if reused_vars:
            details = []
            for rv in reused_vars:
                details.append(f"变量 '{rv['var']}' 被用于: {', '.join(rv['methods'])}")

            errors.append(
                f"规则004[中危]: {func_name}() 中发现 {len(reused_vars)} 个变异数据变量被重复用于多个接口调用，"
                f"会降低 fuzz 覆盖率和数据变异性。详情: {'; '.join(details)}"
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
    
    result = check_reused_data(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
