#!/usr/bin/env python3
"""校验 evals.json 的 ground truth 与 evals/inputs/ 下的 fixture 是否一致。

评测判分规则要求"命中位置必须在植入位置 ±3 行内"，因此植入行号一旦与 fixture 脱节，
判分结论就失去意义（历史缺陷：fixture 中模板字符串缺陷在第 46 行，evals.json 仍写第 42 行，
偏差 4 行，评测却判为通过）。

本脚本在 CI/本地做两件事：
1. 每条 planted_defect 必须声明 file/line/probe，且 probe 字符串确实出现在该文件该行的内容里；
2. expectations 文本里出现的行号必须落在同用例某条植入行号的 ±3 行窗口内（区间只要与窗口相交即可）。

用法：
    python3 evals/check_ground_truth.py            # 在 skill 根目录或任意位置执行均可
    python3 evals/check_ground_truth.py --verbose
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOLERANCE = 3
REQUIRED_DEFECT_FIELDS = ("type", "file", "line", "probe")
LINE_REF_PATTERNS = (
    re.compile(r"第\s*(\d+)(?:\s*[-–~]\s*(\d+))?\s*行"),
    re.compile(r"\bL(\d+)(?:\s*[-–~]\s*L?(\d+))?\b"),
)


def find_skill_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "evals" / "evals.json").exists():
            return candidate
    raise SystemExit(f"未找到 evals/evals.json（从 {start} 向上查找）")


def load_cases(root: Path) -> list[dict]:
    data = json.loads((root / "evals" / "evals.json").read_text(encoding="utf-8"))
    return data.get("evals", [])


def read_lines(root: Path, relative: str) -> list[str] | None:
    path = root / relative
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").split("\n")


def check_defects(case: dict, root: Path, verbose: bool) -> list[str]:
    errors: list[str] = []
    case_id = case.get("id", "<unknown>")

    for relative in case.get("files", []):
        if read_lines(root, relative) is None:
            errors.append(f"[{case_id}] files 中的输入文件不存在：{relative}")

    for index, defect in enumerate(case.get("planted_defects", [])):
        missing = [field for field in REQUIRED_DEFECT_FIELDS if not defect.get(field)]
        if missing:
            errors.append(f"[{case_id}] planted_defects[{index}] 缺少字段：{', '.join(missing)}")
            continue

        relative, line, probe = defect["file"], int(defect["line"]), defect["probe"]
        lines = read_lines(root, relative)
        if lines is None:
            errors.append(f"[{case_id}] planted_defects[{index}] 指向的文件不存在：{relative}")
            continue
        if line < 1 or line > len(lines):
            errors.append(
                f"[{case_id}] planted_defects[{index}] 行号越界：{relative}:{line}（文件共 {len(lines)} 行）"
            )
            continue

        actual = lines[line - 1]
        if probe not in actual:
            errors.append(
                f"[{case_id}] ground truth 过期：{relative}:{line} 不含 probe {probe!r}\n"
                f"      实际内容：{actual.strip()[:120]}\n"
                f"      修复方式：更新 planted_defects[{index}] 的 line/probe 使其与 fixture 一致"
            )
            continue
        if verbose:
            print(f"  OK  [{case_id}] {relative}:{line} ← {probe!r}")

    return errors


def check_expectation_lines(case: dict, root: Path, verbose: bool) -> list[str]:
    errors: list[str] = []
    case_id = case.get("id", "<unknown>")
    planted = [int(d["line"]) for d in case.get("planted_defects", []) if d.get("line")]
    if not planted:
        return errors

    for expectation in case.get("expectations", []):
        for pattern in LINE_REF_PATTERNS:
            for match in pattern.finditer(expectation):
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else start
                if end < start:
                    start, end = end, start
                hit = next((p for p in planted if start - TOLERANCE <= p <= end + TOLERANCE), None)
                if hit is None:
                    errors.append(
                        f"[{case_id}] expectations 中的行号 {match.group(0)} 与植入行号 {planted} "
                        f"相差超过 ±{TOLERANCE} 行，判分结论不可信"
                    )
                elif verbose:
                    print(f"  OK  [{case_id}] {match.group(0)} ← 植入行 {hit}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 evals.json ground truth 与 fixture 的一致性")
    parser.add_argument("--verbose", "-v", action="store_true", help="打印每一条通过校验的记录")
    parser.add_argument("--skill-root", type=Path, default=None, help="skill 根目录（默认自动定位）")
    args = parser.parse_args()

    start = (args.skill_root or Path(__file__).resolve().parent.parent).resolve()
    root = find_skill_root(start)
    cases = load_cases(root)

    print(f"skill root : {root}")
    print(f"eval cases : {len(cases)}")
    print(f"tolerance  : ±{TOLERANCE} lines\n")

    errors: list[str] = []
    for case in cases:
        errors.extend(check_defects(case, root, args.verbose))
        errors.extend(check_expectation_lines(case, root, args.verbose))

    if errors:
        print(f"FAIL：{len(errors)} 处 ground truth 与 fixture 不一致\n")
        for error in errors:
            print(f" - {error}")
        return 1

    total = sum(len(case.get("planted_defects", [])) for case in cases)
    print(f"PASS：{len(cases)} 个用例、{total} 条植入缺陷的行号与 probe 全部与 fixture 一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
