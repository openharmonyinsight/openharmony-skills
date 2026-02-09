#!/usr/bin/env python3
"""
Generate comprehensive code review reports from analysis results.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class ReportGenerator:
    """Generate markdown code review reports."""

    def __init__(self, analysis_results: List[Dict[str, Any]]):
        self.results = analysis_results
        self.stats = self._calculate_stats()

    def _calculate_stats(self) -> Dict[str, int]:
        """Calculate issue statistics."""
        stats = {
            'total_issues': 0,
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'files': len(self.results)
        }

        for result in self.results:
            for issue in result.get('issues', []):
                stats['total_issues'] += 1
                severity = issue.get('severity', 'LOW')
                stats[severity.lower()] = stats.get(severity.lower(), 0) + 1

        return stats

    def generate_report(self, template_path: str = None) -> str:
        """Generate markdown report."""
        if template_path and Path(template_path).exists():
            return self._generate_from_template(template_path)
        else:
            return self._generate_default_report()

    def _generate_default_report(self) -> str:
        """Generate default markdown report."""
        lines = []
        lines.append("# Code Review Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(f"- **Files Analyzed:** {self.stats['files']}")
        lines.append(f"- **Total Issues:** {self.stats['total_issues']}")
        lines.append("")
        lines.append("### Issue Breakdown by Severity")
        lines.append("")
        lines.append("| Severity | Count |")
        lines.append("|----------|-------|")
        lines.append(f"| 🔴 CRITICAL | {self.stats['critical']} |")
        lines.append(f"| 🟠 HIGH | {self.stats['high']} |")
        lines.append(f"| 🟡 MEDIUM | {self.stats['medium']} |")
        lines.append(f"| 🟢 LOW | {self.stats['low']} |")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Critical Issues
        if self.stats['critical'] > 0:
            lines.append("## 🔴 CRITICAL Issues")
            lines.append("")
            lines.append("*Must fix before merge*")
            lines.append("")
            self._add_issues_by_severity(lines, 'CRITICAL')
            lines.append("")

        # High Issues
        if self.stats['high'] > 0:
            lines.append("## 🟠 HIGH Priority Issues")
            lines.append("")
            lines.append("*Should fix before merge*")
            lines.append("")
            self._add_issues_by_severity(lines, 'HIGH')
            lines.append("")

        # Medium Issues
        if self.stats['medium'] > 0:
            lines.append("## 🟡 MEDIUM Priority Issues")
            lines.append("")
            lines.append("*Fix soon*")
            lines.append("")
            self._add_issues_by_severity(lines, 'MEDIUM')
            lines.append("")

        # Low Issues
        if self.stats['low'] > 0:
            lines.append("## 🟢 LOW Priority Issues")
            lines.append("")
            lines.append("*Nice to have*")
            lines.append("")
            self._add_issues_by_severity(lines, 'LOW')
            lines.append("")

        # Dimension Breakdown
        lines.append("## Issues by Dimension")
        lines.append("")
        self._add_dimension_breakdown(lines)
        lines.append("")

        # File Details
        lines.append("## File-by-File Details")
        lines.append("")
        for result in self.results:
            issues = result.get('issues', [])
            if issues:
                lines.append(f"### {result['file_path']}")
                lines.append("")
                lines.append(f"**Language:** {result.get('language', 'Unknown')}")
                lines.append("")
                for issue in issues:
                    lines.append(f"#### Line {issue['line_number']}: {issue['title']}")
                    lines.append("")
                    lines.append(f"**Dimension:** {issue['dimension']}")
                    lines.append(f"**Severity:** {issue['severity']}")
                    lines.append("")
                    lines.append(f"**Description:** {issue['description']}")
                    lines.append("")
                    lines.append(f"**Suggestion:** {issue['suggestion']}")
                    if issue.get('code_snippet'):
                        lines.append("")
                        lines.append("```cpp")
                        lines.append(issue['code_snippet'])
                        lines.append("```")
                    lines.append("")

        # Recommendations
        lines.append("## Recommendations")
        lines.append("")
        self._add_recommendations(lines)
        lines.append("")

        # Checklist
        lines.append("## Review Checklist")
        lines.append("")
        self._add_checklist(lines)
        lines.append("")

        return "\n".join(lines)

    def _add_issues_by_severity(self, lines: List[str], severity: str):
        """Add issues filtered by severity."""
        count = 0
        for result in self.results:
            for issue in result.get('issues', []):
                if issue.get('severity') == severity:
                    count += 1
                    lines.append(f"### {count}. {issue['title']}")
                    lines.append("")
                    lines.append(f"**File:** `{result['file_path']}`")
                    lines.append(f"**Line:** {issue['line_number']}")
                    lines.append(f"**Dimension:** {issue['dimension']}")
                    lines.append("")
                    lines.append(f"{issue['description']}")
                    lines.append("")
                    lines.append(f"**Suggestion:** {issue['suggestion']}")
                    if issue.get('code_snippet'):
                        lines.append("")
                        lines.append("```")
                        lines.append(issue['code_snippet'])
                        lines.append("```")
                    lines.append("")

    def _add_dimension_breakdown(self, lines: List[str]):
        """Add issues grouped by dimension."""
        dimension_counts = {}
        dimension_issues = {}

        for result in self.results:
            for issue in result.get('issues', []):
                dimension = issue.get('dimension', 'Unknown')
                dimension_counts[dimension] = dimension_counts.get(dimension, 0) + 1

                if dimension not in dimension_issues:
                    dimension_issues[dimension] = []
                dimension_issues[dimension].append({
                    'file': result['file_path'],
                    'line': issue['line_number'],
                    'title': issue['title'],
                    'severity': issue['severity']
                })

        # Sort by count
        sorted_dimensions = sorted(dimension_counts.items(),
                                  key=lambda x: x[1],
                                  reverse=True)

        lines.append("| Dimension | Issues |")
        lines.append("|-----------|--------|")
        for dimension, count in sorted_dimensions:
            lines.append(f"| {dimension} | {count} |")

    def _add_recommendations(self, lines: List[str]):
        """Add prioritized recommendations."""
        lines.append("### Immediate Actions")
        lines.append("")
        lines.append("1. **Fix all CRITICAL issues** - These may cause crashes or security vulnerabilities")
        lines.append("2. **Address HIGH priority memory issues** - Prevent leaks and use-after-free")
        lines.append("3. **Review HIGH priority security issues** - Validate all inputs and sanitize outputs")
        lines.append("")
        lines.append("### Short-term Actions")
        lines.append("")
        lines.append("1. **Refactor large classes and methods** - Improve maintainability")
        lines.append("2. **Add error handling** - Improve stability")
        lines.append("3. **Remove duplicate code** - Reduce maintenance burden")
        lines.append("")
        lines.append("### Long-term Actions")
        lines.append("")
        lines.append("1. **Improve test coverage** - Add unit tests for critical paths")
        lines.append("2. **Update documentation** - Keep knowledge base current")
        lines.append("3. **Refactor code smells** - Incremental improvements")
        lines.append("")

    def _add_checklist(self, lines: List[str]):
        """Add review checklist."""
        lines.append("- [ ] All CRITICAL issues resolved")
        lines.append("- [ ] All HIGH priority issues reviewed")
        lines.append("- [ ] Memory leaks fixed")
        lines.append("- [ ] Security vulnerabilities addressed")
        lines.append("- [ ] Error handling added")
        lines.append("- [ ] Code follows ACE Engine architecture")
        lines.append("- [ ] RefPtr used correctly")
        lines.append("- [ ] Naming conventions followed")
        lines.append("- [ ] Unit tests added/updated")
        lines.append("- [ ] Documentation updated")
        lines.append("")


def main():
    parser = argparse.ArgumentParser(
        description="Generate code review report from analysis results"
    )
    parser.add_argument(
        '--analysis', '-a',
        required=True,
        help="Path to analysis JSON file"
    )
    parser.add_argument(
        '--output', '-o',
        default='code_review_report.md',
        help="Output report file path (default: code_review_report.md)"
    )
    parser.add_argument(
        '--template', '-t',
        help="Path to report template file"
    )

    args = parser.parse_args()

    # Load analysis results
    try:
        with open(args.analysis, 'r', encoding='utf-8') as f:
            analysis_results = json.load(f)
    except Exception as e:
        print(f"Error loading analysis file: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate report
    generator = ReportGenerator(analysis_results)
    report = generator.generate_report(args.template)

    # Write report
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Report generated: {args.output}")
    print(f"  Files: {generator.stats['files']}")
    print(f"  Total issues: {generator.stats['total_issues']}")
    print(f"    CRITICAL: {generator.stats['critical']}")
    print(f"    HIGH: {generator.stats['high']}")
    print(f"    MEDIUM: {generator.stats['medium']}")
    print(f"    LOW: {generator.stats['low']}")


if __name__ == '__main__':
    import sys
    main()
