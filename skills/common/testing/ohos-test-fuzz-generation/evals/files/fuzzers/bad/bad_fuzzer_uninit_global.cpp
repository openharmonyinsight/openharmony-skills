#include "ipc_class.h"
#include <cstddef>
#include <cstdint>

namespace OHOS {
namespace Display {

DisplayServiceStub *g_stub = nullptr;

void DisplayServiceFuzzTest(const uint8_t *data, size_t size)
{
    if (g_stub == nullptr) {
        g_stub = new DisplayServiceStub();
    }

    MessageParcel msgParcel;
    msgParcel.WriteBuffer(data, size);
    MessageParcel replyParcel;
    MessageOption option;

    uint32_t code = static_cast<uint32_t>(IDisplayService::SET_BRIGHTNESS);
    g_stub->OnRemoteRequest(code, msgParcel, replyParcel, option);
}

} // namespace Display
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Display::DisplayServiceFuzzTest(data, size);
    return 0;
}
