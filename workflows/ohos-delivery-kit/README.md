# ohos-delivery-kit (ODK) Workflow Plugin

Neutral-source plugin providing OpenHarmony delivery artifact specification skills,
session routing, validator executables, and runtime assets.

## 0.14.0 configurable execution and device-version planning

Build/test commands, review hooks, PR tools and CI/online-test triggers can be
configured through `runtime/assets/odk_config.yaml` and an optional sibling
`odk_config_ext.yaml`. Planning records the resolved commands and device-version
strategy: QEMU (`arm64_virt`) needs no daily firmware; every other product asks
whether to obtain daily or use existing firmware. Implementation reuses the
recorded choice; manual preparation remains available when automatic flashing
is unsupported. Automatic flashing requires rk3568 and a configured skill.

Resource self-checks resolve files from the loaded guide location and do not
require resource-root variable injection. Brainstorm recovery uses the installed
skill name on every host. Goal-to-US coverage checks accompany document validation.
CI/online-test triggers do not by themselves attest that remote tests have passed.

## 0.13.0 structured clarification

Adds the standalone `odk-brainstorm` interview and active clarification in
propose/spec/design. This release ships 27 ODK skills, including the FMEA engine
and its complete `references/` library. Installers must copy skill auxiliary
files and relocate literal runtime paths before this release is distributed.

## 0.12.1 FMEA analysis and AC traceability

Adds `odk-fmea` with an 18-class fault-mode library and a DFX disposition gate.
Every knowledge-base hit and AD entry must have a disposition; linked ACs must
exist in spec.md and all their traceability rows must be Pass before archive.
The proposal ID and delivery handoff contracts from 0.12.0 remain in force.

## 0.12.0 proposal ID / delivery handoff

**Migration required:** proposal frontmatter and metadata now use `proposal_id`;
the binding command is `odk-link-proposal`. Existing numeric IDs are unchanged.
Old identity fields and command aliases are not retained. Follow
[the 0.12.0 migration guide](MIGRATION-0.12.0.md) before using the new validator.

Implementation now runs review and archive validation automatically, then stops
with a reminder to submit the source PR. Only the user's source-PR instruction
starts commit/push/PR creation and prepares local metadata from the verified PR.
A separate confirmation starts the design-docs PR workflow; neither step merges.
For non-GitCode origins, supply the design-docs address for this submission, even
if a profile already has an address. PR creation/query failure must not be hidden
by an empty metadata list. Non-GitCode PR/MR records use their actual URL plus
an explicit HTTPS `repository_url`; host, port and namespace/path must match.
Legacy GitCode repository URLs remain optional. Issue tracking remains GitCode-only.

**Breaking change:** a formal `proposal-id` must contain digits only, with no length
restriction. The formal archive location remains
`codespec/changes/<repo-name>/<proposal-id>/`; its directory name, `proposal.md` frontmatter
`proposal_id`, and `metadata_tracking.yaml` `proposal_id` must agree. Drafts continue to use an
English slug and cannot be submitted as formal design documents.

`odk-submit-design-docs` now creates or refreshes `metadata_tracking.yaml` before a
design-docs submission. Its strict `--design-docs-submit` gate requires all five files
in the formal archive: `proposal.md`, `spec.md`, `design.md`,
`execution-plan.md`, and `metadata_tracking.yaml`. A repository entry may use an empty
`pull_requests: []` list when no pull request exists yet.

For `API/SDK=是`, the submission also includes
`evidence/task1-api-declaration-en.diff` and `evidence/task1-api-declaration-zh.diff`
at their original relative paths. These must be nonempty unified diffs with complete
hunks and actual added/deleted lines. Missing or invalid evidence warns in draft mode
and fails archive/submission mode; blank files are not a no-change exemption.
The structural check does not prove applicability, bilingual equivalence, or compiler
correctness. Preserve other evidence referenced by the documents when submitting.

