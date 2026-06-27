// Eval file for rule: C接口中包含buffer等地址的参数需要指定buffer的大小
// 正例1：字符串复制函数，同时提供源字符串长度和目标缓冲区大小
/**
 * @brief Copies a string from source to destination buffer.
 *
 * @param dest Destination buffer.
 * @param destSize Size of the destination buffer in bytes.
 * @param src Source string to copy.
 * @param srcLen Length of the source string in bytes.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int CopyString(char* dest, size_t destSize, const char* src, size_t srcLen);

// 正例2：读取数据到缓冲区，提供缓冲区大小并返回实际读取长度
/**
 * @brief Reads data from a file into a buffer.
 *
 * @param buffer Buffer to store the read data.
 * @param bufferSize Size of the buffer in bytes.
 * @param bytesWritten Output parameter for actual bytes written.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ReadFileData(void* buffer, size_t bufferSize, size_t* bytesWritten);

// 正例3：通过单独的长度参数指定输入缓冲区大小
/**
 * @brief Processes data from an input buffer.
 *
 * @param data Input data buffer.
 * @param dataLength Length of the input data in bytes.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ProcessData(const uint8_t* data, size_t dataLength);

// 正例4：写入数据，明确指定要写入的数据长度
/**
 * @brief Writes data to a buffer.
 *
 * @param buffer Source buffer containing data to write.
 * @param length Number of bytes to write.
 * @return int Returns actual bytes written on success, or -1 on failure.
 * @since 7
 */
int WriteToBuffer(const void* buffer, size_t length);

// 正例5：结构体数组处理，同时提供数组长度
/**
 * @brief Processes an array of user structures.
 *
 * @param users Array of user structures.
 * @param count Number of users in the array.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ProcessUsers(const User* users, size_t count);

// 正例6：同时提供输入缓冲区大小和输出缓冲区大小
/**
 * @brief Encodes data using a specific algorithm.
 *
 * @param input Input data buffer.
 * @param inputSize Size of the input data.
 * @param output Output buffer for encoded data.
 * @param outputSize Size of the output buffer.
 * @param outputLength Output parameter for actual encoded data length.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int EncodeData(const uint8_t* input, size_t inputSize,
               uint8_t* output, size_t outputSize, size_t* outputLength);

// 正例7：通过结构体传递缓冲区信息
typedef struct {
    void* data;      ///< Buffer pointer
    size_t size;     ///< Buffer size in bytes
} BufferInfo;

/**
 * @brief Processes buffer using BufferInfo structure.
 *
 * @param buffer Buffer information including data pointer and size.
 * @return int Returns 0 on success, error code on failure.
 * @since 7
 */
int ProcessBufferStruct(const BufferInfo* buffer);
