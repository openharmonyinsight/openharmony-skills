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

**Problem:** The handle needs to be brought back to the parent scope, and temporary handles inside the function need to be released.

```cpp
// ❌ LEAK
void main() {
    napi_value objValue = nullptr;
    func(env, objValue);
}

void func(napi_env env, napi_value& objValue) {
    HandleScope handleScope(env);  // This may cause incorrect release
    objValue = CreateJsBaseContext(env, objValue);
}

// ✅ FIXED
void main() {
    napi_value objValue = nullptr;
    func(env, objValue);
}

void func(napi_env env, napi_value& objValue) {
    HandleScope handleScope(env);
    objValue = CreateJsBaseContext(env);
    // objValue is now managed by the parent scope
}
```

## Case 7: External Function with EventHandler

**Scenario:** Function is referenced by external function using EventHandler.

**Problem:** Async callbacks need their own `HandleScope` to manage `napi_value` created in the callback.

```cpp
// ❌ LEAK
void ExternalFunction(napi_env env, napi_value callback) {
    std::thread([env, callback]() {
        napi_value result = nullptr;
        napi_create_string_utf8(env, "async result", NAPI_AUTO_LENGTH, &result);
        // result leaks - created in wrong thread without scope
    }).detach();
}

// ✅ FIXED
void ExternalFunction(napi_env env, napi_value callback, std::shared_ptr<AbilityHandler> handler) {
    std::string data = "async result";
    auto task = [env, callback, data]() {
        HandleScope handleScope(env);
        napi_value result = nullptr;
        napi_create_string_utf8(env, data.c_str(), NAPI_AUTO_LENGTH, &result);
        napi_call_function(env, callback, 1, &result, nullptr);
    };
    handler->PostTask(task, "AsyncTask");
}
```

## Key Insights

1. **Return to JS side:** After returning to JS side, no management is needed. JS side calls C++ side with an implicit scope that manages the call (the largest Scope).

2. **Async tasks:** Objects in async tasks need to open corresponding scope for management.

3. **Performance-sensitive call chains:** Add one scope management for the entire chain (identify based on business needs).

4. **Function scope:** C-side management logic is that local objects should be released when leaving the local scope. Each `napi_value` object (local object) should be limited to the current scope.
