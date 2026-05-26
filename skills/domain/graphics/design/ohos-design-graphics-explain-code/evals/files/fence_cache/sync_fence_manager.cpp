#include "sync_fence_manager.h"
#include <algorithm>

namespace OHOS::Rosen {

SyncFence::~SyncFence() {
    if (fd_ >= 0) {
        close(fd_);
    }
}

int32_t SyncFence::Wait(uint32_t timeoutMs) {
    if (!IsValid()) return -1;
    // platform-specific sync_wait
    return sync_wait(fd_, timeoutMs);
}

SyncFenceManager& SyncFenceManager::Instance() {
    static SyncFenceManager instance;
    return instance;
}

std::shared_ptr<SyncFence> SyncFenceManager::CreateFence(int32_t fd) {
    std::lock_guard<std::mutex> lock(mutex_);
    auto fence = std::make_shared<SyncFence>(fd);
    fenceMap_[fd] = fence;
    totalFenceCount_++;
    return fence;
}

std::shared_ptr<SyncFence> SyncFenceManager::GetFence(int32_t fd) {
    std::lock_guard<std::mutex> lock(mutex_);
    auto it = fenceMap_.find(fd);
    if (it != fenceMap_.end()) {
        return it->second;
    }
    return nullptr;
}

void SyncFenceManager::ReleaseFence(int32_t fd) {
    std::lock_guard<std::mutex> lock(mutex_);
    fenceMap_.erase(fd);
}

void FenceCache::EvictOldest() {
    auto oldest = cache_.begin();
    for (auto it = cache_.begin(); it != cache_.end(); ++it) {
        if (it->second.lastAccess < oldest->second.lastAccess) {
            oldest = it;
        }
    }
    if (oldest != cache_.end()) {
        cache_.erase(oldest);
    }
}

void FenceCache::CleanupExpiredEntries(uint64_t maxAgeMs) {
    std::lock_guard<std::mutex> lock(mutex_);
    auto now = std::chrono::steady_clock::now();
    for (auto it = cache_.begin(); it != cache_.end(); ) {
        auto ageMs = std::chrono::duration_cast<std::chrono::milliseconds>(
            now - it->second.lastAccess).count();
        if (ageMs > maxAgeMs) {
            it = cache_.erase(it);
        } else {
            ++it;
        }
    }
}

std::shared_ptr<SyncFence> RenderFencePool::GetOrCreateFence(const std::string& semaphoreKey) {
    auto existing = cache_.Get(semaphoreKey);
    if (existing && existing->IsValid()) {
        return existing;
    }
    return CreateFenceFromSemaphore(semaphoreKey);
}

std::shared_ptr<SyncFence> RenderFencePool::CreateFenceFromSemaphore(const std::string& key) {
    if (!semaphoreCallback_) {
        return nullptr;
    }
    int32_t fd = semaphoreCallback_(key);
    if (fd < 0) {
        return nullptr;
    }
    auto fence = SyncFenceManager::Instance().CreateFence(fd);
    cache_.Insert(key, fence);
    return fence;
}

void RenderFencePool::RecycleFence(const std::string& key) {
    pendingRecycle_.push_back(key);
}

void RenderFencePool::OnFrameEnd() {
    for (const auto& key : pendingRecycle_) {
        auto fence = cache_.Get(key);
        if (fence) {
            SyncFenceManager::Instance().ReleaseFence(fence->GetFd());
        }
        cache_.Remove(key);
    }
    pendingRecycle_.clear();
    cache_.CleanupExpiredEntries(5000);
}

} // namespace OHOS::Rosen