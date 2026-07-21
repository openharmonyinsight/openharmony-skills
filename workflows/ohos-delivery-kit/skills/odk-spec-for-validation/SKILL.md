# ODK Spec for Validation

Use when deriving spec-for-validation.md (integration/system scenarios, SC→AC trace) from spec.md. Parallel bypass, does not block main flow. Zero plugin dependencies.
Runs independently after spec.md is complete, alongside plan/implement/review.

This artifact is named "spec-for-validation" (not "test-spec") to distinguish it from
test design activities. It specifies **what to validate** (acceptance scenarios for
verification), not **how to test** (test strategy, test case design, test automation).

## Execution Mode

Bypass branch — runs independently alongside plan/implement/review to avoid context pollution.
Inputs are `proposal.md` and `spec.md` (no code dependency).

## Prerequisites

- `proposal.md` exists (success criteria for system-level scenarios)
- `spec.md` exists (AC list, error codes, exception rules)
- `design.md` exists (optional — enhances integration validation scenarios with module details and ADR traceability)
- Load `using-odk` for archive structure and profile detection.

## Input

1. Read `proposal.md` — success criteria, end-to-end flows, non-functional requirements
2. Read `spec.md` — AC numbers, error codes, exception rules
3. Read `design.md` (optional) — architecture decisions, module impact table
4. Read template from `{{ODK_ASSET_ROOT}}/templates/ai/spec-for-validation.md`

## Steps

0. Profile Detection: apply `template_overrides.spec_for_validation` if matched
1. Derive AC range and validation level (L2/L3/L4) from spec.md scope; populate the overview table (associated ACs, validation level, tags)
2. Generate incremental validation scenarios (SC-N) — **conditional, not mandatory**:
   - **Integration**: cross-module interaction derived from **spec.md AC** (interface-observable behavior) + spec.md error codes; enhance with design.md module impact if available
   - **System**: end-to-end journeys and non-functional scenarios derived from **proposal.md success criteria** (system-level) + spec.md AC
   - SC 的 Given/When 从 spec AC 的可观测行为派生**集成/系统视角**（跨模块、并发、重放、端到端）；**不重复 spec 用户故事或 proposal 用户场景的可操作序列**（那是 spec US 职责，spec-for-validation 只做集成/系统验证增量）。
   - **Compatibility**: version/device combination validation and cross-version regression scenarios from proposal.md compatibility requirements
   - **Conditional — generate only when the requirement actually involves the domain**:
     - `performance` scenarios: only when proposal.md or spec.md contains performance metrics / SLA / latency / throughput requirements
     - `power` scenarios: only when the requirement explicitly involves power consumption / battery / standby / wakeup constraints
     - `security` scenarios: only when the proposal's `安全/权限` dimension = 「是」 (involves permission / authentication / encryption / data protection / compliance); the `[安全与权限 security]` scenario verifies mitigations identified in `安全基础检查` / `threat-model.md`, traced to spec.md AC
   - Decision method: scan proposal.md non-functional requirements section (the `安全/权限` dimension) + spec.md AC keywords for performance/power/security; skip the corresponding scenario when no relevant requirement exists — do NOT leave empty placeholders
3. Each SC references >=1 spec.md AC number (traceability)
4. Generate data-driven parameter tables **only when** a scenario has multiple boundary-value parameter combinations cumbersome to express inline; nest the table under its `### SC-N` so the association is implicit by location. Simple scenarios (binary outcomes, single thresholds) keep parameter values inline in Given/When/Then — do NOT spawn a table for them
5. Extract reusable Given/When/Then concept definitions; reference concept names in scenarios instead of repeating steps
6. Populate environment prerequisites section from proposal.md and spec.md (validation environment, accounts/devices, dependencies/mocks)
7. Initialize change history table as v0.1 with current date

## Key Rules

- Every SC-N must reference >=1 spec.md AC number
- Do NOT repeat normal-flow or exception scenarios already in spec.md — only incremental scenarios (concurrency, replay, cross-component, runtime metrics)
- Validation focus: user-observable behavior and **public interfaces** (public API / SDK-exposed interfaces) input/output, NOT internal implementation details
- Out of scope: unit test coverage; **internal interfaces** (inner / system / internal / private / @hide annotated methods) are NOT within validation scope — covered by unit tests
- Tags: `happy-path` `negative` `compatibility` `performance` `security` `power` `smoke` `regression` `api`
- `performance` / `power` / `security` tags are used only when the requirement actually involves the corresponding domain
- Performance scenarios MUST include quantified metrics (e.g. P95 latency, throughput) and baseline environment description; do NOT generate vague assertions like "performance is acceptable"
- Compatibility scenarios MUST list specific version/device combinations and cross-version operations
- Security scenarios (`security` tag) verify observable behavior (unauthorized access, information leakage, audit logging) for mitigations identified in `安全基础检查` / `threat-model.md`, traced to spec.md AC — NOT re-define error codes from spec.md
- Data-driven tables are conditional and scenario-scoped: only multi-boundary-value scenarios get a table (nested under its `### SC-N`); simple scenarios keep values inline
- Data-driven tables support two formats: inline markdown tables (`|` separated) and external CSV references (`<table:path/to/data.csv>`)
- Concept definitions: after extracting reusable Given/When/Then step combinations into concept definitions, reference the concept name in scenarios instead of repeating the steps
- Optional artifact: does not block the main delivery flow; generation failure is a warning, not an error

## Output

Write to `.codespec/changes/<id>/spec-for-validation.md`

Suggest next step: run `{{CMD_PREFIX}}plan` to generate the execution plan (spec-for-validation does not block the main flow).
