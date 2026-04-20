# 测试用例生成模块

> 📖 **相关文档**：
> - [N-API 和 ETS 公共模式](./test_patterns_napi_ets.md) - N-API 封装和 ETS 测试的公共模式定义
> - [N-API 和 ETS 高级模式](./test_patterns_napi_ets_advance.md) - N-API 封装和 ETS 测试的高级模式和特殊场景
> - [工程配置模板指南](./project_config_templates.md) - BUILD.gn、Test.json、syscap.json 配置模板
> - [通用校验模块](./verification_common.md) - 三重 N-API 校验、编译前工程结构校验

## 一、模块概述

L2_Generation 模块负责根据 API 信息和测试策略，生成符合 XTS C 规范的测试用例。

## 二、测试用例生成策略

### 2.1 测试类型

| 类型 | 说明 | 生成规则 |
|------|------|---------|
| PARAM | 参数测试 | 为每个参数生成正常值、边界值、特殊值测试 |
| ERROR | 错误码测试 | 测试所有可能的错误返回值 |
| RETURN | 返回值测试 | 验证返回值的正确性 |
| BOUNDARY | 边界值测试 | 测试数值边界、字符串边界等 |
| MEMORY | 内存管理测试 | 测试内存分配、释放、泄漏 |

### 2.2 参数测试生成

```c
// N-API 封装测试：参数测试生成
// 参数正常值测试
static napi_value HiLogPrint_NormalParamTest(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 参数类型检查
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string");
        return nullptr;
    }

    // 从 napi_value 提取参数值
    char tag[256] = {0};
    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], tag, sizeof(tag) - 1, &strLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get string value");
        return nullptr;
    }

    // 调用原生 C 函数
    const char* fmt = "Test message: %d";
    int value = 42;
    int ret = HiLogPrint(LOG_CORE, LOG_INFO, LOG_DOMAIN, tag, fmt, value);

    // 验证结果
    napi_value result;
    if (ret >= 0) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_throw_error(env, nullptr, "Test failed");
        return nullptr;
    }

    return result;
}
```

### 2.3 错误码测试生成

```c
// N-API 封装测试：错误码测试生成
static napi_value HiLogPrint_ErrorCodeTest(napi_env env, napi_callback_info info)
{
    // 测试空指针参数，预期会返回错误码
    const char* fmt = "Test message";
    int ret = HiLogPrint(LOG_CORE, LOG_INFO, LOG_DOMAIN, nullptr, fmt);
    
    // 在napi层使用napi_throw_error抛出异常，在ets中通过try-catch捕获异常
    if (ret < 0) {
        napi_throw_error(env, "NEGATIVE_RETURN", "Negative return value");
        return nullptr;
    }
    
    // 如果没有错误，返回成功值
    napi_value result;
    napi_create_int32(env, 0, &napiResult);
    return napiResult;
}
```

### 2.4 边界值测试生成

```c
// N-API 封装测试：边界值测试生成
static napi_value HiLogPrint_BoundaryValueTest(napi_env env, napi_callback_info info)
{
    // 测试最大日志级别边界值
    const char* tag = "TEST_TAG";
    const char* fmt = "Test message";
    
    // 调用原生 C 函数测试最大日志级别
    int ret = HiLogPrint(LOG_CORE, LOG_FATAL, LOG_DOMAIN, tag, fmt);
    
    // 测试无效日志级别边界值
    int ret2 = HiLogPrint(LOG_CORE, 999, LOG_DOMAIN, tag, fmt);
    
    // 在napi层使用napi_throw_error抛出异常，在ets中通过try-catch捕获异常
    if (ret >= 0 && ret2 < 0) {
        napi_value result;
        napi_create_int32(env, 0, &napiResult);
        return napiResult;
    } else {
        napi_throw_error(env, "BOUNDARY_ERROR", "Boundary value test failed");
        return nullptr;
    }
}
```

### 2.5 内存管理测试生成

```c
// N-API 封装测试：内存管理测试生成
static napi_value HiLogPrint_MemoryManagementTest(napi_env env, napi_callback_info info)
{
    // 分配内存
    char* tag = (char*)malloc(16);
    if (tag == NULL) {
        napi_throw_error(env, "MEMORY_ERROR", "Memory allocation failed");
        return nullptr;
    }

    // 复制字符串
    strcpy_s(tag, 16, "TEST_TAG");

    // 调用原生 C 函数
    const char* fmt = "Test message";
    int ret = HiLogPrint(LOG_CORE, LOG_INFO, LOG_DOMAIN, tag, fmt);
    
    // 释放内存
    free(tag);

    // 验证结果
    napi_value result;
    if (ret >= 0) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_throw_error(env, nullptr, "Test failed");
        return nullptr;
    }

    return result;
}
```

