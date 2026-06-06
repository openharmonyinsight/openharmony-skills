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


def is_wsl():
    try:
        if sys.platform == 'linux' and os.path.exists('/proc/version'):
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower()
    except Exception:
        pass
    return False


def win_path_to_wsl(win_path):
    if not win_path:
        return win_path
    win_path = win_path.replace('\\', '/')
    if len(win_path) >= 2 and win_path[1] == ':':
        drive = win_path[0].lower()
        return f'/mnt/{drive}{win_path[2:]}'
    return win_path


def wsl_path_to_win(wsl_path):
    if not wsl_path:
        return wsl_path
    if wsl_path.startswith('/mnt/') and len(wsl_path) > 5:
        drive = wsl_path[5].upper()
        rest = wsl_path[6:].replace('/', '\\')
        return f'{drive}:{rest}'
    return wsl_path


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


def get_dir_size(path, timeout=5):
    import threading
    result = [0]
    def _calc():
        total = 0
        for dirpath, _dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
            result[0] = total
    t = threading.Thread(target=_calc, daemon=True)
    t.start()
    t.join(timeout=timeout)
    if t.is_alive():
        return -1
    return result[0]


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def _copy_via_system(src, dst):
    """使用系统 cp -r 命令复制，比 shutil.copytree 快 5-8 倍（尤其跨 FS 场景）"""
    if sys.platform == 'win32':
        cmd = ['xcopy', src, dst, '/E', '/I', '/Y', '/Q']
    else:
        cmd = ['cp', '-r', src, dst]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(f"cp failed (rc={result.returncode}): {result.stderr}")


def _merge_dir_contents(src, dst):
    """将 src 目录内容合并到 dst 目录（不覆盖已存在文件）"""
    if sys.platform == 'win32':
        cmd = ['xcopy', src, dst, '/E', '/I', '/Y', '/Q']
    else:
        cmd = ['cp', '-rn', os.path.join(src, '.'), dst]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(f"merge failed (rc={result.returncode}): {result.stderr}")


