# Async Work Pattern

OpenHarmony's async work pattern follows Node.js N-API conventions but with some implementation differences.

## Complete Pattern

```cpp
struct AsyncContext {
    napi_env env;
    napi_async_work asyncWork;
    napi_deferred deferred;
    // Add your data fields here
};

static napi_value AsyncMethod(napi_env env, napi_callback_info info)
{
    // Create promise
    napi_deferred deferred;
    napi_value promise;
    napi_create_promise(env, &deferred, &promise);
    
    // Create async context
    AsyncContext* context = new AsyncContext;
    context->env = env;
    context->deferred = deferred;
    
    // Create async work
    napi_value resourceName;
    napi_create_string_latin1(env, "AsyncMethod", NAPI_AUTO_LENGTH, &resourceName);
    
    napi_create_async_work(
        env,
        nullptr,
        resourceName,
        [](napi_env env, void* data) {
            // Execute callback (background thread)
            AsyncContext* context = (AsyncContext*)data;
            // Do your work here
        },
        [](napi_env env, napi_status status, void* data) {
            // Complete callback (main thread)
            AsyncContext* context = (AsyncContext*)data;
            
            // Resolve or reject promise
            napi_value result;
            napi_create_string_utf8(env, "result", NAPI_AUTO_LENGTH, &result);
            napi_resolve_deferred(env, context->deferred, result);
            
            // Cleanup
            napi_delete_async_work(env, context->asyncWork);
            delete context;
        },
        context,
        &context->asyncWork
    );
    
    napi_queue_async_work(env, context->asyncWork);
    return promise;
}
```

## Key Components

### 1. AsyncContext Structure
- Stores all data needed for async operation
- Contains napi_env, async_work, and deferred
- Custom data fields depend on your use case

### 2. Execute Callback (Background Thread)
- Runs on worker thread
- Perform heavy computations here
- Do NOT call NAPI functions here (except specific allowed ones)
- Must be thread-safe

### 3. Complete Callback (Main Thread)
- Runs on main JS thread
- Can call NAPI functions
- Resolve/reject the promise
- Cleanup resources (delete async work and context)

### 4. Promise-based Return
- Returns a promise to JS caller
- JS code can use `await` or `.then()/.catch()`

## Important Notes for OpenHarmony

**async_hooks Support**:
- OpenHarmony: Does NOT support async_hooks resource management
- Node.js: Full async_hooks support
- async_resource_name is not validated in OpenHarmony

**Memory Management**:
- Always delete async work in complete callback
- Always delete context in complete callback
- Prevent memory leaks by proper cleanup

**Thread Safety**:
- Execute callback runs on background thread
- Complete callback runs on main JS thread
- Do not share napi_env across threads
- Use napi_threadsafe_function for cross-thread communication

## QoS Priority Extension

OpenHarmony provides QoS-based async work scheduling:

```cpp
napi_status napi_queue_async_work_with_qos(napi_env env,
                                           napi_async_work work,
                                           napi_qos_t qos);
```

QoS levels:
- `napi_qos_background`: Low priority, invisible tasks
- `napi_qos_utility`: Medium-low priority
- `napi_qos_default`: Default priority
- `napi_qos_user_initiated`: High priority, user-visible tasks

## Error Handling

Check napi_status for all async work operations:

```cpp
napi_status status = napi_create_async_work(...);
if (status != napi_ok) {
    delete context;
    napi_reject_deferred(env, deferred, error);
    return promise;
}
```

## Best Practices

1. Use promise-based async pattern
2. Clean up resources in complete callback
3. Handle errors properly
4. Consider QoS priority for performance optimization
5. Ensure thread safety in execute callback
6. Do not access shared state without proper synchronization