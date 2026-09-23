---
name: odk-submit-design-docs
description: "Use when submitting, publishing, or synchronizing an ODK design-document bundle. Confirms the design-docs destination from the source remote or developer configuration, then generates metadata_tracking.yaml. Zero plugin dependencies."
license: MIT
---

# ODK Submit Design Documents

## Preconditions

- Resolve the active directory as `codespec/changes/<repo-name>/<req-id>/`.
- `<req-id>` and `proposal.md` frontmatter `req` must contain digits only; drafts cannot be submitted.

## Confirm Destination

Read the business repository's `git remote get-url origin` (not the design-docs checkout's remote) and developer-owned `codespec/profile.yaml` key `design_docs_repository`. If `origin` is missing or ambiguous, ask which source remote applies; never select another remote silently.

Use the read-only resolver `{{EXECUTABLE_ROOT}}/lib/odk_repository.py` with `--remote` and, when configured, `--configured` to obtain `action`, `repository`, and `source`. It performs no network access or writes.

- For a valid configured address, show that address and request confirmation; never silently replace an explicit configuration with the default.
- Without a configured address, a GitCode source (`gitcode.com` exact host; HTTPS, SSH URL, or SCP-style `git@gitcode.com:org/repo.git`) prompts: “是否将当前设计文档提交到 https://gitcode.com/OpenHarmonyAI/design-docs ？” The URL is a suggestion, not authorization. Do not match `gitcode.com` substrings in paths or other hostnames.
- For any other source, unavailable remote, or invalid configuration, report “design-docs 仓地址：待开发者填写” and require the user to supply a repository address, then confirm it. Do not default these cases to OpenHarmonyAI or the business repository.
- If the user declines the suggested destination, ask for another address or cancel. No answer is not consent. Before confirmation, do not clone, copy, stage, commit, or push design documents. A confirmed target may be used for this submission; only persist it to the developer-owned profile when the user requests that change.
- Before reusing a checkout, run the resolver with `--configured` set to the confirmed address and `--checkout-remote` set to that checkout's origin. Reuse only when `checkout_matches` is true. It compares transport, host, effective port, account and full repository path, including SSH absolute versus home-relative paths. Different ports, accounts, paths, or HTTPS/SSH transports are not automatic aliases: use a matching checkout, or show the actual endpoint and obtain explicit confirmation for it, then recheck. Confirm branch and commit/push/PR scope; never infer permission to push a protected/default branch.
- Fetch identity does not authorize push. When pushing is requested, choose the explicit push remote and refspec within the user's scope; immediately before push, read **all** effective addresses with `git remote get-url --push --all <that-remote>`. Pass each returned URL as a separate `--push-url` to the resolver with the confirmed `--configured` target. Proceed only when `push_targets_match` is explicitly true; lookup errors, no addresses, unresolved addresses or any mismatch stop the push. This includes `pushurl` and `pushInsteadOf` rewrites. Reconfirm any changed actual target rather than silently accepting it. Use that same checked remote and explicit refspec for push, not Git's implicit push destination; if configuration/selection changes, recheck.

## Steps

Before copying, staging, committing, or pushing design documents, generate or refresh `metadata_tracking.yaml` from `{{ASSET_ROOT}}/templates/metadata_tracking.yaml`:

1. Set `req_id` from the formal directory leaf. It is the same identifier as proposal `req`; do not introduce a second requirement-identity field.
2. Set `target_release` from `proposal.md` frontmatter.
3. Resolve the business repository as full `namespace/repository` from the Git `origin` URL (preserve subgroup paths). Do not store only the repository basename or replace the business identity with the design-docs destination. If a local/unsupported remote cannot provide this identity, ask for a supported business remote; do not guess it.
4. Run `git rev-parse HEAD` in the business repository and use that exact current-branch commit for a PR entry. Inspect the current branch and its upstream. For a GitCode source, query the available GitCode PR interface for PRs whose source branch or head commit matches. For other hosts, do not query GitCode as though it were the source; report PR discovery unavailable under the current GitCode-only PR schema and use step 6. Never invent a PR number, title, state, or commit.
5. Add every matching business-code GitCode PR with its URL, title, state (`open`, `merged`, or `closed`), and commit SHA. If GitCode cannot be queried, preserve existing valid PR entries and report that discovery was unavailable.
6. Write the explicit key `pull_requests: []` only when no matching business-code PR exists or PR discovery is unavailable and the file has no valid existing PR entry. This is a valid submission state; report which condition applied.
7. Do not add `issues` by default. Treat it as an optional extension: preserve existing valid issue entries, or add them only when the user explicitly requests issue tracking. When used, include known `issue`, GitCode URL, title, type (`requirement`, `bug`, `task`, or `epic`), state (`open` or `closed`), and `closed_at: YYYY-MM-DD` values.
8. Preserve valid entries for other involved repositories when refreshing an existing file. Never discard cross-repository tracking data merely because it cannot be re-derived locally.

For a non-GitCode current business repository, the current schema requires `pull_requests: []` and absent/empty `issues` for that entry. GitCode records with the same namespace/path are not records of this source host. If existing data has that ambiguity, report the conflict and stop for user resolution rather than silently deleting or relabeling it; distinct other-repository entries remain intact.

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
  "codespec/changes/<repo-name>/<req-id>" --design-docs-submit
```

`--design-docs-submit` automatically enables the same final-readiness checks as `--archive`, including unresolved placeholders, code mapping, per-task `Actual Result`, DFX closure, and resource constraints.

Do not submit if validation fails. Copy the five base files and required conditional
evidence to the same relative path under the confirmed design-docs checkout:
`codespec/changes/<repo-name>/<req-id>/`. Preserve evidence referenced by the documents;
do not copy unrelated files. Before committing, verify the copied files against the
validated source bundle; do not substitute the design-docs remote/HEAD for business
repository identity or re-generate business metadata in the destination checkout.

An explicit request to submit or publish the design documents authorizes preparing and synchronizing this bundle. Follow the user's requested Git scope for commit/push/PR operations; the ordinary business-code submission reminder alone is not authorization to mutate another repository.

## Output

Report:

- the resolved `design_docs_repository`, whether it came from configuration/default/user input, and the user's destination confirmation;
- the destination directory;
- whether `metadata_tracking.yaml` was created or refreshed;
- whether `pull_requests` is populated or intentionally `[]`;
- validator result;
- the Git commit/push/PR action actually performed, if any.
