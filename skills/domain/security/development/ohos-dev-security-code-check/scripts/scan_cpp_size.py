#!/usr/bin/env python3
"""
Scan C/C++ source files for extra large files and functions.
Reports files and functions with 2000+ non-blank, non-comment lines.
"""

import argparse
import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class LargeFunction:
    """Represents a function that exceeds the size threshold."""
    name: str
    line_start: int
    line_end: int
    lines_count: int
    file_path: str


@dataclass
class LargeFile:
    """Represents a file that exceeds the size threshold."""
    path: str
    lines_count: int
    large_functions: List[LargeFunction]


# C/C++ file extensions
CPP_EXTENSIONS = {
    '.c', '.cpp', '.cc', '.cxx', '.c++',
    '.h', '.hpp', '.hh', '.hxx', '.h++',
    '.inl', '.inc'
}

# Patterns for detecting function definitions
# Matches: return_type function_name(params) or return_type class::function_name(params)
FUNCTION_PATTERNS = [
    # Standard function: type name(params) or type name(params) const/override/final
    re.compile(
        r'^\s*(?:template\s*<[^>]*>\s*)?'  # optional template
        r'(?:[\w\s\*&:]+?)'  # return type (lazy match)
        r'\b([a-zA-Z_]\w*)\s*'  # function name
        r'(?:\s*::\s*[a-zA-Z_]\w*)?'  # optional qualifier for class::method
        r'\s*\([^)]*\)\s*'  # parameters
        r'(?:const\s+)?(?:override\s+)?(?:final\s+)?'  # optional qualifiers
        r'(?:\{|->\s*\w+\s*;?)',  # opening brace or single line arrow return
        re.MULTILINE
    ),
    # Constructor/destructor: ClassName::ClassName(params) or ~ClassName(params)
    re.compile(
        r'^\s*(?:[\w:]+::)?([a-zA-Z_]\w*)\s*\([^)]*\)\s*(?:const\s+)?(?::\s*[^{]*)?\{',
        re.MULTILINE
    ),
    # Lambda capture: [&](params) { - but we'll skip lambdas as they're inline
]

# Single line comment pattern
SINGLE_LINE_COMMENT = re.compile(r'//.*?$')

# Multi-line comment pattern
MULTI_LINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)

# Preprocessor directives
PREPROCESSOR = re.compile(r'^\s*#.*?$')


def count_effective_lines(content: str) -> int:
    """Count non-blank, non-comment lines."""
    lines = content.split('\n')
    count = 0

    for line in lines:
        # Remove single line comments
        line = SINGLE_LINE_COMMENT.sub('', line)
        # Check if line has non-whitespace content
        if line.strip():
            count += 1

    # Now remove multi-line comments and count remaining
    content_without_multi = MULTI_LINE_COMMENT.sub('', content)
    lines_without_multi = content_without_multi.split('\n')

    # More accurate count - exclude preprocessor directives
    count = 0
    for line in lines_without_multi:
        # Remove single line comments first
        line = SINGLE_LINE_COMMENT.sub('', line)
        stripped = line.strip()
        # Exclude blank lines, preprocessor directives
        if stripped and not stripped.startswith('#'):
            count += 1

    return count


