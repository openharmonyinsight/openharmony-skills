#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CLANG_FORMAT_CONFIG = SCRIPT_DIR / ".clang-format"
CLANG_TIDY_CONFIG = SCRIPT_DIR / ".clang-tidy"
FORMAT_EXTENSIONS = {".h", ".hh", ".hpp", ".hxx", ".c", ".cc", ".cpp", ".cxx"}
TIDY_EXTENSIONS = {".c", ".cc", ".cpp", ".cxx"}
OHOS_ROOT_ENV_VARS = ("OHOS_ROOT", "OHOS_BASE", "OPENHARMONY_ROOT")


def collect_files(paths: list[str], extensions: set[str]) -> list[Path]:
    if not paths:
        paths = ["."]

    collected: list[Path] = []
    seen: set[Path] = set()

    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(f"path not found: {path}")
        if path.is_file():
            if path.suffix.lower() in extensions:
                resolved = path.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    collected.append(resolved)
            continue

        for child in path.rglob("*"):
            if not child.is_file():
                continue
            if child.suffix.lower() not in extensions:
                continue
            resolved = child.resolve()
            if resolved not in seen:
                seen.add(resolved)
                collected.append(resolved)

    return sorted(collected)


def run_command(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    completed = subprocess.run(cmd)
    return completed.returncode


def host_tags() -> list[str]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "linux":
        return ["linux-x86_64"]
    if system == "darwin":
        return ["darwin-arm64", "darwin-x86_64"] if machine in {"arm64", "aarch64"} else ["darwin-x86_64", "darwin-arm64"]
    if system == "windows":
        return ["windows-x86_64"]
    return []


def build_tool_host_tags() -> list[str]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "linux":
        return ["linux-x86", "linux-x86_64"]
    if system == "darwin":
        return ["darwin-arm64", "darwin-x86_64"] if machine in {"arm64", "aarch64"} else ["darwin-x86_64", "darwin-arm64"]
    if system == "windows":
        return ["windows-x86", "windows-x86_64"]
    return []


def candidate_roots(paths: list[str], explicit_root: str | None) -> list[Path]:
    roots: list[Path] = []
    if explicit_root:
        roots.append(Path(explicit_root))
    for env_var in OHOS_ROOT_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            roots.append(Path(value))
    roots.append(Path.cwd())
    for raw in paths:
        path = Path(raw)
        roots.append(path if path.is_dir() else path.parent)
    return roots


def find_ohos_root(paths: list[str], explicit_root: str | None) -> Path | None:
    seen: set[Path] = set()
    for root in candidate_roots(paths, explicit_root):
        try:
            current = root.resolve()
        except OSError:
            continue
        for candidate in [current, *current.parents]:
            if candidate in seen:
                continue
            seen.add(candidate)
            if (candidate / "prebuilts" / "clang").is_dir():
                return candidate
    return None


def executable_name(name: str) -> str:
    return f"{name}.exe" if platform.system().lower() == "windows" else name


def first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.is_file():
            return path
    return None


def find_prebuilt_tool(ohos_root: Path | None, name: str) -> Path | None:
    if ohos_root is None:
        return None

    tool_name = executable_name(name)
    clang_root = ohos_root / "prebuilts" / "clang"
    direct_candidates: list[Path] = []
    for tag in host_tags():
        direct_candidates.extend(
            [
                clang_root / "ohos" / tag / "llvm" / "bin" / tool_name,
                clang_root / "host" / tag / "llvm" / "bin" / tool_name,
            ]
        )
        direct_candidates.extend(sorted((clang_root / "ohos" / tag).glob(f"**/bin/{tool_name}")))
        direct_candidates.extend(sorted((clang_root / "host" / tag).glob(f"**/bin/{tool_name}")))

    return first_existing(direct_candidates)


def find_prebuilt_build_tool(ohos_root: Path | None, name: str) -> Path | None:
    if ohos_root is None:
        return None

    tool_name = executable_name(name)
    build_tools = ohos_root / "prebuilts" / "build-tools"
    candidates: list[Path] = []
    for tag in build_tool_host_tags():
        candidates.append(build_tools / tag / "bin" / tool_name)
    return first_existing(candidates)


def resolve_build_tool(name: str, ohos_root: Path | None) -> str | None:
    prebuilt = find_prebuilt_build_tool(ohos_root, name)
    if prebuilt is not None:
        return str(prebuilt)

    path_tool = shutil.which(name)
    if path_tool is not None:
        print(f"{name}: OpenHarmony host prebuilt not found; falling back to PATH: {path_tool}", file=sys.stderr)
    return path_tool


def resolve_tool(name: str, explicit: str | None, ohos_root: Path | None) -> str | None:
    if explicit:
        path = Path(explicit)
        return str(path.resolve()) if path.exists() else explicit

    prebuilt = find_prebuilt_tool(ohos_root, name)
    if prebuilt is not None:
        return str(prebuilt)

    path_tool = shutil.which(name)
    if path_tool is not None:
        print(f"{name}: OHOS prebuilt not found; falling back to PATH: {path_tool}", file=sys.stderr)
    return path_tool


def normalize_compile_db_path(raw: str) -> Path | None:
    candidate = Path(raw)
    if candidate.is_dir():
        db = candidate / "compile_commands.json"
        return candidate.resolve() if db.exists() else None
    return candidate.parent.resolve() if candidate.name == "compile_commands.json" and candidate.exists() else None


def find_compile_db(explicit: str | None, ohos_root: Path | None) -> Path | None:
    if explicit:
        return normalize_compile_db_path(explicit)

    candidates: list[Path] = [Path("."), Path("build"), Path("out")]
    if ohos_root is not None:
        candidates.extend([ohos_root, ohos_root / "out"])

    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        db = candidate / "compile_commands.json"
        if db.exists():
            return resolved
    return None


def resolve_build_dir(raw: str, ohos_root: Path | None) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    if ohos_root is not None:
        return ohos_root / path
    return path


def generate_compile_db(ohos_root: Path | None, build_dir: str, output: str | None) -> Path | None:
    if ohos_root is None:
        print("cannot generate compile_commands.json without an OpenHarmony root; pass --ohos-root", file=sys.stderr)
        return None

    ninja = resolve_build_tool("ninja", ohos_root)
    if ninja is None:
        print("ninja not found under OpenHarmony host prebuilts/build-tools or PATH", file=sys.stderr)
        return None

    resolved_build_dir = resolve_build_dir(build_dir, ohos_root)
    if not resolved_build_dir.is_dir():
        print(f"build directory not found: {resolved_build_dir}", file=sys.stderr)
        return None

    output_path = Path(output) if output else ohos_root / "out" / "compile_commands.json"
    if not output_path.is_absolute():
        output_path = ohos_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [str(ninja), "-C", str(resolved_build_dir), "-w", "dupbuild=warn", "-t", "compdb", "cc", "cxx"]
    print("+", " ".join(cmd), ">", output_path)
    completed = subprocess.run(cmd, stdout=subprocess.PIPE)
    if completed.returncode != 0:
        return None
    output_path.write_bytes(completed.stdout)
    return output_path.parent.resolve()


def is_ohos_prebuilt_tool(tool: str) -> bool:
    try:
        parts = Path(tool).resolve().parts
    except OSError:
        return False
    return "prebuilts" in parts and "clang" in parts


def fallback_libcxx_include_dirs(ohos_root: Path | None) -> list[Path]:
    if ohos_root is None:
        return []

    candidates: list[Path] = [
        ohos_root / "third_party" / "llvm-project" / "libcxx" / "include",
        ohos_root / "third_party" / "libcxx" / "include",
    ]
    for tag in host_tags():
        candidates.extend(
            [
                ohos_root / "prebuilts" / "clang" / "ohos" / tag / "llvm_ndk" / "include" / "libcxx-ohos" / "include" / "c++" / "v1",
                ohos_root / "prebuilts" / "clang" / "ohos" / tag / "llvm" / "include" / "c++" / "v1",
            ]
        )

    includes: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if not candidate.is_dir():
            continue
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        includes.append(resolved)
    return includes


def default_tidy_extra_args(clang_tidy: str, ohos_root: Path | None) -> list[str]:
    if is_ohos_prebuilt_tool(clang_tidy):
        return []

    args: list[str] = []
    for include_dir in fallback_libcxx_include_dirs(ohos_root):
        args.extend(["-isystem", str(include_dir)])
    return args


def run_clang_format(clang_format: str, files: list[Path], fix: bool) -> int:
    if not files:
        print("clang-format: no matching files")
        return 0

    style = f"file:{CLANG_FORMAT_CONFIG}" if CLANG_FORMAT_CONFIG.exists() else "file"
    cmd = [clang_format, f"-style={style}"]
    if fix:
        cmd.append("-i")
    else:
        cmd.extend(["--dry-run", "--Werror"])
    cmd.extend(str(path) for path in files)
    return run_command(cmd)


def run_clang_tidy(
    clang_tidy: str,
    files: list[Path],
    compile_db: Path | None,
    extra_args: list[str],
) -> int:
    if not files:
        print("clang-tidy: no matching files")
        return 0

    overall = 0
    for path in files:
        cmd = [clang_tidy, str(path)]
        if CLANG_TIDY_CONFIG.exists():
            cmd.append(f"--config-file={CLANG_TIDY_CONFIG}")
        if compile_db is not None:
            cmd.extend(["-p", str(compile_db)])
        else:
            cmd.append("--")
            cmd.append("-std=c++17")
        for arg in extra_args:
            if compile_db is not None:
                cmd.extend(["--extra-arg", arg])
            else:
                cmd.append(arg)
        rc = run_command(cmd)
        if rc != 0:
            overall = rc
    return overall


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run OpenHarmony-oriented clang-format / clang-tidy guards from packaged skill config."
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to inspect. Defaults to current directory.")
    parser.add_argument("--format-only", action="store_true", help="Run only clang-format checks.")
    parser.add_argument("--tidy-only", action="store_true", help="Run only clang-tidy checks.")
    parser.add_argument("--fix-format", action="store_true", help="Apply clang-format in place instead of dry-run.")
    parser.add_argument("--compile-db", help="Path to compile_commands.json or its containing directory.")
    parser.add_argument("--build-dir", default="out/rk3568", help="OpenHarmony GN/Ninja build directory used for compile database generation or lookup.")
    parser.add_argument(
        "--generate-compile-db",
        action="store_true",
        help="Generate compile_commands.json with OpenHarmony prebuilt ninja before running clang-tidy.",
    )
    parser.add_argument(
        "--compile-db-output",
        default="out/compile_commands.json",
        help="Output path for --generate-compile-db. Defaults to out/compile_commands.json under the OpenHarmony root.",
    )
    parser.add_argument("--ohos-root", help="OpenHarmony source root. Defaults to OHOS_ROOT/OHOS_BASE/OPENHARMONY_ROOT or upward search.")
    parser.add_argument("--clang-format", help="Path to clang-format. Defaults to OHOS prebuilts before PATH.")
    parser.add_argument("--clang-tidy", help="Path to clang-tidy. Defaults to OHOS prebuilts before PATH.")
    parser.add_argument(
        "--no-fallback-cxx-includes",
        action="store_true",
        help="Do not add OpenHarmony libc++ include paths when falling back to a non-OHOS clang-tidy.",
    )
    parser.add_argument(
        "--no-ohos-cxx-includes",
        action="store_true",
        dest="no_fallback_cxx_includes",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        help="Extra compiler argument forwarded to clang-tidy. Repeatable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.format_only and args.tidy_only:
        print("--format-only and --tidy-only cannot be used together", file=sys.stderr)
        return 2

    need_format = not args.tidy_only
    need_tidy = not args.format_only
    ohos_root = find_ohos_root(args.paths, args.ohos_root)
    if ohos_root is not None:
        print(f"OHOS root: {ohos_root}")

    overall = 0

    if need_format:
        clang_format = resolve_tool("clang-format", args.clang_format, ohos_root)
        if clang_format is None:
            print("clang-format not found in OHOS prebuilts or PATH", file=sys.stderr)
            overall = 1
        else:
            format_files = collect_files(args.paths, FORMAT_EXTENSIONS)
            rc = run_clang_format(clang_format, format_files, args.fix_format)
            if rc != 0:
                overall = rc

    if need_tidy:
        clang_tidy = resolve_tool("clang-tidy", args.clang_tidy, ohos_root)
        if clang_tidy is None:
            print("clang-tidy not found in OHOS prebuilts or PATH", file=sys.stderr)
            overall = 1
        else:
            tidy_files = collect_files(args.paths, TIDY_EXTENSIONS)
            compile_db = find_compile_db(args.compile_db, ohos_root)
            if compile_db is None and args.generate_compile_db:
                compile_db = generate_compile_db(ohos_root, args.build_dir, args.compile_db_output)
            if compile_db is None:
                print("compile_commands.json not found; falling back to -- -std=c++17", file=sys.stderr)
            extra_args = list(args.extra_arg)
            if not args.no_fallback_cxx_includes:
                extra_args = default_tidy_extra_args(clang_tidy, ohos_root) + extra_args
            rc = run_clang_tidy(clang_tidy, tidy_files, compile_db, extra_args)
            if rc != 0:
                overall = rc

    return overall


if __name__ == "__main__":
    sys.exit(main())
