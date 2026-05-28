---
name: openharmony-build
description: Use for OpenHarmony build execution and diagnosis, including 编译OpenHarmony/完整代码/测试/SDK/host/最小模拟器/全量模拟器/部件独立编译/测试列表, plus full product builds, targeted component/test builds, fast rebuilds, hb independent builds, and build.log failure analysis.
version: 0.9.0
---

# OpenHarmony Build Skill

Use this skill for OpenHarmony build execution, targeted build verification, and build-log diagnosis. Keep context small: start here, then load only the reference that matches the task.

`<skill-dir>` means the directory containing this `SKILL.md`.

## Core Rules

- Run builds from the OpenHarmony root containing both `.gn` and `build.sh`.
- If the user gives an exact command, run that command.
- For failures, inspect the primary build log before guessing at source fixes.
- Do not revert unrelated dirty-worktree changes.
- Prefer narrow rebuilds after fixes, then rerun the user-requested command when practical.

## Never / Ask Before

- Never run `repo sync`, source download, prebuilt download, or environment bootstrap unless the user explicitly asks for setup; these are slow and can mutate the workspace.
- Never delete source logic just to make a build pass; preserve behavior and fix the real dependency, symbol, or configuration issue.
- Never diagnose a failed build from terminal tail alone when `build.log` exists; the primary log is the source of truth.
- Never treat a repository name as the `hb build` component name without checking; independent builds require OpenHarmony component names.
- Never broadly delete `out/`, generated artifacts, or test binaries. Ask first unless the user requested cleanup; for test-list disk pressure, only use the path in `references/test-list-builds.md`.
- Ask before changing product, target, branch, or user-provided command arguments.

## Find Root

Use this root test:

```bash
find_oh_root() {
    local dir="${1:-$PWD}"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/.gn" && -f "$dir/build.sh" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}
```

## Command Selection

Default full build:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache
```

Targeted build:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name <product> --build-target <target> --ccache
```

Special products:

- SDK: `./build.sh --export-para PYCACHE_ENABLE:true --product-name ohos-sdk --ccache`
- Host: `./build.sh --product-name host_product --ccache --no-prebuilt-sdk`
- Minimal emulator: `./build.sh --product-name qemu-arm-linux-min --ccache --no-prebuilt-sdk --deps-guard=false --load-test-config false --gn-args linux_kernel_version=\"linux-5.10\"`
- Full emulator: `./build.sh --product-name arm64_virt --ccache --deps-guard=false`

Read `references/build-commands.md` for the full command matrix, products, targets, SDK/host/emulator notes, and fast-rebuild examples.

Reference routing:

- Read `references/build-commands.md` when choosing command syntax, products, targets, SDK/host/emulator commands, or fast-rebuild examples.
- Read `references/log-locations.md` only when locating or explaining build outputs and logs.
- Read `references/common-errors.md` only after a concrete error class is known.

## Fast Rebuild

Use `--fast-rebuild` only when build configuration did not change. Do not use it after edits to `BUILD.gn`, `*.gni`, product config, dependency metadata, or first-time output generation.

Helper:

```bash
bash <skill-dir>/scripts/check_fast_rebuild.sh 30 "$OH_ROOT"
```

## Independent Component Build

Use for "部件独立编译", "独立编译部件", or explicit `hb build` requests.

```bash
command -v hb
hb build <component-name> -i
hb build <component-name> -t
```

Rules:

- Use the OpenHarmony component name, not necessarily the repository name.
- Put `-i` or `-t` after the component name.
- Run `-i` before `-t` when both are requested.
- Diagnose independent builds from `out/standard/`.

Reference routing: for `hb` independent builds, always read `references/independent-build.md`; do not load `references/test-list-builds.md` unless the task is specifically about target-list builds.

## Test Builds

For ACE Engine development, prefer:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --ccache
```

Build all unit tests only when requested or required:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target unittest --ccache
```

For target-list builds:

```bash
bash <skill-dir>/scripts/build_test_list.sh rk3568 "$OH_ROOT"
```

Reference routing: for target-list builds, read `references/test-list-builds.md`; do not load `references/independent-build.md` unless the target-list run uses `hb build`.

## Success Check

A successful build usually has:

- command exit code `0`
- `=====build successful=====` or equivalent success output
- expected output under `out/`
- no final fatal/error section in the primary build log

Use exit code as the first signal. Check artifacts only when the user needs artifact confirmation.

## Failure Analysis

Always start from the primary log:

- regular product: `out/<product>/build.log`
- SDK: `out/sdk/build.log`
- host product: `out/host/host_product/build.log`
- independent build: `out/standard/build.log` or the relevant `out/standard/` sublog

Use scripts before broad manual searching:

```bash
bash <skill-dir>/scripts/resolve_build_log.sh <product> "$OH_ROOT"
bash <skill-dir>/scripts/find_recent_errors.sh <product> "$OH_ROOT"
bash <skill-dir>/scripts/analyze_build_error.sh <product> "$OH_ROOT"
```

For `hb build` failures, pass `standard` as the product:

```bash
bash <skill-dir>/scripts/find_recent_errors.sh standard "$OH_ROOT"
bash <skill-dir>/scripts/analyze_build_error.sh standard "$OH_ROOT"
```

Reference routing:

- Read `references/failure-analysis.md` for non-zero build exits, first-failure extraction, and fix/rebuild workflow.
- Read `references/log-locations.md` when the log path is unclear.
- Read `references/common-errors.md` only after identifying the error class.

## Bundled Resources

Scripts:

- `scripts/resolve_build_log.sh`: print the primary build log for a product/root.
- `scripts/analyze_build_error.sh`: summarize failures from the primary log.
- `scripts/find_recent_errors.sh`: quick recent error scan.
- `scripts/check_fast_rebuild.sh`: decide whether `--fast-rebuild` is appropriate.
- `scripts/build_test_list.sh`: build targets listed in `unittest_targets.txt`.

References:

- `references/build-commands.md`: complete command reference.
- `references/log-locations.md`: output and log path mapping.
- `references/common-errors.md`: common failure classes and fixes.
- `references/failure-analysis.md`: structured diagnosis workflow.
- `references/independent-build.md`: `hb build` rules and diagnosis patterns.
- `references/test-list-builds.md`: target-list builds and disk-space recovery.

Do not load `README.md` or `examples/example-workflow.md` during normal skill execution; they are repository-facing summaries, not runtime instructions.
