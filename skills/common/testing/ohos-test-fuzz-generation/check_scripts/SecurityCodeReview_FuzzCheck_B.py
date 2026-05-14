#!/usr/bin/env python3
"""
规则B: BUILD.gn格式验证
检查BUILD.gn文件是否使用正确的模板和参数
"""

import re
import os


def check_build_gn(content):
    """
    规则B: 检查BUILD.gn格式
    - 必须使用 ohos_fuzztest() 模板
    - 必须包含 fuzz_config_file 参数
    - fuzz_config_file 路径必须以 // 开头
    - 必须包含 group("fuzztest") 部分
    - group("fuzztest") 中的 deps 与 ohos_fuzztest 目标名一致
    """
    errors = []
    target_name = None
    if "ohos_fuzztest(" not in content:
        if "ohos_fuzz_test(" in content:
            errors.append("规则B: 使用了旧版 ohos_fuzz_test()，应改为 ohos_fuzztest()")
        else:
            errors.append("规则B: BUILD.gn 必须使用 ohos_fuzztest() 模板")
    else:
        target_match = re.search(r'ohos_fuzztest\(\s*"([^"]+)"', content)
        if target_match:
            target_name = target_match.group(1)

    if "fuzz_config_file" not in content:
        if "fuzz_config" in content:
            errors.append("规则B: 使用了 fuzz_config，应改为 fuzz_config_file")
        else:
            errors.append("规则B: BUILD.gn 必须包含 fuzz_config_file 参数")
    else:
        config_match = re.search(r'fuzz_config_file\s*=\s*"([^"]+)"', content)
        if config_match:
            config_path = config_match.group(1)
            if not (config_path.startswith("//") or config_path.startswith("./") or config_path.startswith("../")):
                errors.append("规则B: fuzz_config_file 路径应以 // 或相对路径(./../)开头")

    if 'group("fuzztest")' not in content:
        errors.append('规则B: BUILD.gn 必须包含 group("fuzztest") 部分')
    elif target_name:
        # 检查 deps 是否包含 ohos_fuzztest 目标名
        group_match = re.search(
            r'group\(\s*"fuzztest"\s*\)\s*\{([^}]*)\}', content, re.DOTALL
        )
        if group_match:
            group_body = group_match.group(1)
            if target_name not in group_body:
                errors.append(
                    f"规则B: group(\"fuzztest\") 中的 deps 应包含 ohos_fuzztest 目标名 '{target_name}'"
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
    
    result = check_build_gn(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
