#!/usr/bin/env python3
"""
FUZZ检查工具基础模块
提供共享的辅助函数
"""

import re


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
