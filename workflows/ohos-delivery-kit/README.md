# ohos-delivery-kit (ODK) Workflow Plugin

Neutral-source plugin providing OpenHarmony delivery artifact specification skills,
session routing, validator executable, and runtime assets.

## 0.8.0 archive migration

**Breaking change:** the former hidden archive root and issue-number directory naming
are no longer supported. Formal delivery artifacts now use
`codespec/changes/<req-id>-<english-slug>/`. Before a requirement ID is available,
keep the draft at `codespec/changes/draft-<yyyymmdd>-<english-slug>/`; after obtaining
the ID, run `odk-link-req` to rename the directory and update `proposal.md`.

`req-id` may contain letters, digits, and internal hyphens. Existing repositories
must migrate old archive directories and references before running strict validation.

## Source

Synced from `oshunter/ohos-delivery-kit` branch
`release/req-archive-dev-integration` via
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
