#!/usr/bin/env python3
"""
DTS Analyzer - Analyze TypeScript definition files for @crossplatform coverage

This script scans .d.ts files to determine which interfaces have been adapted
for cross-platform support by checking for @crossplatform annotations.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
import argparse


class DTSAnalyzer:
    def __init__(self, dts_file: str):
        self.dts_file = Path(dts_file)
        if not self.dts_file.exists():
            raise FileNotFoundError(f"DTS file not found: {dts_file}")

        self.content = self.dts_file.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')

    def analyze(self) -> Dict:
        """Perform comprehensive analysis of the .d.ts file"""
        interfaces = self._find_interfaces()

        adapted_count = sum(1 for iface in interfaces if iface['has_crossplatform'])
        total_count = len(interfaces)

        return {
            'file': str(self.dts_file),
            'total_interfaces': total_count,
            'adapted_interfaces': adapted_count,
            'needs_adaptation': total_count - adapted_count,
            'coverage_percent': (adapted_count / total_count * 100) if total_count > 0 else 0,
            'by_category': self._categorize_interfaces(interfaces),
            'needs_adaptation_list': [iface for iface in interfaces if not iface['has_crossplatform']],
        }

    def _find_interfaces(self) -> List[Dict]:
        """Find all interfaces with their crossplatform status"""
        interfaces = []
        current_interface = None
        in_interface_block = False
        brace_depth = 0

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Detect interface/class/function declaration
            if re.match(r'(export\s+)?(class|interface|function)\s+\w+', line):
                match = re.search(r'(class|interface|function)\s+(\w+)', line)
                if match:
                    current_interface = {
                        'type': match.group(1),
                        'name': match.group(2),
                        'line': i,
                        'has_crossplatform': False,
                        'signature': stripped
                    }

            # Check for @crossplatform annotation in nearby lines (within 5 lines above)
            if current_interface and not current_interface['has_crossplatform']:
                # Check from declaration up to 5 lines back
                start_line = max(0, current_interface['line'] - 6)
                context_lines = self.lines[start_line:current_interface['line']]
                for ctx_line in context_lines:
                    if '@crossplatform' in ctx_line or '@cp' in ctx_line:
                        current_interface['has_crossplatform'] = True
                        break

            # Save interface when we exit its block
            if current_interface and '{' in line:
                brace_depth += 1
                in_interface_block = True

            if in_interface_block and '}' in line:
                brace_depth -= 1
                if brace_depth == 0 and current_interface:
                    interfaces.append(current_interface)
                    current_interface = None
                    in_interface_block = False

        return interfaces

    def _categorize_interfaces(self, interfaces: List[Dict]) -> Dict:
        """Categorize interfaces by type"""
        categories = Counter()
        for iface in interfaces:
            categories[iface['type']] += 1

        return dict(categories)

    def print_report(self, analysis: Dict):
        """Print formatted analysis report"""
        print(f"\n{'='*70}")
        print(f"📋 API Interface Analysis: {self.dts_file.name}")
        print(f"{'='*70}")

        print(f"\n📊 Interface Statistics:")
        print(f"   Total interfaces:        {analysis['total_interfaces']}")

        if analysis['by_category']:
            print(f"\n   By Category:")
            for category, count in sorted(analysis['by_category'].items()):
                print(f"   - {category}: {count}")

        print(f"\n✅ Adaptation Status:")
        print(f"   Already adapted (@crossplatform):    {analysis['adapted_interfaces']} "
              f"({analysis['coverage_percent']:.1f}%)")
        print(f"   Needs adaptation (no @crossplatform): {analysis['needs_adaptation']} "
              f"({100-analysis['coverage_percent']:.1f}%)")

        if analysis['needs_adaptation_list']:
            print(f"\n📋 Interfaces Needing Adaptation:")
            for iface in analysis['needs_adaptation_list']:
                print(f"   ❌ {iface['type']} {iface['name']}")
                print(f"      {iface['signature']}")
                print(f"      - Line {iface['line']}")

        # Progress bar
        progress = int(analysis['coverage_percent'] / 5)
        bar = '█' * progress + '░' * (20 - progress)
        print(f"\n📈 Adaptation Progress: {bar} {analysis['coverage_percent']:.1f}%")

        # Recommendation
        if analysis['coverage_percent'] >= 80:
            print(f"\n⚠️  Recommendation:")
            print(f"   High coverage detected. Consider incremental adaptation")
            print(f"   of the remaining {analysis['needs_adaptation']} interfaces.")
            priority = "MEDIUM" if analysis['coverage_percent'] < 95 else "LOW"
            print(f"   Priority: {priority}")
        elif analysis['coverage_percent'] < 50:
            print(f"\n⚠️  Recommendation:")
            print(f"   Low coverage detected. Consider full module adaptation")
            print(f"   with architecture analysis first.")
            print(f"   Priority: HIGH")
        else:
            print(f"\n⚠️  Recommendation:")
            print(f"   Medium coverage. Proceed with standard adaptation workflow.")
            print(f"   Priority: MEDIUM")

        print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze .d.ts files for @crossplatform coverage'
    )
    parser.add_argument(
        'dts_file',
        help='Path to the .d.ts file to analyze'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    try:
        analyzer = DTSAnalyzer(args.dts_file)
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
