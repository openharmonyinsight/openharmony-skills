---
name: ohos-dev-arkuix-framework-api-adapter
description: >
  Guide OHOS modules cross-platform adaptation with automated architecture analysis, code sync, configuration generation, and E2E verification. Use for adapting OHOS subsystem modules (@ohos.data.preferences, @ohos.intl, @ohos.multimedia.image, etc.) to Android/iOS. Provides 7-phase workflow: info collection → code sync → API analysis → architecture analysis → recommendation → implementation → E2E verification. Also covers app-level NAPI platform extension (平台扩展) for developers without OHOS source code — uses CMake + Gradle/Xcode instead of BUILD.gn. Includes automated scripts for DTS analysis, architecture analysis, and configuration generation.
  Do NOT use for: adapting existing C++ native modules to Android/iOS (use arkuix-cpp-adapter instead).
  触发关键词："模块适配"、"跨平台适配"、"架构模式分析"、"DTS分析"、"E2E验证"、
  "平台扩展"、"扩展@ohos"、"NAPI平台扩展"、"app-level adaptation"、
  "module adaptation"、"architecture analysis"、"OHOS cross-platform"、"cross-platform test"、
  "platform extension"、"nm_modname"、"CMake配置"、"五层架构"。
---

# ArkUIX Framework API Adapter Skill

## Mandatory Constraints (Read Before Starting)

### 1. Interface Signature Compatibility

Adapted APIs **MUST** have signatures identical to the OHOS SDK d.ts definition. Zero deviation allowed.

- **Method names**: exact match with d.ts
- **Parameter order**: exact match with d.ts
- **Parameter types**: exact match with d.ts
- **Return types**: exact match with d.ts
- **Import method**: `import xxx from '@ohos.xxx'` — developers must NOT need to import any `.so` file

**Rationale**: Developers use the same API regardless of platform. If a signature differs, the module is NOT adapted — it's reimplemented with incompatibility.

### 2. Return Values and Error Codes

Return values and error codes **MUST** follow the OHOS original module's convention:

- If OHOS uses `BusinessError` with error codes → adapter uses the same error codes
- If OHOS uses int return values (0 = success, -1 = failure) → adapter uses the same pattern
- If OHOS uses Promise rejection with specific error objects → adapter produces the same error objects
- **Never invent custom error codes** — always reference the OHOS source implementation

### 3. Execution Environment

This skill executes within an **ArkUI-X SDK source tree** (contains `.repo/`, `plugins/`, `interface/`). If you are in an application project (contains `entry/`, `.arkui-x/`), use `arkuix-ohosapi-platform-extension` instead.

## 7-Phase Workflow

### Artifact Directory

All phase outputs are stored as `.md` files under `.arkuix-adaptation/`, named by module. If a module's files exist, it has been partially adapted — **read existing artifacts before starting any phase to determine resume point**.

```
.arkuix-adaptation/
├── settings-info.md              # Phase 1: 模块身份信息
├── settings-api-inventory.md     # Phase 3: API 接口清单 + 覆盖率
├── settings-architecture.md      # Phase 4: 架构分析报告
├── settings-plan.md              # Phase 5: 执行计划 + 测试用例规格
└── settings-e2e-report.md        # Phase 7: E2E 验证报告
```

**Naming rule**: `{module_short_name}-{purpose}.md`, where `module_short_name` is the last segment of the `@ohos.*` path (e.g., `@ohos.data.preferences` → `preferences`, `@ohos.settings` → `settings`).

### Resume Protocol

Before starting ANY phase, check for existing artifacts:

```
1. ls .arkuix-adaptation/{module_short_name}-*.md → which phase files exist?
2. Read the latest phase file → is it complete?
3. Resume from the NEXT incomplete phase
4. Do NOT re-run completed phases (read their output instead)
```

| File exists & complete | Meaning | Action |
|---|---|---|
| `{module}-info.md` | Phase 1 done | Read module name, skip Phase 1 |
| `{module}-api-inventory.md` | Phase 3 done | Read API list, skip Phase 1–3 |
| `{module}-architecture.md` | Phase 4 done | Read dependency ratio, skip Phase 1–4 |
| `{module}-plan.md` | Phase 5 done | Read plan + test spec, skip Phase 1–5 |
| `{module}-e2e-report.md` | All done | Read report, verify all PASS |

