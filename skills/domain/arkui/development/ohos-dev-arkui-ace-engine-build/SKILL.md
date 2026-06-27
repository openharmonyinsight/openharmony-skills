---
name: ohos-dev-arkui-ace-engine-build
description: >
  Build ACE Engine with arkui-specific knowledge: when --fast-rebuild is safe (GN change detection),
  coverage for ace_engine_test, SDK build constraints, host UT (TDD) builds for x86 local execution,
  and test list builds from unittest_targets.txt. Use when user says 编译/build ace_engine, 编译测试,
  编译SDK, 快速编译, host测试, TDD, or mentions ace_engine_test, rk3568, host_product.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: ace-engine-build
  version: 0.2.0
  status: trial
---

# ACE Engine Build

Build OpenHarmony ACE Engine and related components using the `build.sh` build system.

## Environment

- Build script: `./build.sh` in OpenHarmony root (nearest ancestor with `.gn` file; scripts auto-detect this)
- Build system: hb (Harmony Build)
- Output: `out/<product>/` (SDK special case: `out/sdk/`, NOT `out/ohos-sdk/` / Host UT special case: `out/host/host_product`, NOT `out/host_product/`)

## Build Decision Tree

Before building, answer these questions in order:

**Q1: Can `--fast-rebuild` be used?**
All conditions must be met:
1. `out/<product>/` exists with a prior successful build for the **same product**
2. Only source code changed (.cpp/.h/.ts/.ets) — no BUILD.gn / *.gni modifications
3. Not sure about (1) or (2) → run `${SKILL_BASE_DIR}/scripts/check_fast_rebuild.sh` to verify (default path when uncertain)

If any condition is unmet → full build.

**Q2: What to verify?**
- "Does it compile?" → `--build-target ace_engine`
- "Do tests pass?" → `--build-target ace_engine_test` with coverage (see Q3)
- "Run tests on build server without device?" → Host UT build (see Q2a)
- "Is the full system ok?" → full build (no `--build-target`)
- "Is SDK affected?" → `--product-name ohos-sdk` (**NEVER** specify `--build-target` — causes cryptic failures)
- "Multiple specific tests?" → Test list build from `unittest_targets.txt`

**Q2a: Host UT (TDD) build?**
For running ace_engine unit tests directly on the x86 build server without rk3568 device or emulator:
- Use `--product-name host_product --no-prebuilt-sdk --build-target ace_engine_test`
- `--no-prebuilt-sdk` is **required** — host_product must compile against current source
- Binaries are x86 ELF gtest executables — can run directly: `./out/host/host_product/tests/unittest/ace_engine/<test_name>`

**Q3: Coverage?**
- Default: add `--gn-args ace_engine_feature_enable_coverage=true` for ace_engine test builds — coverage overhead is negligible and enables report generation. Skip only when: user explicitly wants fastest feedback, or environment does not support this GN arg (build error on the flag itself)
- Only applies to ace_engine targets; safe with global `unittest` (other repos unaffected)
- Use simple target name (e.g. `ui_content_stub_unittest`), **NEVER** GN path format (`//path:target`)

**Q4: Build failed?**
- Invoke `ohos-dev-arkui-build-error-analyzer` skill. Fallback: `grep -i "error:" out/<product>/build.log | tail -50`

**Result — compose the command:**
```
./build.sh --export-para PYCACHE_ENABLE:true --product-name <PRODUCT> [--build-target <TARGET>] [--gn-args ...] --ccache [--fast-rebuild]
```

| Scenario | Command |
|----------|---------|
| Full build | `./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache` |
| Code-only changes | Add `--fast-rebuild` (only if Q1 conditions met) |
| ACE Engine component | Add `--build-target ace_engine` |
| ACE Engine tests | `--build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true` |
| Fast test iteration | `--build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true --fast-rebuild` |
| SDK | `--product-name ohos-sdk` (no `--build-target`) |
| Host UT (TDD) | `--product-name host_product --no-prebuilt-sdk --build-target ace_engine_test --ccache` |

