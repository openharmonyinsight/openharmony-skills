---
name: odk-link-issue
description: "Use when binding a GitCode/issue ID to an existing draft change directory (links to `issue-<number>-<slug>`). Zero plugin dependencies."
license: MIT
---

# ODK Link Issue

## Input

- **Issue number** (required) — the issue ID from GitCode or other source code platform
- **Slug** (optional) — the short slug of the draft directory to link. Required when multiple draft directories exist.

## Prerequisites

- At least one `draft-*` directory exists under `.codespec/changes/`
- If no slug is provided and multiple drafts exist, list them and ask the user to specify

## Steps

1. Find directories matching `draft-*` under `.codespec/changes/`. If slug is provided, match `draft-*-<slug>` exactly. If no slug, there must be exactly one draft directory.
2. Extract the slug from the matched draft directory name (the part after `draft-<yyyymmdd>-`)
3. Rename using filesystem `mv`: `draft-<yyyymmdd>-<slug>/` → `issue-<id>-<slug>/`
4. Stage the rename: `git add` the new path and `git rm --cached` the old path (if previously tracked)
5. Update `proposal.md` frontmatter: set `issue: "<id>"`
6. If optional `evidence/gates/` notes exist, append `Issue linked: #<id> on <date>` to the relevant note. Do not create gate files by default.

## Output

Confirm the rename and frontmatter update to the user:

```
Renamed: draft-20260522-arkui-focus/ → issue-12345-arkui-focus/
Updated: proposal.md frontmatter issue = "12345"
```
