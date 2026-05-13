# Ability 子系统示例

> **说明**：Ability 是 OpenHarmony 的应用能力子系统，负责应用的启动、生命周期管理、数据传递等功能

## 1. 基础功能测试

```typescript
// Ability 启动测试
it('Ability_Start_Success', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 启动 Ability
    let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
    expect(startResult).assertEqual(0);
    
    // 验证 Ability 状态
    let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
    expect(status).assertEqual('ACTIVE');
    
    hilog.info(DOMAIN, 'AbilityTest', 'Ability start test passed');
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'AbilityTest', `Ability start test failed: ${errMsg}`);
    done();
  }
})
```

## 2. 参数测试

```typescript
// Ability 参数测试
it('Ability_Start_WithParam', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 测试正常参数
    let param = {
      bundleName: 'com.example.ability',
      abilityName: 'MainAbility',
      parameters: {
        userId: 12345,
        sessionId: 'session_001',
        extra: 'test data'
      }
    };
    
    let startResult = testNapi.Ability_StartWithParam('com.example.ability.MainAbility', param);
    expect(startResult).assertEqual(0);
    
    // 测试空参数
    let emptyParam = {
      bundleName: '',
      abilityName: '',
      parameters: null
    };
    
    let invalidResult = testNapi.Ability_StartWithParam('com.example.ability.MainAbility', emptyParam);
    expect(invalidResult).assertNotEqual(0);
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'AbilityTest', `Ability param test failed: ${errMsg}`);
    done();
  }
})
```

## 3. 错误测试

```typescript
// Ability 错误测试
it('Ability_Start_ErrorCase', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 测试不存在的 Ability
    let result1 = testNapi.Ability_Start('non.existent.ability');
    expect(result1).assertNotEqual(0);
    
    // 测试重复启动
    let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
    expect(startResult).assertEqual(0);
    
    let duplicateStart = testNapi.Ability_Start('com.example.ability.MainAbility');
    expect(duplicateStart).assertNotEqual(0); // 重复启动应该失败
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    let code = (err as BusinessError).code;
    expect(code).assertEqual('ERROR_CODE');
    done();
  }
})
```

## 4. 生命周期测试

```typescript
// Ability 生命周期测试
it('Ability_Lifecycle', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 启动 Ability
    let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
    expect(startResult).assertEqual(0);
    
    // 验证生命周期状态
    let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
    expect(status).assertEqual('ACTIVE');
    
    // 暂停 Ability
    let pauseResult = testNapi.Ability_Pause('com.example.ability.MainAbility');
    expect(pauseResult).assertEqual(0);
    
    // 验证暂停状态
    let pausedStatus = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
    expect(pausedStatus).assertEqual('INACTIVE');
    
    // 恢复 Ability
    let resumeResult = testNapi.Ability_Resume('com.example.ability.MainAbility');
    expect(resumeResult).assertEqual(0);
    
    // 验证恢复状态
    let resumedStatus = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
    expect(resumedStatus).assertEqual('ACTIVE');
    
    // 停止 Ability
    let stopResult = testNapi.Ability_Stop('com.example.ability.MainAbility');
    expect(stopResult).assertEqual(0);
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'AbilityTest', `Ability lifecycle test failed: ${errMsg}`);
    done();
  }
})
```

## 5. 数据传递测试

```typescript
// Ability 数据传递测试
it('Ability_Data_Passing', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 设置数据
    let setData = {
      userId: 12345,
      userName: 'John Doe',
      preferences: {
        theme: 'dark',
        language: 'zh'
      }
    };
    
    let setResult = testNapi.Ability_SetData('com.example.ability.MainAbility', 'userProfile', setData);
    expect(setResult).assertEqual(0);
    
    // 获取数据
    let getData = testNapi.Ability_GetData('com.example.ability.MainAbility', 'userProfile');
    expect(getData).assertNotNull();
    expect(getData.userId).assertEqual(12345);
    expect(getData.userName).assertEqual('John Doe');
    
    // 更新数据
    let updateData = {
      ...setData,
      preferences: {
        ...setData.preferences,
        theme: 'light'
      }
    };
    
    let updateResult = testNapi.Ability_SetData('com.example.ability.MainAbility', 'userProfile', updateData);
    expect(updateResult).assertEqual(0);
    
    // 验证更新
    let updatedData = testNapi.Ability_GetData('com.example.ability.MainAbility', 'userProfile');
    expect(updatedData.preferences.theme).assertEqual('light');
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'AbilityTest', `Ability data passing test failed: ${errMsg}`);
    done();
  }
})
```

