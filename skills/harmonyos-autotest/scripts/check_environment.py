#!/usr/bin/env python3
"""
检测 HarmonyOS 测试环境
用法: python check_environment.py [--app package_name]
"""
import subprocess
import sys
import json


def run_command(cmd: str) -> tuple:
    """执行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timeout"
    except Exception as e:
        return False, "", str(e)


def check_hdc():
    """检测 HDC 工具"""
    success, stdout, stderr = run_command("hdc version")
    if success and stdout:
        # 提取版本号
        version = stdout.split('\n')[0] if stdout else "unknown"
        return {"installed": True, "version": version}
    return {"installed": False, "version": None, "error": stderr or "HDC not found"}


def check_hypium():
    """检测 Hypium 框架"""
    success, stdout, stderr = run_command("pip3 show hypium")
    if success and stdout:
        # 提取版本号
        for line in stdout.split('\n'):
            if line.startswith('Version:'):
                version = line.split(':')[1].strip()
                return {"installed": True, "version": version}
    return {"installed": False, "version": None, "error": "Hypium not installed. Run: pip3 install hypium"}


def check_devices():
    """检测设备连接"""
    success, stdout, stderr = run_command("hdc list targets")
    devices = []
    if success and stdout:
        for line in stdout.split('\n'):
            line = line.strip()
            if line and line != 'empty':
                status = "connected" if '[connected]' in line.lower() or not '[' in line else "offline"
                sn = line.split('[')[0].strip() if '[' in line else line
                devices.append({"sn": sn, "status": status})
    return devices


def check_app(package_name: str):
    """检测应用是否安装"""
    success, stdout, stderr = run_command(f"hdc shell bm dump -n {package_name}")
    installed = success and package_name in stdout
    return {"checked": True, "installed": installed, "package_name": package_name}


def main():
    package_name = None
    if len(sys.argv) > 2 and sys.argv[1] == "--app":
        package_name = sys.argv[2]

    result = {
        "is_ready": True,
        "checks": {
            "hdc": check_hdc(),
            "hypium": check_hypium(),
            "devices": check_devices()
        },
        "recommendations": []
    }

    # 检查 HDC
    if not result["checks"]["hdc"]["installed"]:
        result["is_ready"] = False
        result["recommendations"].append("安装 HDC 工具并添加到 PATH")

    # 检查 Hypium
    if not result["checks"]["hypium"]["installed"]:
        result["is_ready"] = False
        result["recommendations"].append("运行: pip3 install hypium")

    # 检查设备
    if not result["checks"]["devices"]:
        result["is_ready"] = False
        result["recommendations"].append("连接 HarmonyOS 设备并确保已授权")

    # 检查应用（可选）
    if package_name:
        result["checks"]["app"] = check_app(package_name)

    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))

    return 0 if result["is_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
