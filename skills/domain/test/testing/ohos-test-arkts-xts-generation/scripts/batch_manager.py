#!/usr/bin/env python3
"""
Batch manager for XTS test generation.

Splits uncovered APIs into batches (max 10 APIs per batch, grouped by module),
tracks completion status, and supports resume from interruption.

Usage:
    python scripts/batch_manager.py plan [--max-apis 10]
    python scripts/batch_manager.py status
    python scripts/batch_manager.py start <batch_id>
    python scripts/batch_manager.py complete <batch_id> --api-file <path>
    python scripts/batch_manager.py skip <batch_id>
    python scripts/batch_manager.py resume
    python scripts/batch_manager.py reset
"""

import argparse
import glob
import json
import os
import sys
from collections import OrderedDict
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(SCRIPT_DIR, '..')

WORKSPACE_DIR = os.path.join(SKILL_ROOT, 'batch_workspace')
COMPLETED_JSON = os.path.join(WORKSPACE_DIR, 'completed.json')
BATCH_PLAN_JSON = os.path.join(WORKSPACE_DIR, 'batch_plan.json')


def _ensure_workspace():
    os.makedirs(WORKSPACE_DIR, exist_ok=True)


def _load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _init_completed():
    return {
        "metadata": {
            "total_apis": 0,
            "completed_count": 0,
            "completed_batches": [],
            "skipped_batches": [],
            "last_batch": None,
            "last_update": None,
        },
        "api_status": {},
    }


def _init_batch_plan():
    return {
        "metadata": {
            "created_at": None,
            "total_batches": 0,
            "total_apis": 0,
            "max_apis_per_batch": 10,
        },
        "batches": OrderedDict(),
    }


