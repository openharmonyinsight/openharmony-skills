// Eval file for rule: 不同语言相同功能接口错误码定义应保持一致
// 正例：C接口和TypeScript接口使用一致的错误码
/**
 * @brief Starts an ability.
 * @param want The ability want.
 * @return 0 on success, 201 on permission denied, 401 on parameter error.
 */
int OH_AbilityRuntime_StartAbility(Want* want);

// C++实现返回相同的错误码
int OH_AbilityRuntime_StartAbility(Want* want) {
    if (!CheckPermission()) return 201;  // 与TS接口一致
    if (want == nullptr) return 401;      // 与TS接口一致
    return DoStartAbility(want);
}

// 正例2：跨语言错误码定义一致
#define ERR_PERMISSION_DENIED 201
#define ERR_INVALID_PARAM 401
#define ERR_NOT_SUPPORTED 801

/**
 * @brief Connects to a service.
 * @param serviceId Service identifier.
 * @return 0 on success, ERR_PERMISSION_DENIED(201) on permission denied,
 *         ERR_INVALID_PARAM(401) on parameter error,
 *         ERR_NOT_SUPPORTED(801) if capability not supported.
 */
int32_t ConnectService(const char* serviceId);
