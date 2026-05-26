#!/usr/bin/env python3
"""
Architecture Analyzer - Analyze OHOS module code architecture

This script analyzes the code composition, platform dependencies, and
complexity of an OHOS module to recommend the best adaptation approach.
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter


class ArchitectureAnalyzer:
    def __init__(self, module_path: str):
        self.module_path = Path(module_path)
        if not self.module_path.exists():
            raise FileNotFoundError(f"Module path not found: {module_path}")

    def analyze(self) -> Dict:
        """Perform comprehensive architecture analysis"""
        # Find all C++ source files
        cpp_files = list(self.module_path.rglob("*.cpp"))
        h_files = list(self.module_path.rglob("*.h"))

        total_lines = 0
        napi_lines = 0
        business_logic_lines = 0
        platform_specific_lines = 0

        # Analyze each file
        for file in cpp_files + h_files:
            try:
                content = file.read_text(encoding='utf-8')
                lines = len(content.split('\n'))
                total_lines += lines

                # Categorize file
                if self._is_napi_file(file):
                    napi_lines += lines
                elif self._is_platform_file(file):
                    platform_specific_lines += lines
                else:
                    business_logic_lines += lines

            except Exception as e:
                print(f"Warning: Could not read {file}: {e}")

        # Find dependencies
        dependencies = self._find_dependencies(cpp_files)

        # Calculate platform independence ratio
        platform_independent = business_logic_lines
        platform_ratio = (platform_independent / total_lines * 100) if total_lines > 0 else 0

        # Recommend architecture mode
        recommendation = self._recommend_mode(platform_ratio, platform_specific_lines, total_lines)

        return {
            'total_lines': total_lines,
            'napi_lines': napi_lines,
            'business_logic_lines': business_logic_lines,
            'platform_specific_lines': platform_specific_lines,
            'platform_independence_percent': platform_ratio,
            'dependencies': dependencies,
            'recommendation': recommendation,
            'estimated_reuse': self._estimate_reuse(platform_ratio),
            'estimated_effort': self._estimate_effort(platform_ratio, platform_specific_lines),
        }

    def _is_napi_file(self, file_path: Path) -> bool:
        """Check if file is NAPI binding code"""
        name_lower = file_path.name.lower()
        path_lower = str(file_path).lower()
        return 'napi' in name_lower or 'js_' in path_lower

    def _is_platform_file(self, file_path: Path) -> bool:
        """Check if file is platform-specific"""
        path_lower = str(file_path).lower()
        return any(keyword in path_lower for keyword in [
            'adapter/', 'platform/', 'osal/', 'ohos/', 'android/', 'ios/'
        ])

    def _find_dependencies(self, files: List[Path]) -> Dict:
        """Find dependencies from #include statements"""
        internal_deps = Counter()
        external_deps = Counter()

        for file in files:
            try:
                content = file.read_text(encoding='utf-8')
                # Find #include statements
                includes = re.findall(r'#include\s*[<"]([^>"<]+)[>"]', content)

                for inc in includes:
                    if inc.startswith('module_|@ohos/'):
                        # Internal dependency
                        internal_deps[inc] += 1
                    elif not inc.startswith('base/|foundation/|core/'):
                        # External dependency
                        external_deps[inc] += 1
            except Exception:
                pass

        return {
            'internal': dict(internal_deps.most_common(20)),
            'external': dict(external_deps.most_common(10)),
        }

    def _recommend_mode(self, platform_ratio: float, platform_lines: int, total_lines: int) -> str:
        """Recommend architecture mode based on analysis"""
        if platform_ratio >= 90:
            return "OHOS Reuse Mode"
        elif platform_ratio <= 30 or (platform_lines / total_lines > 0.7 if total_lines > 0 else False):
            return "Independent Implementation Mode"
        else:
            return "Hybrid Mode"

    def _estimate_reuse(self, platform_ratio: float) -> str:
        """Estimate code reuse percentage"""
        if platform_ratio >= 90:
            return "90-95%"
        elif platform_ratio >= 60:
            return "60-80%"
        else:
            return "10-30%"

    def _estimate_effort(self, platform_ratio: float, platform_lines: int) -> Dict:
        """Estimate implementation effort"""
        if platform_ratio >= 90:
            return {
                'new_code_lines': '500-800',
                'time_weeks': '4-6',
                'complexity': 'Low'
            }
        elif platform_ratio >= 60:
            return {
                'new_code_lines': '1,500-2,500',
                'time_weeks': '6-10',
                'complexity': 'Medium'
            }
        else:
            return {
                'new_code_lines': '4,000-6,000',
                'time_weeks': '10-16',
                'complexity': 'High'
            }

    def print_report(self, analysis: Dict):
        """Print formatted architecture analysis report"""
        print(f"\n{'='*70}")
        print(f"📊 Architecture Analysis")
        print(f"{'='*70}")

        print(f"\n📊 Code Composition:")
        print(f"   - NAPI bindings: {analysis['napi_lines']:,} lines")
        print(f"   - Business logic (C++): {analysis['business_logic_lines']:,} lines")
        print(f"   - Platform-specific: {analysis['platform_specific_lines']:,} lines")
        print(f"   - Total: {analysis['total_lines']:,} lines")

        print(f"\n🎯 Platform Dependency:")
        print(f"   - Platform-independent: {analysis['platform_independence_percent']:.1f}%")
        print(f"   - Platform-specific: {100-analysis['platform_independence_percent']:.1f}%")

        if analysis['dependencies']['internal']:
            print(f"\n📦 Internal Dependencies:")
            for dep, count in list(analysis['dependencies']['internal'].items())[:10]:
                print(f"   - {dep}")

        if analysis['dependencies']['external']:
            print(f"\n📦 External Dependencies:")
            for dep, count in analysis['dependencies']['external'].items():
                print(f"   - {dep}")

        print(f"\n✅ Recommendation: {analysis['recommendation']}")

        print(f"\n📈 Estimated Effort:")
        effort = analysis['estimated_effort']
        print(f"   - New code: {effort['new_code_lines']} lines")
        print(f"   - Time: {effort['time_weeks']} weeks")
        print(f"   - Complexity: {effort['complexity']}")
        print(f"   - Code reuse: {analysis['estimated_reuse']}")

        print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze OHOS module architecture for cross-platform adaptation'
    )
    parser.add_argument(
        'module_path',
        help='Path to the OHOS module directory'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    try:
        analyzer = ArchitectureAnalyzer(args.module_path)
        analysis = analyzer.analyze()

        if args.json:
            import json
            print(json.dumps(analysis, indent=2))
        else:
            analyzer.print_report(analysis)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