### Before Starting Adaptation, Ask Yourself

- **Module type**: Is this a data module (preferences, RDB) or platform-service module (bluetooth, camera)? This determines the architecture mode.
- **C/C++ purity**: Is the core logic pure C/C++ with no platform APIs? If yes → likely OHOS Reuse with zero platform code.
- **DTS coverage**: Does the .d.ts already have `@crossplatform` annotations? If yes → some work already done.
- **Reference implementation**: Is there an existing adapted module in `plugins/` you can reference?

### Phase → Superpowers Mapping

Each phase integrates with superpowers process skills for discipline and parallelism:

| Phase | Superpowers / Skills | Purpose |
|-------|-----------|---------|
| Phase 1–3 | `dispatching-parallel-agents` | Parallel exploration (d.ts, manifest, plugins/) |
| Phase 4 | `brainstorming` (if ambiguous) | Resolve boundary cases before mode selection |
| Phase 5 | `writing-plans` | Formalize recommendation into execution plan |
| Phase 6 | `subagent-driven-development` | Android/iOS/OHOS implementations in parallel |
| Phase 6 | `test-driven-development` | Write tests before implementation |
| Phase 6 (errors) | `systematic-debugging` | Structured debugging on build failures |
| **Phase 7** | **`arkuix-e2e-test`** | **End-to-end verification: build → overlay SDK → test project → deploy → validate** |
| Post Phase 7 | `verification-before-completion` | Evidence-based completion check |

**MANDATORY — READ for full details**: [references/superpowers-workflow.md](references/superpowers-workflow.md)

### Phase 1–2: Information Collection & Code Sync

Collect module identity, then **obtain OHOS source code for architecture analysis**. OHOS implementation must be analyzed regardless of the final adaptation strategy — even if you end up not reusing any OHOS code, understanding the original implementation is mandatory for informed decision-making.

**Must collect**: Module name (e.g., `@ohos.data.preferences`), subsystem path, GitCode repo name.

**Where to find**: `.d.ts` at `interface/sdk-js/api/@ohos.{module}.d.ts` → manifest at `.repo/manifests/openharmony.xml` → repo at `https://gitcode.com/openharmony/{repo}`.

**Code Sync — mandatory steps**:

1. **Check `openharmony.xml`** for the module's OHOS repository entry:
   ```bash
   grep -i "{module_or_repo_name}" .repo/manifests/openharmony.xml
   ```
2. **If found** → OHOS source already configured, analyze code directly at the mapped `path`:
   ```
   # Example: grep finds this line:
   # <project path="foundation/distributeddatamgr/preferences"
   #         name="distributeddatamgr_preferences" remote="openharmony" .../>
   # → Source code is at: foundation/distributeddatamgr/preferences/
   ```
3. **If NOT found** → ask developer for GitCode repository info, then configure and sync:
   ```bash
   # Developer provides: repo name (e.g., "startup_init") + local path (e.g., "base/startup/init")
   # Add to .repo/manifests/openharmony.xml:
   #   <project path="{local_path}" name="{repo_name}" remote="openharmony" revision="weekly_YYYYMMDD" />
   # Then sync:
   repo sync {local_path}
   ```

**MANDATORY — READ**: [references/phase1-information-collection.md](references/phase1-information-collection.md) and [references/phase2-code-sync.md](references/phase2-code-sync.md). **Do NOT load** other phase references yet.

**⚡ Parallel Exploration**: Dispatch 3 explore agents simultaneously:
1. Read `.d.ts` for API inventory
2. Search `openharmony.xml` for repository mapping
3. Check `plugins/` for existing adapted code

**Output**: Write to `.arkuix-adaptation/{module}-info.md` (template: [references/output-templates.md](references/output-templates.md) § Phase 1)

### Phase 3: API Interface Analysis

Analyzes `.d.ts` file to determine `@crossplatform` coverage.

**Metrics**:
- Total interface count (by category)
- Adapted vs needs adaptation counts
- Coverage percentage
- Detailed list of interfaces needing adaptation

**Output**: Write to `.arkuix-adaptation/{module}-api-inventory.md` (template: [references/output-templates.md](references/output-templates.md) § Phase 3)

**Automation**: `scripts/dts_analyzer.py interface/sdk-js/api/@ohos.{module}.d.ts`

