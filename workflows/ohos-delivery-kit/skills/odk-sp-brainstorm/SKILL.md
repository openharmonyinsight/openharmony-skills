
# ODK SP Brainstorm

Use when Superpowers is installed AND the user wants one-session proposal+spec+design via Superpowers brainstorming. Output redirected to ODK archive. Falls back to odk-propose+odk-spec+odk-design if unavailable.

## Purpose

Invoke Superpowers `brainstorming` for requirement clarification and approach selection. Redirect output to ODK archive format in `.codespec/changes/<id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `.codespec/changes/<id>/` skeleton must exist (run `{{CMD_PREFIX}}init` first).
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Steps

1. Invoke Superpowers `brainstorming` for requirement clarification and approach selection.
2. Apply `using-odk-bridge` Output Redirection Rules when brainstorming tries to write to `docs/superpowers/specs/`.
3. Process output per active mode: ensure `proposal.md`, `spec.md`, `design.md` conform to ODK templates in strict mode; preserve plugin format in passthrough mode; append ODK sections in merge mode. For `design.md`, rely on `using-odk-bridge` Design State Ownership Rules so complex state changes include explicit ownership and checkable invariants. In strict mode, also inherit `odk-design`'s security trigger: when `proposal.md`「安全/权限」=「是」, expand `design.md`「安全基础检查」; if high-risk criteria are hit, produce `threat-model.md` (see `odk-security-threat-model`).

## Output

- Written to `.codespec/changes/<id>/proposal.md`, `spec.md`, `design.md`
- Report any fields that still need human approval
