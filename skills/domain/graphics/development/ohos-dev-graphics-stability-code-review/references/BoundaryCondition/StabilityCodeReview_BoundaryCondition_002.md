---
rule_id: "StabilityCodeReview_BoundaryCondition_002"
name: "Parcel数据不可直接作为数组下标"
category: "边界条件"
severity: "CRITICAL"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Parcel数据不可直接作为数组下标

## 问题描述

从Parcel中读取的不可信数据不可以直接作为固定大小数组的下标值访问，否则可能造成数组越界访问，导致内存破坏、程序崩溃或安全漏洞。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：Parcel数据直接作为数组下标
constexpr int BUFFER_SIZE = 100;

void ProcessBuffer(Parcel& parcel)
{
    int index = parcel.ReadInt32();  // 不可信数据
    int buffer[BUFFER_SIZE];
    int value = buffer[index];  // 危险：index可能越界
}

// 错误示例2：Parcel数据用于多维数组访问
void ProcessMatrix(Parcel& parcel)
{
    int matrix[10][10];
    int row = parcel.ReadInt32();
    int col = parcel.ReadInt32();
    int value = matrix[row][col];  // 危险：row/col可能越界
}

// 错误示例3：Parcel数据作为数组索引赋值
void SetArrayValue(Parcel& parcel)
{
    int arr[50];
    int idx = parcel.ReadInt32();
    arr[idx] = 100;  // 危险：越界写入
}

// 错误示例4：全局数组使用Parcel下标
int g_data[256];

void UpdateGlobalData(Parcel& parcel)
{
    int pos = parcel.ReadInt32();
    g_data[pos] = parcel.ReadInt32();  // 危险：越界访问全局数组
}

// 错误示例5：类成员数组使用Parcel下标
class DataHandler {
private:
    int data_[128];
public:
    void Handle(Parcel& parcel) {
        int idx = parcel.ReadInt32();
        data_[idx] = 0;  // 危险：越界访问成员数组
    }
};
```

### ✅ 修复方案

```cpp
// 正确示例1：添加边界检查
constexpr int BUFFER_SIZE = 100;

void ProcessBuffer(Parcel& parcel)
{
    int index = parcel.ReadInt32();
    if (index < 0 || index >= BUFFER_SIZE) {
        LOGE("Invalid index: %d, valid range [0, %d)", index, BUFFER_SIZE);
        return;
    }
    int buffer[BUFFER_SIZE];
    int value = buffer[index];
}

// 正确示例2：多维数组边界检查
void ProcessMatrix(Parcel& parcel)
{
    constexpr int ROWS = 10;
    constexpr int COLS = 10;
    int matrix[ROWS][COLS];
    
    int row = parcel.ReadInt32();
    int col = parcel.ReadInt32();
    
    if (row < 0 || row >= ROWS || col < 0 || col >= COLS) {
        LOGE("Invalid matrix index: [%d][%d]", row, col);
        return;
    }
    int value = matrix[row][col];
}

// 正确示例3：安全的数组赋值
constexpr int ARRAY_SIZE = 50;

void SetArrayValue(Parcel& parcel)
{
    int arr[ARRAY_SIZE];
    int idx = parcel.ReadInt32();
    if (idx >= 0 && idx < ARRAY_SIZE) {
        arr[idx] = 100;
    } else {
        LOGE("Array index out of bounds: %d", idx);
    }
}

// 正确示例4：全局数组的边界检查
constexpr int GLOBAL_DATA_SIZE = 256;
int g_data[GLOBAL_DATA_SIZE];

void UpdateGlobalData(Parcel& parcel)
{
    int pos = parcel.ReadInt32();
    if (pos < 0 || pos >= GLOBAL_DATA_SIZE) {
        LOGE("Invalid position: %d", pos);
        return;
    }
    g_data[pos] = parcel.ReadInt32();
}

// 正确示例5：使用安全的访问函数
class DataHandler {
private:
    static constexpr int DATA_SIZE = 128;
    int data_[DATA_SIZE];
    
    bool IsValidIndex(int idx) const {
        return idx >= 0 && idx < DATA_SIZE;
    }
    
public:
    void Handle(Parcel& parcel) {
        int idx = parcel.ReadInt32();
        if (!IsValidIndex(idx)) {
            LOGE("Invalid index: %d", idx);
            return;
        }
        data_[idx] = 0;
    }
};
```

## 检测范围

检查以下模式：

1. Parcel读取值直接用于数组下标访问：`array[parcel.ReadInt32()]`
2. Parcel读取的变量用于数组下标：`int idx = parcel.ReadInt32(); array[idx]`
3. 成员数组使用Parcel数据作为下标
4. 多维数组使用Parcel数据作为索引

## 检测要点

1. 识别固定大小数组的定义
2. 追踪Parcel读取变量到数组访问
3. 检查是否进行了边界检查
4. 识别`array[index]`和`array[index] = value`模式
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: Parcel读取的不可信数据
- **RISK_TYPE**: 数组越界访问
- **RISK_PATH**: 不可信数据 -> 数组下标 -> 越界读写
- **IMPACT_POINT**: 内存破坏、程序崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: Parcel数据直接作为数组下标
- **Propagation**: 恶意构造超大或负数索引导致越界访问
- **Consequence**: 内存读取越界、内存写入越界、任意代码执行
- **Mitigation**: 使用前检查索引是否在有效范围内

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有边界检查 | 存在范围判断条件 | 不报 |
| 动态数组 | 使用std::vector等容器 | 容器自身有边界检查 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_002_trigger.cpp
void trigger_bad_1(Parcel& parcel)
{
    int buffer[100];
    int idx = parcel.ReadInt32();
    int val = buffer[idx];  // 应该报：无边界检查
}

void trigger_bad_2(Parcel& parcel)
{
    int arr[50];
    int pos = parcel.ReadInt32();
    arr[pos] = 100;  // 应该报：无边界检查
}

void trigger_bad_3(Parcel& parcel)
{
    int matrix[10][10];
    int row = parcel.ReadInt32();
    int col = parcel.ReadInt32();
    int val = matrix[row][col];  // 应该报：无边界检查
}

class Handler {
    int data_[128];
public:
    void trigger_bad_4(Parcel& parcel) {
        int idx = parcel.ReadInt32();
        data_[idx] = 0;  // 应该报：成员数组越界
    }
};
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_002_safe.cpp
void safe_good_1(Parcel& parcel)
{
    int buffer[100];
    int idx = parcel.ReadInt32();
    if (idx >= 0 && idx < 100) {  // 安全：有边界检查
        int val = buffer[idx];
    }
}

void safe_good_2(Parcel& parcel)
{
    std::vector<int> vec(100);
    int idx = parcel.ReadInt32();
    // 安全：vector的at()会进行边界检查
    if (idx >= 0 && static_cast<size_t>(idx) < vec.size()) {
        int val = vec[idx];
    }
}

void safe_good_3(Parcel& parcel)
{
    constexpr int SIZE = 50;
    int arr[SIZE];
    int pos = parcel.ReadInt32();
    if (pos < 0 || pos >= SIZE) {  // 安全：边界检查
        LOGE("Invalid pos");
        return;
    }
    arr[pos] = 100;
}

// NOPROTECT: 测试代码
void noprotect_case(Parcel& parcel)
{
    int arr[10];
    int idx = parcel.ReadInt32();
    arr[idx] = 100;
}
```