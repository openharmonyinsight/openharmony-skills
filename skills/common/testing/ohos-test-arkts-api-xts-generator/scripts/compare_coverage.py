#!/usr/bin/env python3
"""
覆盖率前后对比工具

对比同一轮迭代中 before_generation 和 after_generation 的 CSV 文件，
计算覆盖率提升并生成 Markdown 报告。

用法：
    python scripts/compare_coverage.py --iter 1
    python scripts/compare_coverage.py --iter 1 --ets-version ets1.1
"""

import argparse
import csv
import glob
import json
import os
import sys
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(SCRIPT_DIR, '..')


def load_config():
    config_path = os.path.join(SKILL_ROOT, '.oh-xts-config.json')
    if not os.path.exists(config_path):
        return ['ets1.1']
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    ets_version = config.get('ets_version', ['ets1.1'])
    if isinstance(ets_version, str):
        ets_version = [v.strip() for v in ets_version.split(',')]
    return ets_version


def find_csv(iter_dir, prefix):
    pattern = os.path.join(iter_dir, f'{prefix}_*.csv')
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


def parse_coverage_csv(filepath):
    covered = {}
    uncovered = {}
    total = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) < 2:
        return covered, uncovered, total

    header = rows[0]
    col_count = len(header)

    method_col = 2
    is_covered_col = None
    for i, h in enumerate(header):
        if h and 'covered' in str(h).lower():
            is_covered_col = i
            break

    if is_covered_col is None and col_count >= 27:
        is_covered_col = 26

    for row in rows[1:]:
        if len(row) < 3:
            continue
        api_type = row[4] if len(row) > 4 else ''
        if api_type in ('Import', 'TypeAlias', 'EnumValue'):
            continue

        method = row[method_col] if len(row) > method_col else ''
        cls = row[1] if len(row) > 1 else ''
        key = f"{cls}.{method}"

        total += 1

        if is_covered_col is not None and is_covered_col < len(row):
            val = str(row[is_covered_col]).strip().lower()
            if val in ('true', '1', 'yes'):
                covered[key] = row
            else:
                uncovered[key] = row
        else:
            uncovered[key] = row

    return covered, uncovered, total


def generate_report(before_total, before_covered, before_uncovered,
                    after_total, after_covered, after_uncovered,
                    version, iter_num):
    before_rate = len(before_covered) / before_total * 100 if before_total > 0 else 0
    after_rate = len(after_covered) / after_total * 100 if after_total > 0 else 0
    delta = after_rate - before_rate

    newly_covered = set(after_covered.keys()) - set(before_covered.keys())
    still_uncovered = set(after_uncovered.keys()) & set(before_uncovered.keys())

    lines = [
        f'# Coverage Comparison Report',
        f'',
        f'- **ETS Version**: {version}',
        f'- **Iteration**: {iter_num}',
        f'- **Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'',
        f'## Summary',
        f'',
        f'| Metric | Before | After | Delta |',
        f'|--------|--------|-------|-------|',
        f'| Total APIs | {before_total} | {after_total} | |',
        f'| Covered | {len(before_covered)} | {len(after_covered)} | +{len(after_covered) - len(before_covered)} |',
        f'| Uncovered | {len(before_uncovered)} | {len(after_uncovered)} | {len(after_uncovered) - len(before_uncovered)} |',
        f'| Coverage Rate | {before_rate:.1f}% | {after_rate:.1f}% | {"+" if delta >= 0 else ""}{delta:.1f}% |',
        f'',
        f'## Newly Covered APIs ({len(newly_covered)})',
        f'',
    ]

    if newly_covered:
        for api in sorted(newly_covered)[:50]:
            lines.append(f'- `{api}`')
        if len(newly_covered) > 50:
            lines.append(f'- ... and {len(newly_covered) - 50} more')
    else:
        lines.append('None')

    lines.extend([
        f'',
        f'## Still Uncovered ({len(still_uncovered)})',
        f'',
    ])

    if still_uncovered:
        for api in sorted(still_uncovered)[:30]:
            lines.append(f'- `{api}`')
        if len(still_uncovered) > 30:
            lines.append(f'- ... and {len(still_uncovered) - 30} more')
    else:
        lines.append('All APIs covered!')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compare before/after coverage CSV files')
    parser.add_argument('--iter', type=int, default=1, help='Iteration number')
    parser.add_argument('--ets-version', default=None, help='Specific ETS version (default: all configured)')
    args = parser.parse_args()

    ets_versions = [args.ets_version] if args.ets_version else load_config()
    iter_dir = os.path.join(SKILL_ROOT, '.coverage_data', f'iter-{args.iter}')

    if not os.path.exists(iter_dir):
        print(f'[ERROR] Iteration directory not found: {iter_dir}')
        return 1

    for ver in ets_versions:
        print(f'\n[COMPARE] {ver}, iteration {args.iter}')

        before_file = find_csv(iter_dir, f'before_generation_{ver}')
        after_file = find_csv(iter_dir, f'after_generation_{ver}')

        if not before_file:
            print(f'  [ERROR] No before_generation CSV found for {ver}')
            continue
        if not after_file:
            print(f'  [ERROR] No after_generation CSV found for {ver}')
            continue

        print(f'  Before: {os.path.basename(before_file)}')
        print(f'  After:  {os.path.basename(after_file)}')

        before_cov, before_uncov, before_total = parse_coverage_csv(before_file)
        after_cov, after_uncov, after_total = parse_coverage_csv(after_file)

        report = generate_report(
            before_total, before_cov, before_uncov,
            after_total, after_cov, after_uncov,
            ver, args.iter
        )

        report_path = os.path.join(iter_dir, f'coverage_comparison_{ver}.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        before_rate = len(before_cov) / before_total * 100 if before_total > 0 else 0
        after_rate = len(after_cov) / after_total * 100 if after_total > 0 else 0
        print(f'  Before: {before_rate:.1f}% ({len(before_cov)}/{before_total})')
        print(f'  After:  {after_rate:.1f}% ({len(after_cov)}/{after_total})')
        print(f'  Delta:  {"+" if after_rate >= before_rate else ""}{after_rate - before_rate:.1f}%')
        print(f'  Report: {report_path}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
