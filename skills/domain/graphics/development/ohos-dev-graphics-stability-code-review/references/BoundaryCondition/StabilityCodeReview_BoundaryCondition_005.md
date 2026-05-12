---
rule_id: "StabilityCodeReview_BoundaryCondition_005"
name: "Parcel整数转枚举需校验有效性"
category: "边界条件"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Parcel整数转枚举需校验有效性

## 问题描述

从Parcel中读取的整数不能直接转化为枚举类，需要校验值的有效性。未经验证的枚举值转换可能导致未定义行为、程序逻辑错误或安全漏洞。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：直接强制转换
enum class Color { RED = 0, GREEN = 1, BLUE = 2 };

Color ReadColor(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    return static_cast<Color>(value);  // 危险：value可能不在枚举范围内
}

// 错误示例2：隐式转换
enum Status { OK = 0, ERROR = 1, PENDING = 2 };

Status ReadStatus(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    return static_cast<Status>(value);  // 危险：未验证枚举范围
}

// 错误示例3：使用switch后仍未覆盖所有情况
enum class Type { TYPE_A = 0, TYPE_B = 1, TYPE_C = 2 };

Type ReadType(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    Type type = static_cast<Type>(value);  // 危险：未验证就转换
    
    switch (type) {
        case Type::TYPE_A:
            HandleA();
            break;
        case Type::TYPE_B:
            HandleB();
            break;
        default:  // 可能落入无效值
            break;
    }
    return type;
}

// 错误示例4：枚举值直接赋值
enum class Mode { MODE_READ = 0, MODE_WRITE = 1 };

void SetMode(Parcel& parcel)
{
    Mode mode = static_cast<Mode>(parcel.ReadInt32());  // 危险：未验证
    currentMode_ = mode;
}

// 错误示例5：位域枚举直接转换
enum class Flags : uint32_t {
    FLAG_NONE = 0,
    FLAG_A = 1 << 0,
    FLAG_B = 1 << 1,
    FLAG_C = 1 << 2
};

Flags ReadFlags(Parcel& parcel)
{
    uint32_t value = parcel.ReadUint32();
    return static_cast<Flags>(value);  // 危险：可能包含无效标志位
}
```

### ✅ 修复方案

```cpp
// 正确示例1：验证后转换
enum class Color { RED = 0, GREEN = 1, BLUE = 2 };

Color ReadColor(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    switch (value) {
        case static_cast<int>(Color::RED):
        case static_cast<int>(Color::GREEN):
        case static_cast<int>(Color::BLUE):
            return static_cast<Color>(value);
        default:
            LOGE("Invalid color value: %d", value);
            return Color::RED;  // 返回默认值
    }
}

// 正确示例2：使用辅助函数验证
enum Status { OK = 0, ERROR = 1, PENDING = 2 };

bool IsValidStatus(int value)
{
    return value == OK || value == ERROR || value == PENDING;
}

Status ReadStatus(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    if (!IsValidStatus(value)) {
        LOGE("Invalid status value: %d", value);
        return OK;  // 返回默认值
    }
    return static_cast<Status>(value);
}

// 正确示例3：完整验证所有枚举值
enum class Type { TYPE_A = 0, TYPE_B = 1, TYPE_C = 2 };

bool IsValidType(int value)
{
    return value >= static_cast<int>(Type::TYPE_A) &&
           value <= static_cast<int>(Type::TYPE_C);
}

Type ReadType(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    if (!IsValidType(value)) {
        LOGE("Invalid type value: %d", value);
        return Type::TYPE_A;  // 返回默认值
    }
    return static_cast<Type>(value);
}

// 正确示例4：枚举类模板验证
template<typename E>
bool IsValidEnumValue(int value, E minVal, E maxVal)
{
    return value >= static_cast<int>(minVal) && value <= static_cast<int>(maxVal);
}

enum class Mode { MODE_READ = 0, MODE_WRITE = 1 };

