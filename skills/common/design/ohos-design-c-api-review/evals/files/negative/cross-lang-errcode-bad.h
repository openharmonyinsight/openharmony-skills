// Eval file for rule: 不同语言相同功能接口错误码定义应保持一致
// 反例1：C接口定义的错误码与TypeScript接口不一致
#define ERR_PERMISSION_DENIED 201
#define ERR_INVALID_PARAM 401

// C接口声明错误码201（权限拒绝）和401（参数错误）
/**
 * @brief Starts an ability.
 * @param want The ability want.
 * @return 0 on success, 201 on permission denied, 401 on parameter error.
 */
int OH_AbilityRuntime_StartAbility(Want* want);

// 但TypeScript接口使用不同的错误码
// TS: @throws { BusinessError } 202 - Permission error.
// 问题：TS使用202，C使用201，不一致

// 反例2：C接口实现中有错误码但其他语言实现中缺少对应定义
#define ERR_NETWORK_ERROR 301
#define ERR_TIMEOUT 302

int32_t ConnectService(const char* serviceId) {
    if (!IsNetworkAvailable()) return ERR_NETWORK_ERROR;  // C有301
    if (IsTimeout()) return ERR_TIMEOUT;                   // C有302
    return DoConnect(serviceId);
}
// 问题：其他语言实现中可能缺少301和302的错误码定义

// 反例3：错误码含义不一致
// C接口: 401 = "parameter type/count mismatch"
// TS接口: 401 = "parameter value out of range"
// 问题：同一错误码401，C和TS的语义定义不一致
