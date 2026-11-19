---
name: odk-sp-brainstorm
description: "Use when Superpowers is installed AND the user wants one-session proposal+spec+design via Superpowers brainstorming. Output redirected to ODK archive. Falls back to odk-propose+odk-spec+odk-design if unavailable."
license: MIT
---

# ODK SP Brainstorm

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
Read `contracts/skill-guides/router/delivery-levels.md` and use the effective
contract. It takes precedence over standard-only artifact lists below; native
OpenSpec schemas remain standard/critical and lite uses the base flow.
<!-- /ODK:reference -->

## Purpose

Invoke Superpowers `brainstorming` for requirement clarification and approach selection. Redirect output to ODK archive format in `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `codespec/changes/<repo-name>/<proposal-id>/` skeleton must exist (run `{{CMD_PREFIX}}init` first).
- If Superpowers skills are unavailable, fall back to `odk-brainstorm` (built-in lightweight interview skill, zero dependencies) instead of jumping straight to `odk-propose`. Clearly report the degradation and load `odk-brainstorm` to run the interview first.

## Steps

1. Invoke Superpowers `brainstorming` for requirement clarification and approach selection.
2. Apply `using-odk-bridge` Output Redirection Rules when brainstorming tries to write to `docs/superpowers/specs/`.
3. Process output per active mode: ensure `proposal.md`, `spec.md`, `design.md` conform to ODK templates in strict mode; when `API/SDK=是`, also run the `odk-spec` API metadata workflow and produce validated the applicable API metadata files plus a summary-only API overview; passthrough does not waive this API contract; preserve otherwise compatible plugin format in passthrough mode; append ODK sections in merge mode. Strict/merge `proposal.md` must include `1+8 设备差异规格` and `外部依赖`. For `design.md`, rely on `using-odk-bridge` Design State Ownership Rules so complex state changes include explicit ownership and checkable invariants. In strict mode, also inherit `odk-design`'s DFX design and security steps:
   - DFX 设计（必填，Step 6）：执行 4 步故障模式分析流程（识别涉及仓库 → 委托内置 `odk-fmea` skill 执行故障模式分析 → 按落盘契约回填故障模式分析表 → 处置决策与 AC 回填），详见 `odk-design/SKILL.md` Step 6；降级路径契约见 `contracts/dfx-fmea-matcher.yaml`。
   - Security baseline check (conditional, Step 7): when `proposal.md`「安全/权限」=「是」, expand `design.md`「安全基础检查」; if high-risk criteria are hit, produce `threat-model.md` (see `odk-security-threat-model`).

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/proposal.md`, `spec.md`, `design.md`
- When `API/SDK=是`, also written to `codespec/changes/<repo-name>/<proposal-id>/arkts-api-spec.yaml and/or c-api-spec.yaml`
- Report any fields that still need human approval
