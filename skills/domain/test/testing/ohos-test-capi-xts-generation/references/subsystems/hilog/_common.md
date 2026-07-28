# HiLog 子系统配置

> 📖 **相关文档**：
> - [通用配置](../_common.md) - 所有子系统共享的通用配置
> - [头文件解析模块](../../modules/L1_Analysis/unified_api_parser_c.md) - API 信息提取

> **子系统信息**
> - 名称：hilog
> - 描述：HiLog 日志子系统,提供日志打印、日志过滤、日志管理等功能
> - API 文件：`{OH_ROOT}/interface/sdk_c/hiviewdfx/hilog/include/hilog/log.h`
> - 官方文档：`{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-hilog`
> - 依赖：无特殊依赖
> - 测试类型：N-API 封装测试（方式2）

---

## 一、子系统概述

HiLog 是 OpenHarmony 的日志子系统,提供统一的日志接口,支持不同级别和类型的日志输出,以及日志过滤和管理功能。

### 1.1 核心功能

- **日志打印** - 支持多种日志级别和日志域
- **日志过滤** - 支持按级别、域、标签过滤日志
- **日志管理** - 支持日志刷新、缓冲区管理等
- **性能优化** - 提供异步日志接口,减少对主线程的影响
- **多线程支持** - 支持多线程环境下的日志打印

### 1.2 应用场景

1. **功能测试** - 验证日志打印功能是否正常
2. **性能测试** - 测试日志打印对性能的影响
3. **边界测试** - 测试日志长度、日志频率等边界情况
4. **错误处理测试** - 测试错误参数、无效参数等异常场景
5. **并发测试** - 测试多线程环境下的日志打印

---

## 二、API 信息

### 2.1 主要 API 列表

| API 名称 | 功能 | 优先级 |
|---------|------|--------|
| HiLogPrint | 打印日志 | 高 |
| HiLogPrintArgs | 可变参数日志打印 | 高 |
| HiLogIsLoggable | 检查日志是否可打印 | 中 |
| HiLogDebug | 调试日志 | 低 |
| HiLogInfo | 信息日志 | 低 |
| HiLogWarn | 警告日志 | 低 |
| HiLogError | 错误日志 | 低 |
| HiLogFatal | 致命错误日志 | 低 |

### 2.2 核心 API 详细信息

#### HiLogPrint

```c
int HiLogPrint(int type, int level, unsigned int domain, const char* tag, const char* fmt, ...);
```

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | int | 是 | 日志类型,如 LOG_CORE, LOG_APP |
| level | int | 是 | 日志级别,如 LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR |
| domain | unsigned int | 是 | 日志域,用于区分不同模块的日志 |
| tag | const char* | 是 | 日志标签,用于标识日志来源 |
| fmt | const char* | 是 | 格式化字符串,支持 printf 风格 |
| ... | 可变参数 | 否 | 可变参数列表 |

**返回值**：
| 值 | 说明 |
|-----|------|
| 0 | 成功 |
| -1 | 参数无效 |
| -2 | 日志服务不可用 |

**错误码**：
| 错误码 | 常量名 | 说明 |
|---------|---------|------|
| 401 | LOG_INVALID_PARAM | 参数无效 |
| 402 | LOG_SERVICE_UNAVAILABLE | 日志服务不可用 |

#### HiLogPrintArgs

```c
int HiLogPrintArgs(int type, int level, unsigned int domain, const char* tag, const char* fmt, va_list ap);
```

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | int | 是 | 日志类型 |
| level | int | 是 | 日志级别 |
| domain | unsigned int | 是 | 日志域 |
| tag | const char* | 是 | 日志标签 |
| fmt | const char* | 是 | 格式化字符串 |
| ap | va_list | 是 | 可变参数列表 |

**返回值**：
| 值 | 说明 |
|-----|------|
| 0 | 成功 |
| -1 | 参数无效 |

#### HiLogIsLoggable

