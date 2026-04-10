---
name: appmgr-api-generator
description: Generate complete API implementation chain from AppMgrClient to AppMgrServiceInner. Use when adding new interfaces to the app_manager service that require: (1) Client implementation, (2) IPC proxy/stub code, (3) AppMgrService service implementation, (4) AppMgrServiceInner business logic implementation, (5) Complete call chain: client.cpp → proxy.cpp → stub.cpp → service.cpp → service_inner.cpp
---

# AppMgr API Generator

Automatically generate complete API call chain from client to service for new AppMgr APIs.

## Quick Start

Ask: "Add a new API named [ApiName] with parameters [params] and return type [type]"

The skill will:
1. Ask for interface details (name, parameters, return type, functionality)
2. Generate all necessary code modifications
3. Show diff preview for each file

## Generated Files

For each new API, code is generated for the following files:
- `interfaces/inner_api/app_manager/include/appmgr/app_mgr_client.h`
- `interfaces/inner_api/app_manager/src/appmgr/app_mgr_client.cpp`
- `interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h`
- `interfaces/inner_api/app_manager/include/appmgr/app_mgr_proxy.h`
- `interfaces/inner_api/app_manager/src/appmgr/app_mgr_proxy.cpp`
- `interfaces/inner_api/app_manager/include/appmgr/app_mgr_interface.h`
- `services/appmgr/include/app_mgr_service.h` (**NEW**)
- `services/appmgr/src/app_mgr_service.cpp` (**NEW**)
- `services/appmgr/src/app_mgr_service_inner.cpp`
- `services/appmgr/src/app_mgr_service_inner.h`
- `services/appmgr/src/appmgrstub/app_mgr_stub.cpp`

## Workflow

1. **Interface Definition**: Provide API name, parameters, return type
2. **Code Generation**: Use `scripts/generate_appmgr_api.py`
3. **Review**: Check generated code before applying changes
4. **Apply**: Apply changes to all files in the call chain

## Architecture Overview

Complete call chain path:
```
AppMgrClient → AppMgrProxy → IPC → AppMgrStub → AppMgrService → AppMgrServiceInner
```

- **AppMgrClient**: Client-side API wrapper
- **AppMgrProxy**: Client-side IPC proxy, marshals parameters
- **AppMgrStub**: Server-side IPC handler, unmarshals parameters
- **AppMgrService**: Service implementation, checks service status and delegates
- **AppMgrServiceInner**: Business logic implementation

## Implementation Notes

- Follow existing code patterns in ability_runtime
- Generate appropriate IPC serialization/deserialization code
- Handle synchronous/asynchronous calls appropriately
- Include error handling and logging
- **Important**: Ensure to include AppMgrService layer implementation (was missing in previous versions)

See [references/patterns.md](references/patterns.md) for advanced patterns or special cases.
