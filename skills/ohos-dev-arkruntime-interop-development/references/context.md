# Interop Context (`InteropCtx`)

`InteropCtx` is the heart of the interop runtime. It is defined in `interop_context.h`.

## Responsibilities

1.  **State Management**: Holds `napi_env` (JS environment) and links to `EtsCoroutine`.
2.  **Caching**: Maintains `JSRefConvertCache` to avoid recreating converters for commonly used types.
3.  **String Storage**: Manages `JSValueStringStorage` and `ConstStringStorage` for efficient string passing.
4.  **Proxies**: Manages `CommonJSObjectCache` and provides access to `JSProxy` and `EtsClassWrapper` caches.
5.  **Exceptions**: Provides utilities to throw JS or ETS errors (`ThrowJSError`, `ThrowETSError`).

## Accessing the Context

You can retrieve the current context from the current coroutine:

```cpp
auto coro = EtsCoroutine::GetCurrent();
auto ctx = InteropCtx::Current(coro);
napi_env env = ctx->GetJSEnv();
```

## Shared State

`SharedEtsVmState` holds data that is shared across multiple contexts/threads, such as:
-   Global class references (`jsRuntimeClass`, `jsValueClass`, etc.).
-   The `PandaEtsVM` instance.
-   Proxy maps.
