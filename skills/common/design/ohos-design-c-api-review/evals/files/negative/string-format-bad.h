// Eval file for rule: 字符串类型给出字符串格式
// 反例1：颜色字符串未说明格式
/**
 * @param color Background color string.
 */
int32_t SetBackgroundColor(const char* color);

// 反例2：URI字符串未说明格式
/**
 * @param uri Resource URI string.
 */
int32_t SetResourceUri(const char* uri);

// 反例3：日期字符串未说明格式
/**
 * @param date Date string.
 */
int32_t SetDate(const char* date);

// 反例4：电话号码字符串未说明格式
/**
 * @param phone Phone number string.
 */
int32_t SetPhoneNumber(const char* phone);

// 反例5：邮箱字符串未说明格式
/**
 * @param email Email address string.
 */
int32_t SetEmail(const char* email);

// 反例6：版本号字符串未说明格式
/**
 * @param version Version string.
 */
int32_t SetVersion(const char* version);