## 三、测试用例模板

### 3.0 N-API 封装重要说明

> ⚠️ **重要：TypeScript 接口声明**
>
> 在 N-API 封装测试中，需要同时进行三个关键步骤：
>
> 1. **C++ N-API 封装实现**（napi_init.cpp）
>    - 实现封装函数
>    - 在 `Init` 函数中注册到 `napi_property_descriptor` 数组
>
> 2. **TypeScript 接口声明**（types/libentry/Index.d.ts）
>    - 在 Index.d.ts 中导出所有新增的 N-API 函数
>    - 确保函数签名与 C++ 实现一致
>    - 支持正确的参数类型和返回类型
>
> 3. **ETS 测试导入和调用**（.test.ets）
>    - 使用 `import testNapi from 'libentry.so'` 导入
>    - 在测试用例中调用封装后的函数
>
> **三者必须同步**：缺少任一步骤将导致编译错误或运行时错误
>
> #### TypeScript 接口声明示例
> ```typescript
> // types/libentry/Index.d.ts
> export const [函数名]: ([参数类型]) => [返回类型];
> ```
>
> #### 对应关系
> - C++ 中的注册：`{ "[函数名]", nullptr, [函数实现], ... }`
> - TypeScript 中的声明：`export const [函数名]: ...`
> - ETS 中的导入：`import testNapi from 'libentry.so'`
>
> **忘记添加 TypeScript 声明的常见错误**：
> - ❌ TypeScript 编译错误：找不到函数定义
> - ❌ 运行时错误：`undefined is not a function`
> - ❌ ETS 导入错误：模块 'libentry.so' 没有导出该函数
>
> **解决方案**：每添加一个新的 N-API 封装函数，必须同步更新：
> 1. napi_init.cpp 中的 `napi_property_descriptor` 数组
> 2. types/libentry/Index.d.ts 中的 `export const` 声明
>
> **验证方法**：编译后检查生成的 .d.ts 文件是否包含所有新增的函数声明

### 3.1 N-API 封装基础模板

```c
/*
 * N-API 封装测试：基础模板
 * 测试 [API] 的 [测试场景描述]
 */

// 模块定义
static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "[模块名]",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

// 模块注册
extern "C" __attribute__((constructor)) void RegisterEntryModule(void) {
    napi_module_register(&demoModule);
}

// 基础N-API封装函数
static napi_value [API名称]_BasicTest(napi_env env, napi_callback_info info)
{
    // 1. 参数验证和获取
    size_t argc = [参数数量];
    napi_value args[argc];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < [最小参数数量]) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 2. 参数类型检查
    for (size_t i = 0; i < argc; i++) {
        napi_valuetype valuetype;
        status = napi_typeof(env, args[i], &valuetype);
        if (status != napi_ok || valuetype != napi_[参数类型]) {
            napi_throw_error(env, nullptr, "Argument must be [参数类型]");
            return nullptr;
        }
    }

    // 3. 从 napi_value 提取参数值
    char* param = NULL;
    status = napi_get_value_string_utf8(env, args[0], NULL, 0, NULL);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get string length");
        return nullptr;
    }

    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], NULL, 0, &strLen);
    param = (char*)malloc(strLen + 1);
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    status = napi_get_value_string_utf8(env, args[0], param, strLen + 1, NULL);
    if (status != napi_ok) {
        free(param);
        napi_throw_error(env, nullptr, "Failed to get string value");
        return nullptr;
    }

    // 4. 调用原生 C 函数
    [返回类型] result = [API名称](param);
    free(param);

    // 5. 错误处理 - 使用 napi_throw_error 抛出异常
    if (result == [错误码1]) {
        napi_throw_error(env, "[错误码1]", "[错误信息1]");
        return nullptr;
    }
    if (result == [错误码2]) {
        napi_throw_error(env, "[错误码2]", "[错误信息2]");
        return nullptr;
    }

    // 6. 将结果转换为 napi_value
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);

    // 7. 返回结果
    return napiResult;
}

// 模块初始化函数
EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"[函数名]_BasicTest", nullptr, [API名称]_BasicTest, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END
```

### 3.2 N-API 参数测试模板

