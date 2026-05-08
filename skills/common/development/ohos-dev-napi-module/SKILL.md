---
name: ohos-dev-napi-module
description: Use when developing, debugging, porting, or reviewing OpenHarmony/HarmonyOS NAPI native modules, ArkTS native bindings, napi_module registration, BUILD.gn ace_napi shared libraries, DECLARE_NAPI macros, async work, Sendable/QoS/serialization APIs, or behavior differences from Node.js N-API.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: napi
  capability: module
  version: 0.1.0
  status: draft
  tags:
    - napi
    - native-module
    - arkts-binding
---

# OpenHarmony NAPI Module Development

Guide native module work where OpenHarmony diverges from Node.js N-API: module registration, GN integration, security flags, OpenHarmony extensions, and runtime behavior differences.

## First Classification

Before writing or reviewing code, classify the request:

| User need | Load now | Do not load |
| --- | --- | --- |
| New basic native module or registration failure | This file only | Extended API refs |
| `BUILD.gn`, install path, CFI/PAC, missing `ace_napi` | `references/build-configuration.md` | Async/extended refs unless used |
| Porting Node.js N-API code or behavior mismatch | `references/api-behavior-differences.md` | Build ref unless build files are touched |
| `DECLARE_NAPI_*` macro details | `references/helper-macros.md` | Other refs unless touched |
| Promise async work, background task, QoS scheduling | `references/async-work-pattern.md` | Extended API ref unless Sendable/QoS APIs are used directly |
| Sendable, serialization, Ark runtime, module loading APIs | `references/extended-apis.md` | Async ref unless async work is also present |

If multiple rows apply to the same change, load each matching reference. If none apply, keep the context small and use this file only.

## Expert Checks

Ask these before choosing an implementation:

- **Import identity**: What exact ArkTS/JS import name must resolve to this native module? `nm_modname` must match that identity, not merely the library filename.
- **Module shape**: Is this a plain native export, or does it need bundled JS/ABC via `napi_module_with_js`?
- **System placement**: Which subsystem and part own the module? `relative_install_dir`, `subsystem_name`, and `part_name` should reflect that ownership.
- **Runtime boundary**: Will native work cross threads or runtimes? Do not carry ordinary `napi_value`/`napi_env` assumptions across those boundaries.
- **Node.js parity**: Is the code copied from Node.js N-API examples? Treat registration, build files, selected API behavior, and OpenHarmony extensions as suspect until checked.

## Required OpenHarmony Patterns

### Module Registration

Use explicit OpenHarmony registration:

```cpp
#include "napi/native_api.h"

static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        DECLARE_NAPI_FUNCTION("methodName", MethodCallback),
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}

static napi_module g_module = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "moduleName",
    .nm_priv = nullptr,
    .reserved = {0}
};

extern "C" __attribute__((constructor)) void RegisterModule()
{
    napi_module_register(&g_module);
}
```

`Init` should normally be `static`, and the constructor function name should be unique enough to avoid collisions inside the shared object.

### Bundled JS/ABC Module

Use `napi_module_with_js` only when the native module must expose associated JS/ABC code. This is an OpenHarmony extension, not a Node.js feature.

```cpp
#include "napi/native_node_api.h"

static napi_module_with_js g_module = {
    .nm_version = 1,
    .nm_register_func = Init,
    .nm_modname = "moduleName",
    .nm_get_abc_code = GetABCCodeCallback,
};

extern "C" __attribute__((constructor)) void RegisterModuleWithJs()
{
    napi_module_with_js_register(&g_module);
}
```

### BUILD.gn Baseline

For build changes, load `references/build-configuration.md` before editing. Minimum expected shape:

```python
import("//build/ohos.gni")

ohos_shared_library("module_name") {
  sanitize = {
    cfi = true
    cfi_cross_dso = true
  }
  branch_protector_ret = "pac_ret"

  external_deps = [ "napi:ace_napi", "hilog:libhilog" ]
  relative_install_dir = "module/subsystem"
}
```

`"napi:ace_napi"` is not optional for NAPI modules. CFI/PAC settings are security requirements in system native code, not cosmetic build flags.

## Never Do

- **NEVER use Node.js `NAPI_MODULE()` for OpenHarmony modules.** It hides the registration path OpenHarmony expects; missing constructor registration commonly appears as "module not found".
- **NEVER assume `nm_modname` can be arbitrary.** It must align with the import/module lookup path; a good shared library can still fail at runtime if this name is wrong.
- **NEVER copy `binding.gyp`/node-gyp assumptions into OpenHarmony.** OpenHarmony uses GN and system install metadata; the build target must declare `ace_napi`, ownership, and install location.
- **NEVER treat Node.js N-API behavior as authoritative when porting.** Some validation, error object, reference, typed array, async work, and threadsafe-function behaviors differ; load the behavior reference for ports or strange runtime results.
- **NEVER call ordinary NAPI APIs from an async execute callback.** Use the complete callback for JS interaction, or a threadsafe function for cross-thread communication.
- **NEVER keep handle scopes unpaired.** Pair `napi_open_handle_scope`/`napi_close_handle_scope` and escapable scopes on every path, including errors.
- **NEVER pass `napi_env` across threads as if it were a general runtime handle.** Crossing thread/runtime boundaries needs an explicit NAPI mechanism such as async work, threadsafe function, Sendable, or serialization.

## Failure Triage

| Symptom | First suspects | What to inspect |
| --- | --- | --- |
| Module not found at import/load time | Wrong `nm_modname`, missing constructor, wrong install dir | Registration block, `relative_install_dir`, import string |
| Constructor seemingly never runs | Used `NAPI_MODULE()`, missing `__attribute__((constructor))`, symbol stripped/collided | Registration function and shared object build |
| Build fails with NAPI headers/libs | Missing `napi:ace_napi`, wrong target type | `BUILD.gn` external deps and `ohos_shared_library` |
| Security/runtime crash after load | CFI/PAC mismatch, invalid function pointer path | `sanitize`, `branch_protector_ret`, callback signatures |
| Ported Node.js addon behaves differently | API behavior mismatch | Load `api-behavior-differences.md` and compare touched APIs |
| Async code crashes or hangs | NAPI called on worker thread, bad cleanup, env misuse | Execute/complete callbacks, async work lifecycle |

## Review Checklist

When reviewing a NAPI module patch, check in this order:

1. Registration uses `napi_module_register` or `napi_module_with_js_register` from an `extern "C"` constructor.
2. `nm_modname` matches the ArkTS/JS import identity expected by the caller.
3. Export descriptors use the local OpenHarmony macros or valid `napi_property_descriptor` fields.
4. `BUILD.gn` declares `ohos_shared_library`, `napi:ace_napi`, install path, subsystem/part metadata, and required security flags.
5. Async code separates background work from JS/NAPI calls and releases async work/context on every completion path.
6. References, handle scopes, wrapped native objects, and finalizers have clear ownership and cleanup.
7. Any Node.js sample-derived code has been checked against OpenHarmony behavior differences.

## Related Skills

- Use `openharmony-build` for broader OpenHarmony build system issues.
- Use `openharmony-cpp` for general OpenHarmony C++ style beyond NAPI-specific rules.
