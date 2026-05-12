---
rule_id: "StabilityCodeReview_ExceptionHandling_001"
name: "禁止异常处理机制"
category: "异常处理"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 禁止异常处理机制

## 问题描述

OpenHarmony 不允许使用 C++ 异常处理机制（try/catch/throw）。异常处理机制会引入运行时开销和代码膨胀，影响系统稳定性和性能。代码中如果使用了异常处理，违反了 OpenHarmony 编码规范。

## 检测示例

### ❌ 问题代码

```cpp
// 使用 try/catch - 禁止
void ProcessData() {
    try {
        DoSomething();
    } catch (const std::exception& e) {
        LOGE("Exception: %s", e.what());
    }
}

// 使用 throw - 禁止
void ValidateInput(int value) {
    if (value < 0) {
        throw std::invalid_argument("Invalid value");
    }
}
```

### ✅ 修复方案

```cpp
// 使用错误码返回值替代
ErrorCode ProcessData() {
    ErrorCode ret = DoSomething();
    if (ret != ErrorCode::SUCCESS) {
        LOGE("DoSomething failed: %d", ret);
        return ret;
    }
    return ErrorCode::SUCCESS;
}

// 使用错误码返回值替代
ErrorCode ValidateInput(int value) {
    if (value < 0) {
        LOGE("Invalid value: %d", value);
        return ErrorCode::INVALID_PARAM;
    }
    return ErrorCode::SUCCESS;
}
```

## 检测范围

检查以下关键字：

- `try` - try 块关键字
- `catch` - catch 块关键字  
- `throw` - throw 语句关键字

## 检测要点

1. 检测代码中是否包含 try 关键字
2. 检测代码中是否包含 catch 关键字
3. 检测代码中是否包含 throw 关键字
4. 排除 NOPROTECT 标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 代码中使用了 try/catch/throw 异常处理关键字
- **RISK_TYPE**: 违反 OpenHarmony 编码规范
- **RISK_PATH**: 异常处理机制引入运行时开销和代码膨胀
- **IMPACT_POINT**: 影响系统稳定性和性能

## 影响分析（ImpactAnalysis）

- **Trigger**: 代码中使用异常处理机制
- **Propagation**: 异常处理机制引入运行时开销和代码膨胀
- **Consequence**: 违反 OpenHarmony 编码规范，可能导致稳定性问题
- **Mitigation**: 使用错误码返回值替代异常处理机制

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录或 _test.cpp 文件 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ExceptionHandling_001_trigger.cpp
void trigger_bad_1() {
    try {  // 应该报：使用了 try
        DoSomething();
    } catch (...) {
    }
}

void trigger_bad_2() {
    throw std::runtime_error("error");  // 应该报：使用了 throw
}

void trigger_bad_3() {
    try {
        Process();
    } catch (const std::exception& e) {  // 应该报：使用了 catch
    }
}
```

### 安全用例（不应该报）

```cpp
// test_ExceptionHandling_001_safe.cpp
void safe_good() {
    // 使用错误码返回值
    ErrorCode ret = DoSomething();
    if (ret != ErrorCode::SUCCESS) {
        LOGE("Failed: %d", ret);
    }
}

// NOPROTECT 标记
void noprotect_case() {
    // NOPROTECT: 第三方库接口要求使用异常
    try {
        ThirdPartyCall();
    } catch (...) {
    }
}
```