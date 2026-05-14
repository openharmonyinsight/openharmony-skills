# 规则001: 目标API不适合FUZZ

**严重程度**: 中危

**问题描述**: 测试的API/接口没有参数，无法构造各种参数进行fuzz测试，失去了fuzz测试的意义。

**核心原则**:
1. FUZZ测试必须针对有参数的API
2. 无参数API应使用单元测试而非FUZZ测试
3. 固定参数API不适合FUZZ，因为无法产生变异

**错误示例**:
```cpp
// ❌ 无参数API不适用FUZZ
void DoGetVersion(FuzzedDataProvider& fdp)
{
    g_instance->GetVersion();  // 无参数，无法fuzz
}

// ❌ 仅使用固定参数
void DoInit(FuzzedDataProvider& fdp)
{
    g_instance->Init(0);  // 固定参数0，无意义
}
```

**正确示例**:
```cpp
// ✅ 对有参数的API，每个参数都从fdp提取变异数据
void DoSetScreenConfig(FuzzedDataProvider& fdp)
{
    bool enable = fdp.ConsumeBool();
    int32_t mode = fdp.ConsumeIntegral<int32_t>();
    std::string name = fdp.ConsumeRandomLengthString(64);
    std::vector<uint8_t> data;
    uint8_t count = fdp.ConsumeIntegral<uint8_t>() % 32;
    for (uint8_t i = 0; i < count; i++) {
        data.push_back(fdp.ConsumeIntegral<uint8_t>());
    }
    g_instance->SetScreenConfig(enable, mode, name, data);
}
```

**检查方法**:
1. 识别API是否有可变参数
2. 无参数API使用单元测试而非FUZZ

**豁免场景**: 
- API确实无参数且无需FUZZ测试（如纯查询类接口）
- API仅返回常量值，无业务逻辑处理

---