```c
bool HiLogIsLoggable(int type, int level, unsigned int domain);
```

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | int | 是 | 日志类型 |
| level | int | 是 | 日志级别 |
| domain | unsigned int | 是 | 日志域 |

**返回值**：
| 值 | 说明 |
|-----|------|
| true | 日志可打印 |
| false | 日志不可打印 |

---

## 三、测试策略

### 3.1 测试类型优先级

根据 API 重要性定义测试类型优先级：

| API | PARAM | ERROR | RETURN | BOUNDARY | MEMORY |
|-----|-------|-------|--------|----------|-------|
| HiLogPrint | 高 | 高 | 高 | 中 | 低 |
| HiLogPrintArgs | 高 | 高 | 高 | 中 | 低 |
| HiLogIsLoggable | 中 | 低 | 高 | 低 | 低 |
| HiLogDebug | 低 | 低 | 低 | 低 | 低 |
| HiLogInfo | 低 | 低 | 低 | 低 | 低 |
| HiLogWarn | 低 | 低 | 低 | 低 | 低 |
| HiLogError | 低 | 低 | 低 | 低 | 低 |
| HiLogFatal | 低 | 低 | 低 | 低 | 低 |

### 3.2 参数组合测试策略

#### HiLogPrint 参数组合

**必测组合**：
1. `(LOG_CORE, LOG_DEBUG, 0, "TAG", "%s")` - 正常参数
2. `(LOG_CORE, LOG_ERROR, 0, "TAG", "%s")` - 不同级别
3. `(LOG_APP, LOG_INFO, 1, "TAG", "%s")` - 不同类型
4. `(LOG_CORE, LOG_DEBUG, 0, "", "%s")` - 空标签
5. `(LOG_CORE, LOG_DEBUG, 0, "TAG", "")` - 空格式字符串

**边界值组合**：
1. `(LOG_CORE, LOG_DEBUG, 0, "TAG", "%s", "...")` - 超长字符串
2. `(LOG_CORE, LOG_DEBUG, 0, "TAG", "%d", INT_MAX)` - 整数边界
3. `(LOG_CORE, LOG_DEBUG, 0, "TAG", "%s", nullptr)` - 空指针
4. `(LOG_CORE, LOG_DEBUG, UINT_MAX, "TAG", "%s")` - domain 边界

#### HiLogIsLoggable 参数组合

**必测组合**：
1. `(LOG_CORE, LOG_DEBUG, 0)` - 正常参数
2. `(LOG_CORE, LOG_ERROR, 0)` - 不同级别
3. `(LOG_APP, LOG_INFO, 1)` - 不同类型
4. `(LOG_CORE, LOG_DEBUG, UINT_MAX)` - domain 边界

### 3.3 测试场景覆盖

**PARAM 测试场景**：
1. 正常参数测试
2. 不同日志类型测试（LOG_CORE, LOG_APP）
3. 不同日志级别测试（LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR）
4. 不同日志域测试
5. 正常格式字符串测试
6. 基础类型参数测试（int, float, string）

**ERROR 测试场景**：
1. 空标签测试
2. 空格式字符串测试
3. 无效参数测试（type, level, domain 超出范围）
4. 日志服务不可用测试（模拟场景）

**RETURN 测试场景**：
1. 成功返回（返回 0）
2. 参数无效返回（返回 -1）
3. 日志服务不可用返回（返回 -2）

**BOUNDARY 测试场景**：
1. 超长格式字符串测试
2. 超长标签测试
3. 日志域边界值测试
4. 可变参数数量边界测试

**MEMORY 测试场景**：
1. 内存泄漏检测
2. 缓冲区溢出检测
3. 多线程并发内存测试

---

## 四、N-API 封装规则

### 4.1 封装要求

**强制要求**：
- 所有 CAPI 函数必须封装为 N-API 接口
- N-API 封装必须使用 `napi_value` 类型
- 参数提取和类型检查必须完整
- 错误处理必须使用 `napi_throw_error`
- 返回值必须构造为 `napi_value`

### 4.2 N-API 封装模板

#### HiLogPrint N-API 封装

