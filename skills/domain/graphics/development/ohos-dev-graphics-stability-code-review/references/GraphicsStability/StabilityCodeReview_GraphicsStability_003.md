---
rule_id: "StabilityCodeReview_GraphicsStability_003"
name: "RS主线程禁止使用RenderNodeDrawable"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# RS主线程禁止使用RenderNodeDrawable

## 问题描述

RSMainThread类（RS主线程）不能使用RenderNodeDrawable，只能产生RenderNodeDrawable。**RSMainThread类负责渲染的Prepare及以前阶段**，包括处理事务数据、执行动画、计算遮挡、准备渲染数据等，而RenderNodeDrawable的实际绘制操作应在RSUniRenderThread类（Process及以后阶段）执行。如果在RSMainThread类中直接使用RenderNodeDrawable执行绘制，会破坏线程模型，引发渲染异常或崩溃。

**渲染流程说明**：
- RSMainThread类：负责Prepare及以前阶段（OnVsync → ProcessCommand → Animate → Prepare → CalcOcclusion → Sync）
- RSUniRenderThread类：负责Process及以后阶段（Render → OnDraw → GPU操作 → 资源管理）

## 检测示例

### 错误示例

```cpp
// 错误示例1：RS主线程直接使用RenderNodeDrawable绘制
void RSMainThread::OnRender()
{
    auto drawable = GetRenderNodeDrawable();  // 错误：主线程获取Drawable
    
    // 错误：主线程直接执行绘制操作
    drawable->Draw(canvas);  // 错误：主线程不应执行绘制
    
    // 错误：主线程操作Drawable状态
    drawable->SetVisible(true);  // 错误：主线程不应操作Drawable
}

// 错误示例2：主线程回调中使用RenderNodeDrawable
class MainThreadHandler {
public:
    void HandleRenderCommand()
    {
        if (IsMainThread()) {
            auto drawable = node->GetDrawable();  // 错误：主线程获取
            drawable->UpdateContent();  // 错误：主线程使用
        }
    }
};
```

### 正确示例

```cpp
// 正确示例1：RS主线程只产生RenderNodeDrawable
void RSMainThread::ProcessCommand()
{
    auto node = CreateRenderNode();
    auto drawable = RenderNodeDrawable::Create(node);  // 正确：主线程创建
    
    // 正确：提交到渲染线程执行
    SubmitToRenderThread(drawable);
}

// 正确示例2：渲染线程使用RenderNodeDrawable
void RenderThread::OnRender()
{
    auto drawable = GetPendingDrawable();  // 正确：渲染线程获取
    
    // 正确：渲染线程执行绘制
    drawable->Draw(canvas);  // 正确：渲染线程绘制
}

// 正确示例3：主线程通过命令传递
void RSMainThread::UpdateNode()
{
    UpdateRenderNodeCommand cmd;
    cmd.nodeId = node->GetId();
    cmd.content = newContent;
    
    SubmitCommand(cmd);  // 正确：通过命令传递，不直接操作Drawable
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: RSMainThread类使用RenderNodeDrawable
- **RISK_TYPE**: 线程职责越界
- **RISK_PATH**: RSMainThread类使用RenderNodeDrawable -> 线程安全风险 -> 渲染异常或崩溃
- **IMPACT_POINT**: 渲染异常、线程安全问题

## 影响分析（ImpactAnalysis）

- **Trigger**: RSMainThread类直接操作RenderNodeDrawable
- **Propagation**: 破坏渲染线程模型
- **Consequence**: 渲染异常、界面卡顿、崩溃
- **Mitigation**: RSMainThread类只产生RenderNodeDrawable，不直接使用

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 创建操作 | RenderNodeDrawable::Create, OnGenerate | 不报（允许创建）|
| 渲染线程上下文 | RSUniRenderThread::, RenderThread:: | 不报 |
| 通过Drawable访问Node | drawable->GetRenderNode() | 不报（允许Get）|

### 创建vs使用的场景区分

RSMainThread允许**创建**RenderNodeDrawable，但禁止**使用**（绘制）：

#### ✅ 允许场景（创建RenderNodeDrawable）

```cpp
// 正确场景1：创建RenderNodeDrawable
void RSMainThread::PrepareNode(RSRenderNode& node)
{
    auto drawable = RenderNodeDrawable::OnGenerate(node);  // ✅ 允许创建
    node.SetDrawable(drawable);  // ✅ 允许设置
}

