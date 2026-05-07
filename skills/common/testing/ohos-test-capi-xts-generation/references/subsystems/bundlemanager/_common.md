# BundleManager 子系统 CAPI 配置

## 一、子系统基础信息

- **子系统名称**: BundleManager
- **子系统描述**: BundleManager 包管理
- **API 语言**: C（通过 N-API 封装供 ETS/ArkTS 测试）
- **测试路径**: `test/xts/acts/bundlemanager/`

## 二、测试方式说明

### 2.1 测试架构

BundleManager 子系统支持两种测试方式：

#### 方式1：Native C 测试（用于标准系统）
- 使用 gtest/HWTEST_F 测试框架
- 直接测试 C 函数
- 适用于：标准系统的 C 接口测试
- 参考用例：`{OH_ROOT}/test/xts/acts/bundlemanager/zlib/actszlibtest/ActsZlibTest.cpp`

#### 方式2：N-API 封装测试（用于标准系统）
- 将 C 函数封装为 N-API (napi_value、napi_env) 接口
- 封装函数返回 `napi_value` 类型供 ETS/ArkTS 测试调用
- 适用于：标准系统的跨语言集成测试
- 参考用例：`{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest/entry/src/main/cpp/NapiTest.cpp`

### 2.2 N-API 测试特点

- **封装目的**：将 C API 封装为 JS/ArkTS 可调用接口
- **调用方式**：ETS/ArkTS 测试调用封装后的 N-API 函数
- **测试分层**：
  - N-API 封装层（C++）测试 N-API 接口正确性
  - ETS/ArkTS 测试层（.ets）测试业务逻辑
- **优势**：支持跨语言测试，模拟实际使用场景

## 三、头文件路径

### 3.1 主要头文件

```c
#include "bundle/ability_resource_info.h"
#include "bundle/native_interface_bundle.h"
#include "bundle/bundle_manager_common.h"
#include "napi/native_api.h"
```

### 3.2 头文件位置（相对于 {OH_ROOT}/interface/sdk_c）

```
{OH_ROOT}/interface/sdk_c/bundlemanager/bundle_framework/bundle/include/native_interface_bundle.h
{OH_ROOT}/interface/sdk_c/bundlemanager/bundle_framework/bundle/include/ability_resource_info.h
{OH_ROOT}/interface/sdk_c/bundlemanager/bundle_framework/bundle/include/bundle_manager_common.h
```

## 四、API 列表

### 4.1 核心函数

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `OH_NativeBundle_GetCurrentApplicationInfo` | 获取当前应用信息 | OH_NativeBundle_ApplicationInfo* | native_interface_bundle.h |
| `OH_NativeBundle_GetAppId` | 获取应用 ID | char* | native_interface_bundle.h |
| `OH_NativeBundle_GetAppIdentifier` | 获取应用标识符 | char* | native_interface_bundle.h |
| `OH_NativeBundle_GetMainElementName` | 获取主元素名称 | OH_NativeBundle_ElementName* | native_interface_bundle.h |
| `OH_NativeBundle_GetCompatibleDeviceType` | 获取兼容设备类型 | char* | native_interface_bundle.h |
| `OH_NativeBundle_IsDebugMode` | 获取应用调试模式 | bool | native_interface_bundle.h |
| `OH_NativeBundle_GetModuleMetadata` | 获取模块元数据数组 | OH_NativeBundle_ModuleMetadata* | native_interface_bundle.h |
| `OH_NativeBundle_GetAbilityResourceInfo` | 获取支持打开文件格式的应用能力列表 | BundleManager_ErrorCode | native_interface_bundle.h |

