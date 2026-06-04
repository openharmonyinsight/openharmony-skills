#!/usr/bin/env python3

import re
import argparse

# .ii line marker format: # linenum "filename" [flags]
# Flags (from GCC/Clang preprocessor output):
#   1 = entering a new file (#include)
#   2 = returning to this file (after an include)
#   3 = following text comes from a system header (externally generated)
#   4 = returning to a file that should not be re-exported
# A line may have multiple flags (e.g., "3 4" or no flags at all).
LINE_MARKER_RE = re.compile(r'^#\s*(\d+)\s+"([^"]+)"(?:\s+(\d+(?:\s+\d+)*))?$')


def parse_ii_file(file_path, target_prefix="foundation/arkui/"):
    dependencies = []
    stack = []
    guard_depth = 0  # tracks include-guard re-entries we skipped

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = LINE_MARKER_RE.match(line)
            if not match:
                continue

            filename = match.group(2)
            flags_str = match.group(3) or ""
            flags = set(int(x) for x in flags_str.split()) if flags_str.strip() else set()

            if 1 in flags:
                if filename in stack:
                    # Re-entering a file already in stack (include guard)
                    guard_depth += 1
                else:
                    # Entering a new file (push)
                    stack.append(filename)
                    if target_prefix in filename:
                        filtered = [p for p in stack if target_prefix in p]
                        if filtered:
                            dependencies.append(list(filtered))
            elif 2 in flags or (3 in flags and 4 in flags):
                if guard_depth > 0 and filename in stack:
                    # Return matching a guard re-entry we skipped — no-op
                    guard_depth -= 1
                elif stack and stack[-1] == filename:
                    stack.pop()
                elif filename in stack:
                    # Pop back to this file (handles skipped intermediaries)
                    idx = stack.index(filename)
                    stack = stack[:idx + 1]

    return dependencies


def build_tree_structure(dependencies):
    tree = {}
    for path in dependencies:
        current = tree
        for f in path:
            if f not in current:
                current[f] = {}
            current = current[f]
    return tree


def print_tree(tree, prefix='', output_file=None):
    items = list(tree.items())
    for i, (name, subtree) in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = '└── ' if is_last else '├── '
        new_prefix = prefix + ('    ' if is_last else '│   ')
        line = prefix + connector + name
        print(line)
        if output_file:
            output_file.write(line + '\n')
        print_tree(subtree, new_prefix, output_file)


def main(file_path, output_path=None):
    dependencies = parse_ii_file(file_path)
    tree = build_tree_structure(dependencies)

    header = "Header dependency tree:"
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
            print(f"\nDependency tree saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse .ii file and display header dependency tree.')
    parser.add_argument('file', type=str, help='Path to .ii file')
    parser.add_argument('--output', '-o', type=str, help='Save dependency tree to file')
    args = parser.parse_args()
    main(args.file, args.output)
