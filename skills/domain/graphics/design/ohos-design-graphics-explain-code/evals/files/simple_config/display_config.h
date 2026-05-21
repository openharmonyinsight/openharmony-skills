#ifndef DISPLAY_CONFIG_H
#define DISPLAY_CONFIG_H

#include <cstdint>
#include <string>
#include <vector>

namespace OHOS::Rosen {

struct DisplayMode {
    uint32_t width;
    uint32_t height;
    uint32_t refreshRate;
    uint32_t id;
};

struct DisplayConfig {
    uint32_t densityDpi;
    float scaleFactor;
    std::string orientation;
    std::vector<DisplayMode> supportedModes;
    uint32_t defaultModeId;
};

DisplayMode GetDefaultDisplayMode(const DisplayConfig& config);
uint32_t CalculateDensityDpi(uint32_t physicalWidthMm, uint32_t widthPx);
float GetScaleFactorForDpi(uint32_t dpi);

} // namespace OHOS::Rosen

#endif