# Ability 子系统 CAPI 配置

## 一、子系统基础信息

- **子系统名称**: Ability
- **子系统描述**: Ability 能力框架，提供能力管理和上下文管理
- **API 语言**: C（通过 N-API 封装供 ETS/ArkTS 测试）
- **测试路径**: `test/xts/acts/ability/`

## 二、测试方式说明

### 2.1 测试架构

Ability 子系统使用**方式2（N-API 封装测试）**：

#### 方式2：N-API 封装测试（必需使用）
- 将 C 函数封装为 N-API (napi_value、napi_env) 接口
- 封装函数返回 `napi_value` 类型供 ETS/ArkTS 测试调用
- 适用于：标准系统的跨语言集成测试
- 参考用例：`{OH_ROOT}/test/xts/acts/ability/ability_runtime/abilitycapitest/actscapistartselfuiabilitytest20/`

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
#include "ability_base/want.h"
#include "ability_base/ability_base_common.h"
#include "ability_runtime/context.h"
#include "ability_runtime/ability_runtime_common.h"
#include "ability_runtime/start_options.h"
#include "ability_runtime/application_context.h"
#include "ability_runtime/extension_ability.h"
#include "napi/native_api.h"
```

### 3.2 头文件位置（相对于 {OH_ROOT}/interface/sdk_c）

```
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_base/want.h
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_base/ability_base_common.h
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_runtime/context.h
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_runtime/ability_runtime_common.h
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_runtime/start_options.h
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_runtime/application_context.h
{OH_ROOT}/interface/sdk_c/AbilityKit/ability_runtime/extension_ability.h
```

## 四、API 列表

### 4.1 AbilityBase_Want 模块

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `OH_AbilityBase_CreateWant` | 创建 Want 对象 | AbilityBase_Want* | want.h |
| `OH_AbilityBase_DestroyWant` | 销毁 Want 对象 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_SetWantElement` | 设置 Want 元素 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantElement` | 获取 Want 元素 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_SetWantCharParam` | 设置 char 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantCharParam` | 获取 char 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_AddWantFd` | 添加文件描述符 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantFd` | 获取文件描述符 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_SetWantUri` | 设置 URI | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantUri` | 获取 URI | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_SetWantInt32Param` | 设置 int32 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantInt32Param` | 获取 int32 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_SetWantBoolParam` | 设置 bool 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantBoolParam` | 获取 bool 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_SetWantDoubleParam` | 设置 double 参数 | AbilityBase_ErrorCode | want.h |
| `OH_AbilityBase_GetWantDoubleParam` | 获取 double 参数 | AbilityBase_ErrorCode | want.h |

