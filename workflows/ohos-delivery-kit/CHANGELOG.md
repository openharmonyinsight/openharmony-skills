# Changelog

All notable changes to the published `ohos-delivery-kit` workflow are documented in
this file. Source artifacts are synchronized from
`oshunter/ohos-delivery-kit` `main` through the marketplace publisher.

## [0.12.1] - 2026-10-15

Source: `main@81489b83490c5eb7e211a51308b237d940426bea`.

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
- 66 test cases in `test-validate-dfx.py` covering C3 gate and export table.

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

## [0.11.0] - 2026-09-04

Source: `main@b4686f444d8550489a0e8cfcb0fd0ee9100736c9`.

### Added

- `odk-submit-design-docs` generates `metadata_tracking.yaml` before design-docs
  submission and validates the formal five-file bundle.
- The metadata template supports `pull_requests: []` before a pull request is created.
- A release-documentation regression check keeps the published README and changelog
  aligned with the shipped workflow contract.
- An executable per-API specification contract validates shared attributes, qualified
  signatures, required specification and description elements, and device behavior.

### Changed

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

- Local archive-migration validation detects legacy non-numeric formal IDs before
  they are submitted with the 0.11.0 contract.
- Per-API validation ignores HTML comments and fenced examples, rejects duplicate or
  unresolved API decisions and malformed shared attributes, validates C/ArkTS generic
  and type syntax, handles escaped table pipes, and canonicalizes semantic signatures.
- Design-docs metadata requires complete populated PR/issue entries, accepts GitCode
  `merge_requests` URLs, rejects unknown fields, correlates issue IDs with URLs, and
  enforces issue state consistency.
