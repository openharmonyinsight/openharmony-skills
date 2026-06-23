// Eval file for rule: Public接口禁止返回位置信息
// 反例1：Public接口返回WiFi BSSID
/**
 * @brief Get the current WiFi connection info.
 *
 * @param info Output connection info.
 * @return 0 on success, negative error code on failure.
 * @since 10
 */
int32_t GetWifiConnectionInfo(WifiConnectionInfo* info);

typedef struct {
    char ssid[33];
    char bssid[18];        // 问题：Public接口返回BSSID
    int32_t rssi;
} WifiConnectionInfo;

// 反例2：Public接口返回蓝牙设备真实MAC地址
/**
 * @brief Get the remote Bluetooth device info.
 *
 * @param deviceId Remote device ID.
 * @param info Output device info.
 * @return 0 on success.
 * @since 10
 */
int32_t GetRemoteDeviceInfo(const char* deviceId, BluetoothDeviceInfo* info);

typedef struct {
    char address[18];      // 问题：返回蓝牙设备真实MAC地址
    char name[241];
    int32_t deviceClass;
} BluetoothDeviceInfo;

// 反例3：Public接口返回蜂窝基站信息
/**
 * @brief Get the current cell information.
 *
 * @param cellInfo Output cell information.
 * @return 0 on success.
 * @since 10
 */
int32_t GetCellInformation(CellInformation* cellInfo);

typedef struct {
    int32_t cellId;        // 问题：Cell ID 可用于位置推算
    int32_t lac;           // 问题：LAC 可用于位置推算
    int32_t mcc;           // 问题：MCC 可辅助定位
    int32_t mnc;           // 问题：MNC 可辅助定位
    int32_t signalStrength;
} CellInformation;

// 反例4：返回对象中嵌套包含位置敏感信息
/**
 * @brief Get the network scan result.
 *
 * @param results Output array of scan results.
 * @param count Number of results returned.
 * @return 0 on success.
 * @since 10
 */
int32_t GetNetworkScanResults(NetworkScanResult* results, int32_t* count);

typedef struct {
    char ssid[33];
    char mac[18];          // 问题：WiFi MAC地址可推算位置
    int32_t rssi;
    int32_t frequency;
} NetworkScanResult;

// 反例5：回调参数中包含BSSID
/**
 * @brief Register a callback for WiFi state changes.
 *
 * @param callback Callback function, receives WiFi info including BSSID.
 * @return 0 on success.
 * @since 10
 */
int32_t RegisterWifiStateCallback(WifiStateCallback callback);

typedef struct {
    char ssid[33];
    char bssid[18];        // 问题：回调参数中的BSSID同样属于位置信息泄露
    int32_t rssi;
} WifiStateInfo;

typedef void (*WifiStateCallback)(const WifiStateInfo* info);
