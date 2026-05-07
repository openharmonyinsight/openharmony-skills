#!/usr/bin/env python3
"""
APICoverageDetector 扫描环境管理工具

将子系统测试文件和 SDK 文件复制到扫描工具目录，并管理 arkts_config.json 配置。
APICoverageDetector 不支持扫描 junction 链接目录，因此使用文件复制方式。

用法：
    python scripts/manage_scan_env.py setup --subsystem multimedia
    python scripts/manage_scan_env.py teardown --subsystem multimedia
    python scripts/manage_scan_env.py status
"""

import json
import os
import shutil
import subprocess
import sys
import argparse
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(SCRIPT_DIR, '..')


def load_global_config():
    config_path = os.path.join(SKILL_ROOT, '.oh-xts-config.json')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_scan_tool_root():
    config = load_global_config()
    scan_tool_root = config.get('scan_tool_root', '')
    if scan_tool_root and os.path.isdir(scan_tool_root):
        return scan_tool_root
    return os.path.join(SKILL_ROOT, 'APICoverageDetector')


CASE_ROOT = os.path.join(get_scan_tool_root(), 'testcase')
SDK_ROOT = os.path.join(get_scan_tool_root(), 'sdk', 'openharmony', 'ets')
ARKTS_CONFIG_PATH = os.path.join(get_scan_tool_root(), 'configs', 'arkts_config.json')


def load_arkts_config():
    if not os.path.exists(ARKTS_CONFIG_PATH):
        raise FileNotFoundError(f"arkts_config.json 不存在: {ARKTS_CONFIG_PATH}")
    with open(ARKTS_CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_arkts_config(config):
    with open(ARKTS_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def backup_arkts_config():
    backup_path = ARKTS_CONFIG_PATH + '.bak'
    shutil.copy2(ARKTS_CONFIG_PATH, backup_path)
    return backup_path


def get_dir_size(path):
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def copy_directory_with_progress(src, dst, label=""):
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)

    if os.path.exists(dst):
        print(f"  [SKIP] 目标目录已存在: {dst}")
        return True

    if not os.path.exists(src):
        print(f"  [ERROR] 源目录不存在: {src}")
        return False

    src_size = get_dir_size(src)
    print(f"  [INFO] 源目录大小: {format_size(src_size)}")

    if label:
        print(f"  [COPY] {label}: {src} -> {dst}")
    else:
        print(f"  [COPY] {src} -> {dst}")

    try:
        shutil.copytree(src, dst, copy_function=shutil.copy2)
    except Exception as e:
        print(f"  [ERROR] 复制失败: {e}")
        if os.path.exists(dst):
            print(f"  [CLEANUP] 清理不完整的副本...")
            shutil.rmtree(dst, ignore_errors=True)
        return False

    print(f"  [OK] 复制完成: {dst}")
    return True


def _rename_sdk_dirs(sdk_root):
    rename_map = {'dynamic': 'ets1.1', 'static': 'ets1.2'}
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(sdk_root, old_name)
        new_path = os.path.join(sdk_root, new_name)
        if os.path.isdir(old_path) and not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"  [RENAME] {old_name}/ -> {new_name}/ (APICoverageDetector requires ets1.1/ets1.2 naming)")


def remove_copied_directory(path):
    path = os.path.normpath(path)

    if not os.path.exists(path):
        print(f"  [SKIP] 目录不存在: {path}")
        return

    try:
        shutil.rmtree(path)
        print(f"  [OK] 已删除副本: {path}")
    except Exception as e:
        print(f"  [ERROR] 删除失败: {e}")


