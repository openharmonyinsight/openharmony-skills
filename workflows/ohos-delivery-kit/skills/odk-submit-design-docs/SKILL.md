---
name: odk-submit-design-docs
description: "Use when submitting, publishing, or synchronizing an ODK design-document bundle to the developer-configured design-docs GitCode repository. Generates metadata_tracking.yaml before submission. Zero plugin dependencies."
license: MIT
---

# ODK Submit Design Documents

## Preconditions

- Resolve the active directory as `codespec/changes/<repo-name>/<req-id>/`.
- `<req-id>` and `proposal.md` frontmatter `req` must contain digits only; drafts cannot be submitted.
- Read `design_docs_repository` from developer-owned `codespec/profile.yaml`. If it is absent, report “待开发者填写” and ask for the address; never guess it.

## Steps

Before copying, staging, committing, or pushing design documents, generate or refresh `metadata_tracking.yaml` from `{{ASSET_ROOT}}/templates/metadata_tracking.yaml`:

1. Set `req_id` from the formal directory leaf. It is the same identifier as proposal `req`; do not introduce a second requirement-identity field.
2. Set `target_release` from `proposal.md` frontmatter.
3. Resolve the business repository as `organization/repository` from the Git `origin` URL. Do not store only the repository basename.
4. Run `git rev-parse HEAD` in the business repository and use that exact current-branch commit for a PR entry. Inspect the current branch and its upstream, then query the available GitCode PR interface for PRs whose source branch or head commit matches. Never invent a PR number, title, state, or commit.
5. Add every matching business-code GitCode PR with its URL, title, state (`open`, `merged`, or `closed`), and commit SHA. If GitCode cannot be queried, preserve existing valid PR entries and report that discovery was unavailable.
6. Write the explicit key `pull_requests: []` only when no matching business-code PR exists or PR discovery is unavailable and the file has no valid existing PR entry. This is a valid submission state; report which condition applied.
7. Do not add `issues` by default. Treat it as an optional extension: preserve existing valid issue entries, or add them only when the user explicitly requests issue tracking. When used, include known `issue`, GitCode URL, title, type (`requirement`, `bug`, `task`, or `epic`), state (`open` or `closed`), and `closed_at: YYYY-MM-DD` values.
8. Preserve valid entries for other involved repositories when refreshing an existing file. Never discard cross-repository tracking data merely because it cannot be re-derived locally.

## Validate and Submit

The design-docs submission bundle is exactly:

- `proposal.md`
- `spec.md`
- `design.md`
- `execution-plan.md`
- `metadata_tracking.yaml`

Run:

```bash
python3 "{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py" \
  "codespec/changes/<repo-name>/<req-id>" --design-docs-submit
```

`--design-docs-submit` automatically enables the same final-readiness checks as `--archive`, including unresolved placeholders, code mapping, per-task `Actual Result`, DFX closure, and resource constraints.

Do not submit if validation fails. Copy the five files to the same relative path under the configured design-docs checkout: `codespec/changes/<repo-name>/<req-id>/`.

An explicit request to submit or publish the design documents authorizes preparing and synchronizing this bundle. Follow the user's requested Git scope for commit/push/PR operations; the ordinary business-code submission reminder alone is not authorization to mutate another repository.

## Output

Report:

- the resolved `design_docs_repository`;
- the destination directory;
- whether `metadata_tracking.yaml` was created or refreshed;
- whether `pull_requests` is populated or intentionally `[]`;
- validator result;
- the Git commit/push/PR action actually performed, if any.
