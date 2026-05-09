# 规则018: 变异数据使用不当

**严重程度**: 中危

**问题描述**: 在fuzz测试中，禁止直接使用`data`指针或将`data`作为原始字节流传给被测接口，而不通过`FuzzedDataProvider`提取。`data`指针是fuzz引擎提供的原始变异数据，应通过`FuzzedDataProvider`提供的方法（如`ConsumeIntegral`、`ConsumeRandomLengthString`、`ConsumeBytes`等）按类型提取，以确保变异数据被正确消费和类型化。

**核心原则**:
1. 必须使用`FuzzedDataProvider`来消费变异数据，而非直接操作`data`指针
2. 禁止将`data`指针直接传递给被测接口或中间处理函数
3. 禁止手动计算偏移量从`data`中截取数据
4. 禁止直接索引`data`数组（如`data[0]`、`data[1]`等）

**错误示例**:
```cpp
// ❌ 直接使用data指针
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    g_instance->ProcessData(data, size);  // 直接传入data指针
    return 0;
}

// ❌ 手动计算偏移量截取数据
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (size < 8) return 0;
    int32_t value = *reinterpret_cast<const int32_t*>(data);  // 不安全
    std::string str(reinterpret_cast<const char*>(data + 4), 4);
    g_instance->Process(value, str);
    return 0;
}

// ❌ 将data强转为结构体指针
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (size < sizeof(MyStruct)) return 0;
    auto* p = reinterpret_cast<const MyStruct*>(data);  // 不安全且不可移植
    g_instance->Handle(p->field1, p->field2);
    return 0;
}

// ❌ 直接索引data数组（如data[0], data[1]等）
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (size < 2) return 0;
    uint8_t first = data[0];   // 错误：直接索引data
    uint8_t second = data[1];  // 错误：直接索引data
    g_instance->Process(first, second);
    return 0;
}
```

**正确示例**:
```cpp
// ✅ 使用FuzzedDataProvider按类型提取数据
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    std::string str = fdp.ConsumeRandomLengthString(64);
    auto bytes = fdp.ConsumeBytes<uint8_t>(128);
    
    g_instance->Process(value, str, bytes);
    return 0;
}

// ✅ 需要传入原始字节时，通过ConsumeBytes提取
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    size_t len = fdp.ConsumeIntegralInRange<uint32_t>(0, 1024);
    auto rawData = fdp.ConsumeBytes<uint8_t>(len);
    g_instance->ProcessData(rawData.data(), rawData.size());
    return 0;
}
```

**检查方法**: 1. 检查`LLVMFuzzerTestOneInput`函数中是否直接使用了`data`指针（非`FuzzedDataProvider`构造）
2. 检查是否存在对`data`的指针算术运算（如`data + offset`）
3. 检查是否存在对`data`的`reinterpret_cast`类型转换
4. 检查是否存在直接索引`data`数组（如`data[N]`）
5. 确保所有数据提取均通过`fdp.ConsumeXxx()`方法完成

**豁免场景**: 
- `FuzzedDataProvider`的构造函数参数中使用`data`和`size`（这是合法的）

---
