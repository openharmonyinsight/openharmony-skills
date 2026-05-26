#include "display_config.h"
#include <cmath>
#include <algorithm>

namespace OHOS::Rosen {

DisplayMode GetDefaultDisplayMode(const DisplayConfig& config) {
    for (const auto& mode : config.supportedModes) {
        if (mode.id == config.defaultModeId) {
            return mode;
        }
    }
    return config.supportedModes.empty() ? DisplayMode{} : config.supportedModes[0];
}

uint32_t CalculateDensityDpi(uint32_t physicalWidthMm, uint32_t widthPx) {
    if (physicalWidthMm == 0) return 160;
    float physicalWidthInch = static_cast<float>(physicalWidthMm) / 25.4f;
    return static_cast<uint32_t>(std::round(static_cast<float>(widthPx) / physicalWidthInch));
}

float GetScaleFactorForDpi(uint32_t dpi) {
    if (dpi <= 120) return 0.75f;
    if (dpi <= 160) return 1.0f;
    if (dpi <= 240) return 1.5f;
    if (dpi <= 320) return 2.0f;
    if (dpi <= 480) return 3.0f;
    if (dpi <= 640) return 4.0f;
    return 4.0f;
}

} // namespace OHOS::Rosen