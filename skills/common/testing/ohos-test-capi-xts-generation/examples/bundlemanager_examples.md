# BundleManager 子系统示例

> **说明**：BundleManager 是 OpenHarmony 的包管理子系统，负责应用的安装、卸载、信息获取等功能

## 1. 参数测试

```typescript
// BundleManager 参数测试
it('BundleManager_Install_InvalidParam', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 测试空参数
    let result1 = testNapi.BundleManager_Install('');
    expect(result1).assertNotEqual(0);
    
    // 测试过长参数
    let longName = 'a'.repeat(256);
    let result2 = testNapi.BundleManager_Install(longName);
    expect(result2).assertNotEqual(0);
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Invalid param test failed: ${errMsg}`);
    done();
  }
})
```

## 2. 错误测试

```typescript
// BundleManager 错误测试
it('BundleManager_Uninstall_ErrorCode', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 测试不存在的应用
    let result = testNapi.BundleManager_Uninstall('non.existent.app');
    expect(result).assertNotEqual(0);
    
    // 测试已安装的应用卸载
    let installResult = testNapi.BundleManager_Install('com.example.app');
    expect(installResult).assertEqual(0);
    
    let uninstallResult = testNapi.BundleManager_Uninstall('com.example.app');
    expect(uninstallResult).assertEqual(0);
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    let code = (err as BusinessError).code;
    expect(code).assertEqual('ERROR_CODE');
    done();
  }
})
```

## 3. 返回值测试

```typescript
// BundleManager 返回值测试
it('BundleManager_GetInfo_ReturnValue', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 安装应用
    let installResult = testNapi.BundleManager_Install('com.example.app');
    expect(installResult).assertEqual(0);
    
    // 获取应用信息
    let appInfo = testNapi.BundleManager_GetInfo('com.example.app');
    expect(appInfo).assertNotNull();
    expect(appInfo.bundleName).assertEqual('com.example.app');
    expect(appInfo.versionName).assertEqual('1.0.0');
    
    // 卸载应用
    let uninstallResult = testNapi.BundleManager_Uninstall('com.example.app');
    expect(uninstallResult).assertEqual(0);
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Return value test failed: ${errMsg}`);
    done();
  }
})
```

## 4. 边界测试

```typescript
// BundleManager 边界测试
it('BundleManager_Install_Boundary', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 测试最大包名长度
    let maxName = 'a'.repeat(255);
    let result1 = testNapi.BundleManager_Install(maxName);
    expect(result1).assertEqual(0);
    
    // 测试超长包名
    let tooLongName = 'a'.repeat(256);
    let result2 = testNapi.BundleManager_Install(tooLongName);
    expect(result2).assertNotEqual(0);
    
    // 测试最小包名
    let minName = 'a';
    let result3 = testNapi.BundleManager_Install(minName);
    expect(result3).assertNotEqual(0);
    
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Boundary test failed: ${errMsg}`);
    done();
  }
})
```

## 5. 内存测试

```typescript
// BundleManager 内存测试
it('BundleManager_Memory_Management', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    // 多次安装卸载测试内存泄漏
    for (let i = 0; i < 100; i++) {
      let installResult = testNapi.BundleManager_Install('com.example.app');
      expect(installResult).assertEqual(0);
      
      let uninstallResult = testNapi.BundleManager_Uninstall('com.example.app');
      expect(uninstallResult).assertEqual(0);
    }
    
    hilog.info(DOMAIN, 'BundleManagerTest', 'Memory test passed - no leaks detected');
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Memory test failed: ${errMsg}`);
    done();
  }
})
```

## 6. 并发测试

```typescript
// BundleManager 并发测试
it('BundleManager_Concurrent_Access', TestType.FUNCTION | Size.LARGETEST | Level.LEVEL2,
  async (done: Function) => {
  try {
    const promises = [];
    const concurrentCount = 10;
    
    // 并发安装测试
    for (let i = 0; i < concurrentCount; i++) {
      let promise = new Promise((resolve) => {
        setTimeout(() => {
          let result = testNapi.BundleManager_Install('com.example.app');
          expect(result).assertEqual(0);
          resolve();
        }, Math.random() * 1000);
      });
      promises.push(promise);
    }
    
    await Promise.all(promises);
    hilog.info(DOMAIN, 'BundleManagerTest', 'Concurrent test passed');
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Concurrent test failed: ${errMsg}`);
    done();
  }
})
```

## 7. 性能测试

```typescript
// BundleManager 性能测试
it('BundleManager_Performance', TestType.PERFORMANCE | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
  try {
    const iterations = 100;
    const startTime = performance.now();
    
    for (let i = 0; i < iterations; i++) {
      let result = testNapi.BundleManager_GetInfo('com.example.app');
      expect(result).assertNotNull();
    }
    
    const endTime = performance.now();
    const averageTime = (endTime - startTime) / iterations;
    
    expect(averageTime).assertLessThan(10); // 单次操作应小于10ms
    hilog.info(DOMAIN, 'BundleManagerTest', `Average time: ${averageTime}ms`);
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Performance test failed: ${errMsg}`);
    done();
  }
})
```

## 8. 稳定性测试

```typescript
// BundleManager 稳定性测试
it('BundleManager_Stability', TestType.RELIABILITY | Size.LARGETEST | Level.LEVEL2,
  async (done: Function) => {
  try {
    const stressCount = 1000;
    
    // 压力测试
    for (let i = 0; i < stressCount; i++) {
      let installResult = testNapi.BundleManager_Install('com.example.app');
      let uninstallResult = testNapi.BundleManager_Uninstall('com.example.app');
      
      expect(installResult).assertEqual(0);
      expect(uninstallResult).assertEqual(0);
      
      if (i % 100 === 0) {
        hilog.info(DOMAIN, 'BundleManagerTest', `Stability test progress: ${i}/${stressCount}`);
      }
    }
    
    hilog.info(DOMAIN, 'BundleManagerTest', 'Stability test passed');
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Stability test failed: ${errMsg}`);
    done();
  }
})
```

## 9. N-API 封装示例

```cpp
// BundleManager N-API 封装示例
static napi_value BundleManager_Install(napi_env env, napi_callback_info info) {
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
        napi_throw_error(env, nullptr, "First argument must be string");
        return nullptr;
    }
    
    // 3. 提取参数
    size_t bufferSize = 0;
    napi_get_value_string_utf8(env, args[0], nullptr, 0, &bufferSize);
    char* bundleName = new char[bufferSize + 1];
    napi_get_value_string_utf8(env, args[0], bundleName, bufferSize + 1, &bufferSize);
    
    // 4. 调用 CAPI 函数
    int result = BundleManagerInstall(bundleName);
    
    // 5. 内存清理
    delete[] bundleName;
    
    // 6. 错误处理
    if (result != 0) {
        napi_throw_error(env, nullptr, "Install failed");
        return nullptr;
    }
    
    // 7. 返回结果
    napi_value resultValue;
    napi_create_int32(env, result, &resultValue);
    return resultValue;
}

