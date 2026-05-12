---
rule_id: "StabilityCodeReview_GraphicsStability_007"
name: "Surface/Image创建和释放线程一致性"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Surface/Image创建和释放线程一致性

## 问题描述

Surface/Image涉及GPU资源，创建和释放应处于同一线程。跨线程创建和释放会导致GPU驱动状态不一致，引发资源泄漏或提前释放。

## 检测示例

### 错误示例

```cpp
// 错误示例1：主线程创建，渲染线程释放
void MainThread_Create()
{
    auto surface = Surface::MakeRenderTarget(context, info);  // 主线程创建
    g_surface = surface;  // 传递给全局
}

void RenderThread_Release()
{
    // 错误：渲染线程释放主线程创建的Surface
    g_surface.reset();  // 错误：跨线程释放
}

// 错误示例2：异步创建，同步释放
class AsyncImageCreator {
public:
    void CreateAsync() {
        std::thread t([this]() {
            image_ = Image::MakeFromEncoded(data);  // 异步线程创建
        });
        t.detach();
    }
    
    void ReleaseSync() {
        // 错误：主线程释放异步线程创建的Image
        image_.reset();  // 错误：跨线程释放
    }
    
private:
    sk_sp<Image> image_;
};

// 错误示例3：回调创建，主线程释放
void OnTextureLoadedCallback(Texture* texture)
{
    g_image = Image::MakeFromTexture(texture);  // IO线程创建
}

void MainThread_Cleanup()
{
    // 错误：主线程释放IO线程创建的Image
    g_image = nullptr;  // 错误：跨线程释放
}
```

### 正确示例

```cpp
// 正确示例1：同一线程创建和释放
void RenderThread_Lifecycle()
{
    // 正确：渲染线程创建
    auto surface = Surface::MakeRenderTarget(context, info);
    
    // 使用Surface
    RenderWithSurface(surface);
    
    // 正确：渲染线程释放
    surface.reset();  // 正确：同一线程释放
}

// 正确示例2：主线程管理全生命周期
class SurfaceManager {
public:
    void Create() {
        // 正确：主线程创建
        surface_ = Surface::MakeRenderTarget(context_, info_);
    }
    
    void Release() {
        // 正确：主线程释放
        surface_.reset();  // 正确：同一线程释放
    }
    
private:
    sk_sp<Surface> surface_;
    GrDirectContext* context_;
};

// 正确示例3：通过BackendTexture跨线程安全传递
void ThreadA_CreateBackendTexture()
{
    auto surface = Surface::MakeRenderTarget(contextA, info);
    BackendTexture backend = surface->getBackendTexture();
    
    // 正确：传递BackendTexture而非Surface
    SendToThreadB(backend);  // 正确
}

void ThreadB_CreateFromBackend()
{
    BackendTexture backend = ReceiveFromThreadA();
    // 正确：线程B创建新的Surface
    auto surface = Surface::MakeFromBackendTexture(contextB, backend, ...);  // 正确
    
    // 正确：线程B释放自己创建的Surface
    surface.reset();  // 正确
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: Surface/Image创建和释放不在同一线程
- **RISK_TYPE**: 线程安全违规
- **RISK_PATH**: 跨线程创建和释放 -> GPU驱动状态不一致 -> 资源泄漏或提前释放
- **IMPACT_POINT**: GPU资源泄漏或提前释放

## 影响分析（ImpactAnalysis）

- **Trigger**: 跨线程释放GPU资源
- **Propagation**: GPU驱动状态不一致
- **Consequence**: GPU崩溃、内存泄漏、渲染异常
- **Mitigation**: 确保Surface/Image在同一线程创建和释放

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 同线程创建释放 | 上下文分析确认同线程 | 不报 |
| 使用BackendTexture | MakeFromBackendTexture | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// 在MainThread创建，在RenderThread释放
void MainThread_Create()
{
    sk_sp<Surface> surface = Surface::MakeRenderTarget(...);  // 主线程创建
    g_surface = surface;
}

void RenderThread_Release()
{
    g_surface.reset();  // 应该报：跨线程释放
}
```

### 安全用例（不应该报）

```cpp
// 同一线程创建和释放
void RenderThread_Lifecycle()
{
    sk_sp<Surface> surface = Surface::MakeRenderTarget(...);  // 渲染线程创建
    surface.reset();  // 不报：同一线程释放
}
```