```c
/*
 * N-API 封装测试：参数测试模板
 * 测试 [API] 的参数 [参数名] 为正常值时的行为
 */

// N-API 封装函数 - 参数正常值测试
static napi_value [API名称]_NormalParamTest(napi_env env, napi_callback_info info)
{
    // 1. 参数验证和获取
    size_t argc = [参数数量];
    napi_value args[argc];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < [最小参数数量]) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 2. 参数类型检查
    for (size_t i = 0; i < argc; i++) {
        napi_valuetype valuetype;
        status = napi_typeof(env, args[i], &valuetype);
        if (status != napi_ok || valuetype != napi_[参数类型]) {
            napi_throw_error(env, nullptr, "Argument must be [参数类型]");
            return nullptr;
        }
    }

    // 3. 从 napi_value 提取参数值
    char* param = NULL;
    status = napi_get_value_string_utf8(env, args[0], NULL, 0, NULL);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get string length");
        return nullptr;
    }

    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], NULL, 0, &strLen);
    param = (char*)malloc(strLen + 1);
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    status = napi_get_value_string_utf8(env, args[0], param, strLen + 1, NULL);
    if (status != napi_ok) {
        free(param);
        napi_throw_error(env, nullptr, "Failed to get string value");
        return nullptr;
    }

    // 4. 调用原生 C 函数
    [返回类型] result = [API名称](param);
    free(param);

    // 5. 验证结果
    napi_value napiResult;
    if (result == [期望返回值]) {
        napi_create_int32(env, 0, &napiResult);
    } else {
        napi_throw_error(env, nullptr, "Test failed");
        return nullptr;
    }

    return napiResult;
}
```

### 3.3 N-API 错误码测试模板

```c
/*
 * N-API 封装测试：错误码测试模板
 * 测试 [API] 在 [错误场景] 时的错误码
 */

// N-API 封装函数 - 错误码测试
static napi_value [API名称]_ErrorCodeTest(napi_env env, napi_callback_info info)
{
    // 准备无效参数
    [参数类型] [参数名] = [无效值];

    // 调用原生 C 函数
    [返回类型] result = [API名称]([参数]);

    // 在napi层使用napi_throw_error抛出异常，在ets中通过try-catch捕获异常
    if (result == [错误码1]) {
        napi_throw_error(env, "[错误码1]", "[错误信息1]");
        return nullptr;
    }
    if (result == [错误码2]) {
        napi_throw_error(env, "[错误码2]", "[错误信息2]");
        return nullptr;
    }
    
    // 如果没有错误，返回成功值
    napi_value napiResult;
    napi_create_int32(env, 0, &napiResult);
    return napiResult;
}
```

### 3.4 N-API 边界值测试模板

```c
/*
 * N-API 封装测试：边界值测试模板
 * 测试 [API] 在边界值 [边界值描述] 时的行为
 */

// N-API 封装函数 - 边界值测试
static napi_value [API名称]_BoundaryTest(napi_env env, napi_callback_info info)
{
    // 准备边界值
    char* param = NULL;
    
    // 调用原生 C 函数测试边界值
    [返回类型] result1 = [API名称]([最小边界值]);
    [返回类型] result2 = [API名称]([最大边界值]);

    // 验证边界值结果
    if (result1 == [期望值1] && result2 == [期望值2]) {
        napi_value napiResult;
        napi_create_int32(env, 0, &napiResult);
        return napiResult;
    } else {
        napi_throw_error(env, "BOUNDARY_ERROR", "Boundary value test failed");
        return nullptr;
    }
}
```

## 四、测试设计文档生成

生成每个测试用例时同步生成测试设计文档，包含用例列表（编号、名称、描述、类型、状态）、用例详情和覆盖率统计（API/参数/错误码覆盖率）。

## 五、代码风格应用

- **5.1 缩进风格**：应用现有测试文件的缩进风格（4 空格）
- **5.2 命名规范**：应用现有测试文件的命名规范
- **5.3 注释风格**：应用现有测试文件的注释风格

## 六、工程配置与校验

> 📋 **BUILD.gn、Test.json、syscap.json、hap 包名对应等工程配置详见**：[工程配置模板指南](./project_config_templates.md)

