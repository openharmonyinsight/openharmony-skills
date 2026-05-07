# N-API 和 ETS/ArkTS 高级测试模式

> **文档目的**：提供 N-API 封装和 ETS/ArkTS 测试的高级模式和特殊场景参考

> 📖 **相关文档**：
> - [公共基础模式](./test_patterns_napi_ets.md) - N-API 和 ETS 公共模式定义
> - [工程配置模板](./project_config_templates.md) - Test.json、oh-package.json5 配置指南
> - [测试生成核心](./test_generation_c.md) - 测试用例生成核心文档

## 模式概述

本文档提供 N-API 封装和 ETS/ArkTS 测试的高级模式和特殊场景参考。基础模式（正常测试、错误码测试、参数校验等）请参考 [公共基础模式文档](./test_patterns_napi_ets.md)。

**重要要求**：
1. **强制要求使用 N-API 封装测试** - 封装时注意如果 CAPI 返回异常或参数校验异常时，使用 `napi_throw_error` 抛出异常
2. **生成用例时要求能够覆盖返回值的多种可能**：
   - 返回值类型为枚举值时，要求构造的用例能够覆盖所有枚举值返回
   - 返回值为 bool 时，要求覆盖返回 true/false
   - 返回值为错误码时，要求覆盖所有错误码
3. **在 ETS 中调用对 CAPI 封装得到的 JS API**，并对 API 返回值、抛出异常值做断言

**重要原则**：
- **返回值覆盖**：构造用例覆盖所有可能的返回值（枚举值、bool 值、错误码）
- **错误处理一致性**：N-API 层使用 `napi_throw_error` 抛出异常，ETS 层通过 try-catch 捕获并断言
- **参数校验**：在 N-API 层进行参数类型检查，ETS 层传递测试数据

---

## 高级模式（L3 专用）

### 模式 A1：多参数组合测试

**测试场景**：测试 API 处理多个参数的不同组合情况

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 多参数组合测试
 * 测试多个参数的不同组合情况
 */
static napi_value [API名称]_MultiParamTest(napi_env env, napi_callback_info info)
{
    size_t argc = 3;
    napi_value args[3];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 3) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 提取多个参数
    [参数类型1] param1;
    [参数类型2] param2;
    [参数类型3] param3;
    
    status = napi_get_value_[type1](env, args[0], &param1);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get param1");
        return nullptr;
    }
    
    status = napi_get_value_[type2](env, args[1], &param2);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get param2");
        return nullptr;
    }
    
    status = napi_get_value_[type3](env, args[2], &param3);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get param3");
        return nullptr;
    }

    // 调用函数
    [返回类型] result = [API名称](param1, param2, param3);

    // 错误处理
    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }

    // 返回结果
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with multiple parameter combinations
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    const testCases = [
      { param1: "value1", param2: "value2", expected: "result1" },
      { param1: "value3", param2: "value4", expected: "result2" },
      // ... 更多测试用例
    ];

    for (let i = 0; i < testCases.length; i++) {
      try {
        let result = testNapi.[函数名]_MultiParamTest(testCases[i].param1, testCases[i].param2, testCases[i].param3);
        expect(result).assertEqual(testCases[i].expected);
        hilog.info(DOMAIN, 'testTag', `Test case ${i} passed`);
      } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.info(DOMAIN, "testTag", `Test case ${i} failed: errCode:${code} message:${errMsg}`);
        expect.fail(`Test case ${i} should not throw error but got: ${errMsg}`);
      }
    }

    done();
  })
```

---

### 模式 A2：数组参数处理

**测试场景**：测试 API 处理数组参数的情况

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 数组参数处理
 */
static napi_value [API名称]_ArrayTest(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 检查是否为数组
    bool isArray;
    status = napi_is_array(env, args[0], &isArray);
    if (status != napi_ok || !isArray) {
        napi_throw_error(env, nullptr, "Argument must be an array");
        return nullptr;
    }

    // 获取数组长度
    uint32_t arrayLength;
    status = napi_get_array_length(env, args[0], &arrayLength);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get array length");
        return nullptr;
    }

    // 处理数组元素
    [参数类型]* elements = ([参数类型]*)malloc(arrayLength * sizeof([参数类型]));
    if (elements == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    for (uint32_t i = 0; i < arrayLength; i++) {
        napi_value element;
        status = napi_get_element(env, args[0], i, &element);
        if (status != napi_ok) {
            free(elements);
            napi_throw_error(env, nullptr, "Failed to get array element");
            return nullptr;
        }

        status = napi_get_value_[type](env, element, &elements[i]);
        if (status != napi_ok) {
            free(elements);
            napi_throw_error(env, nullptr, "Failed to get element value");
            return nullptr;
        }
    }

    // 调用函数
    [返回类型] result = [API名称](elements, arrayLength);
    free(elements);

    // 错误处理
    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }

    // 返回结果
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with array parameter
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    const testArray = [1, 2, 3, 4, 5];
    try {
      let result = testNapi.[函数名]_ArrayTest(testArray);
      // 断言返回值
      expect(result).assertEqual([期望结果]);
      hilog.info(DOMAIN, 'testTag', 'Array test passed');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Array test failed: errCode:${code} message:${errMsg}`);
      expect.fail(`Array test should not throw error but got: ${errMsg}`);
      done();
    }
  })
