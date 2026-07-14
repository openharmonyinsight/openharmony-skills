# NAPI Memory Management Background

## Why Scope Management is Required

When leaving the current scope, the C-side `napi_value` temporary variable is released, but the handles in the Handle Table and the JS object memory are not released and become inaccessible. During GC cleanup, the JS object is considered to have a reference (the reference in the handle table), leading to memory leaks.

## Handle Table and Scope Management

**Handle Table:** Indirect addressing → manages actual addresses in JS heap

**Scope Management Logic:**
- Handle table maintains a pointer to the current stack top
- When opening a scope, a start point is marked in the HandleTable
- When closing the scope, the stack top pointer retreats to the scope's marked position
- This logically cleans up handles in the local scope
- During subsequent GC, corresponding JS objects are considered unreferenced and not marked as active, allowing GC to clean them up

## JS Memory Management - GC (Garbage Collection)

### Mark-and-Sweep Algorithm

GC periodically finds variables that are no longer in use and releases the memory they occupy.

**Key Concepts:**
- **Root Objects:** Global objects (window/global), variables (in the current execution stack), parameters
- **Reachable Objects:** Objects accessible through reference chains from root objects
- **Unreachable Objects:** Objects that cannot be traced from root objects are considered "garbage"
- **Mark Phase:** GC traverses from root objects, marking all accessible objects as "active"
- **Sweep Phase:** Traverses memory, destroys unmarked objects (unreachable objects)
- **Fragmentation:** Clearing creates memory fragments, usually combined with "Mark-Compact" algorithm

## C++ Memory Management

### Core Mechanisms

**Stack:**
- Stores local variables
- Automatically allocated and released by compiler
- High execution efficiency, limited space

**Heap:**
- Stores dynamically allocated objects (via `new` or `malloc`)
- Must be manually released, otherwise memory leaks occur

**Global/Static Area:**
- Stores global and static variables
- Released when program ends

### RAII (Resource Acquisition Is Initialization)

**Principle:** Uses the characteristic that "stack objects automatically call destructors when leaving scope" to write resource release logic in destructors.

**Effect:** When creating a memory-managed object, the heap memory it manages is automatically released when the object leaves scope, without waiting for GC scanning.

### Smart Pointers

**std::unique_ptr (Exclusive Pointer):**
- Only one pointer can own the object at a time
- Released when pointer goes out of scope

**std::shared_ptr (Shared Pointer):**
- Uses reference counting
- Count +1 when more pointers point to it
- Count -1 when pointer is destroyed
- Released when count reaches 0

**std::weak_ptr (Weak Pointer):**
- Solves circular reference problems similar to JS
- Observes objects without increasing reference count
- Does not prevent objects from being reclaimed

## NAPI_VALUE Memory Management

### Scope Management

- **Scope:** Similar to C++ stack management mechanism, opens a local scope
- Local variables applied within the scope are released when leaving the scope

### Persistent References (napi_ref)

A local `napi_value` is only valid within its scope (and only on its creating JS thread). To keep a JS object alive beyond the current scope — or to reach it from another thread/async work — use a persistent reference.

- **Create:** `napi_create_reference(env, value, initial_refcount, &ref)`. The second argument is the initial reference count: `1` creates a **strong** reference (keeps the JS object alive), `0` creates a **weak** reference (does not prevent GC).
- **Must be paired with delete:** Every `napi_create_reference` needs a matching `napi_delete_reference`. Forgetting it leaks the reference slot and (for a strong ref) pins the JS object forever.
- **Typical lifecycle:** create the `napi_ref` on the JS thread → do background work without touching NAPI → back on the JS thread, `napi_get_reference_value` to retrieve the value, use it, then `napi_delete_reference`. This is the pattern used by `NapiAsyncTask::ResolveWithNoError` in Ability Runtime.
- **Crossing threads:** Never carry a raw `napi_value`/`napi_env` into another thread. Carry a `napi_ref` (or use `napi_threadsafe_function`) and resolve it back on the JS thread.
- **OpenHarmony difference:** deleting a **strong** reference triggers the object's finalize immediately on that thread. If the wrapped native object does non-trivial teardown, it runs synchronously inside `napi_delete_reference` — be aware of reentrancy. Node.js does not guarantee this timing.

### napi_wrap and Finalizers

- `napi_wrap(env, jsObject, nativePtr, finalizer, finalizeHint, &result)` binds a C++ instance to a JS object so the native object can be reclaimed when the JS object is GC'd.
- **Non-null finalizer required on OpenHarmony:** the finalizer must free the wrapped native object (`delete static_cast<T*>(nativePtr)`). A null finalizer leaves the native object leaked.
- **Retrieve / remove:** `napi_unwrap` to fetch the native pointer, `napi_remove_wrap` to detach and take ownership back. `napi_remove_wrap` runs the finalizer unless ownership was transferred.
- **napi_add_finalizer:** attaches a finalizer without wrapping (used when there is no native pointer to store). The same non-null-finalizer expectation applies.

### Quick reference table

| Need | API |
| --- | --- |
| Release temporaries at scope exit | `HandleScope` / `napi_open_handle_scope` |
| Promote one handle to parent scope | `HandleEscape` / `napi_escape_handle` |
| Keep a JS object alive across scope/thread | `napi_create_reference` + `napi_delete_reference` |
| Bind native lifetime to JS object | `napi_wrap` (+ non-null finalizer) |
| Attach cleanup without wrap | `napi_add_finalizer` |
| Call JS from another thread | `napi_threadsafe_function` or `napi_async_work` |

### napi_value Lifecycle

**Note:** The execution of the following functions creates corresponding objects in JS and returns corresponding handle addresses to the C side, so attention must be paid to using scope management.

**Basic Data Type Creation:**
- `napi_create_int32`, `napi_create_uint32`, `napi_create_int64`
- `napi_create_double`, `napi_create_bigint_int64`, `napi_create_bigint_uint64`
- `napi_create_string_utf8`, `napi_create_string_utf16`, `napi_create_string_latin1`

**Other Creations:**
- `napi_create_array`, `napi_create_array_with_length`
- `napi_new_instance` (class creation)
- `napi_create_function` (function creation)

### NAPI Management Functions

**Low-level API:**
- `napi_open_handle_scope`, `napi_close_handle_scope` - Open and reclaim handle contents in handle table
- `napi_open_escapable_handle_scope`, `napi_close_escapable_handle_scope` - Escapable handle scope
- `napi_escape_handle` - Promote ArkTS object lifecycle to parent scope

**js_runtime_utils Wrapper:**
- **HandleScope:** Constructor calls `napi_open_handle_scope`, destructor calls `napi_close_handle_scope`
- **HandleEscape:** Constructor calls `napi_open_escapable_handle_scope`, destructor calls `napi_close_escapable_handle_scope`, `Escape` method calls `napi_escape_handle`

## Summary

C-side management logic is that local objects should be released when leaving the local scope. Therefore, each `napi_value` object (local object) should be limited to the current scope and should be released when leaving the scope. (`napi_value` itself will be destructed, what needs to be managed is the JS-side object)
