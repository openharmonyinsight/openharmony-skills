# HilogCoverageTest 测试设计文档

## 接口 1: OH_LOG_PrintMsg

### 基本信息
- **头文件**: `hilog/log.h`
- **函数签名**: `int OH_LOG_PrintMsg(LogType type, LogLevel level, unsigned int domain, const char *tag, const char *message)`
- **返回值**: >= 0 表示成功，< 0 表示失败
- **@since**: 18

### 测试用例 1: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_001 |
| 用例名 | 正常参数打印日志 |
| N-API 函数名 | OH_LOG_PrintMsg_ParamTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_PrintMsg_ParamTest(0, 4, 0xFF00, "TestTag", "Hello PrintMsg")\n2. 获取返回值 result |
| 预期结果 | result >= 0（日志打印成功） |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 2: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_002 |
| 用例名 | 不同日志级别打印 |
| N-API 函数名 | OH_LOG_PrintMsg_LevelTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_PrintMsg_LevelTest(0, 3, 0xFF00, "TestTag", "debug msg") — LOG_DEBUG\n2. 调用 testNapi.OH_LOG_PrintMsg_LevelTest(0, 5, 0xFF00, "TestTag", "warn msg") — LOG_WARN\n3. 调用 testNapi.OH_LOG_PrintMsg_LevelTest(0, 7, 0xFF00, "TestTag", "fatal msg") — LOG_FATAL\n4. 验证所有调用返回值 >= 0 |
| 预期结果 | 三次调用返回值均 >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 3: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_BOUNDARY_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_BOUNDARY_001 |
| 用例名 | 空字符串消息和标签边界 |
| N-API 函数名 | OH_LOG_PrintMsg_EmptyMsgTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_PrintMsg_EmptyMsgTest(0, 4, 0xFF00, "", "")\n2. 获取返回值 result |
| 预期结果 | result 为 int 类型，函数不崩溃 |
| 场景 | 边界场景 |
| 类型 | BOUNDARY |
| 级别 | P2 |
| 依赖关系 | 无 |

---

## 接口 2: OH_LOG_PrintMsgByLen

### 基本信息
- **头文件**: `hilog/log.h`
- **函数签名**: `int OH_LOG_PrintMsgByLen(LogType type, LogLevel level, unsigned int domain, const char *tag, size_t tagLen, const char *message, size_t messageLen)`
- **返回值**: >= 0 表示成功，< 0 表示失败
- **@since**: 18

### 测试用例 4: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_PARAM_001 |
| 用例名 | 正常参数带长度打印日志 |
| N-API 函数名 | OH_LOG_PrintMsgByLen_ParamTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_PrintMsgByLen_ParamTest(0, 4, 0xFF00, "TestTag", "Hello PrintMsgByLen")\n2. 获取返回值 result |
| 预期结果 | result >= 0（日志打印成功） |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 5: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_BOUNDARY_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_BOUNDARY_001 |
| 用例名 | tagLen=0 和 messageLen=0 边界值 |
| N-API 函数名 | OH_LOG_PrintMsgByLen_BoundaryTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_PrintMsgByLen_BoundaryTest(0, 4, 0xFF00, "TestTag", 0, "Hello", 0)\n2. 获取返回值 result |
| 预期结果 | result 为 int 类型，函数不崩溃 |
| 场景 | 边界场景 |
| 类型 | BOUNDARY |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 6: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_RETURN_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_RETURN_001 |
| 用例名 | 返回值验证成功场景 |
| N-API 函数名 | OH_LOG_PrintMsgByLen_ReturnTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 使用正常参数调用 testNapi.OH_LOG_PrintMsgByLen_ReturnTest(0, 4, 0xFF00, "TestTag", 7, "TestMsg", 7)\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | RETURN |
| 级别 | P1 |
| 依赖关系 | 无 |

---

## 接口 3: OH_LOG_VPrint

### 基本信息
- **头文件**: `hilog/log.h`
- **函数签名**: `int OH_LOG_VPrint(LogType type, LogLevel level, unsigned int domain, const char *tag, const char *fmt, va_list ap)`
- **返回值**: >= 0 表示成功，< 0 表示失败
- **@since**: 18
- **注意**: va_list 参数需要通过辅助函数（variadic wrapper）间接调用

