# 规则015: 中间产物由合法流程生成

**严重程度**: 中危

**问题描述**: 如果测试接口的输入参数需要经过一个"合法生成流程"（编解码、序列化/反序列化、加密/解密、打包/解包等）来构造，导致传入的总是格式正确的数据，则 fuzz 只能验证"正常路径"，无法触及对非法/畸形数据的处理分支。

**核心问题**：中间产物经由合法流程生成，会过滤掉 fuzz 引擎产生的变异数据中的异常值，使测试失去意义。

**常见场景**:
- **编解码**：先编码再解码，解码的总是格式正确的数据
- **序列化**：先序列化对象再反序列化，数据总是合法的
- **加密/解密**：加密后解密，数据完整性被保证
- **打包/解包**：先打包再解包，包结构总是合法的
- **校验和/签名**：重新计算校验和使数据总是通过验证
- **屏幕参数构造**：使用正常规则构造的屏幕参数（如分辨率、刷新率）总是合法的，无法测试内部对非法参数的处理

**核心原则**:
1. 避免通过合法流程生成中间产物
2. 直接使用变异数据测试被测接口
3. 合法流程会过滤掉异常值

**错误示例**:
```cpp
// ❌ 编解码场景：先编码再解码，解码的总是正确的
void DoTestCodec(FuzzedDataProvider& fdp)
{
    std::vector<uint8_t> rawData = fdp.ConsumeBytes<uint8_t>(256);
    std::vector<uint8_t> encodedData = encoder.Encode(rawData);
    std::vector<uint8_t> decodedData = decoder.Decode(encodedData);
    // decodedData总是正确的，失去了fuzz的意义
}

// ❌ 序列化场景：先序列化再反序列化
void DoTestParser(FuzzedDataProvider& fdp)
{
    MyObject obj;
    obj.id = fdp.ConsumeIntegral<uint32_t>();
    obj.name = fdp.ConsumeRandomLengthString(32);
    
    std::string json = obj.ToJson();  // 序列化
    MyObject parsed = MyObject::FromJson(json);  // 反序列化
    // json总是格式正确的，无法测试解析器的鲁棒性
}

// ❌ 屏幕参数构造：使用正常规则构造，总是合法的
void DoSetScreenInfo(FuzzedDataProvider& fdp)
{
    // 使用正常规则构造屏幕参数，无法测试非法参数处理
    uint32_t width = 1920;   // 固定合法值
    uint32_t height = 1080;  // 固定合法值
    uint32_t refreshRate = 60; // 固定合法值
    
    // 应该使用变异数据来测试内部对非法参数的处理
    g_instance->SetScreenInfo(width, height, refreshRate);
}
```

**正确示例**:
```cpp
// ✅ 直接用变异数据测试解码接口
void DoTestDecoder(FuzzedDataProvider& fdp)
{
    std::vector<uint8_t> fuzzData = fdp.ConsumeBytes<uint8_t>(256);
    std::vector<uint8_t> decodedData = decoder.Decode(fuzzData);
    // fuzzData可能是非法的，能测试解码的鲁棒性
}

// ✅ 直接用变异数据测试解析器
void DoTestParser(FuzzedDataProvider& fdp)
{
    std::string json = fdp.ConsumeRandomLengthString(256);
    MyObject parsed = MyObject::FromJson(json);
    // json可能是畸形的，能测试解析器的错误处理
}

// ✅ 仅对部分字段使用合法生成，关键字段保留变异
void DoTestWithPartialValidData(FuzzedDataProvider& fdp)
{
    // 构造一个合法的基础结构
    PacketHeader header;
    header.magic = 0x12345678;  // 固定Magic
    header.version = 1;          // 固定版本
    
    // 但payload直接使用变异数据
    std::vector<uint8_t> payload = fdp.ConsumeBytes<uint8_t>(256);
    
    g_instance->ProcessPacket(header, payload);
}

// ✅ 使用变异数据测试屏幕参数（构造不合理的参数）
void DoSetScreenInfo(FuzzedDataProvider& fdp)
{
    // 使用变异数据构造各种参数，包括不合理的值
    uint32_t width = fdp.ConsumeIntegral<uint32_t>();
    uint32_t height = fdp.ConsumeIntegral<uint32_t>();
    uint32_t refreshRate = fdp.ConsumeIntegral<uint32_t>();
    
    // 测试内部对非法参数的处理（如width=0, height=0xFFFFFFFF等）
    g_instance->SetScreenInfo(width, height, refreshRate);
}
```

**检查方法**: 1. 识别测试接口是否依赖中间产物（检查是否存在 Encode/Decode、Serialize/Deserialize、Encrypt/Decrypt、Pack/Unpack、ToJson/FromJson 等成对调用）
2. 检查是否使用合法流程生成数据后再传入被测接口
3. 检查是否使用固定值构造参数（如固定的分辨率、刷新率等），而非使用变异数据
4. 如果是，改为直接使用 fuzz 变异数据，或确保关键字段保留变异以测试异常路径

**豁免场景**: 
- 测试目标就是编码/序列化接口本身
- 合法生成流程的输出需要进一步变异处理

---
