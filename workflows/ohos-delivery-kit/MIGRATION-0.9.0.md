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

For hidden `issue-*` archives, ODK 0.8 flat formal archives, and in-flight flat
drafts, create a two-column TSV mapping outside the worktree:

```text
.codespec/changes/issue-9988-legacy-focus	REQ-9988
codespec/changes/REQ-12345-arkui-focus	REQ-12345
codespec/changes/REQ-PLAT-88-render-cache	REQ-PLAT-88
codespec/changes/draft-20260831-new-focus	-
```

The second column is the developer-confirmed requirement ID. Use a single `-`
for a valid `draft-*` that has no requirement ID; the planner preserves the full
draft leaf and only adds the repository layer. Never invent an ID for a draft.
The map must cover every legacy archive discovered by the tool.

Validate the plan before moving anything:

```bash
python3 runtime/executables/validate-archive-migration.py plan \
  --map ../odk-0.9-archive-map.tsv --repo .
```

Execute the printed `PLAN` moves with `git mv`, update repository references, and
stage the complete migration. Keep a formal proposal's `req:` equal to its ID;
keep a draft's `req:` empty or absent. Then reuse the same map:

```bash
python3 runtime/executables/validate-archive-migration.py check-staged \
  --map ../odk-0.9-archive-map.tsv --repo .
python3 runtime/executables/validate-artifacts-contract.py \
  codespec/changes/<repo-name>/<req-id> --archive
```

`check-staged` verifies conservation against `HEAD`: every mapped legacy source
must be deleted from the staged index and its worktree directory must be gone,
including ignored leftovers. Every planned target must exist exactly once, and
the staged proposal set must exactly match the map. Run Archive
validation for formal targets and Draft validation for draft targets. Do not
commit until the applicable commands pass. The planner blocks duplicate targets,
existing targets, incomplete mappings, invalid requirement IDs, and
repository-name path mismatches.
