---
name: ohos-dev-gitcode-pr-review
description: Review a GitCode pull request from a PR number or URL when `oh-gc` must fetch PR metadata, diff, and comments, local repository code must be inspected for context, and the output should be concrete findings or a GitCode submission draft. Use for GitCode PR review or comment-submission requests that depend on `oh-gc`. Do not use for generic local review, GitHub/GitLab flows, or automatic submission without explicit user confirmation.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: gitcode
  capability: pr-review
  version: 0.1.0
  status: draft
  tags:
    - gitcode
    - pr-review
    - code-review
  related-skills:
    - ohos-dev-security-code-review
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

- `oh-gc pr view NUMBER --json`
- `oh-gc pr diff NUMBER --json`
- `oh-gc pr diff NUMBER --name-only`
- `oh-gc pr diff NUMBER --color never`
- `oh-gc pr comments NUMBER --json --comment-type pr_comment`
- `oh-gc pr comments NUMBER --json --comment-type diff_comment`

Review the generated artifact directory before making claims. Read artifacts in this order:

1. `summary.json` to identify changed files, parsed hunks, commentable new-side lines, and existing normalized context.
2. `pr-diff.txt` to verify exact diff text and hunk boundaries for any candidate finding.
3. `pr-view.json` for title, description, branch, and high-level PR metadata.
4. `pr-diff.json` or raw comments output only when the normalized summary is insufficient.

Do not load every artifact by default. Start from `summary.json` and only drill down when a finding needs more evidence.

### 3. Read Local Code

Do not review from the diff alone.

Use `references/deep-review-checklist.md` as the required checklist for depth, stopping conditions, and risk-specific review prompts.

This skill owns the GitCode PR review workflow: PR context collection, changed-file coverage, finding quality, and optional submission draft preparation. When the changed code matches a domain-specific review scenario, load the matching specialist skill as an additional review lens instead of replacing this workflow.

For OpenHarmony native/C++ system-service security scenarios, use `ohos-dev-security-code-review` alongside this skill when changed code touches IPC dispatch, `MessageParcel`, remote objects, file descriptors, callbacks, `AccessTokenKit`, `IPCSkeleton`, System Ability trust boundaries, privacy-sensitive logging, or shared service state reachable from untrusted callers.

For skill-definition PRs (new or modified `SKILL.md`, `agents/*.yaml`, `evals/*` files in a skills repository like `openharmony-skills`), load `references/reviewing-skill-prs.md` for the specific review dimensions — frontmatter completeness, hard dependency declaration, agent config alignment with skill routing, eval version pinning, and anti-pattern quality.

For skills-repository **sync PRs** (a workflow directory imported from a source repo via a sync script with placeholder/path rewrites), additionally load `references/skill-sync-pr-pitfalls.md` — recurring leftover patterns (old placeholder/path strings, dangling contract `truth_sources`, missing `related-skills`/governance metadata) and the verification recipe that catches them.

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

**Finding exclusions** — Do NOT include findings of these types unless the user explicitly asks for them:
- "命令无法验证" / "Commands cannot be verified from this review context"
- "官方文档链接缺失" / "Missing official documentation links"

The user considers these low-signal noise. Focus on correctness bugs, behavior regressions, broken call-site assumptions, missing or invalid tests, and security/data-handling issues.

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
- Record confirmed findings in `findings.json` using `references/findings-schema.md`
- Produce findings for the user
- If the user wants submission, generate or create a structured draft first

Use `references/findings-schema.md` for review-time issue records. Use `references/review-draft-schema.md` for the final submission draft shape. Use `scripts/prepare_review_submission.py` to convert findings, validate drafts against the collected context, and preview commands.

The draft may include:

- One general PR summary comment
- Zero or more diff comments with `path` and `line`
- Optional approval intent

Approval gate:

- Set `approve: true` only when no blocking or high-severity findings remain and the user explicitly wants approval.
- If the review contains blocking findings, submit comments only; do not call `oh-gc pr review`.

Important: `oh-gc pr review` only supports approval. It is not a general "submit review" endpoint.

For submitted comments, follow the Markdown and Chinese-writing rules in `references/review-draft-schema.md`.

**Pitfall: `oh-gc pr comment` does NOT accept `--comment-type`.** Only `--path` and `--line` are needed for diff-line comments. The flag `--comment-type diff_comment` was previously assumed but is nonexistent and causes exit code 2. Correct syntax:

```bash
oh-gc pr comment <NUMBER> --repo <OWNER/REPO> \
  --path "<file_path>" --line <new_side_line> \
  --body "<comment body>"
```

Do NOT add `--comment-type` to this command — it will fail.

**Pitfall: `summary.json` `commentable_lines` is NOT the ground truth for comment placement.** It lists the entire hunk range (context + added lines), but GitCode only accepts comments on `+` added lines. Always pre-check every target with `verify_diff_lines.py` (from the `cli-agent-delegation` skill) before submitting:

```bash
python3 /root/.hermes/skills/devops/cli-agent-delegation/scripts/verify_diff_lines.py \
  <pr-diff.txt> "path:line" ["path:line" ...]
```

**Pitfall: `verify_diff_lines.py` mis-parses RENAMED files (`status: renamed | +N -M`).** The script reports `MISSING (added X..Y)` even for genuinely added lines when the file is a rename (PR 325 R3: `proposal.md` was `renamed | +22 -14`, lines 4/6/8/9/16 all reported MISSING while line 24 was OK). When the target file is a rename, do not trust the script's verdict — manually open the diff hunk (`grep -n "path b/" pr-diff.txt`, then read the hunk lines) and pick an unambiguous `+` line yourself, then re-verify just that one line. This is also why the FIRST check should include the script's exit code: exit 1 with a mix of OK/MISSING means "recheck the MISSING ones manually", not "trust the output".

If a finding's line is `MISSING` (context line), remap to the nearest added line in the same hunk and mention the real line number in the comment body. If the problem lines are entirely outside any hunk, use a file-level comment (`--path` WITHOUT `--line`). Full rules in `references/codex-delegation-pattern.md` ("Ground truth" section).

**Pitfall: `verify_diff_lines.py` mis-verifies RENAMED files.** When the target file is a rename (`R` status in diff output, e.g. a directory relocation PR), the script can report `MISSING (added N..M)` even for genuinely added `+` lines — it mis-parses the hunk range for renamed entries. Fix: open the file's `diff --git` block directly, count new-side line numbers from the `@@ -a,b +c,d @@` header, and pick an explicit `+` line; confirm by reading the file content at that line. Production case: PR 326 (skill relocation) — `proposal.md:8`/`:16` reported MISSING but `:24` (an added table row) verified OK.

### 6. Submit Only After Confirmation

Never submit to GitCode implicitly.

When the user explicitly asks to submit:

1. Build `findings.json` or `review-draft.json`
2. Run `prepare_review_submission.py` without `--execute` to convert, validate, and preview commands
3. Show the user the exact summary and comment count you plan to post
4. After confirmation, run the same command with `--execute`

If execution fails partway through, report exactly which comments succeeded and which did not.

### 6b. Merge Gate (approve + test + merge)

When the user explicitly authorizes merging ("标记，检视通过，测试通过 并合入" / "合入"), the GitCode gate sequence is three separate commands, all with `--repo OWNER/REPO`:

```bash
oh-gc pr review <N> --repo <OWNER/REPO> --force   # mark review approved  → "Approved PR #N"
oh-gc pr test <N> --repo <OWNER/REPO> --force     # mark test passed      → "Marked PR #N as test passed"
oh-gc pr merge <N> --repo <OWNER/REPO>            # merge                 → "Merged PR #N (<sha>)"
```

Pitfalls:
- **`--force` is required on `pr review` and `pr test` when the operator is not an assigned reviewer/tester of the MR** (e.g. author-self-review flow). Without it: `pr review` → `403 Forbidden - You don't have the authority to approval this merge request`; `pr test` → `400 Must be a tester of this merge request`. With `--force` both succeed. `pr merge` needs no force.
- Merge is a destructive operation — only run it after the user explicitly authorizes the exact target (per `ohos-ci-gitcode-cli-usage` safety rules). A review conclusion of "暂不建议合入 / Request changes" does NOT itself authorize merging; the user deciding to merge anyway is a business decision, not a review outcome.
- Before merging, re-verify head SHA hasn't moved (`oh-gc pr view <N> --json` → `head.sha`). If a new commit landed between your last review and the merge, merging would include unreviewed code — flag it to the user first.
- After merge, confirm `state: merged` in `pr view` output and report the merge commit SHA.
- `oh-gc pr review` only supports approval (it is not a general submit-review endpoint); there is no separate "request changes" API call — that state is conveyed by comments.

