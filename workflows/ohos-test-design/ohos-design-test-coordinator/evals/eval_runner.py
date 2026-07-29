#!/usr/bin/env python3
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLACEHOLDERS = {}


def load_evals(eval_path):
    eval_path = Path(eval_path).resolve()
    with open(eval_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    fixtures_dir = str(eval_path.parent / 'fixtures')
    PLACEHOLDERS['{fixtures_dir}'] = fixtures_dir
    return data, eval_path


def substitute(text):
    if not text:
        return text
    result = text
    for ph, val in PLACEHOLDERS.items():
        result = result.replace(ph, val)
    return result


def resolve_files(files, eval_path):
    resolved = []
    base_dir = eval_path.parent
    for f in files:
        resolved.append(str((base_dir / f).resolve()))
    return resolved


def stage_fixtures(eval_path, output_dir, eval_item):
    base_dir = eval_path.parent
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    staged = []
    for f in eval_item.get('files', []):
        src = (base_dir / f).resolve()
        if not src.exists():
            print(f"  [WARN] fixture not found: {src}")
            continue
        dst = out / src.name
        shutil.copy2(str(src), str(dst))
        staged.append(str(dst))
        print(f"  [STAGED] {src.name} -> {dst}")
    return staged


def find_files(target_pattern):
    pattern = substitute(target_pattern)
    normalized = pattern.replace('\\', '/')
    matches = glob.glob(normalized, recursive=True)
    return sorted(matches)


def check_file_exists(assertion):
    target = assertion.get('target', '')
    matches = find_files(target)
    passed = len(matches) >= 1
    detail = f"matched {len(matches)} file(s)" if matches else "no files matched"
    return passed, detail


def check_file_contains(assertion):
    target = assertion.get('target', '')
    pattern = assertion.get('pattern', '')
    match_mode = assertion.get('match_mode', 'any')
    matches = find_files(target)
    if not matches:
        return False, "no files matched target glob"
    containing = []
    for fp in matches:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            if pattern in content:
                containing.append(fp)
        except Exception as e:
            return False, f"read error: {e}"
    if match_mode == 'all':
        passed = len(containing) == len(matches)
        detail = f"{len(containing)}/{len(matches)} files contain '{pattern}'"
    else:
        passed = len(containing) >= 1
        detail = f"{len(containing)}/{len(matches)} files contain '{pattern}'"
    return passed, detail


def check_file_not_contains(assertion):
    target = assertion.get('target', '')
    pattern = assertion.get('pattern', '')
    match_mode = assertion.get('match_mode', 'all')
    matches = find_files(target)
    if not matches:
        return True, "no files matched (vacuously true)"
    containing = []
    for fp in matches:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            if pattern in content:
                containing.append(fp)
        except Exception as e:
            return False, f"read error: {e}"
    if match_mode == 'all':
        passed = len(containing) == 0
        detail = f"0/{len(matches)} files contain '{pattern}' (all clean)"
        if not passed:
            detail = f"{len(containing)}/{len(matches)} files contain '{pattern}' (violation)"
    else:
        passed = len(containing) < len(matches)
        detail = f"{len(matches) - len(containing)}/{len(matches)} files do NOT contain '{pattern}'"
    return passed, detail


def check_dir_contains(assertion):
    dir_path = substitute(assertion.get('dir', ''))
    pattern = assertion.get('pattern', '')
    min_count = assertion.get('min_count', 1)
    search_dir = Path(dir_path)
    if not search_dir.exists():
        return False, f"directory does not exist: {dir_path}"
    normalized = pattern.replace('\\', '/')
    full_pattern = str(search_dir / '**' / normalized)
    matches = glob.glob(full_pattern, recursive=True)
    matches = [m for m in matches if os.path.isfile(m)]
    passed = len(matches) >= min_count
    detail = f"found {len(matches)} file(s), min required {min_count}"
    return passed, detail


def check_script_exit_code(assertion):
    command = substitute(assertion.get('command', ''))
    expected = assertion.get('expected', 0)
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=300
        )
        passed = result.returncode == expected
        detail = f"exit code {result.returncode} (expected {expected})"
        if result.stderr:
            detail += f" stderr: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return False, "command timed out (300s)"
    except Exception as e:
        return False, f"command failed: {e}"
    return passed, detail


