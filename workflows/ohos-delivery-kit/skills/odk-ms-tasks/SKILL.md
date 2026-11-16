---
name: odk-ms-tasks
description: "Use when MatrixSpec is installed AND the user wants /matspec.tasks to drive execution-plan.md. Falls back to odk-plan if unavailable."
license: MIT
---

# ODK MS Tasks

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

Invoke MatrixSpec `/matspec.tasks` for task breakdown generation. Redirect output to ODK archive format in `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- Read `design.md` if present; it is required only when the effective contract requires design (standard/critical).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.
- If proposal.md `API/SDK` = 「是」, a structurally valid the applicable API metadata files must exist before task generation. If it is missing, stop and require `{{CMD_PREFIX}}spec` (or the declared fallback); do not generate a plan that starts from implementation.

## Confirm the build product before invoking the bridge

First apply the host-only exception in the delivery-level and product guides.
Target builds require the build-name menu. Runtime target confirmation and firmware preparation are conditional on the explicit validation scope; build-only requires neither.

Run `python3 runtime/executables/lib/odk_repository.py --build-product-options`
(source checkout: `python3 scripts/lib/odk_repository.py --build-product-options`).
<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md`, show the configured
menu and wait for an explicit product choice before invoking matspec.tasks.
Reuse a real choice already made for this plan; a configured default or general
autonomous/recommended-options authorization does not confirm a product.
<!-- /ODK:reference -->

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/change-impact.md -->
For code Tasks, read `contracts/skill-guides/delivery/change-impact.md` and include
its capability check, affected paths and cross-Task checks in planning. Preserve
results through the existing plan/evidence route in every mode; unavailable LSP/AST uses
the documented fallback without requiring another plugin.
<!-- /ODK:reference -->

1. Invoke MatrixSpec `/matspec.tasks` for layered task generation (Data -> Domain -> Application -> Infrastructure -> Interface -> Tests -> Docs -> Verification).
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK execution-plan format at `templates/ai/execution-plan.md`. Add AC-Task traceability table, code scope per task (file-level paths), completion criteria.
   - passthrough: Copy to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` unchanged.
   - merge: Use MatrixSpec layered format, append AC-Task traceability table and code scope column.
4. If proposal.md `API/SDK` = 「是」, apply `odk-plan`'s API rule: insert Task-1 as API declaration generation from the applicable API metadata files, before all implementation tasks. Passthrough output that omits this task is invalid.
5. Confirm with user.

Before writing `execution-plan.md`, apply `odk-plan`'s build-product and command resolution step (without replacing the active bridge's task decomposition).
<!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
Read `contracts/skill-guides/delivery/device-version.md` after following build-products: preserve the concrete or abstract build name; record `验证范围` (build-only/emulator/device), separately confirmed `验证产品` and `验证目标确认`. Only device validation asks daily/existing. Resolve commands with `--resolve-product-commands` using the separate name contexts. Preserve these fields and confirmations in every output mode; do not infer runtime targets from build names.
<!-- /ODK:reference -->

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md`
- Report any fields needing human approval
