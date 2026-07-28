#!/usr/bin/env python3
"""
Timing & Checkpoint Helper - 测试设计流程计时与检查点协议操作工具

按 ohos-design-test-task-manager 协议操作 {输出目录}/tasks/ 下的 timing.json
与 task_checkpoints/ 文件，供 ohos-design-test-coordinator 调用或用户独立排查使用。

用法:
  python timing_helper.py record --output <dir> --phase <key> --point <field> [--value <n>]
      采集某计时机，写入 timing.json 对应字段（epoch 秒，等价 date +%s）。
      --point 可选: phase_started_at / agent_completed_at / confirmation_started_at
                   / confirmation_completed_at / phase_completed_at
                   / optimization_round（自增1） / optimization_duration（累加 --value）
  python timing_helper.py checkpoint save --output <dir> --phase <key> --artifact name=path [--artifact ...] [--status <status>]
      保存检查点（含保存前检查清单校验：输出文件可读、timing 完整、前序检查点存在）。
  python timing_helper.py resume --output <dir>
      扫描检查点目录，按 phase 编号排序输出恢复起始点（输出缺失时降级到前一检查点）。
  python timing_helper.py report --output <dir>
      读取 timing.json 生成计时报告（markdown 表格）。

phase key 取值: phase1 / phase2 / phase2_adv / phase3-1 / phase3-2 / phase3-3
                / phase4 / phase4_adv / phase5
"""

import argparse
import json
import os
import sys
import time

PHASE_NAMES = {
    "phase1": "阶段1：需求解析",
    "phase2": "阶段2：测试点生成",
    "phase2_adv": "阶段2：对抗评估",
    "phase3-1": "阶段3-子阶段1：Demo UI设计",
    "phase3-2": "阶段3-子阶段2：Demo代码生成",
    "phase3-3": "阶段3-子阶段3：编译验证",
    "phase4": "阶段4：用例细化",
    "phase4_adv": "阶段4：对抗评估",
    "phase5": "阶段5：验证导出",
}

PHASE_ORDER = ["phase1", "phase2", "phase2_adv", "phase3-1", "phase3-2", "phase3-3",
               "phase4", "phase4_adv", "phase5"]

CHECKPOINT_FILES = {
    "phase1": "phase1_requirement_checkpoint.json",
    "phase2": "phase2_testpoint_checkpoint.json",
    "phase3-1": "phase3_demo_checkpoint.json",
    "phase3-2": "phase3_demo_checkpoint.json",
    "phase3-3": "phase3_demo_checkpoint.json",
    "phase4": "phase4_testcase_checkpoint.json",
    "phase5": "phase5_validate_checkpoint.json",
}

TIMING_FILE = "timing.json"
CHECKPOINT_DIR = "task_checkpoints"
PHASE_NUM_FIELD = "phase"  # checkpoint.phase int


def tasks_dir(output_dir: str) -> str:
    return os.path.join(output_dir, "tasks")


def timing_path(output_dir: str) -> str:
    return os.path.join(tasks_dir(output_dir), TIMING_FILE)


def checkpoint_dir(output_dir: str) -> str:
    return os.path.join(tasks_dir(output_dir), CHECKPOINT_DIR)


def phase_number(key: str) -> int:
    # 单调递增编号，用于恢复排序（phase3 子步骤合并到同一检查点文件但编号递增）
    order = {k: i for i, k in enumerate(PHASE_ORDER, start=1)}
    return order.get(key, 0)


def now_epoch() -> int:
    return int(time.time())


def load_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_or_create_phase(timing: dict, phase_key: str) -> dict:
    name = PHASE_NAMES[phase_key]
    phases = timing.setdefault("phases", [])
    for p in phases:
        if p.get("name") == name:
            return p
    entry = {
        "name": name,
        "phase_started_at": 0,
        "agent_completed_at": 0,
        "confirmation_started_at": 0,
        "confirmation_completed_at": 0,
        "phase_completed_at": 0,
        "optimization_rounds": 0,
        "optimization_duration_seconds": 0,
    }
    phases.append(entry)
    return entry


