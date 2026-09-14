# AppMgr API Patterns Reference

This document lists the patterns the generator follows and the variations the
script does not auto-generate (hand-edit after generation).

## Return Types

### AppMgrResultCode
Client-facing status code. It is an **enum at the Client boundary only**; over
IPC it is transported as `int32_t`:

- `AppMgrClient` returns `AppMgrResultCode` and maps the `int32_t` IPC result
  back to the enum (`result != ERR_OK` -> `AppMgrResultCode::ERROR_SERVICE_NOT_READY`,
  `ERR_OK` -> `AppMgrResultCode::RESULT_OK`).
- `IAppMgr` / `AppMgrProxy` / `AppMgrService` / `AppMgrServiceInner` all declare
  and return `int32_t`. The Stub writes `reply.WriteInt32(result)`.

This mirrors the real `ClearUpApplicationData` path. The generator threads a
transport return type (`int32_t` for `AppMgrResultCode`) through the IPC layers
automatically — do not hand-edit the proxy/interface/service signatures back to
`AppMgrResultCode`, or the int32_t transport contract breaks.

```cpp
// client.cpp (public enum)
AppMgrResultCode AppMgrClient::SomeMethod(const std::string &param)
{
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {
        return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;
    }
    int32_t result = service->SomeMethod(param);   // IPC transports int32_t
    if (result != ERR_OK) {
        return AppMgrResultCode::ERROR_SERVICE_NOT_READY;
    }
    return AppMgrResultCode::RESULT_OK;
}
```

```cpp
// proxy.cpp (IPC transport: int32_t)
int32_t AppMgrProxy::SomeMethod(const std::string &param)
{
    // ... PARCEL_UTIL_SENDREQ_RET_INT(...) ; validated reply read ; return ret;
}
```

### int32_t
Used when returning an OS-level error code directly.

```cpp
// client.cpp
int32_t AppMgrClient::SomeMethod(const std::string &param)
{
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {
        return AAFwk::ERR_APP_MGR_SERVICE_NOT_CONNECTED;
    }
    return service->SomeMethod(param);
}
```

### void
Used for fire-and-forget calls. The proxy uses `_NORET` macros, the stub calls
through and returns `ERR_NONE`.

```cpp
// client.cpp
void AppMgrClient::SomeMethod(const std::string &param)
{
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {
        return;
    }
    service->SomeMethod(param);
}
```

## PARCEL_UTIL_* Macros

The codebase has paired macros for void and non-void methods. The generator
picks the right family automatically based on the return type:

| Return type | Write param | Send request |
|---|---|---|
| `void` | `PARCEL_UTIL_WRITE_NORET` | `PARCEL_UTIL_SENDREQ_NORET` |
| `int32_t` / `int` / `AppMgrResultCode` | `PARCEL_UTIL_WRITE_RET_INT` | `PARCEL_UTIL_SENDREQ_RET_INT` |
| `bool` / `std::string` | explicit `data.WriteXxx` (type-safe failure return) | `SendRequest(...)` wrapper (runs `IsForbidStart()` + null-safe `Remote()`) |

`AppMgrResultCode` is transported as `int32_t` over IPC (see Return Types
above), so it shares the `_RET_INT` path with `int32_t`/`int`. The `_RET_INT`
send macro returns an `int32_t` error code on failure — correct for an
`int32_t`-returning (transport) method, but it cannot convert to `bool`
(negative error code -> `true`, wrong semantics) or `std::string` (compile
error). For those two types the generator emits an explicit `SendRequest`
wrapper call (the same unified path the `_RET_INT` macro uses internally)
with a type-appropriate failure return.

## Parameter Marshaling

Every Stub parameter read uses the bool-returning `ReadXxx(value)` form and
returns `ERR_INVALID_VALUE` on failure, so a truncated/empty request cannot feed
a default (0 / false / null) into the business layer. `sptr` results
(`ReadRemoteObject` / `iface_cast`) are null-checked before being passed to the
service.

| C++ type | Write | Read (validated) |
|---|---|---|
| `std::string` | `PARCEL_UTIL_WRITE_*(data, String16, Str8ToStr16(name))` | `std::u16string n16; if (!data.ReadString16(n16)) return ERR_INVALID_VALUE; std::string n = Str16ToStr8(n16);` |
| `int32_t` / `pid_t` | `PARCEL_UTIL_WRITE_*(data, Int32, v)` | `int32_t v; if (!data.ReadInt32(v)) return ERR_INVALID_VALUE;` |
| `uint32_t` | `PARCEL_UTIL_WRITE_*(data, Uint32, v)` | `uint32_t v; if (!data.ReadUint32(v)) return ERR_INVALID_VALUE;` |
| `uint64_t` | `PARCEL_UTIL_WRITE_*(data, Uint64, v)` | `uint64_t v; if (!data.ReadUint64(v)) return ERR_INVALID_VALUE;` |
| `bool` | `PARCEL_UTIL_WRITE_*(data, Bool, v)` | `bool v; if (!data.ReadBool(v)) return ERR_INVALID_VALUE;` |
| `const sptr<IRemoteObject>&` | `PARCEL_UTIL_WRITE_*(data, RemoteObject, name.GetRefPtr())` | `sptr<IRemoteObject> n = data.ReadRemoteObject(); if (!n) return ERR_INVALID_VALUE;` |
| `const sptr<IXxx>&` (IRemoteBroker) | `PARCEL_UTIL_WRITE_*(data, RemoteObject, name->AsObject())` | `sptr<IXxx> n = iface_cast<IXxx>(data.ReadRemoteObject()); if (!n) return ERR_INVALID_VALUE;` |

