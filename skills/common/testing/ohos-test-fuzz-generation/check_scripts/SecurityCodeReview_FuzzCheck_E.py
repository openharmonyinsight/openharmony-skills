#!/usr/bin/env python3
"""
规则E: .cpp文件头文件包含验证
检查.cpp文件是否包含对应的同名.h头文件，以及使用双引号包含
"""

import os
import re

SYSTEM_HEADERS = {
    "cstdint",
    "unistd.h",
    "climits",
    "cstdio",
    "cstdlib",
    "fcntl.h",
    "vector",
    "map",
    "set",
    "string",
    "memory",
    "functional",
    "algorithm",
    "array",
    "deque",
    "list",
    "queue",
    "stack",
    "tuple",
    "utility",
    "chrono",
    "thread",
    "mutex",
    "atomic",
    "condition_variable",
    "iostream",
    "fstream",
    "sstream",
    "iomanip",
    "iosfwd",
    "cmath",
    "complex",
    "numeric",
    "valarray",
    "cassert",
    "cerrno",
    "cfloat",
    "cinttypes",
    "climits",
    "clocale",
    "csignal",
    "cstdalign",
    "cstdarg",
    "cstdbool",
    "cstddef",
    "cstdint",
    "cstdio",
    "cstdlib",
    "cstring",
    "ctgmath",
    "ctime",
    "cuchar",
    "cwchar",
    "cwctype",
    "sys/types.h",
    "sys/stat.h",
    "sys/mman.h",
    "sys/socket.h",
    "netinet/in.h",
    "arpa/inet.h",
    "pthread.h",
    "dlfcn.h",
    "errno.h",
    "fcntl.h",
    "limits.h",
    "signal.h",
    "stdarg.h",
    "stddef.h",
    "stdint.h",
    "stdio.h",
    "stdlib.h",
    "string.h",
    "time.h",
    "unistd.h",
    "wchar.h",
    "wctype.h",
    "optional",
    "variant",
    "any",
    "string_view",
    "filesystem",
    "fuzzer/FuzzedDataProvider.h",
}


def check_cpp_include(filename, content):
    """
    规则E: 检查.cpp文件头文件包含
    - .cpp 文件应包含对应的同名 .h 头文件
    - 包含路径应使用双引号而非尖括号
    """
    errors = []
    # 获取文件名（不含路径）
    basename = os.path.basename(filename)
    expected_header = basename.replace(".cpp", ".h")
    include_pattern = rf'#include\s+"{re.escape(expected_header)}"'
    if not re.search(include_pattern, content):
        includes = re.findall(r'#include\s+"([^"]+\.h)"', content)
        # 检查是否包含期望的头文件（只比较文件名）
        includes_basenames = [os.path.basename(inc) for inc in includes]
        if includes and expected_header not in includes_basenames:
            errors.append(
                f"规则E: .cpp 包含的头文件 '{includes[0]}' 与文件名 '{expected_header}' 不一致"
            )
        elif not includes:
            errors.append(
                f"规则E: .cpp 文件未使用双引号包含自身头文件 '{expected_header}'"
            )

    angle_bracket_includes = re.findall(r"#include\s*<([^>]+\.h)>", content)
    project_angle = [h for h in angle_bracket_includes if h not in SYSTEM_HEADERS]
    if project_angle:
        errors.append(
            f"规则E: 项目头文件应使用双引号包含而非尖括号，发现: <{', <'.join(project_angle)}>"
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
    
    result = check_cpp_include(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
