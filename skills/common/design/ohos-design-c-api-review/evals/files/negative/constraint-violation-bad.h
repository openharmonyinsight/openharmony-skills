// Eval file for rule: 给出超出取值约束时的行为
// 反例1：有范围约束但未说明超出时的行为
/**
 * @param alpha Alpha value. The value range is [0.0, 1.0].
 */
int32_t SetAlpha(float alpha);

// 反例2：有长度约束但未说明超出时的行为
/**
 * @param name Name string. Maximum length is 20 characters.
 */
int32_t SetName(const char* name, size_t nameLen);

// 反例3：有枚举约束但未说明非法值时的行为
/**
 * @param mode Mode enum value.
 */
int32_t SetMode(int32_t mode);

// 反例4：有取值范围但未说明越界处理
/**
 * @param volume Volume level. Valid range: [0, 100].
 */
int32_t SetVolume(int32_t volume);

// 反例5：有精度约束但未说明处理方式
/**
 * @param scale Scale factor. Must be a positive number.
 */
int32_t SetScale(float scale);
