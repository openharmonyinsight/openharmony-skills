# Changelog

All notable changes to the published `ohos-delivery-kit` workflow are documented in
this file. Source artifacts are synchronized from
`oshunter/ohos-delivery-kit` `main` through the marketplace publisher.

## [0.14.0] - 2026-10-27

Source: `main@ca98f5494b5ec4075d539bc09340261d856441d6`.

### Added

- Configurable build/test commands, review hooks, source/design-docs PR tools,
  CI and online-test triggers, and physical-device preparation settings.
- Goal-to-user-story coverage validation and code-grounded brainstorming before
  proposal, specification and design generation.

### Changed

- Confirm device firmware strategy while writing the execution plan: QEMU skips
  daily selection; other products ask daily versus existing firmware and persist
  the preparation method. Implementation and final verification reuse the choice.
- Preserve the daily choice when automatic flashing is unavailable by confirming
  a supported manual preparation method. Bridge planning paths follow the same rule.

### Fixed

- Resolve resource self-checks relative to the actual guide location in source,
  native and neutral layouts, without restoring resource-root placeholders.
- Require rk3568 and a configured flashing skill before automatic flashing;
  confirm the target device and avoid repeated firmware preparation.
- Resume brainstorm using its installed skill name rather than a Claude command.
- Ship the default configuration, archive migration validator and all Python
  runtime libraries; align release metadata with the merged source revision.
- Declare the complete asset tree so installation includes the default config,
  retaining named asset components for literal-path relocation. Remove stale
  skill-local symlinks pointing to a maintainer's machine; keep FMEA references
  as real files alongside the skill.

### Installation limitation

- oh-skillhub 0.1.42 resolves the shared runtime paths, but its workflow-plugin
  projection does not copy FMEA skill-local references. The full installation
  regression remains failing until the installer supports this path; source
  publication and three-host resource projection checks pass.

## [0.13.0] - 2026-10-21

Source: `main@c85abe290808fac290a2bce596b53ca9d4751887`.

### Added

- Register `odk-brainstorm`, bringing the release to 27 skills. Add structured
  clarification before proposal, specification and design generation.
- Add an opt-in real-installation check for Claude Code, Codex and OpenCode:
  verify relocated paths, execute the validator outside the source tree, and
  compare all skill auxiliary files with the shipped source.

### Fixed

- Normalize DFX subsection headings with the shared ATX parser, preventing
  indentation or closing hashes from hiding undispositioned AD entries.
- Align published reference tests with literal resource paths; retain ordinary
  path instructions without restoring resource-root placeholders.
- Document the installer requirement to preserve skill auxiliary directories,
  including the complete FMEA reference library, and relocate runtime paths.

## [0.12.1] - 2026-10-15

Source: `main@9f14e1b65c40aad1f32f2a233865a84aaa6aa34e`.

### Added

- New `odk-fmea` skill: AIAG-VDA 7-step FMEA engine with repository-level
  `docs/dfx/fmea.yaml` knowledge base discovery, 18-class generic fault-mode
  library with two-stage loading (trigger index → detail on match), DFX table
  compatible backfill, and library export table (66-column template).
- DFX fault-mode → AC gate (validator Level C3): every main-table hit and AD
  derived entry must be dispositioned in `### DFX 故障模式处置` table
  (新增 AC / 复用 AC / 纳入设计约束 / 现有控制覆盖 / 本变更不触及);
  dangling AC references fail in Draft; archive requires linked ACs traced Pass.
- `odk-design` Step 6 now delegates to `odk-fmea` in subagent (isolated context);
  new Step 6.4 adds disposition decision and spec.md US-DFX backfill.
- `odk-spec` preserves US-DFX backfill content on regeneration.
- `odk-plan` Self-Review adds FM coverage check; FM ACs cannot be deferred.
- `odk-implement` requires fault-injection/error-path verification for FM ACs.
- `odk-review` adds DFX fault-mode coverage check.
- `odk-validate` documents Level C3 gate.
- Published regression tests cover DFX dispositions, linked AC archive status,
  skill registration, and shared asset paths.

### Changed

- `distribute-skills.sh` now copies skill auxiliary files (references/) via
  `copy_skill_assets`; description length measured in bytes (not characters)
  to match truncation threshold under UTF-8 locales.
- `validate-doc-drift.sh` excludes history sections from skill count checks.
- `validate-skill-descriptions.sh` forces LC_ALL=C for byte-accurate length.
- `validate-skill-references.py` checks skill asset files exist byte-identical
  in all four platform copies; validates relative Markdown links in skill trees.
- AD-level derived entries require library-basis annotation.
- Export table enforces 66-column structure (WARN on drift, not FAIL).

### Fixed

- Refresh the import from merged `main@9f14e1b`; retain the existing
  shared runtime/assets layout and declared host asset/executable variables.
- Use `proposal_id` / `PROPOSAL_ID` and `odk-link-proposal` consistently; legacy
  identity names remain only in migration instructions and rejection checks.
- Preserve the 0.12.0 proposal ID, API validation, and delivery handoff contracts.
- Register `odk-fmea` alongside `odk-link-proposal` and align the manifest version
  with sourceVersion 0.12.1.
- Resolve shared skill references through the declared `ASSET_ROOT` variable;
  retain asset-relative template paths in artifacts.yaml for the validator.

## [0.12.0] - 2026-09-24

Source: `main@e48ec3f7aa7940fefb7b2fd188dec5a4976122f3`.

### Changed

