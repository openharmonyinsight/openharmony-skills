// Eval file for rule: 说明枚举值等价关系
// 反例1：等价枚举值未说明关系
typedef enum {
    DISMISS_BACK_PRESS = 0,
    DISMISS_TOUCH_OUTSIDE = 1,
    DISMISS_CLOSE_BUTTON = 2,
    DISMISS_SLIDE_DOWN = 3,
    DISMISS_TOUCH_OUTSIDE2 = 2  // 未说明与DISMISS_CLOSE_BUTTON等价
} DialogDismissReason;

// 反例2：等价枚举值未说明使用建议
typedef enum {
    ERROR_NONE = 0,
    ERROR_SUCCESS = 0,  // 未说明推荐使用哪个
    ERROR_FAILED = 1
} ErrorCode;

// 反例3：兼容性保留值未说明原因
typedef enum {
    LOG_DEBUG = 0,
    LOG_TRACE = 0,  // 未说明是为兼容旧版本保留
    LOG_INFO = 1
} LogLevel;

// 反例4：多个等价值无任何说明
typedef enum {
    STATE_IDLE = 0,
    STATE_READY = 1,
    STATE_INIT = 0,      // 未说明与STATE_IDLE等价
    STATE_PREPARED = 1,   // 未说明与STATE_READY等价
    STATE_RUNNING = 2
} SystemState;