```

---

### 模式 A3：对象参数处理

**测试场景**：测试 API 处理对象参数的情况

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 对象参数处理
 */
static napi_value [API名称]_ObjectTest(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 检查是否为对象
    bool isObject;
    status = napi_is_object(env, args[0], &isObject);
    if (status != napi_ok || !isObject) {
        napi_throw_error(env, nullptr, "Argument must be an object");
        return nullptr;
    }

    // 从对象提取属性
    napi_value property1;
    napi_value property2;
    
    status = napi_get_named_property(env, args[0], "[属性名1]", &property1);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get property1");
        return nullptr;
    }
    
    status = napi_get_named_property(env, args[0], "[属性名2]", &property2);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get property2");
        return nullptr;
    }

    // 提取属性值
    [参数类型1] value1;
    [参数类型2] value2;
    
    status = napi_get_value_[type1](env, property1, &value1);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get value1");
        return nullptr;
    }
    
    status = napi_get_value_[type2](env, property2, &value2);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get value2");
        return nullptr;
    }

    // 调用函数
    [返回类型] result = [API名称](value1, value2);

    // 错误处理
    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }

    // 返回结果
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with object parameter
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    const testObject = {
      property1: "value1",
      property2: 123,
      property3: true
    };
    
    try {
      let result = testNapi.[函数名]_ObjectTest(testObject);
      // 断言返回值
      expect(result).assertEqual([期望结果]);
      hilog.info(DOMAIN, 'testTag', 'Object test passed');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Object test failed: errCode:${code} message:${errMsg}`);
      expect.fail(`Object test should not throw error but got: ${errMsg}`);
      done();
    }
  })
```

---

### 模式 A4：异步测试模式

**测试场景**：测试 API 的异步操作

#### N-API 封装模板

```cpp
/*
 * N-API 封装函数 - 异步调用模式
 * 使用 napi_queue_async_work 进行异步操作
 */
struct AsyncData {
    napi_env env;
    napi_deferred deferred;
    [参数类型] params;
    [返回类型] result;
    bool success;
    char* error;
};

static void ExecuteWork(napi_env env, void* data) {
    AsyncData* asyncData = (AsyncData*)data;
    // 执行异步工作
    asyncData->result = [API名称](asyncData->params);
    if (asyncData->result == [错误码]) {
        asyncData->success = false;
        asyncData->error = strdup("Operation failed");
    } else {
        asyncData->success = true;
    }
}

static void CompleteWork(napi_env env, napi_status status, void* data) {
    AsyncData* asyncData = (AsyncData*)data;
    
    napi_value result;
    if (asyncData->success) {
        napi_create_[type](env, asyncData->result, &result);
        napi_resolve_deferred(env, asyncData->deferred, result);
    } else {
        napi_value error;
        napi_create_string_utf8(env, asyncData->error, NAPI_AUTO_LENGTH, &error);
        napi_reject_deferred(env, asyncData->deferred, error);
        free(asyncData->error);
    }
    
    delete asyncData;
}

static napi_value [API名称]_AsyncTest(napi_env env, napi_callback_info info) {
    size_t argc = [参数数量];
    napi_value args[argc];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < [最小参数数量]) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 创建 Promise
    napi_value promise, deferred;
    status = napi_create_promise(env, &deferred, &promise);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to create promise");
        return nullptr;
    }

    // 准备异步数据
    AsyncData* asyncData = new AsyncData();
    asyncData->env = env;
    asyncData->deferred = deferred;
    
    // 提取参数
    [提取参数代码]
    asyncData->params = [参数];

    // 创建异步工作项
    napi_value workName;
    napi_create_string_utf8(env, "[API名称]_AsyncTest", NAPI_AUTO_LENGTH, &workName);
    
    napi_async_work* work;
    napi_create_async_work(env, nullptr, workName, ExecuteWork, CompleteWork, asyncData, &work);
    
    // 队列异步工作
    napi_queue_async_work(env, work);

    return promise;
}
```

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with asynchronous operation
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let promiseResult = testNapi.[函数名]_AsyncTest([测试参数]);
      // 验证是否为 Promise
      expect(promiseResult instanceof Promise).assertTrue();
      
      // 等待 Promise 完成
      let result = await promiseResult;
      expect(result).assertEqual([期望结果]);
      hilog.info(DOMAIN, 'testTag', 'Async test passed');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Async test failed: errCode:${code} message:${errMsg}`);
      expect.fail(`Async test should not throw error but got: ${errMsg}`);
      done();
    }
  })
