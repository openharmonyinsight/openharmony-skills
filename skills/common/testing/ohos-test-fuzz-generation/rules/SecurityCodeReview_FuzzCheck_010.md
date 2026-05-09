# 规则010: size当作变异数据

**严重程度**: 中危

**问题描述**: `size`参数（即`LLVMFuzzerTestOneInput`的第二个参数）表示`data`缓冲区的长度，仅应用于`FuzzedDataProvider`的初始化和边界检查。禁止将`size`作为变异数据传给被测接口、用于业务逻辑判断或作为循环计数器。`size`的值由fuzz引擎决定，不代表有意义的业务输入。

**核心原则**:
1. `size`仅用于初始化`FuzzedDataProvider`和做最小长度检查
2. 禁止将`size`作为参数传递给被测API
3. 禁止用`size`做业务逻辑分支判断
4. 需要长度值时，应通过`fdp.ConsumeIntegral()`提取

**错误示例**:
```cpp
// ❌ 将size直接传给被测API
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    g_instance->Process(size);  // size不是变异数据
    return 0;
}

// ❌ 用size做业务分支判断
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    if (size > 100) {        // size用于分支判断
        g_instance->Method1(fdp.ConsumeIntegral<int32_t>());
    } else {
        g_instance->Method2(fdp.ConsumeIntegral<int32_t>());
    }
    return 0;
}

// ❌ 用size作为循环次数
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    for (size_t i = 0; i < size; i++) {  // size用于循环
        g_instance->ProcessItem(fdp.ConsumeIntegral<uint8_t>());
    }
    return 0;
}

// ❌ size参与运算后传给API
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    int32_t count = size / 4;  // size参与运算
    g_instance->SetCount(count);
    return 0;
}
```

**正确示例**:
```cpp
// ✅ size仅用于FuzzedDataProvider初始化和边界检查
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (size < sizeof(int32_t)) return 0;  // 边界检查
    FuzzedDataProvider fdp(data, size);
    
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    g_instance->Process(value);  // 使用fdp提取的数据
    return 0;
}

// ✅ 需要长度/循环次数时，从fdp提取
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    int32_t count = fdp.ConsumeIntegralInRange<int32_t>(1, 100);  // 从fdp提取
    for (int32_t i = 0; i < count; i++) {
        g_instance->ProcessItem(fdp.ConsumeIntegral<uint8_t>());
    }
    return 0;
}

// ✅ 需要做分支判断时，从fdp提取
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    bool useMethod1 = fdp.ConsumeBool();  // 从fdp提取分支条件
    if (useMethod1) {
        g_instance->Method1(fdp.ConsumeIntegral<int32_t>());
    } else {
        g_instance->Method2(fdp.ConsumeIntegral<int32_t>());
    }
    return 0;
}
```

**检查方法**: 1. 检查`size`变量是否出现在`FuzzedDataProvider`初始化和最小长度检查以外的位置
2. 检查`size`是否被传递给被测API
3. 检查`size`是否用于`if`/`switch`分支判断
4. 检查`size`是否用于循环条件或计数
5. 检查`size`是否参与算术运算后作为业务参数

**豁免场景**: 
- 无

---
