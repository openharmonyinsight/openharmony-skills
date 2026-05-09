#!/usr/bin/env python3
"""
规则008: 种子合理构造
检查corpus目录是否存在、是否为空、种子文件大小和格式是否合理
"""

import re
import os


def check_seed_files(filepath, content):
    """
    规则008: 检查种子文件是否合理构造

    检测以下问题：
    1. corpus/ 目录是否存在
    2. corpus/ 目录是否为空
    3. 种子文件大小是否为0
    4. 种子文件格式是否与API类型匹配

    豁免场景：
    - 新生成的fuzzer（包含TODO注释或生成器标记）
    - 纯查询类API（无输入参数）
    """
    errors = []

    file_dir = os.path.dirname(filepath)
    corpus_dir = os.path.join(file_dir, "corpus")

    # 检查是否是新生成的fuzzer（包含TODO注释）
    # 新生成的fuzzer可能还没有种子文件，这是正常的
    if re.search(r"//\s*TODO|TODO:", content):
        # 新生成的fuzzer，跳过种子检查
        return errors

    # 检查是否是纯查询类API（无输入参数）
    # 如果没有使用fdp.Consume，说明是纯查询类API，不需要种子
    if not re.search(r"fdp\.Consume", content):
        return errors

    # 检查是否是新生成的fuzzer（文件创建时间在24小时内）
    # 新生成的fuzzer可能还没有种子文件，给予宽限期
    try:
        file_stat = os.stat(filepath)
        import time

        # 如果文件创建时间在24小时内，跳过检查
        if (time.time() - file_stat.st_ctime) < 24 * 3600:
            return errors
    except (OSError, AttributeError):
        pass

    # 检查是否是纯查询类API（无输入参数）
    # 如果没有使用fdp.Consume，说明是纯查询类API，不需要种子
    if not re.search(r"fdp\.Consume", content):
        return errors

    # 1. 检查 corpus/ 目录是否存在
    if not os.path.exists(corpus_dir):
        errors.append(
            "规则008[中危]: 未找到 corpus/ 目录，建议创建并放置合理的初始种子文件，"
            "可使用工具: python3 tools/seed_generator.py -t <type> -o corpus/init"
        )
        return errors

    # 2. 检查 corpus/ 目录是否为空
    if os.path.isdir(corpus_dir):
        seed_files = [
            f
            for f in os.listdir(corpus_dir)
            if os.path.isfile(os.path.join(corpus_dir, f))
        ]
        if not seed_files:
            errors.append(
                "规则008[中危]: corpus/ 目录为空，建议放置合理的初始种子文件，"
                "可使用工具: python3 tools/seed_generator.py -t <type> -o corpus/init"
            )
            return errors

        # 3. 检查种子文件大小
        for seed_file in seed_files:
            seed_path = os.path.join(corpus_dir, seed_file)
            file_size = os.path.getsize(seed_path)
            if file_size == 0:
                errors.append(
                    f"规则008[中危]: 种子文件 '{seed_file}' 大小为0，"
                    f"空文件无法提供有效的初始变异基础"
                )

        # 4. 检查种子文件格式是否与API类型匹配
        api_types = infer_api_types(content)
        if api_types:
            for seed_file in seed_files:
                file_ext = os.path.splitext(seed_file)[1].lower()
                if not is_seed_format_valid(file_ext, api_types):
                    errors.append(
                        f"规则008[中危]: 种子文件 '{seed_file}' 格式（{file_ext}）"
                        f"可能与API期望的输入类型（{', '.join(api_types)}）不匹配，"
                        f"建议使用: python3 tools/seed_generator.py 生成合适的种子"
                    )

    return errors


def infer_api_types(content):
    """从代码内容推断API期望的输入类型"""
    api_types = set()

    if any(
        kw in content for kw in ["Decode", "Encode", "Image", "JPEG", "PNG", "Bitmap"]
    ):
        api_types.add("image")

    if any(kw in content for kw in ["Json", "JSON", "ParseJson"]):
        api_types.add("json")

    if any(kw in content for kw in ["Xml", "XML", "ParseXml"]):
        api_types.add("xml")

    if any(kw in content for kw in ["String", "Text", "Char"]):
        api_types.add("text")

    if any(kw in content for kw in ["Bytes", "Binary", "Buffer", "Data"]):
        api_types.add("binary")

    if any(kw in content for kw in ["Parcel", "Message", "Packet", "Protocol"]):
        api_types.add("protocol")

    return api_types


def is_seed_format_valid(file_ext, api_types):
    """检查种子文件格式是否与API类型匹配"""
    format_mapping = {
        ".jpg": ["image"],
        ".jpeg": ["image"],
        ".png": ["image"],
        ".gif": ["image"],
        ".bmp": ["image"],
        ".json": ["json"],
        ".xml": ["xml"],
        ".txt": ["text"],
        ".bin": ["binary", "protocol"],
        ".dat": ["binary", "protocol"],
        "": ["binary", "protocol"],
    }

    if not api_types:
        return True

    if file_ext in format_mapping:
        valid_types = format_mapping[file_ext]
        return any(api_type in valid_types for api_type in api_types)

    return True


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
    
    result = check_seed_files(filepath, content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
