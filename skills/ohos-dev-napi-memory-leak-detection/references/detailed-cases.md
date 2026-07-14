# Detailed Memory Leak Cases

## Case 1: Function Creates napi_value Internally (No Return)

**Scenario:** Function creates `napi_value` but doesn't return it.

**Problem:** Temporary `napi_value` created in function needs `HandleScope` management. Without it, async calls to this function cause memory leaks.

```cpp
// ❌ LEAK
void Func(napi_env env) {
    napi_value temp = nullptr;
    napi_new_instance(env, class2, 0, nullptr, &temp);
    
    napi_value result = nullptr;
    napi_new_instance(env, class1, 0, nullptr, &result);
}

// ✅ FIXED
void Func(napi_env env) {
    HandleScope handleScope(env);
    
    napi_value temp = nullptr;
    napi_new_instance(env, class2, 0, nullptr, &temp);
    
    napi_value result = nullptr;
    napi_new_instance(env, class1, 0, nullptr, &result);
}
```

## Case 2: Function Creates Multiple napi_values with Return

**Scenario:** Function creates multiple `napi_value` and returns one.

**Problem:** Need to use `HandleEscape` to escape the returned value. Other `napi_value` will be released when `handleEscape` destructs. Without it, async calls cause memory leaks.

```cpp
// ❌ LEAK
napi_value Func(napi_env env) {
    napi_value temp = nullptr;
    napi_new_instance(env, class2, 0, nullptr, &temp);
    
    napi_value result = nullptr;
    napi_new_instance(env, class1, 0, nullptr, &result);
    
    return result;
}

// ✅ FIXED
napi_value Func(napi_env env) {
    HandleEscape handleEscape(env);
    
    napi_value temp = nullptr;
    napi_new_instance(env, class2, 0, nullptr, &temp);
    
    napi_value result = nullptr;
    napi_new_instance(env, class1, 0, nullptr, &result);
    
    return handleEscape.Escape(result);
}
```

## Case 3: Getting napi_value from Other Functions

**Scenario:** Function calls another function that returns `napi_value`.

**Problem:** The returned `napi_value` enters this function's scope, so this function needs `HandleScope`. The called function creates a handle pointing to a JS object. If the handle isn't released, the JS object cannot be GC reclaimed.

```cpp
// ❌ LEAK
bool Func(napi_env env) {
    auto executorNapiVal = jsObj_->GetNapiValue();
    // executorNapiVal will leak when function returns
}

// ✅ FIXED
bool Func(napi_env env) {
    HandleScope handleScope(env);
    auto executorNapiVal = jsObj_->GetNapiValue();
    // executorNapiVal is managed by handleScope
}
```

## Case 4: napi_value Used in Conditional Expressions

**Scenario:** Function returns `napi_value` which is used in conditional check.

**Problem:** Once `napi_value` escapes from a child function, the current function scope needs to manage it. Otherwise, async calls cause memory leaks.

```cpp
// ❌ LEAK
napi_value Func1(napi_env env) {
    napi_value xxx = nullptr;
    napi_create_double(env, 42.0, &xxx);
    return xxx;
}

bool TestFunc(napi_env env) {
    napi_value X = nullptr;
    napi_create_double(env, 42.0, &X);
    
    if (Func1(env) == X) {
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

bool TestFunc(napi_env env) {
    HandleScope handleScope(env);
    napi_value X = nullptr;
    napi_create_double(env, 42.0, &X);
    
    if (Func1(env) == X) {
        // All napi_values are managed
    }
    return true;
}
```

## Case 5: Setting Properties with Temporary Variables

**Scenario:** Setting object properties creates temporary `napi_value` variables.

**Problem:** `napiElementName`, `CreateJsValue(env, info.pid)` etc. create temporary variables. `napi_set_named_property` only operates on the target JS object, so temporary handles from `CreateJsValue` should be released. Note: releasing handles doesn't cause JS objects to be reclaimed because JS objects are held by `objValue` during the set operation.

