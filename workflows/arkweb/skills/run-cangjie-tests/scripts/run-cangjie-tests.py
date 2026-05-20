#!/usr/bin/env python3
"""Helper script for running Cangjie test cases.

Supports platforms: linux_x86_64, linux_aarch64, mac_x86_64, mac_aarch64

Usage:
    python3 run-cangjie-tests.py [--platform PLATFORM] [--suite SUITE] [--parallel N]
                                 [--timeout SECONDS] [--verbose] [--retry N] [test_path]

Examples:
    python3 run-cangjie-tests.py --suite hlt --platform linux_x86_64
    python3 run-cangjie-tests.py --suite llt --retry 3
    python3 run-cangjie-tests.py path/to/test_case.cj --suite hlt --verbose
"""

import argparse
import os
import subprocess
import sys

SUPPORTED_PLATFORMS = ["linux_x86_64", "linux_aarch64", "mac_x86_64", "mac_aarch64"]

PLATFORM_MAP = {
    "linux_x86_64": "linux_x86",
    "linux_aarch64": "linux_arm",
    "mac_x86_64": "mac_x86",
    "mac_aarch64": "mac_arm",
}

HLT_CONFIG_TEMPLATE = "cangjie_test/testsuites/HLT/configs/cjnative/cangjie2cjnative_{platform}_test.cfg"
LLT_CONFIG = "cangjie_test/testsuites/LLT/configs/cjnative/cjnative_test.cfg"
CJCOV_CONFIG = "cangjie_test/testsuites/LLT/Tools/cjcov/configs/test.cfg"
FRAMEWORK_ENTRY = "cangjie_test_framework/main.py"


def detect_platform():
    """Auto-detect the current platform."""
    import platform as plat
    machine = plat.machine().lower()
    system = plat.system().lower()
    os_name = "linux" if system == "linux" else "mac" if system == "darwin" else None
    arch = "x86_64" if machine in ("x86_64", "amd64") else "aarch64" if machine in ("aarch64", "arm64") else None
    if not os_name or not arch:
        print(f"Unsupported platform: {system}/{machine}", file=sys.stderr)
        sys.exit(1)
    return f"{os_name}_{arch}"


def run(cmd):
    """Run a shell command and return exit code."""
    print(f"[test] {cmd}")
    return subprocess.run(cmd, shell=True).returncode


def get_hlt_config(platform):
    return HLT_CONFIG_TEMPLATE.format(platform=PLATFORM_MAP[platform])


def build_command(args, platform):
    """Build the test framework command."""
    cmd_parts = [f"python3 {FRAMEWORK_ENTRY}"]

    if args.suite == "hlt":
        cmd_parts.append(f"--test_cfg={get_hlt_config(platform)}")
        if not args.test_path:
            cmd_parts.append("--test_list=cangjie_test/testsuites/HLT/testlist")
            cmd_parts.append("cangjie_test/testsuites/HLT/")
    elif args.suite == "llt":
        cmd_parts.append(f"--test_cfg={LLT_CONFIG}")
        if not args.test_path:
            plat_short = PLATFORM_MAP[platform].replace("_", "/")
            cmd_parts.append(
                f"--test_list=cangjie_test/testsuites/LLT/cjnative_testlist,"
                f"cangjie-ci/scripts/cangjie/ci/test/llt/{plat_short}/exclude_cjnative_testlist"
            )
            cmd_parts.append("cangjie_test/testsuites/LLT/")
    elif args.suite == "cjcov":
        cmd_parts.append(f"--test_cfg={CJCOV_CONFIG}")
        if not args.test_path:
            cmd_parts.append("--test_list=cangjie_test/testsuites/LLT/Tools/cjcov/configs/testlist")
            cmd_parts.append("cangjie_test/testsuites/LLT/Tools/cjcov")

    cmd_parts.append(f"-j{args.parallel}")
    cmd_parts.append(f"--timeout={args.timeout}")
    cmd_parts.append("-pFAIL")

    if args.verbose:
        cmd_parts.append("--verbose")
    else:
        cmd_parts.append("--fail-verbose")

    if args.retry > 0:
        cmd_parts.append(f"--retry={args.retry}")

    if args.fail_exit:
        cmd_parts.append("--fail_exit")

    if args.debug:
        cmd_parts.append("--debug")

    if args.test_path:
        cmd_parts.append(args.test_path)

    return " ".join(cmd_parts)


def main():
    parser = argparse.ArgumentParser(description="Run Cangjie test cases")
    parser.add_argument("test_path", nargs="?", default=None,
                        help="Path to specific test case (optional)")
    parser.add_argument("--platform", choices=SUPPORTED_PLATFORMS, default=None,
                        help="Target platform (auto-detected if omitted)")
    parser.add_argument("--suite", choices=["hlt", "llt", "cjcov"], default="hlt",
                        help="Test suite to run (default: hlt)")
    parser.add_argument("--parallel", "-j", type=int, default=20,
                        help="Number of parallel test jobs (default: 20)")
    parser.add_argument("--timeout", type=int, default=180,
                        help="Timeout per test in seconds (default: 180)")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output for all tests")
    parser.add_argument("--retry", type=int, default=0,
                        help="Number of retries for failed tests")
    parser.add_argument("--fail-exit", action="store_true",
                        help="Exit with non-zero code if any test fails")
    parser.add_argument("--debug", action="store_true",
                        help="Keep only failed test temp files")
    args = parser.parse_args()

    platform = args.platform or detect_platform()
    print(f"[test] Platform: {platform}")
    print(f"[test] Suite: {args.suite}")

    if not os.environ.get("CANGJIE_HOME"):
        print("[test] WARNING: CANGJIE_HOME is not set", file=sys.stderr)

    cmd = build_command(args, platform)
    sys.exit(run(cmd))


if __name__ == "__main__":
    main()


