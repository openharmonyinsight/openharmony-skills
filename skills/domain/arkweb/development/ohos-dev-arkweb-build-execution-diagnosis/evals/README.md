# ArkWeb Build Execution And Diagnosis Skill Evals

Use [`evals.json`](evals.json) as the seed set for the first benchmark iteration.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-arkweb-build-execution-diagnosis-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-wrapper-root-default-webview/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Minimum success criteria

- At least one eval checks ArkWeb wrapper-root detection: `build_arkweb.sh` and `src/arkweb/build/build.sh` must both exist, and build commands run from the wrapper root rather than `src/`.
- At least one eval checks first-build versus incremental-build detection using `src/out/<product>/build.log`, including the 2 to 3 hour first-build warning.
- At least one eval checks default command selection for `rk3568_64 -t w -A` and common target aliases (`n`, `b`, `w`, `coreut`). `allut` and `smokeut` remain reference coverage unless additional evals are added.
- At least one eval checks workflow-provided command precedence over defaults.
- At least one eval checks failure diagnosis from `src/out/<product>/build.log`, stage classification, and use of bundled scripts.
- At least one eval checks change-first diagnosis using `scripts/show_relevant_changes.sh`, including default dirty-file filtering and separate `src` / `src/arkweb` repository handling.
- At least one eval checks Git LFS / SDK package failures through `check_lfs_artifacts.sh`, `.gitattributes`, and `src/ohos_sdk/.install` without patching `src/ohos_sdk/`.
- At least one eval checks compile/link failures: single failed command verification is allowed only for `ninja-compile-link` and must run from `src/out/<product>`.
- At least one eval checks GN generation and Ninja graph failures: do not use single compiler/linker-command verification.
- At least one eval checks silent-stop/resource-pressure diagnosis via `capture_resource_snapshot.sh` and reduced `-j`.
- At least one eval checks direct Ninja continuation rules: only for already-configured incremental builds, from `src/`, with the same target set.
- Negative cases are covered across the eval set: no `git clean`, `git reset --hard`, `rm -rf src/out`, `gn clean`, `ninja -t clean`, dependency resync, or touching files outside the current ArkWeb project unless explicitly requested.
- Assertions measure ArkWeb-build-specific behavior rather than generic OpenHarmony build troubleshooting.

## Current coverage map

- `0`: wrapper-root detection, default WebView command, first-build warning, and `src/out/rk3568_64/build.log`.
- `1`: workflow-provided command precedence and no fallback override.
- `2`: command matrix for native, BrowserShell, WebView, tests, release, ASan, and product output directories.
- `3`: failure diagnosis from a fixture `build.log`, stage classification, and helper-script routing.
- `4`: change-first diagnosis from fixture raw status plus `build.log`, with default dirty-file filtering and separate `src` / `src/arkweb` repos.
- `5`: Git LFS / SDK prebuilt archive failure diagnosis from fixture `.install`, `.gitattributes`, and LFS pointer content.
- `6`: compile/link failure post-fix verification using the failed command from a fixture `build.log` and `src/out/<product>`.
- `7`: GN generation and Ninja target graph failures from a fixture error log, rerun strategy, and `args.gn` checks.
- `8`: silent Ninja stop or OOM/resource-pressure diagnosis using fixture `build.log` tail, resource snapshot, and reduced parallelism.
- `9`: direct Ninja continuation from fixture context for already-configured incremental builds and same target set.
- `10`: repair responsibility and forbidden change boundaries, especially `src/ohos_sdk/` and outside-project files.
- `11`: output expectations and success verification: command, cwd, product/target, exit status, log path, failure type, minimal next fix.

## Dimension coverage summary

| Skill dimension | Eval IDs | Coverage |
|-----------------|----------|----------|
| Wrapper root detection | 0, 2 | covered |
| Default command selection | 0, 2 | covered |
| Workflow command precedence | 1 | covered |
| First-build detection | 0 | covered |
| Primary log routing | 0, 3, 11 | covered |
| Failure-stage classification | 3, 6, 7, 8 | covered |
| Change-first diagnosis | 4 | covered |
| LFS / SDK artifact diagnosis | 5 | covered |
| Compile/link quick verification | 6 | covered |
| GN / Ninja graph rerun rules | 7 | covered |
| Resource pressure diagnosis | 8 | covered |
| Direct Ninja continuation | 9 | covered |
| Forbidden changes and safety | 5, 10 | covered |
| Structured final reporting | 11 | covered |

See [`../SKILL.md`](../SKILL.md) for the runtime rules and [`../references/`](../references/) for command, log, and failure-analysis details.
