---
rule_id: "StabilityCodeReview_GraphicsStability_001"
name: "VulkanCleanupHelper引用计数管理"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# VulkanCleanupHelper引用计数管理

## 问题描述

使用`MakeFromBackendTexture`或`BuildFromTexture`创建GPU资源时，应正确使用`NativeBufferUtils::VulkanCleanupHelper`管理VkImage的引用计数。首次传入`vulkanCleanupHelper`，后续传入`vulkanCleanupHelper->Ref()`，配合`NativeBufferUtils::DeleteVkImage`函数，确保底层VkImage的生命周期正确管理，避免GPU发生UAF问题或资源泄漏。

注意：`DeleteVkImage`函数指针接收void*参数，内部调用`VulkanCleanupHelper::UnRef()`减少引用计数。`VulkanCleanupHelper`是引用计数管理类，通过Ref()/UnRef()机制维护VkImage的生命周期。

## 检测示例

### 错误示例

```cpp
// 错误示例1：首次和后续调用都传入vulkanCleanupHelper（引用计数错误）
void CreateSurfaceFromTexture(
    Drawing::GPUContext* gpuContext,
    const Drawing::BackendTexture& backendTexture,
    NativeBufferUtils::VulkanCleanupHelper* vulkanCleanupHelper)
{
    // 首次创建：正确传入vulkanCleanupHelper
    auto surface1 = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, backendTexture.GetTextureInfo(), Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr,
        NativeBufferUtils::DeleteVkImage, vulkanCleanupHelper);
    
    // 后续创建：错误！应该传入vulkanCleanupHelper->Ref()
    auto surface2 = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, backendTexture.GetTextureInfo(), Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr,
        NativeBufferUtils::DeleteVkImage, vulkanCleanupHelper);  // 错误：引用计数管理不当
    
    // 当surface1和surface2都销毁时，引用计数会出错
}

// 错误示例2：未传入VulkanCleanupHelper
bool CreateImageFromTexture(
    Drawing::GPUContext& gpuContext,
    const Drawing::TextureInfo& textureInfo,
    Drawing::VKTextureInfo* vkTextureInfo)
{
    auto image = std::make_shared<Drawing::Image>();
    // 错误：未传入vulkanCleanupHelper管理VkImage生命周期
    bool ret = image->BuildFromTexture(gpuContext, textureInfo,
        Drawing::TextureOrigin::TOP_LEFT, Drawing::BitmapFormat(), nullptr);
    // 缺少生命周期管理，VkImage可能泄漏或提前释放
    
    return ret;
}

// 错误示例3：deleteFunc传入错误函数
void WrongCleanupFunc(void* ptr) {
    delete static_cast<int*>(ptr);  // 错误：不是调用UnRef()
}

std::shared_ptr<Drawing::Image> CreateImageWrong(
    Drawing::GPUContext& gpuContext,
    const Drawing::TextureInfo& textureInfo,
    NativeBufferUtils::VulkanCleanupHelper* vulkanCleanupHelper)
{
    auto image = std::make_shared<Drawing::Image>();
    // 错误：deleteFunc应传入NativeBufferUtils::DeleteVkImage
    bool ret = image->BuildFromTexture(gpuContext, textureInfo,
        Drawing::TextureOrigin::TOP_LEFT, Drawing::BitmapFormat(), nullptr,
        WrongCleanupFunc, vulkanCleanupHelper);  // 错误函数
    
    return image;
}
```

### 正确示例