The submission gate applies the same final-readiness checks as archive mode. When
`proposal.md` marks `API/SDK` as involved, the validator also requires a complete
per-API specification with shared attributes, owner-qualified signatures, API
description elements, and supported-device behavior tables.
HTML-commented and fenced specifications do not satisfy the gate. API decisions must be
unique and final; shared attributes reject malformed values. Signature validation handles
C/ArkTS generics, escaped table pipes, malformed types, and semantic duplicates.

The `issues` field is an optional extension. ODK omits it by default, preserves valid
existing issue entries, and adds entries only when the developer explicitly requests
issue tracking. Populated PR and issue entries require complete tracking fields; issue IDs
must match their GitCode URLs, and `closed_at` is valid only for closed issues. Repositories
with previous non-numeric formal IDs must use the bundled
`validate-archive-migration.py` `plan` and `check-staged` gates before adopting 0.12.0.

See [CHANGELOG.md](CHANGELOG.md) for the released change summary.

## 0.10.0 proposal contract change

**Breaking change:** archived `proposal.md` documents now require 13 sections. The two
new required sections are `1+8 Device Variation Specification` and `External
Dependencies`. Each device row must explicitly state whether a difference exists and
explain it. The dependency table must either list complete dependencies or contain one
explicit not-applicable row; it cannot contain both.

The archive validator enforces these requirements for native ODK artifacts and for
strict/merge output produced through OpenSpec, MatrixSpec, or Superpowers bridges.
Existing proposals must follow the [0.10.0 migration guide](MIGRATION-0.10.0.md)
before archival.

When code development is complete and a GitCode commit, push, or PR is about to be
created, ODK reminds the developer to submit `codespec/` documents separately to the
design-docs repository configured by the developer as `design_docs_repository` in
`codespec/profile.yaml`. If the address is missing and the business repository's
`origin` host is exactly `gitcode.com`, ODK offers
`https://gitcode.com/OpenHarmonyAI/design-docs` for explicit confirmation. For other
origins it asks the developer for an address. No response is not consent: ODK must
confirm the target before submission and verify every effective push URL against
that endpoint. Confirmation alone does not persist a profile change.

## 0.9.0 archive path change

**Breaking change:** formal delivery artifacts now use two repository-scoped levels:
`codespec/changes/<repo-name>/<proposal-id>/`. The repository name is resolved from the
Git `origin` URL (without `.git`), falling back to the worktree root directory name.
The formal directory leaf is exactly `proposal-id` and no longer retains the English slug.

Before a proposal ID is available, keep the English description in
`codespec/changes/<repo-name>/draft-<yyyymmdd>-<english-slug>/`. After obtaining the
ID, run `odk-link-proposal` to rename it to `<repo-name>/<proposal-id>/` and update `proposal.md`.

Repositories upgrading from ODK 0.8.x must migrate the former flat
`codespec/changes/<proposal-id>-<english-slug>/` directories and their references. Follow
the executable [0.9.0 migration guide](MIGRATION-0.9.0.md). The installed
`runtime/executables/validate-archive-migration.py` provides local `plan` and
`check-staged` gates and now detects both 0.8 flat archives and older issue archives.

## 0.8.0 historical migration

**Breaking change:** the former hidden archive root and issue-number directory naming
are no longer supported. Formal delivery artifacts now use
`codespec/changes/<proposal-id>-<english-slug>/`. Before a proposal ID is available,
keep the draft at `codespec/changes/draft-<yyyymmdd>-<english-slug>/`; after obtaining
the ID, run `odk-link-proposal` to rename the directory and update `proposal.md`.

`proposal-id` may contain letters, digits, and internal hyphens. The
[0.8.0 migration guide](MIGRATION-0.8.0.md) is frozen historical documentation
and must only be used with pinned 0.8.0 tools; current users must follow the
[0.9.0 migration guide](MIGRATION-0.9.0.md). `odk-link-proposal` only links new drafts;
it is not a legacy archive migrator.
The 0.8.0 rules above are historical; 0.9.0 repositories must use the new
repository-scoped layout.

