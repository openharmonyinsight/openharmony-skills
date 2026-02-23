#!/usr/bin/env python3
"""
运行 HarmonyOS 测试用例
用法: python run_test.py [test_name] [--screenshot] [--debug]
"""
import subprocess
import sys
import os


def run_test(test_name: str = "Example", screenshot: bool = True, debug: bool = False):
    """运行测试用例"""
    params = ["agent_mode:bin"]
    if screenshot:
        params.append("screenshot:true")

    cmd = f"xdevice run -l {test_name} -ta {';'.join(params)}"
    print(f"执行命令: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd())
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False


def force_stop_app(package_name: str):
    """强制关闭应用"""
    cmd = f"hdc shell aa force-stop {package_name}"
    print(f"关闭应用: {cmd}")
    subprocess.run(cmd, shell=True)


def main():
    test_name = "Example"
    screenshot = True
    package_name = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--screenshot":
            screenshot = True
        elif arg == "--no-screenshot":
            screenshot = False
        elif arg == "--stop-app" and i + 1 < len(sys.argv):
            package_name = sys.argv[i + 1]
            i += 1
        elif not arg.startswith("--"):
            test_name = arg
        i += 1

    # 如果指定了应用包名，先关闭应用
    if package_name:
        force_stop_app(package_name)

    # 运行测试
    success = run_test(test_name, screenshot)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
