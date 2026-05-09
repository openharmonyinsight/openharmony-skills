#!/usr/bin/env python3
"""
规则015: 中间产物由合法流程生成
检测编解码/序列化等成对调用，以及使用固定值构造参数
"""

import re
import os


def check_intermediate_products(content):
    """
    规则015: 检查中间产物是否由合法流程生成

    检测以下模式：
    1. 成对的编解码/序列化/加密/打包函数调用
    2. 使用固定值构造参数（如分辨率、刷新率等常见屏幕参数）
    3. 使用合法流程生成数据后再调用被测接口
    """
    errors = []

    # 1. 检测成对的编解码/序列化/加密/打包函数
    paired_patterns = [
        (r"[Ee]ncode\w*\s*\(", r"[Dd]ecode\w*\s*\(", "编解码"),
        (
            r"[Ss]erializ\w*\s*\(",
            r"[Dd]eserializ\w*\s*\(",
            "序列化/反序列化",
        ),
        (r"[Ee]ncrypt\w*\s*\(", r"[Dd]ecrypt\w*\s*\(", "加密/解密"),
        (r"[Pp]ack\w*\s*\(", r"[Uu]npack\w*\s*\(", "打包/解包"),
        (r"[Tt]o[Jj]son\s*\(", r"[Ff]rom[Jj]son\s*\(", "JSON序列化/反序列化"),
        (r"[Tt]o[Ss]tring\s*\(", r"[Ff]rom[Ss]tring\s*\(", "字符串序列化/反序列化"),
    ]

    for encode_pattern, decode_pattern, desc in paired_patterns:
        encode_matches = list(re.finditer(encode_pattern, content))
        decode_matches = list(re.finditer(decode_pattern, content))

        if encode_matches and decode_matches:
            for enc_match in encode_matches:
                enc_line = content[: enc_match.start()].count("\n") + 1
                func_start = content.rfind("void ", 0, enc_match.start())
                if func_start == -1:
                    func_start = content.rfind('extern "C" ', 0, enc_match.start())

                if func_start != -1:
                    func_name_match = re.search(
                        r"\b(\w+)\s*\(", content[func_start : enc_match.start()]
                    )
                    if func_name_match:
                        func_name = func_name_match.group(1)
                        func_end = content.find("\n}", enc_match.start())
                        if func_end == -1:
                            func_end = len(content)
                        func_body = content[enc_match.start() : func_end]

                        if re.search(decode_pattern, func_body):
                            errors.append(
                                f"规则015[高危]: 函数 '{func_name}' 中检测到{desc}成对调用，"
                                f"中间产物经由合法流程生成，会过滤掉变异数据中的异常值，"
                                f"建议直接使用变异数据测试被测接口"
                            )
                            break

    # 2. 检测使用固定值构造屏幕参数（仅检测明确的分辨率大数字，避免小数字误报）
    screen_params_patterns = [
        (
            r"uint32_t\s+\w*(?:width|Width|W)\w*\s*=\s*(1920|1080|720|480|2560|1440|3840|2160)\s*;",
            "分辨率",
        ),
        (
            r"uint32_t\s+\w*(?:height|Height|H)\w*\s*=\s*(1920|1080|720|480|2560|1440|3840|2160)\s*;",
            "分辨率",
        ),
    ]

    for pattern, param_type in screen_params_patterns:
        matches = list(re.finditer(pattern, content))
        if len(matches) >= 2:
            func_names = set()
            for match in matches:
                func_start = content.rfind("void ", 0, match.start())
                if func_start != -1:
                    func_name_match = re.search(
                        r"\b(\w+)\s*\(", content[func_start : match.start()]
                    )
                    if func_name_match:
                        func_names.add(func_name_match.group(1))

            for func_name in func_names:
                errors.append(
                    f"规则015[高危]: 函数 '{func_name}' 中使用固定值构造{param_type}参数，"
                    f"无法测试内部对非法参数的处理，建议使用变异数据构造各种参数值"
                )

    # 3. 检测使用合法流程生成数据后再调用被测接口
    generation_patterns = [
        r"\b(\w+)\s*=\s*(\w+)[Ee]ncode\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)[Ss]erializ\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)[Ee]ncrypt\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)[Pp]ack\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)\.([Tt]o[Jj]son|[Tt]o[Ss]tring)\s*\(",
    ]

    for pattern in generation_patterns:
        for match in re.finditer(pattern, content):
            var_name = match.group(1)
            usage_pattern = (
                rf"(?:g_\w+|\w+)\s*->\s*\w+\s*\([^)]*{re.escape(var_name)}[^)]*\)"
            )
            if re.search(usage_pattern, content[match.end() : match.end() + 500]):
                func_start = content.rfind("void ", 0, match.start())
                if func_start != -1:
                    func_name_match = re.search(
                        r"\b(\w+)\s*\(", content[func_start : match.start()]
                    )
                    if func_name_match:
                        func_name = func_name_match.group(1)
                        errors.append(
                            f"规则015[高危]: 函数 '{func_name}' 中先通过合法流程生成数据，"
                            f"再传给被测接口，建议直接使用变异数据"
                        )

    # 4. 检测校验和/签名的重新计算
    checksum_patterns = [
        r"\b\w+[Cc]hecksum\w*\s*\(",
        r"\b\w*[Hh]ash\w*\s*\([^)]*\)",
        r"\b[Cc]ompute[Ss]ignature\w*\s*\(",
        r"\b[Cc]alculate[Cc]rc\w*\s*\(",
        r"\b\w*[Ss]ign\w*\s*\(\s*\w+\s*\)",
    ]
    for pattern in checksum_patterns:
        checksum_match = re.search(pattern, content)
        if checksum_match:
            func_start = content.rfind("void ", 0, checksum_match.start())
            if func_start != -1:
                func_name_match = re.search(
                    r"\b(\w+)\s*\(", content[func_start : checksum_match.start()]
                )
                if func_name_match:
                    func_name = func_name_match.group(1)
                    errors.append(
                        f"规则015[高危]: 函数 '{func_name}' 中检测到校验和/签名计算，"
                        f"重新计算的校验值会使数据总是通过验证，建议直接使用变异数据测试校验逻辑"
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
    
    result = check_intermediate_products(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
