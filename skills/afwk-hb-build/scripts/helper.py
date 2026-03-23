#!/usr/bin/env python3
"""
Ability Runtime 自动编译脚本
功能：检测修改的文件，自动推断编译目标，并在编译失败时尝试修复
"""

import os
import sys
import subprocess
import re
import json
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")

def print_success(msg: str):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {msg}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {msg}")

def print_error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {msg}")

# 文件路径到编译目标的映射
# 格式: '路径前缀': ('目标名称', '完整构建路径')
FILE_TARGET_MAP = {
    # AbilityManagerService
    'services/abilitymgr': ('abilityms', '//foundation/ability/ability_runtime/services/abilitymgr:abilityms'),

    # AppManagerService
    'services/appmgr': ('appms', '//foundation/ability/ability_runtime/services/appmgr:appms'),

    # UriPermissionManager
    'services/uripermmgr': ('libupms', '//foundation/ability/ability_runtime/services/uripermmgr:libupms'),

    # DataObserverManager
    'services/dataobsmgr': ('dataobsms', '//foundation/ability/ability_runtime/services/dataobsmgr:dataobsms'),

    # QuickFix Manager
    'services/quickfixmgr': ('quickfixmgr', '//foundation/ability/ability_runtime/services/quickfixmgr:quickfixmgr'),
}

# 目标名称到完整路径的映射（反向索引）
TARGET_NAME_TO_PATH = {
    'abilityms': '//foundation/ability/ability_runtime/services/abilitymgr:abilityms',
    'appms': '//foundation/ability/ability_runtime/services/appmgr:appms',
    'libupms': '//foundation/ability/ability_runtime/services/uripermmgr:libupms',
    'dataobsms': '//foundation/ability/ability_runtime/services/dataobsmgr:dataobsms',
    'quickfixmgr': '//foundation/ability/ability_runtime/services/quickfixmgr:quickfixmgr',
}

def get_project_root() -> Path:
    """获取项目根目录（包含 build.py 的目录，用于运行 hb build）"""
    current = Path.cwd()
    while current != current.parent:
        # 查找 build.py（可能是一个符号链接）
        if (current / 'build.py').exists():
            return current
        current = current.parent
    # 如果没找到 build.py，返回当前目录
    return Path.cwd()

