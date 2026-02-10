#!/usr/bin/env python3
"""
Scan C/C++ codebase for circular dependencies between directory modules.

Parses GN build files to understand include paths and generates a markdown report.

A "module" is defined as a directory containing C/C++ files.
Detects circular dependencies between these directory modules.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Set, List, Tuple
from collections import defaultdict


@dataclass
class IncludeInfo:
    """Represents an include directive found in a file."""
    included_file: str
    line_number: int
    is_system: bool


@dataclass
class FileInfo:
    """Represents a C/C++ source/header file."""
    path: str
    dir_path: str
    includes: List[IncludeInfo] = field(default_factory=list)
    file_type: str = ""  # 'header' or 'source'


@dataclass
class CircularDependency:
    """Represents a circular dependency path."""
    cycle: List[str]  # List of directory paths
    cycle_type: str  # 'header' or 'module' or 'directory'


@dataclass
class ModuleInfo:
    """Represents a module - a directory with C/C++ files."""
    dir_path: str
    files: List[str] = field(default_factory=list)
    module_name: str = ""


# C/C++ file extensions
HEADER_EXTENSIONS = {'.h', '.hpp', '.hh', '.hxx', '.h++', '.inl', '.inc'}
SOURCE_EXTENSIONS = {'.c', '.cpp', '.cc', '.cxx', '.c++'}
CPP_EXTENSIONS = HEADER_EXTENSIONS | SOURCE_EXTENSIONS

# Pattern for #include directives
INCLUDE_PATTERN = re.compile(
    r'^\s*#\s*include\s+(?P<angle><[^>]+>|"[^"]+")',
    re.MULTILINE
)

# GN build file patterns
GN_INCLUDE_DIR = re.compile(r'"([^"]+)"')


def get_file_type(file_path: Path) -> str:
    """Determine if a file is a header or source file."""
    ext = file_path.suffix.lower()
    if ext in HEADER_EXTENSIONS:
        return 'header'
    elif ext in SOURCE_EXTENSIONS:
        return 'source'
    return 'unknown'


def parse_gn_build_file(gn_file: Path) -> List[str]:
    """Parse a BUILD.gn or *.gni file to extract include directories."""
    try:
        content = gn_file.read_text(encoding='utf-8')
    except Exception:
        return []

    include_dirs = []

    # Find include_dirs = [...] assignments
    for match in re.finditer(r'include_dirs\s*=\s*\[([^\]]+)', content):
        section = match.group(1)
        for dir_match in GN_INCLUDE_DIR.finditer(section):
            include_dirs.append(dir_match.group(1))

    # Check for cflags with -I
    for match in re.finditer(r'cflags\s*=\s*\[([^\]]+)', content):
        for flag_match in re.finditer(r'-I([^"]+)"', match.group(1)):
            include_dirs.append(flag_match.group(1))

    return include_dirs


def find_gn_build_files(root_path: Path) -> List[Path]:
    """Find all BUILD.gn and *.gni files in the project."""
    build_files = []
    skip_dirs = {'build', 'out', 'node_modules', '.git', 'third_party',
                 'vendor', 'external', '__pycache__', 'cmake-build'}

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for filename in files:
            if filename == 'BUILD.gn' or filename.endswith('.gni'):
                build_files.append(Path(root) / filename)

    return build_files


def normalize_include_path(include: str, source_dir: Path,
                           include_dirs: Set[Path], file_cache: Dict[str, str]) -> str:
    """Normalize an include path to an actual file path."""
    # Extract the path from angle brackets or quotes
    match = INCLUDE_PATTERN.match(f'#include {include}')
    if not match:
        return ""

    include_path = match.group('angle').strip('<>').strip('"')

    # Check cache first
    cache_key = str(source_dir) + "::" + include_path
    if cache_key in file_cache:
        return file_cache[cache_key]

    # Try to resolve the include path
    candidates = []

    # Check relative to source file
    rel_path = source_dir / include_path
    if rel_path.exists():
        candidates.append(str(rel_path.resolve()))

    # Check all include directories
    for inc_dir in include_dirs:
        check_path = inc_dir / include_path
        if check_path.exists():
            candidates.append(str(check_path.resolve()))

    # Try appending .h, .hpp if no extension
    if not Path(include_path).suffix:
        for suffix in ('.h', '.hpp'):
            rel_path = source_dir / (include_path + suffix)
            if rel_path.exists():
                candidates.append(str(rel_path.resolve()))
            for inc_dir in include_dirs:
                check_path = inc_dir / (include_path + suffix)
                if check_path.exists():
                    candidates.append(str(check_path.resolve()))

    # Cache and return
    result = candidates[0] if candidates else include_path
    file_cache[cache_key] = result
    return result


def scan_file(file_path: Path, include_dirs: Set[Path], file_cache: Dict[str, str]) -> FileInfo:
    """Scan a single C/C++ file for includes."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return FileInfo(
            path=str(file_path.resolve()),
            dir_path=str(file_path.parent.resolve()),
            file_type=get_file_type(file_path)
        )

    file_info = FileInfo(
        path=str(file_path.resolve()),
        dir_path=str(file_path.parent.resolve()),
        file_type=get_file_type(file_path)
    )

    source_dir = file_path.parent

    for match in INCLUDE_PATTERN.finditer(content):
        include_spec = match.group('angle')
        line_num = content[:match.start()].count('\n') + 1
        is_system = include_spec.startswith('<')

        if not is_system:  # Only track local includes
            resolved = normalize_include_path(include_spec, source_dir, include_dirs, file_cache)
            file_info.includes.append(IncludeInfo(
                included_file=resolved,
                line_number=line_num,
                is_system=is_system
            ))

    return file_info


