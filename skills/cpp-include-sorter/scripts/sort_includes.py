#!/usr/bin/env python3
"""
Script to sort #include statements in C/C++ files.
Supports conditional compilation blocks (#ifdef/#ifndef/#if defined).
Organizes includes into 3 categories: corresponding header, system headers (<>), local headers ("").
"""
import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Any


class IncludeLine:
    """Represents an include line with its associated comments."""
    def __init__(self, line_num: int, line: str, before_comment: str = '', after_comment: str = ''):
        self.line_num = line_num
        self.original_line = line
        self.before_comment = before_comment
        self.after_comment = after_comment

    @property
    def full_line(self) -> str:
        if self.after_comment:
            if self.after_comment in self.original_line:
                return self.original_line
            return self.original_line.rstrip() + ' ' + self.after_comment
        return self.original_line


class IfDefBlock:
    """Represents a conditional compilation block containing includes."""
    def __init__(self, start_line: int, condition: str):
        self.start_line = start_line
        self.condition = condition
        self.includes: List[IncludeLine] = []
        self.end_line = -1
        self.else_if_blocks: List['IfDefBlock'] = []
        self.else_block: Optional['IfDefBlock'] = None

    def add_include(self, include: IncludeLine):
        self.includes.append(include)

    @property
    def all_includes(self) -> List[IncludeLine]:
        result = list(self.includes)
        for block in self.else_if_blocks:
            result.extend(block.all_includes)
        if self.else_block:
            result.extend(self.else_block.all_includes)
        return result


def extract_include_path(line: str) -> str:
    line_without_comment = line.split('//')[0] if '//' in line else line
    match = re.search(r'#include\s*[<"]([^>"]+)[>"]', line_without_comment)
    if match:
        return match.group(1).lower()
    return line.strip().lower()


def extract_include_path_from_obj(obj: IncludeLine) -> str:
    return extract_include_path(obj.original_line)


def get_corresponding_header(filepath: Path) -> Optional[str]:
    stem = filepath.stem
    return stem.lower()


def is_corresponding_header(line: str, header_name: str) -> bool:
    path = extract_include_path(line)
    filename = path.split('/')[-1].split('\\')[-1]
    filename_without_ext = filename.replace('.h', '')
    header_without_ext = header_name.replace('.h', '')
    return filename_without_ext == header_without_ext


def is_system_include(line: str) -> bool:
    return '<' in line


def extract_includes_with_ifdef(content: str) -> Tuple[int, int, List[Any]]:
    lines = content.split('\n')
    items = []
    include_start = -1
    include_end = -1
    i = 0
    ifdef_stack: List[IfDefBlock] = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('#if') or stripped.startswith('#ifndef'):
            if include_start == -1:
                include_start = i
            include_end = i
            block = IfDefBlock(i, stripped)
            ifdef_stack.append(block)
            items.append(block)
            i += 1
            continue

        if stripped.startswith('#elif'):
            if ifdef_stack:
                current = ifdef_stack[-1]
                elif_block = IfDefBlock(i, stripped)
                current.else_if_blocks.append(elif_block)
                ifdef_stack.pop()
                ifdef_stack.append(elif_block)
            i += 1
            continue

        if stripped.startswith('#else'):
            if ifdef_stack:
                current = ifdef_stack[-1]
                else_block = IfDefBlock(i, stripped)
                current.else_block = else_block
                ifdef_stack.pop()
                ifdef_stack.append(else_block)
            i += 1
            continue

        if stripped.startswith('#endif'):
            if ifdef_stack:
                block = ifdef_stack.pop()
                block.end_line = i
            include_end = i
            i += 1
            continue

        if stripped.startswith('#include'):
            if include_start == -1:
                include_start = i
            include_end = i

            inline_comment = ''
            if '//' in line:
                parts = line.split('//', 1)
                inline_comment = '//' + parts[1]

            before_comment = ''
            if i > 0:
                prev_line = lines[i - 1].strip()
                if prev_line.startswith('//') and not prev_line.startswith('///'):
                    before_comment = lines[i - 1]

            include_obj = IncludeLine(i, line, before_comment, inline_comment)

            if ifdef_stack:
                ifdef_stack[-1].add_include(include_obj)
            else:
                items.append(include_obj)

        elif include_start != -1:
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                if not ifdef_stack:
                    break
        i += 1

    return include_start, include_end, items


