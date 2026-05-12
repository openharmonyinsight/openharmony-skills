---
rule_id: "StabilityCodeReview_BoundaryCondition_006"
name: "Parcel序列化和反序列化必须匹配"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Parcel序列化和反序列化必须匹配

## 问题描述

Parcel的序列化和反序列化必须完全匹配，包括顺序、类型和数量。不匹配的序列化/反序列化会导致数据错误、内存越界读取或程序崩溃。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：顺序不匹配
// 序列化
void WriteData(Parcel& parcel)
{
    parcel.WriteInt32(count);     // 1. 写入count
    parcel.WriteString(name);     // 2. 写入name
    parcel.WriteBool(enabled);    // 3. 写入enabled
}

// 反序列化 - 顺序错误
void ReadData(Parcel& parcel)
{
    enabled = parcel.ReadBool();      // 错误：先读Bool，但实际是Int32
    name = parcel.ReadString();       // 错误：读取顺序不匹配
    count = parcel.ReadInt32();       // 错误：顺序不匹配
}

// 错误示例2：类型不匹配
// 序列化
void Serialize(Packet& packet)
{
    parcel.WriteUint32(id);
    parcel.WriteFloat(value);
}

// 反序列化 - 类型错误
void Deserialize(Packet& packet)
{
    id = parcel.ReadInt32();      // 错误：Uint32用Int32读取
    value = parcel.ReadDouble();  // 错误：Float用Double读取
}

// 错误示例3：数量不匹配（多读）
// 序列化
void Save(Parcel& parcel)
{
    parcel.WriteInt32(a);
    parcel.WriteInt32(b);
}

// 反序列化 - 多读
void Load(Parcel& parcel)
{
    a = parcel.ReadInt32();
    b = parcel.ReadInt32();
    c = parcel.ReadInt32();  // 错误：多读了一个，越界读取
}

// 错误示例4：数量不匹配（少读）
// 序列化
void Store(Parcel& parcel)
{
    parcel.WriteInt32(x);
    parcel.WriteInt32(y);
    parcel.WriteInt32(z);
}

// 反序列化 - 少读
void Restore(Parcel& parcel)
{
    x = parcel.ReadInt32();
    y = parcel.ReadInt32();
    // 错误：少读了z，可能导致后续读取错误
}

// 错误示例5：条件字段不匹配
// 序列化
void SerializeData(Parcel& parcel, const Data& data)
{
    parcel.WriteBool(data.hasExtra);
    parcel.WriteInt32(data.value);
    if (data.hasExtra) {
        parcel.WriteString(data.extra);
    }
}

// 反序列化 - 条件不匹配
void DeserializeData(Parcel& parcel, Data& data)
{
    data.hasExtra = parcel.ReadBool();
    data.value = parcel.ReadInt32();
    data.extra = parcel.ReadString();  // 错误：无条件读取，hasExtra为false时越界
}

// 错误示例6：数组处理不匹配
// 序列化
void SerializeArray(Parcel& parcel, const std::vector<int>& arr)
{
    parcel.WriteUint32(arr.size());
    for (int val : arr) {
        parcel.WriteInt32(val);
    }
}

// 反序列化 - 数量不匹配
void DeserializeArray(Parcel& parcel, std::vector<int>& arr)
{
    uint32_t count = parcel.ReadUint32();
    for (uint32_t i = 0; i < count + 1; i++) {  // 错误：多读一个
        arr.push_back(parcel.ReadInt32());
    }
}

// 错误示例7：版本兼容问题
// 旧版本序列化
void SerializeV1(Parcel& parcel)
{
    parcel.WriteInt32(version);
    parcel.WriteString(name);
}

// 新版本反序列化 - 期望更多字段
void DeserializeV2(Parcel& parcel)
{
    int version = parcel.ReadInt32();
    std::string name = parcel.ReadString();
    std::string extra = parcel.ReadString();  // 错误：V1没有这个字段
}
```

### ✅ 修复方案

```cpp
// 正确示例1：顺序匹配
// 序列化
void WriteData(Parcel& parcel)
{
    parcel.WriteInt32(count);
    parcel.WriteString(name);
    parcel.WriteBool(enabled);
}

// 反序列化 - 顺序正确
void ReadData(Parcel& parcel)
{
    count = parcel.ReadInt32();    // 1. 读取count
    name = parcel.ReadString();    // 2. 读取name
    enabled = parcel.ReadBool();   // 3. 读取enabled
}

// 正确示例2：类型匹配
// 序列化
void Serialize(Packet& packet)
{
    parcel.WriteUint32(id);
    parcel.WriteFloat(value);
}

// 反序列化 - 类型正确
void Deserialize(Packet& packet)
{
    id = parcel.ReadUint32();   // 正确：Uint32匹配
    value = parcel.ReadFloat(); // 正确：Float匹配
}

// 正确示例3：数量匹配
// 序列化
void Save(Parcel& parcel)
{
    parcel.WriteInt32(a);
    parcel.WriteInt32(b);
}

// 反序列化 - 数量正确
void Load(Parcel& parcel)
{
    a = parcel.ReadInt32();
    b = parcel.ReadInt32();
    // 数量完全匹配
}

// 正确示例4：条件字段匹配
// 序列化
void SerializeData(Parcel& parcel, const Data& data)
{
    parcel.WriteBool(data.hasExtra);
    parcel.WriteInt32(data.value);
    if (data.hasExtra) {
        parcel.WriteString(data.extra);
    }
}

// 反序列化 - 条件匹配
void DeserializeData(Parcel& parcel, Data& data)
{
    data.hasExtra = parcel.ReadBool();
    data.value = parcel.ReadInt32();
    if (data.hasExtra) {  // 正确：条件匹配
        data.extra = parcel.ReadString();
    }
}

