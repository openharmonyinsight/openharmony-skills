---
rule_id: "StabilityCodeReview_GraphicsStability_006"
name: "Surface/Image跨线程跨Context操作风险"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Surface/Image跨线程跨Context操作风险

## 问题描述

Surface/Image应尽量避免跨线程/跨Context操作，如果必须多线程访问，应首先考虑使用BackendTexture创建新的Surface/Image，否则必须要保证Surface/Image在同一把锁的保护范围内。跨线程/跨Context操作GPU资源会导致状态不一致，引发GPU崩溃。

## 检测示例

### 错误示例

```cpp
// 错误示例1：跨线程访问Surface无锁保护
class SharedSurfaceManager {
public:
    sk_sp<Surface> surface_;
    
    void ThreadA_Draw() {
        // 错误：线程A直接访问共享Surface
        auto canvas = surface_->getCanvas();  // 错误：无锁保护
        canvas->drawRect(rect, paint);
    }
    
    void ThreadB_Draw() {
        // 错误：线程B直接访问同一Surface
        auto canvas = surface_->getCanvas();  // 错误：无锁保护
        canvas->drawCircle(center, radius, paint);
    }
};

// 错误示例2：跨Context使用Image
void CrossContextUsage()
{
    auto image = CreateImageOnContext1();  // 在Context1创建
    
    // 错误：在Context2使用
    auto canvas2 = context2_surface->getCanvas();
    canvas2->drawImage(image);  // 错误：跨Context使用
}

// 错误示例3：多线程共享Image无保护
std::shared_ptr<Image> g_sharedImage;

void Thread1() {
    g_sharedImage->readPixels(info, pixels);  // 错误：无保护
}

void Thread2() {
    g_sharedImage->makeSubset(region);  // 错误：无保护
}
```

### 正确示例

```cpp
// 正确示例1：使用BackendTexture创建新Surface
void SafeCrossThreadAccess()
{
    BackendTexture backendTexture = surface1->getBackendTexture();
    
    // 正确：线程B使用BackendTexture创建新的Surface
    auto surface2 = Surface::MakeFromBackendTexture(
        context2, backendTexture, origin, 1, colorType, nullptr, nullptr);  // 正确
    
    auto canvas2 = surface2->getCanvas();  // 正确：独立Surface
}

// 正确示例2：使用锁保护Surface访问
class LockedSurfaceManager {
public:
    sk_sp<Surface> surface_;
    std::mutex mutex_;
    
    void ThreadA_Draw() {
        std::lock_guard<std::mutex> lock(mutex_);
        auto canvas = surface_->getCanvas();  // 正确：有锁保护
        canvas->drawRect(rect, paint);
    }
    
    void ThreadB_Draw() {
        std::lock_guard<std::mutex> lock(mutex_);
        auto canvas = surface_->getCanvas();  // 正确：有锁保护
        canvas->drawCircle(center, radius, paint);
    }
};

// 正确示例3：每个线程独立创建Image
void ThreadSafeImageUsage()
{
    // 正确：每个线程创建独立Image
    BackendTexture texture = GetSharedBackendTexture();
    
    // 线程A
    auto imageA = Image::MakeFromBackendTexture(contextA, texture, origin, colorType, nullptr, nullptr);  // 正确
    
    // 线程B
    auto imageB = Image::MakeFromBackendTexture(contextB, texture, origin, colorType, nullptr, nullptr);  // 正确
}
```

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: Surface/Image跨线程/跨Context操作
- **RISK_TYPE**: 线程安全风险
- **RISK_PATH**: 跨线程访问Surface/Image -> 数据竞争 -> GPU资源状态不一致
- **IMPACT_POINT**: GPU崩溃、渲染异常

## 影响分析（ImpactAnalysis）

- **Trigger**: 多线程同时访问同一Surface/Image
- **Propagation**: GPU资源状态不一致
- **Consequence**: 渲染异常、GPU崩溃、黑屏
- **Mitigation**: 使用BackendTexture创建新Surface/Image，或用锁保护访问

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 使用BackendTexture | MakeFromBackendTexture | 不报 |
| 有锁保护 | lock_guard、unique_lock | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// 跨线程访问Surface无锁保护
std::thread t1([&]() {
    surface->getCanvas()->drawRect(rect, paint);  // 应该报：无保护
});
std::thread t2([&]() {
    surface->getCanvas()->drawCircle(c, r, paint);  // 应该报
});
```

### 安全用例（不应该报）

```cpp
// 使用锁保护
std::lock_guard<std::mutex> lock(mutex);
surface->getCanvas()->drawRect(rect, paint);  // 不报：有锁

// 使用BackendTexture创建新Surface
auto surface2 = Surface::MakeFromBackendTexture(...);  // 不报
```