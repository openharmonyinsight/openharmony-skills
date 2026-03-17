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
argument-hint: "[commit|pr|fix-codecheck|review <PR_URL>] [--issue N] [--target branch]"
---

# oh-pr-workflow: OpenHarmony PR Lifecycle Workflow

Unified workflow for OpenHarmony GitCode repositories. Five modes:
- **Commit only**: user says "提交", "commit" → commit with standardized message, stop
- **Full PR**: user says "创建PR", "提个PR" → commit (if needed) + push + Issue + PR
- **Fix Codecheck**: user says "修复告警", "修复门禁", "修复codecheck" or provides a PR URL → fetch gate codecheck defects and auto-fix
- **Review PR**: user says "review pr", "检视pr", "看下这个pr" + PR URL → fetch PR changes to local for review
- **Fix Review**: user says "修复review", "修复检视意见", "fix review" + PR URL → fetch unresolved review comments and auto-fix

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

See `references/commit-format.md` for full spec. Summary:

```
type(scope): 描述（≤49字符）

Issue: https://gitcode.com/{owner}/{repo}/issues/{number}
Signed-off-by: Name <email>
Co-Authored-By: Agent
```

## Remote Detection

Never assume remote names. Parse all remotes:

```bash
git remote -v
```

Classify by owner:
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
  No changes → inform user, stop

Step 2: Resolve email
  Follow Email Resolution above

Step 3: Determine Issue
  Follow Issue Detection above (target_branch defaults to master)

Step 4: Generate commit message
  - Title: ≤49 chars, Claude generates from diff or user provides
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
  No changes → skip

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
  Read .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md from repo
  Fill template:
    - 关联的Issue: #{issue_number}
    - 修改原因: summarized from commit messages
    - 修改描述: file change summary from git diff --stat
    - Checklist: intelligently check items based on change scope
  MCP create_pull_request:
    owner: {upstream_owner}
    repo: {upstream_repo}
    title: same as first commit title or summarized
    head: {fork_owner}:{current_branch}
    base: {target_branch}
    body: filled template content
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
  Fetch PR comments via API (MCP list_pr_comments or direct curl):
    GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
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

Step 3: Fetch all PR comments and filter review comments
  Fetch via API:
    GET /repos/{owner}/{repo}/pulls/{pull_number}/comments?per_page=100
  Filter for:
    - comment_type == "diff_comment" (line-level review comments)
    - resolved == false (unresolved only)
  Extract from each:
    - user.login: reviewer name
    - body: review comment content
    - diff_position.start_new_line / end_new_line: original diff line number
    - discussion_id: for grouping replies

  Outdated detection (after force-push, diff line numbers shift):
    Get current PR diff via list_pr_files, extract the new-file lines from patch.
    For each review comment, compare its diff_position line against the current
    diff's content at that same line number:
      - Content matches → comment is still ACTIVE
      - Content differs or line out of range → comment is OUTDATED
    Present outdated comments separately (greyed out) so user can confirm skipping.

Step 4: Get PR changed files for context
  MCP list_pr_files(owner, repo, pull_number)
    → file list with patches, to map line numbers to actual file paths

Step 5: Present review comments and proposed fixes to user
  Group comments into ACTIVE and OUTDATED based on Step 3 outdated detection.

  For OUTDATED comments:
    Show as "~~已过期~~" with original content, no fix proposed.

  For ACTIVE comments:
    - Reviewer: {user.login}
    - Comment: {body}
    - Location: search current code for the function/variable mentioned in comment
    - Proposed fix: Claude reads the file, analyzes the comment, shows before/after diff

  *** HARD GATE: STOP HERE AND WAIT FOR USER CONFIRMATION ***
  Do NOT proceed to Step 6 until the user explicitly confirms.
  Present all proposed fixes and ask: "以上修复方案是否可以执行？"
  User may:
    - Confirm all → proceed to Step 6
    - Confirm some, reject others → adjust and re-present
    - Reject all → stop

Step 6: Apply confirmed fixes
  Only apply fixes the user confirmed:
    a. Read the target file
    b. Apply the fix at the indicated line
    c. Edit the file

Step 7: Squash into original commit and push
  IMPORTANT: Always squash fix into original commit, never create separate commit.
    git add {fixed files}
    git commit --amend --no-edit
    git push --force {fork_remote} {branch}

Step 8: Trigger rebuild
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
- **Commit title > 49 chars**: Claude auto-shortens
- **No changes to commit**: skip commit in PR mode, stop in commit mode
- **Email not found**: prompt user to configure git email or GitCode token

## GitCode MCP Tools Used

- `get_authenticated_user` — get current user email for Signed-off-by
- `create_issue` — create Issue on upstream repo
- `get_issue` — validate user-specified Issue exists
- `list_pull_requests` — check for existing PR
- `create_pull_request` — create PR from fork to upstream
- `list_pr_comments` — get PR comments (Mode 3: Fix Codecheck)
- `get_pull_request` — get PR details including head.ref, head.sha, head.repo, base.ref, base.sha
- `list_pr_commits` — list exact commits in a PR
- `list_pr_files` — list exact changed files in a PR with additions/deletions/patch
- `create_pr_comment` — post comment on PR (used to trigger gate CI with "start build")
