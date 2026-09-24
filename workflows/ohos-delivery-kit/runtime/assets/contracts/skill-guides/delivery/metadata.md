# Business PR metadata preparation

Generate or refresh local `metadata_tracking.yaml` using [the metadata template](../../../templates/metadata_tracking.yaml). Relative links resolve from this guide; codespec paths resolve from the business repository.

1. Set `proposal_id` from the formal directory leaf. It is the same identifier as proposal `proposal_id`; do not introduce a second proposal-identity field.
2. Set `target_release` from `proposal.md` frontmatter.
3. Resolve the business repository as full `namespace/repository` from the Git `origin` URL (preserve subgroup paths). Do not store only the repository basename or replace the business identity with the design-docs destination. If a local/unsupported remote cannot provide this identity, ask for a supported business remote; do not guess it.
4. Run `git rev-parse HEAD` in the business repository. Inspect the current branch and its upstream. Query the actual PR using that host's available API/tool and its confirmed URL or unambiguous source repository/branch and target/base. Use its remote source head SHA, not a predicted local commit or merge SHA; require agreement with business HEAD before submission. A push-time rewrite must preserve the reviewed tree. Never query GitCode for another host or invent a PR number, title, state, or commit.
5. Add verified business-code PR entries with the real URL, title, normalized state (`open`, `merged`, or `closed`), and full commit SHA. Set `repository_url` to the credential-free HTTPS web repository address for every newly generated repository entry, including empty origin entries. It must match `repo` and the PR's host, port and repository path. A fork PR's URL belongs to the target repository: store it under that target repository, and retain a separate origin entry (possibly `pull_requests: []`) when different. Never relabel the PR URL as belonging to the fork. If the host cannot be queried, preserve valid existing records and report the limitation.
6. Write the explicit key `pull_requests: []` only when no matching business-code PR exists or PR discovery is unavailable and the file has no valid existing PR entry. This is a valid submission state; report which condition applied.
7. Do not add `issues` by default. Treat it as an optional extension: preserve existing valid issue entries, or add them only when the user explicitly requests issue tracking. When used, include known `issue`, GitCode URL, title, type (`requirement`, `bug`, `task`, or `epic`), state (`open` or `closed`), and `closed_at: YYYY-MM-DD` values.
8. Preserve valid entries for other involved repositories when refreshing an existing file. Never discard cross-repository tracking data merely because it cannot be re-derived locally.

The automatic post-source-PR handoff requires a confirmed PR and fresh remote
metadata. If creation/query fails, the PR is ambiguous, or the source host is
not queryable with available tools/access, stop that handoff without replacing records with an empty list.
Steps 6–7 retain compatibility for explicit standalone design-document submission
without a PR; they must not mask a failed automatic source-PR operation.

Update an existing entry by its exact PR URL rather than appending duplicates.
Do not replace stale unrelated PR records with the current HEAD; report conflicts
that the strict submission validator cannot accept and ask for resolution.

`repository_url` is optional for legacy GitCode records (omission means
`https://gitcode.com/<repo>`). Non-GitCode PR records require it. Legacy empty
non-GitCode origin entries remain readable when no explicit current-origin entry
exists; otherwise an unqualified entry retains its default GitCode identity.
Write explicit URLs when refreshing.
Repository identity includes host, HTTPS port and full namespace/path, so identical
paths on different hosts are distinct. Never relabel ambiguous existing records.
Supported numeric PR/MR paths are `/pull/`, `/pulls/`, `/merge_requests/`,
`/-/merge_requests/`, `/pull-requests/`, and `/pullrequest/` after the repository
path (GitHub, GitLab, Gitea, Bitbucket and compatible hosts). Do not rewrite an
unsupported URL to fit: report the unsupported format and stop for resolution.
URLs must have no credentials, query or fragment. This extension covers PRs;
`issues` remain a GitCode-only extension and must be absent/empty on other hosts.
