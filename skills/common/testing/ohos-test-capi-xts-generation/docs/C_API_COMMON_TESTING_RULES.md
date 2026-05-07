# 从历史测试用例中提取的 CAPI 通用测试规则

## 基于测试用例文件分析

测试用例文件：`{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest/entry/src/main/cpp/NapiTest.cpp`

## 通用测试规则总结

### 1. 参数验证规则

#### 1.1 参数类型检查

- **规则**：验证参数类型是否正确
- **实现**：使用 `napi_typeof` 检查参数类型
- **测试场景**：
  - 期望字符串类型：传入其他类型（number、boolean、object、null）
  - 期望空指针：传入有效字符串
  - 期望字符串或null：传入其他类型

**代码示例**：
```c
napi_valuetype valuetype;
napi_status status = napi_typeof(env, args[0], &valuetype);

if (valuetype == napi_null) {
    // 处理空指针
} else if (valuetype == napi_string) {
    // 处理字符串
} else {
    // 抛出类型错误
    napi_throw_error(env, nullptr, "Argument must be string or null");
}
```

#### 1.2 字符串参数验证

- **规则**：验证字符串参数的有效性
- **测试场景**：
  - 空字符串
  - 正常字符串
  - 超长字符串
  - 特殊字符

**代码示例**：
```c
char fileType[256] = {0};
size_t strLen;
napi_status status = napi_get_value_string_utf8(env, args[0], fileType, sizeof(fileType) - 1, &strLen);

if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Failed to get fileType string");
    return nullptr;
}
```

#### 1.3 空指针参数测试

- **规则**：验证函数对空指针参数的处理
- **测试场景**：
  - 主要参数为空指针
  - 输出参数为空指针

**代码示例**：
```c
// 测试空指针
ret = OH_NativeBundle_GetBundleName(nullptr, &bundleName);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID);
```

### 2. 错误码测试规则

#### 2.1 通用错误码定义

```c
const int ERRORCODE = 401;  // 通用错误码，用于参数无效等错误
```

**常见错误码**：
- `BUNDLE_MANAGER_ERROR_CODE_NO_ERROR = 0` - 无错误，操作成功
- `BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID = 401` - 参数无效
- `BUNDLE_MANAGER_ERROR_CODE_PERMISSION_DENIED = 201` - 权限拒绝

#### 2.2 错误码验证模式

- **规则**：验证返回的错误码是否符合预期
- **测试场景**：
  - 成功情况：返回 0
  - 参数无效：返回 401
  - 权限拒绝：返回 201
  - 其他错误：返回相应错误码

**代码示例**：
```c
napi_value result;
if (ret == BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID) {
    napi_create_int32(env, ERRORCODE, &result);
} else if (ret == BUNDLE_MANAGER_ERROR_CODE_NO_ERROR) {
    napi_create_int32(env, 0, &result);
} else {
    napi_create_int32(env, ret, &result);
}
```

#### 2.3 错误码测试优先级

1. **高优先级**：参数无效（401）
   - 空指针
   - 错误类型
   - 无效参数值

2. **中优先级**：权限拒绝（201）
   - 权限不足
   - 权限被拒绝

3. **低优先级**：其他错误
   - 其他系统错误
   - 未知错误

### 3. 返回值验证规则

#### 3.1 指针返回值验证

- **规则**：验证返回的指针是否有效
- **测试场景**：
  - 正常情况：返回有效指针
  - 错误情况：返回 nullptr
  - 内存不足：返回 nullptr

**代码示例**：
```c
char* appId = OH_NativeBundle_GetAppId();
ASSERT_NE(appId, nullptr);  // 验证非空

free(appId);  // 释放内存
```

#### 3.2 结构体返回值验证

- **规则**：验证返回的结构体成员是否有效
- **测试场景**：
  - 结构体指针非空
  - 结构体成员有效
  - 结构体成员符合预期

**代码示例**：
```c
OH_NativeBundle_ApplicationInfo* appInfo = OH_NativeBundle_GetCurrentApplicationInfo();
ASSERT_NE(appInfo, nullptr);  // 验证结构体指针非空
EXPECT_NE(appInfo->bundleName, nullptr);  // 验证成员
EXPECT_NE(appInfo->fingerprint, nullptr);
```

#### 3.3 整数返回值验证

- **规则**：验证返回的数值是否在预期范围内
- **测试场景**：
  - 成功：返回 0
  - 数量检查：返回正数
  - 索引检查：返回非负数

**代码示例**：
```c
int size = OH_NativeBundle_GetSize();
EXPECT_GT(size, 0);  // 验证大于0
```

### 4. 内存管理规则

#### 4.1 字符串释放规则

- **规则**：所有返回的字符串必须手动释放
- **测试场景**：
  - 返回的字符串非空
  - 释放后不应有内存泄漏
  - 释放空指针应该是安全的

**代码示例**：
```c
char* bundleName = nullptr;
OH_NativeBundle_GetBundleName(resourceInfo, &bundleName);

if (bundleName) {
    free(bundleName);  // 释放内存
    bundleName = nullptr;  // 避免悬空指针
}
```

#### 4.2 资源销毁规则

- **规则**：使用专用的销毁函数释放资源
- **测试场景**：
  - 正常销毁：使用正确的 count
  - 空指针：应返回参数无效错误
  - 重复销毁：检查安全性

