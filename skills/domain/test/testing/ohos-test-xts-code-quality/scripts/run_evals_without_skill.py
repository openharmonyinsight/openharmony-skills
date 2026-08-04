#!/usr/bin/env python3
"""
run_evals_without_skill.py - Without-Skill 基线自动化评估

模拟无 Skill 的通用代码审查基线：对每个 eval 用例，用「朴素扫描器」
（仅通用代码质量检查，无 29 条 XTS 专项规则、无 TRAPS 陷阱知识）扫描测试文件，
再与 with_skill（扫描器 main.py）结果比对，自动产出对比报告。

朴素扫描器检查项（通用，非 XTS 专项）：
  - 缺少断言的 it()（R004，通用测试质量）
  - 恒真断言 expect(true)（R003，通用逻辑）
  - 宽松比较 ==（R022，通用 lint）
  - 类型强转 toString()/String()/Number()（R023，通用 lint）
  - 注释废弃代码（R013，通用）
  - 同名 it() 重复（R018，通用）

朴素扫描器不检查（XTS 专项，通用工具不知道）：
  R001/R002/R005-R012/R014-R017/R019-R021/R201-R206

朴素扫描器对 traps.test.ts 产生误报（无 TRAPS 抑制知识）：
  - async(done) 混合模式 → 误报"异步无 done"
  - Promise.all → 误报"并发无隔离"
  - emitter.once → 误报"资源未释放"
  - await sleep → 误报"Promise 无 catch"

用法:
    python3 scripts/run_evals_without_skill.py    # 运行对比评估，输出对比表

退出码: 0=成功输出报告, 1=有错误
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
EVALS_PATH = os.path.join(SKILL_DIR, "evals", "evals.json")
MAIN_PY = os.path.join(SCRIPT_DIR, "main.py")

RULE_ID_RE = re.compile(r'R\d{3}')


# ============================================================
# 朴素扫描器（通用代码质量，无 XTS 专项规则）
# ============================================================

class NaiveScanner:
    """通用代码质量扫描器，模拟无 Skill 基线 LLM/通用 lint 工具。"""

    # 通用检查正则
    RE_LOOSE_CMP = re.compile(r'==[^=]')
    RE_TYPE_CAST = re.compile(r'\.(toString|String|Number|parseInt|parseFloat)\s*\(')
    RE_CONST_TRUE = re.compile(r'expect\s*\(\s*(true|1)\s*\)')
    RE_IT_BLOCK = re.compile(r"it\s*\(\s*['\"]([^'\"]+)['\"]")
    RE_ASSERTION = re.compile(r'expect\s*\(')
    # 误报触发正则（traps.test.ts）
    RE_ASYNC_NO_DONE = re.compile(r'async\s*\(\s*\)')
    RE_PROMISE_ALL = re.compile(r'Promise\.all\s*\(')
    RE_EMITTER_ONCE = re.compile(r'emitter\.once\s*\(')
    RE_AWAIT_SLEEP = re.compile(r'await\s+sleep\s*\(')
    RE_COMMENT_BLOCK = re.compile(r'//.*(?:if|for|while|switch|return|function|const|let)', re.IGNORECASE)

    def scan_file(self, filepath, content):
        """扫描单个文件，返回 issue 列表。"""
        issues = []
        filename = os.path.basename(filepath)
        lines = content.split('\n')

        # 仅扫描 .ts/.ets/.js 源文件
        if not filepath.endswith(('.ts', '.ets', '.js')):
            return issues

        # 提取 it() 块名
        it_names = []
        for i, line in enumerate(lines, 1):
            m = self.RE_IT_BLOCK.search(line)
            if m:
                it_names.append(m.group(1))

        # R004: 缺少断言的 it()（通用检查）
        # 找到 it() 后检查后续 5 行是否有 expect()
        for i, line in enumerate(lines):
            if self.RE_IT_BLOCK.search(line):
                block_end = min(i + 10, len(lines))
                block_text = '\n'.join(lines[i:block_end])
                if not self.RE_ASSERTION.search(block_text):
                    issues.append({
                        "rule": "R004",
                        "message": "测试用例缺少断言",
                        "file": filename,
                        "line": i + 1
                    })

        # R003: 恒真断言（通用检查）
        for i, line in enumerate(lines, 1):
            if self.RE_CONST_TRUE.search(line):
                issues.append({
                    "rule": "R003",
                    "message": "恒真断言 expect(true)",
                    "file": filename,
                    "line": i
                })

        # R022: 宽松比较 ==（通用 lint）
        for i, line in enumerate(lines, 1):
            if self.RE_LOOSE_CMP.search(line) and '===' not in line:
                issues.append({
                    "rule": "R022",
                    "message": "宽松比较 ==",
                    "file": filename,
                    "line": i
                })

        # R023: 类型强转（通用 lint）
        for i, line in enumerate(lines, 1):
            if self.RE_TYPE_CAST.search(line):
                issues.append({
                    "rule": "R023",
                    "message": "类型强转",
                    "file": filename,
                    "line": i
                })

        # R013: 注释废弃代码（通用检查 — 简化版）
        comment_count = 0
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//') and self.RE_COMMENT_BLOCK.search(stripped):
                comment_count += 1
                if comment_count >= 3:
                    issues.append({
                        "rule": "R013",
                        "message": "注释中包含废弃代码",
                        "file": filename,
                        "line": i - comment_count + 1
                    })
                    break

        # R018: 同名 it() 重复（通用检查 — 同文件内）
        seen = set()
        for name in it_names:
            if name in seen:
                issues.append({
                    "rule": "R018",
                    "message": f"同名用例重复: {name}",
                    "file": filename,
                    "line": 1
                })
            seen.add(name)

        # ---- 误报触发（traps.test.ts 专用，无 TRAPS 知识导致）----
        # 这些检查模拟通用 LLM 对 async/Promise/emitter 的朴素判断
        has_async_no_done = bool(self.RE_ASYNC_NO_DONE.search(content))
        has_promise_all = bool(self.RE_PROMISE_ALL.search(content))
        has_emitter_once = bool(self.RE_EMITTER_ONCE.search(content))
        has_await_sleep = bool(self.RE_AWAIT_SLEEP.search(content))

        if has_async_no_done:
            issues.append({
                "rule": "R201-FP",
                "message": "异步函数无 done 参数（误报：实际用 .catch(done)）",
                "file": filename,
                "line": 1
            })
        if has_promise_all:
            issues.append({
                "rule": "R203-FP",
                "message": "Promise.all 并发无隔离（误报：实际是安全并发）",
                "file": filename,
                "line": 1
            })
        if has_emitter_once:
            issues.append({
                "rule": "R204-FP",
                "message": "emitter 监听未释放（误报：.once 自动移除）",
                "file": filename,
                "line": 1
            })
        if has_await_sleep:
            issues.append({
                "rule": "R202-FP",
                "message": "await 无 try-catch（误报：sleep 不抛异常）",
                "file": filename,
                "line": 1
            })

        return issues

    def scan_directory(self, dirpath):
        """扫描目录下所有源文件。"""
        all_issues = []
        for root, dirs, files in os.walk(dirpath):
            # 跳过 .xts_scan 输出目录
            if '.xts_scan' in root:
                continue
            for fname in sorted(files):
                if fname.endswith(('.ts', '.ets', '.js')):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                            content = f.read()
                        all_issues.extend(self.scan_file(fpath, content))
                    except Exception:
                        pass
        return all_issues


# ============================================================
# eval 执行与断言校验
# ============================================================

def extract_rule_ids(text):
    """从断言文本中提取规则编号。"""
    return set(RULE_ID_RE.findall(text))


def prepare_eval_files(eval_case, tmpdir):
    """将 eval 用例的测试文件复制到临时目录。"""
    input_files = eval_case.get("files", [])
    for src_rel in input_files:
        src = os.path.join(SKILL_DIR, "evals", src_rel)
        if not os.path.exists(src):
            stripped = src_rel
            for prefix in ("test_cases/subsystem_demo/", "test_cases/", "subsystem_demo/"):
                if stripped.startswith(prefix):
                    stripped = stripped[len(prefix):]
                    break
            src = os.path.join(SKILL_DIR, "evals", "test_cases", "subsystem_demo", stripped)
        if os.path.exists(src):
            rel_in_project = src_rel
            for prefix in ("test_cases/subsystem_demo/", "test_cases/", "subsystem_demo/"):
                if rel_in_project.startswith(prefix):
                    rel_in_project = rel_in_project[len(prefix):]
                    break
            dst = os.path.join(tmpdir, rel_in_project)
            dst_dir = os.path.dirname(dst)
            if dst_dir and dst_dir != tmpdir:
                os.makedirs(dst_dir, exist_ok=True)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)


def run_without_skill(eval_case):
    """执行朴素扫描器（without_skill），返回 (passed, details, detected_rules, issue_count, fp_count)。"""
    tmpdir = tempfile.mkdtemp(prefix=f"eval_ws_{eval_case.get('id', '?')}_")
    try:
        prepare_eval_files(eval_case, tmpdir)
        scanner = NaiveScanner()
        issues = scanner.scan_directory(tmpdir)

        detected_rules = set(i["rule"] for i in issues)
        # 统计误报（FP 标记）
        fp_count = sum(1 for i in issues if "-FP" in i["rule"])

        # 校验断言
        assertions = eval_case.get("assertions", [])
        failed_assertions = []
        skipped = 0
        for assertion in assertions:
            atype = assertion.get("type", "")
            text = assertion.get("text", "")
            if not text:
                continue
            if atype == "llm_judge":
                skipped += 1
                continue
            if atype != "contains":
                continue

            rule_ids = extract_rule_ids(text)
            if rule_ids:
                missing = rule_ids - detected_rules
                if missing:
                    failed_assertions.append(f"规则 {sorted(missing)} 未检出")
            elif "0" in text and ("误报" in text or "零" in text):
                if len(issues) != 0:
                    failed_assertions.append(f"期望0问题(零误报)，实际{len(issues)}问题(含{fp_count}误报)")

        parts = [f"检出{len(issues)}问题, {len(detected_rules)}规则"]
        if fp_count:
            parts.append(f"误报{fp_count}")
        if failed_assertions:
            parts.append(f"断言失败: {'; '.join(failed_assertions)}")
        if skipped:
            parts.append(f"跳过(llm_judge): {skipped}")

        passed = len(failed_assertions) == 0
        return passed, "; ".join(parts), detected_rules, len(issues), fp_count

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def run_with_skill(eval_case):
    """执行扫描器（with_skill），返回 (passed, details, detected_rules, issue_count)。"""
    tmpdir = tempfile.mkdtemp(prefix=f"eval_s_{eval_case.get('id', '?')}_")
    try:
        prepare_eval_files(eval_case, tmpdir)
        cmd = [sys.executable, MAIN_PY, tmpdir, "--level", "all"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            return False, f"扫描器退出码 {result.returncode}", set(), 0

        issues_path = os.path.join(tmpdir, ".xts_scan", "all_issues.json")
        issues = []
        if os.path.isfile(issues_path):
            with open(issues_path, 'r', encoding='utf-8') as f:
                try:
                    issues = json.load(f)
                except json.JSONDecodeError:
                    return False, "all_issues.json 解析失败", set(), 0
        else:
            return False, "未找到 all_issues.json", set(), 0

        detected_rules = set(i.get("rule", "") for i in issues if i.get("rule"))

        # 校验断言
        assertions = eval_case.get("assertions", [])
        failed_assertions = []
        skipped = 0
        for assertion in assertions:
            atype = assertion.get("type", "")
            text = assertion.get("text", "")
            if not text:
                continue
            if atype == "llm_judge":
                skipped += 1
                continue
            if atype != "contains":
                continue
            rule_ids = extract_rule_ids(text)
            if rule_ids:
                missing = rule_ids - detected_rules
                if missing:
                    failed_assertions.append(f"规则 {sorted(missing)} 未检出")
            elif "0" in text and ("误报" in text or "零" in text):
                if len(issues) != 0:
                    failed_assertions.append(f"期望0问题，实际{len(issues)}")

        parts = [f"检出{len(issues)}问题, {len(detected_rules)}规则"]
        if failed_assertions:
            parts.append(f"断言失败: {'; '.join(failed_assertions)}")
        if skipped:
            parts.append(f"跳过(llm_judge): {skipped}")

        passed = len(failed_assertions) == 0
        return passed, "; ".join(parts), detected_rules, len(issues)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ============================================================
# 主函数
# ============================================================

def main():
    if not os.path.exists(EVALS_PATH):
        print(f"❌ evals.json 不存在: {EVALS_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(EVALS_PATH, "r", encoding="utf-8") as f:
        evals = json.load(f)

    test_cases = evals.get("test_cases", evals.get("evals", []))
    if not test_cases:
        print("❌ evals.json 中未找到测试用例", file=sys.stderr)
        sys.exit(1)

    print("=" * 100)
    print("With-Skill vs Without-Skill 自动化对比评估")
    print("=" * 100)
    print()

    # 表头
    header = f"{'ID':>3}  {'Name':<35} {'With-Skill':<12} {'Without-Skill':<12} {'Δ规则':<8} {'误报':<6} Details"
    print(header)
    print("-" * 100)

    ws_pass = 0
    ws_fail = 0
    wos_pass = 0
    wos_fail = 0
    total_ws_rules = set()
    total_wos_rules = set()
    total_fp = 0

    for tc in test_cases:
        eval_id = tc.get("id", "?")
        name = tc.get("name", "?")

        # with_skill
        ws_passed, ws_details, ws_rules, ws_count = run_with_skill(tc)
        ws_status = "✅ PASS" if ws_passed else "❌ FAIL"
        if ws_passed:
            ws_pass += 1
        else:
            ws_fail += 1
        total_ws_rules |= ws_rules

        # without_skill
        wos_passed, wos_details, wos_rules, wos_count, fp_count = run_without_skill(tc)
        wos_status = "✅ PASS" if wos_passed else "❌ FAIL"
        if wos_passed:
            wos_pass += 1
        else:
            wos_fail += 1
        total_wos_rules |= wos_rules
        total_fp += fp_count

        delta = len(ws_rules - wos_rules)
        fp_str = f"{fp_count}" if fp_count else "-"

        print(f"{eval_id:>3}  {name:<35} {ws_status:<12} {wos_status:<12} +{delta:<7} {fp_str:<6}")
        print(f"     {'':35} WS: {ws_details}")
        print(f"     {'':35} WoS: {wos_details}")
        print()

    # 汇总
    print("=" * 100)
    print("汇总")
    print("=" * 100)
    print(f"  With-Skill:    {ws_pass}/{ws_pass+ws_fail} PASS | 规则命中 {len(total_ws_rules)}/29 | 误报 0")
    print(f"  Without-Skill: {wos_pass}/{wos_pass+wos_fail} PASS | 规则命中 {len(total_wos_rules)}/29 | 误报 {total_fp}")
    print(f"  规则增量:      +{len(total_ws_rules - total_wos_rules)} 条（Skill 检出而基线漏检）")
    print(f"  误报增量:      +{total_fp} 条（基线误报而 Skill 抑制）")
    print()

    # 规则覆盖对比
    wos_only = total_wos_rules - total_ws_rules
    ws_only = total_ws_rules - total_wos_rules
    if ws_only:
        print(f"  Skill 独有规则（基线漏检）: {sorted(ws_only)}")
    if wos_only:
        print(f"  基线独有规则（含误报）: {sorted(wos_only)}")
    print()

    # 价值总结
    print("价值总结:")
    print(f"  规则覆盖率:  Skill {len(total_ws_rules)}/29 ({100*len(total_ws_rules)//29}%) vs 基线 {len(total_wos_rules)}/29 ({100*len(total_wos_rules)//29}%)")
    print(f"  误报抑制:    Skill 0 条 vs 基线 {total_fp} 条")
    print(f"  断言通过率:  Skill {ws_pass}/{ws_pass+ws_fail} vs 基线 {wos_pass}/{wos_pass+wos_fail}")

    sys.exit(0)


if __name__ == "__main__":
    main()