```cpp
// 正确示例1：正确使用VulkanCleanupHelper引用计数（参考源码RSCanvasDrawingRenderNodeDrawable::CreateGpuSurface）
void CreateGpuSurface(
    const Drawing::ImageInfo& imageInfo,
    const std::shared_ptr<Drawing::GPUContext>& gpuContext,
    bool& newVulkanCleanupHelper)
{
    auto vkTextureInfo = backendTexture_.GetTextureInfo().GetVKTextureInfo();
    if (vkTextureInfo == nullptr || gpuContext == nullptr) {
        return;
    }
    
    // 判断是否需要新建VulkanCleanupHelper
    newVulkanCleanupHelper = vulkanCleanupHelper_ == nullptr;
    if (newVulkanCleanupHelper) {
        // 首次创建VulkanCleanupHelper
        vulkanCleanupHelper_ = new NativeBufferUtils::VulkanCleanupHelper(
            RsVulkanContext::GetSingleton(), vkTextureInfo, pid);
    }
    
    // 正确：首次传入vulkanCleanupHelper_，后续传入vulkanCleanupHelper_->Ref()
    surface_ = Drawing::Surface::MakeFromBackendTexture(
        gpuContext.get(), backendTexture_.GetTextureInfo(),
        Drawing::TextureOrigin::TOP_LEFT, 1, Drawing::COLORTYPE_RGBA_8888,
        imageInfo.GetColorSpace(),
        NativeBufferUtils::DeleteVkImage,
        newVulkanCleanupHelper ? vulkanCleanupHelper_ : vulkanCleanupHelper_->Ref());  // 正确
    
    // 当有多个Surface共享同一VkImage时，引用计数正确增加
}

// 正确示例2：BuildFromTexture正确管理引用计数
bool CreateImageFromTexture(
    Drawing::GPUContext& gpuContext,
    const Drawing::TextureInfo& textureInfo,
    NativeBufferUtils::VulkanCleanupHelper* vulkanCleanupHelper,
    bool isFirstTime)
{
    auto image = std::make_shared<Drawing::Image>();
    Drawing::BitmapFormat bitmapFormat;
    
    // 正确：首次传入vulkanCleanupHelper，后续传入vulkanCleanupHelper->Ref()
    bool ret = image->BuildFromTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        bitmapFormat, nullptr,
        NativeBufferUtils::DeleteVkImage,
        isFirstTime ? vulkanCleanupHelper : vulkanCleanupHelper->Ref());  // 正确
    
    if (!ret) {
        RS_LOGE("BuildFromTexture failed");
        NativeBufferUtils::DeleteVkImage(vulkanCleanupHelper);
        return false;
    }
    return true;
}

// 正确示例3：清理失败时的资源释放
void CleanupOnFailure(
    Drawing::GPUContext& gpuContext,
    NativeBufferUtils::VulkanCleanupHelper* vulkanCleanupHelper)
{
    auto image = std::make_shared<Drawing::Image>();
    bool ret = image->BuildFromTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        bitmapFormat, nullptr,
        NativeBufferUtils::DeleteVkImage,
        vulkanCleanupHelper->Ref());
    
    if (!ret) {
        // 正确：失败时需要手动释放引用计数
        NativeBufferUtils::DeleteVkImage(vulkanCleanupHelper);
        RS_LOGE("BuildFromTexture failed, cleanupHelper released");
    }
}

// 正确示例4：不需要清理时传入nullptr（资源由其他机制管理）
// NOPROTECT: texture资源由NativeBuffer管理，不需要额外清理
std::shared_ptr<Drawing::Surface> CreateSurfaceNoCleanup(
    Drawing::GPUContext* gpuContext,
    const Drawing::TextureInfo& textureInfo)
{
    // 正确：明确不需要清理时，传入nullptr（资源由其他地方管理）
    auto surface = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr, nullptr, nullptr);
    
    return surface;
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: VulkanCleanupHelper引用计数管理不当，首次和后续调用未正确使用Ref()
- **RISK_TYPE**: 引用计数错误
- **RISK_PATH**: 首次传入vulkanCleanupHelper后，后续未传入vulkanCleanupHelper->Ref() → 引用计数不一致 → VkImage生命周期管理失败 → UAF或资源泄漏
- **IMPACT_POINT**: GPU UAF问题、GPU崩溃、渲染异常

## 影响分析（ImpactAnalysis）

- **Trigger**: MakeFromBackendTexture/BuildFromTexture调用时，后续调用未使用vulkanCleanupHelper->Ref()
- **Propagation**: VkImage引用计数错误，资源提前释放或泄漏
- **Consequence**: GPU释放后使用(UAF)、程序崩溃、渲染黑屏、内存泄漏
- **Mitigation**: 首次传入vulkanCleanupHelper，后续传入vulkanCleanupHelper->Ref()，deleteFunc传入NativeBufferUtils::DeleteVkImage

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 正确使用Ref() | 存在 vulkanCleanupHelper->Ref() | 不报 |
| 不需要清理 | deleteFunc和cleanupHelper都为nullptr，且有注释说明 | 不报 |
| deleteFunc正确 | NativeBufferUtils::DeleteVkImage | 不报 |

## 测试用例

### 触发用例（应该报）

```cpp
// 错误：后续调用未使用vulkanCleanupHelper->Ref()
void CreateSurfaceWrong(
    Drawing::GPUContext* gpuContext,
    NativeBufferUtils::VulkanCleanupHelper* vulkanCleanupHelper)
{
    // 首次创建正确
    auto surface1 = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr,
        NativeBufferUtils::DeleteVkImage, vulkanCleanupHelper);
    
    // 后续创建错误：应该传入vulkanCleanupHelper->Ref()
    auto surface2 = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr,
        NativeBufferUtils::DeleteVkImage, vulkanCleanupHelper);  // 应该报
}

// 错误：deleteFunc传入错误函数
auto surface = Drawing::Surface::MakeFromBackendTexture(
    gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
    1, Drawing::COLORTYPE_RGBA_8888, nullptr,
    WrongDeleteFunc, vulkanCleanupHelper);  // 应该报：deleteFunc错误
```

### 安全用例（不应该报）

```cpp
// 正确：后续调用使用vulkanCleanupHelper->Ref()
void CreateSurfaceCorrect(
    Drawing::GPUContext* gpuContext,
    NativeBufferUtils::VulkanCleanupHelper* vulkanCleanupHelper)
{
    // 首次创建
    auto surface1 = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr,
        NativeBufferUtils::DeleteVkImage, vulkanCleanupHelper);
    
    // 后续创建正确：传入vulkanCleanupHelper->Ref()
    auto surface2 = Drawing::Surface::MakeFromBackendTexture(
        gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
        1, Drawing::COLORTYPE_RGBA_8888, nullptr,
        NativeBufferUtils::DeleteVkImage, vulkanCleanupHelper->Ref());  // 不报
}

// 正确：明确不需要清理
// NOPROTECT: texture资源由buffer管理，不需要额外清理
auto surface = Drawing::Surface::MakeFromBackendTexture(
    gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
    1, Drawing::COLORTYPE_RGBA_8888, nullptr, nullptr, nullptr);  // 不报

// 正确：首次创建时使用三元运算符判断
bool newVulkanCleanupHelper = vulkanCleanupHelper_ == nullptr;
auto surface = Drawing::Surface::MakeFromBackendTexture(
    gpuContext, textureInfo, Drawing::TextureOrigin::TOP_LEFT,
    1, Drawing::COLORTYPE_RGBA_8888, nullptr,
    NativeBufferUtils::DeleteVkImage,
    newVulkanCleanupHelper ? vulkanCleanupHelper_ : vulkanCleanupHelper_->Ref());  // 不报
```