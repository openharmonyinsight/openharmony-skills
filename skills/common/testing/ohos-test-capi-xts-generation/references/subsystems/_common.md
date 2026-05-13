# CAPI XTS 测试通用配置

> **子系统通用配置** - 所有子系统共享的 CAPI N-API 封装测试配置

## 重要说明

### ⭐ 测试方式要求

**本技能专门用于生成方式2（N-API 封装测试）的测试用例**

- ✅ **强制使用方式2**：N-API 封装测试
- ❌ **不再使用方式1**：Native C 测试（仅用于 Legacy 测试用例维护）

### 方式对比

| 特性 | 方式1：Native C 测试 | 方式2：N-API 封装测试 |
|------|------|------|
| 测试框架 | gtest/HWTEST_F | N-API + ETS/ArkTS |
| 测试文件 | `.cpp` | `NapiTest.cpp` + `.test.ets` |
| 函数封装 | 直接调用 C 函数 | N-API 封装后调用 |
| 测试环境 | C/C++ 测试环境 | ETS/ArkTS 测试环境 |
| 状态 | 已淘汰 | **必需使用** |

---

## 一、测试用例编号规范

### 1.1 编号格式

```
SUB_[子系统]_[模块]_[API]_[类型]_[序号]
```

### 1.2 编号示例

```
SUB_HILOG_LOG_HiLogPrint_PARAM_001
SUB_HILOG_LOG_HiLogPrint_ERROR_001
SUB_HILOG_LOG_HiLogPrint_RETURN_001
SUB_HILOG_LOG_HiLogPrint_BOUNDARY_001
```

### 1.3 类型说明

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| PARAM | 参数测试 | 测试正常参数、特殊参数 |
| ERROR | 错误码测试 | 测试错误返回值 |
| RETURN | 返回值测试 | 测试返回值的正确性 |
| BOUNDARY | 边界值测试 | 测试边界条件 |
| MEMORY | 内存管理测试 | 测试内存分配释放 |

---

## 二、N-API 封装函数规范

### 2.1 函数签名

```c
static napi_value [API名]_[测试场景]_napi(napi_env env, napi_callback_info info)
```

### 2.2 函数注释

```c
/**
 * @tc.name: SUB_[子系统]_[模块]_[API]_[类型]_[序号]
 * @tc.desc: [测试场景描述]
 * @tc.type: FUNC
 * @tc.require: [需求编号]
 */
```

### 2.3 函数结构

```c
/**
 * @tc.name: SUB_HILOG_LOG_HiLogPrint_PARAM_001
 * @tc.desc: 测试 HiLogPrint 的正常参数
 * @tc.type: FUNC
 */
static napi_value HiLogPrint_NormalParam_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status;

    // 1. 获取回调信息
    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 2. 参数类型检查
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string");
        return nullptr;
    }

    // 3. 提取参数值
    char tag[256] = {0};
    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], tag, sizeof(tag) - 1, &strLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get string value");
        return nullptr;
    }

    // 4. 调用原生 C 函数
    const char* fmt = "Test message: %d";
    int value = 42;
    int ret = HiLogPrint(LOG_CORE, LOG_INFO, LOG_DOMAIN, tag, fmt, value);

    // 5. 验证结果并返回
    napi_value result;
    if (ret >= 0) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_throw_error(env, "NEGATIVE_RETURN", "Negative return value");
        return nullptr;
    }

    return result;
}
```

### 2.4 错误处理

```c
// 使用 napi_throw_error 抛出异常
if (ret < 0) {
    napi_throw_error(env, "ERROR_CODE", "Error message");
    return nullptr;
}

// 返回成功结果
napi_value result;
napi_create_int32(env, 0, &result);
return result;
```

---

## 三、ETS/ArkTS 测试用例规范

### 3.1 测试用例结构

