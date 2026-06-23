// Eval file for rule: Public接口禁止返回位置信息
// 正例1：WiFi接口不返回BSSID
/**
 * @brief Get the current WiFi connection info.
 *
 * @param info Output connection info. Does not contain BSSID or MAC address.
 * @return 0 on success, negative error code on failure.
 * @since 10
 */
int32_t GetWifiConnectionInfo(WifiConnectionInfo* info);

typedef struct {
    char ssid[33];
    int32_t rssi;
    int32_t frequency;
    int32_t link_speed;
    // 不包含 bssid 字段
} WifiConnectionInfo;

// 正例2：蓝牙接口通过系统接口开放（经过TMG评审+权限控制）
/**
 * @brief Get the Bluetooth device address.
 * @permission ohos.permission.ACCESS_BLUETOOTH
 * @systemapi
 *
 * @param address Output buffer for device address string.
 * @param bufferSize Size of the output buffer.
 * @return 0 on success.
 * @since 10
 */
int32_t GetDeviceAddress(char* address, size_t bufferSize);

// 正例3：网络接口返回信息不包含基站标识
/**
 * @brief Get the current network registration info.
 *
 * @param info Output network registration info.
 * @return 0 on success, negative error code on failure.
 * @since 10
 */
int32_t GetNetworkRegistrationInfo(NetworkRegistrationInfo* info);

typedef struct {
    int32_t networkType;
    int32_t registrationState;
    bool isRoaming;
    // 不包含 cellId, lac, mcc, mnc 等基站标识字段
} NetworkRegistrationInfo;
