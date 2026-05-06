---
name: ohos-ci-gitcode-cli
description: Use when managing GitCode repositories from the terminal with oh-gc CLI. Triggers on GitCode issue or pull request work, oh-gc commands, creating or reviewing PRs, assigning reviewers or testers, managing labels, releases, repository settings, or when the user wants GitCode operations without a browser.
---

# oh-gc CLI - GitCode Command Line Tool

Use this skill to operate GitCode from the terminal with `oh-gc`.

`oh-gc` version covered by these references: `0.7.4`.

Package: `npm install -g @oh-gc/cli` with Node.js 18+.

## Mandatory First Step

Run this before any other `oh-gc` command:

```bash
oh-gc --version
```

If `oh-gc` is missing or the version is not `0.7.4`, install the exact version first:

```bash
npm install -g @oh-gc/cli@0.7.4
```

Do not run `oh-gc auth`, `oh-gc issue`, `oh-gc pr`, or any mutating command until the version is confirmed.

## Setup Checks

After the version check:

1. Check login state with `oh-gc auth status`.
2. If not logged in, run `oh-gc auth login`.
3. Confirm repository context:
   - Prefer running inside a git repository with a `gitcode.com` remote.
   - Otherwise use `--repo owner/repo`.

Token storage: `~/.config/gitcode-cli/config.json`.

Remote override storage: `.gitcode/oh-gc-config.json`.

## Reference Selection

Load references only when needed:

| Need | Read |
| --- | --- |
| Common auth, repository flag, Issue, PR, reviewer, tester, label, comment, merge, and troubleshooting commands | `references/common-issue-pr-commands.md` |
| Less common release, repository configuration, search, user, branch, commit, file, collaborator, milestone, webhook, tag, and organization commands | `references/extended-commands.md` |
| Full GitCode PR automation from local changes to fork push and upstream PR | `references/gitcode-pr-workflow.md` |

## Default Workflow

For most requests:

1. Run `oh-gc --version` and enforce `0.7.4`.
2. Run `oh-gc auth status`.
3. Determine repository context, using `--repo owner/repo` when not inside the target clone.
4. Read `references/common-issue-pr-commands.md` for Issue/PR tasks.
5. Read `references/extended-commands.md` only when the request involves low-frequency command groups.
6. Prefer `--json` when output will be parsed or summarized.

## Common Decisions

Use Issue commands when the user wants to list, inspect, create, comment on, close, reopen, label, or link issues.

Use PR commands when the user wants to list, inspect, create, update, close, reopen, diff, comment, assign reviewers or testers, approve review, mark tests, label, link issues, or merge pull requests.

Use `--repo owner/repo` when the current directory is not the target repository or when operating cross-repo.

For fork-to-upstream PRs, use `--repo upstream-owner/repo` and `--head fork-owner:branch`. Do not use `fork-owner/branch`.

When reporting GitCode PR links, use:

```text
https://gitcode.com/{owner}/{repo}/pull/{number}
```

Use singular `pull`, not `pulls`.

## Safety Rules

Before mutating remote state, state the target repository and object number or branch in your own working notes.

For destructive operations such as delete, close, archive, transfer, force approval, merge, or resetting assignees, make sure the user request clearly authorizes the operation. If the target is ambiguous, ask a concise clarification.

Do not expose tokens. Prefer `oh-gc auth login` or environment variables over embedding tokens in commands. If a remote URL contains a token, do not print it back to the user.

## Error Handling

Common errors:

| Error | Likely cause | Fix |
| --- | --- | --- |
| `Not logged in` | No token configured | Run `oh-gc auth login` |
| `Authentication failed` | Token expired or invalid | Re-run `oh-gc auth login` with a new token |
| `Remote not found` | Not in a git repo or remote missing | Use `--repo owner/repo`, or inspect `git remote -v` |
| `Not a GitCode repository` | Remote URL is not `gitcode.com` | Add or select a GitCode remote |
| `Could not connect` | Network or proxy issue | Check network and `https_proxy` / `HTTPS_PROXY` |
| `Rate limit exceeded` | Too many API calls | Wait and retry |
| `API error 405` | CLI/API mismatch | Confirm `oh-gc` version and update if needed |
| `Can not find the branch` | Cross-repo `--head` format is wrong | Use `owner:branch` |