```typescript
/**
 * @tc.name: SUB_[子系统]_[模块]_[API]_[类型]_[序号]
 * @tc.desc: [测试场景描述]
 * @tc.type: FUNC
 * @tc.require: [需求编号]
 */
it('[API名]_[场景描述]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    // 测试代码
    done();
  });
```

### 3.2 测试用例注释

```typescript
/**
 * @tc.name: SUB_HILOG_LOG_HiLogPrint_PARAM_001
 * @tc.desc: 测试 HiLogPrint 的正常参数
 * @tc.type: FUNC
 */
```

### 3.3 测试用例结构

```typescript
/**
 * @tc.name: SUB_HILOG_LOG_HiLogPrint_PARAM_001
 * @tc.desc: 测试 HiLogPrint 的正常参数
 * @tc.type: FUNC
 */
it('HiLogPrint_NormalParam', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    // 1. 准备测试数据
    const testTag = "TEST_TAG";
    const testMsg = "Test message";

    try {
      // 2. 调用 N-API 封装的函数
      let result = testNapi.HiLogPrint_NormalParam_napi(testTag);

      // 3. 验证返回值
      expect(result).assertEqual(0);

      hilog.info(DOMAIN, "testTag", `Test passed: result=${result}`);
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.error(DOMAIN, "testTag", `Test failed: errCode:${code} message:${errMsg}`);
      expect.fail(`Test should not throw error but got: ${errMsg}`);
    }

    done();
  });
```

### 3.4 异常处理

```typescript
try {
  let result = testNapi.API_Function_napi(param1, param2);
  expect(result).assertEqual(expected);
} catch (err) {
  let errMsg = (err as BusinessError).message;
  let code = (err as BusinessError).code;
  hilog.error(DOMAIN, "testTag", `Test failed: errCode:${code} message:${errMsg}`);
  expect.fail(`Test should not throw error but got: ${errMsg}`);
}
```

---

## 四、N-API 常用 API 规范

### 4.1 参数提取

```c
// 获取参数数量
size_t argc = 1;

// 获取参数数组
napi_value args[1];

// 获取回调信息
napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
if (status != napi_ok || argc < 1) {
    napi_throw_error(env, nullptr, "Invalid arguments");
    return nullptr;
}
```

### 4.2 类型检查

```c
// 获取值的类型
napi_valuetype valuetype;
status = napi_typeof(env, args[0], &valuetype);
if (status != napi_ok || valuetype != napi_string) {
    napi_throw_error(env, nullptr, "Argument must be a string");
    return nullptr;
}
```

### 4.3 字符串转换

```c
// 从 napi_value 提取字符串
char str[256] = {0};
size_t strLen;
status = napi_get_value_string_utf8(env, args[0], str, sizeof(str) - 1, &strLen);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Failed to get string value");
    return nullptr;
}
```

### 4.4 整数转换

```c
// 从 napi_value 提取整数
int32_t value;
status = napi_get_value_int32(env, args[0], &value);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Failed to get int32 value");
    return nullptr;
}
```

### 4.5 创建返回值

```c
// 创建整数返回值
napi_value result;
napi_create_int32(env, value, &result);
return result;

// 创建布尔返回值
napi_value result;
napi_get_boolean(env, true, &result);
return result;
```

### 4.6 抛出异常

```c
// 抛出一般异常
napi_throw_error(env, "ERROR_CODE", "Error message");
return nullptr;

// 抛出类型错误
napi_throw_type_error(env, "TypeError message");
return nullptr;

// 抛出范围错误
napi_throw_range_error(env, "RangeError message");
return nullptr;
```

---

## 五、测试用例命名规范

### 5.1 测试套命名

- 格式：`[模块名]Test`
- 示例：`HilogTest`, `BundleManagerTest`

### 5.2 N-API 封装函数命名

- 格式：`[API名]_[场景描述]_napi`
- 示例：`HiLogPrint_NormalParam_napi`, `HiLogPrint_NullPointer_napi`

### 5.3 ETS 测试用例命名

