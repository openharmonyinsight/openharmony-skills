---
rule_id: "StabilityCodeReview_BoundaryCondition_007"
name: "外部数据类型转换需范围检查"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 外部数据类型转换需范围检查

## 问题描述

对外部数据进行类型转换前需要进行范围检查，避免整数溢出、整数回绕。不安全的类型转换可能导致数据截断、溢出或符号错误，造成程序逻辑错误或安全漏洞。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：int到size_t转换
void AllocateBuffer(int size)
{
    size_t bufferSize = size;  // 危险：size为负数时转换错误
    char* buffer = new char[bufferSize];
}

// 错误示例2：int64到int32截断
void StoreValue(int64_t largeValue)
{
    int32_t smallValue = static_cast<int32_t>(largeValue);  // 危险：可能截断
    data_.push_back(smallValue);
}

// 错误示例3：uint32到int32转换
void ProcessUnsigned(uint32_t unsignedValue)
{
    int32_t signedValue = static_cast<int32_t>(unsignedValue);  // 危险：可能溢出
    array_[signedValue] = 100;  // 可能越界
}

// 错误示例4：Parcel数据直接转换
int GetArrayIndex(Parcel& parcel)
{
    int64_t value = parcel.ReadInt64();
    int index = static_cast<int>(value);  // 危险：截断和范围问题
    return index;
}

// 错误示例5：size_t到int转换
int CalculatePosition(size_t pos)
{
    int position = static_cast<int>(pos);  // 危险：pos可能超过INT_MAX
    return position;
}

// 错误示例6：浮点到整数转换
void ConvertCoordinate(double coordinate)
{
    int intCoord = static_cast<int>(coordinate);  // 危险：可能溢出
    positions_[intCoord] = 1;
}

// 错误示例7：乘法溢出
int CalculateTotal(int base, int multiplier)
{
    return base * multiplier;  // 危险：可能溢出
}

// 错误示例8：加法溢出
int IncrementCounter(int current, int increment)
{
    return current + increment;  // 危险：可能溢出
}

// 错误示例9：负数取模
int ComputeHash(int key, int tableSize)
{
    return key % tableSize;  // 危险：key为负数时结果可能为负
}

// 错误示例10：隐式转换
void SetSize(unsigned int size)
{
    int actualSize = size;  // 危险：隐式转换，可能溢出
    buffer_.resize(actualSize);
}

// 错误示例11：表达式溢出
int CalculateIndex(int x, int y, int z)
{
    return x * y + z;  // 危险：x*y可能溢出
}

// 错误示例12：long到int转换
void ProcessLongValue(long value)
{
    int intValue = value;  // 危险：隐式截断
    DoSomething(intValue);
}
```

### ✅ 修复方案

```cpp
// 正确示例1：检查范围后转换
void AllocateBuffer(int size)
{
    if (size < 0 || size > MAX_BUFFER_SIZE) {
        LOGE("Invalid buffer size: %d", size);
        return;
    }
    size_t bufferSize = static_cast<size_t>(size);  // 正确：已验证
    char* buffer = new char[bufferSize];
}

// 正确示例2：检查截断范围
void StoreValue(int64_t largeValue)
{
    if (largeValue < INT32_MIN || largeValue > INT32_MAX) {
        LOGE("Value out of int32 range: %lld", largeValue);
        return;
    }
    int32_t smallValue = static_cast<int32_t>(largeValue);  // 正确：已验证
    data_.push_back(smallValue);
}

// 正确示例3：unsigned到signed转换检查
void ProcessUnsigned(uint32_t unsignedValue)
{
    if (unsignedValue > INT32_MAX) {
        LOGE("Value too large: %u", unsignedValue);
        return;
    }
    int32_t signedValue = static_cast<int32_t>(unsignedValue);  // 正确：已验证
    array_[signedValue] = 100;
}

