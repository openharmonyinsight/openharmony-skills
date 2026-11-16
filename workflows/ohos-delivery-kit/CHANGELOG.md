# Changelog

All notable changes to the published `ohos-delivery-kit` workflow are documented in
this file. Source artifacts are synchronized from
`oshunter/ohos-delivery-kit` `main` through the marketplace publisher.

## [0.15.0] - 2026-11-03

Source: `main@0122bc6cc0ac5a828a1d39eae1c9644a269e853e`.

This republish imports the review fixes merged into the source `main` after the
first 0.15.0 import (`4ff4729`); the version stays 0.15.0 because that release PR
has not been merged yet.

This import publishes the language-specific API metadata contract and its
breaking migration. Existing 0.14 API changes must be moved with
`odk-upgrade-api-chain` or restarted from proposal; the legacy chain is not
accepted as a compatibility layer.

### Added

- Make `arkts-api-spec.yaml` / `c-api-spec.yaml` the API SDD contract source:
  `odk-spec` generates machine-readable API metadata and delegates the
  human-facing three/five elements to an isolated subagent; `spec.md` keeps only
  the API overview; plan and implement consume only the applicable metadata;
  validate checks metadata structure, overview union consistency, declaration
  diffs, documentation closure and exact paths. Legacy `api-spec.yaml`,
  mixed-language declaration diffs and per-API Markdown specifications are no
  longer accepted directly.
- Add `odk-upgrade-api-chain` for 0.14 / `ohos-sdd/v1` chains: dry-run extracts
  facts from the proposal, API repository knowledge and legacy spec, missing or
  conflicting facts require developer confirmation, then the assistant writes
  language metadata atomically and saves a migration report. Mixed-language
  chains run once per language and accumulate the overview.
- Add the proposal coverage matrix to `spec.md`: goals, non-goals, assumptions
  and open questions must map to AC, BR, EB, language-specific API metadata, a
  justified `N/A` or `Open-N`; the `lite` delivery level keeps its lean sections.
- Split API declaration diff evidence by declaration repository and language
  (`task1-arkts-api-declaration-<lang>.diff` and
  `task1-c-api-declaration-<lang>.diff`); only applicable language files are
  generated and the mixed-repository `task1-api-declaration-<lang>.diff` is no
  longer compatible.
- Add declaration-comment description closure: the eight API-level fields that
  are not `N/A`, plus parameter, return and error-code descriptions, must appear
  in the language diff; descriptions are plain text without element labels and
  do not restate `since`, `syscap` or error-code attributes. Comment layout must
  align with the declaration and leave no blank line after `*/`, and API-level
  descriptions must not repeat the same behavior clause as parameter or return
  descriptions.
- Add the `check-api-documentation-context.py` process gate: before merging
  documentation subagent output it verifies API ID closure, bilingual field
  completeness and confirmed-value coverage, so units, ranges and defaults from
  the bounded context are not lost.
- Apply the OpenHarmony Chinese documentation rules to the API documentation
  contract: a single `forbidden-terms.yaml` source and the
  `chineseEnglishSpacing` switch (off by default) are shared by the process gate,
  the example check and the final archive validation; the duplicate
  documentation threshold is configurable with Draft WARN and Archive FAIL, and
  both rule files carry `rulesetVersion` and `sourceOfTruth`.
- Let API repository knowledge indexes declare prerequisites; `odk-spec` loads
  them in declared order and stops when a prerequisite is unavailable.
- Support the optional ArkTS `apiMode`: omitting it means dynamic only, static
  and dynamic-plus-static modes must be declared and cross-checked with the
  proposal, file path and `since` marker; static APIs accept `.d.ets` + `static`
  or `.static.d.ets` + `staticonly`, and static declarations reject `any` and
  union types.

### Fixed

- Preserve C pointer return types and qualifiers; parse inline-formatted legacy
  error codes without removing pointer operators inside code spans.
- Preserve confirmed ArkTS API modes in both legacy formats. Reject explicit
  null, false, empty or otherwise invalid modes before writing; only a missing
  mode field permits 0.14 defaults or inference from the file path.
- Reuse the final validator's mode/path/since/declaration checks before migration
  writes, including generic declarations. Conflicts keep all original files.
- Accept confirmed numeric range endpoints and Chinese-adjacent decimal,
  negative and unit values, while rejecting different signs, precision,
  exponent fragments and Unicode unit continuations.
- Use installer-relocatable runtime paths in API skill commands, and make the
  release gate reject legacy runtime paths wrapped in variables; shared guides
  reuse the path exposed by the loaded skill. The gate also verifies that quoted
  executable paths exist and were relocated, with and without braces.
