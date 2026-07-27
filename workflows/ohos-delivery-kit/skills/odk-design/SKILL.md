---
name: odk-design
description: "Use when writing ODK design.md (architecture, decisions, Mermaid, spec-AC references, conditional security check). Default template-driven, zero plugin dependencies. Use after spec.md."
license: MIT
---

# ODK Design

## Key Rules

- Keep the base `design.md` template minimal for simple changes.
- For complex state/ownership/lifecycle/concurrency/compatibility/performance/capacity/migration changes, use the conditional `状态归属与不变量` guidance embedded in the `design.md` template.
- Design owns internal implementation moved from spec AC (state machines, registries/caches, internal flows, traversal algorithms) → `状态归属与不变量` conditional section.
- Internal implementation invariants are verified via TDD in `execution-plan.md` tasks (design declares invariants; verification happens at implementation, not by explicit design-level verification declarations).

## Prerequisites

- `proposal.md` exists and has been approved (success criteria finalized)
- `spec.md` exists with acceptance criteria and business rules

## Input

1. Read `proposal.md` summary (first 15 lines or user-provided summary)
2. Read `spec.md` AC list and business rules (for architecture decisions to reference)

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.design` (additional sections, fragments) and `agent_instructions.design`
1. **Code fact baseline (conditional):** If the change modifies an existing module (not pure greenfield, pure docs, or config-only), search the codebase for key facts the design will reference:
   - Search for existing data structures, key function signatures, and runtime flows in the affected module(s)
   - Record findings as a brief code fact baseline: file:line references for key structures, signatures, and flow paths
   - If search results contradict assumptions from `proposal.md` or `spec.md`, surface the discrepancy to the user before proceeding to generate design
   - Skip this step for brand-new modules with no existing code, pure documentation changes, or config-only changes
2. Read template from `{{ASSET_ROOT}}/templates/ai/design.md`
3. Generate `design.md` per the template. Conditionally include `代码事实基线`, `类图`, and `状态归属与不变量` when applicable — add `类图` (Mermaid `classDiagram`) when the change involves class/interface inheritance or implementation hierarchies (e.g. IPC interface→proxy→stub→impl) or cross-module composition. Reference specific `spec.md` AC numbers in design decisions.
4. If Step 1 produced code facts, populate `代码事实基线`; otherwise omit it.
5. After design is generated, review spec's `错误码定义` and `接口变更分析` — resolve any `TBD` values, and update if design decisions introduce new error codes or change interface signatures.
6. **安全基础检查（条件触发）**:
   - 触发来源：`proposal.md` 的 `安全/权限` 维度 = 「是」（单一来源，与 `artifacts.yaml` 的 `conditional_sections.required_when` 一致）。
   - 「安全基础检查」章节的触发条件（信任边界/敏感数据/加密认证等）见 `artifacts.yaml` 的 `conditional_sections.required_when`；**升级到独立 `threat-model.md` 的高风险判据**见 `odk-security-threat-model/SKILL.md` 的触发条件表，本步骤不重复枚举。
   - 如 `安全/权限` 维度 = 「是」，在 `design.md` 中展开"安全基础检查"章节并填写适用维度；命中高风险判据时按 `深度威胁分析（如需）` 章节指引产出 `threat-model.md`。
   - 如不满足，在章节中填写"不涉及"并说明理由。

## Output

Write to `.codespec/changes/<id>/design.md`

Confirm with the user that design decisions are aligned with requirements.

Suggest next step: run `{{CMD_PREFIX}}plan` to generate the execution plan with AC-to-Task traceability.
