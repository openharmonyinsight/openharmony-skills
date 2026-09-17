---
name: ohos-dev-appmgr-api-generator
description: "Generate the complete API implementation chain from AppMgrClient to AppMgrServiceInner for new app_manager interfaces in OpenHarmony ability_runtime. Use when adding a new IPC API that requires code across these 12 files: app_mgr_client.h/.cpp, app_mgr_ipc_interface_code.h, app_mgr_proxy.h/.cpp, app_mgr_interface.h, app_mgr_stub.h/.cpp, app_mgr_service.h/.cpp, app_mgr_service_inner.h/.cpp. Triggers include phrases like 'add a new AppMgr API', 'generate AppMgr call chain', 'add IPC method to app_manager', or providing an API name with parameters and return type."
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: app-framework
  capability: appmgr-api-generator
  version: 0.1.0
  status: draft
  tags: [appmgr, ipc, ability-runtime, api-generator, codegen]
---

# AppMgr API Generator

Generate the complete client-to-service call chain for a new AppMgr API in one pass.

## Quick Start

Provide three things, then invoke the script:

1. **API name** (camelCase, e.g. `GetConfiguration`)
2. **Return type**: `AppMgrResultCode` | `int32_t` | `void` | `bool` | `std::string`
3. **Parameters**: list of `<type> <name>`, e.g. `const std::string& bundleName`

Optional flag: async IPC (`TF_ASYNC`).

```bash
python scripts/generate_appmgr_api.py <ability_runtime_root>
```

The script prints 12 code snippets; apply each to the file identified by the snippet's key.

## Workflow

1. Collect API signature (name, return type, params, async) from the user.
2. Run `scripts/generate_appmgr_api.py` to generate all snippets.
3. Apply each snippet to its target file (see references/files.md for exact paths and insertion guidance).
4. For the stub, three artifacts are produced: a `Handle<ApiName>` declaration (insert into `app_mgr_stub.h`), a `case` label (insert into the appropriate `OnRemoteRequestInnerN` switch), and a `Handle<ApiName>` method definition (append in `app_mgr_stub.cpp`).
5. Fill in the business logic in `app_mgr_service_inner.cpp` (the generator leaves a `// TODO` marker).

## Architecture

```
AppMgrClient  ->  AppMgrProxy  ->  [IPC]  ->  AppMgrStub  ->  AppMgrService  ->  AppMgrServiceInner
```

- **AppMgrClient**: public API surface; converts `int32_t` IPC results to `AppMgrResultCode` when needed.
- **AppMgrProxy**: marshals params, sends IPC request via `PARCEL_UTIL_*` helpers.
- **AppMgrStub**: dispatches IPC codes to `Handle<ApiName>` methods. `OnRemoteRequestInner()` fans out to a series of `OnRemoteRequestInnerN` functions — read the current fan-out in `app_mgr_stub.cpp` (currently up to Ninth) and pick the group whose code range covers the new enum value.
- **AppMgrService**: checks `IsReady()`, delegates to `AppMgrServiceInner`.
- **AppMgrServiceInner**: actual business logic.

## Implementation Notes

- **Async vs sync**: default `TF_SYNC`. Use `TF_ASYNC` only for fire-and-forget calls (e.g. one-shot notifications). Async forces `void` return type — a non-void method cannot use `TF_ASYNC` because there is no reply to read.
- **Return-type contract**: `AppMgrResultCode` is a client-facing enum; over IPC it is transported as `int32_t` (Client returns the enum and maps `result != ERR_OK` → `ERROR_SERVICE_NOT_READY`, `ERR_OK` → `RESULT_OK`; IAppMgr/Proxy/Service/ServiceInner declare and return `int32_t`; the Stub writes `reply.WriteInt32(result)`). The generator threads the transport return type through the IPC layers automatically.
- **Macro choice**: void methods use `PARCEL_UTIL_WRITE_NORET` / `PARCEL_UTIL_SENDREQ_NORET`; `int32_t`/`int` **and `AppMgrResultCode`** (transported as `int32_t`) use `_RET_INT`; `bool`/`std::string` use explicit `data.WriteXxx` (with a type-safe failure return) plus the unified `AppMgrProxy::SendRequest` wrapper (which runs `IsForbidStart()` and a null-safe `Remote()`, like the `_RET_INT` send macro). The script handles this automatically based on the return type.
- **Parcel validation**: every Proxy/Stub parcel read (token, params, reply) is validated — a failed read returns a type-appropriate error instead of forwarding a default value. `sptr` parameters are null-guarded before dereference on both sides; Stub `iface_cast`/`ReadRemoteObject` results are null-checked before reaching the service.
- **Error codes**: int32_t (and AppMgrResultCode transport) proxy returns `IPC_PROXY_ERR` on token/param-write or reply-read failure, and transparently returns the `SendRequest` code on send failure; service returns `AAFwk::ERR_APP_MGR_SERVICE_NOT_READY` when not ready; Stub returns `ERR_INVALID_VALUE` on param-read failure and `IPC_STUB_ERR` on reply-write failure. `bool` returns `false`, `std::string` returns `""` on failure.
- **IPC enum**: each new API needs a unique `AppMgrInterfaceCode` value; the script reads the existing enum and proposes the next free value.
- **Stub dispatch**: do NOT inline the parameter handling in the case body. Delegate to a `Handle<ApiName>` method — this matches the existing stub layout and keeps `OnRemoteRequestInnerN` switches readable. The `Handle<ApiName>` declaration goes in `app_mgr_stub.h`.

See [references/files.md](references/files.md) for the full per-file guide (paths, insertion points, examples) and [references/patterns.md](references/patterns.md) for parameter marshaling tables and advanced patterns (async, vectors, nullable sptr).
