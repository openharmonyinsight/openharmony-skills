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
import argparse
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple


class IncludeAnalyzer:
    """Analyze C++ header file includes and dependencies."""

    # Known header→type mappings for quick lookup.
    # For headers NOT in this list, the scanner extracts class/struct/enum names
    # directly from the included header file.
    KNOWN_TYPES = {
        "frame_node.h": ["FrameNode"],
        "ui_node.h": ["UINode"],
        "element.h": ["Element"],
        "render_node.h": ["RenderNode"],
        "pattern.h": ["Pattern"],
        "layout_property.h": ["LayoutProperty"],
        "paint_property.h": ["PaintProperty"],
        "event_hub.h": ["EventHub"],
        "gesture_event_hub.h": ["GestureEventHub"],
        "render_context.h": ["RenderContext"],
        "touch_event.h": ["TouchEvent", "TouchEventTarget"],
        "drag_event.h": ["DragEvent"],
        "gesture_info.h": ["GestureInfo", "GestureType"],
        "pipeline_base.h": ["PipelineBase"],
        "pipeline_context.h": ["PipelineContext"],
        "gesture_recognizer.h": ["GestureRecognizer"],
        "input_event.h": ["InputEvent"],
        "drag_drop_proxy.h": ["DragDropProxy"],
    }

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

    def _resolve_type_names(self, include_path: str) -> List[str]:
        """Get type names exported by an include.

        Priority:
        1. KNOWN_TYPES dict (reliable, curated)
        2. Scan the actual header file for class/struct/enum class declarations
        3. Fall back to PascalCase of filename
        """
        basename = Path(include_path).name

        # 1. Known mapping
        for header, types in self.KNOWN_TYPES.items():
            if header == basename:
                return types

        # 2. Scan the actual header file
        # Try to resolve relative to the analyzed header's directory tree
        search_roots = [self.header_path.parent]
        for _ in range(8):
            search_roots.append(search_roots[-1].parent)

        for root in search_roots:
            candidate = root / include_path
            if candidate.exists():
                try:
                    content = candidate.read_text()
                    types = re.findall(
                        r'(?:class|struct|enum\s+class)\s+(\w+)', content
                    )
                    # Filter obvious internal names (Impl_, Test, etc.)
                    types = [t for t in types if not t.endswith('_') and not t.startswith('_')]
                    if types:
                        return types[:5]  # cap at 5 to avoid noise
                except Exception:
                    pass
                break

        # 3. Fallback: PascalCase from filename
        name = Path(include_path).stem
        # Remove common suffixes
        for suffix in ('_ng', '_ohos', '_builder', '_manager', '_helper'):
            name = name.removesuffix(suffix)
        pascal = re.sub(r'(^|_)([a-z])', lambda m: m.group(2).upper(), name)
        return [pascal]

    def identify_forward_decl_candidates(self) -> List[Dict]:
        """Identify includes that could be replaced with forward declarations.

        Returns a three-state safety classification per candidate:
          - 'candidate': likely safe (type used only as pointer/ref/RefPtr/unique_ptr)
          - 'needs_check': heuristic is inconclusive — manual review required
          - 'unsafe': definitely cannot forward declare (base class, value member, etc.)
        """
        candidates = []
        body = re.sub(r'^\s*#include.*$', '', self.content, flags=re.MULTILINE)

        for include in self.includes:
            include_path = include['path']
            type_names = self._resolve_type_names(include_path)

            # Check if any type from this include is used
            any_used = False
            for type_name in type_names:
                if self.find_type_usage(type_name) > 0:
                    any_used = True
                    break

            if not any_used:
                # Include not used at all — flag for potential removal
                candidates.append({
                    'include_path': include_path,
                    'type_name': ', '.join(type_names[:3]),
                    'usage_count': 0,
                    'safety': 'unused',
                    'flags': {},
                    'recommendation': "Possibly unused — no exported types found in file",
                })
                continue

            # Analyze each used type for forward-declaration safety
            for type_name in type_names:
                usage_count = self.find_type_usage(type_name)
                if usage_count == 0:
                    continue

                esc = re.escape(type_name)

                # --- checks that make it UNSAFE ---
                is_base_class = bool(re.search(
                    rf':\s*public\s+(?:{esc}|::\w*\*?\s*{esc})', body
                ))

                # Value member: Type used as a non-pointer, non-reference member
                value_member_re = (
                    r'\b' + esc + r'\b(?!\s*\*)'
                    r'(?!\s*&)'
                    r'(?!\s*>)'
                    r'\s+\w+\s*(?:[{;=])'
                )
                has_value_member = bool(re.search(value_member_re, body))

                # sizeof / decltype / type_traits require complete type
                has_sizeof_decltype = bool(re.search(
                    rf'(?:sizeof|decltype|static_assert|is_base_of|is_convertible|is_constructible)\s*[(<].*{esc}',
                    body
                ))

                # Inline method body accessing members of the type (-> or . on type)
                has_inline_member_access = bool(re.search(
                    rf'\b{esc}\s*\w+\s*\([^)]*\)\s*(?:const\s*)?\{{[^}}]*->',
                    body, re.DOTALL
                ))

                # --- checks that make it a CANDIDATE ---
                ptr_ref_only = True
                remaining = body
                remaining = re.sub(rf'(?:RefPtr|unique_ptr|shared_ptr)\s*<\s*{esc}\s*>', '', remaining)
                remaining = re.sub(rf'\b{esc}\s*[*&]', '', remaining)
                remaining = re.sub(rf'class\s+{esc}\s*;', '', remaining)
                remaining = re.sub(r'//.*$', '', remaining, flags=re.MULTILINE)
                remaining = re.sub(r'/\*.*?\*/', '', remaining, flags=re.DOTALL)
                if re.search(rf'\b{esc}\b', remaining):
                    ptr_ref_only = False

                # --- classify ---
                if is_base_class or has_value_member or has_sizeof_decltype:
                    safety = 'unsafe'
                elif ptr_ref_only and not has_inline_member_access:
                    safety = 'candidate'
                else:
                    safety = 'needs_check'

                candidates.append({
                    'include_path': include_path,
                    'type_name': type_name,
                    'usage_count': usage_count,
                    'safety': safety,
                    'flags': {
                        'is_base_class': is_base_class,
                        'has_value_member': has_value_member,
                        'has_sizeof_decltype': has_sizeof_decltype,
                        'has_inline_member_access': has_inline_member_access,
                        'ptr_ref_only': ptr_ref_only,
                    },
                    'recommendation': self._get_recommendation(safety),
                })

        self.forward_decl_candidates = candidates
        return candidates

    def _get_recommendation(self, safety: str) -> str:
        """Generate recommendation based on safety classification."""
        if safety == 'unused':
            return "Possibly unused — verify and remove"
        elif safety == 'candidate':
            return "Can likely replace with forward declaration"
        elif safety == 'needs_check':
            return "Needs manual review — heuristic inconclusive"
        else:
            return "Keep full include (unsafe to forward declare)"

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
        fwd_count = sum(1 for c in self.forward_decl_candidates if c['safety'] == 'candidate')
        unused_count = sum(1 for c in self.forward_decl_candidates if c['safety'] == 'unused')
        if fwd_count > 0:
            recommendations.append(
                f"Found {fwd_count} potential forward declaration candidates"
            )
        if unused_count > 0:
            recommendations.append(
                f"Found {unused_count} possibly unused includes"
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
                safety = candidate['safety']
                if safety == 'unused':
                    status = "[unused]"
                elif safety == 'candidate':
                    status = "[candidate]"
                elif safety == 'needs_check':
                    status = "[? review]"
                else:
                    status = "[unsafe]"
                lines.append(f"  {status} {candidate['include_path']}")
                lines.append(f"      Type: {candidate['type_name']}")
                lines.append(f"      Used {candidate['usage_count']} time(s)")
                lines.append(f"      -> {candidate['recommendation']}")
                if safety != 'candidate':
                    flags = candidate.get('flags', {})
                    reasons = []
                    if flags.get('is_base_class'):
                        reasons.append('base class')
                    if flags.get('has_value_member'):
                        reasons.append('value member')
                    if flags.get('has_sizeof_decltype'):
                        reasons.append('sizeof/decltype')
                    if flags.get('has_inline_member_access'):
                        reasons.append('inline member access')
                    if not flags.get('ptr_ref_only') and not reasons:
                        reasons.append('used beyond ptr/ref context')
                    if reasons:
                        lines.append(f"      Flags: {', '.join(reasons)}")
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
    parser = argparse.ArgumentParser(
        description='Extract and analyze include statistics from C++ header files.'
    )
    parser.add_argument('header_file', type=str, help='Path to header file')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                        help='Output format (default: text)')
    args = parser.parse_args()

    try:
        analyzer = IncludeAnalyzer(args.header_file)
        analysis = analyzer.analyze()

        if args.format == "json":
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
