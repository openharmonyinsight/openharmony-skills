#!/usr/bin/env python3
"""Compare before/after uncovered API JSON files and generate a coverage change report.

Reads two JSON files produced by extract_uncovered.py (before and after generation),
computes per-API dimension-level changes, and outputs a Markdown comparison report.

Usage:
    python compare_uncovered.py \\
        --before .coverage_data/iter-1/uncovered_apis_xxx.json \\
        --after  .coverage_data/iter-2/uncovered_apis_xxx.json

    # With manual_confirm files (optional, enriches the report)
    python compare_uncovered.py \\
        --before .coverage_data/iter-1/uncovered_apis_xxx.json \\
        --after  .coverage_data/iter-2/uncovered_apis_xxx.json \\
        --before-mc .coverage_data/iter-1/manual_confirm_xxx.json \\
        --after-mc  .coverage_data/iter-2/manual_confirm_xxx.json

    # Specify output path
    python compare_uncovered.py \\
        --before ... --after ... \\
        --output .coverage_data/iter-2/coverage_comparison_ets1.1.md
"""

import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(SCRIPT_DIR, '..')

DIMS = ['call', 'param', 'param_spec', 'return_value', 'error_code', 'permission', 'stage', 'meta']


def load_json(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_api_map(uncovered_json, mc_json=None):
    """Build a unified map: key -> {dims, uncovered_dims, mc_dims, entry}.

    key format: "module|class|method|func"
    """
    api_map = {}

    # From uncovered JSON
    if uncovered_json:
        for ver in uncovered_json:
            if ver == 'metadata':
                continue
            ver_data = uncovered_json[ver]
            for category in ('methods', 'interfaces', 'properties'):
                for entry in ver_data.get(category, []):
                    key = f"{entry.get('module','')}|{entry.get('class','')}|{entry.get('method','')}|{entry.get('func','')}"
                    uncovered_dims = list(entry.get('coverage', {}).keys())
                    api_map[key] = {
                        'entry': entry,
                        'uncovered_dims': uncovered_dims,
                        'mc_dims': [],
                        'all_uncovered': set(uncovered_dims),
                    }

    # From manual_confirm JSON
    if mc_json:
        for entry in mc_json.get('manual_confirm', []):
            key = f"{entry.get('module','')}|{entry.get('class','')}|{entry.get('method','')}|{entry.get('func','')}"
            mc_dims = [k for k in entry if k not in ('module', 'class', 'method', 'func',
                                                       'file_path', 'subsystem', 'kit')
                       and isinstance(entry[k], dict) and 'status' in entry[k]]
            if key in api_map:
                api_map[key]['mc_dims'] = mc_dims
                api_map[key]['all_uncovered'].update(mc_dims)
            else:
                api_map[key] = {
                    'entry': entry,
                    'uncovered_dims': [],
                    'mc_dims': mc_dims,
                    'all_uncovered': set(mc_dims),
                }

    return api_map


def compare(before_map, after_map):
    """Compare before/after maps, return structured diff."""
    all_keys = sorted(set(list(before_map.keys()) + list(after_map.keys())))

    improved = []       # some dims newly covered
    regressed = []      # dims lost coverage
    fully_covered = []  # all previously uncovered dims now covered
    still_uncovered = [] # no change, still has uncovered dims
    newly_uncovered = [] # was fully covered, now has uncovered dims

    for key in all_keys:
        b = before_map.get(key)
        a = after_map.get(key)

        b_uncov = b['all_uncovered'] if b else set()
        a_uncov = a['all_uncovered'] if a else set()

        b_info = b['entry'] if b else {}
        a_info = a['entry'] if a else {}

        display = f"{a_info.get('class', b_info.get('class',''))}::{a_info.get('method', b_info.get('method',''))}"

        if b_uncov and not a_uncov:
            # Was uncovered, now fully covered
            fully_covered.append({
                'key': key,
                'display': display,
                'before_dims': sorted(b_uncov),
                'before_entry': b_info,
                'after_entry': a_info,
            })
        elif not b_uncov and a_uncov:
            # Was covered, now uncovered (regression)
            newly_uncovered.append({
                'key': key,
                'display': display,
                'after_dims': sorted(a_uncov),
                'before_entry': b_info,
                'after_entry': a_info,
            })
        elif b_uncov and a_uncov:
            resolved = b_uncov - a_uncov
            new_issues = a_uncov - b_uncov
            if resolved and not new_issues:
                improved.append({
                    'key': key,
                    'display': display,
                    'resolved_dims': sorted(resolved),
                    'still_dims': sorted(a_uncov),
                    'before_entry': b_info,
                    'after_entry': a_info,
                })
            elif new_issues and not resolved:
                regressed.append({
                    'key': key,
                    'display': display,
                    'new_dims': sorted(new_issues),
                    'before_entry': b_info,
                    'after_entry': a_info,
                })
            elif resolved and new_issues:
                # Mixed: some improved, some regressed
                improved.append({
                    'key': key,
                    'display': display,
                    'resolved_dims': sorted(resolved),
                    'still_dims': sorted(a_uncov),
                    'new_dims': sorted(new_issues),
                    'before_entry': b_info,
                    'after_entry': a_info,
                    'mixed': True,
                })
            else:
                # No change
                still_uncovered.append({
                    'key': key,
                    'display': display,
                    'dims': sorted(a_uncov),
                    'entry': a_info,
                })
        # else: both empty, no change, skip

    return {
        'improved': improved,
        'regressed': regressed,
        'fully_covered': fully_covered,
        'still_uncovered': still_uncovered,
        'newly_uncovered': newly_uncovered,
    }


def generate_report(diff, before_path, after_path, before_mc_path=None, after_mc_path=None):
    """Generate Markdown comparison report."""
    R = []

    R.append('# 覆盖率变化对比报告')
    R.append('')
    R.append(f'- **Before**: {os.path.basename(before_path)}')
    R.append(f'- **After**:  {os.path.basename(after_path)}')
    if before_mc_path:
        R.append(f'- **Before MC**: {os.path.basename(before_mc_path)}')
    if after_mc_path:
        R.append(f'- **After MC**:  {os.path.basename(after_mc_path)}')
    R.append(f'- **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    R.append('')

    # Summary stats
    total_before = (len(diff['fully_covered']) + len(diff['improved']) +
                    len(diff['still_uncovered']) + len(diff['regressed']) +
                    len(diff['newly_uncovered']))
    total_resolved = len(diff['fully_covered'])
    total_improved = len(diff['improved'])
    total_unchanged = len(diff['still_uncovered'])
    total_regressed = len(diff['regressed']) + len(diff['newly_uncovered'])

    R.append('## 1. 总体概览')
    R.append('')
    R.append('| 指标 | 数量 | 说明 |')
    R.append('|------|------|------|')
    R.append(f'| 涉及 API 总数 | {total_before} | before/after 中出现过未覆盖维度的 API |')
    R.append(f'| 新增完全覆盖 | {total_resolved} | 之前未覆盖维度现已全部解决 |')
    R.append(f'| 部分改善 | {total_improved} | 部分维度新增覆盖 |')
    R.append(f'| 无变化（仍有未覆盖） | {total_unchanged} | 覆盖维度未变化 |')
    R.append(f'| 回退 | {total_regressed} | 新增未覆盖维度（需关注） |')
    R.append('')

    # Fully covered
    if diff['fully_covered']:
        R.append('## 2. 新增完全覆盖')
        R.append('')
        for item in diff['fully_covered']:
            dims = ', '.join(item['before_dims'])
            R.append(f'- **{item["display"]}** ← {dims}')
        R.append('')

    # Improved
    if diff['improved']:
        R.append('## 3. 部分改善')
        R.append('')
        for item in diff['improved']:
            resolved = ', '.join(item['resolved_dims'])
            still = ', '.join(item['still_dims'])
            line = f'- **{item["display"]}**: +{resolved}'
            if item.get('new_dims'):
                line += f', -{", ".join(item["new_dims"])}'
            line += f' (仍缺: {still})'
            R.append(line)
        R.append('')

    # Still uncovered
    if diff['still_uncovered']:
        R.append(f'## 4. 无变化（仍有未覆盖维度）— {len(diff["still_uncovered"])} 个')
        R.append('')
        for item in diff['still_uncovered']:
            dims = ', '.join(item['dims'])
            entry = item.get('entry', {})
            fp = entry.get('file_path', '')
            R.append(f'- **{item["display"]}**: {dims}' + (f'  ({fp})' if fp else ''))
        R.append('')

    # Regressed
    if diff['regressed'] or diff['newly_uncovered']:
        R.append('## 5. 回退（需关注）')
        R.append('')
        for item in diff['regressed']:
            dims = ', '.join(item['new_dims'])
            R.append(f'- **{item["display"]}**: 新增未覆盖维度 {dims}')
        for item in diff['newly_uncovered']:
            dims = ', '.join(item['after_dims'])
            R.append(f'- **{item["display"]}**: 从覆盖变为未覆盖 {dims}')
        R.append('')

    return '\n'.join(R)


def main():
    parser = argparse.ArgumentParser(
        description='Compare before/after uncovered API JSON files and generate a change report')
    parser.add_argument('--before', required=True,
                        help='Path to before uncovered_apis JSON')
    parser.add_argument('--after', required=True,
                        help='Path to after uncovered_apis JSON')
    parser.add_argument('--before-mc', default=None,
                        help='Path to before manual_confirm JSON (optional)')
    parser.add_argument('--after-mc', default=None,
                        help='Path to after manual_confirm JSON (optional)')
    parser.add_argument('--output', '-o', default=None,
                        help='Output path for MD report (default: auto-generate)')
    parser.add_argument('--iter', type=int, default=None,
                        help='Iteration number for auto output path')
    parser.add_argument('--task-subsystem', type=str, default=None,
                        help='Task subsystem for output path (e.g. testfwk)')
    parser.add_argument('--task-module', type=str, default=None,
                        help='Task module for output path (e.g. uitest)')
    parser.add_argument('--session-id', type=str, default=None,
                        help='Session ID matching .task_summary/session_XXX (e.g. session_20260602_150300)')
    args = parser.parse_args()

    before_data = load_json(args.before)
    after_data = load_json(args.after)
    before_mc = load_json(args.before_mc)
    after_mc = load_json(args.after_mc)

    if not before_data:
        print(f'[ERROR] Cannot load before file: {args.before}', file=sys.stderr)
        return 1
    if not after_data:
        print(f'[ERROR] Cannot load after file: {args.after}', file=sys.stderr)
        return 1

    before_map = build_api_map(before_data, before_mc)
    after_map = build_api_map(after_data, after_mc)

    print(f'Before: {len(before_map)} APIs with uncovered dims')
    print(f'After:  {len(after_map)} APIs with uncovered dims')

    diff = compare(before_map, after_map)

    print(f'  Fully covered: {len(diff["fully_covered"])}')
    print(f'  Improved:      {len(diff["improved"])}')
    print(f'  Still uncovered: {len(diff["still_uncovered"])}')
    print(f'  Regressed:     {len(diff["regressed"]) + len(diff["newly_uncovered"])}')

    report = generate_report(diff, args.before, args.after, args.before_mc, args.after_mc)

    # Determine output path
    output_path = args.output
    if not output_path:
        iter_num = args.iter or 2
        base_dir = os.path.join(SKILL_ROOT, '.coverage_data')
        if args.task_subsystem and args.task_module:
            base_dir = os.path.join(base_dir, args.task_subsystem, args.task_module)
        if getattr(args, 'session_id', None):
            base_dir = os.path.join(base_dir, args.session_id)
        output_dir = os.path.join(base_dir, f'iter-{iter_num}')
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        output_path = os.path.join(output_dir, f'coverage_comparison_{timestamp}.md')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'\nReport saved to: {output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
