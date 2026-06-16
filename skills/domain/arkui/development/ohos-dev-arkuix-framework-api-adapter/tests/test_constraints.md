# Evaluation Cases: Constraint Enforcement Tests

> **Category C**: Tests mandatory constraints are properly enforced.
>
> **How to use**: Present the violation scenario to an agent. Verify the agent REJECTS the violation and applies the correct constraint.

---

## C01: Interface Signature Compatibility

**Input**: Agent is asked to adapt `@ohos.settings.getValue` but proposes:

```typescript
// WRONG: Added defaultValue parameter that doesn't exist in d.ts
export function getValue(context: Context, name: string, defaultValue: string): string;
```

Original d.ts signature:
```typescript
export function getValue(context: Context, name: string, callback: AsyncCallback<string>): void;
```

**Expected agent behavior**:
- Constraint 1 (Interface Signature Compatibility) triggered
- Agent recognizes: parameter count mismatch (3 vs 3 but different types), return type mismatch
- Agent corrects to exact d.ts signature
- Agent states: "signatures MUST be identical to OHOS SDK d.ts"

**PASS criteria**: Final adapted API signature = exact match with d.ts. Zero deviation.

---

## C02: 7-Point Naming Consistency (Mode B)

**Input**: Agent generates Mode B code with these names:

| # | Location | Value (WRONG) | Should Be |
|---|----------|---------------|-----------|
| 1 | CMake target | `settings` | `settings_ext` |
| 2 | nm_modname | `settings` | `settings_ext` |
| 3 | types/ dir | `libsettings/` | `libsettings_ext/` |
| 4 | oh-package.json5 (types) | `libsettings.so` | `libsettings_ext.so` |
| 5 | oh-package.json5 (entry dep) | `libsettings.so` | `libsettings_ext.so` |
| 6 | index.d.ts import | `libsettings.so` | `libsettings_ext.so` |
| 7 | ArkTS import | `from '@ohos.settings'` only | dual: `@ohos.settings` + `libsettings_ext.so` |

**Expected agent behavior**:
- Constraint 5 (7-Point Naming Consistency) triggered
- Agent detects mismatch between points
- Agent corrects ALL 7 points to use `settings_ext` suffix consistently
- Agent explains: "dual import conflict avoidance — NAPI module name must differ from OHOS built-in"

**PASS criteria**: All 7 naming points are consistent with `_ext` suffix.

---

## C03: 4 Mandatory Config Files Completeness

**Input**: Agent completes Phase 6 but forgets `apiConfig.json` entry.

**Expected agent behavior**:
- Agent runs `code_generator.py --validate` or checks manually
- Detects missing `apiConfig.json` entry
- Phase 6 completion checklist fails:
  - [x] `plugin_lib.gni` — updated
  - [ ] `apiConfig.json` — **MISSING** ← caught
  - [x] `arkui_cross_sdk_description_std.json` — updated
  - [x] `@ohos.{module}.d.ts` — @crossplatform added
- Agent generates missing entry before declaring Phase 6 complete

**PASS criteria**: All 4 config files present and cross-checked. Module name consistent across all files.

---

## C04: CamelCase vs snake_case Naming Pitfall

**Input**: Module `@ohos.deviceInfo` — d.ts uses camelCase (`deviceInfo`), directory uses snake_case (`device_info`).

**Expected agent behavior**:
- Agent recognizes the naming pitfall
- Agent cross-checks all 4 config files:
  - d.ts: `@ohos.deviceInfo`
  - plugin_lib.gni: `device_info`
  - apiConfig.json: `deviceInfo` (matches d.ts module name)
  - sdk_description.json: `device_info`
- Agent states: "d.ts module name uses camelCase while directory uses snake_case — cross-check character by character"

**PASS criteria**: No naming mismatch between config files. Agent explicitly verifies the camelCase/snake_case mapping.
