#!/usr/bin/env python3
"""
SDK API 存在性检查工具

验证工具 SDK 目录和源接口目录中是否存在指定的 API 声明文件。
适用于新增接口场景（Flow C），在生成测试前确认 SDK 是否已包含该接口。

用法:
    # 检查单个 API 文件
    python scripts/check_api_in_sdk.py --api text.d.ts
    python scripts/check_api_in_sdk.py --api component/text.d.ts
    python scripts/check_api_in_sdk.py --api @internal/component/ets/text.d.ts

    # 检查多个 API 文件
    python scripts/check_api_in_sdk.py --api text.d.ts button.d.ts

    # 指定 ETS 版本
    python scripts/check_api_in_sdk.py --api text.d.ts --ets-version ets1.1

    # 仅检查工具 SDK，不检查源接口
    python scripts/check_api_in_sdk.py --api text.d.ts --tool-only

    # 列出指定目录下所有 .d.ts 文件（探索模式）
    python scripts/check_api_in_sdk.py --list @internal/component/ets/

退出码:
    0 - 所有指定 API 均存在
    1 - 有 API 缺失或参数错误
"""

import argparse
import glob
import json
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(SCRIPT_DIR, '..')


def load_config():
    config_path = os.path.join(SKILL_ROOT, '.oh-xts-config.json')
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_tool_sdk_root(config):
    scan_tool_root = config.get('scan_tool_root', '')
    if scan_tool_root and os.path.isdir(scan_tool_root):
        return os.path.join(scan_tool_root, 'sdk', 'openharmony', 'ets')
    return os.path.join(SKILL_ROOT, 'APICoverageDetector', 'sdk', 'openharmony', 'ets')


def get_interface_path(config):
    # 兼容旧配置 sdk_path
    path = config.get('interface_path', '') or config.get('sdk_path', '')
    if not path:
        oh_root = config.get('OH_ROOT', '')
        if oh_root:
            path = os.path.join(oh_root, 'interface', 'sdk-js')
    return path


def find_api_in_tree(root, api_name):
    """在目录树中递归查找匹配 api_name 的文件。

    Args:
        root: 搜索根目录
        api_name: 文件名或相对路径（如 'text.d.ts' 或 'component/ets/text.d.ts'）

    Returns:
        list: 匹配的完整路径列表
    """
    matches = []
    # 去除前导路径分隔符
    api_name = api_name.lstrip('/').lstrip('\\')

    # 判断是纯文件名还是含路径的相对路径
    has_path_sep = '/' in api_name or '\\' in api_name

    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if has_path_sep:
                # 相对路径匹配：api_name 尾部必须匹配 rel_path 尾部
                rel = os.path.relpath(os.path.join(dirpath, fname), root).replace('\\', '/')
                if rel.endswith(api_name):
                    matches.append(os.path.join(dirpath, fname))
            else:
                # 纯文件名匹配：必须精确匹配文件名
                if fname == api_name:
                    matches.append(os.path.join(dirpath, fname))

    return matches


def check_api_in_tool_sdk(tool_sdk_root, api_name, ets_versions):
    """在工具 SDK 中检查 API 是否存在。

    Returns:
        dict: {version: {'found': bool, 'paths': [str]}}
    """
    result = {}
    for ver in ets_versions:
        ver_dir = os.path.join(tool_sdk_root, ver)
        if not os.path.isdir(ver_dir):
            result[ver] = {'found': False, 'paths': [], 'reason': f'版本目录不存在: {ver_dir}'}
            continue

        matches = find_api_in_tree(ver_dir, api_name)
        result[ver] = {'found': len(matches) > 0, 'paths': matches}

    return result


def check_api_in_interface(interface_path, api_name):
    """在源接口目录中检查 API 是否存在。

    Returns:
        dict: {'found': bool, 'paths': [str]}
    """
    if not interface_path or not os.path.isdir(interface_path):
        return {'found': False, 'paths': [], 'reason': f'源接口目录不存在: {interface_path}'}

    matches = find_api_in_tree(interface_path, api_name)
    return {'found': len(matches) > 0, 'paths': matches}


def list_api_files(root, sub_dir='', ext='.d.ts'):
    """列出指定目录下所有匹配扩展名的文件。"""
    search_dir = os.path.join(root, sub_dir) if sub_dir else root
    if not os.path.isdir(search_dir):
        return []

    results = []
    for dirpath, _dirnames, filenames in os.walk(search_dir):
        for fname in filenames:
            if fname.endswith(ext):
                rel = os.path.relpath(os.path.join(dirpath, fname), root).replace('\\', '/')
                results.append(rel)
    return sorted(results)


