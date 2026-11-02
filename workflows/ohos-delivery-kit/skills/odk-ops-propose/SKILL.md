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

## Confirm the build product before invoking the bridge

First apply the host-only exception in the delivery-level and product guides.
Only target-build/device plans require the menu and firmware selection below.

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
   - execution-plan: AC-Task traceability table, code scope per task.

Before writing `execution-plan.md`, apply `odk-plan`'s build-product and command resolution step (without replacing the active bridge's task decomposition).
<!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
Read `contracts/skill-guides/delivery/device-version.md` to skip daily selection for QEMU, ask daily versus existing for every other product, and persist the choice and preparation method in `## 构建与验证环境`. Preserve this environment section in every output mode.
<!-- /ODK:reference -->

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/proposal.md`, `spec.md`, `design.md`, `execution-plan.md`.
- Report any fields needing human approval.