- Check the full number, sign and precision boundary for Chinese unit and range
  confirmed values, so `10.5ms` or `-0.5ms` is not accepted as `0.5ms`.
- Apply the hardened NAPI/ArkTS and RAII/symbol-export guidance from the
  AI-draft versus release diff to `odk-fmea` and the implementation-quality
  guide.

## [0.14.7] - 2026-11-13

Source: `main@85673017d17fcd84aad724d37b60603d04558f66`.

This republish imports the review and release-gate fixes merged into the source
`main` after the first 0.14.7 import (`0989ab3`); the version stays 0.14.7 because
that release PR has not been merged yet.

This import also publishes changes that the source still listed as Unreleased at
this commit: the `odk-task-review` five-dimension Task review guide wired into the
base, Superpowers and OpenSpec entries, and the delivery-body boundary rule with
its prompt-residue checker (source issue #157).

### Fixed

- Reject corrupt Task review verdicts instead of silently degrading them: top-level
  non-mapping syntax, duplicate fields, and indented content before the first field
  are invalid. Draft warns and archive fails, while comments, blank lines and nested
  metadata under a top-level field stay supported.
- Check the raw command projection list before the installer de-duplicates it, then
  verify the effective command set and the generated OpenCode command wrappers, so
  duplicate declarations or registering only `components.skills` while omitting
  `commandProjection.commands` fail the neutral release gate.
- Use the same concrete or abstract product name for build commands and `out/`
  artifacts, and confirm the device validation target separately through an
  explicit `{validation_product}`. Plans record the validation scope and target,
  and artifacts are located from the recorded directory or the build manifest
  under `out/<build product>`; the old product list and configuration templates
  stay readable, and older plans proceed after adding the target (source PR #158).
- Stop treating "not applicable (emulator/QEMU)" as a launcher or validation
  target, and detect product placeholders in mixed-case variants; the parser and
  plan validator reject unexpanded placeholders.

## [0.14.6] - 2026-11-12

### Added

- Add a Task-level review gate: after each Task's verification and before marking
  it Done, run a five-dimension review (duplicate work, performance, missed
  changes, external interface impact, security and attack surface) according to
  its `R0` / `R1` / `R2` risk level. `R2` uses the fixed arch/scope/security
  seats and writes evidence to `evidence/reviews/task-<n>/`.
- Add the host delegation capability probe `scripts/lib/odk_host_capabilities.py`:
  without delegation support or when the probe fails, run three read-only checks
  serially and write `independent: false` in the verdict instead of passing by
  default.

### Changed

- `execution-plan.md` gains a risk-level column, a Task-detail risk field and the
  mandatory `Gate-Task` gate; `odk-plan` records the initial level and rationale
  during planning.
- `odk-implement` and the `odk-sp-implement` bridge run the same gate before
  Done; an open `Critical` / `High` finding marks the Task `❌ Blocked` and blocks
  later Tasks, and risk escalation updates the plan's risk cell.
- `odk-review` checks every R1/R2 Task verdict before an overall PASS, and
  `odk-validate --archive` fails on missing, non-PASS or still-blocking verdicts
  and fixes nested evidence-directory counting.

### Fixed

- Read risk levels only from the single Task-list section, so earlier risk-summary
  tables cannot shadow the real task table; duplicate sections or duplicate risk
  tables inside a section fail validation.
- Treat an empty or non-`R0`/`R1`/`R2` risk level as a Draft warning and an
  Archive failure instead of silently skipping the review check.
- Treat broken `verdict.md` frontmatter (for example an unclosed `---`) as a Draft
  warning and an Archive failure instead of ignoring the parse error.
- Reject uncommented YAML continuation lines in the five required verdict fields,
  so a real `PASS FAIL` or `0 2` is not truncated to `PASS` or `0` and wrongly
  accepted; comments, blank lines and extra metadata stay supported.
- Accept only one unambiguous `R0` / `R1` / `R2` risk cell (an annotation such as
  `R2（公共接口）` is allowed); ambiguous values such as `R1→R2`, `R0/R2` or `R0.5`
  no longer degrade by prefix or skip review as R0, becoming a Draft warning and
  an Archive failure.
- Treat non-exact Task IDs such as `TASK-1（回调）`, `TASK-1, TASK-2` or an empty
  value as a Draft warning and an Archive failure instead of silently skipping
  the review check.
- Run the Task review gate only when the effective contract includes
  `execution-plan`, so `--phase define/specify/design` no longer fails on future
  plan errors.
- Distinguish the OpenCode 2.x `subagent` dispatch protocol from 1.x `task`
  (required `subagent_type`, background tasks need
  `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true`); the capability probe does
  not claim background support when the version is unknown and degrades serially
  when tools or parameters are unavailable.
- Move teaching-example Tasks that hit callback, lifecycle and public `.d.ts`
  triggers to `R2`, add the arch/scope/security reports and verdicts, and fix the
  construct rows displaced by the new risk column.

## [0.14.5] - 2026-11-06

### Added

- Add a change-impact scope check: probe the LSP, semantic index or AST available
  to the current agent and project, and query references, call relations and other
  implementations according to tool capability; when unavailable, use entry and
  file lists, call-site search, TDD and full diff review to check for missed
  changes.

### Changed

- Wire impact paths, handling and verification limits into planning,
  implementation and review in the base and bridge flows; read-only discovery in
  authorized repositories must update Task context and file scope before it is
  used as a basis for changes.

## [0.14.4] - 2026-11-06

### Added

- Add a shared Chinese writing guide, 19 positive and negative example pairs and a
  pre-output self-check that require applicable conditions, actions and results,
  while preserving technical identifiers, values, exceptions and pending states.

### Changed

- Define content boundaries for spec, design and plan: keep the spec when external
  requirements do not change, and update only the affected design and plan with
  re-verification when the internal approach changes. Templates and examples keep
  stable acceptance scenarios, while concrete test implementation and execution
  records live in the plan and evidence.
- Adjust colloquial and mixed-English wording in the design and execution-plan
  templates; remove personal repository links, source commit IDs and
  business-specific evidence paths from writing examples, and replace personal
  absolute paths in the demonstration plan with relative paths.

### Fixed

- Extend the Codex uninstaller's manifest path scope to `.codex/runtime/`, clean
  old runtime files still recorded in the manifest on upgrade, and remove runtime
  libraries and assets on uninstall; unlisted user tools, skills and configuration
  are preserved, with install/upgrade/uninstall regressions (source issue #151).
- Preflight the Codex manifest and delete owned files without following directory
  links; keep the manifest and stop the upgrade on unsafe paths. User extension
  configuration is not deleted even if it was wrongly listed, and the missing
  manifest hint plus Codex installation notes are completed.
- Share resource and path rules across Codex first install, upgrade and uninstall,
  reject directory links before writing and backing up configuration, and make
  unknown or illegal manifest entries fail while keeping the manifest. Errors
  report the concrete path and errno, and the whole installation package is
  checked against the manifest.
- Unify review, test, validate and bridge findings back into the affected
  artifacts and record handling and re-verification in the existing execution
  plan; invalidate affected old conclusions after input changes. Archiving
  requires all AC and verification results to pass, all Tasks to be Done, blocking
  issues to be closed, historical Red evidence to be retained and a Verification
  Final Status.
- Sync post-PR repairs to the original source PR and re-verify its actual head;
  add a read-only source publication check that blocks uncommitted or unpushed
  repairs. Unfinished Steps now recognise ordered and unordered lists, and a clean
  closure section is no longer warned about when omitted.

## [0.14.3] - 2026-10-31

Source: `main@67f904394df4743913a42f56dae7f6b89732eb08`.

### Added

- Track the Session ID of every deliverable update in a `.sessions.json` sidecar
  and mirror it into frontmatter plus a `## 会话记录` table. The new
  `update-sessions-sidecar.py` takes a cross-platform lock, deduplicates sessions
  without dropping log entries, accepts OpenCode `ses_*` and Codex/Claude UUIDs,
  and fails open when the host exposes no ID. Templates, contracts, validation,
  the Claude/Codex/OpenCode/OpenClaw hooks and nine skills carry the same
  contract (source PR !181).
- Load the OpenCode plugin under OpenCode 2.x through a V2 default export with
  `{id, setup}` while keeping the V1 named export, so the bootstrap and
  session-ID context hook run on both versions (source PR !181).
- Query one effective delivery contract and validate by phase: base rules,
  recorded profiles, artifact dependencies and conditional triggers merge into a
  single result shared by generation and validation (source PR !193).
- Add `lite` / `standard` / `critical` delivery levels. Lite changes need fewer
  sections and may omit a standalone design; critical changes add a validation
  spec and the applicable threat analysis. A host-only verification plan may
  declare `host-only` without choosing a target product or device (source
  PR !193).
- The OpenSpec bridge collects native CLI state, immutable source snapshots and
  task mapping, keeps its native directory, delta and task progress, then syncs
  the ODK delivery artifacts separately (source PR !193).

### Changed

- Clarify the boundaries of Chinese placeholder markers and how to fill status
  values, with regressions for ordinary Chinese prose and explicit status values
  (source PR !193).
- Refresh quick-start, user guide and handoff docs for version checks,
  configured-skill installation and initialization, and state that the source
  version is not the published version (source PR !193).

### Fixed

- Every skill reads the complete existing target document before revising it in
  place, preserving confirmed decisions, stable IDs, progress and evidence, and
  creates a file only when it is missing; init also reuses an existing proposal
  (source PR !193).
- Profile-added sections, AC categories, prohibitions and required dimensions
  participate in programmatic validation; resource, security and i18n trigger
  results enter the effective contract; OpenSpec native writes are no longer
  redirected into ODK directories (source PR !193).
- Review, test, validate and bridge findings are written back to the affected
  artifacts and recorded with re-verification in the existing execution plan;
  changing an input invalidates affected earlier conclusions. Archive requires
  all ACs and verifications to pass, tasks complete and blocking issues closed,
  keeps historical Red evidence and adds a Verification Final Status (source
  PR !194).
- Post-PR repairs must be synced to the original source PR and re-verified
  against its actual head; a new read-only source-publication check blocks
  uncommitted or unpushed repairs. Incomplete Steps recognize ordered and
  unordered lists, and a clean result omits the closure section without a
  warning (source PR !194).
- The Codex uninstaller includes `.codex/runtime/` in the manifest path scope,
  cleans runtime files still recorded in the manifest on upgrade, and removes
  runtime libraries and assets on uninstall while preserving unlisted user
  tools, skills and configuration; adds install/upgrade/uninstall regressions
  (source PR !195, issue #151).
- Codex deletes manifest-owned files after a preflight and never follows
  directory links; unsafe paths keep the manifest and stop the upgrade. User
  extension configuration is never deleted even if it appears in the manifest,
  and missing-manifest guidance plus Codex install docs are added (source
  PR !195).
- Codex first install, upgrade and uninstall share resource and path rules;
  installation rejects directory links before writing and before backing up
  configuration; unknown or illegal manifest entries fail and keep the
  manifest. Errors report the concrete path and errno, and whole-package
  manifest coverage is checked (source PR !195).
- Ship the OpenSpec `ohos-spec-driven` schema and its templates under
  `runtime/assets/adapters/openspec-schemas/`, so bridge skills can install the
  complete schema from the published package instead of a source-only path
  (source PR !198).
- Treat the legacy `国际化/无障碍` involvement label as `国际化` when reading
  existing artifacts, so previously written tables stay valid (source PR !198).
- Keep OpenSpec's native `ADDED` / `MODIFIED` / `REMOVED Requirements` delta
  sections, with US IDs in `### Requirement:` titles and AC IDs in
  `#### Scenario:` titles carrying WHEN/THEN behavior, in the shipped schema,
  the spec template and the bridge guide; the previous template emitted an AC
  list that native validation rejects (source PR !199).
- Require native delta validation before an authorized archive or main-spec
  merge, since status/apply completion only tracks artifacts and tasks
  (source PR !199).
- Require complete archive evidence: every listed task needs exactly one detail
  block, all verification rows need Actual Result and Pass status, and unassigned
  tables or duplicate details fail; custom headings inside Task details no
  longer hide a failing verification table (source PR !202).
- Keep native OpenSpec Requirement and Scenario titles verbatim for
  MODIFIED/REMOVED requirements, since those titles are archive matching keys;
  record ODK US/AC associations in the delivery projection and
  `requirement_map` / `scenario_map` instead of renaming the native titles
  (source PR !202).
- Require lite execution plans to declare `验证范围 = host-only` and reject
  target build or device commands in the plan and its task verification
  (source PR !202).
- Detect target tools executed inside quoted command substitutions, so a
  host-only plan such as `test "$(hdc shell uname)" = OpenHarmony` again needs a
  target product and device; single quotes, escaped literals, tool lookups and
  `noexec` arguments keep their host-only meaning, and only an enclosing
  Markdown code span is stripped (source PR !203).
- Accept quoted session IDs in YAML block and flow sequences, and keep partial
  writes from corrupting the sidecar (source PR !181).
- Run the Node.js session-start hooks directly on Windows, replace real session
  IDs in examples with fake data, and remove the unused dsh adapter
  (source PR !181).

## [0.14.2] - 2026-10-30

Source: `main@b7b728353dad9a546ba74049155f365493e08159`.

### Added

- Entry commands check for ODK updates before running and compare the session
  snapshot instead of on-disk versions, so an update already seen in this session
  is not reported again (source PR !182).
- Configured skills are installed on demand: when a configured skill is missing
  for the current agent, ODK reads the install link from the comment above the
  parameter (user override first, then the default config), verifies it, installs
  it and continues. Covers review hooks, post-CR/MR/PR hooks, device flashing and
  CI/online-test triggers; a step that needs a restart stays pending (source
  PR !186).
- brainstorm, propose, spec and design share one decision-interview protocol that
  separates code facts, confirmed goals and assumptions, tracks open questions,
  decisions, contradictions and their dependencies between rounds, and reopens
  the affected decisions when a premise changes (source PR !179).

### Changed

- `post_pr_hooks` is renamed to `post_cr_mr_pr_hooks`. The legacy name stays
  readable in user overrides, and the new key wins when both appear in the same
  file, including an explicit empty value (source PR !185).
- `构建与验证环境` is no longer a globally required `execution-plan.md` section.
  Current plans still fill it through the plan template and the example check,
  while legacy plans keep the implement-time backfill (source PR !148).

### Fixed

- Archive validation distinguishes real unfinished values from prohibition
  examples: `TBD` / `TODO` quoted after 不得/禁止/请勿 + 使用/出现 no longer blocks
  archiving, and markers written next to Chinese text are detected too (source
  PR !191, issues #149/#150).
- Archive placeholder diagnostics report the section name and the file line
  (from 1) instead of a section-relative offset, for required and optional
  documents alike (source PR !191, issue #150).
- Entry commands continue the original request when a legacy installer never
  injects a session version snapshot, rather than asking for a restart that
  cannot help. A genuine pending restart or incomplete upgrade still stops the
  step (source PR !188).
- Distribution works with macOS system tools: no GNU sed, BSD `find` and Bash 3.2
  are supported, and shared resource replacement uses a Python POSIX file lock
  (source PR !189).
- plan requires explicit confirmation of the build product before writing the
  execution plan instead of silently adopting the configured default, and records
  the candidate list with the confirmed product (source PR !183).
- The update flow verifies each agent's installation after updating and keeps the
  pending step when a restart or a later round is required (source PR !184).

## [0.14.0] - 2026-10-28

Source: `main@bfcaabbbea79835569dbf93d61925083a001d570`.

### Added

- Internationalization scope criteria, design sections and validation from source PR !168.

- Reject ambiguous document sections: a duplicated required or conditional
  section (including `DFX 设计` and its fault-mode subsections) now fails closed
  and is reported once, instead of being read as absent and silently skipping the
  DFX gates (source PR !177).
- Accept private PR/MR route names and opaque IDs in `metadata_tracking.yaml`,
  validating credential-free HTTPS, host and repository path boundary while
  rejecting navigation segments and encoded delimiters.

- Configure an ordered product menu with `build_products`; retain `build_product`
  as the preferred default. Plans record the candidate list and one confirmed
  product; implementation reuses the selection or resolves a requested switch.

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

- Reject duplicate nine-column DFX main tables so an ambiguous layout cannot
  bypass the C2/C3 gates (source PR !178).

- Import the source revision containing PR !174 contract-gate repairs (bare template paths and migrated regression fixtures).

- Resolve resource self-checks relative to the actual guide location in source,
  native and neutral layouts, without restoring resource-root placeholders.
- Require rk3568 and a configured flashing skill before automatic flashing;
  confirm the target device and avoid repeated firmware preparation.
- Resume brainstorm using its installed skill name rather than a Claude command.
- Ship the default configuration, archive migration validator and all Python
  runtime libraries; align release metadata with the merged source revision.
- Ship the shared `require_unique_section` runtime helper so gates can tell a
  duplicate section from a missing one, and make `repository_url` an explicit
  template field so non-GitCode PRs record their real target repository URL.
- Declare the complete asset tree so installation includes the default config,
  retaining named asset components for literal-path relocation. Remove stale
  skill-local symlinks pointing to a maintainer's machine; keep FMEA references
  as real files alongside the skill.

### Installation verification

- Re-synchronized source main after merging configurable product selection and verified installation
  with the official npm oh-skillhub 0.1.43 release containing the auxiliary-file
  copy fix. All 40 workflow regression tests pass, including V1/V2 installation
  for Claude Code, Codex and OpenCode, FMEA's 44 reference files, default config
  and runtime references. The source release gate also passes for all three hosts.
- oh-skillhub 0.1.42 still omits skill-local files in workflow-plugin projections;
  use 0.1.43 or a later version passing the installation check.

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
