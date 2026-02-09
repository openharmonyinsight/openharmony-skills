#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug CLI
HarmonyOS/OpenHarmony 应用构建工具命令行界面
"""

import sys
import os
from pathlib import Path

# 获取包所在目录
PACKAGE_DIR = Path(__file__).parent
TOOLS_DIR = PACKAGE_DIR / "tools"

# 将 tools 目录添加到 Python 路径
sys.path.insert(0, str(TOOLS_DIR))


def print_usage():
    """打印使用帮助"""
    print()
    print("OHOS App Build & Debug - HarmonyOS/OpenHarmony 应用构建工具")
    print()
    print("使用方法:")
    print("  ohos-app-build-debug <command> [options]")
    print()
    print("可用命令:")
    print("  build         编译 HarmonyOS/OpenHarmony 应用")
    print("  install       安装 HAP 文件到设备")
    print("  launch        启动已安装的应用")
    print("  screenshot    捕获设备屏幕截图")
    print("  parse-crash   解析应用崩溃堆栈")
    print("  env           显示环境检测信息")
    print()
    print("获取命令详细帮助:")
    print("  ohos-app-build-debug <command> --help")
    print()
    print("示例:")
    print("  ohos-app-build-debug build                    # 编译应用")
    print("  ohos-app-build-debug build -m release         # 编译 release 版本")
    print("  ohos-app-build-debug install -f app.hap       # 安装 HAP 文件")
    print("  ohos-app-build-debug launch                   # 启动应用")
    print("  ohos-app-build-debug env                      # 显示环境信息")
    print()


def main():
    """主入口"""
    # 无参数或 --help 时显示帮助
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h", "help"]:
        print_usage()
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]  # 剩余参数传递给子命令

    # 命令映射
    commands = {
        "build": "build",
        "compile": "build",  # 别名
        "install": "install",
        "launch": "launch",
        "start": "launch",  # 别名
        "screenshot": "screenshot",
        "screen": "screenshot",  # 别名
        "parse-crash": "parse_crash",
        "env": "env_detector",
    }

    if command not in commands:
        print(f"错误: 未知命令 '{command}'", file=sys.stderr)
        print()
        print_usage()
        sys.exit(1)

    # 获取对应的模块名
    module_name = commands[command]

    try:
        # 动态导入并执行模块
        if command == "env":
            # 环境检测特殊处理
            from env_detector import detect_environment, print_detection_report

            # 检查是否需要刷新缓存
            force_refresh = "--refresh" in args or "-r" in args

            env_info = detect_environment(force_refresh=force_refresh)
            print_detection_report(env_info)

        elif command in ["build", "compile"]:
            # 编译命令
            import build
            sys.argv = ["build"] + args
            build.main()

        elif command == "install":
            # 安装命令
            import install
            sys.argv = ["install"] + args
            install.main()

        elif command in ["launch", "start"]:
            # 启动命令
            import launch
            sys.argv = ["launch"] + args
            launch.main()

        elif command in ["screenshot", "screen"]:
            # 截图命令
            import screenshot
            sys.argv = ["screenshot"] + args
            screenshot.main()

        elif command == "parse-crash":
            # 崩溃解析命令
            import parse_crash
            sys.argv = ["parse_crash"] + args
            parse_crash.main()

    except ImportError as e:
        print(f"错误: 无法导入模块 '{module_name}': {e}", file=sys.stderr)
        print(f"请确保 skill 正确安装在: {PACKAGE_DIR}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
