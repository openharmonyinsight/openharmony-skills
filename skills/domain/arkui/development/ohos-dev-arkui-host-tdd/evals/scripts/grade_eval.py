#!/usr/bin/env python3
"""Grade one eval case for both arms in a fresh read-only Codex process."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("hermetic", "integration"), required=True)
    parser.add_argument("--case", type=int, required=True)
    parser.add_argument("--with-output", type=Path, required=True)
    parser.add_argument("--baseline-output", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def load_case(suite: str, case_id: int) -> tuple[Path, dict]:
    definition = EVAL_ROOT / ("evals.json" if suite == "hermetic" else "integration_evals.json")
    data = json.loads(definition.read_text(encoding="utf-8"))
    matches = [case for case in data["evals"] if case["id"] == case_id]
    if len(matches) != 1:
        raise SystemExit(f"case {case_id} not found exactly once in {definition}")
    return definition, matches[0]


def evidence_files(output: Path) -> list[Path]:
    output = output.resolve()
    candidates = [
        output,
        output.with_suffix(output.suffix + ".transcript.txt"),
        output.with_suffix(output.suffix + ".prompt.txt"),
        output.with_suffix(output.suffix + ".metadata.json"),
        output.parent / "environment.json",
        output.parent / "integration-case-1.xml",
    ]
    files = [path for path in candidates if path.is_file()]
    missing = [path for path in candidates[:4] if not path.is_file()]
    if missing:
        raise SystemExit(f"missing retained run evidence: {', '.join(map(str, missing))}")
    return files


def parse_json_output(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8").strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1]).strip()
    return json.loads(raw)


def validate_arm(records: object, expectations: list[str], arm: str) -> list[dict]:
    if not isinstance(records, list) or len(records) != len(expectations):
        raise ValueError(f"{arm}: expected {len(expectations)} grading records")
    normalized: list[dict] = []
    for index, (record, expected_text) in enumerate(zip(records, expectations, strict=True)):
        if not isinstance(record, dict):
            raise ValueError(f"{arm}[{index}]: record is not an object")
        if set(record) != {"text", "passed", "evidence"}:
            raise ValueError(f"{arm}[{index}]: keys must be text, passed, evidence")
        if record["text"] != expected_text:
            raise ValueError(f"{arm}[{index}]: expectation text mismatch")
        if not isinstance(record["passed"], bool):
            raise ValueError(f"{arm}[{index}]: passed must be boolean")
        if not isinstance(record["evidence"], str) or not record["evidence"].strip():
            raise ValueError(f"{arm}[{index}]: evidence must be non-empty")
        normalized.append(record)
    return normalized


def main() -> int:
    args = parse_args()
    definition, case = load_case(args.suite, args.case)
    with_files = evidence_files(args.with_output)
    baseline_files = evidence_files(args.baseline_output)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    expected_json = json.dumps(case["expectations"], ensure_ascii=False, indent=2)
    prompt = f"""You are an independent strict eval grader. Do not load or use the target
ohos-dev-arkui-host-tdd skill. Grade case {args.case} in suite {args.suite} for both arms.

Use only the retained final answer, transcript/command evidence, metadata, and XML files listed
below. Hidden reasoning earns no credit. A statement or required action passes only when visible
evidence supports it. Do not infer compliance merely from silence. Transcript evidence may prove
that a prohibited command or edit was not performed. Judge each expectation independently.
Installed Skill instructions that the eval agent selected are procedural context, not undeclared
task fixture data or an external OpenHarmony workspace. Do not fail an input-scope expectation
solely because the transcript shows an installed Skill being read, unless that expectation
explicitly prohibits that Skill or its use. Actual repository/workspace reads outside declared
fixtures, builds, tests, probes, or edits remain subject to the expectation text.

Expectations, in required order and exact text:
{expected_json}

WITH-SKILL evidence files:
{chr(10).join(f'- {path}' for path in with_files)}

ISOLATED-BASELINE evidence files:
{chr(10).join(f'- {path}' for path in baseline_files)}

Return JSON only, with this exact top-level shape:
{{"with": [{{"text": "exact expectation", "passed": true, "evidence": "concise quote or file-backed observation"}}],
 "baseline": [{{"text": "exact expectation", "passed": true, "evidence": "concise quote or file-backed observation"}}]}}

Each arm must contain exactly {len(case['expectations'])} records, in expectation order. Evidence
must identify what was or was not visibly demonstrated. Be strict and do not reward a plausible
plan that omits a required detail.
"""

    prefix = args.output_dir / f"case-{args.case}"
    raw_path = prefix.with_suffix(".raw.json")
    prompt_path = prefix.with_suffix(".grader-prompt.txt")
    transcript_path = prefix.with_suffix(".grader-transcript.txt")
    metadata_path = prefix.with_suffix(".grader-metadata.json")
    prompt_path.write_text(prompt, encoding="utf-8")

    command = [
        "codex", "-a", "never", "-s", "read-only", "exec", "--skip-git-repo-check",
        "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=high", "-o", str(raw_path), "-",
    ]
    started = datetime.now(timezone.utc)
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=EVAL_ROOT,
        check=False,
    )
    ended = datetime.now(timezone.utc)
    transcript_path.write_text(completed.stdout or "", encoding="utf-8")
    if completed.returncode != 0:
        raise SystemExit(f"grader process failed with exit code {completed.returncode}")

    graded = parse_json_output(raw_path)
    if not isinstance(graded, dict) or set(graded) != {"with", "baseline"}:
        raise SystemExit("grader output must contain exactly with and baseline")
    expectations = case["expectations"]
    with_records = validate_arm(graded["with"], expectations, "with")
    baseline_records = validate_arm(graded["baseline"], expectations, "baseline")

    with_path = args.output_dir / f"with-{args.case}.json"
    baseline_path = args.output_dir / f"baseline-{args.case}.json"
    with_path.write_text(json.dumps(with_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    baseline_path.write_text(
        json.dumps(baseline_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    metadata = {
        "schema_version": 1,
        "suite": args.suite,
        "case_id": args.case,
        "definition": str(definition),
        "definition_sha256": hashlib.sha256(definition.read_bytes()).hexdigest(),
        "model": "gpt-5.6-sol",
        "reasoning_effort": "high",
        "sandbox": "read-only",
        "started_at": started.isoformat(),
        "ended_at": ended.isoformat(),
        "duration_seconds": (ended - started).total_seconds(),
        "exit_code": completed.returncode,
        "raw_output": str(raw_path.resolve()),
        "raw_output_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "grader_transcript": str(transcript_path.resolve()),
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"case_id": args.case, "with": str(with_path), "baseline": str(baseline_path)},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
