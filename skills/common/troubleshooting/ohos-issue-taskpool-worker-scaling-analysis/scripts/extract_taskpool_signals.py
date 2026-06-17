#!/usr/bin/env python3
"""Extract taskpool worker-scaling clues from logs.

This helper is intentionally heuristic. It highlights lines worth reading; it
does not prove root cause.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = {
    "queue": re.compile(r"waitingTasksNum|globalTaskQueue|enqueue|queued|waiting task|backlog", re.I),
    "worker": re.compile(r"GlobalQueueWorker|workerBody|workers(?:Size| size)?|worker id|managerWorker", re.I),
    "expand": re.compile(r"tryTriggerExpand|triggerExpand|expand|workersLimit|targetNum|idleWorkersNum", re.I),
    "blocked": re.compile(
        r"blockedWorker|executingTaskBodyStartTime|blockedWorkerThresholdMs|long task|blocked|hang", re.I
    ),
    "priority": re.compile(
        r"USER_INTERACTION|DEADLINE_REQUEST|HIGH|MEDIUM|LOW|IDLE|priority|setCurrentTaskpoolWorkerPriority", re.I
    ),
    "shutdown": re.compile(r"closeWorker|setWorkerActive|condVarNotifyAll|join|shutdown|shrink|idleTime", re.I),
    "dependency": re.compile(r"pendingDependencyTasks|notifyDependencies|tryActivatePendingDependencyTask|dependency", re.I),
    "launch": re.compile(r"isTaskPoolUseLaunch|isUsingLaunch|launchImpl|Job\.Await|launch mode", re.I),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize taskpool scaling signals from a log file.")
    parser.add_argument("logfile", type=Path, help="Path to a text log file")
    parser.add_argument("--context", type=int, default=0, help="Number of nearby lines to show before and after matches")
    parser.add_argument("--limit", type=int, default=12, help="Maximum lines to show for each category")
    return parser.parse_args()


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"error: log file not found: {path}")
    if not path.is_file():
        raise SystemExit(f"error: not a regular file: {path}")
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def collect(lines: list[str], context: int) -> dict[str, list[tuple[int, str]]]:
    result: dict[str, list[tuple[int, str]]] = {name: [] for name in PATTERNS}
    emitted: dict[str, set[int]] = {name: set() for name in PATTERNS}

    for idx, line in enumerate(lines):
        for name, pattern in PATTERNS.items():
            if not pattern.search(line):
                continue
            start = max(0, idx - context)
            end = min(len(lines), idx + context + 1)
            for line_no in range(start, end):
                if line_no not in emitted[name]:
                    result[name].append((line_no + 1, lines[line_no]))
                    emitted[name].add(line_no)
    return result


def main() -> int:
    args = parse_args()
    lines = read_lines(args.logfile)
    matches = collect(lines, args.context)

    for name, entries in matches.items():
        print(f"## {name} ({len(entries)} lines)")
        if not entries:
            print("No obvious signals found.")
            print()
            continue
        for line_no, text in entries[: args.limit]:
            print(f"{line_no}: {text}")
        if len(entries) > args.limit:
            print(f"... {len(entries) - args.limit} more")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
