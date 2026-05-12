---
rule_id: "StabilityCodeReview_BoundaryCondition_003"
name: "Parcel数据不可直接作为内存申请大小"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Parcel数据不可直接作为内存申请大小

## 问题描述

从Parcel中读取的数据不可信，不能直接作为内存申请大小的值，否则可能造成内存超大申请，导致内存耗尽、程序崩溃或拒绝服务攻击。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：Parcel数据直接用于malloc
void* AllocateBuffer(Parcel& parcel)
{
    size_t size = parcel.ReadUint32();  // 不可信数据
    void* buffer = malloc(size);  // 危险：size可能为超大值
    return buffer;
}

// 错误示例2：Parcel数据用于new数组
int* CreateIntArray(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    int* arr = new int[count];  // 危险：count可能为超大值
    return arr;
}

// 错误示例3：Parcel数据用于std::vector初始化
std::vector<char> ReadVector(Parcel& parcel)
{
    uint32_t size = parcel.ReadUint32();
    std::vector<char> vec(size);  // 危险：size可能为超大值
    return vec;
}

// 错误示例4：Parcel数据用于std::string分配
std::string ReadString(Parcel& parcel)
{
    uint32_t len = parcel.ReadUint32();
    std::string str;
    str.resize(len);  // 危险：len可能为超大值
    parcel.ReadBuffer(static_cast<void*>(&str[0]), len);
    return str;
}

// 错误示例5：Parcel数据用于realloc
void* ResizeBuffer(Parcel& parcel, void* oldPtr, size_t oldSize)
{
    size_t newSize = parcel.ReadUint32();
    void* newPtr = realloc(oldPtr, newSize);  // 危险：newSize可能为超大值
    return newPtr;
}

// 错误示例6：多级内存申请叠加
void** CreateBufferArray(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    void** arr = new void*[count];  // 危险1：count可能超大
    for (int i = 0; i < count; i++) {
        size_t bufSize = parcel.ReadUint32();
        arr[i] = malloc(bufSize);  // 危险2：bufSize可能超大
    }
    return arr;
}
```

### ✅ 修复方案

```cpp
// 正确示例1：添加上限检查
constexpr size_t MAX_BUFFER_SIZE = 10 * 1024 * 1024;  // 10MB

void* AllocateBuffer(Parcel& parcel)
{
    size_t size = parcel.ReadUint32();
    if (size == 0 || size > MAX_BUFFER_SIZE) {
        LOGE("Invalid buffer size: %zu, max allowed: %zu", size, MAX_BUFFER_SIZE);
        return nullptr;
    }
    void* buffer = malloc(size);
    if (buffer == nullptr) {
        LOGE("malloc failed for size: %zu", size);
    }
    return buffer;
}

// 正确示例2：限制数组大小
constexpr int MAX_ARRAY_COUNT = 100000;

int* CreateIntArray(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    if (count <= 0 || count > MAX_ARRAY_COUNT) {
        LOGE("Invalid array count: %d, max allowed: %d", count, MAX_ARRAY_COUNT);
        return nullptr;
    }
    int* arr = new (std::nothrow) int[count];
    if (arr == nullptr) {
        LOGE("new failed for count: %d", count);
    }
    return arr;
}

// 正确示例3：安全的vector初始化
constexpr uint32_t MAX_VECTOR_SIZE = 1024 * 1024;  // 1M elements

std::vector<char> ReadVector(Parcel& parcel)
{
    uint32_t size = parcel.ReadUint32();
    if (size == 0 || size > MAX_VECTOR_SIZE) {
        LOGE("Invalid vector size: %u", size);
        return std::vector<char>();
    }
    std::vector<char> vec;
    vec.reserve(size);  // 使用reserve而非直接初始化
    return vec;
}

// 正确示例4：安全的string处理
constexpr uint32_t MAX_STRING_LEN = 1024 * 1024;  // 1MB

std::string ReadString(Parcel& parcel)
{
    uint32_t len = parcel.ReadUint32();
    if (len == 0 || len > MAX_STRING_LEN) {
        LOGE("Invalid string length: %u", len);
        return "";
    }
    std::string str;
    str.resize(len);
    if (parcel.ReadBuffer(static_cast<void*>(&str[0]), len) != len) {
        LOGE("Failed to read string data");
        return "";
    }
    return str;
}

