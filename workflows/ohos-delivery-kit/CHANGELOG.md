# Changelog

All notable changes to the published `ohos-delivery-kit` workflow are documented in
this file. Source artifacts are synchronized from
`oshunter/ohos-delivery-kit` `main` through the marketplace publisher.

## [0.12.0] - 2026-09-24

Source: `main@1ba43562551f551c4d9ee2feb5e0b3bada9ff849`.

### Changed

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
