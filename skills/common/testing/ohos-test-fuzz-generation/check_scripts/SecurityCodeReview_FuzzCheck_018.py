#!/usr/bin/env python3
"""
规则018: 变异数据使用不当
检查是否直接使用data指针或手动计算偏移量，而非通过FuzzedDataProvider提取
"""

import re
import os


def check_raw_data_usage(content):
    """
    规则018: 检查变异数据使用不当

    检测以下模式：
    1. 直接将data指针传给被测API
    2. 手动计算偏移量从data中截取数据
    3. 将data强转为结构体指针
    4. 对data进行指针算术运算
    """
    errors = []

    if not re.search(r"LLVMFuzzerTestOneInput", content):
        return errors

    # 1. 检查是否直接使用data指针传给API（非FuzzedDataProvider构造）
    # 排除合法场景：FuzzedDataProvider构造、size参数、边界检查
    # 匹配模式：g_instance->Method(data, ...) 或 ProcessData(data, ...)
    direct_data_patterns = [
        r"(?:g_\w+|\w+)\s*->\s*(\w+)\s*\([^)]*\bdata\b[^)]*\)",
        r"(\w+)\s*\([^)]*\bdata\b[^)]*\)",
    ]

    for pattern in direct_data_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            method_name = match.group(1)
            call_text = match.group(0)
            # 排除：函数参数声明（如 const uint8_t* data）
            if re.search(r"const\s+uint8_t\s*\*\s*data", call_text):
                continue
            # 排除：FuzzedDataProvider fdp(data, size)
            if re.search(
                r"FuzzedDataProvider\s+\w+\s*\(\s*data\s*,\s*size\s*\)", call_text
            ):
                continue
            # 排除：if (data == nullptr) 等边界检查
            if re.search(r"if\s*\([^)]*\bdata\b[^)]*\)", call_text):
                continue
            # 排除：return -1 等错误处理
            if re.search(r"return\s+-?\d+", call_text):
                continue
            # 排除：OnRemoteRequest测试（data传给MessageParcel是正常的）
            if method_name == "OnRemoteRequest":
                continue
            # 排除：WriteBuffer等Parcel操作方法（使用buffer.data()是正常的）
            if method_name in [
                "WriteBuffer",
                "WriteInterfaceToken",
                "WriteInt32",
                "WriteUint32",
                "WriteString",
            ]:
                continue
            # 排除：函数声明
            if method_name == "LLVMFuzzerTestOneInput":
                continue
            # 排除：if语句
            if method_name == "if":
                continue
            # 排除：fdp构造
            if method_name == "fdp":
                continue
            # 检查是否在LLVMFuzzerTestOneInput函数体中直接使用data
            func_start = content.rfind("LLVMFuzzerTestOneInput", 0, match.start())
            if func_start != -1:
                # 确保不是FuzzedDataProvider的构造
                fdp_construct = re.search(
                    r"FuzzedDataProvider\s+\w+\s*\(\s*data\s*,\s*size\s*\)",
                    content[func_start : match.start()],
                )
                if not fdp_construct or match.start() > fdp_construct.end() + 50:
                    # 检查是否有fdp.Consume的使用
                    if not re.search(
                        r"fdp\.Consume", content[func_start : match.end()]
                    ):
                        errors.append(
                            f"规则018[高危]: 直接使用data指针调用 {method_name}()，"
                            f"应通过FuzzedDataProvider提取数据后再传入，如 fdp.ConsumeBytes<uint8_t>(len)"
                        )

    # 2. 检查手动计算偏移量截取数据（如 data + 4, data + offset）
    offset_patterns = [
        r"data\s*+\s*\d+",
        r"data\s*+\s*\w+",
        r"\*data\s*+\s*\d+",
    ]
    for pattern in offset_patterns:
        if re.search(pattern, content):
            # 检查是否在合法的FuzzedDataProvider构造之外使用
            func_start = content.rfind(
                "LLVMFuzzerTestOneInput", 0, content.find(pattern)
            )
            if func_start != -1:
                func_body_start = content.find("{", func_start)
                if func_body_start != -1:
                    offset_pos = content.find(pattern)
                    if offset_pos > func_body_start:
                        # 检查是否不是在FuzzedDataProvider构造中使用
                        fdp_construct_end = content.find(")", func_body_start)
                        if (
                            fdp_construct_end != -1
                            and offset_pos > fdp_construct_end + 10
                        ):
                            errors.append(
                                "规则018[高危]: 手动计算偏移量从data中截取数据，"
                                "应使用fdp.ConsumeIntegral<T>()或fdp.ConsumeBytes<T>(len)按类型提取"
                            )
                            break

    # 3. 检查将data强转为结构体指针（reinterpret_cast<const X*>(data)）
    cast_patterns = [
        r"reinterpret_cast\s*<\s*const\s+(\w+)\s*\*\s*>\s*\(\s*data\s*\)",
        r"reinterpret_cast\s*<\s*(\w+)\s*\*\s*>\s*\(\s*data\s*\)",
        r"\(\s*(\w+)\s*\*\s*\)\s*data",
    ]
    for pattern in cast_patterns:
        match = re.search(pattern, content)
        if match:
            type_name = match.group(1)
            errors.append(
                f"规则018[高危]: 将data指针强转为 {type_name}* 类型，"
                f"不安全且不可移植，应通过fdp.ConsumeIntegral<T>()逐字段提取数据"
            )

    # 4. 检查对data的指针算术运算（如 *data, data[0]）
    pointer_arith_patterns = [
        r"\*\s*data\b",
        r"data\s*\[\s*\d+\s*\]",
        r"data\s*\[\s*\w+\s*\]",
    ]
    for pattern in pointer_arith_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            # 排除：函数参数声明（如 const uint8_t* data）
            line_start = content.rfind("\n", 0, match.start()) + 1
            line = content[line_start : match.end() + 50]
            if re.search(r"const\s+uint8_t\s*\*\s*data", line):
                continue
            # 排除：FuzzedDataProvider fdp(data, size)
            if re.search(r"FuzzedDataProvider\s+\w+\s*\(\s*data\s*,\s*size\s*\)", line):
                continue
            # 排除：if (data == nullptr) 等边界检查
            if re.search(r"if\s*\([^)]*\bdata\b[^)]*\)", line):
                continue
            # 排除：return -1 等错误处理
            if re.search(r"return\s+-?\d+", line):
                continue
            # 检查是否在LLVMFuzzerTestOneInput函数体中
            func_start = content.rfind("LLVMFuzzerTestOneInput", 0, match.start())
            if func_start != -1:
                # 确保不是FuzzedDataProvider的构造
                fdp_construct = re.search(
                    r"FuzzedDataProvider\s+\w+\s*\(\s*data\s*,\s*size\s*\)",
                    content[func_start : match.start()],
                )
                if not fdp_construct:
                    errors.append(
                        "规则018[高危]: 对data指针进行算术运算（如*data或data[N]），"
                        "应使用FuzzedDataProvider的方法提取数据"
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
    
    result = check_raw_data_usage(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
