---
rule_id: "StabilityCodeReview_BoundaryCondition_001"
name: "Parcel数据不可作为循环或递归条件"
category: "边界条件"
severity: "CRITICAL"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Parcel数据不可作为循环或递归条件

## 问题描述

从Parcel中读取的数据不可信，不能直接作为循环或递归的条件，必须进行上限保护处理。恶意构造的Parcel数据可能包含超大数值，导致死循环、栈溢出或拒绝服务攻击。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：Parcel数据直接作为循环条件
void ReadDataFromParcel(Parcel& parcel)
{
    int count = parcel.ReadInt32();  // 不可信数据
    for (int i = 0; i < count; i++) {  // 危险：count可能为超大值
        ProcessItem(parcel);
    }
}

// 错误示例2：Parcel数据作为递归深度
void ProcessNestedData(Parcel& parcel, int depth)
{
    if (depth <= 0) return;
    int count = parcel.ReadInt32();
    for (int i = 0; i < count; i++) {  // 嵌套循环，可能深度爆炸
        ProcessNestedData(parcel, depth - 1);
    }
}

// 错误示例3：while循环使用Parcel数据
void ReadMessages(Parcel& parcel)
{
    int32_t msgCount = parcel.ReadInt32();
    while (msgCount > 0) {  // 危险：msgCount可能为负数或超大值
        ProcessMessage(parcel);
        msgCount--;
    }
}

// 错误示例4：递归函数使用Parcel数据作为终止条件
struct TreeNode {
    int value;
    std::vector<TreeNode*> children;
};

TreeNode* BuildTree(Parcel& parcel)
{
    int childCount = parcel.ReadInt32();  // 不可信数据
    TreeNode* node = new TreeNode();
    for (int i = 0; i < childCount; i++) {  // 危险：可能构造超大树
        node->children.push_back(BuildTree(parcel));  // 递归深度不可控
    }
    return node;
}
```

### ✅ 修复方案

```cpp
// 正确示例1：添加上限保护（实际代码中的动态上限）
void ReadDataFromParcel(Parcel& parcel)
{
    int32_t commandSize = 0;
    // 关键：先检查Parcel读取是否成功
    if (!parcel.ReadInt32(commandSize)) {
        ROSEN_LOGE("cannot read commandSize");
        return false;
    }
    
    // 关键：使用动态上限而非仅常量上限
    size_t readableSize = parcel.GetReadableBytes();
    size_t len = static_cast<size_t>(commandSize);
    
    // 多重检查：动态上限 + 容器上限
    if (len > readableSize || len > payload_.max_size()) {
        ROSEN_LOGE("Failed read vector, size:%zu, readAbleSize:%zu", len, readableSize);
        return false;
    }
    
    for (size_t i = 0; i < len; i++) {  // 安全：已校验len不超过readableSize
        ProcessItem(parcel);
    }
}

// 正确示例1b：常量上限保护（适用于简单场景）
constexpr int MAX_ITEM_COUNT = 1000;

void ReadSimpleData(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_ITEM_COUNT) {  // 常量上限
        LOGE("Invalid count: %d, max allowed: %d", count, MAX_ITEM_COUNT);
        return;
    }
    for (int i = 0; i < count; i++) {
        ProcessItem(parcel);
    }
}

// 正确示例2：递归深度限制
constexpr int MAX_RECURSION_DEPTH = 10;
constexpr int MAX_CHILD_COUNT = 100;

void ProcessNestedData(Parcel& parcel, int depth)
{
    if (depth <= 0 || depth > MAX_RECURSION_DEPTH) {
        LOGE("Invalid recursion depth: %d", depth);
        return;
    }
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_CHILD_COUNT) {
        LOGE("Invalid count: %d", count);
        return;
    }
    for (int i = 0; i < count; i++) {
        ProcessNestedData(parcel, depth - 1);
    }
}

// 正确示例3：使用安全的循环控制
constexpr int32_t MAX_MESSAGE_COUNT = 500;

void ReadMessages(Parcel& parcel)
{
    int32_t msgCount = parcel.ReadInt32();
    if (msgCount < 0 || msgCount > MAX_MESSAGE_COUNT) {
        LOGE("Invalid message count: %d", msgCount);
        return;
    }
    for (int32_t i = 0; i < msgCount; i++) {
        ProcessMessage(parcel);
    }
}

// 正确示例4：限制树结构和递归深度
constexpr int MAX_TREE_DEPTH = 8;
constexpr int MAX_TREE_CHILDREN = 20;

TreeNode* BuildTree(Parcel& parcel, int currentDepth)
{
    if (currentDepth > MAX_TREE_DEPTH) {
        LOGE("Tree depth exceeded: %d", currentDepth);
        return nullptr;
    }
    int childCount = parcel.ReadInt32();
    if (childCount < 0 || childCount > MAX_TREE_CHILDREN) {
        LOGE("Invalid child count: %d", childCount);
        return nullptr;
    }
    TreeNode* node = new TreeNode();
    for (int i = 0; i < childCount; i++) {
        TreeNode* child = BuildTree(parcel, currentDepth + 1);
        if (child != nullptr) {
            node->children.push_back(child);
        }
    }
    return node;
}
```

## 检测范围

检查以下模式：

1. 从Parcel读取数据后直接用于`for`循环
2. 从Parcel读取数据后直接用于`while`循环
3. 从Parcel读取数据后直接用于递归终止条件
4. 从Parcel读取数据后用于嵌套循环控制

## 检测要点

1. 识别Parcel读取函数：`ReadInt32`, `ReadInt64`, `ReadUint32`, `ReadUint64`等
2. 跟踪读取的变量是否用于循环条件
3. 检查是否进行了上限保护
4. 检查递归函数是否限制递归深度
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: Parcel读取的不可信数据
- **RISK_TYPE**: 边界条件缺失
- **RISK_PATH**: 不可信数据 -> 循环/递归条件 -> 无限循环/栈溢出
- **IMPACT_POINT**: 系统资源耗尽、拒绝服务

## 影响分析（ImpactAnalysis）

- **Trigger**: 使用Parcel数据作为循环或递归条件
- **Propagation**: 恶意构造超大数值导致无限循环或深度递归
- **Consequence**: CPU资源耗尽、栈溢出、系统崩溃
- **Mitigation**: 添加数值上限检查，限制循环次数和递归深度

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有上限检查 | 存在常量比较或条件判断 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_001_trigger.cpp
void trigger_bad_1(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    for (int i = 0; i < count; i++) {  // 应该报：无上限保护
        ProcessItem(parcel);
    }
}

void trigger_bad_2(Parcel& parcel)
{
    int32_t n = parcel.ReadInt32();
    while (n > 0) {  // 应该报：无上限保护
        HandleItem(parcel);
        n--;
    }
}

void trigger_bad_3(Parcel& parcel)
{
    uint32_t depth = parcel.ReadUint32();
    RecurseProcess(parcel, depth);  // 应该报：递归深度未限制
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_001_safe.cpp
constexpr int MAX_COUNT = 1000;

void safe_good_1(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_COUNT) {  // 安全：有上限保护
        LOGE("Invalid count");
        return;
    }
    for (int i = 0; i < count; i++) {
        ProcessItem(parcel);
    }
}

void safe_good_2(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    count = std::min(count, MAX_COUNT);  // 安全：限制上限
    for (int i = 0; i < count; i++) {
        ProcessItem(parcel);
    }
}

// NOPROTECT: 特殊场景需要处理大数量
void noprotect_case(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    for (int i = 0; i < count; i++) {
        ProcessItem(parcel);
    }
}
```