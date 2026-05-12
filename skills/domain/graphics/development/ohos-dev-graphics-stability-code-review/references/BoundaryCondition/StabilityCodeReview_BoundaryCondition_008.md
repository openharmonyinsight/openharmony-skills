---
rule_id: "StabilityCodeReview_BoundaryCondition_008"
name: "加减乘除运算应避免类型溢出或回绕"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 加减乘除运算应避免类型溢出或回绕

## 问题描述

整数运算时未检查溢出，可能导致数值回绕、逻辑错误或安全问题。尤其在内存分配大小计算、数组索引计算等关键场景，溢出可能导致内存分配不足或越界访问。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：乘法溢出导致内存分配不足
void AllocateBuffer(int count, int itemSize)
{
    int totalSize = count * itemSize;  // 危险：可能溢出
    char* buffer = new char[totalSize];
    // ...
}

// 错误示例2：加法溢出
void ProcessData(int offset, int length)
{
    int end = offset + length;  // 危险：可能溢出
    for (int i = offset; i < end; i++) {
        ProcessItem(i);
    }
}

// 错误示例3：减法回绕（无符号）
void CopyData(uint32_t start, uint32_t end)
{
    uint32_t size = end - start;  // 危险：若end < start，回绕到超大值
    char* buffer = new char[size];
    // ...
}

// 错误示例4：计算缓冲区大小
int CalculateBufferSize(int width, int height, int bpp)
{
    return width * height * bpp;  // 危险：多次乘法可能溢出
}
```

### ✅ 修复方案

```cpp
// 正确示例1：乘法溢出检查
void AllocateBuffer(int count, int itemSize)
{
    // 检查乘法溢出
    if (itemSize > 0 && count > INT_MAX / itemSize) {
        LOGE("Multiplication overflow: %d * %d", count, itemSize);
        return;
    }
    int totalSize = count * itemSize;
    if (totalSize <= 0) {
        LOGE("Invalid size: %d", totalSize);
        return;
    }
    char* buffer = new char[totalSize];
    // ...
}

// 正确示例2：使用安全整数运算库
void AllocateBufferSafe(int count, int itemSize)
{
    int totalSize;
    if (!base::CheckMul(count, itemSize).AssignIfValid(&totalSize)) {
        LOGE("Multiplication overflow");
        return;
    }
    char* buffer = new char[totalSize];
    // ...
}

// 正确示例3：使用saturated_cast
void ProcessData(int offset, int length)
{
    int64_t end = base::saturated_cast<int64_t>(offset) + 
                  base::saturated_cast<int64_t>(length);
    if (end > INT_MAX || end < offset) {
        LOGE("Addition overflow");
        return;
    }
    for (int i = offset; i < static_cast<int>(end); i++) {
        ProcessItem(i);
    }
}

// 正确示例4：使用64位中间值
int64_t CalculateBufferSize(int width, int height, int bpp)
{
    int64_t size = static_cast<int64_t>(width) * 
                   static_cast<int64_t>(height) * 
                   static_cast<int64_t>(bpp);
    if (size > INT_MAX || size <= 0) {
        LOGE("Buffer size overflow or invalid");
        return -1;
    }
    return static_cast<int>(size);
}
```

## 检测范围

检查以下运算模式：

- `a * b`、`a * b * c` 等乘法运算
- `a + b`、`a + b + c` 等加法运算
- `a - b` 减法运算（特别是无符号类型）
- 内存分配大小计算：`malloc(a * b)`、`new char[a * b]`
- 数组索引计算：`array[a + b]`、`array[a * b]`

## 检测要点

1. 识别算术运算表达式（+、-、*）
2. 检查是否在内存分配上下文中使用
3. 检查是否在数组索引上下文中使用
4. 检查是否存在溢出保护机制
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 整数运算表达式
- **RISK_TYPE**: 整数溢出/回绕
- **RISK_PATH**: 运算结果溢出 -> 数值回绕 -> 内存分配错误/数组越界
- **IMPACT_POINT**: 内存损坏、安全漏洞、程序崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: 运算结果超出类型表示范围
- **Propagation**: 结果回绕为负值或意外大值
- **Consequence**: 内存分配不足、缓冲区溢出、数据损坏
- **Mitigation**: 使用安全整数运算库或添加溢出检查

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有溢出检查 | 存在 INT_MAX、溢出函数调用 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
| 常量运算 | 编译期可计算的表达式 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_008_trigger.cpp
void trigger_bad_1(int count, int itemSize)
{
    int total = count * itemSize;  // 应该报：乘法溢出风险
    char* buffer = new char[total];
}

void trigger_bad_2(int a, int b, int c)
{
    int size = a * b * c;  // 应该报：多次乘法溢出风险
    ProcessBuffer(size);
}

void trigger_bad_3(uint32_t start, uint32_t end)
{
    uint32_t size = end - start;  // 应该报：无符号减法回绕风险
    char* buffer = new char[size];
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_008_safe.cpp
void safe_good_1(int count, int itemSize)
{
    if (itemSize > 0 && count <= INT_MAX / itemSize) {  // 安全：有溢出检查
        int total = count * itemSize;
        char* buffer = new char[total];
    }
}

void safe_good_2(int count, int itemSize)
{
    int total = base::saturated_cast<int>(
        static_cast<int64_t>(count) * itemSize);  // 安全：使用saturated
    char* buffer = new char[total];
}

// NOPROTECT: 常量运算不会溢出
void noprotect_case()
{
    const int SIZE = 10 * 20;  // 编译期常量，不报
    char buffer[SIZE];
}
```