### 测试用例 7: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_001 |
| 用例名 | 正常参数可变参数日志打印 |
| N-API 函数名 | OH_LOG_VPrint_ParamTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_VPrint_ParamTest(0, 4, 0xFF00, "TestTag", "%s", "Hello VPrint")\n2. 获取返回值 result |
| 预期结果 | result >= 0（日志打印成功） |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 8: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_002 |
| 用例名 | 格式化整数参数日志打印 |
| N-API 函数名 | OH_LOG_VPrint_FmtIntTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_VPrint_FmtIntTest(0, 4, 0xFF00, "TestTag", "%d", 42)\n2. 获取返回值 result |
| 预期结果 | result >= 0（日志打印成功） |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 9: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_RETURN_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_RETURN_001 |
| 用例名 | 返回值验证 |
| N-API 函数名 | OH_LOG_VPrint_ReturnTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.OH_LOG_VPrint_ReturnTest(0, 4, 0xFF00, "TestTag", "plain text")\n2. 获取返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | RETURN |
| 级别 | P1 |
| 依赖关系 | 无 |

---

## 接口 4: PreferStrategy 枚举

### 基本信息
- **头文件**: `hilog/log.h`
- **枚举定义**: `UNSET_LOGLEVEL = 0`, `PREFER_CLOSE_LOG = 1`, `PREFER_OPEN_LOG = 2`
- **关联函数**: `void OH_LOG_SetLogLevel(LogLevel level, PreferStrategy prefer)`
- **@since**: 21

### 测试用例 10: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_001 |
| 用例名 | 遍历所有 PreferStrategy 枚举值 |
| N-API 函数名 | PreferStrategy_ParamTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.PreferStrategy_ParamTest(4, 0) — UNSET_LOGLEVEL\n2. 调用 testNapi.PreferStrategy_ParamTest(7, 1) — PREFER_CLOSE_LOG\n3. 调用 testNapi.PreferStrategy_ParamTest(3, 2) — PREFER_OPEN_LOG\n4. 每次调用后验证 OH_LOG_PrintMsg 返回值类型为 int |
| 预期结果 | 三次调用均返回 int 类型值，函数不崩溃 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 无 |

### 测试用例 11: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_002 |
| 用例名 | PREFER_CLOSE_LOG 策略后验证日志级别限制 |
| N-API 函数名 | PreferStrategy_CloseLogTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.PreferStrategy_CloseLogTest(7, 1) 设置 PREFER_CLOSE_LOG + LOG_FATAL\n2. 调用 testNapi.OH_LOG_PrintMsg_ParamTest(0, 3, 0xFF00, "TestTag", "debug after close") 尝试打印 DEBUG 级别日志\n3. 获取第二次调用返回值 result |
| 预期结果 | result 为 int 类型（可能 < 0 因为 DEBUG < FATAL，或 >= 0 取决于系统策略） |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 依赖 SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_001 |

### 测试用例 12: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_003

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_003 |
| 用例名 | PREFER_OPEN_LOG 策略后验证日志输出 |
| N-API 函数名 | PreferStrategy_OpenLogTest |
| 预置条件 | hilog 服务可用 |
| 测试步骤 | 1. 调用 testNapi.PreferStrategy_OpenLogTest(4, 2) 设置 PREFER_OPEN_LOG + LOG_INFO\n2. 调用 testNapi.OH_LOG_PrintMsg_ParamTest(0, 4, 0xFF00, "TestTag", "info after open") 打印 INFO 级别日志\n3. 获取第二次调用返回值 result |
| 预期结果 | result >= 0 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P2 |
| 依赖关系 | 依赖 SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_001 |

---

## 覆盖率统计

| API | PARAM | ERROR | RETURN | BOUNDARY | 合计 |
|-----|-------|-------|--------|----------|------|
| OH_LOG_PrintMsg | 2 | 0 | 0 | 1 | 3 |
| OH_LOG_PrintMsgByLen | 1 | 0 | 1 | 1 | 3 |
| OH_LOG_VPrint | 2 | 0 | 1 | 0 | 3 |
| PreferStrategy | 3 | 0 | 0 | 0 | 3 |
| **合计** | **8** | **0** | **2** | **2** | **12** |
