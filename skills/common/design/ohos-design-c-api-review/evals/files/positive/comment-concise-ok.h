// Eval file for rule: 注释内容突出重点，简洁完备
// 正例1：brief 简洁准确，直接说明核心功能
/**
 * @brief Creates a new file at the specified path.
 *
 * @param path The absolute path of the file to create.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CreateFile(const char* path);

// 正例2：关键信息（使用前提）前置说明
/**
 * @brief Reads sensor data from the device.
 *
 * The sensor must be started before calling this function.
 *
 * @param sensorId The unique identifier of the sensor.
 * @param data Output buffer to store the sensor data.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int ReadSensorData(int sensorId, SensorData* data);

// 正例3：重要限制在 @param 中说明
/**
 * @brief Sets the display brightness level.
 *
 * @param level Brightness level, valid range: [0, 100].
 *               Values outside this range will be clamped.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetBrightness(int level);

// 正例4：返回值说明简洁但完整
/**
 * @brief Gets the current battery level.
 *
 * @return Returns the battery level as a percentage (0-100),
 *         or -1 if battery information is unavailable.
 * @since 7
 */
int GetBatteryLevel(void);

// 正例5：枚举值注释简洁
/**
 * @brief Network connection state.
 */
typedef enum {
    /** Disconnected from the network. */
    NET_STATE_DISCONNECTED = 0,
    /** Connecting to the network. */
    NET_STATE_CONNECTING = 1,
    /** Connected to the network. */
    NET_STATE_CONNECTED = 2,
} NetState;

// 正例6：结构体成员注释简洁明了
/**
 * @brief User information.
 */
typedef struct {
    /** Unique user identifier. */
    int userId;
    /** Username, maximum 63 characters. */
    char username[64];
    /** User creation timestamp (seconds since epoch). */
    time_t createTime;
} UserInfo;

// 正例7：回调函数注释说明关键点
/**
 * @brief Registers a callback for state change notifications.
 *
 * The callback is invoked on a worker thread. Ensure thread safety.
 *
 * @param callback The callback function. Pass NULL to unregister.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int RegisterStateCallback(void (*callback)(State));
