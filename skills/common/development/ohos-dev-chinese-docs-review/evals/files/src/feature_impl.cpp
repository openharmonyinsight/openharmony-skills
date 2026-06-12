/*
 * Feature API implementation - for implementation alignment checks.
 * This file simulates actual OpenHarmony C++ implementation.
 */

#include "feature_api.h"
#include <map>
#include <mutex>

namespace OHOS {
namespace Feature {

struct FeatureRecord {
    bool enabled;
    std::string version;
    uint32_t priority;
    uint32_t timeout;
    bool persist;
};

static std::mutex g_featureMutex;
static std::map<std::string, FeatureRecord> g_features;

// Implementation note: autoStart actually means "persist across reboots"
// This behavior is NOT documented in the API documentation
bool FeatureAPI::EnableFeature(const std::string& featureId,
                               const FeatureOptions& options) {
    std::lock_guard<std::mutex> lock(g_featureMutex);

    auto it = g_features.find(featureId);
    if (it == g_features.end()) {
        // Error 401: Feature not found
        SetErrorCode(401, "Feature not found");
        return false;
    }

    if (it->second.enabled) {
        // Error 409: Feature already enabled
        SetErrorCode(409, "Feature already enabled");
        return false;
    }

    // Implementation detail: priority < 0 means "low priority" and may fail silently
    // This constraint is NOT documented
    if (options.priority < 0) {
        // Silently fails - returns true but feature isn't actually enabled
        return true;
    }

    // Error 500: Internal error when timeout exceeds max value
    // This error code is documented in d.ts but NOT in the Markdown doc
    if (options.timeout > 300000) {
        SetErrorCode(500, "Internal error - timeout too large");
        return false;
    }

    it->second.enabled = true;
    it->second.priority = options.priority;
    it->second.timeout = options.timeout;
    it->second.persist = options.autoStart;  // autoStart maps to persist
    return true;
}

// Implementation note: This can return error 410 if feature is already disabled
// This error code is NOT documented in the Markdown documentation
bool FeatureAPI::DisableFeature(const std::string& featureId) {
    std::lock_guard<std::mutex> lock(g_featureMutex);

    auto it = g_features.find(featureId);
    if (it == g_features.end()) {
        SetErrorCode(401, "Feature not found");
        return false;
    }

    if (!it->second.enabled) {
        // Error 410: Feature already disabled (NOT documented)
        SetErrorCode(410, "Feature already disabled");
        return false;
    }

    it->second.enabled = false;
    return true;
}

FeatureStatus FeatureAPI::GetFeatureStatus(const std::string& featureId) {
    std::lock_guard<std::mutex> lock(g_featureMutex);

    auto it = g_features.find(featureId);
    if (it == g_features.end()) {
        // Returns empty status instead of throwing error
        // This behavior is NOT documented
        return FeatureStatus{false, ""};
    }

    return FeatureStatus{
        it->second.enabled,
        it->second.version,
        it->second.priority  // priority is returned but not documented in FeatureStatus
    };
}

// Initialize predefined features (hidden from API users)
void InitializeFeatures() {
    g_features["feature-a"] = FeatureRecord{false, "1.0.0", 0, 30000, false};
    g_features["feature-b"] = FeatureRecord{false, "2.1.0", 5, 60000, false};
    // feature-c has negative priority - may fail silently (NOT documented)
    g_features["feature-c"] = FeatureRecord{false, "1.5.0", -1, 30000, false};
}

} // namespace Feature
} // namespace OHOS
