# 规则004: 重复使用变异数据

**严重程度**: 中危

**问题描述**: 在同一个fuzz测试函数中，从`fdp`提取的变异数据变量不应该被重复用于多个不同的接口调用。每个接口调用应该使用独立的变异数据，以确保每个接口都能接收到不同的输入值，从而提高fuzz覆盖率和数据变异性。

**核心原则**:
1. 每个测试函数应该只测试一个API接口
2. 如果需要在同一个`LLVMFuzzerTestOneInput`中测试多个接口，应该使用switch-case模式，每个case分支使用独立的变异数据
3. 避免将从fdp提取的变量传递给多个不同的方法

**错误示例**:
```cpp
// ❌ 多个接口使用相同的变异数据
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    std::string str = fdp.ConsumeRandomLengthString(64);
    
    // 同一个变量被用于多个不同的方法
    g_instance->Method1(value, str);  // 使用value和str
    g_instance->Method2(value, str);  // 重复使用相同的value和str
    g_instance->Method3(value, str);  // 再次重复使用
    
    return 0;
}

// ❌ 在测试函数中重复使用变异数据
void DoProcessData(FuzzedDataProvider& fdp)
{
    int32_t id = fdp.ConsumeIntegral<int32_t>();
    
    // 同一个id被用于多个调用
    g_instance->SetId(id);
    g_instance->ProcessId(id);  // 重复使用id
    g_instance->ValidateId(id);  // 再次重复使用id
}
```

**正确示例**:
```cpp
// ✅ 每个接口使用不同的变异数据（switch-case模式）
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    uint8_t choice = fdp.ConsumeIntegral<uint8_t>() % 3;
    
    switch (choice) {
        case 0: {
            // Method1使用独立的变异数据
            int32_t value1 = fdp.ConsumeIntegral<int32_t>();
            std::string str1 = fdp.ConsumeRandomLengthString(64);
            g_instance->Method1(value1, str1);
            break;
        }
        case 1: {
            // Method2使用独立的变异数据
            int32_t value2 = fdp.ConsumeIntegral<int32_t>();
            std::string str2 = fdp.ConsumeRandomLengthString(64);
            g_instance->Method2(value2, str2);
            break;
        }
        case 2: {
            // Method3使用独立的变异数据
            int32_t value3 = fdp.ConsumeIntegral<int32_t>();
            std::string str3 = fdp.ConsumeRandomLengthString(64);
            g_instance->Method3(value3, str3);
            break;
        }
    }
    
    return 0;
}

// ✅ 每个测试函数只测试一个API
void DoMethod1(FuzzedDataProvider& fdp)
{
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    std::string str = fdp.ConsumeRandomLengthString(64);
    g_instance->Method1(value, str);  // 只调用Method1
}

void DoMethod2(FuzzedDataProvider& fdp)
{
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    std::string str = fdp.ConsumeRandomLengthString(64);
    g_instance->Method2(value, str);  // 只调用Method2，使用独立的数据
}
```

**检查方法**: 1. 检查同一个函数中，从fdp提取的变量是否被用于多个不同的接口调用
2. 检查是否使用了switch-case模式来分发到不同的测试函数
3. 确保每个测试函数只测试一个API接口

**豁免场景**: 
- 无

---
