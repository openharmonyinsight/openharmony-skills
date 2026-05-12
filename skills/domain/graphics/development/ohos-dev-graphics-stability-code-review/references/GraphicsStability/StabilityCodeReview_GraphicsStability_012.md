---
rule_id: "StabilityCodeReview_GraphicsStability_012"
name: "SyncFence智能指针缓存管理"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# SyncFence智能指针缓存管理

## 问题描述

使用GetFenceFdFromSemaphore、vkGetSemaphoreFdKHR等接口从vulkan信号量中导出的fd由智能指针sptr<SyncFence>接管生命周期后,需检验该智能指针是否被存于缓存中,若存在缓存逻辑,需确保缓存的释放逻辑完整且正确、释放时机合理,避免缓存遗漏清理导致内存泄漏与fd泄漏。

## 检测示例

### 错误示例

```cpp
// 错误示例1:缓存智能指针但未清理
class FenceCache {
private:
    std::map<uint64_t, sptr<SyncFence>> fenceCache_;
    
public:
    void AddFence(uint64_t id, VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) {
            return;
        }
        
        sptr<SyncFence> fence = new SyncFence(fd);
        // 错误:加入缓存但从未清理
        fenceCache_[id] = fence;
    }
    
    // 错误:析构时未清理缓存
    ~FenceCache() {}
};

// 错误示例2:缓存清理逻辑不完整
class SyncFenceManager {
private:
    std::unordered_map<int, sptr<SyncFence>> fenceMap_;
    
public:
    void CacheFence(int key, VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) {
            return;
        }
        
        sptr<SyncFence> fence = new SyncFence(fd);
        fenceMap_[key] = fence;
    }
    
    void RemoveFence(int key)
    {
        auto it = fenceMap_.find(key);
        if (it != fenceMap_.end()) {
            // 错误:只erase未检查是否需要手动释放
            fenceMap_.erase(it);
        }
    }
    
    // 错误:析构时未检查缓存是否为空
};

// 错误示例3:缓存释放时机不合理
class RenderFencePool {
private:
    std::vector<sptr<SyncFence>> fencePool_;
    
public:
    void RecycleFence(VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) {
            return;
        }
        
        sptr<SyncFence> fence = new SyncFence(fd);
        // 错误:缓存一直增长,无清理机制
        fencePool_.push_back(fence);
    }
    
    // 错误:缺少定期清理或限制缓存的机制
};
```

### 正确示例

```cpp
// 正确示例1:完整的缓存清理逻辑
class FenceCache {
private:
    std::map<uint64_t, sptr<SyncFence>> fenceCache_;
    
public:
    void AddFence(uint64_t id, VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) {
            return;
        }
        
        sptr<SyncFence> fence = new SyncFence(fd);
        fenceCache_[id] = fence;
        
        // 正确:检查缓存大小并清理旧条目
        if (fenceCache_.size() > MAX_CACHE_SIZE) {
            auto oldest = fenceCache_.begin();
            fenceCache_.erase(oldest);
        }
    }
    
    void RemoveFence(uint64_t id)
    {
        auto it = fenceCache_.find(id);
        if (it != fenceCache_.end()) {
            // 正确:sptr引用计数自动管理,erase即可
            fenceCache_.erase(it);
        }
    }
    
    void ClearCache()
    {
        // 正确:提供清理接口
        fenceCache_.clear();
    }
    
    ~FenceCache()
    {
        // 正确:析构时清理缓存
        ClearCache();
    }
};

// 正确示例2:带引用计数和过期检查的缓存管理
class SyncFenceManager {
private:
    std::unordered_map<int, std::pair<sptr<SyncFence>, int64_t>> fenceMap_;
    
public:
    void CacheFence(int key, VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) {
            return;
        }
        
        sptr<SyncFence> fence = new SyncFence(fd);
        int64_t timestamp = GetCurrentTime();
        
        // 正确:清理过期条目
        CleanupExpiredEntries();
        
        fenceMap_[key] = {fence, timestamp};
    }
    
    void RemoveFence(int key)
    {
        // 正确:erase会自动减少引用计数
        fenceMap_.erase(key);
    }
    
    void CleanupExpiredEntries()
    {
        int64_t now = GetCurrentTime();
        for (auto it = fenceMap_.begin(); it != fenceMap_.end(); ) {
            if (now - it->second.second > CACHE_TIMEOUT) {
                it = fenceMap_.erase(it);
            } else {
                ++it;
            }
        }
    }
};

// 正确示例3:限制缓存大小并提供清理机制
class RenderFencePool {
private:
    std::deque<sptr<SyncFence>> fencePool_;
    static const size_t MAX_POOL_SIZE = 100;
    
public:
    void RecycleFence(VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) {
            return;
        }
        
        sptr<SyncFence> fence = new SyncFence(fd);
        
        // 正确:限制缓存大小
        if (fencePool_.size() >= MAX_POOL_SIZE) {
            fencePool_.pop_front();  // 移除最旧的
        }
        
        fencePool_.push_back(fence);
    }
    
    void ClearPool()
    {
        fencePool_.clear();
    }
    
    size_t GetPoolSize() const
    {
        return fencePool_.size();
    }
};
```

