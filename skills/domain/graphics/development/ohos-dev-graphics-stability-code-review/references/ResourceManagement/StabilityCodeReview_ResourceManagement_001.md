---
rule_id: "StabilityCodeReview_ResourceManagement_001"
name: "反序列化内存泄漏"
category: "资源管理"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 反序列化内存泄漏

## 问题描述

在反序列化过程中申请的内存在异常分支未及时释放，造成内存泄漏。反序列化代码中常见的模式是先申请内存，然后读取数据填充，如果读取过程中发生错误，需要正确释放已申请的内存，否则会导致内存泄漏。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：反序列化失败后内存未释放
Data* DeserializeData(Parcel& parcel)
{
    Data* data = new Data();  // 申请内存
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_COUNT) {
        LOGE("Invalid count: %d", count);
        return nullptr;  // 错误：返回nullptr，data内存泄漏
    }
    data->count = count;
    data->name = parcel.ReadString();
    return data;
}

// 场景2：嵌套反序列化内存泄漏
TreeNode* DeserializeTree(Parcel& parcel)
{
    TreeNode* node = new TreeNode();  // 申请内存
    node->id = parcel.ReadInt32();
    int childCount = parcel.ReadInt32();
    
    if (childCount < 0) {
        LOGE("Invalid childCount");
        return nullptr;  // 错误：node内存泄漏
    }
    
    for (int i = 0; i < childCount; i++) {
        TreeNode* child = DeserializeTree(parcel);
        if (child == nullptr) {
            // 错误：child反序列化失败，但node已创建
            // 未清理其他已添加的children
            return nullptr;  // node和已添加的children全部泄漏
        }
        node->children.push_back(child);
    }
    return node;
}

// 场景3：数组反序列化部分失败泄漏
int* DeserializeArray(Parcel& parcel, int& size)
{
    size = parcel.ReadInt32();
    if (size < 0 || size > MAX_SIZE) {
        return nullptr;  // 此处正确，内存未申请
    }
    
    int* arr = new int[size];  // 申请内存
    for (int i = 0; i < size; i++) {
        int value = parcel.ReadInt32();
        if (value < 0) {  // 业务校验失败
            LOGE("Invalid value at index %d", i);
            return nullptr;  // 错误：arr内存泄漏
        }
        arr[i] = value;
    }
    return arr;
}

// 场景4：对象成员反序列化失败泄漏
class Config {
public:
    char* buffer_;
    int bufferSize_;
    
    bool Deserialize(Parcel& parcel) {
        bufferSize_ = parcel.ReadInt32();
        if (bufferSize_ <= 0 || bufferSize_ > MAX_BUFFER) {
            return false;  // 正确：buffer_未申请
        }
        
        buffer_ = new char[bufferSize_];  // 申请内存
        if (!parcel.ReadBuffer(buffer_, bufferSize_)) {
            LOGE("ReadBuffer failed");
            return false;  // 错误：buffer_内存泄漏
        }
        return true;
    }
};
```

### ✅ 修复方案

```cpp
// 修复场景1：使用智能指针自动管理
Data* DeserializeData(Parcel& parcel)
{
    std::unique_ptr<Data> data(new Data());  // 使用unique_ptr管理
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_COUNT) {
        LOGE("Invalid count: %d", count);
        return nullptr;  // unique_ptr自动释放
    }
    data->count = count;
    data->name = parcel.ReadString();
    return data.release();  // 成功时释放所有权
}

// 修复场景2：嵌套反序列化安全清理
TreeNode* DeserializeTree(Parcel& parcel)
{
    std::unique_ptr<TreeNode> node(new TreeNode());
    node->id = parcel.ReadInt32();
    int childCount = parcel.ReadInt32();
    
    if (childCount < 0) {
        LOGE("Invalid childCount");
        return nullptr;  // unique_ptr自动释放node
    }
    
    for (int i = 0; i < childCount; i++) {
        TreeNode* child = DeserializeTree(parcel);
        if (child == nullptr) {
            // unique_ptr会自动清理node和已添加的children
            return nullptr;
        }
        node->children.push_back(child);
    }
    return node.release();
}

// 修复场景3：数组反序列化安全清理
int* DeserializeArray(Parcel& parcel, int& size)
{
    size = parcel.ReadInt32();
    if (size < 0 || size > MAX_SIZE) {
        return nullptr;
    }
    
    std::unique_ptr<int[]> arr(new int[size]);
    for (int i = 0; i < size; i++) {
        int value = parcel.ReadInt32();
        if (value < 0) {
            LOGE("Invalid value at index %d", i);
            return nullptr;  // unique_ptr自动释放
        }
        arr[i] = value;
    }
    return arr.release();
}

