---
rule_id: "StabilityCodeReview_GraphicsStability_004"
name: "RSUniRenderThread禁止访问RenderNode"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# RSUniRenderThread禁止访问RenderNode

## 问题描述

RSUniRenderThread类（统一渲染线程）不能访问RenderNode。**RSUniRenderThread类负责渲染的Process及以后阶段**，包括执行绘制命令、GPU操作、资源管理等。访问RenderNode应在RSMainThread类（Prepare阶段）进行，RSUniRenderThread类通过命令或Drawable间接获取渲染信息。

**渲染流程说明**：
- RSMainThread类：负责Prepare及以前阶段（OnVsync → ProcessCommand → Animate → Prepare → CalcOcclusion → Sync），可以直接访问RenderNode
- RSUniRenderThread类：负责Process及以后阶段（Render → OnDraw → GPU操作 → 资源管理），不应直接访问RenderNode

## 检测示例

### 错误示例

```cpp
// 错误示例1：RSUniRenderThread类直接访问RenderNode
void RSUniRenderThread::RenderFrame()
{
    auto node = GetRenderNode(id);  // 错误：RSUniRenderThread类获取RenderNode
    
    // 错误：RSUniRenderThread类直接操作RenderNode
    node->UpdateContent();  // 错误：不应在RSUniRenderThread类访问
    
    // 错误：RSUniRenderThread类读取RenderNode状态
    auto bounds = node->GetBounds();  // 错误：不应在RSUniRenderThread类访问
}

// 错误示例2：RSUniRenderThread类回调中访问RenderNode
class UniRenderCallback {
public:
    void OnRenderComplete()
    {
        if (IsUniRenderThread()) {
            RenderNode* node = nodeMap_->GetNode(surfaceId);  // 错误
            node->SetRenderComplete();  // 错误
        }
    }
};
```

### 正确示例

```cpp
// 正确示例1：RSUniRenderThread类通过Drawable获取信息
void RSUniRenderThread::RenderFrame()
{
    auto drawable = GetDrawableForRender();  // 正确：通过Drawable
    
    // 正确：从Drawable获取渲染信息
    drawable->Draw(canvas);  // 正确：不直接访问RenderNode
}

// 正确示例2：RSUniRenderThread类通过命令接收数据
void RSUniRenderThread::ProcessCommand(const RenderCommand& cmd)
{
    // 正确：从命令中获取需要的信息
    auto bounds = cmd.bounds;
    auto content = cmd.content;
    
    RenderInternal(bounds, content);  // 正确：使用命令数据
}

// 正确示例3：RSMainThread类管理RenderNode
void RSMainThread::UpdateRenderNode(NodeId id, const Content& content)
{
    auto node = GetRenderNode(id);  // 正确：RSMainThread类访问
    node->UpdateContent(content);  // 正确：RSMainThread类操作
    
    // 正确：通知RSUniRenderThread类
    SubmitRenderCommand(id, node->GetBounds());
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: RSUniRenderThread类访问RenderNode
- **RISK_TYPE**: 线程访问越界
- **RISK_PATH**: RSUniRenderThread类访问RenderNode -> 线程安全风险 -> 数据竞争
- **IMPACT_POINT**: 渲染数据不一致、崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: RSUniRenderThread类直接访问RenderNode
- **Propagation**: 破坏线程模型，引发数据竞争
- **Consequence**: 渲染异常、数据损坏、崩溃
- **Mitigation**: RSUniRenderThread类不应直接访问RenderNode

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 主线程上下文 | RSMainThread:: | 不报 |
| 通过Drawable间接获取 | drawable->GetRenderNode().lock() | 不报（允许间接获取）|
| 只读访问 | drawable->GetNodeBounds() | 不报（从Drawable获取数据）|

### 间接获取vs直接访问的场景区分

RSUniRenderThread允许通过Drawable**间接获取**RenderNode信息，但禁止**直接访问**RenderNode对象：

#### ✅ 允许场景（通过Drawable间接获取）

```cpp
// 正确场景1：通过Drawable获取Node信息
void RSUniRenderThread::RenderDrawable(RSRenderNodeDrawable* drawable)
{
    auto node = drawable->GetRenderNode().lock();  // ✅ 允许：通过Drawable间接获取
    if (!node) {
        return;
    }
    // 使用node的只读信息进行绘制准备
    auto bounds = node->GetBounds();  // ✅ 允许：通过Drawable获取的只读访问
}