ASSERTION_CHECKERS = {
    'file_exists': check_file_exists,
    'file_contains': check_file_contains,
    'file_not_contains': check_file_not_contains,
    'dir_contains': check_dir_contains,
    'script_exit_code': check_script_exit_code,
}


def run_assertion(assertion):
    atype = assertion.get('type', '')
    checker = ASSERTION_CHECKERS.get(atype)
    if not checker:
        return False, f"unknown assertion type: {atype}"
    return checker(assertion)


def evaluate_output_dir(eval_data, eval_path, output_dir, eval_id=None):
    PLACEHOLDERS['{output_dir}'] = str(Path(output_dir).resolve())
    skill_root_default = str(eval_path.parent.parent.resolve())
    PLACEHOLDERS.setdefault('{skill_root}', skill_root_default)

    results = []
    evals = eval_data.get('evals', [])
    for ev in evals:
        if eval_id is not None and ev['id'] != eval_id:
            continue
        ev_results = []
        for assertion in ev.get('assertions', []):
            passed, detail = run_assertion(assertion)
            ev_results.append({
                'eval_id': ev['id'],
                'eval_name': ev['name'],
                'assertion_id': assertion['id'],
                'assertion_type': assertion['type'],
                'description': assertion.get('description', ''),
                'passed': passed,
                'detail': detail,
            })
        results.extend(ev_results)
    return results


def print_eval_results(results, label):
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"{'='*70}")
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    current_eval = None
    for r in results:
        if r['eval_id'] != current_eval:
            current_eval = r['eval_id']
            ev_name = r['eval_name']
            ev_assertions = [x for x in results if x['eval_id'] == current_eval]
            ev_passed = sum(1 for x in ev_assertions if x['passed'])
            print(f"\n  [Eval {current_eval}] {ev_name}")
            print(f"  {ev_passed}/{len(ev_assertions)} assertions passed")
            print(f"  {'-'*66}")
        status = 'PASS' if r['passed'] else 'FAIL'
        print(f"    [{status}] {r['assertion_id']} ({r['assertion_type']}): {r['description']}")
        if not r['passed']:
            print(f"           -> {r['detail']}")
    print(f"\n  Total: {passed}/{total} assertions passed ({100*passed/total:.0f}%)" if total else "\n  Total: 0 assertions")
    return passed, total


def run_compare(args, eval_data, eval_path):
    skill_root = args.skill_root or str(eval_path.parent.parent.resolve())
    PLACEHOLDERS['{skill_root}'] = skill_root

    with_results = evaluate_output_dir(eval_data, eval_path, args.with_skill_dir)
    without_results = evaluate_output_dir(eval_data, eval_path, args.without_skill_dir)

    w_passed, w_total = print_eval_results(with_results, "WITH SKILL")
    wo_passed, wo_total = print_eval_results(without_results, "WITHOUT SKILL")

    print(f"\n{'='*70}")
    print(f"  COMPARISON SUMMARY")
    print(f"{'='*70}")
    print(f"\n  {'Eval':<6} {'Name':<40} {'With':<8} {'Without':<8} {'Delta':<8}")
    print(f"  {'-'*70}")

    eval_ids = sorted(set(r['eval_id'] for r in with_results), key=lambda x: x)
    total_delta = 0
    for eid in eval_ids:
        w_ev = [r for r in with_results if r['eval_id'] == eid]
        wo_ev = [r for r in without_results if r['eval_id'] == eid]
        w_p = sum(1 for r in w_ev if r['passed'])
        wo_p = sum(1 for r in wo_ev if r['passed'])
        name = w_ev[0]['eval_name'] if w_ev else ''
        delta = w_p - wo_p
        total_delta += delta
        print(f"  {eid:<6} {name:<40} {w_p}/{len(w_ev):<5} {wo_p}/{len(wo_ev):<5} +{delta}")

    print(f"  {'-'*70}")
    print(f"  {'TOTAL':<46} {w_passed}/{w_total:<5} {wo_passed}/{wo_total:<5} +{total_delta}")
    print(f"\n  Skill incremental value: {total_delta} additional assertions passed with skill.\n")

    print(f"\n  {'Eval':<6} {'Assert':<10} {'Description':<45} {'With':<7} {'W/O':<7}")
    print(f"  {'-'*75}")
    for w_r, wo_r in zip(with_results, without_results):
        w_s = 'PASS' if w_r['passed'] else 'FAIL'
        wo_s = 'PASS' if wo_r['passed'] else 'FAIL'
        flag = '  <-- skill gained' if (w_r['passed'] and not wo_r['passed']) else ('      <-- w/o gained' if (wo_r['passed'] and not w_r['passed']) else '')
        print(f"  {w_r['eval_id']:<6} {w_r['assertion_id']:<10} {w_r['description'][:45]:<45} {w_s:<7} {wo_s:<7}{flag}")

    if args.output:
        report = {
            'with_skill': {'passed': w_passed, 'total': w_total},
            'without_skill': {'passed': wo_passed, 'total': wo_total},
            'delta': total_delta,
            'details': [],
        }
        for w_r, wo_r in zip(with_results, without_results):
            report['details'].append({
                'eval_id': w_r['eval_id'],
                'assertion_id': w_r['assertion_id'],
                'description': w_r['description'],
                'with_skill': w_r['passed'],
                'without_skill': wo_r['passed'],
                'gained_by_skill': w_r['passed'] and not wo_r['passed'],
            })
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n  Report saved to: {args.output}")