def format_ifdef_block(block: IfDefBlock) -> List[str]:
    result = []
    all_includes = block.all_includes

    if not all_includes:
        result.append(block.condition)
        result.append('#endif')
        return result

    system_includes = []
    local_includes = []

    for inc in all_includes:
        path = extract_include_path_from_obj(inc)
        if is_system_include(inc.original_line):
            system_includes.append((inc, path))
        else:
            local_includes.append((inc, path))

    system_includes.sort(key=lambda x: x[1])
    local_includes.sort(key=lambda x: x[1])

    result.append(block.condition)

    for inc, _ in system_includes:
        if inc.before_comment:
            result.append(inc.before_comment)
        result.append(inc.full_line)

    for inc, _ in local_includes:
        if inc.before_comment:
            result.append(inc.before_comment)
        result.append(inc.full_line)

    result.append('#endif')
    return result


def sort_includes_with_ifdef(items: List[Any], corresponding_header: Optional[str]) -> List[str]:
    corresponding_include = None
    corresponding_include_path_len = 0
    system_items = []
    local_items = []

    for item in items:
        if isinstance(item, IncludeLine):
            line = item.original_line
            path = extract_include_path_from_obj(item)

            if corresponding_header and is_corresponding_header(line, corresponding_header):
                path_len = len(path)
                if path_len > corresponding_include_path_len:
                    if corresponding_include is not None:
                        old_path = extract_include_path_from_obj(corresponding_include)
                        if is_system_include(corresponding_include.original_line):
                            system_items.append((corresponding_include, old_path, 'include'))
                        else:
                            local_items.append((corresponding_include, old_path, 'include'))
                    corresponding_include = item
                    corresponding_include_path_len = path_len
                else:
                    if is_system_include(line):
                        system_items.append((item, path, 'include'))
                    else:
                        local_items.append((item, path, 'include'))
                continue

            if is_system_include(line):
                system_items.append((item, path, 'include'))
            else:
                local_items.append((item, path, 'include'))

        elif isinstance(item, IfDefBlock):
            first_inc = item.all_includes[0] if item.all_includes else None
            if first_inc:
                path = extract_include_path_from_obj(first_inc)
                if is_system_include(first_inc.original_line):
                    system_items.append((item, path, 'ifdef'))
                else:
                    local_items.append((item, path, 'ifdef'))
            else:
                local_items.append((item, item.condition.lower(), 'ifdef'))

    system_items.sort(key=lambda x: x[1])
    local_items.sort(key=lambda x: x[1])

    result = []

    if corresponding_include:
        if corresponding_include.before_comment:
            result.append(corresponding_include.before_comment)
        result.append(corresponding_include.full_line)

    if system_items:
        if corresponding_include:
            result.append('')
        for item, _, item_type in system_items:
            if item_type == 'include':
                if item.before_comment:
                    result.append(item.before_comment)
                result.append(item.full_line)
            else:
                result.extend(format_ifdef_block(item))

    if local_items:
        if system_items or corresponding_include:
            result.append('')
        for item, _, item_type in local_items:
            if item_type == 'include':
                if item.before_comment:
                    result.append(item.before_comment)
                result.append(item.full_line)
            else:
                result.extend(format_ifdef_block(item))

    return result


def check_and_fix_file(filepath: Path, dry_run: bool = False) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    include_start, include_end, items = extract_includes_with_ifdef(content)

    if not items:
        return False

    corresponding_header = get_corresponding_header(filepath)
    sorted_includes = sort_includes_with_ifdef(items, corresponding_header)

    current_lines = []
    lines = content.split('\n')
    for item in items:
        if isinstance(item, IncludeLine):
            if item.before_comment:
                current_lines.append(item.before_comment)
            current_lines.append(item.full_line)
        elif isinstance(item, IfDefBlock):
            for i in range(item.start_line, item.end_line + 1):
                current_lines.append(lines[i])

    if current_lines == sorted_includes:
        return False

    new_lines = lines[:include_start] + sorted_includes + lines[include_end + 1:]
    new_content = '\n'.join(new_lines)

    if dry_run:
        print(f"Would fix: {filepath}")
        return True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Fixed: {filepath}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Sort #include statements in C/C++ files')
    parser.add_argument('directory', help='Directory containing files to sort')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without modifying files')
    parser.add_argument('--ext', default='.cpp', help='File extension to process (default: .cpp)')
    args = parser.parse_args()

    dir_path = Path(args.directory)

    if not dir_path.exists():
        print(f"Error: Directory {dir_path} does not exist")
        sys.exit(1)

    files_to_check = list(dir_path.glob(f'*{args.ext}'))

    if not files_to_check:
        print(f"No files with extension {args.ext} found in {dir_path}")
        sys.exit(0)

    print(f"Found {len(files_to_check)} files with extension {args.ext}")

    if args.dry_run:
        print("Running in dry-run mode...\n")

    fixed_count = 0
    for filepath in files_to_check:
        if check_and_fix_file(filepath, args.dry_run):
            fixed_count += 1

    if args.dry_run:
        print(f"\n{fixed_count} files would be fixed")
    else:
        print(f"\nFixed {fixed_count} files")


if __name__ == '__main__':
    main()