### 7. Multi-Round Review & Author Reply

After submitting findings, the PR author may modify the code and request re-review. Handle iterative rounds as follows:

**Eval-runner / grading-script findings recur across rounds — verify against the repo's real schema, not synthetic tests.** When a PR adds or modifies an eval runner, grader, or scoring script (`run_skill_evals.py`, `grading.json`, benchmark manifests), check these explicitly:
- Assertion field names must match the repo's actual `evals.json` schema. PR 325's runner read `assertion["text"]` for `regex` assertions while real evals put the pattern in `pattern` — valid outputs were judged failed. `not_contains` fell back to natural-language `text` instead of explicit `tokens`/`patterns`, so outputs containing `TBD` passed. Verify by running the runner against REAL eval files from the repo (e.g. feed a `flowchart TD` output to a regex eval, a `TBD` output to a not_contains eval), not just its own unit tests.
- Benchmark totals must be conserved: `total = programmatic + manual + unsupported`. A runner that reports `102 total` but `62 + 44 = 106` categories is broken even if unit tests pass.
- A runner that only grades pre-saved text but never executes `prompt`/fixtures is a collector, not an executor — the "eval passed" claim is weaker than it looks.
- New unit tests for the runner often use idealized schemas and miss real-schema mismatches; require at least one end-to-end test that walks the repo's own eval files.

**Re-review (Rounds 2+):**
1. Launch Codex again with a modified prompt that lists all prior findings and their status from the last round.
2. Tell Codex to read PR comments (`oh-gc pr comments NUMBER ... --limit 100`) to see author replies.
3. For each prior finding, label: ✅ 已修复 / ❌ 未修复 / 🔄 部分修复 / ✅ 合理拒绝（仅当作者拒绝理由经规范原文、仓库先例、依赖闭包核实成立后才可判此状态）.
4. Use separate report files (`-r2`, `-r3` suffixes) to preserve history.
5. After re-review, submit line comments **only for findings still marked ❌ or 🔄** — do NOT re-submit already-✅ findings.
6. See `references/codex-delegation-pattern.md#re-review-second-round-pattern` for the exact prompt template.
7. **Before launching ANY re-review round, detect head drift.** Authors frequently push new commits between rounds (and sometimes while a round is still running). Sequence: `oh-gc pr view N --json` → extract head SHA → `git fetch <fork> <branch>:pr<N>-r<round>` → `git diff <prev_head>..<new_head> --stat`. Diff the actual new-commit scope BEFORE assembling the prompt and include it — otherwise Codex re-verifies stale content. Production case (PR 325): five different heads across R1→R4 (`21ad5ca → d3baf91 → 394e545 → f14dd93 → 25a8822`), each round landing a new commit right after the previous round's comments. If the head moves AGAIN mid-round, re-check before submitting comments so they don't attach to a stale version. Note: `oh-gc pr view --json`'s `head.sha` is the ground truth; `pr commits --json` may omit commit messages.

**Re-review (Rounds 4+ — full regression check):**
After several rounds when all previous findings appear fixed, launch a full regression check:
1. List ALL previous findings (from all prior rounds), not just the last round's leftovers.
2. Instruct Codex to check each one for regression (did a subsequent commit undo the fix?).
3. Also check if new commits added since the last review round introduce any new issues.
4. Use a prompt with "确认前几轮的遗留问题是否已全部修复" and "请检查是否因新提交出现了回归" — this distinguishes R4+ from R2/R3 which focus on unfixed items only.
5. Submit comments only for any regression or new issue found; if all clean, report that the PR is ready to merge.

**Replying to author comments:**
- Read existing PR comments (`oh-gc pr comments NUMBER --comment-type pr_comment`) to find the author's responses. If JSON mode times out, pipe to a file first: `oh-gc pr comments NUMBER --repo OWNER/REPO --comment-type pr_comment > /tmp/comments.txt && cat /tmp/comments.txt`.
- When the author disputes a finding with incorrect reasoning (e.g., confusing two different code paths or functions with similar names in different files), address the specific confusion with code-level evidence — do not repeat the original finding verbatim.
- Post replies as new PR-level comments via `oh-gc pr comment NUMBER --body "$(cat /tmp/reply.md)"` (write body to a temp file first to avoid shell escaping issues).
- In the reply, reference the specific file, line, and function name so the author can locate the exact code.