```

---

### 模式 A5：性能测试模式

**测试场景**：测试 API 的性能表现

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] performance
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    const iterations = 1000;
    const startTime = performance.now();

    for (let i = 0; i < iterations; i++) {
      try {
        let result = testNapi.[函数名]([测试参数]);
        expect(result).assertEqual([期望值]);
      } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.info(DOMAIN, "testTag", `Performance test failed: errCode:${code} message:${errMsg}`);
        expect.fail(`Performance test should not throw error but got: ${errMsg}`);
      }
    }

    const endTime = performance.now();
    const averageTime = (endTime - startTime) / iterations;
    hilog.info(DOMAIN, 'testTag', `Average execution time: ${averageTime}ms`);

    expect(averageTime).assertLessThan([最大平均时间]);
    done();
  })
```

---

### 模式 A6：并发测试模式

**测试场景**：测试 API 的并发执行能力

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with concurrent execution
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    const concurrentCount = 10;
    const testPromises = [];

    for (let i = 0; i < concurrentCount; i++) {
      testPromises.push(
        new Promise<void>((resolve, reject) => {
          try {
            let result = testNapi.[函数名]([测试参数]);
            expect(result).assertEqual([期望值]);
            resolve();
          } catch (err) {
            let errMsg = (err as BusinessError).message;
            let code = (err as BusinessError).code;
            hilog.info(DOMAIN, "testTag", `Concurrent test failed: errCode:${code} message:${errMsg}`);
            reject(err);
          }
        })
      );
    }

    try {
      await Promise.all(testPromises);
      hilog.info(DOMAIN, 'testTag', 'Concurrent test passed');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.info(DOMAIN, "testTag", `Concurrent test failed: errCode:${code} message:${errMsg}`);
      expect.fail(`Concurrent test failed: ${errMsg}`);
      done();
    }
  })
```

---

### 模式 A7：边界值组合测试

**测试场景**：测试 API 在边界值组合情况下的行为

#### ETS/ArkTS 测试模板

```typescript
/**
 * @tc.number Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.name Sub_[子系统]_[模块]_[API]_[序号]
 * @tc.desc Test [API] with boundary value combinations
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 2
 */
it('Sub_[子系统]_[模块]_[API]_[序号]', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    const boundaryTestCases = [
      { description: "最小边界值", param: [最小值], expected: [期望结果] },
      { description: "最大边界值", param: [最大值], expected: [期望结果] },
      { description: "空指针", param: [null], expected: [期望结果] },
      { description: "空字符串", param: [""], expected: [期望结果] },
      { description: "超长字符串", param: [超长字符串], expected: [期望结果] },
    ];

    for (const testCase of boundaryTestCases) {
      try {
        let result = testNapi.[函数名](testCase.param);
        expect(result).assertEqual(testCase.expected);
        hilog.info(DOMAIN, 'testTag', `Boundary test passed: ${testCase.description}`);
      } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.info(DOMAIN, "testTag", `Boundary test failed: ${testCase.description}, errCode:${code} message:${errMsg}`);
        expect.fail(`Boundary test failed: ${testCase.description}, got: ${errMsg}`);
      }
    }

    done();
  })
```

---

## 测试配置模板

### Test.json 高级配置

```json
{
    "description": "Configuration for Tests",
    "driver": {
        "type": "OHJSUnitTest",
        "test-timeout": "180000",
        "shell-timeout": "180000",
        "bundle-name": "[包名]",
        "module-name": "[模块名]"
    },
    "kits": [
        {
            "test-file-name": [
                "[HAP文件名].hap"
            ],
            "type": "AppInstallKit",
            "cleanup-apps": true
        }
    ],
    "test": {
        "disable": [
            "testDisabled"
        ],
        "features": [
            "feature1",
            "feature2"
        ]
    },
    "params": {
        "timeout": 30000,
        "retry": 2,
        "log-level": "INFO"
    }
}
```

### 高级测试套结构

```typescript
/*
 * 高级测试套结构 - 包含多种测试类型
 */
