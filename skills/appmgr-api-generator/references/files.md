# AppMgr File Structure

This document describes the files involved in the AppMgr API call chain.

## Call Chain Overview

```
AppMgrClient
    ↓ (method call)
AppMgrProxy
    ↓ (IPC SendRequest)
AppMgrStub
    ↓
AppMgrService
    ↓
AppMgrServiceInner
```

## Files and Their Roles

### Client Side

**interfaces/inner_api/app_manager/include/appmgr/app_mgr_client.h**
- Declares `AppMgrClient` class
- Public API declarations that external code uses
- Example:
```cpp
class AppMgrClient {
public:
    virtual AppMgrResultCode SomeMethod(const std::string &param);
};
```

**interfaces/inner_api/app_manager/src/appmgr/app_mgr_client.cpp**
- Implements `AppMgrClient` methods
- Gets remote service and calls through it
- Example:
```cpp
AppMgrResultCode AppMgrClient::SomeMethod(const std::string &param) {
    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service != nullptr) {
        int32_t result = service->SomeMethod(param);
        return result == ERR_OK ? RESULT_OK : ERROR_SERVICE_NOT_READY;
    }
    return ERROR_SERVICE_NOT_CONNECTED;
}
```

### IPC Layer

**interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h**
- Defines `AppMgrInterfaceCode` enum
- Each API needs a unique code
- Example:
```cpp
enum class AppMgrInterfaceCode {
    APP_SOME_METHOD = 125,
    // Add new codes at the bottom
};
```

**interfaces/inner_api/app_manager/include/appmgr/app_mgr_proxy.h**
- Declares `AppMgrProxy` class (inherits from `IRemoteProxy<IAppMgr>`)
- Proxy methods are called by client
- Example:
```cpp
class AppMgrProxy : public IRemoteProxy<IAppMgr> {
public:
    int32_t SomeMethod(const std::string &param) override;
};
```

**interfaces/inner_api/app_manager/src/appmgr/app_mgr_proxy.cpp**
- Implements `AppMgrProxy` methods
- Marshals parameters and sends IPC request
- Example:
```cpp
int32_t AppMgrProxy::SomeMethod(const std::string &param) {
    MessageParcel data;
    MessageParcel reply;
    MessageOption option(MessageOption::TF_SYNC);
    if (!WriteInterfaceToken(data)) {
        return ERR_NULL_OBJECT;
    }
    PARCEL_UTIL_WRITE(data, String16, Str8ToStr16(param));
    PARCEL_UTIL_SENDREQ(AppMgrInterfaceCode::APP_SOME_METHOD, data, reply, option);
    return reply.ReadInt32();
}
```

**interfaces/inner_api/app_manager/include/appmgr/app_mgr_interface.h**
- Defines `IAppMgr` interface
- Both Proxy and Stub implement this
- Example:
```cpp
class IAppMgr : public IRemoteBroker {
public:
    virtual int32_t SomeMethod(const std::string &param) = 0;
};
```

**services/appmgr/src/appmgrstub/app_mgr_stub.cpp**
- Implements `AppMgrStub` class (server-side IPC handler)
- Deserializes parameters and calls AppMgrService
- Example:
```cpp
int32_t AppMgrStub::OnRemoteRequest(uint32_t code, MessageParcel& data, ...) {
    switch (code) {
        case AppMgrInterfaceCode::APP_SOME_METHOD: {
            std::string param = Str16ToStr8(data.ReadString16());
            auto result = this->SomeMethod(param);
            reply.WriteInt32(result);
            return ERR_NONE;
        }
    }
}
```

### Server Side

**services/appmgr/include/app_mgr_service.h**
- Declares `AppMgrService` class (inherits from AppMgrStub and SystemAbility)
- Service layer implementation declarations
- Example:
```cpp
class AppMgrService : public SystemAbility, public AppMgrStub {
public:
    int32_t SomeMethod(const std::string &param);
};
```

**services/appmgr/src/app_mgr_service.cpp**
- Implements `AppMgrService` methods
- Service readiness check and delegates to AppMgrServiceInner
- Example:
```cpp
int32_t AppMgrService::SomeMethod(const std::string &param) {
    TAG_LOGD(AAFwkTag::APPMGR, "call");
    if (!IsReady()) {
        TAG_LOGE(AAFwkTag::APPMGR, "Service not ready");
        return AAFwk::ERR_APP_MGR_SERVICE_NOT_READY;
    }
    return appMgrServiceInner_->SomeMethod(param);
}
```

**services/appmgr/src/app_mgr_service_inner.h**
- Declares `AppMgrServiceInner` class
- Business logic implementation declarations
- Example:
```cpp
class AppMgrServiceInner {
public:
    int32_t SomeMethod(const std::string &param);
};
```

**services/appmgr/src/app_mgr_service_inner.cpp**
- Implements `AppMgrServiceInner` methods
- Actual business logic implementation
- Example:
```cpp
int32_t AppMgrServiceInner::SomeMethod(const std::string &param) {
    TAG_LOGD(AAFwkTag::APPMGR, "called");
    // Actual implementation goes here
    return ERR_OK;
}
```

## Add New API - Checklist

1. [ ] Add method to `app_mgr_client.h`
2. [ ] Add implementation to `app_mgr_client.cpp`
3. [ ] Add enum to `app_mgr_ipc_interface_code.h`
4. [ ] Add method to `app_mgr_proxy.h`
5. [ ] Add implementation to `app_mgr_proxy.cpp`
6. [ ] Add method to `app_mgr_interface.h`
7. [ ] Add case to `app_mgr_stub.cpp` (OnRemoteRequest switch)
8. [ ] Add method to `app_mgr_service.h`
9. [ ] Add implementation to `app_mgr_service.cpp`
10. [ ] Add method to `app_mgr_service_inner.h`
11. [ ] Add implementation to `app_mgr_service_inner.cpp`

## Common Pitfalls

- **Missing IPC code**: Each new API needs a unique enum value in `AppMgrInterfaceCode`
- **Wrong return types**: Client usually returns `AppMgrResultCode` while interface returns `int32_t`
- **Missing const**: Methods that don't modify state should be marked as `const`
- **Wrong serialization**: Strings need `Str8ToStr16()` when writing, `Str16ToStr8()` when reading
- **Unread parameters**: All parameters must be read from MessageParcel in the stub
- **Missing AppMgrService layer**: Don't forget the service layer between stub and inner implementations
