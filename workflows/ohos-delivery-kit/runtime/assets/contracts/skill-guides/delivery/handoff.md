# Automatic post-implementation handoff

Applies after all approved implementation Tasks are Done. Explicit user limits
(for example implementation only or no publishing) take precedence. This is an
agent orchestration policy, not a background daemon. Invoke skills by their
installed names; do not ask the user to type the next review/validation command.

## 1. Review and validate without publishing

- Invoke `odk-review` for a fresh AC/code-quality review of the actual working-tree
  diff, including untracked implementation files. A commit is not a prerequisite.
  Review code, tests, error paths and deviations, not just document structure.
- Then invoke `odk-validate` with the pre-PR archive gate: use the installed
  `validate-artifacts-contract.py <change-dir> --archive`. Do not use
  `--design-docs-submit` yet or fabricate PR metadata to satisfy the gate.
  Missing metadata is allowed here; existing metadata must remain well formed.
- Reuse verification evidence only for the same relevant code, inputs and
  environment. Changed inputs invalidate affected review/test results. Report
  checks not run; script exit 0 alone does not establish functional correctness
  or resolve warnings. Required tests and unresolved review findings must not
  be silently waived.
- On failure, report findings and fix only within the approved Task scope, then
  re-review and rerun affected checks. Stop for user direction on scope/design
  changes, missing prerequisites, or a repeated finding after one repair pass;
  never loop indefinitely. Any unfinished Task prevents the handoff.
- Called review/validate skills return results to this coordinator; they do not
  recursively restart it or each initiate a publishing flow. Standalone calls
  remain supported and do not imply approval to commit or publish.

## 2. Remind, then wait for the user to trigger the source PR

Only after review and validation pass, summarize results and remind the user:
“下一步是提交源码仓 PR，需要时请告诉我提交。” End the automatic checks here.
Do not begin staging, committing, pushing, or PR creation from this reminder.
Wait for an explicit source-PR instruction such as “提交源码 PR”. Confirmation of
implementation or successful validation is not submission authorization.

After the user triggers source PR submission, automatically perform the following
within that request. Show the source repository, actual push endpoint, branch and
PR target/base. Ask only for missing or ambiguous routing information; do not
repeat a permission question for the same already-authorized submission. If code
changed since the checks, re-review/revalidate affected inputs before publishing.

- Stage only the reviewed business-code scope. Exclude `codespec/` and metadata
  from the source-code commit; never sweep unrelated user changes into a commit.
- Verify all effective push URLs for the selected remote against the approved
  endpoint immediately before pushing; use that remote and explicit refspec.
  Do not infer permission for protected branches, force pushes, or merging.
- Query existing PRs by source repository/branch and target/base. Update a unique
  matching open PR instead of creating a duplicate; ask on ambiguity or a closed
  or merged prior PR. On uncertain API results, query before retrying a creation.
- Confirm the actual remote PR URL, title, state, source head SHA and repository
  identities after push. If push/PR creation/query fails, report the partial
  result and stop; never claim PR success or replace it with empty PR metadata.
- Check that any push-time SHA rewrite preserved the reviewed source tree. If
  remote content differs, stop and re-review/revalidate; do not label it verified.

## 3. Generate local metadata, then ask about design-docs

Once the source PR is confirmed, follow [metadata.md](metadata.md) to generate or
refresh local `metadata_tracking.yaml` from that actual PR. Preparation is part of
the approved source-PR handoff; it does not authorize a write to another repository.
Preserve unrelated repository/issue records. Confirm the remote head SHA agrees
with the business checkout HEAD; stop on a mismatch rather than inventing a SHA.

Track non-GitCode PRs using their real URLs and an explicit `repository_url` as
specified in the metadata guide. Do not convert them to GitCode URLs or represent
successful tracking as an empty list. Unsupported URL formats or unavailable host
access stop the handoff with an explanation. Standalone document submission
retains its documented no-PR mode.

Report the source PR and local metadata status, then ask whether to create/update
the design-docs repository's PR. For an exact `gitcode.com` business origin, use
`codespec/profile.yaml` key `design_docs_repository` if configured, otherwise offer
`https://gitcode.com/OpenHarmonyAI/design-docs`. For any non-GitCode or unknown
business origin, require the user to supply the design-docs address for this
submission; never silently reuse a profile address or infer the source host is
also the documentation host. A supplied address in the current request satisfies
this requirement. Missing destination configuration does not block the earlier
source-PR submission.

Only after separate document-submission confirmation invoke
`odk-submit-design-docs`: verify destination/push endpoints, refresh metadata if
needed and run `--design-docs-submit` in the business checkout before copying the
five base files plus required evidence. No clone/copy/stage/commit/push to the
document repository before confirmation. After confirmation and address resolution,
automatically commit/push the document branch and create or update its PR, not just
copy files; return the verified document PR URL. Ask only for missing branch/base
or access information. Refusal keeps the source PR and local metadata intact.
Neither source nor document submission authorizes merging.