def get_git_root() -> Path:
    """获取 Git 仓库根目录（包含 .git 的目录）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / '.git').exists():
            return current
        current = current.parent
    # 如果没找到 .git，返回当前目录
    return Path.cwd()

def get_ability_runtime_root() -> Path:
    """获取 ability_runtime 组件根目录"""
    project_root = get_project_root()
    art_path = project_root / 'foundation' / 'ability' / 'ability_runtime'
    if art_path.exists():
        return art_path
    # 如果找不到，尝试从当前目录向上查找
    current = Path.cwd()
    while current != current.parent:
        if (current / 'services' / 'abilitymgr').exists():
            return current
        current = current.parent
    return Path.cwd()

def get_modified_files() -> List[str]:
    """获取修改的文件列表"""
    git_root = get_git_root()
    art_root = get_ability_runtime_root()

    result = subprocess.run(
        ['git', 'status', '--short'],
        capture_output=True,
        text=True,
        cwd=git_root
    )

    if result.returncode != 0:
        return []

    # 需要忽略的路径模式
    ignore_patterns = [
        '.claude/',
        '.hvigor/',
        'build/',
        'local.properties',
        'out/',
        '.git/',
        'services/dialog_ui/ams_system_dialog/.hvigor/',
    ]

    modified = []
    for line in result.stdout.strip().split('\n'):
        if line:
            # 解析 git status 输出: M  file_path 或 ?? file_path
            parts = line.strip().split()
            if len(parts) >= 2:
                file_path = parts[1]
                # 跳过忽略的文件
                if any(pattern in file_path for pattern in ignore_patterns):
                    continue
                # 跳过 Markdown 文档
                if file_path.endswith('.md'):
                    continue

                # 如果 Git 仓库根目录就是 ability_runtime，直接使用相对路径
                # 如果 Git 仓库根目录包含 ability_runtime，则需要提取相对路径
                try:
                    rel_path = str(Path(file_path).relative_to(art_root))
                    modified.append(rel_path)
                except ValueError:
                    # 如果无法计算相对路径，可能是因为 Git 仓库根目录就是 ability_runtime
                    # 这种情况下直接使用 file_path
                    modified.append(file_path)

    return modified

def detect_build_targets(modified_files: List[str]) -> List[Tuple[str, str]]:
    """根据修改的文件推断编译目标（支持多个目标）"""
    if not modified_files:
        print_warning("未检测到修改的文件，默认编译 ability_runtime")
        return [('full', None)]

    # 统计每个目标的命中次数
    target_scores = {}

    for file_path in modified_files:
        for path_pattern, target_info in FILE_TARGET_MAP.items():
            if file_path.startswith(path_pattern):
                target_name = target_info[0]
                target_scores[target_name] = target_scores.get(target_name, 0) + 1

    if not target_scores:
        print_warning("无法确定编译目标，将编译全仓")
        return [('full', None)]

    # 返回所有命中过的目标，按命中次数排序
    sorted_targets = sorted(target_scores.items(), key=lambda x: x[1], reverse=True)

    # 构建返回列表
    targets = []
    for target_name, score in sorted_targets:
        target_full_path = TARGET_NAME_TO_PATH.get(target_name)
        targets.append((target_name, target_full_path))

    return targets

def get_build_command(targets: List[str], build_type: str, fast_rebuild: bool) -> List[str]:
    """构建编译命令（支持多个目标）"""
    project_root = get_project_root()
    cmd = ['hb', 'build', 'ability_runtime', build_type]

    # 添加所有编译目标
    for target in targets:
        if target != 'full':
            cmd.extend(['--build-target', target])

    if fast_rebuild:
        cmd.append('--fast-rebuild')

    return cmd

def parse_compiler_errors(output: str) -> List[str]:
    """解析编译器错误信息"""
    errors = []

    # 匹配 C++ 编译错误
    # 例如: /path/to/file.cpp:123:45: error: xxx
    error_pattern = r'^([^:]+):(\d+):(\d+):\s*error:\s*(.+)$'
    for line in output.split('\n'):
        match = re.match(error_pattern, line.strip())
        if match:
            file_path = match.group(1)
            line_num = match.group(2)
            error_msg = match.group(4)
            errors.append(f"{file_path}:{line_num} - {error_msg}")

    return errors

def try_fix_errors(errors: List[str]) -> bool:
    """尝试修复编译错误（简单错误）"""
    if not errors:
        return False

    print_info(f"检测到 {len(errors)} 个编译错误，尝试分析...")

    for error in errors[:5]:  # 只分析前5个错误
        print_warning(f"  - {error}")

    print_info("建议：请查看上述错误并手动修复")
    return False

def should_auto_retry(output: str, stderr: str) -> Tuple[bool, str]:
    """
    分析编译错误，判断是否应该自动重试
    返回: (是否应该重试, 原因)
    """
    combined_output = output + stderr

    # 不应该自动重试的错误类型
    fatal_errors = [
        # 语法错误 - 需要手动修复
        r'syntax error',
        r'undefined reference',
        r'error: .* was not declared',
        r'error: no matching function',
        # 类型错误
        r'error: cannot convert',
        r'error: invalid conversion',
        # 头文件缺失
        r'error: .*: No such file or directory',
        r'fatal error: .*: No such file',
    ]

    # 应该自动重试的错误类型
    retryable_errors = [
        # 构建系统问题
        r'ninja: error: rebuilding',
        r'error: build stopped',
        # 链接时问题（偶尔出现）
        r'collect2: error: ld returned',
        # 临时文件问题
        r'error: could not create',
        r'error: unable to open',
        # 并发问题
        r'error: multiple rules generate',
        # 依赖问题（有时重新编译能解决）
        r'missing dependency',
    ]

    for pattern in fatal_errors:
        if re.search(pattern, combined_output, re.IGNORECASE):
            return False, f"发现需要手动修复的错误: {pattern}"

    for pattern in retryable_errors:
        if re.search(pattern, combined_output, re.IGNORECASE):
            return True, f"发现可重试的错误: {pattern}"

    # 默认不自动重试
    return False, "未知错误类型"

def run_build(command: List[str], retry_count: int = 0, max_retries: int = 3, auto_retry: bool = True) -> bool:
    """
    执行编译命令，支持自动重试

    Args:
        command: 编译命令
        retry_count: 当前重试次数
        max_retries: 最大重试次数
        auto_retry: 是否启用自动重试判断
    """
    project_root = get_project_root()

    print_info(f"执行编译命令（第 {retry_count + 1} 次，最多 {max_retries} 次）")
    print_info(f"命令: {' '.join(command)}")
    print_info(f"工作目录: {project_root}")

    result = subprocess.run(
        command,
        cwd=project_root,
        capture_output=True,
        text=True
    )

    # 实时输出
    if result.stdout:
        print(result.stdout)

    if result.returncode == 0:
        print_success("编译成功！")
        return True

    # 编译失败
    print_error(f"编译失败（返回码: {result.returncode}）")

    if result.stderr:
        print(result.stderr)

    # 解析错误
    errors = parse_compiler_errors(result.stdout + result.stderr)
    if errors:
        print_error(f"发现 {len(errors)} 个编译错误")

    # 如果还有重试次数，决定是否继续
    if retry_count < max_retries - 1:
        # 分析是否应该自动重试
        should_retry, reason = should_auto_retry(result.stdout, result.stderr)

        if auto_retry and should_retry:
            # 自动重试
            print_warning(f"✓ {reason}")
            print_warning(f"⚠ 自动重试中... ({max_retries - retry_count - 1} 次剩余)")
            import time
            time.sleep(2)  # 等待 2 秒后重试
            return run_build(command, retry_count + 1, max_retries, auto_retry)
        else:
            # 需要手动确认
            print_warning(f"\n原因: {reason}")
            print_warning(f"\n还有 {max_retries - retry_count - 1} 次重试机会")
            print_info("您可以：")
            print_info("  1. 手动修复代码后，按 Enter 继续重试")
            print_info("  2. 输入 'r' 开启自动重试模式")
            print_info("  3. 输入 'q' 或 'quit' 退出")

            user_input = input("\n您的选择 [Enter/r/q]: ").strip().lower()

            if user_input in ['q', 'quit']:
                print_info("用户取消编译")
                return False
            elif user_input == 'r':
                print_info("启用自动重试模式")
                import time
                time.sleep(2)
                return run_build(command, retry_count + 1, max_retries, auto_retry=True)

            # 尝试修复（这里只是提示，实际修复需要手动完成）
            try_fix_errors(errors)

            # 递归重试
            return run_build(command, retry_count + 1, max_retries, auto_retry)

    return False

def main():
    parser = argparse.ArgumentParser(description='Ability Runtime 自动编译脚本')
    parser.add_argument('--target', type=str, default='auto', nargs='+',
                        help='编译目标 (auto/full/abilityms/appms/libupms/dataobsms/quickfixmgr 或多个目标，用空格分隔)')
    parser.add_argument('--type', type=str, default='-i',
                        help='编译类型 (-i: 功能代码, -t: 测试套)')
    parser.add_argument('--fast', action='store_true',
                        help='启用快速编译 (--fast-rebuild)')
    parser.add_argument('--max-retries', type=int, default=3,
                        help='最大重试次数')
    parser.add_argument('--auto-retry', action='store_true',
                        help='启用自动重试（默认开启）')

    args = parser.parse_args()

    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Ability Runtime 自动编译工具{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    # 获取修改的文件
    modified_files = get_modified_files()

    if modified_files:
        print_info(f"检测到 {len(modified_files)} 个修改的文件:")
        for f in modified_files:
            print(f"  - {f}")
        print()
    else:
        print_warning("未检测到修改的文件")
        print()

    # 确定编译目标
    targets = []
    target_names = []

    if 'auto' in args.target:
        # 自动检测模式 - 返回所有需要编译的目标
        detected_targets = detect_build_targets(modified_files)

        # 判断是否需要整仓编译
        if len(detected_targets) > 5:
            print_warning(f"检测到 {len(detected_targets)} 个编译目标，超过 5 个")
            print_warning(f"建议使用整仓编译以节省时间")
            targets = ['full']
            target_names = ['full']
        elif len(detected_targets) > 1:
            # 多个目标一起编译
            print_info(f"检测到 {len(detected_targets)} 个编译目标，将一起编译")
            for target_name, target_full_path in detected_targets:
                if target_full_path:
                    targets.append(target_full_path)
                else:
                    targets.append(target_name)
                target_names.append(target_name)
        else:
            # 单个目标
            target_name, target_full_path = detected_targets[0]
            if target_full_path:
                targets.append(target_full_path)
            else:
                targets.append(target_name)
            target_names.append(target_name)
    else:
        # 手动指定模式（支持多个目标）
        for target in args.target:
            target_full_path = TARGET_NAME_TO_PATH.get(target)
            if not target_full_path and target != 'full':
                # 如果在 TARGET_NAME_TO_PATH 中找不到，尝试作为完整路径
                if target.startswith('//'):
                    target_full_path = target
                    targets.append(target_full_path)
                    target_names.append(target.split(':')[-1] if ':' in target else target)
                else:
                    targets.append(target)
                    target_names.append(target)
            elif target_full_path:
                targets.append(target_full_path)
                target_names.append(target)
            else:  # full
                targets.append('full')
                target_names.append('full')

    # 显示编译目标信息
    if len(targets) == 1:
        if targets[0] == 'full':
            print_info(f"编译目标: {Colors.BOLD}{target_names[0]}{Colors.END} (全仓编译)")
        else:
            print_info(f"编译目标: {Colors.BOLD}{target_names[0]}{Colors.END}")
            if targets[0] != target_names[0]:
                print_info(f"完整路径: {targets[0]}")
    else:
        print_info(f"编译目标 ({Colors.BOLD}{len(targets)}{Colors.END} 个):")
        for i, (name, path) in enumerate(zip(target_names, targets), 1):
            if path == 'full':
                print(f"  {i}. {Colors.BOLD}{name}{Colors.END} (全仓编译)")
            elif path != name:
                print(f"  {i}. {Colors.BOLD}{name}{Colors.END}")
                print(f"     路径: {path}")
            else:
                print(f"  {i}. {Colors.BOLD}{name}{Colors.END}")

    print_info(f"编译类型: {Colors.BOLD}{args.type}{Colors.END}")
    if args.fast:
        print_info(f"快速编译: {Colors.BOLD}启用{Colors.END}")
    print_info(f"自动重试: {Colors.BOLD}{'开启' if args.auto_retry else '手动'}{Colors.END}")
    print_info(f"最大重试: {Colors.BOLD}{args.max_retries}{Colors.END} 次")
    print()

    # 构建命令
    command = get_build_command(targets, args.type, args.fast)

    # 执行编译
    success = run_build(command, max_retries=args.max_retries, auto_retry=args.auto_retry)

    print()
    if success:
        print_success("=" * 60)
        print_success("编译完成！")
        print_success("=" * 60)

        # 显示编译产物位置
        project_root = get_project_root()
        out_dir = project_root / 'out'
        if out_dir.exists():
            print_info(f"\n编译产物目录: {out_dir}")
    else:
        print_error("=" * 60)
        print_error("编译失败")
        print_error("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    main()
