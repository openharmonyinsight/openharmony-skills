# ODK OPS Propose

Use when OpenSpec is installed AND the user wants /opsx:propose to generate all 4 artifacts (proposal+spec+design+execution-plan) in one pass, split into ODK format. Falls back to base commands if unavailable.

## Purpose

One-stop command: invoke OpenSpec `/opsx:propose` to generate proposal + delta specs + design + tasks, then redirect output to `.codespec/changes/<id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `.codespec/changes/<id>/` skeleton must exist (run `{{CMD_PREFIX}}init` first).
- If OpenSpec is unavailable, use the fallback chain declared in `adapters/openspec.yaml` and clearly report the degradation.

## Steps

1. Invoke OpenSpec `/opsx:propose` which produces proposal + delta specs + design + tasks in one call.
2. When OpenSpec tries to write to `openspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per the active output mode (strict/passthrough/merge, default strict):
   - **strict**: Transform each artifact to conform to ODK templates at `{{PLUGIN_ROOT}}/templates/ai/`.
   - **passthrough**: Copy original format to `.codespec/changes/<id>/` unchanged.
   - **merge**: Use OpenSpec format as base, append ODK-required sections.
4. In strict mode, ensure ODK-required fields are present:
   - proposal: target_release, non-goals, 8-dimension N/A table, success criteria.
   - design: module impact table, verification approach table; inherit `odk-design` security trigger (proposal 安全/权限=是 → expand 安全基础检查, high-risk → `threat-model.md`).
   - spec: AC numbering (AC-X.Y format), compatibility declaration, verification mapping.
   - execution-plan: AC-Task traceability table, code scope per task.

## Output

- Written to `.codespec/changes/<id>/proposal.md`, `spec.md`, `design.md`, `execution-plan.md`.
- Report any fields needing human approval.
