# Automatic post-implementation handoff

Applies after all approved implementation Tasks are Done. Explicit user limits
(for example implementation only or no publishing) take precedence. This is an
agent orchestration policy, not a background daemon. Invoke skills by their
installed names; do not ask the user to type the next review/validation command.

## 1. Review and validate without publishing

- Read `pre_commit_reviews` from config (odk_config_ext.yaml (optional, in runtime/assets/) overrides odk_config.yaml; absent or empty → defaults to `odk-review`). It is a space-separated list of skill names to invoke in order before the source PR. Invoke each listed skill in sequence; each must return PASS or actionable findings. All must pass before the PR reminder in Step 2. The default `odk-review` does a fresh AC/code-quality review of the actual working-tree diff, including untracked implementation files. A commit is not a prerequisite. Review code, tests, error paths and deviations, not just document structure.
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

Only after all `pre_commit_reviews` skills pass, summarize results and remind the user:
“下一步是提交源码仓 PR，需要时请告诉我提交。” End the automatic checks here.
Do not begin staging, committing, pushing, or PR creation from this reminder.
Wait for an explicit source-PR instruction such as “提交源码 PR”. Confirmation of
implementation or successful validation is not submission authorization.

After the user triggers source PR submission, automatically perform the following
within that request. Read `source_cli` from config (odk_config_ext.yaml overrides odk_config.yaml; default `oh-gc`) — use it for all PR create/list/query operations below. Show the source repository, actual push endpoint, branch and
PR target/base. Ask only for missing or ambiguous routing information; do not
repeat a permission question for the same already-authorized submission. If code
changed since the checks, re-review/revalidate affected inputs before publishing.

- Stage only the reviewed business-code scope. **Never include `codespec/` or any file under it in the source-code commit** — `codespec/` is the design-docs archive and belongs exclusively to the design-docs repository; committing it to the source-code repository is a hard constraint, not a suggestion. Never sweep unrelated user changes into a commit. Before running `git commit`, run `git status` and verify that no path beginning with `codespec/` appears in the staged list; if any do, unstage them immediately with `git restore --staged codespec/` before proceeding. If `codespec/` is not in `.gitignore`, add it now — this prevents accidental staging in future commits.
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
- After the source PR URL is confirmed, invoke each skill listed in `post_commit_reviews` (from config; space-separated) in order. Each skill receives the confirmed PR URL as context. Report findings; unresolved findings from post-commit reviews are surfaced to the user but do not roll back the PR.
- After post-commit reviews, **ask the user whether to trigger the CI gate** before executing it — unless `ci_trigger` is `none`, in which case skip the prompt entirely. Read `ci_trigger` from config (odk_config_ext.yaml overrides odk_config.yaml; default `comment:start build`). Prompt (only when ci_trigger ≠ none):
  ```
  源码 PR 已确认：<PR URL>
  是否需要触发门禁（CI）？
  A) 是，触发门禁（<ci_trigger 模式简述>）
  B) 否，跳过

  （ci_trigger = <config 中的值>）
  ```
  If the user chooses A, execute the mode: `comment:<text>` — post a PR comment via `source_cli`; `label:<name>` — add the label via `source_cli`; `skill:<name>` — invoke the named skill with the PR URL. Report the result; if it fails to post, report it without retrying silently.
- After the CI gate action is resolved, **ask the user whether to trigger online tests** before executing them — unless `online_test_trigger` is `none`, in which case skip the prompt entirely. Read `online_test_trigger` from config (odk_config_ext.yaml overrides odk_config.yaml; default `none`). Prompt (only when online_test_trigger ≠ none):
  ```
  是否需要触发线上测试？
  A) 是，触发线上测试（<online_test_trigger 模式简述>）
  B) 否，跳过

  （online_test_trigger = <config 中的值>）
  ```
  If the user chooses A, execute the mode using the same comment/label/skill semantics as ci_trigger. Report the result.
- After the online-test action is resolved, **execute any custom post-PR hooks** configured in `post_pr_hooks` (from config; odk_config_ext.yaml overrides odk_config.yaml; default `""`). If `post_pr_hooks` is empty, skip silently. Otherwise invoke each skill listed (space-separated) in order, passing the confirmed source PR URL as context. Report each skill's findings. Unresolved findings are surfaced to the user but do not roll back the PR.

## 3. Generate local metadata, then ask about design-docs

Once the source PR is confirmed, **immediately generate `metadata_tracking.yaml`** from that actual PR before doing anything else in this step. Follow [metadata.md](metadata.md) to generate or refresh it. This is mandatory — do not skip or defer it. Preparation is part of the approved source-PR handoff; it does not authorize a write to another repository. Preserve unrelated repository/issue records. Confirm the remote head SHA agrees with the business checkout HEAD; stop on a mismatch rather than inventing a SHA.

Track non-GitCode PRs using their real URLs and an explicit `repository_url` as
specified in the metadata guide. Do not convert them to GitCode URLs or represent
successful tracking as an empty list. Unsupported URL formats or unavailable host
access stop the handoff with an explanation. Standalone document submission
retains its documented no-PR mode.

After `metadata_tracking.yaml` is generated and verified, **immediately prompt the user about design-docs submission** with an explicit choice — do not bury this as a side note:
```
源码 PR 已提交：<PR URL>

下一步：是否需要将设计文档提交到 design-docs 仓？
A) 是，现在提交 design-docs 仓的 PR
B) 否，稍后再提交

design-docs 仓地址：<从 odk_config_ext.yaml 覆盖 odk_config.yaml 的 design_docs_repository 读取，默认 https://gitcode.com/OpenHarmonyAI/design-docs；若为空则显示"待开发者填写"并请用户提供>
```
Wait for the user's explicit answer. Only proceed with design-docs submission after choosing A.

Only after separate document-submission confirmation invoke
`odk-submit-design-docs`: verify destination/push endpoints, refresh metadata if
needed and run `--design-docs-submit` in the business checkout before copying the
five base files plus required evidence. No clone/copy/stage/commit/push to the
document repository before confirmation. After confirmation and address resolution,
automatically commit/push the document branch and create or update its PR, not just
copy files; return the verified document PR URL. Ask only for missing branch/base
or access information. Refusal keeps the source PR and local metadata intact.
Neither source nor document submission authorizes merging.
