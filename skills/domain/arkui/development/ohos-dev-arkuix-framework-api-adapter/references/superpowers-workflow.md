# Superpowers Integration Guide

## Overview

This document details how the framework-api-adapter 7-phase workflow integrates with superpowers process skills. Framework-api-adapter provides domain knowledge (WHAT to do); superpowers provide engineering discipline (HOW to execute).

## Integration Map

```
Phase 1–3 (Analysis)          Phase 4–5 (Decision)          Phase 6 (Implementation)
┌──────────────────┐     ┌──────────────────────┐     ┌───────────────────────────┐
│ dispatching-     │     │ brainstorming        │     │ subagent-driven-          │
│   parallel-      │     │   (if ambiguous)     │     │   development             │
│   agents         │────►│                      │────►│                           │
│                  │     │ writing-plans         │     │ test-driven-development   │
│ 3x explore       │     │   → .sisyphus/plans/ │     │ systematic-debugging      │
│   agents         │     │                      │     │ verification-before-      │
│   in parallel    │     │                      │     │   completion              │
└──────────────────┘     └──────────────────────┘     └───────────────────────────┘
```

## Phase 1–3: Parallel Exploration

### When to Use
Always. The three analysis phases involve independent data collection that benefits from parallelism.

### How to Dispatch

```
Task 1 (explore, background): Read .d.ts file, extract API inventory, count interfaces
Task 2 (explore, background): Search manifest XML + plugins/ for repository mapping
Task 3 (explore, background): Check plugins/ directory for existing adapted code
```

### Anti-Duplication Rule
Once explore agents are dispatched for a search, do NOT perform the same search manually. Wait for results, then synthesize.

## Phase 4: Brainstorming for Ambiguous Modules

### When to Use
Only when a module sits on the boundary between architecture modes:
- Module has BOTH data access AND platform control (e.g., `@ohos.settings`)
- C/C++ purity is unclear (some platform calls but mostly portable)
- Platform dependency ratio is between 30-70%

### How to Use
```
brainstorming prompt:
  "Is {module} better suited for OHOS Reuse or Hybrid mode?
   - It has {X}% data access APIs and {Y}% platform-specific APIs
   - Platform-specific functions: {list}
   - Risk factors: {iOS limitations, Android permissions}"
```

### When NOT to Use
- Pure data modules (preferences, RDB, crypto) → Always OHOS Reuse
- Heavy platform modules (bluetooth, camera) → Always Independent
- Clear-cut cases → Skip brainstorming, proceed directly

## Phase 5: Writing Plans

### When to Use
ALWAYS after architecture mode selection. Convert the recommendation into a structured execution plan.

### Plan Structure

Save to `.sisyphus/plans/{module}-adaptation.md`:

```markdown
# {Module} Cross-Platform Adaptation Plan

## Mode: {OHOS Reuse | Hybrid | Independent}
## Estimated: {lines} new code, {weeks} timeline

## Tasks

### Task A: Shared Layer
- Scope: NAPI bindings, constants, pure virtual interface
- Files: {list}
- Success: Compiles on all platforms
- Depends on: none

### Task B: Android Implementation
- Scope: JNI adapter, Java plugin
- Files: {list}
- Success: Android build passes, getValue/setValue functional
- Depends on: Task A (interface)
- load_skills: ["ohos-dev-cpp-coding-style"]

### Task C: iOS Implementation
- Scope: ObjC++ adapter
- Files: {list}
- Success: iOS build passes, getValue/setValue functional
- Depends on: Task A (interface)
- load_skills: ["ohos-dev-cpp-coding-style"]

### Task D: Configuration Files
- Scope: 4 mandatory config files
- Files: plugin_lib.gni, apiConfig.json, arkui_cross_sdk_description_std.json, .d.ts
- Success: Module appears in build system
- Depends on: Task A (module name)
```

### Parallelism Rules by Mode

| Mode | Parallel Tasks | Sequential |
|------|---------------|------------|
| OHOS Reuse | B (OHOS wrapper) + C (path config) | A → (B, C) → D |
| Hybrid | B (Android) + C (iOS) + D (config) | A → (B, C, D) |
| Independent | B (Android) + C (iOS) + D (OHOS) | A → (B, C, D) |

## Phase 6: Subagent-Driven Development

### Task Dispatch Template

```
task(
  category="deep",
  load_skills=["arkuix-framework-api-adapter", "ohos-dev-cpp-coding-style"],
  run_in_background=true,
  description="{platform} adapter for {module}",
  prompt="""
  TASK: Implement {platform} platform adapter for @{module}

  EXPECTED OUTCOME:
  - {platform} adapter compiles successfully
  - All {N} APIs from Phase 3 DTS analysis are implemented
  - Follows existing pattern from plugins/{reference_module}/

  REQUIRED TOOLS: read, write, edit, bash, grep, glob

  MUST DO:
  - Read reference implementation: plugins/{reference_module}/{platform}/
  - Implement all methods listed in {module}_adapter.h
  - Use platform-specific APIs: {Android: Settings.System JNI | iOS: NSUserDefaults ObjC++}
  - Add error handling for unsupported features
  - Update BUILD.gn for this platform

  MUST NOT DO:
  - Modify shared NAPI binding code (Task A owns this)
  - Touch other platform's implementation
  - Skip error handling for unsupported platform features
  - Use as any or suppress type errors

  CONTEXT:
  - Pure virtual interface: {module}_adapter.h
  - Reference plugin: plugins/{reference_module}/
  - Platform-specific considerations: {list}
  """
)
```

### Result Collection Protocol