def run_evaluate(args, eval_data, eval_path):
    skill_root = args.skill_root or str(eval_path.parent.parent.resolve())
    PLACEHOLDERS['{skill_root}'] = skill_root
    results = evaluate_output_dir(eval_data, eval_path, args.output_dir, args.eval_id)
    if not results:
        print("No assertions to evaluate.")
        return
    print_eval_results(results, f"EVALUATE: {Path(args.output_dir).resolve()}")


def run_stage(args, eval_data, eval_path):
    evals = eval_data.get('evals', [])
    for ev in evals:
        if args.eval_id is not None and ev['id'] != args.eval_id:
            continue
        print(f"\n[Eval {ev['id']}] {ev['name']}")
        if not ev.get('files'):
            print("  No fixture files to stage.")
            continue
        stage_fixtures(eval_path, args.output_dir, ev)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(
        description='Skill eval runner: evaluate assertions and compare with/without skill results.'
    )
    sub = parser.add_subparsers(dest='command', required=True)

    p_eval = sub.add_parser('evaluate', help='Evaluate all assertions against one output directory')
    p_eval.add_argument('--evals', required=True, help='Path to evals.json')
    p_eval.add_argument('--output-dir', required=True, help='Output directory to evaluate')
    p_eval.add_argument('--skill-root', help='Skill root directory (default: parent of evals/)')
    p_eval.add_argument('--eval-id', type=int, help='Evaluate only this eval id')

    p_cmp = sub.add_parser('compare', help='Compare with-skill vs without-skill output dirs')
    p_cmp.add_argument('--evals', required=True, help='Path to evals.json')
    p_cmp.add_argument('--with-skill-dir', required=True, help='Output dir from run WITH skill')
    p_cmp.add_argument('--without-skill-dir', required=True, help='Output dir from run WITHOUT skill')
    p_cmp.add_argument('--skill-root', help='Skill root directory')
    p_cmp.add_argument('--output', help='Save comparison report as JSON to this path')

    p_stage = sub.add_parser('stage', help='Stage fixture files to output directory')
    p_stage.add_argument('--evals', required=True, help='Path to evals.json')
    p_stage.add_argument('--output-dir', required=True, help='Output directory to stage fixtures into')
    p_stage.add_argument('--eval-id', type=int, help='Stage only this eval id')

    args = parser.parse_args()

    eval_data, eval_path = load_evals(args.evals)

    if args.command == 'evaluate':
        run_evaluate(args, eval_data, eval_path)
    elif args.command == 'compare':
        run_compare(args, eval_data, eval_path)
    elif args.command == 'stage':
        run_stage(args, eval_data, eval_path)


if __name__ == '__main__':
    main()
