---
rule_id: "StabilityCodeReview_GraphicsStability_009"
name: "RSRenderNodeMap线程访问限制"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# RSRenderNodeMap线程访问限制

## 问题描述

RSRenderNodeMap只能在RSMainThread类（主线程）访问，不允许在其它线程访问。**RSMainThread类负责渲染的Prepare阶段**，需要访问RenderNodeMap进行节点遍历、遮挡计算等操作。RenderNodeMap存储渲染节点映射关系，是RSMainThread类的核心数据结构。RSUniRenderThread类（Process阶段）或其他线程访问会导致数据竞争和状态不一致。

**渲染流程说明**：
- RSMainThread类：负责Prepare及以前阶段，可以访问RenderNodeMap进行节点管理
- RSUniRenderThread类：负责Process及以后阶段，不应直接访问RenderNodeMap，应使用副本数据

## 检测示例

### 错误示例

```cpp
// 错误示例1：RSUniRenderThread类访问RenderNodeMap
void RSUniRenderThread::ProcessRender()
{
    // 错误：RSUniRenderThread类访问RenderNodeMap
    auto nodeMap = GetRenderNodeMap();  // 错误：非RSMainThread类访问
    auto node = nodeMap->GetNode(surfaceId);  // 错误
}

// 错误示例2：IO线程访问RenderNodeMap
void IOThread::OnDataReceived()
{
    // 错误：IO线程访问RenderNodeMap
    auto node = renderNodeMap_->FindNodeById(nodeId);  // 错误
    node->UpdateFromData(data);  // 错误
}

// 错误示例3：Worker线程操作RenderNodeMap
class RenderWorker {
public:
    void DoWork() {
        // 错误：Worker线程修改RenderNodeMap
        g_renderNodeMap->RegisterNode(newNode);  // 错误
    }
};

// 错误示例4：回调中访问RenderNodeMap
void OnSurfaceCreatedCallback(SurfaceId id)
{
    // 错误：回调可能在非主线程执行
    auto node = renderNodeMap_->GetNode(id);  // 错误
}
```

### 正确示例

```cpp
// 正确示例1：RS主线程访问RenderNodeMap
void RSMainThread::HandleSurfaceCreated(SurfaceId id)
{
    // 正确：主线程访问RenderNodeMap
    auto nodeMap = GetRenderNodeMap();  // 正确
    auto node = nodeMap->GetNode(id);  // 正确
    node->Initialize();
}

// 正确示例2：通过命令传递到主线程
void IOThread::OnDataReceived(NodeId id, const Data& data)
{
    // 正确：通过命令传递
    UpdateNodeCommand cmd;
    cmd.nodeId = id;
    cmd.data = data;
    
    SubmitToMainThread(cmd);  // 正确：发送到主线程处理
}

// 正确示例3：主线程处理回调
void RSMainThread::OnCallbackReceived(const Callback& cb)
{
    // 正确：主线程处理回调中的RenderNodeMap操作
    if (cb.type == UPDATE_NODE) {
        auto node = renderNodeMap_->GetNode(cb.nodeId);  // 正确
        node->UpdateFromCallback(cb);
    }
}

// 正确示例4：RSUniRenderThread类使用副本数据
void RSUniRenderThread::RenderFrame()
{
    // 正确：使用RSMainThread类传递的副本数据
    auto renderList = GetRenderListCopy();  // 正确：不直接访问Map
    
    for (auto& item : renderList) {
        RenderItem(item);
    }
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 非RSMainThread类（RS主线程）访问RSRenderNodeMap
- **RISK_TYPE**: 线程安全违规
- **RISK_PATH**: 非RSMainThread类访问RSRenderNodeMap -> 数据竞争 -> 渲染状态不一致
- **IMPACT_POINT**: 渲染异常、崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: 非RSMainThread类访问RSRenderNodeMap
- **Propagation**: 数据竞争、状态不一致
- **Consequence**: 渲染异常、界面错乱、崩溃
- **Mitigation**: RSRenderNodeMap只能在RSMainThread类访问

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 主线程上下文 | RSMainThread:: | 不报 |
| 使用副本数据 | GetRenderListCopy() | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// RSUniRenderThread类访问RenderNodeMap
void RSUniRenderThread::OnRender()
{
    auto node = renderNodeMap->GetNode(id);  // 应该报：非RSMainThread类访问
}
```

### 安全用例（不应该报）

```cpp
// RSMainThread类访问RenderNodeMap
void RSMainThread::HandleNode()
{
    auto node = renderNodeMap->GetNode(id);  // 不报：RSMainThread类访问
}
```