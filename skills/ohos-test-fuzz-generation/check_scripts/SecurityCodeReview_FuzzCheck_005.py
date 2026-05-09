#!/usr/bin/env python3
"""
规则005: 复杂参数未合理构造
结构体/指针/回调/容器需合理构造，不能传nullptr或空对象
"""

import re
import os


def _get_target_class(content):
    """从代码中推断被测试的目标类名"""
    m = (
        re.search(r"std::make_shared<(\w+)>", content)
        or re.search(r"(\w+)::GetInstance\(\)", content)
        or re.search(r"(\w+)::Create\(\)", content)
        or re.search(r"(\w+)\*\s+g_\w+\s*=\s*nullptr", content)
    )
    return m.group(1) if m else None


def _extract_fuzzer_func_body(content, func_name, start_pos):
    """提取函数体（匹配大括号）"""
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


def check_complex_params(content):
    """
    规则005: 检查复杂参数是否合理构造
    - 不能传 nullptr 或空对象
    - 必须用 fdp 填充字段
    - 必须构造有意义的对象
    - 输出参数（由函数内部赋值的指针/引用参数）可以初始化为0/nullptr
    """
    errors = []

    # 排除的类型（不需要fdp填充的类型）
    SKIP_TYPES = {
        "FuzzedDataProvider",
        "std::string",
        "std::vector",
        "std::map",
        "std::set",
        "std::list",
        "std::shared_ptr",
        "std::unique_ptr",
        "MessageParcel",
        "MessageOption",
        "uint8_t",
        "uint16_t",
        "uint32_t",
        "uint64_t",
        "int8_t",
        "int16_t",
        "int32_t",
        "int64_t",
        "int",
        "bool",
        "char",
        "size_t",
        "float",
        "double",
        "void",
        "std::thread",
        "std::mutex",
        "std::lock_guard",
    }

    # 1. 检查智能指针（shared_ptr/unique_ptr/sptr）直接赋值为 nullptr
    smart_ptr_nullptr = re.findall(
        r"(std::shared_ptr<[^>]+>|std::unique_ptr<[^>]+>|\bsptr<[^>]+>)\s+(\w+)\s*=\s*nullptr\s*;",
        content,
    )
    for ptr_type, var_name in smart_ptr_nullptr:
        if not re.search(
            rf"\b{re.escape(var_name)}\s*=\s*(?:std::)?(?:make_shared|make_unique)\b",
            content,
        ) and not re.search(
            rf"\b{re.escape(var_name)}\s*=\s*new\b",
            content,
        ):
            errors.append(
                f"规则005[高危]: 智能指针 {var_name}（{ptr_type}）赋值为 nullptr 且未构造有效对象，"
                f"nullptr 会被业务前置校验拦截，应使用 make_shared/make_unique 构造有效对象"
            )

    # 2. 检查将 nullptr 作为回调（更宽泛的匹配）
    callback_nullptr = re.findall(
        r"(\w+)\s*=\s*nullptr\s*;",
        content,
    )
    for var_name in callback_nullptr:
        if re.search(
            rf"(?:\w+\s*->\s*\w+|(?:Set|Register|Add|Bind)\w+)\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)",
            content,
        ):
            if not re.search(
                rf"std::(?:shared_ptr|unique_ptr)<[^>]+>\s+{re.escape(var_name)}\b",
                content,
            ):
                errors.append(
                    f"规则005[高危]: 变量 {var_name} 为 nullptr 并传给接口，"
                    f"应构造有效的对象（如 lambda、函数对象等）"
                )

    # 3. 检查 make_shared/make_unique 无参构造（未从 fdp 获取参数）
    target_class = _get_target_class(content)
    make_empty = re.findall(
        r"(?:std::)?(?:make_shared|make_unique)<(\w+)>\s*\(\s*\)", content
    )
    for cls in make_empty:
        if cls == target_class:
            continue
        if not re.search(
            rf"(?:std::)?(?:make_shared|make_unique)<{re.escape(cls)}>\s*\([^)]*fdp\.",
            content,
        ):
            errors.append(
                f"规则005[高危]: make_shared/make_unique<{cls}>() 无参构造，"
                f"应从 FuzzedDataProvider 获取构造参数"
            )

    # 4. 检查结构体/类默认构造（无字段填充）
    # 按函数逐个检查，排除输出参数
    func_pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )

    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        # 查找函数体内的结构体/类声明
        # 匹配模式: TypeName varName; （大驼峰命名）
        struct_patterns = re.findall(
            r"\b([A-Z][a-zA-Z0-9_]*)\s+([a-z][a-zA-Z0-9_]*)\s*;",
            body,
        )

        # 去重
        seen_structs = set()
        unique_struct_patterns = []
        for struct_type, var_name in struct_patterns:
            key = (struct_type, var_name)
            if key not in seen_structs:
                seen_structs.add(key)
                unique_struct_patterns.append((struct_type, var_name))

        for struct_type, var_name in unique_struct_patterns:
            if struct_type in SKIP_TYPES:
                continue

            # 排除被赋值初始化的情况（如 Type var = fdp.Consume...）
            if re.search(
                rf"\b{re.escape(struct_type)}\s+{re.escape(var_name)}\s*=\s*fdp\.", body
            ):
                continue
            # 排除使用初始化列表的情况（如 Type var{fdp.Consume...}）
            if re.search(
                rf"\b{re.escape(struct_type)}\s+{re.escape(var_name)}\s*\{{\s*fdp\.",
                body,
            ):
                continue

            # 检查是否是输出参数（在函数调用中作为非const引用传递）
            is_output_param = False

            # 检查变量是否被初始化为0/nullptr（输出参数的典型特征）
            init_pattern = (
                rf"\b{re.escape(struct_type)}\s+{re.escape(var_name)}\s*=\s*(0|nullptr)"
            )
            if re.search(init_pattern, body):
                # 进一步检查是否在API调用中被使用
                api_call_pattern = (
                    rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)"
                )
                if re.search(api_call_pattern, body):
                    is_output_param = True

            # 检查是否有fdp填充字段
            has_fdp_fill = re.search(
                rf"{re.escape(var_name)}\.\w+\s*\(\s*fdp\.", body
            ) or re.search(rf"{re.escape(var_name)}\.\w+\s*=\s*fdp\.", body)

            if not has_fdp_fill and not is_output_param:
                errors.append(
                    f"规则005[高危]: 函数 {func_name}() 中结构体/类 {struct_type} 的变量 {var_name} "
                    f"默认构造后未用 fdp 填充字段，会被业务前置校验拦截，"
                    f"应使用 fdp.ConsumeXxx() 填充每个字段"
                )

    # 5. 检查空容器构造（排除通过赋值初始化的容器、作为API参数的容器和输出参数）
    # 按函数逐个检查
    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        # 查找函数体内的容器声明
        empty_containers = re.findall(
            r"(std::vector<[^>]+>|std::list<[^>]+>|std::map<[^>]+>)\s+(\w+)\s*;",
            body,
        )

        for container_type, var_name in empty_containers:
            # 排除通过 fdp 赋值初始化的（如 auto data = fdp.ConsumeBytes...）
            if re.search(rf"\b{re.escape(var_name)}\s*=\s*fdp\.Consume", body):
                continue

            # 检查是否有填充操作
            has_fill_ops = re.search(
                rf"{re.escape(var_name)}\.(?:push_back|emplace_back|emplace|insert|append|resize)\s*\(",
                body,
            )

            if has_fill_ops:
                continue  # 有填充操作，不报错

            # 检查是否被传给API（作为输入或输出参数）
            api_call_pattern = (
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)"
            )
            api_calls = re.findall(api_call_pattern, body)

            if api_calls:
                # 检查是否是输出参数（API调用后不再使用，除了可能在return中）
                is_output_param = True
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
                                is_output_param = False
                                break

                if is_output_param:
                    continue  # 是输出参数，不报错
                else:
                    continue  # 作为API输入参数，不报错（API可能会填充它）

            # 如果没有填充操作，且没有被传给API，则报错
            errors.append(
                f"规则005[高危]: 函数 {func_name}() 中容器 {container_type} 的变量 {var_name} 为空容器，"
                f"会被业务前置校验拦截或走空逻辑分支，应使用 fdp 填充元素"
            )

    # 6. 检查 C 风格指针传 nullptr
    if re.search(r"\w+\s*\*\s*\w+\s*=\s*nullptr\s*;", content):
        null_ptr_vars = re.findall(r"\w+\s*\*(\w+)\s*=\s*nullptr\s*;", content)
        for var in null_ptr_vars:
            if re.search(
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var)}\b[^)]*\)", content
            ):
                errors.append(
                    f"规则005[高危]: C 风格指针 {var} 为 nullptr 并传给接口，"
                    f"会被业务前置校验拦截，应分配有效内存并填充数据"
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

    result = check_complex_params(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