**MANDATORY — READ**: [references/phase3-api-analysis.md](references/phase3-api-analysis.md) — detailed DTS analysis workflow and coverage interpretation.
**Do NOT load** phase4 or phase5 references yet.

**⚡ Parallel with Phase 1–2**: This analysis can run concurrently with Phase 1 exploration agents.

### Phase 4: Architecture Analysis

Understand module composition to inform mode selection. This is an **exploratory** phase — the right questions matter more than exact metrics.

**Step 0: Check Existing Adaptation** (run BEFORE analyzing OHOS source)

Phase 1-2 may have found existing adapted code in `plugins/`. This changes Phase 4's scope:

| # | `openharmony.xml` | `plugins/` | Phase 4 Action |
|---|-------------------|------------|----------------|
| A | ✅ OHOS source available | ❌ No adaptation | Full analysis of OHOS source → determine architecture mode → full adaptation |
| B | ✅ OHOS source available | ✅ Partial adaptation | Analyze OHOS source **AND** existing `plugins/` code → determine if existing mode is correct → supplement remaining APIs in same pattern |
| C | ✅ OHOS source available | ✅ Already complete | **Skip Phase 4-6** → go directly to Phase 7 E2E verification |
| D | ❌ No OHOS source | ✅ Already adapted | Analyze existing `plugins/` code only → understand the architecture mode used |

```bash
# Quick check for existing adaptation
ls plugins/{module_dir}/
ls plugins/{module_dir}/android/ plugins/{module_dir}/ios/ 2>/dev/null
```

**Core Questions to Answer** (only if Step 0 determines analysis is needed):

1. **How much of this module is pure C/C++?** — Scan for `std::`, third-party libs (sqlite, libxml2, openssl), file I/O. If >90% → likely zero platform code needed.
2. **Where does it touch the OS?** — Search for `OHOS::`, `hilog`, `safwk`, system service calls. Each hit = potential platform adapter needed.
3. **What does the dependency tree look like?** — `grep "#include"` + BUILD.gn `deps`. Deep OHOS dependency chains → harder to reuse.

**Expert Heuristics** (non-obvious):

| Signal | Interpretation |
|--------|---------------|
| Module uses SQLite / libxml2 / OpenSSL | Pure C++ — portable, OHOS Reuse with ~50 lines path config |
| Module has `services/platform/` directory | Already has platform abstraction — likely OHOS Reuse |
| NAPI bindings > 2000 lines | Heavy JS↔C++ bridge — consider if all APIs are worth adapting |
| Module calls `DataObsMgrClient` or similar IPC | Platform-specific notification system — needs adapter |
| Module depends on `safwk` (System Ability) | OHOS service framework — requires service abstraction (Hybrid) |
| Module has hardware-specific code (BLE, camera HAL) | Platform-heavy — Independent mode likely |

**Key Rule**: C/C++ Cross-Platform Native Support
- Many data modules (preferences, RDB, crypto) are pure C/C++ and require **zero** platform-specific implementation
- Only path/configuration differences needed (~50 lines per platform)
- **Do NOT over-engineer**: if the code compiles on Android/iOS with only path changes, OHOS Reuse mode with no adapter is the correct choice

**Output**: Write to `.arkuix-adaptation/{module}-architecture.md` (template: [references/output-templates.md](references/output-templates.md) § Phase 4)

**Automation**: `scripts/architecture_analyzer.py foundation/{module_path}`

**MANDATORY — READ**: [references/phase4-architecture-analysis.md](references/phase4-architecture-analysis.md) — complete analysis dimensions and C/C++ native assessment.
**MANDATORY — READ**: [references/architecture-modes.md](references/architecture-modes.md) — three architecture modes with detailed comparison.

**⚡ Brainstorming (if ambiguous)**: For modules on the boundary between modes (e.g., settings = data access + platform control), invoke brainstorming to clarify classification before proceeding.

### Phase 5: Architecture Recommendation

Recommends adaptation mode based on analysis: **OHOS Reuse** / **Independent** / **Hybrid**

**Decision Matrix**:

| Mode | Code Reuse | New Code | Time | Best For |
|------|------------|----------|------|----------|
| OHOS Reuse | 90-95% | 500-800 lines | 4-6 weeks | Data-focused (preferences, kv_store) |
| Hybrid | 60-80% | 1,500-2,500 lines | 6-10 weeks | Mixed (location, sensor) |
| Independent | 10-30% | 4,000-6,000 lines | 10-16 weeks | Platform-heavy (BLE, pasteboard) |

