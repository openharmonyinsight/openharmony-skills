---
name: odk-plan
description: "Use when writing ODK execution-plan.md (AC-to-Task traceability, file-level scope, anti-fake checks). Default template-driven, zero plugin dependencies. Use after design.md."
license: MIT
---

# ODK Plan

## Prerequisites

- `spec.md` with numbered AC list
- `design.md` with architecture decisions (required for state ownership fields when design declares complex state)

## Input

1. Read `proposal.md` to check `API/SDK` dimension
2. Read `spec.md` AC list
3. If `design.md` contains `状态归属与不变量`, read the declared dimensions — these map to the state ownership fields each Task must fill in

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.execution-plan` (additional prohibitions) and `agent_instructions.plan` before generating content
1. Read template from `{{ASSET_ROOT}}/templates/ai/execution-plan.md`
2. **API 声明文件任务（条件触发）**：若 proposal.md `API/SDK` = 「是」，必须在所有任务的最前面插入一个 API 声明文件修改任务（排在 Task-1），任务内容为"根据 spec.md `## API 规格定义` 修改声明文件"。该任务排在第一位的原因是：后续功能实现任务依赖声明文件的修改结果，声明文件未完成时其他任务无法开展。
3. Generate `execution-plan.md` per the template. Fill the required traceability, task detail, verification, and code-scope fields enough to pass artifact contract validation. For each Task, fill「任务间接口」（Produces=供后续 Task 依赖的接口签名/错误码/innerAPI/数据结构，Consumes=来自前置 Task 的契约；无跨 Task 契约写「无」），让只读单 Task 的执行者也能对齐跨 Task 命名与签名。
   If any proposal `资源开销审视` dimension is `required`, expand `资源验证矩阵` (`contracts/artifacts.yaml#resource_contract`). Commands/evidence layout are subsystem-owned (often `evidence/resource/`); ODK requires the section and meaningful, non-placeholder content without imposing a subsystem measurement schema.
4. Populate `execution-plan.md` AC-to-Task 追溯 (AC / Task / 验证状态) with the Task assignments.
5. Self-Review the generated `execution-plan.md` before handing off — find issues and fix them inline, then move on without a second self-review pass. Self-review is an AI self-check only; it does not replace human approval or `odk-review`, and the Phase Gate in `using-odk` still applies:
   - **跨 Task 契约一致性**：逐 Task 比对「任务间接口」——后续 Task 的 Consumes 是否对得上某个前置 Task 的 Produces（函数名/参数/错误码/数据结构）；`clearLayers()` 在 TASK-3 产出、TASK-7 却写成 `clearFullLayers()` 就是 bug，就地改正。
   - **占位符扫描**：确认无 `TBD`/`TODO`/`适当处理`/`补充测试`/`参考上文` 等不可执行占位（见「禁止项」）。
   - **Spec 覆盖**：确认「AC 到 Task 追溯」每个 AC 都有 Task 承接；发现未覆盖的 spec 要求就补 Task。
   三项都干净则进入下一步（写出 `execution-plan.md`），等待人工审批。

## Quality Boundary

- This skill owns routing, profile application, context loading, and populating `execution-plan.md` AC-Task 追溯.
- `execution-plan.md` template owns required tables and fields.
- `{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py` owns machine-checkable traceability and table completeness.

## Output

Write to `codespec/changes/<id>/execution-plan.md`

Suggest next step: run `{{CMD_PREFIX}}implement` to begin Task-by-Task implementation.
