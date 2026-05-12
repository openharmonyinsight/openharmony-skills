---
rule_id: "StabilityCodeReview_GraphicsStability_005"
name: "RS主线程禁止GPU Context操作"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# RS主线程禁止GPU Context操作

## 问题描述

RSMainThread类（RS主线程）不能做任何与GPU Context相关的操作。**RSMainThread类负责渲染的Prepare及以前阶段**，包括处理事务数据、执行动画、计算遮挡、准备渲染数据等。GPU Context操作（如flush、submit、MakeCurrent、SwapBuffers等）属于Process阶段，应在RSUniRenderThread类执行。RSMainThread类执行这些操作会阻塞Prepare阶段，导致卡顿或ANR。

**渲染流程说明**：
- RSMainThread类：负责Prepare及以前阶段（OnVsync → ProcessCommand → Animate → Prepare → CalcOcclusion → Sync）
- RSUniRenderThread类：负责Process及以后阶段（Render → OnDraw → GPU操作 → 资源管理）

## 检测示例

### 错误示例

```cpp
// 错误示例1：RS主线程执行GPU flush
void RSMainThread::RenderFrame()
{
    auto context = GetGPUContext();
    
    // 错误：主线程执行flush
    context->flush();  // 错误：阻塞主线程
    
    // 错误：主线程执行submit
    context->submit();  // 错误：阻塞主线程
}

// 错误示例2：RS主线程执行SwapBuffers
void RSMainThread::OnSurfaceChanged()
{
    if (IsMainThread()) {
        // 错误：主线程执行SwapBuffers
        SwapBuffers();  // 错误：阻塞主线程
    }
}

// 错误示例3：RS主线程创建GPU Context
void RSMainThread::Initialize()
{
    // 错误：主线程创建GPU Context
    auto context = GrDirectContext::MakeGL();  // 错误
    
    // 错误：主线程MakeCurrent
    MakeCurrent(context);  // 错误
}
```

### 正确示例

```cpp
// 正确示例1：渲染线程执行GPU Context操作
void RenderThread::OnRender()
{
    auto context = GetGPUContext();
    
    // 正确：渲染线程执行flush
    context->flush();  // 正确
    
    // 正确：渲染线程执行submit
    context->submit();  // 正确
    
    // 正确：渲染线程SwapBuffers
    SwapBuffers();  // 正确
}

// 正确示例2：主线程通过命令通知渲染线程
void RSMainThread::RequestRender()
{
    // 正确：发送渲染命令
    RenderCommand cmd;
    cmd.type = RENDER_TYPE_FLUSH;
    SubmitToRenderThread(cmd);  // 正确：不直接操作GPU
}

// 正确示例3：主线程只负责命令构建
void RSMainThread::BuildRenderCommands()
{
    // 正确：构建渲染命令，不执行GPU操作
    auto node = GetRenderNode();
    auto cmd = BuildCommandFromNode(node);  // 正确
    
    SubmitToRenderThread(cmd);  // 正确
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: RSMainThread类执行GPU Context操作
- **RISK_TYPE**: 线程职责越界
- **RISK_PATH**: RSMainThread类操作GPU Context -> 阻塞主线程 -> UI卡顿或崩溃
- **IMPACT_POINT**: UI卡顿、渲染异常

## 影响分析（ImpactAnalysis）

- **Trigger**: RSMainThread类调用GPU Context相关API
- **Propagation**: 阻塞主线程执行
- **Consequence**: UI卡顿、响应超时、ANR
- **Mitigation**: 将GPU Context操作移至渲染线程执行

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 渲染线程上下文 | RSUniRenderThread::, RenderThread:: | 不报 |
| 获取Context指针 | GetGPUContext() | 不报（允许获取）|
| 内存清理场景 | context->abandonedContext(), PurgeCache | 不报（内存清理）|

### GPU Context操作的场景区分

RSMainThread禁止常规的GPU Context操作，但内存清理等特定场景允许：

#### ❌ 禁止场景（阻塞主线程的GPU操作）

```cpp
// 错误场景1：主线程执行渲染flush
void RSMainThread::RenderFrame()
{
    auto context = GetGPUContext();
    context->flush();  // ❌ 禁止：阻塞主线程
}

