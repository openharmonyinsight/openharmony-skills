#!/usr/bin/env python3
"""
规则C: project.xml格式验证
检查project.xml文件格式是否规范
"""

import os
import re


def check_project_xml(filepath):
    """
    规则C: 检查project.xml格式
    - 必须以 <?xml 声明开头
    - 根元素必须是 <fuzz_config>
    - 必须包含 <fuzztest> 子元素
    - 必须包含 max_len, max_total_time, rss_limit_mb 配置项
    """
    errors = []
    if not os.path.exists(filepath):
        return errors

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return [f"规则C: 无法读取 {filepath}"]

    if not content.strip().startswith('<?xml version="1.0" encoding="utf-8"?>'):
        errors.append(
            '规则C: project.xml 必须以 <?xml version="1.0" encoding="utf-8"?> 开头'
        )

    if "<fuzz_config>" not in content:
        errors.append("规则C: project.xml 根元素必须是 <fuzz_config>")

    if "<fuzztest>" not in content:
        errors.append("规则C: project.xml 必须包含 <fuzztest> 子元素")

    for config in ["max_len", "max_total_time", "rss_limit_mb"]:
        if f"<{config}>" not in content:
            errors.append(f"规则C: project.xml 缺少 {config} 配置项")
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
    
    result = check_project_xml(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
