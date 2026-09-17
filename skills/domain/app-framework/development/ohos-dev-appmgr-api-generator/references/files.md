# AppMgr File Structure

This document lists the 12 files involved when adding a new AppMgr API and the
exact insertion point for each.

## Call Chain

```
AppMgrClient
    |  method call
AppMgrProxy
    |  IPC SendRequest
AppMgrStub  (Handle<ApiName> dispatch)
    |
AppMgrService  (IsReady() check)
    |
AppMgrServiceInner  (business logic)
```

## Files and Insertion Points

All paths are relative to the `ability_runtime` project root.

### Client side

#### `interfaces/inner_api/app_manager/include/appmgr/app_mgr_client.h`
- **Insert**: public method declaration inside `class AppMgrClient`.
- **Snippet key**: `client_h`.
- Example:
```cpp
virtual AppMgrResultCode SomeMethod(const std::string &param);
```

#### `interfaces/inner_api/app_manager/src/appmgr/app_mgr_client.cpp`
- **Insert**: new method definition.
- **Snippet key**: `client_cpp`.
- Example:
```cpp
AppMgrResultCode AppMgrClient::SomeMethod(const std::string &param)
{
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;
    }
    int32_t result = service->SomeMethod(param);
    if (result != ERR_OK) {
        return AppMgrResultCode::ERROR_SERVICE_NOT_READY;
    }
    return AppMgrResultCode::RESULT_OK;
}
```

### IPC layer

#### `interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h`
- **Insert**: new enum value at the bottom of `enum class AppMgrInterfaceCode`.
- **Snippet key**: `ipc_code_h`.
- Example:
```cpp
APP_SOME_METHOD = 140,  // value suggested by the script
```

#### `interfaces/inner_api/app_manager/include/appmgr/app_mgr_proxy.h`
- **Insert**: public method declaration inside `class AppMgrProxy`.
- **Snippet key**: `proxy_h`.
- Notes: the declaration uses the **IPC transport return type** — `int32_t` for `AppMgrResultCode` (the enum stays at the Client boundary), the public type for `int32_t`/`void`/`bool`/`std::string`.
- Example (`AppMgrResultCode` API — proxy declares `int32_t`):
```cpp
int32_t SomeMethod(const std::string &param) override;
```

#### `interfaces/inner_api/app_manager/src/appmgr/app_mgr_proxy.cpp`
- **Insert**: new method definition.
- **Snippet key**: `proxy_cpp`.
- Notes: the write/send macros depend on the IPC transport return type — `void` uses `PARCEL_UTIL_WRITE_NORET` + `PARCEL_UTIL_SENDREQ_NORET`; `int32_t`/`int` and `AppMgrResultCode` (transported as `int32_t`) use `_RET_INT` and read the reply; `bool`/`std::string` use explicit `data.WriteXxx` (type-safe failure return) + the unified `AppMgrProxy::SendRequest` wrapper. The script picks the branch from the return type — do not hand-edit to `_RET_INT` for `bool`/`std::string` (it returns an int that cannot convert, or turns a negative error code into `true` for bool).
- Example (`AppMgrResultCode` API — proxy returns `int32_t`, Client maps to enum):
```cpp
int32_t AppMgrProxy::SomeMethod(const std::string &param)
{
    TAG_LOGD(AAFwkTag::APPMGR, "called");
    MessageParcel data;
    MessageParcel reply;
    MessageOption option(MessageOption::TF_SYNC);
    HITRACE_METER_NAME(HITRACE_TAG_ABILITY_MANAGER, __PRETTY_FUNCTION__);
    if (!WriteInterfaceToken(data)) {
        TAG_LOGE(AAFwkTag::APPMGR, "SomeMethod write interface token failed");
        return IPC_PROXY_ERR;
    }
    PARCEL_UTIL_WRITE_RET_INT(data, String16, Str8ToStr16(param));
    PARCEL_UTIL_SENDREQ_RET_INT(AppMgrInterfaceCode::APP_SOME_METHOD, data, reply, option);
    int32_t ret;
    if (!reply.ReadInt32(ret)) {
        TAG_LOGE(AAFwkTag::APPMGR, "SomeMethod read reply failed");
        return IPC_PROXY_ERR;
    }
    return ret;
}
```

#### `interfaces/inner_api/app_manager/include/appmgr/app_mgr_interface.h`
- **Insert**: new virtual method on `class IAppMgr`.
- **Snippet key**: `interface_h`.
- Notes: provide a default inline body so derived classes don't have to override every method. The declaration uses the IPC transport return type (`int32_t` for `AppMgrResultCode`).
- Example (`AppMgrResultCode` API — interface declares `int32_t`):
```cpp
virtual int32_t SomeMethod(const std::string &param)
{
    return 0;
}
```

### Stub

#### `interfaces/inner_api/app_manager/include/appmgr/app_mgr_stub.h`
- **Insert**: `Handle<ApiName>` method declaration inside `class AppMgrStub`.
- **Snippet key**: `stub_h`.
- Example:
```cpp
int32_t HandleSomeMethod(MessageParcel &data, MessageParcel &reply);
```

#### `interfaces/inner_api/app_manager/src/appmgr/app_mgr_stub.cpp`
> Note: this file lives under `interfaces/`, NOT under `services/appmgr/src/appmgrstub/`.

The real stub dispatches via `OnRemoteRequestInner()` which fans out to a
series of `OnRemoteRequestInnerN` functions (currently up to Ninth). Each
case delegates to a `Handle<ApiName>` method; parameter reads and reply
writes live inside the `Handle*` method, not in the switch case.

