---
rule_id: "StabilityCodeReview_GraphicsStability_010"
name: "回调函数执行进程限制"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 回调函数执行进程限制

## 问题描述

应用进程传入的回调函数不能在RS进程中执行，只能在应用进程执行。RS进程和应用进程有独立的地址空间和执行上下文，直接在RS进程执行应用回调会导致回调在错误的上下文中执行，引发崩溃或状态不一致。

## 检测示例

### 错误示例

```cpp
// 错误示例1：RS进程直接执行应用回调
void RSProcess::OnRenderComplete(SurfaceId id)
{
    auto callback = GetAppCallback(id);
    
    // 错误：RS进程直接执行应用回调
    callback->OnComplete();  // 错误：回调在错误进程执行
}

// 错误示例2：RS服务直接调用应用监听器
class RenderService {
public:
    void NotifyAppListener(RenderResult result)
    {
        auto listener = appListener_;  // 应用传入的监听器
        
        // 错误：RS服务直接调用应用监听器
        listener->OnResult(result);  // 错误：跨进程调用
    }
};

// 错误示例3：RS线程执行应用回调函数
void RSRenderThread::HandleCallback()
{
    std::function<void()> appCallback = GetPendingCallback();
    
    // 错误：RS线程执行应用回调
    appCallback();  // 错误：回调在RS进程执行
}

// 错误示例4：RS进程的回调处理
void RenderServiceProcess::ProcessCallbacks()
{
    for (auto& cb : pendingCallbacks_) {
        // 错误：在RS进程执行应用回调
        cb.execute();  // 错误
    }
}
```

### 正确示例

```cpp
// 正确示例1：通过IPC发送回调到应用进程
void RSProcess::OnRenderComplete(SurfaceId id)
{
    auto callback = GetAppCallback(id);
    
    // 正确：通过IPC发送到应用进程执行
    PostCallbackToApp(callback);  // 正确：IPC通知应用
}

// 正确示例2：使用消息机制通知应用
class RenderService {
public:
    void NotifyAppListener(RenderResult result)
    {
        // 正确：通过IPC消息发送结果
        SendResultToApp(result);  // 正确
        
        // 应用进程收到消息后执行回调
    }
};

// 正确示例3：应用进程处理回调
void AppProcess::HandleRSMessage(const RSMessage& msg)
{
    if (msg.type == RENDER_COMPLETE) {
        // 正确：应用进程执行回调
        auto callback = GetCallback(msg.surfaceId);
        callback->OnComplete();  // 正确：在应用进程执行
    }
}

// 正确示例4：使用Binder IPC传递
void RSProcess::ScheduleAppCallback(std::function<void()> callback)
{
    // 正确：通过Binder IPC发送
    BinderCallbackToken token = RegisterCallback(callback);
    SendCallbackTokenToApp(token);  // 正确
    
    // 应用进程根据token执行回调
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: RS进程直接执行应用回调函数
- **RISK_TYPE**: 进程边界违规
- **RISK_PATH**: RS进程执行应用回调 -> 回调在错误进程上下文执行 -> 状态不一致
- **IMPACT_POINT**: 回调失败、进程崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: RS进程直接调用应用传入的回调
- **Propagation**: 回调在错误进程上下文执行
- **Consequence**: 回调失败、进程通信异常、崩溃
- **Mitigation**: 通过IPC将回调发送到应用进程执行

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| IPC发送 | PostToApp、SendToApp | 不报 |
| 应用进程上下文 | AppProcess:: | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// RSProcess中直接执行应用回调
void RSProcess::OnComplete()
{
    appCallback->OnComplete();  // 应该报：在RS进程执行应用回调
}
```

### 安全用例（不应该报）

```cpp
// RSProcess通过IPC发送回调
void RSProcess::OnComplete()
{
    PostCallbackToApp(appCallback);  // 不报：通过IPC发送
    
// 应用进程执行回调
void AppProcess::HandleCallback()
{
    appCallback->OnComplete();  // 不报：在应用进程执行
}
```