// 正确示例4：安全的Parcel数据转换
int GetArrayIndex(Parcel& parcel)
{
    int64_t value = parcel.ReadInt64();
    if (value < 0 || value > INT_MAX) {
        LOGE("Invalid index from parcel: %lld", value);
        return -1;
    }
    return static_cast<int>(value);  // 正确：已验证
}

// 正确示例5：size_t到int安全转换
int CalculatePosition(size_t pos)
{
    if (pos > INT_MAX) {
        LOGE("Position too large: %zu", pos);
        return -1;
    }
    return static_cast<int>(pos);  // 正确：已验证
}

// 正确示例6：浮点到整数安全转换
void ConvertCoordinate(double coordinate)
{
    if (coordinate < INT_MIN || coordinate > INT_MAX) {
        LOGE("Coordinate out of range: %f", coordinate);
        return;
    }
    int intCoord = static_cast<int>(coordinate);  // 正确：已验证
    if (intCoord >= 0 && intCoord < MAX_POSITIONS) {
        positions_[intCoord] = 1;
    }
}

// 正确示例7：使用安全乘法
int CalculateTotal(int base, int multiplier)
{
    if (base > 0 && multiplier > INT_MAX / base) {
        LOGE("Multiplication overflow");
        return INT_MAX;
    }
    if (base < 0 && multiplier < INT_MAX / base) {
        LOGE("Multiplication overflow");
        return INT_MIN;
    }
    return base * multiplier;  // 正确：已验证
}

// 正确示例8：安全加法
int IncrementCounter(int current, int increment)
{
    if (increment > 0 && current > INT_MAX - increment) {
        LOGE("Addition overflow");
        return INT_MAX;
    }
    if (increment < 0 && current < INT_MIN - increment) {
        LOGE("Addition underflow");
        return INT_MIN;
    }
    return current + increment;  // 正确：已验证
}

// 正确示例9：安全的哈希计算
int ComputeHash(int key, int tableSize)
{
    int hash = key % tableSize;
    if (hash < 0) {  // 正确：处理负数结果
        hash += tableSize;
    }
    return hash;
}

// 正确示例10：安全的隐式转换
void SetSize(unsigned int size)
{
    if (size > INT_MAX) {
        LOGE("Size too large: %u", size);
        return;
    }
    int actualSize = static_cast<int>(size);  // 正确：已验证
    buffer_.resize(actualSize);
}

// 正确示例11：表达式溢出检查
int CalculateIndex(int x, int y, int z)
{
    // 先检查乘法
    if (x != 0 && y != 0) {
        if (x > 0 && y > INT_MAX / x) {
            LOGE("Multiplication overflow");
            return -1;
        }
        if (x > 0 && y < INT_MIN / x) {
            LOGE("Multiplication underflow");
            return -1;
        }
        if (x < 0 && y > INT_MIN / x) {
            LOGE("Multiplication overflow");
            return -1;
        }
        if (x < 0 && y < INT_MAX / x) {
            LOGE("Multiplication underflow");
            return -1;
        }
    }
    int product = x * y;
    
    // 再检查加法
    if (z > 0 && product > INT_MAX - z) {
        LOGE("Addition overflow");
        return -1;
    }
    if (z < 0 && product < INT_MIN - z) {
        LOGE("Addition underflow");
        return -1;
    }
    return product + z;  // 正确：已验证
}

// 正确示例12：使用辅助函数
template<typename DestType, typename SrcType>
bool SafeCast(SrcType src, DestType& dest)
{
    if (src > static_cast<SrcType>(std::numeric_limits<DestType>::max()) ||
        src < static_cast<SrcType>(std::numeric_limits<DestType>::lowest())) {
        return false;
    }
    dest = static_cast<DestType>(src);
    return true;
}

void ProcessLongValue(long value)
{
    int intValue;
    if (!SafeCast(value, intValue)) {  // 正确：使用辅助函数
        LOGE("Value out of int range: %ld", value);
        return;
    }
    DoSomething(intValue);
}

