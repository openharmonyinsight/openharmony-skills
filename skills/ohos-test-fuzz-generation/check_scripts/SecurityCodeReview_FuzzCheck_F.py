#!/usr/bin/env python3
"""
规则F: 版权头规范
检查文件是否包含正确的华为版权声明和Apache License 2.0
"""

import re
import os


def check_copyright(filepath, content):
    """
    规则F: 检查版权头
    - .cpp/.h 文件必须包含正确的版权声明
    - BUILD.gn 必须包含正确的版权声明
    - project.xml 必须包含正确的版权声明
    - 所有文件必须包含 Apache License 2.0 声明
    """
    errors = []
    filename = os.path.basename(filepath)
    first_lines = "\n".join(content.splitlines()[:30])

    copyright_pattern = r"Copyright\s*\(\s*c\s*\)\s*((202[0-9]|2030)|\{YEAR\})\s+Huawei\s+Device\s+Co\.?\s*,?\s*Ltd\.?"
    has_copyright = re.search(copyright_pattern, first_lines)

    has_apache = bool(
        re.search(
            r"Licensed\s+under\s+the\s+Apache\s+License", first_lines, re.IGNORECASE
        )
    )

    if filename.endswith((".cpp", ".h")):
        if not has_copyright:
            errors.append(
                "规则F: .cpp/.h 文件版权头不正确，必须包含 'Copyright (c) <year> Huawei Device Co., Ltd.'（年份应为 2020-2030 的实际年份）"
            )
        if not has_apache:
            errors.append("规则F: .cpp/.h 文件缺少 Apache License 2.0 声明")
    elif filename == "BUILD.gn":
        if not has_copyright:
            errors.append(
                "规则F: BUILD.gn 版权头不正确，必须包含 '# Copyright (c) <year> Huawei Device Co., Ltd.'（年份应为 2020-2030 的实际年份）"
            )
        if not has_apache:
            errors.append("规则F: BUILD.gn 缺少 Apache License 2.0 声明")
    elif filename == "project.xml":
        if not has_copyright:
            errors.append(
                "规则F: project.xml 版权头不正确，必须包含 '<!-- Copyright (c) <year> Huawei Device Co., Ltd.'（年份应为 2020-2030 的实际年份）"
            )
        if not has_apache:
            errors.append("规则F: project.xml 缺少 Apache License 2.0 声明")
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
    
    result = check_copyright(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