// 修复场景4：对象成员使用智能指针
class Config {
public:
    std::unique_ptr<char[]> buffer_;
    int bufferSize_;
    
    bool Deserialize(Parcel& parcel) {
        bufferSize_ = parcel.ReadInt32();
        if (bufferSize_ <= 0 || bufferSize_ > MAX_BUFFER) {
            return false;
        }
        
        buffer_.reset(new char[bufferSize_]);  // unique_ptr管理
        if (!parcel.ReadBuffer(buffer_.get(), bufferSize_)) {
            LOGE("ReadBuffer failed");
            buffer_.reset();  // 或自动清理
            return false;
        }
        return true;
    }
};

// 修复场景5：手动释放内存
Data* DeserializeDataManual(Parcel& parcel)
{
    Data* data = new Data();
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_COUNT) {
        LOGE("Invalid count: %d", count);
        delete data;  // 手动释放
        return nullptr;
    }
    data->count = count;
    data->name = parcel.ReadString();
    return data;
}

// 修复场景6：使用goto统一清理（C风格）
int* DeserializeArrayGoto(Parcel& parcel, int& size)
{
    int* arr = nullptr;
    
    size = parcel.ReadInt32();
    if (size < 0 || size > MAX_SIZE) {
        goto error;
    }
    
    arr = new int[size];
    for (int i = 0; i < size; i++) {
        int value = parcel.ReadInt32();
        if (value < 0) {
            LOGE("Invalid value");
            goto error;
        }
        arr[i] = value;
    }
    return arr;
    
error:
    if (arr) {
        delete[] arr;
    }
    size = 0;
    return nullptr;
}
```

## 检测范围

检查以下模式：

- `new/delete` 在反序列化函数中的使用
- `malloc/free` 在反序列化函数中的使用
- 异常分支（`return nullptr`, `return false`, `return -1`等）前未释放内存
- 反序列化函数中多个内存申请点的清理

## 检测要点

1. 识别反序列化函数（包含`Parcel`, `Deserialize`, `Unmarshal`, `Read`等关键字）
2. 检测内存申请操作（`new`, `malloc`, `calloc`）
3. 检测异常返回分支
4. 检查异常分支前是否有对应的释放操作
5. 排除使用智能指针的情况

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：反序列化函数中申请的内存
- **RISK_TYPE**：内存泄漏
- **RISK_PATH**：申请内存 -> 异常分支 -> 未释放返回 -> 内存泄漏
- **IMPACT_POINT**：内存资源耗尽、程序稳定性下降

## 影响分析（ImpactAnalysis）

- **Trigger**：反序列化过程中遇到异常数据或读取失败
- **Propagation**：异常分支返回时未释放已申请内存
- **Consequence**：内存泄漏累积、系统内存耗尽、性能下降
- **Mitigation**：使用智能指针自动管理或手动释放内存

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 使用智能指针 | unique_ptr/shared_ptr | 不报 |
| 有delete释放 | 异常分支前有delete/free | 不报 |
| 使用RAII类 | 封装了清理的类对象 | 不报 |
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ResourceManagement_001_trigger.cpp
Data* trigger_bad_1(Parcel& parcel)
{
    Data* data = new Data();  // 应该报：new后异常返回未释放
    int count = parcel.ReadInt32();
    if (count < 0) {
        return nullptr;  // 内存泄漏
    }
    data->count = count;
    return data;
}

int* trigger_bad_2(Parcel& parcel)
{
    int* arr = (int*)malloc(100 * sizeof(int));  // 应该报：malloc后异常返回未释放
    int value = parcel.ReadInt32();
    if (value < 0) {
        return nullptr;  // 内存泄漏
    }
    arr[0] = value;
    return arr;
}
```

### 安全用例（不应该报）

```cpp
// test_ResourceManagement_001_safe.cpp
Data* safe_good_1(Parcel& parcel)
{
    std::unique_ptr<Data> data(new Data());  // 安全：使用智能指针
    int count = parcel.ReadInt32();
    if (count < 0) {
        return nullptr;  // unique_ptr自动释放
    }
    data->count = count;
    return data.release();
}

Data* safe_good_2(Parcel& parcel)
{
    Data* data = new Data();
    int count = parcel.ReadInt32();
    if (count < 0) {
        delete data;  // 安全：手动释放
        return nullptr;
    }
    data->count = count;
    return data;
}

// NOPROTECT: 特殊场景
// NOPROTECT: 测试代码
Data* noprotect_case(Parcel& parcel)
{
    Data* data = new Data();
    if (parcel.ReadInt32() < 0) {
        return nullptr;
    }
    return data;
}
```