// 错误场景2：主线程执行SwapBuffers
void RSMainThread::OnVsync()
{
    SwapBuffers();  // ❌ 禁止：阻塞主线程
}

// 错误场景3：主线程执行GPU绘制
void RSMainThread::DrawContent()
{
    auto context = GetGPUContext();
    context->MakeCurrent();  // ❌ 禁止：GPU绑定
    DrawOnGPU();  // ❌ 禁止：GPU绘制
}
```

#### ✅ 允许场景（内存清理和非阻塞操作）

```cpp
// 正确场景1：内存清理时abandonedContext
void RSMainThread::PurgeMemory()
{
    auto context = GetGPUContext();
    if (context) {
        context->abandonedContext();  // ✅ 允许：内存清理，不阻塞
    }
}

// 正确场景2：释放GPU资源（内存压力响应）
void RSMainThread::OnMemoryPressure()
{
    auto context = GetGPUContext();
    context->purgeCache();  // ✅ 允许：清理GPU缓存，释放内存
    
    // 内存清理场景，不执行渲染
}

// 正确场景3：销毁Context（进程退出）
void RSMainThread::OnDestroy()
{
    auto context = GetGPUContext();
    if (context) {
        context->release();  // ✅ 允许：资源释放，不渲染
    }
}

// 正确场景4：获取Context但不操作
void RSMainThread::CheckContextValid()
{
    auto context = GetGPUContext();  // ✅ 允许：仅获取指针
    if (context && context->isValid()) {  // ✅ 允许：仅判断有效性
        // 不执行GPU渲染操作
    }
}
```

### GPU Context操作分类

根据是否阻塞主线程，将GPU Context操作分为两类：

- **阻塞型操作**（RSMainThread禁止）：
  - `flush()` - 等待GPU完成
  - `submit()` - 提交渲染命令
  - `SwapBuffers()` - 交换缓冲区
  - `MakeCurrent()` - GPU绑定
  - 实际的GPU绘制操作
  - 等待GPU Fence

- **非阻塞型操作**（RSMainThread可能允许）：
  - `abandonedContext()` - 放弃Context（内存清理）
  - `purgeCache()` - 清理GPU缓存（内存压力）
  - `release()` - 释放资源（进程退出）
  - `isValid()` - 判断有效性（不执行操作）
  - `GetGPUContext()` - 获取指针（不执行操作）

### 检测规则细化

**应该报的情况**：
- RSMainThread中调用`context->flush()`
- RSMainThread中调用`context->submit()`
- RSMainThread中调用`SwapBuffers()`
- RSMainThread中调用`context->MakeCurrent()`
- RSMainThread中执行GPU绘制操作

**不应该报的情况**：
- RSMainThread中调用`context->abandonedContext()`（内存清理）
- RSMainThread中调用`context->purgeCache()`（内存清理）
- RSMainThread中调用`context->release()`（资源释放）
- RSMainThread中调用`GetGPUContext()`（仅获取）
- RSMainThread中调用`context->isValid()`（仅判断）
- RSUniRenderThread中的任何GPU Context操作
## 测试用例

### 触发用例（应该报）

```cpp
// RSMainThread中执行GPU Context操作
void RSMainThread::OnRender()
{
    context->flush();  // 应该报：主线程不应flush
    context->submit();  // 应该报
    SwapBuffers();  // 应该报
}
```

### 安全用例（不应该报）

```cpp
// 渲染线程执行GPU Context操作
void RenderThread::OnRender()
{
    context->flush();  // 不报：渲染线程允许
}

// 主线程获取Context但不操作
void RSMainThread::GetContext()
{
    auto context = GetGPUContext();  // 不报：允许获取
}
```