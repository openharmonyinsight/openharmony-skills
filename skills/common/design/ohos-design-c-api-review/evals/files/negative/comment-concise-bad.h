// Eval file for rule: 注释内容突出重点，简洁完备
// 反例1：brief 过于冗长，包含过多细节
/**
 * @brief This function is responsible for creating a new file at the specified
 *        file path location on the storage device, and it will return a result
 *        code indicating whether the operation was successful or not.
 * 问题：brief 过长，核心信息被淹没
 *
 * @param path The file path.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CreateFile(const char* path);

// 反例2：brief 与详细描述重复
/**
 * @brief Creates a file at the specified path.
 *
 * This function creates a file at the specified path. If the file already exists,
 * it will be truncated. The parent directory must exist.
 * 问题：第一句与 brief 完全重复
 *
 * @param path The path of the file to create.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CreateFile2(const char* path);

// 反例3：参数描述冗长重复
/**
 * @brief Sets the display brightness.
 *
 * @param level This parameter is used to set the brightness level of the display.
 *              The value should be between 0 and 100. A value of 0 means the
 *              display is turned off, and a value of 100 means maximum brightness.
 * 问题：描述过于啰嗦，应直接说明范围和含义
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetBrightness(int level);

// 反例4：详细描述包含无关信息
/**
 * @brief Reads data from a file.
 *
 * This function uses the standard POSIX read system call to read data from
 * the file descriptor. It internally calls the kernel's read implementation
 * which handles all the low-level details of file I/O. The data is read into
 * the provided buffer at the specified offset.
 * 问题：开发者不需要知道内部实现细节
 *
 * @param fileDesc The file descriptor.
 * @param buffer The buffer to store data.
 * @param size Number of bytes to read.
 * @return Returns actual bytes read on success, or -1 on failure.
 * @since 7
 */
ssize_t ReadFile(int fileDesc, void* buffer, size_t size);

// 反例5：关键信息缺失（线程安全信息）
/**
 * @brief Gets the current configuration.
 *
 * @param config Output buffer to store the configuration.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int GetConfig(Config* config);
// 问题：如果这个函数不是线程安全的，必须在注释中说明

// 反例6：关键信息缺失（使用前提）
/**
 * @brief Reads the next record from the database cursor.
 *
 * @param cursor The database cursor.
 * @param record Output buffer to store the record.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int FetchNextRecord(Cursor* cursor, Record* record);
// 问题：未说明必须先调用 Query() 创建 cursor

// 反例7：关键信息缺失（资源释放）
/**
 * @brief Creates an image decoder.
 *
 * @param imageData The image data buffer.
 * @param dataSize Size of the image data.
 * @param decoder Output parameter for the created decoder.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CreateImageDecoder(const uint8_t* imageData, size_t dataSize, ImageDecoder** decoder);
// 问题：未说明需要调用 DestroyImageDecoder() 释放资源

// 反例8：注意事项过于冗长
/**
 * @brief Sends data to the remote server.
 *
 * Note: Please be aware that this function will block the calling thread until
 *       all the data has been successfully sent to the server, or until an error
 *       occurs. If you need to perform non-blocking operations, you should use
 *       the SendDataAsync function instead. Also, make sure that the connection
 *       has been established before calling this function, otherwise it will
 *       return an error.
 * 问题：注意事项过长，应简化
 *
 * @param data The data buffer to send.
 * @param size Number of bytes to send.
 * @return Returns actual bytes sent on success, or -1 on failure.
 * @since 7
 */
ssize_t SendData(const void* data, size_t size);
