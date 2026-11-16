---
name: odk-validate
description: "Use when checking a change against the ODK delivery contract (Level A/B/C/D readiness) before archiving. Final gate. Zero plugin dependencies."
license: MIT
---

# ODK Validate

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and obtain the effective
contract before choosing artifacts, sections or phase prerequisites.
<!-- /ODK:reference -->

## Input

- Change directory path (e.g. `codespec/changes/arkui/12345/`)
- If not specified, resolve the current repository name and auto-detect from `codespec/changes/<repo-name>/` (fail if multiple exist)

## Sources

- Artifact contract: installed `contracts/artifacts.yaml` (OpenCode: `contracts/artifacts.yaml`)
- Templates: installed `templates/ai/` (OpenCode: `templates/ai/`)
- Strict validator: `runtime/executables/validate-artifacts-contract.py`. It is installed with ODK on every supported platform; execute it directly and use this skill to explain and remediate its findings.
- Archive migration validator: `runtime/executables/validate-archive-migration.py`. Use `plan --map <map.tsv>` before moving legacy archives and `check-staged --map <the-same-map.tsv>` before committing so old-source deletion and planned-target conservation are verified.

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/feedback.md -->
Read `contracts/skill-guides/delivery/feedback.md`. Record validation findings in
the existing plan, identify affected owning artifacts and return corrections to
the coordinator. Re-run on the final backfilled documents; document validation
does not prove semantic consistency or successful target tests.
<!-- /ODK:reference -->

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

1. Resolve the target change directory and load the artifact contract. Invoking this skill authorizes the agent to run the packaged document validator through the available shell/terminal tool and parse its stdout, stderr and exit code; do not merely print a command for the user to copy. Resolve the executable from the installation selected by the `using-odk` resource check, including symlinked host skills. Quote the absolute executable and change-directory paths. If no execution tool exists, report NOT RUN and the exact command; never report PASS from reading instructions alone. Archive validation may execute the repository's declared resource gate; preserve its existing authorization requirements.
2. Check Level A/B: repository segment and directory name (formal leaf exactly matches `<proposal-id>`, or draft matches `draft-<yyyymmdd>-<slug>`), required files, required sections, and conditional-section warnings per `artifacts.yaml`. A standalone `<!-- 不涉及：章节名；理由：具体原因 -->` closes only the named optional condition; it cannot waive required sections or trigger-specific gates.
3. Check Level C traceability:
   - **API metadata contract**：`API/SDK=是` 时至少存在一个适用的 `arkts-api-spec.yaml` 或 `c-api-spec.yaml`，并校验 schemaVersion、language、API kind、id、parent、enum/member 闭合、类型专属必填字段和双语三要素/五要素。`spec.md` 只允许 API 概览，不得重新展开逐 API 规格；概览 API ID 必须与所有适用 metadata 文件的并集完全一致。默认 validate、archive 和 design-docs submission 都必须校验完整 API contract version chain：metadata、`spec.md`、`design.md`、`execution-plan.md` 全部存在且均为 `1.0.0`。任何缺失或不一致输出一个 actionable blocking finding，列出全部 Artifact / Declared / Required、禁止手改版本；可识别的 0.14 旧 Markdown 链路先建议 `{{CMD_PREFIX}}upgrade-api-chain`，无法闭环时要求从 proposal 重跑，并指向 `docs/migrations/0.15.0-api-metadata-hard-migration.md`。旧 `api-spec.yaml`、旧混合语言声明 diff、缺失或不一致的契约版本均 FAIL。
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
   - every AC traceability row is Pass; a later Pass cannot mask Fail/Blocked
   - every Task has status Done/Complete/Completed/已完成, with no unchecked Task Steps
   - implementation files and Task links are backfilled; each Verification row has meaningful Actual Result and explicit Final Status=Pass (retain historical Red failures)
   - the existing plan's 问题闭环 table, when present, has complete, unique finding IDs and valid AC/Task/artifact references; blocking items must be Resolved, nonblocking accepted risks must be Accepted with disposition and recheck evidence
   - optional evidence under `evidence/reviews/` and `evidence/gates/` is non-empty and supports any passing conclusion
   - every R1/R2 Task has `evidence/reviews/task-<n>/verdict.md` with `verdict: PASS` and `blocking_findings: 0`; R2 also has the arch/scope/security reports (validator enforcement: Draft missing/non-PASS → WARN, Archive → FAIL)
   - `API/SDK=是` changes must archive the applicable metadata file(s) and language-specific declaration-diff evidence (validator enforcement: Draft missing → WARN, Archive missing → FAIL). When `arkts-api-spec.yaml` exists, require `evidence/task1-arkts-api-declaration-en.diff` and `evidence/task1-arkts-api-declaration-zh.diff`. When `c-api-spec.yaml` exists, require `evidence/task1-c-api-declaration-en.diff` and `evidence/task1-c-api-declaration-zh.diff`. A change involving both languages requires all four files. Each file must contain only the target API repository's paths. Declaration diffs must be checked against the matching metadata file: declarations must appear in continuous new-side hunks grouped under the target file, with the complete doc comment and declaration in one hunk; `@since`, `@syscap`, permission, platform, and application-model markers must match metadata. Duplicate signatures must be uniquely bound by API identity or source position. The validator also enforces documentation closure: every non-`N/A` / non-`不适用` API-level description element, parameter description, return description, and error-code description must be covered by the matching language's declaration comment. It rejects element-name labels such as `Scenario:` / `Notes:` and `notes` values that merely restate API availability already represented by `since` or error-code tables already represented by `returnType` / `errorCodes`. Coverage is normalized token matching, not a natural-language semantic proof. This remains a structural/delivery gate, not a compiler.