## Source

Synced from `oshunter/ohos-delivery-kit` branch `main` via
`ohos-marketplace/scripts/publish-plugins.sh --target openharmony-skills --plugin ohos-delivery-kit`.
Current source: `main@fec9666a20195dd22df920c3eb3997b89af1e16f`.
The current publisher needs the default config, archive-migration entrypoint and
all Python runtime libraries supplemented; the source release gate verifies the
final package against this pinned revision.

## Structure

- `plugin.yaml` — neutral manifest (hand-maintained)
- `provenance.yaml` — source tracking (auto-updated by publish script)
- `hooks/session-router.yaml` — declarative session-start hook
- `prompts/session-router.md` — router prompt
- `skills/` — 27 ODK skills (synced from `core/skills/`)
- `runtime/assets/` — templates, profiles, contracts (including skill-guides), rules, adapters
- `runtime/executables/` — artifact and archive-migration validators

## Shared runtime assets

These are passive files read on demand, not generated business-repository artifacts.
Templates define document structure; contracts define validation and workflow rules;
profiles add subsystem-specific guidance; rules and adapters provide shared policies
and bridge mappings. Skills and validators share these files to avoid divergent copies.

Skill instructions use literal asset-relative paths such as `templates/ai/design.md`
and `contracts/artifacts.yaml`, or workflow-relative `runtime/assets/...` and
`runtime/executables/...`. Installers relocate these references to the installed
`assets/` and `executables/` directories. No resource-root placeholders are needed.
When reading this source tree, asset-relative paths start at `runtime/assets/`.
The business repository working directory is not the plugin root. Paths within
a loaded guide remain relative to that guide. The `template` values in
`contracts/artifacts.yaml` stay asset-relative `templates/...` paths consumed
separately by the validator. Skill-local files such as `odk-fmea/references/`
must be installed alongside the rendered `SKILL.md`, preserving relative links.

To check real V1 and V2 installation artifacts without registering plugins in
your agents, provide a local installer source or unpacked npm package.
Installation was verified with the official npm package oh-skillhub 0.1.43:
all 40 workflow regression tests pass, including V1 and V2 installation for
Claude Code, Codex and OpenCode. Skill-local auxiliary files, including all 44
FMEA reference files, are copied alongside SKILL.md; the default configuration
and shared runtime references also resolve correctly. Use 0.1.43 or a later
version that passes this check. Version 0.1.42 omits skill-local auxiliary files
in workflow-plugin projections; 0.1.40 also lacks literal-path relocation.
Reproduce the installation check with:

```bash
OH_SKILLHUB_PACKAGE_ROOT=/path/to/oh-skillhub \
  python3 -m unittest discover -s workflows/ohos-delivery-kit/tests -v
```

The installation check verifies runtime references, runs the rendered validator
from outside the source tree, and compares every skill auxiliary file byte for byte.
It uses temporary directories and performs no network access or host registration.

## Variables

- `ASSET_ROOT` — source asset root declared as `runtime/assets`
- `EXECUTABLE_ROOT` — source executable root declared as `runtime/executables`
- `{{CMD_PREFIX}}` — resolved per-host (`/odk-` for claude, `odk-` for codex/opencode)

## Build product selection

Set a space-separated candidate list and its preferred default in the override configuration:

```yaml
build_products: arm64_virt rk3568 my_board
build_product: rk3568
```

Planning presents the configured choices and waits for one confirmed product.
The plan records the list and selection for implementation to reuse. QEMU skips
firmware selection; other products ask daily versus existing firmware.

**Upgrade limitation:** oh-skillhub 0.1.43 does not preserve user-added
`odk_config_ext.yaml` inside the installed assets directory when rebuilding the
plugin during an update. Back up this file before updating and restore it after
installation. The bundled configuration's promise of automatic preservation is
not supported by this installer; persistent configuration remains a known issue.
