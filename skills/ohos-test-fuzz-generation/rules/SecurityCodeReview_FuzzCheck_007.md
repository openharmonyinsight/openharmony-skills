# 规则007: 目标API跨进程

**严重程度**: 中危

**问题描述**: FUZZ进程只能监控当前程序，编写IPC的用例时，如果通过client端接口触发服务端api，服务端api不受fuzz程序监控，无法收集运行数据。

**核心原则**:
1. IPC服务端逻辑必须通过OnRemoteRequest测试
2. 跨进程调用无法被fuzz引擎监控
3. 客户端和服务端逻辑应分开测试

**错误示例**:
```cpp
// ❌ 通过client端接口测试IPC服务端逻辑（无法监控服务端）
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    auto proxy = RSInterface::GetInstance();
    int32_t result = proxy->SomeMethod(fdp.ConsumeIntegral<int32_t>());  
    // 错误：服务端代码在另一个进程，fuzz无法监控服务端分支覆盖
    return 0;
}
```

**正确示例**:
```cpp
// ✅ 通过OnRemoteRequest直接测试stub（覆盖服务端逻辑）
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    MessageParcel dataParcel;
    MessageParcel replyParcel;
    MessageOption option;
    
    uint32_t code = fdp.ConsumeIntegral<uint32_t>();
    dataParcel.WriteInt32(fdp.ConsumeIntegral<int32_t>());
    
    auto stub = std::make_unique<RSInterfaceStub>();
    int32_t result = stub->OnRemoteRequest(code, dataParcel, replyParcel, option);
    // 服务端代码在fuzz进程内执行，可以监控覆盖率和崩溃
    
    return 0;
}

// ✅ 测试客户端对外接口（仅覆盖客户端逻辑）
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    // 测试客户端参数构造、状态管理等客户端特有逻辑
    uint32_t screenId = fdp.ConsumeIntegral<uint32_t>();
    int32_t mode = fdp.ConsumeIntegral<int32_t>();
    
    // 客户端接口调用，只覆盖客户端代码路径
    RSInterfaces::GetInstance().SetScreenMode(screenId, mode);
    
    return 0;
}
```

**检查方法**: 
1. 检测代码中是否包含 IPC proxy/stub 相关类（Proxy/Stub/IPC 关键字）
2. 如果涉及 IPC 接口但未通过 OnRemoteRequest 测试 stub，则报错
3. 区分测试目标是服务端还是客户端

**豁免场景**: 
- 测试客户端(proxy)端的特定逻辑（参数构造、状态管理等客户端代码）

---
