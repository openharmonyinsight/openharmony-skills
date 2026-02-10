# Phase 6: Implementation Guide

## Overview

This phase provides actual implementation code, not just templates. The skill generates complete, working implementations with error handling, test cases, and edge case handling.

## Implementation Workflow

### Step 1: Research Platform APIs

The skill automatically searches for platform-specific API documentation:

**For Android**:
```bash
web_search "Android SharedPreferences API NDK JNI 2025"
```

**For iOS**:
```bash
web_search "iOS NSUserDefaults API Objective-C++ 2025"
```

**Documentation Sources**:
- Android: https://developer.android.com/reference/android/content/SharedPreferences
- iOS: https://developer.apple.com/documentation/foundation/nsuserdefaults

### Step 2: Generate Interface Layer

**File**: `foundation/{module}/interfaces/adapter/include/{module}_adapter.h`

Generate complete, production-ready pure virtual interface with:
- Comprehensive documentation
- Parameter validation requirements
- Error code specifications
- Thread safety considerations

**Example**: See [CODE_EXAMPLES.md](code-examples.md) - Pure Virtual Interface

### Step 3: Generate OHOS Adapter (100% Forwarding)

**File**: `foundation/{module}/services/adapter/{module}_adapter_ohos.cpp`

Generate thin wrapper that delegates all calls to existing OHOS implementation:
- Zero additional logic
- Zero performance impact
- Complete forwarding (1:1 mapping)

**Example**: See [CODE_EXAMPLES.md](code-examples.md) - OHOS Thin Wrapper

### Step 4: Generate Android Adapter

**File**: `plugins/{module}/adapter/android/{module}_adapter_android.cpp`

Generate complete JNI implementation with:
- Thread-safe operations (mutex protection)
- Proper JNI lifecycle management
- Comprehensive error handling
- Memory leak prevention
- Method ID caching for performance

**Example**: See [CODE_EXAMPLES.md](code-examples.md) - Android JNI Adapter

### Step 5: Generate iOS Adapter

**File**: `plugins/{module}/adapter/ios/{module}_adapter_ios.mm`

Generate complete Objective-C++ implementation with:
- Thread-safe operations (mutex protection)
- Objective-C exception handling (@try-@catch)
- Comprehensive error handling
- Memory-safe string conversion
- ARC memory management

**Example**: See [CODE_EXAMPLES.md](code-examples.md) - iOS Objective-C++ Adapter

### Step 6: Generate Build Configuration

**File**: `plugins/{module}/BUILD.gn`

Generate platform-specific build targets with:
- Conditional compilation for Android/iOS
- Proper dependency declarations
- Framework linking for iOS
- NDK integration for Android

**Example**: See [CODE_EXAMPLES.md](code-examples.md) - Build Configuration

### Step 7: Update SDK Configuration

**Files Modified**:
1. `plugins/plugin_lib.gni` - Add module entry
2. `interface/sdk/plugins/api/apiConfig.json` - Add library config
3. `build_plugins/sdk/arkui_cross_sdk_description_std.json` - Add build entries
4. `interface/sdk-js/api/@ohos.{module}.d.ts` - Add @crossplatform annotations

**Automation**: Use `scripts/code_generator.py` to update all 4 files automatically.

### Step 8: Generate Test Code

**File**: `test/{module}/{module}_adapter_test.cpp`

Generate comprehensive unit tests with:
- CRUD operation tests
- Async behavior tests
- Observer pattern tests
- Error handling tests
- Thread safety tests
- Cross-platform consistency tests

**Example**: See [CODE_EXAMPLES.md](code-examples.md) - Unit Tests

## Implementation Checklist

### OHOS Repository Changes

- [ ] Pure virtual interface defined
- [ ] OHOS thin wrapper implemented (100% forwarding)
- [ ] Existing implementation wrapped with adapter macros
- [ ] OHOS compilation successful

### Plugin Repository Changes

- [ ] Android adapter implemented (JNI + platform API)
- [ ] iOS adapter implemented (ObjC++ + platform API)
- [ ] Business logic wrappers created for both platforms
- [ ] Build configuration updated (BUILD.gn)
- [ ] Android/iOS compilation successful

### SDK Configuration Changes

