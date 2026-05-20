#!/usr/bin/env python3
"""Profile script for Cangjie compiler - time and memory profiling.

Uses cjc's built-in --profile-compile-time and --profile-compile-memory flags
to generate .prof files for analysis.

Usage:
    python3 profile-cangjie.py <source.cj> [--time] [--memory] [--both]
    python3 profile-cangjie.py --analyze <file.prof>

Examples:
    python3 profile-cangjie.py test.cj --both
    python3 profile-cangjie.py test.cj --memory
    python3 profile-cangjie.py --analyze test.cj.mem.prof
"""

import argparse
import glob
import os
import subprocess
import sys


def find_compiler_root():
    """Find cangjie_compiler root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", "..", "..", ".."))


def setup_env(compiler_root):
    """Source envsetup.sh and return updated env."""
    envsetup = os.path.join(compiler_root, "output", "envsetup.sh")
    if not os.path.exists(envsetup):
        print(f"[profile] envsetup.sh not found: {envsetup}", file=sys.stderr)
        print(f"[profile] Please build the compiler first.", file=sys.stderr)
        sys.exit(1)

    # Source envsetup.sh and capture environment
    cmd = f"source {envsetup} && env"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash")
    env = os.environ.copy()
    for line in result.stdout.splitlines():
        if '=' in line:
            key, _, val = line.partition('=')
            env[key] = val
    return env


def run_profile(source_file, profile_time, profile_memory, env):
    """Run cjc with profiling flags."""
    if not os.path.exists(source_file):
        print(f"[profile] Source file not found: {source_file}", file=sys.stderr)
        sys.exit(1)

    flags = []
    if profile_time:
        flags.append("--profile-compile-time")
    if profile_memory:
        flags.append("--profile-compile-memory")

    if not flags:
        flags = ["--profile-compile-time", "--profile-compile-memory"]

    base = os.path.splitext(source_file)[0]
    cmd = ["cjc"] + flags + [source_file, "-o", base]
    print(f"[profile] {' '.join(cmd)}")

    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print(f"[profile] cjc exited with code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)

    # Find generated .prof files
    prof_files = glob.glob(f"{source_file}*.prof")
    if prof_files:
        print(f"\n[profile] Generated profiling files:")
        for f in prof_files:
            print(f"  {f}")
            print(f"  --- content ---")
            with open(f) as fh:
                print(fh.read())
    else:
        print(f"[profile] No .prof files generated. Check cjc output above.")


def analyze_prof(prof_file):
    """Display contents of a .prof file."""
    if not os.path.exists(prof_file):
        print(f"[profile] File not found: {prof_file}", file=sys.stderr)
        sys.exit(1)
    with open(prof_file) as f:
        print(f.read())


def main():
    parser = argparse.ArgumentParser(description="Profile Cangjie compiler")
    parser.add_argument("source", nargs="?", help="Cangjie source file to profile")
    parser.add_argument("--time", action="store_true", help="Profile compile time only")
    parser.add_argument("--memory", action="store_true", help="Profile memory only")
    parser.add_argument("--both", action="store_true", help="Profile both time and memory (default)")
    parser.add_argument("--analyze", metavar="PROF_FILE", help="Analyze an existing .prof file")
    args = parser.parse_args()

    if args.analyze:
        analyze_prof(args.analyze)
        return

    if not args.source:
        parser.error("source file is required (or use --analyze)")

    compiler_root = find_compiler_root()
    env = setup_env(compiler_root)

    profile_time = args.time or args.both or (not args.time and not args.memory)
    profile_memory = args.memory or args.both or (not args.time and not args.memory)

    run_profile(args.source, profile_time, profile_memory, env)


if __name__ == "__main__":
    main()
