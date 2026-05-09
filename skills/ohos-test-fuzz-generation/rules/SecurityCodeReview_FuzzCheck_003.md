# 规则003: 未使用变异数据

**严重程度**: 中危

**问题描述**: FUZZ测试的核心是使用变异数据（mutated data）来测试API的健壮性。如果测试代码没有使用`data`参数中的变异数据，而是使用固定值、常量或硬编码的参数，那么这就完全失去了FUZZ测试的意义。变异数据是由FUZZ引擎（如libFuzzer）根据覆盖率反馈不断变异生成的，能够产生各种边界值、异常值和随机值，从而发现潜在的崩溃、内存错误和逻辑漏洞。

**核心原则**:
1. 必须从`data`参数中提取数据，使用`FuzzedDataProvider`提供的`ConsumeXxx`方法
2. 所有传给被测API的参数都应该是从变异数据中提取的
3. 不允许使用固定值、常量或硬编码的参数（除非业务必需的Magic Number、版本号等）

**错误示例**:
```cpp
// ❌ 完全没有使用变异数据 - 直接调用API
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    // 完全没有使用data参数！
    g_instance->SomeMethod(123, "fixed string", true);
    return 0;
}

// ❌ 虽然声明了fdp但没有使用
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    // 声明了fdp但没有调用任何Consume方法
    g_instance->SomeMethod(0, "test", false);  // 仍然使用固定值
    return 0;
}

// ❌ 测试函数中没有使用fdp
void DoSetConfig(FuzzedDataProvider& fdp)
{
    // 没有使用fdp提取数据
    g_instance->SetConfig(100);  // 固定值
}
```

**正确示例**:
```cpp
// ✅ 正确使用变异数据
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    // 所有参数都从变异数据中提取
    int32_t param1 = fdp.ConsumeIntegral<int32_t>();
    std::string param2 = fdp.ConsumeRandomLengthString(64);
    bool param3 = fdp.ConsumeBool();
    
    g_instance->SomeMethod(param1, param2, param3);
    return 0;
}

// ✅ 测试函数中使用fdp提取数据
void DoSetConfig(FuzzedDataProvider& fdp)
{
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    g_instance->SetConfig(value);  // 使用变异数据
}
```

**检查方法**:
1. 检查`LLVMFuzzerTestOneInput`函数中是否创建了`FuzzedDataProvider`对象并调用了`ConsumeXxx`方法
2. 检查所有测试函数中是否使用了`fdp.ConsumeXxx()`提取数据
3. 检查传给被测API的参数是否都是从变异数据中提取的

**豁免场景**: 
- Magic Number、版本号等业务必需的固定参数
- 测试框架初始化代码

---
