#!/usr/bin/env python3
"""Build script for Cangjie compiler and its dependencies.

Supports platforms: linux_x86_64, linux_aarch64, mac_x86_64, mac_aarch64

Usage:
    python3 build-cangjie.py [--platform PLATFORM] [-t TYPE] [--version VERSION]
                             [--component COMPONENT] [--no-tests] [--incremental]
                             [--workspace WORKSPACE]

Examples:
    python3 build-cangjie.py --platform linux_x86_64 -t relwithdebinfo --no-tests
    python3 build-cangjie.py --platform mac_aarch64 --component compiler -t release --no-tests
    python3 build-cangjie.py --incremental --component cjc
    python3 build-cangjie.py --workspace /path/to/workspace -t debug
"""

import argparse
import multiprocessing
import os
import subprocess
import sys

SUPPORTED_PLATFORMS = ["linux_x86_64", "linux_aarch64", "mac_x86_64", "mac_aarch64"]
BUILD_TYPES = ["release", "relwithdebinfo", "debug"]
COMPONENTS = ["all", "compiler", "cjc", "runtime", "stdlib", "stdx", "tools"]

PLATFORM_CONFIG = {
    "linux_x86_64": {
        "runtime_output": "common/linux_release_x86_64",
        "stdx_target": "linux_x86_64_cjnative",
    },
    "linux_aarch64": {
        "runtime_output": "common/linux_release_aarch64",
        "stdx_target": "linux_aarch64_cjnative",
    },
    "mac_x86_64": {
        "runtime_output": "common/darwin_release_x86_64",
        "stdx_target": "darwin_x86_64_cjnative",
    },
    "mac_aarch64": {
        "runtime_output": "common/darwin_release_aarch64",
        "stdx_target": "darwin_aarch64_cjnative",
    },
}


