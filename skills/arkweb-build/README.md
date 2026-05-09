# ArkWeb Build Skill

This skill is for ArkWeb build execution, incremental verification, and build failure diagnosis.

Environment requirement: Linux build host with GNU coreutils and `/proc` available.

## Core Flow

1. Resolve the ArkWeb wrapper root. Build commands run from `<arkweb-root>`.
2. Check whether `src/out/<product>/build.log` already exists and call out first-build versus incremental-build behavior.
3. Before any full build or direct Ninja rerun, record a resource snapshot:

```bash
bash <skill-dir>/scripts/capture_resource_snapshot.sh <product> before-build <arkweb-root>
```

The first argument is the product name, for example `rk3568_64`. Do not call this script with the ArkWeb root as the first argument.

4. Run the configured workflow command first. Use defaults only when no workflow command is provided.
5. On failure, inspect `src/out/<product>/build.log`, then run:

```bash
bash <skill-dir>/scripts/analyze_build_error.sh <product> <arkweb-root>
bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>
```

`analyze_build_error.sh` also accepts an explicit build log path: `analyze_build_error.sh <arkweb-root>/src/out/<product>/build.log <arkweb-root>`.

## Script Usage

`capture_resource_snapshot.sh` supports both the full labeled form and the short form:

```bash
bash <skill-dir>/scripts/capture_resource_snapshot.sh <product> <label> <arkweb-root>
bash <skill-dir>/scripts/capture_resource_snapshot.sh <product> <arkweb-root>
```

Rules:

- `<product>` must be a product directory name such as `rk3568_64`; it must not be an absolute path or contain `/`.
- `<arkweb-root>` is the wrapper root that contains `build_arkweb.sh`; it can be absolute or relative.
- `<label>` is optional in the short form and defaults to `snapshot`.
- If `<label>` contains spaces, `/`, or other unsafe filename characters, the script replaces them with `_`.
- Snapshots are written to `<arkweb-root>/src/out/<product>/resource_snapshots/`.

`analyze_build_error.sh` supports both product-based and log-path-based forms:

```bash
bash <skill-dir>/scripts/analyze_build_error.sh <product> <arkweb-root>
bash <skill-dir>/scripts/analyze_build_error.sh <arkweb-root>/src/out/<product>/build.log <arkweb-root>
```

If the first argument is a `*.log` path, the script uses that log directly and derives `<product>` from its parent directory.

## Failure Stages

`scripts/analyze_build_error.sh` classifies failures into:

- `pre-gn/sdk-lfs`: SDK setup, archive extraction, missing package, Git LFS pointer, or gzip/tar/unzip failure before GN or Ninja.
- `gn-generation`: `ERROR at //...`, `Unable to load`, or GN file evaluation failure.
- `ninja-graph-or-target`: unknown target, missing `build.ninja`, or Ninja graph loading failure.
- `ninja-compile-link`: compiler or linker failure after Ninja starts.
- `resource-or-terminated`: explicit `killed` or `OutOfMemory`.
- `resource-or-terminated-suspected`: log tail still looks like Ninja progress, with no `FAILED:`, GN error, or Ninja target error. Inspect the latest resource snapshot before changing code.

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
bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root> --show-all
bash <skill-dir>/scripts/show_relevant_changes.sh --show-all <arkweb-root>
```

The script checks both `src` and `src/arkweb`, expands untracked directories with `git status --short -uall`, prints ignored default dirty entries, and filters known default dirty entries before showing relevant changes. Use `--show-all` or `--no-ignore` to disable filtering; the flag can be placed before or after `<arkweb-root>`.

## LFS Failures

For `pre-gn/sdk-lfs` failures, use:

```bash
bash <skill-dir>/scripts/check_lfs_artifacts.sh <arkweb-root>
```

The script treats packages from `src/ohos_sdk/.install` as current-build required items. Other LFS entries from `.gitattributes`, including `arkweb.profdata`, are informational unless the failing log explicitly points to them.

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
