# Engineering Workflow Guide

How to execute each phase of the 7-phase adaptation workflow with engineering discipline. This guide provides process methodology — the "HOW" — while the main SKILL.md provides domain knowledge — the "WHAT".

## Phase 1–3: Parallel Exploration

### Principle
The three analysis phases involve independent data collection. Run them in parallel, not sequentially.

### How to Execute

Dispatch three parallel exploration tasks simultaneously:

```
Task 1: Read .d.ts file, extract API inventory, count interfaces
Task 2: Search manifest XML + plugins/ for repository mapping  
Task 3: Check plugins/ directory for existing adapted code
```

### Rules
- Once exploration tasks are dispatched for a search, do NOT perform the same search manually. Wait for results, then synthesize.
- If you have independent work while waiting, do it. Otherwise, wait.

---

## Phase 4: Resolving Ambiguous Modules

### When to Pause and Think Deeper

Only when a module sits on the boundary between architecture modes:
- Module has BOTH data access AND platform control (e.g., `@ohos.settings`)
- C/C++ purity is unclear (some platform calls but mostly portable)
- Platform dependency ratio is between 30-70%

### How to Resolve

Ask these questions explicitly before choosing a mode:

```
1. Is {module} better suited for OHOS Reuse or Hybrid mode?
2. It has {X}% data access APIs and {Y}% platform-specific APIs
3. Platform-specific functions: {list}
4. Risk factors: {iOS limitations, Android permissions}
5. What happens if we choose wrong? (cost of reversal)
```

### When NOT to Pause
- Pure data modules (preferences, RDB, crypto) → Always OHOS Reuse
- Heavy platform modules (bluetooth, camera) → Always Independent
- Clear-cut cases → Proceed directly

---

## Phase 5: Execution Plan Structure

### Always Write a Plan

After architecture mode selection, convert the recommendation into a structured execution plan before coding.

### Plan Template

Save to `.arkuix-adaptation/{module}-plan.md`:

```markdown
# {Module} Cross-Platform Adaptation Plan

## Mode: {OHOS Reuse | Hybrid | Independent}
## Estimated: {lines} new code, {weeks} timeline

## Tasks

### Task A: Shared Layer [no dependency]
- Scope: NAPI bindings, constants, pure virtual interface
- Files: {list}
- Success: Compiles on all platforms
- Depends on: none

### Task B: Android Implementation [depends on Task A]
- Scope: JNI adapter, Java plugin
- Files: {list}
- Success: Android build passes, getValue/setValue functional
- Depends on: Task A (interface)

### Task C: iOS Implementation [depends on Task A]
- Scope: ObjC++ adapter
- Files: {list}
- Success: iOS build passes, getValue/setValue functional
- Depends on: Task A (interface)

### Task D: Configuration Files [depends on Task A]
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

---

## Phase 6: Parallel Implementation

### Task Dispatch Pattern

Break the plan into independent tasks and execute them in parallel:

```
Task A (shared layer): NAPI bindings + constants + pure virtual interface
Task B (Android):      JNI adapter + Java plugin  
Task C (iOS):          ObjC++ adapter
Task D (config):       4 mandatory configuration files

→ A executes first
→ After A completes: B, C, D execute in parallel
→ After all complete: verify each task's output
```

### Task Prompt Template

Each task should specify:

```
TASK: Implement {platform} platform adapter for @{module}

EXPECTED OUTCOME:
- {platform} adapter compiles successfully
- All {N} APIs from Phase 3 DTS analysis are implemented
- Follows existing pattern from plugins/{reference_module}/

MUST DO:
- Read reference implementation: plugins/{reference_module}/{platform}/
- Implement all methods listed in {module}_adapter.h
- Use platform-specific APIs: {Android: JNI | iOS: ObjC++}
- Add error handling for unsupported features
- Update BUILD.gn for this platform

MUST NOT DO:
- Modify shared NAPI binding code (Task A owns this)
- Touch other platform's implementation
- Skip error handling for unsupported platform features
- Suppress type errors
```

### Result Collection Protocol

1. Dispatch all independent tasks in parallel
2. Continue non-overlapping work while waiting (e.g., write documentation)
3. Wait for completion notifications
4. Collect and verify each task result
5. If verification fails: send fix instructions with specific error details

---

## Phase 6: Test-Driven Approach

### When to Use

Recommended for core data access APIs (getValue/setValue family) where behavioral parity is critical across platforms.

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

---

## Phase 6: Debugging Build Failures

### Protocol

```
1. Read the error message carefully
2. Identify the category:
   - Include path error → Check BUILD.gn deps and include paths
   - Linker error → Check source file registration in GN
   - Platform macro error → Check IS_ARKUI_X_TARGET / ANDROID_PLATFORM / IOS_PLATFORM
   - NAPI binding error → Check napi_value type conversions
3. Fix the root cause (not the symptom)
4. Re-verify after EVERY fix attempt
5. After 3 consecutive failures: STOP, revert, document what was attempted
```

### Common Build Errors

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `fatal error: 'xxx.h' file not found` | Missing include path in BUILD.gn | Add `include_dirs` to GN target |
| `undefined reference to xxx` | Source file not in GN sources list | Add `.cpp` to `sources` in BUILD.gn |
| `use of undeclared identifier 'ANDROID_PLATFORM'` | Missing platform guard | Add `#ifdef IS_ARKUI_X_TARGET` |
| `no viable conversion from napi_value to X` | NAPI type extraction error | Use correct `napi_get_value_*` API |

---

## Verification Before Completion

### Evidence Checklist

Before declaring any task complete, collect evidence:

- [ ] `lsp_diagnostics` on all changed/created files — no errors
- [ ] Build command exits with code 0 (if applicable)
- [ ] 4 mandatory config files verified:
  - `plugin_lib.gni` has module entry
  - `apiConfig.json` has library entry
  - `arkui_cross_sdk_description_std.json` has build entry
  - `.d.ts` has `@crossplatform` annotations on adapted interfaces
- [ ] No type error suppression (`as any`, `@ts-ignore`)
- [ ] No empty catch blocks

### Principle: No Evidence = Not Complete

If any check fails, the task is NOT complete. Fix and re-verify. Never claim completion without running verification.
