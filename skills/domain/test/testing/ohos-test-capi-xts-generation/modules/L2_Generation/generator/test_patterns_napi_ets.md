# N-API 封装和 ETS 测试公共模式

> **文档目的**：定义 N-API 封装和 ETS/ArkTS 测试的公共模式，供 L2_Generation 模块引用

## 模式概述

本文档定义了 N-API 封装测试和 ETS/ArkTS 测试的公共模式。每个模式包含两部分：
1. **N-API 封装模板**：C++ 层的 N-API 封装函数实现
2. **ETS/ArkTS 测试模板**：ETS 层的测试用例实现

**重要原则**：
- **返回值覆盖**：构造用例覆盖所有可能的返回值（枚举值、bool 值、错误码）
- **错误处理一致性**：N-API 层使用 `napi_throw_error` 抛出异常，ETS 层通过 try-catch 捕获并断言
- **参数校验**：在 N-API 层进行参数类型检查，ETS 层传递测试数据

---

## 模式 1：正常情况测试模式

**测试场景**：测试 API 在正常输入情况下的行为

### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 正常情况测试
 * 测试 [API] 的正常场景
 */
static napi_value [API名称]_NormalTest(napi_env env, napi_callback_info info)
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
    [参数类型提取代码]

    // 4. 调用原生 C 函数
    [返回类型] result = [API名称]([参数]);

    // 5. 错误处理 - 使用 napi_throw_error 抛出异常
    if (result == [错误码]) {
        napi_throw_error(env, "[错误码]", "[错误信息]");
        return nullptr;
    }

    // 6. 将结果转换为 napi_value
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);

    // 7. 返回结果
    return napiResult;
}
```

### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with [测试场景] - 正常情况
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let result = testNapi.[函数名]_NormalTest([测试参数]);
      hilog.info(DOMAIN, 'testTag', `Test success, result is ${JSON.stringify(result)}`);
      expect(result).assertEqual(期望值);
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Test errCode:${code} message:${errMsg}`);
      expect.fail(`Test should not throw error but got: ${errMsg}`);
      done();
    }
  })
```

---

## 模式 2：错误码测试模式

**测试场景**：测试 API 返回错误码时的异常处理

### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 错误码测试
 * 测试 [API] 返回错误码时的处理
 */
static napi_value [API名称]_ErrorCodeTest(napi_env env, napi_callback_info info)
{
    // 准备测试参数（可能触发错误码的场景）
    [参数类型] [参数名] = [测试参数];

    // 调用原生 C 函数
    [返回类型] result = [API名称]([参数]);

    // 在 napi 层使用 napi_throw_error 抛出异常，在 ETS 中通过 try-catch 捕获异常
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

### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with [测试场景] - 错误码测试
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      // 调用 NAPI 函数，预期会抛出异常
      testNapi.[函数名]_ErrorCodeTest([测试参数]);
      // 如果没有抛出异常，则测试失败
      expect.fail('Test should throw error but no error thrown');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Test errCode:${code} message:${errMsg}`);
      // 在 ETS 中通过 try-catch 捕获异常，并对错误码进行断言
      expect(code).assertEqual([错误码]);
      done();
    }
  })
```

---

## 模式 3：返回值覆盖测试模式

**测试场景**：测试 API 返回不同类型值的覆盖情况

### 3.1 枚举值覆盖

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 枚举值测试
 * 测试 [API] 返回枚举值的情况
 */
static napi_value [API名称]_EnumTest(napi_env env, napi_callback_info info)
{
    // 准备测试参数
    [参数类型] [参数名] = [测试参数];

    // 测试枚举值返回
    [枚举类型] enumValue = [API名称]([参数]);
    
    napi_value napiResult;
    napi_create_int32(env, enumValue, &napiResult);
    return napiResult;
}
```

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with [测试场景] - 枚举值测试
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let result = testNapi.[函数名]_EnumTest([测试参数]);
      // 断言返回值为预期的枚举值
      expect(result).assertEqual([枚举值]);
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Test errCode:${code} message:${errMsg}`);
      expect.fail(`Test should not throw error but got: ${errMsg}`);
      done();
    }
  })
```

### 3.2 Bool 值覆盖

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - bool 值测试
 * 测试 [API] 返回 bool 值的情况
 */
