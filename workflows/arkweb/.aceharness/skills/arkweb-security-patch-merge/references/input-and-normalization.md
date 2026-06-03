# Input And Patch Normalization

## Inputs

This workflow accepts either:

- a normal current-run patch fetch result: `.ace-outputs/{runId}/02_patch_fetch.md/json` or `03_patch_fetch.md/json`
- a single archived issue directory containing `01_issue_analysis.*`, `02_patch_fetch.*`, `03_impact_decision.*`, `04_final_archive.*`, and `patches/`
- a batch archive run directory containing numeric issue subdirectories

Keep the ArkWeb project root separate from the archive input directory.

- ArkWeb project root comes from `context.codebase` / `context.automation.repoPath`. `context.projectRoot` is the lightweight workflow output root.
- The archive input directory comes from `context.requirements`.
- For archive input, read `02_patch_fetch.json` from the issue archive directory. Both `{"issues":[...]}` and flat JSON are supported; use the first issue record when the wrapper exists. `patch_files[]` is the patch source and `modified_files[]` is the allowed merge/manual-write scope.

Impact fields such as `summary.json.impact` or `03_impact_decision.json` are evidence for later risk/reporting. They must not filter patches out of automatic merge when the issue has complete patch artifacts.

## Normalize Patches

Use `scripts/normalize_patch.mjs` before scanning paths or running `git apply`.

```bash
node skills/arkweb-security-patch-merge/scripts/normalize_patch.mjs <patch-file> --out <normalized-file>
```

The script detects raw diff, raw mbox, base64 diff, and base64 mbox. It writes a normalized patch only when standard patch signals are present and prints JSON with:

- `format`
- `valid`
- `validation_signals`
- `original_sha256`
- `normalized_sha256`
- `diff_paths`

Do not overwrite files in the input archive directory. Store normalized copies in the current workflow output directory:

```text
single issue: .ace-outputs/{runId}/normalized_patches/<patch-name>.patch
batch issue:  .ace-outputs/{runId}/issues/{issue_id}/normalized_patches/<patch-name>.patch
```

Patch path resolution for archive input:

1. Absolute `patch_files[].path` values are used as-is.
2. Relative `patch_files[].path` values are resolved against the current issue archive directory first.
3. Then try `<issue archive dir>/patches/<path>`.
4. Then try the batch archive root.
5. Only after archive-relative checks fail may a generic process-relative fallback be considered.

Do not resolve archive patch paths against `context.projectRoot` first; that can accidentally treat the ArkWeb source tree as the patch archive.

Use the normalized files for:

- `diff --git` path scanning
- target subrepo detection
- strip parameter detection
- `git apply`

Use the stable field name `patch_normalization[]`. If reading legacy `normalized_patches`, rewrite current results as `patch_normalization[]`.
