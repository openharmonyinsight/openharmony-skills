---
name: oh-pr-workflow
description: |
  OpenHarmony PR full lifecycle workflow. Five modes:
  - Commit: standardized commit with DCO sign-off and Issue linking
  - Create PR: commit + push to fork + create Issue + create PR on upstream
  - Fix Codecheck: fetch gate CI codecheck defects from a PR and auto-fix them
  - Review PR: fetch a PR's changes to local for code review
  - Fix Review: fetch unresolved review comments from a PR and auto-fix them
  Triggers on: /oh-pr-workflow, "提交代码", "创建PR", "提个PR", "commit",
  "修复告警", "修复门禁", "修复codecheck", "fix codecheck",
  "review pr", "review这个pr", "看下这个pr", "检视pr",
  "修复review", "修复检视意见", "fix review",
  or a GitCode PR URL with fix/review intent.
argument-hint: "[commit|pr|fix-codecheck|review|fix-review <PR_URL>] [--issue N] [--target branch]"
---

# oh-pr-workflow: OpenHarmony PR Lifecycle Workflow

Unified workflow for OpenHarmony GitCode repositories. Five modes:
- **Commit only**: user says "提交", "commit" → commit with standardized message, stop
- **Full PR**: user says "创建PR", "提个PR" → commit (if needed) + push + Issue + PR
- **Fix Codecheck**: user says "修复告警", "修复门禁", "修复codecheck" or provides a PR URL → fetch gate codecheck defects and auto-fix
- **Review PR**: user says "review pr", "检视pr", "看下这个pr" + PR URL → fetch PR changes to local for review
- **Fix Review**: user says "修复review", "修复检视意见", "fix review" + PR URL → fetch unresolved review comments and auto-fix

## Mode Selection (Quick Reference)

