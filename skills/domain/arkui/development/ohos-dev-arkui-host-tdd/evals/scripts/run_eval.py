#!/usr/bin/env python3
"""Run one Host TDD eval case in a fresh Codex process and retain metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "ohos-dev-arkui-host-tdd"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("hermetic", "integration"), required=True)
    parser.add_argument("--case", type=int, required=True)
    parser.add_argument("--arm", choices=("with", "baseline"), required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cwd", type=Path)
    parser.add_argument("--baseline-isolated", action="store_true")
    return parser.parse_args()


def load_case(suite: str, case_id: int) -> tuple[Path, dict]:
    definition = EVAL_ROOT / ("evals.json" if suite == "hermetic" else "integration_evals.json")
    with definition.open(encoding="utf-8") as stream:
        data = json.load(stream)
    matches = [case for case in data["evals"] if case["id"] == case_id]
    if len(matches) != 1:
        raise SystemExit(f"case {case_id} not found exactly once in {definition}")
    return definition, matches[0]


def extract_command_evidence(transcript: str) -> str:
    """Keep exec command blocks and their completion status, omitting command output."""
    lines = transcript.splitlines()
    evidence: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index] == "exec":
            evidence.append("exec")
            index += 1
            while index < len(lines):
                evidence.append(lines[index])
                if " succeeded in " in lines[index] or " failed in " in lines[index]:
                    break
                index += 1
            evidence.append("")
        index += 1
    if not evidence:
        return "No exec tool commands recorded.\n"
    return "\n".join(evidence).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    if args.arm == "baseline" and not args.baseline_isolated:
        raise SystemExit("baseline requires --baseline-isolated after disabling the target skill")

    definition, case = load_case(args.suite, args.case)
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    resolved_files: list[Path] = []
    for declared in case["files"]:
        expanded = declared.replace("${EVAL_ARTIFACT_DIR}", str(args.artifact_dir.resolve()))
        path = Path(expanded)
        if not path.is_absolute():
            path = EVAL_ROOT / path
        path = path.resolve()
        if not path.is_file():
            raise SystemExit(f"declared input does not exist: {path}")
        resolved_files.append(path)

    lines = []
    if args.arm == "with":
        lines.append(f"Use ${SKILL_NAME}.")
    lines.extend(
        [
            "",
            case["prompt"],
            "",
            "随附文件（只读取这些声明的评测输入）：",
            *[f"- {path}" for path in resolved_files],
            "",
            "可以使用只读文件查看命令读取上述输入；场景中的‘不要执行命令’是指不要执行 OpenHarmony、构建、产物探测或测试命令。",
            "不要读取 evals.json、integration_evals.json、reports/、grading/ 或任何预期答案。",
        ]
    )
    prompt = "\n".join(lines).strip() + "\n"

    prompt_path = args.output.with_suffix(args.output.suffix + ".prompt.txt")
    metadata_path = args.output.with_suffix(args.output.suffix + ".metadata.json")
    transcript_path = args.output.with_suffix(args.output.suffix + ".transcript.txt")
    command_evidence_path = args.output.with_suffix(args.output.suffix + ".commands.txt")
    prompt_path.write_text(prompt, encoding="utf-8")

    sandbox = "read-only" if args.suite == "hermetic" else "workspace-write"
    command = [
        "codex",
        "-a",
        "never",
        "-s",
        sandbox,
        "exec",
        "--skip-git-repo-check",
        "-m",
        "gpt-5.6-sol",
        "-c",
        "model_reasoning_effort=high",
        "-o",
        str(args.output.resolve()),
        "-",
    ]
    started = datetime.now(timezone.utc)
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=(args.cwd or EVAL_ROOT).resolve(),
        check=False,
    )
    ended = datetime.now(timezone.utc)
    transcript = completed.stdout or ""
    transcript_path.write_text(transcript, encoding="utf-8")
    command_evidence = extract_command_evidence(transcript)
    command_evidence_path.write_text(command_evidence, encoding="utf-8")

    metadata = {
        "schema_version": 1,
        "suite": args.suite,
        "case_id": args.case,
        "arm": args.arm,
        "target_skill": SKILL_NAME,
        "baseline_isolated_confirmed": args.arm == "baseline" and args.baseline_isolated,
        "definition": str(definition),
        "definition_sha256": hashlib.sha256(definition.read_bytes()).hexdigest(),
        "files": [str(path) for path in resolved_files],
        "model": "gpt-5.6-sol",
        "reasoning_effort": "high",
        "sandbox": sandbox,
        "cwd": str((args.cwd or EVAL_ROOT).resolve()),
        "started_at": started.isoformat(),
        "ended_at": ended.isoformat(),
        "duration_seconds": (ended - started).total_seconds(),
        "exit_code": completed.returncode,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "output": str(args.output.resolve()),
        "transcript": str(transcript_path.resolve()),
        "transcript_sha256": hashlib.sha256(transcript.encode()).hexdigest(),
        "command_evidence": str(command_evidence_path.resolve()),
        "command_evidence_sha256": hashlib.sha256(command_evidence.encode()).hexdigest(),
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "case_id": args.case,
                "arm": args.arm,
                "exit_code": completed.returncode,
                "output": str(args.output.resolve()),
                "transcript": str(transcript_path.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