// 正确场景2：获取Drawable但不执行绘制
void RSMainThread::ProcessNode(RSRenderNode& node)
{
    auto drawable = node.GetDrawable();  // ✅ 允许获取
    if (drawable) {
        drawable->UpdateBounds(node.GetBounds());  // ✅ 允许Prepare阶段的状态更新
    }
}

// 正确场景3：Prepare阶段的状态准备
void RSMainThread::PrepareRenderNode(RSRenderNode& node)
{
    auto drawable = RenderNodeDrawable::Create(node);  // ✅ 允许创建
    drawable->SetPrepareData(data);  // ✅ 允许Prepare数据设置
}
```

#### ❌ 禁止场景（使用RenderNodeDrawable执行绘制）

```cpp
// 错误场景1：主线程执行Draw绘制
void RSMainThread::RenderFrame()
{
    auto drawable = GetDrawable();
    drawable->Draw(canvas);  // ❌ 禁止：主线程不应绘制
}

// 错误场景2：主线程执行OnDraw
void RSMainThread::OnRender()
{
    auto drawable = GetDrawable();
    drawable->OnDraw(canvas);  // ❌ 禁止：主线程不应OnDraw
}

// 错误场景3：主线程执行GPU相关绘制命令
void RSMainThread::RenderNode()
{
    auto drawable = GetDrawable();
    drawable->RenderContent();  // ❌ 禁止：GPU绘制操作
}
```

### RenderNodeDrawable生命周期

理解RenderNodeDrawable的两个阶段：

- **Prepare阶段（RSMainThread）**：
  - 创建RenderNodeDrawable
  - 设置Prepare数据（bounds、content等）
  - 更新Drawable状态（可见性、脏区域等）
  - 不执行实际的绘制操作

- **Process阶段（RSUniRenderThread）**：
  - 获取已创建的Drawable
  - 执行Draw/OnDraw绘制
  - 执行GPU相关操作
  - 资源管理和清理

### 检测规则细化

**应该报的情况**：
- RSMainThread中调用`drawable->Draw(canvas)`
- RSMainThread中调用`drawable->OnDraw(canvas)`
- RSMainThread中调用`drawable->RenderContent()`
- RSMainThread中执行GPU绘制命令

**不应该报的情况**：
- RSMainThread中调用`RenderNodeDrawable::Create(node)`
- RSMainThread中调用`RenderNodeDrawable::OnGenerate(node)`
- RSMainThread中调用`drawable->GetRenderNode()`
- RSMainThread中调用`drawable->UpdateBounds(bounds)`（Prepare数据）
- RSUniRenderThread中的任何Drawable操作
## 测试用例

### 触发用例（应该报）

```cpp
// RSMainThread上下文中使用RenderNodeDrawable
void RSMainThread::OnRender()
{
    auto drawable = GetRenderNodeDrawable();
    drawable->Draw(canvas);  // 应该报：主线程不应绘制
}
```

### 安全用例（不应该报）

```cpp
// RSMainThread只创建RenderNodeDrawable
void RSMainThread::CreateDrawable()
{
    auto drawable = RenderNodeDrawable::Create(node);  // 不报：允许创建
    SubmitToRenderThread(drawable);
}

// 渲染线程使用RenderNodeDrawable
void RenderThread::OnRender()
{
    drawable->Draw(canvas);  // 不报：渲染线程允许使用
}
```