---
name: ohos-ci-gitcode-cli-usage
description: Use when managing GitCode repositories from the terminal with oh-gc CLI. Triggers on GitCode issue or pull request work, oh-gc commands, creating or reviewing PRs, assigning reviewers or testers, managing labels, releases, repository settings, or when the user wants GitCode operations without a browser.
metadata:
  author: openharmony
  scope: common
  stage: cicd
  domain: gitcode
  capability: cli-usage
  version: 0.1.0
  status: draft
  tags:
    - gitcode
    - oh-gc
    - cli
    - pr
    - issue
---

# oh-gc CLI - GitCode Command Line Tool

Use this skill to operate GitCode from the terminal with `oh-gc`.

`oh-gc` version covered by these references: greater than `0.7.4`.

Package: `npm install -g @oh-gc/cli@latest` with Node.js 18+.

## Mandatory First Step

Run this before any other `oh-gc` command:

```bash
oh-gc --version
```

If `oh-gc` is missing or the version is not greater than `0.7.4`, install or update it first:

```bash
npm install -g @oh-gc/cli@latest
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
| Issue or PR operations: auth, repository flag, reviewer, tester, label, comment, diff, merge, and troubleshooting | Read `references/common-issue-pr-commands.md` only. Do NOT load `extended-commands.md` or `gitcode-pr-workflow.md`. |
| Low-frequency operations: release, repository configuration, search, user, branch, commit, file, collaborator, milestone, webhook, tag, or organization | Read `references/extended-commands.md` only. Do NOT load `gitcode-pr-workflow.md`. |
| Full local-to-upstream PR automation: commit local changes, push a fork branch, create required Issue, and open upstream PR | Read `references/gitcode-pr-workflow.md`; also read `references/common-issue-pr-commands.md` only if command syntax details are needed. |
| Repo discovery (search by partial name, explore user/org repos) | Read `references/extended-commands.md` → "Repo Discovery Tips" section. Use `--json` + Python filtering — `oh-gc search repos` often fails. |
| Adding/removing repo collaborators, checking permission levels | Read `references/extended-commands.md` → "Collaborators" section. **Critical: `--permission admin` grants Maintainer(40), NOT Owner(50)** — there is no oh-gc flag reaching Owner level; `collaborator list` also mislabels non-Owners as `none`. See the Collaborators pitfalls. |
| Repo directory hygiene / merge planning (numbered report repos, e.g. ai-code-harness-7.0) | Read `references/repo-hygiene-merge-planning.md`. |
| Skills-repo relocation / misplaced-skill fixes (openharmony-skills structure moves, website yaml registration, frontmatter YAML block scalar) | Read `references/skill-relocation-workflow.md`. |

## Default Workflow

For most requests:

1. Run `oh-gc --version` and confirm it is greater than `0.7.4`.
2. Run `oh-gc auth status`.
3. Determine repository context, using `--repo owner/repo` when not inside the target clone.
4. Read the minimum reference file from the table above.
5. Do not load low-frequency references for routine Issue/PR tasks.
6. When a needed command or flag is unfamiliar, run the command with `--help` first and prefer the live CLI help over memory.
7. Prefer `--json` when output will be parsed or summarized.

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

## Never Do

NEVER skip `oh-gc --version`; command syntax and behavior depend on the CLI version.

NEVER run `oh-gc auth`, `oh-gc issue`, `oh-gc pr`, or any mutating command before confirming the version is greater than `0.7.4`.

NEVER print, persist, commit, or echo a remote URL containing a token such as `https://user:token@gitcode.com/...`. Use token-free remote URLs and `oh-gc auth login` or config-based authentication instead.

NEVER use `owner/branch` for cross-repo PR `--head`; GitCode expects `owner:branch`.

NEVER report a PR URL with `/pulls/`; GitCode uses singular `/pull/`.

NEVER merge, close, delete, archive, transfer, force approve, force test, or reset all assignees unless the user explicitly authorized that exact target and operation.

## PR Creation & Merge Workflow Pitfalls

**Pitfall: `--body` with backticks/`$()` gets shell-expanded.** When creating or updating a PR with a markdown body containing backtick-wrapped paths or `$(...)`, the shell interprets them BEFORE `oh-gc` sees them — backtick paths become commands (e.g. `skills/foo/` → "No such file or directory") and the body is silently truncated. Fix: write the body to a temp file with `write_file`, then pass `--body "$(cat /tmp/body.md)"`. The same applies to `oh-gc pr update N --body` when correcting a mangled body. Verified on PR 326: inline body lost all backtick paths; temp-file body preserved them.

**Pitfall: `git add -A` / `git add skills/` sweeps untracked `__pycache__/*.pyc` into the commit.** In repos with untracked build artifacts (e.g. `skills/review-gitcode-pr/scripts/__pycache__/`), a broad `git add` commits them. This happened twice in one session (PR 326). Fix: after staging, check `git show --stat HEAD | grep -c pycache` == 0; if a commit already contains them, `git rm --cached` + `git commit --amend` (or `git reset --soft` + re-commit) before pushing. Prefer `git add <specific files>` over `git add -A`.

**Pitfall: `oh-gc pr diff` has no `--stat` flag.** `oh-gc pr diff N --stat` fails with `Nonexistent flag: --stat` (verified on 0.8.2). Only `--json`, `--name-only`, `--color`, `--token`, `--repo` exist. For per-file change stats, fetch the head locally (`git fetch <fork-url> <branch>:prN-head`) and run `git diff <base>..prN-head --stat` / `--numstat`.

**Merge approval sequence (GitCode):** `oh-gc pr review N` (marks approved) → `oh-gc pr test N` (marks test passed) → `oh-gc pr merge N`. User's "标记，检视通过，测试通过 并合入" maps 1:1 to this sequence. Verify after merge: `oh-gc pr view N --json` → `state: merged`.

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

**Before documenting a workaround for unexpected CLI behavior**, check for a newer CLI version first: `npm view @oh-gc/cli version`, upgrade with `npm install -g @oh-gc/cli@latest`, then re-test. Record the versions the workaround was verified on (e.g. `verified on 0.7.4 and 0.8.2`). Example: `oh-gc org list` returns `No organizations found (API endpoint may not be available)` on both 0.7.4 and 0.8.2 — the workaround `oh-gc user orgs <username>` is still required.
