#ifndef MANY_METHODS_CLASS_H
#define MANY_METHODS_CLASS_H

#include <cstdint>
#include <string>
#include "screen_types.h"

namespace OHOS {
namespace Rosen {

class RSInterfaces : public IRemoteBroker {
public:
    DECLARE_INTERFACE_DESCRIPTOR(u"OHOS.Rosen.RSInterfaces");

    enum Code : uint32_t {
        SET_SCREEN_POWER_STATUS = 0,
        GET_SCREEN_POWER_STATUS = 1,
        SET_SCREEN_BACKLIGHT = 2,
        GET_SCREEN_BACKLIGHT = 3,
        SET_SCREEN_COLOR_GAMUT = 4,
        REGISTER_CALLBACK = 5,
        GET_SCREEN_SUPPORTED_COLOR_GAMUTS = 6,
        GET_SCREEN_SUPPORTED_MODES = 7,
        GET_SCREEN_CAPABILITY = 8,
        SET_SCREEN_VCP_FEATURE = 9,
        SET_SCREEN_VSYNC_ENABLED = 10,
        SET_SCREEN_COLOR_TRANSFORM = 11,
        SET_SCREEN_GAME_MODE = 12,
        GET_SCREEN_GAME_MODE = 13,
    };

    virtual int32_t SetScreenPowerStatus(ScreenId screenId, ScreenPowerStatus status) = 0;
    virtual int32_t GetScreenPowerStatus(ScreenId screenId, ScreenPowerStatus& status) = 0;
    virtual int32_t SetScreenBacklight(ScreenId screenId, uint32_t level) = 0;
    virtual int32_t GetScreenBacklight(ScreenId screenId, uint32_t& level) = 0;
    virtual int32_t SetScreenColorGamut(ScreenId screenId, GraphicColorGamut gamut) = 0;
    virtual int32_t RegisterCallback(sptr<IDisplayCallback> callback) = 0;
    virtual int32_t GetScreenSupportedColorGamuts(ScreenId screenId, std::vector<GraphicColorGamut>& gamuts) = 0;
    virtual int32_t GetScreenSupportedModes(ScreenId screenId, std::vector<GraphicDisplayModeInfo>& modes) = 0;
    virtual int32_t GetScreenCapability(ScreenId screenId, GraphicDisplayCapability& capability) = 0;
    virtual int32_t SetScreenVCPFeature(uint8_t vcpCode, uint16_t currentValue, uint16_t maximumValue, int32_t& errorCode) = 0;
    virtual int32_t SetScreenVsyncEnabled(bool enabled) = 0;
    virtual int32_t SetScreenColorTransform(const std::vector<float>& matrix) = 0;
    virtual int32_t SetScreenGameMode(bool isEnabled) = 0;
    virtual int32_t GetScreenGameMode(bool& isEnabled) = 0;
};

} // namespace Rosen
} // namespace OHOS

#endif // MANY_METHODS_CLASS_H
