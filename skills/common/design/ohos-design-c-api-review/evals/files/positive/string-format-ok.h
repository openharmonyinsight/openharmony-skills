// Eval file for rule: 字符串类型给出字符串格式
// 正例1：说明颜色格式
/**
 * @param maskColor Indicates the mask color, in 0xARGB format.
 */
int32_t SetMaskColor(uint32_t maskColor);

// 正例2：说明颜色格式
/**
 * .value[0].u32: shadow color, in 0xARGB format.
 */

// 正例3：说明颜色格式
/**
 * @param arrowColor the color of the arrow, in 0xARGB format.
 */
int32_t SetArrowColor(uint32_t arrowColor);

// 正例4：说明URI格式
/**
 * @param uri Resource URI, in format "file://<path>" or "http://<host>/<path>".
 */
int32_t SetResourceUri(const char* uri);

// 正例5：说明日期格式
/**
 * @param date Date string, in format "yyyy-MM-dd".
 */
int32_t SetDate(const char* date);

// 正例6：说明GUID格式
/**
 * @param deviceId Device unique identifier, in GUID format "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
 */
int32_t SetDeviceId(const char* deviceId);
