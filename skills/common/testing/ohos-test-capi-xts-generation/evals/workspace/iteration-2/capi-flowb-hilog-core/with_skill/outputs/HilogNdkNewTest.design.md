# HilogNdkNewTest 测试设计文档

## 目标 API

1. **OH_LOG_Print** - `int OH_LOG_Print(LogType type, LogLevel level, unsigned int domain, const char *tag, const char *fmt, ...)`
2. **OH_LOG_IsLoggable** - `bool OH_LOG_IsLoggable(unsigned int domain, const char *tag, LogLevel level)`
3. **OH_LOG_SetMinLogLevel** - `void OH_LOG_SetMinLogLevel(LogLevel level)`

## 枚举定义

| 枚举 | 值 |
|------|-----|
| LOG_APP | 0 |
| LOG_DEBUG | 3 |
| LOG_INFO | 4 |
| LOG_WARN | 5 |
| LOG_ERROR | 6 |
| LOG_FATAL | 7 |

---

## 接口 1: OH_LOG_Print

### 基本信息
- **头文件**: `hilog/log.h`
- **函数签名**: `int OH_LOG_Print(LogType type, LogLevel level, unsigned int domain, const char *tag, const char *fmt, ...)`
- **返回值**: >= 0 表示成功，< 0 表示失败
- **注意**: 变参函数，N-API 封装中使用固定参数调用

### 测试用例 1: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001 |
| 用例名 | OH_LOG_Print 正常参数 LOG_INFO 级别 |
| N-API 函数名 | OHLogPrintInfoLevel |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintInfoLevel(0, 4, 0x3200, "testTag", "test info message")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 2: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002 |
| 用例名 | OH_LOG_Print 正常参数 LOG_DEBUG 级别 |
| N-API 函数名 | OHLogPrintDebugLevel |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintDebugLevel(0, 3, 0x3200, "testTag", "test debug message")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 3: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_003

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_003 |
| 用例名 | OH_LOG_Print 正常参数 LOG_WARN 级别 |
| N-API 函数名 | OHLogPrintWarnLevel |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintWarnLevel(0, 5, 0x3200, "testTag", "test warn message")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 4: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_004

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_004 |
| 用例名 | OH_LOG_Print 正常参数 LOG_FATAL 级别 |
| N-API 函数名 | OHLogPrintFatalLevel |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintFatalLevel(0, 7, 0x3200, "testTag", "test fatal message")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 5: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_005

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_005 |
| 用例名 | OH_LOG_Print domain 为 0 |
| N-API 函数名 | OHLogPrintDomainZero |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintDomainZero(0, 4, 0, "testTag", "domain zero message")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 6: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_006

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_006 |
| 用例名 | OH_LOG_Print domain 为 0xFFFF |
| N-API 函数名 | OHLogPrintDomainMax |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintDomainMax(0, 4, 0xFFFF, "testTag", "domain max message")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 7: SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001 |
| 用例名 | OH_LOG_Print 返回值验证 |
| N-API 函数名 | OHLogPrintReturnTest |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogPrintReturnTest(0, 6, 0x3200, "testTag", "return test")\n2. 获取返回值 result |
| 预期结果 | result 为 int 类型且 result >= 0 |
| 场景 | 正常场景 |
| 类型 | RETURN |
| 级别 | P1 |
| 依赖关系 | 无 |

---

## 接口 2: OH_LOG_IsLoggable

### 基本信息
- **头文件**: `hilog/log.h`
- **函数签名**: `bool OH_LOG_IsLoggable(unsigned int domain, const char *tag, LogLevel level)`
- **返回值**: true 表示可输出，false 表示不可输出