def cmd_record(args) -> int:
    if args.phase not in PHASE_NAMES:
        print(f"❌ 未知 phase key: {args.phase}，可选: {' / '.join(PHASE_ORDER)}", file=sys.stderr)
        return 2
    path = timing_path(args.output)
    timing = load_json(path, default={})
    if timing is None:
        print(f"❌ timing.json 损坏无法解析: {path}", file=sys.stderr)
        timing = {"pipeline_started_at": 0, "pipeline_completed_at": 0, "phases": []}
    if timing.get("pipeline_started_at", 0) == 0:
        timing["pipeline_started_at"] = now_epoch()

    entry = find_or_create_phase(timing, args.phase)
    point = args.point
    if point == "optimization_round":
        entry["optimization_rounds"] = int(entry.get("optimization_rounds", 0)) + 1
    elif point == "optimization_duration":
        if args.value is None:
            print("❌ optimization_duration 需 --value <秒数>", file=sys.stderr)
            return 2
        entry["optimization_duration_seconds"] = (
            int(entry.get("optimization_duration_seconds", 0)) + int(args.value)
        )
    elif point in ("phase_started_at", "agent_completed_at",
                   "confirmation_started_at", "confirmation_completed_at", "phase_completed_at"):
        entry[point] = now_epoch()
        if point == "phase_completed_at":
            timing["pipeline_completed_at"] = (
                entry[point] if args.phase == "phase5" else timing.get("pipeline_completed_at", 0)
            )
    else:
        print(f"❌ 未知 timing point: {point}", file=sys.stderr)
        return 2

    save_json(path, timing)
    print(f"✅ 已记录 {args.phase}.{point} = {entry.get(point, args.value)} -> {path}")
    return 0


def _readable(path: str) -> bool:
    return os.path.exists(path) and os.access(path, os.R_OK)


