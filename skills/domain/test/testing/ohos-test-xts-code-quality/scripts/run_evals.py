#!/usr/bin/env python3
"""
run_evals.py - 可执行的 eval 回归测试运行器

用法:
    python3 scripts/run_evals.py                    # with_skill: 运行扫描器 + 断言校验
    python3 scripts/run_evals.py --without-skill    # 输出 without_skill prompt pack JSON

功能:
    with_skill 模式（默认）: 对 evals.json 中每个用例，复制 files 到临时目录，
        执行扫描入口 main.py，读取 .xts_scan/all_issues.json，
        对 contains 类型断言做自动校验（提取规则编号比对检出结果），输出 pass/fail 表格。
    without_skill 模式: 输出各 eval 的 prompt + 预期断言 JSON 至 stdout，
        供无 Skill 基线 LLM 手动执行后与 with_skill 结果比对（不自动运行 LLM，不产生孤儿文件）。

退出码: 0=全部通过(或 prompt pack 输出成功), 1=有失败, 2=配置错误
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


def extract_rule_ids(text):
    """从断言文本中提取规则编号（R001-R023, R201-R206）。"""
    return set(RULE_ID_RE.findall(text))


def run_eval_with_skill(eval_case):
    """执行单个 eval 用例（with_skill），返回 (passed, details, detected_rules)。"""
    eval_id = eval_case.get("id", "?")
    name = eval_case.get("name", "?")
    input_files = eval_case.get("files", [])
    assertions = eval_case.get("assertions", [])

    tmpdir = tempfile.mkdtemp(prefix=f"eval_{eval_id}_")
    try:
        for src_rel in input_files:
            # 解析源文件路径：evals.json 中路径形如 test_cases/subsystem_demo/xxx
            src = os.path.join(SKILL_DIR, "evals", src_rel)
            if not os.path.exists(src):
                # 回退：剥离已知前缀后在 subsystem_demo 下查找
                stripped = src_rel
                for prefix in ("test_cases/subsystem_demo/", "test_cases/", "subsystem_demo/"):
                    if stripped.startswith(prefix):
                        stripped = stripped[len(prefix):]
                        break
                src = os.path.join(SKILL_DIR, "evals", "test_cases", "subsystem_demo", stripped)
            if os.path.exists(src):
                # 保留子目录结构（pages/、signature/），R019/R020 需路径含 /pages/
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

        # 执行扫描入口（不传 --json，main.py 不支持该参数；结果写入 .xts_scan/）
        cmd = [sys.executable, MAIN_PY, tmpdir, "--level", "all"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            return False, f"扫描器退出码 {result.returncode}: {result.stderr[:200]}", set()

        # 读取 .xts_scan/all_issues.json（main.py 总是生成此文件，即使0问题）
        issues_path = os.path.join(tmpdir, ".xts_scan", "all_issues.json")
        issues = []
        if os.path.isfile(issues_path):
            with open(issues_path, 'r', encoding='utf-8') as f:
                try:
                    issues = json.load(f)
                except json.JSONDecodeError:
                    return False, f"all_issues.json 解析失败", set()
        else:
            return False, "未找到 .xts_scan/all_issues.json（扫描可能异常退出）", set()

        detected_rules = set(i.get("rule", "") for i in issues if i.get("rule"))

        # 校验断言
        failed_assertions = []
        skipped_count = 0
        for assertion in assertions:
            atype = assertion.get("type", "")
            text = assertion.get("text", "")
            if not text:
                continue
            if atype == "llm_judge":
                skipped_count += 1
                continue
            if atype != "contains":
                continue

            # 提取断言中的规则编号
            rule_ids = extract_rule_ids(text)
            if rule_ids:
                missing = rule_ids - detected_rules
                if missing:
                    failed_assertions.append(f"规则 {sorted(missing)} 未检出 ({text})")
            elif "0" in text and ("误报" in text or "零" in text):
                # 零误报断言：检查总问题数为0
                if len(issues) != 0:
                    failed_assertions.append(f"期望0问题，实际{len(issues)} ({text})")
            # 其他 contains 断言无规则编号且非零误报检查：跳过（无法自动校验）

        details_parts = []
        if failed_assertions:
            details_parts.append(f"断言失败: {'; '.join(failed_assertions)}")
        details_parts.append(f"检出{len(issues)}问题, {len(detected_rules)}规则")
        if skipped_count:
            details_parts.append(f"跳过(llm_judge): {skipped_count}")

        passed = len(failed_assertions) == 0
        return passed, "; ".join(details_parts), detected_rules

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def output_without_skill_prompts(test_cases):
    """输出 without_skill prompt pack JSON 至 stdout（供无 Skill 基线 LLM 手动执行）。

    不创建任何文件（避免孤儿文件），仅输出 JSON 到 stdout，
    用户可重定向到文件或管道给 LLM。
    """
    prompt_pack = []
    for tc in test_cases:
        prompt_pack.append({
            "id": tc.get("id", "?"),
            "name": tc.get("name", "?"),
            "prompt": tc.get("prompt", ""),
            "files": tc.get("files", []),
            "file_root": os.path.join(SKILL_DIR, "evals", "test_cases", "subsystem_demo"),
            "expected_output": tc.get("expected_output", ""),
            "assertions": [
                {"text": a.get("text", ""), "type": a.get("type", "")}
                for a in tc.get("assertions", [])
            ],
        })
    print(json.dumps(prompt_pack, ensure_ascii=False, indent=2))
    print(f"\n# without_skill prompt pack 已输出（{len(prompt_pack)} 个 eval）", file=sys.stderr)
    print("# 将上述 JSON 喂给无 Skill 的 LLM 执行，记录其检出规则后与 with_skill 结果比对", file=sys.stderr)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='XTS eval 回归测试运行器')
    parser.add_argument('--without-skill', action='store_true',
                        help='输出 without_skill prompt pack JSON（不运行扫描器，不产生文件）')
    args = parser.parse_args()

    if not os.path.exists(EVALS_PATH):
        print(f"❌ evals.json 不存在: {EVALS_PATH}", file=sys.stderr)
        sys.exit(2)

    with open(EVALS_PATH, "r", encoding="utf-8") as f:
        evals = json.load(f)

    test_cases = evals.get("test_cases", evals.get("evals", []))
    if not test_cases:
        print("❌ evals.json 中未找到测试用例", file=sys.stderr)
        sys.exit(2)

    # without_skill 模式：输出 prompt pack JSON 到 stdout
    if args.without_skill:
        output_without_skill_prompts(test_cases)
        sys.exit(0)

    # with_skill 模式：运行扫描器 + 断言校验
    print(f"{'ID':>3}  {'Name':<40} {'Result':<8} Details")
    print("=" * 90)

    passed_count = 0
    failed_count = 0

    for tc in test_cases:
        eval_id = tc.get("id", "?")
        name = tc.get("name", "?")
        passed, details, _ = run_eval_with_skill(tc)
        status = "✅ PASS" if passed else "❌ FAIL"
        if passed:
            passed_count += 1
        else:
            failed_count += 1
        print(f"{eval_id:>3}  {name:<40} {status:<8} {details}")

    print("=" * 90)
    print(f"总计: {passed_count} 通过, {failed_count} 失败")

    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