def _load_config():
    config_path = os.path.join(SKILL_ROOT, '.oh-xts-config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def _get_scan_tool_root():
    config = _load_config()
    scan_tool_root = config.get('scan_tool_root', '')
    if scan_tool_root and os.path.isdir(scan_tool_root):
        return scan_tool_root
    return os.path.join(SKILL_ROOT, 'APICoverageDetector')


def _find_uncovered_files():
    config = _load_config()
    subsystem = config.get('subsystem', '')
    ets_versions = config.get('ets_version', ['ets1.1'])
    if isinstance(ets_versions, str):
        ets_versions = [v.strip() for v in ets_versions.split(',')]

    results_dir = os.path.join(_get_scan_tool_root(), 'results')
    candidates = []
    for ver in ets_versions:
        pattern = os.path.join(results_dir, ver, 'open_source', '*.csv')
        candidates.extend(glob.glob(pattern))
        pattern2 = os.path.join(results_dir, ver, 'open_source', '*.xlsx')
        candidates.extend(glob.glob(pattern2))

    iter_dir = os.path.join(SKILL_ROOT, 'batch_workspace', 'coverage_data')
    if os.path.exists(iter_dir):
        for ver in ets_versions:
            pattern = os.path.join(iter_dir, ver, '*.csv')
            candidates.extend(glob.glob(pattern))

    return sorted(set(candidates), key=os.path.getmtime, reverse=True)


def _parse_csv_apis(csv_path):
    apis = []
    module_apis = {}
    try:
        import csv as csv_mod
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv_mod.reader(f)
            header = next(reader, None)
            if not header:
                return apis, module_apis

            col_map = {}
            for i, h in enumerate(header):
                h_lower = h.strip().lower()
                if 'module' in h_lower:
                    col_map['module'] = i
                elif 'class' in h_lower:
                    col_map['class'] = i
                elif 'method' in h_lower or 'func' in h_lower or 'api' in h_lower:
                    col_map['method'] = i
                elif 'subsystem' in h_lower:
                    col_map['subsystem'] = i
                elif 'kit' in h_lower:
                    col_map['kit'] = i

            for row in reader:
                if len(row) <= max(col_map.values(), default=0):
                    continue

                module = row[col_map.get('module', 0)].strip() if 'module' in col_map else ''
                cls = row[col_map.get('class', 1)].strip() if 'class' in col_map else ''
                method = row[col_map.get('method', 2)].strip() if 'method' in col_map else ''
                subsystem = row[col_map.get('subsystem', -1)].strip() if 'subsystem' in col_map else ''
                kit = row[col_map.get('kit', -1)].strip() if 'kit' in col_map else ''

                if not module and not method:
                    continue

                api_key = f"{module}.{cls}.{method}" if cls else f"{module}.{method}"
                if not api_key or api_key == '.':
                    continue

                api_info = {
                    "api_key": api_key,
                    "module": module,
                    "class": cls,
                    "method": method,
                    "subsystem": subsystem,
                    "kit": kit,
                }
                apis.append(api_info)

                if module not in module_apis:
                    module_apis[module] = []
                module_apis[module].append(api_info)

    except Exception as e:
        print(f"Warning: Failed to parse {csv_path}: {e}", file=sys.stderr)

    return apis, module_apis


def _group_apis_by_module(apis, module_apis, max_apis=10):
    batches = OrderedDict()
    batch_id = 1

    sorted_modules = sorted(module_apis.keys(), key=lambda m: len(module_apis[m]), reverse=True)

    for module in sorted_modules:
        module_api_list = module_apis[module]
        total = len(module_api_list)
        num_batches_for_module = (total + max_apis - 1) // max_apis

        for i in range(num_batches_for_module):
            start = i * max_apis
            end = min(start + max_apis, total)
            chunk = module_api_list[start:end]

            batch_key = str(batch_id)
            batches[batch_key] = {
                "batch_id": batch_id,
                "module": module,
                "api_count": len(chunk),
                "apis": [a["api_key"] for a in chunk],
                "status": "pending",
            }
            batch_id += 1

    return batches


def cmd_plan(args):
    _ensure_workspace()
    max_apis = args.max_apis or 10

    csv_files = _find_uncovered_files()
    if not csv_files:
        print("No uncovered API files found. Run coverage scan first.")
        print("Expected locations:")
        print(f"  {os.path.join(_get_scan_tool_root(), 'results', '<ets_version>', 'open_source', '*.csv')}")
        return 1

    all_apis = []
    module_apis = {}
    for csv_path in csv_files:
        apis, mod_apis = _parse_csv_apis(csv_path)
        all_apis.extend(apis)
        for mod, api_list in mod_apis.items():
            if mod not in module_apis:
                module_apis[mod] = []
            module_apis[mod].extend(api_list)

    seen = set()
    unique_apis = []
    unique_module_apis = {}
    for api in all_apis:
        if api["api_key"] not in seen:
            seen.add(api["api_key"])
            unique_apis.append(api)
            mod = api["module"]
            if mod not in unique_module_apis:
                unique_module_apis[mod] = []
            unique_module_apis[mod].append(api)

    batches = _group_apis_by_module(unique_apis, unique_module_apis, max_apis)

    plan = _init_batch_plan()
    plan["metadata"]["created_at"] = datetime.now().isoformat()
    plan["metadata"]["total_batches"] = len(batches)
    plan["metadata"]["total_apis"] = len(unique_apis)
    plan["metadata"]["max_apis_per_batch"] = max_apis
    plan["metadata"]["source_files"] = csv_files
    plan["batches"] = batches
    _save_json(BATCH_PLAN_JSON, plan)

    completed = _init_completed()
    completed["metadata"]["total_apis"] = len(unique_apis)
    _save_json(COMPLETED_JSON, completed)

    print(f"\n{'='*60}")
    print(f"  Batch Plan Generated")
    print(f"{'='*60}")
    print(f"  Total APIs: {len(unique_apis)}")
    print(f"  Total batches: {len(batches)}")
    print(f"  Max APIs per batch: {max_apis}")
    print(f"  Modules: {len(unique_module_apis)}")
    print(f"{'='*60}\n")

    for bid, batch in batches.items():
        status_marker = "[ ]"
        print(f"  {status_marker} Batch {bid}: {batch['module']} ({batch['api_count']} APIs)")
        for api_key in batch['apis'][:5]:
            print(f"      - {api_key}")
        if len(batch['apis']) > 5:
            print(f"      ... and {len(batch['apis']) - 5} more")

    print(f"\nPlan saved to: {BATCH_PLAN_JSON}")
    print(f"Run 'python scripts/batch_manager.py start <batch_id>' to begin.\n")
    return 0


def cmd_status(args):
    plan = _load_json(BATCH_PLAN_JSON)
    completed = _load_json(COMPLETED_JSON)

    if not plan:
        print("No batch plan found. Run 'plan' first.")
        return 1

    meta = plan["metadata"]
    comp_meta = completed["metadata"] if completed else {}

    total = meta["total_batches"]
    done = len(comp_meta.get("completed_batches", []))
    skipped = len(comp_meta.get("skipped_batches", []))
    pending = total - done - skipped

    print(f"\n{'='*60}")
    print(f"  Batch Execution Status")
    print(f"{'='*60}")
    print(f"  Total APIs:    {meta['total_apis']}")
    print(f"  Total batches: {total}")
    print(f"  Completed:     {done}  ({done*100//total if total else 0}%)")
    print(f"  Skipped:       {skipped}")
    print(f"  Pending:       {pending}")
    print(f"  Last update:   {comp_meta.get('last_update', 'N/A')}")
    print(f"{'='*60}\n")

    for bid, batch in plan["batches"].items():
        api_status = completed.get("api_status", {}) if completed else {}
        batch_done = sum(1 for a in batch["apis"] if api_status.get(a, {}).get("completed", False))
        status = "PENDING"
        if int(bid) in comp_meta.get("completed_batches", []):
            status = "DONE"
        elif int(bid) in comp_meta.get("skipped_batches", []):
            status = "SKIP"
        elif batch_done > 0 and batch_done < batch["api_count"]:
            status = "PARTIAL"

        markers = {"DONE": "✅", "SKIP": "⏭️", "PARTIAL": "🔄", "PENDING": "[ ]"}
        marker = markers.get(status, "[ ]")
        print(f"  {marker} Batch {bid}: {batch['module']} ({batch_done}/{batch['api_count']} APIs) {status}")

    print()
    return 0


def cmd_start(args):
    _ensure_workspace()
    plan = _load_json(BATCH_PLAN_JSON)
    completed = _load_json(COMPLETED_JSON)

    if not plan:
        print("No batch plan found. Run 'plan' first.")
        return 1

    batch_id = str(args.batch_id)
    if batch_id not in plan["batches"]:
        print(f"Batch {batch_id} not found. Valid: 1-{plan['metadata']['total_batches']}")
        return 1

    batch = plan["batches"][batch_id]
    api_status = completed.get("api_status", {}) if completed else {}

    pending_apis = [a for a in batch["apis"] if not api_status.get(a, {}).get("completed", False)]

    if not pending_apis:
        print(f"Batch {batch_id} already completed.")
        return 0

    batch_file = os.path.join(WORKSPACE_DIR, f"batch_{batch_id}_generated_apis.json")
    batch_data = {
        "metadata": {
            "batch_id": int(batch_id),
            "module": batch["module"],
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "api_count": len(pending_apis),
        },
        "apis": {api_key: {"status": "generating"} for api_key in pending_apis},
    }
    _save_json(batch_file, batch_data)

    print(f"\n{'='*60}")
    print(f"  Batch {batch_id}: {batch['module']}")
    print(f"{'='*60}")
    print(f"  APIs to generate: {len(pending_apis)}")
    print(f"  Module: {batch['module']}")
    print(f"{'='*60}\n")

    for api_key in pending_apis:
        print(f"  - {api_key}")

    print(f"\nBatch file: {batch_file}")
    print(f"Generate test cases for these APIs now.\n")
    return 0


def cmd_complete(args):
    from batch_lock import FileLock

    _ensure_workspace()
    plan = _load_json(BATCH_PLAN_JSON)
    completed = _load_json(COMPLETED_JSON)

    if not plan:
        print("No batch plan found.")
        return 1

    batch_id = str(args.batch_id)
    if batch_id not in plan["batches"]:
        print(f"Batch {batch_id} not found.")
        return 1

    batch = plan["batches"][batch_id]
    batch_file = os.path.join(WORKSPACE_DIR, f"batch_{batch_id}_generated_apis.json")

    if args.api_file and os.path.exists(args.api_file):
        with open(args.api_file, 'r', encoding='utf-8') as f:
            generated = json.load(f)
        completed_apis = generated.get("apis", {})
    elif os.path.exists(batch_file):
        batch_data = _load_json(batch_file)
        completed_apis = batch_data.get("apis", {})
        for api_key in completed_apis:
            completed_apis[api_key]["status"] = "completed"
    else:
        completed_apis = {api_key: {"status": "completed"} for api_key in batch["apis"]}

    lock_path = COMPLETED_JSON + ".lock"
    with FileLock(lock_path, timeout=30):
        if completed is None:
            completed = _init_completed()
            completed["metadata"]["total_apis"] = plan["metadata"]["total_apis"]

        now = datetime.now().isoformat()
        for api_key, info in completed_apis.items():
            completed["api_status"][api_key] = {
                "batch": int(batch_id),
                "completed": True,
                "completed_at": now,
                "test_files": info.get("test_files", []),
            }

        completed["metadata"]["completed_count"] = sum(
            1 for v in completed["api_status"].values() if v.get("completed")
        )
        bid_int = int(batch_id)
        if bid_int not in completed["metadata"]["completed_batches"]:
            completed["metadata"]["completed_batches"].append(bid_int)
        completed["metadata"]["last_batch"] = bid_int
        completed["metadata"]["last_update"] = now
        _save_json(COMPLETED_JSON, completed)

    if os.path.exists(batch_file):
        batch_data = _load_json(batch_file)
        batch_data["metadata"]["completed_at"] = now
        for api_key in batch_data.get("apis", {}):
            batch_data["apis"][api_key]["status"] = "completed"
        _save_json(batch_file, batch_data)

    done = len(completed["metadata"]["completed_batches"])
    total = plan["metadata"]["total_batches"]
    print(f"\nBatch {batch_id} completed! ({done}/{total} batches done)")
    return 0


def cmd_skip(args):
    from batch_lock import FileLock

    _ensure_workspace()
    plan = _load_json(BATCH_PLAN_JSON)
    completed = _load_json(COMPLETED_JSON)
    if not plan or not completed:
        print("No batch plan found.")
        return 1

    batch_id = str(args.batch_id)
    bid_int = int(batch_id)

    lock_path = COMPLETED_JSON + ".lock"
    with FileLock(lock_path, timeout=30):
        if bid_int not in completed["metadata"]["skipped_batches"]:
            completed["metadata"]["skipped_batches"].append(bid_int)
        completed["metadata"]["last_update"] = datetime.now().isoformat()
        _save_json(COMPLETED_JSON, completed)

    print(f"Batch {batch_id} skipped.")
    return 0


def cmd_resume(args):
    plan = _load_json(BATCH_PLAN_JSON)
    completed = _load_json(COMPLETED_JSON)

    if not plan:
        print("No batch plan found. Run 'plan' first.")
        return 1

    comp_meta = completed.get("metadata", {}) if completed else {}
    done_batches = set(comp_meta.get("completed_batches", []))
    skipped_batches = set(comp_meta.get("skipped_batches", []))

    next_batches = []
    for bid in plan["batches"]:
        bid_int = int(bid)
        if bid_int not in done_batches and bid_int not in skipped_batches:
            next_batches.append(bid)

    if not next_batches:
        print("All batches completed or skipped!")
        return 0

    print(f"\nNext pending batches: {', '.join(next_batches)}")
    print(f"Run: python scripts/batch_manager.py start {next_batches[0]}\n")
    return 0


def cmd_reset(args):
    import shutil

    if os.path.exists(WORKSPACE_DIR):
        if not args.force:
            print("This will delete all batch workspace data. Use --force to confirm.")
            return 1
        shutil.rmtree(WORKSPACE_DIR)

    print("Batch workspace reset.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="XTS batch test generation manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    p_plan = subparsers.add_parser("plan", help="Generate batch plan from uncovered APIs")
    p_plan.add_argument("--max-apis", type=int, default=10, help="Max APIs per batch (default: 10)")

    p_status = subparsers.add_parser("status", help="Show batch execution status")

    p_start = subparsers.add_parser("start", help="Start a batch")
    p_start.add_argument("batch_id", type=int, help="Batch ID to start")

    p_complete = subparsers.add_parser("complete", help="Mark a batch as completed")
    p_complete.add_argument("batch_id", type=int, help="Batch ID to complete")
    p_complete.add_argument("--api-file", help="Path to generated APIs JSON file")

    p_skip = subparsers.add_parser("skip", help="Skip a batch")
    p_skip.add_argument("batch_id", type=int, help="Batch ID to skip")

    subparsers.add_parser("resume", help="Show next pending batch")

    p_reset = subparsers.add_parser("reset", help="Reset batch workspace")
    p_reset.add_argument("--force", action="store_true", help="Force reset without confirmation")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "plan": cmd_plan,
        "status": cmd_status,
        "start": cmd_start,
        "complete": cmd_complete,
        "skip": cmd_skip,
        "resume": cmd_resume,
        "reset": cmd_reset,
    }

    handler = commands.get(args.command)
    if handler:
        sys.path.insert(0, SCRIPT_DIR)
        return handler(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
