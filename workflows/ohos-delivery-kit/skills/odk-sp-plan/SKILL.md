
# ODK SP Plan

Use when Superpowers is installed AND the user wants writing-plans discipline for execution-plan.md (task decomposition, file-level boundaries, AC-Task trace). Falls back to odk-plan if unavailable.

## Purpose

Invoke Superpowers `writing-plans` for task decomposition and file-level boundaries. Transform output into ODK `execution-plan.md` format with AC-Task traceability.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `spec.md` must exist with numbered ACs.
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Steps

1. Invoke Superpowers `writing-plans` for task discipline and file-level task boundaries.
2. Apply `using-odk-bridge` Output Redirection Rules when plan tries to write to `docs/plans/`.
3. Process output per active mode: transform into ODK `execution-plan.md` format with AC-Task traceability, read-only context, file-level scope, state ownership fields when declared in design, anti-fake completion checks, expected/actual verification, review gates, and dependency graph in strict mode.
4. Populate `execution-plan.md` AC-Task 追溯 with Task assignments.

## Output

- Written to `.codespec/changes/<id>/execution-plan.md`
- Report Task count, dependency structure, and any scope gaps
