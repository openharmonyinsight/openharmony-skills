#import <CoreLocation/CoreLocation.h>
#include "location_adapter.h"

namespace OHOS {
namespace Location {

class IOSLocationAdapter : public LocationAdapter {
public:
    bool StartLocating(const LocationRequest& request) override {
        if (!manager_) {
            manager_ = [[CLLocationManager alloc] init];
            manager_.delegate = delegate_;
            manager_.desiredAccuracy = kCLLocationAccuracyBest;
        }
        [manager_ startUpdatingLocation];
        return true;
    }

    bool StopLocating() override {
        if (manager_) {
            [manager_ stopUpdatingLocation];
        }
        return true;
    }

    LocationInfo GetCachedLocation() override {
        LocationInfo info = {};
        if (manager_ && manager_.location) {
            CLLocation* loc = manager_.location;
            info.latitude = loc.coordinate.latitude;
            info.longitude = loc.coordinate.longitude;
            info.altitude = loc.altitude;
            info.accuracy = loc.horizontalAccuracy;
            info.speed = loc.speed;
            info.timestamp = loc.timestamp.timeIntervalSince1970 * 1000;
        }
        return info;
    }

    void SetLocationCallback(std::function<void(const LocationInfo&)> callback) override {
        callback_ = callback;
    }

private:
    CLLocationManager* manager_ = nil;
    id<CLLocationManagerDelegate> delegate_ = nil;
    std::function<void(const LocationInfo&)> callback_;
};

}
}
