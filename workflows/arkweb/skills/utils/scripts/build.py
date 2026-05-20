#!/usr/bin/env python3
"""
鸿蒙应用构建脚本 - Python 版本
自动执行依赖安装、仓颉预编译、资源生成、编译、打包等步骤
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def load_env_file(env_file: Path) -> dict:
    """读取 .env 文件并设置环境变量"""
    print(f"正在加载配置文件: {env_file}")
    env_vars = {}

    if not env_file.exists():
        print(f"警告: 配置文件不存在 -> {env_file}")
        return env_vars

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip("'").strip('"').strip()
            env_vars[key] = value
            os.environ[key] = value

    return env_vars


def run_command(cmd: list, description: str, timeout: int = 300):
    """执行命令并输出结果"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"命令: {' '.join(str(c) for c in cmd)}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=timeout
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"错误: 命令执行超时 ({timeout}秒)")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='鸿蒙应用构建脚本')
    parser.add_argument('--project-root', type=str, default=None,
                        help='项目根目录路径，默认当前目录')
    parser.add_argument('--no-install', action='store_true',
                        help='跳过依赖安装')
    args = parser.parse_args()

    # 1. 确定项目根目录
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent.parent

    print(f"项目根目录: {project_root}")

    # 切换到项目根目录
    os.chdir(project_root)

    # 2. 加载环境变量
    env_file = project_root / '.claude' / 'skills' / 'utils' / 'scripts' / '.env'
    env_vars = load_env_file(env_file)

    # 3. 校验必需的环境变量
    deveco_home = os.environ.get('DEVECO_HOME')
    if not deveco_home:
        print("错误: .env 文件中未配置 DEVECO_HOME")
        sys.exit(1)

    deveco_home = Path(deveco_home)
    print(f"DevEco Studio 路径: {deveco_home}")

    # 4. 验证 SDK 路径
    sdk_path = deveco_home / 'sdk'
    if sdk_path.exists():
        os.environ['DEVECO_SDK_HOME'] = str(sdk_path)
        print(f"SDK 路径验证成功: {sdk_path}")
    else:
        print(f"警告: 拼接后的路径无效 -> {sdk_path}")
        print("请检查 .env 文件中 DEVECO_HOME 的结尾是否有空格！")
        sys.exit(1)

    # 5. 动态获取 Cangjie SDK
    user_profile = Path(os.environ.get('USERPROFILE', os.path.expanduser('~')))
    cangjie_sdk_root = user_profile / '.cangjie-sdk' / '6.0' / 'cangjie'

    if cangjie_sdk_root.exists():
        os.environ['DEVECO_CANGJIE_PATH'] = str(cangjie_sdk_root)
        print(f"已动态注入 Cangjie SDK 环境: {cangjie_sdk_root}")

        # 执行官方 envsetup 脚本设置环境
        env_setup_script = cangjie_sdk_root / 'build-tools' / 'envsetup.ps1'
        if env_setup_script.exists():
            print(f"已找到仓颉 SDK 环境配置脚本: {env_setup_script}")
            # 在 Windows 上执行 PowerShell 脚本
            subprocess.run([
                'powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                '-File', str(env_setup_script)
            ], check=False)
    else:
        print(f"警告: 未在 {cangjie_sdk_root} 找到仓颉 SDK")

    # 6. 动态注入 Java 环境
    java_home = deveco_home / 'jbr'
    if java_home.exists():
        os.environ['JAVA_HOME'] = str(java_home)
        os.environ['PATH'] = str(java_home / 'bin') + ';' + os.environ.get('PATH', '')
        print(f"已动态注入 Java 环境: {java_home}")
    else:
        print(f"警告: 未在 {java_home} 找到 Java 运行时")

    # 7. 设置工具路径
    ohpm_path = deveco_home / 'tools' / 'ohpm' / 'bin' / 'ohpm.bat'
    node_exe = deveco_home / 'tools' / 'node' / 'node.exe'
    hvigorw_js = deveco_home / 'tools' / 'hvigor' / 'bin' / 'hvigorw.js'

    print(f"PATH is...: {os.environ.get('PATH')}")

    # 8. 执行构建流程
    success = True

    # 8.1 安装依赖
    if not args.no_install and ohpm_path.exists():
        print("\n开始安装依赖...")
        success = run_command(
            [str(ohpm_path), 'install', '--all',
             '--registry', 'https://ohpm.openharmony.cn/ohpm/',
             '--strict_ssl', 'true'],
            "安装依赖",
            timeout=600
        )
        if not success:
            print("警告: 依赖安装可能失败，继续执行...")

    # 8.2 执行 SyncCangjieResource
    if node_exe.exists() and hvigorw_js.exists():
        print("\n执行 SyncCangjieResource...")
        success = run_command(
            [str(node_exe), str(hvigorw_js),
             '--mode', 'module',
             '-p', 'module=entry@default',
             'SyncCangjieResource',
             '--analyze=normal',
             '--parallel',
             '--incremental',
             '--no-daemon'],
            "仓颉资源同步",
            timeout=600
        )

    # 8.3 执行 assembleHap
    if success and node_exe.exists() and hvigorw_js.exists():
        print("\n执行 assembleHap...")
        success = run_command(
            [str(node_exe), str(hvigorw_js),
             '--mode', 'module',
             '-p', 'product=default',
             'assembleHap',
             '--analyze=normal',
             '--parallel',
             '--incremental',
             '--no-daemon'],
            "打包 HAP",
            timeout=900
        )

    # 9. 输出结果
    print("\n" + "="*60)
    if success:
        print("构建任务完成！")
    else:
        print("构建任务完成，但存在错误！")
        sys.exit(1)


if __name__ == '__main__':
    main()
