---
name: memory-leak-detection
description: Detect and fix NAPI memory leaks in OpenHarmony Ability Runtime. Use when reviewing NAPI code for memory leaks, especially functions that: (1) Return napi_value, (2) Have napi_value& parameters, (3) Call napi_create_* functions, (4) Set properties with temporary napi_value variables, (5) Work in async callbacks. See references/background.md for detailed memory management principles.
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

Use `HandleEscape` when returning `napi_value` to parent scope.

```cpp
// ❌ LEAK
napi_value Func(napi_env env) {
    napi_value result = nullptr;
    napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &result);
    return result;
}

// ✅ FIXED
napi_value Func(napi_env env) {
    HandleEscape handleEscape(env);
    napi_value result = nullptr;
    napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &result);
    return handleEscape.Escape(result);
}
```

### Pattern 2: Function with napi_value& Parameter

Use `HandleScope` when receiving `napi_value&` as output parameter.

```cpp
// ❌ LEAK
void Func(napi_env env, napi_value& objValue) {
    napi_value temp = nullptr;
    napi_new_instance(env, cls, 0, nullptr, &temp);
    objValue = temp;
}

// ✅ FIXED
void Func(napi_env env, napi_value& objValue) {
    HandleScope handleScope(env);
    napi_value temp = nullptr;
    napi_new_instance(env, cls, 0, nullptr, &temp);
    objValue = temp;
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

Async tasks need their own `HandleScope` to manage napi_value created in callbacks.

```cpp
// ❌ LEAK
void AsyncBad(napi_env env, napi_value callback) {
    std::thread([env, callback]() {
        napi_value result = nullptr;
        napi_create_string_utf8(env, "async result", NAPI_AUTO_LENGTH, &result);
    }).detach();
}

// ✅ FIXED
void AsyncGood(napi_env env, napi_value callback, std::shared_ptr<AbilityHandler> handler) {
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
    HandleScope handleScope(env);
    // ... function body ...
    output = value;
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

Functions that commonly return `napi_value` and need scope management:

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

1. **HandleEscape** when returning `napi_value` to parent scope
2. `HandleScope` when receiving `napi_value&` as output parameter
3. All `napi_create_*` calls create JS objects that need scope management
4. Async callbacks need their own `HandleScope`
5. Temporary `napi_value` variables must be managed
6. Functions returning `napi_value` need `HandleEscape`
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
