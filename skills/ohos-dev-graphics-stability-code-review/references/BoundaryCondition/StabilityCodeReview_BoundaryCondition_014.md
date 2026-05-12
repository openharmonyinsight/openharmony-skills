---
rule_id: "StabilityCodeReview_BoundaryCondition_014"
name: "JSON解析安全风险"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# JSON解析安全风险

## 问题描述

JSON解析存在多种安全风险：解析深度过大导致栈溢出、超大JSON导致内存耗尽、未捕获解析异常、键不存在导致的空指针访问、类型不匹配导致的类型混淆、以及数值溢出问题。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：无深度限制导致栈溢出
void ParseNestedJson(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(jsonStr, root);  // 错误：未限制解析深度，恶意嵌套JSON可致栈溢出
    
    ProcessJson(root);
}

// 场景2：超大JSON未限制导致内存耗尽
void LoadLargeJson(const char* filePath)
{
    std::ifstream file(filePath);
    Json::Value root;
    Json::Reader reader;
    reader.parse(file, root);  // 错误：未限制JSON大小，超大文件可耗尽内存
}

// 场景3：未捕获解析异常
void ParseJsonData(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    if (!reader.parse(jsonStr, root)) {
        // 错误：parse失败但未记录错误信息，继续使用root可能访问无效数据
        ProcessData(root);
    }
}

// 场景4：键不存在导致空指针访问
void GetValueFromJson(const Json::Value& root)
{
    int id = root["id"].asInt();  // 错误：键可能不存在，访问无效Json::Value
    std::string name = root["name"].asString();  // 错误：键可能不存在
}

// 场景5：类型不匹配导致错误
void ParseTypedData(const Json::Value& root)
{
    int count = root["count"].asInt();  // 错误：count可能是字符串，类型混淆
    double value = root["value"].asDouble();  // 错误：value可能是数组
}

// 场景6：数值溢出
void ParseLargeNumber(const Json::Value& root)
{
    int32_t id = root["id"].asInt();  // 错误：id可能超过int32_t范围，溢出
    size_t size = root["size"].asUInt();  // 错误：size可能是负数或超大值
}

// 场景7：数组越界访问
void ParseArrayData(const Json::Value& root)
{
    const Json::Value& arr = root["items"];
    for (int i = 0; i < 10; i++) {  // 错误：固定循环次数，arr可能少于10个元素
        ProcessItem(arr[i]);  // 错误：可能越界访问
    }
}

// 场景8：未检查解析成功状态
void UseJsonResult(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(jsonStr, root);  // 错误：未检查parse返回值
    
    int value = root["value"].asInt();  // root可能无效
}
```

### ✅ 修复方案

```cpp
// 修复场景1：限制解析深度
void ParseNestedJson(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    
    Json::Features features;
    features.allowNestedDepth_ = 100;  // 正确：限制嵌套深度
    reader.parse(jsonStr, root, features);
    
    ProcessJson(root);
}

// 修复场景2：限制JSON大小
void LoadLargeJson(const char* filePath)
{
    std::ifstream file(filePath);
    
    // 正确：限制文件大小
    file.seekg(0, std::ios::end);
    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);
    
    const size_t MAX_JSON_SIZE = 10 * 1024 * 1024;  // 10MB限制
    if (size > MAX_JSON_SIZE) {
        LOGE("JSON file too large: %lld", size);
        return;
    }
    
    Json::Value root;
    Json::Reader reader;
    reader.parse(file, root);
}

// 修复场景3：捕获并处理解析错误
void ParseJsonData(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    
    if (!reader.parse(jsonStr, root)) {
        LOGE("JSON parse failed: %s", reader.getFormattedErrorMessages().c_str());  // 正确：记录错误信息
        return;
    }
    
    ProcessData(root);
}

// 修复场景4：检查键存在性
void GetValueFromJson(const Json::Value& root)
{
    if (!root.isMember("id") || !root["id"].isInt()) {  // 正确：检查键存在和类型
        LOGE("Missing or invalid 'id' field");
        return;
    }
    int id = root["id"].asInt();
    
    if (!root.isMember("name") || !root["name"].isString()) {  // 正确：检查键存在和类型
        LOGE("Missing or invalid 'name' field");
        return;
    }
    std::string name = root["name"].asString();
}

// 修复场景5：检查类型匹配
void ParseTypedData(const Json::Value& root)
{
    if (root.isMember("count") && root["count"].isInt()) {  // 正确：检查类型
        int count = root["count"].asInt();
    }
    
    if (root.isMember("value") && root["value"].isDouble()) {  // 正确：检查类型
        double value = root["value"].asDouble();
    }
}

