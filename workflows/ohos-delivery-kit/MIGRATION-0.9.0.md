# ODK 0.9.0 repository-scoped archive migration

ODK 0.9.0 replaces `codespec/changes/<req-id>-<english-slug>/` with
`codespec/changes/<repo-name>/<req-id>/`. This is a breaking change.

`repo-name` comes from the Git `origin` repository basename without `.git`; when
`origin` is unavailable, use the worktree root directory name. Formal directories
contain the requirement ID only. The English slug remains only in drafts:

```text
codespec/changes/<repo-name>/draft-<yyyymmdd>-<english-slug>/
```

After receiving the requirement ID, run `odk-link-req`; it renames the draft to
`codespec/changes/<repo-name>/<req-id>/` and fills `proposal.md` `req:`.

For existing formal archives, create a two-column TSV mapping outside the worktree:

```text
codespec/changes/REQ-12345-arkui-focus	REQ-12345
codespec/changes/REQ-PLAT-88-render-cache	REQ-PLAT-88
```

Validate the plan before moving anything:

```bash
python3 runtime/executables/validate-archive-migration.py plan \
  --map ../odk-0.9-archive-map.tsv --repo .
```

Execute the printed `PLAN` moves with `git mv`, update repository references, and
stage the complete migration. Then run:

```bash
python3 runtime/executables/validate-archive-migration.py check-staged --repo .
python3 runtime/executables/validate-artifacts-contract.py \
  codespec/changes/<repo-name>/<req-id> --archive
```

Do not commit until both commands pass. The planner blocks duplicate targets,
existing targets, incomplete mappings, invalid requirement IDs, and repository-name
path mismatches.
