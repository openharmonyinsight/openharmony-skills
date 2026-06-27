// Eval file for rule: Public接口禁止返回个人敏感数据
// 反例1：Public接口返回设备序列号SN
/**
 * @brief Get the device serial number.
 *
 * @param serial Output serial number string.
 * @param bufferSize Buffer size.
 * @return 0 on success.
 * @since 10
 */
int32_t GetDeviceSerial(char* serial, size_t bufferSize);

// 反例2：设备信息结构体包含MEID
/**
 * @brief Get device information.
 *
 * @param info Output device info.
 * @return 0 on success.
 * @since 10
 */
int32_t GetDeviceInfo(DeviceInfo* info);

typedef struct {
    char brand[64];
    char model[64];
    char meid[16];         // 问题：返回MEID
    char osVersion[64];
} DeviceInfo;

// 反例3：Public接口返回MAC地址
/**
 * @brief Get the device MAC address.
 *
 * @param mac Output MAC address string.
 * @param bufferSize Buffer size.
 * @return 0 on success.
 * @since 10
 */
int32_t GetMacAddress(char* mac, size_t bufferSize);

// 反例4：Public接口返回IMSI
/**
 * @brief Get the IMSI from the SIM card.
 *
 * @param imsi Output IMSI string.
 * @param bufferSize Buffer size.
 * @return 0 on success.
 * @since 10
 */
int32_t GetIMSI(char* imsi, size_t bufferSize);

// 反例5：SIM卡信息返回ICCID
/**
 * @brief Get the SIM card information.
 *
 * @param simInfo Output SIM card info.
 * @return 0 on success.
 * @since 10
 */
int32_t GetSimCardInfo(SimCardInfo* simInfo);

typedef struct {
    char operatorName[64];
    char iccid[21];        // 问题：ICCID可唯一标识SIM卡/用户
    bool isReady;
} SimCardInfo;

// 反例6：返回对象中嵌套包含设备唯一标识
/**
 * @brief Get the full system information.
 *
 * @param sysInfo Output system info.
 * @return 0 on success.
 * @since 10
 */
int32_t GetFullSystemInfo(FullSystemInfo* sysInfo);

typedef struct {
    char deviceName[64];
    char osVersion[64];
    struct {
        char model[64];
        char serialNumber[64];  // 问题：嵌套包含设备序列号
    } hardware;
} FullSystemInfo;

// 反例7：回调参数中包含手机号
/**
 * @brief Register callback for incoming call events.
 *
 * @param callback Callback function.
 * @return 0 on success.
 * @since 10
 */
int32_t RegisterCallEventCallback(CallEventCallback callback);

typedef struct {
    int32_t callState;
    char phoneNumber[21];   // 问题：回调中返回来电手机号
} CallEventInfo;

typedef void (*CallEventCallback)(const CallEventInfo* info);
