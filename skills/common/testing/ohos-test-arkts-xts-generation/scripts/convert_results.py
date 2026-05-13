#!/usr/bin/env python3
"""
覆盖率扫描结果 Excel → CSV 转换工具

读取 APICoverageDetector 输出的 Excel 文件，自动根据 .oh-xts-config.json 中的
ets_version 配置，为每个版本转换 Excel → CSV 并保存到迭代目录。

用法：
    python scripts/convert_results.py --iter 1 --phase before
    python scripts/convert_results.py --iter 1 --phase after
    python scripts/convert_results.py --phase before  (自动 iter-1)
"""

import argparse
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
        return ['ets1.1'], os.path.join(SKILL_ROOT, 'APICoverageDetector')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    ets_version = config.get('ets_version', ['ets1.1'])
    if isinstance(ets_version, str):
        ets_version = [v.strip() for v in ets_version.split(',')]
    scan_tool_root = config.get('scan_tool_root', '')
    if not scan_tool_root or not os.path.isdir(scan_tool_root):
        scan_tool_root = os.path.join(SKILL_ROOT, 'APICoverageDetector')
    return ets_version, scan_tool_root


def main():
    parser = argparse.ArgumentParser(description='Convert APICoverageDetector Excel results to CSV')
    parser.add_argument('--iter', type=int, default=1, help='Iteration number (default: 1)')
    parser.add_argument('--phase', required=True, choices=['before', 'after'],
                        help='Phase: before=before generation, after=after generation')
    parser.add_argument('--source', choices=['detailed', 'summary', 'all'], default='all',
                        help='Which xlsx to convert: detailed=all_collect.xlsx, summary=sdk_result.xlsx, all=both')
    args = parser.parse_args()

    ets_versions, scan_tool_root = load_config()
    results_dir = os.path.join(scan_tool_root, 'results')
    iter_dir = os.path.join(SKILL_ROOT, '.coverage_data', f'iter-{args.iter}')
    os.makedirs(iter_dir, exist_ok=True)

    read_excel_path = os.path.join(SCRIPT_DIR, 'read_excel.py')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    converted = 0

    xlsx_sources = []
    if args.source in ('detailed', 'all'):
        xlsx_sources.append(('all_collect.xlsx', 'detailed'))
    if args.source in ('summary', 'all'):
        xlsx_sources.append(('sdk_result.xlsx', 'summary'))

    for ver in ets_versions:
        ver_dir = os.path.join(results_dir, ver, 'open_source')
        if not os.path.isdir(ver_dir):
            print(f"  [SKIP] {ver}: results dir not found at {ver_dir}")
            continue

        for xlsx_name, label in xlsx_sources:
            excel_path = os.path.join(ver_dir, xlsx_name)
            if not os.path.exists(excel_path):
                print(f"  [SKIP] {ver}/{label}: {xlsx_name} not found")
                continue

            csv_name = f'{args.phase}_generation_{ver}_{label}_{timestamp}.csv'
            csv_path = os.path.join(iter_dir, csv_name)

            import subprocess
            result = subprocess.run(
                [sys.executable, read_excel_path, excel_path, '-f', 'csv', '-o', csv_path],
                capture_output=True, text=True, timeout=120
            )

            if result.returncode == 0 and os.path.exists(csv_path):
                size = os.path.getsize(csv_path)
                print(f"  [OK] {ver}/{label}: {csv_name} ({size} bytes)")
                converted += 1
            else:
                print(f"  [ERROR] {ver}/{label}: conversion failed")
                if result.stderr:
                    print(f"         {result.stderr.strip()[:200]}")

    print(f"\n  Iteration dir: {iter_dir}")
    print(f"  Converted: {converted} file(s)")

    return 0 if converted > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