static napi_value [API名称]_BoolTest(napi_env env, napi_callback_info info)
{
    // 准备测试参数
    [参数类型] [参数名] = [测试参数];

    // 测试 bool 返回值
    bool result = [API名称]([参数]);
    
    napi_value napiResult;
    napi_get_boolean(env, result, &napiResult);
    return napiResult;
}
```

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with [测试场景] - bool值测试（true/false）
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let result = testNapi.[函数名]_BoolTest([测试参数]);
      // 断言返回值为 true/false
      expect(result).assertEqual([期望的bool值]);
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Test errCode:${code} message:${errMsg}`);
      expect.fail(`Test should not throw error but got: ${errMsg}`);
      done();
    }
  })
```

---

## 模式 4：参数校验异常测试模式

**测试场景**：测试 API 在无效参数时的异常处理

### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 参数校验异常测试
 * 测试 [API] 在参数校验失败时的处理
 */
static napi_value [API名称]_ParamValidationTest(napi_env env, napi_callback_info info)
{
    size_t argc = [参数数量];
    napi_value args[argc];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < [最小参数数量]) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 参数类型检查
    for (size_t i = 0; i < argc; i++) {
        napi_valuetype valuetype;
        status = napi_typeof(env, args[i], &valuetype);
        if (status != napi_ok || valuetype != napi_[参数类型]) {
            napi_throw_error(env, nullptr, "Argument must be [参数类型]");
            return nullptr;
        }
    }

    // 调用函数（可能返回错误码）
    [返回类型] result = [API名称]([参数]);

    // 如果返回错误码，抛出异常
    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Parameter validation failed");
        return nullptr;
    }

    // 返回成功
    napi_value napiResult;
    napi_create_int32(env, 0, &napiResult);
    return napiResult;
}
```

### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with [测试场景] - 参数校验异常
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      // 测试参数校验异常
      testNapi.[函数名]_ParamValidationTest([无效参数]);
      // 如果没有抛出异常，则测试失败
      expect.fail('Test should throw error but no error thrown');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Test errCode:${code} message:${errMsg}`);
      // 断言异常码为预期的错误码
      expect(code).assertEqual([错误码]);
      done();
    }
  })
```

---

## 模式 5：参数类型处理模式

**测试场景**：处理不同类型参数的 N-API 封装

### 5.1 字符串参数处理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 字符串参数处理
 */
static napi_value ProcessStringParam(napi_env env, napi_value arg)
{
    // 获取字符串长度
    napi_status status = napi_get_value_string_utf8(env, arg, NULL, 0, NULL);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get string length");
        return nullptr;
    }

    // 分配内存
    size_t strLen;
    status = napi_get_value_string_utf8(env, arg, NULL, 0, &strLen);
    char* param = (char*)malloc(strLen + 1);
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    // 获取字符串内容
    status = napi_get_value_string_utf8(env, arg, param, strLen + 1, NULL);
    if (status != napi_ok) {
        free(param);
        napi_throw_error(env, nullptr, "Failed to get string value");
        return nullptr;
    }

    // 使用参数...
    char* result = ProcessFunction(param);
    free(param);

    // 返回结果
    napi_value napiResult;
    napi_create_string_utf8(env, result, NAPI_AUTO_LENGTH, &napiResult);
    free(result);
    return napiResult;
}
```

### 5.2 数值参数处理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 数值参数处理
 */
static napi_value ProcessIntParam(napi_env env, napi_value arg)
{
    int32_t value;
    napi_status status = napi_get_value_int32(env, arg, &value);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Invalid integer value");
        return nullptr;
    }

    // 调用函数
    int result = ProcessFunction(value);

    // 返回结果
    napi_value napiResult;
    napi_create_int32(env, result, &napiResult);
    return napiResult;
}
```

### 5.3 布尔参数处理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 布尔参数处理
 */
