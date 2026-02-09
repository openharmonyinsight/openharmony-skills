#!/usr/bin/env python3
"""
Comprehensive Code Review Analysis Script

Analyzes C++ and TypeScript/ArkTS code for ACE Engine compliance and quality issues.
Supports multiple dimensions: stability, performance, security, memory, and more.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Dimension(Enum):
    STABILITY = "Stability"
    PERFORMANCE = "Performance"
    THREADING = "Threading"
    SECURITY = "Security"
    MEMORY = "Memory"
    MODERN_CPP = "Modern C++"
    CODE_SMELL = "Code Smell"
    SOLID = "SOLID"
    ARCHITECTURE = "Architecture"


@dataclass
class Issue:
    """Represents a code review issue."""
    file_path: str
    line_number: int
    dimension: Dimension
    severity: Severity
    title: str
    description: str
    suggestion: str
    code_snippet: Optional[str] = None


@dataclass
class AnalysisResult:
    """Contains analysis results for a file."""
    file_path: str
    language: str
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    def get_issues_by_severity(self, severity: Severity) -> List[Issue]:
        return [i for i in self.issues if i.severity == severity]

    def get_issues_by_dimension(self, dimension: Dimension) -> List[Issue]:
        return [i for i in self.issues if i.dimension == dimension]


class CppAnalyzer:
    """Analyzes C++ code for ACE Engine compliance."""

    def __init__(self):
        self.patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for code analysis."""
        return {
            # Memory Issues
            'raw_pointer_new': re.compile(r'\bnew\s+\w+'),
            'raw_pointer_delete': re.compile(r'\bdelete\s+'),
            'static_cast': re.compile(r'\bstatic_cast\s*<'),
            'dynamic_cast_check': re.compile(r'\bstatic_cast.*\*.*='),

            # Security Issues
            'system_call': re.compile(r'\bsystem\s*\('),
            'strcpy': re.compile(r'\bstrcpy\s*\('),
            'sprintf': re.compile(r'\bsprintf\s*\('),
            'fopen_no_check': re.compile(r'\bfopen\s*\([^)]+\)\s*;'),

            # Stability Issues
            'unchecked_return': re.compile(r'=\s*\w+\s*\([^)]+\)\s*;'),
            'no_null_check': re.compile(r'(\w+)\s*->\s*\w+'),  # Pointer use without null check

            # ACE Engine Specific
            'refptr_make': re.compile(r'AceType::MakeRefPtr'),
            'refptr_cast': re.compile(r'AceType::DynamicCast'),
            'weak_claim': re.compile(r'WeakClaim'),
            'weak_upgrade': re.compile(r'Upgrade\s*\(\)'),

            # Threading
            'post_task': re.compile(r'PostTask\s*\('),
            'this_capture': re.compile(r'\[this\]'),

            # Code Smells
            'long_function': None,  # Will detect by line count
            'large_class': None,    # Will detect by line count

            # Naming Conventions
            'class_name': re.compile(r'^class\s+([a-z][a-zA-Z0-9_]*)'),
            'private_member': re.compile(r'private:\s*\n\s*(\w+)\s+(\w+)(?<!_)'),
        }

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a C++ file."""
        result = AnalysisResult(file_path, "C++")

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            result.add_issue(Issue(
                file_path=file_path,
                line_number=0,
                dimension=Dimension.STABILITY,
                severity=Severity.HIGH,
                title="Failed to read file",
                description=str(e),
                suggestion="Ensure file is accessible and valid UTF-8"
            ))
            return result

        # Check each line
        for line_num, line in enumerate(lines, start=1):
            self._analyze_line(line, line_num, lines, result)

        # Check for structural issues
        self._analyze_structure(lines, file_path, result)

        return result

    def _analyze_line(self, line: str, line_num: int,
                      all_lines: List[str], result: AnalysisResult):
        """Analyze a single line of code."""
        # Memory: Check for raw new/delete
        if self.patterns['raw_pointer_new'].search(line) and \
           'RefPtr' not in line and 'MakeRefPtr' not in line:
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.MEMORY,
                severity=Severity.HIGH,
                title="Raw pointer allocation detected",
                description="Using 'new' instead of RefPtr/MakeRefPtr",
                suggestion="Use AceType::MakeRefPtr<T>() instead of new T()",
                code_snippet=line.strip()
            ))

        # Security: Dangerous functions
        if self.patterns['system_call'].search(line):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.SECURITY,
                severity=Severity.CRITICAL,
                title="Potential command injection",
                description="Using system() with user input can lead to command injection",
                suggestion="Use safe alternatives or whitelist validate input",
                code_snippet=line.strip()
            ))

        if self.patterns['strcpy'].search(line):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.SECURITY,
                severity=Severity.HIGH,
                title="Unsafe string function",
                description="strcpy() is vulnerable to buffer overflows",
                suggestion="Use strlcpy() or std::string instead",
                code_snippet=line.strip()
            ))

        # Stability: Check for fopen without null check
        if self.patterns['fopen_no_check'].search(line):
            # Check if next few lines have null check
            has_check = False
            for i in range(line_num, min(line_num + 3, len(all_lines))):
                if 'if' in all_lines[i] and ('fp' in line or all_lines[i]):
                    has_check = True
                    break

            if not has_check:
                result.add_issue(Issue(
                    file_path=result.file_path,
                    line_number=line_num,
                    dimension=Dimension.STABILITY,
                    severity=Severity.HIGH,
                    title="Unchecked file open",
                    description="fopen() result is not checked for null",
                    suggestion="Always check return value: if (!fp) { /* handle error */ }",
                    code_snippet=line.strip()
                ))

        # Threading: Unsafe this capture
        if self.patterns['this_capture'].search(line) and \
           self.patterns['post_task'].search(''.join(all_lines[max(0, line_num-5):line_num])):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.THREADING,
                severity=Severity.HIGH,
                title="Unsafe 'this' capture in async callback",
                description="Capturing raw 'this' can lead to use-after-free",
                suggestion="Use WeakClaim: auto weak = AceType::WeakClaim(this); [weak]() { ... }",
                code_snippet=line.strip()
            ))

        # ACE Engine: Check for static_cast without DynamicCast
        if self.patterns['static_cast'].search(line):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.MEMORY,
                severity=Severity.MEDIUM,
                title="Using static_cast instead of DynamicCast",
                description="static_cast is not type-safe in ACE Engine",
                suggestion="Use AceType::DynamicCast<T>() with null check",
                code_snippet=line.strip()
            ))

        # Naming: Class names should be PascalCase
        class_match = self.patterns['class_name'].search(line)
        if class_match:
            class_name = class_match.group(1)
            if not class_name[0].isupper():
                result.add_issue(Issue(
                    file_path=result.file_path,
                    line_number=line_num,
                    dimension=Dimension.CODE_SMELL,
                    severity=Severity.LOW,
                    title="Class name not PascalCase",
                    description=f"Class '{class_name}' should start with uppercase",
                    suggestion="Rename class to follow PascalCase convention",
                    code_snippet=line.strip()
                ))

    def _analyze_structure(self, lines: List[str],
                          file_path: str, result: AnalysisResult):
        """Analyze file structure for code smells."""
        # Count lines in functions/classes
        current_function = None
        function_lines = 0
        brace_count = 0
        in_function = False

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Detect function start
            if re.search(r'^\w+\s+\w+\s*\([^)]*\)\s*{?', stripped):
                in_function = True
                function_lines = 0
                brace_count = 1 if '{' in stripped else 0

            # Count braces and lines
            if in_function:
                function_lines += 1
                brace_count += line.count('{')
                brace_count -= line.count('}')

                # Function ends when brace_count returns to 0
                if brace_count == 0 and function_lines > 1:
                    if function_lines > 50:
                        result.add_issue(Issue(
                            file_path=file_path,
                            line_number=line_num - function_lines,
                            dimension=Dimension.CODE_SMELL,
                            severity=Severity.MEDIUM,
                            title="Long function detected",
                            description=f"Function is {function_lines} lines (recommended: <50)",
                            suggestion="Extract smaller functions to improve readability"
                        ))
                    in_function = False


class TypeScriptAnalyzer:
    """Analyzes TypeScript/ArkTS code."""

    def __init__(self):
        self.patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        return {
            'any_type': re.compile(r':\s*any\b'),
            'any_array': re.compile(r'Array<any>|any\[\]'),
            'console_log': re.compile(r'console\.log'),
            'ignore_error': re.compile(r'catch\s*\([^)]*\)\s*{?\s*}?'),
            'missing_type': re.compile(r'function\s+\w+\s*\([^)]*\)\s*{'),
        }

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a TypeScript file."""
        result = AnalysisResult(file_path, "TypeScript")

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            result.add_issue(Issue(
                file_path=file_path,
                line_number=0,
                dimension=Dimension.STABILITY,
                severity=Severity.HIGH,
                title="Failed to read file",
                description=str(e),
                suggestion="Ensure file is accessible"
            ))
            return result

        for line_num, line in enumerate(lines, start=1):
            self._analyze_line(line, line_num, result)

        return result

    def _analyze_line(self, line: str, line_num: int, result: AnalysisResult):
        """Analyze a single line of TypeScript code."""

        # Type safety: 'any' type
        if self.patterns['any_type'].search(line):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.STABILITY,
                severity=Severity.MEDIUM,
                title="Using 'any' type",
                description="Using 'any' loses type safety",
                suggestion="Use specific types or 'unknown' with type guards",
                code_snippet=line.strip()
            ))

        # Observability: console.log in production
        if self.patterns['console_log'].search(line):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.OBSERVABILITY if hasattr(Dimension, 'OBSERVABILITY') else Dimension.STABILITY,
                severity=Severity.LOW,
                title="Console.log statement",
                description="Consider using proper logging framework",
                suggestion="Use HiLog or framework logging instead of console.log",
                code_snippet=line.strip()
            ))

        # Stability: Empty catch blocks
        if self.patterns['ignore_error'].search(line):
            result.add_issue(Issue(
                file_path=result.file_path,
                line_number=line_num,
                dimension=Dimension.STABILITY,
                severity=Severity.MEDIUM,
                title="Ignoring errors",
                description="Empty catch block ignores all errors",
                suggestion="Log errors or handle them appropriately",
                code_snippet=line.strip()
            ))