| User Intent | Mode | Skip to |
|---|---|---|
| "提交", "commit" | **Mode 1: Commit Only** | [Mode 1](#mode-1-commit-only) |
| "创建PR", "提个PR" | **Mode 2: Full PR** | [Mode 2](#mode-2-full-pr) |
| "修复告警", "修复门禁", "fix codecheck" + PR URL | **Mode 3: Fix Codecheck** | [Mode 3](#mode-3-fix-codecheck) |
| "review pr", "检视pr" + PR URL | **Mode 4: Review PR** | [Mode 4](#mode-4-review-pr) |
| "修复review", "fix review" + PR URL | **Mode 5: Fix Review** | [Mode 5](#mode-5-fix-review) |

After identifying the mode, verify prerequisites below, then jump directly to the relevant mode section.

**Prerequisite**: Before executing any mode:
1. GitCode Token must be configured. Check: `git config --get gitcode.token`
   If empty → inform user:
   "请先配置 GitCode 个人访问令牌：git config --global gitcode.token YOUR_TOKEN
    令牌获取：GitCode 个人设置 → 访问令牌 → 创建（需要 api 和 read_api 权限）"
   Stop execution.
2. Check if `get_authenticated_user` MCP tool is available (ToolSearch "get_authenticated_user")
   If NOT available → run setup automatically:
   ```bash
   bash ~/.claude/skills/oh-pr-workflow/gitcode-mcp/setup.sh
   ```
   Then inform user: "GitCode MCP 已自动安装，请重启 Claude Code 会话以加载新工具。"
   Stop execution (new session needed for MCP tools to load).
3. Both checks pass → proceed with the workflow.

## Scope

This workflow applies to ALL GitCode repository submissions, not just the current
working directory. When submitting to a different repo (e.g., cloning a separate
repo to /tmp for a PR), the same rules MUST be followed:
- Commit message format (type(scope): title + Issue + Signed-off-by + Co-Authored-By)
- Issue must exist BEFORE writing it into commit message (create if needed)
- Never reference an Issue URL without first verifying or creating it via API

## Commit Message Format

See `references/commit-format.md` for full spec (format, types, rules, examples).

**HARD LIMIT**: The first line (title) of the commit message MUST NOT exceed 49 characters
(including `type(scope): ` prefix). Count characters BEFORE committing. If over 49, shorten it.
Example: `fix(aptool): add ABC metadata checks` (37 chars) ✓
Counter-example: `fix(aptool): add defensive checks for ABC metadata lookup` (58 chars) ✗

## Remote Detection

Never assume remote names. Run `git remote -v` and classify by owner:
- `openharmony` → **UPSTREAM** (PR target, Issue creation)
- Other → **FORK** (push target, PR head)

Both must exist. Missing fork → prompt user. Ambiguous → ask user to select.

## Email Resolution

Get email for `Signed-off-by` line. Priority:

1. **Memory cache**: check if `user_gitcode_email.md` exists in auto-memory. If found, use `email` field directly.
2. **MCP API**: call `get_authenticated_user` tool (no parameters). Extract `email` field. Save to memory as `user_gitcode_email.md` with type `user`.
3. **Git config**: `git config user.email` as fallback.
4. **None**: prompt user to configure.

## Issue Detection

Determines which Issue to use for commit message and PR. Shared by both modes.

**Input**: user may specify `--issue N` or `--issue URL`.

**Algorithm**:
1. User specified Issue → validate with `get_issue`, use if valid
2. Scan `git log {upstream_remote}/{target_branch}..HEAD` for existing Issue URLs
   - Regex: `Issue:\s*https://gitcode\.com/[^/]+/[^/]+/issues/(\d+)`
   - If found → reuse the **earliest** match
3. Not found → auto-create via `create_issue` on upstream repo
   - Title: derived from branch name or commit diff
   - Body: use `references/issue_template.md`, fill from git diff context

**Issue URL format**: `https://gitcode.com/{upstream_owner}/{upstream_repo}/issues/{number}`

## Mode 1: Commit Only

Trigger: user wants to commit without creating PR.

```
Step 1: Check uncommitted changes
  git status --porcelain

Step 2: Resolve email
  Follow Email Resolution above

Step 3: Determine Issue
  Follow Issue Detection above (target_branch defaults to master)

Step 4: Generate commit message
  - Title: MUST be ≤49 chars (count before committing!), Claude generates from diff or user provides
  - Body: Issue URL + Signed-off-by + Co-Authored-By: Agent

Step 5: Stage files
  a. Identify files to commit:
     - Files that Claude created or modified in this session → always include
     - Other changed files in working tree → need user confirmation
  b. Filter out files that should NEVER be committed:
     Exclude patterns:
       - .idea/*, .vscode/*, .claude/*, .DS_Store
       - .env, .env.*, credentials*, *secret*
       - out/*, build/*, *.o, *.so, *.a, *.pyc, __pycache__/
       - report.json, rules.txt, *.log
       - Any file matched by .gitignore
  c. If there are files beyond what Claude modified:
     Present to user: "以下文件也有变更，是否一起提交？" + file list
     User selects which to include
  d. git add {final file list} — always add specific files by name
     NEVER use "git add ." or "git add -A"

Step 6: Pre-commit codecheck
  If oh-precommit-codecheck skill is available, run it on staged files:
    Invoke: /oh-precommit-codecheck
  If defects found:
    - Present defects to user
    - Ask: "发现代码告警，是否先修复再提交？"
    - User confirms fix → fix defects, re-stage, re-run codecheck
    - User skips → proceed to commit (warn that gate may fail)
  If no defects or skill not available → proceed

Step 7: Commit
  - git commit with formatted message (use HEREDOC for multi-line)
  - Output: commit hash, linked Issue
```

**Commit command template**:
```bash
git commit -m "$(cat <<'EOF'
type(scope): title here

Issue: https://gitcode.com/owner/repo/issues/N
Signed-off-by: Name <email>
Co-Authored-By: Agent
EOF
)"
```

## Mode 2: Full PR

Trigger: user wants to create a PR.

**Input**: `--target branch` (optional, default: `master`)

```
Step 1: Check status & detect remotes
  git status, git remote -v
  Identify upstream and fork
  Determine target branch

Step 2: Handle uncommitted changes
  git status --porcelain
  Has changes → execute Commit Only mode (Steps 2-7)

Step 3: Push to fork
  git push -u {fork_remote} {current_branch}

Step 4: Check existing PR
  MCP list_pull_requests (upstream owner/repo)
  Search results for current branch name
  Found → inform user "PR !{number} already exists", stop
  Not found → continue

Step 5: Determine Issue
  Follow Issue Detection above

Step 6: Create PR
  Read .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md from repo (prioritize repo template if exists)
  Fill template with bilingual content (Chinese + English per item, NOT repeated blocks):
    - Issue: full URL https://gitcode.com/{upstream_owner}/{upstream_repo}/issues/{number}
      (NEVER use #{number} shorthand — always use the full Issue URL)
    - 描述/Description, 原因/Reason, 修改方案/Scheme: write bilingual per item.
      Format each point as "中文 / English" on the same bullet, e.g.:
        - `FindRecordByName` 匹配失败时无日志 / No log output when match fails
      Do NOT write all Chinese first then repeat all English — interleave per item.
    - Checklist: intelligently check items based on change scope
  If no template found in repo, use a simple bilingual structure with Issue URL,
  Description, Reason, Scheme sections.
  MCP create_pull_request:
    owner: {upstream_owner}
    repo: {upstream_repo}
    title: concise summary from commit messages
    head: {fork_owner}:{current_branch}
    base: {target_branch}
    body: filled template content (bilingual)
  Output: PR URL, linked Issue number

Step 7: Trigger gate CI
  After PR is created, post comment to trigger build:
  MCP create_pr_comment:
    owner: {upstream_owner}
    repo: {upstream_repo}
    pull_number: {pr_number from Step 6}
    body: "start build"
  Output: inform user that gate CI has been triggered
```

**Example successful run**:
```
git remote -v → openharmony (upstream), origin (fork)
git status → 2 files changed
→ Commit: fix(napi): add null check [32 chars] ✓
→ Push: origin/fix-null-check
→ Issue: #1985 created on openharmony/arkui_napi
→ PR: !2610 created (zhuheng_z:fix-null-check → master)
→ Comment: "start build" posted, gate CI triggered
```

## Mode 3: Fix Codecheck

Trigger: user says "修复告警", "修复门禁", "修复codecheck", "fix codecheck", or provides a GitCode PR URL asking to fix codecheck issues.

**Input**: A GitCode PR URL like `https://gitcode.com/{owner}/{repo}/pull/{number}`

```
Step 1: Parse PR URL and get PR details
  Extract owner, repo, pull_number from the URL
  Regex: https://gitcode\.com/([^/]+)/([^/]+)/pull/(\d+)
  MCP get_pull_request(owner, repo, pull_number) to get:
    - head.ref: source branch
    - head.sha: head commit SHA
    - head.repo.full_name: fork repo (e.g., "zhuheng_z/arkui_napi")

Step 2: Ensure PR code is checked out locally
  a. Check if head commit exists locally:
       git cat-file -t {head.sha} 2>/dev/null
  b. Check if current branch matches PR branch:
       git branch --show-current == head.ref ?
  c. Decision:
     - Current branch matches AND head SHA matches → code is local, proceed
     - Head SHA exists but wrong branch → git checkout {head.ref}
     - Head SHA not local → fetch and checkout:
         Extract head_owner from head.repo.full_name
         git remote add pr-fix-{head_owner} https://gitcode.com/{head_owner}/{repo}.git 2>/dev/null || true
         git fetch pr-fix-{head_owner} {head.ref}
         git checkout -b fix/pr-{pull_number} FETCH_HEAD
  d. Record original branch for later return

Step 3: Get PR comments and find failed gate check
  MCP list_pr_comments(owner, repo, pull_number, per_page=100)
  Search for the first comment containing "代码门禁未通过"
  If not found → inform user "No failed gate check found", stop

Step 4: Extract CI eventId and taskId from the failed comment body
  ciEventId: regex /detail/([a-f0-9]+)/runlist  (this is the CI event ID)
  taskId:    regex taskId=(MR_[a-f0-9]+)
  date:      extract from comment created_at (YYYY-MM-DD)

Step 5: Get codecheck UUID from CI event info
  IMPORTANT: The defect detail API needs the codecheck UUID, NOT the CI event ID.
  Fetch CI event info:
    GET https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/{ciEventId}
  Extract codecheck UUID from response:
    response.data.codeCheckSummary[0].uuid → this is the codecheckEventId
  Use codecheckEventId (not ciEventId) for the defect API.

Step 6: Fetch all defects
  Run: bash ~/.claude/skills/oh-pr-workflow/scripts/fetch_gate_defects.sh <codecheckEventId> <taskId> <date>
  This auto-paginates and outputs a JSON array to stdout
  Parse the JSON to get the defect list

Step 7: Summarize defects
  Present a summary table to user:
    - Total defect count
    - Breakdown by rule (e.g., G.FMT.11-CPP: 56, G.FMT.04-CPP: 48, ...)
    - Breakdown by file
  Ask user to confirm before proceeding with fixes

Step 8: Auto-fix defects
  For each defective file:
    a. Read the file
    b. For each defect in that file, understand the rule and fix it:
       - G.FMT.04-CPP (one statement per line): split multi-declarations
       - G.FMT.11-CPP (braces): add {} around single-line if/for/while/else
       - G.FMT.05-CPP (line width): break lines over 120 chars
       - G.NAM.03-CPP (naming): rename to match convention
       - G.EXP.35-CPP (nullptr): replace NULL/0 with nullptr
       - G.EXP.41-CPP (loop variable): restructure loop
       - G.FUN.01-CPP (function size): cannot auto-fix, report to user
       - Other rules: read the defectContent, apply best-effort fix
    c. Edit the file with fixes

Step 9: Verify fixes (optional)
  If oh-precommit-codecheck skill is available, run local codecheck on fixed files
  Report any remaining issues
```

## Mode 4: Review PR

Trigger: user says "review pr", "review这个pr", "看下这个pr", "检视pr", or provides a PR URL with review intent.

**Input**: A GitCode PR URL like `https://gitcode.com/{owner}/{repo}/pull/{number}`

```
Step 1: Parse PR URL
  Extract owner, repo, pull_number from the URL
  Regex: https://gitcode\.com/([^/]+)/([^/]+)/pull/(\d+)

Step 2: Get PR details via MCP
  MCP get_pull_request(owner, repo, pull_number)
  From response extract:
    - head.ref: source branch name (e.g., "fix/strdup-free-mismatch")
    - head.sha: head commit SHA
    - head.repo.full_name: fork full name (e.g., "yewei0794/arkui_napi")
    - head.user.login: PR author login
    - base.ref: target branch (e.g., "master")
    - base.sha: base commit SHA
    - title, body, state, labels

Step 3: Get PR commits and files via MCP (precise, no git fetch needed)
  MCP list_pr_commits(owner, repo, pull_number)
    → exact commit list with SHA and message
  MCP list_pr_files(owner, repo, pull_number)
    → exact changed file list with filename, additions, deletions, patch

Step 4: Present PR summary
  - PR title, author, head branch → base branch
  - Commit list (from Step 3)
  - Changed files with +/- stats (from Step 3)

Step 5: Fetch PR code to local
  Always fetch to local so user can browse the code after review:
    a. Record current branch: git branch --show-current
    b. Stash if dirty: git stash (if needed)
    c. Extract head_owner from head.repo (e.g., "yewei0794")
    d. git remote add pr-review-{head_owner} https://gitcode.com/{head_owner}/{repo}.git 2>/dev/null || true
    e. git fetch pr-review-{head_owner} {head.ref}
    f. git checkout -b review/pr-{pull_number} FETCH_HEAD
  Use patch data from Step 3 for the review analysis itself (faster),
  but the local branch ensures user can inspect files afterwards.

Step 6: Perform code review
  For each changed file:
    a. Use patch from list_pr_files for diff analysis
    b. Read full file from local checkout when deeper context is needed
    c. Identify issues: bugs, style, security, performance, logic errors
    d. Present review comments organized by file with line references
  After presenting all review findings, ask the user which comments (if any)
  should be posted as line-level diff comments on the PR.
  If the user confirms specific comments → post them using the Line-Level
  Review Comment API described below.

Step 7: Keep local branch, inform user
  After review, switch back to original branch but DO NOT delete the review branch:
    git checkout {original_branch}
    git stash pop (if stashed)
  Inform user:
    "Review 完成。PR 代码保留在本地分支 review/pr-{pull_number}，你可以随时切换查看。
     清理命令: git branch -D review/pr-{pull_number} && git remote remove pr-review-{head_owner}"
```

## Mode 5: Fix Review

Trigger: user says "修复review", "修复检视意见", "fix review", or provides a PR URL with intent to fix review comments.

**Input**: A GitCode PR URL like `https://gitcode.com/{owner}/{repo}/pull/{number}`

```
Step 1: Parse PR URL and get PR details
  Extract owner, repo, pull_number from the URL
  MCP get_pull_request(owner, repo, pull_number) to get:
    - head.ref, head.sha, head.repo.full_name

Step 2: Ensure PR code is checked out locally
  Same logic as Mode 3 Step 2:
    - Check head SHA exists locally + current branch matches
    - If not → fetch and checkout

Step 3: Fetch diff data and review comments
  a. Get PR changed files with diff hunks (needed for file path mapping):
     MCP list_pr_files(owner, repo, pull_number)
     For each file, parse hunk headers from patch.diff:
       Regex: @@ -(\d+),?(\d*) \+(\d+),?(\d*) @@
     Build a line-to-file mapping:
       For each file, each hunk defines a new_line range:
         new_start to new_start + new_count - 1 → filename

     Worked example:
       A review comment has diff_position.start_new_line = 2650.
       list_pr_files returns ark_native_engine.cpp with hunk header:
         @@ -2638,15 +2640,31 @@
       Parse: new_start=2640, new_count=31 → range is [2640, 2670].
       Check: 2650 falls within [2640, 2670].
       Result: comment maps to ark_native_engine.cpp, line 2650 in the new file.

       If another file utils.cpp has hunk @@ -100,10 +100,12 @@ (range [100, 111]),
       2650 does NOT fall in [100, 111], so utils.cpp is ruled out.

  b. Get review comments:
     MCP list_pr_comments(owner, repo, pull_number, comment_type="diff_comment", per_page=100)
     Filter for unresolved only: resolved == false
     Extract from each:
       - user.login: reviewer name
       - body: review comment content
       - diff_position.start_new_line / end_new_line: line number in new file
       - discussion_id: for grouping replies

  c. Map each comment to its file:
     IMPORTANT: GitCode API does NOT return a `path` field in diff_comment JSON.
     Use the line-to-file mapping from step (a) to determine the file:
       For each comment, find the file whose hunk range contains
       diff_position.start_new_line → that is the file the comment belongs to.

  d. Outdated detection (after force-push, diff line numbers shift):
     For each review comment, compare its diff_position line against the current
     diff's hunk ranges:
       - Line falls within a current hunk range → comment is still ACTIVE
       - Line out of range for all hunks → comment is OUTDATED
     Present outdated comments separately (greyed out) so user can confirm skipping.

Step 4: Present review comments and proposed fixes to user
  Group comments into ACTIVE and OUTDATED based on Step 3(d) outdated detection.

  For OUTDATED comments:
    Show as "~~已过期~~" with original content, no fix proposed.

  For ACTIVE comments:
    - Reviewer: {user.login}
    - File: {mapped filename from Step 3(c)}
    - Line: {diff_position.start_new_line}
    - Comment: {body}
    - Proposed fix: Claude reads the file at that line, analyzes the comment, shows before/after diff

  *** HARD GATE: STOP HERE AND WAIT FOR USER CONFIRMATION ***
  Do NOT proceed to Step 6 until the user explicitly confirms.
  Present all proposed fixes and ask: "以上修复方案是否可以执行？"
  User may:
    - Confirm all → proceed to Step 6
    - Confirm some, reject others → adjust and re-present
    - Reject all → stop

Step 5: Apply confirmed fixes
  Only apply fixes the user confirmed:
    a. Read the target file
    b. Apply the fix at the indicated line
    c. Edit the file

Step 6: Squash into original commit and push
  IMPORTANT: Always squash fix into original commit, never create separate commit.
    git add {fixed files}
    git commit --amend --no-edit

  *** CONFIRM BEFORE FORCE-PUSH ***
  Inform user: "将 squash 进原始 commit 并 force-push 到 {fork_remote}/{branch}。确认？"
  Wait for user confirmation before proceeding. Do NOT force-push without explicit approval.

    git push --force {fork_remote} {branch}

Step 7: Trigger rebuild
  MCP create_pr_comment(owner, repo, pull_number, body="start build")
```

## Error Handling (Mode 5: Fix Review)

- **No unresolved review comments**: inform user "No unresolved review comments found"
- **Review comment unclear**: present the comment to user and ask for guidance
- **File not found locally**: warn and skip
- **Cannot determine fix from comment**: report to user with context for manual fix

## Error Handling (Mode 4: Review PR)

- **PR URL not provided**: ask user for the PR URL
- **PR not found**: inform user, check if PR number is correct
- **head/base fields empty**: fallback to list_pr_commits + list_pr_files for review data
- **Fetch fails**: the PR source fork may be private or deleted; use API patches if available
- **Local repo is different repo**: warn if current repo doesn't match PR's repo
- **Dirty working tree**: warn user about uncommitted changes, suggest stash before switching branches

## Error Handling (Mode 3: Fix Codecheck)

- **PR URL not provided**: ask user for the PR URL
- **No failed gate found**: inform user, suggest checking if gate passed
- **DCP API returns 500**: inform user DCP service may be down, show the eventId/taskId for manual retry
- **Defect in file not in local repo**: warn and skip (PR may be from a different branch/repo)
- **Cannot auto-fix**: report the defect to user with file:line and rule description

## Error Handling (General)

- **MCP not configured**: warn and stop immediately
- **No upstream remote**: prompt user to add openharmony remote
- **No fork remote**: prompt user to fork the repo
- **PR already exists**: only push, inform user with PR number
- **Issue creation fails**: warn, continue with commit (Issue line omitted)
- **Push fails**: show error, suggest checking remote/permissions
- **Commit message title > 49 chars**: MUST shorten before committing — this is a HARD LIMIT (applies to commit message title only, NOT PR title). Always count characters including the `type(scope): ` prefix before running git commit
- **No changes to commit**: skip commit in PR mode, stop in commit mode
- **Email not found**: prompt user to configure git email or GitCode token

## Common Mistakes (Anti-Patterns)

These are critical errors that have caused real failures. NEVER make these mistakes:

1. **NEVER confuse ciEventId with codecheckEventId** (Mode 3)
   The defect detail API needs the UUID from `codeCheckSummary[0].uuid`, NOT the CI event ID extracted from the gate comment URL. The CI event ID (from `/detail/{id}/runlist`) is only used to *fetch* the codecheck summary — the actual defect query requires the `uuid` field returned inside `codeCheckSummary`.

2. **NEVER use best-effort fix for rules you do not recognize** (Mode 3)
   If a codecheck rule is not listed in Step 8's known rules (G.FMT.04-CPP, G.FMT.11-CPP, etc.), do NOT attempt a speculative fix. Instead, report the defect to the user with the rule ID, file:line, and defectContent so they can decide how to handle it.

3. **NEVER assume diff_position.start_new_line is a global offset** (Mode 5)
   `diff_position.start_new_line` is a line number within the specific file's new version, not a global position across all files. You MUST use the line-to-file mapping from `list_pr_files` hunk headers to determine which file the line belongs to.

4. **NEVER force-push without user confirmation** (Mode 5)
   `git push --force` is destructive. Always show the user what will be pushed and to where, then wait for explicit confirmation.

5. **NEVER create a separate commit for review fixes** (Mode 5)
   Review fixes must always be squashed into the original commit via `git commit --amend --no-edit`. Creating a new commit pollutes the PR history and may violate upstream merge policies.

## GitCode MCP Tools Used

> **Note**: This section is a reference catalog. You do not need to read it during normal execution — the specific MCP tools to call are listed inline within each mode's steps above.

**Core workflow tools:**
- `get_authenticated_user` — get current user email for Signed-off-by
- `create_issue` — create Issue on upstream repo
- `get_issue` — validate user-specified Issue exists
- `list_pull_requests` — check for existing PR
- `create_pull_request` — create PR from fork to upstream
- `get_pull_request` — get PR details (head.ref, head.sha, head.repo, base.ref, base.sha)
- `list_pr_commits` — list exact commits in a PR
- `list_pr_files` — list changed files with additions/deletions/patch
- `list_pr_comments` — list PR comments with optional comment_type filter (diff_comment/pr_comment)
- `create_pr_comment` — post comment on PR (general or line-level with path+position)
- `delete_pr_comment` — delete a PR comment by note_id

**Additional tools available:**
- `update_pull_request` — update PR title/body/state/base
- `merge_pull_request` — merge PR (merge/squash/rebase)
- `submit_pr_review` — approve PR review
- `submit_pr_test` — mark PR test passed
- `update_pr_reviewers` — assign reviewers
- `update_pr_testers` — assign testers
- `update_pr_labels` — add/remove PR labels
- `pr_link_issues` — link issues to PR
- `list_pr_operation_logs` — PR operation history
- `update_issue` / `close_issue` / `reopen_issue` — issue state management
- `add_issue_comment` / `list_issue_comments` / `edit_issue_comment` / `delete_issue_comment` — issue comments
- `add_issue_labels` / `remove_issue_label` / `list_labels` — label management
- `list_pr_reactions` / `create_pr_reaction` — PR emoji reactions
- `list_issue_reactions` / `create_issue_reaction` — issue emoji reactions
- `create_release` — create repository release

## Line-Level Review Comment

The MCP `create_pr_comment` tool supports both general and line-level comments:

**General comment**: `create_pr_comment(owner, repo, pull_number, body="...")`
**Line-level comment**: `create_pr_comment(owner, repo, pull_number, body="...", path="file.cpp", position=N)`

**Determining `position`**:
- `position` is the line number in the **unified diff**, NOT the file line number.
- For **new files** (100% addition): diff line number == file line number.
- For **modified files**: count lines sequentially within the file's unified diff
  (the `@@` header line is not counted; first content line after `@@` is position 1;
  positions are cumulative across all hunks in the file).
- Use the `patch` field from `list_pr_files` to compute the correct position.

**Deleting a comment**: `delete_pr_comment(owner, repo, comment_id=NOTE_ID)`
