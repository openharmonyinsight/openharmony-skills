// Eval file for rule: 给出超出取值约束时的行为
// 正例1：说明取值范围和超出时的返回值
/**
 * @param levelOrder Indicates the display order. The valid range is [-100000.0, 100000.0].
 * @return Returns the error code.
 *         Returns ARKUI_ERROR_CODE_PARAM_INVALID if a parameter error occurs.
 */
int32_t SetLevelOrder(float levelOrder);

// 正例2：说明参数取值范围
/**
 * .value[0].f32: width of the image. The value range is [0, +inf), and the unit is vp.
 */

// 正例3：说明超出范围时的错误码
/**
 * @param processName The process name to set. Maximum length is 64 characters.
 * @return Returns NCP_ERR_INVALID_PARAM if the input parameters are invalid.
 */
int32_t SetProcessName(const char* processName, size_t len);

// 正例4：说明非法值时的行为
/**
 * @param alpha Alpha value. The valid range is [0.0, 1.0].
 *              Values outside this range will be clamped to the nearest valid value.
 * @return Returns 0 on success, ARKUI_ERROR_CODE_PARAM_INVALID on invalid parameter.
 */
int32_t SetAlpha(float alpha);