def get_component_module(dir_path: str, root_path: Path) -> str:
    """
    Get the component/module name for a file directory.
    Handles the common src/include pattern:
    - Files in path/to/cpp/src/<name>/* -> path/to/cpp/<name>
    - Files in path/to/cpp/include/<name>/* -> path/to/cpp/<name>
    - Otherwise, use the directory itself
    """
    try:
        relative_parts = list(Path(dir_path).relative_to(root_path).parts)
    except ValueError:
        relative_parts = list(Path(dir_path).parts)

    # Check for .../cpp/src/<component>/ or .../cpp/include/<component>/ pattern
    # In this case, we want to group by .../cpp/<component>
    if len(relative_parts) >= 3:
        # Find the position of 'cpp' in the path
        cpp_idx = -1
        for i, part in enumerate(relative_parts):
            if part == 'cpp':
                cpp_idx = i
                break

        # Check if we have pattern: .../cpp/src/<component>/ or .../cpp/include/<component>/
        if cpp_idx >= 0 and cpp_idx + 3 <= len(relative_parts):
            if cpp_idx + 2 < len(relative_parts):
                subdir = relative_parts[cpp_idx + 1]
                component = relative_parts[cpp_idx + 2]
                if subdir in ('src', 'include') and component not in ('src', 'include'):
                    # Found pattern: .../cpp/src/<component>/ or .../cpp/include/<component>/
                    # Group by: .../cpp/<component>
                    component_parts = relative_parts[:cpp_idx + 1] + [component]
                    return '/'.join(component_parts)

    # Default: use the full directory path
    try:
        rel_path = str(Path(dir_path).relative_to(root_path))
    except ValueError:
        rel_path = dir_path
    return rel_path.replace(os.sep, '/')


def group_files_by_directory(all_files: Dict[str, FileInfo],
                              root_path: Path) -> Tuple[Dict[str, ModuleInfo], Dict[str, str]]:
    """
    Group files by component/module into modules.
    Handles src/ and include/ subdirectories as part of the same component.
    Returns (modules dict, file_to_module mapping).
    """
    modules = {}
    file_to_module = {}
    component_to_files = defaultdict(list)

    # First pass: group files by component module
    for file_path, file_info in all_files.items():
        dir_path = file_info.dir_path
        module_name = get_component_module(dir_path, root_path)
        component_to_files[module_name].append(file_path)

    # Create modules for each component
    for module_name, files in component_to_files.items():
        # Only create modules for components with actual source files
        has_source = any(all_files[f].file_type == 'source' for f in files)
        if has_source:
            modules[module_name] = ModuleInfo(
                dir_path=module_name,  # Store module name as dir_path
                files=files.copy(),
                module_name=module_name
            )

    # Build file to module mapping (including headers from include/ dirs)
    for mod_name, mod_info in modules.items():
        for file_path in mod_info.files:
            file_to_module[file_path] = mod_name

    # Also map header files to their component's module
    # This is important for detecting when a source file includes a header from another component
    for file_path, file_info in all_files.items():
        if file_path not in file_to_module:
            dir_path = file_info.dir_path
            module_name = get_component_module(dir_path, root_path)
            if module_name in modules:
                file_to_module[file_path] = module_name

    return modules, file_to_module


