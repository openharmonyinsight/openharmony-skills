#include <unordered_map>
#include <fstream>
#include <sstream>
#include "preferences_helper.h"

namespace OHOS {
namespace Preferences {

std::shared_ptr<PreferencesStore> PreferencesHelper::store_ = nullptr;

std::string PreferencesHelper::GetValue(const std::string& key, const std::string& defValue) {
    if (!store_) {
        return defValue;
    }
    return store_->Get(key, defValue);
}

bool PreferencesHelper::SetValue(const std::string& key, const std::string& value) {
    if (!store_) {
        return false;
    }
    return store_->Put(key, value);
}

bool PreferencesHelper::DeleteValue(const std::string& key) {
    if (!store_) {
        return false;
    }
    return store_->Delete(key);
}

bool PreferencesHelper::HasKey(const std::string& key) {
    if (!store_) {
        return false;
    }
    return store_->Contains(key);
}

void PreferencesHelper::Flush() {
    if (store_) {
        store_->Save("/data/preferences/default.xml");
    }
}

void PreferencesHelper::Clear() {
    if (store_) {
        store_->ClearAll();
    }
}

bool PreferencesStore::Load(const std::string& filePath) {
    std::ifstream file(filePath);
    if (!file.is_open()) {
        return false;
    }
    std::string line;
    while (std::getline(file, line)) {
        size_t pos = line.find('=');
        if (pos != std::string::npos) {
            std::string key = line.substr(0, pos);
            std::string value = line.substr(pos + 1);
            data_[key] = value;
        }
    }
    return true;
}

bool PreferencesStore::Save(const std::string& filePath) {
    std::ofstream file(filePath);
    if (!file.is_open()) {
        return false;
    }
    for (const auto& pair : data_) {
        file << pair.first << "=" << pair.second << "\n";
    }
    return true;
}

std::string PreferencesStore::Get(const std::string& key, const std::string& defValue) const {
    auto it = data_.find(key);
    return (it != data_.end()) ? it->second : defValue;
}

bool PreferencesStore::Put(const std::string& key, const std::string& value) {
    data_[key] = value;
    return true;
}

bool PreferencesStore::Delete(const std::string& key) {
    return data_.erase(key) > 0;
}

bool PreferencesStore::Contains(const std::string& key) const {
    return data_.find(key) != data_.end();
}

void PreferencesStore::ClearAll() {
    data_.clear();
}

}
}
