#!/usr/bin/env python3
"""
规则001: 目标API不适合FUZZ
检查API是否有参数，无参数API不适合FUZZ测试
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


def check_unfuzzable_api(content):
    """
    规则001: 检查是否有不适合fuzz的API（无参数或仅固定参数）

    检测策略:
    1. 函数体中完全没有使用 fdp. 的情况 → 报错
    2. 有 fdp. 使用，但只使用了选择器变量（如 tarPos）而没有实际的业务参数消费 → 提示
    """
    errors = []
    pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )
    for m in pattern.finditer(content):
        func_name = m.group(1)
        start = m.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        # 1. 检查是否真正使用了 fdp 构造参数
        # 排除 (void)fdp; 这种仅压制编译器警告的用法
        has_real_fdp_usage = bool(
            re.search(
                r"fdp\.(Consume|Pick|ConsumeBytes|ConsumeRemainingBytes|ConsumeRandomLengthString)",
                body,
            )
        )

        if not has_real_fdp_usage:
            # 检查是否是智能指针 nullptr 测试（合法场景）
            has_nullptr_test = bool(
                re.search(
                    r"\bnullptr\b\s*;?\s*/\*\s*auto-generated\s+for\s+(sptr|std::shared_ptr)",
                    body,
                )
            )
            if has_nullptr_test:
                continue  # nullptr 测试是合法的 fuzz 策略

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
                f"规则001[高危]: {func_name}() 中目标 API 调用未使用 FuzzedDataProvider 构造参数，"
                "属于无参数或固定参数 API，不适合 FUZZ 测试，建议移除或改为单元测试"
            )
            continue

        # 2. 有 fdp. 使用，但检查是否有实际的业务参数消费
        # 排除仅用于选择器的情况（如 tarPos = fdp.ConsumeIntegral<uint8_t>() % TARGET_SIZE）
        # 业务参数消费特征：
        # - fdp.ConsumeIntegral<T>() 且不是 % TARGET_SIZE 的选择器
        # - fdp.ConsumeBool()
        # - fdp.ConsumeFloatingPoint<T>()
        # - fdp.ConsumeRandomLengthString()
        # - fdp.ConsumeBytes()
        # - fdp.ConsumeRemainingBytes()

        # 查找所有 fdp.Consume 调用
        consume_calls = re.findall(r"fdp\.(Consume\w+)(?:<[^>]+>)?\s*\(", body)

        # 检查是否有选择器模式（如 tarPos = fdp.ConsumeIntegral<uint8_t>() % TARGET_SIZE）
        has_selector = bool(
            re.search(
                r"fdp\.ConsumeIntegral<\w+>\s*\(\)\s*%\s*\w+_SIZE|fdp\.ConsumeIntegral<\w+>\s*\(\)\s*%\s*TARGET_SIZE",
                body,
            )
        )

        # 检查是否有实际的业务参数消费（排除选择器）
        business_consumes = []
        for call in consume_calls:
            # 检查这个消费调用是否用于选择器
            # 获取消费调用的位置
            for match in re.finditer(rf"fdp\.{re.escape(call)}(?:<[^>]+>)?\s*\(", body):
                call_start = match.start()
                # 检查后面是否有 % 限制（在分配附近）
                remaining = body[call_start : call_start + 100]
                if not re.search(r"%\s*(?:\w+_SIZE|TARGET_SIZE)", remaining):
                    business_consumes.append(call)

        # 如果只有选择器消费，没有业务参数消费
        if has_selector and not business_consumes and len(consume_calls) > 0:
            # 检查API调用是否有参数
            api_calls = re.findall(r"\w+\s*->\s*\w+\s*\(([^)]*)\)", body)
            for args_str in api_calls:
                args = [a.strip() for a in args_str.split(",") if a.strip()]
                if len(args) <= 1:  # 只有一个参数或没有参数（可能是this指针）
                    errors.append(
                        f"规则001[中危]: {func_name}() 中目标 API 调用参数过少（{len(args)}个），"
                        "可能不适合 FUZZ 测试，建议检查是否需要更多参数覆盖"
                    )
                    break

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

    result = check_unfuzzable_api(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