- [ ] `plugin_lib.gni` updated with module entry
- [ ] `apiConfig.json` updated with library paths
- [ ] `arkui_cross_sdk_description_std.json` updated
- [ ] `.d.ts` files annotated with `@crossplatform`

### Testing

- [ ] Unit tests written for all adapters
- [ ] Integration tests pass on Android
- [ ] Integration tests pass on iOS
- [ ] Integration tests pass on OHOS
- [ ] Performance benchmarks acceptable

## Key Implementation Notes

### 1. Error Handling

**Android (JNI)**:
```cpp
// Check for JNI exceptions
if (env->ExceptionCheck()) {
    env->ExceptionDescribe();
    env->ExceptionClear();
    return -1;
}
```

**iOS (Objective-C++)**:
```objc
@try {
    // Operation
} @catch (NSException* exception) {
    NSLog(@"Exception: %@", exception);
    return -1;
}
```

### 2. Thread Safety

```cpp
std::mutex mutex_;

int Put(const std::string& key, const std::string& value) override {
    std::lock_guard<std::mutex> lock(mutex_);
    // Operation
}
```

### 3. Memory Management

**Android (JNI)**:
```cpp
// Clean up local references
env->DeleteLocalRef(jKey);
env->DeleteLocalRef(jValue);

// Clean up global refs in destructor
env->DeleteGlobalRef(prefs_);
```

**iOS**: ARC handles memory automatically

### 4. Performance

**Android**:
- Cache JNI method IDs (expensive lookup done once)
- Minimize JNI calls across boundary

**iOS**:
- Use NSString efficiently
- Avoid unnecessary conversions

## Common Implementation Patterns

### Pattern 1: Platform Selection Macro

```cpp
#ifdef IS_ARKUI_X_TARGET
    #ifdef ANDROID_PLATFORM
        #define ADAPTER() (GetAdapterAndroid())
    #elif defined(IOS_PLATFORM)
        #define ADAPTER() (GetAdapterIOS())
    #endif
#else
    #define ADAPTER() (GetAdapterOHOS())
#endif
```

### Pattern 2: Factory Function

```cpp
extern "C" ACE_FORCE_EXPORT IAdapter* CreateAdapter() {
    #ifdef IS_ARKUI_X_TARGET
        #ifdef ANDROID_PLATFORM
            return GetAdapterAndroid();
        #elif defined(IOS_PLATFORM)
            return GetAdapterIOS();
        #endif
    #else
        return GetAdapterOHOS();
    #endif
}
```

### Pattern 3: Singleton Instance

```cpp
IAdapter* GetAdapterAndroid() {
    static AdapterAndroid instance;
    return &instance;
}
```

## Troubleshooting Implementation

### Issue: JNI Crashes

**Symptoms**: Random crashes or segfaults on Android

**Solutions**:
1. Check JNIEnv attachment status
2. Verify thread attachment for background threads
3. Check for GlobalRef leaks
4. Verify method ID validity
5. Check for exception handling

### Issue: Memory Leaks

**Symptoms**: Memory usage increases over time

**Solutions**:
1. Verify DeleteLocalRef for all JNI local refs
2. Check DeleteGlobalRef in destructor
3. Verify std::unique_ptr usage
4. Check for circular references

### Issue: Build Failures

**Symptoms**: GN build errors on Android/iOS

**Solutions**:
1. Check dependency declarations
2. Verify framework linking (iOS)
3. Check NDK integration (Android)
4. Verify include paths
5. Check for missing symbols

## Best Practices

1. **Start with Interface**: Define pure virtual interface first
2. **Implement OHOS First**: Test forwarding logic on OHOS
3. **Add Android**: Implement JNI adapter with comprehensive testing
4. **Add iOS**: Implement ObjC++ adapter with comprehensive testing
5. **Test Thoroughly**: Unit tests + integration tests on all platforms
6. **Document**: Comment complex JNI/ObjC++ code

## Related Files

- **Phase 5**: [ARCHITECTURE_RECOMMENDATION.md](phase5-architecture-recommendation.md) - Recommended architecture
- **Reference**: [ARCHITECTURE_MODES.md](architecture-modes.md) - Architecture pattern details
- **Reference**: [CODE_EXAMPLES.md](code-examples.md) - Complete code examples
- **Scripts**: `scripts/code_generator.py` - Configuration file generator
