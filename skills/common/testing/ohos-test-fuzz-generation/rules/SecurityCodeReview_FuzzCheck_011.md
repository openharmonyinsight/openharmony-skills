# 规则011: 系统安全准入条件

**严重程度**: 中危

**问题描述**: 当目标 API 或 stub 端存在系统级安全校验时，若用例未构造满足准入条件的调用上下文，请求会在入口处被拒绝，fuzz 无法触及后续业务逻辑。这是 fuzz 用例编写中最容易被忽视的问题之一。

**与规则010的区别**: 规则9关注的是**"谁可以调用"**（调用者身份与权限），规则010关注的是**"参数是否合法"**（入值范围与状态）。

**常见安全准入条件**:
1. **权限校验**: 缺少必要权限 token 或 caller 身份不符合要求
2. **UID/PID 校验**: 仅允许特定系统进程/用户调用
3. **能力集（Capability）校验**: 要求调用方持有特定系统能力
4. **安全标签/ACL**: 访问控制列表拦截
5. **系统状态校验**: 要求系统处于特定状态（如已初始化、未锁定等）
6. **会话/Token 校验**: 需要有效的会话或访问令牌
7. **白名单校验**: 仅允许特定模块或接口调用

**核心原则**:
1. 测试前必须构造完整的安全上下文
2. 权限、身份、状态等准入条件必须满足
3. 缺少准入条件会导致无法触及业务逻辑

**错误示例**:
```cpp
// ❌ 没有构造权限token，导致鉴权失败
void DoSensitiveOperation(FuzzedDataProvider& fdp)
{
    g_instance->SensitiveOperation(fdp.ConsumeIntegral<int32_t>());
    // stub端会鉴权失败，直接返回，无法测试后续逻辑
}

// ❌ 未设置caller身份，被UID/PID校验拦截
void DoSystemCall(FuzzedDataProvider& fdp)
{
    g_instance->SystemCall(fdp.ConsumeIntegral<uint32_t>());
    // 服务端：if (!IsSystemApp()) return;
}

// ❌ 未初始化系统状态，被状态校验拦截
void DoInitialize(FuzzedDataProvider& fdp)
{
    g_instance->Configure(fdp.ConsumeIntegral<int32_t>());
    // 服务端：if (!IsInitialized()) return;
}

// ❌ 未设置会话token，被会话校验拦截
void DoProcessRequest(FuzzedDataProvider& fdp)
{
    g_instance->ProcessRequest(fdp.ConsumeIntegral<uint32_t>());
    // 服务端：if (!HasValidSession()) return;
}
```

**正确示例**:
```cpp
// ✅ 构造满足权限校验的token
void DoSensitiveOperation(FuzzedDataProvider& fdp)
{
    std::string token = fdp.ConsumeRandomLengthString(32);
    g_instance->SetPermission(token);
    g_instance->SensitiveOperation(fdp.ConsumeIntegral<int32_t>());
}

// ✅ 模拟系统应用身份
void DoSystemCall(FuzzedDataProvider& fdp)
{
    SetCallerUid(SYSTEM_UID);
    g_instance->SystemCall(fdp.ConsumeIntegral<uint32_t>());
}

// ✅ 先初始化系统状态
void DoInitialize(FuzzedDataProvider& fdp)
{
    // 先调用初始化接口
    g_instance->Init();
    // 再调用需要初始化状态的接口
    g_instance->Configure(fdp.ConsumeIntegral<int32_t>());
}

// ✅ 先建立有效会话
void DoProcessRequest(FuzzedDataProvider& fdp)
{
    // 先创建会话
    std::string sessionId = fdp.ConsumeRandomLengthString(16);
    g_instance->CreateSession(sessionId);
    // 再调用需要会话的接口
    g_instance->ProcessRequest(fdp.ConsumeIntegral<uint32_t>());
}
```

**检查方法**: 1. 阅读目标 API 源码或文档，识别所有安全准入条件（权限、身份、状态、会话等）
2. 检查用例是否构造了满足准入条件的调用上下文
3. 确保在调用目标 API 前，已完成所有必要的前置准备（初始化、鉴权、设置身份等）
4. 对于 stub 端接口，检查是否绕过了安全校验或构造了合法的调用者身份

**豁免场景**: 
- API本身无安全准入条件
- fuzz测试目的就是测试准入条件校验逻辑

---