**代码示例**：
```c
// 获取资源
OH_NativeBundle_AbilityResourceInfo* resourceInfo = nullptr;
size_t moduleCount = 0;
OH_NativeBundle_GetAbilityResourceInfo("test", &resourceInfo, &moduleCount);

// 销毁资源
BundleManager_ErrorCode ret = OH_AbilityResourceInfo_Destroy(resourceInfo, moduleCount);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_NO_ERROR);

// 测试空指针
ret = OH_AbilityResourceInfo_Destroy(nullptr, 0);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID);
```

#### 4.3 结构体释放规则

- **规则**：先释放结构体成员，再释放结构体指针
- **测试场景**：
  - 成功释放：所有成员都已释放
  - 内存泄漏检查：使用 valgrind 或 ASan
- **顺序**：字符串指针 → 其他指针 → 结构体指针

**代码示例**：
```c
OH_NativeBundle_ApplicationInfo* appInfo = OH_NativeBundle_GetCurrentApplicationInfo();

if (appInfo) {
    if (appInfo->bundleName) {
        free(appInfo->bundleName);
        appInfo->bundleName = nullptr;
    }
    if (appInfo->fingerprint) {
        free(appInfo->fingerprint);
        appInfo->fingerprint = nullptr;
    }
    free(appInfo);
}
```

### 5. 边界值测试规则

#### 5.1 字符串长度边界

- **规则**：测试字符串的最大长度限制
- **测试场景**：
  - 空字符串
  - 单字符字符串
  - 最大长度字符串
  - 超长字符串

**代码示例**：
```c
// 测试空字符串
char emptyStr[1] = {0};
ret = OH_NativeBundle_GetAbilityResourceInfo(emptyStr, &resourceInfo, &moduleCount);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_NO_ERROR);

// 测试超长字符串
char longStr[1000];
memset(longStr, 'a', sizeof(longStr) - 1);
ret = OH_NativeBundle_GetAbilityResourceInfo(longStr, &resourceInfo, &moduleCount);
// 验证行为
```

#### 5.2 数值边界

- **规则**：测试数值的最小值和最大值
- **测试场景**：
  - 零值（如适用）
  - INT_MIN
  - INT_MAX
  - 特殊值（-1）

**代码示例**：
```c
// 测试正常值
int appIndex = -1;
ret = OH_NativeBundle_GetAppIndex(resourceInfo, &appIndex);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_NO_ERROR);
EXPECT_GE(appIndex, 0);  // 验证索引非负

// 测试无效索引
ret = OH_NativeBundle_GetAppIndex(resourceInfo, &appIndex);
// 验证错误码
```

#### 5.3 特殊值测试

- **规则**：测试特殊值和异常值
- **测试场景**：
  - 空值
  - 负数（如适用）
  - 特殊字符
  - Unicode 字符

**代码示例**：
```c
// 测试特殊字符
char specialCharStr[] = "test@#$%";
ret = OH_NativeBundle_GetAbilityResourceInfo(specialCharStr, &resourceInfo, &moduleCount);
// 验证结果
```

### 6. 并发和线程安全规则

#### 6.1 线程安全考虑

- **规则**：验证函数在多线程环境下的行为
- **测试场景**：
  - 多线程同时调用
  - 共享资源的并发访问
  - 竞态条件

**代码示例**：
```c
// 使用互斥锁保护共享资源
pthread_mutex_t mutex;
pthread_mutex_init(&mutex, nullptr);

// 在测试中测试并发
void* thread_func(void* arg) {
    pthread_mutex_lock(&mutex);
    // 访问共享资源
    pthread_mutex_unlock(&mutex);
    return nullptr;
}
```

### 7. 性能测试规则

#### 7.1 性能基准测试

- **规则**：测量函数的执行时间
- **测试场景**：
  - 单次调用性能
  - 批量调用性能
  - 大数据量性能

**代码示例**：
```c
#include <time.h>

struct timespec start, end;
clock_gettime(CLOCK_MONOTONIC, &start);

for (int i = 0; i < 1000; i++) {
    OH_NativeBundle_GetAppId();
}

clock_gettime(CLOCK_MONOTONIC, &end);
long elapsed = (end.tv_sec - start.tv_sec) * 1000000000L + 
                  (end.tv_nsec - start.tv_nsec);

EXPECT_LT(elapsed, 100000000);  // 小于100ms
```

### 8. 集成测试规则

#### 8.1 API 序列调用测试

- **规则**：验证多个 API 按顺序调用的正确性
- **测试场景**：
  - 获取信息 → 使用信息 → 销毁信息
  - API 依赖关系
  - 前置条件验证

**代码示例**：
```c
// 序列调用测试
OH_NativeBundle_AbilityResourceInfo* resourceInfo = nullptr;
size_t moduleCount = 0;
BundleManager_ErrorCode ret = OH_NativeBundle_GetAbilityResourceInfo("test", &resourceInfo, &moduleCount);
ASSERT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_NO_ERROR);

char* bundleName = nullptr;
ret = OH_NativeBundle_GetBundleName(resourceInfo, &bundleName);
ASSERT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_NO_ERROR);
ASSERT_NE(bundleName, nullptr);

free(bundleName);
OH_AbilityResourceInfo_Destroy(resourceInfo, moduleCount);
```

---

**版本**: 1.0.0
**基于测试用例文件**: NapiTest.cpp
**提取日期**: 2026-03-06
