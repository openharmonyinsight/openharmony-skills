#ifndef SYNC_FENCE_MANAGER_H
#define SYNC_FENCE_MANAGER_H

#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>
#include <mutex>
#include <memory>
#include <chrono>

namespace OHOS::Rosen {

class SyncFence {
public:
    SyncFence(int32_t fd) : fd_(fd) {}
    ~SyncFence();

    int32_t GetFd() const { return fd_; }
    bool IsValid() const { return fd_ >= 0; }

    int32_t Wait(uint32_t timeoutMs);

private:
    int32_t fd_;
};

class FenceCache {
public:
    FenceCache(size_t maxSize) : maxSize_(maxSize) {}

    void Insert(const std::string& key, std::shared_ptr<SyncFence> fence) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (cache_.size() >= maxSize_) {
            EvictOldest();
        }
        cache_[key] = {fence, std::chrono::steady_clock::now()};
    }

    std::shared_ptr<SyncFence> Get(const std::string& key) {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = cache_.find(key);
        if (it != cache_.end()) {
            it->second.lastAccess = std::chrono::steady_clock::now();
            return it->second.fence;
        }
        return nullptr;
    }

    void Remove(const std::string& key) {
        std::lock_guard<std::mutex> lock(mutex_);
        cache_.erase(key);
    }

    void CleanupExpiredEntries(uint64_t maxAgeMs);

    size_t Size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return cache_.size();
    }

private:
    void EvictOldest();

    struct CacheEntry {
        std::shared_ptr<SyncFence> fence;
        std::chrono::steady_clock::time_point lastAccess;
    };

    size_t maxSize_;
    std::unordered_map<std::string, CacheEntry> cache_;
    std::mutex mutex_;
};

class SyncFenceManager {
public:
    static SyncFenceManager& Instance();

    std::shared_ptr<SyncFence> CreateFence(int32_t fd);
    std::shared_ptr<SyncFence> GetFence(int32_t fd);

    void ReleaseFence(int32_t fd);

    uint32_t GetTotalFenceCount() const { return totalFenceCount_; }

private:
    SyncFenceManager() = default;
    std::unordered_map<int32_t, std::shared_ptr<SyncFence>> fenceMap_;
    std::mutex mutex_;
    std::atomic<uint32_t> totalFenceCount_{0};
};

class RenderFencePool {
public:
    RenderFencePool(size_t poolSize) : poolSize_(poolSize), cache_(poolSize) {}

    std::shared_ptr<SyncFence> GetOrCreateFence(const std::string& semaphoreKey);

    void RecycleFence(const std::string& key);

    void OnFrameEnd();

    void SetSemaphoreCallback(std::function<int32_t(const std::string&)> cb) {
        semaphoreCallback_ = cb;
    }

    size_t GetActiveFenceCount() const {
        return cache_.Size();
    }

private:
    std::shared_ptr<SyncFence> CreateFenceFromSemaphore(const std::string& key);

    size_t poolSize_;
    FenceCache cache_;
    std::function<int32_t(const std::string&)> semaphoreCallback_;
    std::vector<std::string> pendingRecycle_;
};

} // namespace OHOS::Rosen

#endif // SYNC_FENCE_MANAGER_H