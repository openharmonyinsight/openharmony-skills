"""
OpenHarmony 测试用例部署工具

从 WSL 环境中编译好的 OpenHarmony 测试用例部署到连接的设备。

使用方法:
    python deploy_oh_test.py <测试用例名称> [--wsl-distro <发行版名称>]

示例:
    python deploy_oh_test.py LnnNetBuilderFuzzTest
    python deploy_oh_test.py LnnNetBuilderFuzzTest --wsl-distro Ubuntu-22.04

环境要求:
    - WSL 已安装并配置 OpenHarmony 编译环境
    - OpenHarmony 编译输出路径: /root/OpenHarmony/out/rk3568/tests/
    - hdc (Harmony Device Connector) 工具已安装并在 PATH 中
    - 设备已通过 USB 连接并可通过 hdc 访问

工作流程:
    1. 在 WSL 中查找指定名称的测试用例文件
    2. 将 Linux 路径转换为 Windows 可访问的 WSL 路径
    3. 通过 hdc file send 命令将文件发送到设备的 /data/test/ 目录
"""

import subprocess
import sys
import argparse
import io

# 设置标准输出编码为 UTF-8，避免中文乱码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def get_wsl_distro():
    """
    获取 WSL 发行版名称

    Returns:
        str: 默认 WSL 发行版名称，失败时返回 "Ubuntu-20.04"
    """
    cmd = "wsl -l -q"
    success, result = run_command(cmd)
    if success and result:
        # 取第一个非空行作为默认发行版
        distros = [line.strip() for line in result.split('\n') if line.strip()]
        if distros:
            return distros[0]
    return "Ubuntu-20.04"  # fallback


def run_command(cmd):
    """
    执行 shell 命令

    Args:
        cmd (str): 要执行的命令

    Returns:
        tuple: (success: bool, output: str)
            - success: 命令是否成功执行
            - output: 命令输出或错误信息
    """
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, errors='replace')
        # 移除空字符和其他不可见字符，避免后续处理出错
        result = result.strip().replace('\0', '').replace('\x00', '')
        return True, result
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.replace('\0', '') if e.stderr else ''
        return False, f"命令执行失败，返回码: {e.returncode}\n错误输出: {stderr}" if stderr else f"命令执行失败，返回码: {e.returncode}"
    except Exception as e:
        return False, f"执行异常: {str(e)}"


def deploy_test_case(test_name, wsl_distro=None):
    """
    部署测试用例到设备

    Args:
        test_name (str): 测试用例文件名
        wsl_distro (str, optional): WSL 发行版名称，默认自动获取

    Returns:
        tuple: (success: bool, output: str)
    """
    if wsl_distro is None:
        wsl_distro = get_wsl_distro()

    # 1. 执行 WSL 命令查找用例
    cmd = f'wsl bash -c "cd /root/OpenHarmony/out/rk3568/tests/ && find . -name {test_name} | xargs realpath"'
    success, result = run_command(cmd)

    if not success:
        return False, f"查找用例失败: {result}"

    if not result:
        return False, f"未找到用例: {test_name}"

    # 2. 转换为 Windows WSL 路径 (格式: \\wsl.localhost\<发行版>\<路径>)
    windows_path = result.replace("/", "\\")
    windows_path = f"\\\\wsl.localhost\\{wsl_distro}{windows_path}"

    # 3. 通过 hdc 发送到设备
    cmd = f"hdc file send {windows_path} /data/test/"
    success, result = run_command(cmd)

    if not success:
        return False, f"发送文件失败: {result}"

    return True, result


def main():
    parser = argparse.ArgumentParser(description="部署 OpenHarmony 测试用例到设备")
    parser.add_argument("test_name", help="测试用例名称，如: LnnNetBuilderFuzzTest")
    parser.add_argument("--wsl-distro", default=None, help="WSL 发行版名称 (默认自动获取)")
    args = parser.parse_args()

    # 如果用户未指定 wsl-distro，则自动获取
    wsl_distro = args.wsl_distro if args.wsl_distro else None
    success, result = deploy_test_case(args.test_name, wsl_distro)

    if success:
        print(f"部署成功: {result}")
        return 0
    else:
        print(f"部署失败: {result}")
        return 1


if __name__ == "__main__":
    sys.exit(main())