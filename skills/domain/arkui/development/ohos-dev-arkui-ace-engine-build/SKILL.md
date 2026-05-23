---
name: ohos-dev-arkui-ace-engine-build
description: Build the OpenHarmony ACE Engine and related components. Use when the user asks to build or compile OpenHarmony, ace_engine, ace_engine_test, or any component/target. Handles full system builds, component builds, test builds with coverage, fast rebuild (skip GN), SDK builds, and test list builds from unittest_targets.txt. Trigger keywords include "编译", "build", "compile", "快速编译", "fast-build", "编译测试", "编译测试用例", "编译覆盖率", "build coverage", "编译 sdk", "build sdk", "编译测试列表", "build test list", "按列表编译测试", "编译指定测试", and any mention of building the OpenHarmony codebase.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: ace-engine-build
  version: 0.1.0
  status: trial
---

# ACE Engine Build

Build OpenHarmony ACE Engine and related components using the `build.sh` build system.

## Environment

- Build script: `./build.sh` in OpenHarmony root (identified by `.gn` file)
- Build system: hb (Harmony Build)
- Output: `out/<product>/` (SDK special case: `out/sdk/`, NOT `out/ohos-sdk/`)

Find root dynamically:
```bash
find_oh_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir")"
        [[ "$dir" == "/" ]] && { echo "Error: .gn not found" >&2; return 1; }
    done
    echo "$dir"
}
```

## Build Decision Tree

Before building, answer these questions in order:

**Q1: What changed?**
- Source code only (.cpp/.h/.ts/.ets) → `--fast-rebuild`
- BUILD.gn / *.gni modified → full build (**NEVER** `--fast-rebuild` — will silently use stale ninja files and produce incorrect output)
- First build ever → full build
- Not sure → run `scripts/check_fast_rebuild.sh [minutes]` to check

**Q2: What to verify?**
- "Does it compile?" → `--build-target ace_engine`
- "Do tests pass?" → `--build-target ace_engine_test` with coverage (see Q3)
- "Is the full system ok?" → full build (no `--build-target`)
- "Is SDK affected?" → `--product-name ohos-sdk` (**NEVER** specify `--build-target` — causes cryptic failures)
- "Multiple specific tests?" → Test list build from `unittest_targets.txt`

**Q3: Coverage?**
- **NEVER** skip `--gn-args ace_engine_feature_enable_coverage=true` for ace_engine test builds — coverage is zero-cost and always valuable
- Only applies to ace_engine targets; safe with global `unittest` (other repos unaffected)
- Use simple target name (e.g. `ui_content_stub_unittest`), **NEVER** GN path format (`//path:target`)

**Q4: Build failed?**
- Check `out/<product>/build.log` for errors
- Use error analysis skill if available, otherwise: `grep -i "error:" out/<product>/build.log | tail -50`

**Result — compose the command:**
```
./build.sh --export-para PYCACHE_ENABLE:true --product-name <PRODUCT> [--build-target <TARGET>] [--gn-args ...] --ccache [--fast-rebuild]
```

| Scenario | Command |
|----------|---------|
| Full build | `./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache` |
| Code-only changes | Add `--fast-rebuild` to any command |
| ACE Engine component | Add `--build-target ace_engine` |
| ACE Engine tests | `--build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true` |
| Fast test iteration | `--build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true --fast-rebuild` |
| SDK | `--product-name ohos-sdk` (no `--build-target`) |

Products: `rk3568`, `rk3588`, `ohos-sdk` | Targets: `ace_engine`, `ace_engine_test`, `unittest`, `benchmark_linux`

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
├── <product>/
│   ├── packages/          # Built packages
│   ├── libs/              # Compiled libraries
│   ├── tests/ace_engine/unittest/<path>/<test_target_name>
│   ├── exe.unstripped/tests/unittest/ace_engine/  # Safe to delete for disk space
│   └── build.log          # Primary build log
└── sdk/                   # SDK output (ohos-sdk only, NOT out/ohos-sdk/)
```

## Scripts

- **`scripts/check_fast_rebuild.sh`** `[--root <path>] [--product <name>] [minutes]` — Three-stage safety check before using `--fast-rebuild`:
  1. `git status` for uncommitted BUILD.gn/*.gni changes
  2. GN vs `build.ninja` timestamp comparison (catches changes outside the time window)
  3. Recent modification time check (last N minutes, default 30)

  If any check fails, recommends standard build. Defaults to full build when uncertain.
