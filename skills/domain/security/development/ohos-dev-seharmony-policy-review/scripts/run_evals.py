#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two-gate eval runner: scanner regression gate + report eval gate (F6/R5-F7).

Usage:
  python3 scripts/run_evals.py                        # scanner gate only (machine_checks
                                                       # + summary consistency + git regressions
                                                       # + grader self-test + full-CLI negative
                                                       # self-test); report assertions
                                                       # are counted and reported as pending
  python3 scripts/run_evals.py --evals evals/evals.json
  python3 scripts/run_evals.py --reports evals/reports  # scanner gate + report gate: every
                                                       # assertion's grader rules are executed
                                                       # against evals/reports/eval-<id>.md
Exit code: 0 all requested gates passed; 1 any failure

Gate 1 — scanner regression (always runs):
  1. machine_checks of every evals.json case:
     exit_code / scan_output_contains / scan_output_not_contains /
     scan_output_contains_count(min|exact) / rom_value
  2. Summary consistency (R4-4): rule-line count, policy-file count and A value
     match independent counting (oh-gc rendered fixtures are normalized first,
     mirroring scan.py's stdin normalization — R5-F1)
  3. Built-in git regressions (R3-1/F1/F4): two-commit branch merge-base net diff via
     short name, origin/<name>, refs/heads/<name> and refs/remotes/<name>; detached
     SHA stays a tip-commit scan; S4 verdicts stay identical across different
     checkouts (target-tree binding); empty net diff after revert
  4. Grader self-test: wrong status / impossible mention / missing table row must
     all fail the grader (proves the gate can go red)
  5. Full-CLI negative self-test (R5-F7): corrupted golden reports — conflicting
     status, duplicate rows, sign-flipped ROM, FAIL without disposal — must make
     the complete CLI exit non-zero

Gate 2 — report eval (--reports):
  6. Assertion schema validation: every assertion is an object with a prose "text"
     and a non-empty "grader" rule list of known types — an assertion nothing
     consumes fails the run (no silent skip, no fake green)
  7. Structural report validation per report (R5-F7/F8), BEFORE assertion grading:
     each results-table row unique; each status cell exactly one status token;
     exactly one ROM conclusion, sign-aware, cross-checked against the scanner's
     ROM/A/D/M; report file/rule counts and A/D/M cross-checked against the
     scanner output; internal arithmetic (A − D + M) × 100 must equal the ROM value;
     every FAIL/SUGGESTION/WARNING row must have a matching [Sx] item in the
     corresponding disposal section (必须修复/建议修复/需评审决策)
  8. Report grading: evals/reports/eval-<id>.md graded rule by rule against each
     assertion's grader; a missing report file is a failure

Grader rule schema (each rule is a dict with "type" plus fields):
  {"type": "status", "check": "S2", "expect": "WARNING"}        row exists, status token in expect (str or list, any-of)
  {"type": "status_not", "check": "S17", "reject": "FAIL"}      row exists, status token not in reject
  {"type": "no_status", "status": "FAIL"}                        no results-table row carries this status
  {"type": "mentions", "text": "..."}                            report contains text (whitespace-normalized)
  {"type": "not_contains", "text": "..."}                        report must not contain text
  {"type": "rom", "value": "200 B"}                              signed ROM conclusion line matches (conclusion field only)
  {"type": "table_complete"}                                     all 22 check rows present (S1-S7,S9-S13,S15-S23,
                                                                 S20b included; S8/S14 removed, must stay absent)
  {"type": "disposal_group", "group": "必须修复", "present": true} disposal section heading present/absent
  {"type": "report_present"}                                     report file exists and is non-empty
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(SCRIPT_DIR, "scan.py")
sys.path.insert(0, SCRIPT_DIR)
import scan as scan_mod  # noqa: E402  (reuse normalize_diff_text so summary counting mirrors scan.py)

RULE_RE = re.compile(r"^\s*(allow|allowxperm|neverallow)\s")
STAT_RE = re.compile(r"^\s*(allow|allowxperm|neverallow|attribute|typeattribute)\s")

# results-table rows required by the report template (S8/S14 removed, not reused)
TABLE_CHECKS = [
    "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S9", "S10", "S11", "S12", "S13",
    "S15", "S16", "S17", "S18", "S19", "S20", "S20b", "S21", "S22", "S23",
]
STATUS_TOKENS = ("PASS", "SUGGESTION", "WARNING", "FAIL", "NA")
DISPOSAL_GROUPS = ("必须修复", "建议修复", "需评审决策")
STATUS_TO_DISPOSAL = {"FAIL": "必须修复", "SUGGESTION": "建议修复", "WARNING": "需评审决策"}
# signed ROM conclusion line of the report template (uses U+2212 minus, like the template)
ROM_CONCLUSION_RE = re.compile(r"\(A − D \+ M\) × 100B = \*\*(-?\d+) B\*\*")
GRADER_TYPES = (
    "status", "status_not", "no_status", "mentions", "not_contains",
    "rom", "table_complete", "disposal_group", "report_present",
)

SCANNER_FAILURES = []
REPORT_FAILURES = []


def scanner_fail(case, msg):
    SCANNER_FAILURES.append("[%s] %s" % (case, msg))
    print("  FAIL: %s" % msg)


def report_fail(case, msg):
    REPORT_FAILURES.append("[%s] %s" % (case, msg))
    print("  FAIL: %s" % msg)


def ok(msg):
    print("  ok: %s" % msg)


_SCAN_CACHE = {}


def run_scan_stdin(diff_path, use_cache=True):
    """Run scan.py on a fixture via stdin. Results are cached per fixture path —
    check_case and grade_reports share one scan per fixture instead of two."""
    key = os.path.abspath(diff_path)
    if use_cache and key in _SCAN_CACHE:
        return _SCAN_CACHE[key]
    with open(diff_path, "r", encoding="utf-8", errors="replace") as fh:
        proc = subprocess.run(
            [sys.executable, SCAN, "-"], input=fh.read(),
            capture_output=True, text=True, errors="replace",
        )
    result = (proc.returncode, proc.stdout, proc.stderr)
    if use_cache:
        _SCAN_CACHE[key] = result
    return result


def validate_assertion_schema(evals_data, fail=report_fail):
    """(F6) Every assertion must be an object with prose text and a non-empty grader
    rule list of known types. Anything unconsumed fails the run up front."""
    problems = 0
    total = 0
    for case in evals_data["evals"]:
        name = case.get("name", "eval-%s" % case.get("id", "?"))
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            fail(name, "missing non-empty assertions list")
            problems += 1
            continue
        for i, a in enumerate(assertions, 1):
            total += 1
            where = "%s assertion %d" % (name, i)
            if not isinstance(a, dict) or not a.get("text"):
                fail(where, "must be an object with a prose 'text' field")
                problems += 1
                continue
            rules = a.get("grader")
            if not isinstance(rules, list) or not rules:
                fail(where, "assertion has no grader rules — nothing consumes it: %s" % a["text"][:60])
                problems += 1
                continue
            for r in rules:
                if not isinstance(r, dict) or r.get("type") not in GRADER_TYPES:
                    fail(where, "unknown grader rule type: %r" % (r,))
                    problems += 1
                elif r["type"] in ("status", "status_not") and not r.get("check"):
                    fail(where, "grader rule %r missing 'check'" % (r,))
                    problems += 1
                elif r["type"] in ("status",) and not r.get("expect"):
                    fail(where, "status rule missing 'expect'")
                    problems += 1
                elif r["type"] in ("status_not",) and not r.get("reject"):
                    fail(where, "status_not rule missing 'reject'")
                    problems += 1
                elif r["type"] == "no_status" and not r.get("status"):
                    fail(where, "no_status rule missing 'status'")
                    problems += 1
                elif r["type"] in ("mentions", "not_contains") and not r.get("text"):
                    fail(where, "%s rule missing 'text'" % r["type"])
                    problems += 1
                elif r["type"] == "rom" and not r.get("value"):
                    fail(where, "rom rule missing 'value'")
                    problems += 1
                elif r["type"] == "disposal_group" and r.get("group") not in DISPOSAL_GROUPS:
                    fail(where, "disposal_group rule group must be one of %s" % (DISPOSAL_GROUPS,))
                    problems += 1
    return total, problems


# ---------------------------------------------------------------- report grading

def _norm(text):
    return " ".join(text.split())


def _table_rows(report_text):
    """Yield (check_id_cell, status_cell) from results-table rows. The report
    template table is | 编号 | 自检项 | 状态 | 位置/依据 | — check id is cell 0,
    status is cell 2; rows without the full 4-column shape are not table rows."""
    for line in report_text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 4:
            yield cells[0], cells[2]


def _cell_has_token(cell, token):
    return re.search(r"\b%s\b" % re.escape(token), cell) is not None


def _check_word_match(cell, check):
    return re.search(r"\b%s\b" % re.escape(check), cell) is not None


def grade_rule(report_text, rule):
    """Return (passed: bool, detail: str) for one grader rule against a report."""
    t = rule["type"]
    if t == "status":
        expects = rule["expect"] if isinstance(rule["expect"], list) else [rule["expect"]]
        for cid, status in _table_rows(report_text):
            if _check_word_match(cid, rule["check"]):
                if any(_cell_has_token(status, e) for e in expects):
                    return True, "row %s status %s" % (rule["check"], status)
                return False, "row %s status is %r, expected %r" % (rule["check"], status, expects)
        return False, "no results-table row for check %s" % rule["check"]
    if t == "status_not":
        rejects = rule["reject"] if isinstance(rule["reject"], list) else [rule["reject"]]
        for cid, status in _table_rows(report_text):
            if _check_word_match(cid, rule["check"]):
                if any(_cell_has_token(status, rj) for rj in rejects):
                    return False, "row %s status is %r, rejected %r" % (rule["check"], status, rejects)
                return True, "row %s status %s" % (rule["check"], status)
        return False, "no results-table row for check %s" % rule["check"]
    if t == "no_status":
        for cid, status in _table_rows(report_text):
            if _cell_has_token(status, rule["status"]):
                return False, "row %s carries status %s" % (cid, rule["status"])
        return True, "no row carries status %s" % rule["status"]
    if t == "mentions":
        if _norm(rule["text"]) in _norm(report_text):
            return True, "mentions %r" % rule["text"]
        return False, "report does not mention %r" % rule["text"]
    if t == "not_contains":
        if _norm(rule["text"]) not in _norm(report_text):
            return True, "does not contain %r" % rule["text"]
        return False, "report must not contain %r" % rule["text"]
    if t == "rom":
        # (R5-F7) match the signed ROM conclusion field only — a sign-flipped value
        # (-600 B) must not satisfy a 600 B expectation, and stray numbers elsewhere
        # in the report must not count
        try:
            expected = int(re.sub(r"[^\d-]", "", rule["value"]))
        except ValueError:
            return False, "rom rule value %r is not numeric" % rule["value"]
        found = [int(x) for x in ROM_CONCLUSION_RE.findall(report_text)]
        if expected in found:
            return True, "ROM conclusion %s present" % rule["value"]
        return False, "ROM conclusion %s not found (conclusions found: %s)" % (rule["value"], found)
    if t == "table_complete":
        present = {cid for cid, _ in _table_rows(report_text)}
        missing = [c for c in TABLE_CHECKS if not any(_check_word_match(p, c) for p in present)]
        if missing:
            return False, "results table missing rows: %s" % ", ".join(missing)
        return True, "all %d check rows present" % len(TABLE_CHECKS)
    if t == "disposal_group":
        heading = "## %s" % rule["group"]
        has = heading in report_text
        want = bool(rule.get("present", True))
        if has == want:
            return True, "disposal group %s %s" % (rule["group"], "present" if want else "absent")
        return False, "disposal group %s should be %s" % (rule["group"], "present" if want else "absent")
    if t == "report_present":
        if report_text.strip():
            return True, "report present"
        return False, "report file is empty"
    return False, "unknown grader rule type %r" % t


def grade_assertions(name, report_text, assertions):
    """Grade every assertion (all its grader rules must pass). Returns passed count."""
    passed = 0
    for i, a in enumerate(assertions, 1):
        details = []
        all_ok = True
        for rule in a["grader"]:
            good, detail = grade_rule(report_text, rule)
            if not good:
                all_ok = False
            details.append(("ok" if good else "FAIL") + ": " + detail)
        if all_ok:
            passed += 1
        else:
            report_fail("%s assertion %d" % (name, i), a["text"])
            for d in details:
                if d.startswith("FAIL"):
                    print("       %s" % d)
    return passed


# ------------------------------------------------------- structural report validation

def _sections(report_text):
    """Split a report into {'<heading>': body} on '## ' headings ('_preamble' first)."""
    secs = {}
    cur = "_preamble"
    buf = []
    for line in report_text.splitlines():
        if line.startswith("## "):
            secs[cur] = "\n".join(buf)
            cur = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    secs[cur] = "\n".join(buf)
    return secs


def _status_tokens(cell):
    return [t for t in STATUS_TOKENS if _cell_has_token(cell, t)]


def _disposal_item_re(cid):
    # disposal items are tagged [Sx] or with a sub-item suffix: [S11d], [S2-A], [S18-B]
    return re.compile(r"\[%s(?:[a-z]|-[ABC])?\]" % re.escape(cid))


def structural_check_report(name, report_text, scan_out):
    """(R5-F7/F8) Whole-report structure validation, run before assertion grading.
    Returns a list of problems (empty = structurally valid)."""
    problems = []
    # 1. each results-table row unique; each status cell exactly one status token
    #    (only S<number> rows count — header/separator rows are skipped)
    seen = {}
    for cid, status in _table_rows(report_text):
        if not re.match(r"^S\d+[a-z]?$", cid):
            continue
        if cid in seen:
            problems.append("duplicate results-table row for check %s" % cid)
            continue
        seen[cid] = status
        tokens = _status_tokens(status)
        if len(tokens) != 1:
            problems.append(
                "row %s status %r must contain exactly one status token (found %s)"
                % (cid, status, tokens)
            )
    # 2. exactly one ROM conclusion; sign-aware cross-check with the scanner
    roms = ROM_CONCLUSION_RE.findall(report_text)
    if len(roms) != 1:
        problems.append("expected exactly one ROM conclusion line, found %d" % len(roms))
    else:
        scan_rom = re.search(r"ROM increment estimate = \(A - D \+ M\) × 100B = (-?\d+) B", scan_out)
        if scan_rom and int(roms[0]) != int(scan_rom.group(1)):
            problems.append("ROM conclusion %s B != scanner %s B" % (roms[0], scan_rom.group(1)))
    # 3. A/D/M detail lines: internal arithmetic + cross-check with the scanner
    ma = re.search(r"新增策略规则行（A）：(\d+) 条", report_text)
    md = re.search(r"删减策略规则行（D）：(\d+) 条", report_text)
    mm = re.search(r"access_vector 范围变更（M）：(\d+) 处", report_text)
    if not (ma and md and mm):
        problems.append("ROM A/D/M detail lines missing")
    elif len(roms) == 1:
        a, d, m = int(ma.group(1)), int(md.group(1)), int(mm.group(1))
        if (a - d + m) * 100 != int(roms[0]):
            problems.append("ROM arithmetic: (A %d − D %d + M %d) × 100 != %s B" % (a, d, m, roms[0]))
        sa = re.search(r"^A=(\d+)\s+D=(\d+)\s+M=(\d+)", scan_out, re.M)
        if sa and (a, d, m) != tuple(int(x) for x in sa.groups()):
            problems.append(
                "report A/D/M (%d/%d/%d) != scanner A/D/M (%s/%s/%s)" % (a, d, m, *sa.groups())
            )
    # 4. summary counts cross-checked with the scanner (file count, rule count);
    #    a missing summary line is itself a failure (N1: no silent skip)
    mf = re.search(r"\*\*涉及策略文件\*\*：(\d+) 个", report_text)
    mr = re.search(r"\*\*新增规则行\*\*：(\d+) 条", report_text)
    sf = re.search(r"Policy files involved: (\d+)", scan_out)
    sr = re.search(r"New rule lines \(allow/allowxperm/neverallow, indented included\): (\d+)", scan_out)
    if mf is None:
        problems.append("summary line '**涉及策略文件**：N 个' missing")
    elif sf and int(mf.group(1)) != int(sf.group(1)):
        problems.append("report file count %s != scanner file count %s" % (mf.group(1), sf.group(1)))
    if mr is None:
        problems.append("summary line '**新增规则行**：N 条' missing")
    elif sr and int(mr.group(1)) != int(sr.group(1)):
        problems.append("report rule count %s != scanner rule count %s" % (mr.group(1), sr.group(1)))
    # 5. status -> disposal enforcement: FAIL/SUGGESTION/WARNING rows must have a
    #    matching [Sx] item in the corresponding disposal section (heading matched
    #    by prefix — template headings carry parenthetical suffixes)
    secs = _sections(report_text)
    for cid, status in seen.items():
        tokens = _status_tokens(status)
        if len(tokens) != 1:
            continue  # already reported above
        tok = tokens[0]
        group = STATUS_TO_DISPOSAL.get(tok)
        if not group:
            continue
        body = None
        for heading, text in secs.items():
            if heading.startswith(group):
                body = text
                break
        if body is None:
            problems.append("row %s is %s but disposal section '%s' is missing" % (cid, tok, group))
        elif not _disposal_item_re(cid).search(body):
            problems.append("row %s is %s but no [%s] item in '%s'" % (cid, tok, cid, group))
    return problems


# ---------------------------------------------------------------- scanner gate

def check_case(idx, case):
    name = case.get("name", "case-%d" % idx)
    print("== eval %d: %s" % (case.get("id", idx), name))
    fixture = os.path.join(SCRIPT_DIR, "..", "evals", "files", os.path.basename(case["files"][0]))
    fixture = os.path.normpath(fixture)
    if not os.path.exists(fixture):
        scanner_fail(name, "fixture missing: %s" % fixture)
        return
    code, out, err = run_scan_stdin(fixture)
    mc = case.get("machine_checks", {})
    if "exit_code" in mc and code != mc["exit_code"]:
        scanner_fail(name, "exit_code=%d expected %d (stderr: %s)" % (code, mc["exit_code"], err.strip()[:120]))
    else:
        ok("exit_code=%d" % code)
    for s in mc.get("scan_output_contains", []):
        if s not in out:
            scanner_fail(name, "output missing: %r" % s)
    for s in mc.get("scan_output_not_contains", []):
        if s in out:
            scanner_fail(name, "output must not contain: %r" % s)
    cnt = mc.get("scan_output_contains_count")
    if cnt:
        n = len(re.findall(cnt["pattern"], out))
        if "min" in cnt and n < cnt["min"]:
            scanner_fail(name, "pattern %r count %d < min %d" % (cnt["pattern"], n, cnt["min"]))
        if "exact" in cnt and n != cnt["exact"]:
            scanner_fail(name, "pattern %r count %d != exact %d" % (cnt["pattern"], n, cnt["exact"]))
    if "rom_value" in mc:
        expect = "ROM increment estimate = (A - D + M) × 100B = %s" % mc["rom_value"]
        if expect not in out:
            scanner_fail(name, "ROM expectation %r not found in output" % expect)
    # summary consistency (R4-4; R5-F1: normalize first so oh-gc rendered fixtures
    # — no +++ b/ lines — count the same as standard git diffs)
    with open(fixture, "r", encoding="utf-8", errors="replace") as fh:
        diff_text = scan_mod.normalize_diff_text(fh.read())
    rule_n = sum(
        1 for raw in diff_text.splitlines()
        if raw.startswith("+") and not raw.startswith("+++") and RULE_RE.match(raw[1:])
    )
    m = re.search(r"New rule lines \(allow/allowxperm/neverallow, indented included\): (\d+)", out)
    if not m or int(m.group(1)) != rule_n:
        scanner_fail(name, "summary rule-line count %s != independent count %d" % (m.group(1) if m else "?", rule_n))
    file_n = sum(1 for raw in diff_text.splitlines() if raw.startswith("+++ b/"))
    m = re.search(r"Policy files involved: (\d+)", out)
    if not m or int(m.group(1)) != file_n:
        scanner_fail(name, "summary file count %s != independent count %d" % (m.group(1) if m else "?", file_n))
    a_n = sum(
        1 for raw in diff_text.splitlines()
        if raw.startswith("+") and not raw.startswith("+++") and STAT_RE.match(raw[1:])
    )
    m = re.search(r"^A=(\d+)", out, re.M)
    if not m or int(m.group(1)) != a_n:
        scanner_fail(name, "ROM A value %s != independent count %d" % (m.group(1) if m else "?", a_n))


def git_repo_regression():
    """R3-1/F1: two-commit branch merge-base net diff via every branch-ref spelling;
    detached SHA stays a tip-commit scan; empty net diff after revert."""
    print("== git regression: branch ref spellings / two-commit branch / empty net diff")
    repo = tempfile.mkdtemp(prefix="scanpy-reg-")
    try:
        def git(*args, **kw):
            return subprocess.run(
                ["git", "-C", repo] + list(args),
                capture_output=True, text=True, errors="replace", **kw
            )

        def scan(ref):
            return subprocess.run(
                [sys.executable, SCAN, ref], cwd=repo,
                capture_output=True, text=True, errors="replace",
            )

        git("init", "-q", "-b", "master")
        git("config", "user.email", "t@t")
        git("config", "user.name", "t")
        os.makedirs(os.path.join(repo, "sepolicy/ohos_policy/test/test_comp/system"))
        os.makedirs(os.path.join(repo, "sepolicy/base/public"))
        with open(os.path.join(repo, "sepolicy/ohos_policy/test/test_comp/system/base.te"), "w") as fh:
            fh.write("# base\n")
        # a type defined in public (for S4 placement judgment)
        with open(os.path.join(repo, "sepolicy/base/public/global.te"), "w") as fh:
            fh.write("type demo_type;\n")
        git("add", "-A")
        git("commit", "-qm", "base")
        git("checkout", "-qb", "feature")
        # commit 1: add an allow (early commit, not in the branch tip) +
        # a neverallow referencing a public type (S4 placement suggestion)
        with open(os.path.join(repo, "sepolicy/ohos_policy/test/test_comp/system/base.te"), "a") as fh:
            fh.write("allow foo default_service:service_manager { add };\n")
            fh.write("neverallow demo_type self:process { ptrace };\n")
        git("add", "-A")
        git("commit", "-qm", "add allow")
        # commit 2 (tip): comment only
        with open(os.path.join(repo, "sepolicy/ohos_policy/test/test_comp/system/base.te"), "a") as fh:
            fh.write("# just a comment\n")
        git("add", "-A")
        git("commit", "-qm", "comment only")
        # publish the branch as a remote-tracking ref (origin/feature)
        git("update-ref", "refs/remotes/origin/feature", "feature")

        # F1: every branch-ref spelling must resolve merge-base and scan the net diff,
        # catching the early commit's allow (incl. S16 default_service)
        for ref in ("feature", "origin/feature", "refs/heads/feature", "refs/remotes/origin/feature"):
            proc = scan(ref)
            if proc.returncode != 0:
                scanner_fail("git-regression", "scan.py %s exit code %d: %s" % (ref, proc.returncode, proc.stderr.strip()[:200]))
            elif "allow foo default_service:service_manager" not in proc.stdout:
                scanner_fail("git-regression", "scan.py %s missed the early commit's allow (merge-base net diff broken)" % ref)
            elif "[S4 suggestion]" not in proc.stdout:
                scanner_fail("git-regression", "scan.py %s: S4 placement suggestion missing" % ref)
            else:
                ok("scan.py %s caught the early commit's allow (merge-base net diff) + S4 suggestion" % ref)

        # F1 negative: a detached SHA is a tip-commit scan — the comment-only tip must
        # NOT surface the early commit's allow
        tip_sha = git("rev-parse", "feature").stdout.strip()
        proc = scan(tip_sha)
        if proc.returncode != 0:
            scanner_fail("git-regression", "scan.py <sha> exit code %d: %s" % (proc.returncode, proc.stderr.strip()[:200]))
        elif "allow foo default_service:service_manager" in proc.stdout:
            scanner_fail("git-regression", "detached SHA scan must not surface other commits' changes")
        else:
            ok("scan.py <detached-sha> scans the tip commit only (no early-commit leak)")

        # range scan catches it too
        proc2 = scan("master..feature")
        if "allow foo default_service:service_manager" not in proc2.stdout:
            scanner_fail("git-regression", "range scan missed the allow")
        else:
            ok("scan.py master..feature caught the allow")

        # R5-F4: S4 verdicts must bind to the scanned target's tree, not the
        # current checkout — move demo_type's definition to system/ on another
        # branch, check it out, and rescan feature: the verdict must not change
        # (run BEFORE the empty-net-diff revert below, which empties feature)
        git("checkout", "-qb", "moved", "master")
        os.makedirs(os.path.join(repo, "sepolicy/base/system"), exist_ok=True)
        os.rename(
            os.path.join(repo, "sepolicy/base/public/global.te"),
            os.path.join(repo, "sepolicy/base/system/global.te"),
        )
        git("add", "-A")
        git("commit", "-qm", "move demo_type to system")
        git("checkout", "-q", "moved")  # worktree now has demo_type in system/
        proc4 = scan("feature")
        if "[S4 suggestion]" not in proc4.stdout:
            scanner_fail("git-regression", "S4 verdict changed with the checkout (target-tree binding broken): %s" % [
                l.strip() for l in proc4.stdout.splitlines() if "[S4" in l][:2])
        else:
            ok("S4 verdict checkout-invariant (bound to feature's tree, demo_type still public there)")
        git("checkout", "-q", "master")  # clean up the moved branch's checkout
        git("checkout", "-q", "feature")  # back on feature for the empty-net-diff revert below

        # empty net diff: add then fully revert -> exit 1 + message
        with open(os.path.join(repo, "sepolicy/ohos_policy/test/test_comp/system/base.te"), "w") as fh:
            fh.write("# base\n")
        git("add", "-A")
        git("commit", "-qm", "revert allow")
        proc3 = scan("master..feature")
        if proc3.returncode == 1 and "empty diff" in proc3.stderr:
            ok("empty net diff: exit 1 + message (no false positives)")
        else:
            scanner_fail("git-regression", "empty net diff not handled as empty: rc=%d stderr=%r" % (proc3.returncode, proc3.stderr.strip()[:120]))
    finally:
        shutil.rmtree(repo, ignore_errors=True)


# ---------------------------------------------------------------- grader self-test

_SELFTEST_TABLE = """
| 编号 | 自检项 | 状态 | 位置/依据 |
|------|--------|------|-----------|
| S1 | 敏感词 | PASS | - |
| S2 | base 落点 | WARNING | demo/file.te `allow demo demo_file:file { read };` |
| S3 | 参数标签 | NA | - |
| S4 | neverallow 落点 | NA | - |
| S5 | SA 看护 | NA | - |
| S6 | 系统参数 | NA | - |
| S7 | 写执行管控 | NA | - |
| S9 | debug 隔离 | NA | - |
| S10 | developer 隔离 | NA | - |
| S11 | 安全评审 | NA | - |
| S12 | sh 主体 | NA | - |
| S13 | su 客体 | NA | - |
| S15 | hap 范围 | NA | - |
| S16 | 默认标签 | NA | - |
| S17 | avc 注释 | NA | - |
| S18 | allow 落点 | NA | - |
| S19 | 空行分隔 | NA | - |
| S20 | appdat | NA | - |
| S20b | binder 完整性 | NA | - |
| S21 | service_contexts | NA | - |
| S22 | flex 白名单 | NA | - |
| S23 | 产品宏 | NA | - |
"""

_SELFTEST_GOOD = "# SELinux 策略提交自检报告\n" + _SELFTEST_TABLE + """
## ROM 增量估算
- **预计 ROM 增量**：(A − D + M) × 100B = **200 B**

## 需评审决策（WARNING 需确认，结论回填后再合入）
- [S2] demo/file.te：`allow demo demo_file:file { read };` → 相关性确认
"""


def grader_selftest():
    """(F6) Prove the report gate can go red: wrong status, impossible mention,
    missing table row, wrong ROM and wrong disposal presence must all fail."""
    print("== grader self-test: gate must fail on wrong/missing content")
    bad_report = _SELFTEST_GOOD.replace("| S2 | base 落点 | WARNING |", "| S2 | base 落点 | PASS |")
    cases = [
        ("status match", _SELFTEST_GOOD, {"type": "status", "check": "S2", "expect": "WARNING"}, True),
        ("status mismatch must fail", bad_report, {"type": "status", "check": "S2", "expect": "WARNING"}, False),
        ("impossible mention must fail", _SELFTEST_GOOD,
         {"type": "mentions", "text": "THIS_STRING_IS_GUARANTEED_ABSENT_XYZ_987654321"}, False),
        ("missing table row must fail", _SELFTEST_TABLE.replace("| S19 | 空行分隔 | NA | - |\n", ""),
         {"type": "table_complete"}, False),
        ("complete table passes", _SELFTEST_GOOD, {"type": "table_complete"}, True),
        ("wrong ROM must fail", _SELFTEST_GOOD, {"type": "rom", "value": "900 B"}, False),
        ("right ROM passes", _SELFTEST_GOOD, {"type": "rom", "value": "200 B"}, True),
        ("absent disposal group must fail", _SELFTEST_GOOD,
         {"type": "disposal_group", "group": "必须修复", "present": True}, False),
        ("present disposal group passes", _SELFTEST_GOOD,
         {"type": "disposal_group", "group": "需评审决策", "present": True}, True),
        ("no_status FAIL passes on clean report", _SELFTEST_GOOD, {"type": "no_status", "status": "FAIL"}, True),
        ("no_status must fail when FAIL present", bad_report.replace("| S2 | base 落点 | PASS |", "| S2 | base 落点 | FAIL |"),
         {"type": "no_status", "status": "FAIL"}, False),
    ]
    for label, report, rule, expect_pass in cases:
        got_pass, _ = grade_rule(report, rule)
        if got_pass == expect_pass:
            ok("grader %s" % label)
        else:
            scanner_fail("grader-selftest", "%s: expected %s" % (label, "pass" if expect_pass else "FAIL"))


# ---------------------------------------------------------------- report gate

_NEG_BASE_REPORT = """# SELinux 策略提交自检报告

**扫描范围**：clean_positive.diff（stdin，1 个策略文件）
**diff 性质**：新增权限（1 条新增 allow）
**涉及策略文件**：1 个  **新增规则行**：1 条

| 编号 | 自检项 | 状态 | 位置/依据（含策略原文） |
|------|--------|------|------------------------|
| S1 | 敏感词 | PASS | - |
| S2 | base 落点 | PASS | - |
| S3 | 参数标签 | NA | - |
| S4 | neverallow 落点 | NA | - |
| S5 | SA 看护 | NA | - |
| S6 | 系统参数 | NA | - |
| S7 | 写执行管控 | NA | - |
| S9 | debug 隔离 | NA | - |
| S10 | developer 隔离 | NA | - |
| S11 | 安全评审 | NA | - |
| S12 | sh 主体 | NA | - |
| S13 | su 客体 | NA | - |
| S15 | hap 范围 | NA | - |
| S16 | 默认标签 | PASS | - |
| S17 | avc 注释 | PASS | `allow init sys_file:file { read };` 已配 #avc: |
| S18 | allow 落点 | PASS | system/ |
| S19 | 空行分隔 | PASS | - |
| S20 | appdat | NA | - |
| S20b | binder 完整性 | NA | - |
| S21 | service_contexts | NA | - |
| S22 | flex 白名单 | NA | - |
| S23 | 产品宏 | PASS | - |

## ROM 增量估算
- 新增策略规则行（A）：1 条 × 100B（含 allow/allowxperm/neverallow/attribute/typeattribute）
- 删减策略规则行（D）：0 条 × 100B（可抵消）
- access_vector 范围变更（M）：0 处 × 100B（按新增计，删减不抵消）
- **预计 ROM 增量**：(A − D + M) × 100B = **100 B**
"""

_NEG_EVALS = {
    "skill_name": "negative-selftest",
    "evals": [{
        "id": 1,
        "name": "neg-case",
        "files": ["evals/files/clean_positive.diff"],
        "machine_checks": {"exit_code": 0, "rom_value": "100 B"},
        "assertions": [
            {"text": "S17 PASS", "grader": [{"type": "status", "check": "S17", "expect": ["PASS", "NA"]}]},
            {"text": "ROM 100 B", "grader": [{"type": "rom", "value": "100 B"}]},
        ],
    }],
}


def full_cli_negative_selftest():
    """(R5-F7) Reviewer PoC, end to end: corrupted golden reports — conflicting
    status cell, duplicate rows, sign-flipped ROM, FAIL without disposal — must
    make the COMPLETE CLI exit non-zero; the uncorrupted report must pass."""
    print("== full-CLI negative self-test: corrupted reports must exit non-zero")
    tmp = tempfile.mkdtemp(prefix="runneg-")
    try:
        evals_path = os.path.join(tmp, "evals.json")
        with open(evals_path, "w", encoding="utf-8") as fh:
            json.dump(_NEG_EVALS, fh, ensure_ascii=False)

        def run_cli(reports_dir):
            return subprocess.run(
                [sys.executable, os.path.abspath(__file__),
                 "--evals", evals_path, "--reports", reports_dir, "--selftests-off"],
                capture_output=True, text=True, errors="replace",
            )

        variants = {
            # three content corruptions in one report (conflicting status cell,
            # duplicate opposite row, sign-flipped ROM) — must exit non-zero;
            # per-check attribution is covered by the in-process grader self-test
            "content-corruptions": lambda r: r
                .replace("| S1 | 敏感词 | PASS | - |", "| S1 | 敏感词 | PASS / FAIL | - |")
                .replace(
                    "| S2 | base 落点 | PASS | - |",
                    "| S2 | base 落点 | PASS | - |\n| S2 | 相反结论 | FAIL | - |")
                .replace("× 100B = **100 B**", "× 100B = **-100 B**"),
            "fail-without-disposal": lambda r: r.replace(
                "| S1 | 敏感词 | PASS | - |", "| S1 | 敏感词 | FAIL | - |"),
            # N1: a deleted summary line must fail, not silently skip the cross-check
            "missing-summary-line": lambda r: r.replace(
                "**涉及策略文件**：1 个  **新增规则行**：1 条\n", ""),
        }
        for label, mutate in variants.items():
            reports_dir = os.path.join(tmp, label)
            os.makedirs(reports_dir)
            with open(os.path.join(reports_dir, "eval-1.md"), "w", encoding="utf-8") as fh:
                fh.write(mutate(_NEG_BASE_REPORT))
            proc = run_cli(reports_dir)
            if proc.returncode != 0:
                ok("corrupted report (%s) -> exit %d" % (label, proc.returncode))
            else:
                scanner_fail("cli-negative", "corrupted report (%s) passed with exit 0 — fake green" % label)

        reports_dir = os.path.join(tmp, "clean")
        os.makedirs(reports_dir)
        with open(os.path.join(reports_dir, "eval-1.md"), "w", encoding="utf-8") as fh:
            fh.write(_NEG_BASE_REPORT)
        proc = run_cli(reports_dir)
        if proc.returncode == 0:
            ok("uncorrupted report -> exit 0")
        else:
            scanner_fail("cli-negative", "clean report failed unexpectedly: %s" % proc.stdout.strip()[-300:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def grade_reports(evals_data, reports_dir):
    print("== report gate: grading final reports from %s" % reports_dir)
    total = passed = 0
    for case in evals_data["evals"]:
        name = case.get("name", "eval-%s" % case.get("id", "?"))
        path = os.path.join(reports_dir, "eval-%s.md" % case.get("id"))
        print("== report eval %s: %s (%s)" % (case.get("id", "?"), name, path))
        fixture = os.path.normpath(
            os.path.join(SCRIPT_DIR, "..", "evals", "files", os.path.basename(case["files"][0]))
        )
        if not os.path.exists(fixture):
            report_fail(name, "fixture missing: %s" % fixture)
            total += len(case.get("assertions", []))
            continue
        _, scan_out, _ = run_scan_stdin(fixture)
        if not os.path.exists(path):
            report_fail(name, "report file missing: %s" % path)
            total += len(case.get("assertions", []))
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            report_text = fh.read()
        # structural validation first (R5-F7/F8): uniqueness, single-enum status,
        # signed ROM + A/D/M cross-check, summary counts, status->disposal forcing
        for p in structural_check_report(name, report_text, scan_out):
            report_fail(name, "structure: %s" % p)
        n = len(case.get("assertions", []))
        p = grade_assertions(name, report_text, case.get("assertions", []))
        total += n
        passed += p
        if p == n:
            ok("%d/%d assertions graded" % (p, n))
    return passed, total


def main():
    evals_path = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "evals", "evals.json"))
    reports_dir = None
    selftests = True
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--evals" and i + 1 < len(args):
            evals_path = os.path.abspath(args[i + 1])
            i += 2
        elif args[i] == "--reports" and i + 1 < len(args):
            reports_dir = os.path.abspath(args[i + 1])
            i += 2
        elif args[i] == "--selftests-off":
            # internal: used by full_cli_negative_selftest to avoid re-spawning itself
            selftests = False
            i += 1
        else:
            print("usage: run_evals.py [--evals evals.json] [--reports reports_dir]")
            sys.exit(2)
    with open(evals_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    # assertion schema is validated in every mode (fake-green prevention)
    assertion_total, schema_problems = validate_assertion_schema(data)

    print("-- gate 1: scanner regression --")
    for idx, case in enumerate(data["evals"], 1):
        check_case(idx, case)
    if selftests:
        git_repo_regression()
        grader_selftest()
        full_cli_negative_selftest()
    print()
    if SCANNER_FAILURES:
        print("SCANNER REGRESSION FAILED (%d):" % len(SCANNER_FAILURES))
        for f in SCANNER_FAILURES:
            print("  - %s" % f)
    else:
        print(
            "SCANNER REGRESSION PASSED (%d machine-check evals + git regression + grader self-test)"
            % len(data["evals"])
        )

    if reports_dir:
        print()
        print("-- gate 2: report eval --")
        passed, total = grade_reports(data, reports_dir)
        print()
        if REPORT_FAILURES:
            print("REPORT EVAL FAILED (%d/%d assertions failed):" % (total - passed, total))
            for f in REPORT_FAILURES:
                print("  - %s" % f)
        else:
            print("REPORT EVAL PASSED (%d/%d assertions across %d cases)" % (passed, total, len(data["evals"])))
    else:
        print(
            "REPORT EVAL: PENDING — %d assertions across %d cases not graded; "
            "run with --reports <dir> to grade final reports"
            % (assertion_total, len(data["evals"]))
        )

    print()
    if SCANNER_FAILURES or REPORT_FAILURES or schema_problems:
        print(
            "FAILED (scanner: %d, report: %d, schema: %d)"
            % (len(SCANNER_FAILURES), len(REPORT_FAILURES), schema_problems)
        )
        sys.exit(1)
    if reports_dir:
        print("ALL GATES PASSED (scanner regression + report eval)")


if __name__ == "__main__":
    main()
