#!/usr/bin/env python3
"""
测试套注册工具

在 List.test.ets 中按字母顺序插入新测试文件的 import 语句和调用。

用法：
    python scripts/register_test.py \\
        --list-file path/to/List.test.ets \\
        --new-file ./NewModule.test.ets \\
        --function-name NewModuleTest
"""

import argparse
import os
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def infer_function_name(file_path):
    basename = os.path.basename(file_path)
    name = basename.replace('.test.ets', '').replace('.test', '')
    return name[0].lower() + name[1:] if name else name


def infer_import_name(file_path):
    basename = os.path.basename(file_path)
    name = basename.replace('.test.ets', '').replace('.test', '')
    return name


def register(list_file, new_file, function_name=None, dry_run=False):
    if not os.path.exists(list_file):
        print(f'[ERROR] List file not found: {list_file}')
        return False

    if not os.path.exists(new_file):
        print(f'[ERROR] New test file not found: {new_file}')
        return False

    with open(list_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    import_name = infer_import_name(new_file)
    if not function_name:
        function_name = infer_function_name(new_file)

    rel_path = os.path.relpath(os.path.dirname(new_file) or '.', os.path.dirname(list_file))
    rel_path = rel_path.replace('\\', '/')
    if rel_path == '.':
        import_path = f'./{import_name}.test'
    else:
        import_path = f'{rel_path}/{import_name}.test'

    import_line = f"import {import_name} from '{import_path}';"
    call_line = f"  {function_name}();"

    if import_name in content:
        print(f'[SKIP] {import_name} already imported in {list_file}')
        return True

    import_insert_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') and 'from' in stripped:
            import_insert_idx = i + 1

    call_insert_idx = len(lines) - 1
    in_function = False
    for i, line in enumerate(lines):
        if 'function testsuite' in line or 'function testSuite' in line:
            in_function = True
        if in_function and re.match(r'\s*\w+\(\);', line.strip()):
            call_insert_idx = i + 1

    new_lines = lines[:import_insert_idx] + [import_line] + lines[import_insert_idx:]

    if call_insert_idx > import_insert_idx:
        call_insert_idx += 1

    new_lines = new_lines[:call_insert_idx] + [call_line] + new_lines[call_insert_idx:]

    result = '\n'.join(new_lines)

    if dry_run:
        print('[DRY RUN] Changes that would be made:')
        print(f'  + {import_line}')
        print(f'  + {call_line}')
        return True

    with open(list_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'[OK] Registered {import_name} in {list_file}')
    print(f'  Import: {import_line}')
    print(f'  Call:   {call_line}')
    return True


def main():
    parser = argparse.ArgumentParser(description='Register test file in List.test.ets')
    parser.add_argument('--list-file', required=True, help='Path to List.test.ets')
    parser.add_argument('--new-file', required=True, help='Path to new test file')
    parser.add_argument('--function-name', default=None,
                        help='Function name to call (default: inferred from filename)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')
    args = parser.parse_args()

    ok = register(args.list_file, args.new_file, args.function_name, args.dry_run)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