- 格式：`[API名]_[场景描述]`
- 示例：`HiLogPrint_NormalParam`, `HiLogPrint_NullPointer`, `HiLogPrint_BoundaryValue`

---

## 六、测试级别说明

| 级别 | 说明 | 使用场景 |
|------|------|---------|
| Level0 | 冒烟测试，基本功能验证 | 最基本的测试用例 |
| Level1 | 基本功能测试 | 正常场景测试 |
| Level2 | 重要功能测试 | 主要功能测试 |
| Level3 | 全面功能测试 | 完整功能测试 |
| Level4 | 压力测试、稳定性测试 | 压力和稳定性测试 |

---

## 七、测试规模说明

| 规模 | 说明 | 使用场景 |
|------|------|---------|
| SMALLTEST | 小规模测试（< 1分钟） | 简单功能测试 |
| MEDIUMTEST | 中等规模测试（1-10分钟） | 常规功能测试 |
| LARGETEST | 大规模测试（> 10分钟） | 复杂功能测试 |

---

## 八、返回值覆盖要求

### 8.1 完整性要求

每个 API 必须覆盖：
- ✅ 枚举值：覆盖所有枚举值返回
- ✅ bool 值：覆盖 true/false 两种情况
- ✅ 错误码：覆盖所有错误码
- ✅ 指针：覆盖 nullptr、有效指针
- ✅ 数值：覆盖正数、负数、零、边界值

### 8.2 覆盖示例

```typescript
// 枚举值覆盖
it('ReturnValue_Enum_AllValues', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, ...)

// bool 值覆盖
it('ReturnValue_Bool_True', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, ...)
it('ReturnValue_Bool_False', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, ...)

// 错误码覆盖
it('ErrorCode_InvalidParam', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, ...)
it('ErrorCode_NullPointer', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, ...)
```

---

## 九、内存管理规范

### 9.1 N-API 内存管理

```c
// N-API 环境会自动管理内存，避免手动释放
// 但仍需注意：
// - 不要返回局部变量的地址
// - 确保所有 napi_value 正确创建
```

### 9.2 原生 C 函数内存管理

```c
// 调用原生 C 函数时，确保：
// - 所有分配的内存都有对应的释放
// - 使用后指针置为 nullptr
// - 无悬空指针
```

---

## 十、断言方法规范

### 10.1 ETS/ArkTS 断言

| 场景 | 断言方法 |
|------|---------|
| 检查相等 | `expect(actual).assertEqual(expected)` |
| 检查不等 | `expect(actual).assertNotEqual(expected)` |
| 检查为真 | `expect(condition).assertTrue()` |
| 检查为假 | `expect(condition).assertFalse()` |
| 检查抛出异常 | `expect(() => { ... }).toThrow()` |
| 测试失败 | `expect.fail("Message")` |

### 10.2 异常断言

```typescript
// 使用 try-catch 捕获异常并断言
try {
  let result = testNapi.API_Function_napi(param);
  expect(result).assertEqual(expected);
} catch (err) {
  let errMsg = (err as BusinessError).message;
  let code = (err as BusinessError).code;
  hilog.error(DOMAIN, "testTag", `Test failed: errCode:${code} message:${errMsg}`);
  expect.fail(`Test should not throw error but got: ${errMsg}`);
}
```

---

## 十一、测试设计文档规范

### 11.1 文件命名

```
测试设计文档.md
```

### 11.2 文档格式

```markdown
# 测试设计文档：[测试文件名]

## 测试用例列表

| 编号 | 名称 | 描述 | 类型 | 状态 |
|------|------|------|------|------|
| SUB_[子系统]_[模块]_[API]_PARAM_001 | [测试用例名] | [描述] | PARAM | 已生成 |

## 测试用例详情

### SUB_[子系统]_[模块]_[API]_PARAM_001

- **名称**: [测试用例名]
- **描述**: [测试用例描述]
- **类型**: PARAM
- **前置条件**: [前置条件]
- **测试步骤**:
  1. 准备测试数据
  2. 调用被测 API
  3. 验证结果
- **预期结果**: [预期结果]
- **实际结果**: [实际结果]
- **状态**: PASS/FAIL
```

