---
rule_id: "StabilityCodeReview_BoundaryCondition_013"
name: "返回值类型不匹配风险"
category: "边界条件"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 返回值类型不匹配风险

## 问题描述

函数返回值类型与接收变量类型不匹配可能导致隐式类型转换、数值截断、符号扩展错误等问题。这类问题可能导致数据错误、逻辑异常，甚至引发安全漏洞。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：size_t返回值赋给int
int GetBufferSize()
{
    size_t size = CalculateSize();  // size_t可能是unsigned long
    return size;  // 错误：size_t赋给int，可能截断
}

// 场景2：int64返回值赋给int32
int32_t GetId()
{
    int64_t id = GenerateUniqueId();  // int64_t
    return id;  // 错误：int64_t赋给int32_t，可能截断
}

// 场景3：unsigned返回值赋给signed
int GetCount()
{
    unsigned int count = GetElementCount();  // unsigned
    return count;  // 错误：unsigned赋给int，可能产生负数错误
}

// 场景4：指针与整数混用
int GetPointerValue()
{
    void* ptr = GetAddress();
    return (int)ptr;  // 错误：指针强制转换为int，64位平台指针截断
}

// 场景5：枚举与整数不匹配
int GetStatus()
{
    Status status = GetObjectStatus();  // 枚举类型
    return status;  // 错误：枚举返回值类型不明确
}

// 场景6：函数返回bool但接收为int
int ProcessData()
{
    bool result = ValidateData();  // bool返回值
    return result;  // 错误：bool赋给int，语义不明确
}
```

### ✅ 修复方案

```cpp
// 修复场景1：使用匹配的类型
size_t GetBufferSize()
{
    size_t size = CalculateSize();
    return size;  // 正确：返回类型匹配
}

// 或者如果需要int，添加范围检查
int GetBufferSize()
{
    size_t size = CalculateSize();
    if (size > INT_MAX) {  // 正确：校验范围
        return -1;  // 错误码
    }
    return static_cast<int>(size);
}

// 修复场景2：使用匹配的类型
int64_t GetId()
{
    int64_t id = GenerateUniqueId();
    return id;  // 正确：返回类型匹配
}

// 修复场景3：保持类型一致性
unsigned int GetCount()
{
    unsigned int count = GetElementCount();
    return count;  // 正确：返回类型匹配
}

// 或者如果需要int，添加范围检查
int GetCount()
{
    unsigned int count = GetElementCount();
    if (count > INT_MAX) {  // 正确：校验范围
        LOGE("count overflow");
        return -1;
    }
    return static_cast<int>(count);
}

// 修复场景4：使用intptr_t处理指针
intptr_t GetPointerValue()
{
    void* ptr = GetAddress();
    return reinterpret_cast<intptr_t>(ptr);  // 正确：intptr_t保证能容纳指针
}

// 修复场景5：明确枚举返回类型
Status GetStatus()
{
    Status status = GetObjectStatus();
    return status;  // 正确：返回枚举类型
}

// 修复场景6：保持bool语义
bool ProcessData()
{
    bool result = ValidateData();
    return result;  // 正确：返回bool类型
}
```

## 检测范围

检查以下模式：

- `size_t` / `ssize_t` 返回值赋给 `int`
- `int64_t` / `uint64_t` 返回值赋给 `int32_t`
- `unsigned` 返回值赋给 `signed` 类型
- 指针类型强制转换为整数类型
- 枚举类型返回值赋给整数
- `bool` 返回值赋给 `int`

## 检测要点

1. 识别函数返回值类型
2. 检查接收变量类型是否匹配
3. 判断是否存在隐式类型转换风险
4. 检查是否有范围校验（如 INT_MAX 检查）
5. 排除明确标记为安全的强制转换

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：类型不匹配的返回值赋值
- **RISK_TYPE**：隐式类型转换错误
- **RISK_PATH**：返回值类型不匹配 → 隐式转换 → 数值截断或符号错误 → 数据错误
- **IMPACT_POINT**：逻辑错误、数据损坏、潜在安全漏洞

## 影响分析（ImpactAnalysis）

- **Trigger**：返回值超出目标类型范围
- **Propagation**：数值截断、符号位改变、精度丢失
- **Consequence**：数据错误、逻辑异常、安全漏洞
- **Mitigation**：使用匹配类型或添加范围校验

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 有范围校验 | 有INT_MAX等范围检查 | 不报 |
| 明确强制转换 | 有static_cast且类型明确 | 需判断安全性 |
| 同类型 | 返回类型和接收类型相同 | 不报 |
| NOPROTECT标记 | // NOPROTECT 注释 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_013_trigger.cpp
int trigger_bad_1()
{
    size_t size = CalculateSize();
    return size;  // 应该报：size_t赋给int
}

int32_t trigger_bad_2()
{
    int64_t id = GenerateUniqueId();
    return id;  // 应该报：int64_t赋给int32_t
}

int trigger_bad_3()
{
    unsigned count = GetElementCount();
    return count;  // 应该报：unsigned赋给int
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_013_safe.cpp
size_t safe_good_1()
{
    size_t size = CalculateSize();
    return size;  // 安全：类型匹配
}

int safe_good_2()
{
    size_t size = CalculateSize();
    if (size <= INT_MAX) {  // 安全：有范围校验
        return static_cast<int>(size);
    }
    return -1;
}

// NOPROTECT: 特殊场景
int noprotect_case()
{
    unsigned count = GetElementCount();
    return count;  // NOPROTECT标记，不报
}
```