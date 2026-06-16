#include "ipc_class.h"
#include <cstddef>
#include <cstdint>
#include <fuzztest/fuzz_data_provider.h>
#include "message_parcel.h"
#include "message_option.h"

namespace OHOS {
namespace Display {

static DisplayServiceStub *g_displayStub = nullptr;

void DisplayServiceStubFuzzTest(const uint8_t *data, size_t size)
{
    if (g_displayStub == nullptr) {
        return;
    }

    FuzzedDataProvider fdp(data, size);
    uint32_t code = fdp.ConsumeIntegral<uint32_t>();

    MessageParcel dataParcel;
    MessageParcel replyParcel;
    MessageOption option;

    std::string payload = fdp.ConsumeRemainingAsString<uint8_t>();
    dataParcel.WriteBuffer(payload.data(), payload.size());

    g_displayStub->OnRemoteRequest(code, dataParcel, replyParcel, option);
}

} // namespace Display
} // namespace OHOS

extern "C" int LLVMFuzzerInitialize(int *argc, char ***argv)
{
    OHOS::Display::g_displayStub = new OHOS::Display::DisplayServiceStub();
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Display::DisplayServiceStubFuzzTest(data, size);
    return 0;
}
