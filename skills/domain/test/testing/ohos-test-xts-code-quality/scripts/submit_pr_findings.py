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
"""Submit XTS scan findings as GitCode PR comments.

v1.1 - Initial implementation

v1.2 - Added fixable_rules support for showing fixable indicator in PR comments

Supports three submission modes:
- summary: PR-level comment with scan statistics
- line: Diff-level comments for Critical issues on new lines
- full: Summary comment + line-level comments for Critical issues

Authentication: oh-gc CLI > --token > GITCODE_TOKEN env var
Adapted from review-gitcode-pr/scripts/prepare_review_submission.py

Usage:
    python submit_pr_findings.py --pr <URL> --issues issues.json [--mode full]
    python submit_pr_findings.py --pr <URL> --summary-only --body "summary text"
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys


def is_oh_gc_available():
    return shutil.which('oh-gc') is not None


def resolve_token(token=None):
    if token:
        return token, 'token'
    env_token = os.environ.get('GITCODE_TOKEN', '')
    if env_token:
        return env_token, 'token'
    return None, 'oh-gc' if is_oh_gc_available() else None


def parse_pr_url(pr_url):
    match = re.search(r"gitcode\.com/([^/]+)/([^/]+)/pull/(\d+)", pr_url)
    if not match:
        raise ValueError(f"Invalid GitCode PR URL: {pr_url}")
    return match.group(1), match.group(2), match.group(3)


def build_summary_comment(issues, pr_title, rule_counts=None, rules_info=None, original_stats=None, fixable_rules=None):
    """Build a PR-level summary comment with scan statistics and rule summary.
    
    Args:
        issues: 去重后的issue列表（用于提取示例）
        pr_title: PR标题
        rule_counts: 规则统计（原始数量，未去重）
        rules_info: 规则元信息
        original_stats: 原始扫描统计 {'critical': N, 'warning': M, 'total': K}
        fixable_rules: 可自动修复规则ID列表
    
    
    Shows:
    - Scan statistics (使用original_stats，去重前的数量)
    - Rules with issues (one line per rule + one example issue per rule)
    - Fixable indicator for each rule
    """
    stats = original_stats or {}
    total_orig = stats.get('total', len(issues))
    critical_orig = stats.get('critical', len([i for i in issues if i.get('severity') == 'Critical']))
    warning_orig = stats.get('warning', len([i for i in issues if i.get('severity') == 'Warning']))

    lines = [
        f"## XTS 代码质量扫描报告",
        f"",
        f"**PR**: {pr_title}",
        f"",
        f"### 扫描统计",
        f"",
        f"| 严重级别 | 问题数量 |",
        f"|----------|----------|",
        f"| Critical | {critical_orig} |",
        f"| Warning | {warning_orig} |",
        f"| **总计** | **{total_orig}** |",
        f"",
    ]

    if rule_counts:
        rules_with_issues = {rid: count for rid, count in rule_counts.items() if count > 0}
        if rules_with_issues:
            lines.append(f"### 问题规则统计")
            lines.append("")
            lines.append("| 规则编号 | 问题数量 | 可自动修复 |")
            lines.append("|----------|----------|-----------|")
            
            fixable_set = set(fixable_rules or [])
            for rid, count in sorted(rules_with_issues.items(), key=lambda x: (-x[1], x[0])):
                fixable_mark = "Yes" if rid in fixable_set else "No"
                lines.append(f"| {rid} | {count} | {fixable_mark} |")
            lines.append("")
            
            rule_issues = {}
            for i in issues:
                rid = i.get('rule', '')
                if rid in rules_with_issues and rid not in rule_issues:
                    rule_issues[rid] = i
            
            if rule_issues:
                lines.append(f"### 问题示例（每规则一个案例）")
                lines.append("")
                for rid in sorted(rule_issues.keys()):
                    example = rule_issues[rid]
                    file_path = example.get('file', '')
                    line_num = example.get('line', 0)
                    issue_type = example.get('type', '')
                    snippet = example.get('snippet', '')
                    suggestion = example.get('suggestion', '')
                    
                    fixable_mark = "Yes" if rid in fixable_set else "No"
                    
                    lines.append(f"**{rid}** `{file_path}:{line_num}` {issue_type} `[可自动修复: {fixable_mark}]`")
                    if snippet:
                        lines.append(f"```")
                        lines.append(snippet.strip())
                        lines.append(f"```")
                    lines.append("")
                    if suggestion:
                        lines.append(f"> {suggestion}")
                    if fixable_mark == "Yes":
                        lines.append(f"> 可使用 `--fix` 自动修复或参考修复指南")
                    lines.append("")
            
            lines.append(f"> 更多问题详情请使用 `ohos-test-xts-code-quality` Skill 执行完整扫描，查看HTML报告。")
            lines.append("")

    lines.append("---")
    lines.append("*由 XTS 代码质量检查工具自动生成*")

    return '\n'.join(lines)


def build_line_comments(issues, diff_context=None):
    """Build diff-level comments for issues on new/changed lines.

    Only includes Critical issues that fall within diff hunks.
    """
    comments = []

    for issue in issues:
        if issue.get('severity') != 'Critical':
            continue

        file_path = issue.get('file', '')
        line = issue.get('line', 0)

        if diff_context:
            ctx = diff_context.get(file_path)
            if ctx and ctx.get('commentable_lines'):
                if line not in ctx['commentable_lines']:
                    continue

        body = (
            f"**{issue.get('rule', '')}** {issue.get('type', '')}\n\n"
        )
        if issue.get('snippet'):
            body += f"```\n{issue['snippet']}\n```\n\n"
        if issue.get('suggestion'):
            body += f"修复建议: {issue['suggestion']}\n"
        body += "\n---\n*由 XTS 代码质量检查工具自动生成*"

        comments.append({
            'path': file_path,
            'line': line,
            'body': body,
        })

    return comments


def preview_comments(summary_body, line_comments):
    """Print preview of comments to be submitted."""
    print(f"\n[预览] 将提交以下评论:", flush=True)
    print(f"  PR摘要评论: 1 条 ({len(summary_body)} 字符)", flush=True)
    print(f"  行级评论: {len(line_comments)} 条", flush=True)
    print(f"  总计: {1 + len(line_comments)} 条评论", flush=True)

    if line_comments:
        print(f"\n  行级评论预览:", flush=True)
        for c in line_comments[:5]:
            print(f"    {c['path']}:{c['line']} - {c['body'][:60]}...", flush=True)
        if len(line_comments) > 5:
            print(f"    ... 还有 {len(line_comments) - 5} 条", flush=True)


def execute_via_oh_gc(owner, repo, pr_id, summary_body, line_comments, dry_run=False):
    """Submit comments using oh-gc CLI."""
    repo_arg = f"{owner}/{repo}"
    results = []
    commands = []

    commands.append(['oh-gc', 'pr:comment', str(pr_id), '--body', summary_body, '--repo', repo_arg])

    for c in line_comments:
        commands.append([
            'oh-gc', 'pr:comment', str(pr_id),
            '--body', c['body'],
            '--path', c['path'],
            '--line', str(c['line']),
            '--repo', repo_arg,
        ])

    for cmd in commands:
        cmd_display = cmd[:5] + [f"...({len(cmd[5])} chars)"] if len(cmd) > 5 and '--body' in cmd else cmd
        if dry_run:
            print(f"  [dry-run] {' '.join(cmd_display)}", flush=True)
            results.append({'command': cmd, 'exit_code': 0, 'dry_run': True})
            continue

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        result = {
            'command': cmd_display,
            'exit_code': proc.returncode,
            'stdout': proc.stdout.strip()[:200],
            'stderr': proc.stderr.strip()[:200],
        }
        results.append(result)

        if proc.returncode != 0:
            print(f"  [失败] {' '.join(cmd_display)}", file=sys.stderr, flush=True)
            print(f"  stderr: {proc.stderr.strip()[:200]}", file=sys.stderr, flush=True)
            break
        else:
            print(f"  [成功] {' '.join(cmd_display)}", flush=True)

    return results


def execute_via_api(token, owner, repo, pr_id, summary_body, line_comments, dry_run=False):
    """Submit comments using GitCode REST API."""
    base_url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{pr_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    results = []

    if dry_run:
        print(f"  [dry-run] POST {base_url}/comments (summary)", flush=True)
        for c in line_comments:
            print(f"  [dry-run] POST {base_url}/comments ({c['path']}:{c['line']})", flush=True)
        return results

    try:
        import requests
        HAS_REQUESTS = True
    except ImportError:
        HAS_REQUESTS = False

    def _post(url, data):
        if HAS_REQUESTS:
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            return resp.json()
        else:
            import urllib.request
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))

    comment_url = f"{base_url}/comments"

    result = _post(comment_url, {"body": summary_body})
    results.append({'type': 'summary', 'status': 'ok'})
    print(f"  [成功] 提交PR摘要评论", flush=True)

    for c in line_comments:
        try:
            data = {
                "body": c['body'],
                "path": c['path'],
                "line": c['line'],
            }
            _post(comment_url, data)
            results.append({'type': 'line', 'path': c['path'], 'line': c['line'], 'status': 'ok'})
            print(f"  [成功] 提交行级评论 {c['path']}:{c['line']}", flush=True)
        except Exception as e:
            results.append({'type': 'line', 'path': c['path'], 'line': c['line'], 'status': 'error', 'error': str(e)})
            print(f"  [失败] 行级评论 {c['path']}:{c['line']}: {e}", file=sys.stderr, flush=True)

    return results


def main():
    parser = argparse.ArgumentParser(description='Submit XTS scan findings as PR comments')
    parser.add_argument('--pr', required=True, help='GitCode PR URL')
    parser.add_argument('--token', default=None, help='GitCode PAT (auto-detects oh-gc)')
    parser.add_argument('--issues', help='Path to JSON file with scan issues list')
    parser.add_argument('--rule-counts', help='Path to JSON file with rule counts dict')
    parser.add_argument('--rules-info', help='Path to JSON file with rules metadata')
    parser.add_argument('--original-stats', help='JSON string with original stats: {"critical":N,"warning":M,"total":K}')
    parser.add_argument('--diff-context', help='Path to JSON file with diff context')
    parser.add_argument('--mode', choices=['summary', 'line', 'full'], default='summary',
                        help='Submission mode (default: summary)')
    parser.add_argument('--summary-only', action='store_true',
                        help='Submit only a pre-built summary text (use with --body)')
    parser.add_argument('--body', help='Pre-built summary text (use with --summary-only)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview comments without actually submitting')
    parser.add_argument('--fixable-rules', help='JSON string with fixable rule IDs: ["R008","R012",...]')
    args = parser.parse_args()

    fixable_rules = []
    if args.fixable_rules:
        try:
            fixable_rules = json.loads(args.fixable_rules)
        except json.JSONDecodeError:
            pass

    owner, repo, pr_id = parse_pr_url(args.pr)
    token, auth_method = resolve_token(args.token)

    if not token and auth_method != 'oh-gc':
        print("  错误: 无可用认证方式。请选择以下任一方式：", file=sys.stderr, flush=True)
        print("    1) 安装 oh-gc CLI: npm install -g @oh-gc-cli  然后  oh-gc auth:login", file=sys.stderr, flush=True)
        print("    2) 命令行参数: --token <YOUR_TOKEN>", file=sys.stderr, flush=True)
        print("    3) 环境变量: export GITCODE_TOKEN=<YOUR_TOKEN>", file=sys.stderr, flush=True)
        sys.exit(1)

    print(f"[提交] PR: {owner}/{repo}#{pr_id}, 认证: {auth_method}, 模式: {args.mode}", flush=True)

    issues = []
    if args.issues:
        with open(args.issues, 'r', encoding='utf-8') as f:
            issues = json.load(f)
    elif not args.summary_only:
        print("  错误: 需要 --issues 或 --summary-only 参数", file=sys.stderr)
        sys.exit(1)

    rule_counts = {}
    if args.rule_counts:
        with open(args.rule_counts, 'r', encoding='utf-8') as f:
            raw_counts = json.load(f)
        if isinstance(raw_counts, dict):
            if 'rule_stats' in raw_counts:
                rule_counts = raw_counts['rule_stats']
            else:
                rule_counts = raw_counts

    rules_info = []
    if args.rules_info and os.path.exists(args.rules_info):
        with open(args.rules_info, 'r', encoding='utf-8') as f:
            rules_info = json.load(f)

    diff_context = {}
    if args.diff_context:
        with open(args.diff_context, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            for path, ctx in raw.items():
                new_added = set(ctx.get('new_added_lines', []))
                commentable = ctx.get('commentable_lines', [])
                hunks = ctx.get('hunks', [])
                diff_context[path] = {
                    'new_added_lines': new_added,
                    'commentable_lines': commentable,
                    'hunks': hunks,
                }

    original_stats = {}
    if args.original_stats:
        try:
            original_stats = json.loads(args.original_stats)
        except json.JSONDecodeError:
            pass

    if args.summary_only:
        summary_body = args.body or ''
    else:
        pr_title = f"{owner}/{repo}#{pr_id}"
        summary_body = build_summary_comment(issues, pr_title, rule_counts, rules_info, original_stats, fixable_rules)

    line_comments = []
    if args.mode in ('line', 'full') and not args.summary_only:
        line_comments = build_line_comments(issues, diff_context)

    preview_comments(summary_body, line_comments)

    if args.dry_run:
        print(f"\n[dry-run] 未实际提交评论", flush=True)
        return

    print(f"\n[执行] 提交评论...", flush=True)
    if auth_method == 'oh-gc':
        results = execute_via_oh_gc(owner, repo, pr_id, summary_body, line_comments)
    else:
        results = execute_via_api(token, owner, repo, pr_id, summary_body, line_comments)

    success_count = sum(1 for r in results if r.get('status') == 'ok' or r.get('exit_code') == 0)
    fail_count = len(results) - success_count

    print(f"\n[结果] 成功: {success_count}, 失败: {fail_count}, 总计: {len(results)}", flush=True)

    if fail_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