// 正确示例13：使用标准库安全整数运算
#include <limits>

int SafeMultiply(int a, int b)
{
    if (a == 0 || b == 0) return 0;
    if (a > 0) {
        if (b > 0 && a > std::numeric_limits<int>::max() / b) {
            throw std::overflow_error("Multiplication overflow");
        }
        if (b < 0 && b < std::numeric_limits<int>::min() / a) {
            throw std::overflow_error("Multiplication underflow");
        }
    } else {
        if (b > 0 && a < std::numeric_limits<int>::min() / b) {
            throw std::overflow_error("Multiplication underflow");
        }
        if (b < 0 && a < std::numeric_limits<int>::max() / b) {
            throw std::overflow_error("Multiplication overflow");
        }
    }
    return a * b;
}
```

## 检测范围

检查以下模式：

1. `static_cast<Type>(value)` - 显式类型转换
2. `Type value = srcValue` - 隐式类型转换
3. `(Type)value` - C风格转换
4. 整数运算：`*`, `+`, `-` 可能溢出
5. 浮点到整数转换

## 检测要点

1. 识别类型转换操作
2. 检查源类型和目标类型的范围
3. 识别外部输入数据来源（参数、Parcel、用户输入）
4. 检查是否进行了范围检查
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 外部输入数据
- **RISK_TYPE**: 整数溢出/截断
- **RISK_PATH**: 类型转换 -> 数据截断/溢出 -> 程序错误
- **IMPACT_POINT**: 数组越界、内存错误、逻辑错误

## 影响分析（ImpactAnalysis）

- **Trigger**: 不安全的类型转换或整数运算
- **Propagation**: 数据截断导致后续计算错误
- **Consequence**: 数组越界、缓冲区溢出、程序崩溃
- **Mitigation**: 转换前检查范围，使用安全运算函数

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有范围检查 | 存在数值范围判断 | 不报 |
| 安全类型 | 同类型或更大范围转换 | 不报 |
| 常量转换 | 转换常量值 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_007_trigger.cpp
void trigger_bad_1(int size)
{
    size_t bufferSize = size;  // 应该报：int到size_t无检查
    char* buffer = new char[bufferSize];
}

void trigger_bad_2(int64_t value)
{
    int32_t small = static_cast<int32_t>(value);  // 应该报：截断无检查
}

void trigger_bad_3(Parcel& parcel)
{
    uint32_t value = parcel.ReadUint32();
    int32_t signedValue = static_cast<int32_t>(value);  // 应该报：无范围检查
}

int trigger_bad_4(int a, int b)
{
    return a * b;  // 应该报：乘法可能溢出
}

int trigger_bad_5(int current, int increment)
{
    return current + increment;  // 应该报：加法可能溢出
}

void trigger_bad_6(double coord)
{
    int intCoord = static_cast<int>(coord);  // 应该报：浮点到整数无检查
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_007_safe.cpp
void safe_good_1(int size)
{
    if (size < 0 || size > MAX_SIZE) {  // 安全：有范围检查
        return;
    }
    size_t bufferSize = static_cast<size_t>(size);
    char* buffer = new char[bufferSize];
}

void safe_good_2(int64_t value)
{
    if (value >= INT32_MIN && value <= INT32_MAX) {  // 安全：有范围检查
        int32_t small = static_cast<int32_t>(value);
    }
}

int safe_good_3(int a, int b)
{
    if (a > 0 && b > INT_MAX / a) {  // 安全：有溢出检查
        return INT_MAX;
    }
    return a * b;
}

void safe_good_4(double coord)
{
    if (coord >= INT_MIN && coord <= INT_MAX) {  // 安全：有范围检查
        int intCoord = static_cast<int>(coord);
    }
}

// NOPROTECT: 特殊处理场景
void noprotect_case(int64_t value)
{
    int32_t small = static_cast<int32_t>(value);
}
```