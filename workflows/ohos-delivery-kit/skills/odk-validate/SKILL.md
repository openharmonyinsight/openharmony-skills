---
name: odk-validate
description: "Use when checking a change against the ODK delivery contract (Level A/B/C/D readiness) before archiving. Final gate. Zero plugin dependencies."
license: MIT
---

# ODK Validate

## Input

- Change directory path (e.g. `.codespec/changes/issue-12345-arkui-focus/`)
- If not specified, auto-detect from `.codespec/changes/` (fail if multiple exist)

## Sources

- Artifact contract: installed `contracts/artifacts.yaml` (OpenCode: `{{ASSET_ROOT}}/contracts/artifacts.yaml`)
- Templates: installed `templates/ai/` (OpenCode: `{{ASSET_ROOT}}/templates/ai/`)
- If running inside the ODK repo, prefer `{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py <change-dir>` for strict checks and use this skill to explain/remediate failures

## Steps

1. Resolve the target change directory and load the artifact contract.
2. Check Level A/B: directory name (must match `issue-<number>-<slug>` or `draft-<yyyymmdd>-<slug>`, e.g. `issue-12345-arkui-focus`), required files, required sections, and conditional-section warnings per `artifacts.yaml`.
3. Check Level C traceability:
   - every `spec.md` AC appears in the verification mapping with a non-empty verification method
   - every AC appears in `execution-plan.md` AC-to-Task traceability with a Task and verification method
   - every traced Task has a Task list row and Task detail section with Files and Verification tables
   - every traced Task in `execution-plan.md` 代码范围映射 has a non-empty file (AC→Task→code closure)
4. Check Level D archive readiness:
   - no critical placeholders remain in required archive content
   - implementation files, Task links, verification status, and Actual Result are backfilled where implementation has happened
   - optional evidence under `evidence/reviews/` and `evidence/gates/` is non-empty and supports any passing conclusion
5. Report PASS/WARN/FAIL by level. Warnings do not block draft review, but archive readiness requires explicit resolution or accepted risk.

## Output

Print concise validation results with file/section/table references for each issue.

If all levels pass, report archive readiness. Do not generate gate files unless the user explicitly asks for optional process evidence.
