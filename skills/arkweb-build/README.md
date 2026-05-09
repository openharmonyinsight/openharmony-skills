# ArkWeb Build Skill

This skill is for ArkWeb build execution, incremental verification, and build failure diagnosis.

## Core Flow

1. Resolve the ArkWeb wrapper root. Build commands run from `<arkweb-root>`.
2. Check whether `src/out/<product>/build.log` already exists and call out first-build versus incremental-build behavior.
3. Before any full build or direct Ninja rerun, record a resource snapshot:

```bash
bash <skill-dir>/scripts/capture_resource_snapshot.sh <product> before-build <arkweb-root>
```

4. Run the configured workflow command first. Use defaults only when no workflow command is provided.
5. On failure, inspect `src/out/<product>/build.log`, then run:

```bash
bash <skill-dir>/scripts/analyze_build_error.sh <product> <arkweb-root>
bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>
```

## Failure Stages

`scripts/analyze_build_error.sh` classifies failures into:

- `pre-gn/sdk-lfs`: SDK setup, archive extraction, missing package, Git LFS pointer, or gzip/tar/unzip failure before GN or Ninja.
- `gn-generation`: `ERROR at //...`, `Unable to load`, or GN file evaluation failure.
- `ninja-graph-or-target`: unknown target, missing `build.ninja`, or Ninja graph loading failure.
- `ninja-compile-link`: compiler or linker failure after Ninja starts.
- `resource-or-terminated`: `killed`, `OutOfMemory`, or a silent process disappearance.

Only `ninja-compile-link` supports single-command quick verification.

## Single-Command Ninja Verification

For `ninja-compile-link` failures, after fixing the root cause:

1. Run the failed compiler or linker command from the Ninja output directory:

```bash
cd <arkweb-root>/src/out/<product>
<failed command printed after the first FAILED: line>
```

2. If that succeeds, switch back before broader verification:

```bash
cd <arkweb-root>
bash <skill-dir>/scripts/capture_resource_snapshot.sh <product> before-full-build <arkweb-root>
<full configured build_arkweb.sh command>
```

Use `<arkweb-root>/src` only when deliberately rerunning the same direct Ninja target set.

## Dirty File Filtering

Use:

```bash
bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>
```

The script checks both `src` and `src/arkweb`, expands untracked directories with `git status --short -uall`, and filters known default dirty entries before showing relevant changes.

## LFS Failures

For `pre-gn/sdk-lfs` failures, use:

```bash
bash <skill-dir>/scripts/check_lfs_artifacts.sh <arkweb-root>
```

The script checks packages from `src/ohos_sdk/.install`, parses LFS entries from `.gitattributes` files, detects missing files and LFS pointer files, and reports unmatched LFS patterns.

Typical fix:

```bash
cd <arkweb-root>
repo forall -c 'git lfs pull'
```

Or current repo only:

```bash
git -C <arkweb-root>/src lfs pull
```

Do not patch `src/ohos_sdk/` toolchain files or install scripts to bypass missing LFS resources.

