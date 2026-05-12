---
rule_id: "StabilityCodeReview_BoundaryCondition_009"
name: "使用json库获取键值内容前应先判断类型是否匹配、键值是否存在"
category: "边界条件"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 使用json库获取键值内容前应先判断类型是否匹配、键值是否存在

## 问题描述

直接访问json对象的键值而不检查键是否存在或类型是否匹配，可能导致程序崩溃、异常抛出或数据错误。恶意构造的json数据可能包含错误的类型，导致服务不可用。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：直接访问键值不检查存在性
void ParseConfig(const Json::Value& config)
{
    std::string name = config["name"].asString();  // 危险：键可能不存在
    int port = config["port"].asInt();  // 危险：同上
}

// 错误示例2：不检查类型直接转换
void ProcessJson(const Json::Value& data)
{
    int count = data["count"].asInt();  // 危险：可能是其他类型
    std::string value = data["value"].asString();  // 危险：同上
}

// 错误示例3：嵌套json访问
void ParseNested(const Json::Value& root)
{
    int id = root["user"]["id"].asInt();  // 危险：user可能不存在
    std::string name = root["user"]["profile"]["name"].asString();  // 危险：多层不检查
}

// 错误示例4：数组访问
void ProcessArray(const Json::Value& arr, int index)
{
    std::string item = arr[index].asString();  // 危险：可能越界或类型不匹配
}
```

### ✅ 修复方案

```cpp
// 正确示例1：先检查键是否存在
void ParseConfig(const Json::Value& config)
{
    if (!config.isMember("name") || !config["name"].isString()) {
        LOGE("Invalid or missing 'name' field");
        return;
    }
    std::string name = config["name"].asString();
    
    if (!config.isMember("port") || !config["port"].isInt()) {
        LOGE("Invalid or missing 'port' field");
        return;
    }
    int port = config["port"].asInt();
}

// 正确示例2：使用安全的get方法
void ProcessJson(const Json::Value& data)
{
    int count = data.get("count", 0).asInt();  // 提供默认值
    std::string value = data.get("value", "").asString();
    
    // 或者先检查类型
    if (data.isMember("count") && data["count"].isInt()) {
        int count = data["count"].asInt();
    }
}

// 正确示例3：嵌套json安全访问
void ParseNested(const Json::Value& root)
{
    if (!root.isMember("user") || !root["user"].isObject()) {
        LOGE("Missing or invalid 'user' object");
        return;
    }
    const Json::Value& user = root["user"];
    
    if (!user.isMember("id") || !user["id"].isInt()) {
        LOGE("Missing or invalid 'user.id'");
        return;
    }
    int id = user["id"].asInt();
}

// 正确示例4：数组安全访问
void ProcessArray(const Json::Value& arr, int index)
{
    if (!arr.isArray() || index < 0 || index >= arr.size()) {
        LOGE("Invalid array or index");
        return;
    }
    if (!arr[index].isString()) {
        LOGE("Array element is not string");
        return;
    }
    std::string item = arr[index].asString();
}
```

## 检测范围

检查以下模式：

- `json["key"]` 直接访问后调用 `.asXxx()`
- `json[key]` 变量作为键访问
- 嵌套访问 `json["a"]["b"]["c"]`
- 数组访问 `json[index]`
- 类型转换方法：`asString()`、`asInt()`、`asDouble()`、`asBool()`、`asArray()`、`asObject()`

## 检测要点

1. 识别json键值访问表达式
2. 检查是否在访问前调用了 `isMember()`、`has()`、`contains()`
3. 检查是否在转换前调用了类型检查方法：`isString()`、`isInt()` 等
4. 检查是否使用了安全的 `get()` 方法
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: json对象键值访问
- **RISK_TYPE**: 键不存在/类型不匹配
- **RISK_PATH**: 直接访问键值 -> 键不存在或类型错误 -> 异常/崩溃
- **IMPACT_POINT**: 服务异常、程序崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: 访问不存在的键或类型不匹配的值
- **Propagation**: 抛出异常或返回错误默认值
- **Consequence**: 程序崩溃、服务不可用、数据错误
- **Mitigation**: 访问前检查键存在性和类型匹配性

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有检查 | 存在 isMember、isXxx 调用 | 不报 |
| 使用get方法 | 使用 .get() 安全方法 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_009_trigger.cpp
void trigger_bad_1(const Json::Value& config)
{
    std::string name = config["name"].asString();  // 应该报：未检查键存在性和类型
}

void trigger_bad_2(const Json::Value& data)
{
    int count = data["count"].asInt();  // 应该报：未检查类型
}

void trigger_bad_3(const Json::Value& root)
{
    int id = root["user"]["id"].asInt();  // 应该报：嵌套访问未检查
}

void trigger_bad_4(const Json::Value& arr, int idx)
{
    std::string item = arr[idx].asString();  // 应该报：数组访问未检查
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_009_safe.cpp
void safe_good_1(const Json::Value& config)
{
    if (config.isMember("name") && config["name"].isString()) {  // 安全：有检查
        std::string name = config["name"].asString();
    }
}

void safe_good_2(const Json::Value& data)
{
    int count = data.get("count", 0).asInt();  // 安全：使用默认值
}

void safe_good_3(const Json::Value& root)
{
    if (root.isMember("user") && root["user"].isObject()) {  // 安全：有检查
        const Json::Value& user = root["user"];
        if (user.isMember("id") && user["id"].isInt()) {
            int id = user["id"].asInt();
        }
    }
}

// NOPROTECT: 已确认数据格式正确
void noprotect_case(const Json::Value& data)
{
    std::string value = data["value"].asString();  // 已确认格式
}
```