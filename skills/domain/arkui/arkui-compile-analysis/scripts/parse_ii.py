#!/usr/bin/env python3

import re
import argparse
from collections import defaultdict

def parse_ii_file(file_path):
    file_include_pattern = re.compile(r'#\s*\d+\s+"([^"]+)"')
    target_prefix = "foundation/arkui/"
    dependencies = []
    stack = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = file_include_pattern.match(line)
            if match:
                new_file = match.group(1)
                if target_prefix in new_file:
                    if new_file in stack:
                        index = stack.index(new_file)
                        dependencies.append(stack[:index + 1])
                        stack = stack[:index]
                    stack.append(new_file)

    if stack:
        dependencies.append(stack)

    return dependencies

def build_tree_structure(dependencies):
    tree = {}
    for path in dependencies:
        current_level = tree
        for file in path:
            if file not in current_level:
                current_level[file] = {}
            current_level = current_level[file]
    return tree

def print_tree(tree, prefix='', is_last=True, output_file=None):
    items = list(tree.items())
    count = len(items)
    for i, (file, subtree) in enumerate(items):
        connector = '└──' if i == count - 1 else '├──'
        new_prefix = prefix + ('    ' if i == count - 1 else '│   ')

        line = prefix + connector + ' ' + file
        print(line)

        # 如果指定了输出文件，写入文件
        if output_file:
            output_file.write(line + '\n')

        # 递归处理子节点
        print_tree(subtree, new_prefix, is_last=i == count - 1, output_file=output_file)

def main(file_path, output_path=None):
    dependencies = parse_ii_file(file_path)
    tree = build_tree_structure(dependencies)

    header = "头文件的依赖关系树："
    print(header)

    output_file = None
    if output_path:
        output_file = open(output_path, 'w', encoding='utf-8')
        output_file.write(header + '\n')

    try:
        print_tree(tree, output_file=output_file)
    finally:
        if output_file:
            output_file.close()
            print(f"\n✓ 依赖树已保存到: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='解析 .ii 文件并显示头文件依赖关系树。')
    parser.add_argument('file', type=str, help='要解析的 .ii 文件路径')
    parser.add_argument('--output', '-o', type=str, help='保存依赖树到指定文件（可选）')
    args = parser.parse_args()

    # 如果指定了输出文件路径，使用该路径；否则输出到控制台
    output_path = args.output if args.output else None
    main(args.file, output_path)
