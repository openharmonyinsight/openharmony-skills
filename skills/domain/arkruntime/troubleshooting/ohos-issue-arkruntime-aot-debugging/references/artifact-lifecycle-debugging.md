# Artifact Lifecycle Debugging

Use this reference for `.an` generation, reuse, overwrite, update cleanup, idle AOT, framework static AOT, and shared HSP host-private artifacts.

## Classify the AOT Path

Do not answer artifact questions globally. First classify:

- Dynamic AOT
- Ordinary static app idle AOT
- Framework static AOT
- Shared HSP host-private AOT
- Host/PAOC test build output

## Evidence to Collect

- The external trigger: `bm` / `bundle_tool`, install/update/uninstall, idle scheduler, Ability/app lifecycle, or test harness.
- The AOT path and owner process.
- The expected input ABC path.
- The expected output `.an` path.
- Whether an existence/version check ran.
- Whether the caller treats an existing output as success, skip, overwrite, or stale.
- For updates, the exact BundleManager/update path under discussion.

## Debugging Steps

1. Locate output path construction.
2. If the trigger is command-line install/update/query, inspect `bundle_tool` command parsing and BundleManager IPC handoff before compiler internals.
3. If the trigger is app startup or lifecycle, inspect Ability runtime and BundleManager state before compiler internals.
4. Locate existence checks and return-code mapping.
5. Locate version checks such as AOT-file version validation.
6. Locate cleanup ownership for update/uninstall only in the exact path.
7. Decide whether the observed behavior is reuse, regeneration, cleanup, or failed emission.

## Fix Direction

- Wrong output path: fix path construction or recorded path/header metadata at the owner that creates the argument.
- Unexpected reuse: fix the path-specific existence/version gate, not a global AOT rule.
- Unexpected regeneration: confirm whether this path has any service-layer short-circuit; add one only if lifecycle semantics require it.
- Missing artifact: inspect child compiler emission logs, file permissions, signing/persistence steps, and caller return-code handling.

## Cannot Conclude

- Do not say an existing `.an` is always skipped.
- Do not say app update always deletes all `.an` files.
- Do not generalize dynamic AOT reuse behavior to ordinary static app idle AOT or shared HSP AOT.