| 配置项 | 说明 | 详细文档 |
|--------|------|---------|
| BUILD.gn | 测试套目录 + 上层目录两个层级 | [工程配置模板](./project_config_templates.md#buildgn-配置) |
| syscap.json | 系统能力声明及子系统映射 | [工程配置模板](./project_config_templates.md) |
| Test.json | 配置及 hap 包名对应规则 | [工程配置模板](./project_config_templates.md) |
| N-API 模块注册 | 已包含在 3.1 节基础模板中 | 见 3.1 节 |
| 三重 N-API 校验 | N-API 注册 ↔ TS 声明 ↔ ETS 调用一致性 | [通用校验模块](./verification_common.md#一三重napi校验) |
| 编译前配置验证 | 目录结构、配置文件、一致性校验 | [通用校验模块](./verification_common.md#二编译前工程结构校验) |

## 七、生成规则

### 7.1 N-API 参数测试规则

- **强制要求使用 N-API 封装测试**：封装时注意如果 CAPI 返回异常或参数校验异常时，使用 `napi_throw_error` 抛出异常
- **为每个参数生成至少一个正常值测试**：确保参数在正常范围内的行为正确
- **为数值参数生成最小值、最大值测试**：覆盖数值边界
- **为字符串参数生成空字符串、超长字符串测试**：覆盖字符串边界
- **为指针参数生成空指针测试**：覆盖空指针异常

### 7.2 N-API 错误码测试规则

- **在 napi 层使用 `napi_throw_error` 抛出异常**：在 ETS 中通过 try-catch 捕获异常
- **测试所有可能的错误返回值**：确保每个错误码都有对应的测试用例
- **验证错误码触发的条件**：确保错误码触发的逻辑正确
- **在 ETS 中对错误码进行断言**：验证抛出的异常码

#### 7.2.1 Error Code Constants (MANDATORY)

Error codes MUST use named constants, NEVER hardcode numeric values.

**Correct**:
```typescript
// ETS test file
let errCodeParamError = 401;

try {
    testNapi.someFunction(null);
} catch (error) {
    expect(error.code).assertEqual(errCodeParamError);
}
```

```c
// C++ NAPI wrapper
#define ERR_CODE_PARAM_ERROR 401

if (param == nullptr) {
    napi_throw_error(env, std::to_string(ERR_CODE_PARAM_ERROR).c_str(), "Invalid parameter: null pointer");
    return nullptr;
}
```

**Incorrect** (NEVER do this):
```typescript
// ❌ Hardcoded error code
expect(error.code).assertEqual(401);
```

```c
// ❌ Hardcoded error code in napi_throw_error
napi_throw_error(env, "401", "Invalid parameter");
```

#### 7.2.2 Error Code Constant Naming Convention

```
let errCode[Scenario][Type] = [numeric value];
```

| Scenario | Example |
|----------|---------|
| Parameter validation | `errCodeParamError = 401` |
| Permission denied | `errCodePermissionDenied = 201` |

Error code values MUST come from the `.h` header file's error code enums or macros. Do NOT fabricate error code numbers. When the header defines error code macros (e.g., `OH_NATIVE_BUNDLE_ERR_CODE_INVALID_PARAMETER`), prefer using those names as constant names.

### 7.3 N-API 边界值测试规则

- **测试数值的最小值、最大值**：覆盖数值边界
- **测试字符串的空字符串、最大长度**：覆盖字符串边界
- **测试数组的边界索引**：覆盖数组边界
- **在 napi 层对边界值结果进行验证**：正确处理边界条件

### 7.4 N-API 内存管理测试规则

- **确保所有分配的内存都有对应的释放**：避免内存泄漏
- **使用 `malloc` 和 `free` 正确管理内存**：遵循 N-API 内存管理规范
- **测试内存分配失败情况**：处理内存分配异常
- **在 ETS 中通过 try-catch 捕获异常**：验证内存管理异常

### 7.5 返回值覆盖测试规则

- **返回值类型为枚举值时**：要求构造的用例能够覆盖所有枚举值返回
- **返回值为 bool 时**：要求覆盖返回 true/false 两种情况
- **返回值为错误码时**：要求覆盖所有错误码
- **在 ETS 中对返回值进行断言**：验证返回值正确性

## 八、常见问题

**Q1: 如何生成复杂的测试场景？** 将复杂场景拆分为多个简单测试用例，使用多个测试用例覆盖不同方面。

**Q2: 如何处理可变参数函数？** 为可变参数生成多个测试用例，覆盖不同数量和类型的参数。

**Q3: 如何生成 N-API 封装测试？** 使用 N-API 封装函数模板将 CAPI 函数封装为 N-API 接口，在 napi 层使用 `napi_throw_error` 抛出异常，在 ETS 中通过 try-catch 捕获异常，为每种返回值类型生成对应的测试用例。

**Q4: 如何处理 N-API 中的参数类型转换？** 使用 `napi_get_value_string_utf8`/`napi_create_string_utf8` 处理字符串，`napi_get_value_int32`/`napi_create_int32` 处理数值，`napi_get_boolean` 处理布尔类型。

**Q5: 如何确保 N-API 测试的覆盖率？** 测试所有可能的错误码返回，覆盖所有枚举值返回，覆盖 bool 类型的 true/false 返回，使用参数校验异常测试覆盖参数边界，使用内存管理测试覆盖内存分配和释放。

---

**版本**: 1.2.0
**更新日期**: 2026-03-24
