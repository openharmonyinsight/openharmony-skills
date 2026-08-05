---
name: ohos-dev-napi-memory-leak-detection
description: Detect and fix OpenHarmony NAPI memory leaks caused by missing HandleScope / HandleEscape scope management or mishandled napi_ref lifecycle. Use when reviewing or writing C/C++ NAPI module code that: (1) returns napi_value, (2) has napi_value& output parameters, (3) calls napi_create_* / napi_new_instance, (4) sets object properties with temporary napi_value variables, (5) runs in async work / async callbacks across threads, or (6) uses napi_wrap / napi_create_reference / napi_delete_reference. Covers HandleScope, HandleEscape, napi_escape_handle, napi_ref strong/weak references, napi_async_work, napi_threadsafe_function, and OpenHarmony Ability Runtime differences. See references/background.md for memory management principles.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: napi
  capability: memory-leak-detection
  version: 0.1.0
  status: draft
  tags:
    - napi
    - memory-leak
    - handlescope
    - napi-ref
    - native-module
---

# NAPI Memory Leak Detection

## Quick Start

Functions working with `napi_value` need scope management to prevent leaks.

**Detection Checklist:**
- [ ] Function returns `napi_value`?
- [ ] Function has `napi_value&` parameter?
- [ ] Function calls `napi_create_*`?
- [ ] Creates temporary `napi_value` variables?
- [ ] Async callback without `HandleScope`?
- [ ] Gets napi_value from other functions?

**For detailed background on JS/C++ memory management, see [references/background.md](references/background.md)**

## Common Patterns

### Pattern 1: Function Returns napi_value

Use `HandleEscape` only when the function opens its own scope and must promote a created handle into the parent scope. A NAPI callback that returns directly to JS is already covered by the caller's implicit top-level scope and does not need `HandleEscape`; the need arises inside long call chains where the ambient scope would reclaim the handle before JS sees it.

```cpp
// ❌ LEAK — function opens its own HandleScope; the returned handle is reclaimed
// when that scope closes, so JS receives a dangling handle.
napi_value Func(napi_env env) {
    HandleScope handleScope(env);
    napi_value result = nullptr;
    napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &result);
    return result;
}

// ✅ FIXED — promote the handle into the parent scope with HandleEscape.
napi_value Func(napi_env env) {
    HandleEscape handleEscape(env);
    napi_value result = nullptr;
    napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &result);
    return handleEscape.Escape(result);
}
```

### Pattern 2: Function with napi_value& Parameter

Use `HandleEscape` when the internally created `napi_value` must survive into the parent scope. A plain `HandleScope` would reclaim the handle on destruction, leaving the output reference dangling.

```cpp
// ❌ LEAK
void Func(napi_env env, napi_value& objValue) {
    napi_value temp = nullptr;
    napi_new_instance(env, cls, 0, nullptr, &temp);
    objValue = temp;
}

// ✅ FIXED
void Func(napi_env env, napi_value& objValue) {
    HandleEscape handleEscape(env);
    napi_value temp = nullptr;
    napi_new_instance(env, cls, 0, nullptr, &temp);
    objValue = handleEscape.Escape(temp);
}
```

### Pattern 3: Property Setting with Temporaries

Temporary `napi_value` variables created during property setting need management.

```cpp
// ❌ LEAK
napi_value CreateInfo(napi_env env, const Data& data) {
    napi_value obj = nullptr;
    napi_create_object(env, &obj);
    
    napi_value name = CreateJsValue(env, data.name);    // Leak
    napi_value pid = CreateJsValue(env, data.pid);      // Leak
    napi_set_named_property(env, obj, "name", name);
    napi_set_named_property(env, obj, "pid", pid);
    
    return obj;
}

// ✅ FIXED
napi_value CreateInfo(napi_env env, const Data& data) {
    HandleEscape handleEscape(env);
    napi_value obj = nullptr;
    napi_create_object(env, &obj);
    
    napi_value name = CreateJsValue(env, data.name);
    napi_value pid = CreateJsValue(env, data.pid);
    napi_set_named_property(env, obj, "name", name);
    napi_set_named_property(env, obj, "pid", pid);
    
    return handleEscape.Escape(obj);
}
```

