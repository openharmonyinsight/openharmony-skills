# Changelog

All notable changes to the published `ohos-delivery-kit` workflow are documented in
this file. Source artifacts are synchronized from
`oshunter/ohos-delivery-kit` `main` through the marketplace publisher.

## [0.11.0] - 2026-09-04

Source: `main@adaeb314b7434673259c1bbb67a7e22da5054a5d`.

### Added

- `odk-submit-design-docs` generates `metadata_tracking.yaml` before design-docs
  submission and validates the formal five-file bundle.
- The metadata template supports `pull_requests: []` before a pull request is created.
- A release-documentation regression check keeps the published README and changelog
  aligned with the shipped workflow contract.

### Changed

- **Breaking:** formal `req-id` values are digits only. The archive directory,
  `proposal.md` `req`, and `metadata_tracking.yaml` `req_id` must match.
- The formal design-docs submission gate requires `proposal.md`, `spec.md`,
  `design.md`, `execution-plan.md`, and `metadata_tracking.yaml` under
  `codespec/changes/<repo-name>/<req-id>/`.
- `issues` is an optional extension: it is omitted by default and added only when a
  developer explicitly requests issue tracking.

### Fixed

- Local archive-migration validation detects legacy non-numeric formal IDs before
  they are submitted with the 0.11.0 contract.
