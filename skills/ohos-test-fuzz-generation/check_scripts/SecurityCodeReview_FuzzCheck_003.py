#!/usr/bin/env python3
"""
规则003: 未使用变异数据
检查所有测试函数中是否使用fdp.ConsumeXxx提取数据
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


def check_fuzzed_data_usage(content):
    """
    规则003: 检查是否使用了变异数据
    检查所有接收 FuzzedDataProvider 的函数中是否使用 fdp.ConsumeXxx 提取数据
    """
    errors = []

    # 1. 检查文件级别是否有 fdp.Consume
    has_fdp_consume = re.search(r"fdp\.Consume", content)
    has_llvm = re.search(r"LLVMFuzzerTestOneInput", content)

    if not has_fdp_consume and has_llvm:
        errors.append(
            "规则003[高危]: 未使用 FuzzedDataProvider 提取变异数据，"
            "fuzz 测试必须通过 fdp.ConsumeXxx() 从变异数据中提取参数"
        )
        return errors

    # 2. 检查所有接收 FuzzedDataProvider 参数的函数是否使用了 fdp.Consume
    fdp_func_pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )
    for func_match in fdp_func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        if not re.search(r"fdp\.", body):
            # 检查是否有智能指针构造（sptr 或 std::shared_ptr 的 new/make_shared）
            has_smart_ptr_construction = bool(
                re.search(
                    r"(sptr<[^>]+>\s+\w+\s*=\s*new\s+|std::shared_ptr<[^>]+>\s+\w+\s*=\s*std::make_shared<)",
                    body,
                )
            )
            if has_smart_ptr_construction:
                continue  # 智能指针构造是合法的参数构造方式

            errors.append(
                f"规则003[高危]: {func_name}() 函数未使用 fdp.ConsumeXxx() 提取变异数据，"
                f"属于无参数或固定参数调用，不适合 FUZZ 测试"
            )

    # 3. 检查 LLVMFuzzerTestOneInput 函数内部是否使用了 fdp.Consume
    llvm_match = re.search(
        r"extern\s+\"C\"\s+int\s+LLVMFuzzerTestOneInput\s*\([^)]*\)\s*\{",
        content,
    )
    if llvm_match:
        start = llvm_match.end() - 1
        body = _extract_fuzzer_func_body(content, "LLVMFuzzerTestOneInput", start)

        if not re.search(r"fdp\.Consume", body):
            if re.search(r"FuzzedDataProvider\s+\w+", body):
                errors.append(
                    "规则003[高危]: LLVMFuzzerTestOneInput() 中定义了 FuzzedDataProvider 但未使用 fdp.ConsumeXxx() 提取数据"
                )

    # 4. 检查API调用参数中是否存在固定值（字面量数字、字符串、bool）
    #    即：有fdp使用，但调用API时部分参数仍用固定值
    all_func_pattern = re.compile(
        r"\b(?:void|extern\s+\"C\"\s+int)\s+(\w+)\s*\([^)]*\)\s*\{"
    )
    for m in all_func_pattern.finditer(content):
        func_name = m.group(1)
        start = m.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)
        if not re.search(r"fdp\.Consume", body):
            continue

        # 提取所有 g_instance->Method(...) 或 obj.Method(...) 调用
        call_matches = re.finditer(r"(?:g_\w+|\w+)\s*->\s*(\w+)\s*\(([^)]*)\)", body)
        for call_match in call_matches:
            method_name = call_match.group(1)
            args_str = call_match.group(2).strip()
            if not args_str:
                continue
            args = [a.strip() for a in args_str.split(",")]
            fixed_args = []
            for arg in args:
                if re.match(r'^(?:\d+|0x[0-9A-Fa-f]+|"[^"]*"|true|false)$', arg):
                    fixed_args.append(arg)
            # 超过一半参数是固定值时报错
            if len(fixed_args) >= 2 and len(fixed_args) > len(args) / 2:
                errors.append(
                    f"规则003[高危]: {func_name}() 中调用 {method_name}() 时有 {len(fixed_args)}/{len(args)} 个参数使用固定值"
                    f"（{', '.join(fixed_args)}），应全部使用 fdp.ConsumeXxx() 提取变异数据"
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

    result = check_fuzzed_data_usage(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
