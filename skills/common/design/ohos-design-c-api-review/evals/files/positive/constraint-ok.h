// Eval file for rule: 约束限制合理
// 正例1：路径参数允许常见字符，符合行业惯例
/**
 * @brief Open a file from the specified path.
 *
 * @param path File path, supports common characters including letters, digits, hyphens, and underscores.
 * @param mode File open mode.
 * @return File handle.
 * @since 10
 */
FileHandle OpenFile(const char* path, FileMode mode);

// 正例2：缓冲区大小限制合理，允许足够大的缓冲区
/**
 * @brief Read data from the buffer.
 *
 * @param buffer Target buffer to receive data.
 * @param bufferSize Size of the target buffer, in bytes. Maximum allowed size is 16MB.
 * @return Number of bytes actually read.
 * @since 11
 */
int32_t ReadBuffer(uint8_t* buffer, size_t bufferSize);

// 正例3：约束简洁明确，只有必要的约束
/**
 * @brief Subscribe to sensor data.
 *
 * @param sensorId Sensor type ID. Must be a valid sensor type.
 * @param callback Callback function for sensor data.
 * @return 0 on success, negative error code on failure.
 * @since 10
 */
int32_t SubscribeSensor(int32_t sensorId, SensorCallback callback);
