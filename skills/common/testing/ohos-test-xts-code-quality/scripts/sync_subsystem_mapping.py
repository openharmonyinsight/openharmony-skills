#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""同步 subsystem_mapping.md 到 common.py 的 SUBSYSTEM_MAPPING 字典

用法:
    python sync_subsystem_mapping.py [--check] [--update]

--check: 仅检查差异，不更新
--update: 自动更新 common.py
"""

import re
import os
import sys
import argparse
from pathlib import Path


def parse_markdown_table(md_content):
    """解析 markdown 表格，提取目录-子系统映射"""
    mappings = {}
    
    for line in md_content.split('\n'):
        # 匹配表格行: | 目录 | 子系统 | 备注 |
        if line.startswith('|') and not line.startswith('| 目录'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3 and parts[1] and parts[2]:
                directory = parts[1]
                subsystem = parts[2]
                # 跳过空行和分隔行
                if directory and subsystem and directory != '------':
                    mappings[directory] = subsystem
    
    return mappings


def generate_python_dict(mappings):
    """生成 Python 字典代码块"""
    # 按长度降序排序，确保最长前缀优先匹配
    sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
    
    # 分组
    multi_level = [(k, v) for k, v in sorted_mappings if '/' in k]
    single_level = [(k, v) for k, v in sorted_mappings if '/' not in k]
    wifi_range = [(k, v) for k, v in sorted_mappings if k.startswith('communication/wifi_p') and k.endswith('p')]
    validator_subdirs = [(k, v) for k, v in sorted_mappings if k.startswith("validator/acts_validator/entry")]
    
    # 过滤掉 wifi_range（用 for 循环生成）和 validator_subdirs（单独处理）
    multi_level = [(k, v) for k, v in multi_level if not k.startswith('communication/wifi_p')]
    multi_level = [(k, v) for k, v in multi_level if not k.startswith("validator/acts_validator/entry")]
    
    lines = []
    lines.append("# ======================== SUBSYSTEM MAPPING ========================")
    lines.append("# Source: references/subsystem_mapping.md")
    lines.append("# Sync rule: Run sync_subsystem_mapping.py when subsystem_mapping.md changes")
    lines.append("")
    lines.append("SUBSYSTEM_MAPPING = {")
    
    # 多级目录（紧凑格式，每行多个）
    chunk_size = 4
    for i in range(0, len(multi_level), chunk_size):
        chunk = multi_level[i:i+chunk_size]
        line_parts = [f'"{k}": "{v}"' for k, v in chunk]
        lines.append("    " + ", ".join(line_parts) + ",")
    
    lines.append("}")
    
    # wifi_p3p ~ wifi_p40p
    lines.append("for _i in range(3, 41):")
    lines.append("    SUBSYSTEM_MAPPING[f\"communication/wifi_p{_i}p\"] = \"短距\"")
    
    # validator子目录映射
    if validator_subdirs:
        lines.append("")
        lines.append("# validator子目录映射（根据pages下的子目录判断子系统）")
        lines.append("SUBSYSTEM_MAPPING.update({")
        for k, v in validator_subdirs:
            lines.append(f'    "{k}": "{v}",')
        lines.append("})")
    
    # 单级目录（推断）
    lines.append("")
    lines.append("SUBSYSTEM_MAPPING.update({")
    for i in range(0, len(single_level), chunk_size):
        chunk = single_level[i:i+chunk_size]
        line_parts = [f'"{k}": "{v}"' for k, v in chunk]
        lines.append("    " + ", ".join(line_parts) + ",")
    lines.append("})")
    
    return '\n'.join(lines)


def update_common_py(py_path, new_mapping_block):
    """更新 common.py 中的 SUBSYSTEM_MAPPING 块"""
    with open(py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到映射块的开始和结束
    start_pattern = r'# ======================== SUBSYSTEM MAPPING ========================'
    end_pattern = r'SORTED_DIRS = sorted'
    
    start_match = re.search(start_pattern, content)
    end_match = re.search(end_pattern, content)
    
    if not start_match:
        print("错误: 无法找到 SUBSYSTEM MAPPING 注释块")
        return False
    
    if not end_match:
        print("错误: 无法找到 SORTED_DIRS 定义")
        return False
    
    start = start_match.start()
    end = end_match.start()
    
    # 替换内容
    new_content = content[:start] + new_mapping_block + "\n\n" + content[end:]
    
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    parser = argparse.ArgumentParser(description='同步 subsystem_mapping.md 到 common.py')
    parser.add_argument('--check', action='store_true', help='仅检查差异，不更新')
    parser.add_argument('--update', action='store_true', help='自动更新 common.py')
    args = parser.parse_args()
    
    # 获取路径
    script_dir = Path(__file__).parent
    md_path = script_dir.parent / 'references' / 'subsystem_mapping.md'
    py_path = script_dir / 'common.py'
    
    if not md_path.exists():
        print(f"错误: subsystem_mapping.md 不存在: {md_path}")
        sys.exit(1)
    
    if not py_path.exists():
        print(f"错误: common.py 不存在: {py_path}")
        sys.exit(1)
    
    # 解析 markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    md_mappings = parse_markdown_table(md_content)
    print(f"从 subsystem_mapping.md 解析到 {len(md_mappings)} 条映射")
    
    # 生成新的 Python 代码块
    new_code_block = generate_python_dict(md_mappings)
    
    if args.check:
        print("\n生成的代码预览:")
        print(new_code_block[:800] + "\n...")
        print(f"\n总计: {len(md_mappings)} 条映射")
        return
    
    if args.update:
        print(f"\n正在更新 {py_path}...")
        if update_common_py(py_path, new_code_block):
            print("✓ 更新成功")
        else:
            print("✗ 更新失败")
            sys.exit(1)
    else:
        print("\n请使用 --update 参数执行更新")


if __name__ == '__main__':
    main()