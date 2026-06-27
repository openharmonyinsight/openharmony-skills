// Eval file for rule: 注释内容正确无歧义
// 反例1：参数名是 src，注释描述成 dest（复制粘贴错误）
/**
 * @brief Copies data from source to destination.
 *
 * @param src The destination buffer.  <-- 错误：应该是 source buffer
 * @param dest The source buffer.     <-- 错误：应该是 destination buffer
 * @param size Number of bytes to copy.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CopyData(const char* src, char* dest, size_t size);

// 反例2：函数名是 StartSensor，注释却描述停止功能（复制粘贴错误）
/**
 * @brief Stops the sensor and releases resources.
 *
 * After calling this function, the sensor will stop working.
 * <-- 错误：函数是 StartSensor 不是 StopSensor
 *
 * @param sensorId The sensor identifier.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int StartSensor(int sensorId);

// 反例3：返回值描述与实际不符
/**
 * @brief Gets the current timestamp.
 *
 * @return Returns the battery level.  <-- 错误：应该是 timestamp
 * @since 7
 */
time_t GetTimestamp(void);

// 反例4：参数方向描述错误
/**
 * @brief Reads data from a file.
 *
 * @param filePath The path of the file to write.  <-- 错误：应该是 read
 * @param buffer The buffer containing data to write. <-- 错误：应该是 to store read data
 * @param size Number of bytes to read.
 * @return Returns actual bytes written on success.  <-- 错误：应该是 read
 * @since 7
 */
ssize_t ReadFile(const char* filePath, void* buffer, size_t size);

// 反例5：结构体成员注释与成员名不匹配
/**
 * @brief User information structure.
 */
typedef struct {
    /** User's unique email address. */  <-- 错误：对应的是 userId
    int userId;
    /** User's unique identifier. */     <-- 错误：对应的是 userName
    char userName[64];
    /** Account creation timestamp. */
    time_t createTime;
} UserInfo;

// 反例6：枚举值注释错误
/**
 * @brief Network connection state.
 */
typedef enum {
    /** Device is disconnected. */
    NET_STATE_DISCONNECTED = 0,
    /** Device is disconnected. */      <-- 错误：重复描述
    NET_STATE_CONNECTING = 1,
    /** Device is connected. */
    NET_STATE_CONNECTED = 2,
    /** Device is connected. */         <-- 错误：应该是 FAILED
    NET_STATE_FAILED = 3,
} NetState;

// 反例7：@see 引用的函数名错误
/**
 * @brief Connects to the server.
 *
 * @param serverIp The server IP address.
 * @param port The server port number.
 * @return Returns 0 on success, or a negative error code on failure.
 * @see DisconnectToServer()  <-- 错误：应该是 DisconnectFromServer
 * @since 7
 */
int ConnectToServer(const char* serverIp, uint16_t port);

// 反例8：参数类型与注释不符
/**
 * @brief Sets the volume level.
 *
 * @param volume The volume level to set, range [0, 100].
 *               Pass a floating-point value for finer control.  <-- 错误：参数是 int 类型
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetVolume(int volume);

// 反例9：单位描述错误
/**
 * @brief Sets the request timeout period.
 *
 * @param timeout The timeout value in seconds.  <-- 错误：实际是毫秒
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetTimeout(int timeout);