def find_directory_cycles(all_files: Dict[str, FileInfo],
                         modules: Dict[str, ModuleInfo],
                         file_to_module: Dict[str, str],
                         root_path: Path) -> List[CircularDependency]:
    """
    Find circular dependencies between directory modules.
    A directory A depends on directory B if any file in A includes any file in B.
    """
    # Build directory dependency graph
    graph = defaultdict(set)  # module_name -> set of dependent module names

    # Track which files in each module are included by others
    module_file_set = {}  # module_name -> set of file paths in that module
    for mod_name, mod_info in modules.items():
        module_file_set[mod_name] = set(mod_info.files)

    # Build dependencies: for each file in each module, check what it includes
    for mod_name, mod_info in modules.items():
        dependencies = set()

        for file_path in mod_info.files:
            file_info = all_files.get(file_path)
            if not file_info:
                continue

            for inc in file_info.includes:
                if inc.included_file:
                    # Check if the included file belongs to any module
                    target_mod = file_to_module.get(inc.included_file)
                    if target_mod and target_mod != mod_name:
                        dependencies.add(target_mod)

        graph[mod_name] = dependencies

    # Find cycles using DFS
    cycles = []
    visited = set()
    rec_stack = set()

    def dfs(node: str, path: List[str]) -> None:
        if node in rec_stack:
            # Found a cycle
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return

        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, set()):
            if neighbor in modules:  # Only follow edges to known modules
                dfs(neighbor, path + [node])

        rec_stack.remove(node)

    for mod_name in modules:
        if mod_name not in visited:
            dfs(mod_name, [])

    # Deduplicate cycles
    unique_cycles = []
    seen = set()

    for cycle in cycles:
        # Normalize by rotating to start with smallest element
        min_idx = cycle.index(min(cycle))
        rotated = tuple(cycle[min_idx:] + cycle[:min_idx])
        reverse_rotated = tuple(reversed(rotated))

        if rotated not in seen and reverse_rotated not in seen:
            seen.add(rotated)
            unique_cycles.append(cycle)

    return [CircularDependency(cycle=c, cycle_type='directory') for c in unique_cycles]


def scan_project(root_path: Path, verbose: bool = False) -> Tuple[Dict[str, FileInfo], Set[Path]]:
    """Scan entire project for C/C++ files."""
    all_files = {}
    all_include_dirs = {root_path.resolve()}
    file_cache = {}
    skip_dirs = {'build', 'out', 'node_modules', '.git', 'third_party',
                 'vendor', 'external', '__pycache__', 'cmake-build'}

    # Find GN build files
    if verbose:
        print("Finding GN build files...", file=sys.stderr, flush=True)
    gn_files = find_gn_build_files(root_path)

    for gn_file in gn_files:
        include_dirs = parse_gn_build_file(gn_file)
        for inc_dir in include_dirs:
            if not os.path.isabs(inc_dir):
                inc_path = (gn_file.parent / inc_dir).resolve()
            else:
                inc_path = Path(inc_dir).resolve()

            if inc_path.exists():
                all_include_dirs.add(inc_path)

    # Scan files
    if verbose:
        print("Scanning C/C++ files...", file=sys.stderr, flush=True)
    count = 0
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in CPP_EXTENSIONS:
                file_path = Path(root) / filename
                file_info = scan_file(file_path, all_include_dirs, file_cache)
                all_files[file_info.path] = file_info
                count += 1
                if verbose and count % 500 == 0:
                    print(f"  Scanned {count} files...", file=sys.stderr, flush=True)

    return all_files, all_include_dirs


