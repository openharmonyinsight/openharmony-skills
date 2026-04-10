# AppMgr API Patterns Reference

This document describes common patterns used in AppMgr API implementation.

## Common Return Types

### AppMgrResultCode
Used for operations that need explicit success/failure indication:
```cpp
virtual AppMgrResultCode SomeMethod();

// Client implementation:
AppMgrResultCode AppMgrClient::SomeMethod() {
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service != nullptr) {
        int32_t result = service->SomeMethod();
        if (result == ERR_OK) {
            return AppMgrResultCode::RESULT_OK;
        }
        return AppMgrResultCode::ERROR_SERVICE_NOT_READY;
    }
    return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;
}
```

### int32_t
Used for operations returning integer results or error codes:
```cpp
virtual int32_t SomeMethod();

// Client implementation:
int32_t AppMgrClient::SomeMethod() {
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;
    }
    return service->SomeMethod();
}
```

### void
Used for async operations with no return value:
```cpp
virtual void SomeMethod();

// Client implementation:
void AppMgrClient::SomeMethod() {
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service != nullptr) {
        service->SomeMethod();
    }
}
```

## Parameter Marshaling

### Common Types
```cpp
// std::string
PARCEL_UTIL_WRITE(data, String16, Str8ToStr16(paramName));
// Read:
std::string paramName = Str16ToStr8(data.ReadString16());

// int32_t
PARCEL_UTIL_WRITE(data, Int32, paramName);
// Read:
int32_t paramName = data.ReadInt32();

// bool
PARCEL_UTIL_WRITE(data, Bool, paramName);
// Read:
bool paramName = data.ReadBool();

// sptr<IRemoteObject>
PARCEL_UTIL_WRITE(data, RemoteObject, paramName.GetRefPtr());
// Read:
sptr<IRemoteObject> paramName = data.ReadRemoteObject();

// std::vector<T>
PARCEL_UTIL_WRITE(data, Vector, paramName);
// Read:
std::vector<T> paramName;
// Note: Vector reading requires template specialization
```

## IPC Message Options

```cpp
// Sync call (waits for response)
MessageOption option(MessageOption::TF_SYNC);

// Async call (fire and forget)
MessageOption option(MessageOption::TF_ASYNC);
```

## Common Parameter Types

| Type | Declaration | Write | Read |
|------|-------------|-------|------|
| std::string | const std::string &name | String16, Str8ToStr16(name) | Str16ToStr8(ReadString16()) |
| int32_t | int32_t value | Int32, value | ReadInt32() |
| bool | bool flag | Bool, flag | ReadBool() |
| sptr<IRemoteObject> | const sptr<IRemoteObject> &token | RemoteObject, token.GetRefPtr() | ReadRemoteObject() |
| pid_t | pid_t pid | Int32, pid | ReadInt32() |
| std::vector<T> | const std::vector<T> &items | Vector, items | (requires template) |

## Const Methods

For methods that don't modify state:
```cpp
virtual int32_t SomeMethod() const;
                                    ^^^^^
```

## Template Methods

Some interface methods have default implementations in the base class:
```cpp
virtual int32_t SomeMethod() {
    return 0;  // Default implementation
}
```

Override these in service implementation only when needed.

## Naming Conventions

- **Methods**: camelCase (e.g., `GetConfiguration`)
- **IPC Codes**: UPPER_SNAKE_CASE with APP_ prefix (e.g., `APP_GET_CONFIGURATION`)
- **Parameters**: camelCase (e.g., `bundleName`, `userId`)
- **Member Variables**: camelCase with trailing underscore (e.g., `mgrHolder_`)
