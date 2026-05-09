#!/usr/bin/env python3
"""
规则013: 枚举值构造不合理
核心原则: 使用uint8_t而非大整数类型，不要按业务上限取模
"""

import re
import os

_NON_ENUM_TYPES = {
    "int8_t",
    "uint8_t",
    "int16_t",
    "uint16_t",
    "int32_t",
    "uint32_t",
    "int64_t",
    "uint64_t",
    "int",
    "unsigned",
    "long",
    "size_t",
    "ssize_t",
    "float",
    "double",
    "bool",
    "char",
    "void",
    "string",
    "String",
    "FuzzedDataProvider",
    # 非枚举类型（typedef/alias for built-in types）
    "ScreenId",
    "NodeId",
    "WindowId",
    "DisplayId",
    "ProcessId",
    "UserId",
    "Uid",
    "Pid",
    "Handle",
    "Fd",
    "DrawableId",
}


def _looks_like_enum(name):
    if name in _NON_ENUM_TYPES:
        return False
    if re.match(r"^[A-Z][a-zA-Z0-9_]*$", name) and len(name) > 1:
        return True
    return False


def check_enum_range(content):
    """
    规则013: 检查枚举值构造是否合理
    核心原则: 使用 uint8_t 而非大整数类型，不要按业务上限取模
    """
    errors = []
    lines = content.split("\n")
    code_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*"):
            continue
        code_lines.append(line)
    code_content = "\n".join(code_lines)

    enum_casts_64_direct = re.findall(
        r"static_cast\<(\w+)\>\s*\(\s*fdp\.ConsumeIntegral\<(uint64_t|int64_t)\>\s*\(",
        code_content,
    )
    for enum_name, src_type in enum_casts_64_direct:
        if _looks_like_enum(enum_name):
            errors.append(
                f"规则013[中危]: 枚举 {enum_name} 使用 {src_type} 构造，范围过大（0~18446744073709551615），"
                f"合法值命中率极低，建议使用 uint8_t（0~255）提取"
            )

    all_static_casts = re.finditer(
        r"static_cast\<(\w+)\>\s*\(\s*(\w+)\s*\)",
        code_content,
    )
    for match in all_static_casts:
        enum_name = match.group(1)
        var_name = match.group(2)
        if not _looks_like_enum(enum_name):
            continue
        var_def = re.search(
            rf"\b(uint64_t|int64_t)\s+{re.escape(var_name)}\s*=\s*fdp\.ConsumeIntegral",
            code_content,
        )
        if var_def:
            errors.append(
                f"规则013[中危]: 枚举 {enum_name} 使用 uint64_t/int64_t 构造，范围过大（0~18446744073709551615），"
                f"合法值命中率极低，建议使用 uint8_t（0~255）提取"
            )

    all_static_casts_32 = re.finditer(
        r"static_cast\<(\w+)\>\s*\(\s*(\w+)\s*\)",
        code_content,
    )
    seen_32 = set()
    for match in all_static_casts_32:
        enum_name = match.group(1)
        var_name = match.group(2)
        if not _looks_like_enum(enum_name):
            continue
        if enum_name in seen_32:
            continue
        var_def = re.search(
            rf"\b(uint32_t|int32_t)\s+{re.escape(var_name)}\s*=\s*fdp\.ConsumeIntegral",
            code_content,
        )
        if var_def:
            seen_32.add(enum_name)
            errors.append(
                f"规则013[中危]: 枚举 {enum_name} 使用 uint32_t/int32_t 构造，范围过大（0~4294967295），"
                f"合法值命中率极低，建议使用 uint8_t（0~255）提取"
            )

    enum_assignments = re.finditer(
        r"(\w+)\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<(uint32_t|int32_t|uint64_t|int64_t)>\s*\(",
        code_content,
    )
    for match in enum_assignments:
        enum_type = match.group(1)
        var_name = match.group(2)
        src_type = match.group(3)
        if _looks_like_enum(enum_type):
            # 检查是否有 static_cast<enum_type>(var_name)
            cast_found = re.search(
                rf"static_cast<{re.escape(enum_type)}>\s*\(\s*{re.escape(var_name)}\s*\)",
                code_content,
            )
            if cast_found:
                continue
            # 检查变量是否实际上是 uint8_t 类型（通过 ConsumeIntegral<uint8_t> 提取）
            uint8_def = re.search(
                rf"\buint8_t\s+{re.escape(var_name)}\s*=\s*fdp\.ConsumeIntegral<uint8_t>",
                code_content,
            )
            if uint8_def:
                continue
            errors.append(
                f"规则013[中危]: 枚举类型 {enum_type} 的变量 {var_name} 使用 {src_type} 提取，"
                f"范围过大，建议使用 uint8_t（0~255）提取"
            )

    small_modulo = re.finditer(
        r"static_cast<(\w+)>\s*\(\s*fdp\.ConsumeIntegral<\w+>\s*\(\)\s*%\s*(\d+)\s*\)",
        code_content,
    )
    for match in small_modulo:
        enum_name = match.group(1)
        mod_value = int(match.group(2))
        if _looks_like_enum(enum_name) and mod_value <= 8:
            # 只有非常小的模数（<=8）才报错，因为会严重限制枚举值范围
            errors.append(
                f"规则013[中危]: 发现枚举 {enum_name} 取模 % {mod_value}，可能将枚举限制到业务上限，"
                f"会丢失非法值处理分支的覆盖。建议直接使用 uint8_t 提取而不取模，"
                f"或取模到更大的值（如 % 256）以保留非法值覆盖。"
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

    result = check_enum_range(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