def run(cmd, cwd=None):
    """Run a shell command and exit on failure."""
    print(f"[build] {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"[build] FAILED: {cmd}", file=sys.stderr)
        sys.exit(result.returncode)


def detect_platform():
    """Auto-detect the current platform."""
    import platform as plat
    machine = plat.machine().lower()
    system = plat.system().lower()

    if system == "linux":
        os_name = "linux"
    elif system == "darwin":
        os_name = "mac"
    else:
        print(f"Unsupported OS: {system}", file=sys.stderr)
        sys.exit(1)

    if machine in ("x86_64", "amd64"):
        arch = "x86_64"
    elif machine in ("aarch64", "arm64"):
        arch = "aarch64"
    else:
        print(f"Unsupported architecture: {machine}", file=sys.stderr)
        sys.exit(1)

    return f"{os_name}_{arch}"


def find_workspace_root(custom_workspace=None):
    """Find workspace root (parent of cangjie_compiler).
    
    Args:
        custom_workspace: Optional custom workspace path provided by user
        
    Returns:
        tuple: (workspace_root, compiler_root)
    """
    if custom_workspace:
        workspace_root = os.path.abspath(custom_workspace)
        compiler_root = os.path.join(workspace_root, "cangjie_compiler")
        if not os.path.exists(compiler_root):
            print(f"[build] ERROR: cangjie_compiler not found in {workspace_root}", file=sys.stderr)
            print(f"[build] Please check the workspace path or specify --workspace", file=sys.stderr)
            sys.exit(1)
        return workspace_root, compiler_root
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # scripts/ -> build-cangjie/ -> skills/ ->  -> cangjie_compiler/ -> workspace
    compiler_root = os.path.abspath(os.path.join(script_dir, "..", "..", "..", ".."))
    workspace_root = os.path.dirname(compiler_root)
    
    # Verify compiler_root exists
    if not os.path.exists(os.path.join(compiler_root, "build.py")):
        print(f"[build] ERROR: cangjie_compiler not found at {compiler_root}", file=sys.stderr)
        print(f"[build] Please specify workspace path using --workspace", file=sys.stderr)
        sys.exit(1)
    
    return workspace_root, compiler_root


def prepare_llvm(workspace_root, compiler_root):
    """Copy LLVM source into compiler third_party."""
    llvm_src = os.path.join(workspace_root, "llvm-project")
    llvm_dst = os.path.join(compiler_root, "third_party", "llvm-project")
    if not os.path.exists(llvm_src):
        print(f"[build] LLVM source not found at {llvm_src}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(llvm_dst):
        run(f"cp -R {llvm_src} {os.path.join(compiler_root, 'third_party/')}")
    else:
        print("[build] LLVM already in third_party, skipping copy")


def build_compiler(compiler_root, build_type, version, no_tests):
    """Build the Cangjie compiler."""
    cmd = f"python3 build.py -t {build_type} -v {version}"
    if no_tests:
        cmd += " --no-tests"
    run(cmd, cwd=compiler_root)


def build_cjc_incremental(compiler_root):
    """Incremental build of cjc only with parallel compilation."""
    build_dir = os.path.join(compiler_root, "build", "build")
    if not os.path.exists(build_dir):
        print(f"[build] ERROR: Build directory not found at {build_dir}", file=sys.stderr)
        print(f"[build] Please run a full build first (without --incremental)", file=sys.stderr)
        sys.exit(1)
    
    # Use all available CPU cores for parallel compilation
    num_jobs = multiprocessing.cpu_count()
    print(f"[build] Using {num_jobs} parallel jobs for incremental build")
    run(f"ninja cjc -j{num_jobs}", cwd=build_dir)


def build_runtime(workspace_root, compiler_root, platform, build_type, version):
    """Build the Cangjie runtime."""
    cfg = PLATFORM_CONFIG[platform]
    runtime_dir = os.path.join(workspace_root, "cangjie_runtime", "runtime")
    run("python3 build.py clean", cwd=runtime_dir)
    run(f"python3 build.py build -t {build_type} -v {version}", cwd=runtime_dir)
    run("python3 build.py install", cwd=runtime_dir)
    output_path = os.path.join(runtime_dir, "output", cfg["runtime_output"])
    dest = os.path.join(compiler_root, "output")
    run(f"cp -R {output_path}/lib {output_path}/runtime {dest}/")


def build_stdlib(workspace_root, compiler_root, build_type):
    """Build the standard library.

    Note: --target-lib must be an absolute path.
    """
    envsetup = os.path.join(compiler_root, "output", "envsetup.sh")
    stdlib_dir = os.path.join(workspace_root, "cangjie_runtime", "stdlib")
    # Use absolute path for runtime_output (required by build.py)
    runtime_output = os.path.abspath(os.path.join(workspace_root, "cangjie_runtime", "runtime", "output"))
    run(f"bash -c 'source {envsetup} && cd {stdlib_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {stdlib_dir} && python3 build.py build -t {build_type} --target-lib={runtime_output}'")
    run(f"bash -c 'source {envsetup} && cd {stdlib_dir} && python3 build.py install'")
    run(f"cp -R {os.path.join(stdlib_dir, 'output')}/* {os.path.join(compiler_root, 'output')}/")


def build_stdx(workspace_root, compiler_root, platform, build_type):
    """Build stdx."""
    cfg = PLATFORM_CONFIG[platform]
    stdx_dir = os.path.join(workspace_root, "cangjie_stdx")
    envsetup = os.path.join(compiler_root, "output", "envsetup.sh")
    run(f"bash -c 'source {envsetup} && cd {stdx_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {stdx_dir} && python3 build.py build -t {build_type}'")
    run(f"bash -c 'source {envsetup} && cd {stdx_dir} && python3 build.py install'")
    stdx_path = os.path.join(stdx_dir, "target", cfg["stdx_target"], "static", "stdx")
    print(f"\n[build] Set environment variables:")
    print(f"  export CANGJIE_STDX_PATH={stdx_path}")
    print(f"  export LD_LIBRARY_PATH={stdx_path}:$LD_LIBRARY_PATH")


def build_cangjie_tools(workspace_root, compiler_root, build_type, platform):
    """Build cangjie_tools (cjpm, cjcov, cjfmt, cjlint, etc) and install to output/tools/bin."""
    envsetup = os.path.join(compiler_root, "output", "envsetup.sh")
    tools_dir = os.path.join(workspace_root, "cangjie_tools")
    tools_bin_dir = os.path.join(compiler_root, "output", "tools", "bin")
    tools_config_dir = os.path.join(compiler_root, "output", "tools", "config")

    # Create output directories
    os.makedirs(tools_bin_dir, exist_ok=True)
    os.makedirs(tools_config_dir, exist_ok=True)

    # Determine RPATH based on platform
    cfg = PLATFORM_CONFIG[platform]
    if "darwin" in cfg["runtime_output"]:
        rpath = "@executable_path/../../runtime/lib"
    else:
        rpath = "$ORIGIN/../../runtime/lib"

    # Build cjpm (depends on stdx)
    print(f"\n[build] Building cjpm...")
    cjpm_dir = os.path.join(tools_dir, "cjpm", "build")
    run(f"bash -c 'source {envsetup} && cd {cjpm_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {cjpm_dir} && python3 build.py build -t {build_type} --set-rpath {rpath}'")
    run(f"bash -c 'source {envsetup} && cd {cjpm_dir} && python3 build.py install'")
    # Copy to output
    cjpm_dist = os.path.join(tools_dir, "cjpm", "dist")
    run(f"cp {os.path.join(cjpm_dist, 'cjpm')} {tools_bin_dir}/")
    # Copy config files if exist
    run(f"bash -c 'if ls {cjpm_dist}/*.toml 1> /dev/null 2>&1; then cp {cjpm_dist}/*.toml {tools_config_dir}/; fi'")

    # Build cjfmt
    print(f"\n[build] Building cjfmt...")
    cjfmt_dir = os.path.join(tools_dir, "cjfmt", "build")
    run(f"bash -c 'source {envsetup} && cd {cjfmt_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {cjfmt_dir} && python3 build.py build -t {build_type}'")
    run(f"bash -c 'source {envsetup} && cd {cjfmt_dir} && python3 build.py install'")

    # Build cjlint
    print(f"\n[build] Building cjlint...")
    cjlint_dir = os.path.join(tools_dir, "cjlint", "build")
    run(f"bash -c 'source {envsetup} && cd {cjlint_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {cjlint_dir} && python3 build.py build -t {build_type}'")
    run(f"bash -c 'source {envsetup} && cd {cjlint_dir} && python3 build.py install'")

    # Build cjcov (depends on stdx)
    print(f"\n[build] Building cjcov...")
    cjcov_dir = os.path.join(tools_dir, "cjcov", "build")
    run(f"bash -c 'source {envsetup} && cd {cjcov_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {cjcov_dir} && python3 build.py build -t {build_type}'")
    run(f"bash -c 'source {envsetup} && cd {cjcov_dir} && python3 build.py install'")

    # Build cjtrace-recover
    print(f"\n[build] Building cjtrace-recover...")
    cjtrace_dir = os.path.join(tools_dir, "cjtrace-recover", "build")
    cangjie_home = os.environ.get("CANGJIE_HOME", os.path.join(compiler_root, "output"))
    run(f"bash -c 'source {envsetup} && cd {cjtrace_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {cjtrace_dir} && python3 build.py build -t {build_type}'")
    run(f"bash -c 'source {envsetup} && cd {cjtrace_dir} && python3 build.py install --prefix {cangjie_home}/tools'")

    # Build hyperlangExtension (hle) if exists
    hle_dir = os.path.join(tools_dir, "hyperlangExtension", "build")
    if os.path.exists(hle_dir):
        print(f"\n[build] Building hyperlangExtension...")
        run(f"bash -c 'source {envsetup} && cd {hle_dir} && python3 build.py clean'")
        run(f"bash -c 'source {envsetup} && cd {hle_dir} && python3 build.py build -t {build_type}'")
        run(f"bash -c 'source {envsetup} && cd {hle_dir} && python3 build.py install'")

    # Build cangjie-language-server (lsp)
    print(f"\n[build] Building cangjie-language-server...")
    lsp_dir = os.path.join(tools_dir, "cangjie-language-server", "build")
    run(f"bash -c 'source {envsetup} && cd {lsp_dir} && python3 build.py clean'")
    run(f"bash -c 'source {envsetup} && cd {lsp_dir} && python3 build.py build -t {build_type} -j 32'")
    run(f"bash -c 'source {envsetup} && cd {lsp_dir} && python3 build.py install'")

    print(f"\n[build] All cangjie_tools built and installed to {tools_bin_dir}")


def verify_build(compiler_root):
    """Verify the build by compiling and running a hello world program."""
    envsetup = os.path.join(compiler_root, "output", "envsetup.sh")
    test_code = 'main() { println("Hello, Cangjie") }'
    run(f"bash -c 'source {envsetup} && cd /tmp && echo \\'{test_code}\\' > hello.cj && cjc hello.cj -o hello && ./hello'")


def prompt_build_type():
    """Prompt user for build type if running interactively."""
    if not sys.stdin.isatty():
        return "relwithdebinfo"
    
    print("\n[build] Select build type:")
    print("  1. release         - Optimized, no debug info")
    print("  2. relwithdebinfo  - Optimized with debug info (default)")
    print("  3. debug           - No optimization, full debug info")
    
    choice = input("\nEnter choice [1-3] (default: 2): ").strip()
    
    if choice == "1":
        return "release"
    elif choice == "3":
        return "debug"
    else:
        return "relwithdebinfo"


def main():
    parser = argparse.ArgumentParser(description="Build Cangjie compiler and dependencies")
    parser.add_argument("--platform", choices=SUPPORTED_PLATFORMS, default=None,
                        help="Target platform (auto-detected if omitted)")
    parser.add_argument("-t", "--build-type", choices=BUILD_TYPES, default=None,
                        help="Build type: release, relwithdebinfo, debug (default: relwithdebinfo, prompted if interactive)")
    parser.add_argument("--version", default="1.1.0.beta.999",
                        help="Version string (default: 1.1.0.beta.999)")
    parser.add_argument("--component", choices=COMPONENTS, default="all",
                        help="Component to build (default: all)")
    parser.add_argument("--no-tests", action="store_true",
                        help="Skip unittest compilation (recommended for faster builds)")
    parser.add_argument("--incremental", action="store_true",
                        help="Incremental build with parallel compilation (only for cjc component)")
    parser.add_argument("--verify", action="store_true",
                        help="Run verification after build")
    parser.add_argument("--workspace", default=None,
                        help="Workspace root path (auto-detected if omitted)")
    args = parser.parse_args()

    # Determine build type
    build_type = args.build_type
    if build_type is None and not args.incremental:
        build_type = prompt_build_type()
    elif build_type is None:
        build_type = "relwithdebinfo"

    platform = args.platform or detect_platform()
    print(f"[build] Platform: {platform}")
    print(f"[build] Build type: {build_type}")
    print(f"[build] Component: {args.component}")
    print(f"[build] Skip tests: {args.no_tests}")

    workspace_root, compiler_root = find_workspace_root(args.workspace)
    print(f"[build] Workspace: {workspace_root}")
    print(f"[build] Compiler: {compiler_root}")

    if args.incremental and args.component == "cjc":
        build_cjc_incremental(compiler_root)
        return

    if args.component in ("all", "compiler"):
        prepare_llvm(workspace_root, compiler_root)
        build_compiler(compiler_root, build_type, args.version, args.no_tests)

    if args.component in ("all", "runtime"):
        # Use dash version for runtime
        rt_version = args.version.replace(".beta.", "-beta.")
        build_runtime(workspace_root, compiler_root, platform, build_type, rt_version)

    if args.component in ("all", "stdlib"):
        build_stdlib(workspace_root, compiler_root, build_type)

    if args.component in ("all", "stdx"):
        build_stdx(workspace_root, compiler_root, platform, build_type)

    if args.component in ("all", "tools"):
        build_cangjie_tools(workspace_root, compiler_root, build_type, platform)

    if args.verify or args.component == "all":
        verify_build(compiler_root)

    print("\n[build] Done.")


if __name__ == "__main__":
    main()
