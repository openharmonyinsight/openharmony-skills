#include "location_adapter.h"
#include "location_manager.h"
#include "location_cache.h"

namespace OHOS {
namespace Location {

class OHOSLocationAdapter : public LocationAdapter {
public:
    bool StartLocating(const LocationRequest& request) override {
        return LocationManager::GetInstance().Start(request.priority, request.intervalMs);
    }

    bool StopLocating() override {
        return LocationManager::GetInstance().Stop();
    }

    LocationInfo GetCachedLocation() override {
        return LocationCache::GetInstance().Get();
    }

    void SetLocationCallback(std::function<void(const LocationInfo&)> callback) override {
        LocationManager::GetInstance().SetCallback(callback);
    }
};

}
}