static napi_value ProcessBoolParam(napi_env env, napi_value arg)
{
    bool value;
    napi_status status = napi_get_value_bool(env, arg, &value);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Invalid boolean value");
        return nullptr;
    }

    // 调用函数
    bool result = ProcessFunction(value);

    // 返回结果
    napi_value napiResult;
    napi_get_boolean(env, result, &napiResult);
    return napiResult;
}
```

---

## 模式 6：错误处理模式

**测试场景**：不同层次的错误处理策略

### 6.1 简单错误处理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 简单错误处理
 */
static napi_value SimpleErrorTest(napi_env env, napi_callback_info info)
{
    [返回类型] result = [API名称]([参数]);
    
    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }
    
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

### 6.2 多错误码处理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 多错误码处理
 */
static napi_value MultiErrorCodeTest(napi_env env, napi_callback_info info)
{
    [返回类型] result = [API名称]([参数]);
    
    switch (result) {
        case [错误码1]:
            napi_throw_error(env, "[错误码1]", "[错误信息1]");
            return nullptr;
        case [错误码2]:
            napi_throw_error(env, "[错误码2]", "[错误信息2]");
            return nullptr;
        case [错误码3]:
            napi_throw_error(env, "[错误码3]", "[错误信息3]");
            return nullptr;
        default:
            break;
    }
    
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

---

## 模式 7：内存管理模式

**测试场景**：测试内存分配和释放的正确性

### 7.1 基础内存管理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 内存管理测试
 */
static napi_value MemoryManagementTest(napi_env env, napi_callback_info info)
{
    char* param = (char*)malloc(256);
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    strcpy(param, "[测试数据]");

    [返回类型] result = [API名称](param);
    free(param);

    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }

    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

### 7.2 复杂结构体处理

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 复杂结构体处理
 */
static napi_value ComplexStructTest(napi_env env, napi_callback_info info)
{
    // 分配结构体内存
    ComplexStruct* param = (ComplexStruct*)malloc(sizeof(ComplexStruct));
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    // 填充结构体
    param->field1 = [值1];
    param->field2 = [值2];

    // 调用函数
    ComplexStruct* result = [API名称](param);
    free(param);

    if (result == NULL) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }

    // 创建返回对象
    napi_value napiResult;
    napi_create_object(env, &napiResult);

    // 设置字段
    napi_value field1Value;
    napi_create_int32(env, result->field1, &field1Value);
    napi_set_named_property(env, napiResult, "field1", field1Value);

    // 释放结果
    free(result);

    return napiResult;
}
```

---

## 模式 8：测试套结构模式

**测试场景**：完整的测试套结构和模块注册

### 8.1 模块初始化函数

#### N-API 封装模板

```cpp
/*
 * 模块初始化函数
 * 在 Init 函数中注册所有 N-API 封装函数
 */
EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"[函数名]_NormalTest", nullptr, [API名称]_NormalTest, nullptr, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"[函数名]_ErrorCodeTest", nullptr, [API名称]_ErrorCodeTest, nullptr, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"[函数名]_EnumTest", nullptr, [API名称]_EnumTest, nullptr, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"[函数名]_BoolTest", nullptr, [API名称]_BoolTest, nullptr, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"[函数名]_ParamValidationTest", nullptr, [API名称]_ParamValidationTest, nullptr, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END
```

### 8.2 模块定义和注册

#### N-API 封装模板

```cpp
/*
 * 模块定义
 */
static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "[模块名]",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

/*
 * 模块注册
 */
extern "C" __attribute__((constructor)) void RegisterEntryModule(void) {
    napi_module_register(&demoModule);
}
```

### 8.3 ETS 测试套基础结构

#### ETS/ArkTS 测试模板

```typescript
/*
 * ETS/ArkTS 测试套基础结构
 */
import { hilog } from '@kit.PerformanceAnalysisKit';
import { describe, it, expect, TestType, Size, Level } from '@ohos/hypium';
import testNapi from 'libentry.so';
import { BusinessError } from '@kit.BasicServicesKit';

const DOMAIN: number = 0xFF00;

export default function acts[测试套名]() {
  describe('[测试套名]', () => {
    // 所有测试用例将在这里定义
  })
}
```

---

## 重要注意事项

### 返回值覆盖规则

1. **枚举值返回**：构造用例覆盖所有枚举值
2. **bool 值返回**：构造用例覆盖 true/false 两种情况
3. **错误码返回**：构造用例覆盖所有错误码

### 错误处理一致性

1. **N-API 层**：使用 `napi_throw_error` 抛出异常，包含错误码和错误信息
2. **ETS 层**：使用 try-catch 捕获异常，通过 `expect` 断言错误码
3. **断言规则**：期望抛出异常时使用 `expect.fail()`，捕获异常时断言错误码

### 参数校验规则

1. **N-API 层**：在 N-API 封装函数中进行参数类型检查
2. **ETS 层**：传递有效或无效参数，验证异常行为
3. **类型检查**：使用 `napi_typeof` 检查参数类型

---

**版本**: 1.0.0
**创建日期**: 2026-03-19
**兼容性**: OpenHarmony API 10+
