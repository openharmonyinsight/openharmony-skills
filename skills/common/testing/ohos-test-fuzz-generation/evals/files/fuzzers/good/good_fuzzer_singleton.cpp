#include "simple_class.h"
#include <cstddef>
#include <cstdint>
#include <fuzztest/fuzz_data_provider.h>

namespace OHOS {
namespace Utils {

static ConfigManager *g_configManager = nullptr;

void ConfigManagerFuzzTest(const uint8_t *data, size_t size)
{
    if (g_configManager == nullptr) {
        return;
    }

    FuzzedDataProvider fdp(data, size);

    int32_t sectionId = fdp.ConsumeIntegral<int32_t>();
    std::string configKey = fdp.ConsumeRandomLengthString(256);
    g_configManager->SetConfig(sectionId, configKey);

    int32_t key = fdp.ConsumeIntegral<int32_t>();
    float weight = fdp.ConsumeFloatingPoint<float>();
    g_configManager->UpdateValue(key, weight);

    int32_t resetId = fdp.ConsumeIntegral<int32_t>();
    g_configManager->ResetSection(resetId);

    std::string sourcePath = fdp.ConsumeRandomLengthString(256);
    int32_t priority = fdp.ConsumeIntegralInRange<int32_t>(0, 100);
    g_configManager->MergeConfig(sourcePath, priority);

    int32_t queryKey = fdp.ConsumeIntegral<int32_t>();
    int32_t defaultValue = fdp.ConsumeIntegral<int32_t>();
    g_configManager->QueryValue(queryKey, defaultValue);
}

} // namespace Utils
} // namespace OHOS

extern "C" int LLVMFuzzerInitialize(int *argc, char ***argv)
{
    OHOS::Utils::g_configManager = new OHOS::Utils::ConfigManager();
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Utils::ConfigManagerFuzzTest(data, size);
    return 0;
}