// 修复场景6：检查数值范围
void ParseLargeNumber(const Json::Value& root)
{
    if (root.isMember("id") && root["id"].isInt()) {
        Json::Int64 id64 = root["id"].asInt64();  // 正确：使用Int64避免溢出
        
        if (id64 >= INT32_MIN && id64 <= INT32_MAX) {  // 正确：检查范围
            int32_t id = static_cast<int32_t>(id64);
        }
    }
    
    if (root.isMember("size") && root["size"].isUInt()) {
        Json::UInt64 size64 = root["size"].asUInt64();  // 正确：使用UInt64
        
        if (size64 <= SIZE_MAX) {  // 正确：检查范围
            size_t size = static_cast<size_t>(size64);
        }
    }
}

// 修复场景7：检查数组大小
void ParseArrayData(const Json::Value& root)
{
    if (!root.isMember("items") || !root["items"].isArray()) {  // 正确：检查键和类型
        return;
    }
    
    const Json::Value& arr = root["items"];
    for (Json::ArrayIndex i = 0; i < arr.size(); i++) {  // 正确：使用实际大小
        ProcessItem(arr[i]);
    }
}

// 修复场景8：检查解析成功状态
void UseJsonResult(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    
    bool success = reader.parse(jsonStr, root);  // 正确：检查返回值
    if (!success) {
        LOGE("JSON parse failed");
        return;
    }
    
    if (root.isMember("value") && root["value"].isInt()) {  // 正确：检查字段
        int value = root["value"].asInt();
    }
}
```

## 检测范围

检查以下模式：

- JSON解析未限制嵌套深度
- JSON解析未限制文件/字符串大小
- JSON解析失败后继续使用root对象
- 访问JSON键前未检查键是否存在（isMember）
- 转换JSON值前未检查类型匹配（isXxx）
- 数值转换可能导致溢出（asInt转int32_t）
- JSON数组访问前未检查数组大小

## 检测要点

1. 识别JSON解析函数调用（parse、parseFromStream）
2. 检查是否有深度限制设置（allowNestedDepth）
3. 检查是否有大小限制检查
4. 检查是否检查parse返回值
5. 检查是否在访问键前调用isMember
6. 检查是否在类型转换前调用isXxx
7. 检查数组访问是否使用size()判断边界
8. 排除NOPROTECT标记

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：JSON解析操作
- **RISK_TYPE**：栈溢出/内存耗尽/空指针/类型混淆/数值溢出
- **RISK_PATH**：恶意构造JSON → 解析未限制 → 资源耗尽或数据错误 → 程序崩溃
- **IMPACT_POINT**：栈溢出崩溃、OOM崩溃、空指针崩溃、数据损坏

## 影响分析（ImpactAnalysis）

- **Trigger**：恶意构造的JSON输入触发各种安全问题
- **Propagation**：栈溢出、内存耗尽、无效数据访问、数值溢出
- **Consequence**：程序崩溃、拒绝服务、数据损坏、安全漏洞
- **Mitigation**：限制深度和大小、检查返回值、验证键和类型、使用安全的数值类型

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 有深度限制 | 设置allowNestedDepth | 不报 |
| 有大小检查 | 有文件大小判断 | 不报 |
| 有parse返回值检查 | 有 if (!parse()) | 不报 |
| 有键检查 | 有 isMember() | 不报 |
| 有类型检查 | 有 isXxx() | 不报 |
| 有数组边界检查 | 使用 arr.size() | 不报 |
| NOPROTECT标记 | // NOPROTECT 注释 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_014_trigger.cpp
void trigger_bad_1(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    reader.parse(jsonStr, root);  // 应该报：未限制深度
}

void trigger_bad_2(const Json::Value& root)
{
    int id = root["id"].asInt();  // 应该报：键未检查存在性
}

void trigger_bad_3(const Json::Value& root)
{
    int count = root["count"].asInt();  // 应该报：类型未检查
}

void trigger_bad_4(const Json::Value& root)
{
    const Json::Value& arr = root["items"];
    for (int i = 0; i < 10; i++) {
        ProcessItem(arr[i]);  // 应该报：数组越界访问
    }
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_014_safe.cpp
void safe_good_1(const std::string& jsonStr)
{
    Json::Value root;
    Json::Reader reader;
    
    Json::Features features;
    features.allowNestedDepth_ = 100;  // 安全：有深度限制
    reader.parse(jsonStr, root, features);
}

void safe_good_2(const Json::Value& root)
{
    if (root.isMember("id") && root["id"].isInt()) {  // 安全：有键和类型检查
        int id = root["id"].asInt();
    }
}

void safe_good_3(const Json::Value& root)
{
    const Json::Value& arr = root["items"];
    for (Json::ArrayIndex i = 0; i < arr.size(); i++) {  // 安全：使用size()判断边界
        ProcessItem(arr[i]);
    }
}

// NOPROTECT: 特殊场景
void noprotect_case(const Json::Value& root)
{
    int id = root["id"].asInt();  // NOPROTECT标记，不报
}
```