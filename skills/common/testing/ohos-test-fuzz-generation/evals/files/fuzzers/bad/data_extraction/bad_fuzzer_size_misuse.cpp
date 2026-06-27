#include "simple_class.h"
#include <cstddef>
#include <cstdint>
#include <fuzztest/fuzz_data_provider.h>

namespace OHOS {
namespace Utils {

void ConfigManagerFuzzTest(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    ConfigManager mgr;

    mgr.SetConfig(fdp.ConsumeIntegral<int32_t>(), fdp.ConsumeRandomLengthString(256));

    mgr.UpdateValue(fdp.ConsumeIntegral<int32_t>(), fdp.ConsumeFloatingPoint<float>());

    mgr.ResetSection(fdp.ConsumeIntegral<int32_t>());

    mgr.MergeConfig(fdp.ConsumeRandomLengthString(256), fdp.ConsumeIntegral<int32_t>());

    mgr.QueryValue(fdp.ConsumeIntegral<int32_t>(), fdp.ConsumeIntegral<int32_t>());

    if (size > 0) {
        mgr.SetConfig(size, std::to_string(size));
        mgr.UpdateValue(size, static_cast<float>(size));
    }
}

} // namespace Utils
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Utils::ConfigManagerFuzzTest(data, size);
    return 0;
}