### 测试用例 8: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001 |
| 用例名 | OH_LOG_IsLoggable 正常参数 LOG_DEBUG 级别 |
| N-API 函数名 | OHLogIsLoggableDebug |
| 预置条件 | 日志级别未被设置过高 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableDebug(0x3200, "testTag", 3)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 9: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002 |
| 用例名 | OH_LOG_IsLoggable LOG_INFO 级别 |
| N-API 函数名 | OHLogIsLoggableInfo |
| 预置条件 | 日志级别未被设置过高 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableInfo(0x3200, "testTag", 4)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 10: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_003

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_003 |
| 用例名 | OH_LOG_IsLoggable LOG_WARN 级别 |
| N-API 函数名 | OHLogIsLoggableWarn |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableWarn(0x3200, "testTag", 5)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 11: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_004

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_004 |
| 用例名 | OH_LOG_IsLoggable LOG_ERROR 级别 |
| N-API 函数名 | OHLogIsLoggableError |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableError(0x3200, "testTag", 6)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 12: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_005

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_005 |
| 用例名 | OH_LOG_IsLoggable LOG_FATAL 级别 |
| N-API 函数名 | OHLogIsLoggableFatal |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableFatal(0x3200, "testTag", 7)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 13: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_006

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_006 |
| 用例名 | OH_LOG_IsLoggable 无效日志级别 |
| N-API 函数名 | OHLogIsLoggableInvalidLevel |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableInvalidLevel(0x3200, "testTag", 100)\n2. 获取返回值 result |
| 预期结果 | result 为 false |
| 场景 | 异常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 14: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_007

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_007 |
| 用例名 | OH_LOG_IsLoggable domain 为 0 |
| N-API 函数名 | OHLogIsLoggableDomainZero |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableDomainZero(0, "testTag", 4)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 15: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_008

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_008 |
| 用例名 | OH_LOG_IsLoggable domain 为 0xFFFF |
| N-API 函数名 | OHLogIsLoggableDomainMax |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableDomainMax(0xFFFF, "testTag", 4)\n2. 获取返回值 result |
| 预期结果 | result 为 true |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 16: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_001 |
| 用例名 | OH_LOG_IsLoggable 返回 true |
| N-API 函数名 | OHLogIsLoggableReturnTrue |
| 预置条件 | 日志级别为默认 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableReturnTrue(0x3200, "testTag", 6)\n2. 获取返回值 result |
| 预期结果 | result 为 boolean 类型且为 true |
| 场景 | 正常场景 |
| 类型 | RETURN |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 17: SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_002 |
| 用例名 | OH_LOG_IsLoggable 返回 false (超出范围 domain) |
| N-API 函数名 | OHLogIsLoggableReturnFalse |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogIsLoggableReturnFalse(0x32000, "testTag", 4)\n2. 获取返回值 result |
| 预期结果 | result 为 boolean 类型且为 false |
| 场景 | 异常场景 |
| 类型 | RETURN |
| 级别 | P1 |
| 依赖关系 | 无 |

---

## 接口 3: OH_LOG_SetMinLogLevel

### 基本信息
- **头文件**: `hilog/log.h`
- **函数签名**: `void OH_LOG_SetMinLogLevel(LogLevel level)`
- **返回值**: void