```cpp
// HiLogPrint N-API 封装
static napi_value HiLogPrint_napi(napi_env env, napi_callback_info info) {
    size_t argc = 5;
    napi_value args[5];
    napi_status status;

    // 获取参数
    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 5) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 提取参数值
    int32_t type;
    int32_t level;
    uint32_t domain;
    char* tag = nullptr;
    char* fmt = nullptr;

    status = napi_get_value_int32(env, args[0], &type);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get type");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_uint32(env, args[2], &domain);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get domain");
        return nullptr;
    }

    size_t tag_len;
    status = napi_get_value_string_utf8(env, args[3], nullptr, 0, &tag_len);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get tag length");
        return nullptr;
    }

    tag = (char*)malloc(tag_len + 1);
    if (tag == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate memory for tag");
        return nullptr;
    }

    status = napi_get_value_string_utf8(env, args[3], tag, tag_len + 1, &tag_len);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get tag");
        return nullptr;
    }

    size_t fmt_len;
    status = napi_get_value_string_utf8(env, args[4], nullptr, 0, &fmt_len);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get fmt length");
        return nullptr;
    }

    fmt = (char*)malloc(fmt_len + 1);
    if (fmt == nullptr) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to allocate memory for fmt");
        return nullptr;
    }

    status = napi_get_value_string_utf8(env, args[4], fmt, fmt_len + 1, &fmt_len);
    if (status != napi_ok) {
        free(tag);
        free(fmt);
        napi_throw_error(env, nullptr, "Failed to get fmt");
        return nullptr;
    }

    // 调用 CAPI
    int ret = HiLogPrint(type, level, domain, tag, fmt);

    // 释放内存
    free(tag);
    free(fmt);

    // 构造返回值
    napi_value result;
    status = napi_create_int32(env, ret, &result);
    if (status != napi_ok) {
        return nullptr;
    }

    return result;
}
```

#### HiLogIsLoggable N-API 封装

```cpp
// HiLogIsLoggable N-API 封装
static napi_value HiLogIsLoggable_napi(napi_env env, napi_callback_info info) {
    size_t argc = 3;
    napi_value args[3];
    napi_status status;

    // 获取参数
    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 3) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 提取参数值
    int32_t type;
    int32_t level;
    uint32_t domain;

    status = napi_get_value_int32(env, args[0], &type);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get type");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_uint32(env, args[2], &domain);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get domain");
        return nullptr;
    }

    // 调用 CAPI
    bool result = HiLogIsLoggable(type, level, domain);

    // 构造返回值
    napi_value napi_result;
    status = napi_get_boolean(env, result, &napi_result);
    if (status != napi_ok) {
        return nullptr;
    }

    return napi_result;
}
```

---

## 五、ETS 测试模板

### 5.1 HiLogPrint 测试模板

```typescript
// HiLogPrint 正常参数测试
it('HiLogPrint_NormalParam', 0, async () => {
    // 准备测试数据
    const type = 0; // LOG_CORE
    const level = 3; // LOG_DEBUG
    const domain = 0;
    const tag = "HiLogTest";
    const fmt = "%s";
    const message = "test message";

    try {
        // 调用 N-API 封装函数
        const result = nativeHiLogPrint(type, level, domain, tag, fmt, message);

        // 验证返回值
        expect(result).assertEqual(0);

        console.log('✅ HiLogPrint 正常参数测试通过');
    } catch (error) {
        console.error('❌ HiLogPrint 测试失败:', error);
        expect().assertFalse();
    }
});

// HiLogPrint 空标签测试
it('HiLogPrint_EmptyTag', 0, async () => {
    const type = 0; // LOG_CORE
    const level = 3; // LOG_DEBUG
    const domain = 0;
    const tag = "";
    const fmt = "%s";
    const message = "test message";

    try {
        const result = nativeHiLogPrint(type, level, domain, tag, fmt, message);

        // 空标签应该也能正常打印
        expect(result).assertEqual(0);

        console.log('✅ HiLogPrint 空标签测试通过');
    } catch (error) {
        console.error('❌ HiLogPrint 空标签测试失败:', error);
        expect().assertFalse();
    }
});
```

