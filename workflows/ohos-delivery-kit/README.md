# ohos-delivery-kit (ODK) Workflow Plugin

Neutral-source plugin providing OpenHarmony delivery artifact specification skills,
session routing, validator executable, and runtime assets.

## Source

Synced from `oshunter/ohos-delivery-kit` dev branch via
`ohos-marketplace/scripts/publish-plugins.sh --target openharmony-skills`.

## Structure

- `plugin.yaml` — neutral manifest (hand-maintained)
- `provenance.yaml` — source tracking (auto-updated by publish script)
- `hooks/session-router.yaml` — declarative session-start hook
- `prompts/session-router.md` — router prompt
- `skills/` — 24 ODK skills (synced from `core/skills/`)
- `runtime/assets/` — templates, profiles, contracts, rules, adapters, examples
- `runtime/executables/` — validator script

## Variables

- `{{ASSET_ROOT}}` — resolved to `runtime/assets` at build time
- `{{EXECUTABLE_ROOT}}` — resolved to `runtime/executables` at build time
- `{{CMD_PREFIX}}` — resolved per-host (`/odk-` for claude, `odk-` for codex/opencode)
