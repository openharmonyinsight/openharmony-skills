#!/usr/bin/env python3
"""
规则014: 使用固定参数
fuzz测试应使用变异数据，除非业务必需（API版本号、Magic Number等）
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


def check_fixed_params(content):
    """
    规则014: 检查是否使用固定参数
    fuzz测试应使用变异数据，除非业务必需（API版本号、Magic Number等）

    检测策略:
    1. 如果函数中所有参数都是固定值（无论是否"合理"），则报错
    2. 如果存在多个不合理的固定值（非业务必需），则报错
    3. 输出参数（初始化为0/nullptr）不算固定参数
    """
    errors = []

    # 合理的固定值（业务必需场景）
    reasonable_fixed_values = {
        "0x52494646",
        "0x12345678",
        "0x504B0304",
        "0x89504E47",
        "0xFFD8FF",
        "0xFF",
        "0xFFFF",
        "0xFFFFFFFF",
        "0x00",
        "0x01",
        "0x02",
    }

    # 合理的变量名（暗示这是业务必需固定值）
    reasonable_fixed_names = {
        "version",
        "Version",
        "VERSION",
        "magic",
        "Magic",
        "MAGIC",
        "headerSize",
        "HEADER_SIZE",
        "flag",
        "flags",
        "Flag",
        "Flags",
        "FLAG",
        "FLAGS",
        "enable",
        "disable",
        "Enabled",
        "Disabled",
        "true",
        "false",
    }

    # 找到所有DoXXX函数定义
    func_pattern = re.compile(
        r"\bvoid\s+(Do\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )

    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        func_body = _extract_func_body(content, func_match.end() - 1)

        if not func_body:
            continue

        # 1. 查找 fdp.Consume 调用（变异数据）
        consume_calls = re.findall(r"\w+\s*=\s*fdp\.Consume\w+", func_body)

        # 2. 查找固定数字赋值
        fixed_assignments = []

        # 匹配: Type var = value; 或 auto var = value;
        assignment_patterns = [
            r"(?:uint32_t|int32_t|uint8_t|int8_t|uint16_t|int16_t|size_t|int|unsigned|uint64_t|int64_t|auto)\s+(\w+)\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*;",
            r"(\w+)\s*=\s*(0x[0-9A-Fa-f]{3,}|\d{3,})\s*;",
        ]

        seen_assignments = set()
        for pattern in assignment_patterns:
            for var_match in re.finditer(pattern, func_body):
                var_name = var_match.group(1)
                value = var_match.group(2)

                # 去重：避免同一个赋值被多个模式匹配
                assignment_key = (var_name, value)
                if assignment_key in seen_assignments:
                    continue
                seen_assignments.add(assignment_key)

                # 排除循环变量
                if re.search(rf"for\s*\([^)]*{re.escape(var_name)}[^)]*\)", func_body):
                    continue
                # 排除const
                if re.search(rf"const\s+\w+\s+{re.escape(var_name)}", func_body):
                    continue
                # 排除输出参数（初始化为0）
                if value == "0" and re.search(
                    rf"\b{re.escape(var_name)}\b[^=]*\)", func_body
                ):
                    # 检查是否在API调用中被修改
                    api_call_pattern = (
                        rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)"
                    )
                    if re.search(api_call_pattern, func_body):
                        continue

                fixed_assignments.append((var_name, value))

        # 3. 查找字符串固定值
        string_assignments = re.findall(r'\w+\s*=\s*"([^"]{4,})"\s*;', func_body)

        # 4. 查找 bool 固定值
        bool_assignments = re.findall(r"\w+\s*=\s*(true|false)\s*;", func_body)

        # 判断逻辑:
        # A. 如果没有任何 Consume 调用，且存在固定赋值，则所有参数都是固定的
        if len(consume_calls) == 0 and (
            len(fixed_assignments) > 0
            or len(string_assignments) > 0
            or len(bool_assignments) > 0
        ):
            errors.append(
                f"规则014[高危]: 函数 '{func_name}' 中所有参数都使用固定值，未使用 fdp.Consume*() 获取变异数据"
            )
            continue

        # B. 如果有 Consume 调用，检查不合理的固定值
        unreasonable_count = 0
        unreasonable_details = []

        for var_name, value in fixed_assignments:
            # 检查是否是合理的固定值
            # 小数值（0-5）通常合理（如索引、计数等）
            # 但大于5的数值通常不合理，应该使用变异数据
            is_small_value = value in ("0", "1", "2", "3", "4", "5")

            is_reasonable = (
                value in reasonable_fixed_values
                or var_name in reasonable_fixed_names
                or is_small_value
            )

            if not is_reasonable:
                unreasonable_count += 1
                unreasonable_details.append(f"{var_name}={value}")

        # 字符串固定值通常都不合理（除非是空字符串或短字符串）
        for s in string_assignments:
            if len(s) > 5:  # 长度大于5的字符串固定值通常不合理
                unreasonable_count += 1
                unreasonable_details.append(f'string="{s}"')

        # bool固定值通常合理（开关类参数）
        # 但如果有多个bool固定值，可能不合理
        if len(bool_assignments) > 2:
            unreasonable_count += len(bool_assignments) - 2

        # 如果存在不合理的固定值，则报错
        # 阈值：只要有1个不合理的固定值就报错（因为fuzz测试应该使用变异数据）
        if unreasonable_count > 0:
            errors.append(
                f"规则014[高危]: 函数 '{func_name}' 中存在 {unreasonable_count} 个不合理的固定参数"
                f"（{', '.join(unreasonable_details[:3])}），"
                f"fuzz 测试应使用变异数据构造参数以增加覆盖率"
            )
        elif len(fixed_assignments) > 0 and len(consume_calls) == 0:
            # 如果没有consume调用，但有固定值，也报错
            errors.append(
                f"规则014[高危]: 函数 '{func_name}' 使用固定参数而非变异数据，"
                f"应使用 fdp.Consume*() 提取数据"
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
    
    result = check_fixed_params(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
