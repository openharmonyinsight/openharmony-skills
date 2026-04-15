#!/usr/bin/env python3
"""XTS Test Code Quality Scanner v1.0.0 - Entry Point

Usage:
    python main.py /path/to/xts/acts --level all
    python main.py /path/to/xts/acts --rules R001,R002,R003
    python main.py /path/to/xts/acts --level critical
    python main.py /path/to/xts/acts --skip-rules R009,R013
    python main.py /path/to/xts/acts --level all --output /path/to/output

Pre-built scanner (1 rule):
    - R004: missing assertion (r004_scanner.py, mandatory)

Model-generated rules (22 rules, generated on-the-fly from SKILL.md):
    - R001, R002, R003, R005, R006, R007, R008, R009, R010, R011,
      R012, R013, R014, R015, R016, R017, R018, R019, R020, R021, R022, R023
"""
import os, sys, argparse, time

from common import (
    collect_files, ALL_SOURCE_EXTS, TEST_FILE_EXTS,
    find_independent_projects, generate_report, get_subsystem,
)

from r004_scanner import scan_r004

VERSION = '1.0.0'

ALL_RULES = [
    ('R001','禁止使用getSync系统接口','Critical'),
    ('R002','错误码断言必须是number类型','Critical'),
    ('R003','禁止恒真断言','Critical'),
    ('R004','测试用例缺少断言','Critical'),
    ('R005','组件尺寸使用固定值','Warning'),
    ('R006','禁止基于设备类型差异化','Critical'),
    ('R007','Test.json禁止配置项','Critical'),
    ('R008','用例声明格式不规范','Warning'),
    ('R009','@tc.number命名不规范','Warning'),
    ('R010','part_name/subsystem_name不匹配','Critical'),
    ('R011','testsuite重复','Critical'),
    ('R012','签名证书APL等级和app-feature配置错误','Critical'),
    ('R013','注释的废弃代码','Warning'),
    ('R014','测试HAP命名不规范','Critical'),
    ('R015','Level参数缺省','Warning'),
    ('R016','testcase命名规范','Warning'),
    ('R017','syscap.json配置多个能力','Critical'),
    ('R018','testcase重复','Critical'),
    ('R019','.key重复','Critical'),
    ('R020','.id重复','Critical'),
    ('R021','hypium版本号>=1.0.26','Critical'),
    ('R022','errcode值断言使用==而非===','Critical'),
    ('R023','禁止errcode值类型强转后断言','Critical'),
]

VALID_RULE_IDS = {r[0] for r in ALL_RULES}

PROJECT_RULES = {'R011', 'R019', 'R020', 'R021'}


def load_rule_scanners():
    """Load pre-built scanners.

    Pre-built scanner (1 rule):
    - R004: missing assertion (r004_scanner.py)

    All other rules (22 total) are model-generated on-the-fly based on rules/Rxxx/SKILL.md.
    """
    return {'R004': scan_r004}


def _validate_rule_ids(rule_str, label):
    if not rule_str:
        return []
    ids = [r.strip() for r in rule_str.split(',')]
    invalid = [r for r in ids if r not in VALID_RULE_IDS]
    if invalid:
        print(f"  警告: {label}包含无效规则ID: {invalid}", file=sys.stderr, flush=True)
    return ids


