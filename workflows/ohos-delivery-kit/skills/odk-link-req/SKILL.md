---
name: odk-link-req
description: "Use when a requirement ID must be bound to an existing draft ODK change directory. Zero plugin dependencies."
license: MIT
---

# ODK Link Requirement

## Input

- **Requirement ID** (required) — a requirement identifier matching `^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$`; `issue-<digits>` (case-insensitive) is reserved legacy input and must be rejected
- **Slug** (optional) — the short slug used to narrow draft candidates. It must identify exactly one draft directory.

## Prerequisites

- At least one eligible draft directory exists under `codespec/changes/`
- The optional slug is not a tie-breaker: a matching draft must still be unique.

## Steps

1. Validate the requirement ID against the approved regex above. Reject `issue-<digits>` explicitly; do not offer an issue-linking compatibility path. Validate both the supplied and extracted slug against `^[a-z0-9]+(?:-[a-z0-9]+)*$` and a maximum length of 40.
2. Collect all `draft-*` directory candidates under `codespec/changes/`, then retain only eligible candidates: each must be an immediate child matching `draft-[0-9]{8}-<valid-slug>`, have an extracted slug that passes the slug rule, and contain a readable `proposal.md` with valid first-line YAML frontmatter with exactly one empty `req:` field. Exclude a candidate with a nonempty `req:`, including `req: draft-YYYYMMDD`.
3. If a slug is provided, filter eligible candidates by the exact extracted slug. Require exactly one candidate after optional filtering. Zero matches: report that no draft matches and stop. Multiple matches: list every candidate, ask the user to disambiguate, and stop. Never select newest or first.
4. Resolve the selected draft as `$old_path` and its target as `$new_path`. Record whether `$old_path` has any tracked files before any rename with `git ls-files -- "$old_path"`; retain that result for staging. Preflight proposal readability and writeability, exact `req:` replacement feasibility, optional `evidence/gates/define.md` writeability, and rollback snapshots. Include proposal and optional define gate content in the rollback snapshots. When `$old_path` and `$new_path` differ, preflight target nonexistence before `mv`.
5. When `$old_path == $new_path`, skip target nonexistence and `mv`; the draft-shaped requirement ID is valid and linking is a content-only update. Otherwise rename using filesystem `mv`: `$old_path` → `$new_path`. Update `$new_path/proposal.md` YAML frontmatter by replacing the exactly one empty `req:` value with `req: "<id>"`, preserving all other frontmatter and body content. If `evidence/gates/define.md` exists, append `Requirement linked: <req> on YYYY-MM-DD` before staging; do not create it. Complete all filesystem, frontmatter, and optional evidence updates before staging.
6. On any content update failure, restore proposal and define gate content from snapshots; if a rename occurred, then rename the directory back. Report the failure and do not stage or claim a successful link.
7. Record the pre-existing cached path list. Stage only the completed rename and updates according to the pre-`mv` tracked-path result: Previously tracked old path: `git add -A -- "$old_path" "$new_path"`. Untracked old path: `git add -A -- "$new_path"` only. Verify that newly staged paths are only under `$old_path` or `$new_path`. If staging fails, report it, leave the working tree recoverable, and do not claim success.

## Output

Confirm the actual path outcome and frontmatter update to the user. For a renamed path, report `Renamed:`:

```
Renamed: codespec/changes/draft-20260522-arkui-focus/ → codespec/changes/REQ-12345-arkui-focus/
Updated: codespec/changes/REQ-12345-arkui-focus/proposal.md frontmatter req = "REQ-12345"
```

For `$old_path == $new_path`, report `Linked in place:` and do not claim a rename:

```
Linked in place: codespec/changes/draft-20260522-arkui-focus/
Updated: codespec/changes/draft-20260522-arkui-focus/proposal.md frontmatter req = "draft-20260522"
```

If no unique draft can be selected, report the matching candidates and request a disambiguating slug; do not rename or stage any directory.

If preflight, content update, or staging fails, report the failed step and the recoverable state; do not report the requirement as linked.