Mode ReadMode(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    if (!IsValidEnumValue(value, Mode::MODE_READ, Mode::MODE_WRITE)) {
        LOGE("Invalid mode value: %d", value);
        return Mode::MODE_READ;
    }
    return static_cast<Mode>(value);
}

// 正确示例5：位域枚举验证
enum class Flags : uint32_t {
    FLAG_NONE = 0,
    FLAG_A = 1 << 0,
    FLAG_B = 1 << 1,
    FLAG_C = 1 << 2,
    ALL_FLAGS = FLAG_A | FLAG_B | FLAG_C
};

Flags ReadFlags(Parcel& parcel)
{
    uint32_t value = parcel.ReadUint32();
    // 验证是否为有效的标志组合
    if ((value & ~static_cast<uint32_t>(Flags::ALL_FLAGS)) != 0) {
        LOGE("Invalid flags value: 0x%x", value);
        return Flags::FLAG_NONE;
    }
    return static_cast<Flags>(value);
}

// 正确示例6：使用映射表验证
enum class Command { CMD_START = 0, CMD_STOP = 1, CMD_PAUSE = 2, CMD_RESUME = 3 };

static const std::unordered_set<int> VALID_COMMANDS = {
    static_cast<int>(Command::CMD_START),
    static_cast<int>(Command::CMD_STOP),
    static_cast<int>(Command::CMD_PAUSE),
    static_cast<int>(Command::CMD_RESUME),
};

Command ReadCommand(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    if (VALID_COMMANDS.find(value) == VALID_COMMANDS.end()) {
        LOGE("Invalid command value: %d", value);
        return Command::CMD_START;
    }
    return static_cast<Command>(value);
}
```

## 检测范围

检查以下模式：

1. `static_cast<EnumType>(parcel.ReadInt32())`
2. `static_cast<EnumType>(parcel.ReadUint32())`
3. `(EnumType)parcel.ReadInt32()`
4. 隐式枚举转换

## 检测要点

1. 识别`enum`和`enum class`定义
2. 追踪Parcel读取变量到枚举转换
3. 检查是否进行了值有效性验证
4. 识别`static_cast`和C风格转换
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: Parcel读取的不可信整数
- **RISK_TYPE**: 无效枚举值转换
- **RISK_PATH**: 不可信数据 -> 枚举转换 -> 未定义行为
- **IMPACT_POINT**: 程序逻辑错误、安全漏洞

## 影响分析（ImpactAnalysis）

- **Trigger**: Parcel数据直接转换为枚举类型
- **Propagation**: 无效枚举值导致switch/default分支异常
- **Consequence**: 未定义行为、程序崩溃、安全漏洞
- **Mitigation**: 转换前验证值在枚举范围内

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有验证逻辑 | 存在switch/范围检查 | 不报 |
| 内部枚举 | 仅在内部使用，非外部输入 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_005_trigger.cpp
enum class Color { RED = 0, GREEN = 1, BLUE = 2 };

Color trigger_bad_1(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    return static_cast<Color>(value);  // 应该报：未验证
}

enum Status { OK = 0, ERROR = 1 };

Status trigger_bad_2(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    return (Status)value;  // 应该报：C风格转换未验证
}

void trigger_bad_3(Parcel& parcel)
{
    enum class Mode { READ, WRITE };
    Mode mode = static_cast<Mode>(parcel.ReadInt32());  // 应该报：未验证
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_005_safe.cpp
enum class Color { RED = 0, GREEN = 1, BLUE = 2 };

Color safe_good_1(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    if (value >= 0 && value <= 2) {  // 安全：有验证
        return static_cast<Color>(value);
    }
    return Color::RED;
}

Color safe_good_2(Parcel& parcel)
{
    int value = parcel.ReadInt32();
    switch (value) {  // 安全：switch验证
        case 0: return Color::RED;
        case 1: return Color::GREEN;
        case 2: return Color::BLUE;
        default: return Color::RED;
    }
}

// NOPROTECT: 内部使用
enum Status { OK, ERROR };
Status noprotect_case(Parcel& parcel)
{
    return static_cast<Status>(parcel.ReadInt32());
}
```