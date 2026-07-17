#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""XTS Test Code Quality Scanner v2.0.12 - Entry Point

v2.0.12 changes:
- PR评论增加"可自动修复"提示： 问题规则统计表增加"可自动修复"列，- 问题示例增加"可自动修复"标识和修复建议提示

v2.0.11 changes:
- PR模式增加--submit提示：扫描完成后提示用户可使用--submit提交PR检视评论

v2.0.10 changes:
- R012修复：补充APL_RE和APP_FEATURE_RE正则定义，修复openssl解析失败时回退逻辑不工作的问题

v2.0.9 changes:
- 报告增强：Excel和HTML报告增加"可自动修复"列，提示用户使用--fix或参考修复指南
- 终端输出：扫描结果表增加"可自动修复"列，汇总提示可自动修复的问题数和修复指南路径

v2.0.2 changes:
- 元数据整改：符合OpenHarmony Skills命名空间与目录放置规范
- R201修复：async+done混用模式下检测所有异步操作（包括setTimeout）
- R202修复：扩大catch检测范围，添加文件大小限制，避免误报
- 性能优化：禁用grep预过滤，解决大目录扫描超时问题
- 测试验证：完成11个子系统对比测试，修复效果验证通过

v2.0.0 changes:
- 文件级并行引擎（替代规则级并行）
- 整合29个规则脚本为2个引擎文件（unified_engine + complex_rules）
- 文件数减少90%，代码量减少73%
- 性能提升3-5倍（遍历次数从29×N降到1×N）
- 进展反馈：每5分钟输出扫描进展

Usage:
    python main.py /path/to/xts_acts --level all
    python main.py /path/to/xts_acts --rules R001,R003,R201
    python main.py --pr https://gitcode.com/openharmony/xts_acts/pull/123 --token ghp_xxx --level all