> `sptr<IRemoteObject>` is the object itself — write it via `GetRefPtr()`.
> `sptr<IXxx>` where `IXxx` derives from `IRemoteBroker` (e.g.
> `IConfigurationObserver`, `IApplicationStateObserver`) must be written as the
> underlying object via `name->AsObject()`; `GetRefPtr()` would yield the
> interface pointer, not the `IRemoteObject` `WriteRemoteObject` expects.
>
> **Null guard**: the Proxy null-checks every `sptr` parameter *before*
> evaluating the accessor (`name->AsObject()` / `name.GetRefPtr()` dereferences
> a null `sptr` and is UB). The Stub null-checks `ReadRemoteObject()` and
> `iface_cast` results before forwarding them to the service.

Parcelable (`AAFwk::Want`, `Configuration`) and `std::vector<T>` parameters are
**not** in this table — the generator rejects them at input with a clear
diagnostic (see [Variations](#variations-the-generator-does-not-cover)).

## MessageOption (sync / async)

```cpp
MessageOption option(MessageOption::TF_SYNC);  // wait for reply
MessageOption option(MessageOption::TF_ASYNC); // fire-and-forget
```

The generator asks `is_async` and emits the right flag. Async (one-way) IPC
has no reply, so the generator forces `void` return type when `is_async` is
selected — a non-void method cannot use `TF_ASYNC`. Async methods use
`_NORET` macros on the proxy side.

## Error Codes Used in Generated Code

`AppMgrResultCode` is transported as `int32_t` over IPC, so its IPC-layer error
codes share the `int32_t` column; the Client maps the result back to the enum.

| Context | `int32_t` / `AppMgrResultCode` (IPC transport) | `bool` | `std::string` | `void` |
|---|---|---|---|---|
| Proxy write-token / param-write failure | `IPC_PROXY_ERR` | `false` | `""` | `return;` |
| Proxy SendRequest failure | transparent `SendRequest` return code (`_RET_INT` macro returns `ret`; explicit branch returns the type-appropriate error) | `false` | `""` | `return;` |
| Proxy reply-read failure | `IPC_PROXY_ERR` | `false` | `""` | `return;` |
| Service `IsReady()` failure | `AAFwk::ERR_APP_MGR_SERVICE_NOT_READY` | `false` | `""` | `return;` |
| Stub param-read failure | `ERR_INVALID_VALUE` (all return types) | | | |
| Stub write-reply failure | `IPC_STUB_ERR` (all return types) | | | |
| Stub success | `ERR_NONE` (all return types) | | | |

> The `int32_t` SendRequest path uses `PARCEL_UTIL_SENDREQ_RET_INT`, whose
> send-failure branch returns the actual `SendRequest` return code (transparent),
> **not** a fixed `IPC_PROXY_ERR`. Only the token / parameter-write failure
> path returns the fixed `IPC_PROXY_ERR`.

## Stub Dispatch (Handle* Pattern)

The stub's `OnRemoteRequest()` fans out to a series of `OnRemoteRequestInnerN`
functions (currently up to Ninth). Each case delegates to a `Handle<ApiName>`
method that owns parameter reads and reply writes. New APIs must follow the
same shape.

### Inserting the case

Read the current fan-out in `app_mgr_stub.cpp` and pick the `OnRemoteRequestInnerN`
whose code range covers the new enum value:

```cpp
// OnRemoteRequestInnerFirst handles the low codes
// OnRemoteRequestInnerNinth handles the most recent additions
```

The case line is:

```cpp
case static_cast<uint32_t>(AppMgrInterfaceCode::APP_SOME_METHOD):
    return HandleSomeMethod(data, reply);
```

### Defining the Handle method

Append near the bottom of `app_mgr_stub.cpp`, and declare it in `app_mgr_stub.h`:

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

> The Stub example is kept in sync with the generator's `stub_cpp` snippet:
> bool-form `ReadString16(out)` + `ERR_INVALID_VALUE` on failure (a truncated
> request must not feed a default value into the business layer), and
> `WriteInt32(result)` without an enum cast (`result` is already `int32_t` on
> the IPC transport).

## Naming Conventions

- **Methods**: camelCase — `GetConfiguration`, `PreloadApplication`.
- **IPC enum**: `APP_UPPER_SNAKE_CASE` — `APP_GET_CONFIGURATION`. The script derives it from the method name.
- **Parameters**: camelCase — `bundleName`, `userId`.
- **Member variables**: camelCase with trailing underscore — `mgrHolder_`, `appMgrServiceInner_`.

## Variations the Generator Does NOT Cover

These are rejected at input or need manual adjustment after generation:

- **Nullable sptr**: real code writes a `bool` sentinel before the optional object (see `AppMgrProxy::MakeImage`). Add by hand.
- **Parcelable parameters** (`AAFwk::Want`, `Configuration`) and **`std::vector<T>` parameters**: the generator **rejects these at input** with a clear diagnostic rather than emit broken-looking `WriteObject`/`WriteVector` calls (these need type-specific marshaling the generator does not model). Add the parameter and its symmetric read/write by hand after generation.
- **Async business logic with task queue**: `AppMgrService::AttachApplication` submits a lambda to `taskHandler_`. If the new API needs that, add it inside `AppMgrService::Xxx` before delegating.
- **`XCOLLIE_TIMER_LESS(__PRETTY_FUNCTION__)`**: long-running service methods add this at the top of the service impl; add by hand if the API may block.