- **Insert (1)**: a `case` line into the appropriate `OnRemoteRequestInnerN`
  switch — read the current fan-out in the file and pick the group whose code
  range covers the new enum value.
- **Insert (2)**: a new `Handle<ApiName>` method definition at the bottom of
  the file (also declare it in `app_mgr_stub.h`).
- **Snippet key**: `stub_cpp` (contains both artifacts, separated by a comment).
- Example case line:
```cpp
case static_cast<uint32_t>(AppMgrInterfaceCode::APP_SOME_METHOD):
    return HandleSomeMethod(data, reply);
```
- Example Handle method (`AppMgrResultCode` API — `result` is `int32_t`, no enum cast):
```cpp
int32_t AppMgrStub::HandleSomeMethod(MessageParcel &data, MessageParcel &reply)
{
    std::u16string param16;
    if (!data.ReadString16(param16)) {
        TAG_LOGE(AAFwkTag::APPMGR, "read param failed.");
        return ERR_INVALID_VALUE;
    }
    std::string param = Str16ToStr8(param16);
    auto result = this->SomeMethod(param);
    if (!reply.WriteInt32(result)) {
        TAG_LOGE(AAFwkTag::APPMGR, "Write reply failed.");
        return IPC_STUB_ERR;
    }
    return ERR_NONE;
}
```

### Server side

#### `services/appmgr/include/app_mgr_service.h`
- **Insert**: public method declaration on `class AppMgrService`.
- **Snippet key**: `service_h`.

#### `services/appmgr/src/app_mgr_service.cpp`
- **Insert**: new method definition.
- **Snippet key**: `service_cpp`.
- Notes: always start with `IsReady()` check; delegate to `appMgrServiceInner_`.
- Example (`AppMgrResultCode` API — service returns `int32_t`, Client maps to enum):
```cpp
int32_t AppMgrService::SomeMethod(const std::string &param)
{
    TAG_LOGD(AAFwkTag::APPMGR, "SomeMethod called");
    if (!IsReady()) {
        TAG_LOGE(AAFwkTag::APPMGR, "SomeMethod failed");
        return AAFwk::ERR_APP_MGR_SERVICE_NOT_READY;
    }
    return appMgrServiceInner_->SomeMethod(param);
}
```

#### `services/appmgr/include/app_mgr_service_inner.h`
- **Insert**: public method declaration on `class AppMgrServiceInner`.
- **Snippet key**: `service_inner_h`.

#### `services/appmgr/src/app_mgr_service_inner.cpp`
- **Insert**: new method definition.
- **Snippet key**: `service_inner_cpp`.
- Notes: this is where the actual business logic goes; the script leaves a `// TODO` marker. Returns the IPC transport type (`int32_t` for `AppMgrResultCode`).
- Example (`AppMgrResultCode` API — inner returns `int32_t`):
```cpp
int32_t AppMgrServiceInner::SomeMethod(const std::string &param)
{
    TAG_LOGD(AAFwkTag::APPMGR, "SomeMethod called");
    // TODO: implement
    return AAFwk::ERR_APP_MGR_SERVICE_NOT_READY;
}
```

## Checklist

- [ ] `app_mgr_client.h` — public declaration
- [ ] `app_mgr_client.cpp` — wraps IPC, maps int32_t to AppMgrResultCode
- [ ] `app_mgr_ipc_interface_code.h` — new enum value (use the script-suggested code)
- [ ] `app_mgr_proxy.h` — override declaration
- [ ] `app_mgr_proxy.cpp` — parcel write + send + reply read
- [ ] `app_mgr_interface.h` — virtual method with default body
- [ ] `app_mgr_stub.h` — `Handle<ApiName>` declaration
- [ ] `app_mgr_stub.cpp` — case label **and** `Handle<ApiName>` method
- [ ] `app_mgr_service.h` — public declaration
- [ ] `app_mgr_service.cpp` — `IsReady()` guard + delegate
- [ ] `app_mgr_service_inner.h` — public declaration
- [ ] `app_mgr_service_inner.cpp` — actual implementation

## Common Pitfalls

- **Missing IPC code**: each new API needs a unique `AppMgrInterfaceCode` value. The script reads the existing enum and proposes the next free value.
- **Return type mismatch**: `AppMgrResultCode` is a client-facing enum; the interface/proxy/service/service-inner transport it as `int32_t` (the Client maps `result != ERR_OK` -> `ERROR_SERVICE_NOT_READY`, `ERR_OK` -> `RESULT_OK`). The generator threads the transport return type through the IPC layers automatically — do not hand-edit signatures back to `AppMgrResultCode` or the int32_t contract breaks.
- **Wrong macro for return type**: void proxy methods use `_NORET`; `int32_t`/`int` **and `AppMgrResultCode`** (transported as `int32_t`) use `_RET_INT`; `bool`/`std::string` use explicit `data.WriteXxx` writes plus the unified `AppMgrProxy::SendRequest` wrapper. Using `_RET_INT` for `bool`/`std::string` causes compile errors or wrong semantics (e.g. negative error code → `true` for bool). The script handles this; do not hand-edit.
- **Async with non-void return**: `TF_ASYNC` means fire-and-forget — there is no reply to read. The script forces `void` when async is selected; do not override this.
- **Missing `static_cast<uint32_t>`**: the stub switch receives `uint32_t`, so case labels must cast.
- **Inlining stub case bodies**: keep the switch lean — delegate to `Handle<ApiName>`. Inline bodies break the existing pattern and bloat the dispatch tables.
- **Wrong stub file**: `app_mgr_stub.cpp` is under `interfaces/inner_api/app_manager/src/appmgr/`, not under `services/appmgr/`.
