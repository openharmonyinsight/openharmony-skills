// Eval file for rule: 针对一系列关联接口或特性是否支持，提供能力查询接口
// 反例1：能力查询接口命名不规范
/**
 * @brief Check whether NFC is supported.
 *
 * @return True if NFC is supported.
 * @since 10
 */
bool HasNfc(void);
// 问题：布尔值能力查询应命名为 IsXXXSupported（如 IsNfcSupported），而非 HasXXX

// 反例2：硬件相关接口在部分设备不可用但没有提供查询
/**
 * @brief Start device vibration.
 *
 * @param options Vibration options.
 * @return 0 on success, 801 if not supported.
 * @since 10
 */
int32_t StartVibration(const VibrateOptions* options);
// 问题：振动马达在部分设备不存在，缺少 IsVibratorSupported() 查询接口

// 反例3：返回列表的查询接口命名不规范
/**
 * @brief Get supported audio encoding formats.
 *
 * @param formats Output format list.
 * @param count Output count.
 * @return 0 on success.
 * @since 10
 */
int32_t QueryAudioFormats(AudioFormat* formats, int32_t* count);
// 问题：返回列表应命名为 GetSupportedXXX（如 GetSupportedAudioFormats），而非 QueryXXX
