#!/usr/bin/env python3
"""
Phase Execution Tracker - Phase 执行状态追踪机制

维护 phase_progress.json 文件，记录每个 Phase 的执行状态。
确保 Phase 按序执行，关键 Phase（4, 7）不可跳过。

用法:
  python phase_tracker.py init                                    # 初始化新的追踪文件
  python phase_tracker.py start <phase> [--output <path>]         # 标记 Phase 开始
  python phase_tracker.py complete <phase> [--output <path>]      # 标记 Phase 完成
  python phase_tracker.py skip <phase> --reason <reason>          # 标记 Phase 跳过（强制 Phase 不可跳过）
  python phase_tracker.py check <phase>                           # 检查前置 Phase 是否完成
  python phase_tracker.py status                                  # 显示所有 Phase 状态
  python phase_tracker.py report                                  # 生成工作流执行检查清单
"""

import argparse
import json
import os
import sys
from datetime import datetime

MANDATORY_PHASES = [4, 7]
ALL_PHASES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
PHASE_NAMES = {
    0: "Init Config",
    1: "Task Config & Subsystem",
    2: "Initial Coverage Scan",
    3: "Targeted API Info Parsing",
    4: "Generate Test Design",
    5: "Generate Test Cases",
    6: "Register Test Suites",
    7: "Format & Validate",
    8: "Build Verification",
    9: "Test Execution & Failure Analysis",
    10: "Coverage Verification",
    11: "Output Results",
}

PROGRESS_FILE = "phase_progress.json"


def get_progress_path(output_dir: str) -> str:
    return os.path.join(output_dir, PROGRESS_FILE)


def load_progress(output_dir: str) -> dict:
    path = get_progress_path(output_dir)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_progress(output_dir: str, data: dict):
    os.makedirs(output_dir, exist_ok=True)
    path = get_progress_path(output_dir)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_init(output_dir: str):
    data = {
        "created_at": datetime.now().isoformat(),
        "current_phase": 0,
        "phases": {},
    }
    for p in ALL_PHASES:
        data["phases"][str(p)] = {
            "status": "pending",
            "timestamp": None,
            "output": None,
            "note": None,
        }
    save_progress(output_dir, data)
    print(f"✅ 已初始化 Phase 追踪文件: {get_progress_path(output_dir)}")


def cmd_start(output_dir: str, phase: int):
    data = load_progress(output_dir)
    if data is None:
        print("❌ 追踪文件不存在，请先执行 init")
        sys.exit(1)

    phase_key = str(phase)

    if not check_prerequisites(data, phase):
        sys.exit(1)

    data["current_phase"] = phase
    data["phases"][phase_key] = {
        "status": "in_progress",
        "timestamp": datetime.now().isoformat(),
        "output": None,
        "note": None,
    }
    save_progress(output_dir, data)
    print(f"▶️ Phase {phase} [{PHASE_NAMES.get(phase, '')}] 已开始")


def cmd_complete(output_dir: str, phase: int, output: str = None):
    data = load_progress(output_dir)
    if data is None:
        print("❌ 追踪文件不存在，请先执行 init")
        sys.exit(1)

    phase_key = str(phase)
    entry = data["phases"].get(phase_key, {})
    entry["status"] = "completed"
    entry["completed_at"] = datetime.now().isoformat()
    if output:
        entry["output"] = output

    data["phases"][phase_key] = entry

    next_phase = phase + 1
    if next_phase <= 11:
        data["current_phase"] = next_phase
    else:
        data["current_phase"] = -1

    save_progress(output_dir, data)
    print(f"✅ Phase {phase} [{PHASE_NAMES.get(phase, '')}] 已完成")


def cmd_skip(output_dir: str, phase: int, reason: str):
    if phase in MANDATORY_PHASES:
        print(f"🚫 Phase {phase} [{PHASE_NAMES.get(phase, '')}] 是强制 Phase，不允许跳过！")
        print(f"   原因: Phase {phase} 是工作流的关键质量保证环节。")
        sys.exit(1)

    data = load_progress(output_dir)
    if data is None:
        print("❌ 追踪文件不存在，请先执行 init")
        sys.exit(1)

    phase_key = str(phase)
    data["phases"][phase_key] = {
        "status": "skipped",
        "timestamp": datetime.now().isoformat(),
        "output": None,
        "note": reason,
    }
    next_phase = phase + 1
    if next_phase <= 11:
        data["current_phase"] = next_phase
    save_progress(output_dir, data)
    print(f"⏭️ Phase {phase} [{PHASE_NAMES.get(phase, '')}] 已跳过: {reason}")


def check_prerequisites(data: dict, phase: int) -> bool:
    if phase == 0:
        return True

    # Phase 1 可在 Phase 0 跳过时直接执行（配置文件已存在）
    if phase == 1:
        prev_entry = data["phases"].get("0", {})
        prev_status = prev_entry.get("status", "pending")
        # Phase 0 未执行或跳过时，允许直接执行 Phase 1
        return prev_status in ("completed", "skipped", "pending")

    prev_phase = phase - 1
    prev_key = str(prev_phase)
    prev_entry = data["phases"].get(prev_key, {})
    prev_status = prev_entry.get("status", "pending")

    if prev_status in ("completed", "skipped"):
        return True

    if prev_status == "pending":
        print(f"❌ Phase {phase} 的前置 Phase {prev_phase} [{PHASE_NAMES.get(prev_phase, '')}] 尚未执行！")
        print(f"   请先执行 Phase {prev_phase}。")
        return False

    if prev_status == "in_progress":
        print(f"⚠️ Phase {phase} 的前置 Phase {prev_phase} [{PHASE_NAMES.get(prev_phase, '')}] 仍在执行中。")
        print(f"   请等待 Phase {prev_phase} 完成后再继续。")
        return False

    return True


