# Skills-Repo Sync PR Review Pitfalls

Recurring failure modes found when reviewing **marketplace sync PRs** in skills
repositories (e.g. `openharmony-skills`): a workflow directory
(`workflows/<name>/`) is imported from a source repo via a sync script, which
rewrites placeholders/paths (`{{PLUGIN_ROOT}}` → `{{ASSET_ROOT}}`,
`openharmony/` → `runtime/assets/`, rename `ohos-spec-for-test` →
`ohos-spec-for-validation`, etc.). The sync script handles most replacements but
consistently leaves leftovers. Review with `reviewing-skill-prs.md` as the base
lens, plus these sync-specific checks.

## 1. Placeholder & path-migration leftovers

- Old placeholder strings that should have been replaced (`{{PLUGIN_ROOT}}`),
  allowing occurrences that only *explain* the substitution rule.
- Old path prefixes from the previous layout (`openharmony/`,
  `context-engine/analysis/`). Leftovers cluster in **README files and per-profile
  `profile.md` files**, not just top-level files.
- Do a **full-tree scan** (`rg -n '<old-string>' <workflow-dir>`) rather than
  eyeballing the diff — leftovers often live in files the diff shows as unchanged.
- Slash-command renames (`/ohos-intake` + `/ohos-baseline` → `/ohos-propose`):
  check `commandProjection` and workflow files for old command names. CLI strings
  that exist only to *detect and block* old names are legitimate, not leftovers.

## 2. Contract / manifest dangling references

- `contracts/*.yaml` `truth_sources` may still point at directories the sync
  removed from runtime assets (e.g. `active_docs: docs` after `docs/` is moved to
  nonRuntimeAssets). `validate --source` typically does **not** check
  `truth_sources` existence, so a green contract self-check does not prove the
  truth source exists.
- `plugin.yaml` asset/executable entries: verify each declared path resolves to a
  real file; watch for asset dirs removed from the manifest but still referenced
  in templates/workflow/profiles.

## 3. Skill metadata gaps (skill-definition lens)

- `metadata.related-skills` missing on skills that invoke other skills at runtime
  (meta-routers like `using-*`, slash-command skills, conditional routers).
- Governance fields missing on new/renamed `SKILL.md` frontmatter:
  `scope/stage/domain/capability/version/status`.
- `name` vs directory mismatch after a skill rename.

## 4. Verify the PR author's self-reported "known issues"

PR bodies often list 「已知问题 / known issues」 — verify each one against the
actual tree; they may be stale or already fixed. Example: PR 323 claimed
`templates/design.md:282` still referenced a removed `docs/security-guide.md`,
but the rename to `analysis/security-playbook.md` was complete and the workflow
no longer referenced the old guide at all.

## Verification recipe that catches these

1. Reconcile against the source repo at the **provenance commit** (not the short
   SHA in the PR body — that may be an older ancestor; the provenance commit is
   authoritative).
2. Run the workflow's own tests and report counts: contract self-check
   (`validate-artifacts.sh`), CLI smoke, published-layout test, python unittest,
   skill quality check (e.g. "190 checks / 0 broken").
3. Full-tree string scans for every old placeholder/prefix (see #1).
4. Check `py_compile` / `bash -n` syntax on all synced CLI files.