### Pattern 4: Getting napi_value from Other Functions

When calling functions that return `napi_value`, the returned value needs scope management.

```cpp
// ❌ LEAK
bool Func(napi_env env) {
    auto executorNapiVal = jsObj_->GetNapiValue();
    // executorNapiVal escapes when function returns
}

// ✅ FIXED
bool Func(napi_env env) {
    HandleScope handleScope(env);
    auto executorNapiVal = jsObj_->GetNapiValue();
    // Use executorNapiVal within this scope
}
```

### Pattern 5: Async Callbacks

Plain `napi_env` and `napi_value` are only valid on the JS thread that created them. Crossing an async boundary (a worker thread, a detached `std::thread`, a delayed `PostTask`) requires a `napi_ref` to hold the callback alive and a JS-thread re-entry path (`napi_async_work` / `NapiAsyncTask`, or `napi_threadsafe_function`) to call it. Never capture a raw `napi_env`/`napi_value` into a background thread, and never call ordinary NAPI from a non-JS thread.

```cpp
// ❌ LEAK + undefined behavior
void AsyncBad(napi_env env, napi_value callback) {
    // env and callback are only valid on this JS thread; using them on
    // another thread corrupts the VM state and leaks the created handle.
    std::thread([env, callback]() {
        napi_value result = nullptr;
        napi_create_string_utf8(env, "async result", NAPI_AUTO_LENGTH, &result);
    }).detach();
}

// ✅ FIXED — napi_ref holds the callback; napi_async_work re-enters the JS thread;
// the complete callback releases both the reference and the async_work resource.
struct AsyncContext {
    napi_ref callbackRef = nullptr;
    napi_async_work work = nullptr;
    std::string data;
};

void AsyncGood(napi_env env, napi_value callback) {
    auto* context = new AsyncContext{ .data = "async result" };
    if (napi_create_reference(env, callback, 1, &context->callbackRef) != napi_ok) {
        delete context;
        return;
    }

    napi_value name = nullptr;
    napi_create_string_utf8(env, "AsyncTask", NAPI_AUTO_LENGTH, &name);
    if (napi_create_async_work(env, nullptr, name,
        [](napi_env env, void* data) {
            // Background thread — NO napi calls allowed here.
            auto* ctx = static_cast<AsyncContext*>(data);
            // ...do background work using ctx->data...
        },
        [](napi_env env, napi_status status, void* data) {
            // JS thread — safe to use env and resolve references.
            auto* ctx = static_cast<AsyncContext*>(data);
            HandleScope handleScope(env);
            napi_value cb = nullptr;
            napi_get_reference_value(env, ctx->callbackRef, &cb);
            napi_value result = nullptr;
            napi_create_string_utf8(env, ctx->data.c_str(), NAPI_AUTO_LENGTH, &result);
            napi_value recv = nullptr;
            napi_get_undefined(env, &recv);
            napi_value argv[] = { result };
            napi_call_function(env, recv, cb, 1, argv, nullptr);
            napi_delete_reference(env, ctx->callbackRef);
            napi_delete_async_work(env, ctx->work);
            delete ctx;
        },
        context, &context->work) != napi_ok) {
        napi_delete_reference(env, context->callbackRef);
        delete context;
        return;
    }
    if (napi_queue_async_work(env, context->work) != napi_ok) {
        napi_delete_async_work(env, context->work);
        napi_delete_reference(env, context->callbackRef);
        delete context;
    }
}
```

### Pattern 6: napi_value Used in Conditional Expressions

When `napi_value` is used in conditional checks, it needs scope management.

```cpp
// ❌ LEAK
napi_value Func1(napi_env env) {
    napi_value xxx = nullptr;
    napi_create_double(env, 42.0, &xxx);
    return xxx;
}

bool TestFunc(napi_env env) {
    if (Func1(env) == someValue) {
        // Func1 returns napi_value that leaks
    }
    return true;
}

// ✅ FIXED
napi_value Func1(napi_env env) {
    HandleEscape handleEscape(env);
    napi_value xxx = nullptr;
    napi_create_double(env, 42.0, &xxx);
    return handleEscape.Escape(xxx);
}
```

