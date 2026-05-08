# OpenHarmony Helper Macros

OpenHarmony provides extensive helper macros for defining properties. These macros are OpenHarmony-specific and NOT available in Node.js N-API.

## Available Macros

### Basic Macros

**DECLARE_NAPI_FUNCTION(name, func)**:
- Define a method
- Example: `DECLARE_NAPI_FUNCTION("methodName", MethodCallback)`

**DECLARE_NAPI_PROPERTY(name, val)**:
- Define a property
- Example: `DECLARE_NAPI_PROPERTY("propertyName", propertyValue)`

**DECLARE_NAPI_STATIC_FUNCTION(name, func)**:
- Define a static method
- Example: `DECLARE_NAPI_STATIC_FUNCTION("staticMethod", StaticMethodCallback)`

### Getter/Setter Macros

**DECLARE_NAPI_GETTER(name, getter)**:
- Define a getter
- Example: `DECLARE_NAPI_GETTER("propertyName", GetterCallback)`

**DECLARE_NAPI_SETTER(name, setter)**:
- Define a setter
- Example: `DECLARE_NAPI_SETTER("propertyName", SetterCallback)`

**DECLARE_NAPI_GETTER_SETTER(name, getter, setter)**:
- Define getter/setter pair
- Example: `DECLARE_NAPI_GETTER_SETTER("propertyName", GetterCallback, SetterCallback)`

### Advanced Macros

**DECLARE_NAPI_DEFAULT_PROPERTY(name, val)**:
- Define property with WEC (Writable, Enumerable, Configurable) attributes
- Example: `DECLARE_NAPI_DEFAULT_PROPERTY("propertyName", propertyValue)`

**DECLARE_NAPI_WRITABLE_FUNCTION(name, func)**:
- Define writable function
- Example: `DECLARE_NAPI_WRITABLE_FUNCTION("methodName", MethodCallback)`

## Comparison with Node.js

**OpenHarmony Approach** (using macros):
```cpp
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        DECLARE_NAPI_FUNCTION("methodName", MethodCallback),
        DECLARE_NAPI_PROPERTY("propertyName", propertyValue),
        DECLARE_NAPI_STATIC_FUNCTION("staticMethod", StaticMethodCallback),
        DECLARE_NAPI_GETTER_SETTER("getterSetter", GetterCallback, SetterCallback),
    };
    
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

**Node.js Approach** (manual descriptor):
```cpp
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"methodName", nullptr, MethodCallback, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"propertyName", nullptr, nullptr, nullptr, nullptr, propertyValue, napi_default, nullptr},
    };
    
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

## Key Benefits

1. **Simplified syntax**: Macros provide cleaner, more readable code
2. **Reduced errors**: Less chance of mistakes in property descriptor construction
3. **OpenHarmony-specific**: Optimized for OpenHarmony's NAPI implementation
4. **Type safety**: Macros help ensure correct parameter types

## Important Notes

- These macros are defined in `interfaces/inner_api/napi/native_common.h`
- They are OpenHarmony-specific extensions to Node.js N-API
- Not available in standard Node.js N-API
- Must include `napi/native_api.h` or `napi/native_node_api.h` to use them