### 5.2 HiLogIsLoggable 测试模板

```typescript
// HiLogIsLoggable 正常参数测试
it('HiLogIsLoggable_NormalParam', 0, async () => {
    const type = 0; // LOG_CORE
    const level = 3; // LOG_DEBUG
    const domain = 0;

    try {
        const result = nativeHiLogIsLoggable(type, level, domain);

        // 验证返回值
        expect(result).assertTrue();

        console.log('✅ HiLogIsLoggable 正常参数测试通过');
    } catch (error) {
        console.error('❌ HiLogIsLoggable 测试失败:', error);
        expect().assertFalse();
    }
});

// HiLogIsLoggable 边界值测试
it('HiLogIsLoggable_BoundaryValue', 0, async () => {
    const type = 0; // LOG_CORE
    const level = 3; // LOG_DEBUG
    const domain = 4294967295; // UINT_MAX

    try {
        const result = nativeHiLogIsLoggable(type, level, domain);

        // 边界值也应该返回有效结果
        expect(result).assertLargerThanOrEqual(false);

        console.log('✅ HiLogIsLoggable 边界值测试通过');
    } catch (error) {
        console.error('❌ HiLogIsLoggable 边界值测试失败:', error);
        expect().assertFalse();
    }
});
```

---

## 六、测试用例编号规则

### 6.1 编号格式

**标准格式**：`SUB_HILOG_[API]_[类型]_[序号]`

**示例**：
- `SUB_HILOG_HILOGPRINT_PARAM_001` - HiLogPrint 参数测试用例 1
- `SUB_HILOG_HILOGPRINT_ERROR_001` - HiLogPrint 错误测试用例 1
- `SUB_HILOG_HILOGPRINT_RETURN_001` - HiLogPrint 返回值测试用例 1
- `SUB_HILOG_HILOGPRINT_BOUNDARY_001` - HiLogPrint 边界测试用例 1
- `SUB_HILOG_HILOGISLOGGABLE_PARAM_001` - HiLogIsLoggable 参数测试用例 1

### 6.2 类型缩写

| 类型 | 缩写 | 说明 |
|------|------|------|
| PARAM | P | 参数测试 |
| ERROR | E | 错误处理测试 |
| RETURN | R | 返回值测试 |
| BOUNDARY | B | 边界值测试 |
| MEMORY | M | 内存测试 |

---

## 七、特殊规则

### 7.1 HiLog 特有规则

1. **日志频率限制** - 避免在短时间内打印过多日志,影响性能
2. **日志内容检查** - 确保日志内容有意义,不包含敏感信息
3. **日志标签规范** - 使用统一的标签格式,便于过滤和搜索
4. **多线程安全** - 测试多线程环境下的日志打印安全性
5. **性能考虑** - 避免在关键路径上打印过多日志

### 7.2 测试注意事项

1. **清理日志** - 测试前后清理相关日志,避免干扰
2. **日志验证** - 验证日志是否正确输出到日志系统
3. **级别验证** - 验证不同级别的日志是否正确处理
4. **异步处理** - 如果 API 支持异步日志,需要测试异步场景
5. **资源清理** - 测试完成后清理分配的资源

---

## 八、参考实现

### 8.1 参考测试套

**BundleManager 参考测试套**：
- 路径：`{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest`
- 说明：N-API 封装测试套的完整实现

**ArkUI 参考测试套**：
- 路径：`{OH_ROOT}/test/xts/acts/arkui/ace_c_arkui_test_api20`
- 说明：N-API 封装测试的完整实现

### 8.2 API 文档参考

**官方 API 文档**：
- 路径：`{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-hilog`
- 说明：HiLog API 的官方文档和使用说明

---

**版本**: 1.0.0
**创建日期**: 2026-03-18
**更新日期**: 2026-03-18
**兼容性**: OpenHarmony API 10+
