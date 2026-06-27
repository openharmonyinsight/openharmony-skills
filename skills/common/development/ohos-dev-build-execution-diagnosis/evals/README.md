# OpenHarmony Build Execution And Diagnosis Skill Evals

Use [`evals.json`](evals.json) as the seed set for the first benchmark iteration.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-build-execution-diagnosis-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-exact-command-log-first/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Minimum success criteria

- At least one eval checks exact user-command execution from the OpenHarmony root containing `.gn` and `build.sh`.
- At least one eval checks failure diagnosis from the primary `build.log`, not from terminal tail alone.
- At least one eval checks product-specific log routing: regular product, SDK, host product, minimal emulator, full emulator, and independent build.
- At least one eval checks command selection for host, minimal emulator, full emulator, SDK, targeted builds, ACE Engine tests, and all-unit-test builds.
- At least one eval checks `--fast-rebuild` discipline: use only after confirming no build configuration changed.
- At least one eval checks `hb build` independent-build rules: component name, `-i`/`-t` placement, `out/standard/` logs, and no repository-name guessing.
- At least one eval checks test-list builds using `scripts/build_test_list.sh`, first-failure recovery, and narrow resume.
- At least one eval checks preloader/load failure diagnosis through `out/preloader/<product>/parts.json`.
- At least one eval checks link-failure diagnosis by tracing missing symbol owners, deps, source inclusion, and conditional flags.
- At least one eval checks safe cleanup rules: no broad `out/` deletion, only explicitly allowed generated/test-artifact paths.
- Negative cases are covered across the eval set: do not mutate workspace setup without request, do not infer from terminal tail when logs exist, do not delete source logic to pass builds, do not change product/target/args without asking.
- Assertions measure OpenHarmony-build-specific behavior rather than generic troubleshooting quality.

## Current coverage map

- `0`: exact user command, root detection, exit-code handling, and primary log inspection without starting a long real build during eval.
- `1`: regular product compile failure from a fixture `out/rk3568/build.log`: extract first real compiler error, make smallest source/build fix.
- `2`: host product command and log routing: `host_product`, `--no-prebuilt-sdk`, `out/host/host_product/build.log`.
- `3`: minimal and full emulator command selection, required flags, and no argument drift.
- `4`: `--fast-rebuild` eligibility and rejection after `BUILD.gn` / `*.gni` / product config changes.
- `5`: `hb build` independent component build: component-name verification, option placement, `out/standard/` diagnosis.
- `6`: target-list builds from fixture `unittest_targets.txt` context, helper usage, first-failure recovery, and limited disk cleanup.
- `7`: preloader/load failure from fixture `parts.json` and component metadata: inspect `out/preloader/<product>/parts.json` before source fixes.
- `8`: link failure from fixture `build.log`: missing symbol ownership, deps/source inclusion/flags, no logic deletion.
- `9`: SDK and targeted test command selection, ACE Engine focused test versus all `unittest`.
- `10`: log-location routing across product classes, including `qemu-arm-linux-min -> out/qemu-arm-linux/build.log`, and helper-script usage.
- `11`: safety boundaries: no `repo sync`, source/prebuilt download, broad cleanup, or product/target argument changes without request.

## Dimension coverage summary

| Skill dimension | Eval IDs | Coverage |
|-----------------|----------|----------|
| OpenHarmony root detection | 0, 1, 3 | covered |
| Exact command execution | 0, 3, 11 | covered |
| Product command selection | 2, 3, 9 | covered |
| Primary log routing | 1, 2, 5, 10 | covered |
| Failure-first extraction | 1, 7, 8 | covered |
| Fast rebuild discipline | 4 | covered |
| Independent component build | 5 | covered |
| Test-list builds | 6 | covered |
| Preloader/load diagnosis | 7 | covered |
| Link diagnosis | 8 | covered |
| Cleanup safety | 6, 11 | covered |
| Non-mutating setup boundary | 0, 11 | covered |

See [`../SKILL.md`](../SKILL.md) for the runtime rules and [`../references/`](../references/) for command, log, and failure-analysis details.
