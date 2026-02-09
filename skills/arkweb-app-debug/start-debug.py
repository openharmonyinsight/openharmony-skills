#!/usr/bin/env python3
"""
ArkWeb App Debug Tool - Cross-platform Quick Start Script
自动使用 ohos-app-build-debug 检测到的环境启动调试

Supports: Windows, macOS, Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Optional, Dict


class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Add color to text for terminal output."""
        return f"{color}{text}{Colors.RESET}"


def print_header():
    """Print header banner."""
    print("=" * 50)
    print(Colors.colorize("ArkWeb App Debug Tool - Quick Start", Colors.BLUE))
    print("=" * 50)
    print()


def find_ohos_skill() -> Optional[Path]:
    """Find ohos-app-build-debug skill directory."""
    ohos_skill = Path.home() / ".claude" / "skills" / "ohos-app-build-debug"

    if not ohos_skill.exists():
        print(Colors.colorize("❌ ohos-app-build-debug skill not found", Colors.RED))
        print("Please install ohos-app-build-debug skill first:")
        print("  https://github.com/your-repo/ohos-app-build-debug")
        return None

    print(Colors.colorize("✓ Found ohos-app-build-debug skill", Colors.GREEN))
    return ohos_skill


def check_deveco_studio(ohos_skill: Path) -> Dict[str, str]:
    """Check DevEco Studio installation and return tool paths."""
    print(Colors.colorize("🔍 Checking DevEco Studio environment...", Colors.BLUE))

    # Run ohos-app-build-debug env
    env_script = ohos_skill / ("ohos-app-build-debug.exe" if platform.system() == "Windows" else "ohos-app-build-debug")

    try:
        result = subprocess.run(
            [str(env_script), "env"],
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        print(Colors.colorize("❌ Timeout checking DevEco Studio", Colors.RED))
        return {}
    except FileNotFoundError:
        print(Colors.colorize("❌ ohos-app-build-debug executable not found", Colors.RED))
        return {}

    env_output = result.stdout + result.stderr

    # Check if DevEco Studio was detected
    if "未检测到 DevEco Studio" in env_output or "not detected" in env_output.lower():
        print(Colors.colorize("❌ DevEco Studio not detected", Colors.RED))
        print("Please install DevEco Studio first:")
        print("  https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download")
        return {}

    print(Colors.colorize("✓ DevEco Studio detected", Colors.GREEN))

    # Parse tool paths from output
    tools = {}
    for line in env_output.split('\n'):
        if 'toolchains:' in line:
            parts = line.split()
            if len(parts) >= 2:
                tools['toolchains'] = parts[-1]
        elif 'hdc:' in line:
            parts = line.split()
            if len(parts) >= 2:
                tools['hdc'] = parts[-1]
        elif 'hvigorw:' in line:
            parts = line.split()
            if len(parts) >= 2:
                tools['hvigorw'] = parts[-1]

    return tools


def setup_environment(tools: Dict[str, str]) -> Dict[str, str]:
    """Set up environment variables from detected tools."""
    print(Colors.colorize("🔧 Setting up environment...", Colors.BLUE))

    env = os.environ.copy()
    path_parts = env.get('PATH', '').split(os.pathsep)

    # Add tool paths to PATH
    if 'toolchains' in tools:
        toolchains = Path(tools['toolchains'])
        if toolchains.exists():
            path_parts.insert(0, str(toolchains))
            print(Colors.colorize(f"  ✓ Toolchains: {toolchains}", Colors.GREEN))

    if 'hdc' in tools:
        hdc_path = Path(tools['hdc'])
        hdc_dir = hdc_path.parent
        if hdc_dir.exists():
            path_parts.insert(0, str(hdc_dir))
            print(Colors.colorize(f"  ✓ HDC: {hdc_dir}", Colors.GREEN))

    if 'hvigorw' in tools:
        hvigorw_path = Path(tools['hvigorw'])
        hvigorw_dir = hvigorw_path.parent
        if hvigorw_dir.exists():
            path_parts.insert(0, str(hvigorw_dir))
            print(Colors.colorize(f"  ✓ Hvigorw: {hvigorw_dir}", Colors.GREEN))

    env['PATH'] = os.pathsep.join(path_parts)
    env['HDC_SERVER_PORT'] = '7035'

    return env


def check_device(env: Dict[str, str]) -> bool:
    """Check device connection."""
    print(Colors.colorize("📱 Checking device connection...", Colors.BLUE))

    try:
        # Determine hdc command based on platform
        hdc_cmd = "hdc.exe" if platform.system() == "Windows" else "hdc"

        result = subprocess.run(
            [hdc_cmd, "list", "targets"],
            capture_output=True,
            text=True,
            env=env,
            timeout=5
        )

        devices = result.stdout.strip()

        if not devices or devices.count('\n') <= 1:  # Only header or empty
            print(Colors.colorize("⚠ No device found", Colors.YELLOW))
            print("Please check:")
            print("  1. Device is connected via USB")
            print("  2. USB debugging is enabled")
            print("  3. Device is authorized")
            print()

            response = input("Continue anyway? (y/N): ").strip().lower()
            return response == 'y'
        else:
            device_id = devices.split('\n')[0]
            print(Colors.colorize(f"✓ Device found: {device_id}", Colors.GREEN))
            return True

    except Exception as e:
        print(Colors.colorize(f"⚠ Warning: Could not check device: {e}", Colors.YELLOW))
        return True  # Continue anyway


def start_debugging(env: Dict[str, str], args: list):
    """Start debugging session."""
    print(Colors.colorize("🚀 Starting DevTools debugging session...", Colors.BLUE))
    print()

    # Get script directory
    script_dir = Path(__file__).parent.resolve()

    # Determine arkweb-app-debug executable name
    if platform.system() == "Windows":
        executable = script_dir / "arkweb-app-debug.exe"
    else:
        executable = script_dir / "arkweb-app-debug"

    if not executable.exists():
        print(Colors.colorize(f"❌ Executable not found: {executable}", Colors.RED))
        sys.exit(1)

    # Build command
    cmd = [str(executable)] + args

    # Start debugging
    try:
        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=str(script_dir)
        )
        process.wait()
        sys.exit(process.returncode)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(Colors.colorize(f"❌ Error starting debugging: {e}", Colors.RED))
        sys.exit(1)


def main():
    """Main entry point."""
    print_header()

    # Find ohos-app-build-debug skill
    ohos_skill = find_ohos_skill()
    if not ohos_skill:
        sys.exit(1)

    print()

    # Check DevEco Studio
    tools = check_deveco_studio(ohos_skill)
    if not tools:
        sys.exit(1)

    print()

    # Set up environment
    env = setup_environment(tools)

    print()

    # Check device
    if not check_device(env):
        sys.exit(1)

    print()

    # Get command line arguments
    args = sys.argv[1:]

    # Start debugging
    start_debugging(env, args)


if __name__ == "__main__":
    main()
