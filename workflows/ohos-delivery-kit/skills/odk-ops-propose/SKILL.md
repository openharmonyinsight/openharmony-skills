---
name: odk-ops-propose
description: "Use when OpenSpec is installed AND the user wants /opsx:propose to generate all 4 artifacts (proposal+spec+design+execution-plan) in one pass, split into ODK format. Falls back to base commands if unavailable."
license: MIT
---

# ODK OPS Propose

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

## Native OpenSpec state

<!-- ODK:reference contracts/skill-guides/router/openspec-state.md -->
Read `contracts/skill-guides/router/openspec-state.md` before invoking OpenSpec.
Keep the native workspace and task file authoritative; capture native CLI state
and reconcile existing ODK artifacts without replacing either side.
<!-- /ODK:reference -->

## Purpose

One-stop command: invoke OpenSpec `/opsx:propose` to generate proposal + delta specs + design + tasks, then reconcile the delivery projection under `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `codespec/changes/<repo-name>/<proposal-id>/` skeleton must exist (run `{{CMD_PREFIX}}init` first).
- If OpenSpec is unavailable, use the fallback chain declared in `adapters/openspec.yaml` and clearly report the degradation.
- If proposal output marks `API/SDK` = 「是」, OpenSpec's Markdown/delta spec cannot replace the applicable API metadata files. The one-stop command must stop or use the declared `odk-spec` fallback when it cannot produce valid API metadata.

## Confirm the build product before invoking the bridge

First apply the host-only exception in the delivery-level and product guides.
Target builds require the build-name menu. Runtime target confirmation and firmware preparation are conditional on the explicit validation scope; build-only requires neither.

Run `python3 runtime/executables/lib/odk_repository.py --build-product-options`
(source checkout: `python3 scripts/lib/odk_repository.py --build-product-options`).
<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md`, show the configured
menu and wait for an explicit product choice before invoking opsx:propose,
because it also generates the execution plan. Reuse a real choice already made
for this plan; a configured default or general autonomous/recommended-options
authorization does not confirm a product.
<!-- /ODK:reference -->

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/change-impact.md -->
Before generating native code tasks, read `contracts/skill-guides/delivery/change-impact.md`
and include its usable-capability, affected-path and cross-Task checks. Preserve
evidence through the native task/ODK plan or existing evidence route in every mode;
unavailable LSP/AST uses the documented fallback without changing native ownership.
<!-- /ODK:reference -->

1. Invoke OpenSpec `/opsx:propose` which produces proposal + delta specs + design + tasks in one call.
2. Preserve OpenSpec’s native CLI-returned output paths. Capture native status and source artifacts using `runtime/executables/lib/odk_openspec.py`, then read and revise existing ODK targets per the native-state guide. Never redirect `openspec/changes/`.
3. Process output per the active output mode (strict/passthrough/merge, default strict):
   - **strict**: Transform each artifact to conform to ODK templates at `templates/ai/`.
   - **passthrough**: Reconcile source content in original format within `codespec/changes/<repo-name>/<proposal-id>/` unchanged.
   - **merge**: Use OpenSpec format as base, append ODK-required sections.
4. In strict mode, ensure ODK-required fields are present:
   - proposal: target_release, non-goals, `1+8 设备差异规格`, `外部依赖`, 8-dimension N/A table, success criteria.
   - design: module impact table, verification approach table; inherit `odk-design` DFX design and security steps:
     - DFX 设计（必填，Step 6）：执行 4 步故障模式分析流程（识别涉及仓库 → 委托内置 `odk-fmea` skill 执行故障模式分析 → 按落盘契约回填故障模式分析表 → 处置决策与 AC 回填），详见 `odk-design/SKILL.md` Step 6；降级路径契约见 `contracts/dfx-fmea-matcher.yaml`。
     - Security baseline check (conditional, Step 7): when `proposal.md`「安全/权限」=「是」, expand `design.md`「安全基础检查」; if high-risk criteria are hit, produce `threat-model.md` (see `odk-security-threat-model`).
   - spec: AC numbering (AC-X.Y format), compatibility declaration, verification mapping.
   - api metadata: when `API/SDK=是`, run the `odk-spec` API workflow — language-specific template, isolated documentation subagent, validated the applicable API metadata files, and summary-only `spec.md` API overview.
   - execution-plan: AC-Task traceability table, code scope per task; when `API/SDK=是`, Task-1 generates declarations from the applicable API metadata files.

Before writing `execution-plan.md`, apply `odk-plan`'s build-product and command resolution step (without replacing the active bridge's task decomposition).
<!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
Read `contracts/skill-guides/delivery/device-version.md` after following build-products: preserve the concrete or abstract build name; record `验证范围` (build-only/emulator/device), separately confirmed `验证产品` and `验证目标确认`. Only device validation asks daily/existing. Resolve commands with `--resolve-product-commands` using the separate name contexts. Preserve these fields and confirmations in every output mode; do not infer runtime targets from build names.
<!-- /ODK:reference -->

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/proposal.md`, `spec.md`, `design.md`, `execution-plan.md`.
- When `API/SDK=是`, also written to `codespec/changes/<repo-name>/<proposal-id>/arkts-api-spec.yaml and/or c-api-spec.yaml`.
- Report any fields needing human approval.
