#!/usr/bin/env python3
"""Parse OpenHarmony api_diff results into the standard uncovered_apis.json.

This script powers **Flow D (API change-driven mode)** of the main skill. It has
two input paths and always produces the canonical `uncovered_apis_<ts>.json`
layout that Phase 3 / Phase 4 consume, with an extra `change_info` block per API.

Input paths
-----------
1. User-provided diff report (recommended, zero environment deps):
       python parse_api_diff.py --diff-report /path/to/diff(old_new).json
2. Built-in invocation of the api_diff tool (needs OH_ROOT + node):
       python parse_api_diff.py --old /path/to/old_sdk --new /path/to/new_sdk
3. By PR merge commit (needs OH_ROOT, auto-exports base/head api/ via git worktree):
       python parse_api_diff.py --pr '!34064'      # PR number
       python parse_api_diff.py --pr af59f9f4c      # or merge commit hash
4. By two tags (needs OH_ROOT, auto-exports both api/ via git worktree):
       python parse_api_diff.py --tag OpenHarmony-v5.1.0-Release,OpenHarmony-v6.0-Release

The api_diff tool (interface/sdk-js/build-tools/api_diff) scans `{old,new}/api/*.d.ts`
and `{old,new}/component/*.d.ts`, then writes a SINGLE JSON file
`diff({oldVersion}_{newVersion}).json` containing an array of change records.

Paths 2/3/4 require OH_ROOT (the OpenHarmony source root) configured in
.oh-xts-config.json; the git repo is assumed at {OH_ROOT}/interface/sdk-js.

Filtering (optional): --subsystem / --kit / --dts-file, mirroring extract_uncovered.py.

Output
------
Writes `.coverage_data/iter-{N}/uncovered_apis_<timestamp>.json` and prints the
path as the last line so callers can capture it.

Each API entry carries:
    {
      "module": ..., "class": ..., "method": ..., "type": ..., "func": ...,
      "kit": ..., "file_path": ..., "subsystem": ..., "error_codes": ...,
      "coverage": { ...standard 8-dim, all 未覆盖... },
      "change_info": {
          "statusCode": 7,
          "change_type": "ERRORCODE_CHANGES",
          "risk_level": "MEDIUM",
          "status_text": "...",
          "old_message": "...", "new_message": "...",
          "raw_text": "...",
          "incremental": { ...computed delta for Phase 4... }
      }
    }
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(SCRIPT_DIR, '..')

# ---------------------------------------------------------------------------
# statusCode classification (authoritative source: interface/sdk-js api_diff
# ApiStatusCode enum). Mapped to risk level + change_type label used downstream.
# ---------------------------------------------------------------------------
STATUS_MAP = {
    0:  ('API_DELETE', 'HIGH'),
    1:  ('DTS_DELETE', 'HIGH'),
    2:  ('CLASS_DELETE', 'HIGH'),
    3:  ('NEW_API', 'LOW'),
    4:  ('VERSION_CHANGES', 'LOW'),
    5:  ('DEPRECATE_CHANGES', 'LOW'),
    6:  ('NEW_ERRORCODE', 'MEDIUM'),
    7:  ('ERRORCODE_CHANGES', 'MEDIUM'),
    8:  ('SYSCAP_CHANGES', 'LOW'),
    9:  ('ACCESS_LEVEL_CHANGES', 'LOW'),
    10: ('PERMISSION_CHANGES', 'MEDIUM'),
    11: ('NEW_PERMISSION', 'MEDIUM'),
    12: ('DELETE_PERMISSION', 'MEDIUM'),
    13: ('TYPE_CHANGES', 'LOW'),
    14: ('FUNCTION_TYPE_CHANGES', 'HIGH'),
    15: ('CLASS_CHANGES', 'HIGH'),
    16: ('FUNCTION_CHANGES', 'HIGH'),
    18: ('HISTORICAL_NO_CHANGE', 'LOW'),
    19: ('TYPE_DECLARE_CHANGES', 'LOW'),
    20: ('TYPE_RELATION_CHANGES', 'LOW'),
    21: ('NEW_DTS', 'LOW'),
    22: ('NEW_CLASS', 'LOW'),
}

# StatusCodes that are pure increments and behave like Flow C (new API).
NEW_API_CODES = {3, 21, 22}
# StatusCodes for which no test should be generated (API is gone).
DELETE_CODES = {0, 1, 2}

PERMISSION_RE = re.compile(r'ohos\.permission\.[A-Za-z0-9_]+')
# Business error codes: 6-9 digit numeric tokens (e.g. 17000099, 401, 201, 801).
ERRORCODE_RE = re.compile(r'\b(?:\d{3}|\d{6,})\b')
# Type union members: split "string | number" -> {"string", "number"}.
TYPE_UNION_SPLIT_RE = re.compile(r'\s*\|\s*')


def load_config():
    cfg_path = os.path.join(SKILL_ROOT, '.oh-xts-config.json')
    if not os.path.exists(cfg_path):
        cfg_path = os.path.join(SKILL_ROOT, '.oh-xts-config.example.json')
    oh_root = None
    ets_versions = ['ets1.1']
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as fp:
                cfg = json.load(fp)
            oh_root = cfg.get('OH_ROOT') or cfg.get('oh_root')
            ev = cfg.get('ets_version')
            if isinstance(ev, list) and ev:
                ets_versions = ev
        except Exception:
            pass
    return oh_root, ets_versions


# ---------------------------------------------------------------------------
# Git-based export (paths 3/4: --pr / --tag)
# ---------------------------------------------------------------------------
HEX_RE = re.compile(r'^[0-9a-f]{7,40}$', re.IGNORECASE)


def resolve_git_repo_root(oh_root):
    """Locate the interface/sdk-js git repo under OH_ROOT."""
    if not oh_root:
        sys.exit('[parse_api_diff] OH_ROOT not configured; required for --pr/--tag/--old.')
    repo = os.path.join(oh_root, 'interface', 'sdk-js')
    if not os.path.isdir(repo):
        sys.exit(f'[parse_api_diff] SDK repo not found: {repo}')
    # Verify it is a git worktree.
    try:
        subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'],
                                cwd=repo, stderr=subprocess.DEVNULL)
    except Exception:
        sys.exit(f'[parse_api_diff] {repo} is not a git worktree; '
                 f'--pr/--tag need the full OpenHarmony source tree')
    return repo


def resolve_pr_to_merge_commit(repo_root, pr):
    """Accept a merge commit hash or a PR number (e.g. '34064' or '!34064')."""
    pr = pr.lstrip('!')
    if HEX_RE.match(pr):
        return pr  # already a commit hash
    # Search merge commits whose message contains "!{pr}".
    out = subprocess.check_output(
        ['git', 'log', '--all', '--merges', '-1', '--format=%H', f'--grep=!{pr}'],
        cwd=repo_root, stderr=subprocess.DEVNULL).decode().strip()
    if not out:
        sys.exit(f'[parse_api_diff] PR !{pr} not found among merge commits in {repo_root}')
    return out


def export_ref_to_sdk_dir(repo_root, ref, sdk_dir):
    """Checkout `ref` into a temp worktree, copy its api/ into sdk_dir, remove worktree.

    The api_diff tool scans {sdk_dir}/api/*.d.ts and {sdk_dir}/component/*.d.ts
    (see util.js listApiDeclarationFiles), so we only need the api/ subtree.
    """
    wt = tempfile.mkdtemp(prefix='apidiff_wt_')
    try:
        subprocess.check_call(
            ['git', 'worktree', 'add', '--detach', wt, ref],
            cwd=repo_root, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        api_src = os.path.join(wt, 'api')
        api_dst = os.path.join(sdk_dir, 'api')
        if os.path.isdir(api_src):
            shutil.copytree(api_src, api_dst)
        else:
            print(f'[parse_api_diff] WARNING: no api/ dir in ref {ref}; produced empty SDK')
            os.makedirs(api_dst, exist_ok=True)
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode() if e.stderr else str(e)
        sys.exit(f'[parse_api_diff] failed to export ref {ref}: {err.strip()}')
    finally:
        subprocess.call(['git', 'worktree', 'remove', wt, '--force'],
                        cwd=repo_root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ---------------------------------------------------------------------------
# Built-in api_diff invocation (path 2)
# ---------------------------------------------------------------------------
def run_api_diff_tool(old_dir, new_dir, old_version, new_version, oh_root, output_dir):
    """Invoke interface/sdk-js api_diff and return the produced JSON path."""
    if not oh_root:
        sys.exit('[parse_api_diff] OH_ROOT not configured; provide --diff-report instead, '
                 'or set OH_ROOT in .oh-xts-config.json')

    api_diff_root = os.path.join(oh_root, 'interface', 'sdk-js', 'build-tools', 'api_diff')
    entry = os.path.join(api_diff_root, 'src', 'entry', 'main.js')
    if not os.path.exists(entry):
        sys.exit(f'[parse_api_diff] api_diff entry not found: {entry}')

    # Ensure node_modules present (npm install once).
    node_modules = os.path.join(api_diff_root, 'node_modules')
    if not os.path.isdir(node_modules):
        print('[parse_api_diff] installing api_diff npm deps (one time)...')
        subprocess.check_call(['npm', 'install'], cwd=api_diff_root,
                              stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        'node', entry, 'diff',
        '--old', old_dir,
        '--new', new_dir,
        '--oldVersion', old_version or 'old',
        '--newVersion', new_version or 'new',
        '--output', output_dir,
        '--format', 'json',
    ]
    print('[parse_api_diff] running api_diff tool...')
    subprocess.check_call(cmd, cwd=api_diff_root)

    # The tool writes a SINGLE file: diff({oldVersion}_{newVersion}).json
    # (see api_writer.js JSONReporter.write). Resolve its absolute path.
    expected = os.path.join(output_dir, f'diff({old_version or "old"}_{new_version or "new"}).json')
    if os.path.exists(expected):
        return [expected]
    # Fallback: locate any diff(*_).json the tool produced.
    produced = sorted(
        os.path.join(output_dir, f) for f in os.listdir(output_dir)
        if f.startswith('diff(') and f.endswith('.json')
    )
    if not produced:
        sys.exit(f'[parse_api_diff] api_diff produced no JSON in {output_dir}')
    return produced[:1]


def load_diff_entries(json_paths):
    """Load and normalize api_diff JSON into a flat list of change dicts."""
    raw = []
    for jp in json_paths:
        with open(jp, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        raw.extend(_coerce_to_list(data))
    return raw


def load_diff_report(report_path):
    """Load a user-provided diff report file (JSON)."""
    if not os.path.exists(report_path):
        sys.exit(f'[parse_api_diff] diff report not found: {report_path}')
    with open(report_path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return _coerce_to_list(data)


def _coerce_to_list(data):
    """Accept array, single object, or object with a known wrapper key."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if 'statusCode' in data or 'rawText' in data:
            return [data]
        for key in ('diffs', 'apiDiffs', 'changes', 'apiChanges', 'data', 'results'):
            if key in data and isinstance(data[key], list):
                return data[key]
        # last resort: any list value
        for v in data.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
    return []


# ---------------------------------------------------------------------------
# Diff entry -> standard API entry with change_info
# ---------------------------------------------------------------------------
def extract_method_name(raw_text):
    if not raw_text:
        return ''
    # property "foo: Type" vs method "foo(a: T): R" vs function decl "function foo(...)"
    m = re.match(r'(?:static\s+|readonly\s+|get\s+|set\s+|function\s+|export\s+)*([\w$]+)\s*[:(]?', raw_text.strip())
    return m.group(1) if m else ''


def extract_param_types(message):
    """Return the set of TS types referenced in a signature message."""
    if not message:
        return set()
    # Grab the param block between the first '(' and its matching ')'.
    start = message.find('(')
    types = set()
    if start != -1:
        depth = 0
        end = -1
        for i, ch in enumerate(message[start:], start):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        block = message[start + 1:end] if end != -1 else message[start + 1:]
        # "name: Type, name2: Type2" -> take the type part of each param.
        for seg in block.split(','):
            if ':' in seg:
                t = seg.split(':', 1)[1].strip()
                for part in TYPE_UNION_SPLIT_RE.split(t):
                    part = part.strip().rstrip('?').strip()
                    if part and part not in ('', ','):
                        types.add(part)
    return types


def compute_incremental(status_code, old_msg, new_msg):
    """Compute the actionable delta Phase 4 consumes directly."""
    inc = {}
    if status_code in (6, 7):  # new / changed error codes
        old_codes = set(ERRORCODE_RE.findall(old_msg or ''))
        new_codes = set(ERRORCODE_RE.findall(new_msg or ''))
        inc['new_error_codes'] = sorted(c for c in (new_codes - old_codes))
        inc['removed_error_codes'] = sorted(c for c in (old_codes - new_codes))
    elif status_code in (11, 12, 10):  # permission add/delete/change
        old_perm = set(PERMISSION_RE.findall(old_msg or ''))
        new_perm = set(PERMISSION_RE.findall(new_msg or ''))
        inc['new_permissions'] = sorted(new_perm - old_perm)
        inc['removed_permissions'] = sorted(old_perm - new_perm)
    elif status_code == 16:  # function signature change
        old_types = extract_param_types(old_msg)
        new_types = extract_param_types(new_msg)
        inc['new_param_types'] = sorted(new_types - old_types)
        inc['removed_param_types'] = sorted(old_types - new_types)
    return inc


def build_api_entry(diff, ets_version, subsystem=''):
    """Convert one api_diff change into a standard uncovered_apis entry."""
    status_code = int(diff.get('statusCode', -1))
    change_type, risk = STATUS_MAP.get(status_code, ('UNKNOWN', 'MEDIUM'))
    class_name = diff.get('className') or ''
    raw_text = diff.get('rawText') or diff.get('newMessage') or ''
    method_name = extract_method_name(raw_text)
    package = diff.get('packageName') or ''
    dts_name = diff.get('dtsName') or ''
    dts_path = diff.get('dtsPath') or ('api/' + dts_name if dts_name else '')
    old_msg = diff.get('oldMessage') or ''
    new_msg = diff.get('newMessage') or ''
    # The api_diff tool leaves newMessage empty for NEW_API and oldMessage empty
    # for DELETE; the signature lives in rawText. Backfill so downstream always
    # has the full before/after text.
    if not new_msg and status_code in NEW_API_CODES:
        new_msg = raw_text
    if not old_msg and status_code in DELETE_CODES:
        old_msg = raw_text
    syscap = diff.get('syscap') or ''

    incremental = compute_incremental(status_code, old_msg, new_msg)

    # error_codes aggregated from the new message for convenience.
    err_str = ''
    if new_msg:
        codes = ERRORCODE_RE.findall(new_msg)
        if codes:
            err_str = ','.join(codes)

    type_field = 'Method'
    if change_type in ('CLASS_CHANGES', 'NEW_CLASS', 'CLASS_DELETE'):
        type_field = 'Class'
    elif change_type in ('NEW_API',) and not method_name:
        type_field = 'Property'

    entry = {
        'module': package,
        'class': class_name,
        'method': method_name,
        'type': type_field,
        'func': new_msg or raw_text,
        'kit': syscap,
        'file_path': dts_path.replace('\\', '/'),
        'subsystem': subsystem,
        'error_codes': err_str,
        'start_version': '',
        'stage_label': '',
        'interface_covered_status': '否',
        'coverage': _default_coverage(status_code),
        'change_info': {
            'statusCode': status_code,
            'change_type': change_type,
            'risk_level': risk,
            'status_text': diff.get('status') or '',
            'old_message': old_msg,
            'new_message': new_msg,
            'raw_text': raw_text,
            'incremental': incremental,
        },
    }
    return entry


def _default_coverage(status_code):
    """For delete codes nothing needs generating; otherwise mark relevant dims."""
    if status_code in DELETE_CODES:
        return {'call': {'status': '已覆盖', 'note': 'API deleted, no test to generate'}}
    cov = {
        'call': {'status': '未覆盖'},
        'param': {'status': '未覆盖'},
        'return_value': {'status': '未覆盖'},
    }
    if status_code in (6, 7):
        cov['error_code'] = {'status': '未覆盖', 'err_desc': '新增/变更错误码分支'}
    if status_code in (10, 11, 12):
        cov['permission'] = {'status': '未覆盖', 'err_desc': '权限路径变更'}
    return cov


# ---------------------------------------------------------------------------
# Rename detection (pair DELETE + NEW_API by class + signature)
# ---------------------------------------------------------------------------
SIG_RE = re.compile(r'\(.*\).*;')


def signature_fingerprint(raw_text):
    """Strip the method name, keep only params + return type as a fingerprint.

    'isBefore(com: Component): On;'  -> '(com: Component): On;'
    Used to pair renamed APIs (old name deleted + new name added with same sig).
    """
    if not raw_text:
        return ''
    m = SIG_RE.search(raw_text)
    return m.group(0).strip() if m else raw_text.strip()


def detect_renames(entries):
    """Pair DELETE(0) and NEW_API(3) entries that share (class, signature).

    A rename is identified when, within the same class, K deletions and K
    additions share the exact same param/return signature. Such pairs are
    re-tagged change_type='API_RENAME' so Phase 4 can treat them as "migrate
    old test by renaming" instead of "delete + generate from scratch".

    Mutates entries in place; returns (rename_count, true_delete, true_new).
    """
    from collections import defaultdict
    groups = defaultdict(lambda: {'del': [], 'new': []})
    for e in entries:
        ci = e.get('change_info', {})
        if ci.get('statusCode') in DELETE_CODES:
            key = (e.get('class', ''), signature_fingerprint(ci.get('raw_text', '')))
            if key[1]:
                groups[key]['del'].append(e)
        elif ci.get('statusCode') in NEW_API_CODES:
            key = (e.get('class', ''), signature_fingerprint(ci.get('raw_text', '')))
            if key[1]:
                groups[key]['new'].append(e)

    rename_count = 0
    for (cls, signature), g in groups.items():
        nd, nn = len(g['del']), len(g['new'])
        if nd == 0 or nn == 0:
            continue
        paired = min(nd, nn)
        rename_count += paired
        old_names = [_short_name(e['change_info']['raw_text']) for e in g['del']]
        new_names = [_short_name(e['change_info']['raw_text']) for e in g['new']]
        # Re-tag every entry in this group (both old & new) as RENAME.
        for e in g['del'] + g['new']:
            ci = e['change_info']
            ci['change_type'] = 'API_RENAME'
            ci['risk_level'] = 'MEDIUM'  # rename is less severe than delete/new
            ci['rename_info'] = {
                'is_rename': True,
                'old_names': old_names,
                'new_names': new_names,
                'signature': signature,
                'class': cls,
                'migrate_hint': (f'API 改名（参数逻辑不变）：'
                                 f'{",".join(old_names)} → {",".join(new_names)}，'
                                 f'现有用例可改方法名迁移'),
            }
            # Mark old-name entries as not-generating (like delete), keep new-name
            # entries generatable so Phase 5 produces the renamed test.
            if ci['statusCode'] in DELETE_CODES:
                e['coverage'] = {'call': {'status': '已覆盖',
                                          'note': f'改名前的旧方法名，新名见 rename_info.new_names'}}
    return rename_count


def _short_name(raw_text):
    """'export function isBefore(com: Component): On;' -> 'isBefore'."""
    m = re.match(r'(?:export\s+)?(?:function\s+)?([\w$]+)\s*\(', raw_text.strip())
    return m.group(1) if m else raw_text.strip()


# ---------------------------------------------------------------------------
# Filtering & assembly
# ---------------------------------------------------------------------------
def passes_filter(entry, subsystem, kit, dts_file):
    fp = entry.get('file_path', '')
    if dts_file and dts_file.replace('\\', '/') not in fp.replace('\\', '/'):
        return False
    if kit and entry.get('kit', '') != kit:
        return False
    if subsystem and entry.get('subsystem', '') != subsystem:
        return False
    return True


def build_output(diffs, ets_versions, subsystem, kit, dts_file, iter_phase, task_dir):
    version_data = {ver: {'methods': [], 'interfaces': [], 'properties': []} for ver in ets_versions}
    # api_diff is version-agnostic; place entries under the primary ets version.
    primary = ets_versions[0]

    kept = 0
    skipped_delete = 0
    built_entries = []
    for d in diffs:
        entry = build_api_entry(d, primary, subsystem or '')
        if not passes_filter(entry, subsystem, kit, dts_file):
            continue
        built_entries.append(entry)

    # Rename detection: pair DELETE + NEW_API by (class, signature) so Phase 4
    # can recommend "migrate old test by renaming" instead of "delete + regen".
    rename_count = detect_renames(built_entries)
    if rename_count:
        print(f'[parse_api_diff] detected {rename_count} API rename(s) (DELETE+NEW paired by signature)')

    for entry in built_entries:
        kept += 1
        if entry['change_info']['statusCode'] in DELETE_CODES \
                and entry['change_info'].get('change_type') != 'API_RENAME':
            skipped_delete += 1
        t = entry['type']
        if t == 'Class':
            version_data[primary]['interfaces'].append(entry)
        elif t == 'Property':
            version_data[primary]['properties'].append(entry)
        else:
            version_data[primary]['methods'].append(entry)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_dir = os.path.join(task_dir, f'iter-{iter_phase}')
    os.makedirs(output_dir, exist_ok=True)

    out = {}
    for ver in ets_versions:
        vd = version_data.get(ver, {'methods': [], 'interfaces': [], 'properties': []})
        if vd['methods'] or vd['interfaces'] or vd['properties']:
            out[ver] = vd
    out['metadata'] = {
        'ets_versions': ets_versions,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'api_diff (Flow D)',
        'summary': {
            ver: {
                'methods': len(version_data[ver]['methods']),
                'interfaces': len(version_data[ver]['interfaces']),
                'properties': len(version_data[ver]['properties']),
            } for ver in ets_versions
        },
    }

    out_path = os.path.join(output_dir, f'uncovered_apis_{timestamp}.json')
    with open(out_path, 'w', encoding='utf-8') as fp:
        json.dump(out, fp, indent=2, ensure_ascii=False)

    print('[parse_api_diff] === SUMMARY ===')
    print(f'[parse_api_diff] diff entries kept (after filter): {kept}')
    print(f'[parse_api_diff]   - delete (report only, no test): {skipped_delete}')
    by_type = {}
    for ver in ets_versions:
        for e in version_data[ver]['methods'] + version_data[ver]['interfaces'] + version_data[ver]['properties']:
            ct = e['change_info']['change_type']
            by_type[ct] = by_type.get(ct, 0) + 1
    for ct, n in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f'[parse_api_diff]   - {ct}: {n}')
    print(f'[parse_api_diff] output: {out_path}')
    print(out_path)
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description='Parse api_diff results into standard uncovered_apis.json (Flow D). '
                    'Input can be: a diff report (--diff-report), two SDK dirs (--old/--new), '
                    'a PR (--pr), or two tags (--tag old,new).')
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--diff-report', type=str, help='Path to a user-provided api_diff JSON report')
    src.add_argument('--old', type=str, help='Old SDK dir (built-in api_diff path)')
    src.add_argument('--pr', type=str,
                     help='PR merge commit hash or PR number (e.g. 34064 / !34064). '
                          'Auto-exports base(PR^1)/head(PR) api/ via git worktree.')
    src.add_argument('--tag', type=str,
                     help='Two tags comma-separated, e.g. TagA,TagB. '
                          'Auto-exports each tag\'s api/ via git worktree.')
    parser.add_argument('--new', type=str, help='New SDK dir (built-in api_diff path, use with --old)')
    parser.add_argument('--old-version', type=str, default='old')
    parser.add_argument('--new-version', type=str, default='new')
    parser.add_argument('--subsystem', type=str, default=None)
    parser.add_argument('--kit', type=str, default=None)
    parser.add_argument('--dts-file', type=str, default=None, help='Filter by d.ts file (partial match)')
    parser.add_argument('--iter-phase', type=int, default=1)
    parser.add_argument('--task-subsystem', type=str, default=None)
    parser.add_argument('--task-module', type=str, default=None)
    parser.add_argument('--session-id', type=str, default=None)
    args = parser.parse_args()

    oh_root, ets_versions = load_config()
    tmp_root = os.path.join(SKILL_ROOT, '.coverage_data', '_api_diff_tmp')

    # Resolve input diffs via one of four paths.
    if args.diff_report:
        diffs = load_diff_report(args.diff_report)
        print(f'[parse_api_diff] loaded {len(diffs)} change(s) from report: {args.diff_report}')
    elif args.old:
        if not args.new:
            parser.error('--new is required when using --old')
        tmp_out = os.path.join(tmp_root, 'manual')
        json_paths = run_api_diff_tool(args.old, args.new, args.old_version, args.new_version,
                                       oh_root, tmp_out)
        diffs = load_diff_entries(json_paths)
        print(f'[parse_api_diff] api_diff produced {len(diffs)} change(s)')
    elif args.pr:
        repo_root = resolve_git_repo_root(oh_root)
        merge_commit = resolve_pr_to_merge_commit(repo_root, args.pr)
        old_ver, new_ver = f'base@{merge_commit[:8]}', f'PR{args.pr.lstrip("!")}'
        old_sdk = os.path.join(tmp_root, 'pr_old'); new_sdk = os.path.join(tmp_root, 'pr_new')
        shutil.rmtree(tmp_root, ignore_errors=True)
        print(f'[parse_api_diff] --pr {args.pr} -> merge commit {merge_commit[:12]}')
        export_ref_to_sdk_dir(repo_root, f'{merge_commit}^1', old_sdk)  # base before merge
        export_ref_to_sdk_dir(repo_root, merge_commit, new_sdk)         # head at merge
        tmp_out = os.path.join(tmp_root, 'out')
        json_paths = run_api_diff_tool(old_sdk, new_sdk, old_ver, new_ver, oh_root, tmp_out)
        diffs = load_diff_entries(json_paths)
        print(f'[parse_api_diff] PR diff produced {len(diffs)} change(s)')
    elif args.tag:
        tags = [t.strip() for t in args.tag.split(',') if t.strip()]
        if len(tags) != 2:
            parser.error('--tag requires exactly two tags: --tag OldTag,NewTag')
        repo_root = resolve_git_repo_root(oh_root)
        old_sdk = os.path.join(tmp_root, 'tag_old'); new_sdk = os.path.join(tmp_root, 'tag_new')
        shutil.rmtree(tmp_root, ignore_errors=True)
        export_ref_to_sdk_dir(repo_root, tags[0], old_sdk)
        export_ref_to_sdk_dir(repo_root, tags[1], new_sdk)
        tmp_out = os.path.join(tmp_root, 'out')
        json_paths = run_api_diff_tool(old_sdk, new_sdk, tags[0], tags[1], oh_root, tmp_out)
        diffs = load_diff_entries(json_paths)
        print(f'[parse_api_diff] tag diff ({tags[0]} -> {tags[1]}) produced {len(diffs)} change(s)')

    # Resolve output task dir.
    coverage_data_dir = os.path.join(SKILL_ROOT, '.coverage_data')
    task_dir = coverage_data_dir
    if args.task_subsystem and args.task_module:
        task_dir = os.path.join(task_dir, args.task_subsystem, args.task_module)
    if args.session_id:
        task_dir = os.path.join(task_dir, args.session_id)

    build_output(diffs, ets_versions, args.subsystem, args.kit, args.dts_file,
                 args.iter_phase, task_dir)


if __name__ == '__main__':
    main()