## 检测范围

检查以下API/函数/模式:

- `GetFenceFdFromSemaphore()`后创建`sptr<SyncFence>`并存入缓存
- 将`SyncFence`智能指针存入`std::map`、`std::unordered_map`、`std::vector`等容器
- 缓存`SyncFence`对象的管理类、管理器

## 检测要点

1. 识别将SyncFence智能指针存入缓存的代码
2. 检查缓存是否有清理机制(erase/clear/remove等)
3. 检查缓存清理逻辑是否完整,所有退出路径是否都清理
4. 检查缓存大小是否有限制,避免无限增长
5. 检查析构函数是否清理缓存

## 风险流分析(RiskFlow)

- **RISK_SOURCE**: SyncFence智能指针存入缓存但未正确管理
- **RISK_TYPE**: 内存泄漏、文件描述符泄漏
- **RISK_PATH**: fd导出 → SyncFence管理 → 存入缓存 → 未清理 → 内存和fd泄漏
- **IMPACT_POINT**: 系统资源耗尽,程序性能下降或崩溃

## 影响分析(ImpactAnalysis)

- **Trigger**: 将SyncFence智能指针存入缓存容器
- **Propagation**: 缓存未清理或清理逻辑不完整,条目持续累积
- **Consequence**: 内存泄漏、fd泄漏累积,系统资源耗尽
- **Mitigation**: 确保缓存有完整的清理逻辑、大小限制、过期机制

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 临时缓存立即清理 | 缓存后立即erase/clear | 不报 |
| 有定期清理机制 | 定时器或定期调用clear | 不报 |
| 缓存大小有限制 | 检查size并删除旧条目 | 不报 |
| 缓存生命周期短暂 | 局部缓存在作用域结束时销毁 | 不报 |

## 测试用例

### 触发用例(应该报)

```cpp
// test_StabilityCodeReview_GraphicsStability_012_trigger.cpp
class BadFenceCache {
private:
    std::map<int, sptr<SyncFence>> cache_;
    
public:
    void Add(int key, VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) return;
        
        sptr<SyncFence> fence = new SyncFence(fd);
        cache_[key] = fence;
        // 应该报:缓存未清理
    }
    
    // 应该报:析构函数未清理缓存
};
```

### 安全用例(不应该报)

```cpp
// test_StabilityCodeReview_GraphicsStability_012_safe.cpp
class GoodFenceCache {
private:
    std::map<int, sptr<SyncFence>> cache_;
    static const size_t MAX_SIZE = 100;
    
public:
    void Add(int key, VkSemaphore sem)
    {
        int fd = GetFenceFdFromSemaphore(sem);
        if (fd < 0) return;
        
        sptr<SyncFence> fence = new SyncFence(fd);
        
        // 不报:有大小限制和清理机制
        if (cache_.size() >= MAX_SIZE) {
            cache_.erase(cache_.begin());
        }
        
        cache_[key] = fence;
    }
    
    void Remove(int key)
    {
        cache_.erase(key);  // 不报:有清理接口
    }
    
    ~GoodFenceCache()
    {
        cache_.clear();  // 不报:析构时清理
    }
};
```