def generate_markdown_report(directory_cycles: List[CircularDependency],
                             all_files: Dict[str, FileInfo],
                             modules: Dict[str, ModuleInfo],
                             root_path: Path,
                             include_dirs: Set[Path]) -> str:
    """Generate a markdown report."""
    lines = [
        "# C/C++ Circular Dependency Report (Directory-Based)",
        "",
        f"**Scan Path:** `{root_path}`",
        "",
        f"**Include Directories:** {len(include_dirs)}",
        f"**Files Scanned:** {len(all_files)}",
        f"**Directory Modules:** {len(modules)}",
    ]

    if directory_cycles:
        lines.append(f"**Circular Dependencies:** {len(directory_cycles)}")

    lines.extend(["", "---", ""])

    if directory_cycles:
        lines.extend([
            "## Directory Circular Dependencies",
            "",
            f"Detected {len(directory_cycles)} circular dependencies **between directory modules**.",
            "",
            "A module is a directory containing C/C++ source files.",
            "",
        ])

        for i, cycle in enumerate(directory_cycles, 1):
            lines.extend([f"### Cycle {i}", "", "```"])
            for j, mod_name in enumerate(cycle.cycle):
                lines.append(f"{mod_name}")
            lines.extend(["```", ""])

            # Show details of what each directory includes
            lines.append("**Dependency Details:**")
            lines.append("")

            for j, mod_name in enumerate(cycle.cycle):
                if j == 0:
                    lines.append(f"- `{mod_name}/`")
                else:
                    lines.append(f"  ↓ depends on")
                    lines.append(f"- `{mod_name}/`")

                # Show which files in this directory create the dependency
                mod_info = modules.get(mod_name)
                next_mod = cycle.cycle[(j + 1) % len(cycle.cycle)]

                if mod_info and j < len(cycle.cycle) - 1:
                    # Find files that include something from the next module
                    next_mod_info = modules.get(next_mod)
                    if next_mod_info:
                        next_files = set(next_mod_info.files)
                        deps_found = []

                        for file_path in mod_info.files:
                            file_info = all_files.get(file_path)
                            if file_info:
                                for inc in file_info.includes:
                                    if inc.included_file in next_files:
                                        filename = Path(file_path).name
                                        target_file = Path(inc.included_file).name
                                        deps_found.append(f"  - `{filename}` includes `{target_file}` (line {inc.line_number})")
                                        break

                        if deps_found:
                            lines.extend(deps_found[:3])  # Show up to 3 examples
                            if len(deps_found) > 3:
                                lines.append(f"  - ... and {len(deps_found) - 3} more")

                lines.append("")

            lines.extend(["---", ""])

    else:
        lines.extend([
            "## Result",
            "",
            "No circular dependencies detected between directory modules!",
            "",
        ])

    if directory_cycles:
        lines.extend([
            "## Recommendations",
            "",
            "- Extract common code into a separate shared directory",
            "- Use interfaces to decouple implementations",
            "- Consider restructuring if directories are tightly coupled",
            "",
        ])

    # Directory modules section
    lines.extend(["---", "", "## Directory Modules", ""])
    for mod_name in sorted(modules.keys()):
        mod_info = modules[mod_name]
        file_count = len(mod_info.files)
        lines.append(f"- `{mod_name}/` - {file_count} files")

    # Include directories
    lines.extend(["---", "", "## Include Directories", ""])
    for inc_dir in sorted(include_dirs)[:20]:
        rel_path = str(Path(inc_dir).relative_to(root_path)) if str(inc_dir).startswith(str(root_path)) else str(inc_dir)
        lines.append(f"- `{rel_path}`")
    if len(include_dirs) > 20:
        lines.append(f"- ... and {len(include_dirs) - 20} more")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Scan C/C++ codebase for circular dependencies between directory modules.'
    )
    parser.add_argument('path', help='Path to the C/C++ project')
    parser.add_argument('-o', '--output', help='Output markdown file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--no-gn', action='store_true',
                        help='Skip GN parsing')

    args = parser.parse_args()
    scan_path = Path(args.path)

    if not scan_path.exists():
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    if args.verbose:
        print(f"Scanning: {scan_path}", file=sys.stderr)

    all_files, include_dirs = scan_project(scan_path, args.verbose)

    if args.verbose:
        print(f"Files: {len(all_files)}, Include dirs: {len(include_dirs)}", file=sys.stderr)

    modules, file_to_module = group_files_by_directory(all_files, scan_path)

    if args.verbose:
        print(f"Directory modules: {len(modules)}", file=sys.stderr)

    directory_cycles = find_directory_cycles(all_files, modules, file_to_module, scan_path)

    if args.verbose:
        print(f"Circular dependencies: {len(directory_cycles)}", file=sys.stderr)

    report = generate_markdown_report(directory_cycles, all_files, modules, scan_path, include_dirs)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report: {args.output}", file=sys.stderr)
    else:
        print(report)

    return 0 if not directory_cycles else 1


if __name__ == '__main__':
    sys.exit(main())
