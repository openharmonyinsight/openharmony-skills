// Eval file for rule: 注释的核心读者是应用开发者
// 正例1：描述功能用途，让开发者知道何时使用
/**
 * @brief Creates a new file at the specified path.
 *
 * This function creates a new empty file. If the file already exists, it will be truncated.
 * The parent directory must exist before calling this function.
 *
 * @param path The absolute path of the file to create.
 * @return Returns 0 on success, or a negative error code on failure.
 * @retval 0 Success
 * @retval -1 Invalid path
 * @retval -2 Permission denied
 * @retval -3 File already exists and cannot be overwritten
 * @see DeleteFile()
 * @since 7
 */
int CreateFile(const char* path);

// 正例2：说明参数的实际含义和使用注意事项
/**
 * @brief Sets the timeout for network requests.
 *
 * The timeout value is in milliseconds. A value of 0 means no timeout (wait indefinitely).
 * The timeout applies to each individual request, not the total session time.
 *
 * @param timeoutMs Timeout in milliseconds. Valid range: [0, 300000].
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetRequestTimeout(int timeoutMs);

// 正例3：清晰说明使用场景和限制
/**
 * @brief Reads sensor data from the device.
 *
 * This function blocks until new sensor data is available or the timeout expires.
 * The sensor must be started before calling this function.
 * Call StartSensor() first if the sensor is not running.
 *
 * @param sensorId The unique identifier of the sensor.
 * @param data Output buffer to store the sensor data.
 * @param timeoutMs Maximum time to wait for data, in milliseconds.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int ReadSensorData(int sensorId, SensorData* data, int timeoutMs);

// 正例4：说明返回值的实际含义
/**
 * @brief Gets the current battery level.
 *
 * @return Returns the battery level as a percentage (0-100).
 * @retval 0-100 Current battery level
 * @retval -1 Battery information unavailable
 * @since 7
 */
int GetBatteryLevel(void);

// 正例5：提供使用示例，帮助开发者快速上手
/**
 * @brief Registers a callback for state change notifications.
 *
 * The callback will be invoked on a worker thread. Ensure the callback is thread-safe.
 * Only one callback can be registered at a time. Registering a new callback replaces the old one.
 *
 * Usage example:
 * @code
 * void OnStateChanged(State newState) {
 *     printf("State changed to: %d\n", newState);
 * }
 *
 * // Register the callback
 * RegisterStateChangeCallback(OnStateChanged);
 * @endcode
 *
 * @param callback Function pointer to the callback handler. Pass NULL to unregister.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int RegisterStateChangeCallback(void (*callback)(State));

// 正例6：说明使用前提条件
/**
 * @brief Disconnects from the remote server.
 *
 * This function should be called after Connect() succeeds.
 * Calling this function without an active connection has no effect.
 *
 * @return Returns 0 on success, or a negative error code on failure.
 * @see Connect()
 * @since 7
 */
int Disconnect(void);

// 正例7：解释复杂概念的业务含义
/**
 * @brief Gets the device's unique identifier.
 *
 * The device ID is a persistent value that remains unchanged across device reboots.
 * It can be used for device registration, authentication, and data association.
 * Note: This ID is different from the serial number and should not be used for hardware tracking.
 *
 * @param idBuffer Buffer to store the device ID string.
 * @param bufferSize Size of the buffer in bytes. Recommended: 64 bytes.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int GetDeviceId(char* idBuffer, size_t bufferSize);