### 4.2 AbilityResourceInfo 函数

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `OH_NativeBundle_GetBundleName` | 获取包名称 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_GetModuleName` | 获取模块名称 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_GetAbilityName` | 获取能力名称 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_GetLabel` | 获取标签 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_GetAppIndex` | 获取应用索引 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_CheckDefaultApp` | 检查是否默认应用 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_GetDrawableDescriptor` | 获取可绘制描述符 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_AbilityResourceInfo_Destroy` | 销毁能力资源信息 | BundleManager_ErrorCode | ability_resource_info.h |
| `OH_NativeBundle_GetSize` | 获取能力资源信息大小 | int | ability_resource_info.h |

### 4.3 错误码枚举

| 错误码 | 值 | 说明 | 头文件 |
|--------|------|------|--------|
| `BUNDLE_MANAGER_ERROR_CODE_NO_ERROR` | 0 | 无错误 | bundle_manager_common.h |
| `BUNDLE_MANAGER_ERROR_CODE_PERMISSION_DENIED` | 201 | 权限拒绝 | bundle_manager_common.h |
| `BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID` | 401 | 参数无效 | bundle_manager_common.h |

## 五、N-API 测试规范

### 5.1 N-API 模块定义

```cpp
static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "entry",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterModule(void) {
    napi_module_register(&demoModule);
}
```

### 5.2 N-API 封装函数模式

#### 封装函数返回 napi_value

```cpp
static napi_value GetBundleNameErrorTest(napi_env env, napi_callback_info info)
{
    // 调用 C 函数
    char* bundleName = nullptr;
    BundleManager_ErrorCode ret = OH_NativeBundle_GetBundleName(resourceInfo, &bundleName);
    
    // 封装为 napi_value
    napi_value result;
    if (ret == BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID) {
        napi_create_int32(env, ERRORCODE, &result);
    } else if (ret == BUNDLE_MANAGER_ERROR_CODE_NO_ERROR) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, ret, &result);
    }
    return result;
}
```

#### 属性定义模式

```cpp
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"getBundleNameTest", nullptr, GetBundleNameErrorTest, nullptr, nullptr, napi_default, nullptr},
        {"getModuleNameTest", nullptr, GetModuleNameErrorTest, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

### 5.3 参数验证模式

```cpp
static napi_value GetAbilityResourceInfo(napi_env env, napi_callback_info info)
{
    // 获取参数
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    
    // 验证参数类型
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected fileType string.");
        return nullptr;
    }
    
    // 验证参数值类型
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string");
    }
    
    // 调用 C 函数并返回 napi_value
    OH_NativeBundle_AbilityResourceInfo *modules = nullptr;
    size_t moduleCount = 0;
    BundleManager_ErrorCode ret = OH_NativeBundle_GetAbilityResourceInfo(fileType, &modules, &moduleCount);
    
    napi_value result;
    if (ret == BUNDLE_MANAGER_ERROR_CODE_NO_ERROR) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, ret, &result);
    }
    return result;
}
```

### 5.4 复杂数据返回模式

```cpp
static napi_value ProcessMatchingModule(napi_env env, OH_NativeBundle_AbilityResourceInfo *modules,
                                         size_t moduleCount)
{
    const char *targetBundleName = "com.acts.getabilityresourceinfo";
    size_t nativeBundleSize = OH_NativeBundle_GetSize();
    
    for (size_t i = 0; i < moduleCount; i++) {
        auto module = (OH_NativeBundle_AbilityResourceInfo *)((char *)modules + nativeBundleSize * i);
        char *currentBundleName = nullptr;
        OH_NativeBundle_GetBundleName(module, &currentBundleName);
        
        if (currentBundleName && strcmp(currentBundleName, targetBundleName) == 0) {
            napi_value moduleArray;
            napi_create_array(env, &moduleArray);
            size_t index = 0;
            
            // 添加数值属性
            napi_value sizeValue;
            napi_create_uint32(env, nativeBundleSize, &sizeValue);
            napi_set_element(env, moduleArray, index++, sizeValue);
            
            // 添加字符串属性
            AddStringProperty(env, moduleArray, &index, module, OH_NativeBundle_GetLabel);
            
            free(currentBundleName);
            return moduleArray;
        }
        if (currentBundleName) {
            free(currentBundleName);
        }
    }
    
    napi_throw_error(env, nullptr, "No matching bundle found");
    return nullptr;
}
```

### 5.5 错误处理模式

```cpp
static napi_value GetBundleNameErrorTest(napi_env env, napi_callback_info info)
{
    // 测试成功情况
    OH_NativeBundle_AbilityResourceInfo *modules = nullptr;
    char *bundleName = nullptr;
    BundleManager_ErrorCode ret = OH_NativeBundle_GetBundleName(modules, &bundleName);
    
    napi_value result;
    if (ret == BUNDLE_MANAGER_ERROR_CODE_NO_ERROR) {
        napi_create_int32(env, 0, &result);
    }
    
    return result;
}
```

### 5.6 内存管理模式

```cpp
static napi_value GetMainElementName(napi_env env, napi_callback_info info)
{
    OH_NativeBundle_ElementName elementName = OH_NativeBundle_GetMainElementName();
    
    napi_value result;
    napi_create_object(env, &result);
    
    // 添加字符串属性
    napi_value napi_elementName_bundleName;
    napi_create_string_utf8(env, elementName.bundleName, NAPI_AUTO_LENGTH, &napi_elementName_bundleName);
    napi_set_named_property(env, result, "bundleName", napi_elementName_bundleName);
    
    // 添加模块名称属性
    napi_value napi_elementName_moduleName;
    napi_create_string_utf8(env, elementName.moduleName, NAPI_AUTO_LENGTH, &napi_elementName_moduleName);
    napi_set_named_property(env, result, "moduleName", napi_elementName_moduleName);
    
    // 添加能力名称属性
    napi_value napi_elementName_abilityName;
    napi_create_string_utf8(env, elementName.abilityName, NAPI_AUTO_LENGTH, &napi_elementName_abilityName);
    napi_set_named_property(env, result, "abilityName", napi_elementName_abilityName);
    
    // 释放 C 返回的字符串
    free(elementName.bundleName);
    free(elementName.moduleName);
    free(elementName.abilityName);
    
    return result;
}
```

## 六、测试用例模板

### 6.1 ETS 测试命名规范

```
格式：Sub_Bms_Framework_[API名称]_[测试类型]_[序号]
示例：Sub_Bms_Framework_GetAbilityInfo_0100
```

### 6.2 N-API 封装函数模板

#### 基础封装函数

```cpp
static napi_value GetBundleNameNormalTest(napi_env env, napi_callback_info info)
{
    // 1. 获取 AbilityResourceInfo
    OH_NativeBundle_AbilityResourceInfo* resourceInfo = nullptr;
    size_t moduleCount = 0;
    BundleManager_ErrorCode ret = OH_NativeBundle_GetAbilityResourceInfo("com.example.test", &resourceInfo, &moduleCount);
    
    if (ret != BUNDLE_MANAGER_ERROR_CODE_NO_ERROR || resourceInfo == nullptr || moduleCount == 0) {
        napi_throw_error(env, nullptr, "Failed to get ability resource info");
        return nullptr;
    }
    
    // 2. 获取 BundleName
    char* bundleName = nullptr;
    ret = OH_NativeBundle_GetBundleName(resourceInfo, &bundleName);
    
    // 3. 封装为 napi_value 对象
    napi_value result;
    napi_create_object(env, &result);
    
    napi_value napi_bundleNameValue;
    napi_create_string_utf8(env, bundleName, NAPI_AUTO_LENGTH, &napi_bundleNameValue);
    napi_set_named_property(env, result, "bundleName", napi_bundleNameValue);
    
    // 4. 释放内存
    free(bundleName);
    OH_AbilityResourceInfo_Destroy(resourceInfo, moduleCount);
    
    return result;
}
```

#### 错误码测试封装

```cpp
static napi_value GetBundleNameErrorTest(napi_env env, napi_callback_info info)
{
    OH_NativeBundle_AbilityResourceInfo* resourceInfo = nullptr;
    char* bundleName = nullptr;
    
    // 测试空指针参数
    BundleManager_ErrorCode ret = OH_NativeBundle_GetBundleName(nullptr, &bundleName);
    
    napi_value result;
    if (ret == BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID) {
        napi_create_int32(env, ERRORCODE, &result);
    } else {
        napi_create_int32(env, 0, &result);
    }
    
    return result;
}
```

#### 参数验证封装

```cpp
static napi_value GetAbilityResourceInfoValidationTest(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    
    // 验证参数类型
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get argument type");
        return nullptr;
    }
    
    // 验证参数必须是字符串
    if (valuetype != napi_string && valuetype != napi_null) {
        napi_throw_error(env, nullptr, "Argument must be string or null");
        return nullptr;
    }
    
    // 获取字符串参数
    char fileType[256] = {0};
    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], fileType, sizeof(fileType) - 1, &strLen);
    
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get fileType string");
        return nullptr;
    }
    
    // 调用 C 函数
    OH_NativeBundle_AbilityResourceInfo* modules = nullptr;
    size_t moduleCount = 0;
    BundleManager_ErrorCode ret = OH_NativeBundle_GetAbilityResourceInfo(fileType, &modules, &moduleCount);
    
    napi_value result;
    if (ret == BUNDLE_MANAGER_ERROR_CODE_NO_ERROR) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, ret, &result);
    }
    
    // 释放资源
    if (modules) {
        OH_AbilityResourceInfo_Destroy(modules, moduleCount);
    }
    
    return result;
}
```

## 七、测试覆盖要求

### 7.1 应用信息 API 测试

- ✅ 测试 `OH_NativeBundle_GetCurrentApplicationInfo` 正常情况
- ✅ 测试 `OH_NativeBundle_GetAppId` 正常情况
- ✅ 测试 `OH_NativeBundle_GetAppIdentifier` 正常情况
- ✅ 测试 `OH_NativeBundle_GetMainElementName` 正常情况
- ✅ 测试 `OH_NativeBundle_GetCompatibleDeviceType` 正常情况
- ✅ 测试 `OH_NativeBundle_IsDebugMode` 正常情况和空指针
- ✅ 测试 `OH_NativeBundle_GetModuleMetadata` 正常情况和空指针
- ✅ 测试 `OH_NativeBundle_GetAbilityResourceInfo` 正常情况、权限拒绝、参数无效

### 7.2 AbilityResourceInfo API 测试

- ✅ 测试 `OH_NativeBundle_GetBundleName` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_GetModuleName` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_GetAbilityName` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_GetLabel` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_GetAppIndex` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_CheckDefaultApp` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_GetDrawableDescriptor` 正常情况和参数无效
- ✅ 测试 `OH_NativeBundle_GetSize` 正常情况
- ✅ 测试 `OH_AbilityResourceInfo_Destroy` 正常情况和空指针

### 7.3 N-API 封装测试

- ✅ 测试参数验证（类型检查）
- ✅ 测试参数验证（值检查）
- ✅ 测试错误码返回
- ✅ 测试内存管理（字符串释放）
- ✅ 测试复杂对象返回（数组、对象）
- ✅ 测试模块注册

---

**版本**: 1.0.0
**更新日期**: 2026-03-10
**基于测试用例**: NapiTest.cpp (N-API 封装）