**Pitfall: author says "no fix needed" but is wrong.** When the author responds that a finding doesn't need changes, verify by checking whether they are looking at the correct function or file. Example from production: the author claimed `_find_profiles_dir()` was already fixed because `ohos_sdd_engine.py` (with `../profiles`) was correct, but the actual issue was in `ohos_sdd_spec_for_test.py` (a different `_find_profiles_dir()` without `../profiles`). Always cross-reference the specific line and function name from your finding against the actual file content before accepting "no fix needed."

**Pitfall: author blanket-fix claims are NOT evidence.** When the author replies with a PR-level comment like "已按评论区意见完成一轮修复，提交 `<sha>`" without per-comment replies, do NOT treat the claim as fixing anything. Launch the next round as a normal re-review and verify each prior finding against head code, one by one. Production example (PR 325 R3/R4): author claimed "已按评论区意见完成一轮修复" but per-finding verification found 6 of 8 prior findings still unfixed and 2 new high-severity issues introduced. A blanket claim without line-level evidence changes nothing.

**Pitfall: head drifts between rounds AND during a review.** Authors on iterative PRs often push a new fix commit (a) after our comments land, and (b) WHILE Codex is still running. Consequences:
- When the user says "作者更新了，再检视一下", first diff the new head against the reviewed head (`git fetch <fork> <branch>:pr<N>-rX && git log --oneline <old>..pr<N>-rX`) to scope what changed, then pass that range to Codex — do not re-review blind.
- After Codex finishes, re-check the PR head SHA before submitting comments. If it moved again (author pushed mid-review), your findings may reference stale lines; re-collect context against the newest head before submitting. PR 325 R3 launched against `394e545` but Codex finished against `f14dd93` — the report must note which head was actually reviewed.
- Report files accumulate per round (`-r2`, `-r3`, `-r4` suffixes) AND the findings list grows: keep a running table of ALL findings across rounds with per-round status (✅/❌/🔄/合理拒绝), and in R4+ check regressions across the whole table, not just last round's leftovers.

## Quick Flow

Use these commands only as a compact reminder after reading the workflow above.

Run `collect_pr_context.py` from the local checkout of the repository being reviewed so it can infer `OWNER/REPO` from that checkout's GitCode remote and write `.review-gitcode-pr` artifacts beside the code you will inspect. If you run it from another directory, pass `--repo OWNER/REPO` and `--out-dir PATH` explicitly.

The example below assumes the skill directory is available through `$SKILL_DIR` and the current working directory is the repository being reviewed.

```bash
python3 "$SKILL_DIR/scripts/collect_pr_context.py" 123
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
python3 "$SKILL_DIR/scripts/prepare_review_submission.py" \
  --context-dir .review-gitcode-pr/pr-123 \
  --findings findings.json \
  --write-draft review-draft.json
```

Preview an existing draft submission:

```bash
python3 "$SKILL_DIR/scripts/prepare_review_submission.py" \
  --context-dir .review-gitcode-pr/pr-123 \
  --draft review-draft.json
```

Execute only after explicit user confirmation:

```bash
python3 "$SKILL_DIR/scripts/prepare_review_submission.py" \
  --context-dir .review-gitcode-pr/pr-123 \
  --draft review-draft.json \
  --execute
```

## Delegating to Codex (OpenAI CLI)

When the user requires Codex for code review (user-enforced policy), the entire workflow — context collection, diff analysis, local code inspection, and finding production — must run inside a single `codex exec` invocation. **Do NOT pre-collect PR context before delegating; let Codex handle everything including `oh-gc` fetches and `collect_pr_context.py`.**

### How to invoke Codex

Codex CLI does **not** support the ACP (`--acp --stdio`) protocol that `delegate_task` uses. Using `acp_command=codex` will silently fail (the agent falls back to its own model and times out). The correct method is `terminal()`:

