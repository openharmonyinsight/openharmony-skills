// Eval file for rule: 针对一系列关联接口或特性是否支持，提供能力查询接口
// 正例1：POI服务提供能力查询
/**
 * @brief Check whether the POI service is supported.
 *
 * @return True if POI service is supported.
 * @since 12
 */
bool IsPoiServiceSupported(void);

/**
 * @brief Get POI information near the current location.
 *
 * @param request POI query request.
 * @param result Output POI information list.
 * @param resultCount Output count of results.
 * @return 0 on success, 801 if capability not supported.
 * @since 12
 */
int32_t GetPoiInfo(const PoiRequest* request, PoiInfo* result, int32_t* resultCount);

// 正例2：相机提供支持的设备列表查询
/**
 * @brief Get the list of supported cameras.
 *
 * @param cameras Output camera device list.
 * @param count Output count of cameras.
 * @return 0 on success.
 * @since 10
 */
int32_t GetSupportedCameras(CameraDevice* cameras, int32_t* count);

/**
 * @brief Create a camera input.
 *
 * @param camera Camera device.
 * @param input Output camera input handle.
 * @return 0 on success, 801 if not supported.
 * @since 10
 */
int32_t CreateCameraInput(const CameraDevice* camera, CameraInputHandle* input);

// 正例3：传感器提供能力查询
/**
 * @brief Check whether a sensor type is supported.
 *
 * @param sensorId Sensor type ID.
 * @return True if the sensor is supported.
 * @since 10
 */
bool IsSensorSupported(int32_t sensorId);

/**
 * @brief Subscribe to sensor data.
 *
 * @param sensorId Sensor type ID.
 * @param callback Sensor data callback.
 * @return 0 on success, 801 if not supported.
 * @since 10
 */
int32_t SubscribeSensor(int32_t sensorId, SensorCallback callback);

// 正例4：硬件特性查询
/**
 * @brief Check whether the device supports a specific hardware feature.
 *
 * @param featureId Hardware feature ID.
 * @return True if the feature is supported.
 * @since 10
 */
bool IsHardwareFeatureSupported(int32_t featureId);