## Quick Fix Templates

### Template 1: Function Returning napi_value

```cpp
napi_value FunctionName(napi_env env, /* parameters */) {
    HandleEscape handleEscape(env);
    // ... function body ...
    return handleEscape.Escape(result);
}
```

### Template 2: Function with napi_value& Parameter

```cpp
void FunctionName(napi_env env, napi_value& output, /* parameters */) {
    HandleEscape handleEscape(env);
    // ... function body ...
    output = handleEscape.Escape(value);
}
```

### Template 3: Function Creating Multiple Properties

```cpp
napi_value CreateJsObject(napi_env env, const DataType& data) {
    HandleEscape handleEscape(env);
    napi_value obj = nullptr;
    napi_create_object(env, &obj);
    
    napi_value prop1 = CreateJsValue(env, data.field1);
    napi_value prop2 = CreateJsValue(env, data.field2);
    napi_set_named_property(env, obj, "prop1", prop1);
    napi_set_named_property(env, obj, "prop2", prop2);
    
    return handleEscape.Escape(obj);
}
```

## Functions to Review

Functions that commonly create and return `napi_value`. Whether they need scope management depends on the call site: a direct return to JS is managed by the implicit caller scope, while use deep inside a call chain (or inside an explicitly opened scope) needs `HandleScope`/`HandleEscape`:

**Create Functions:**
- `Convert2JSValue`
- `CreateJsAppStateData`, `CreateJsAbilityStateData`, `CreateJsProcessData`
- `CreateJsMissionInfo`, `CreateJsWant`, `CreateJsWantParams`
- `CreateJsError`

**Wrap Functions:**
- `WrapVoidToJS`, `WrapStringToJS`, `WrapInt32ToJS`
- `WrapConfiguration`, `WrapElementName`
- `WrapWant`, `WrapWantAgent`, `WrapWantParams`
- `WrapAbilityResult`

**Custom Functions:**
Any function with `Create` or `Wrap` in the name that returns `napi_value`

## Testing

### ASAN Detection

```bash
export ASAN_OPTIONS=detect_leaks=1
./build.sh --product-name <product> --build-target ability_runtime --ccache
```

### Manual Testing

```cpp
// Call function repeatedly to detect memory growth
for (int i = 0; i < 10000; i++) {
    auto result = FunctionToTest(env);
}
// Monitor memory usage for continuous growth
```

### XTS Memory Leak Detection

**Wiki:** https://wiki.huawei.com/domains/1048/wiki/8/WIKI202511108963910

**Workflow:**
1. Configure device
2. Flash version
3. Sync code and push diff
4. Compile .so files
5. Push .so and replace with symbol version
6. Enable detection switch and restart device
7. Capture logs
8. Extract leak stack traces

## Key Principles

1. **HandleEscape** only when a function opens its own scope and must return a handle to the parent scope (not for direct callback-to-JS returns, which are managed by the implicit caller scope)
2. **HandleScope** when a function consumes `napi_value` internally and all handles may be reclaimed on exit
3. All `napi_create_*` calls create JS objects that need scope management
4. Async callbacks need their own `HandleScope`, and crossing threads requires `napi_ref` plus JS-thread re-entry
5. Temporary `napi_value` variables must be managed
6. `napi_value&` output parameters need `HandleEscape`, not plain `HandleScope`
7. `napi_value` used in expressions needs scope management

## Common napi_create_* Functions

These functions create JS objects and return `napi_value`:

**Primitives:**
- `napi_create_int32`, `napi_create_uint32`, `napi_create_int64`
- `napi_create_double`, `napi_create_bigint_int64`, `napi_create_bigint_uint64`

**Strings:**
- `napi_create_string_utf8`, `napi_create_string_utf16`, `napi_create_string_latin1`

**Objects:**
- `napi_create_object`, `napi_create_array`, `napi_create_array_with_length`

**Functions and Classes:**
- `napi_create_function`, `napi_new_instance`

## Additional Resources

- **Background knowledge:** [references/background.md](references/background.md)
- **Detailed cases:** [references/detailed-cases.md](references/detailed-cases.md)
- **Contact:** Chen Rui (00951372), Deng Wenjun (00850728) for uncertain cases
