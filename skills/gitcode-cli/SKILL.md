---
name: gitcode-cli
description: Use when managing GitCode repositories from the terminal with oh-gc CLI — auth, issues, PRs, reviewers, testers, labels, releases, and repo config. TRIGGERS on: oh-gc commands, GitCode issue/PR management, "提交pr", "提交PR", "生成pr", "生成PR", "创建pr", "创建PR", "提交并生成pr", "提交并生成PR", "commit and create PR", "push and create PR", "创建一笔pr", "创建一笔PR", or when user wants to interact with GitCode without a browser.
---

# oh-gc CLI — GitCode Command Line Tool

`oh-gc` is a CLI for [GitCode](https://gitcode.com), modeled after GitHub CLI (`gh`). Manages authentication, issues, pull requests, releases, and repo configuration from the terminal.

**Package:** `npm install -g @oh-gc/cli` (requires Node.js 18+)

## Rules

When executing gitcode-cli operations, follow these rules:

1. **"当前改动"定义**: 当用户说"当前的改动"、"当前文件的改动"时，指的是**当前文件所在 git 仓库的改动**，使用 `git status` 和 `git diff` 查看。

2. **Remote 命名规范**:
   | Remote 名称 | 用途 |
   |-------------|------|
   | `gitcode` | 上游原始仓库 |
   | `personal` | 个人 Fork 仓库 |

3. **Fork 地址自动拼接**: 如果 `personal` remote 不存在，根据 `gitcode` remote 自动拼接：
   ```bash
   UPSTREAM_URL=$(git remote get-url gitcode)
   REPO_NAME=$(echo "$UPSTREAM_URL" | sed -E 's|.*/([^/]+/[^/]+)(\.git)?|\1|')
   PERSONAL_URL="https://${USERNAME}:${TOKEN}@gitcode.com/${USERNAME}/${REPO_NAME#*/}.git"
   ```

4. **Commit Message 格式** (DCO 标准):
   ```
   具体的改动说明

   Co-Authored-By:Agent

   Signed-off-by: 用户名 <邮箱>
   ```

## Prerequisites

Before using any command:

1. **Token configured?** Run `oh-gc auth:status`
   - If not logged in → `oh-gc auth:login` (prompts for GitCode personal access token)
   - Token obtained at: GitCode → 个人设置 → 访问令牌
2. **Repository context?** Either:
   - Inside a git repo with a `gitcode.com` remote (remote name configurable via `oh-gc repo:set-remote <name>`), OR
   - Use `--repo owner/repo` flag to specify any repository

## Global Flags

All commands support:
- `--json` — output raw JSON instead of formatted table
- `--help` — show command help

## Repository Flag

Most commands that operate on a repository support the `--repo` flag, which allows specifying a target repository without being inside a git clone:

- `--repo owner/repo` — target repository in OWNER/REPO format

This is useful for:
- Operating on repositories you haven't cloned locally
- Cross-repo operations (e.g., creating a PR from fork to upstream)
- CI/CD scripts that need to interact with multiple repositories

```bash
# List issues in any repository
oh-gc issue:list --repo openharmony/arkui_ace_engine

# Create an issue without cloning
oh-gc issue:create --repo owner/repo --title "Bug report"

# View a PR on another repo
oh-gc pr:view 123 --repo owner/repo

# Cross-repo PR (fork to upstream)
oh-gc pr:create --repo upstream-owner/repo --head my-feature --base main
```

## Command Reference

### Authentication

```bash
oh-gc auth:login          # Log in with personal access token (interactive prompt)
oh-gc auth:logout         # Remove stored token
oh-gc auth:status         # Show current user info
```

Token stored at `~/.config/gitcode-cli/config.json`.

### Issues

```bash
# List
oh-gc issue:list                              # Open issues (default)
oh-gc issue:list --state closed               # Closed issues
oh-gc issue:list --state all                  # All issues
oh-gc issue:list --assignee alice             # Filter by assignee
oh-gc issue:list --search "login bug"         # Search by keyword
oh-gc issue:list --limit 50                   # Max results (default: 30)

# View
oh-gc issue:view 12                           # Show issue detail + recent comments

# Create
oh-gc issue:create                            # Interactive mode
oh-gc issue:create --title "Bug" --body "..."         # With flags
oh-gc issue:create --repo owner/repo --title "Bug"    # On another repo
oh-gc issue:create --assignee alice --labels "bug,P0" # With metadata

# Comment
oh-gc issue:comment 12                        # Interactive prompt
oh-gc issue:comment 12 --body "Confirmed"     # With flag

# Close/Reopen
oh-gc issue:close 12                          # Close an issue
oh-gc issue:reopen 12                         # Reopen a closed issue

# Labels
oh-gc issue:labels 12 bug,feature             # Add labels
oh-gc issue:labels 12 bug --remove            # Remove label
```

### Pull Requests

```bash
# List
oh-gc pr:list                                 # Open PRs (default)
oh-gc pr:list --state merged                  # Merged PRs
oh-gc pr:list --state all                     # All PRs
oh-gc pr:list --author alice                  # Filter by author
oh-gc pr:list --reviewer bob                  # Filter by reviewer
oh-gc pr:list --assignee carol                # Filter by assignee
oh-gc pr:list --limit 50                      # Max results (default: 30)

# View
oh-gc pr:view 5                               # Show PR detail

# Create
oh-gc pr:create                               # Interactive mode
oh-gc pr:create --title "Fix bug" --base main         # From current branch
oh-gc pr:create --head feature --base main --draft    # Draft PR
oh-gc pr:create --repo owner/repo --head my-feature   # Cross-repo PR

# Update
oh-gc pr:update 5 --title "New title"         # Update title
oh-gc pr:update 5 --body "New description"    # Update body
oh-gc pr:update 5 --state closed              # Close PR
oh-gc pr:update 5 --state open                # Reopen PR
oh-gc pr:update 5 --draft                     # Mark as draft
oh-gc pr:update 5 --labels "bug,wip"          # Set labels

# Close/Reopen
oh-gc pr:close 5                              # Close a PR
oh-gc pr:reopen 5                             # Reopen a closed PR

# Diff
oh-gc pr:diff 5                               # Show full diff with colors
oh-gc pr:diff 5 --name-only                   # Only changed file names
oh-gc pr:diff 5 --color never                 # No color (for piping)

# Merge
oh-gc pr:merge 5                              # Merge commit (default)
oh-gc pr:merge 5 --method squash              # Squash merge
oh-gc pr:merge 5 --method rebase              # Rebase merge

# Comment
oh-gc pr:comment 5 --body "LGTM!"                                    # General comment
oh-gc pr:comment 5 --body "Fix this" --path src/main.ts --line 10    # Line comment
oh-gc pr:comment 5 --repo owner/repo --body "Note"                   # On another repo

# List/delete comments
oh-gc pr:comments 5                                   # List all comments
oh-gc pr:comments 5 --comment-type diff_comment       # Only diff/line comments
oh-gc pr:comments 5 --comment-type pr_comment         # Only general comments
oh-gc pr:comments 5 --delete 12345                    # Delete by note_id

# Commits
oh-gc pr:commits 5                            # List commits in PR

# Reviewers
oh-gc pr:reviewers 5 alice,bob                # Assign reviewers
oh-gc pr:reviewers 5 alice --append           # Add to existing reviewers
oh-gc pr:reviewers 5 alice --remove           # Remove reviewer

# Testers
oh-gc pr:testers 5 alice,bob                  # Assign testers
oh-gc pr:testers 5 alice --append             # Add to existing testers
oh-gc pr:testers 5 alice --remove             # Remove tester

# Review & Test approval
oh-gc pr:review 5                             # Approve PR review
oh-gc pr:review 5 --force                     # Force approve
oh-gc pr:test 5                               # Mark test passed
oh-gc pr:test 5 --force                       # Force mark

# Labels
oh-gc pr:labels 5 bug,enhancement             # Add labels
oh-gc pr:labels 5 bug --remove                # Remove label

# Link issues
oh-gc pr:link 5 1,2,3                         # Link issues to PR
oh-gc pr:link 5 1,2 --remove                  # Unlink issues

# Operation logs
oh-gc pr:logs 5                               # Show PR operation history
```

### Releases

```bash
oh-gc release:create                          # Use version from package.json
oh-gc release:create v1.0.0                   # Specific version
oh-gc release:create --prerelease             # Mark as prerelease
oh-gc release:create v1.0.0 --notes "..."     # Custom release notes
```

### Repo Configuration

```bash
oh-gc repo:get-remote                         # Show which remote oh-gc uses
oh-gc repo:set-remote upstream                # Use a different remote
oh-gc repo:view                               # View repository info
oh-gc repo:update --description "..."         # Update repository settings
oh-gc repo:transfer <new-owner>               # Transfer repository ownership
```

Remote override stored at `.gitcode/oh-gc-config.json` in repo root.

### Search

```bash
oh-gc search:repos "keyword"                  # Search repositories
oh-gc search:issues "keyword"                 # Search issues across repos
oh-gc search:code "keyword"                   # Search code across repos
```

### User

```bash
oh-gc user:view                               # View your profile
oh-gc user:view alice                         # View another user's profile
oh-gc user:emails                             # List your email addresses
oh-gc user:followers                          # List your followers
oh-gc user:following                          # List users you follow
```

### Branches

```bash
oh-gc branch:list                             # List all branches
oh-gc branch:list --protected                 # List only protected branches
oh-gc branch:get <name>                       # Get branch details
oh-gc branch:protect <name>                   # Set branch protection rules
```

### Commits

```bash
oh-gc commit:list                             # List commits
oh-gc commit:list --sha main                  # List commits from specific branch
oh-gc commit:get <sha>                        # Get commit details
oh-gc commit:diff <sha>                       # View commit diff
oh-gc commit:compare <base> <head>            # Compare two commits or branches
```

### Files

```bash
oh-gc file:get <path>                         # Get file contents (base64 encoded)
oh-gc file:raw <path> --ref main              # Get raw file contents
oh-gc file:list                               # List repository files
```

### Collaborators

```bash
oh-gc collaborator:list                       # List repository collaborators
oh-gc collaborator:add <username>             # Add a collaborator
oh-gc collaborator:remove <username>          # Remove a collaborator
oh-gc collaborator:permission <username>      # Get collaborator permission level
```

### Labels

```bash
oh-gc label:list                              # List repository labels
oh-gc label:get <name>                        # Get label details
oh-gc label:create                            # Create a new label
oh-gc label:update <name>                     # Update a label
oh-gc label:delete <name>                     # Delete a label
```

### Milestones

```bash
oh-gc milestone:list                          # List milestones
oh-gc milestone:get <number>                  # Get milestone details
oh-gc milestone:create                        # Create a new milestone
oh-gc milestone:update <number>               # Update a milestone
oh-gc milestone:delete <number>               # Delete a milestone
```

### Webhooks

```bash
oh-gc hook:list                               # List repository webhooks
oh-gc hook:get <id>                           # Get webhook details
oh-gc hook:create                             # Create a webhook
oh-gc hook:delete <id>                        # Delete a webhook
```

### Tags

```bash
oh-gc tag:list                                # List repository tags
oh-gc tag:protect <name>                      # Protect a tag
```

### Organizations

```bash
oh-gc org:list                                # List your organizations
oh-gc org:view <org>                          # Get organization details
oh-gc org:members <org>                       # List organization members
oh-gc org:repos <org>                         # List organization repositories
```

## Workflow: Full PR Lifecycle

Complete workflow from code change to merged PR:

```
Step 1: Create PR
  oh-gc pr:create --title "Add feature X" --base main
  → outputs PR number (e.g., #42)

Step 2: Assign people
  oh-gc pr:reviewers 42 alice,bob
  oh-gc pr:testers 42 carol

Step 3: Add metadata
  oh-gc pr:labels 42 feature,v2.0
  oh-gc pr:link 42 15,16           # Link related issues

Step 4: Review cycle
  oh-gc pr:diff 42                 # Reviewer checks diff
  oh-gc pr:comments 42             # Check existing feedback
  oh-gc pr:comment 42 --body "LGTM"
  oh-gc pr:review 42               # Approve review
  oh-gc pr:test 42                 # Mark test passed

Step 5: Merge
  oh-gc pr:merge 42 --method squash
```

## Workflow: Issue Triage

```
Step 1: Find issues
  oh-gc issue:list --search "crash"
  oh-gc issue:list --state all --assignee alice

Step 2: Inspect
  oh-gc issue:view 15

Step 3: Respond
  oh-gc issue:comment 15 --body "Investigating, likely related to #12"

Step 4: Create follow-up
  oh-gc issue:create --title "Fix crash on login" --labels "bug,P0" --assignee bob
```

## Workflow: Cross-Repo PR (Fork → Upstream)

For contributing to repositories you don't own:

```
Step 1: Create PR from fork to upstream
  oh-gc pr:create --repo upstream-owner/repo --head my-feature --base master --title "Fix bug"

Step 2: Manage on the upstream repo
  oh-gc pr:view 42 --json    # Check status
```

Note: `--repo` flag targets the upstream repo. The `--head` branch is resolved from your fork.

## Configuration

| Setting | Location | How to set |
|---------|----------|------------|
| Auth token | `~/.config/gitcode-cli/config.json` | `oh-gc auth:login` |
| Remote override | `.gitcode/oh-gc-config.json` | `oh-gc repo:set-remote <name>` |
| Proxy | `https_proxy` / `HTTPS_PROXY` env var | Automatic |

## Decision Tree

```
User wants to interact with GitCode
  ↓
Logged in? (oh-gc auth:status)
  ↓ No → oh-gc auth:login
  ↓ Yes
Inside git repo with gitcode.com remote?
  ↓ No → Use --repo flag, or cd to repo
  ↓ Yes
What does user want?
  ├─ List/view issues      → oh-gc issue:list / issue:view
  ├─ Create issue           → oh-gc issue:create
  ├─ Update issue           → oh-gc issue:update
  ├─ Close/reopen issue     → oh-gc issue:close / issue:reopen
  ├─ Comment on issue       → oh-gc issue:comment
  ├─ Manage issue labels    → oh-gc issue:labels
  ├─ List/view PRs          → oh-gc pr:list / pr:view
  ├─ Create PR              → oh-gc pr:create
  ├─ Update PR              → oh-gc pr:update
  ├─ Close/reopen PR        → oh-gc pr:close / pr:reopen
  ├─ Review PR diff         → oh-gc pr:diff
  ├─ Comment on PR          → oh-gc pr:comment (general) or --path --line (line-level)
  ├─ Assign reviewers       → oh-gc pr:reviewers
  ├─ Assign testers         → oh-gc pr:testers
  ├─ Approve review         → oh-gc pr:review
  ├─ Mark test passed       → oh-gc pr:test
  ├─ Manage labels          → oh-gc pr:labels
  ├─ Link issues to PR      → oh-gc pr:link
  ├─ Merge PR               → oh-gc pr:merge
  ├─ View PR history        → oh-gc pr:logs
  ├─ Create release         → oh-gc release:create
  ├─ Search repos/issues    → oh-gc search:repos / search:issues / search:code
  ├─ View user profile      → oh-gc user:view
  ├─ Manage branches        → oh-gc branch:list / branch:get / branch:protect
  ├─ View commits/files     → oh-gc commit:list / file:get
  ├─ Manage collaborators   → oh-gc collaborator:list / add / remove
  ├─ Manage labels          → oh-gc label:list / create / update / delete
  ├─ Manage milestones      → oh-gc milestone:list / create / update
  ├─ Manage webhooks        → oh-gc hook:list / create / delete
  └─ Configure remote       → oh-gc repo:set-remote / repo:get-remote
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "Not logged in" | No token configured | `oh-gc auth:login` |
| "Authentication failed" | Token expired or invalid | Re-run `oh-gc auth:login` with new token |
| "Remote not found" | Not in a git repo or remote missing | `cd` to repo, check `git remote -v` |
| "Not a GitCode repository" | Remote URL isn't `gitcode.com` | Add a gitcode.com remote |
| "Could not connect" | Network issue or proxy not set | Check internet; set `https_proxy` env var if behind proxy |
| "Rate limit exceeded" | Too many API calls | Wait and retry |
| "API error 405" | Wrong HTTP method (internal) | Update oh-gc to latest version |

## Tips

- Use `--json` to pipe output to `jq` for scripting: `oh-gc pr:list --json | jq '.[].title'`
- Use `--repo owner/repo` to operate on any repository without cloning it first
- Interactive mode (no flags) prompts for required fields — useful for one-off operations
- `oh-gc pr:comments --comment-type diff_comment` filters to only code review comments
- `oh-gc pr:reviewers --append` adds reviewers without replacing existing ones
- `oh-gc pr:update --state closed` is the way to close a PR without merging