5. Report PASS（通过）/WARN（警告）/FAIL（失败）by level. Warnings do not block draft review, but archive readiness requires explicit resolution or accepted risk. API signatures are opaque document text: check presence, placeholders and duplicates only, not C/ArkTS syntax, types or array bounds. Document PASS is not compilation success. Source review and target toolchain/CI own language correctness; report unrun checks as NOT VERIFIED. Do not require GCC for document validation.
6. Resource constraints (`contracts/artifacts.yaml#resource_contract`): parse `资源开销审视`; `review-required` blocks archive; `required` needs meaningful, non-placeholder Spec/Design/Plan resource sections. Archive runs root `AGENTS.md` `odk_resource_gate` (missing/non-zero/timeout fails). ODK orchestrates the subsystem gate but does not recompute its measurements.
7. Run `python3 runtime/executables/validate-artifacts-contract.py <change-dir>` for Draft validation, or add `--archive` before `<change-dir>` for the archive gate. Report the exact command and result.
   In the automatic post-implementation/pre-PR handoff, use `--archive`: metadata is not required yet. Do not use `--design-docs-submit` or create dummy PR entries before a real PR exists. Return results to the calling coordinator; do not recursively invoke review/implement or independently start submission. Keep standalone Draft/archive validation available.
8. If validation is the final step before a GitCode commit, push, or PR, resolve the design-docs repository address (priority: `codespec/profile.yaml` if present → `odk_config_ext.yaml` → `odk_config.yaml`; do not warn if `codespec/profile.yaml` is absent) and remind the user that `codespec/` documents must be submitted separately to that design-docs repository. If no address can be resolved, report “待开发者填写”; do not guess or automatically push across repositories. For actual design-docs submission, require `metadata_tracking.yaml` and run the validator with `--design-docs-submit`.

## Output

Print concise validation results with file/section/table references for each issue.

For API signatures, use explicit template markers (e.g. `<完整签名>` or `[待填写]`), not keyword guesses inside source text. Identifier substrings such as `TODO_COUNT` and quoted literals are not placeholders. Draft and archive checks share this policy; ordinary prose placeholder checks remain unchanged.

If all levels pass, report archive readiness and include the GitCode `design_docs_repository` reminder when submission is next. Do not generate gate files unless the user explicitly asks for optional process evidence.
