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

    int32_t sectionId = fdp.ConsumeIntegral<int32_t>();
    std::string configKey = fdp.ConsumeRandomLengthString(256);
    mgr.SetConfig(sectionId, configKey);

    int32_t key = fdp.ConsumeIntegral<int32_t>();
    float weight = fdp.ConsumeFloatingPoint<float>();
    mgr.UpdateValue(key, weight);

    int32_t resetId = fdp.ConsumeIntegral<int32_t>();
    mgr.ResetSection(resetId);

    std::string sourcePath = fdp.ConsumeRandomLengthString(256);
    int32_t priority = fdp.ConsumeIntegralInRange<int32_t>(0, 100);
    mgr.MergeConfig(sourcePath, priority);

    int32_t queryKey = fdp.ConsumeIntegral<int32_t>();
    int32_t defaultValue = fdp.ConsumeIntegral<int32_t>();
    mgr.QueryValue(queryKey, defaultValue);
}

} // namespace Utils
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Utils::ConfigManagerFuzzTest(data, size);
    return 0;
}