**Boundary Cases — When the Decision Isn't Obvious**:

Modules on the mode boundary require judgment. Use these expert heuristics:

| Module Characteristic | Lean Toward | Because |
|----------------------|-------------|---------|
| Data access + platform control (e.g., `@ohos.settings`) | OHOS Reuse | Read/write is 90% data; platform control APIs can be stubbed |
| Has `services/platform/` but also heavy NAPI | OHOS Reuse | Platform abstraction already exists → thin adapter |
| Uses IPC but only for notifications | Hybrid | Notification system needs adapter but core logic is portable |
| Network stack with platform certificate handling | Hybrid | Core protocol is portable, only cert path is platform-specific |
| Media playback with hardware codec | Independent | Hardware codec access is entirely platform-specific |
| Module depends on 3+ OHOS system abilities | Independent | Deep system integration = fragile reuse |

**The 60/40 Rule**: If you're unsure between two modes, choose the one with more code reuse. It's always easier to add platform adapters later than to maintain duplicated code. Only override this if the module has >3 hard platform dependencies.

**Output**: Recommended mode with rationale, effort estimates, and test case specification

**⚡ Writing Plans + Test Cases**: After mode selection, produce TWO deliverables:

#### Deliverable 1: Execution Plan

Write to `.arkuix-adaptation/{module}-plan.md`. Single file containing BOTH execution plan AND test spec:

1. Decompose into parallel work units based on chosen mode:
   - **OHOS Reuse**: Task A = shared NAPI + interface, Task B = OHOS wrapper, Task C = path config
   - **Hybrid**: Task A = shared layer, Task B = Android impl, Task C = iOS impl, Task D = config files
   - **Independent**: Task A = Android impl, Task B = iOS impl, Task C = OHOS impl, Task D = config files
2. Include success criteria per task (compile, tests, config file completeness)

#### Deliverable 2: E2E Test Case Specification

Write to the SAME file `{module}-plan.md`, in the "## E2E 测试用例规格" section:

For EVERY API in Phase 3's inventory, write a test case with:
- **Test ID**: `test{ApiName}{NNN}`
- **API signature**: from Phase 3
- **Input**: concrete test parameters
- **Expected behavior per platform**: Android / iOS / OHOS (may differ)
- **Expected failure mode**: what happens on unsupported platforms

Group test cases by **parity group** (platform behavior alignment):
- `all_platforms_same`: identical behavior across all 3 platforms
- `ios_differs`: iOS throws or returns different value
- `android_only` / `ohos_only`: only available on one platform

These test cases become the **input for Phase 7.3** (auto-generate test code) and the **acceptance criteria for Phase 7.5** (validate results).

Template: [references/output-templates.md](references/output-templates.md) § Phase 5

### Phase 6: Implementation Guidance

Generate production-ready code based on the chosen architecture mode.

**MANDATORY — READ ENTIRE FILE**: [references/code-examples.md](references/code-examples.md) — production-ready code templates for ALL layers (pure virtual interface, OHOS wrapper, Android JNI, iOS ObjC++, NAPI bindings, unit tests). **DO NOT implement without reading this file first — it contains the exact patterns, boilerplate, and platform-specific API usage needed for each layer.**

**Implementation order**:
1. Define pure virtual interface (`{module}_adapter.h`)
2. Implement OHOS thin wrapper (`{module}_adapter_ohos.cpp`)
3. Implement Android JNI adapter (`{module}_adapter_android.cpp`)
4. Implement iOS ObjC++ adapter (`{module}_adapter_ios.mm`)
5. Update build configuration (GN templates)
6. Generate 4 mandatory configuration files
7. Write unit tests

**Automation**: `scripts/code_generator.py {module} {repo} --api-version {ver}`

**MANDATORY — READ ENTIRE FILE**: [references/phase6-implementation-guide.md](references/phase6-implementation-guide.md) — complete implementation workflow.
**MANDATORY — READ ENTIRE FILE**: [references/code-examples.md](references/code-examples.md) — production-ready code templates for ALL layers (Android JNI, iOS ObjC++, OHOS wrapper, NAPI bindings). **DO NOT implement without reading this file first — it contains the exact patterns and boilerplate needed for each platform.**
**Do NOT load** phase1-4 references — already completed.

