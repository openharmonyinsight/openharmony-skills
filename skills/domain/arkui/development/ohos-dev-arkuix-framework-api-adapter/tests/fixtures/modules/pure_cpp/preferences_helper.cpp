#include <string>
#include <memory>

namespace OHOS {
namespace Preferences {

class PreferencesHelper {
public:
    static std::string GetValue(const std::string& key, const std::string& defValue);
    static bool SetValue(const std::string& key, const std::string& value);
    static bool DeleteValue(const std::string& key);
    static bool HasKey(const std::string& key);
    static void Flush();
    static void Clear();
private:
    static std::shared_ptr<PreferencesStore> store_;
};

class PreferencesStore {
public:
    bool Load(const std::string& filePath);
    bool Save(const std::string& filePath);
    std::string Get(const std::string& key, const std::string& defValue) const;
    bool Put(const std::string& key, const std::string& value);
    bool Delete(const std::string& key);
    bool Contains(const std::string& key) const;
    void ClearAll();
private:
    std::unordered_map<std::string, std::string> data_;
};

}
}