1. Dispatch all tasks with `run_in_background=true`
2. Continue non-overlapping work (e.g., write documentation)
3. Wait for `<system-reminder>` notifications
4. Collect results via `background_output`
5. **Verify each task**: Does it compile? Does it follow existing patterns?
6. If verification fails: use `session_id` to send fix instructions

## Phase 6: Test-Driven Development

### When to Use
Recommended for core data access APIs (getValue/setValue family) where behavioral parity is critical.

### TDD Cycle

```
1. Write test: getValue returns correct value for known setting key
2. Run test → FAIL (no implementation yet)
3. Implement platform-specific getValue
4. Run test → PASS
5. Repeat for setValue, observer, etc.
```

### Cross-Platform Parity Tests

Test cases that MUST produce same behavior on Android/iOS/OHOS:
- getValue with valid key → returns stored value
- getValue with unknown key → returns null/empty
- setValue then getValue → round-trip succeeds
- registerKeyObserver → callback fires on change

## Phase 6: Systematic Debugging

### When to Use
After any build failure during Phase 6 implementation.

### Debugging Protocol

```
1. Read the error message carefully
2. Identify the category:
   - Include path error → Check BUILD.gn deps and include paths
   - Linker error → Check source file registration in GN
   - Platform macro error → Check IS_ARKUI_X_TARGET / ANDROID_PLATFORM / IOS_PLATFORM
   - NAPI binding error → Check napi_value type conversions
3. Fix the root cause (not the symptom)
4. Re-verify after EVERY fix attempt
5. After 3 consecutive failures: STOP, revert, consult Oracle
```

### Common Build Errors

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `fatal error: 'xxx.h' file not found` | Missing include path in BUILD.gn | Add `include_dirs` to GN target |
| `undefined reference to xxx` | Source file not in GN sources list | Add `.cpp` to `sources` in BUILD.gn |
| `use of undeclared identifier 'ANDROID_PLATFORM'` | Missing platform guard | Add `#ifdef IS_ARKUI_X_TARGET` |
| `no viable conversion from napi_value to X` | NAPI type extraction error | Use correct `napi_get_value_*` API |

## Phase 6: Verification Before Completion

### Evidence Checklist

Before declaring any task complete, collect:

- [ ] `lsp_diagnostics` on all changed/created files — no errors
- [ ] Build command exits with code 0 (if applicable)
- [ ] 4 mandatory config files verified:
  - `plugin_lib.gni` has module entry
  - `apiConfig.json` has library entry
  - `arkui_cross_sdk_description_std.json` has build entry
  - `.d.ts` has `@crossplatform` annotations on adapted interfaces
- [ ] No `as any`, `@ts-ignore`, or empty catch blocks

### No Evidence = Not Complete

If any check fails, the task is NOT complete. Fix and re-verify.

## Phase 7: End-to-End Verification (via arkuix-e2e-test)

### When to Use
ALWAYS after Phase 6 code generation. Code that compiles is not code that works.

### Prerequisite
Load the `arkuix-e2e-test` skill: `skill(name="arkuix-e2e-test")`

### Full Pipeline

```
Phase 6 产出                           Phase 7 消费
┌───────────────────────┐          ┌──────────────────────────────┐
│ 适配完成的 C++ 代码    │          │ 7.1 编译框架 (包含新代码)     │
│ 4 个配置文件           │ ──────► │ 7.2 替换 SDK (overlay)       │
│ @crossplatform 注解    │          │ 7.3 建测试工程 + 生成测试代码  │
│ Phase 3 API 清单       │          │ 7.4 编译部署到设备             │
└───────────────────────┘          │ 7.5 日志验证 + crash 检测     │
                                   └──────────────────────────────┘
```

### Test Code Generation from Phase 3 API Inventory

Phase 3 produces a complete API inventory. Use it to auto-generate E2E test cases:

**Mapping rule**: One test function per adapted API.

```
Phase 3 API: getValue(context: Context, name: string): Promise<string>
→ Test: call getValue with known key, verify non-null result

Phase 3 API: setValue(context: Context, name: string, value: string): Promise<boolean>
→ Test: setValue then getValue roundtrip, verify value matches

Phase 3 API: enableAirplaneMode(enable: boolean): Promise<void>
→ Test: call enableAirplaneMode(false), verify no error

Phase 3 API: openDisplaySettingsPage(context: Context): void
→ Test: call openDisplaySettingsPage, verify no crash
```

### Validation Criteria

A module adaptation passes E2E verification when ALL are true:

- [ ] Framework builds successfully with the new module code
- [ ] SDK overlay completes without error
- [ ] Test project compiles on both Android and iOS
- [ ] App launches without crash on both platforms
- [ ] All adapted APIs show PASS in test results
- [ ] No ERROR/Fatal level logs related to the module
- [ ] No SIGABRT/SIGSEGV in crash logs

### Failure Handling

| Failure Point | Action |
|--------------|--------|
| Framework build fails | Fix in Phase 6 code, re-build. Do NOT modify test code. |
| SDK overlay fails | Check version match in arkui-x.json |
| Test project build fails | Check plugin dependency in oh-package.json5 |
| App crashes on launch | Check NAPI module registration + plugin_lib.gni |
| API test returns FAIL | Check platform adapter implementation. Use `systematic-debugging`. |
| Crash logs show SIGABRT | Check NAPI binding — likely null pointer or type mismatch |

### After 3 E2E Failures

STOP. Revert to last known working state. Consult Oracle with:
- Full failure log
- Module architecture mode chosen
- Platform-specific behavior differences observed
