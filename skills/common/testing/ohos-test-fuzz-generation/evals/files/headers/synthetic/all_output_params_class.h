#ifndef ALL_OUTPUT_PARAMS_CLASS_H
#define ALL_OUTPUT_PARAMS_CLASS_H

#include <cstdint>
#include <vector>

namespace OHOS {
namespace Sensor {

class SensorDataReader {
public:
    SensorDataReader() = default;
    ~SensorDataReader() = default;

    void GetAccelerometerData(float& x, float& y, float& z);
    void GetGyroscopeData(float& angularX, float& angularY, float& angularZ);
    void GetProximityDistance(int32_t& distance);
    void GetAmbientLightLevel(int32_t& luxValue);
    void GetAllSensorData(std::vector<int32_t>& readings);
};

} // namespace Sensor
} // namespace OHOS

#endif // ALL_OUTPUT_PARAMS_CLASS_H
