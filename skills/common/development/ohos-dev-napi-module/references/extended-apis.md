# OpenHarmony Extended APIs

OpenHarmony provides many extension APIs beyond Node.js standard library. These APIs are specific to OpenHarmony and not available in Node.js N-API.

## Runtime Environment Management

```cpp
// Create/destroy Ark runtime
napi_status napi_create_ark_runtime(napi_env *env);
napi_status napi_destroy_ark_runtime(napi_env *env);

// Event loop control
napi_status napi_run_event_loop(napi_env env, napi_event_mode mode);
napi_status napi_stop_event_loop(napi_env env);

typedef enum {
    napi_event_mode_default = 0,  // Block until no tasks
    napi_event_mode_nowait = 1,   // Non-blocking, process one task
} napi_event_mode;
```

## QoS (Quality of Service) Priority

```cpp
typedef enum {
    napi_qos_background = 0,      // Low priority, invisible tasks
    napi_qos_utility = 1,         // Medium-low priority
    napi_qos_default = 2,         // Default priority
    napi_qos_user_initiated = 3,  // High priority, user-visible
} napi_qos_t;

// Queue async work with QoS priority
napi_status napi_queue_async_work_with_qos(napi_env env,
                                           napi_async_work work,
                                           napi_qos_t qos);
```

## Sendable Object APIs (For Concurrent Programming)

OpenHarmony provides Sendable objects for concurrent programming with worker threads:

```cpp
// Create Sendable objects
napi_status napi_create_sendable_array(napi_env env, napi_value* result);
napi_status napi_create_sendable_array_with_length(napi_env env, size_t length, napi_value* result);
napi_status napi_create_sendable_arraybuffer(napi_env env, size_t byte_length, void** data, napi_value* result);
napi_status napi_create_sendable_typedarray(napi_env env, napi_typedarray_type type,
                                            size_t length, napi_value arraybuffer,
                                            size_t byte_offset, napi_value* result);
napi_status napi_create_sendable_object_with_properties(napi_env env,
                                                         size_t property_count,
                                                         const napi_property_descriptor* properties,
                                                         napi_value* result);

// Define Sendable class
napi_status napi_define_sendable_class(napi_env env, const char* utf8name,
                                       size_t length, napi_callback constructor,
                                       void* data, size_t property_count,
                                       const napi_property_descriptor* properties,
                                       napi_value parent, napi_value* result);

// Wrap/unwrap Sendable objects
napi_status napi_wrap_sendable(napi_env env, napi_value js_object,
                               void* native_object, napi_finalize finalize_cb,
                               void* finalize_hint);
napi_status napi_wrap_sendable_with_size(napi_env env, napi_value js_object,
                                         void* native_object, napi_finalize finalize_cb,
                                         void* finalize_hint, size_t native_binding_size);
napi_status napi_unwrap_sendable(napi_env env, napi_value js_object, void** result);
napi_status napi_remove_wrap_sendable(napi_env env, napi_value js_object, void** result);

// Check if object is Sendable
napi_status napi_is_sendable(napi_env env, napi_value value, bool* result);
```

## Serialization APIs

```cpp
// Serialize ArkTS object to native data
napi_status napi_serialize(napi_env env, napi_value object,
                           napi_value transfer_list, napi_value clone_list,
                           void** result);

// Deserialize native data to ArkTS object
napi_status napi_deserialize(napi_env env, void* buffer, napi_value* object);

// Delete serialization data
napi_status napi_delete_serialization_data(napi_env env, void* buffer);
```

## Enhanced Wrap Functions

```cpp
// Enhanced wrap with async finalizer and memory size tracking
napi_status napi_wrap_enhance(napi_env env, napi_value js_object,
                              void* native_object, napi_finalize finalize_cb,
                              bool async_finalizer, void* finalize_hint,
                              size_t native_binding_size, napi_ref* result);

// Key differences from standard napi_wrap:
// 1. async_finalizer: Execute finalize callback asynchronously (must be thread-safe)
// 2. native_binding_size: Track native object size for GC triggering
// 3. When accumulated size reaches GC threshold, runtime triggers garbage collection
```

## Module Loading APIs

```cpp
// Load system module or custom module
napi_status napi_load_module(napi_env env, const char* path, napi_value* result);

// Load module with info (usable in new Ark runtime)
napi_status napi_load_module_with_info(napi_env env, const char* path,
                                       const char* module_info, napi_value* result);

// Run specific abc file
napi_status napi_run_script_path(napi_env env, const char* abcPath, napi_value* result);
```

## Native Binding Object APIs

```cpp
// Coerce to native binding object with detach/attach callbacks
napi_status napi_coerce_to_native_binding_object(napi_env env, napi_value js_object,
                                                 napi_native_binding_detach_callback detach_cb,
                                                 napi_native_binding_attach_callback attach_cb,
                                                 void* native_object, void* hint);
```

## Priority-based Threadsafe Function Call

```cpp
typedef enum {
    napi_task_priority_high = 0,
    napi_task_priority_medium = 1,
    napi_task_priority_low = 2,
} napi_task_priority;

// Call threadsafe function with priority and queue position
napi_status napi_call_threadsafe_function_with_priority(napi_threadsafe_function func,
                                                         void *data,
                                                         napi_task_priority priority,
                                                         bool isTail);
// isTail: true - queue at tail, false - execute immediately
```

## Object Creation Helpers

```cpp
// Create object with properties in one call
napi_status napi_create_object_with_properties(napi_env env, napi_value* result,
                                                size_t property_count,
                                                const napi_property_descriptor* properties);

// Create object with named properties
napi_status napi_create_object_with_named_properties(napi_env env, napi_value* result,
                                                     size_t property_count,
                                                     const char** keys,
                                                     const napi_value* values);
```

## When to Use Extended APIs

1. **Sendable APIs**: Use when sharing objects between worker threads
   - Required for concurrent programming
   - Provides thread-safe object sharing
   - Better performance than standard approaches

2. **QoS APIs**: Use for performance optimization
   - Background tasks: data sync, backup
   - Utility tasks: downloads, imports
   - User-initiated tasks: opening documents

3. **Enhanced Wrap**: Use for complex native bindings
   - When finalize callback needs async execution
   - When tracking native object memory size
   - For better GC control

4. **Serialization APIs**: Use for cross-thread communication
   - Worker thread data transfer
   - State persistence
   - IPC scenarios

5. **Runtime APIs**: Use in worker or special contexts
   - Creating isolated runtime environments
   - Manual event loop control
   - Custom threading scenarios