#ifndef COMPLEX_PARAM_CLASS_H
#define COMPLEX_PARAM_CLASS_H

#include <vector>
#include <functional>
#include <cstdint>
#include "sptr.h"
#include "surface.h"

namespace OHOS {
namespace Rosen {

struct RSScreenModeInfo {
    int32_t width;
    int32_t height;
    int32_t refreshRate;
    int32_t id;
};

enum ScreenPowerStatus : uint8_t {
    POWER_STATUS_OFF = 0,
    POWER_STATUS_ON = 1,
    POWER_STATUS_STANDBY = 2,
    POWER_STATUS_SUSPEND = 3,
};

enum GraphicPixelFormat : uint8_t {
    PIXEL_FMT_RGB_565 = 0,
    PIXEL_FMT_RGBA_8888 = 1,
    PIXEL_FMT_BGRA_8888 = 2,
    PIXEL_FMT_YCBCR_422_SP = 3,
};

typedef uint64_t NodeId;

class ScreenManager {
public:
    ScreenManager() = default;
    ~ScreenManager() = default;

    int32_t SetScreenMode(uint32_t screenId, const RSScreenModeInfo &modeInfo);
    int32_t SetScreenPowerStatus(uint32_t screenId, ScreenPowerStatus status);
    int32_t SetScreenPixelFormat(uint32_t screenId, GraphicPixelFormat format);
    int32_t RegisterVirtualScreen(const std::string &name, uint32_t width, uint32_t height,
                                  const sptr<Surface> &surface, int32_t flags);
    int32_t SetScreenActiveMode(uint32_t screenId, uint32_t modeId);
    int32_t RemoveVirtualScreen(NodeId nodeId);
    int32_t SetScreenBacklight(uint32_t screenId, uint32_t level);
    int32_t GetScreenSupportedModes(uint32_t screenId, std::vector<RSScreenModeInfo> &modes);
    void SetRenderCallback(std::function<void(NodeId, uint64_t)> callback);
};

} // namespace Rosen
} // namespace OHOS

#endif // COMPLEX_PARAM_CLASS_H
