---
rule_id: "StabilityCodeReview_GraphicsStability_002"
name: "VulkanCleanUpHelper与SharedContext引用计数混用"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# VulkanCleanUpHelper与SharedContext引用计数混用

## 问题描述

VulkanCleanUpHelper与SharedContext分属两套引用计数管理，不能混用。同一资源不能同时使用两种引用计数机制管理，否则会导致引用计数不一致，引发资源泄漏或提前释放。

## 检测示例

### 错误示例

```cpp
// 错误示例1：同一资源使用两种引用计数管理
class TextureManager {
public:
    sk_sp<Surface> CreateSurface(
        GrDirectContext* context,
        const GrBackendTexture& backendTexture,
        VulkanCleanUpHelper* cleanUpHelper,
        SharedContext* sharedContext)
    {
        // 错误：同时使用VulkanCleanUpHelper和SharedContext
        auto surface = Surface::MakeFromBackendTexture(
            context, backendTexture, kTopLeft_GrSurfaceOrigin,
            1, kRGBA_8888_SkColorType, 
            sharedContext->GetSurfaceProps(),  // SharedContext引用计数
            cleanUpHelper);  // VulkanCleanUpHelper引用计数
        return surface;  // 错误：两套引用计数混用
    }
};

// 错误示例2：引用计数操作混用
class ImageResource {
public:
    void AddRef() {
        cleanUpHelper_->ref();  // VulkanCleanUpHelper引用
        sharedContext_->AddRef();  // SharedContext引用  // 错误：混用
    }
    
    void Release() {
        cleanUpHelper_->unref();  // VulkanCleanUpHelper释放
        sharedContext_->Release();  // SharedContext释放  // 错误：混用
    }
    
private:
    VulkanCleanUpHelper* cleanUpHelper_;
    SharedContext* sharedContext_;
};
```

### 正确示例

```cpp
// 正确示例1：仅使用VulkanCleanUpHelper管理
class TextureManager {
public:
    sk_sp<Surface> CreateSurface(
        GrDirectContext* context,
        const GrBackendTexture& backendTexture,
        VulkanCleanUpHelper* cleanUpHelper)
    {
        auto surface = Surface::MakeFromBackendTexture(
            context, backendTexture, kTopLeft_GrSurfaceOrigin,
            1, kRGBA_8888_SkColorType, nullptr, cleanUpHelper);  // 正确：仅使用一套机制
        return surface;
    }
};

// 正确示例2：仅使用SharedContext管理
class ImageManager {
public:
    sk_sp<Image> CreateImage(
        SharedContext* sharedContext,
        const GrBackendTexture& backendTexture)
    {
        auto image = sharedContext->CreateImageFromBackendTexture(backendTexture);  // 正确
        return image;
    }
};
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: VulkanCleanUpHelper与SharedContext引用计数混用
- **RISK_TYPE**: 引用计数管理冲突
- **RISK_PATH**: 两套引用计数机制混用 -> 引用计数不一致 -> 资源泄漏或提前释放
- **IMPACT_POINT**: 内存泄漏、GPU崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: 同一资源使用两种引用计数管理
- **Propagation**: 引用计数机制冲突，计数不一致
- **Consequence**: 资源泄漏或提前释放、GPU崩溃、渲染异常
- **Mitigation**: 选择一种引用计数机制统一管理，不要混用

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 仅使用一种机制 | 只存在一种引用计数 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// 错误：混用两套引用计数
void MixedRefCount()
{
    cleanUpHelper->ref();  // VulkanCleanUpHelper
    sharedContext->AddRef();  // SharedContext  // 应该报
}
```

### 安全用例（不应该报）

```cpp
// 正确：仅使用一套引用计数
void SingleRefCount()
{
    cleanUpHelper->ref();  // 仅VulkanCleanUpHelper  // 不报
}
```