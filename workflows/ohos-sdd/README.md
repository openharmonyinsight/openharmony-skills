# ohos-sdd Workflow Plugin

OpenHarmony SDD workflow plugin providing skills, profiles, and runtime assets.

## Source

Synced from `oshunter/ohos-sdd` main branch via
`ohos-marketplace/scripts/publish-plugins.sh --target openharmony-skills`.

## Structure

- `plugin.yaml` — neutral manifest (hand-maintained)
- `provenance.yaml` — source tracking (auto-updated by publish script)
- `hooks/session-router.yaml` — declarative session-start hook
- `prompts/session-router.md` — router prompt
- `skills/` — 10 ohos-sdd skills (synced from `skills/`)
- `runtime/assets/` — templates, profiles, contracts, workflow, analysis, cli, rules

## Variables

- `{{ASSET_ROOT}}` — resolved to `runtime/assets` at build time
- `{{CMD_PREFIX}}` — resolved per-host (`/ohos-sdd-` for claude, `ohos-sdd-` for codex/opencode)

## Differences from ODK Plugin

- No validator executable (CLI executable registered instead)
- Additional assets: workflow/, analysis/, cli/, rules/
- security-playbook.md included in analysis/ (referenced by design.md template for security checks)
- Skills use `{{ASSET_ROOT}}` placeholder (synced from source `{{PLUGIN_ROOT}}`)
