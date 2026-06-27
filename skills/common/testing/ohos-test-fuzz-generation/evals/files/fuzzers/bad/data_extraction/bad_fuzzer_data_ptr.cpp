#include "simple_class.h"
#include <cstddef>
#include <cstdint>

namespace OHOS {
namespace Utils {

void ConfigManagerFuzzTest(const uint8_t *data, size_t size)
{
    if (size < sizeof(int32_t) * 2) {
        return;
    }

    ConfigManager mgr;

    int32_t sectionId = *(int32_t *)data;
    data += sizeof(int32_t);
    std::string configKey(reinterpret_cast<const char *>(data), 32);
    mgr.SetConfig(sectionId, configKey);

    int32_t key = *(int32_t *)data;
    data += sizeof(int32_t);
    float weight = *(float *)data;
    data += sizeof(float);
    mgr.UpdateValue(key, weight);

    int32_t resetId = *(int32_t *)data;
    mgr.ResetSection(resetId);
}

} // namespace Utils
} // namespace OHOS

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    OHOS::Utils::ConfigManagerFuzzTest(data, size);
    return 0;
}
