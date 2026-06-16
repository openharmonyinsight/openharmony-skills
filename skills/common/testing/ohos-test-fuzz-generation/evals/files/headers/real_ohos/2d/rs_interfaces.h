#ifndef REAL_OHOS_RS_INTERFACES_H
#define REAL_OHOS_RS_INTERFACES_H

#include <cstdint>
#include <string>
#include <vector>

namespace OHOS {
namespace Rosen {

typedef uint64_t ScreenId;
typedef uint64_t NodeId;

enum ScreenPowerStatus : uint32_t {
    POWER_STATUS_OFF = 0,
    POWER_STATUS_ON = 1,
    POWER_STATUS_ON_STANDBY = 2,
    POWER_STATUS_ON_SUSPEND = 3,
    POWER_STATUS_OFF_FAKE = 4,
    POWER_STATUS_ON_FAKE = 5,
    POWER_STATUS_ON_EXPEND = 6,
    POWER_STATUS_ON_VIRTUAL = 7,
    POWER_STATUS_ON_ADVANCED = 8,
    POWER_STATUS_ON_INTERNAL = 9,
    POWER_STATUS_ON_EXTERNAL = 10,
    INVALID_POWER_STATUS = 11,
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
    COLOR_GAMUT_DISPLAY_BT2020 = 8,
};

enum ScreenRotation : uint32_t {
    ROTATION_0 = 0,
    ROTATION_90 = 1,
    ROTATION_180 = 2,
    ROTATION_270 = 3,
    INVALID_SCREEN_ROTATION = 4,
};

struct GraphicDisplayModeInfo {
    int32_t width;
    int32_t height;
    int32_t refreshRate;
    int32_t id;
};

struct GraphicDisplayCapability {
    int32_t width;
    int32_t height;
};

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

#endif // REAL_OHOS_RS_INTERFACES_H
