# CAPI 测试模式参考

> 从历史测试用例中提取的测试模式，补充 `_common.md` 未覆盖的具体场景和代码示例。
> `_common.md` 已包含：编号规范、N-API 封装函数规范、断言方法、代码风格、质量标准。

## 一、参数验证模式

### 1.1 参数类型检查

测试 API 对不同参数类型的处理：

| 测试场景 | 期望类型 | 传入类型 | 预期行为 |
|----------|---------|---------|---------|
| 正常类型 | string | string | 正常处理 |
| 类型不匹配 | string | number | `napi_throw_error` |
| 类型不匹配 | string | boolean | `napi_throw_error` |
| null 处理 | string 或 null | null | 走 null 分支 |
| 非法类型 | string | object | `napi_throw_error` |

```c
napi_valuetype valuetype;
napi_status status = napi_typeof(env, args[0], &valuetype);

if (valuetype == napi_null) {
    // 处理空指针
} else if (valuetype == napi_string) {
    // 处理字符串
} else {
    napi_throw_error(env, nullptr, "Argument must be string or null");
}
```

### 1.2 空指针参数测试

```c
// C API 侧空指针测试
ret = OH_NativeBundle_GetBundleName(nullptr, &bundleName);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID);

// 对应的 N-API 封装：ETS 侧传 null，N-API 层检测 napi_null 后传入 nullptr
```

### 1.3 字符串参数验证

| 测试场景 | 输入 | 预期 |
|----------|------|------|
| 空字符串 | `""` | 按 API 语义返回 |
| 正常字符串 | `"valid"` | 正常处理 |
| 超长字符串 | 256+ 字符 | 截断或返回错误 |
| 特殊字符 | `"test@#$%"` | 按 API 语义处理 |

## 二、错误码测试模式

### 2.1 错误码优先级

| 优先级 | 错误码 | 触发条件 | 测试策略 |
|--------|--------|---------|---------|
| 高 | 参数无效（401） | 空指针、错误类型、无效值 | 每个参数维度的无效场景 |
| 中 | 权限拒绝（201） | 权限不足、权限被拒 | 模拟无权限场景 |
| 低 | 系统错误 | 内部错误、未知错误 | 验证返回值非零即可 |

### 2.2 N-API 层错误码映射

```c
napi_value result;
if (ret == ERROR_CODE_PARAM_INVALID) {
    napi_throw_error(env, "401", "Parameter invalid");
    return nullptr;
} else if (ret == ERROR_CODE_NO_ERROR) {
    napi_create_int32(env, 0, &result);
} else {
    napi_create_int32(env, ret, &result);
}
return result;
```

## 三、返回值验证模式

### 3.1 指针返回值

```c
char* appId = OH_NativeBundle_GetAppId();
ASSERT_NE(appId, nullptr);
free(appId);  // 必须释放
```

### 3.2 结构体返回值

```c
OH_NativeBundle_ApplicationInfo* appInfo = OH_NativeBundle_GetCurrentApplicationInfo();
ASSERT_NE(appInfo, nullptr);
EXPECT_NE(appInfo->bundleName, nullptr);
EXPECT_NE(appInfo->fingerprint, nullptr);
```

### 3.3 整数返回值

```c
int size = OH_NativeBundle_GetSize();
EXPECT_GT(size, 0);  // 正数表示成功
```

## 四、内存管理测试模式

### 4.1 字符串释放

```c
char* bundleName = nullptr;
OH_NativeBundle_GetBundleName(resourceInfo, &bundleName);
if (bundleName) {
    free(bundleName);
    bundleName = nullptr;
}
```

### 4.2 资源销毁（配对操作）

```c
OH_NativeBundle_AbilityResourceInfo* resourceInfo = nullptr;
size_t moduleCount = 0;
OH_NativeBundle_GetAbilityResourceInfo("test", &resourceInfo, &moduleCount);

BundleManager_ErrorCode ret = OH_AbilityResourceInfo_Destroy(resourceInfo, moduleCount);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_NO_ERROR);

ret = OH_AbilityResourceInfo_Destroy(nullptr, 0);
EXPECT_EQ(ret, BUNDLE_MANAGER_ERROR_CODE_PARAM_INVALID);
```

### 4.3 结构体释放顺序

**释放顺序：字符串成员 → 其他指针成员 → 结构体本身**

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

## 五、边界值测试模式

### 5.1 字符串长度边界

| 场景 | 输入 | 关注点 |
|------|------|--------|
| 空字符串 | `""` | API 是否接受 |
| 单字符 | `"a"` | 最短有效输入 |
| 最大长度 | N-1 字符 | 缓冲区边界 |
| 超长 | N+1 字符 | 截断或报错 |

### 5.2 数值边界

| 场景 | 输入 | 关注点 |
|------|------|--------|
| 零值 | `0` | 特殊语义 |
| INT_MIN | `-2147483648` | 下溢 |
| INT_MAX | `2147483647` | 上溢 |
| -1 | `-1` | 常见错误码值 |

## 六、集成测试模式：API 序列调用

配对操作必须在一个测试用例内完成（create → use → destroy），不跨用例共享资源：

```c
// 序列调用：获取 → 使用 → 销毁
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
**来源**: 从历史测试用例 NapiTest.cpp 中提取
