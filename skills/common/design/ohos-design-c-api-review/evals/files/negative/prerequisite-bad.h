// Eval file for rule: 说明前置依赖关系和环境要求
// 反例1：网络依赖API未说明
/**
 * @return Returns device basic info.
 */
DeviceInfo* GetDeviceBasicInfo(void);

// 反例2：资源依赖API未说明
/**
 * Executes data transfer.
 * @return 0 on success.
 */
int32_t ExecuteDataTransfer(void);

// 反例3：权限依赖API未说明
/**
 * @param dataId Data ID.
 * @return Data pointer.
 */
Data* ReadSensitiveData(int32_t dataId);

// 反例4：初始化依赖API未说明
/**
 * Gets the current location.
 * @param location Output location.
 * @return 0 on success.
 */
int32_t GetCurrentLocation(Location* location);

// 反例5：设备状态依赖未说明
/**
 * Starts camera capture.
 * @return 0 on success.
 */
int32_t StartCameraCapture(void);
