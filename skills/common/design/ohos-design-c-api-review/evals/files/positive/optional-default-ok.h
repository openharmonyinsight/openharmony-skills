// Eval file for rule: 可选属性或参数提供默认值
// 正例1：说明默认值
/**
 * Connection timeout interval. The default value is 60000 ms.
 */
int32_t SetConnectionTimeout(int32_t timeout);

// 正例2：布尔类型说明默认值
/**
 * Whether to skip certificate verification. The default value is false.
 */
int32_t SetSkipCertVerification(bool skip);

// 正例3：说明枚举类型默认值
/**
 * No alignment. This is the default value.
 */

// 正例4：说明数值类型默认值
/**
 * .value[0].f32: distance to translate along the x-axis, in vp. The default value is 0.
 * .value[1].f32: distance to translate along the y-axis, in vp. The default value is 0.
 */

// 正例5：说明字符串类型默认值
/**
 * @param logLevel Log level string. The default value is "info".
 */
int32_t SetLogLevel(const char* logLevel);