// 正确场景2：从Drawable获取渲染数据
void RSUniRenderThread::DrawContent(RSRenderNodeDrawable* drawable)
{
    // Drawable已经缓存了必要的渲染数据
    drawable->Draw(canvas);  // ✅ 允许：使用Drawable绘制
    
    // 不直接访问Node获取数据
    // auto node = nodeMap_->GetNode(id);  // ❌ 禁止
}

// 正确场景3：使用Drawable缓存的Prepare数据
void RSUniRenderThread::ProcessDrawable()
{
    auto drawable = GetDrawable();
    auto bounds = drawable->GetCachedBounds();  // ✅ 允许：使用Drawable缓存的数据
    auto content = drawable->GetCachedContent();  // ✅ 允许
}
```

#### ❌ 禁止场景（直接访问RenderNode）

```cpp
// 错误场景1：通过NodeMap直接获取RenderNode
void RSUniRenderThread::RenderFrame()
{
    auto node = nodeMap_->GetNode(nodeId);  // ❌ 禁止：直接访问NodeMap
    node->UpdateContent();  // ❌ 禁止：直接操作RenderNode
}

// 错误场景2：通过全局容器访问RenderNode
void RSUniRenderThread::ProcessNodes()
{
    for (auto& node : globalNodeList) {  // ❌ 禁止：直接遍历Node容器
        node->Render();  // ❌ 禁止
    }
}

// 错误场景3：通过id直接查询RenderNode
void RSUniRenderThread::OnRender(NodeId id)
{
    RSRenderNode* node = RSBaseRenderNode::GetNodeById(id);  // ❌ 禁止：直接查询
    auto bounds = node->GetBounds();  // ❌ 禁止
}
```

### RenderNode访问路径说明

理解RenderNode的两种访问路径：

- **RSMainThread路径**（允许直接访问）：
  - `GetRenderNode(id)` - 直接从NodeMap获取
  - `RSRenderNode::GetNodeById(id)` - 直接查询
  - 可以执行Update、Prepare等操作

- **RSUniRenderThread路径**（只能间接访问）：
  - `drawable->GetRenderNode().lock()` - 通过Drawable获取weak_ptr
  - `drawable->GetCachedXXX()` - 使用Drawable缓存的数据
  - 只能读取Prepare阶段缓存的数据，不能修改

### 检测规则细化

**应该报的情况**：
- RSUniRenderThread中调用`nodeMap_->GetNode(id)`
- RSUniRenderThread中调用`RSBaseRenderNode::GetNodeById(id)`
- RSUniRenderThread中直接操作`RSRenderNode*`指针
- RSUniRenderThread中遍历`globalNodeList`等Node容器

**不应该报的情况**：
- RSUniRenderThread中调用`drawable->GetRenderNode().lock()`（通过Drawable间接获取）
- RSUniRenderThread中调用`drawable->GetCachedXXX()`（使用Drawable缓存数据）
- RSMainThread中的任何RenderNode访问
- Prepare阶段的RenderNode操作（在RSMainThread中）
## 测试用例

### 触发用例（应该报）

```cpp
// RSUniRenderThread类访问RenderNode
void RSUniRenderThread::OnRender()
{
    RenderNode* node = GetRenderNode(id);  // 应该报
    node->GetBounds();  // 应该报
}
```

### 安全用例（不应该报）

```cpp
// RSMainThread类访问RenderNode
void RSMainThread::UpdateNode()
{
    RenderNode* node = GetRenderNode(id);  // 不报：RSMainThread类允许
}

// RSUniRenderThread类使用Drawable
void RSUniRenderThread::OnRender()
{
    auto drawable = GetDrawable();  // 不报
    drawable->Draw(canvas);  // 不报
}
```