def main():
    parser = argparse.ArgumentParser(
        description='SDK API 存在性检查工具 — 验证工具 SDK 和源接口中是否存在指定 API'
    )
    parser.add_argument('--api', nargs='+', help='API 文件名或相对路径（如 text.d.ts, component/text.d.ts）')
    parser.add_argument('--ets-version', nargs='*', default=None,
                        help='ETS 版本（如 ets1.1 ets1.2），默认从配置读取')
    parser.add_argument('--tool-only', action='store_true',
                        help='仅检查工具 SDK 目录，不检查源接口目录')
    parser.add_argument('--list', metavar='SUBDIR', default=None,
                        help='列出指定子目录下的所有 API 文件（探索模式）')
    parser.add_argument('--json', action='store_true', dest='json_output',
                        help='以 JSON 格式输出结果')

    args = parser.parse_args()
    config = load_config()
    ets_versions = args.ets_version or config.get('ets_version', ['ets1.1'])
    tool_sdk_root = get_tool_sdk_root(config)
    interface_path = get_interface_path(config)

    # 探索模式：列出 API 文件
    if args.list:
        sub_dir = args.list
        print(f"[LIST] 工具 SDK 中的 API 文件 ({sub_dir}):")
        print(f"  根目录: {tool_sdk_root}")
        for ver in ets_versions:
            files = list_api_files(os.path.join(tool_sdk_root, ver), sub_dir)
            print(f"\n  === {ver} ({len(files)} 个文件) ===")
            for f in files[:50]:
                print(f"    {f}")
            if len(files) > 50:
                print(f"    ... 还有 {len(files) - 50} 个文件")

        if not args.tool_only:
            print(f"\n  === 源接口目录 ({sub_dir}) ===")
            files = list_api_files(interface_path, sub_dir)
            print(f"  {interface_path} ({len(files)} 个文件)")
            for f in files[:50]:
                print(f"    {f}")
            if len(files) > 50:
                print(f"    ... 还有 {len(files) - 50} 个文件")
        return 0

    # 常规模式：检查指定 API
    if not args.api:
        parser.print_help()
        return 1

    all_found = True
    results = {}

    for api_name in args.api:
        api_result = {'api': api_name, 'tool_sdk': {}, 'interface': {}}

        # 检查工具 SDK
        tool_result = check_api_in_tool_sdk(tool_sdk_root, api_name, ets_versions)
        api_result['tool_sdk'] = tool_result

        # 检查源接口
        if not args.tool_only:
            iface_result = check_api_in_interface(interface_path, api_name)
            api_result['interface'] = iface_result

        results[api_name] = api_result

        # 判断是否缺失
        tool_all_found = all(v['found'] for v in tool_result.values())
        iface_found = api_result.get('interface', {}).get('found', True)

        if not tool_all_found or not iface_found:
            all_found = False

    # 输出
    if args.json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        _print_results(results, ets_versions, tool_only=args.tool_only)

    return 0 if all_found else 1


def _print_results(results, ets_versions, tool_only=False):
    """人类可读的结果输出。"""
    for api_name, api_result in results.items():
        print(f"\n{'='*60}")
        print(f"API: {api_name}")
        print(f"{'='*60}")

        # 工具 SDK 状态
        print(f"\n  工具 SDK:")
        for ver in ets_versions:
            ver_result = api_result['tool_sdk'].get(ver, {})
            if ver_result.get('found'):
                paths = ver_result['paths']
                print(f"    {ver}: ✅ 找到 ({len(paths)} 处)")
                for p in paths[:5]:
                    print(f"      → {p}")
                if len(paths) > 5:
                    print(f"      ... 还有 {len(paths) - 5} 处")
            else:
                reason = ver_result.get('reason', '未找到')
                print(f"    {ver}: ❌ {reason}")

        # 源接口状态
        if not tool_only:
            iface_result = api_result.get('interface', {})
            if iface_result.get('found'):
                paths = iface_result['paths']
                print(f"\n  源接口 (interface_path): ✅ 找到 ({len(paths)} 处)")
                for p in paths[:5]:
                    print(f"    → {p}")
            else:
                reason = iface_result.get('reason', '未找到')
                print(f"\n  源接口 (interface_path): ❌ {reason}")

        # 建议
        tool_ok = all(v.get('found') for v in api_result['tool_sdk'].values())
        if not tool_ok:
            print(f"\n  💡 建议: 工具 SDK 中缺失该 API，执行以下命令更新:")
            print(f"     python scripts/manage_scan_env.py update-sdk --force")


if __name__ == '__main__':
    sys.exit(main())