```bash
# Background (parallel PRs, preferred for multiple reviews):
codex exec --dangerously-bypass-approvals-and-sandbox -m gpt-5.6-sol \
  -C /root/work/<repo> \
  -o /tmp/codex-pr-<NUMBER>-report.md \
  '<prompt>'

# Foreground (single PR):
codex exec --dangerously-bypass-approvals-and-sandbox -m gpt-5.6-sol \
  -C /root/work/<repo> \
  '<prompt>'
```

Key flags:
- `--skip-git-repo-check` — always include; Codex may refuse to run in repos with dirty state or detached HEAD
- `--dangerously-bypass-approvals-and-sandbox` — required for non-interactive automation
- `-C <dir>` — set working directory to the repo checkout
- `-o <file>` — write final summary to a file
- **Do NOT append `2>/dev/null`** — it hides the `apply patch` section in process logs that contains the full report

For parallel reviews, use `terminal(background=True, notify_on_complete=True)` for each PR, then use `process(action="wait")` or wait for notifications.

### Prompt structure for Codex

The prompt must be self-contained (Codex runs in a fresh context with no conversation history). Include:

1. **Skill file paths** — Codex can read local files. Reference skill files by absolute path: `/root/.hermes/skills/common/development/ohos-dev-gitcode-pr-review/SKILL.md` etc.
2. **Step-by-step instructions** — `oh-gc` commands to run, files to read, depth expectations, output format.
3. **Output format spec** — severity | path:line | problem | evidence | fix, in Chinese unless otherwise specified.
4. **Report output instruction** — tell Codex to write the full report to the `-o` target file.

### Retrieving Codex output

**Important:** The `-o` file often contains only a short summary. The full detailed report is in Codex's stdout captured by the process tool. To get it:

```bash
# The -o file has just the summary:
read_file /tmp/codex-pr-19638-report.md

# The full report is in process logs — look for the "apply patch" section
# which contains the full report content that Codex wrote to the file:
process(action="log", session_id="<proc_id>", limit=500, offset=<start>)
```

**Pitfall: do NOT launch codex with `| tail -N` and do NOT trust the `-o` file as the full report.** When the process log is truncated or `-o` contains only the summary (Codex overwrites `-o` at the end with its final message), recover the FULL report from the Codex session JSONL: the `apply_patch` tool call that wrote the report file is preserved verbatim in `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Find the `response_item` with `payload.type == 'custom_tool_call'` whose `input` contains `*** Begin Patch`, regex out the content between `*** Begin Patch\n` and `\n*** End Patch`, then unescape `\n` → newline. See `references/codex-delegation-pattern.md` (section "Recovering the full report from the Codex session JSONL") for the exact script. Worked in production: PR 316's report was truncated by `| tail -80` and recovered this way.

### Submitting Codex findings to GitCode

After Codex completes, submit comments using exact diff-side line numbers from `summary.json`:

1. Codex usually generates context via `collect_pr_context.py` — check for `/tmp/codex-pr-<NUMBER>-context/summary.json`
2. Extract `commentable_lines` for the target file from summary.json
3. Match Codex's reported findings to the nearest commentable line
4. Submit via `oh-gc pr comment`:

```bash
oh-gc pr comment <PR_NUMBER> --repo <OWNER/REPO> \
  --path "<file_path>" --line <new_side_line> \
  --body "<comment in Chinese>"
```

### Pitfall: do NOT use delegate_task for Codex

`delegate_task(acp_command="codex")` does not work. Codex is not ACP-compatible. Use `terminal()` directly.

For concrete prompt templates, parallel launch commands, report retrieval, and comment submission commands, see `references/codex-delegation-pattern.md`.

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

- Blocker: `pr diff --json` changes shape, omits hunks, or cannot be parsed reliably enough for structured line mapping.
- Fallback: use `pr-diff.txt` as the source of truth for diff reasoning. Only emit line comments when a new-side line can still be verified confidently from raw diff text; otherwise fall back to file-level or general comments.
- Next step: tell the user that structured diff parsing degraded and that submission precision may be reduced until the JSON format is fixed.

### Submission preview or execute failure

- Blocker: `prepare_review_submission.py` validation fails, preview commands do not match the draft, or `--execute` fails for some comments.
- Fallback: keep the validated draft and any successful partial submission results. Do not silently retry with changed semantics.
- Next step: report the exact failed comment or command, which comments were already posted, and what must be corrected before retrying.