## 6. 并发测试

```typescript
// Ability 并发测试
it('Ability_Concurrent_Access', TestType.FUNCTION | Size.LARGETEST | Level.LEVEL2,
  async (done: Function) => {
  try {
    const promises = [];
    const concurrentCount = 10;
    
    // 并发启动多个 Ability
    for (let i = 0; i < concurrentCount; i++) {
      let abilityName = `com.example.ability.Ability${i}`;
      let promise = new Promise((resolve) => {
        setTimeout(() => {
          let result = testNapi.Ability_Start(abilityName);
          expect(result).assertEqual(0);
          resolve();
        }, Math.random() * 1000);
      });
      promises.push(promise);
    }
    
    await Promise.all(promises);
    hilog.info(DOMAIN, 'AbilityTest', 'Concurrent ability access test passed');
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'AbilityTest', `Concurrent access test failed: ${errMsg}`);
    done();
  }
})
```

## 7. 性能测试

```typescript
// Ability 性能测试
it('Ability_Performance', TestType.PERFORMANCE | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    const iterations = 100;
    const startTime = performance.now();
    
    for (let i = 0; i < iterations; i++) {
      let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
      expect(startResult).assertEqual(0);
      
      let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
      expect(status).assertEqual('ACTIVE');
      
      let stopResult = testNapi.Ability_Stop('com.example.ability.MainAbility');
      expect(stopResult).assertEqual(0);
    }
    
    const endTime = performance.now();
    const averageTime = (endTime - startTime) / iterations;
    
    expect(averageTime).assertLessThan(20); // 单次操作循环应小于 20ms
    hilog.info(DOMAIN, 'AbilityTest', `Average time: ${averageTime}ms`);
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'AbilityTest', `Performance test failed: ${errMsg}`);
    done();
  }
})
```

## 8. N-API 封装示例

