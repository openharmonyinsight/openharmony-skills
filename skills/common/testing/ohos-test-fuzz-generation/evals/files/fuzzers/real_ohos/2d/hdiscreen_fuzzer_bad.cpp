#include <securec.h>
#include "hdi_screen.h"
#include <cstdint>
#include <string>

using namespace OHOS::Rosen;

namespace OHOS {
namespace {
    constexpr size_t STR_LEN = 10;
    const uint8_t* data_ = nullptr;
    size_t size_ = 0;
    size_t pos;
    std::unique_ptr<HdiScreen> g_hdiScreen = nullptr;

    template<class T>
    T GetData()
    {
        T object {};
        size_t objectSize = sizeof(object);
        if (data_ == nullptr || objectSize > size_ - pos) {
            return object;
        }
        errno_t ret = memcpy_s(&object, objectSize, data_ + pos, objectSize);
        if (ret != EOK) {
            return {};
        }
        pos += objectSize;
        return object;
    }

    GraphicGamutMap gamutMap = GetData<GraphicGamutMap>();
    GraphicColorGamut gamut = GetData<GraphicColorGamut>();
    GraphicDispPowerStatus status = GetData<GraphicDispPowerStatus>();
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    if (data == nullptr) {
        return 0;
    }
    data_ = data;
    size_ = size;
    pos = 0;

    if (g_hdiScreen == nullptr) {
        uint32_t screenId = GetData<uint32_t>();
        g_hdiScreen = HdiScreen::CreateHdiScreen(screenId);
    }
    if (g_hdiScreen == nullptr) {
        return 0;
    }

    g_hdiScreen->SetScreenPowerStatus(status);
    g_hdiScreen->SetScreenColorGamut(gamut);
    g_hdiScreen->SetScreenGamutMap(gamutMap);
    return 0;
}
