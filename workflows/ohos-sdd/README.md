# ohos-sdd Workflow Plugin

Neutral-source plugin providing OpenHarmony SDD workflow skills, profiles, and runtime assets.

## Source

Synced from `oshunter/spec-for-ai` dev branch via
`ohos-marketplace/scripts/publish-plugins.sh --target openharmony-skills`.

## Structure

- `plugin.yaml` — neutral manifest (hand-maintained)
- `provenance.yaml` — source tracking (auto-updated by publish script)
- `hooks/session-router.yaml` — declarative session-start hook
- `prompts/session-router.md` — router prompt
- `skills/` — 10 ohos-sdd skills (synced from `openharmony/skills/`)
- `runtime/assets/` — templates, profiles, contracts, workflow, analysis, cli, security-guide, examples

## Variables

- `{{ASSET_ROOT}}` — resolved to `runtime/assets` at build time
- `{{CMD_PREFIX}}` — resolved per-host (`/ohos-sdd-` for claude, `ohos-sdd-` for codex/opencode)

## Differences from ODK Plugin

- No validator executable (CLI executable registered instead)
- Additional assets: workflow/, analysis/, cli/
- security-guide.md included (referenced by skills for security checks)
- Skills use `{{ASSET_ROOT}}` placeholder (synced from source `{{PLUGIN_ROOT}}`)
