# Common Issue and PR Commands

Use this reference for the GitCode operations most agents need day to day: auth, repository selection, issues, pull requests, reviewers, testers, labels, comments, and basic troubleshooting.

## Global Flags

All commands support:

```bash
--json   # output raw JSON instead of formatted table
--help   # show command help
```

## Repository Flag

Most repository commands support:

```bash
--repo owner/repo
```

Use `--repo` when operating outside a clone, across repositories, or from automation.

```bash
oh-gc issue list --repo openharmony/arkui_ace_engine
oh-gc issue create --repo owner/repo --title "Bug report"
oh-gc pr view 123 --repo owner/repo
oh-gc pr create --repo upstream-owner/repo --head myname:my-feature --base main
```

For fork-to-upstream PRs, `--repo` targets the upstream repository and `--head` uses `owner:branch`.

## Authentication

```bash
oh-gc auth login          # Log in with personal access token
oh-gc auth logout         # Remove stored token
oh-gc auth status         # Show current user info
```

Token storage: `~/.config/gitcode-cli/config.json`.

## Issues

```bash
# List
oh-gc issue list
oh-gc issue list --state closed
oh-gc issue list --state all
oh-gc issue list --assignee alice
oh-gc issue list --search "login bug"
oh-gc issue list --limit 50

# View
oh-gc issue view 12

# Create
oh-gc issue create
oh-gc issue create --title "Bug" --body "..."
oh-gc issue create --repo owner/repo --title "Bug"
oh-gc issue create --assignee alice --labels "bug,P0"

# Comment
oh-gc issue comment 12
oh-gc issue comment 12 --body "Confirmed"

# Close/Reopen
oh-gc issue close 12
oh-gc issue reopen 12

# Labels
oh-gc issue labels 12 bug,feature
oh-gc issue labels 12 bug --remove

# History and reactions
oh-gc issue history 12
oh-gc issue reactions 12

# Linked PRs and branches
oh-gc issue prs 12
oh-gc issue prs 12 --mode 1
oh-gc issue branches 12
oh-gc issue branches 12 --set feature-x,fix-y

# Comment management
oh-gc issue comment-get <id>
oh-gc issue comment-edit <id> --body "new"
oh-gc issue comment-delete <id>
oh-gc issue comment-history <id>
oh-gc issue comment-reactions <id>
```

## Pull Requests

```bash
# List
oh-gc pr list
oh-gc pr list --state merged
oh-gc pr list --state all
oh-gc pr list --author alice
oh-gc pr list --reviewer bob
oh-gc pr list --assignee carol
oh-gc pr list --limit 50

# View
oh-gc pr view 5

# Create
oh-gc pr create
oh-gc pr create --title "Fix bug" --base main
oh-gc pr create --head feature --base main --draft
oh-gc pr create --repo owner/repo --head myname:feature

# Update
oh-gc pr update 5 --title "New title"
oh-gc pr update 5 --body "New description"
oh-gc pr update 5 --state closed
oh-gc pr update 5 --state open
oh-gc pr update 5 --draft
oh-gc pr update 5 --labels "bug,wip"

# Close/Reopen
oh-gc pr close 5
oh-gc pr reopen 5

# Diff
oh-gc pr diff 5
oh-gc pr diff 5 --name-only
oh-gc pr diff 5 --color never

# Merge
oh-gc pr merge 5
oh-gc pr merge 5 --method squash
oh-gc pr merge 5 --method rebase

# Comment
oh-gc pr comment 5 --body "LGTM!"
oh-gc pr comment 5 --body "Fix this" --path src/main.ts --line 10
oh-gc pr comment 5 --repo owner/repo --body "Note"

# List/delete comments
oh-gc pr comments 5
oh-gc pr comments 5 --limit 10 --latest
oh-gc pr comments 5 --full-body
oh-gc pr comments 5 --comment-type diff_comment
oh-gc pr comments 5 --comment-type pr_comment
oh-gc pr comments 5 --delete 12345

# Reactions and commits
oh-gc pr reactions 5
oh-gc pr commits 5

# Reviewers
oh-gc pr reviewers 5 alice,bob
oh-gc pr reviewers 5 alice --append
oh-gc pr reviewers 5 alice --remove

# Testers
oh-gc pr testers 5 alice,bob
oh-gc pr testers 5 alice --append
oh-gc pr testers 5 alice --remove

# Review and test approval
oh-gc pr review 5
oh-gc pr review 5 --force
oh-gc pr test 5
oh-gc pr test 5 --force

# Labels
oh-gc pr labels 5 bug,enhancement
oh-gc pr labels 5 bug --remove
oh-gc pr labels 5 bug,feature --replace

# Link issues
oh-gc pr link 5 1,2,3
oh-gc pr link 5 1,2 --remove

# Operation logs, files, history, linked issues
oh-gc pr logs 5
oh-gc pr files 5
oh-gc pr history 5
oh-gc pr linked-issues 5

# Assignees
oh-gc pr assignees 5 --add alice,bob
oh-gc pr assignees 5 --reset
oh-gc pr assignees 5 --reset --all
oh-gc pr assignees 5 --remove alice

# PR settings and eligible reviewers
oh-gc pr settings
oh-gc pr settings-update --merge-method squash --delete-branch-on-merge
oh-gc pr option-reviewers 5

# Comment management
oh-gc pr comment-get <id>
oh-gc pr comment-edit <id> --body "new"
oh-gc pr comment-delete <id>
oh-gc pr comment-history <id>
oh-gc pr comment-reactions <id>
```