def find_functions(content: str) -> List[Dict]:
    """
    Find function definitions and their line ranges.
    Returns list of dicts with name, start_line, end_line, and the function body.
    """
    functions = []
    lines = content.split('\n')

    # Stack to track brace levels
    brace_stack = []
    current_function = None
    function_start_line = 0
    template_depth = 0

    # Pattern to match function signature lines
    # This matches lines that look like function definitions
    func_signature_pattern = re.compile(
        r'^\s*'  # leading whitespace
        r'(?:template\s*<[^>]*>\s*)?'  # optional template
        r'(?:[\w\s\*&:<>]+?)'  # return type (lazy)
        r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*'  # function name
        r'(?:\s*::\s*[a-zA-Z_][a-zA-Z0-9_]*)?'  # optional :: qualifier
        r'\s*\([^)]*\)\s*'  # parameters
        r'(?:const\s+)?(?:volatile\s+)?(?:override\s+)?(?:final\s+)?(?:noexcept\s*\(.*?\))?'  # qualifiers
        r'(?:\s*=\s*0)?'  # pure virtual
        r'(?:\s*->\s*[^{;]+)?'  # trailing return
        r'\s*(:\s*[^{;]+)?'  # constructor initializer list
        r'\s*\{'  # opening brace
    )

    # Pattern for constructor/destructor
    ctor_dtor_pattern = re.compile(
        r'^\s*(?:(?:[\w:]+::)?(?:~?[A-Z][a-zA-Z0-9_]*|[a-z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?::\s*[^{]+)?\{)',
        re.MULTILINE
    )

    i = 0
    while i < len(lines):
        line = lines[i]

        # Track template depth
        if '<' in line and '>' in line:
            template_count = line.count('<') - line.count('>')
            template_depth += template_count

        # Check for function signature
        match = func_signature_pattern.match(line)

        if match and not current_function:
            func_name = match.group(1)

            # Filter out common non-function keywords
            skip_keywords = {
                'if', 'for', 'while', 'switch', 'catch', 'struct', 'class',
                'namespace', 'enum', 'union', 'typedef', 'using', 'extern',
                'return', 'break', 'continue', 'goto', 'do', 'else', 'case',
                'default', 'try', 'throw', 'sizeof', 'decltype', 'typeid',
                'static_assert', 'alignas', 'alignof', 'typeof', 'reinterpret_cast'
            }

            if func_name not in skip_keywords:
                # Count braces to find function end
                brace_count = line.count('{') - line.count('}')
                brace_stack = [brace_count] if brace_count > 0 else []

                if brace_count > 0:
                    current_function = {
                        'name': func_name,
                        'line_start': i + 1,  # 1-indexed
                        'content': []
                    }
                    function_start_line = i
                else:
                    # Opening brace might be on next line
                    if i + 1 < len(lines) and '{' in lines[i + 1]:
                        brace_stack = [lines[i + 1].count('{') - lines[i + 1].count('}')]

                        if brace_stack[0] > 0:
                            current_function = {
                                'name': func_name,
                                'line_start': i + 1,
                                'content': []
                            }
                            function_start_line = i

        elif current_function:
            # Track brace level within function
            open_braces = line.count('{')
            close_braces = line.count('}')
            brace_stack[-1] += open_braces - close_braces

            current_function['content'].append(line)

            # Check if function ended
            if brace_stack[-1] <= 0:
                current_function['line_end'] = i + 1
                functions.append(current_function)
                current_function = None
                brace_stack = []

        i += 1

    return functions


def count_effective_lines_in_text(text: str) -> int:
    """Count non-blank, non-comment, non-preprocessor lines in a text block."""
    lines = text.split('\n')
    count = 0

    in_block_comment = False

    for line in lines:
        # Handle block comment state
        if '/*' in line and '*/' not in line and not in_block_comment:
            in_block_comment = True
            # Remove content before /* and check remaining
            line = line.split('/*')[0]

        if '*/' in line and in_block_comment:
            in_block_comment = False
            # Remove content after */
            parts = line.split('*/')
            if len(parts) > 1:
                line = parts[1]
            else:
                line = ''

        if in_block_comment:
            continue

        # Remove single line comments
        line = SINGLE_LINE_COMMENT.sub('', line)

        stripped = line.strip()

        # Skip blank lines and preprocessor directives
        if stripped and not stripped.startswith('#'):
            count += 1

    return count