def _copy_file_via_system(src, dst):
    """复制单个文件"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if sys.platform == 'win32':
        cmd = ['copy', '/Y', src, dst]
    else:
        cmd = ['cp', src, dst]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"cp failed (rc={result.returncode}): {result.stderr}")


def copy_directory_with_progress(src, dst, label=""):
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)

    if not os.path.exists(src):
        print(f"  [ERROR] 源目录不存在: {src}")
        return False

    is_dir = os.path.isdir(src)
    src_size = get_dir_size(src) if is_dir else os.path.getsize(src)
    size_str = format_size(src_size) if src_size >= 0 else "计算超时"
    print(f"  [INFO] 源大小: {size_str}")

    if label:
        print(f"  [COPY] {label}: {src} -> {dst}")
    else:
        print(f"  [COPY] {src} -> {dst}")

    try:
        if is_dir:
            if os.path.exists(dst):
                print(f"  [INFO] 目标已存在，增量合并: {dst}")
                _merge_dir_contents(src, dst)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                _copy_via_system(src, dst)
        else:
            _copy_file_via_system(src, dst)
    except Exception as e:
        print(f"  [ERROR] 复制失败: {e}")
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


def _resolve_paths(config):
    """解析配置文件中的路径。

    Returns:
        tuple: (xts_acts_path, interface_path, sdk_local_path, env_label)
            - xts_acts_path: XTS 测试仓库路径
            - interface_path: 源接口声明目录（编译前的 .d.ts 文件），用于 API 解析
            - sdk_local_path: 编译后的 SDK 产物目录，用于复制到扫描工具。
              结构说明：
                - 首次编译动态内容：扁平结构（直接含 api/、component/ 等）
                  → 对应扫描工具 sdk/openharmony/ets/ets1.1/
                - 首次编译静态内容：含 dynamic/ + static/ 子目录
                  → dynamic/ 对应 ets1.1/，static/ 对应 ets1.2/
            - env_label: 运行环境标识
    """
    platform_val = config.get('platform', '').lower()
    oh_root = config.get('OH_ROOT', '')
    env_label = platform_val or 'unknown'

    # XTS 测试仓库路径
    xts_acts_path = config.get('xts_acts_path', '')
    if not xts_acts_path and oh_root:
        xts_acts_path = os.path.join(oh_root, 'test', 'xts', 'acts')

    # 源接口声明路径（编译前，含 .d.ts 声明文件）
    # 兼容旧配置：先读 interface_path，不存在则回退读 sdk_path
    interface_path = config.get('interface_path', '') or config.get('sdk_path', '')
    if not interface_path and oh_root:
        interface_path = os.path.join(oh_root, 'interface', 'sdk-js')

    # 编译后的 SDK 产物路径（始终解析，供 update-sdk 和自动检查使用）
    sdk_local_path = config.get('sdk_local_path', '')
    if not sdk_local_path and oh_root:
        ets_version = config.get('ets_version', ['ets1.1'])
        ver_num = ets_version[0].replace('ets', '') if ets_version else '1.1'
        sdk_local_path = os.path.join(oh_root, 'prebuilts', 'ohos-sdk', 'linux', ver_num, 'ets')

    return xts_acts_path, interface_path, sdk_local_path, env_label


def setup(subsystem, module=None):
    print(f"[SETUP] 准备扫描环境，子系统: {subsystem}" + (f"，模块: {module}" if module else ""))

    config = load_global_config()
    xts_acts_path, _interface_path, sdk_local_path, env_label = _resolve_paths(config)
    ets_versions = config.get('ets_version', ['ets1.1'])
    print(f"  运行环境: {env_label}")

    if not xts_acts_path:
        raise ValueError("xts_acts_path not found in config (set xts_acts_path or OH_ROOT in .oh-xts-config.json)")

    filtered_dir = os.path.join(CASE_ROOT, f'xts_acts_filtered_{subsystem}')
    os.makedirs(filtered_dir, exist_ok=True)
    print(f"  过滤目录: {filtered_dir}")

    if module:
        module_parts = module.strip('/').split('/')
        module_source = os.path.join(xts_acts_path, subsystem, *module_parts)
        module_copy = os.path.join(filtered_dir, subsystem, *module_parts)

        if not os.path.exists(module_source):
            print(f"  [ERROR] 模块源路径不存在: {module_source}")
            return False
        print(f"  模块源路径: {module_source}")

        module_size = get_dir_size(module_source)
        print(f"  [INFO] 模块大小: {format_size(module_size)}")

        ok = copy_directory_with_progress(module_source, module_copy, label="模块测试文件")
        if not ok:
            print("[ERROR] 模块测试文件复制失败")
            return False
    else:
        subsystem_source = os.path.join(xts_acts_path, subsystem)
        subsystem_copy = os.path.join(filtered_dir, subsystem)

        if not os.path.exists(subsystem_source):
            print(f"  [WARN] 子系统源路径不存在: {subsystem_source}")
            if is_wsl():
                win_style = wsl_path_to_win(subsystem_source)
                print(f"         Windows 等效路径: {win_style}")
                print(f"         提示：检查该路径在 Windows 侧是否存在，以及 WSL /mnt 挂载是否正常")
            print(f"         继续执行（用户可能提供替代路径）")
        else:
            print(f"  子系统源路径: {subsystem_source}")

        ok = copy_directory_with_progress(subsystem_source, subsystem_copy, label="子系统测试文件")
        if not ok:
            print("[ERROR] 子系统测试文件复制失败")
            return False

    # 自动检查工具 SDK 目录完整性，缺失则从 sdk_local_path 复制
    _ensure_sdk_available(sdk_local_path, ets_versions)

    # 一次性备份 + 修改 arkts_config.json（ets_version + case_path）
    # 注意：所有对 arkts_config.json 的修改集中在此处，避免多处备份互相覆盖
    backup_arkts_config()
    print(f"  [OK] 已备份 arkts_config.json -> arkts_config.json.bak")

    arkts_config = load_arkts_config()

    # 同步 ets_version（从 .oh-xts-config.json → arkts_config.json）
    old_ets_version = arkts_config.get('ets_version', [])
    arkts_config['ets_version'] = ets_versions
    print(f"  [OK] ets_version: {old_ets_version} -> {ets_versions}")

    # 更新 case_path（指向过滤目录）
    arkts_config['case_path'] = arkts_config.get('case_path', {})
    arkts_config['case_path']['open_source'] = [f'xts_acts_filtered_{subsystem}']
    print(f"  [OK] case_path: ['xts_acts_filtered_{subsystem}']")

    save_arkts_config(arkts_config)

    scope = f"{subsystem}/{module}" if module else subsystem
    print(f"\n[DONE] 扫描环境已就绪: {scope}")
    return True


def _ensure_sdk_available(sdk_local_path, ets_versions):
    """自动检查工具 SDK 目录完整性，缺失则从 sdk_local_path 复制。

    检查逻辑：
    1. 对 ets_versions 中每个版本，检查 {SDK_ROOT}/{version}/ 是否存在且非空
    2. 缺失 → 从 sdk_local_path 复制对应版本
    3. 全部存在 → 打印状态，跳过复制
    """
    print(f"\n  [SDK-CHECK] 检查工具 SDK 目录完整性...")

    missing_versions = []
    for ver in ets_versions:
        ver_dir = os.path.join(SDK_ROOT, ver)
        if not os.path.isdir(ver_dir) or not os.listdir(ver_dir):
            missing_versions.append(ver)
            print(f"    {ver}: ❌ 缺失")
        else:
            print(f"    {ver}: ✅ 存在")

    if not missing_versions:
        print(f"  [SDK-CHECK] 所有版本齐全，无需复制")
        return

    if not sdk_local_path:
        print(f"  [SDK-CHECK] ⚠️  以下版本缺失 {missing_versions}，但 sdk_local_path 未配置，无法自动补充")
        print(f"  [SDK-CHECK] 请手动执行: python manage_scan_env.py update-sdk")
        return

    if not os.path.exists(sdk_local_path):
        print(f"  [SDK-CHECK] ⚠️  sdk_local_path 不存在: {sdk_local_path}，无法自动补充")
        return

    print(f"  [SDK-CHECK] 自动补充缺失版本: {missing_versions}")
    _copy_sdk_versions(sdk_local_path, missing_versions)


def _copy_sdk_versions(sdk_local_path, versions, force=False):
    """将指定版本的 SDK 从 sdk_local_path 复制到工具目录。

    Args:
        sdk_local_path: 编译后 SDK 产物目录
        versions: 需要复制的版本列表，如 ['ets1.1'] 或 ['ets1.1', 'ets1.2']
        force: True 时覆盖已有内容
    """
    if not os.path.exists(sdk_local_path):
        print(f"  [ERROR] SDK 产物目录不存在: {sdk_local_path}")
        return False

    # 检测 sdk_local_path 结构
    has_dynamic = os.path.isdir(os.path.join(sdk_local_path, 'dynamic'))
    has_static = os.path.isdir(os.path.join(sdk_local_path, 'static'))

    if has_dynamic or has_static:
        # 子目录结构：dynamic/ → ets1.1, static/ → ets1.2
        print(f"  [INFO] SDK 源结构: 子目录模式（dynamic + static）")
        version_map = {'ets1.1': 'dynamic', 'ets1.2': 'static'}
    else:
        # 扁平结构：整体 → ets1.1
        print(f"  [INFO] SDK 源结构: 扁平模式")
        version_map = {'ets1.1': None}  # None 表示直接用 sdk_local_path

    all_ok = True
    for ver in versions:
        dst_dir = os.path.join(SDK_ROOT, ver)

        # 跳过已存在的（除非 force）
        if os.path.isdir(dst_dir) and os.listdir(dst_dir) and not force:
            print(f"    {ver}: 已存在，跳过（使用 --force 覆盖）")
            continue

        # 确定源目录
        sub_dir = version_map.get(ver)
        if sub_dir is None:
            src_dir = sdk_local_path  # 扁平模式
        else:
            src_dir = os.path.join(sdk_local_path, sub_dir)

        if not os.path.isdir(src_dir):
            print(f"    {ver}: ⚠️ 源目录不存在: {src_dir}")
            all_ok = False
            continue

        label = f"SDK ({os.path.basename(src_dir)} → {ver})"
        ok = copy_directory_with_progress(src_dir, dst_dir, label=label)
        if ok:
            print(f"    {ver}: ✅ 复制完成")
        else:
            print(f"    {ver}: ❌ 复制失败")
            all_ok = False

    # 重命名工具目录下的 dynamic/static（兼容旧命名）
    _rename_sdk_dirs(SDK_ROOT)

    return all_ok


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


def sync(subsystem, files=None, manifest=None):
    """增量同步文件到扫描目录。支持通过文件列表或 manifest 文件指定需要同步的文件。"""
    print(f"[SYNC] 增量同步文件到扫描目录，子系统: {subsystem}")

    config = load_global_config()
    xts_acts_path, _, _, _ = _resolve_paths(config)
    if not xts_acts_path:
        raise ValueError("xts_acts_path not found in config")

    filtered_dir = os.path.join(CASE_ROOT, f'xts_acts_filtered_{subsystem}')
    if not os.path.exists(filtered_dir):
        print(f"  [ERROR] 过滤目录不存在: {filtered_dir}，请先执行 setup")
        return False

    sync_files = []
    if manifest:
        manifest_path = manifest
        if not os.path.isabs(manifest_path):
            manifest_path = os.path.join(SKILL_ROOT, manifest_path)
        if not os.path.exists(manifest_path):
            print(f"  [ERROR] manifest 文件不存在: {manifest_path}")
            return False
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        sync_files = manifest_data if isinstance(manifest_data, list) else manifest_data.get('files', [])
    elif files:
        sync_files = files

    if not sync_files:
        print(f"  [WARN] 无文件需要同步")
        return True

    success = 0
    failed = 0
    for rel_path in sync_files:
        rel_path = rel_path.strip('/')
        src = os.path.join(xts_acts_path, subsystem, rel_path)
        dst = os.path.join(filtered_dir, subsystem, rel_path)

        if not os.path.exists(src):
            print(f"  [SKIP] 源不存在: {rel_path}")
            continue

        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isdir(src):
                _copy_via_system(src, os.path.dirname(dst) if os.path.exists(dst) else dst)
            else:
                _copy_file_via_system(src, dst)
            success += 1
        except Exception as e:
            print(f"  [ERROR] 同步失败: {rel_path} - {e}")
            failed += 1

    print(f"\n[DONE] 增量同步完成: {success} 成功, {failed} 失败")
    return failed == 0


def update_sdk(versions=None, force=False):
    """显式更新工具 SDK 目录。用户主动要求更新 SDK 时调用。

    Args:
        versions: 指定版本列表，如 ['ets1.2']。None 时使用配置中的 ets_version。
        force: True 时覆盖已有内容。
    """
    config = load_global_config()
    _, _, sdk_local_path, env_label = _resolve_paths(config)
    ets_versions = versions or config.get('ets_version', ['ets1.1'])

    print(f"[UPDATE-SDK] 更新工具 SDK (环境: {env_label})")
    print(f"  目标版本: {ets_versions}")
    print(f"  强制覆盖: {force}")
    print(f"  SDK 源: {sdk_local_path or '(未配置)'}")
    print(f"  工具目录: {SDK_ROOT}")

    # 先显示当前状态
    print(f"\n  当前工具 SDK 状态:")
    for ver in ets_versions:
        ver_dir = os.path.join(SDK_ROOT, ver)
        if os.path.isdir(ver_dir) and os.listdir(ver_dir):
            size = get_dir_size(ver_dir)
            print(f"    {ver}: 已存在 ({format_size(size)})")
        else:
            print(f"    {ver}: 缺失")

    if not sdk_local_path:
        print(f"\n  [ERROR] sdk_local_path 未配置，无法更新。")
        print(f"  请在 .oh-xts-config.json 中设置 sdk_local_path 或 OH_ROOT。")
        return False

    if not os.path.exists(sdk_local_path):
        print(f"\n  [ERROR] sdk_local_path 不存在: {sdk_local_path}")
        return False

    print(f"\n  开始更新...")
    ok = _copy_sdk_versions(sdk_local_path, ets_versions, force=force)

    if ok:
        print(f"\n  [DONE] SDK 更新完成")
    else:
        print(f"\n  [DONE] SDK 更新完成（部分失败）")
    return ok


def status():
    env_label = 'WSL' if is_wsl() else ('Windows' if sys.platform == 'win32' else 'Linux')
    print(f"[STATUS] 当前扫描环境状态 (环境: {env_label})")

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
        if size < 0:
            print(f"  SDK 路径: {SDK_ROOT} (计算超时，跳过)")
        else:
            print(f"  SDK 路径: {SDK_ROOT} ({format_size(size)})")
    else:
        print(f"  SDK 路径: {SDK_ROOT} (不存在)")


def main():
    parser = argparse.ArgumentParser(
        description='管理 APICoverageDetector 扫描环境（文件复制 + arkts_config.json 配置）'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    setup_parser = subparsers.add_parser('setup', help='复制子系统文件到扫描目录并配置环境')
    setup_parser.add_argument('--subsystem', required=True, help='目标子系统名称（如 arkui, multimedia）')
    setup_parser.add_argument('--module', default=None, help='目标模块相对路径（如 ace_ets_module_ui/ace_ets_module_imageText），仅复制该模块而非整个子系统')

    teardown_parser = subparsers.add_parser('teardown', help='删除已复制的文件并恢复配置')
    teardown_parser.add_argument('--subsystem', required=True, help='要清理的子系统名称')

    sync_parser = subparsers.add_parser('sync', help='增量同步文件到扫描目录（Phase 9 用）')
    sync_parser.add_argument('--subsystem', required=True, help='目标子系统名称')
    sync_parser.add_argument('--manifest', default=None, help='manifest JSON 文件路径（包含 files 列表）')
    sync_parser.add_argument('--files', nargs='*', default=None, help='要同步的文件相对路径列表')

    sdk_parser = subparsers.add_parser('update-sdk', help='更新扫描工具 SDK（从 sdk_local_path 复制到工具目录）')
    sdk_parser.add_argument('--version', nargs='*', default=None, help='指定版本（如 ets1.1 ets1.2），默认使用配置中的 ets_version')
    sdk_parser.add_argument('--force', action='store_true', help='强制覆盖已有 SDK 内容')

    subparsers.add_parser('status', help='显示当前扫描环境状态')

    args = parser.parse_args()

    try:
        if args.command == 'setup':
            ok = setup(args.subsystem, module=getattr(args, 'module', None))
            return 0 if ok else 1
        elif args.command == 'teardown':
            ok = teardown(args.subsystem)
            return 0 if ok else 1
        elif args.command == 'sync':
            if not args.manifest and not args.files:
                print("[ERROR] sync 需要指定 --manifest 或 --files")
                return 1
            ok = sync(args.subsystem, files=args.files, manifest=args.manifest)
            return 0 if ok else 1
        elif args.command == 'update-sdk':
            ok = update_sdk(versions=args.version, force=args.force)
            return 0 if ok else 1
        elif args.command == 'status':
            status()
            return 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
