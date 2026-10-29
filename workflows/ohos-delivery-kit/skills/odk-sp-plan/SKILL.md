---
name: odk-sp-plan
description: "Use when Superpowers is installed AND the user wants writing-plans discipline for execution-plan.md (task decomposition, file-level boundaries, AC-Task trace). Falls back to odk-plan if unavailable."
license: MIT
---

# ODK SP Plan

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

Before writing `execution-plan.md`, apply `odk-plan`'s build-product and command resolution step (without replacing the active bridge's task decomposition).
<!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
Read `contracts/skill-guides/delivery/device-version.md` to skip daily selection for QEMU, ask daily versus existing for every other product, and persist the choice and preparation method in `## 构建与验证环境`. Preserve this environment section in every output mode.
<!-- /ODK:reference -->

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md`
- Report Task count, dependency structure, and any scope gaps
