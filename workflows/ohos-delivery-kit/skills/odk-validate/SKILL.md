---
name: odk-validate
description: "Use when checking a change against the ODK delivery contract (Level A/B/C/D readiness) before archiving. Final gate. Zero plugin dependencies."
license: MIT
---

# ODK Validate

## Input

- Change directory path (e.g. `codespec/changes/REQ-12345-arkui-focus/`)
- If not specified, auto-detect from `codespec/changes/` (fail if multiple exist)

## Sources

- Artifact contract: installed `contracts/artifacts.yaml` (OpenCode: `{{ASSET_ROOT}}/contracts/artifacts.yaml`)
- Templates: installed `templates/ai/` (OpenCode: `{{ASSET_ROOT}}/templates/ai/`)
- Strict validator: `{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py`. It is installed with ODK on every supported platform; use this skill to explain and remediate its findings.
- Archive migration validator: `{{EXECUTABLE_ROOT}}/validate-archive-migration.py`. Use `plan` before moving legacy archives and `check-staged` before committing the migration.

## Steps

1. Resolve the target change directory and load the artifact contract.
2. Check Level A/B: directory name (must match `<req>-<slug>` or `draft-<yyyymmdd>-<slug>`, e.g. `REQ-12345-arkui-focus`), required files, required sections, and conditional-section warnings per `artifacts.yaml`.
3. Check Level C traceability:
   - every `spec.md` AC appears in the verification mapping with a non-empty verification method
   - every AC appears in `execution-plan.md` AC-to-Task traceability with a Task and verification method
   - every traced Task has a Task list row and Task detail section with Files and Verification tables
   - every traced Task in `execution-plan.md` 代码范围映射 has a non-empty file (AC→Task→code closure)
   - **DFX 故障模式分析**：`design.md` 必须包含 `### DFX 故障模式分析` 子节，其表格列必须为：分析对象/故障模式/故障影响/故障原因/严酷度/恢复措施/关键日志/大数据打点事件/来源。每个命中行必须完整，且来源符合 `<repo>@<commit>:docs/dfx/fmea.yaml#<record-id>`；空数据行 → WARN。
4. Check Level D archive readiness:
   - no critical placeholders remain in required archive content
   - implementation files, Task links, verification status, and Actual Result are backfilled where implementation has happened
   - optional evidence under `evidence/reviews/` and `evidence/gates/` is non-empty and supports any passing conclusion
5. Report PASS/WARN/FAIL by level. Warnings do not block draft review, but archive readiness requires explicit resolution or accepted risk.
6. Resource constraints (`contracts/artifacts.yaml#resource_contract`): parse `资源开销审视`; `review-required` blocks archive; `required` needs meaningful, non-placeholder Spec/Design/Plan resource sections. Archive runs root `AGENTS.md` `odk_resource_gate` (missing/non-zero/timeout fails). ODK orchestrates the subsystem gate but does not recompute its measurements.
7. Run `python3 {{EXECUTABLE_ROOT}}/validate-artifacts-contract.py <change-dir>` for Draft validation, or add `--archive` before `<change-dir>` for the archive gate. Report the exact command and result.

## Output

Print concise validation results with file/section/table references for each issue.

If all levels pass, report archive readiness. Do not generate gate files unless the user explicitly asks for optional process evidence.
