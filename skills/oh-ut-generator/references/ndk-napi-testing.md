# NDK/NAPI Interface Testing

## Overview

The system has identified through full codebase analysis (recursively 20 levels, covering arkcompiler, base, commonlibrary, foundation, device, drivers, interface/sdk_c directories):

- **7088+ NDK interfaces** (OH_xxx): Including OH_AI_*, OH_AV_*, OH_AUDIO_* and other types of interfaces
- **302+ NAPI functions** (napi_xxx): Including napi_create_*, napi_get_*, napi_call_* and other functions
- **918+ NDK test files**, **773+ NAPI test files** actual usage patterns

## NDK Interface Testing

### Interface Identification

NDK interfaces usually start with `OH_`:

- `OH_AI_ContextCreate`, `OH_AVBuffer_Create`, `OH_Pasteboard_Create`
- `OH_Preferences_Create`, `OH_WIFI_*`, `OH_BLUETOOTH_*`

Interface naming pattern: `OH_[ModuleName]_[OperationName]`

Error codes usually start with `ERR_` or `OH_*_STATUS_*`:

- `ERR_OK`, `ERR_INVALID_PARAMETER`
- `OH_NN_SUCCESS`, `PREFERENCES_OK`

### Resource Lifecycle Management (Critical)

#### Create/Destroy Pairing

All objects created through `OH_xxx_Create()` must call corresponding `OH_xxx_Destroy()`:

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_Create001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    ASSERT_NE(pasteboard, nullptr);

    // Test logic...

    OH_Pasteboard_Destroy(pasteboard);  // Must release
}
```

#### Get/Release Pairing

Resources obtained through `OH_xxx_Get()` must call corresponding `OH_xxx_Release()`:

```cpp
OH_ResourceManager* manager = OH_ResourceManager_Get();
// Use manager...
OH_ResourceManager_Release(manager);  // Must release
```

#### Memory Management for Strings

For interfaces returning strings, must call corresponding free function:

```cpp
HWTEST_F(PreferencesTest, OH_Preferences_GetString001, TestSize.Level1) {
    OH_Preferences* pref = OH_Preferences_Create(option);
    OH_Preferences_SetString(pref, "key", "value");

    char* res = nullptr;
    uint32_t len = 0;
    int ret = OH_Preferences_GetString(pref, "key", &res, &len);
    EXPECT_EQ(ret, PREFERENCES_OK);
    EXPECT_STREQ(res, "value");

    OH_Preferences_FreeString(res);  // Must release
    OH_Preferences_Destroy(pref);
}
```

### Test Case Structure

#### Normal Path Test (FunctionName001)

Test normal interface call flow:

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_SetData001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    OH_UdmfData* data = OH_UdmfData_Create();

    int res = OH_Pasteboard_SetData(pasteboard, data);
    EXPECT_EQ(res, ERR_OK);

    OH_UdmfData_Destroy(data);
    OH_Pasteboard_Destroy(pasteboard);
}
```

#### Exception Path Test (FunctionName002)

Test null pointers, invalid parameters, boundary values:

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_SetData002, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    OH_UdmfData* data = OH_UdmfData_Create();

    // Test null pointer
    int res1 = OH_Pasteboard_SetData(nullptr, data);
    EXPECT_EQ(res1, ERR_INVALID_PARAMETER);

    int res2 = OH_Pasteboard_SetData(pasteboard, nullptr);
    EXPECT_EQ(res2, ERR_INVALID_PARAMETER);

    OH_UdmfData_Destroy(data);
    OH_Pasteboard_Destroy(pasteboard);
}
```

#### Boundary Condition Test (FunctionName003)

Test maximum values, minimum values, zero values, negative numbers:

```cpp
HWTEST_F(PreferencesTest, OH_Preferences_SetInt003, TestSize.Level1) {
    OH_Preferences* pref = OH_Preferences_Create(option);

    // Test boundary values
    EXPECT_EQ(OH_Preferences_SetInt(pref, "max_key", INT_MAX), PREFERENCES_OK);
    EXPECT_EQ(OH_Preferences_SetInt(pref, "min_key", INT_MIN), PREFERENCES_OK);
    EXPECT_EQ(OH_Preferences_SetInt(pref, "zero_key", 0), PREFERENCES_OK);

    OH_Preferences_Destroy(pref);
}
```

### Return Value Verification

Must test all possible return values:

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_Subscribe001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    OH_PasteboardObserver* observer = OH_PasteboardObserver_Create();

    int res = OH_Pasteboard_Subscribe(pasteboard, NOTIFY_LOCAL_DATA_CHANGE, observer);
    EXPECT_EQ(res, ERR_OK);  // Must verify return value

    OH_PasteboardObserver_Destroy(observer);
    OH_Pasteboard_Destroy(pasteboard);
}
```

