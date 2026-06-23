// Eval file for rule: 回调类接口说明清楚触发时机
// 反例1：未说明触发时机
/**
 * @param callback Page change callback.
 */
int32_t OnPageChanged(void (*callback)(int32_t pageId));

// 反例2：状态含义不明确
/**
 * @param callback State change callback.
 */
int32_t OnStateChanged(void (*callback)(int32_t state));

// 反例3：未说明执行时机（执行前/中/后）
/**
 * @param callback Click callback.
 */
int32_t OnClick(void (*callback)(void));

// 反例4：回调触发条件模糊
/**
 * @param callback Data callback.
 */
int32_t OnDataReceived(void (*callback)(const uint8_t* data, size_t len));

// 反例5：未说明回调的生命周期管理
/**
 * @param callback Event handler.
 */
int32_t RegisterEventHandler(void (*callback)(Event* event));