def analyze_file(file_path: Path, file_threshold: int, func_threshold: int) -> Dict:
    """Analyze a single C/C++ file."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None

    total_effective_lines = count_effective_lines_in_text(content)
    functions = find_functions(content)

    large_functions = []

    for func in functions:
        func_content = '\n'.join(func['content'])
        func_lines = count_effective_lines_in_text(func_content)

        if func_lines >= func_threshold:
            large_functions.append(LargeFunction(
                name=func['name'],
                line_start=func['line_start'],
                line_end=func['line_end'],
                lines_count=func_lines,
                file_path=str(file_path)
            ))

    is_large_file = total_effective_lines >= file_threshold

    return {
        'path': str(file_path),
        'total_lines': total_effective_lines,
        'is_large_file': is_large_file,
        'large_functions': large_functions
    }


def scan_directory(path: Path, file_threshold: int, func_threshold: int) -> Dict:
    """Scan directory recursively for C/C++ files."""
    results = {
        'large_files': [],
        'all_large_functions': [],
        'total_files_scanned': 0
    }

    for root, dirs, files in os.walk(path):
        # Skip common build/output directories
        dirs[:] = [d for d in dirs if d not in {
            'build', 'out', 'node_modules', '.git', 'third_party',
            'vendor', 'external', '__pycache__', 'cmake-build'
        }]

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in CPP_EXTENSIONS:
                file_path = Path(root) / filename
                results['total_files_scanned'] += 1

                result = analyze_file(file_path, file_threshold, func_threshold)

                if result:
                    if result['is_large_file']:
                        results['large_files'].append(LargeFile(
                            path=result['path'],
                            lines_count=result['total_lines'],
                            large_functions=result['large_functions']
                        ))
                    elif result['large_functions']:
                        # Add to large functions even if file itself isn't large
                        for func in result['large_functions']:
                            results['all_large_functions'].append(func)

                    results['all_large_functions'].extend(result['large_functions'])

    return results


def generate_markdown_report(results: Dict, file_threshold: int, func_threshold: int) -> str:
    """Generate a markdown report from scan results."""
    lines = [
        "# C/C++ Code Size Report",
        "",
        f"**Scan Thresholds:**",
        f"- Large Files: {file_threshold}+ effective lines",
        f"- Large Functions: {func_threshold}+ effective lines",
        "",
        f"**Summary:**",
        f"- Total Files Scanned: {results['total_files_scanned']}",
        f"- Large Files Found: {len(results['large_files'])}",
        f"- Large Functions Found: {len(results['all_large_functions'])}",
        "",
    ]

    if results['large_files']:
        lines.extend([
            "---",
            "",
            "## Large Files",
            "",
            f"The following {len(results['large_files'])} files exceed **{file_threshold} effective lines**:",
            "",
        ])

        # Sort by line count descending
        sorted_files = sorted(results['large_files'], key=lambda x: x.lines_count, reverse=True)

        for i, file_info in enumerate(sorted_files, 1):
            rel_path = file_info.path
            lines.extend([
                f"### {i}. `{rel_path}`",
                "",
                f"- **Effective Lines:** {file_info.lines_count}",
            ])

            if file_info.large_functions:
                lines.extend([
                    f"- **Large Functions in this file:** {len(file_info.large_functions)}",
                    ""
                ])

                for func in sorted(file_info.large_functions, key=lambda x: x.lines_count, reverse=True):
                    lines.append(f"  - `{func.name}` - {func.lines_count} lines (lines {func.line_start}-{func.line_end})")
            else:
                lines.append("")

            lines.append("")

    if results['all_large_functions']:
        # Filter out functions that are already in large files to avoid duplicates
        standalone_functions = [
            f for f in results['all_large_functions']
            if not any(f.file_path == lf.path for lf in results['large_files'])
        ]

        all_funcs = results['all_large_functions']
        lines.extend([
            "---",
            "",
            "## Large Functions",
            "",
            f"The following {len(all_funcs)} functions exceed **{func_threshold} effective lines**:",
            "",
        ])

        # Sort by line count descending
        sorted_funcs = sorted(all_funcs, key=lambda x: x.lines_count, reverse=True)

        for i, func in enumerate(sorted_funcs, 1):
            lines.extend([
                f"### {i}. `{func.name}`",
                "",
                f"- **File:** `{func.file_path}`",
                f"- **Effective Lines:** {func.lines_count}",
                f"- **Location:** Lines {func.line_start}-{func.line_end}",
                "",
            ])

    if not results['large_files'] and not results['all_large_functions']:
        lines.extend([
            "---",
            "",
            "## Results",
            "",
            "No large files or functions found. All files are within the specified thresholds.",
        ])

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Scan C/C++ source files for extra large files and functions.'
    )
    parser.add_argument(
        'path',
        type=str,
        help='Path to scan (file or directory)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '-f', '--file-threshold',
        type=int,
        default=2000,
        help='Threshold for large files in effective lines (default: 2000)'
    )
    parser.add_argument(
        '-F', '--function-threshold',
        type=int,
        default=50,
        help='Threshold for large functions in effective lines (default: 50)'
    )

    args = parser.parse_args()

    scan_path = Path(args.path)

    if not scan_path.exists():
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    results = scan_directory(scan_path, args.file_threshold, args.function_threshold)

    report = generate_markdown_report(results, args.file_threshold, args.function_threshold)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)

    return 0


if __name__ == '__main__':
    exit(main())