### Parameter Validation Tests

Must cover all invalid parameter combinations:

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_Subscribe002, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    OH_PasteboardObserver* observer = OH_PasteboardObserver_Create();

    // Test various invalid parameter combinations
    int res1 = OH_Pasteboard_Subscribe(nullptr, NOTIFY_LOCAL_DATA_CHANGE, observer);
    EXPECT_EQ(res1, ERR_INVALID_PARAMETER);

    int res2 = OH_Pasteboard_Subscribe(pasteboard, 10, observer);  // Invalid enum value
    EXPECT_EQ(res2, ERR_INVALID_PARAMETER);

    int res3 = OH_Pasteboard_Subscribe(pasteboard, -1, observer);  // Negative number
    EXPECT_EQ(res3, ERR_INVALID_PARAMETER);

    int res4 = OH_Pasteboard_Subscribe(pasteboard, NOTIFY_LOCAL_DATA_CHANGE, nullptr);
    EXPECT_EQ(res4, ERR_INVALID_PARAMETER);

    OH_PasteboardObserver_Destroy(observer);
    OH_Pasteboard_Destroy(pasteboard);
}
```

### Data Operation Tests (Set/Get Pairing)

```cpp
HWTEST_F(PreferencesTest, OH_Preferences_SetGetInt001, TestSize.Level1) {
    OH_PreferencesOption* option = GetCommonOption();
    OH_Preferences* pref = OH_Preferences_Create(option);

    // Set data
    int setValue = 12345;
    int res1 = OH_Preferences_SetInt(pref, "test_key", setValue);
    EXPECT_EQ(res1, PREFERENCES_OK);

    // Get data and verify
    int getValue = 0;
    int res2 = OH_Preferences_GetInt(pref, "test_key", &getValue);
    EXPECT_EQ(res2, PREFERENCES_OK);
    EXPECT_EQ(getValue, setValue);

    OH_Preferences_Destroy(pref);
    OH_PreferencesOption_Destroy(option);
}
```

### Callback Function Tests

```cpp
void CallbackFunc(void* context, Pasteboard_NotifyType type) {
    // Callback logic
}

HWTEST_F(PasteboardTest, OH_PasteboardObserver_SetData001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    void* context = static_cast<void*>(pasteboard);
    OH_PasteboardObserver* observer = OH_PasteboardObserver_Create();

    int res = OH_PasteboardObserver_SetData(observer, context, CallbackFunc, ContextFinalizeFunc);
    EXPECT_EQ(res, ERR_OK);

    OH_PasteboardObserver_Destroy(observer);
    OH_Pasteboard_Destroy(pasteboard);
}
```

### State Query Tests

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_IsRemoteData001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();

    bool res = OH_Pasteboard_IsRemoteData(pasteboard);
    EXPECT_FALSE(res);  // Verify state

    OH_Pasteboard_Destroy(pasteboard);
}
```