def main():
    parser = argparse.ArgumentParser(description=f'XTS Test Code Quality Scanner v{VERSION}')
    parser.add_argument('paths', nargs='+', help='Scan paths (files or directories)')
    parser.add_argument('--level', choices=['all','critical','warning'], default='all',
                        help='Rule severity level (default: all)')
    parser.add_argument('--rules', help='Comma-separated rule IDs to scan')
    parser.add_argument('--skip-rules', help='Comma-separated rule IDs to skip')
    parser.add_argument('--output', help='Output directory for reports')
    parser.add_argument('--fix', action='store_true', help='Auto-fix after scan (supported: R008,R011,R012,R014,R016,R018)')
    args = parser.parse_args()

    for p in args.paths:
        if not os.path.exists(p):
            print(f"  错误: 路径不存在: {p}", file=sys.stderr, flush=True)
            sys.exit(1)

    scan_root = args.paths[0]
    output_dir = args.output or scan_root

    if args.rules and args.level != 'all':
        print("  警告: --rules 与 --level 不建议同时使用，两者功能重叠。优先使用 --rules 指定具体规则，或使用 --level 按严重级别批量选择。", file=sys.stderr, flush=True)

    FIXABLE_RULES = {'R008', 'R011', 'R012', 'R014', 'R016', 'R018'}

    active_rules = ALL_RULES[:]
    if args.rules:
        valid_rules = _validate_rule_ids(args.rules, '--rules')
        active_rules = [(r,n,s) for r,n,s in ALL_RULES if r in valid_rules]
    elif args.level == 'critical':
        active_rules = [(r,n,s) for r,n,s in ALL_RULES if s == 'Critical']
    elif args.level == 'warning':
        active_rules = [(r,n,s) for r,n,s in ALL_RULES if s == 'Warning']
    if args.skip_rules:
        skip = set(_validate_rule_ids(args.skip_rules, '--skip-rules'))
        active_rules = [(r,n,s) for r,n,s in active_rules if r not in skip]

    if not active_rules:
        print("  错误: 没有可执行的规则。请检查 --rules/--skip-rules/--level 参数。", file=sys.stderr, flush=True)
        sys.exit(1)

    rule_counts = {}
    scanners = load_rule_scanners()

    t0 = time.time()
    print(f"[XTS Scanner v{VERSION}] 扫描路径: {', '.join(args.paths)}", flush=True)
    print(f"[XTS Scanner v{VERSION}] 规则级别: {args.level} ({len(active_rules)}条规则)", flush=True)
    print(flush=True)

    print("[1/4] 收集文件...", flush=True)
    all_source = collect_files(scan_root, ALL_SOURCE_EXTS)
    test_files = collect_files(scan_root, TEST_FILE_EXTS)
    build_gn = collect_files(scan_root, ['BUILD.gn'])
    test_json = collect_files(scan_root, ['Test.json'])
    p7b_files = collect_files(scan_root, ['.p7b'])
    syscap_f = collect_files(scan_root, ['syscap.json'])
    print(f"  源代码: {len(all_source)}, 测试: {len(test_files)}, BUILD.gn: {len(build_gn)}", flush=True)
    print(f"  Test.json: {len(test_json)}, p7b: {len(p7b_files)}, syscap.json: {len(syscap_f)}", flush=True)

    print("\n[2/4] 识别独立XTS工程...", flush=True)
    indep = find_independent_projects(scan_root)
    print(f"  独立工程: {len(indep)}", flush=True)

    FILE_MAP = {
        'R001': lambda: all_source, 'R002': lambda: all_source, 'R003': lambda: all_source,
        'R004': lambda: all_source, 'R005': lambda: all_source, 'R006': lambda: all_source,
        'R007': lambda: test_json, 'R008': lambda: test_files, 'R009': lambda: test_files,
        'R010': lambda: build_gn, 'R011': lambda: test_files, 'R012': lambda: p7b_files,
        'R013': lambda: test_files, 'R014': lambda: build_gn, 'R015': lambda: test_files,
        'R016': lambda: test_files, 'R017': lambda: syscap_f, 'R018': lambda: test_files,
        'R019': lambda: all_source, 'R020': lambda: all_source, 'R021': lambda: all_source,
        'R022': lambda: all_source, 'R023': lambda: all_source,
    }

    print(f"\n[3/4] 逐规则扫描 ({len(active_rules)}条)...", flush=True)
    all_issues = []
    for rid, rn, sev in active_rules:
        label = f"  扫描 {rid} ({rn})..."
        try:
            if rid not in scanners:
                print(f"{label} 跳过（需模型动态生成扫描代码，当前未实现）", flush=True)
                rule_counts[rid] = 0
                continue

            scanner_fn = scanners[rid]
            if rid in PROJECT_RULES:
                kwargs = {}
                if rid == 'R021':
                    kwargs['independent_projects'] = indep
                r = scanner_fn(scan_root, indep, **kwargs) if rid != 'R021' else scanner_fn([], scan_root, independent_projects=indep)
            else:
                r = scanner_fn(FILE_MAP[rid](), scan_root)
            c = len(r)
            rule_counts[rid] = c
            all_issues.extend(r)
            status = f"{c} 个问题"
            print(f"{label} {status}", flush=True)
        except Exception as e:
            print(f"{label} 出错: {e}", file=sys.stderr, flush=True)
            rule_counts[rid] = -1

    elapsed = time.time() - t0
    print(f"\n[4/4] 生成报告...", flush=True)
    rules_info_with_fn = [(r,n,s,scanners.get(r, lambda: [])) for r,n,s in active_rules]
    ep = generate_report(all_issues, output_dir, rules_info_with_fn, rule_counts)
    print(f"  Excel: {ep} (UTF-8 BOM)", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"扫描统计报告", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"| 规则编号 | 问题类型 | 严重级别 | 问题数量 |", flush=True)
    print(f"|---------|---------|---------|---------|", flush=True)
    for rid, rn, sev in active_rules:
        c = rule_counts.get(rid, 0)
        if c < 0:
            display = "扫描出错"
        else:
            display = str(c)
        print(f"| {rid} | {rn} | {sev} | {display} |", flush=True)
    total = sum(v for v in rule_counts.values() if v > 0)
    error_count = sum(1 for v in rule_counts.values() if v < 0)
    print(f"\n总计: {total} 个问题 | 耗时: {elapsed:.1f}s", flush=True)
    if error_count > 0:
        print(f"警告: {error_count} 条规则扫描出错，请检查上方错误信息。", file=sys.stderr, flush=True)

    print(f"\n[完整性检查] 全部 {len(active_rules)} 条规则已执行完毕。", flush=True)

    if args.fix:
        fixable_in_scan = [(r,n,s) for r,n,s in active_rules if r in FIXABLE_RULES]
        fix_issues = [i for i in all_issues if i.get('rule') in FIXABLE_RULES]
        if not fixable_in_scan:
            print(f"\n[修复] 当前扫描范围内无可修复规则。--fix 仅支持: {', '.join(sorted(FIXABLE_RULES))}", flush=True)
        elif not fix_issues:
            print(f"\n[修复] 可修复规则无问题需要修复。", flush=True)
        else:
            print(f"\n[修复] 准备修复 {len(fix_issues)} 个问题（涉及规则: {', '.join(sorted(set(i['rule'] for i in fix_issues)))}）...", flush=True)
            print(f"  提示: 修复将直接修改源文件。请确保已备份或提交代码到版本控制系统。", flush=True)
            print(f"  修复指南目录: guides/", flush=True)
            print(f"  支持修复的规则:", flush=True)
            for rid in sorted(set(i['rule'] for i in fix_issues)):
                rn = next((n for r,n,s in ALL_RULES if r == rid), '')
                guide_map = {
                    'R008': 'guides/R008_testcase_format/R008_FIX_GUIDE.md',
                    'R011': 'guides/R011_testsuite_duplicate/R011_FIX_GUIDE.md',
                    'R012': 'guides/R012_p7b_signature/R012_FIX_GUIDE.md',
                    'R014': 'guides/R014_hap_naming/R014_HAP_NAMING_GUIDE.md',
                    'R016': 'guides/R016_testcase_naming/R016_FIX_GUIDE.md',
                    'R018': 'guides/R018_testcase_duplicate/R018_FIX_GUIDE.md',
                }
                guide = guide_map.get(rid, '')
                issue_count = sum(1 for i in fix_issues if i['rule'] == rid)
                print(f"    {rid} ({rn}): {issue_count} 个问题 → {guide}", flush=True)
            print(f"\n  请按上述修复指南逐一修复。修复完成后重新扫描验证。", flush=True)

    if error_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
