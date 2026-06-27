// Eval file for rule: 说明枚举值等价关系
// 正例1：枚举值无重复，每个值都有明确含义
typedef enum {
    /** Touching the system-defined Back button or pressing the Esc key. */
    DIALOG_DISMISS_BACK_PRESS = 0,
    /** Touching the mask. */
    DIALOG_DISMISS_TOUCH_OUTSIDE = 1,
    /** Touching the Close button. */
    DIALOG_DISMISS_CLOSE_BUTTON = 2,
    /** Sliding down. */
    DIALOG_DISMISS_SLIDE_DOWN = 3,
} ArkUI_DismissReason;

// 正例2：等价枚举值说明了等价关系和使用建议
typedef enum {
    /** No error. This is the recommended name for success. */
    ERROR_OK = 0,
    /** Alias of ERROR_OK. Provided for backward compatibility. Prefer ERROR_OK. */
    ERROR_SUCCESS = 0,
    ERROR_FAILED = 1
} ErrorCode;

// 正例3：兼容性保留值说明了原因
typedef enum {
    /** Debug level. */
    LOG_DEBUG = 0,
    /** Alias of LOG_DEBUG. Retained for compatibility with API version 8. Prefer LOG_DEBUG. */
    LOG_TRACE = 0,
    /** Information level. */
    LOG_INFO = 1
} LogLevel;