```cpp
// ❌ LEAK
napi_value CreateJsAbilityRunningInfo(napi_env env, const AAFwk::AbilityRunningInfo& info) {
    napi_value objValue = nullptr;
    napi_status createStatus = napi_create_object(env, &objValue);
    if (createStatus != napi_ok || objValue == nullptr) {
        TAG_LOGE(AAFwkTag::ABILITYMGR, "null ObjValue");
        return nullptr;
    }

    napi_value napiElementName = OHOS::AppExecFwk::WrapElementName(env, info.ability);
    napi_set_named_property(env, objValue, "ability", napiElementName);
    napi_set_named_property(env, objValue, "pid", CreateJsValue(env, info.pid));
    napi_set_named_property(env, objValue, "uid", CreateJsValue(env, info.uid));
    napi_set_named_property(env, objValue, "processName", CreateJsValue(env, info.processName));
    napi_set_named_property(env, objValue, "startTime", CreateJsValue(env, info.startTime));
    napi_set_named_property(env, objValue, "abilityState", CreateJsValue(env, info.abilityState));
    
    return objValue;
}

// ✅ FIXED
napi_value CreateJsAbilityRunningInfo(napi_env env, const AAFwk::AbilityRunningInfo& info) {
    HandleEscape handleEscape(env);
    napi_value objValue = nullptr;
    napi_status createStatus = napi_create_object(env, &objValue);
    if (createStatus != napi_ok || objValue == nullptr) {
        TAG_LOGE(AAFwkTag::ABILITYMGR, "null ObjValue");
        return nullptr;
    }

    napi_value napiElementName = OHOS::AppExecFwk::WrapElementName(env, info.ability);
    napi_set_named_property(env, objValue, "ability", napiElementName);
    napi_set_named_property(env, objValue, "pid", CreateJsValue(env, info.pid));
    napi_set_named_property(env, objValue, "uid", CreateJsValue(env, info.uid));
    napi_set_named_property(env, objValue, "processName", CreateJsValue(env, info.processName));
    napi_set_named_property(env, objValue, "startTime", CreateJsValue(env, info.startTime));
    napi_set_named_property(env, objValue, "abilityState", CreateJsValue(env, info.abilityState));
    
    return handleEscape.Escape(objValue);
}
```

## Case 6: napi_value& Reference Parameter

**Scenario:** Function receives `napi_value&` as output parameter.

**Problem:** The handle must survive into the parent scope, so a plain `HandleScope` (which reclaims its handles on destruction) leaves the output reference dangling. Use `HandleEscape` and `Escape()` to promote the handle into the parent scope.

```cpp
// ❌ LEAK
void main() {
    napi_value objValue = nullptr;
    func(env, objValue);
}

void func(napi_env env, napi_value& objValue) {
    napi_value temp = CreateJsBaseContext(env);
    objValue = temp;
}

// ✅ FIXED
void main() {
    napi_value objValue = nullptr;
    func(env, objValue);
    // objValue is now valid: it was escaped into this (parent) scope.
}

void func(napi_env env, napi_value& objValue) {
    HandleEscape handleEscape(env);
    napi_value temp = CreateJsBaseContext(env);
    objValue = handleEscape.Escape(temp);
}
```

## Case 7: External Function with Async Re-entry

**Scenario:** Function must call back into JS after doing work on a non-JS thread.

**Problem:** A raw `napi_env`/`napi_value` is only valid on the JS thread that created it; capturing them into a background thread corrupts VM state and leaks handles. The callback must be held alive with a `napi_ref` and invoked back on the JS thread via `napi_async_work` / `NapiAsyncTask` (or `napi_threadsafe_function`). Note `napi_call_function` takes six arguments: `(env, recv, func, argc, argv, *result)`.

```cpp
// ❌ LEAK + undefined behavior
void ExternalFunction(napi_env env, napi_value callback) {
    std::thread([env, callback]() {
        napi_value result = nullptr;
        napi_create_string_utf8(env, "async result", NAPI_AUTO_LENGTH, &result);
        // result leaks - created in wrong thread without scope
    }).detach();
}

// ✅ FIXED — callback held by napi_ref; re-enter JS thread via napi_async_work;
// release both the reference and the async_work resource on completion.
struct AsyncContext {
    napi_ref callbackRef = nullptr;
    napi_async_work work = nullptr;
    std::string data;
};

void ExternalFunction(napi_env env, napi_value callback) {
    auto* context = new AsyncContext{ .data = "async result" };
    if (napi_create_reference(env, callback, 1, &context->callbackRef) != napi_ok) {
        delete context;
        return;
    }

    napi_value name = nullptr;
    napi_create_string_utf8(env, "AsyncTask", NAPI_AUTO_LENGTH, &name);
    if (napi_create_async_work(env, nullptr, name,
        [](napi_env env, void* data) {
            // Background thread — NO napi calls here.
        },
        [](napi_env env, napi_status status, void* data) {
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

## Key Insights

1. **Return to JS side:** After returning to JS side, no management is needed. JS side calls C++ side with an implicit scope that manages the call (the largest Scope).

2. **Async tasks:** Objects in async tasks need to open corresponding scope for management.

3. **Performance-sensitive call chains:** Add one scope management for the entire chain (identify based on business needs).

4. **Function scope:** C-side management logic is that local objects should be released when leaving the local scope. Each `napi_value` object (local object) should be limited to the current scope.
