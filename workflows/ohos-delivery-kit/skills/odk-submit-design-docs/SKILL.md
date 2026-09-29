---
name: odk-submit-design-docs
description: "Use when submitting, publishing, or synchronizing an ODK design-document bundle. Confirms the design-docs destination from the source remote or developer configuration, then generates metadata_tracking.yaml. Zero plugin dependencies."
license: MIT
---

# ODK Submit Design Documents

## Preconditions

- Resolve the active directory as `codespec/changes/<repo-name>/<proposal-id>/`.
- `<proposal-id>` and `proposal.md` frontmatter `proposal_id` must contain digits only; drafts cannot be submitted.

## Steps

### Confirm Destination

Read the business repository's `git remote get-url origin` (not the design-docs checkout's remote) and developer-owned `codespec/profile.yaml` key `design_docs_repository`. If `origin` is missing or ambiguous, ask which source remote applies; never select another remote silently.

Use the read-only resolver `{{EXECUTABLE_ROOT}}/lib/odk_repository.py` with `--remote` and, when configured, `--configured` to obtain `action`, `repository`, and `source`. It performs no network access or writes.

- For a GitCode business origin and a valid configured address, show that address and request confirmation; never silently replace an explicit configuration with the default.
- Without a configured address, a GitCode source (`gitcode.com` exact host; HTTPS, SSH URL, or SCP-style `git@gitcode.com:org/repo.git`) prompts: “是否将当前设计文档提交到 https://gitcode.com/OpenHarmonyAI/design-docs ？” The URL is a suggestion, not authorization. Do not match `gitcode.com` substrings in paths or other hostnames.
- For any other source or unavailable remote, require the user to supply a design-docs repository address for this submission, even when a profile has a previous address. An address explicitly supplied in the current request counts; otherwise report “design-docs 仓地址：待开发者填写”. Do not default to OpenHarmonyAI or the business repository. Pass the supplied address as `--configured` to validate/reuse the chosen target. Invalid configuration also requires a valid user-supplied address.
- If the user declines the suggested destination, ask for another address or cancel. No answer is not consent. Before confirmation, do not clone, copy, stage, commit, or push design documents. A confirmed target may be used for this submission; only persist it to the developer-owned profile when the user requests that change.
- Before reusing a checkout, run the resolver with `--configured` set to the confirmed address and `--checkout-remote` set to that checkout's origin. Reuse only when `checkout_matches` is true. It compares transport, host, effective port, account and full repository path, including SSH absolute versus home-relative paths. Different ports, accounts, paths, or HTTPS/SSH transports are not automatic aliases: use a matching checkout, or show the actual endpoint and obtain explicit confirmation for it, then recheck. Confirm branch and commit/push/PR scope; never infer permission to push a protected/default branch.
- Fetch identity does not authorize push. When pushing is requested, choose the explicit push remote and refspec within the user's scope; immediately before push, read **all** effective addresses with `git remote get-url --push --all <that-remote>`. Pass each returned URL as a separate `--push-url` to the resolver with the confirmed `--configured` target. Proceed only when `push_targets_match` is explicitly true; lookup errors, no addresses, unresolved addresses or any mismatch stop the push. This includes `pushurl` and `pushInsteadOf` rewrites. Reconfirm any changed actual target rather than silently accepting it. Use that same checked remote and explicit refspec for push, not Git's implicit push destination; if configuration/selection changes, recheck.

## Prepare Local Metadata

This preparation is also called after a confirmed source PR by the automatic
implementation handoff, before any design-docs submission authorization. In that
context perform only metadata preparation, not destination checkout or submission.

<!-- ODK:reference contracts/skill-guides/delivery/metadata.md -->
Read `{{ASSET_ROOT}}/contracts/skill-guides/delivery/metadata.md` to generate or refresh
`metadata_tracking.yaml`. Verify the current branch and upstream, `git rev-parse HEAD`,
and actual source-host PR results. Preserve valid existing tracking and distinguish the
standalone `pull_requests: []` case from failed automatic PR publication.
<!-- /ODK:reference -->

## Validate and Submit

The design-docs submission bundle always includes these five base files:

- `proposal.md`
- `spec.md`
- `design.md`
- `execution-plan.md`
- `metadata_tracking.yaml`

For `API/SDK=是`, also include `evidence/task1-api-declaration-en.diff` and
`evidence/task1-api-declaration-zh.diff`. Both must contain nonempty text unified
diffs with complete hunks and actual added/deleted lines, not blank files or labels.
Preserve their relative paths. No implicit no-change exemption exists: if genuine
evidence is unavailable, stop and report the missing evidence rather than fabricate it.
Structural validation does not prove applicability, bilingual equivalence, or
language correctness; review these against the actual declaration changes.

Run:

```bash
python3 "{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py" \
  "codespec/changes/<repo-name>/<proposal-id>" --design-docs-submit
```

`--design-docs-submit` automatically enables the same final-readiness checks as `--archive`, including unresolved placeholders, code mapping, per-task `Actual Result`, DFX closure, and resource constraints.

Do not submit if validation fails. Copy the five base files and required conditional
evidence to the same relative path under the confirmed design-docs checkout:
`codespec/changes/<repo-name>/<proposal-id>/`. Preserve evidence referenced by the documents;
do not copy unrelated files. Before committing, verify the copied files against the
validated source bundle; do not substitute the design-docs remote/HEAD for business
repository identity or re-generate business metadata in the destination checkout.

An explicit request to submit or publish the design documents authorizes preparing and synchronizing this bundle. Follow the user's requested Git scope for commit/push/PR operations; the ordinary business-code submission reminder alone is not authorization to mutate another repository.

When the user confirms “提交 design-docs 仓的 PR” (including the automatic handoff's
prompt), complete the document PR workflow automatically once target and branch/base
are known: prepare a scoped branch, stage only this bundle, commit, verify effective
push URLs, push, and create/update the unique matching open PR. Reuse a matching PR
rather than duplicate it; ask on ambiguous or closed/merged matches. Verify the remote
PR URL and head before reporting success. If push or PR creation/query fails, report
partial completion and stop; never report that a local copy is a submitted PR.
This confirmation is sufficient for those actions; do not ask again unless the scope
changes or required information is missing. Never auto-merge. Explicit copy-only
requests retain their narrower scope.

## Output

Report:

- the resolved `design_docs_repository`, whether it came from configuration/default/user input, and the user's destination confirmation;
- the destination directory;
- whether `metadata_tracking.yaml` was created or refreshed;
- whether `pull_requests` is populated or intentionally `[]`;
- validator result;
- the Git commit/push/PR action actually performed, if any.