def cmd_check(output_dir: str, phase: int):
    data = load_progress(output_dir)
    if data is None:
        print("❌ 追踪文件不存在，请先执行 init")
        sys.exit(1)

    if check_prerequisites(data, phase):
        print(f"✅ Phase {phase} 前置条件满足，可以开始执行")
    else:
        sys.exit(1)


def cmd_status(output_dir: str):
    data = load_progress(output_dir)
    if data is None:
        print("❌ 追踪文件不存在，请先执行 init")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Phase 执行状态追踪")
    print(f"  创建时间: {data.get('created_at', 'N/A')}")
    print(f"  当前 Phase: {data.get('current_phase', 'N/A')}")
    print(f"{'='*60}\n")

    status_icons = {
        "pending": "⬜",
        "in_progress": "🔄",
        "completed": "✅",
        "skipped": "⏭️",
    }

    for p in ALL_PHASES:
        entry = data["phases"].get(str(p), {})
        status = entry.get("status", "pending")
        icon = status_icons.get(status, "?")
        mandatory = " [MANDATORY]" if p in MANDATORY_PHASES else ""
        timestamp = entry.get("timestamp", "") or entry.get("completed_at", "")
        note = entry.get("note", "")
        time_str = f" ({timestamp[:19]})" if timestamp else ""
        note_str = f" — {note}" if note else ""

        print(f"  {icon} Phase {p:>2}: {PHASE_NAMES.get(p, 'Unknown'):<35}{mandatory}{time_str}{note_str}")

    print()


def cmd_report(output_dir: str):
    data = load_progress(output_dir)
    if data is None:
        print("❌ 追踪文件不存在，请先执行 init")
        sys.exit(1)

    print("\n## 工作流执行检查清单\n")

    checks = [
        ("Phase 0 配置初始化", lambda d: d["phases"].get("0", {}).get("status") in ("completed", "skipped", "pending") or True),
        ("Phase 1 任务配置", lambda d: d["phases"]["1"]["status"] == "completed"),
        ("Phase 2 覆盖率扫描", lambda d: d["phases"]["2"]["status"] in ("completed", "skipped")),
        ("Phase 3 API 解析", lambda d: d["phases"]["3"]["status"] in ("completed", "skipped")),
        ("Phase 4 测试设计文档", lambda d: d["phases"]["4"]["status"] == "completed"),
        ("Phase 5 测试代码生成", lambda d: d["phases"]["5"]["status"] in ("completed", "skipped")),
        ("Phase 6 测试注册", lambda d: d["phases"]["6"]["status"] in ("completed", "skipped")),
        ("Phase 7 格式验证", lambda d: d["phases"]["7"]["status"] == "completed"),
        ("Phase 8 编译验证", lambda d: d["phases"]["8"]["status"] in ("completed", "skipped")),
        ("Phase 9 测试执行与分析", lambda d: d["phases"]["9"]["status"] in ("completed", "skipped")),
        ("Phase 10 覆盖率对比", lambda d: d["phases"]["10"]["status"] in ("completed", "skipped")),
        ("Phase 11 结果输出", lambda d: d["phases"]["11"]["status"] in ("completed", "skipped")),
    ]

    all_pass = True
    for name, check_fn in checks:
        passed = check_fn(data)
        icon = "✅" if passed else "❌"
        status = "通过" if passed else "未通过"
        print(f"| {icon} | {name:<30} | {status:<10} |")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("✅ 所有检查项通过")
    else:
        print("❌ 存在未通过的检查项，请补充执行")
    print()


def add_output_arg(parser):
    parser.add_argument("--output", default=".coverage_data", help="输出目录（默认 .coverage_data）")


def main():
    parser = argparse.ArgumentParser(description="Phase Execution Tracker")

    subparsers = parser.add_subparsers(dest="command", help="命令")

    p_init = subparsers.add_parser("init", help="初始化追踪文件")
    add_output_arg(p_init)

    p_start = subparsers.add_parser("start", help="标记 Phase 开始")
    p_start.add_argument("phase", type=int, help="Phase 编号 (0-11)")
    add_output_arg(p_start)

    p_complete = subparsers.add_parser("complete", help="标记 Phase 完成")
    p_complete.add_argument("phase", type=int, help="Phase 编号 (0-11)")
    p_complete.add_argument("--output-file", help="Phase 输出文件路径")
    add_output_arg(p_complete)

    p_skip = subparsers.add_parser("skip", help="标记 Phase 跳过（强制 Phase 不可跳过）")
    p_skip.add_argument("phase", type=int, help="Phase 编号 (0-11)")
    p_skip.add_argument("--reason", required=True, help="跳过原因")
    add_output_arg(p_skip)

    p_check = subparsers.add_parser("check", help="检查前置 Phase 是否完成")
    p_check.add_argument("phase", type=int, help="Phase 编号 (0-11)")
    add_output_arg(p_check)

    p_status = subparsers.add_parser("status", help="显示所有 Phase 状态")
    add_output_arg(p_status)

    p_report = subparsers.add_parser("report", help="生成工作流执行检查清单")
    add_output_arg(p_report)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    output_dir = args.output

    if args.command == "init":
        cmd_init(output_dir)
    elif args.command == "start":
        cmd_start(output_dir, args.phase)
    elif args.command == "complete":
        cmd_complete(output_dir, args.phase, getattr(args, "output_file", None))
    elif args.command == "skip":
        cmd_skip(output_dir, args.phase, args.reason)
    elif args.command == "check":
        cmd_check(output_dir, args.phase)
    elif args.command == "status":
        cmd_status(output_dir)
    elif args.command == "report":
        cmd_report(output_dir)


if __name__ == "__main__":
    main()
