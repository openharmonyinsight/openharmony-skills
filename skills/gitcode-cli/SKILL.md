---
name: gitcode-cli
description: Use when managing GitCode repositories from the terminal with oh-gc CLI — auth, issues, PRs, reviewers, testers, labels, releases, and repo config. Triggers on oh-gc commands, GitCode issue/PR management, or when user wants to interact with GitCode without a browser.
---

# oh-gc CLI — GitCode Command Line Tool

`oh-gc` is a CLI for [GitCode](https://gitcode.com), modeled after GitHub CLI (`gh`). Manages authentication, issues, pull requests, releases, and repo configuration from the terminal.

**Package:** `npm install -g @oh-gc/cli` (requires Node.js 18+)

## Prerequisites

Before using any command:

1. **Token configured?** Run `oh-gc auth:status`
   - If not logged in → `oh-gc auth:login` (prompts for GitCode personal access token)
   - Token obtained at: GitCode → 个人设置 → 访问令牌
2. **Inside a GitCode repo?** Current directory must be a git repo with a `gitcode.com` remote
   - If remote is not `origin` → `oh-gc repo:set-remote <remote-name>`

## Global Flags

All commands support:
- `--json` — output raw JSON instead of formatted table
- `--help` — show command help

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
```

Remote override stored at `.gitcode/oh-gc-config.json` in repo root.

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
  ↓ No → cd to repo, or oh-gc repo:set-remote <name>
  ↓ Yes
What does user want?
  ├─ List/view issues      → oh-gc issue:list / issue:view
  ├─ Create issue           → oh-gc issue:create
  ├─ Comment on issue       → oh-gc issue:comment
  ├─ List/view PRs          → oh-gc pr:list / pr:view
  ├─ Create PR              → oh-gc pr:create
  ├─ Update PR              → oh-gc pr:update
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
- Interactive mode (no flags) prompts for required fields — useful for one-off operations
- `oh-gc pr:comments --comment-type diff_comment` filters to only code review comments
- `oh-gc pr:reviewers --append` adds reviewers without replacing existing ones
- `oh-gc pr:update --state closed` is the way to close a PR without merging
