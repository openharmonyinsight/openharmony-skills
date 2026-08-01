#!/usr/bin/env python3
"""Validate the split Host TDD eval definitions and declared fixture files."""

from __future__ import annotations

import json
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    with (EVAL_ROOT / name).open(encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    suites = [load("evals.json"), load("integration_evals.json")]
    cases = [case for suite in suites for case in suite["evals"]]
    ids = [case["id"] for case in cases]
    errors: list[str] = []

    if len(cases) != 9:
        errors.append(f"expected 9 cases, found {len(cases)}")
    if len(set(ids)) != len(ids):
        errors.append(f"case ids are not unique: {ids}")

    expectation_count = sum(len(case.get("expectations", [])) for case in cases)
    if expectation_count != 59:
        errors.append(f"expected 59 expectations, found {expectation_count}")

    for case in cases:
        files = case.get("files", [])
        if not files:
            errors.append(f"case {case['id']} has no declared files")
        for declared in files:
            if "${EVAL_ARTIFACT_DIR}" in declared:
                continue
            if not (EVAL_ROOT / declared).is_file():
                errors.append(f"case {case['id']} missing fixture: {declared}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        f"OK: {len(cases)} cases, {expectation_count} expectations, "
        f"ids={','.join(str(item) for item in sorted(ids))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