**Output**: Production-ready code with comprehensive error handling

**⚡ Subagent-Driven Development**: Dispatch parallel implementation tasks:

```
Phase 5 Plan → Decompose into independent tasks:
  Task A (deep): NAPI bindings + constants + pure virtual interface [shared]
  Task B (deep): Android SettingsProvider (JNI + Java)           [load_skills: ohos-dev-cpp-coding-style]
  Task C (deep): iOS SettingsProvider (ObjC++)                   [load_skills: ohos-dev-cpp-coding-style]
  Task D (quick): 4 mandatory configuration files                [load_skills: arkuix-framework-api-adapter]
→ All 4 tasks run in parallel (run_in_background=true)
→ After completion: verify each task's output
```

**⚡ Test-Driven Development** (recommended for core data layer):
1. Write getValue/setValue cross-platform test cases first
2. Implement platform-specific backends to pass tests
3. Ensures behavioral parity across Android/iOS/OHOS

**⚡ Systematic Debugging** (on build failures):
1. Check include paths → GN dependency declarations → platform macros
2. After 3 consecutive failures: STOP, revert, consult Oracle
3. Never shotgun-debug random changes

**⚡ Verification Before Completion**: Before marking any phase done:
- [ ] `lsp_diagnostics` clean on all changed files
- [ ] Build passes on target platform (if applicable)
- [ ] 4 mandatory config files verified complete
- [ ] `@crossplatform` annotations added to d.ts
- No evidence = not complete

### Phase 7: End-to-End Verification

**Uses `arkuix-e2e-test` skill for full pipeline verification.**

After Phase 6 generates code, verify it actually works on real devices/emulators.

**MANDATORY — load skill**: `skill(name="arkuix-e2e-test")` before starting this phase.

**Sub-phases**:

#### 7.1 Build Framework
```bash
./build.sh --product-name arkui-x --target-os android
./build.sh --product-name arkui-x --target-os ios
```
On failure: report error to developer. Do NOT proceed.

#### 7.2 Overlay SDK
Replace local SDK with build output containing the newly adapted module:
```bash
BUILD_ZIP=$(ls out/arkui-x/packages/arkui-x/$(uname -s | tr '[:upper:]' '[:lower:]')/arkui-x-*.zip | head -1)
SDK_TARGET="{SDK_ROOT}/{apiVersion}/arkui-x"
# Backup → Extract → Replace
```

#### 7.3 Create Test Project + Generate Test Code
Use Phase 5's test case specification (not raw API inventory) to generate test code:

```
Phase 5 Test Case Specification          Phase 7.3 Test Code
┌──────────────────────────────┐     ┌────────────────────────────────┐
│ testGetValue001              │     │ await test('getValue', ...)    │
│   Android → Build.MODEL      │     │   // platform assertion built  │
│   iOS → UIDevice.name        │────►│   // from Phase 5 spec         │
│ testSetValueWithDomain001    │     │ await test('setValue', ...)    │
│   roundtrip verify           │     │   // roundtrip per spec        │
│ testEnableAirplaneMode001    │     │ await test('airplane', ...)    │
│   iOS → throws unsupported   │     │   // iOS expects error         │
│ 30+ test cases from Phase 5  │     │ 30+ test functions generated   │
└──────────────────────────────┘     └────────────────────────────────┘
```

```bash
ace create project  # e2eTest project
```

Test code pattern: one `async test(name, fn)` function per adapted API, with platform-specific assertions derived from Phase 5 test spec. Template: [references/output-templates.md](references/output-templates.md) § Phase 7 Test Code.

#### 7.4 Build & Run
```bash
ace build apk && ace run apk   # Android
ace build app && ace run app   # iOS
```

#### 7.5 Validate Results
- [ ] App launches without crash
- [ ] All test cases show ✅ (PASS)
- [ ] No SIGABRT / SIGSEGV in crash logs
- [ ] Android: `adb logcat | grep -E "PASS|FAIL|ERROR|Fatal"` clean
- [ ] iOS: `log stream` no module-related errors

**Output**: Write to `.arkuix-adaptation/{module}-e2e-report.md` (template: [references/output-templates.md](references/output-templates.md) § Phase 7)

