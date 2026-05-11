---
rule_id: "StabilityCodeReview_ExceptionHandling_002"
name: "异常分支应正确处理"
category: "异常处理"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 异常分支应正确处理

## 问题描述

异常处理分支应该有合适的处理方式，不能静默忽略或遗漏return。异常分支中如果只打印日志而没有return，会导致程序继续执行后续逻辑，可能引发更严重的问题。需要根据业务需要来决定异常分支的处理方式。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：异常分支只打印日志，缺少return
void ProcessData(int* data, int size) {
    if (data == nullptr) {
        LOGE("data is null");  // 缺少 return
    }
    // 继续执行，导致空指针访问
    for (int i = 0; i < size; i++) {
        data[i] = 0;
    }
}

// 场景2：异常分支空实现，完全静默
int CalculateResult(int value) {
    if (value < 0) {
        // 空实现，既没有日志也没有return
    }
    return value * 2;
}

// 场景3：异常分支只有注释，缺少实际处理
bool ValidateConfig(const Config& config) {
    if (config.path.empty()) {
        // TODO: handle error  // 只有TODO注释
    }
    return true;  // 错误地返回true
}
```

### ✅ 修复方案

```cpp
// 修复场景1：根据业务需要添加return
void ProcessData(int* data, int size) {
    if (data == nullptr) {
        LOGE("data is null");
        return;  // 添加return，避免空指针访问
    }
    for (int i = 0; i < size; i++) {
        data[i] = 0;
    }
}

// 修复场景2：异常分支记录日志并返回错误值
int CalculateResult(int value) {
    if (value < 0) {
        LOGE("Invalid value: %d, must be non-negative", value);
        return -1;  // 返回错误码
    }
    return value * 2;
}

// 修复场景3：异常分支返回失败状态
bool ValidateConfig(const Config& config) {
    if (config.path.empty()) {
        LOGE("Config path is empty");
        return false;  // 返回失败状态
    }
    return true;
}

// 修复场景4：异常分支包含资源清理
void ProcessResource(Resource* res, const std::string& data) {
    if (res == nullptr) {
        LOGE("Resource is null");
        return;  // 添加return，避免后续资源操作
    }
    if (data.empty()) {
        LOGE("Data is empty, releasing resource");
        ReleaseResource(res);  // 清理已分配的资源
        return;
    }
    // 正常处理流程
}

// 修复场景5：void函数无日志return（适用于Dump/Debug函数）
void DumpNodeInfo(const Node* node) {
    if (node == nullptr) {
        return;  // Debug函数中只return无日志是合理的
    }
    PrintNodeDetails(node);
}
```

## 检测范围

检查以下异常分支模式：

- `if` 条件判断后只有日志语句
- `if` 条件判断后空实现（只有注释或空白）
- 错误处理分支缺少 `return` 语句

## 检测要点

1. 识别 `if` 语句块，特别是包含错误检查的条件（如 `nullptr`、`< 0`、`empty()`）
2. 检查 `if` 块内是否只有日志语句（`LOGE`、`LOG_ERROR` 等）或空实现
3. 检查是否缺少 `return` 语句或有效的错误处理
4. 排除有明确业务逻辑处理的异常分支

### 日志级别使用说明

异常分支中的日志级别应根据问题严重程度选择：

- **LOGE/LOG_ERROR**：严重错误，影响核心功能或系统稳定性，必须立即处理
  - 示例：空指针检查、关键资源分配失败、数据完整性错误
  - 场景：`if (ptr == nullptr) { LOGE("Critical: null pointer"); return; }`

- **LOGW/LOG_WARN**：警告信息，可能影响功能但系统可继续运行
  - 示例：参数范围警告、性能降级、兼容性问题
  - 场景：`if (value < 0) { LOGW("Warning: negative value"); return -1; }`

- **LOGD/LOG_DEBUG**：调试信息，仅在调试构建中输出
  - 示例：调试函数中的状态检查、非关键分支路径
  - 场景：Dump类函数、调试辅助函数

- **LOGI/LOG_INFO**：一般信息，记录程序运行状态
  - 示例：非关键条件分支、可选功能未启用
  - 场景：配置缺失但使用默认值的场景

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：异常分支缺少有效处理（只打印日志或空实现）
- **RISK_TYPE**：异常处理不当导致逻辑缺陷
- **RISK_PATH**：异常情况发生后程序继续执行，导致后续代码在非法状态下运行
- **IMPACT_POINT**：可能引发空指针访问、数据损坏、功能异常等严重问题

## 影响分析（ImpactAnalysis）

- **Trigger**：异常条件触发，但异常分支未正确处理
- **Propagation**：程序继续执行后续代码，使用非法数据或状态
- **Consequence**：空指针崩溃、数据损坏、功能异常，影响系统稳定性
- **Mitigation**：异常分支应根据业务需要添加return语句或有效错误处理

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 故意继续执行 | 有明确业务逻辑处理 | 不报 |
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 统计日志场景 | 只有统计目的的日志 | 根据上下文判断 |
| 条件设置场景 | if 用于设置默认值 | 不报 |
| Dump/Debug 函数 | 函数名含Dump/Debug/Log/Print | 可接受无日志的return |
| 资源清理场景 | 异常分支包含Release/Close/Delete等清理操作 | 不报（已有处理） |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ExceptionHandling_002_trigger.cpp
void trigger_bad_1() {
    int* ptr = nullptr;
    if (ptr == nullptr) {
        LOGE("ptr is null");  // 应该报：缺少return
    }
    *ptr = 10;  // 空指针访问
}

int trigger_bad_2(int value) {
    if (value < 0) {
        // 空实现  // 应该报：既没有日志也没有return
    }
    return value * 2;
}

bool trigger_bad_3(const std::string& path) {
    if (path.empty()) {
        // TODO: handle error  // 应该报：只有TODO注释
    }
    return true;
}
```

### 安全用例（不应该报）

```cpp
// test_ExceptionHandling_002_safe.cpp
void safe_good_1(int* data, int size) {
    if (data == nullptr) {
        LOGE("data is null");
        return;  // 正确：有return
    }
    for (int i = 0; i < size; i++) {
        data[i] = 0;
    }
}

int safe_good_2(int value) {
    if (value < 0) {
        LOGE("Invalid value: %d", value);
        return -1;  // 正确：返回错误码
    }
    return value * 2;
}

// NOPROTECT 标记
void noprotect_case(int* ptr) {
    // NOPROTECT: 此处故意继续执行
    if (ptr == nullptr) {
        LOGW("ptr is null, using default");
    }
    // 继续执行...
}
```