---
name: ohos-dev-arkui-build-error-analyzer
description: >
  Analyze OpenHarmony ArkUI (ACE Engine) build errors from last_error.log and provide fix
  recommendations for undefined symbol (ld.lld), ACE_FORCE_EXPORT, libace.map, ace_core_ng_source_set,
  RefPtr forward declaration, template instantiation, LTO virtual thunk, MinGW dllexport, and BUILD.gn
  configuration issues in the arkui/ace_engine codebase. Use when user says: analyze build errors,
  check compilation errors, diagnose linker errors, fix build issues, build failures, undefined symbols,
  SDK compilation errors, or mentions last_error.log, build.log, ld.lld error, ACE_FORCE_EXPORT,
  libace.map, ace_engine. Supports regular builds and SDK builds. Analysis-only.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: build-error-analyzer
  version: 0.1.0
  status: trial
---

# ArkUI Build Error Analyzer

Analyze ArkUI (ACE Engine) build errors from `last_error.log` and provide **fix recommendations only** (no automatic code modifications).

## Critical Workflow

Follow this exact sequence every time:

1. **Extract errors** from `out/<product>/build.log` using the bundled script
2. **Read** only from `out/<product>/last_error.log` (never read build.log directly)
3. **Check for success** — if content is "build success, no error", stop and report success
4. **Analyze and recommend** — categorize, match patterns, provide fix suggestions

### Extraction Script

```bash
cd <openharmony_root>
# From OpenHarmony root directory:
<skill_dir>/scripts/extract_last_error.sh out/<product>/build.log

# Regular build (e.g., rk3568):
<skill_dir>/scripts/extract_last_error.sh out/rk3568/build.log

# SDK build (NOTE: out/sdk/ NOT out/ohos-sdk/):
<skill_dir>/scripts/extract_last_error.sh out/sdk/build.log
```

The script generates `last_error.log` in the same directory as build.log.

### Success Check

If `last_error.log` contains "build success, no error", **stop immediately** and report:

```
Build succeeded. No errors found in the latest build.
```

If `last_error.log` contains "log read failed" or the extraction script exited non-zero, **do NOT report success** — the log was not read. Fall back to `grep -i "error:" out/<product>/build.log | tail -50` and diagnose manually.

If no `[N/M]` task markers are found in the error block (GN/Ninja configuration errors lack these markers), the extraction script may miss them. Check for GN error patterns directly:

```bash
grep -E "(ERROR at |AssertionError|gn gen failed|ninja: build stopped)" out/<product>/build.log | tail -20
```

Do NOT continue searching in other log files (error.log, build_output*.log, etc.) unless the extraction script failed.

## Behavior Rules

- **Analysis only**: Provide recommendations with file paths, line numbers, before/after code. Never use Edit/Write tools to modify code.
- **Never clear LTO cache**: Never suggest clearing thinlto-cache, llvmcache-*, out/obj, or performing clean builds. 99.9% of errors are code issues, not cache problems.
- **Never read build.log directly**: It contains the entire build history with stale errors. Always extract first.
- **Protect header optimizations**: When encountering "file not found" header errors, add the missing include to the .cpp file with the error, not to optimized headers. Check `git status` to detect if a header is being optimized (staged/modified/recent commit).

## Error Categories

1. **Compilation errors** (CXX tasks) — syntax, missing headers, incomplete types
2. **Linker errors** (SOLINK/LINK tasks) — undefined symbols, missing libraries
3. **Build system errors** — GN/Ninja configuration issues

## Error Patterns and Solutions

### Pattern 1: Undefined Symbol (`ld.lld: error: undefined symbol`)

Identify which library fails to link, then apply the matching scenario:

**Scenario 1: libace/libace_compatible cannot find symbol**
- Implementation missing or .cpp not in BUILD.gn
- Find where similar files are compiled: `grep -r "file.cpp" frameworks/*/BUILD.gn`
- Add .cpp to the correct source_set (not always ace_core_ng_source_set)
- See `references/undefined-symbol-missing-cpp.md`

**Scenario 2: Other library links with libace dependency — symbol not exported**

Distinguish non-template vs template FIRST:

| Aspect | Non-Template | Template |
|--------|-------------|----------|
| Export location | Method declaration in .h | BOTH declaration in .h AND definition in .cpp |
| Class export sufficient? | YES (covers all methods) | NO (individual methods need export) |
| libace.map pattern | Fine-grained: `ClassName::MethodName*;` | Wildcard: `ClassName*;` |

**Non-template solution:**
1. If class has `ACE_FORCE_EXPORT` — already exported, skip to libace.map
2. If class lacks `ACE_FORCE_EXPORT` — add it to the specific method declaration in .h (NOT .cpp)
3. Add to `build/libace.map` with fine-grained pattern: `OHOS::Ace::ClassName::MethodName*;`

**Template function solution** (see `references/template-instantiation-type-export.md`):
1. Add `extern template` declaration in header
2. Add `ACE_FORCE_EXPORT` to declaration in .h AND implementation in .cpp
3. Add explicit instantiation in .cpp
4. Add wildcard pattern to libace.map: `void?OHOS::Ace::ClassName::FunctionName*;`

