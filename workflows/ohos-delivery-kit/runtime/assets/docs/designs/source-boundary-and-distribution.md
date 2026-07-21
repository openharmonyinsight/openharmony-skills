# Source Boundary and Distribution Plan

> Status: Proposed for `dev`

## Goal

Reduce maintenance cost without weakening the final OpenHarmony delivery contract.

ODK has three different kinds of content:

| Layer | Owns | Must not own |
|-------|------|--------------|
| Templates | Artifact sections, required tables, OpenHarmony quality fields, traceability placeholders | Platform install details, plugin fallback behavior |
| Skills / commands | Activation, phase routing, context loading, plugin delegation, fallback, output redirection | Long section definitions, table schemas, archive contract truth |
| Platform packages | Manifest, hook wiring, platform-specific command rendering | Independent copies of contract, templates, profiles |

## Source of Truth

The intended source order is:

1. `core/contracts/artifacts.yaml` defines required archive artifacts, section ownership, dependencies, and evidence policy.
2. `core/templates/` renders the artifact skeletons declared by the contract.
3. `core/profiles/` extends the contract and templates additively for OpenHarmony subsystems.
4. `core/adapters/` declares plugin-to-ODK mappings and fallback commands.
5. `core/skills/` implements routing, bridge behavior, and agent instructions against those sources.
6. `packaging/*` stores platform-specific static packaging inputs.
7. `dist/*` contains generated installable artifacts and is rebuilt from `core/` + `packaging/`.

This keeps final delivery quality anchored in contract + templates + validator, not in long duplicated prompt text.

Template injection details are documented in `docs/template-injection.md`. This document defines ownership boundaries and distribution shape; `template-injection.md` defines when those sources are loaded into agent/plugin workflows.

## Platform Distribution

Claude, Codex, and OpenCode need different package shapes:

| Platform | Needs | Generated from |
|----------|-------|----------------|
| Claude | `dist/claude` plugin package with `.claude-plugin/plugin.json`, hooks, skill frontmatter, `${CLAUDE_PLUGIN_ROOT}` paths | `packaging/claude` static inputs + `core/skills`, `core/templates`, `core/profiles`, `core/contracts`, `core/adapters` |
| Codex | `dist/codex` plugin/manual install package with `.codex-plugin/plugin.json`, hooks, skill frontmatter, `${CODEX_PLUGIN_ROOT}` paths | `packaging/codex` static inputs + `core/skills`, `core/templates`, `core/profiles`, `core/contracts`, `core/adapters` |
| OpenCode | `dist/opencode` JS-plugin copy source: `.opencode/plugins/ohos-delivery-kit.js` + `.opencode/ohos-delivery-kit/` (skills + shared resources) + `.opencode/commands/odk-*.md` | `packaging/opencode` (package.json + plugins/ohos-delivery-kit.js) + `core/skills`, `core/templates`, `core/profiles`, `core/contracts`, `core/adapters` |

`packaging/*` is no longer the generated distribution target. Installable artifacts are generated under `dist/*`, and tracked generated copies have been removed from platform packaging directories. Reviewers should inspect `core/*`, static `packaging/*` inputs, and scripts; `dist/*` is ignored and reproducible.

OpenCode now uses a native JS plugin (Route A; see `plugin-publishing-mechanism.md`), symmetric with Claude/Codex in bootstrap behavior:

- `.opencode/plugins/ohos-delivery-kit.js` is auto-loaded; its `config` hook registers skills for the native skill tool, and `experimental.chat.messages.transform` injects the `using-odk` bootstrap (equivalent to Claude/Codex SessionStart).
- `dist/opencode` is a `.opencode/`-root layout copied into the target project (bare `.js` auto-load, no `plugin[]` needed).
- Shared resources (templates/profiles/contracts/adapters) ARE materialized under `.opencode/ohos-delivery-kit/` (self-contained, like Claude/Codex); `install-opencode.sh` substitutes `__ODK_PLUGIN_ROOT__` → absolute asset root at install time (not `ODK_ROOT` repo read-back).
- The final `.codespec/changes/<id>/` artifact contract is identical across all three platforms.

## Quality Guardrails

Simplification must not remove:

- `target_release` ownership in `proposal.md`
- 8-dimension N/A confirmation
- WHEN/THEN ACs with stable IDs
- compatibility, error-code, verification, and code-mapping tables
- AC-to-Task traceability
- file-scope and actual-result tracking in `execution-plan.md`
- review and validation evidence hooks

Allowed simplifications:

- Shorten skill text that repeats template sections
- Generate platform copies from `core`
- Move adapter mapping from prose docs into `core/adapters/*.yaml`
- Move artifact section truth from prose docs into `core/contracts/artifacts.yaml`

## Rollout Order

1. Add contract and adapter declarations.
2. Add drift checks for contract, templates, adapters, and materialized packages.
3. Update docs to point to the new truth sources.
4. Convert generated packaging to an explicit `dist/*` build artifact.
5. Remove tracked generated leftovers from `packaging/*` once installers are proven on all platforms. Completed in the second dist-only migration step.
