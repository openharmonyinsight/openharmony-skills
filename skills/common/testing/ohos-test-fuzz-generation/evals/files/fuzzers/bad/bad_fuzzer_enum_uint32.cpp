#include "enum_class.h"
#include <cstddef>
#include <cstdint>
#include <fuzztest/fuzz_data_provider.h>

namespace OHOS {
namespace Graphic {

void GraphicComposerFuzzTest(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    GraphicComposer composer;

    uint32_t transformRaw = fdp.ConsumeIntegral<uint32_t>();
    GraphicTransformType transform = static_cast<GraphicTransformType>(transformRaw);
    composer.SetTransform(transform);

    uint32_t usageRaw = fdp.ConsumeIntegral<uint32_t>();
    BufferQueueUsage usage = static_cast<BufferQueueUsage>(usageRaw);
    composer.SetBufferQueueUsage(usage);

    uint32_t colorSpaceRaw = fdp.ConsumeIntegral<uint32_t>();
    ColorSpace colorSpace = static_cast<ColorSpace>(colorSpaceRaw);
    composer.SetColorSpace(colorSpace);

    uint32_t typeRaw = fdp.ConsumeIntegral<uint32_t>();
    CompositionType compType = static_cast<CompositionType>(typeRaw);
    composer.SetCompositionType(compType);

    uint32_t layerId = fdp.ConsumeIntegral<uint32_t>();
    float alpha = fdp.ConsumeFloatingPoint<float>();
    composer.SetLayerAlpha(layerId, alpha);
}

} // namespace Graphic
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Graphic::GraphicComposerFuzzTest(data, size);
    return 0;
}
