#include "simple_class.h"
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <ctime>

namespace OHOS {
namespace Utils {

void ConfigManagerFuzzTest(const uint8_t *data, size_t size)
{
    srand(time(nullptr));
    ConfigManager mgr;

    int32_t sectionId = rand() % 256;
    std::string configKey = "fuzz_config_" + std::to_string(rand() % 1000);
    mgr.SetConfig(sectionId, configKey);

    int32_t key = rand() % 100;
    float weight = static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
    mgr.UpdateValue(key, weight);

    int32_t resetId = rand() % 256;
    mgr.ResetSection(resetId);

    std::string sourcePath = "/tmp/fuzz_" + std::to_string(rand() % 10000);
    int32_t priority = rand() % 100;
    mgr.MergeConfig(sourcePath, priority);

    int32_t queryKey = rand() % 50;
    int32_t defaultValue = rand() % 1000;
    mgr.QueryValue(queryKey, defaultValue);
}

} // namespace Utils
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Utils::ConfigManagerFuzzTest(data, size);
    return 0;
}
