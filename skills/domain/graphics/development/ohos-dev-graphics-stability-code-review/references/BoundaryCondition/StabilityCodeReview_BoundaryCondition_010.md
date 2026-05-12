---
rule_id: "StabilityCodeReview_BoundaryCondition_010"
name: "使用json库获取键值后，在进行类型转换前应先校验参数类型"
category: "边界条件"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 使用json库获取键值后，在进行类型转换前应先校验参数类型

## 问题描述

获取json值后直接进行类型转换，未校验实际类型是否与期望类型匹配，可能导致类型转换异常、数据错误或程序崩溃。恶意构造的json数据可能包含错误类型，造成服务异常。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：获取值后直接转换类型
void ProcessValue(const Json::Value& data)
{
    int count = data["count"].asInt();  // 危险：未检查是否为int类型
    std::string name = data["name"].asString();  // 危险：未检查是否为string类型
}

// 错误示例2：假设类型进行转换
void ParseConfig(const Json::Value& config)
{
    double value = config["value"].asDouble();  // 危险：可能是int或string
    bool enabled = config["enabled"].asBool();  // 危险：可能是string "true"
}

// 错误示例3：强制类型转换
void HandleData(const Json::Value& json)
{
    const Json::Value& arr = json["items"];
    for (int i = 0; i < arr.size(); i++) {
        std::string item = arr[i].asString();  // 危险：元素可能不是string
    }
}

// 错误示例4：static_cast转换
void ConvertValue(const Json::Value& data)
{
    int64_t id = static_cast<int64_t>(data["id"].asInt64());  // 危险：未检查类型
    float rate = static_cast<float>(data["rate"].asDouble());  // 危险：未检查类型
}
```

### ✅ 修复方案

```cpp
// 正确示例1：转换前检查类型
void ProcessValue(const Json::Value& data)
{
    if (!data["count"].isInt()) {
        LOGE("'count' is not an integer");
        return;
    }
    int count = data["count"].asInt();
    
    if (!data["name"].isString()) {
        LOGE("'name' is not a string");
        return;
    }
    std::string name = data["name"].asString();
}

// 正确示例2：使用isXxx系列方法
void ParseConfig(const Json::Value& config)
{
    if (config["value"].isDouble()) {
        double value = config["value"].asDouble();
    } else if (config["value"].isInt()) {
        double value = static_cast<double>(config["value"].asInt());
    } else if (config["value"].isString()) {
        // 处理字符串转换
    } else {
        LOGE("Invalid 'value' type");
    }
    
    if (config["enabled"].isBool()) {
        bool enabled = config["enabled"].asBool();
    } else if (config["enabled"].isString()) {
        bool enabled = (config["enabled"].asString() == "true");
    }
}

// 正确示例3：数组元素类型检查
void HandleData(const Json::Value& json)
{
    const Json::Value& arr = json["items"];
    if (!arr.isArray()) {
        LOGE("'items' is not an array");
        return;
    }
    for (int i = 0; i < arr.size(); i++) {
        if (!arr[i].isString()) {
            LOGE("Item %d is not string", i);
            continue;
        }
        std::string item = arr[i].asString();
    }
}

// 正确示例4：结合null检查
void ConvertValue(const Json::Value& data)
{
    if (data["id"].isNull()) {
        LOGE("'id' is null");
        return;
    }
    if (!data["id"].isInt64() && !data["id"].isInt()) {
        LOGE("'id' is not an integer type");
        return;
    }
    int64_t id = data["id"].asInt64();
}
```

## 检测范围

检查以下类型转换方法：

- `asString()` - 转换为字符串
- `asInt()`、`asInt64()` - 转换为整数
- `asUInt()`、`asUInt64()` - 转换为无符号整数
- `asDouble()`、`asFloat()` - 转换为浮点数
- `asBool()` - 转换为布尔值
- `asArray()` - 转换为数组
- `asObject()` - 转换为对象
- `static_cast<T>(value.asXxx())` - 强制类型转换

## 检测要点

1. 识别 `.asXxx()` 类型转换调用
2. 检查是否在转换前调用了对应的 `isXxx()` 方法
3. 检查是否使用了安全的默认值方法
4. 检查 `static_cast` 前是否有类型校验
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: json值类型转换
- **RISK_TYPE**: 类型转换异常
- **RISK_PATH**: 未校验类型 -> 强制转换 -> 数据错误或异常
- **IMPACT_POINT**: 数据损坏、程序崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: 类型不匹配时进行强制转换
- **Propagation**: 数据被错误解释或抛出异常
- **Consequence**: 数据损坏、程序异常、服务不可用
- **Mitigation**: 转换前使用 `isXxx()` 方法校验类型

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有类型检查 | 存在 isXxx() 调用 | 不报 |
| 使用get默认值 | 使用 .get() 安全方法 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_010_trigger.cpp
void trigger_bad_1(const Json::Value& data)
{
    int count = data["count"].asInt();  // 应该报：未检查类型
}

void trigger_bad_2(const Json::Value& config)
{
    std::string name = config["name"].asString();  // 应该报：未检查类型
}

void trigger_bad_3(const Json::Value& json)
{
    double value = json["value"].asDouble();  // 应该报：未检查类型
}

void trigger_bad_4(const Json::Value& arr)
{
    for (int i = 0; i < arr.size(); i++) {
        std::string item = arr[i].asString();  // 应该报：未检查元素类型
    }
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_010_safe.cpp
void safe_good_1(const Json::Value& data)
{
    if (data["count"].isInt()) {  // 安全：有类型检查
        int count = data["count"].asInt();
    }
}

void safe_good_2(const Json::Value& config)
{
    if (config.isMember("name") && config["name"].isString()) {  // 安全：有检查
        std::string name = config["name"].asString();
    }
}

void safe_good_3(const Json::Value& json)
{
    if (json["value"].isDouble() || json["value"].isInt()) {  // 安全：有类型检查
        double value = json["value"].asDouble();
    }
}

// NOPROTECT: 已确认数据格式
void noprotect_case(const Json::Value& data)
{
    int id = data["id"].asInt();  // 已确认类型正确
}
```