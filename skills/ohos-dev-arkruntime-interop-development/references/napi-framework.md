# ArkUI NAPI Project Overview

The `foundation/arkui/napi` repository provides a framework for extending JavaScript Native Modules using the Node.js N-API standard.

## Architecture Components
- **NativeEngine**: Abstraction layer for different JS engines.
- **ModuleManager**: Handles loading, caching, and management of NAPI modules.
- **ScopeManager & ReferenceManager**: Manage lifecycle of `NativeValue` and `NativeReference`.

## Building and Testing
- **Build Targets**: `//foundation/arkui/napi:ace_napi`, `//foundation/arkui/napi:napi_packages`.
- **Unit Tests**: `test/unittest`.
- **Fuzz Tests**: `test/fuzztest`.

## Development Conventions
- **NAPI Standard**: Follow N-API design patterns.
- **Memory Management**: Use `napi_handle_scope` and `napi_ref` carefully.
- **Error Handling**: Use `NAPI_CALL` and related macros.
- **Performance**: Use `napi_create_async_work` for CPU-intensive tasks.