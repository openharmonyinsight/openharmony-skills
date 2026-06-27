// Eval file for rule: 数值类型给出单位说明
// 反例1：数值类型参数未给出单位说明
/**
 * @param timeout Timeout value.
 */
int32_t SetTimeout(int32_t timeout);

// 反例2：缺少时间单位说明
/**
 * @param duration Duration value.
 */
int32_t SetDuration(int32_t duration);

// 反例3：缺少空间单位说明
/**
 * @param width Width value.
 */
int32_t SetWidth(int32_t width);

// 反例4：缺少频率单位
/**
 * @param frequency Sampling rate.
 */
int32_t SetSamplingRate(int32_t frequency);

// 反例5：缺少速度单位
/**
 * @param speed Speed value.
 */
int32_t SetSpeed(float speed);

// 反例6：缺少角度单位
/**
 * @param angle Rotation value.
 */
int32_t SetRotation(float angle);
