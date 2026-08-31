# ODK 0.8.0 archive path migration

ODK 0.8.0 replaces `.codespec/changes/issue-<issue-number>-<english-slug>/`
with `codespec/changes/<req-id>-<english-slug>/`. This is a breaking change.
`odk-link-req` only links a new `draft-*` directory and is not a legacy archive
migrator.

## 1. Discover and map

Start from a clean worktree and a dedicated branch:

```bash
git status --short
git switch -c migrate/odk-0.8-archives
find .codespec/changes -mindepth 1 -maxdepth 1 -type d \
  -name 'issue-[0-9]*-*' -print | LC_ALL=C sort
```

Create `archive-map.tsv` with the complete old relative path in column one and
the developer-confirmed requirement ID in column two. Do not infer a requirement
ID from the issue number.

```text
.codespec/changes/issue-12345-arkui-focus	REQ-12345
.codespec/changes/issue-67890-render-cache	REQ-PLAT-88
```

## 2. Dry-run collision checks

This command prints the plan and stops before any move if a source, ID, slug, or
target is invalid:

```bash
while IFS=$'\t' read -r old_path req_id; do
  old_name=${old_path##*/}
  slug=$(printf '%s\n' "$old_name" | sed -E 's/^issue-[0-9]+-//')
  new_path="codespec/changes/${req_id}-${slug}"
  test -d "$old_path" || { echo "missing source: $old_path" >&2; exit 1; }
  printf '%s' "$req_id" | grep -Eq '^[A-Za-z0-9]+([A-Za-z0-9-]*[A-Za-z0-9])?$' || exit 1
  printf '%s' "$slug" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$' || exit 1
  test ! -e "$new_path" || { echo "target exists: $new_path" >&2; exit 1; }
  printf 'PLAN\t%s\t%s\n' "$old_path" "$new_path"
done < archive-map.tsv
```

## 3. Move and update metadata

For each reviewed mapping, use `git mv`:

```bash
mkdir -p codespec/changes
git mv .codespec/changes/issue-12345-arkui-focus \
  codespec/changes/REQ-12345-arkui-focus
```

In the moved `proposal.md` YAML frontmatter, remove `issue:`, add exactly one
`req: REQ-12345`, and keep the value identical to the directory requirement ID.
Then review and update every old path, command, and metadata reference:

```bash
rg -n --hidden --glob '!.git/**' \
  '\.codespec/changes|odk-link-issue|^[[:space:]]*issue:' .
```

## 4. Validate and roll back

Validate each migrated directory in Draft mode, then in Archive mode when it is
ready for formal archive:

```bash
python3 /path/to/validate-artifacts-contract.py \
  codespec/changes/REQ-12345-arkui-focus
python3 /path/to/validate-artifacts-contract.py \
  codespec/changes/REQ-12345-arkui-focus --archive
git diff --check
git diff --cached --name-status
```

If migration must be abandoned, only from the dedicated branch that started
clean, restore its uncommitted changes with:

```bash
git restore --staged --worktree --source=HEAD -- .
```

Do not run that rollback command if pre-existing user changes were present;
restore files individually or recover them from a separate worktree instead.
