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

    auto sectionId = fdp.ConsumeIntegral<int32_t>();
    auto configKey = fdp.ConsumeRandomLengthString(256);
    mgr.SetConfig(sectionId, configKey);

    auto key = fdp.ConsumeIntegral<int32_t>();
    auto weight = fdp.ConsumeFloatingPoint<float>();
    mgr.UpdateValue(key, weight);

    auto resetId = fdp.ConsumeIntegral<int32_t>();
    mgr.ResetSection(resetId);

    auto sourcePath = fdp.ConsumeRandomLengthString(256);
    auto priority = fdp.ConsumeIntegralInRange<int32_t>(0, 100);
    mgr.MergeConfig(sourcePath, priority);

    auto queryKey = fdp.ConsumeIntegral<int32_t>();
    auto defaultValue = fdp.ConsumeIntegral<int32_t>();
    mgr.QueryValue(queryKey, defaultValue);
}

} // namespace Utils
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Utils::ConfigManagerFuzzTest(data, size);
    return 0;
}
