---
rule_id: "StabilityCodeReview_GraphicsStability_008"
name: "GetBackendTexture线程限制"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# GetBackendTexture线程限制

## 问题描述

Surface/Image只能在其创建的线程中使用GetBackendTexture。在非创建线程调用GetBackendTexture会导致GPU资源状态不一致，引发纹理损坏或崩溃。

## 检测示例

### 错误示例

```cpp
// 错误示例1：IO线程创建Surface，渲染线程GetBackendTexture
class TextureLoader {
public:
    void LoadOnIOThread() {
        // IO线程创建Surface
        surface_ = Surface::MakeRenderTarget(contextIO, info);  // IO线程创建
    }
    
    void GetTextureOnRenderThread() {
        // 错误：渲染线程调用GetBackendTexture
        BackendTexture backend = surface_->GetBackendTexture();  // 错误：跨线程
    }
    
private:
    sk_sp<Surface> surface_;
};

// 错误示例2：主线程创建Image，其他线程GetBackendTexture
void MainThread_CreateImage()
{
    g_image = Image::MakeFromEncoded(encodedData);  // 主线程创建
}

void WorkerThread_GetBackendTexture()
{
    // 错误：Worker线程调用GetBackendTexture
    BackendTexture backend = g_image->GetBackendTexture();  // 错误：跨线程
}

// 错误示例3：异步回调中使用GetBackendTexture
void OnSurfaceReady(Surface* surface)
{
    // 在回调线程（非创建线程）中调用
    BackendTexture backend = surface->GetBackendTexture();  // 错误
}
```

### 正确示例

```cpp
// 正确示例1：创建线程调用GetBackendTexture
void RenderThread_Lifecycle()
{
    // 正确：渲染线程创建
    auto surface = Surface::MakeRenderTarget(context, info);
    
    // 正确：渲染线程调用GetBackendTexture
    BackendTexture backend = surface->GetBackendTexture();  // 正确：同线程
    
    // 使用backend创建新资源
    auto newSurface = Surface::MakeFromBackendTexture(context, backend, ...);
}

// 正确示例2：在创建Surface的线程传递BackendTexture
class SafeTextureManager {
public:
    void CreateAndExport() {
        // 主线程创建
        surface_ = Surface::MakeRenderTarget(context_, info_);
        
        // 正确：主线程获取BackendTexture
        BackendTexture backend = surface_->GetBackendTexture();  // 正确
        
        // 正确：传递BackendTexture给其他线程使用
        SendBackendTextureToRenderThread(backend);
    }
    
private:
    sk_sp<Surface> surface_;
};

// 正确示例3：每个线程独立创建和访问
void ThreadA_OwnedSurface()
{
    auto surface = Surface::MakeRenderTarget(contextA, info);
    BackendTexture backend = surface->GetBackendTexture();  // 正确：同线程
}

void ThreadB_OwnedSurface()
{
    auto surface = Surface::MakeRenderTarget(contextB, info);
    BackendTexture backend = surface->GetBackendTexture();  // 正确：同线程
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: GetBackendTexture跨线程调用
- **RISK_TYPE**: 线程安全违规
- **RISK_PATH**: 在非创建线程调用GetBackendTexture -> GPU资源状态不一致 -> 纹理损坏
- **IMPACT_POINT**: GPU崩溃、纹理损坏、渲染异常

## 影响分析（ImpactAnalysis）

- **Trigger**: 非创建线程调用GetBackendTexture
- **Propagation**: GPU资源状态不一致
- **Consequence**: GPU崩溃、纹理损坏、渲染异常
- **Mitigation**: GetBackendTexture只能在创建Surface/Image的线程调用

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 同线程创建访问 | 上下文分析确认同线程 | 不报 |
| 传递BackendTexture | 通过参数传递BackendTexture | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// IOThread创建，RenderThread调用GetBackendTexture
void IOThread_Create()
{
    g_surface = Surface::MakeRenderTarget(...);
}

void RenderThread_GetBackend()
{
    BackendTexture backend = g_surface->GetBackendTexture();  // 应该报：跨线程
}
```

### 安全用例（不应该报）

```cpp
// 同一线程创建和GetBackendTexture
void RenderThread_CreateAndGet()
{
    sk_sp<Surface> surface = Surface::MakeRenderTarget(...);  // 渲染线程创建
    BackendTexture backend = surface->GetBackendTexture();  // 不报：同线程
}
```