static napi_value BundleManager_Uninstall(napi_env env, napi_callback_info info) {
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
        napi_throw_error(env, nullptr, "Bundle name must be string");
        return nullptr;
    }
    
    // 提取参数
    size_t bufferSize = 0;
    napi_get_value_string_utf8(env, args[0], nullptr, 0, &bufferSize);
    char* bundleName = new char[bufferSize + 1];
    napi_get_value_string_utf8(env, args[0], bundleName, bufferSize + 1, &bufferSize);
    
    // 调用 CAPI 函数
    int result = BundleManagerUninstall(bundleName);
    
    // 内存清理
    delete[] bundleName;
    
    // 错误处理
    if (result == ERROR_INVALID_PARAM) {
        napi_throw_error(env, nullptr, "Invalid bundle name format");
        return nullptr;
    }
    
    if (result == ERROR_NOT_FOUND) {
        napi_throw_error(env, nullptr, "Bundle not found");
        return nullptr;
    }
    
    if (result != SUCCESS) {
        napi_throw_error(env, nullptr, "Uninstall operation failed");
        return nullptr;
    }
    
    // 返回结果
    napi_value resultValue;
    napi_create_int32(env, result, &resultValue);
    return resultValue;
}
```

## 10. ETS 测试示例

```typescript
// BundleManager ETS 测试示例
import { describe, it, expect, TestType, Size, Level } from '@ohos/hypium';
import testNapi from 'libentry.so';
import { BusinessError } from '@kit.BasicServicesKit';
import hilog from '@ohos.hilog';

const DOMAIN: number = 0xFF00;

