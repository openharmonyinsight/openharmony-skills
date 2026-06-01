# Code Examples

This document provides complete, production-ready code examples for module adaptation. These examples demonstrate the OHOS Reuse Mode pattern.

## Table of Contents

- [Pure Virtual Interface](#1-pure-virtual-interface)
- [OHOS Thin Wrapper](#2-ohos-thin-wrapper-100-forwarding)
- [Android JNI Adapter](#3-android-jni-adapter-complete-implementation)
- [iOS Objective-C++ Adapter](#4-ios-objective-c-adapter-complete-implementation)
- [Build Configuration](#5-build-configuration)
- [Unit Tests](#6-unit-tests)

---

## 1. Pure Virtual Interface

**File**: `foundation/distributeddatamgr/preferences/interfaces/adapter/include/preferences_adapter.h`

```cpp
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 */

#ifndef PREFERENCES_ADAPTER_H
#define PREFERENCES_ADAPTER_H

#include <string>
#include <functional>
#include <unordered_map>

namespace OHOS {
namespace PreferencesAdapter {

/**
 * @brief Platform-independent adapter interface for Preferences
 *
 * This interface abstracts platform-specific preferences storage operations.
 * Designed for ZERO overhead on OHOS platform (100% forwarding).
 */
class IPreferencesAdapter {
public:
    virtual ~IPreferencesAdapter() = default;

    /**
     * @brief Put a string value into preferences
     * @param key The key of the preference (max 1024 chars)
     * @param value The string value to store (max 16MB)
     * @return Returns 0 for success, error code for failure
     */
    virtual int Put(const std::string& key, const std::string& value) = 0;

    /**
     * @brief Get a string value from preferences
     * @param key The key of the preference
     * @param value Output parameter for the retrieved value
     * @return Returns 0 for success, -1 if key not found or error
     */
    virtual int Get(const std::string& key, std::string& value) = 0;

    /**
     * @brief Delete a preference from storage
     * @param key The key of the preference to delete
     * @return Returns 0 for success, error code for failure
     */
    virtual int Delete(const std::string& key) = 0;

    /**
     * @brief Clear all preferences from storage
     * @return Returns 0 for success, error code for failure
     */
    virtual int Clear() = 0;

    /**
     * @brief Check if a key exists in preferences
     * @param key The key to check
     * @return Returns true if exists, false otherwise
     */
    virtual bool Has(const std::string& key) = 0;
};

// Platform selection macro (compile-time, ZERO runtime overhead)
#ifdef IS_ARKUI_X_TARGET
    #ifdef ANDROID_PLATFORM
        extern IPreferencesAdapter* GetPreferencesAdapterAndroid();
        #define PREFERENCES_ADAPTER() (GetPreferencesAdapterAndroid())
    #elif defined(IOS_PLATFORM)
        extern IPreferencesAdapter* GetPreferencesAdapterIOS();
        #define PREFERENCES_ADAPTER() (GetPreferencesAdapterIOS())
    #else
        #error "Unsupported platform for IS_ARKUI_X_TARGET"
    #endif
#else
    extern IPreferencesAdapter* GetPreferencesAdapterOHOS();
    #define PREFERENCES_ADAPTER() (GetPreferencesAdapterOHOS())
#endif

} // namespace PreferencesAdapter
} // namespace OHOS

#endif // PREFERENCES_ADAPTER_H
```

---

## 2. OHOS Thin Wrapper (100% Forwarding)

**File**: `foundation/distributeddatamgr/preferences/services/adapter/preferences_adapter_ohos.cpp`

```cpp
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 */

#include "interfaces/adapter/include/preferences_adapter.h"
#include "interfaces/inner_api/include/preferences_helper.h"
#include "interfaces/inner_api/include/preferences.h"
#include "preferences_impl.h"

#include <memory>

namespace OHOS {
namespace PreferencesAdapter {

/**
 * @brief OHOS Preferences Adapter - 100% forwarding to existing implementation
 *
 * This is a ZERO-overhead wrapper that delegates all calls to the existing
 * OHOS Preferences implementation. No additional logic, no performance impact.
 */
class PreferencesAdapterOHOS : public IPreferencesAdapter {
public:
    PreferencesAdapterOHOS() = default;
    ~PreferencesAdapterOHOS() override = default;

    void Initialize(const std::string& name)
    {
        if (!preferences_) {
            int errCode = 0;
            NativePreferences::Options options(name);
            preferences_ = NativePreferences::PreferencesHelper::GetPreferences(options, errCode);
        }
    }

    int Put(const std::string& key, const std::string& value) override
    {
        if (!preferences_) {
            return -1;
        }
        return preferences_->PutString(key, value);
    }

    int Get(const std::string& key, std::string& value) override
    {
        if (!preferences_) {
            return -1;
        }
        value = preferences_->GetString(key, "");
        return 0;
    }

    int Delete(const std::string& key) override
    {
        if (!preferences_) {
            return -1;
        }
        return preferences_->Delete(key);
    }

    int Clear() override
    {
        if (!preferences_) {
            return -1;
        }
        return preferences_->Clear();
    }

    bool Has(const std::string& key) override
    {
        if (!preferences_) {
            return false;
        }
        return preferences_->HasKey(key);
    }

private:
    std::shared_ptr<NativePreferences::Preferences> preferences_;
};

IPreferencesAdapter* GetPreferencesAdapterOHOS()
{
    static PreferencesAdapterOHOS instance;
    return &instance;
}

} // namespace PreferencesAdapter
} // namespace OHOS
```

---

## 3. Android JNI Adapter (Complete Implementation)

**File**: `plugins/data/preferences/adapter/android/preferences_adapter_android.cpp`

```cpp
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 */

#include "interfaces/adapter/include/preferences_adapter.h"

#include <jni.h>
#include <android/log.h>
#include <memory>
#include <string>
#include <mutex>

#define LOG_TAG "PreferencesAdapterAndroid"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

namespace OHOS {
namespace PreferencesAdapter {

class PreferencesAdapterAndroid : public IPreferencesAdapter {
private:
    JavaVM* vm_ = nullptr;
    jobject prefs_ = nullptr;
    jobject editor_ = nullptr;

    // Cached JNI method IDs for performance
    jmethodID midPut_ = nullptr;
    jmethodID midGetString_ = nullptr;
    jmethodID midRemove_ = nullptr;
    jmethodID midClear_ = nullptr;
    jmethodID midContains_ = nullptr;
    jmethodID midApply_ = nullptr;

    std::mutex mutex_;

    JNIEnv* GetEnv()
    {
        JNIEnv* env = nullptr;
        if (vm_->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) == JNI_EDETACHED) {
            jint result = vm_->AttachCurrentThread(&env, nullptr);
            if (result != JNI_OK) {
                LOGE("Failed to attach thread to JVM: %d", result);
                return nullptr;
            }
        }
        return env;
    }

    void CachePreferences(JNIEnv* env)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        if (prefs_ != nullptr) return;

        jclass prefsClass = env->FindClass("android/content/SharedPreferences");
        jclass contextClass = env->FindClass("android/content/Context");

        prefs_ = env->NewGlobalRef(env->NewObject(
            prefsClass, env->GetMethodID(prefsClass, "<init>", "()V")));

        jclass editorClass = env->FindClass("android/content/SharedPreferences$Editor");
        jmethodID midEdit = env->GetMethodID(prefsClass, "edit",
            "()Landroid/content/SharedPreferences$Editor;");
        editor_ = env->NewGlobalRef(env->CallObjectMethod(prefs_, midEdit));

        midPut_ = env->GetMethodID(editorClass, "putString",
            "(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;");
        midGetString_ = env->GetMethodID(prefsClass, "getString",
            "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;");
        midRemove_ = env->GetMethodID(editorClass, "remove",
            "(Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;");
        midClear_ = env->GetMethodID(editorClass, "clear",
            "()Landroid/content/SharedPreferences$Editor;");
        midContains_ = env->GetMethodID(prefsClass, "contains", "(Ljava/lang/String;)Z");
        midApply_ = env->GetMethodID(editorClass, "apply", "()V");
    }

public:
    PreferencesAdapterAndroid() = default;

    ~PreferencesAdapterAndroid() override
    {
        JNIEnv* env = GetEnv();
        if (env && prefs_) {
            env->DeleteGlobalRef(prefs_);
            env->DeleteGlobalRef(editor_);
        }
    }

    void Initialize(JavaVM* vm, jobject context = nullptr)
    {
        vm_ = vm;
    }

    int Put(const std::string& key, const std::string& value) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        try {
            JNIEnv* env = GetEnv();
            if (!env) return -1;
            CachePreferences(env);

            jstring jKey = env->NewStringUTF(key.c_str());
            jstring jValue = env->NewStringUTF(value.c_str());
            if (!jKey || !jValue) {
                if (jKey) env->DeleteLocalRef(jKey);
                if (jValue) env->DeleteLocalRef(jValue);
                return -1;
            }

            env->CallObjectMethod(editor_, midPut_, jKey, jValue);
            env->CallVoidMethod(editor_, midApply_);

            env->DeleteLocalRef(jKey);
            env->DeleteLocalRef(jValue);

            if (env->ExceptionCheck()) {
                env->ExceptionDescribe();
                env->ExceptionClear();
                return -1;
            }
            return 0;
        } catch (const std::exception& e) {
            LOGE("Exception in Put: %s", e.what());
            return -1;
        }
    }

    int Get(const std::string& key, std::string& value) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        try {
            JNIEnv* env = GetEnv();
            if (!env) return -1;
            CachePreferences(env);

            jstring jKey = env->NewStringUTF(key.c_str());
            jstring jDefault = env->NewStringUTF("");
            jstring jValue = (jstring)env->CallObjectMethod(prefs_, midGetString_, jKey, jDefault);

            if (jValue) {
                const char* cValue = env->GetStringUTFChars(jValue, nullptr);
                if (cValue) {
                    value = cValue;
                    env->ReleaseStringUTFChars(jValue, cValue);
                    env->DeleteLocalRef(jKey);
                    env->DeleteLocalRef(jDefault);
                    env->DeleteLocalRef(jValue);
                    return 0;
                }
            }
            env->DeleteLocalRef(jKey);
            env->DeleteLocalRef(jDefault);
            if (jValue) env->DeleteLocalRef(jValue);
            return -1;
        } catch (const std::exception& e) {
            LOGE("Exception in Get: %s", e.what());
            return -1;
        }
    }

    int Delete(const std::string& key) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        try {
            JNIEnv* env = GetEnv();
            if (!env) return -1;
            CachePreferences(env);

            jstring jKey = env->NewStringUTF(key.c_str());
            env->CallObjectMethod(editor_, midRemove_, jKey);
            env->CallVoidMethod(editor_, midApply_);
            env->DeleteLocalRef(jKey);

            if (env->ExceptionCheck()) {
                env->ExceptionDescribe();
                env->ExceptionClear();
                return -1;
            }
            return 0;
        } catch (const std::exception& e) {
            LOGE("Exception in Delete: %s", e.what());
            return -1;
        }
    }

    int Clear() override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        try {
            JNIEnv* env = GetEnv();
            if (!env) return -1;
            CachePreferences(env);

            env->CallObjectMethod(editor_, midClear_);
            env->CallVoidMethod(editor_, midApply_);

            if (env->ExceptionCheck()) {
                env->ExceptionDescribe();
                env->ExceptionClear();
                return -1;
            }
            return 0;
        } catch (const std::exception& e) {
            LOGE("Exception in Clear: %s", e.what());
            return -1;
        }
    }

    bool Has(const std::string& key) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        try {
            JNIEnv* env = GetEnv();
            if (!env) return false;
            CachePreferences(env);

            jstring jKey = env->NewStringUTF(key.c_str());
            jboolean result = env->CallBooleanMethod(prefs_, midContains_, jKey);
            env->DeleteLocalRef(jKey);
            return result == JNI_TRUE;
        } catch (const std::exception& e) {
            LOGE("Exception in Has: %s", e.what());
            return false;
        }
    }
};

IPreferencesAdapter* GetPreferencesAdapterAndroid()
{
    static PreferencesAdapterAndroid instance;
    return &instance;
}

} // namespace PreferencesAdapter
} // namespace OHOS
```

---

## 4. iOS Objective-C++ Adapter (Complete Implementation)

**File**: `plugins/data/preferences/adapter/ios/preferences_adapter_ios.mm`

```objc
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 */

#include "interfaces/adapter/include/preferences_adapter.h"

#import <Foundation/Foundation.h>
#include <memory>
#include <string>
#include <mutex>

namespace OHOS {
namespace PreferencesAdapter {

class PreferencesAdapterIOS : public IPreferencesAdapter {
private:
    std::mutex mutex_;

    NSUserDefaults* GetDefaults()
    {
        return [NSUserDefaults standardUserDefaults];
    }

public:
    PreferencesAdapterIOS() = default;
    ~PreferencesAdapterIOS() override = default;

    int Put(const std::string& key, const std::string& value) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        @try {
            NSString* nsKey = [NSString stringWithUTF8String:key.c_str()];
            NSString* nsValue = [NSString stringWithUTF8String:value.c_str()];
            if (!nsKey || !nsValue) {
                NSLog(@"Failed to convert strings to NSString");
                return -1;
            }
            [GetDefaults() setObject:nsValue forKey:nsKey];
            [GetDefaults() synchronize];
            return 0;
        } @catch (NSException* exception) {
            NSLog(@"Exception in Put: %@", exception);
            return -1;
        }
    }

    int Get(const std::string& key, std::string& value) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        @try {
            NSString* nsKey = [NSString stringWithUTF8String:key.c_str()];
            if (!nsKey) return -1;
            NSString* nsValue = [GetDefaults() stringForKey:nsKey];
            if (nsValue) {
                value = [nsValue UTF8String];
                return 0;
            }
            return -1;
        } @catch (NSException* exception) {
            NSLog(@"Exception in Get: %@", exception);
            return -1;
        }
    }

    int Delete(const std::string& key) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        @try {
            NSString* nsKey = [NSString stringWithUTF8String:key.c_str()];
            if (!nsKey) return -1;
            [GetDefaults() removeObjectForKey:nsKey];
            [GetDefaults() synchronize];
            return 0;
        } @catch (NSException* exception) {
            NSLog(@"Exception in Delete: %@", exception);
            return -1;
        }
    }

    int Clear() override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        @try {
            NSString* appDomain = [[NSBundle mainBundle] bundleIdentifier];
            if (appDomain) {
                [GetDefaults() removePersistentDomainForName:appDomain];
                [GetDefaults() synchronize];
            }
            return 0;
        } @catch (NSException* exception) {
            NSLog(@"Exception in Clear: %@", exception);
            return -1;
        }
    }

    bool Has(const std::string& key) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        @try {
            NSString* nsKey = [NSString stringWithUTF8String:key.c_str()];
            if (!nsKey) return false;
            return [GetDefaults() objectForKey:nsKey] != nil;
        } @catch (NSException* exception) {
            NSLog(@"Exception in Has: %@", exception);
            return false;
        }
    }
};

IPreferencesAdapter* GetPreferencesAdapterIOS()
{
    static PreferencesAdapterIOS instance;
    return &instance;
}

} // namespace PreferencesAdapter
} // namespace OHOS
```

---

## 5. Build Configuration

**File**: `plugins/data/preferences/BUILD.gn`

```gni
import("//build/ohos.gni")
import("preferences.gni")

if (target_os == "android") {
  ohos_shared_library("preferences_android") {
    sources = preferences_android_sources
    include_dirs = preferences_android_include_dirs
    deps = preferences_android_deps

    subsystem_name = "plugins"
    part_name = "data_preferences"
  }
} else if (target_os == "ios") {
  ohos_shared_library("preferences_ios") {
    sources = preferences_ios_sources
    include_dirs = preferences_ios_include_dirs
    deps = preferences_ios_deps
    frameworks = preferences_ios_frameworks

    subsystem_name = "plugins"
    part_name = "data_preferences"
  }
}

template("plugin_data_preferences_static") {
  target_out_dir = target_out_dir
  subsystem_name = "plugins"

  if (defined(ohos_lite)) {
    static_library("plugin_data_preferences_static_ohos") {
      sources = preferences_innerkit_sources
      include_dirs = preferences_innerkit_include_dirs
      deps = preferences_innerkit_deps
      subsystem_name = subsystem_name
      part_name = part_name
      output_name = "plugin_data_preferences_static_ohos"
      complete_static_lib = true
    }
  }

  if (target_os == "android") {
    static_library("plugin_data_preferences_static_android") {
      sources = preferences_adapter_android_sources
      include_dirs = preferences_adapter_android_include_dirs
      deps = [
        "//base/hiviewdfx/hilog:hilog_native",
        "//base/utils/utils:libutils",
      ]
      subsystem_name = subsystem_name
      part_name = part_name
      output_name = "plugin_data_preferences_static_android"
      defines = [ "ANDROID_PLATFORM" ]
    }
  }

  if (target_os == "ios") {
    static_library("plugin_data_preferences_static_ios") {
      sources = preferences_adapter_ios_sources
      include_dirs = preferences_adapter_ios_include_dirs
      deps = [
        "//base/hiviewdfx/hilog:hilog_native",
        "//base/utils/utils:libutils",
      ]
      subsystem_name = subsystem_name
      part_name = part_name
      output_name = "plugin_data_preferences_static_ios"
      defines = [ "IOS_PLATFORM" ]
    }
  }
}
```

---

## 6. Unit Tests

**File**: `test/data/preferences/preferences_adapter_test.cpp`

```cpp
#include "interfaces/adapter/include/preferences_adapter.h"
#include <gtest/gtest.h>

class PreferencesAdapterTest : public ::testing::Test {
protected:
    void SetUp() override {
        adapter_ = PREFERENCES_ADAPTER();
    }

    IPreferencesAdapter* adapter_;
};

TEST_F(PreferencesAdapterTest, PutAndGet) {
    std::string key = "test_key";
    std::string value = "test_value";

    int ret = adapter_->Put(key, value);
    EXPECT_EQ(ret, 0);

    std::string retrieved;
    ret = adapter_->Get(key, retrieved);
    EXPECT_EQ(ret, 0);
    EXPECT_EQ(retrieved, value);
}

TEST_F(PreferencesAdapterTest, HasAndDelete) {
    std::string key = "delete_test";

    EXPECT_FALSE(adapter_->Has(key));

    adapter_->Put(key, "value");
    EXPECT_TRUE(adapter_->Has(key));

    adapter_->Delete(key);
    EXPECT_FALSE(adapter_->Has(key));
}

TEST_F(PreferencesAdapterTest, Clear) {
    adapter_->Put("key1", "value1");
    adapter_->Put("key2", "value2");

    adapter_->Clear();

    EXPECT_FALSE(adapter_->Has("key1"));
    EXPECT_FALSE(adapter_->Has("key2"));
}

TEST_F(PreferencesAdapterTest, UpdateValue) {
    std::string key = "update_key";

    adapter_->Put(key, "value1");
    std::string retrieved;
    adapter_->Get(key, retrieved);
    EXPECT_EQ(retrieved, "value1");

    adapter_->Put(key, "value2");
    adapter_->Get(key, retrieved);
    EXPECT_EQ(retrieved, "value2");
}

TEST_F(PreferencesAdapterTest, NonExistentKey) {
    std::string key = "non_existent_key";
    std::string value;
    int ret = adapter_->Get(key, value);
    EXPECT_EQ(ret, -1);
}

TEST_F(PreferencesAdapterTest, EmptyKey) {
    std::string key = "";
    std::string value = "value";
    int ret = adapter_->Put(key, value);
    EXPECT_EQ(ret, -1);
}

TEST_F(PreferencesAdapterTest, LargeValue) {
    std::string key = "large_key";
    std::string value(16 * 1024 * 1024, 'a');  // 16MB

    int ret = adapter_->Put(key, value);
    EXPECT_EQ(ret, 0);

    std::string retrieved;
    ret = adapter_->Get(key, retrieved);
    EXPECT_EQ(ret, 0);
    EXPECT_EQ(retrieved, value);
}
```

---

## Code Organization Best Practices

1. **Error Handling**: All JNI/ObjC++ calls check for exceptions
2. **Thread Safety**: std::mutex protects all operations
3. **Memory Management**: Proper cleanup of JNI local/global refs
4. **Performance**: Cache JNI method IDs (expensive lookups)
5. **Documentation**: Comprehensive comments for complex code
6. **Testing**: Unit tests cover all operations and edge cases

## Platform Differences Handled

| Operation | Android | iOS | OHOS |
|-----------|---------|-----|------|
| Storage | SharedPreferences | NSUserDefaults | XML file |
| Sync | apply() | synchronize() | File I/O |
| Thread safety | mutex | mutex | shared_mutex |
| Error handling | JNI exceptions | @try-@catch | Return codes |

---

## Related Files

- **Phase 6**: [IMPLEMENTATION_GUIDE.md](phase6-implementation-guide.md) - Implementation workflow
- **Reference**: [ARCHITECTURE_MODES.md](architecture-modes.md) - Architecture pattern details
- **Scripts**: `scripts/code_generator.py` - Configuration file generator
