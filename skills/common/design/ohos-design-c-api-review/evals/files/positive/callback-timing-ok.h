// Eval file for rule: 回调类接口说明清楚触发时机
// 正例1：说明回调触发时机
/**
 * The callback is triggered when the ratio of the component's visible area to its total area is greater than or
 * equal to the threshold.
 */
int32_t OnVisibleAreaChange(void (*callback)(float ratio));

// 正例2：说明动画回调触发时机
/**
 * @brief Defines the event callback function triggered when the animation starts to play.
 */
int32_t OnAnimationStart(void (*callback)(void));

// 正例3：说明回调触发时机和状态
/**
 * This callback event is triggered whenever a new image is received.
 */
int32_t OnImageArrived(void (*callback)(const ImageData* image));

// 正例4：说明生命周期回调
/**
 * @brief Defines a lifecycle callback for keyEvent. If the callback is triggered, keyEvent will be destroyed.
 */
int32_t OnKeyEvent(void (*callback)(KeyEvent* event));

// 正例5：说明状态变化的具体含义
/**
 * @brief Registers a callback that is triggered when the connection state changes.
 * The callback is invoked after the connection is fully established or after the connection is completely closed.
 * @param callback Connection state change callback.
 */
int32_t OnConnectionStateChanged(void (*callback)(ConnectionState state));