def cmd_checkpoint_save(args) -> int:
    if args.phase not in PHASE_NAMES:
        print(f"❌ 未知 phase key: {args.phase}", file=sys.stderr)
        return 2
    output_dir = args.output
    cdir = checkpoint_dir(output_dir)
    os.makedirs(cdir, exist_ok=True)

    errors = []
    # 1. 输出文件可读性校验
    outputs = {}
    for spec in args.artifact or []:
        if "=" not in spec:
            errors.append(f"artifact 格式错误（需 name=path）: {spec}")
            continue
        name, p = spec.split("=", 1)
        outputs[name] = p
        if not _readable(p):
            errors.append(f"输出文件不可读: {name}={p}")

    # 2. timing 完整性（非关键，仅告警）
    timing = load_json(timing_path(output_dir), default={})
    entry = None
    if timing and "phases" in timing:
        for p in timing["phases"]:
            if p.get("name") == PHASE_NAMES[args.phase]:
                entry = p
                break
    timing_ok = bool(entry and entry.get("phase_started_at", 0) > 0
                     and entry.get("phase_completed_at", 0) > 0)
    if entry and not timing_ok:
        print(f"⚠️ timing 不完整（phase_started_at/phase_completed_at 须 > 0），仍允许保存", file=sys.stderr)

    # 3. 前序检查点存在性
    idx = PHASE_ORDER.index(args.phase)
    if idx > 0:
        prev_key = PHASE_ORDER[idx - 1]
        prev_file = os.path.join(cdir, CHECKPOINT_FILES.get(prev_key, ""))
        if not os.path.exists(prev_file):
            print(f"⚠️ 前序检查点缺失: {prev_key} ({prev_file})，告警但允许继续", file=sys.stderr)

    if errors:
        print("❌ 保存前检查清单未通过：", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    snapshot = {}
    if entry:
        snapshot = {
            "phase_duration_seconds": max(
                int(entry.get("phase_completed_at", 0)) - int(entry.get("phase_started_at", 0)), 0),
            "agent_duration_seconds": max(
                int(entry.get("agent_completed_at", 0)) - int(entry.get("phase_started_at", 0)), 0)
                + int(entry.get("optimization_duration_seconds", 0)),
            "confirmation_duration_seconds": max(
                int(entry.get("confirmation_completed_at", 0))
                - int(entry.get("confirmation_started_at", 0)), 0),
            "optimization_rounds": int(entry.get("optimization_rounds", 0)),
        }

    checkpoint = {
        "checkpoint_id": f"{args.phase}_completed",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "phase": phase_number(args.phase),
        "phase_name": PHASE_NAMES[args.phase],
        "status": args.status or "completed",
        "outputs": outputs,
        "timing_snapshot": snapshot,
        "error_history": [],
    }
    out_path = os.path.join(cdir, CHECKPOINT_FILES.get(args.phase, f"{args.phase}_checkpoint.json"))
    if os.path.exists(out_path):
        print(f"❌ 检查点已存在，禁止覆盖（不可变审计快照）: {out_path}", file=sys.stderr)
        return 1
    save_json(out_path, checkpoint)
    print(f"✅ 已保存检查点: {out_path}")
    return 0


def cmd_resume(args) -> int:
    cdir = checkpoint_dir(args.output)
    if not os.path.isdir(cdir):
        print(f"⚠️ 检查点目录不存在: {cdir}，需从阶段1重新开始", file=sys.stderr)
        return 0
    files = [f for f in os.listdir(cdir) if f.endswith("_checkpoint.json")]
    if not files:
        print("⚠️ 无检查点文件，需从阶段1重新开始", file=sys.stderr)
        return 0

    # 按 phase 编号排序（而非时间戳，因检查点可能跨会话补存）
    def ckpt_phase_num(fname: str) -> int:
        data = load_json(os.path.join(cdir, fname), default={})
        return int(data.get("phase", 0)) if data else 0

    ordered = sorted(files, key=ckpt_phase_num)
    last_valid = None
    for fname in ordered:
        data = load_json(os.path.join(cdir, fname), default=None)
        if not data:
            continue
        if data.get("status") != "completed":
            continue
        outputs = data.get("outputs", {}) or {}
        all_readable = all(_readable(p) for p in outputs.values())
        if all_readable:
            last_valid = (fname, data)
        else:
            print(f"⚠️ 检查点输出文件缺失，降级到前一检查点: {fname}", file=sys.stderr)
            break

    if not last_valid:
        print("⚠️ 无有效检查点（全部 outputs 缺失或无 completed），从阶段1重新开始", file=sys.stderr)
        return 0

    fname, data = last_valid
    pnum = int(data.get("phase", 0))
    next_key = PHASE_ORDER[pnum] if 0 <= pnum < len(PHASE_ORDER) else "phase1"
    print(f"✅ 恢复起始点: {next_key}（{PHASE_NAMES.get(next_key, '')}）")
    print(f"   最后有效检查点: {fname} (phase={pnum}, timestamp={data.get('timestamp')})")
    for name, p in (data.get("outputs", {}) or {}).items():
        flag = "✓" if _readable(p) else "✗"
        print(f"   {flag} {name} -> {p}")
    return 0


def _fmt_duration(sec: int) -> str:
    if sec < 60:
        return f"{sec}s"
    return f"{sec // 60}分{sec % 60}s"


def cmd_report(args) -> int:
    timing = load_json(timing_path(args.output), default=None)
    if not timing or "phases" not in timing:
        print(f"❌ timing.json 不存在或损坏: {timing_path(args.output)}", file=sys.stderr)
        return 1
    total = int(timing.get("pipeline_completed_at", 0)) - int(timing.get("pipeline_started_at", 0))
    total = max(total, 0)
    print("⏱️ 阶段耗时报告\n")
    print("| 阶段 | Agent耗时 | 确认耗时 | 优化耗时(轮次) | 阶段总耗时 |")
    print("|------|-----------|---------|---------------|-----------|")
    sum_agent = sum_conf = sum_opt = 0
    for p in timing["phases"]:
        started = int(p.get("phase_started_at", 0))
        agent_done = int(p.get("agent_completed_at", 0))
        conf_s = int(p.get("confirmation_started_at", agent_done))
        conf_c = int(p.get("confirmation_completed_at", agent_done))
        completed = int(p.get("phase_completed_at", 0))
        opt_dur = int(p.get("optimization_duration_seconds", 0))
        opt_rounds = int(p.get("optimization_rounds", 0))
        agent_dur = max(agent_done - started, 0) + opt_dur
        conf_dur = max(conf_c - conf_s, 0)
        phase_dur = max(completed - started, 0)
        sum_agent += agent_dur
        sum_conf += conf_dur
        sum_opt += opt_dur
        print(f"| {p.get('name','')} | {_fmt_duration(agent_dur)} | {_fmt_duration(conf_dur)} | "
              f"{_fmt_duration(opt_dur)} ({opt_rounds}轮) | {_fmt_duration(phase_dur)} |")
    print(f"| **总耗时** | {_fmt_duration(sum_agent)} | {_fmt_duration(sum_conf)} | "
          f"{_fmt_duration(sum_opt)} | {_fmt_duration(total)} |")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="测试设计计时与检查点协议操作工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p_rec = sub.add_parser("record", help="采集某计时机写入 timing.json")
    p_rec.add_argument("--output", required=True, help="测试设计输出目录")
    p_rec.add_argument("--phase", required=True, help="phase key，如 phase1/phase2_adv/phase3-1")
    p_rec.add_argument("--point", required=True, help="timing 字段，如 phase_started_at/optimization_round")
    p_rec.add_argument("--value", type=int, help="optimization_duration 累加秒数")
    p_rec.set_defaults(func=cmd_record)

    p_ck = sub.add_parser("checkpoint", help="检查点操作")
    ck_sub = p_ck.add_subparsers(dest="ck_command", required=True)
    p_save = ck_sub.add_parser("save", help="保存检查点（含保存前检查清单校验）")
    p_save.add_argument("--output", required=True, help="测试设计输出目录")
    p_save.add_argument("--phase", required=True, help="phase key")
    p_save.add_argument("--artifact", action="append", help="输出文件 name=path，可重复")
    p_save.add_argument("--status", help="状态，默认 completed")
    p_save.set_defaults(func=cmd_checkpoint_save)

    p_res = sub.add_parser("resume", help="扫描检查点输出恢复起始点")
    p_res.add_argument("--output", required=True, help="测试设计输出目录")
    p_res.set_defaults(func=cmd_resume)

    p_rep = sub.add_parser("report", help="生成计时报告")
    p_rep.add_argument("--output", required=True, help="测试设计输出目录")
    p_rep.set_defaults(func=cmd_report)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