```cpp
// Ability N-API 封装示例
static napi_value Ability_Start(napi_env env, napi_callback_info info) {
    // 1. 参数验证
    size_t argc = 0;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments count");
        return nullptr;
    }
    
    // 2. 类型验证
    napi_valuetype valueType;
    status = napi_typeof(env, args[0], &valueType);
    if (status != napi_ok || valueType != napi_string) {
        napi_throw_error(env, nullptr, "Ability name must be string");
        return nullptr;
    }
    
    // 3. 提取参数
    size_t bufferSize = 0;
    napi_get_value_string_utf8(env, args[0], nullptr, 0, &bufferSize);
    char* abilityName = new char[bufferSize + 1];
    napi_get_value_string_utf8(env, args[0], abilityName, bufferSize + 1, &bufferSize);
    
    // 4. 调用 CAPI 函数
    int result = AbilityStart(abilityName);
    
    // 5. 内存清理
    delete[] abilityName;
    
    // 6. 错误处理
    if (result == ERROR_INVALID_PARAM) {
        napi_throw_error(env, nullptr, "Invalid ability name format");
        return nullptr;
    }
    
    if (result == ERROR_NOT_FOUND) {
        napi_throw_error(env, nullptr, "Ability not found");
        return nullptr;
    }
    
    if (result != SUCCESS) {
        napi_throw_error(env, nullptr, "Ability start failed");
        return nullptr;
    }
    
    // 7. 返回结果
    napi_value resultValue;
    napi_create_int32(env, result, &resultValue);
    return resultValue;
}

static napi_value Ability_GetStatus(napi_env env, napi_callback_info info) {
    // 参数验证和类型检查
    size_t argc = 0;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments count");
        return nullptr;
    }
    
    napi_valuetype valueType;
    status = napi_typeof(env, args[0], &valueType);
    if (status != napi_ok || valueType != napi_string) {
        napi_throw_error(env, nullptr, "Ability name must be string");
        return nullptr;
    }
    
    // 提取参数
    size_t bufferSize = 0;
    napi_get_value_string_utf8(env, args[0], nullptr, 0, &bufferSize);
    char* abilityName = new char[bufferSize + 1];
    napi_get_value_string_utf8(env, args[0], abilityName, bufferSize + 1, &bufferSize);
    
    // 调用 CAPI 函数
    char* status = AbilityGetStatus(abilityName);
    
    // 内存清理
    delete[] abilityName;
    
    // 错误处理
    if (status == nullptr) {
        napi_throw_error(env, nullptr, "Ability not found");
        return nullptr;
    }
    
    // 返回结果
    napi_value resultValue;
    napi_create_string_utf8(env, status, NAPI_AUTO_LENGTH, &resultValue);
    
    // 清理状态字符串
    free(status);
    return resultValue;
}

static napi_value Ability_SetData(napi_env env, napi_callback_info info) {
    // 1. 参数验证
    size_t argc = 0;
    napi_value args[3];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    
    if (status != napi_ok || argc < 3) {
        napi_throw_error(env, nullptr, "Invalid arguments count");
        return nullptr;
    }
    
    // 2. 类型验证
    napi_valuetype valueType;
    status = napi_typeof(env, args[0], &valueType);
    if (status != napi_ok || valueType != napi_string) {
        napi_throw_error(env, nullptr, "Ability name must be string");
        return nullptr;
    }
    
    status = napi_typeof(env, args[1], &valueType);
    if (status != napi_ok || valueType != napi_string) {
        napi_throw_error(env, nullptr, "Data key must be string");
        return nullptr;
    }
    
    status = napi_typeof(env, args[2], &valueType);
    if (status != napi_ok || valueType != napi_object) {
        napi_throw_error(env, nullptr, "Data value must be object");
        return nullptr;
    }
    
    // 3. 提取参数
    size_t bufferSize = 0;
    napi_get_value_string_utf8(env, args[0], nullptr, 0, &bufferSize);
    char* abilityName = new char[bufferSize + 1];
    napi_get_value_string_utf8(env, args[0], abilityName, bufferSize + 1, &bufferSize);
    
    napi_get_value_string_utf8(env, args[1], nullptr, 0, &bufferSize);
    char* dataKey = new char[bufferSize + 1];
    napi_get_value_string_utf8(env, args[1], dataKey, bufferSize + 1, &bufferSize);
    
    // 4. 转换对象为 JSON 字符串
    napi_value jsonString;
    status = napi_stringify(env, &jsonString, args[2], nullptr);
    if (status != napi_ok) {
        delete[] abilityName;
        delete[] dataKey;
        napi_throw_error(env, nullptr, "Failed to stringify data object");
        return nullptr;
    }
    
    size_t jsonLength = 0;
    napi_get_value_string_utf8(env, jsonString, nullptr, 0, &jsonLength);
    char* jsonData = new char[jsonLength + 1];
    napi_get_value_string_utf8(env, jsonString, jsonData, jsonLength + 1, &jsonLength);
    
    // 5. 调用 CAPI 函数
    int result = AbilitySetData(abilityName, dataKey, jsonData);
    
    // 6. 内存清理
    delete[] abilityName;
    delete[] dataKey;
    delete[] jsonData;
    
    // 7. 错误处理
    if (result != SUCCESS) {
        napi_throw_error(env, nullptr, "Failed to set ability data");
        return nullptr;
    }
    
    // 8. 返回结果
    napi_value resultValue;
    napi_create_int32(env, result, &resultValue);
    return resultValue;
}
```

## 9. ETS 测试示例

```typescript
// Ability ETS 测试示例
import { describe, it, expect, TestType, Size, Level } from '@ohos/hypium';
import testNapi from 'libentry.so';
import { BusinessError } from '@kit.BasicServicesKit';
import hilog from '@ohos.hilog';

const DOMAIN: number = 0xFF00;

export default function abilityTest() {
  describe('ActsAbilityStartTest', () => {
    beforeAll(() => {
      hilog.info(DOMAIN, 'AbilityTest', 'Test suite started');
    })
    
    afterAll(() => {
      hilog.info(DOMAIN, 'AbilityTest', 'Test suite completed');
    })
    
    beforeEach(() => {
      hilog.debug(DOMAIN, 'AbilityTest', 'Before each test case');
    })
    
    afterEach(() => {
      hilog.debug(DOMAIN, 'AbilityTest', 'After each test case');
    })
    
    it('Ability_Start_Success', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          hilog.info(DOMAIN, 'AbilityTest', 'Starting ability start test');
          
          let result = testNapi.Ability_Start('com.example.ability.MainAbility');
          expect(result).assertEqual(0);
          
          let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
          expect(status).assertEqual('ACTIVE');
          
          hilog.info(DOMAIN, 'AbilityTest', 'Ability start test passed');
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, 'AbilityTest', `Ability start test failed: ${errMsg}, code: ${code}`);
          expect.fail(`Ability start test failed: ${errMsg}`);
          done();
        }
      })
      
    it('Ability_Start_WithParam', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          hilog.info(DOMAIN, 'AbilityTest', 'Starting ability start with param test');
          
          let param = {
            bundleName: 'com.example.ability',
            abilityName: 'MainAbility',
            parameters: {
              userId: 12345,
              sessionId: 'session_001'
            }
          };
          
          let result = testNapi.Ability_StartWithParam('com.example.ability.MainAbility', param);
          expect(result).assertEqual(0);
          
          hilog.info(DOMAIN, 'AbilityTest', 'Ability start with param test passed');
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, 'AbilityTest', `Ability start with param test failed: ${errMsg}, code: ${code}`);
          done();
        }
      })
  })
}
```

