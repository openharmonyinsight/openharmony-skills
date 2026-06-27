// Eval file for rule: 可选属性或参数提供默认值
// 反例1：可选参数未给出默认值说明
/**
 * @param enabled Whether to enable the feature.
 */
int32_t SetFeatureEnabled(bool enabled);

// 反例2：布尔类型可选参数未说明默认行为
/**
 * @param isModal Whether to use modal mode.
 */
int32_t SetModal(bool isModal);

// 反例3：数值类型可选参数未说明默认值
/**
 * @param timeout Timeout interval.
 */
int32_t SetTimeout(int32_t timeout);

// 反例4：枚举类型可选参数未说明默认值
/**
 * @param mode Display mode.
 */
int32_t SetDisplayMode(int32_t mode);

// 反例5：浮点数参数未说明默认值
/**
 * @param opacity Opacity value.
 */
int32_t SetOpacity(float opacity);
