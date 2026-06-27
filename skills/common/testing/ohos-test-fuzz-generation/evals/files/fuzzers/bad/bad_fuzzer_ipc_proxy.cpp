#include "ipc_class.h"
#include <cstddef>
#include <cstdint>
#include <fuzztest/fuzz_data_provider.h>

namespace OHOS {
namespace Display {

void DisplayServiceProxyFuzzTest(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);

    sptr<IRemoteObject> remoteObj = nullptr;
    DisplayServiceProxy proxy(remoteObj);

    int32_t brightness = fdp.ConsumeIntegral<int32_t>();
    proxy.SetBrightness(brightness);

    int32_t status = fdp.ConsumeIntegral<int32_t>();
    proxy.SetPowerStatus(status);

    sptr<IRemoteObject> callbackObj = nullptr;
    proxy.RegisterCallback(callbackObj);
}

} // namespace Display
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Display::DisplayServiceProxyFuzzTest(data, size);
    return 0;
}
