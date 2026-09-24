---
name: odk-link-proposal
description: "Use when a proposal ID must be bound to an existing draft ODK change directory. Zero plugin dependencies."
license: MIT
---

# ODK Link Proposal

## Input

- **Proposal ID** (required) — a proposal identifier matching `^[0-9]+$`; formal IDs contain digits only, with no fixed length
- **Slug** (optional) — the short slug used to narrow draft candidates. It must identify exactly one draft directory.

## Prerequisites

- At least one eligible draft directory exists under `codespec/changes/<repo-name>/`
- The optional slug is not a tie-breaker: a matching draft must still be unique.
- Exclude drafts containing legacy identity fields, even alongside an empty
  `proposal_id`. Require identity-field migration and conflict resolution before
  selecting, renaming, editing or staging such a draft; never silently discard an
  old identifier. This applies to quoted and indented keys as well as bare keys.

## Steps

1. Validate the proposal ID against the approved digits-only regex above. Validate both the supplied and extracted slug against `^[a-z0-9]+(?:-[a-z0-9]+)*$` and a maximum length of 40.
2. Resolve `<repo-name>` from the Git `origin` URL basename without `.git`; if unavailable, use the Git worktree root directory name. Collect all `draft-*` directory candidates under `codespec/changes/<repo-name>/`, then retain only eligible candidates: each must be an immediate child matching `draft-[0-9]{8}-<valid-slug>`, have an extracted slug that passes the slug rule, and contain a readable `proposal.md` with valid first-line YAML frontmatter with exactly one empty `proposal_id:` field. Exclude a candidate with a nonempty `proposal_id:`, including `proposal_id: draft-YYYYMMDD`.
3. If a slug is provided, filter eligible candidates by the exact extracted slug. Require exactly one candidate after optional filtering. Zero matches: report that no draft matches and stop. Multiple matches: list every candidate, ask the user to disambiguate, and stop. Never select newest or first.
4. Resolve the selected draft as `$old_path` and its target `codespec/changes/<repo-name>/<proposal-id>/` as `$new_path`; the formal numeric path always differs from the draft path and intentionally drops the draft slug. Record whether `$old_path` has any tracked files before any rename with `git ls-files -- "$old_path"`; retain that result for staging. Preflight target nonexistence, proposal readability and writeability, exact `proposal_id:` replacement feasibility, optional `evidence/gates/define.md` writeability, and rollback snapshots. Include proposal and optional define gate content in the rollback snapshots.
5. Rename using filesystem `mv`: `$old_path` → `$new_path`. Update `$new_path/proposal.md` YAML frontmatter by replacing the exactly one empty `proposal_id:` value with `proposal_id: "<id>"`, preserving all other frontmatter and body content. If `evidence/gates/define.md` exists, append `Proposal linked: <proposal-id> on YYYY-MM-DD` before staging; do not create it. Complete all filesystem, frontmatter, and optional evidence updates before staging.
6. On any content update failure, restore proposal and define gate content from snapshots, then rename the directory back. Report the failure and do not stage or claim a successful link.
7. Record the pre-existing cached path list. Stage only the completed rename and updates according to the pre-`mv` tracked-path result: Previously tracked old path: `git add -A -- "$old_path" "$new_path"`. Untracked old path: `git add -A -- "$new_path"` only. Verify that newly staged paths are only under `$old_path` or `$new_path`. If staging fails, report it, leave the working tree recoverable, and do not claim success.

## Output

Confirm the actual path outcome and frontmatter update to the user. Report `Renamed:`:

```
Renamed: codespec/changes/arkui/draft-20260522-arkui-focus/ → codespec/changes/arkui/12345/
Updated: codespec/changes/arkui/12345/proposal.md frontmatter proposal_id = "12345"
```

If no unique draft can be selected, report the matching candidates and request a disambiguating slug; do not rename or stage any directory.

If preflight, content update, or staging fails, report the failed step and the recoverable state; do not report the proposal as linked.
