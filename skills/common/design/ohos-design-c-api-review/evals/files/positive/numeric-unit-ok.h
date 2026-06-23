// Eval file for rule: 数值类型给出单位说明
// 正例1：使用"in pixels"说明单位
/**
 * @param width Width of the preview image, in pixels.
 * @param height Height of the preview image, in pixels.
 */
int32_t SetPreviewSize(int32_t width, int32_t height);

// 正例2：使用"in milliseconds"说明单位
/**
 * @param timeout Connection timeout interval. The default value is 60000 ms.
 */
int32_t SetConnectionTimeout(int32_t timeout);

// 正例3：使用"The unit is vp"说明单位
/**
 * .value[0].f32: width of the left edge. The unit is vp.
 * .value[1].f32: width of the top edge. The unit is vp.
 */

// 正例4：使用标准单位符号
/**
 * @param frequency Sampling frequency, in Hz.
 * @param bitrate Audio bitrate, in bit/s.
 */
int32_t SetAudioParams(int32_t frequency, int32_t bitrate);

// 正例5：说明角度单位
/**
 * @param angle Rotation angle, in degrees.
 */
int32_t SetRotation(float angle);
