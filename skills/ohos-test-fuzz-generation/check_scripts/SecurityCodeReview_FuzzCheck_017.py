#!/usr/bin/env python3
"""
规则017: 禁止使用random等函数
应使用FuzzedDataProvider提供的Consume方法
"""

import re
import os


def check_random_usage(content):
    """
    规则017: 检查是否使用了random/rand/srand等函数
    这些函数不可重现且不受fuzz引擎控制
    """
    errors = []

    # 1. 检查C标准库随机函数
    c_random_funcs = [
        (r"\brand\s*\(", "rand()"),
        (r"\brandom\s*\(", "random()"),
        (r"\bsrand\s*\(", "srand()"),
        (r"\brand_r\s*\(", "rand_r()"),
    ]

    for pattern, func_name in c_random_funcs:
        if re.search(pattern, content):
            errors.append(
                f"规则017[高危]: 发现使用 {func_name}，这些函数不可重现且不受 fuzz 引擎控制，"
                f"应使用 fdp.ConsumeIntegral() 等方法"
            )

    # 2. 检查C++标准库随机类
    cpp_random_classes = [
        (r"std::random_device", "std::random_device"),
        (r"std::mt19937", "std::mt19937"),
        (r"std::mt19937_64", "std::mt19937_64"),
        (r"std::minstd_rand", "std::minstd_rand"),
        (r"std::uniform_int_distribution", "std::uniform_int_distribution"),
        (r"std::uniform_real_distribution", "std::uniform_real_distribution"),
        (r"std::normal_distribution", "std::normal_distribution"),
        (r"std::bernoulli_distribution", "std::bernoulli_distribution"),
    ]

    for pattern, class_name in cpp_random_classes:
        if re.search(pattern, content):
            errors.append(
                f"规则017[高危]: 发现使用 {class_name}，应使用 FuzzedDataProvider 提供的 Consume 方法"
            )

    # 3. 检查其他随机函数
    other_random_funcs = [
        (r"\bdrand48\s*\(", "drand48()"),
        (r"\blrand48\s*\(", "lrand48()"),
        (r"\bmrand48\s*\(", "mrand48()"),
        (r"\barc4random\s*\(", "arc4random()"),
        (r"\bgetrandom\s*\(", "getrandom()"),
    ]

    for pattern, func_name in other_random_funcs:
        if re.search(pattern, content):
            errors.append(
                f"规则017[高危]: 发现使用 {func_name}，这些函数不可重现且不受 fuzz 引擎控制，"
                f"应使用 fdp.ConsumeIntegral() 等方法"
            )

    # 4. 检查时间种子（常与srand一起使用）
    if re.search(r"srand\s*\(\s*time\s*\(", content) or re.search(
        r"srand\s*\(\s*clock\s*\(", content
    ):
        errors.append(
            "规则017[高危]: 发现使用 srand(time()) 或 srand(clock())，时间种子不可重现，"
            "应使用 fdp.ConsumeIntegral() 等方法"
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
    
    result = check_random_usage(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