// 正确示例5：数组处理匹配
// 序列化
void SerializeArray(Parcel& parcel, const std::vector<int>& arr)
{
    parcel.WriteUint32(arr.size());
    for (int val : arr) {
        parcel.WriteInt32(val);
    }
}

// 反序列化 - 数量正确
void DeserializeArray(Parcel& parcel, std::vector<int>& arr)
{
    uint32_t count = parcel.ReadUint32();
    if (count > MAX_ARRAY_SIZE) {  // 安全检查
        LOGE("Invalid array count");
        return;
    }
    for (uint32_t i = 0; i < count; i++) {  // 正确：数量匹配
        arr.push_back(parcel.ReadInt32());
    }
}

// 正确示例6：版本兼容处理
// 序列化 - 包含版本号
void SerializeV2(Parcel& parcel)
{
    parcel.WriteInt32(2);  // version
    parcel.WriteString(name);
    parcel.WriteString(extra);  // V2新增字段
}

// 反序列化 - 版本兼容
void Deserialize(Parcel& parcel)
{
    int version = parcel.ReadInt32();
    std::string name = parcel.ReadString();
    std::string extra = "";
    if (version >= 2) {  // 正确：根据版本处理
        extra = parcel.ReadString();
    }
}

// 正确示例7：使用统一的结构体方法
struct PacketData {
    int32_t count;
    std::string name;
    bool enabled;
    
    void Marshal(Parcel& parcel) const {
        parcel.WriteInt32(count);
        parcel.WriteString(name);
        parcel.WriteBool(enabled);
    }
    
    void Unmarshal(Parcel& parcel) {
        count = parcel.ReadInt32();
        name = parcel.ReadString();
        enabled = parcel.ReadBool();
    }
};

// 正确示例8：使用辅助工具确保匹配
class ParcelHelper {
public:
    template<typename T>
    static void Write(Parcel& parcel, const T& value) {
        parcel.WriteParcelable(value);
    }
    
    template<typename T>
    static bool Read(Parcel& parcel, T& value) {
        return parcel.ReadParcelable(&value);
    }
};
```

## 检测范围

检查以下模式：

1. 同一类的序列化和反序列化函数
2. `Write`/`Read`函数对
3. `Serialize`/`Deserialize`函数对
4. `Marshal`/`Unmarshal`函数对
5. `Save`/`Load`函数对

## 检测要点

1. 识别序列化和反序列化函数对
2. 比较`Write*`和`Read*`的调用顺序
3. 比较`Write*`和`Read*`的类型
4. 比较`Write*`和`Read*`的数量
5. 检查条件字段的处理是否一致
6. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 序列化/反序列化函数不匹配
- **RISK_TYPE**: 数据解析错误
- **RISK_PATH**: 不匹配操作 -> 数据错误/越界读取 -> 程序崩溃
- **IMPACT_POINT**: 数据完整性、程序稳定性

## 影响分析（ImpactAnalysis）

- **Trigger**: 序列化与反序列化不匹配
- **Propagation**: 数据读取错误导致后续解析失败
- **Consequence**: 数据损坏、越界读取、程序崩溃
- **Mitigation**: 确保Write/Read顺序、类型、数量完全匹配

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 版本兼容处理 | 有版本号判断逻辑 | 不报 |
| 条件分支一致 | Write和Read都有相同条件 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_006_trigger.cpp
// 序列化
void TriggerBad1Write(Parcel& parcel)
{
    parcel.WriteInt32(count);
    parcel.WriteString(name);
}

// 反序列化 - 顺序错误
void TriggerBad1Read(Parcel& parcel)
{
    name = parcel.ReadString();  // 应该报：顺序不匹配
    count = parcel.ReadInt32();
}

// 序列化
void TriggerBad2Write(Parcel& parcel)
{
    parcel.WriteInt32(a);
    parcel.WriteInt32(b);
}

// 反序列化 - 多读
void TriggerBad2Read(Parcel& parcel)
{
    a = parcel.ReadInt32();
    b = parcel.ReadInt32();
    c = parcel.ReadInt32();  // 应该报：数量不匹配
}

// 序列化
void TriggerBad3Write(Parcel& parcel)
{
    parcel.WriteBool(hasData);
    if (hasData) {
        parcel.WriteString(data);
    }
}

// 反序列化 - 条件不匹配
void TriggerBad3Read(Parcel& parcel)
{
    hasData = parcel.ReadBool();
    data = parcel.ReadString();  // 应该报：无条件读取
}
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_006_safe.cpp
// 序列化
void SafeGood1Write(Parcel& parcel)
{
    parcel.WriteInt32(count);
    parcel.WriteString(name);
    parcel.WriteBool(enabled);
}

// 反序列化 - 完全匹配
void SafeGood1Read(Parcel& parcel)
{
    count = parcel.ReadInt32();
    name = parcel.ReadString();
    enabled = parcel.ReadBool();
}

// 序列化
void SafeGood2Write(Parcel& parcel)
{
    parcel.WriteBool(hasData);
    if (hasData) {
        parcel.WriteString(data);
    }
}

// 反序列化 - 条件匹配
void SafeGood2Read(Parcel& parcel)
{
    hasData = parcel.ReadBool();
    if (hasData) {  // 安全：条件匹配
        data = parcel.ReadString();
    }
}

// NOPROTECT: 特殊处理场景
void noprotect_write(Parcel& parcel)
{
    parcel.WriteInt32(a);
}

void noprotect_read(Parcel& parcel)
{
    a = parcel.ReadInt32();
    b = parcel.ReadInt32();
}
```