#pragma once
#include <string>
#include <functional>
#include <memory>

namespace OHOS {
namespace Location {

struct LocationInfo {
    double latitude;
    double longitude;
    double altitude;
    float accuracy;
    float speed;
    double timestamp;
};

enum class LocationRequestPriority {
    PRIORITY_UNSET = 0,
    PRIORITY_ACCURACY = 1,
    PRIORITY_LOW_POWER = 2,
    PRIORITY_FIRST_FIX = 3
};

struct LocationRequest {
    LocationRequestPriority priority;
    uint64_t scenario;
    uint32_t intervalMs;
};

class LocationAdapter {
public:
    virtual ~LocationAdapter() = default;
    virtual bool StartLocating(const LocationRequest& request) = 0;
    virtual bool StopLocating() = 0;
    virtual LocationInfo GetCachedLocation() = 0;
    virtual void SetLocationCallback(std::function<void(const LocationInfo&)> callback) = 0;
};

}
}
