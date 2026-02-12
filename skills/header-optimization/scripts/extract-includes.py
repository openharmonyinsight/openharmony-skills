#!/usr/bin/env python3
"""
extract-includes.py - Extract and analyze include statistics from C++ header files

Part of header-optimization skill for ace_engine.

Usage:
    python3 extract-includes.py <header_file> [--format json|text]

Features:
    - Extract all #include directives
    - Categorize includes by type (system, project, local)
    - Identify forward declaration candidates
    - Generate statistics and recommendations
"""

import sys
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple


class IncludeAnalyzer:
    """Analyze C++ header file includes and dependencies."""

    # Common ace_engine patterns that are good forward declaration candidates
    FORWARD_DECL_PATTERNS = {
        "frame_node.h": "FrameNode",
        "ui_node.h": "UINode",
        "element.h": "Element",
        "render_node.h": "RenderNode",
        "pattern.h": "Pattern",
        "layout_property.h": "LayoutProperty",
        "paint_property.h": "PaintProperty",
        "event_hub.h": "EventHub",
        "gesture_event_hub.h": "GestureEventHub",
    }

    # Base namespace patterns for ace_engine
    NAMESPACES = [
        "OHOS::Ace",
        "OHOS::Ace::NG",
    ]

    def __init__(self, header_path: str):
        self.header_path = Path(header_path)
        if not self.header_path.exists():
            raise FileNotFoundError(f"Header file not found: {header_path}")

        self.content = self.header_path.read_text()
        self.includes: List[Dict] = []
        self.stats: Dict = {}
        self.forward_decl_candidates: List[Dict] = []

    def extract_includes(self) -> List[Dict]:
        """Extract all #include directives from the header file."""
        include_pattern = r'^\s*#include\s+[<"]([^>"]+)[>"]'

        for match in re.finditer(include_pattern, self.content, re.MULTILINE):
            include_path = match.group(1)
            line_num = self.content[:match.start()].count('\n') + 1

            include_info = {
                'path': include_path,
                'line': line_num,
                'type': self._classify_include(include_path),
            }

            self.includes.append(include_info)

        return self.includes

    def _classify_include(self, include_path: str) -> str:
        """Classify include as system, project, or local."""
        if include_path.startswith('<'):
            return 'system'
        elif any(x in include_path for x in ['ace_engine', 'arkui', 'openharmony']):
            return 'project'
        else:
            return 'local'

    def find_type_usage(self, type_name: str) -> int:
        """Count how many times a type is used in the file."""
        # Exclude include lines
        content_excludes = re.sub(r'^\s*#include.*$', '', self.content, flags=re.MULTILINE)

        # Count occurrences (as whole word)
        pattern = r'\b' + re.escape(type_name) + r'\b'
        matches = re.findall(pattern, content_excludes)
        return len(matches)

    def identify_forward_decl_candidates(self) -> List[Dict]:
        """Identify includes that could be replaced with forward declarations."""
        candidates = []

        for include in self.includes:
            include_path = include['path']

            # Check against known patterns
            for header, type_name in self.FORWARD_DECL_PATTERNS.items():
                if header in include_path:
                    usage_count = self.find_type_usage(type_name)

                    if usage_count > 0:
                        # Check if it's used as base class (can't forward declare)
                        content_excludes = re.sub(r'^\s*#include.*$', '', self.content, flags=re.MULTILINE)
                        is_base_class = bool(re.search(
                            rf':\s*public\s+(?:{re.escape(type_name)}|::\w*\*?\s*{re.escape(type_name)})',
                            content_excludes
                        ))

                        # Check if used as member instance (not pointer/ref)
                        # This is heuristic - actual check requires more parsing
                        has_member_instance = False

                        candidates.append({
                            'include_path': include_path,
                            'type_name': type_name,
                            'usage_count': usage_count,
                            'is_base_class': is_base_class,
                            'can_forward_declare': not is_base_class and not has_member_instance,
                            'recommendation': self._get_recommendation(not is_base_class and not has_member_instance),
                        })

        self.forward_decl_candidates = candidates
        return candidates

    def _get_recommendation(self, can_forward_declare: bool) -> str:
        """Generate recommendation for forward declaration."""
        if can_forward_declare:
            return "Replace with forward declaration"
        else:
            return "Keep full include (base class or member instance)"

    def calculate_statistics(self) -> Dict:
        """Calculate overall statistics about the header file."""
        total_lines = len(self.content.splitlines())
        include_count = len(self.includes)

        # Count by type
        by_type = defaultdict(int)
        for include in self.includes:
            by_type[include['type']] += 1

        # Count inline methods (rough heuristic)
        inline_methods = len(re.findall(
            r'^\s*(?!template)(?:\w+\s+)+\w+\s*\([^)]*\)\s*(?:const\s*)?\{',
            self.content,
            re.MULTILINE
        ))

        self.stats = {
            'total_lines': total_lines,
            'include_count': include_count,
            'includes_by_type': dict(by_type),
            'inline_methods': inline_methods,
            'forward_decl_candidates': len(self.forward_decl_candidates),
        }

        return self.stats

    def generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []

        # High include count
        if self.stats['include_count'] > 7:
            recommendations.append(
                f"HIGH include count ({self.stats['include_count']}): "
                "Strong candidate for optimization"
            )
        elif self.stats['include_count'] > 3:
            recommendations.append(
                f"MEDIUM include count ({self.stats['include_count']}): "
                "Consider forward declarations"
            )

        # Forward declaration candidates
        fwd_count = sum(1 for c in self.forward_decl_candidates if c['can_forward_declare'])
        if fwd_count > 0:
            recommendations.append(
                f"Found {fwd_count} potential forward declaration candidates"
            )

        # Inline methods
        if self.stats['inline_methods'] > 5:
            recommendations.append(
                f"Many inline methods ({self.stats['inline_methods']}): "
                "Consider moving to .cpp file"
            )

        if not recommendations:
            recommendations.append("Header appears well-optimized")

        return recommendations

    def analyze(self) -> Dict:
        """Run complete analysis."""
        self.extract_includes()
        self.identify_forward_decl_candidates()
        self.calculate_statistics()

        return {
            'header': str(self.header_path),
            'stats': self.stats,
            'includes': self.includes,
            'forward_decl_candidates': self.forward_decl_candidates,
            'recommendations': self.generate_recommendations(),
        }

    def format_text(self, analysis: Dict) -> str:
        """Format analysis results as text."""
        lines = []
        lines.append("=" * 60)
        lines.append(f"Header File Analysis: {self.header_path.name}")
        lines.append("=" * 60)
        lines.append("")

        # Statistics
        stats = analysis['stats']
        lines.append("Statistics")
        lines.append("-" * 40)
        lines.append(f"  Total lines:          {stats['total_lines']}")
        lines.append(f"  Total includes:       {stats['include_count']}")
        lines.append(f"  Inline methods:       {stats['inline_methods']}")
        lines.append("")

        # Include breakdown
        lines.append("Includes by Type")
        lines.append("-" * 40)
        for inc_type, count in stats.get('includes_by_type', {}).items():
            lines.append(f"  {inc_type.capitalize():12s}: {count}")
        lines.append("")

        # Current includes
        lines.append("Current Includes")
        lines.append("-" * 40)
        for include in analysis['includes']:
            lines.append(f"  {include['path']}")
        lines.append("")

        # Forward declaration candidates
        if analysis['forward_decl_candidates']:
            lines.append("Forward Declaration Candidates")
            lines.append("-" * 40)
            for candidate in analysis['forward_decl_candidates']:
                status = "✓" if candidate['can_forward_declare'] else "✗"
                lines.append(f"  {status} {candidate['include_path']}")
                lines.append(f"      Type: {candidate['type_name']}")
                lines.append(f"      Used {candidate['usage_count']} time(s)")
                lines.append(f"      → {candidate['recommendation']}")
                lines.append("")

        # Recommendations
        lines.append("Recommendations")
        lines.append("-" * 40)
        for i, rec in enumerate(analysis['recommendations'], 1):
            lines.append(f"  {i}. {rec}")
        lines.append("")

        lines.append("=" * 60)
        lines.append("Use header-optimization skill to apply optimizations")
        lines.append("=" * 60)

        return "\n".join(lines)

    def format_json(self, analysis: Dict) -> str:
        """Format analysis results as JSON."""
        return json.dumps(analysis, indent=2)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 extract-includes.py <header_file> [--format json|text]", file=sys.stderr)
        sys.exit(1)

    header_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "text"

    try:
        analyzer = IncludeAnalyzer(header_file)
        analysis = analyzer.analyze()

        if output_format == "json":
            print(analyzer.format_json(analysis))
        else:
            print(analyzer.format_text(analysis))

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing header: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