// 正确示例5：安全的realloc
void* ResizeBuffer(Parcel& parcel, void* oldPtr, size_t oldSize)
{
    size_t newSize = parcel.ReadUint32();
    if (newSize == 0 || newSize > MAX_BUFFER_SIZE) {
        LOGE("Invalid new size: %zu", newSize);
        return oldPtr;  // 保持原有指针
    }
    void* newPtr = realloc(oldPtr, newSize);
    if (newPtr == nullptr) {
        LOGE("realloc failed");
        return oldPtr;
    }
    return newPtr;
}

// 正确示例6：分级内存申请保护
constexpr int MAX_BUFFER_COUNT = 1000;
constexpr size_t MAX_INDIVIDUAL_BUFFER_SIZE = 1024 * 1024;
constexpr size_t MAX_TOTAL_BUFFER_SIZE = 100 * 1024 * 1024;  // 100MB total

void** CreateBufferArray(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    if (count <= 0 || count > MAX_BUFFER_COUNT) {
        LOGE("Invalid buffer count: %d", count);
        return nullptr;
    }
    
    void** arr = new (std::nothrow) void*[count];
    if (arr == nullptr) {
        LOGE("Failed to allocate buffer array");
        return nullptr;
    }
    
    size_t totalAllocated = 0;
    for (int i = 0; i < count; i++) {
        size_t bufSize = parcel.ReadUint32();
        if (bufSize == 0 || bufSize > MAX_INDIVIDUAL_BUFFER_SIZE) {
            LOGE("Invalid buffer size: %zu", bufSize);
            continue;
        }
        totalAllocated += bufSize;
        if (totalAllocated > MAX_TOTAL_BUFFER_SIZE) {
            LOGE("Total allocation exceeded limit");
            break;
        }
        arr[i] = malloc(bufSize);
    }
    return arr;
}
```

## 检测范围

检查以下模式：

1. Parcel数据用于`malloc/calloc/realloc`
2. Parcel数据用于`new/new[]`
3. Parcel数据用于`std::vector`初始化
4. Parcel数据用于`std::string::resize/reserve`
5. Parcel数据用于容器`resize/reserve`

## 检测要点

1. 识别Parcel读取函数：`ReadInt32`, `ReadUint32`, `ReadInt64`, `ReadUint64`
2. 追踪读取变量到内存申请函数
3. 检查是否进行了上限保护
4. 识别`malloc`, `calloc`, `realloc`, `new`, `new[]`, `vector`, `string`等
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: Parcel读取的不可信数据
- **RISK_TYPE**: 内存超大申请
- **RISK_PATH**: 不可信数据 -> 内存申请大小 -> 内存耗尽
- **IMPACT_POINT**: 系统资源耗尽、拒绝服务

## 影响分析（ImpactAnalysis）

- **Trigger**: Parcel数据直接用于内存申请大小
- **Propagation**: 恶意构造超大数值导致大量内存申请
- **Consequence**: 内存耗尽、程序崩溃、系统不稳定
- **Mitigation**: 添加内存申请上限检查，分级限制

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有上限检查 | 存在常量比较或条件判断 | 不报 |
| 安全分配函数 | 使用自定义安全分配器 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_003_trigger.cpp
void* trigger_bad_1(Parcel& parcel)
{
    size_t size = parcel.ReadUint32();
    return malloc(size);  // 应该报：无上限检查
}

int* trigger_bad_2(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    return new int[count];  // 应该报：无上限检查
}

std::vector<int> trigger_bad_3(Parcel& parcel)
{
    uint32_t size = parcel.ReadUint32();
    return std::vector<int>(size);  // 应该报：无上限检查
}

void trigger_bad_4(Parcel& parcel)
{
    uint32_t len = parcel.ReadUint32();
    std::string str;
    str.resize(len);  // 应该报：无上限检查
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_003_safe.cpp
constexpr size_t MAX_SIZE = 10 * 1024 * 1024;

void* safe_good_1(Parcel& parcel)
{
    size_t size = parcel.ReadUint32();
    if (size == 0 || size > MAX_SIZE) {  // 安全：有上限检查
        LOGE("Invalid size");
        return nullptr;
    }
    return malloc(size);
}

int* safe_good_2(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    if (count <= 0 || count > 1000) {  // 安全：有上限检查
        LOGE("Invalid count");
        return nullptr;
    }
    return new (std::nothrow) int[count];
}

// NOPROTECT: 特殊场景需要大内存
void* noprotect_case(Parcel& parcel)
{
    size_t size = parcel.ReadUint32();
    return malloc(size);
}
```