---
name: review-gitcode-pr
description: Review a GitCode pull request from a PR number or URL when `oh-gc` must fetch PR metadata, diff, and comments, local repository code must be inspected for context, and the output should be concrete findings or a GitCode submission draft. Use for GitCode PR review or comment-submission requests that depend on `oh-gc`. Do not use for generic local review, GitHub/GitLab flows, or automatic submission without explicit user confirmation.
---

# Review GitCode PR

Run this skill when the review starts from a GitCode PR reference and must combine `oh-gc` artifacts with local repository inspection.

## Workflow

### 1. Resolve The PR

Normalize the user input first.

- If the user gave a PR number, use it directly.
- If the user gave a URL, extract the PR number and, when possible, the `OWNER/REPO`.
- If the normalized result does not include `OWNER/REPO`, `scripts/collect_pr_context.py` will try to infer it from the current repository's GitCode remote URLs.
- If remote inference is ambiguous or the current checkout is not a GitCode clone, pass `--repo OWNER/REPO` explicitly.
- Use `scripts/normalize_pr_ref.py` for this normalization step.

### 2. Collect Remote Context

Use `scripts/collect_pr_context.py` to fetch and save the PR context before reviewing code manually.

The script gathers:

- `oh-gc pr:view NUMBER --json`
- `oh-gc pr:diff NUMBER --json`
- `oh-gc pr:diff NUMBER --name-only`
- `oh-gc pr:diff NUMBER --color never`
- `oh-gc pr:comments NUMBER --json --comment-type pr_comment`
- `oh-gc pr:comments NUMBER --json --comment-type diff_comment`

Review the generated artifact directory before making claims. Read artifacts in this order:

1. `summary.json` to identify changed files, parsed hunks, commentable new-side lines, and existing normalized context.
2. `pr-diff.txt` to verify exact diff text and hunk boundaries for any candidate finding.
3. `pr-view.json` for title, description, branch, and high-level PR metadata.
4. `pr-diff.json` or raw comments output only when the normalized summary is insufficient.

Do not load every artifact by default. Start from `summary.json` and only drill down when a finding needs more evidence.

### 3. Read Local Code

Do not review from the diff alone.

Use `references/deep-review-checklist.md` as the required checklist for depth, stopping conditions, and risk-specific review prompts.

For every changed file, assign exactly one review status before finishing:

- `reviewed`: the file and its relevant context were inspected deeply enough to support findings or a no-finding conclusion
- `mechanical-low-risk`: the change is demonstrably mechanical and low-risk after verification against the checklist
- `skipped-with-reason`: the file was not reviewed in depth, and the reason and residual risk are stated explicitly

Do not stop after finding one or two issues. Keep reviewing until every changed file has one of the statuses above.

For each changed file that matters:

- Read the changed hunk.
- Read surrounding local code in the current repository.
- Follow imports, helpers, tests, and callers as far as needed to verify behavior, not just to form an initial suspicion.

Minimum depth rules:

- For production code changes, inspect at least one of: direct callers, direct callees, or related tests.
- For API, schema, persistence, concurrency, permission, cache, state-machine, or error-handling changes, inspect at least two of those areas and do not treat the diff in isolation as sufficient.
- For deleted or moved logic, verify that the previous responsibility still exists somewhere valid or that callers were updated accordingly.
- For new branches or new failure paths, verify whether tests cover both the success path and the new branch or explain why that verification was not possible.

Prioritize:

- Correctness bugs
- Behavior regressions
- Broken assumptions at call sites
- Missing or invalid tests
- Security or data handling issues

Prefer high-signal findings over style commentary.

Depth expectations:

- If a file appears low-risk, prove that with code context or tests instead of intuition.
- If a file appears high-risk, increase inspection depth before deciding there is no finding.
- If the repository context is insufficient, report that as a review limitation instead of silently reducing depth.

Use `references/review-rubric.md` when deciding whether a candidate issue is a real finding, assigning severity, or explaining residual risk when no findings are confirmed.

### 4. Produce Findings

Default output is issue-driven review, not a broad summary.

Use this template for each finding shown to the user:

`Severity | Path:Line | Problem | Evidence | Fix`

Include:

- Severity: `high`, `medium`, or `low`
- Path
- Best-effort line number on the new side of the diff
- Problem: what is wrong and why it matters
- Evidence: concrete code path, behavior, or missing test support
- Fix: what change would address it

If a valid diff line cannot be supported, fall back in this order:

1. File-level comment with `path`
2. General PR comment

Never invent a diff line number.

If no valid findings are discovered, state that explicitly and include:

- the review status for each changed file or file group
- the main code paths, callers, callees, or tests inspected
- any checklist categories that could not be verified
- residual uncertainty or testing gaps instead of padding with style feedback

