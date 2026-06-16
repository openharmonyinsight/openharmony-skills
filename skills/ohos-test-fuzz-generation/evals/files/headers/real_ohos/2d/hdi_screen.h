#ifndef REAL_OHOS_HDI_SCREEN_H
#define REAL_OHOS_HDI_SCREEN_H

#include <cstdint>
#include <vector>
#include <string>
#include <mutex>

namespace OHOS {
namespace Rosen {

enum GraphicDispPowerStatus : uint32_t {
    GRAPHIC_DISP_POWER_STATUS_OFF = 0,
    GRAPHIC_DISP_POWER_STATUS_ON = 1,
    GRAPHIC_DISP_POWER_STATUS_STANDBY = 2,
    GRAPHIC_DISP_POWER_STATUS_SUSPEND = 3,
    GRAPHIC_DISP_POWER_STATUS_ON_EXPEND = 4,
    GRAPHIC_DISP_POWER_STATUS_ON_FAKE = 5,
};

enum GraphicColorGamut : uint32_t {
    COLOR_GAMUT_INVALID = 0,
    COLOR_GAMUT_SRGB = 1,
    COLOR_GAMUT_DISPLAY_P3 = 2,
    COLOR_GAMUT_ADOBE_RGB = 3,
    COLOR_GAMUT_DCI_P3 = 4,
    COLOR_GAMUT_BT2020 = 5,
    COLOR_GAMUT_BT2100_PQ = 6,
    COLOR_GAMUT_BT2100_HLG = 7,
};

enum GraphicGamutMap : uint32_t {
    GAMUT_MAP_CONSTANT = 0,
    GAMUT_MAP_EXPANSION = 1,
    GAMUT_MAP_HDR_EXTENSION = 2,
    GAMUT_MAP_RELATIVE = 3,
};

typedef uint64_t ScreenId;

class HdiScreen {
public:
    HdiScreen(uint32_t screenId);
    virtual ~HdiScreen();

    static std::unique_ptr<HdiScreen> CreateHdiScreen(uint32_t screenId);
    bool Init();

    int32_t SetScreenPowerStatus(GraphicDispPowerStatus status) const;
    int32_t SetScreenColorGamut(GraphicColorGamut gamut) const;
    int32_t SetScreenGamutMap(GraphicGamutMap gamutMap) const;
    int32_t SetScreenVsyncEnabled(bool enabled) const;
    int32_t SetScreenMode(uint32_t modeId);
    int32_t SetScreenColorTransform(const std::vector<float>& matrix) const;

    bool SetHdiDevice(HdiDevice* device);

private:
    uint32_t screenId_;
    HdiDevice *device_ = nullptr;
    std::mutex mutex_;
};

} // namespace Rosen
} // namespace OHOS

#endif // REAL_OHOS_HDI_SCREEN_H
