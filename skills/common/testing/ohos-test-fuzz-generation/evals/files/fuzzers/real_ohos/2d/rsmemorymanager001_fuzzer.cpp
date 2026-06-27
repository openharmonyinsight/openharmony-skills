/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "rsmemorymanager001_fuzzer.h"

#include <fuzzer/FuzzedDataProvider.h>
#include <memory>
#include <set>
#include <string>

#include "memory/rs_memory_manager.h"
#include "image/gpu_context.h"

namespace OHOS {
namespace Rosen {

// Global GPU context, initialized in LLVMFuzzerInitialize, managed by unique_ptr (RAII)
std::unique_ptr<OHOS::Rosen::Drawing::GPUContext> g_gpuContext;

namespace {
const uint8_t DO_RELEASE_UNLOCK_GPU_RES_BY_TAG = 0;
const uint8_t DO_RELEASE_UNLOCK_GPU_RES_BY_PID_SET = 1;
const uint8_t DO_RELEASE_UNLOCK_AND_SAFE_CACHE_GPU_RES = 2;
const uint8_t DO_GET_APP_GPU_MEMORY_IN_MB = 3;
const uint8_t DO_MEMORY_OVER_CHECK = 4;
const uint8_t DO_VMA_DEFRAGMENT = 5;
const uint8_t DO_SET_GPU_CACHE_SUPPRESS_WINDOW_SWITCH = 6;
const uint8_t DO_FLUSH_GPU_MEMORY_IN_WAIT_QUEUE = 7;
const uint8_t DO_SUPPRESS_GPU_CACHE_BELOW_CERTAIN_RATIO = 8;
const uint8_t TARGET_SIZE = 9;
constexpr uint8_t MAX_FUZZ_PID_SET_SIZE = 8;

Drawing::GPUResourceTag CreateFuzzedTag(FuzzedDataProvider& fdp)
{
    pid_t pid = static_cast<pid_t>(fdp.ConsumeIntegral<int32_t>());
    uint32_t tid = fdp.ConsumeIntegral<uint32_t>();
    uint32_t wid = fdp.ConsumeIntegral<uint32_t>();
    uint32_t fid = fdp.ConsumeIntegral<uint32_t>();
    std::string tagName = fdp.ConsumeRandomLengthString(32);
    return Drawing::GPUResourceTag(pid, tid, wid, fid, tagName);
}

OHOS::Rosen::Drawing::GPUContext* GetFuzzedGpuContext(FuzzedDataProvider& fdp)
{
    bool useNull = fdp.ConsumeBool();
    return useNull ? nullptr : g_gpuContext.get();
}

std::set<pid_t> CreateFuzzedPidSet(FuzzedDataProvider& fdp, uint8_t maxCount)
{
    std::set<pid_t> pidSet;
    uint8_t count = fdp.ConsumeIntegralInRange<uint8_t>(0, maxCount);
    for (uint8_t i = 0; i < count; i++) {
        pidSet.insert(static_cast<pid_t>(fdp.ConsumeIntegral<int32_t>()));
    }
    return pidSet;
}

void DoReleaseUnlockGpuResourceByTag(FuzzedDataProvider& fdp)
{
    Drawing::GPUResourceTag tag = CreateFuzzedTag(fdp);
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::ReleaseUnlockGpuResource(gpuContext, tag);
}

void DoReleaseUnlockGpuResourceByPidSet(FuzzedDataProvider& fdp)
{
    std::set<pid_t> exitedPidSet = CreateFuzzedPidSet(fdp, MAX_FUZZ_PID_SET_SIZE);
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::ReleaseUnlockGpuResource(gpuContext, exitedPidSet);
}

void DoReleaseUnlockAndSafeCacheGpuResource(FuzzedDataProvider& fdp)
{
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::ReleaseUnlockAndSafeCacheGpuResource(gpuContext);
}

void DoGetAppGpuMemoryInMB(FuzzedDataProvider& fdp)
{
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::GetAppGpuMemoryInMB(gpuContext);
}

void DoMemoryOverCheck(FuzzedDataProvider& fdp)
{
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::MemoryOverCheck(gpuContext);
}

void DoVmaDefragment(FuzzedDataProvider& fdp)
{
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::VmaDefragment(gpuContext);
}

void DoSetGpuCacheSuppressWindowSwitch(FuzzedDataProvider& fdp)
{
    bool enabled = fdp.ConsumeBool();
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::SetGpuCacheSuppressWindowSwitch(gpuContext, enabled);
}

void DoFlushGpuMemoryInWaitQueue(FuzzedDataProvider& fdp)
{
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    MemoryManager::FlushGpuMemoryInWaitQueue(gpuContext);
}

void DoSuppressGpuCacheBelowCertainRatio(FuzzedDataProvider& fdp)
{
    bool nextFrame = fdp.ConsumeBool();
    OHOS::Rosen::Drawing::GPUContext* gpuContext = GetFuzzedGpuContext(fdp);
    std::function<bool(void)> callback = [nextFrame]() { return nextFrame; };
    MemoryManager::SuppressGpuCacheBelowCertainRatio(gpuContext, callback);
}

} // namespace

} // namespace Rosen
} // namespace OHOS

/* Fuzzer environment initialization */
extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
    OHOS::Rosen::g_gpuContext = std::make_unique<OHOS::Rosen::Drawing::GPUContext>();
    if (!OHOS::Rosen::g_gpuContext) {
        return -1;
    }
    return 0;
}

/* Fuzzer entry point */
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (data == nullptr) {
        return -1;
    }

    FuzzedDataProvider fdp(data, size);

    uint8_t tarPos = fdp.ConsumeIntegral<uint8_t>() % OHOS::Rosen::TARGET_SIZE;
    switch (tarPos) {
        case OHOS::Rosen::DO_RELEASE_UNLOCK_GPU_RES_BY_TAG:
            OHOS::Rosen::DoReleaseUnlockGpuResourceByTag(fdp);
            break;
        case OHOS::Rosen::DO_RELEASE_UNLOCK_GPU_RES_BY_PID_SET:
            OHOS::Rosen::DoReleaseUnlockGpuResourceByPidSet(fdp);
            break;
        case OHOS::Rosen::DO_RELEASE_UNLOCK_AND_SAFE_CACHE_GPU_RES:
            OHOS::Rosen::DoReleaseUnlockAndSafeCacheGpuResource(fdp);
            break;
        case OHOS::Rosen::DO_GET_APP_GPU_MEMORY_IN_MB:
            OHOS::Rosen::DoGetAppGpuMemoryInMB(fdp);
            break;
        case OHOS::Rosen::DO_MEMORY_OVER_CHECK:
            OHOS::Rosen::DoMemoryOverCheck(fdp);
            break;
        case OHOS::Rosen::DO_VMA_DEFRAGMENT:
            OHOS::Rosen::DoVmaDefragment(fdp);
            break;
        case OHOS::Rosen::DO_SET_GPU_CACHE_SUPPRESS_WINDOW_SWITCH:
            OHOS::Rosen::DoSetGpuCacheSuppressWindowSwitch(fdp);
            break;
        case OHOS::Rosen::DO_FLUSH_GPU_MEMORY_IN_WAIT_QUEUE:
            OHOS::Rosen::DoFlushGpuMemoryInWaitQueue(fdp);
            break;
        case OHOS::Rosen::DO_SUPPRESS_GPU_CACHE_BELOW_CERTAIN_RATIO:
            OHOS::Rosen::DoSuppressGpuCacheBelowCertainRatio(fdp);
            break;
        default:
            return -1;
    }
    return 0;
}
