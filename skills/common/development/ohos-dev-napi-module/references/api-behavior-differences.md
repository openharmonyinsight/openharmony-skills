# API Behavior Differences from Node.js Standard Library

This document provides detailed API behavior differences between OpenHarmony NAPI and Node.js standard library that developers must be aware of when porting code.

## Error Handling APIs

**napi_throw_error / napi_throw_type_error / napi_throw_range_error**:
- OpenHarmony: No validation when code is nullptr
- Node.js: Returns napi_invalid_arg when code is nullptr
- Allows code attribute setting to fail

**napi_create_error**:
- OpenHarmony: code parameter supports String or Number type
- Node.js: code parameter only supports String type
- Returns napi_invalid_arg when type mismatch

**napi_create_type_error / napi_create_range_error**:
- OpenHarmony: Creates Error type, not TypeError/RangeError
- Node.js: Creates correct error types (TypeError/RangeError)

## Object and Property APIs

**napi_create_reference**:
- OpenHarmony: No type restriction on value parameter
- Node.js: Only supports Object/Function/Symbol types

**napi_wrap**:
- OpenHarmony: Returns napi_invalid_arg when finalize_cb is nullptr
- Node.js: Allows finalize_cb to be nullptr
- OpenHarmony: Returns strong reference when result is not nullptr
- Node.js: Returns weak reference

**napi_delete_reference**:
- OpenHarmony: Triggers finalize callback when deleting strong reference
- Node.js: Callback triggered during object destruction

## Array and TypedArray APIs

**napi_get_typedarray_info**:
- OpenHarmony: Returns byte length of elements
- Node.js: Returns element count
- OpenHarmony: Supports Sendable TypedArray types
- Node.js: Standard TypedArray only

**napi_is_typedarray**:
- OpenHarmony: Supports Sendable TypedArray
- Node.js: Standard TypedArray only

**napi_set_element**:
- OpenHarmony: Attempts memory allocation for large index
- Node.js: Throws exception and crashes process

**napi_create_array_with_length / napi_create_arraybuffer**:
- OpenHarmony: Attempts memory allocation for large length
- Node.js: Throws exception and crashes process

## Async Work APIs

**napi_create_async_work / napi_queue_async_work**:
- OpenHarmony: Does not support async_hooks resource management
- Node.js: Full async_hooks support
- OpenHarmony: No validation on async_resource_name type

**napi_cancel_async_work**:
- OpenHarmony: No validation on uv return values
- Node.js: Returns specific error codes based on uv failure

## Threadsafe Function APIs

**napi_create_threadsafe_function**:
- OpenHarmony: initial_thread_count limit is 128
- Node.js: No specific limit documented
- OpenHarmony: No type restriction on async_resource and func
- Node.js: Type restrictions apply

**napi_call_threadsafe_function / napi_release_threadsafe_function**:
- OpenHarmony: Checks if env is alive before calling uv_async_send
- Node.js: No such check

**napi_ref_threadsafe_function / napi_unref_threadsafe_function**:
- OpenHarmony: Validates func and env are from same ArkTS thread
- Node.js: No such validation

## Buffer APIs

**napi_create_buffer / napi_create_buffer_copy / napi_create_external_buffer**:
- OpenHarmony: Creates ArrayBufferLike type
- Node.js: Creates Buffer type
- OpenHarmony: size limit 2097152 bytes
- OpenHarmony: Returns napi_invalid_arg for invalid parameters

## Property Operation APIs

Most property APIs (napi_set_property, napi_get_property, etc.):
- OpenHarmony: Returns napi_object_expected for non-Object/Function
- Node.js: May throw exceptions or have different behavior

**napi_define_properties**:
- OpenHarmony: Clears exception and continues execution during property setup
- Node.js: Throws exception immediately

## Additional Differences

- `napi_coerce_to_object`: Returns undefined for null/undefined input
- `napi_instanceof`: Returns error codes without throwing exceptions
- `napi_run_script`: Empty implementation (use napi_run_script_path instead)
- `napi_get_node_version`: Empty implementation (not needed in OpenHarmony)
- `napi_add_finalizer`: Different callback timing and exception handling