---

## 十二、代码风格规范

### 12.1 缩进和空格

- 使用 2 个空格缩进（TypeScript/JavaScript）
- 使用 4 个空格缩进（C/C++）
- 操作符前后添加空格
- 逗号后添加空格

### 12.2 命名规范

- 变量名：使用驼峰命名法（camelCase）
- 函数名：使用驼峰命名法（camelCase）
- 类型名：使用帕斯卡命名法（PascalCase）
- 常量：使用全大写下划线分隔（UPPER_SNAKE_CASE）

### 12.3 注释规范

- 每个测试用例前添加注释块
- 复杂逻辑添加行内注释
- 使用清晰的描述性语言

---

## 十三、禁止事项

### 13.1 禁止的操作

- ❌ 使用 Native C 测试（方式1）
- ❌ 直接调用 C 函数而不通过 N-API 封装
- ❌ 修改工程配置文件
- ❌ 使用未声明的函数
- ❌ 硬编码测试数据（使用常量或配置）
- ❌ 忽略错误返回值
- ❌ 内存泄漏
- ❌ 循环依赖

### 13.2 禁止的测试行为

- ❌ 测试用例相互依赖
- ❌ 使用全局变量（除非必要）
- ❌ 测试不确定的行为
- ❌ 使用不可靠的断言

---

## 十四、测试用例质量标准

### 14.1 代码质量

- ✅ 编译无警告
- ✅ 无内存泄漏
- ✅ 无未定义行为
- ✅ 遵循编码规范

### 14.2 测试覆盖

- ✅ 覆盖所有 API
- ✅ 覆盖所有错误码
- ✅ 覆盖边界条件
- ✅ 覆盖异常场景
- ✅ 覆盖所有返回值类型

### 14.3 测试可靠性

- ✅ 测试用例可重复执行
- ✅ 测试结果稳定
- ✅ 测试执行时间合理
- ✅ 无副作用

---

## 十五、模块注册规范

### 15.1 N-API 模块定义

```c
// N-API 模块定义
static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "[模块名]",
    .nm_priv = ((void *)0),
    .reserved = {0},
};
```

### 15.2 模块初始化

```c
// 模块初始化函数
static napi_value Init(napi_env env, napi_value exports)
{
    // 注册所有测试函数
    napi_property_descriptor desc[] = {
        DECLARE_NAPI_FUNCTION("[函数名1]", [函数名1]_napi),
        DECLARE_NAPI_FUNCTION("[函数名2]", [函数名2]_napi),
        // ...
    };

    NAPI_CALL(env, napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc));

    return exports;
}
```

---

## 十六、校验流程参考

> 📋 **校验流程详见通用校验模块**：[modules/L2_Generation/verification_common.md](../../modules/L2_Generation/verification_common.md)
>
> 本节仅提供校验概要，详细校验方法请查看通用校验模块。

### 16.1 三重Napi校验

测试代码生成完成后必须执行：

| 步骤 | 校验项 | 校验位置 |
|------|--------|---------|
| 步骤 1 | N-API 函数注册 | `entry/src/main/cpp/NapiTest.cpp` 的 `Init` 函数 |
| 步骤 2 | TypeScript 接口声明 | `entry/src/main/cpp/types/libentry/index.d.ts` |
| 步骤 3 | ETS 测试接口使用 | `entry/src/ohosTest/ets/test/*.test.ets` |

### 16.2 编译前工程结构校验

编译前必须执行：

- 必需目录和文件完整性检查
- BUILD.gn 模板配置检查
- hap 包名对应关系检查
- 上层 BUILD.gn 注册检查

---

**版本**: 2.1.0
**创建日期**: 2026-03-06
**更新日期**: 2026-03-24
**兼容性**: OpenHarmony API 10+
**测试方式**: N-API 封装测试（方式2）
