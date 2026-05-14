#!/usr/bin/env python3
"""
规则012: 目标API内部分支覆盖不足
检测常见的导致fuzz无法触及核心逻辑的问题
"""

import re
import os


def check_branch_coverage(content):
    """
    规则012: 检查目标API内部分支覆盖是否可能不足
    检测常见的导致fuzz无法触及核心逻辑的问题

    注意: 本规则专注于分支覆盖问题，不检测空容器/空指针构造
    （空容器/空指针由规则005负责检测）
    """
    errors = []

    # 1. 检测是否使用了固定值作为参数（排除小数值和输出参数初始化）
    # 匹配: Type var = value; ... API(var)
    # 排除: 输出参数初始化（如 uint32_t width = 0;）
    func_pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )

    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1

        # 提取函数体
        brace_count = 0
        body_start = -1
        body = ""
        for i in range(start, len(content)):
            if content[i] == "{":
                brace_count += 1
                if brace_count == 1:
                    body_start = i + 1
            elif content[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    body = content[body_start:i]
                    break

        if not body:
            continue

        # 在函数体内查找固定值赋值
        fixed_assignments = re.findall(
            r"(?:uint32_t|int32_t|uint64_t|int64_t|uint8_t|int8_t|auto)\s+(\w+)\s*=\s*(\d+)\s*;",
            body,
        )

        for var_name, value in fixed_assignments:
            # 排除小数值（0-5通常用于索引、计数等）
            if value in ("0", "1", "2", "3", "4", "5"):
                continue

            # 排除输出参数（初始化为0且在API调用中被修改）
            # 检查是否在API调用中被使用，且后续没有读取
            api_call_pattern = (
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)"
            )
            api_calls = re.findall(api_call_pattern, body)

            if api_calls:
                # 检查API调用后是否还使用了这个变量
                is_output = True
                for api_call in api_calls:
                    api_pos = body.find(api_call)
                    if api_pos >= 0:
                        after_api = body[api_pos + len(api_call) :]
                        # 如果API调用后还有使用（且不是return语句），则不是输出参数
                        if re.search(rf"\b{re.escape(var_name)}\b", after_api):
                            line_start = (
                                after_api.rfind("\n", 0, after_api.find(var_name)) + 1
                            )
                            line = after_api[line_start : line_start + 50]
                            if not re.match(r"\s*return", line):
                                is_output = False
                                break

                if is_output:
                    continue  # 是输出参数，跳过

            # 检查是否使用了fdp（如果使用了fdp，固定值可能是合理的）
            if re.search(r"fdp\.Consume", body):
                # 如果函数中使用了fdp，但仍有固定值，可能是部分参数固定
                errors.append(
                    f"规则012[高危]: 函数 {func_name}() 中发现将固定值 {value} 作为参数传给接口，"
                    f"可能只覆盖了特定分支。应使用 fdp.ConsumeXxx() 产生变异数据以覆盖多分支。"
                )
                break  # 只报告一次

    # 2. 检测是否未构造前置依赖
    dependent_apis_patterns = [
        r"^ProcessData$",
        r"^ProcessImage$",
        r"^HandleRequest$",
        r"^HandleEvent$",
        r"^ExecuteCommand$",
        r"^RenderFrame$",
        r"^DrawSurface$",
        r"^ReceiveData$",
        r"^ParseMessage$",
        r"^ParseData$",
        r"^Configure$",
        r"^Update$",
        r"^Modify$",
    ]
    setup_apis = [
        r"Init",
        r"Initialize",
        r"Create",
        r"Load",
        r"Open",
        r"Prepare",
        r"SetUp",
        r"Connect",
        r"Start",
        r"Begin",
    ]

    api_calls = re.findall(r"\w+\s*->\s*(\w+)\s*\(", content)

    has_dependent = False
    has_setup = False
    for call in api_calls:
        for pattern in dependent_apis_patterns:
            if re.match(pattern, call):
                has_dependent = True
                break
        for pattern in setup_apis:
            if re.search(pattern, call):
                has_setup = True
                break

    if has_dependent and not has_setup and len(api_calls) >= 1:
        if not re.search(
            r"//.*(?:已初始化|initialized|prepared|setup)", content, re.IGNORECASE
        ):
            errors.append(
                "规则012[高危]: 检测到可能调用需要前置状态的接口，但未发现状态准备调用。"
                "请检查目标 API 是否需要先调用 Init/Create/Load 等接口构造前置条件。"
                "缺少前置依赖会导致 fuzz 无法触及核心业务逻辑。"
            )

    # 3. 检测是否使用了 ConsumeBytes 但长度为 0
    zero_bytes = re.search(
        r"ConsumeBytes<\w+>\(\s*0\s*\)",
        content,
    )
    if zero_bytes:
        errors.append(
            "规则012[高危]: 发现使用 ConsumeBytes 时长度为 0，将产生空数据，"
            "可能只覆盖空数据校验分支。应确保长度大于 0 以覆盖数据处理逻辑。"
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
    
    result = check_branch_coverage(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
