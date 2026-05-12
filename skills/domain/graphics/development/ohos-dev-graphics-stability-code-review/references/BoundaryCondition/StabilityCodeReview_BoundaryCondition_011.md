---
rule_id: "StabilityCodeReview_BoundaryCondition_011"
name: "类型强制转换未校验，可能导致越界读"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 类型强制转换未校验，可能导致越界读

## 问题描述

类型强制转换时未校验数值范围，可能导致数据截断、数值错误或越界读取。大类型转小类型时，源值超出目标类型范围会造成数据丢失和潜在的安全问题。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：大整数转小整数
void ProcessValue(int64_t bigValue)
{
    int smallValue = (int)bigValue;  // 危险：可能截断
    array[smallValue] = data;  // 可能导致越界
}

// 错误示例2：size_t转int
void AccessBuffer(size_t index, int offset)
{
    int idx = (int)index + offset;  // 危险：size_t可能超过INT_MAX
    buffer[idx] = value;
}

// 错误示例3：无符号转有符号
void ProcessIndex(uint32_t unsignedIndex)
{
    int signedIndex = (int)unsignedIndex;  // 危险：若unsignedIndex > INT_MAX，变为负数
    array[signedIndex] = data;  // 可能越界访问
}

// 错误示例4：指针强制转换
void HandlePointer(void* ptr)
{
    int* intPtr = (int*)ptr;  // 危险：未检查对齐和有效性
    *intPtr = 0;  // 可能崩溃
}

// 错误示例5：double转int
void ConvertCoordinate(double coord)
{
    int pixel = (int)coord;  // 危险：double可能超出int范围
    screen[pixel] = color;
}
```

### ✅ 修复方案

```cpp
// 正确示例1：添加范围检查
void ProcessValue(int64_t bigValue)
{
    if (bigValue > INT_MAX || bigValue < INT_MIN) {
        LOGE("Value out of int range: %lld", bigValue);
        return;
    }
    int smallValue = static_cast<int>(bigValue);
    array[smallValue] = data;
}

// 正确示例2：使用saturated_cast
void AccessBuffer(size_t index, int offset)
{
    int idx = base::saturated_cast<int>(index) + offset;
    if (idx < 0 || idx >= buffer_size) {
        LOGE("Index out of range: %d", idx);
        return;
    }
    buffer[idx] = value;
}

// 正确示例3：显式范围检查
void ProcessIndex(uint32_t unsignedIndex)
{
    if (unsignedIndex > static_cast<uint32_t>(INT_MAX)) {
        LOGE("Index exceeds INT_MAX: %u", unsignedIndex);
        return;
    }
    int signedIndex = static_cast<int>(unsignedIndex);
    array[signedIndex] = data;
}

// 正确示例4：安全的指针转换
void HandlePointer(void* ptr)
{
    if (ptr == nullptr) {
        LOGE("Null pointer");
        return;
    }
    // 检查对齐
    if (reinterpret_cast<uintptr_t>(ptr) % alignof(int) != 0) {
        LOGE("Pointer not aligned for int");
        return;
    }
    int* intPtr = static_cast<int*>(ptr);
    *intPtr = 0;
}

// 正确示例5：浮点数范围检查
void ConvertCoordinate(double coord)
{
    if (coord > INT_MAX || coord < INT_MIN || !std::isfinite(coord)) {
        LOGE("Invalid coordinate: %f", coord);
        return;
    }
    int pixel = static_cast<int>(coord);
    if (pixel >= 0 && pixel < screen_size) {
        screen[pixel] = color;
    }
}
```

## 检测范围

检查以下类型转换：

- `static_cast<小类型>(大类型值)`
- C风格转换 `(int)`、`(short)`、`(char)` 等
- `reinterpret_cast` 指针转换
- `size_t` → `int`
- `int64_t` → `int32_t`
- `uint32_t` → `int32_t`
- `double` → `int`

## 检测要点

1. 识别类型转换表达式
2. 判断是否为大类型转小类型
3. 检查是否有范围校验
4. 检查是否使用了安全转换函数
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 类型强制转换
- **RISK_TYPE**: 数值截断/越界
- **RISK_PATH**: 大类型转小类型 -> 数值截断 -> 数据错误/越界访问
- **IMPACT_POINT**: 数据损坏、内存越界、安全漏洞

## 影响分析（ImpactAnalysis）

- **Trigger**: 源值超出目标类型表示范围
- **Propagation**: 数值被截断或解释为负值
- **Consequence**: 数组越界、数据损坏、安全漏洞
- **Mitigation**: 转换前校验数值范围

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有范围检查 | 存在 INT_MAX、范围比较 | 不报 |
| 使用安全转换 | 使用 saturated_cast、checked_cast | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_011_trigger.cpp
void trigger_bad_1(int64_t bigValue)
{
    int smallValue = (int)bigValue;  // 应该报：未检查范围
}

void trigger_bad_2(size_t index)
{
    int idx = static_cast<int>(index);  // 应该报：未检查范围
}

void trigger_bad_3(uint32_t unsignedIndex)
{
    int signedIndex = (int)unsignedIndex;  // 应该报：可能变为负数
    array[signedIndex] = data;
}

void trigger_bad_4(double coord)
{
    int pixel = (int)coord;  // 应该报：未检查范围
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_011_safe.cpp
void safe_good_1(int64_t bigValue)
{
    if (bigValue >= INT_MIN && bigValue <= INT_MAX) {  // 安全：有范围检查
        int smallValue = static_cast<int>(bigValue);
    }
}

void safe_good_2(size_t index)
{
    int idx = base::saturated_cast<int>(index);  // 安全：使用saturated_cast
}

void safe_good_3(uint32_t unsignedIndex)
{
    if (unsignedIndex <= static_cast<uint32_t>(INT_MAX)) {  // 安全：有范围检查
        int signedIndex = static_cast<int>(unsignedIndex);
    }
}

// NOPROTECT: 已确认值在范围内
void noprotect_case(int64_t value)
{
    int v = (int)value;  // 已确认范围
}
```