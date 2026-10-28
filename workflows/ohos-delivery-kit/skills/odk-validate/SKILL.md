---
name: odk-validate
description: "Use when checking a change against the ODK delivery contract (Level A/B/C/D readiness) before archiving. Final gate. Zero plugin dependencies."
license: MIT
---

# ODK Validate

## Input

- Change directory path (e.g. `codespec/changes/arkui/12345/`)
- If not specified, resolve the current repository name and auto-detect from `codespec/changes/<repo-name>/` (fail if multiple exist)

## Sources

- Artifact contract: installed `contracts/artifacts.yaml` (OpenCode: `contracts/artifacts.yaml`)
- Templates: installed `runtime/assets/templates/ai/` (OpenCode: `runtime/assets/templates/ai/`)
- Strict validator: `runtime/executables/validate-artifacts-contract.py`. It is installed with ODK on every supported platform; execute it directly and use this skill to explain and remediate its findings.
- Archive migration validator: `runtime/executables/validate-archive-migration.py`. Use `plan --map <map.tsv>` before moving legacy archives and `check-staged --map <the-same-map.tsv>` before committing so old-source deletion and planned-target conservation are verified.

## Steps

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

1. Resolve the target change directory and load the artifact contract. Invoking this skill authorizes the agent to run the packaged document validator through the available shell/terminal tool and parse its stdout, stderr and exit code; do not merely print a command for the user to copy. Resolve the executable from the installation selected by the `using-odk` resource check, including symlinked host skills. Quote the absolute executable and change-directory paths. If no execution tool exists, report NOT RUN and the exact command; never report PASS from reading instructions alone. Archive validation may execute the repository's declared resource gate; preserve its existing authorization requirements.
2. Check Level A/B: repository segment and directory name (formal leaf exactly matches `<proposal-id>`, or draft matches `draft-<yyyymmdd>-<slug>`), required files, required sections, and conditional-section warnings per `artifacts.yaml`. A standalone `<!-- 不涉及：章节名；理由：具体原因 -->` closes only the named optional condition; it cannot waive required sections or trigger-specific gates.
3. Check Level C traceability:
   - AC definition IDs use `AC-<用户故事号>.<序号>`: ASCII digits or `DFX` for the story and ASCII digits for the sequence (e.g. `AC-1.1`, `AC-DFX.1`); both forms participate in verification/Task/DFX traceability; malformed IDs warn in Draft and fail Archive/design-docs submission
   - The format gate checks visible spec definitions, verification mapping AC cells and execution-plan traceability AC cells against `resource_contract.ac_id_pattern` in the installed artifact contract. The default uses ASCII digits and the DFX namespace; a missing pattern falls back to that default, while an invalid regex reports a Draft warning / Archive failure and then uses the default.
   - every `spec.md` AC appears in the verification mapping with a non-empty verification method
   - every AC appears in `execution-plan.md` AC-to-Task traceability with a Task and verification method
   - every traced Task has a Task list row and Task detail section with Files and Verification tables
   - every traced Task in `execution-plan.md` 代码范围映射 has a non-empty file (AC→Task→code closure)
   - **DFX 故障模式分析**：`design.md` 必须包含 `### DFX 故障模式分析` 子节，其表格列必须为：分析对象/故障模式/故障影响/故障原因/严酷度/恢复措施/关键日志/大数据打点事件/来源。每个命中行必须完整，且来源符合 `<repo>@<commit>:docs/dfx/fmea.yaml#<record-id>`；空数据行 → WARN。
   - **DFX 故障模式处置（Level C3，故障模式拦截项）**：主表有命中行或存在 AD 推导条目时，`### DFX 故障模式处置` 必须存在且逐条覆盖（漏处置行、悬空 AC 引用、非法处置值、空证据列、AD 处置行对象/故障模式与原条目不符 → FAIL；整表缺失 → Draft WARN / Archive FAIL）。处置为「新增 AC/复用 AC」的关联 AC 必须存在于 spec.md；处置为「纳入设计约束」的证据列须含设计决策/约束引用与关联 TASK 编号；Archive 时关联 AC 与设计约束 Task 在「AC 到 Task 追溯」的全部行验证状态必须为 Pass（同一 AC/Task 多行时后续 Pass 不得掩盖 Fail/Blocked）。
4. Check Level D archive readiness:
   - no critical placeholders remain in required archive content
   - implementation files, Task links, verification status, and Actual Result are backfilled where implementation has happened
   - optional evidence under `evidence/reviews/` and `evidence/gates/` is non-empty and supports any passing conclusion
   - `API/SDK=是` changes must archive `evidence/task1-api-declaration-en.diff` and `evidence/task1-api-declaration-zh.diff` (validator enforcement: Draft missing → WARN, Archive missing → FAIL)
5. Report PASS（通过）/WARN（警告）/FAIL（失败）by level. Warnings do not block draft review, but archive readiness requires explicit resolution or accepted risk. API signatures are opaque document text: check presence, placeholders and duplicates only, not C/ArkTS syntax, types or array bounds. Document PASS is not compilation success. Source review and target toolchain/CI own language correctness; report unrun checks as NOT VERIFIED. Do not require GCC for document validation.
6. Resource constraints (`contracts/artifacts.yaml#resource_contract`): parse `资源开销审视`; `review-required` blocks archive; `required` needs meaningful, non-placeholder Spec/Design/Plan resource sections. Archive runs root `AGENTS.md` `odk_resource_gate` (missing/non-zero/timeout fails). ODK orchestrates the subsystem gate but does not recompute its measurements.
7. Run `python3 runtime/executables/validate-artifacts-contract.py <change-dir>` for Draft validation, or add `--archive` before `<change-dir>` for the archive gate. Report the exact command and result.
   In the automatic post-implementation/pre-PR handoff, use `--archive`: metadata is not required yet. Do not use `--design-docs-submit` or create dummy PR entries before a real PR exists. Return results to the calling coordinator; do not recursively invoke review/implement or independently start submission. Keep standalone Draft/archive validation available.
8. If validation is the final step before a GitCode commit, push, or PR, resolve the design-docs repository address (priority: `codespec/profile.yaml` if present → `odk_config_ext.yaml` → `odk_config.yaml`; do not warn if `codespec/profile.yaml` is absent) and remind the user that `codespec/` documents must be submitted separately to that design-docs repository. If no address can be resolved, report “待开发者填写”; do not guess or automatically push across repositories. For actual design-docs submission, require `metadata_tracking.yaml` and run the validator with `--design-docs-submit`.

## Output

Print concise validation results with file/section/table references for each issue.

For API signatures, use explicit template markers (e.g. `<完整签名>` or `[待填写]`), not keyword guesses inside source text. Identifier substrings such as `TODO_COUNT` and quoted literals are not placeholders. Draft and archive checks share this policy; ordinary prose placeholder checks remain unchanged.

If all levels pass, report archive readiness and include the GitCode `design_docs_repository` reminder when submission is next. Do not generate gate files unless the user explicitly asks for optional process evidence.
