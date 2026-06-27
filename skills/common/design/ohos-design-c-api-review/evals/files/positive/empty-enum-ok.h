// Eval file for rule: 禁止创建空枚举/常量接口
// 正例：错误码都有对应的返回场景
typedef enum {
    SUCCESS = 0,
    NETWORK_ERROR = 1001,
    TIMEOUT_ERROR = 1002,
} ErrorCode;

int32_t Connect(void) {
    if (!IsNetworkAvailable()) {
        return NETWORK_ERROR;  // NETWORK_ERROR 有对应的返回
    }
    return SUCCESS;
}

int32_t RequestWithTimeout(void) {
    if (IsTimeout()) {
        return TIMEOUT_ERROR;  // TIMEOUT_ERROR 有对应的返回
    }
    return DoRequest();
}
