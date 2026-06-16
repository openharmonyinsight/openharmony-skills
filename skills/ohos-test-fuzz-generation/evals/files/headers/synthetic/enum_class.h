#ifndef ENUM_CLASS_H
#define ENUM_CLASS_H

#include <cstdint>
#include <string>

namespace OHOS {
namespace Graphic {

enum GraphicTransformType : uint8_t {
    GRAPHIC_TRANSFORM_NONE = 0,
    GRAPHIC_TRANSFORM_ROTATE_90 = 1,
    GRAPHIC_TRANSFORM_ROTATE_180 = 2,
    GRAPHIC_TRANSFORM_ROTATE_270 = 3,
    GRAPHIC_TRANSFORM_FLIP_H = 4,
    GRAPHIC_TRANSFORM_FLIP_V = 5,
};

enum BufferQueueUsage : uint8_t {
    BUFFER_QUEUE_USAGE_PRODUCTION = 0,
    BUFFER_QUEUE_USAGE_CONSUMPTION = 1,
    BUFFER_QUEUE_USAGE_CPU_READ = 2,
    BUFFER_QUEUE_USAGE_CPU_WRITE = 3,
};

enum ColorSpace : uint8_t {
    COLOR_SPACE_UNKNOWN = 0,
    COLOR_SPACE_SRGB = 1,
    COLOR_SPACE_DISPLAY_P3 = 2,
    COLOR_SPACE_ADOBE_RGB = 3,
};

enum CompositionType : uint8_t {
    COMPOSITION_DEVICE = 0,
    COMPOSITION_CLIENT = 1,
    COMPOSITION_CURSOR = 2,
    COMPOSITION_VIDEO = 3,
};

class GraphicComposer {
public:
    GraphicComposer() = default;
    ~GraphicComposer() = default;

    int32_t SetTransform(GraphicTransformType transform);
    int32_t SetBufferQueueUsage(BufferQueueUsage usage);
    int32_t SetColorSpace(ColorSpace colorSpace);
    int32_t SetCompositionType(CompositionType type);
    int32_t SetLayerAlpha(uint32_t layerId, float alpha);
    int32_t SetLayerZOrder(uint32_t layerId, int32_t zOrder);
    int32_t SetLayerVisible(uint32_t layerId, bool visible);
    int32_t SetLayerSize(uint32_t layerId, int32_t width, int32_t height);
    int32_t SetLayerCrop(uint32_t layerId, int32_t left, int32_t top, int32_t right, int32_t bottom);
    int32_t SetLayerBuffer(uint32_t layerId, int32_t bufferHandle, BufferQueueUsage usage);
};

} // namespace Graphic
} // namespace OHOS

#endif // ENUM_CLASS_H
