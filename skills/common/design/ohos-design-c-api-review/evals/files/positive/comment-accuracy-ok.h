// Eval file for rule: 注释内容正确无歧义
// 正例1：参数描述与函数名、参数名一致
/**
 * @brief Deletes the specified file.
 *
 * @param filePath The path of the file to delete.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int DeleteFile(const char* filePath);

// 正例2：返回值描述准确，说明具体含义
/**
 * @brief Gets the current battery level.
 *
 * @return Returns the battery level as a percentage (0-100).
 *         Returns -1 if battery information is unavailable.
 * @since 7
 */
int GetBatteryLevel(void);

// 正例3：参数单位明确说明
/**
 * @brief Sets the network request timeout.
 *
 * @param timeoutMs The timeout value in milliseconds.
 *                  Valid range: [100, 30000]. 0 means no timeout.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetRequestTimeout(int timeoutMs);

// 正例4：准确描述参数的方向（输入/输出）
/**
 * @brief Calculates the checksum of the data.
 *
 * @param data Input buffer containing the data to calculate.
 * @param dataLen Length of the input data in bytes.
 * @param checksum Output buffer to store the calculated checksum.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CalculateChecksum(const uint8_t* data, size_t dataLen, uint32_t* checksum);

// 正例5：相关函数的注释各自准确描述其功能
/**
 * @brief Connects to a remote server using TCP.
 *
 * @param serverIp The IP address of the server.
 * @param serverPort The port number of the server.
 * @return Returns the socket descriptor on success, or -1 on failure.
 * @since 7
 */
int ConnectToServer(const char* serverIp, uint16_t serverPort);

/**
 * @brief Disconnects from the connected server.
 *
 * This function closes the active connection. Call this after ConnectToServer().
 *
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int DisconnectFromServer(void);

// 正例6：枚举值注释准确说明每个值的含义
/**
 * @brief Device connection state.
 */
typedef enum {
    /** Device is disconnected. */
    DEVICE_STATE_DISCONNECTED = 0,
    /** Device is connecting. */
    DEVICE_STATE_CONNECTING = 1,
    /** Device is connected. */
    DEVICE_STATE_CONNECTED = 2,
    /** Device connection failed. */
    DEVICE_STATE_FAILED = 3,
} DeviceState;

// 正例7：结构体成员注释准确
/**
 * @brief User information structure.
 */
typedef struct {
    /** Unique user identifier. */
    int userId;
    /** User's display name, maximum 63 characters. */
    char userName[64];
    /** User's email address. */
    char email[128];
    /** Account creation timestamp in seconds since epoch. */
    time_t createTime;
} UserInfo;

// 正例8：错误码描述清晰，说明触发条件
/**
 * @brief Opens a database connection.
 *
 * @param dbPath Path to the database file.
 * @return Returns 0 on success, or a negative error code on failure.
 * @retval 0 Success
 * @retval -1 Invalid database path
 * @retval -2 Database file does not exist
 * @retval -3 Database file is corrupted
 * @retval -4 Insufficient memory
 * @since 7
 */
int OpenDatabase(const char* dbPath);