## 10. 断言示例

```typescript
// Ability 断言示例
it('Ability_Start_Success', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
      expect(startResult).assertEqual(0); // 断言启动成功
      
      let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
      expect(status).assertEqual('ACTIVE'); // 断言状态正确
      
      done();
    } catch (err) {
      done();
    }
  })

// Ability 数据传递断言
it('Ability_Data_P_Assertions', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let setData = {
        userId: 12345,
        userName: 'John Doe',
        preferences: {
          theme: 'dark',
          language: 'zh'
        }
      };
      
      let setResult = testNapi.Ability_SetData('com.example.ability.MainAbility', 'userProfile', setData);
      expect(setResult).assertEqual(0);
      
      let getData = testNapi.Ability_GetData('com.example.ability.MainAbility', 'userProfile');
      expect(getData).assertNotNull();
      expect(getData.userId).assertEqual(12345);
      expect(getData.userName).assertEqual('John Doe');
      
      done();
    } catch (err) {
      done();
    }
  })
```

## 11. 错误处理示例

```typescript
// Ability 错误处理
it('Ability_ErrorHandling', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      // 测试正常情况
      let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
      expect(startResult).assertEqual(0);
      
      // 测试错误情况
      let invalidStart = testNapi.Ability_Start('');
      expect(invalidStart).assertNotEqual(0);
      
      // 测试重复启动
      let duplicateStart = testNapi.Ability_Start('com.example.ability.MainAbility');
      expect(duplicateStart).assertNotEqual(0);
      
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.error(DOMAIN, 'AbilityTest', `Test failed: ${errMsg}, code: ${code}`);
      expect(code).assertEqual('EXPECTED_ERROR_CODE');
      done();
    }
  })
```

## 12. 日志记录示例

```typescript
// Ability 日志示例
it('Ability_Start_Success', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      hilog.info(DOMAIN, 'AbilityTest', 'Starting ability start test');
      
      let result = testNapi.Ability_Start('com.example.ability.MainAbility');
      hilog.debug(DOMAIN, 'AbilityTest', `Start result: ${result}`);
      
      let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
      hilog.debug(DOMAIN, 'AbilityTest', `Status: ${status}`);
      
      expect(result).assertEqual(0);
      expect(status).assertEqual('ACTIVE');
      
      hilog.info(DOMAIN, 'AbilityTest', 'Ability start test passed');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.error(DOMAIN, 'AbilityTest', `Test failed: ${errMsg}, code: ${code}`);
      done();
    }
  })
```

## 13. 稳定性测试

```typescript
// Ability 稳定性测试
it('Ability_Stability', TestType.RELIABILITY | Size.LARGETEST | Level.LEVEL2,
  async (done: Function) => {
    try {
      const stressCount = 1000;
      
      // 压力测试
      for (let i = 0; i < stressCount; i++) {
        let startResult = testNapi.Ability_Start('com.example.ability.MainAbility');
        let status = testNapi.Ability_GetStatus('com.example.ability.MainAbility');
        let stopResult = testNapi.Ability_Stop('com.example.ability.MainAbility');
        
        expect(startResult).assertEqual(0);
        expect(status).assertEqual('ACTIVE');
        expect(stopResult).assertEqual(0);
        
        if (i % 100 === 0) {
          hilog.info(DOMAIN, 'AbilityTest', `Stability test progress: ${i}/${stressCount}`);
        }
      }
      
      hilog.info(DOMAIN, 'AbilityTest', 'Stability test passed');
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      hilog.error(DOMAIN, 'AbilityTest', `Stability test failed: ${errMsg}`);
      done();
    }
  })
```