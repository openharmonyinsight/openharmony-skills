/*
 * Copyright (c) 2022 Huawei Device Co., Ltd.
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

#include "nativewindow_fuzzer.h"

#include <fuzzer/FuzzedDataProvider.h>
#include <securec.h>
#include <cstdint>
#include <vector>
#include <string>

#include "ipc_inner_object.h"
#include "ipc_cparcel.h"
#include "surface.h"
#include "surface_buffer.h"
#include "surface_buffer_impl.h"
#include "ibuffer_producer.h"
#include "iconsumer_surface.h"
#include "native_window.h"
#include "native_buffer.h"
#include "native_buffer_inner.h"

namespace OHOS {
namespace {

class FuzzBufferConsumerListener : public IBufferConsumerListener {
public:
    void OnBufferAvailable() override {}
};

constexpr uint32_t MATRIX_SIZE = (1U << 4);
constexpr size_t STR_LEN_MAX = (5U << 1);
constexpr int DEFAULT_FENCE = ((1 << 6) + (1 << 5) + (1 << 2));
constexpr int32_t DEFAULT_WIDTH_HEIGHT = 0x100;
constexpr int FENCE_FD_MAX = 32768;
constexpr int32_t STD_FD_MAX = 2;
constexpr int32_t BUFFER_GEOMETRY_MAX = 10000;

} // namespace

void HandleOpt(OHNativeWindow *nativeWindow, FuzzedDataProvider& fdp)
{
    int code = SET_USAGE;
    uint64_t usage = fdp.ConsumeIntegral<uint64_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, usage);
    code = SET_BUFFER_GEOMETRY;
    int32_t height = fdp.ConsumeIntegralInRange<int32_t>(0, BUFFER_GEOMETRY_MAX);
    int32_t width = fdp.ConsumeIntegralInRange<int32_t>(0, BUFFER_GEOMETRY_MAX);
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, height, width);
    code = SET_FORMAT;
    int32_t format = fdp.ConsumeIntegral<int32_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, format);
    code = SET_STRIDE;
    int32_t stride = fdp.ConsumeIntegral<int32_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, stride);
    code = GET_USAGE;
    uint64_t usageGet = BUFFER_USAGE_CPU_WRITE;
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, &usageGet);
    code = SET_TIMEOUT;
    int32_t timeoutSet = fdp.ConsumeIntegral<int32_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, timeoutSet);
    code = SET_COLOR_GAMUT;
    int32_t colorGamutSet = fdp.ConsumeIntegral<int32_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, colorGamutSet);
    code = SET_TRANSFORM;
    int32_t transform = fdp.ConsumeIntegral<int32_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, transform);
}

void HandleOpt1(OHNativeWindow *nativeWindow, FuzzedDataProvider& fdp)
{
    int code = SET_UI_TIMESTAMP;
    uint64_t uiTimestamp = fdp.ConsumeIntegral<uint64_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, uiTimestamp);
    code = SET_DESIRED_PRESENT_TIMESTAMP;
    int64_t desiredPresentTimestamp = fdp.ConsumeIntegral<int64_t>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, desiredPresentTimestamp);
    code = SET_SOURCE_TYPE;
    OHSurfaceSource typeSet = static_cast<OHSurfaceSource>(fdp.ConsumeIntegral<int32_t>());
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, typeSet);
    code = GET_SOURCE_TYPE;
    OHSurfaceSource typeGet = OHSurfaceSource::OH_SURFACE_SOURCE_DEFAULT;
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, &typeGet);
    code = SET_APP_FRAMEWORK_TYPE;
    std::string frameworkType = fdp.ConsumeRandomLengthString(STR_LEN_MAX);
    const char* frameWorkTypeSet = frameworkType.c_str();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, frameWorkTypeSet);
    code = SET_HDR_WHITE_POINT_BRIGHTNESS;
    float brightness = fdp.ConsumeFloatingPoint<float>();
    OH_NativeWindow_NativeWindowHandleOpt(nativeWindow, code, brightness);
}

void NativeWindowFuzzTest(OHNativeWindow *nativeWindow, OHNativeWindowBuffer *nwBuffer,
    FuzzedDataProvider& fdp)
{
    int fenceFd = fdp.ConsumeIntegralInRange<int>(0, FENCE_FD_MAX);
    if (fenceFd >= 0 && fenceFd <= STD_FD_MAX) {
        fenceFd = DEFAULT_FENCE;
    }

    Region::Rect rect;
    rect.x = fdp.ConsumeIntegral<int32_t>();
    rect.y = fdp.ConsumeIntegral<int32_t>();
    rect.w = fdp.ConsumeIntegral<int32_t>();
    rect.h = fdp.ConsumeIntegral<int32_t>();
    Region region = {.rects = &rect, .rectNumber = 1};
    OHScalingMode scalingMode = static_cast<OHScalingMode>(fdp.ConsumeIntegral<int32_t>());
    OHScalingModeV2 scalingModeV2 = static_cast<OHScalingModeV2>(fdp.ConsumeIntegral<int32_t>());
    NativeWindowRequestBuffer(nativeWindow, &nwBuffer, &fenceFd);
    if (nwBuffer != nullptr) {
        NativeWindowFlushBuffer(nativeWindow, nwBuffer, fenceFd, region);
        NativeWindowCancelBuffer(nativeWindow, nwBuffer);
        GetBufferHandleFromNative(nwBuffer);
    }
    uint32_t sequence = fdp.ConsumeIntegral<uint32_t>();
    NativeWindowSetScalingMode(nativeWindow, sequence, scalingMode);
    NativeWindowSetScalingModeV2(nativeWindow, scalingModeV2);
    OH_NativeBuffer_TransformType transform =
        static_cast<OH_NativeBuffer_TransformType>(fdp.ConsumeIntegral<int32_t>());
    NativeWindowSetTransformHint(nativeWindow, transform);
    NativeWindowGetTransformHint(nativeWindow, &transform);
}

bool DoSomethingInterestingWithMyAPI(FuzzedDataProvider& fdp)
{
    sptr<OHOS::IConsumerSurface> cSurface = IConsumerSurface::Create();
    if (cSurface == nullptr) {
        return false;
    }
    sptr<IBufferConsumerListener> listener = new FuzzBufferConsumerListener();
    cSurface->RegisterConsumerListener(listener);
    sptr<OHOS::IBufferProducer> producer = cSurface->GetProducer();
    if (producer == nullptr) {
        return false;
    }
    sptr<OHOS::Surface> pSurface = Surface::CreateSurfaceAsProducer(producer);
    if (pSurface == nullptr) {
        return false;
    }
    cSurface->SetDefaultWidthAndHeight(DEFAULT_WIDTH_HEIGHT, DEFAULT_WIDTH_HEIGHT);
    OHNativeWindow* nativeWindow = CreateNativeWindowFromSurface(&pSurface);
    if (nativeWindow == nullptr) {
        return false;
    }
    OHNativeWindowBuffer* nwBuffer = nullptr;
    HandleOpt(nativeWindow, fdp);
    HandleOpt1(nativeWindow, fdp);
    NativeWindowFuzzTest(nativeWindow, nwBuffer, fdp);
    NativeWindowDisconnect(nativeWindow);
    DestoryNativeWindow(nativeWindow);
    return true;
}
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (data == nullptr || size == 0) {
        return 0;
    }

    FuzzedDataProvider fdp(data, size);
    OHOS::DoSomethingInterestingWithMyAPI(fdp);
    return 0;
}
