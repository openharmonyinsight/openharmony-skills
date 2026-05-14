# 规则014: 使用固定参数

**严重程度**: 中危

**问题描述**: Fuzz 测试的核心价值在于通过变异数据发现边界问题和异常处理缺陷。如果参数全部使用固定值，则等同于单元测试（UT），失去了 Fuzz 测试的意义。但某些业务场景下，固定值是必需的（如协议 Magic Number、API 版本号等），需要合理区分。

**关键原则**:
1. **可变参数必须使用变异数据**：直接影响业务逻辑的参数（如 width、height、data、mode 等）必须使用 `fdp.ConsumeXxx()` 提取
2. **固定值必须有业务理由**：只有那些"必须固定才能通过前置校验"或"固定值是协议/标准的一部分"的参数才能使用固定值
3. **避免"偷懒式固定"**：不能因为"懒得构造"或"不知道怎么构造"就使用固定值

**核心原则**:
1. FUZZ测试应使用变异数据而非固定值
2. 仅在业务必需场景使用固定参数
3. Magic Number、版本号等可豁免

**错误示例**:
```cpp
// ❌ 全部使用固定参数（等同于UT）
void DoCreateSurface(FuzzedDataProvider& fdp)
{
    uint32_t width = 1920;   // 固定值 - 错误：应该使用变异数据
    uint32_t height = 1080;  // 固定值 - 错误：应该使用变异数据
    uint32_t format = 1;     // 固定值 - 错误：即使范围小，也应使用变异数据
    
    g_instance->CreateSurface(width, height, format);
    // 问题：每次调用参数都相同，无法测试不同分辨率、不同格式的处理逻辑
}

// ❌ "偷懒式固定" - 因为不知道怎么构造就固定
void DoProcessImage(FuzzedDataProvider& fdp)
{
    uint32_t width = 1920;   // 固定值 - 错误：应该使用 fdp.ConsumeIntegral<uint32_t>()
    uint32_t height = 1080;  // 固定值 - 错误：应该使用变异数据
    std::vector<uint8_t> data = fdp.ConsumeBytes<uint8_t>(100);  // 只有data是变异的
    
    g_instance->ProcessImage(width, height, data);
    // 问题：虽然data是变异的，但width/height固定导致无法测试不同尺寸的处理
}
```

**正确示例**:
```cpp
// ✅ 所有可变参数使用变异数据
void DoCreateSurface(FuzzedDataProvider& fdp)
{
    uint32_t width = fdp.ConsumeIntegral<uint32_t>();   // 变异数据
    uint32_t height = fdp.ConsumeIntegral<uint32_t>();  // 变异数据
    uint32_t format = fdp.ConsumeIntegral<uint32_t>();  // 变异数据，即使范围小也应变异
    
    g_instance->CreateSurface(width, height, format);
    // 现在可以覆盖：不同分辨率、不同格式、边界值、异常值等
}

// ✅ 合理混合：变异数据 + 业务必需的固定值
void DoProcessPacket(FuzzedDataProvider& fdp)
{
    // 协议头部字段 - 固定值（业务必需）
    uint32_t magic = 0x12345678;  // 协议 Magic Number，必须固定
    uint16_t version = 1;          // API 版本号，必须固定
    
    // 业务数据字段 - 变异数据
    uint32_t payloadSize = fdp.ConsumeIntegral<uint32_t>();
    auto payload = fdp.ConsumeBytes<uint8_t>(payloadSize % 1024);
    uint32_t flags = fdp.ConsumeIntegral<uint32_t>();  // 标志位组合，应变异
    
    g_instance->ProcessPacket(magic, version, payload, flags);
    // Magic 和 Version 固定确保通过协议校验
    // Payload 和 Flags 变异测试业务逻辑
}

// ✅ 对范围小的参数也使用变异数据
void DoSetMode(FuzzedDataProvider& fdp)
{
    // 即使 mode 只有 0-5 是合法的，也应该使用变异数据
    // 这样既能测试合法值（0-5），也能测试非法值（6-255）的处理
    uint8_t mode = fdp.ConsumeIntegral<uint8_t>();  // 范围 0-255
    g_instance->SetMode(mode);
}
```

**检查方法**:
1. 识别所有参数，区分"业务数据参数"和"协议/标准常量参数"
2. 业务数据参数必须使用 `fdp.ConsumeXxx()` 提取
3. 固定值必须有注释说明为什么固定（如 `// 协议 Magic Number`）
4. 如果某个参数不知道怎么构造，应查阅业务文档或源码，而不是固定

**豁免场景**: 
- **协议 Magic Number**：如 `0x52494646`（RIFF 文件头）
- **API 版本号**：如 `version = 1`，确保接口兼容性
- **标准常量**：如标准分辨率（仅在测试特定分辨率处理时可固定）
- **标志位组合**：某些固定的标志位掩码
- **布尔开关**：某些业务上必须开启/关闭的选项

---