## Full PR Lifecycle

```text
Step 1: Create PR
  oh-gc pr create --title "Add feature X" --base main

Step 2: Assign people
  oh-gc pr reviewers 42 alice,bob
  oh-gc pr testers 42 carol

Step 3: Add metadata
  oh-gc pr labels 42 feature,v2.0
  oh-gc pr link 42 15,16

Step 4: Review cycle
  oh-gc pr diff 42
  oh-gc pr comments 42
  oh-gc pr comment 42 --body "LGTM"
  oh-gc pr review 42
  oh-gc pr test 42

Step 5: Merge
  oh-gc pr merge 42 --method squash
```

## Issue Triage

```text
Step 1: Find issues
  oh-gc issue list --search "crash"
  oh-gc issue list --state all --assignee alice

Step 2: Inspect
  oh-gc issue view 15

Step 3: Respond
  oh-gc issue comment 15 --body "Investigating, likely related to #12"

Step 4: Create follow-up
  oh-gc issue create --title "Fix crash on login" --labels "bug,P0" --assignee bob
```

## Cross-Repo PR

```bash
oh-gc pr create \
  --repo upstream-owner/repo \
  --head myname:my-feature \
  --base master \
  --title "Fix bug"
```

Use `owner:branch` for `--head`. Do not use `owner/branch`.

## Configuration

| Setting | Location | How to set |
| --- | --- | --- |
| Auth token | `~/.config/gitcode-cli/config.json` | `oh-gc auth login` |
| Remote override | `.gitcode/oh-gc-config.json` | `oh-gc repo set-remote <name>` |
| Proxy | `https_proxy` / `HTTPS_PROXY` | Automatic |

## URL Format

Use these URL forms when reporting links:

```text
Issue: https://gitcode.com/{owner}/{repo}/issues/{number}
PR:    https://gitcode.com/{owner}/{repo}/pull/{number}
```

GitCode PR URLs use singular `pull`, not `pulls`.

## Tips

- Use `--json` for parsed output: `oh-gc pr list --json | jq '.[].title'`.
- Use `--repo owner/repo` to operate without cloning.
- Use interactive mode when flags are omitted.
- Use `oh-gc pr comments --comment-type diff_comment` for code review comments.
- Use `oh-gc pr reviewers --append` to add reviewers without replacing existing reviewers.
- Use `oh-gc pr update --state closed` to close a PR without merging.