"""
import os
import sys
import re
import argparse
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    collect_all_files, find_independent_projects_fast, find_sta_projects,
    generate_report, generate_html_report, get_subsystem, set_default_subsystem, EXCLUDED_DIRS,
    FileContentCache, BlockCache,
)
from config_loader import (
    get_all_rules, get_rule_ids, get_category_rules, get_critical_rules,
    get_warning_rules, get_fixable_rules, get_fix_guide_path, get_version,
    get_excluded_dirs, get_progress_interval,
)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scanners'))
from unified_engine import unified_scan, SIMPLE_RULES
from complex_rules import scan_complex_rules, ComplexRuleEngine

try:
    from pr_scanner import PRScanner, is_oh_gc_available, deduplicate_issues
    HAS_PR_SCANNER = True
except ImportError:
    HAS_PR_SCANNER = False

VERSION = get_version()
PROGRESS_INTERVAL = get_progress_interval()
PROGRESS_CHECK_INTERVAL = 30

ALL_RULES = get_all_rules()
VALID_RULE_IDS = get_rule_ids()
CATEGORY_RULES = get_category_rules()
LEVEL_RULES = {
    'critical': list(get_critical_rules()),
    'warning': list(get_warning_rules()),
    'all': list(VALID_RULE_IDS),
}

SIMPLE_RULE_IDS = set(SIMPLE_RULES.keys())
COMPLEX_RULE_IDS = set(ComplexRuleEngine.SCANNERS.keys())
PROJECT_RULE_IDS = {'R011', 'R019', 'R020'}

FIXABLE_RULES = get_fixable_rules()


def main():
    parser = argparse.ArgumentParser(description=f'XTS Test Code Quality Scanner v{VERSION} (文件级并行)')
    parser.add_argument('paths', nargs='*', default=[], help='Scan paths')
    parser.add_argument('--pr', help='GitCode PR URL')
    parser.add_argument('--token', help='GitCode Personal Access Token')
    parser.add_argument('--submit', action='store_true', help='Submit scan results as PR comments')
    parser.add_argument('--no-diff', action='store_true', help='Skip diff context fetching')
    parser.add_argument('--no-comments', action='store_true', help='Skip existing comments fetching')
    parser.add_argument('--level', choices=['all','critical','warning'], default='all')
    parser.add_argument('--rules', help='Comma-separated rule IDs (支持内置R001等、扩展R001_EXT、自定义C001)')
    parser.add_argument('--category', choices=list(CATEGORY_RULES.keys()))
    parser.add_argument('--ext', action='store_true', help='执行扩展规则（追加到内置规则）')
    parser.add_argument('--custom', action='store_true', help='执行自定义规则（追加到内置规则）')
    parser.add_argument('--rules-file', help='指定扩展/自定义规则JSON文件路径')
    parser.add_argument('--skip-rules', help='Comma-separated rule IDs to skip')
    parser.add_argument('--output', help='Output directory')
    parser.add_argument('--exclude', help='Extra dirs to exclude')
    parser.add_argument('--parallel', type=int, default=0, help='Parallel workers')
    parser.add_argument('--fix', action='store_true', help='Auto-fix after scan')
    parser.add_argument('--fix-only', action='store_true', help='Fix from previous scan results')
    parser.add_argument('--fix-rules', help='Rules to fix in --fix-only mode')
    parser.add_argument('--sta-mode', choices=['all','dyn','sta'], default='all', help='Sta project scan mode')
    args = parser.parse_args()

    scan_root = None
    pr_mode = False
    pr_info = None

    # PR模式处理
    if args.pr:
        if not HAS_PR_SCANNER:
            print("错误: PR模式需要 pr_scanner.py 模块", file=sys.stderr)
            sys.exit(1)
        if not args.token and not is_oh_gc_available() and not os.environ.get('GITCODE_TOKEN'):
            print("错误: --pr 模式需要认证。请选择以下任一方式：", file=sys.stderr)
            print("  1) 安装 oh-gc CLI: npm install -g @oh-gc-cli", file=sys.stderr)
            print("  2) 命令行参数: --token <YOUR_TOKEN>", file=sys.stderr)
            print("  3) 环境变量: export GITCODE_TOKEN=<YOUR_TOKEN>", file=sys.stderr)
            print("  Token获取: https://gitcode.com/-/profile/personal_access_tokens", file=sys.stderr)
            sys.exit(1)

        pr_mode = True
        scanner = PRScanner(token=args.token)
        try:
            pr_result = scanner.fetch_pr_files(
                args.pr,
                output_dir=args.output,
                fetch_diff=not args.no_diff,
                fetch_comments=not args.no_comments,
            )
            scan_root = pr_result.local_dir
            output_dir = args.output or scan_root
            pr_info = pr_result
            print(f"PR模式: {args.pr}", flush=True)
            print(f"  变更文件: {len(pr_result.changed_files)}", flush=True)
            print(f"  Diff上下文: {len(pr_result.diff_context)} 文件", flush=True)
            print(f"  已有评论: {len(pr_result.existing_comments)} 条", flush=True)
            print(f"  本地目录: {scan_root}", flush=True)
        except Exception as e:
            print(f"错误: 无法获取PR信息: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.paths:
            print("错误: 请指定扫描路径或使用 --pr 指定PR链接", file=sys.stderr)
            print("用法: python main.py /path/to/code [options]", file=sys.stderr)
            print("用法: python main.py --pr <URL> --token <TOKEN> [options]", file=sys.stderr)
            sys.exit(1)

        for p in args.paths:
            if not os.path.exists(p):
                print(f"错误: 路径不存在: {p}", file=sys.stderr)
                sys.exit(1)

        scan_root = args.paths[0]
        
        # 如果扫描单个文件，output_dir使用其父目录
        if os.path.isfile(scan_root):
            output_dir = args.output or os.path.dirname(scan_root)
        else:
            output_dir = args.output or scan_root

    # --fix-only 模式
    if args.fix_only:
        fix_rules_str = args.fix_rules or args.rules
        if not fix_rules_str:
            print("错误: --fix-only 模式需要指定 --rules 或 --fix-rules", file=sys.stderr)
            print(f"  可修复规则: {', '.join(sorted(FIXABLE_RULES))}", file=sys.stderr)
            sys.exit(1)

        fix_rule_ids = [r.strip() for r in fix_rules_str.split(',')]
        invalid_fix = [r for r in fix_rule_ids if r not in FIXABLE_RULES]
        if invalid_fix:
            print(f"错误: 以下规则不支持自动修复: {invalid_fix}", file=sys.stderr)
            print(f"  可修复规则: {', '.join(sorted(FIXABLE_RULES))}", file=sys.stderr)
            sys.exit(1)

        scan_meta_dir = os.path.join(output_dir, '.xts_scan')
        meta_path = os.path.join(scan_meta_dir, 'scan_meta.json')
        issues_path = os.path.join(scan_meta_dir, 'all_issues.json')

        if not os.path.isfile(meta_path) or not os.path.isfile(issues_path):
            print(f"错误: 未找到历史扫描结果。请先执行扫描:", file=sys.stderr)
            print(f"  python main.py {scan_root} --level all", file=sys.stderr)
            sys.exit(1)

        with open(meta_path, 'r', encoding='utf-8') as f:
            scan_meta = json.load(f)
        with open(issues_path, 'r', encoding='utf-8') as f:
            all_issues = json.load(f)

        print(f"[--fix-only 模式] 扫描路径: {scan_root}", flush=True)
        print(f"  扫描时间: {scan_meta.get('scan_time', '未知')}", flush=True)
        print(f"  总问题数: {scan_meta.get('total_issues', len(all_issues))}", flush=True)
        print(f"  修复规则: {', '.join(fix_rule_ids)}", flush=True)

        fix_set = set(fix_rule_ids)
        fix_issues = [i for i in all_issues if i.get('rule') in fix_set]
        if fix_issues:
            print(f"\n  请按 guides/ 下的修复指南逐一修复:", flush=True)
            for rid in sorted(set(i['rule'] for i in fix_issues)):
                rn = next((n for r, n, s in ALL_RULES if r == rid), '')
                count = sum(1 for i in fix_issues if i['rule'] == rid)
                guide_path = get_fix_guide_path(rid)
                print(f"    {rid} ({rn}): {count} 个问题 -> {guide_path}", flush=True)
        else:
            print(f"  指定规则无问题需要修复", flush=True)
        sys.exit(0)

    # 确定活动规则
    active_rule_ids = set()
    if args.rules:
        rule_ids = [r.strip() for r in args.rules.split(',')]
        invalid = [r for r in rule_ids if r not in VALID_RULE_IDS]
        if invalid:
            print(f"警告: 无效规则ID: {invalid}", file=sys.stderr)
        active_rule_ids = set(rule_ids) & VALID_RULE_IDS
    elif args.category:
        active_rule_ids = set(CATEGORY_RULES[args.category])
    else:
        active_rule_ids = set(LEVEL_RULES[args.level])

    if args.skip_rules:
        skip_ids = set(r.strip() for r in args.skip_rules.split(','))
        active_rule_ids -= skip_ids

    active_rules = [(r[0], r[1], r[2], lambda: []) for r in ALL_RULES if r[0] in active_rule_ids]

    # 加载扩展/自定义规则
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ext_rules = []
    custom_rules = []
    ext_rule_ids = set()
    custom_rule_ids = set()

    EXT_RULE_PATTERN = re.compile(r'^R\d{3}_EXT', re.IGNORECASE)
    CUSTOM_RULE_PATTERN = re.compile(r'^C\d{3}$', re.IGNORECASE)

    # 从 --rules 参数中识别扩展/自定义规则ID
    if args.rules:
        for rid in [r.strip() for r in args.rules.split(',')]:
            if EXT_RULE_PATTERN.match(rid):
                ext_rule_ids.add(rid)
            elif CUSTOM_RULE_PATTERN.match(rid):
                custom_rule_ids.add(rid)

    # --ext: 加载全部扩展规则
    if args.ext:
        ext_dir = os.path.join(skill_dir, 'references/custom_rules/extensions')
        if os.path.isdir(ext_dir):
            for f in os.listdir(ext_dir):
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(ext_dir, f), 'r', encoding='utf-8') as fp:
                            rule = json.load(fp)
                            if rule.get('type') == 'extension':
                                ext_rules.append(rule)
                                ext_rule_ids.add(rule.get('id'))
                    except Exception as e:
                        print(f"  警告: 加载扩展规则失败 {f}: {e}", file=sys.stderr)

    # --custom: 加载全部自定义规则
    if args.custom:
        custom_dir = os.path.join(scan_root, '.xts_custom_rules')
        if os.path.isdir(custom_dir):
            for f in os.listdir(custom_dir):
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(custom_dir, f), 'r', encoding='utf-8') as fp:
                            rule = json.load(fp)
                            if rule.get('type') == 'custom':
                                custom_rules.append(rule)
                                custom_rule_ids.add(rule.get('id'))
                    except Exception as e:
                        print(f"  警告: 加载自定义规则失败 {f}: {e}", file=sys.stderr)

    # --rules-file: 加载指定规则文件
    if args.rules_file:
        rules_file_path = args.rules_file
        if not os.path.isabs(rules_file_path):
            rules_file_path = os.path.join(scan_root, rules_file_path)
        if os.path.isfile(rules_file_path):
            try:
                with open(rules_file_path, 'r', encoding='utf-8') as fp:
                    rule = json.load(fp)
                    rtype = rule.get('type', '')
                    if rtype == 'extension':
                        ext_rules.append(rule)
                        ext_rule_ids.add(rule.get('id'))
                    elif rtype == 'custom':
                        custom_rules.append(rule)
                        custom_rule_ids.add(rule.get('id'))
            except Exception as e:
                print(f"  警告: 加载规则文件失败 {args.rules_file}: {e}", file=sys.stderr)

    # 根据ID从默认目录补充加载
    for rid in ext_rule_ids:
        if not any(r.get('id') == rid for r in ext_rules):
            ext_dir = os.path.join(skill_dir, 'references/custom_rules/extensions')
            for f in os.listdir(ext_dir) if os.path.isdir(ext_dir) else []:
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(ext_dir, f), 'r', encoding='utf-8') as fp:
                            rule = json.load(fp)
                            if rule.get('id') == rid:
                                ext_rules.append(rule)
                                break
                    except Exception:
                        pass

    for rid in custom_rule_ids:
        if not any(r.get('id') == rid for r in custom_rules):
            custom_dir = os.path.join(scan_root, '.xts_custom_rules')
            for f in os.listdir(custom_dir) if os.path.isdir(custom_dir) else []:
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(custom_dir, f), 'r', encoding='utf-8') as fp:
                            rule = json.load(fp)
                            if rule.get('id') == rid:
                                custom_rules.append(rule)
                                break
                    except Exception:
                        pass

    has_ext_or_custom = bool(ext_rules or custom_rules)

    print(f"\n{'='*60}", flush=True)
    print(f"XTS测试代码质量检查 v{VERSION} (文件级并行)", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"扫描路径: {scan_root}", flush=True)
    print(f"活动规则: {len(active_rules)}条", flush=True)

    # 收集文件
    print(f"\n[1/3] 收集文件...", flush=True)
    t1 = time.time()

    exclude_dirs = set(EXCLUDED_DIRS)
    if args.exclude:
        exclude_dirs.update(args.exclude.split(','))

    cats = collect_all_files(scan_root, exclude_dirs)

    all_source = cats['all_source']
    test_files = cats['test']
    build_gn = cats['build_gn']
    test_json = cats['test_json']
    p7b_files = cats['p7b']
    syscap_f = cats['syscap']

    total_files = len(all_source) + len(test_files) + len(build_gn) + \
                  len(test_json) + len(p7b_files) + len(syscap_f)

    print(f"  源文件: {len(all_source)}", flush=True)
    print(f"  测试文件: {len(test_files)}", flush=True)
    print(f"  BUILD.gn: {len(build_gn)}", flush=True)
    print(f"  test.json: {len(test_json)}", flush=True)
    print(f"  p7b签名: {len(p7b_files)}", flush=True)
    print(f"  syscap.json: {len(syscap_f)}", flush=True)
    print(f"  文件总数: {total_files}", flush=True)
    print(f"  耗时: {time.time()-t1:.1f}s", flush=True)

    # 合并所有需要扫描的文件
    all_files = list(dict.fromkeys(
        all_source + test_files + build_gn + test_json + p7b_files + syscap_f
    ))

    # 确定并行度
    n_workers = args.parallel or min(os.cpu_count() or 4, total_files)
    n_workers = max(1, min(n_workers, 32))

    # 文件级并行扫描
    print(f"\n[2/3] 文件级并行扫描 ({n_workers} 线程)...", flush=True)
    t2 = time.time()
    scan_start_time = time.time()

    all_issues = []
    rule_counts = {}

    fcache = FileContentCache(max_size=200000)
    bc = BlockCache(fcache)

    # 进展反馈线程
    _progress_state = {
        'phase': '',
        'done_files': 0,
        'total_files': len(all_files),
        'found_issues': 0,
        'start_time': scan_start_time,
        'last_report_time': 0,  # 初始为0，确保第一次立即输出
        'stop_event': threading.Event(),
        'lock': threading.Lock(),
    }

    def _progress_reporter():
        first_report = True
        while not _progress_state['stop_event'].is_set():
            wait_time = PROGRESS_CHECK_INTERVAL if not first_report else 1
            _progress_state['stop_event'].wait(wait_time)
            if _progress_state['stop_event'].is_set():
                break
            
            current_time = time.time()
            with _progress_state['lock']:
                last_report = _progress_state['last_report_time']
            
            # 第一次或距离上次报告超过1分钟才输出
            if first_report or current_time - last_report >= PROGRESS_INTERVAL:
                elapsed = int(current_time - _progress_state['start_time'])
                mm, ss = elapsed // 60, elapsed % 60
                with _progress_state['lock']:
                    phase = _progress_state['phase']
                    done = _progress_state['done_files']
                    total = _progress_state['total_files']
                    issues = _progress_state['found_issues']
                    _progress_state['last_report_time'] = current_time
                print(f"[进展] {phase} | 已扫描 {done}/{total} 文件 | 发现 {issues} 个问题 | 已耗时 {mm:02d}:{ss:02d}", flush=True)
                first_report = False

    def _progress_callback(done_files: int, total_files: int, found_issues: int):
        """进度回调函数"""
        with _progress_state['lock']:
            _progress_state['done_files'] = done_files
            _progress_state['found_issues'] = found_issues

    progress_thread = threading.Thread(target=_progress_reporter, daemon=True)
    progress_thread.start()

    # Phase 1: 简单规则 + 工程级规则（unified_engine）
    simple_rule_ids = active_rule_ids & SIMPLE_RULE_IDS
    project_rule_ids = active_rule_ids & PROJECT_RULE_IDS
    
    # 即使simple_rule_ids为空，如果有project_rule_ids，也需要调用unified_scan
    if simple_rule_ids or project_rule_ids:
        print(f"  简单规则: {len(simple_rule_ids)}条 (行级正则)", flush=True)
        print(f"  工程级规则: {len(project_rule_ids)}条 (R011/R019/R020)", flush=True)
        with _progress_state['lock']:
            _progress_state['phase'] = '简单规则+工程级规则扫描'

        simple_issues = unified_scan(
            all_files, scan_root,
            rules=simple_rule_ids,
            workers=n_workers,
            fcache=fcache,
            cats=cats,
            progress_callback=_progress_callback
        )

        for issue in simple_issues:
            rid = issue['rule']
            if rid not in active_rule_ids:
                continue
            rule_counts[rid] = rule_counts.get(rid, 0) + 1
            all_issues.append(issue)

        with _progress_state['lock']:
            _progress_state['done_files'] = len(all_files)
            _progress_state['found_issues'] = len(all_issues)

        print(f"    发现 {len(simple_issues)} 个问题", flush=True)

    # Phase 2: 复杂规则（complex_rules）
    complex_rule_ids = active_rule_ids & COMPLEX_RULE_IDS
    if complex_rule_ids:
        print(f"  复杂规则: {len(complex_rule_ids)}条 (块级/递归/远程)", flush=True)
        with _progress_state['lock']:
            _progress_state['phase'] = '复杂规则扫描'
            _progress_state['done_files'] = 0  # 重置计数
            _progress_state['total_files'] = len(test_files) + len(all_source) + len(p7b_files) + len(build_gn) + len(syscap_f)
            _progress_state['last_report_time'] = 0  # 重置以立即输出

        complex_files = list(dict.fromkeys(test_files + all_source + p7b_files + build_gn + syscap_f))
        
        # 获取Sta工程列表（用于R201/R206等规则）- 传入已收集的build_gn列表避免重复遍历
        sta_projects = find_sta_projects(scan_root, build_gn)
        
        complex_issues = scan_complex_rules(
            complex_files,
            scan_root,
            rules=complex_rule_ids,
            workers=n_workers,
            fcache=fcache,
            bc=bc,
            cats=cats,
            sta_projects=sta_projects,
            progress_callback=_progress_callback
        )

        for issue in complex_issues:
            rid = issue['rule']
            if rid not in active_rule_ids:
                continue
            rule_counts[rid] = rule_counts.get(rid, 0) + 1
            all_issues.append(issue)

        with _progress_state['lock']:
            _progress_state['done_files'] = len(complex_files)
            _progress_state['found_issues'] = len(all_issues)

        print(f"    发现 {len(complex_issues)} 个问题", flush=True)

    # Phase 4: 工程级规则（已在unified_engine中处理）
    _progress_state['stop_event'].set()
    progress_thread.join(timeout=2)

    print(f"  扫描耗时: {time.time()-t2:.1f}s", flush=True)
    print(f"  总问题数: {len(all_issues)}", flush=True)

    # 保存原始统计和问题（去重前）用于报告生成
    original_critical = sum(1 for i in all_issues if i.get('severity') == 'Critical')
    original_warning = sum(1 for i in all_issues if i.get('severity') == 'Warning')
    original_total = len(all_issues)
    original_issues_for_report = list(all_issues)  # 保存完整副本用于报告
    original_issues_for_example = all_issues[:50]  # 取前50个用于PR评论示例

    # PR模式: 问题去重（基于diff上下文和已有评论）
    if pr_mode and pr_info:
        if not args.no_comments or not args.no_diff:
            original_count = len(all_issues)
            all_issues = deduplicate_issues(
                all_issues,
                pr_info.existing_comments,
                pr_info.diff_context if not args.no_diff else None
            )
            dedup_count = original_count - len(all_issues)
            if dedup_count > 0:
                print(f"  去重过滤: 移除 {dedup_count} 个已报告/非变更行问题", flush=True)

        # PR模式风险边界提示
        project_rules_used = active_rule_ids & PROJECT_RULE_IDS
        if project_rules_used:
            print(f"\n  **警告**: PR模式仅扫描变更文件，工程级规则({','.join(project_rules_used)})可能漏检。", flush=True)
            print(f"  建议: 对工程级规则使用完整checkout扫描，或明确声明结论不完整。", flush=True)

    # 生成报告
    print(f"\n[3/3] 生成报告...", flush=True)
    t3 = time.time()

    scan_meta_dir = os.path.join(output_dir, '.xts_scan')
    os.makedirs(scan_meta_dir, exist_ok=True)

    # Markdown报告
    print("\n扫描结果:", flush=True)
    print("| 规则编号 | 问题类型 | 严重级别 | 可自动修复 | 问题数量 |", flush=True)
    print("|---------|---------|---------|-----------|---------|", flush=True)

    for rid, rn, sev, _ in active_rules:
        c = rule_counts.get(rid, 0)
        fixable = 'Yes' if rid in FIXABLE_RULES else 'No'
        print(f"| {rid} | {rn} | {sev} | {fixable} | {c} |", flush=True)
    
    # 可自动修复规则汇总提示
    fixable_issue_rules = [rid for rid in FIXABLE_RULES if rule_counts.get(rid, 0) > 0]
    if fixable_issue_rules:
        print(f"\n可自动修复规则 ({len(fixable_issue_rules)}条有问题):", flush=True)
        for rid in fixable_issue_rules:
            rn = next((n for r, n, s in ALL_RULES if r == rid), '')
            c = rule_counts.get(rid, 0)
            guide_path = get_fix_guide_path(rid)
            print(f"  {rid} ({rn}): {c}个问题 -> 使用 --fix 或参考 {guide_path}", flush=True)

    # 输出扩展/自定义规则信息（供AI执行）
    if has_ext_or_custom:
        ext_custom_path = os.path.join(scan_meta_dir, 'ext_custom_rules.json')
        ext_custom_data = {
            'extension_rules': ext_rules,
            'custom_rules': custom_rules,
            'scan_root': scan_root,
            'scan_files': {
                'source': [os.path.relpath(f, scan_root) for f in all_source[:50]],
                'test': [os.path.relpath(f, scan_root) for f in test_files[:50]],
                'total_source': len(all_source),
                'total_test': len(test_files),
            }
        }
        with open(ext_custom_path, 'w', encoding='utf-8') as f:
            json.dump(ext_custom_data, f, ensure_ascii=False, indent=2)

        print(f"\n扩展/自定义规则扫描 (AI执行):", flush=True)
        print(f"| 规则ID | 类型 | 名称 | 严重级别 |", flush=True)
        print(f"|--------|------|------|---------|", flush=True)
        for r in ext_rules:
            print(f"| {r.get('id')} | 扩展 | {r.get('name')} | {r.get('severity')} |", flush=True)
        for r in custom_rules:
            print(f"| {r.get('id')} | 自定义 | {r.get('name')} | {r.get('severity')} |", flush=True)
        print(f"\n  规则配置已保存到: {ext_custom_path}", flush=True)
        print(f"  请AI读取该文件，根据规则描述扫描代码，发现问题后追加到报告。", flush=True)

    # 构建扫描元数据（供报告生成使用）
    scan_meta = {
        'version': VERSION,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'scan_root': scan_root,
        'active_rules': list(active_rule_ids),
        'rule_stats': {rid: rule_counts.get(rid, 0) for rid in active_rule_ids},
        'total_issues': len(original_issues_for_report),  # 使用原始数量
        'total_files': total_files,
        'workers': n_workers,
        'pr_mode': pr_mode,
    }

    if pr_mode and pr_info:
        scan_meta['pr_url'] = args.pr
        scan_meta['changed_files'] = len(pr_info.changed_files)
        scan_meta['dedup_removed'] = original_total - len(all_issues)  # 记录去重移除数量

    # Excel报告 - 使用原始问题（去重前的完整数据）
    excel_dir = scan_meta_dir
    actual_excel_path = generate_report(original_issues_for_report, excel_dir, active_rules, rule_counts)
    print(f"  Excel报告: {actual_excel_path}", flush=True)

    # HTML报告 - 使用原始问题（去重前的完整数据）
    html_path = generate_html_report(original_issues_for_report, excel_dir, active_rules, rule_counts, scan_meta, actual_excel_path)
    if html_path:
        print(f"  HTML报告: {html_path}", flush=True)

    # JSON中间结果 - 保存原始问题
    meta_path = os.path.join(scan_meta_dir, 'scan_meta.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(scan_meta, f, ensure_ascii=False, indent=2)

    issues_path = os.path.join(scan_meta_dir, 'all_issues.json')
    with open(issues_path, 'w', encoding='utf-8') as f:
        json.dump(original_issues_for_report, f, ensure_ascii=False, indent=2)  # 保存原始问题

    print(f"  元数据: {meta_path}", flush=True)
    print(f"  问题明细: {issues_path}", flush=True)
    print(f"  耗时: {time.time()-t3:.1f}s", flush=True)

    # 总结
    print(f"\n{'='*60}", flush=True)
    print(f"扫描完成", flush=True)
    print(f"{'='*60}", flush=True)
    total_time = time.time() - t1
    print(f"总耗时: {total_time:.1f}s", flush=True)
    if total_files > 0:
        print(f"扫描速度: {total_files/total_time:.1f} 文件/秒", flush=True)
    print(f"问题总数: {len(all_issues)}", flush=True)

    critical_count = sum(1 for i in all_issues if i.get('severity') == 'Critical')
    warning_count = sum(1 for i in all_issues if i.get('severity') == 'Warning')
    print(f"  Critical: {critical_count}", flush=True)
    print(f"  Warning: {warning_count}", flush=True)

    # PR模式摘要
    if pr_mode and pr_info:
        print(f"\nPR审查摘要:", flush=True)
        print(f"| 维度 | 状态 | 说明 |", flush=True)
        print(f"|------|------|------|", flush=True)
        print(f"| 变更文件数 | {len(pr_info.changed_files)} | {pr_info.owner}/{pr_info.repo} |", flush=True)
        high_risk = [rid for rid in ['R001', 'R003', 'R201'] if rule_counts.get(rid, 0) > 0]
        if high_risk:
            print(f"| 高风险规则命中 | {len(high_risk)} | {', '.join(high_risk)} |", flush=True)
        print(f"| 问题总计 | {len(all_issues)} | Critical: {critical_count}, Warning: {warning_count} |", flush=True)

        # --submit提示
        if not args.submit and len(all_issues) > 0:
            print(f"\n提示: 使用 --submit 可将扫描结果提交为PR检视评论", flush=True)
            print(f"  用法: python main.py --pr {args.pr} --level {args.level} --submit", flush=True)

        # --submit: 提交扫描结果到PR评论
        if args.submit:
            print(f"\n[提交] 准备提交PR评论...", flush=True)
            import subprocess
            submit_script = os.path.join(os.path.dirname(__file__), 'submit_pr_findings.py')
            if not os.path.exists(submit_script):
                print(f"  错误: 找不到 submit_pr_findings.py", file=sys.stderr)
                sys.exit(1)

            rules_info_path = os.path.join(scan_meta_dir, 'rules_info.json')
            rules_info_data = []
            for rid, rn, sev, _ in active_rules:
                rules_info_data.append({'rule': rid, 'name': rn, 'severity': sev})
            with open(rules_info_path, 'w', encoding='utf-8') as f:
                json.dump(rules_info_data, f, ensure_ascii=False, indent=2)

            # 保存原始问题用于示例展示
            original_issues_path = os.path.join(scan_meta_dir, 'original_issues_for_example.json')
            with open(original_issues_path, 'w', encoding='utf-8') as f:
                json.dump(original_issues_for_example, f, ensure_ascii=False, indent=2)

            cmd = [
                sys.executable, submit_script,
                '--pr', args.pr,
                '--issues', original_issues_path,
                '--rule-counts', meta_path,
                '--rules-info', rules_info_path,
                '--original-stats', json.dumps({
                    'critical': original_critical,
                    'warning': original_warning,
                    'total': original_total
                }),
                '--fixable-rules', json.dumps(sorted(FIXABLE_RULES)),
                '--mode', 'summary',
            ]
            if args.token:
                cmd.extend(['--token', args.token])
            if pr_info.diff_context:
                diff_context_path = os.path.join(scan_meta_dir, 'diff_context.json')
                diff_context_serializable = {}
                for path, ctx in pr_info.diff_context.items():
                    diff_context_serializable[path] = {
                        'new_added_lines': list(ctx.get('new_added_lines', [])) if isinstance(ctx.get('new_added_lines'), set) else ctx.get('new_added_lines', []),
                        'commentable_lines': ctx.get('commentable_lines', []),
                        'hunks': ctx.get('hunks', []),
                    }
                with open(diff_context_path, 'w', encoding='utf-8') as f:
                    json.dump(diff_context_serializable, f, ensure_ascii=False)
                cmd.extend(['--diff-context', diff_context_path])

            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                print(f"  提交失败: {proc.stderr.strip()}", file=sys.stderr)
                sys.exit(1)
            print(proc.stdout.strip())


if __name__ == '__main__':
    main()