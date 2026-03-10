---
name: graphic-2d-PR
description: The complete workflow for creating a pull request in the OpenHarmony graphic_graphic_2d repository, including creating an issue, linking them, and pushing to the fork.
---

## Prerequisites

- Git remotes configured (use `git remote -v` to check):
  - upstream repository (openharmony/graphic_graphic_2d)
  - user's fork (username/graphic_graphic_2d)
- Gitcode MCP tools available (if not installed, install from [this repo](https://gitcode.com/gitcode-ai/gitcode_mcp_server))
- Build passes successfully

## Workflow

### 1. Stage and Commit Changes

```bash
# Reset any staged changes and stage everything together
git reset HEAD .
git add .
git status

# Create a new branch from current branch
git checkout -b feature/descriptive-branch-name

# Commit with signoff (required)
git commit -s -m "type: brief description

Detailed explanation of the change.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Note**: Always use `-s` flag for signed commits (DCO compliance).

### 2. Push to Fork

```bash
# Push branch to fork (remote 'z')
git push -u z feature/descriptive-branch-name
```

### 3. Create Issue

Use gitcode MCP tool to create an issue in the upstream repository:

```
mcp__gitcode__create_issue
- owner: openharmony
- repo: graphic_graphic_2d
- title: Brief issue title
- body: Detailed issue description with:
  - Summary
  - Problem
  - Solution
  - Impact
  - Files Modified
```

Example issue body:
```markdown
## Summary
Brief description of the issue/change.

## Problem
What problem does this solve?

## Solution
How is it solved?

## Impact
- What changes are made?
- Performance impact
- Test results

## Files Modified
- file1.h
- file2.cpp
```

### 4. Create Pull Request

Use gitcode MCP tool to create PR in upstream repository:

```
mcp__gitcode__create_pull_request
- owner: openharmony
- repo: graphic_graphic_2d
- base: master (NOT main - use master)
- head: zhoutianer:feature/descriptive-branch-name
- title: PR title (matches issue title)
- body: Detailed PR description
```

**Critical**: Use `master` as the base branch, not `main`.

Example PR body:
```markdown
## Summary
Brief description.

## Problem
What problem does this solve?

## Solution
Technical details of the implementation.

## Impact
- Code quality improvements
- Performance impact
- Test results

## Test plan
- [x] Build passes
- [x] All tests pass
- [x] No new warnings

## Files Modified
- file1.h
- file2.cpp

Closes #<issue-number>
```

The `Closes #<issue-number>` at the end automatically links the PR to the issue.

### 5. Link Issue to PR

Add a comment to the issue referencing the PR:

```
mcp__gitcode__create_issue_comment
- owner: openharmony
- repo: graphic_graphic_2d
- issue_number: <issue-number>
- body: Link to PR and summary
```

Example comment:
```markdown
This issue is addressed by PR #<pr-number>: https://gitcode.com/openharmony/graphic_graphic_2d/merge_requests/<pr-number>

The PR implements:
- Key change 1
- Key change 2

Build passes in X:YY time with all tests passing.
```

## Important Notes

1. **Base branch**: Always use `master`, not `main`
2. **Sign commits**: Always use `git commit -s` for DCO compliance
3. **Branch naming**: Use descriptive names like `refactor/feature-name`, `fix/bug-description`
4. **Issue-PR linking**: Include `Closes #<issue-number>` in PR body
5. **Remote names**:
   - `gitcode` - upstream (openharmony/graphic_graphic_2d)
   - `z` - fork (zhoutianer/graphic_graphic_2d)

## Example Session

```bash
# After making code changes
git reset HEAD .
git add .
git checkout -b refactor/color-picker-common-impl
git commit -s -m "refactor: Extract common implementation

- Add HandleColorUpdate to base interface
- Extract CreateColorPickerInfo helper
- Remove ~200 lines of duplication

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push -u z refactor/color-picker-common-impl
```

Then use MCP tools to create issue #22224, PR #28311, and link them.

## Troubleshooting

**PR creation fails with API error (400)**:
- Check that base branch is `master`, not `main`
- Ensure branch was pushed to fork first

**Issue not linking to PR**:
- Verify `Closes #<issue-number>` is in PR body
- Check issue number is correct
- Add manual comment to issue if auto-link fails