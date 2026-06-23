// Eval file for rule: C接口中包含buffer等地址的参数需要指定buffer的大小
// 反例1：只有指针参数，没有缓冲区大小参数，容易导致缓冲区溢出
/**
 * @brief Copies a string without size information. UNSAFE!
 *
 * @param dest Destination buffer.
 * @param src Source string.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int CopyStringUnsafe(char* dest, const char* src);  // 缺少 destSize 和 srcLen

// 反例2：读取数据但不提供缓冲区大小
/**
 * @brief Reads data into buffer without size check. UNSAFE!
 *
 * @param buffer Buffer to store data.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ReadDataUnsafe(void* buffer);  // 缺少 bufferSize 参数

// 反例3：写入数据但不指定写入长度
/**
 * @brief Writes buffer without specifying length. UNSAFE!
 *
 * @param buffer Source buffer.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int WriteBufferUnsafe(const void* buffer);  // 缺少 length 参数

// 反例4：处理数组但不提供数组长度
/**
 * @brief Processes user array without count. UNSAFE!
 *
 * @param users Array of users.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ProcessUsersUnsafe(const User* users);  // 缺少 count 参数

// 反例5：输出参数不提供缓冲区大小，可能导致溢出
/**
 * @brief Gets device information without buffer size. UNSAFE!
 *
 * @param infoBuffer Buffer to store device info.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int GetDeviceInfoUnsafe(DeviceInfo* infoBuffer);  // 缺少 buffer 大小参数

// 反例6：双向缓冲区操作缺少大小参数
/**
 * @brief Processes bidirectional buffer without sizes. UNSAFE!
 *
 * @param inputBuffer Input data buffer.
 * @param outputBuffer Output data buffer.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ProcessBidirectionalUnsafe(const void* inputBuffer, void* outputBuffer);
// 缺少 inputSize 和 outputSize 参数

// 反例7：虽然定义了固定大小常量，但仍应在参数中传递大小
#define MAX_BUFFER_SIZE 256

/**
 * @brief Processes buffer using hardcoded size. NOT RECOMMENDED!
 *
 * @param buffer Data buffer.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ProcessBufferHardcoded(uint8_t* buffer);  // 应该传递实际大小而非依赖宏定义
