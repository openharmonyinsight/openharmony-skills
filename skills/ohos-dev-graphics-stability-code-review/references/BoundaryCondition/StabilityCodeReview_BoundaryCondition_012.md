---
rule_id: "StabilityCodeReview_BoundaryCondition_012"
name: "数组下标的计算应避免整数回绕导致内存越界访问"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 数组下标的计算应避免整数回绕导致内存越界访问

## 问题描述

数组下标计算时若存在整数溢出或回绕，可能导致产生非法下标值，造成内存越界访问。无符号整数减法回绕尤其危险，可能产生超大值导致严重的内存安全问题。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：无符号整数减法回绕
void ProcessRange(uint32_t start, uint32_t end)
{
    uint32_t size = end - start;  // 危险：若end < start，回绕到超大值
    char* buffer = new char[size];
    memcpy(buffer, data, size);  // 可能分配超大内存或越界
}

// 错误示例2：乘法溢出作为下标
void AllocateMatrix(int width, int height)
{
    int index = width * height;  // 危险：可能溢出
    buffer[index] = value;  // 可能越界访问
}

// 错误示例3：加法溢出作为下标
void AccessBuffer(int base, int offset)
{
    int index = base + offset;  // 危险：可能溢出
    array[index] = data;  // 可能越界
}

// 错误示例4：复杂表达式下标
void ProcessBuffer(int a, int b, int c)
{
    int idx = a * b + c;  // 危险：多次运算可能溢出
    buffer[idx] = value;
}

// 错误示例5：无符号减法用于数组访问
void CopyItems(uint32_t count, uint32_t start)
{
    for (uint32_t i = 0; i < count; i++) {
        uint32_t idx = start - 1 + i;  // 危险：start=0时回绕
        array[idx] = items[i];
    }
}
```

### ✅ 修复方案

```cpp
// 正确示例1：检查无符号减法
void ProcessRange(uint32_t start, uint32_t end)
{
    if (end < start) {
        LOGE("Invalid range: end < start");
        return;
    }
    uint32_t size = end - start;
    if (size > MAX_BUFFER_SIZE) {
        LOGE("Size too large: %u", size);
        return;
    }
    char* buffer = new char[size];
    memcpy(buffer, data, size);
}

// 正确示例2：安全乘法
void AllocateMatrix(int width, int height)
{
    if (width <= 0 || height <= 0) {
        LOGE("Invalid dimensions");
        return;
    }
    if (width > INT_MAX / height) {
        LOGE("Multiplication overflow");
        return;
    }
    int index = width * height;
    if (index >= buffer_size) {
        LOGE("Index out of range");
        return;
    }
    buffer[index] = value;
}

// 正确示例3：安全加法
void AccessBuffer(int base, int offset)
{
    if (offset > 0 && base > INT_MAX - offset) {
        LOGE("Addition overflow");
        return;
    }
    if (offset < 0 && base < INT_MIN - offset) {
        LOGE("Addition underflow");
        return;
    }
    int index = base + offset;
    if (index < 0 || index >= array_size) {
        LOGE("Index out of range: %d", index);
        return;
    }
    array[index] = data;
}

// 正确示例4：使用64位中间值
void ProcessBuffer(int a, int b, int c)
{
    int64_t idx = static_cast<int64_t>(a) * b + c;
    if (idx < 0 || idx >= buffer_size) {
        LOGE("Index out of range: %lld", idx);
        return;
    }
    buffer[static_cast<size_t>(idx)] = value;
}

// 正确示例5：安全的无符号运算
void CopyItems(uint32_t count, uint32_t start)
{
    if (start == 0) {
        LOGE("Invalid start index");
        return;
    }
    for (uint32_t i = 0; i < count; i++) {
        uint32_t idx = start - 1 + i;
        if (idx >= array_size) {
            LOGE("Index out of range: %u", idx);
            return;
        }
        array[idx] = items[i];
    }
}
```

## 检测范围

检查以下下标计算模式：

- `array[a + b]` - 加法下标
- `array[a - b]` - 减法下标（尤其无符号）
- `array[a * b]` - 乘法下标
- `array[a * b + c]` - 复合表达式下标
- `uint` 类型减法表达式

## 检测要点

1. 识别数组访问表达式
2. 检测下标中是否包含算术运算
3. 判断是否为危险的无符号减法
4. 检查是否有边界检查
5. 检查是否使用了安全运算函数
6. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 数组下标计算表达式
- **RISK_TYPE**: 整数溢出/回绕
- **RISK_PATH**: 下标计算溢出 -> 产生非法值 -> 内存越界访问
- **IMPACT_POINT**: 内存破坏、信息泄露、安全漏洞

## 影响分析（ImpactAnalysis）

- **Trigger**: 下标计算结果超出数组范围
- **Propagation**: 整数回绕产生非法下标值
- **Consequence**: 越界读写、内存破坏、安全漏洞
- **Mitigation**: 使用安全整数运算库，添加边界检查

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有边界检查 | 存在范围比较、size检查 | 不报 |
| 使用安全运算 | 使用 SAFE_ADD、SafeMul 等 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
| 常量下标 | 编译期可计算的常量 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_012_trigger.cpp
void trigger_bad_1(uint32_t start, uint32_t end)
{
    uint32_t size = end - start;  // 应该报：无符号减法可能回绕
    char* buf = new char[size];
}

void trigger_bad_2(int a, int b)
{
    int idx = a * b;  // 应该报：乘法可能溢出
    buffer[idx] = value;
}

void trigger_bad_3(int base, int offset)
{
    int idx = base + offset;  // 应该报：加法可能溢出
    array[idx] = data;
}

void trigger_bad_4(uint32_t count, uint32_t start)
{
    uint32_t idx = start - 1;  // 应该报：无符号减法可能回绕
    array[idx] = 0;
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_012_safe.cpp
void safe_good_1(uint32_t start, uint32_t end)
{
    if (end < start) {  // 安全：有边界检查
        return;
    }
    uint32_t size = end - start;
    char* buf = new char[size];
}

void safe_good_2(int a, int b)
{
    if (a > 0 && b > 0 && a <= INT_MAX / b) {  // 安全：有溢出检查
        int idx = a * b;
        if (idx < buffer_size) {
            buffer[idx] = value;
        }
    }
}

void safe_good_3(int base, int offset)
{
    int idx = SafeAdd(base, offset);  // 安全：使用安全运算函数
    if (idx >= 0 && idx < array_size) {
        array[idx] = data;
    }
}

// NOPROTECT: 下标已确认在范围内
void noprotect_case(int idx)
{
    buffer[idx] = value;  // 已确认idx合法
}
```