- Refresh source provenance on 2026-09-29 after source PR #143 removed the
  repository-local placeholder archive. Published runtime content is unchanged.

- Normalize Markdown API headings consistently in Draft and Archive: accept
  0–3 spaces of indentation and strip closing hashes before presence, template
  marker and duplicate checks, preserving literal signature content.

- Keep API validation within the document contract: signatures are opaque text,
  not parsed as C/ArkTS syntax, types or array-bound expressions. Source review
  and the target toolchain own language correctness; no GCC dependency is added.
- Preserve empty/duplicate/explicit-placeholder checks. Draft and archive share
  the signature marker policy, accepting identifier substrings and quoted text
  while rejecting template markers such as `<完整签名>`.

- **Breaking:** unify archive identity as `proposal_id`, `<proposal-id>` and
  `odk-link-proposal`; preserve numeric IDs and document field migration.
- Automatically review/validate after implementation; wait for an explicit source
  PR instruction, prepare real PR metadata, then separately confirm a design-docs PR.
- Non-GitCode sources require a documentation address supplied for this submission.
- Track non-GitCode PR/MR URLs using `repository_url`, preserving legacy GitCode
  records and distinguishing identical paths on different hosts.

### Fixed

- Reject legacy identity fields, including quoted/indented forms and mixed fields.
- Preserve same-path cross-host records and normalize repository names consistently.
- Align skill descriptions and action headings with distribution validation.

## [0.11.0] - 2026-09-04

Source: `main@2e5b440fe9e138cd93ec9305c7f5362acedea12f`.

### Added

- `odk-submit-design-docs` generates `metadata_tracking.yaml` before design-docs
  submission and validates the five base files plus required conditional evidence.
- The metadata template supports `pull_requests: []` before a pull request is created.
- A release-documentation regression check keeps the published README and changelog
  aligned with the shipped workflow contract.
- An executable per-API specification contract validates shared attributes, qualified
  signatures, required specification and description elements, and device behavior.

### Changed

- Confirm the design-docs target before submission. An unconfigured GitCode origin
  offers `https://gitcode.com/OpenHarmonyAI/design-docs`; other origins require a
  developer-supplied address. Existing profile configuration remains authoritative.
- Verify the checkout and every effective push URL against the confirmed endpoint,
  including protocol, port, SSH user, and path semantics. Non-GitCode business
  repositories must not generate unsupported GitCode PR/issue metadata.
- Task 1 API declaration gates require English and Chinese diff evidence.
- Split the artifact validator's Markdown and API-signature helpers into runtime
  libraries while preserving document gates and exit codes. Reports explicitly
  mark target language/toolchain validation as NOT VERIFIED.
- Publish all Python runtime libraries and verify their inventory against the
  pinned source commit, rejecting ignored local modules and incomplete bundles.
- Workflow/profile routing and API specification details load on demand from
  shared `runtime/assets/contracts/skill-guides/`; existing rules and approval
  gates are retained. Profile-consuming phase skills reference the shared guide
  directly, with its relative-path base explicitly defined.
- **Breaking:** formal `req-id` values are digits only. The archive directory,
  `proposal.md` `req`, and `metadata_tracking.yaml` `req_id` must match.
- The formal design-docs submission gate requires `proposal.md`, `spec.md`,
  `design.md`, `execution-plan.md`, and `metadata_tracking.yaml` under
  `codespec/changes/<repo-name>/<req-id>/`.
- `--design-docs-submit` now applies archive-equivalent final-readiness checks,
  including unresolved placeholders, task results, DFX closure, and resource gates.
- `issues` is an optional extension: it is omitted by default and added only when a
  developer explicitly requests issue tracking.

### Fixed

- Recognize indented and closing-hash ATX headings when rejecting duplicate API
  and resource contract sections.
- Accept arithmetic C array bounds while rejecting dangling operators and adjacent
  operands. Keep type validation separate from bound expressions.
- Require nonempty unified-diff API evidence with complete hunks and actual changes;
  include both language variants in the design-docs submission bundle.
- Preserve standalone absolute-path loading of the YAML helper. The source focus
  example now includes explicitly illustrative declaration fixtures and aligned scope.

- C array dimensions reject adjacent operands such as `4 4`, for both named
  and abstract parameters, including multidimensional and nested callbacks.

- C callbacks accept named array parameters, including unsized, multidimensional
  and nested callback declarations, without dropping array dimensions.

- C callback parameter declarations support names, including nested callbacks;
  ArkTS arrow types reject empty parameters recursively while preserving tuple types.

- C function-pointer validation recursively rejects empty parameter entries and
  accepts qualified pointers such as `void (* const)(const char *)`.

- Local archive-migration validation detects legacy non-numeric formal IDs before
  they are submitted with the 0.11.0 contract.
- Per-API validation ignores HTML comments and fenced examples, rejects duplicate or
  unresolved API decisions and malformed shared attributes, validates C/ArkTS generic
  and type syntax, handles escaped table pipes, and canonicalizes semantic signatures.
- Design-docs metadata requires complete populated PR/issue entries, accepts GitCode
  `merge_requests` URLs, rejects unknown fields, correlates issue IDs with URLs, and
  enforces issue state consistency.

### Known limitations

- Signature/bound checks are bounded lexical checks, not target SDK/compiler checks.
  Diff structure validation does not establish applicability, bilingual semantic
  equivalence, or genuine business provenance. Illustrative source examples are not
  production evidence and are not included in this publishing channel.