def analyze_file(file_path: str) -> AnalysisResult:
    """Dispatch file to appropriate analyzer."""
    file_ext = Path(file_path).suffix.lower()

    if file_ext in ['.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx']:
        analyzer = CppAnalyzer()
        return analyzer.analyze_file(file_path)
    elif file_ext in ['.ts', '.tsx', '.ets']:
        analyzer = TypeScriptAnalyzer()
        return analyzer.analyze_file(file_path)
    else:
        result = AnalysisResult(file_path, "Unknown")
        result.add_issue(Issue(
            file_path=file_path,
            line_number=0,
            dimension=Dimension.STABILITY,
            severity=Severity.LOW,
            title="Unsupported file type",
            description=f"File extension '{file_ext}' is not supported",
            suggestion="Supported: .cpp, .h, .ts, .tsx, .ets"
        ))
        return result


def analyze_directory(directory: str, recursive: bool = True) -> List[AnalysisResult]:
    """Analyze all code files in a directory."""
    results = []
    path = Path(directory)

    if recursive:
        files = [
            str(f) for f in path.rglob('*')
            if f.suffix.lower() in ['.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.ts', '.tsx', '.ets']
        ]
    else:
        files = [
            str(f) for f in path.glob('*')
            if f.suffix.lower() in ['.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.ts', '.tsx', '.ets']
        ]

    for file_path in files:
        try:
            result = analyze_file(file_path)
            results.append(result)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive Code Review Analysis for ACE Engine"
    )
    parser.add_argument(
        'path',
        help="File or directory to analyze"
    )
    parser.add_argument(
        '--output', '-o',
        help="Output JSON file path"
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help="Recursively analyze directories"
    )
    parser.add_argument(
        '--severity',
        choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
        help="Minimum severity level to report"
    )
    parser.add_argument(
        '--dimension',
        help="Filter by dimension (e.g., Memory, Security)"
    )

    args = parser.parse_args()

    # Analyze
    path = Path(args.path)

    if path.is_file():
        results = [analyze_file(str(path))]
    elif path.is_dir():
        results = analyze_directory(str(path), args.recursive)
    else:
        print(f"Error: {args.path} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)

    # Convert to JSON-serializable format
    output_data = []
    for result in results:
        data = {
            'file_path': result.file_path,
            'language': result.language,
            'issues': [
                {
                    'line_number': issue.line_number,
                    'dimension': issue.dimension.value,
                    'severity': issue.severity.value,
                    'title': issue.title,
                    'description': issue.description,
                    'suggestion': issue.suggestion,
                    'code_snippet': issue.code_snippet
                }
                for issue in result.issues
            ]
        }
        output_data.append(data)

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        print(f"Analysis results saved to {args.output}")
    else:
        print(json.dumps(output_data, indent=2))

    # Print summary
    total_issues = sum(len(r.issues) for r in results)
    critical = sum(len(r.get_issues_by_severity(Severity.CRITICAL)) for r in results)
    high = sum(len(r.get_issues_by_severity(Severity.HIGH)) for r in results)
    medium = sum(len(r.get_issues_by_severity(Severity.MEDIUM)) for r in results)
    low = sum(len(r.get_issues_by_severity(Severity.LOW)) for r in results)

    print(f"\nSummary:", file=sys.stderr)
    print(f"  Files analyzed: {len(results)}", file=sys.stderr)
    print(f"  Total issues: {total_issues}", file=sys.stderr)
    print(f"    CRITICAL: {critical}", file=sys.stderr)
    print(f"    HIGH: {high}", file=sys.stderr)
    print(f"    MEDIUM: {medium}", file=sys.stderr)
    print(f"    LOW: {low}", file=sys.stderr)


if __name__ == '__main__':
    main()