import { hilog } from '@kit.PerformanceAnalysisKit';
import { describe, it, expect, TestType, Size, Level } from '@ohos/hypium';
import testNapi from 'libentry.so';
import { BusinessError } from '@kit.BasicServicesKit';

const DOMAIN: number = 0xFF00;

export default function acts[测试套名]() {
  describe('[测试套名] - 基础功能', () => {
    // 基础功能测试
    it('基础功能测试', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: Function) => {
      // 基础测试逻辑
      done();
    });
  });

  describe('[测试套名] - 边界测试', () => {
    // 边界值测试
    it('边界值测试', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: Function) => {
      // 边界测试逻辑
      done();
    });
  });

  describe('[测试套名] - 性能测试', () => {
    // 性能测试
    it('性能测试', TestType.FUNCTION | Size.LARGETEST | Level.LEVEL1, async (done: Function) => {
      // 性能测试逻辑
      done();
    });
  });
}
```

---

## 最佳实践

### 测试用例命名规范

| 测试类型 | 前缀 | 示例 |
|---------|------|------|
| 正常情况 | `Normal_` | `Normal_BasicFunctionTest` |
| 错误码 | `Error_` | `Error_InvalidParameterTest` |
| 边界值 | `Boundary_` | `Boundary_MinValueTest` |
| 性能 | `Performance_` | `Performance_LoopTest` |
| 并发 | `Concurrent_` | `Concurrent_MultipleCallsTest` |

### 断言使用规范

```typescript
// 数值断言
expect(result).assertEqual(expectedValue);
expect(result).assertGreaterThan(minValue);
expect(result).assertLessThan(maxValue);
expect(result).assertLte(maxValue); // 小于等于
expect(result).assertGte(minValue); // 大于等于

// 字符串断言
expect(result).assertEqual(expectedString);
expect(result).assertContain(subString);
expect(result).assertMatch(regexp);

// 数组断言
expect(array.length).assertEqual(expectedLength);
expect(array).assertContain(item);

// 异常断言
expect(() => { riskyFunction() }).assertThrow();
expect(() => { riskyFunction() }).assertThrow(BusinessError);
```

### 日志记录规范

```typescript
// 测试开始
hilog.info(DOMAIN, 'testTag', `Starting test: ${testName}`);

// 测试成功
hilog.info(DOMAIN, 'testTag', `Test passed: ${testName}, result: ${JSON.stringify(result)}`);

// 测试失败
hilog.error(DOMAIN, 'testTag', `Test failed: ${testName}, error: ${errMsg}`);

// 性能数据
hilog.info(DOMAIN, 'testTag', `Performance: ${duration}ms, avg: ${avgTime}ms`);

// 调试信息
hilog.debug(DOMAIN, 'testTag', `Debug info: ${JSON.stringify(debugData)}`);
```

### 错误处理规范

```typescript
try {
  // 执行测试
  let result = testNapi.[函数名](parameters);
  expect(result).assertEqual(expected);
} catch (err) {
  let errMsg = (err as BusinessError).message;
  let code = (err as BusinessError).code;
  
  // 记录错误
  hilog.error(DOMAIN, 'testTag', `Test failed: errCode:${code} message:${errMsg}`);
  
  // 断言错误
  expect.fail(`Test failed with error: ${errMsg}`);
}
```

### 内存管理规范

1. **确保所有分配的内存都有对应的释放**
   - 使用 `malloc` 分配的内存必须使用 `free` 释放
   - 在错误处理路径中也要确保释放已分配的内存

2. **使用 RAII 模式管理资源**
   - 考虑使用智能指针管理资源
   - 确保异常情况下资源正确释放

### 性能优化规范

1. **避免不必要的类型转换**
   - 尽量使用原生类型
   - 减少类型转换开销

2. **批处理操作**
   - 对于数组操作，尽量批处理
   - 减少函数调用次数

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

### 异步操作规范

1. **Promise 创建**：使用 `napi_create_promise` 创建 Promise
2. **异步工作**：使用 `napi_queue_async_work` 队列异步工作
3. **错误处理**：在 `CompleteWork` 回调中处理错误和成功结果
4. **内存管理**：确保异步数据的正确分配和释放

---

**版本**: 2.0.0  
**创建日期**: 2026-03-19  
**更新日期**: 2026-03-19  
**兼容性**: OpenHarmony API 10+