# ODK 0.8.0 archive path migration

> **Frozen historical guide for ODK 0.8.0 tooling only.** Do not use the target
> layout below or run these commands with an ODK 0.9.0+ installation. Use the
> [0.9.0 repository-scoped migration](MIGRATION-0.9.0.md) to migrate hidden
> `issue-*`, flat formal archives, or flat drafts directly into
> `codespec/changes/<repo-name>/...`.

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

Create a TSV outside the worktree with the complete old relative path in column
one and the developer-confirmed requirement ID in column two. Keeping it outside
the worktree prevents its legacy paths from appearing in the residue scan or a
commit. Do not infer a requirement ID from the issue number.

```bash
map_file=../odk-0.8-archive-map.tsv
```

```text
.codespec/changes/issue-12345-arkui-focus	REQ-12345
.codespec/changes/issue-67890-render-cache	REQ-PLAT-88
```

## 2. Dry-run collision checks

Use the validator from a pinned ODK 0.8.0 source tree or installation. It prints the plan without moving
files and rejects an in-worktree map, invalid legacy paths, missing/extra or
duplicate sources, duplicate planned targets, invalid IDs/slugs, and existing
targets:

```bash
python3 /path/to/ohos-delivery-kit-0.8.0/scripts/validate-archive-migration.py \
  plan --map "$map_file" --repo .
```

Review every `PLAN` line before moving anything.

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

Stage only the migration roots and each explicitly reviewed reference file. Do
not use an unbounded `git add .`:

```bash
git add -A -- .codespec/changes codespec/changes
git add -- path/to/updated-registry.md path/to/updated-script.sh
```

## 4. Validate and roll back

Validate each migrated directory in Draft mode, then in Archive mode when it is
ready for formal archive:

```bash
python3 /path/to/ohos-delivery-kit-0.8.0/scripts/validate-artifacts-contract.py \
  codespec/changes/REQ-12345-arkui-focus
python3 /path/to/ohos-delivery-kit-0.8.0/scripts/validate-artifacts-contract.py \
  codespec/changes/REQ-12345-arkui-focus --archive
python3 /path/to/ohos-delivery-kit-0.8.0/scripts/validate-archive-migration.py \
  check-staged --repo .
git diff --cached --name-status
```

`check-staged` rejects unstaged tracked edits, untracked files, staged whitespace
errors, legacy `issue:` frontmatter, missing/duplicate `req:`, and directory/ID
mismatches. Commit only after it passes.

If migration must be abandoned, only from the dedicated branch that started
clean, restore its uncommitted changes with:

```bash
git restore --staged --worktree --source=HEAD -- .
```

Do not run that rollback command if pre-existing user changes were present;
restore files individually or recover them from a separate worktree instead.
