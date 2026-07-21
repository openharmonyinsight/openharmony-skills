
# ODK Spec

Use when writing ODK spec.md (WHEN/THEN acceptance criteria, error codes, verification mapping). Default template-driven, zero plugin dependencies. Use after proposal.md is approved.

## Prerequisites

- `proposal.md` with finalized success criteria

## Input

1. Read `proposal.md` success criteria and triage result

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.spec` (additional AC categories, fragments) and `agent_instructions.specify` before generating content
1. **Code fact check (conditional):** If the change involves existing APIs, error codes, or data structures, search the codebase before generating spec:
   - Search for existing API signatures, error code definitions, and data structures referenced in the AC scope
   - Confirm interface details are accurate before writing ACs
   - If code facts contradict assumptions from `proposal.md`, surface and resolve before writing ACs
   - Skip this step for pure new features with no existing code dependencies, pure documentation changes, or config-only changes
2. Read template from `{{ODK_ASSET_ROOT}}/templates/ai/spec.md`
3. Generate `spec.md` per the template. Fill in error code values and interface signatures with concrete values where discoverable from the code fact check (Step 1); mark genuinely unknown values as `TBD` with a reason.

## Key Rules

- Do not invent API signatures, error code values, or data structures. Resolve contradictions from code facts before writing ACs.
- Keep ACs concrete enough for the template's verification mapping; code mapping (AC→implementation files) lives in `execution-plan.md`.
- AC 使用 Given/When/Then 格式：Given 前置条件；When 用户/业务可操作动作；Then 通过三层接口边界（public/system/inner API + 终端用户可感知）可观测的结果。
- AC 的 Then 禁止部件内部实现（数据结构/状态机/内部流程/算法）——移 `design.md`「状态归属与不变量」。判定：Then 能否仅凭公开接口判定？需查内部状态则移 design。

## Quality Boundary

- This skill owns profile application, code fact checking, contradiction handling, context loading, and output path.
- `spec.md` template owns required sections, AC format (Given/When/Then) + three-tier observability guidance, verification mapping.
- Internal implementation (data structures/state machines/flows/algorithms) owned by `design.md`; code mapping (AC→implementation files + verification status) owned by `execution-plan.md`.
- `{{ODK_EXECUTABLE_ROOT}}/validator/validate-artifacts-contract.py` owns machine-checkable AC coverage, verification mapping, and traceability checks.

## Output

Write to `.codespec/changes/<id>/spec.md`.

Do not generate `gates/` by default. If the user explicitly wants process evidence, record approval notes under an optional evidence directory such as `evidence/gates/`.

Suggest next step: run `{{CMD_PREFIX}}design` to generate the architecture design, which will reference spec AC numbers and resolve any TBD error codes or interface signatures.