**Template class method solution** (see `references/symbol-export-libace-map.md`):
1. Add `ACE_FORCE_EXPORT` to EACH method implementation in .cpp (class export alone is NOT sufficient)
2. Use wildcard in libace.map: `OHOS::Ace::NG::ClassName*;`
3. Use unquoted patterns — `"ClassName<T>::*"` won't match wildcards

**Fine-grained export priority** (non-template):
- Method-level: `ClassName::MethodName*;` (most preferred)
- Constructor-level: `ClassName::ClassName*;` (all overloads)
- Class-level: `ClassName::*;` (last resort)

**Scenario 3: Special libraries** (libarkoala_native_ani, ace_ndk only)
- These don't link libace but use utility functions
- Add utility .cpp directly to the library's BUILD.gn sources

**Scenario 4: LTO Virtual Thunk** (see `references/lto-virtual-thunk-libace-map-export.md`)
- Error: "undefined symbol: virtual thunk to ClassName::~ClassName()"
- Keep forward declaration optimization, do NOT revert to inline
- Add BOTH patterns to libace.map: `OHOS::Ace::ClassName::*;` AND `virtual?thunk?to?OHOS::Ace::ClassName::*;`

### Pattern 2: Incomplete Type (`member access into incomplete type`)

- Missing header include or forward declaration without full definition
- **RefPtr<T> as class member**: Do NOT add full include to header. Instead, declare special member functions in header, implement with `= default` in .cpp. See `references/forward-declaration-refptr-member.md`
- **Struct with RefPtr member and -> access**: Add helper method to encapsulate type access. See `references/forward-declaration-struct-helper-method.md`
- **std::function<RefPtr<T>>**: Forward declaration works — using alias does NOT instantiate template. See `references/template-instantiation-type-export.md`
- **Default param nullptr with RefPtr**: Replace `= nullptr` with overload functions. See `references/forward-declaration-refptr-member.md`

### Pattern 3: Redefinition (`redefinition of`)

- Constants defined in both header and .cpp
- Keep only `inline constexpr` in header, remove from .cpp
- See `references/redefinition-error-constexpr.md`

### Pattern 4: Test Linking Errors

- Test BUILD.gn missing required .cpp files
- Common missing files: log_wrapper.cpp, string_utils.cpp, layout_constraint.cpp, measure_property.cpp
- Add to appropriate sources based on test template type
- Only add source files — do NOT modify cflags/configs/defines
- See `references/test-missing-source-files.md`

### Pattern 5: MinGW dllexport Mismatch

- Only on MinGW/Windows builds
- Header declaration and .cpp implementation have inconsistent export attributes
- Add `ACE_FORCE_EXPORT` to ALL overloaded method declarations in header
- See `references/mingw-dllexport-declaration-mismatch.md`

### Pattern 6: Namespace Type Resolution

- Type defined in parent namespace, used in child namespace
- Preserve full namespace qualifier (e.g., `OHOS::Ace::DragEvent` in `OHOS::Ace::NG` code)
- Never delete namespace prefixes
- See `references/symbol-export-ace-force-export.md`

## Reference Cases

When analysis matches a known pattern, **read the corresponding reference file completely** for step-by-step solution with code examples and verification commands.

| Pattern | MANDATORY Read | Error Type |
|---------|---------------|-----------|
| Undefined symbol, .cpp not in BUILD.gn | `references/undefined-symbol-missing-cpp.md` | Missing source file |
| Symbol used cross-module, not exported | `references/symbol-export-ace-force-export.md` | ACE_FORCE_EXPORT missing |
| Has ACE_FORCE_EXPORT but still undefined | `references/symbol-export-libace-map.md` | libace.map whitelist missing |
| Redefinition of constexpr | `references/redefinition-error-constexpr.md` | Duplicate definitions |
| File in BUILD.gn but still undefined | `references/build-system-ace-core-ng-source-set.md` | ace_core_ng_source_set missing |
| Incomplete type with RefPtr member | `references/forward-declaration-refptr-member.md` | RefPtr forward declaration |
| Test linking, missing .cpp files | `references/test-missing-source-files.md` | Test missing sources |
| Struct RefPtr with -> access | `references/forward-declaration-struct-helper-method.md` | Helper method pattern |
| LTO virtual thunk undefined | `references/lto-virtual-thunk-libace-map-export.md` | Virtual thunk export |
| MinGW dllexport mismatch | `references/mingw-dllexport-declaration-mismatch.md` | Export attribute mismatch |
| Template instantiation type export | `references/template-instantiation-type-export.md` | Template type visibility |

**Do NOT load** reference files when the error does not match any pattern above.

## Verification Commands

```bash
grep -r "SymbolName" --include="*.h" --include="*.cpp" frameworks/   # Find symbol definition
grep -r "file.cpp" frameworks/*/BUILD.gn                               # Check BUILD.gn
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep SymbolName       # Check export
grep "SymbolName" build/libace.map                                      # Check libace.map
./build.sh --product-name rk3568 --build-target ace_engine --ccache    # Rebuild
```

Provide recommendations with error type, location, root cause, fix with before/after code, and verification steps.
