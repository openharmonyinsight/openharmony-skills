# 规则016: 赋值数据类型不正确

**严重程度**: 中危

**问题描述**: 类型不匹配会导致数据语义失真、精度丢失或未定义行为。常见错误包括：
- **字节宽度不匹配**：小字节类型赋值给大字节类型，导致零填充而非预期值；或fdp生成类型与接收变量类型不一致
- **符号性混用**：有符号与无符号混用，导致负数被解释为超大正数
- **类型类别混用**：整数与浮点互转造成精度丢失；指针与整数混用导致未定义行为
- **数据格式混淆**：将二进制数据直接当C字符串使用，因缺少终止符而溢出
- **fdp生成类型与实际使用类型不一致**：例如用 `ConsumeIntegral<uint32_t>()` 赋值给 `uint8_t` 变量，导致数据截断

**核心原则**:
1. 变量声明类型必须与fdp生成类型匹配
2. 避免小类型赋值给大类型
3. 有符号和无符号类型不能混用

**错误示例**:
```cpp
// ❌ 小类型赋值给大类型（零填充失真）
void DoSetConfig(FuzzedDataProvider& fdp)
{
    uint8_t smallValue = fdp.ConsumeIntegral<uint8_t>();
    uint64_t largeValue = smallValue;  // 错误：仅低8位有效，变异空间受限
    g_instance->SetConfig(largeValue);
}

// ❌ fdp生成类型与接收变量类型不一致（数据截断）
void DoSetId(FuzzedDataProvider& fdp)
{
    uint8_t id = fdp.ConsumeIntegral<uint32_t>();  // 错误：uint32_t -> uint8_t，数据截断
    g_instance->SetId(id);
}

// ❌ 有符号/无符号混用（语义错误）
void DoSetOffset(FuzzedDataProvider& fdp)
{
    int8_t signedValue = fdp.ConsumeIntegral<int8_t>();  // 可能为负
    size_t sizeValue = signedValue;  // 错误：负数变超大正数
    g_instance->SetOffset(sizeValue);
}

// ❌ 整数与浮点混用（精度丢失）
void DoSetFloat(FuzzedDataProvider& fdp)
{
    int32_t intValue = fdp.ConsumeIntegral<int32_t>();
    float floatValue = static_cast<float>(intValue);  // 错误：丢失小数部分
    g_instance->SetFloat(floatValue);
}

// ❌ 将二进制数据当字符串
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    char* str = (char*)data;  // 错误：二进制数据可能无终止符
    g_instance->ProcessString(str);
    return 0;
}

// ❌ 指针与整数混用（未定义行为）
void DoSetPtr(FuzzedDataProvider& fdp)
{
    uintptr_t addr = fdp.ConsumeIntegral<uintptr_t>();
    void* ptr = reinterpret_cast<void*>(addr);  // 错误：随机地址可能无效
    g_instance->UsePointer(ptr);
}
```

**正确示例**:
```cpp
// ✅ 使用匹配的类型大小和符号性
void DoSetConfig(FuzzedDataProvider& fdp)
{
    uint64_t largeValue = fdp.ConsumeIntegral<uint64_t>();
    g_instance->SetConfig(largeValue);
}

void DoSetId(FuzzedDataProvider& fdp)
{
    uint32_t id = fdp.ConsumeIntegral<uint32_t>();  // 类型匹配
    g_instance->SetId(id);
}

void DoSetOffset(FuzzedDataProvider& fdp)
{
    // 根据业务需求选择有符号或无符号
    int64_t offset = fdp.ConsumeIntegral<int64_t>();
    g_instance->SetOffset(offset);
}

// ✅ 使用FDP直接生成浮点数
void DoSetFloat(FuzzedDataProvider& fdp)
{
    float floatValue = fdp.ConsumeFloatingPoint<float>();
    g_instance->SetFloat(floatValue);
}

// ✅ 正确处理字符串
void DoProcessString(FuzzedDataProvider& fdp)
{
    std::string str = fdp.ConsumeRandomLengthString(256);
    g_instance->ProcessString(str);
}

// ✅ 指针应通过合法API构造，而非强制转换
void DoSetPtr(FuzzedDataProvider& fdp)
{
    auto obj = std::make_shared<MyObject>(fdp.ConsumeIntegral<int32_t>());
    g_instance->UsePointer(obj.get());
}
```

**类型大小对照表**:

| 参数类型 | 推荐提取类型 | 字节数 |
|---------|------------|-------|
| int8_t/uint8_t | ConsumeIntegral<int8_t/uint8_t>() | 1 |
| int16_t/uint16_t | ConsumeIntegral<int16_t/uint16_t>() | 2 |
| int32_t/uint32_t | ConsumeIntegral<int32_t/uint32_t>() | 4 |
| int64_t/uint64_t | ConsumeIntegral<int64_t/uint64_t>() | 8 |
| bool | ConsumeBool() | 1 |
| 枚举类型 | ConsumeIntegral<uint32_t>() | 4 |
| 字符串 | ConsumeRandomLengthString() | 可变 |

**检查方法**: 1. 检查变量声明类型与 `fdp.ConsumeIntegral<T>()` 中的模板参数 T 是否一致
2. 检查是否存在小类型变量赋值给大类型变量（如 uint8_t -> uint64_t）
3. 检查有符号类型赋值给无符号类型（如 int8_t -> size_t）
4. 检查整数转浮点数（应使用 ConsumeFloatingPoint）
5. 检查指针与整数混用

**豁免场景**: 
- 业务明确需要的类型转换（如配置项统一用uint64_t接收）
- 有范围限制的安全转换（如已做%取模）

---
