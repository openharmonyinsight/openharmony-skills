# Changelog

All notable changes to the published `ohos-delivery-kit` workflow are documented in
this file. Source artifacts are synchronized from
`oshunter/ohos-delivery-kit` `main` through the marketplace publisher.

## [0.11.0] - 2026-09-04

Source: `main@f639410d6850aaf3e891155860e54cfaf0d90f5f`.

### Added

- `odk-submit-design-docs` generates `metadata_tracking.yaml` before design-docs
  submission and validates the formal five-file bundle.
- The metadata template supports `pull_requests: []` before a pull request is created.
- A release-documentation regression check keeps the published README and changelog
  aligned with the shipped workflow contract.
- An executable per-API specification contract validates shared attributes, qualified
  signatures, required specification and description elements, and device behavior.

### Changed

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
