# ohos-delivery-kit (ODK) Workflow Plugin

Neutral-source plugin providing OpenHarmony delivery artifact specification skills,
session routing, validator executable, and runtime assets.

## 0.9.0 archive path change

**Breaking change:** formal delivery artifacts now use two repository-scoped levels:
`codespec/changes/<repo-name>/<req-id>/`. The repository name is resolved from the
Git `origin` URL (without `.git`), falling back to the worktree root directory name.
The formal directory leaf is exactly `req-id` and no longer retains the English slug.

Before a requirement ID is available, keep the English description in
`codespec/changes/<repo-name>/draft-<yyyymmdd>-<english-slug>/`. After obtaining the
ID, run `odk-link-req` to rename it to `<repo-name>/<req-id>/` and update `proposal.md`.

Repositories upgrading from ODK 0.8.x must migrate the former flat
`codespec/changes/<req-id>-<english-slug>/` directories and their references. Follow
the executable [0.9.0 migration guide](MIGRATION-0.9.0.md). The installed
`runtime/executables/validate-archive-migration.py` provides local `plan` and
`check-staged` gates and now detects both 0.8 flat archives and older issue archives.

## 0.8.0 historical migration

**Breaking change:** the former hidden archive root and issue-number directory naming
are no longer supported. Formal delivery artifacts now use
`codespec/changes/<req-id>-<english-slug>/`. Before a requirement ID is available,
keep the draft at `codespec/changes/draft-<yyyymmdd>-<english-slug>/`; after obtaining
the ID, run `odk-link-req` to rename the directory and update `proposal.md`.

`req-id` may contain letters, digits, and internal hyphens. Existing repositories
must follow the executable [0.8.0 migration guide](MIGRATION-0.8.0.md) before running
strict validation. `odk-link-req` only links new drafts; it is not a legacy archive migrator.
The 0.8.0 rules above are historical; 0.9.0 repositories must use the new
repository-scoped layout.

## Source

Synced from `oshunter/ohos-delivery-kit` branch `dev` via
`ohos-marketplace/scripts/publish-plugins.sh --target openharmony-skills`.

## Structure

- `plugin.yaml` — neutral manifest (hand-maintained)
- `provenance.yaml` — source tracking (auto-updated by publish script)
- `hooks/session-router.yaml` — declarative session-start hook
- `prompts/session-router.md` — router prompt
- `skills/` — 24 ODK skills (synced from `core/skills/`)
- `runtime/assets/` — templates, profiles, contracts, rules, adapters, examples
- `runtime/executables/` — artifact and archive-migration validators

## Variables

- `{{ASSET_ROOT}}` — resolved to `runtime/assets` at build time
- `{{EXECUTABLE_ROOT}}` — resolved to `runtime/executables` at build time
- `{{CMD_PREFIX}}` — resolved per-host (`/odk-` for claude, `odk-` for codex/opencode)
