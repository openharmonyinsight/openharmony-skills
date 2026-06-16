#ifndef SIMPLE_CLASS_H
#define SIMPLE_CLASS_H

#include <string>
#include <cstdint>

namespace OHOS {
namespace Utils {

class ConfigManager {
public:
    ConfigManager() = default;
    ~ConfigManager() = default;

    bool SetConfig(int32_t sectionId, const std::string &configKey);
    int32_t UpdateValue(int32_t key, float weight);
    void ResetSection(int32_t sectionId);
    bool MergeConfig(const std::string &sourcePath, int32_t priority);
    int32_t QueryValue(int32_t key, int32_t defaultValue) const;

private:
    int32_t activeSection_ = 0;
    std::string configRootPath_;
};

} // namespace Utils
} // namespace OHOS

#endif // SIMPLE_CLASS_H
