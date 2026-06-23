// Eval file for rule: 禁止创建空枚举/常量接口
// 反例1：错误码已定义但从未返回
typedef enum {
    SUCCESS = 0,
    NETWORK_ERROR = 1001,
    TIMEOUT_ERROR = 1002,     // TIMEOUT_ERROR 从未被任何函数返回
    PERMISSION_ERROR = 1003,  // PERMISSION_ERROR 从未被任何函数返回
} ErrorCode;

int32_t Connect(void) {
    if (!IsNetworkAvailable()) {
        return NETWORK_ERROR;
    }
    return SUCCESS;
}
// TIMEOUT_ERROR 和 PERMISSION_ERROR 是幽灵错误码，误导开发者

// 反例2：枚举值从未被使用
typedef enum {
    ACTIVE = 0,
    INACTIVE = 1,
    SUSPENDED = 2,  // SUSPENDED 从未被引用
} UserStatus;

int32_t GetStatus(UserStatus* outStatus) {
    if (isActive) {
        *outStatus = ACTIVE;
        return 0;
    }
    *outStatus = INACTIVE;
    return 0;
}
// SUSPENDED 从未被使用，应删除或添加使用场景