def setup(subsystem):
    print(f"[SETUP] 准备扫描环境，子系统: {subsystem}")

    config = load_global_config()

    if sys.platform == 'win32':
        xts_acts_path = config.get('for_windows', {}).get('xts_acts_path', '')
        sdk_path = config.get('for_windows', {}).get('sdk_path', '')
    else:
        xts_acts_path = ''
        sdk_path = ''

    if not xts_acts_path:
        oh_root = config.get('for_linux', {}).get('OH_ROOT', '')
        if oh_root:
            xts_acts_path = os.path.join(oh_root, 'test', 'xts', 'acts')

    if not xts_acts_path:
        raise ValueError("xts_acts_path not found in config")

    filtered_dir = os.path.join(CASE_ROOT, f'xts_acts_filtered_{subsystem}')
    subsystem_source = os.path.join(xts_acts_path, subsystem)
    subsystem_copy = os.path.join(filtered_dir, subsystem)

    os.makedirs(filtered_dir, exist_ok=True)
    print(f"  过滤目录: {filtered_dir}")

    if not os.path.exists(subsystem_source):
        print(f"  [WARN] 子系统源路径不存在: {subsystem_source}")
        print(f"         继续执行（用户可能提供替代路径）")
    else:
        print(f"  子系统源路径: {subsystem_source}")

    ok = copy_directory_with_progress(subsystem_source, subsystem_copy, label="子系统测试文件")
    if not ok:
        print("[ERROR] 子系统测试文件复制失败")
        return False

    if sdk_path:
        sdk_ets_path = os.path.join(sdk_path, 'ets') if not sdk_path.endswith('ets') else sdk_path
        ok = copy_directory_with_progress(sdk_ets_path, SDK_ROOT, label="SDK 文件")
        if not ok:
            print("[WARN] SDK 文件复制失败，扫描可能使用已有 SDK 数据")
        else:
            _rename_sdk_dirs(SDK_ROOT)

    backup_arkts_config()
    print(f"  [OK] 已备份 arkts_config.json")

    arkts_config = load_arkts_config()
    arkts_config['case_path'] = arkts_config.get('case_path', {})
    arkts_config['case_path']['open_source'] = [f'xts_acts_filtered_{subsystem}']
    save_arkts_config(arkts_config)
    print(f"  [OK] 已更新 arkts_config.json -> case_path: ['xts_acts_filtered_{subsystem}']")

    print(f"\n[DONE] 扫描环境已就绪: {subsystem}")
    return True


def teardown(subsystem):
    print(f"[TEARDOWN] 恢复扫描环境，子系统: {subsystem}")

    filtered_dir = os.path.join(CASE_ROOT, f'xts_acts_filtered_{subsystem}')
    subsystem_copy = os.path.join(filtered_dir, subsystem)

    remove_copied_directory(subsystem_copy)

    if os.path.exists(filtered_dir):
        try:
            os.rmdir(filtered_dir)
            print(f"  [OK] 已删除过滤目录: {filtered_dir}")
        except OSError:
            print(f"  [WARN] 过滤目录非空，跳过删除: {filtered_dir}")

    backup_path = ARKTS_CONFIG_PATH + '.bak'
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, ARKTS_CONFIG_PATH)
        print(f"  [OK] 已从备份恢复 arkts_config.json")
    else:
        arkts_config = load_arkts_config()
        arkts_config['case_path'] = arkts_config.get('case_path', {})
        arkts_config['case_path']['open_source'] = ['xts_acts']
        save_arkts_config(arkts_config)
        print(f"  [OK] 已重置 arkts_config.json -> case_path: ['xts_acts']")

    print(f"\n[DONE] 扫描环境已恢复: {subsystem}")
    return True


def status():
    print("[STATUS] 当前扫描环境状态")

    arkts_config = load_arkts_config()
    case_paths = arkts_config.get('case_path', {}).get('open_source', [])
    print(f"  arkts_config.json case_path: {case_paths}")
    print(f"  ets_version: {arkts_config.get('ets_version', [])}")

    for cp in case_paths:
        full_path = os.path.join(CASE_ROOT, cp)
        if os.path.exists(full_path):
            entries = os.listdir(full_path)
            print(f"  {cp}: 存在 ({len(entries)} 个条目)")
            for entry in entries:
                entry_path = os.path.join(full_path, entry)
                if os.path.isdir(entry_path):
                    size = get_dir_size(entry_path)
                    print(f"    -> {entry} (目录, {format_size(size)})")
                else:
                    print(f"    -> {entry} (文件)")
        else:
            print(f"  {cp}: 不存在")

    if os.path.exists(SDK_ROOT):
        size = get_dir_size(SDK_ROOT)
        print(f"  SDK 路径: {SDK_ROOT} ({format_size(size)})")
    else:
        print(f"  SDK 路径: {SDK_ROOT} (不存在)")


def main():
    parser = argparse.ArgumentParser(
        description='管理 APICoverageDetector 扫描环境（文件复制 + arkts_config.json 配置）'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    setup_parser = subparsers.add_parser('setup', help='复制子系统文件到扫描目录并配置环境')
    setup_parser.add_argument('--subsystem', required=True, help='目标子系统名称（如 multimedia, ability）')

    teardown_parser = subparsers.add_parser('teardown', help='删除已复制的文件并恢复配置')
    teardown_parser.add_argument('--subsystem', required=True, help='要清理的子系统名称')

    subparsers.add_parser('status', help='显示当前扫描环境状态')

    args = parser.parse_args()

    try:
        if args.command == 'setup':
            ok = setup(args.subsystem)
            return 0 if ok else 1
        elif args.command == 'teardown':
            ok = teardown(args.subsystem)
            return 0 if ok else 1
        elif args.command == 'status':
            status()
            return 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