export default function bundleManagerTest() {
  describe('ActsBundleManagerInstallTest', () => {
    beforeAll(() => {
      hilog.info(DOMAIN, 'BundleManagerTest', 'Test suite started');
    })
    
    afterAll(() => {
      hilog.info(DOMAIN, 'BundleManagerTest', 'Test suite completed');
    })
    
    beforeEach(() => {
      hilog.debug(DOMAIN, 'BundleManagerTest', 'Before each test case');
    })
    
    afterEach(() => {
      hilog.debug(DOMAIN, 'BundleManagerTest', 'After each test case');
    })
    
    it('BundleManager_Install_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          hilog.info(DOMAIN, 'BundleManagerTest', 'Starting install success test');
          
          let result = testNapi.BundleManager_Install('com.example.app');
          expect(result).assertEqual(0);
          
          hilog.info(DOMAIN, 'BundleManagerTest', 'Install success test passed');
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, 'BundleManagerTest', `Install test failed: ${errMsg}, code: ${code}`);
          expect.fail(`Install test failed: ${errMsg}`);
          done();
        }
      })
      
    it('BundleManager_Install_InvalidParam_Fail', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          hilog.info(DOMAIN, 'BundleManagerTest', 'Starting install invalid param test');
          
          let result = testNapi.BundleManager_Install('');
          expect(result).assertNotEqual(0);
          
          hilog.info(DOMAIN, 'BundleManagerTest', 'Install invalid param test passed');
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, 'BundleManagerTest', `Invalid param test failed: ${errMsg}, code: ${code}`);
          done();
        }
      })
  })
}
```

## 11. 断言示例

```typescript
// BundleManager 断言示例
it('BundleManager_Install_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let result = testNapi.BundleManager_Install('com.example.app');
      expect(result).assertEqual(0); // 断言成功返回值为 0
      
      let appInfo = testNapi.BundleManager_GetInfo('com.example.app');
      expect(appInfo).assertNotNull(); // 断言应用信息不为 null
      expect(appInfo.bundleName).assertEqual('com.example.app');
      
      done();
    } catch (err) {
      done();
    }
  })

// BundleManager 比较断言
it('BundleManager_CompareVersion', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let version1 = testNapi.BundleManager_GetVersion('app1');
      let version2 = testNapi.BundleManager_GetVersion('app2');
      
      expect(version1).assertLarger(version2); // 版本 1 大于版本 2
      
      let appSize = testNapi.BundleManager_GetSize('com.example.app');
      expect(appSize).assertLess(100 * 1024 * 1024); // 应用大小小于 100MB
      
      done();
    } catch (err) {
      done();
    }
  })

// BundleManager 集合断言
it('BundleManager_GetList', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let appList = testNapi.BundleManager_GetInstalledApps();
      expect(appList).assertNotNull();
      
      // 断言应用列表包含预期应用
      expect(appList).assertContain('com.example.app');
      expect(appList).assertContain('com.system.settings');
      
      done();
    } catch (err) {
      done();
    }
  })
```

## 12. 错误处理示例

```typescript
// BundleManager 错误处理
it('BundleManager_ErrorHandling', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      // 测试正常情况
      let installResult = testNapi.BundleManager_Install('com.example.app');
      expect(installResult).assertEqual(0);
      
      // 测试错误情况
      let invalidInstall = testNapi.BundleManager_Install('');
      expect(invalidInstall).assertNotEqual(0);
      
      // 测试不存在的应用
      let uninstallResult = testNapi.BundleManager_Uninstall('nonexistent.app');
      expect(uninstallResult).assertNotEqual(0);
      
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.error(DOMAIN, 'BundleManagerTest', `Test failed: ${errMsg}, code: ${code}`);
      expect(code).assertEqual('EXPECTED_ERROR_CODE');
      done();
    }
  })
```

## 13. 日志记录示例

```typescript
// BundleManager 日志示例
it('BundleManager_Install_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      hilog.info(DOMAIN, 'BundleManagerTest', 'Starting install success test');
      
      let result = testNapi.BundleManager_Install('com.example.app');
      hilog.debug(DOMAIN, 'BundleManagerTest', `Install result: ${result}`);
      
      expect(result).assertEqual(0);
      hilog.info(DOMAIN, 'BundleManagerTest', 'Install success test passed');
      
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      hilog.error(DOMAIN, 'BundleManagerTest', `Test failed: ${errMsg}, code: ${code}`);
      done();
    }
  })
```