Products: `rk3568`, `rk3588`, `ohos-sdk`, `host_product` | Targets: `ace_engine`, `ace_engine_test`, `unittest`, `benchmark_linux`

## Test Target List Build

Build targets sequentially from `unittest_targets.txt`:

```txt
# Comments supported, one target per line
ace_engine_test
adapter/ohos/osal/system_properties_unittest
```

File search order: `foundation/arkui/ace_engine/unittest_targets.txt` first, then OpenHarmony root.

Build each target sequentially with stop-on-error:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target=<target> --ccache
```

**Disk space management**: If disk full during test list build, delete verified test binaries from `out/<product>/exe.unstripped/tests/unittest/ace_engine/` ONLY. **NEVER** delete artifacts outside this directory — will break incremental builds. Resume from failed target.

## Success Verification

Success: exit code 0, output shows `=====build successful=====`

```
out/
├── <product>/                 # rk3568, rk3588
│   ├── packages/
│   ├── libs/
│   ├── tests/ace_engine/unittest/<path>/<test_target_name>
│   ├── exe.unstripped/tests/unittest/ace_engine/  # Safe to delete for disk space
│   └── build.log
├── sdk/                       # ohos-sdk only (NOT out/ohos-sdk/)
└── host/host_product/         # host_product only (NOT out/host_product/)
    └── tests/unittest/ace_engine/  # x86 gtest binaries, run directly on build server
```

## Build Execution

**MUST** Launch the build fully detached from the current process group so it survives subagent cleanup. Before launching, check if a previous build is still running:

```bash
bash ${SKILL_BASE_DIR}/scripts/monitor_progress.sh --root <OH_ROOT> --product <PRODUCT> --check
```

If exit code is 0 (prints `active`), a build is in progress — wait for it or ask the user. If exit code is 1, safe to launch.

Use `setsid` with console output redirected to `out/<product>/build_console.log`, `<product>` **MUST BE** the real output path following the #Environment special cases:

```bash
setsid ./build.sh <args> > out/<product>/build_console.log 2>&1 &
echo "Build PID: $!"
```

**MUST** output a progress monitoring tip to the user so they can watch in a separate terminal:

```
编译已启动。如需监听编译进度，在终端运行：
bash ${SKILL_BASE_DIR}/scripts/monitor_progress.sh --root <OH_ROOT> --product <PRODUCT>
```

Replace `<OH_ROOT>` and `<PRODUCT>` with actual values.

After launching and monitoring tip, use `monitor_progress.sh` to watch `build_console.log` and wait for the build to complete:

```bash
bash ${SKILL_BASE_DIR}/scripts/monitor_progress.sh --root <OH_ROOT> --product <PRODUCT>
```

## Scripts

- **`${SKILL_BASE_DIR}/scripts/check_fast_rebuild.sh`** `[--root <path>] [--product <name>] [minutes]` — Three-stage safety check before using `--fast-rebuild`:
  1. `git status` for uncommitted BUILD.gn/*.gni changes
  2. GN vs `build.ninja` timestamp comparison (catches changes outside the time window)
  3. Recent modification time check (last N minutes, default 30)

  If any check fails, recommends standard build. Defaults to full build when uncertain.
  **Use when**: Q1 is unresolved — user is unsure whether GN files changed.
  **Skip when**: user explicitly confirmed only .cpp/.ts/.ets changes, or Q1 already resolved.

- **`${SKILL_BASE_DIR}/scripts/monitor_progress.sh`** `[--interval <seconds>] [--root <path>] [--product <name>] [--check]` — Monitor an ongoing build by tailing `build_console.log`. Prints `[current/total]` with progress bar every 1s (configurable via `--interval`). Auto-detects build completion or failure.
  With `--check`: non-interactive probe — prints status (`active`/`completed`/`failed`/`stale`/`no_log`) and exits. Exit 0 = build active; exit 1 = no active build.
  **Use when**: always after launching a build via setsid. Use `--check` before launching to detect a running build.
  **Skip when**: build is expected to complete in <30s (e.g., single small target with `--fast-rebuild`).