### 4.2 AbilityRuntime_Context 模块

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `OH_AbilityRuntime_Context_GetCacheDir` | 获取缓存目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetTempDir` | 获取临时目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetFilesDir` | 获取文件目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetDatabaseDir` | 获取数据库目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetPreferencesDir` | 获取首选项目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetBundleCodeDir` | 获取包代码目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetDistributedFilesDir` | 获取分布式文件目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetResourceDir` | 获取资源目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetCloudFileDir` | 获取云文件目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetAreaMode` | 获取区域模式 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_SetAreaMode` | 设置区域模式 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetLogFileDir` | 获取日志文件目录 | AbilityRuntime_ErrorCode | context.h |
| `OH_AbilityRuntime_Context_GetProcessName` | 获取进程名称 | AbilityRuntime_ErrorCode | context.h |

### 4.3 AbilityRuntime_ApplicationContext 模块

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `OH_AbilityRuntime_ApplicationContext_GetCacheDir` | 获取应用缓存目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetAreaMode` | 获取区域模式 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetBundleName` | 获取包名 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetTempDir` | 获取临时目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetFilesDir` | 获取文件目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetDatabaseDir` | 获取数据库目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetPreferencesDir` | 获取首选项目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetBundleCodeDir` | 获取包代码目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetDistributedFilesDir` | 获取分布式文件目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetCloudFileDir` | 获取云文件目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetResourceDir` | 获取资源目录 | AbilityRuntime_ErrorCode | application_context.h |
| `OH_AbilityRuntime_ApplicationContext_GetVersionCode` | 获取版本号 | AbilityRuntime_ErrorCode | application_context.h |

### 4.4 错误码枚举

#### AbilityBase_ErrorCode

| 错误码 | 值 | 说明 | 头文件 |
|--------|------|------|--------|
| `ABILITY_BASE_ERROR_CODE_NO_ERROR` | 0 | 无错误 | ability_base_common.h |
| `ABILITY_BASE_ERROR_CODE_PARAM_INVALID` | 401 | 参数无效 | ability_base_common.h |

#### AbilityRuntime_ErrorCode

| 错误码 | 值 | 说明 | 头文件 |
|--------|------|------|--------|
| `ABILITY_RUNTIME_ERROR_CODE_NO_ERROR` | 0 | 无错误 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_PERMISSION_DENIED` | 201 | 权限拒绝 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_PARAM_INVALID` | 401 | 参数无效 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_NOT_SUPPORTED` | 801 | 不支持 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_NO_SUCH_ABILITY` | 16000001 | 无此能力 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_INCORRECT_ABILITY_TYPE` | 16000002 | 错误的能力类型 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_CROWDTEST_EXPIRED` | 16000008 | 众测过期 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_WUKONG_MODE` | 16000009 | 悟空模式 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_CONTEXT_NOT_EXIST` | 16000011 | 上下文不存在 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_CONTROLLED` | 16000012 | 应用被控制 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_EDM_CONTROLLED` | 16000013 | EDM 控制 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_CROSS_APP` | 16000018 | 跨应用 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_INTERNAL` | 16000050 | 内部错误 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_NOT_TOP_ABILITY` | 16000053 | 非顶层能力 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_VISIBILITY_SETTING_DISABLED` | 16000067 | 可见性设置禁用 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_MULTI_APP_NOT_SUPPORTED` | 16000072 | 多应用不支持 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_INVALID_APP_INSTANCE_KEY` | 16000076 | 无效的应用实例键 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_UPPER_LIMIT_REACHED` | 16000077 | 达到上限 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_MULTI_INSTANCE_NOT_SUPPORTED` | 16000078 | 多实例不支持 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_APP_INSTANCE_KEY_NOT_SUPPORTED` | 16000079 | 应用实例键不支持 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_GET_APPLICATION_INFO_FAILED` | 16000081 | 获取应用信息失败 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_START_TIMEOUT` | 16000133 | 启动超时 | ability_runtime_common.h |
| `ABILITY_RUNTIME_ERROR_CODE_MAIN_THREAD_NOT_SUPPORTED` | 16000134 | 主线程不支持 | ability_runtime_common.h |

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
static napi_value GetCacheDirNoError(napi_env env, napi_callback_info info)
{
    // 1. 获取 context 参数
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 2. 提取 context 指针
    void* contextPtr;
    status = napi_get_value_external(env, args[0], &contextPtr);
    if (status != napi_ok || contextPtr == nullptr) {
        napi_throw_error(env, nullptr, "Failed to get context");
        return nullptr;
    }

    AbilityRuntime_ContextHandle context = static_cast<AbilityRuntime_ContextHandle>(contextPtr);

    // 3. 准备 buffer
    char buffer[PATH_MAX] = {0};
    int32_t writeLength = 0;

    // 4. 调用 C 函数
    AbilityRuntime_ErrorCode ret = OH_AbilityRuntime_Context_GetCacheDir(
        context, buffer, sizeof(buffer), &writeLength);

    // 5. 验证结果并返回
    napi_value result;
    if (ret == ABILITY_RUNTIME_ERROR_CODE_NO_ERROR) {
        napi_create_int32(env, 0, &result);
    } else if (ret == ABILITY_RUNTIME_ERROR_CODE_PARAM_INVALID) {
        napi_create_int32(env, 401, &result);
    } else if (ret == ABILITY_RUNTIME_ERROR_CODE_CONTEXT_NOT_EXIST) {
        napi_create_int32(env, 16000011, &result);
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
        {"getCacheDirNoError", nullptr, GetCacheDirNoError, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"getCacheDirParamInvalid", nullptr, GetCacheDirParamInvalid, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

### 5.3 参数验证模式

```cpp
static napi_value GetCacheDirParamInvalid(napi_env env, napi_callback_info info)
{
    // 测试空 context 参数
    AbilityRuntime_ContextHandle context = nullptr;
    char buffer[PATH_MAX] = {0};
    int32_t writeLength = 0;

    // 调用 C 函数并传入 nullptr
    AbilityRuntime_ErrorCode ret = OH_AbilityRuntime_Context_GetCacheDir(
        context, buffer, sizeof(buffer), &writeLength);

    napi_value result;
    if (ret == ABILITY_RUNTIME_ERROR_CODE_PARAM_INVALID) {
        napi_create_int32(env, 401, &result);
    } else if (ret == ABILITY_RUNTIME_ERROR_CODE_CONTEXT_NOT_EXIST) {
        napi_create_int32(env, 16000011, &result);
    } else {
        napi_create_int32(env, ret, &result);
    }

    return result;
}
```

### 5.4 字符串返回模式

对于返回字符串路径的函数（如 GetCacheDir），需要创建字符串返回值：

```cpp
static napi_value GetCacheDirWithResult(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    void* contextPtr;
    status = napi_get_value_external(env, args[0], &contextPtr);
    AbilityRuntime_ContextHandle context = static_cast<AbilityRuntime_ContextHandle>(contextPtr);

    char buffer[PATH_MAX] = {0};
    int32_t writeLength = 0;

    AbilityRuntime_ErrorCode ret = OH_AbilityRuntime_Context_GetCacheDir(
        context, buffer, sizeof(buffer), &writeLength);

    napi_value result;
    if (ret == ABILITY_RUNTIME_ERROR_CODE_NO_ERROR) {
        // 创建对象返回路径和错误码
        napi_create_object(env, &result);

        napi_value pathValue;
        napi_create_string_utf8(env, buffer, writeLength, &pathValue);
        napi_set_named_property(env, result, "path", pathValue);

        napi_value errorCodeValue;
        napi_create_int32(env, 0, &errorCodeValue);
        napi_set_named_property(env, result, "errorCode", errorCodeValue);
    } else {
        napi_create_int32(env, ret, &result);
    }

    return result;
}
```

## 六、测试用例模板

### 6.1 ETS 测试命名规范

```
格式：SUB_Ability_[模块名]_[API名称]_[测试类型]_[序号]
示例：SUB_Ability_Context_GetCacheDir_PARAM_001
```

### 6.2 N-API 封装函数模板

#### 基础封装函数（目录获取类）

```cpp
/**
 * @tc.name: SUB_Ability_Context_GetCacheDir_0100
 * @tc.desc: 测试 GetCacheDir 正常情况
 * @tc.type: FUNC
 */
static napi_value GetCacheDirNoError(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    void* contextPtr;
    status = napi_get_value_external(env, args[0], &contextPtr);
    if (status != napi_ok || contextPtr == nullptr) {
        napi_throw_error(env, nullptr, "Failed to get context");
        return nullptr;
    }

    AbilityRuntime_ContextHandle context = static_cast<AbilityRuntime_ContextHandle>(contextPtr);

    char buffer[PATH_MAX] = {0};
    int32_t writeLength = 0;

    AbilityRuntime_ErrorCode ret = OH_AbilityRuntime_Context_GetCacheDir(
        context, buffer, sizeof(buffer), &writeLength);

    napi_value result;
    if (ret == ABILITY_RUNTIME_ERROR_CODE_NO_ERROR) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, ret, &result);
    }

    return result;
}
```

#### 错误码测试封装

```cpp
/**
 * @tc.name: SUB_Ability_Context_GetCacheDir_0200
 * @tc.desc: 测试 GetCacheDir 参数无效
 * @tc.type: FUNC
 */
static napi_value GetCacheDirParamInvalid(napi_env env, napi_callback_info info)
{
    // 测试空 context 参数
    AbilityRuntime_ContextHandle context = nullptr;
    char buffer[PATH_MAX] = {0};
    int32_t writeLength = 0;

    AbilityRuntime_ErrorCode ret = OH_AbilityRuntime_Context_GetCacheDir(
        context, buffer, sizeof(buffer), &writeLength);

    napi_value result;
    if (ret == ABILITY_RUNTIME_ERROR_CODE_PARAM_INVALID) {
        napi_create_int32(env, 401, &result);
    } else if (ret == ABILITY_RUNTIME_ERROR_CODE_CONTEXT_NOT_EXIST) {
        napi_create_int32(env, 16000011, &result);
    } else {
        napi_create_int32(env, ret, &result);
    }

    return result;
}
```

### 6.3 ETS 测试用例模板

```typescript
/**
 * @tc.name   SUB_Ability_Context_GetCacheDir_0100
 * @tc.number SUB_Ability_Context_GetCacheDir_0100
 * @tc.desc   测试 GetCacheDir 正常情况
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL1
 */
it('SUB_Ability_Context_GetCacheDir_0100',
  TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: Function) => {
    const LOG_NAME = `SUB_Ability_Context_GetCacheDir_0100`;
    try {
      console.info(`====>${LOG_NAME} start====`);
      let result: number = AbilityKitTest.GetCacheDirNoError(getContext());
      expect(0).assertEqual(result);
      console.info(`====>${LOG_NAME} result: ` + result);
      done();
    } catch (err) {
      console.error(`====>${LOG_NAME} catch err: ` + err);
      expect(false).assertEqual(ABILITY_ERR_OK);
      done();
    }
  })
```

## 七、测试覆盖要求

### 7.1 AbilityBase_Want API 测试

- ✅ 测试 `OH_AbilityBase_CreateWant` 正常情况
- ✅ 测试 `OH_AbilityBase_DestroyWant` 正常情况
- ✅ 测试 `OH_AbilityBase_SetWantElement` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantElement` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_SetWantCharParam` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantCharParam` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_AddWantFd` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantFd` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_SetWantUri` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantUri` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_SetWantInt32Param` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantInt32Param` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_SetWantBoolParam` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantBoolParam` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_SetWantDoubleParam` 正常情况和参数无效
- ✅ 测试 `OH_AbilityBase_GetWantDoubleParam` 正常情况和参数无效

### 7.2 AbilityRuntime_Context API 测试

每个 Context 目录获取函数需要覆盖：

- ✅ 测试正常情况（有效 context）
- ✅ 测试参数无效（nullptr context）
- ✅ 测试上下文不存在（无效的 context）
- ✅ 测试 buffer 为 nullptr
- ✅ 测试 writeLength 为 nullptr
- ✅ 测试 bufferSize 不足

### 7.3 AreaMode API 测试

- ✅ 测试 `OH_AbilityRuntime_Context_GetAreaMode` 正常情况和参数无效
- ✅ 测试 `OH_AbilityRuntime_Context_SetAreaMode` 正常情况和参数无效
- ✅ 覆盖所有 AreaMode 枚举值（EL2, EL3, EL4, EL5）

### 7.4 N-API 封装测试

- ✅ 测试参数验证（类型检查）
- ✅ 测试参数验证（值检查）
- ✅ 测试错误码返回
- ✅ 测试内存管理（字符串释放）
- ✅ 测试复杂对象返回（数组、对象）
- ✅ 测试模块注册

---

**版本**: 1.0.0
**创建日期**: 2026-03-10
**更新日期**: 2026-03-10
**兼容性**: OpenHarmonyOS API 24+
**测试方式**: N-API 封装测试（方式2）
