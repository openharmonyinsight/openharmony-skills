
# ODK Plan

Use when writing ODK execution-plan.md (AC-to-Task traceability, file-level scope, anti-fake checks). Default template-driven, zero plugin dependencies. Use after design.md.

## Prerequisites

- `spec.md` with numbered AC list
- `design.md` with architecture decisions (required for state ownership fields when design declares complex state)

## Input

1. Read `spec.md` AC list
2. If `design.md` contains `状态归属与不变量`, read the declared dimensions — these map to the state ownership fields each Task must fill in

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.execution-plan` (additional prohibitions) and `agent_instructions.plan` before generating content
1. Read template from `{{PLUGIN_ROOT}}/templates/ai/execution-plan.md`
2. Generate `execution-plan.md` per the template. Fill the required traceability, task detail, verification, and code-scope fields enough to pass artifact contract validation. For each Task, fill「任务间接口」（Produces=供后续 Task 依赖的接口签名/错误码/innerAPI/数据结构，Consumes=来自前置 Task 的契约；无跨 Task 契约写「无」），让只读单 Task 的执行者也能对齐跨 Task 命名与签名。
3. Populate `execution-plan.md` AC-to-Task 追溯 (AC / Task / 验证状态) with the Task assignments.

## Quality Boundary

- This skill owns routing, profile application, context loading, and populating `execution-plan.md` AC-Task 追溯.
- `execution-plan.md` template owns required tables and fields.
- `scripts/validate-artifacts-contract.py` owns machine-checkable traceability and table completeness.

## Output

Write to `.codespec/changes/<id>/execution-plan.md`

Suggest next step: run `{{CMD_PREFIX}}implement` to begin Task-by-Task implementation.