**⚡ If validation fails**: Use `systematic-debugging` — do NOT shotgun-fix. After 3 failures, revert and consult Oracle.

## NEVER Do

- **NEVER** skip Phase 4 architecture analysis before choosing a mode — wrong mode selection (e.g., Independent for a pure C/C++ data module) wastes weeks of work
- **NEVER** choose Independent mode for pure C/C++ modules (preferences, kv_store, RDB, crypto) — they need zero platform-specific code, only ~50 lines of path/config differences per platform
- **NEVER** forget to update all 4 mandatory configuration files — missing any one causes silent build failures: `plugin_lib.gni`, `apiConfig.json`, `arkui_cross_sdk_description_std.json`, `@ohos.{module}.d.ts`
- **NEVER** start Phase 6 implementation without completing Phase 3 DTS analysis — you won't know which interfaces need adaptation
- **NEVER** hardcode module paths — use the naming patterns from config.json (`{subsystem}_{module}` or `{module}`)
- **NEVER** skip `--dry-run` when running code_generator.py — always preview changes before applying
- **NEVER** assume a module fits only one architecture mode — hybrid modules (geolocation, sensor) have mixed characteristics requiring careful Phase 4 analysis
- **NEVER** sync OHOS code without verifying the repository exists on GitCode first — `https://gitcode.com/openharmony/{repo}`
- **NEVER** implement Phase 6 sequentially — always parallelize Android/iOS/OHOS via subagent-driven-development
- **NEVER** skip Phase 7 E2E verification — code that compiles is not code that works. Must validate on real device/emulator
- **NEVER** skip Phase 7.5 log validation — "no crash" ≠ "works correctly". Verify side effects, not just absence of errors
- **NEVER** use app-level platform extension for modules with `@crossplatform` tags — the framework's built-in `.so` will silently overwrite your app-level code, making it completely non-functional. Always `grep -c "@crossplatform" @ohos.<module>.d.ts` first
- **NEVER** define `ANDROID_PLATFORM` macro via `arguments` in `build.gradle` — must use `cppFlags "-DANDROID_PLATFORM=1"`. CMake cache at `.arkui-x/android/app/.cxx/` must be wiped after config changes

## Automated Scripts

```bash
python3 scripts/dts_analyzer.py interface/sdk-js/api/@ohos.{module}.d.ts       # Phase 3: coverage
python3 scripts/architecture_analyzer.py foundation/{module_path}               # Phase 4: architecture
python3 scripts/code_generator.py {module} {repo} --api-version {ver} [--dry-run]  # Phase 6: code gen
```

## Evaluation Test Suite

25 evaluation cases across 5 categories validate this skill works correctly.

```bash
python3 tests/test_scripts.py   # Category A: 10 automated script tests
bash tests/run_tests.sh          # Full suite (automated + manual scenario index)
```

**Scenario-based cases** (B/C/D/E) are documented in `tests/` as `.md` files for manual evaluation:

| Category | Cases | Tests |
|----------|-------|-------|
| A: Script Functional | 10 | `test_scripts.py` (automated) |
| B: Decision Trees | 8 | `test_decision_trees.md` (Scenario A/B/C/D, mode selection, boundary) |
| C: Constraint Enforcement | 4 | `test_constraints.md` (signatures, naming, config completeness) |
| D: NEVER List | 3 | `test_never_and_triggers.md` (anti-pattern prevention) |
| E: Skill Triggering | 2 | `test_never_and_triggers.md` (activation + negative tests) |

## Architecture Modes Quick Reference

Full details: [references/architecture-modes.md](references/architecture-modes.md)

| Mode | Reuse | Best For | Example Modules |
|------|-------|----------|----------------|
| OHOS Reuse | 90-95% | Pure data / C++ modules | preferences, kv_store, http |
| Hybrid | 60-80% | Mixed data + platform | geolocation, sensor, request |
| Independent | 10-30% | Heavy platform APIs | bluetooth, pasteboard, camera |

## Implementation Checklist

Full checklist with per-phase items: [references/implementation-checklist.md](references/implementation-checklist.md)

## Mandatory Configuration Files

After code generation, ensure all 4 files are updated. **Exact format and naming rules**: [references/config-files-format.md](references/config-files-format.md)