### 测试用例 18: SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001 |
| 用例名 | OH_LOG_SetMinLogLevel 设置 LOG_INFO 后过滤 DEBUG |
| N-API 函数名 | OHLogSetMinLogLevelInfo |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogSetMinLogLevelInfo()\n2. 内部: OH_LOG_SetMinLogLevel(LOG_INFO)\n3. 内部: 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG) 返回 false\n4. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO) 返回 true |
| 预期结果 | 返回 0 表示 DEBUG 被过滤，INFO 通过 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 19: SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002 |
| 用例名 | OH_LOG_SetMinLogLevel 设置 LOG_WARN 后过滤 INFO |
| N-API 函数名 | OHLogSetMinLogLevelWarn |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogSetMinLogLevelWarn()\n2. 内部: OH_LOG_SetMinLogLevel(LOG_WARN)\n3. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO) 返回 false\n4. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN) 返回 true |
| 预期结果 | 返回 0 表示 INFO 被过滤，WARN 通过 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 20: SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_003

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_003 |
| 用例名 | OH_LOG_SetMinLogLevel 设置 LOG_ERROR 后过滤 WARN |
| N-API 函数名 | OHLogSetMinLogLevelError |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogSetMinLogLevelError()\n2. 内部: OH_LOG_SetMinLogLevel(LOG_ERROR)\n3. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN) 返回 false\n4. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR) 返回 true |
| 预期结果 | 返回 0 表示 WARN 被过滤，ERROR 通过 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 21: SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_004

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_004 |
| 用例名 | OH_LOG_SetMinLogLevel 设置 LOG_FATAL 后过滤 ERROR |
| N-API 函数名 | OHLogSetMinLogLevelFatal |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogSetMinLogLevelFatal()\n2. 内部: OH_LOG_SetMinLogLevel(LOG_FATAL)\n3. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR) 返回 false\n4. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_FATAL) 返回 true |
| 预期结果 | 返回 0 表示 ERROR 被过滤，FATAL 通过 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 22: SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_005

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_005 |
| 用例名 | OH_LOG_SetMinLogLevel 设置 LOG_DEBUG 所有级别通过 |
| N-API 函数名 | OHLogSetMinLogLevelDebug |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.OHLogSetMinLogLevelDebug()\n2. 内部: OH_LOG_SetMinLogLevel(LOG_DEBUG)\n3. 检查 OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG) 返回 true |
| 预期结果 | 返回 0 表示所有级别均通过 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

---

## N-API 函数名映射表

| 用例编号 | N-API 函数名 (JS 侧) | C++ 实现函数 |
|---------|---------------------|-------------|
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001 | OHLogPrintInfoLevel | OHLogPrintInfoLevel_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002 | OHLogPrintDebugLevel | OHLogPrintDebugLevel_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_003 | OHLogPrintWarnLevel | OHLogPrintWarnLevel_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_004 | OHLogPrintFatalLevel | OHLogPrintFatalLevel_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_005 | OHLogPrintDomainZero | OHLogPrintDomainZero_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_006 | OHLogPrintDomainMax | OHLogPrintDomainMax_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001 | OHLogPrintReturnTest | OHLogPrintReturnTest_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001 | OHLogIsLoggableDebug | OHLogIsLoggableDebug_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002 | OHLogIsLoggableInfo | OHLogIsLoggableInfo_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_003 | OHLogIsLoggableWarn | OHLogIsLoggableWarn_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_004 | OHLogIsLoggableError | OHLogIsLoggableError_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_005 | OHLogIsLoggableFatal | OHLogIsLoggableFatal_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_006 | OHLogIsLoggableInvalidLevel | OHLogIsLoggableInvalidLevel_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_007 | OHLogIsLoggableDomainZero | OHLogIsLoggableDomainZero_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_008 | OHLogIsLoggableDomainMax | OHLogIsLoggableDomainMax_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_001 | OHLogIsLoggableReturnTrue | OHLogIsLoggableReturnTrue_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_002 | OHLogIsLoggableReturnFalse | OHLogIsLoggableReturnFalse_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001 | OHLogSetMinLogLevelInfo | OHLogSetMinLogLevelInfo_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002 | OHLogSetMinLogLevelWarn | OHLogSetMinLogLevelWarn_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_003 | OHLogSetMinLogLevelError | OHLogSetMinLogLevelError_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_004 | OHLogSetMinLogLevelFatal | OHLogSetMinLogLevelFatal_napi |
| SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_005 | OHLogSetMinLogLevelDebug | OHLogSetMinLogLevelDebug_napi |

## 覆盖率统计

| API | PARAM | ERROR | RETURN | BOUNDARY | 合计 |
|-----|-------|-------|--------|----------|------|
| OH_LOG_Print | 6 | 0 | 1 | 0 | 7 |
| OH_LOG_IsLoggable | 8 | 0 | 2 | 0 | 10 |
| OH_LOG_SetMinLogLevel | 5 | 0 | 0 | 0 | 5 |
| **合计** | **19** | **0** | **3** | **0** | **22** |
