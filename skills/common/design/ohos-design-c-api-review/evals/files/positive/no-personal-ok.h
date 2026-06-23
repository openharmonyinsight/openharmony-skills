// Eval file for rule: Public接口禁止返回个人敏感数据
// 正例1：设备信息接口不返回SN
/**
 * @brief Get basic device information.
 *
 * @param info Output device info. Does not contain serial number or MEID.
 * @return 0 on success.
 * @since 10
 */
int32_t GetBasicDeviceInfo(BasicDeviceInfo* info);

typedef struct {
    char deviceType[16];
    char manufacture[64];
    char brand[64];
    char model[64];
    char osVersion[64];
    // 不包含 serialNumber、meid 等唯一标识字段
} BasicDeviceInfo;

// 正例2：网络信息不返回MAC地址
/**
 * @brief Get the current active network type.
 *
 * @param networkType Output network type.
 * @return 0 on success.
 * @since 10
 */
int32_t GetActiveNetworkType(int32_t* networkType);

// 正例3：电话号码通过系统接口+权限控制开放（经过TMG评审）
/**
 * @brief Get the phone number of the SIM card.
 * @permission ohos.permission.GET_PHONE_NUMBERS
 * @systemapi
 *
 * @param phoneNumber Output phone number string.
 * @param bufferSize Output buffer size.
 * @return 0 on success.
 * @since 10
 */
int32_t GetPhoneNumber(char* phoneNumber, size_t bufferSize);