- [ ] `plugins/plugin_lib.gni` - Module entry (directory path under plugins/)
- [ ] `interface/sdk/plugins/api/apiConfig.json` - Library configuration (module name matches d.ts)
- [ ] `build_plugins/sdk/arkui_cross_sdk_description_std.json` - Build entries (GN target labels)
- [ ] `interface/sdk-js/api/@ohos.{module}.d.ts` - @crossplatform annotations

**⚠️ Naming pitfall**: d.ts module name may use camelCase (`deviceInfo`) while directory uses snake_case (`device_info`). Cross-check all 4 files character by character.

## Plugin Directory Structure Reference

Real-world directory patterns from `plugins/` for each architecture mode: [references/plugin-directory-reference.md](references/plugin-directory-reference.md)

| Mode | Reference Module | Key Pattern |
|------|-----------------|-------------|
| OHOS Reuse (pure) | `plugins/data/preferences/` | Only BUILD.gn, deps point to OHOS source |
| OHOS Reuse (with adapters) | `plugins/device_info/` | Shared NAPI + android/java/ + ios/ |
| Hybrid | `plugins/net/http/` | Shared logic + android/ + ios/ |
| Independent | `plugins/pasteboard/` | Full independent + mock/ for OHOS deps |

## Common Failure Patterns (Expert)

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| `libxxx.so` loaded but APIs return undefined | `plugin_lib.gni` entry missing or `nm_modname` mismatch | Verify `.gni` module name matches CMake/BUILD.gn target name exactly |
| Build passes but module not available at runtime | `apiConfig.json` or `arkui_cross_sdk_description_std.json` entry missing/typo | All 4 config files must agree on module name — cross-check character by character |
| Android crash: `SIGSEGV` in NAPI init | `IS_ARKUI_X_TARGET` macro not defined → platform selection macro falls through to `#error` | Add `defines = [ "IS_ARKUI_X_TARGET" ]` in BUILD.gn static library target |
| iOS build: linker error for `_GetAdapterIOS` | `.mm` file not in sources list or framework not linked | Add `.mm` to `sources` + `frameworks = [ "Foundation.framework" ]` in GN target |
| OHOS wrapper compiles but returns wrong values | Forwarding not 1:1 — wrapper adds logic that differs from original | OHOS wrapper must be **zero-logic**: every call is `return Original::Method()` with no transformation |
| `@crossplatform` APIs crash after adaptation | Framework `.so` overwrites app-level `.so` silently | Check d.ts for `@crossplatform` — if present, framework already owns this module, app-level code is dead |
| `repo sync` hangs or 404 | Repository name doesn't match GitCode naming pattern | Try `{subsystem}_{module}`, `{category}_{subsystem}_{module}`, or browse https://gitcode.com/org/openharmony/repos |

## App-Level Platform Extension (Alternative Path)

The 7-phase workflow above requires OHOS framework source code access (`repo sync`, `BUILD.gn`, `plugins/`). If you are working **within an application project** (no OHOS source), use `arkuix-ohosapi-platform-extension` skill instead.

### Decision: Framework-Level vs App-Level

| Aspect | 7-Phase Workflow (this skill) | App-Level Extension |
|--------|-------------------------------|---------------------|
| Working directory | ArkUI-X SDK source tree (`.repo/`, `plugins/`) | Application project (`entry/`, `.arkui-x/`) |
| Requires OHOS source | ✅ Yes (repo sync) | ❌ No |
| Build system | BUILD.gn + GN | CMake + Gradle/Xcode |
| Code location | `plugins/{module}/` | `entry/src/main/cpp/{module}/` |
| SDK config files | 4 mandatory files | CMakeLists.txt only |
| Best for | Framework contributors | Application developers |

**→ If your working directory contains `entry/src/main/`, switch to `arkuix-ohosapi-platform-extension` skill.**

## Related Skills

- **arkuix-ohosapi-platform-extension** - App-level NAPI platform extension for developers without OHOS source code (CMake + Gradle/Xcode)
- **arkuix-e2e-test** - Phase 7 end-to-end verification: build → overlay SDK → test project → deploy → validate
- **superpowers/writing-plans** - For formalizing Phase 5 recommendation into execution plan
- **superpowers/subagent-driven-development** - For parallel Phase 6 implementation
- **superpowers/verification-before-completion** - For evidence-based completion check