### Subscribe/Unsubscribe Tests

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_SubscribeUnsubscribe001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
    OH_PasteboardObserver* observer = OH_PasteboardObserver_Create();

    // Subscribe
    int res1 = OH_Pasteboard_Subscribe(pasteboard, NOTIFY_LOCAL_DATA_CHANGE, observer);
    EXPECT_EQ(res1, ERR_OK);

    // Repeat subscribe
    int res2 = OH_Pasteboard_Subscribe(pasteboard, NOTIFY_LOCAL_DATA_CHANGE, observer);
    EXPECT_EQ(res2, ERR_OK);

    // Unsubscribe
    int res3 = OH_Pasteboard_Unsubscribe(pasteboard, NOTIFY_LOCAL_DATA_CHANGE, observer);
    EXPECT_EQ(res3, ERR_OK);

    OH_PasteboardObserver_Destroy(observer);
    OH_Pasteboard_Destroy(pasteboard);
}
```

### String and Buffer Management Tests

```cpp
HWTEST_F(PasteboardTest, OH_Pasteboard_GetDataSource001, TestSize.Level1) {
    OH_Pasteboard* pasteboard = OH_Pasteboard_Create();

    int len = 100;
    char source[100];
    int res = OH_Pasteboard_GetDataSource(pasteboard, source, len);
    EXPECT_EQ(res, ERR_OK);

    // Test insufficient buffer size
    int res2 = OH_Pasteboard_GetDataSource(pasteboard, source, 0);
    EXPECT_EQ(res2, ERR_INVALID_PARAMETER);

    OH_Pasteboard_Destroy(pasteboard);
}
```

### Error Code Coverage Tests

```cpp
HWTEST_F(PreferencesTest, OH_Preferences_GetInt002, TestSize.Level1) {
    OH_Preferences* pref = OH_Preferences_Create(option);

    int value = 0;
    // Test non-existent key
    int res = OH_Preferences_GetInt(pref, "nonexistent_key", &value);
    EXPECT_EQ(res, PREFERENCES_ERROR_KEY_NOT_FOUND);

    OH_Preferences_Destroy(pref);
}
```

### BUILD.gN Dependency Requirements

Must add corresponding NDK module dependencies in `external_deps`:

```gn
external_deps = [
    "pasteboard:pasteboard_ndk",
    "preferences:preferences_ndk",
    "hilog:libhilog",
    "googletest:gtest_main"
]
```

## NAPI Function Testing

### NAPI Function Identification

NAPI functions start with `napi_`:

- `napi_create_object`
- `napi_get_value_string_utf8`
- `napi_call_threadsafe_function`

### Must Fully Implement

Each NAPI function test must include complete call logic:

- Create `napi_env` environment (usually provided by test framework)
- Complete function call
- Return value verification
- `napi_value` lifecycle management

### Memory Management

Correctly manage `napi_value` lifecycle, avoid memory leaks.

### Return Value Check

Use `napi_ok` to check return values:

```cpp
napi_status status = napi_create_object(env, &result);
EXPECT_EQ(status, napi_ok);
```

### Async Operations

Test async operations using `napi_async_work` related functions.

### BUILD.gN Dependency

Add `"napi:napi"` dependency:

```gn
external_deps = [
    "napi:napi",
    "hilog:libhilog",
    "googletest:gtest_main"
]
```

## Mock Strategy

### NDK Interfaces

Can Mock underlying implementations (device drivers, system services):

```cpp
auto mockDriver = std::make_shared<MockDeviceDriver>();
EXPECT_CALL(*mockDriver, OH_DeviceOperation()).WillOnce(Return(ERR_OK));
```

### NAPI Functions

Usually test real implementations directly, as they are bridges between JavaScript and Native.

Use `EXPECT_CALL` to verify NDK interface calls.

## Error Handling

### NDK Interfaces

Usually return error codes:

- `OH_AI_STATUS_SUCCESS`
- `OH_API_RC_SUCCESS`

Tests need to cover both normal paths and error paths.

### NAPI Functions

Return `napi_status`:

- `napi_ok`
- `napi_invalid_arg`

Tests need to cover both success and failure cases.

## Forbidden Patterns

### ❌ Empty Implementations

Cannot have only comments, must include complete call logic.

### ❌ Ignoring Resource Release

Cannot only test functionality while ignoring resource cleanup.

### ❌ Only Testing Normal Path

Must test both normal and exception paths.

### ❌ Ignoring Return Value Verification

Must verify return values of all interfaces.

### ❌ Ignoring Parameter Validation

Must test null pointers, invalid parameters, and other boundary cases.