Do not say "no actionable issues found" unless the file coverage and checklist pass were completed for the inspected scope.

Use `references/no-finding-template.md` as the default output shape when the inspected scope has no confirmed findings.

When drafting comments that may be submitted back to GitCode:

- Write in Chinese by default unless the user explicitly asks for another language.
- Use concise Markdown, not a single pipe-delimited sentence.
- Separate conclusion, problem analysis, and suggested fix into short paragraphs or bullet points.
- Wrap identifiers such as parameters, files, and status codes in backticks.

### 5. Prepare Submission Draft

This skill uses a two-step submission flow.

Default behavior:

- Review the PR
- Produce findings for the user
- If the user wants submission, create a structured draft first

Use `references/review-draft-schema.md` for the draft shape and `scripts/prepare_review_submission.py` to validate it against the collected context.

The draft may include:

- One general PR summary comment
- Zero or more diff comments with `path` and `line`
- Optional approval intent

Approval gate:

- Set `approve: true` only when no blocking or high-severity findings remain and the user explicitly wants approval.
- If the review contains blocking findings, submit comments only; do not call `oh-gc pr:review`.

Important: `oh-gc pr:review` only supports approval. It is not a general "submit review" endpoint.

For submitted comments, follow the Markdown and Chinese-writing rules in `references/review-draft-schema.md`.

### 6. Submit Only After Confirmation

Never submit to GitCode implicitly.

When the user explicitly asks to submit:

1. Build the draft JSON
2. Run `prepare_review_submission.py` without `--execute` to preview commands
3. Show the user the exact summary and comment count you plan to post
4. After confirmation, run the same command with `--execute`

If execution fails partway through, report exactly which comments succeeded and which did not.

## Quick Flow

Use these commands only as a compact reminder after reading the workflow above.

```bash
python3 skills/review-gitcode-pr/scripts/collect_pr_context.py 123
```

Primary review artifacts:

- `summary.json`
- `pr-diff.txt`
- `pr-view.json`

Depth reminder:

1. Read `summary.json`
2. Classify each changed file by risk using `references/deep-review-checklist.md`
3. Review every file until it has a final status
4. Only then decide whether the review has zero findings

Preview a draft submission:

```bash
python3 skills/review-gitcode-pr/scripts/prepare_review_submission.py \
  --context-dir .review-gitcode-pr/pr-123 \
  --draft review-draft.json
```

Execute only after explicit user confirmation:

```bash
python3 skills/review-gitcode-pr/scripts/prepare_review_submission.py \
  --context-dir .review-gitcode-pr/pr-123 \
  --draft review-draft.json \
  --execute
```

## Failure Handling

Handle failures explicitly. For each blocker, report:

- `Blocker`: what failed and which command or assumption failed
- `Fallback`: what review scope remains possible
- `Next step`: what the user or agent should do next

### `oh-gc` unavailable

- Blocker: `oh-gc` is missing from `PATH` or cannot be executed.
- Fallback: do not attempt GitCode fetch or submission. Only continue if a previously collected artifact directory already exists locally and is sufficient for a non-submitting review.
- Next step: ask the user to install or expose `oh-gc`, or point to existing artifacts to review offline.

### Authentication or permission failure

- Blocker: `oh-gc` returns authentication, authorization, or API permission errors for PR view, diff, or comments.
- Fallback: keep any partial artifacts already collected. Continue only with successfully fetched diff/context that is sufficient for a non-submitting review. Do not attempt submission.
- Next step: tell the user which command failed and that they need to re-authenticate or obtain access before remote review or submission can continue.

### Local repository mismatch

- Blocker: the current repository does not match the PR repository, branch layout, or file set closely enough to verify behavior in local code.
- Fallback: do not claim code-level confidence from diff-only inspection. At most, provide a limited review explicitly labeled as diff-only if the user still wants that.
- Next step: ask the user to switch to the matching repository checkout or provide the correct local workspace before continuing with a full review.

### Diff JSON missing, malformed, or incomplete

- Blocker: `pr:diff --json` changes shape, omits hunks, or cannot be parsed reliably enough for structured line mapping.
- Fallback: use `pr-diff.txt` as the source of truth for diff reasoning. Only emit line comments when a new-side line can still be verified confidently from raw diff text; otherwise fall back to file-level or general comments.
- Next step: tell the user that structured diff parsing degraded and that submission precision may be reduced until the JSON format is fixed.

### Submission preview or execute failure

- Blocker: `prepare_review_submission.py` validation fails, preview commands do not match the draft, or `--execute` fails for some comments.
- Fallback: keep the validated draft and any successful partial submission results. Do not silently retry with changed semantics.
- Next step: report the exact failed comment or command, which comments were already posted, and what must be corrected before retrying.
