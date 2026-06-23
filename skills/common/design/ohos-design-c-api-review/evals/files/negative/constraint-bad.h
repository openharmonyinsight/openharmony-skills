// Eval file for rule: 约束限制合理
// 反例1：违背用户直觉/行业惯例 - 日志消息不允许包含换行符
/**
 * @brief Write a log message.
 *
 * @param message Log message. Cannot contain newline characters (\n).
 *   Newline characters will cause undefined behavior.
 * @param level Log level.
 * @since 10
 */
void WriteLog(const char* message, LogLevel level);

// 反例2：无明确技术必要性 - 回调函数必须注册在主线程，但接口本身是异步操作
/**
 * @brief Register a callback for asynchronous data processing.
 *
 * Note: The callback function must be registered on the main thread.
 * Registration from a worker thread will result in the callback not being invoked.
 * This is due to the internal event loop architecture which binds callbacks to the
 * thread-local event queue that is only processed on the main thread's run loop,
 * combined with the cross-thread mutex serialization mechanism.
 *
 * @param callback Data processing callback.
 * @return 0 on success, negative error code on failure.
 * @since 10
 */
int32_t RegisterDataCallback(DataCallback callback);

// 反例3：约束条件过多 - 连接接口有过多的前置约束条件
/**
 * @brief Connect to a remote service.
 *
 * Prerequisites:
 * 1. Network must be in Wi-Fi mode (cellular is not supported).
 * 2. Battery level must be above 20%.
 * 3. Device storage must have at least 100MB free space.
 * 4. No other service connection is active.
 * 5. System thermal level must be below WARNING.
 * 6. The app must be in foreground state.
 *
 * @param serviceId Remote service identifier.
 * @param options Connection options.
 * @return Connection handle.
 * @since 10
 */
ConnectionHandle Connect(const char* serviceId, const ConnectOptions* options);

// 反例4：限制合理使用场景 - 数据缓冲区最大只允许4KB，但实际场景经常需要传输大块数据
/**
 * @brief Write data to the output stream.
 *
 * @param data Data buffer to write.
 * @param size Size of data in bytes. Must not exceed 4096 (4KB).
 *   Data exceeding this limit will be truncated.
 * @return Number of bytes actually written.
 * @since 10
 */
int32_t WriteData(const uint8_t* data, size_t size);

// 反例5：违背用户直觉 - 线程池最大线程数不能超过CPU核心数
/**
 * @brief Create a thread pool.
 *
 * @param maxThreads Maximum number of threads. Cannot exceed the number of CPU cores.
 * @return Thread pool handle.
 * @since 11
 */
ThreadPoolHandle CreateThreadPool(uint32_t maxThreads);

// 反例6：无明确技术必要性 - 枚举值必须从特定数字开始
/**
 * @brief Register a custom event type.
 *
 * @param eventId Event type ID. Must start from 10000 and be a multiple of 100.
 *   This is required by the internal event dispatching hash table implementation.
 * @param handler Event handler function.
 * @return 0 on success, negative error code on failure.
 * @since 10
 */
int32_t RegisterEvent(int32_t eventId, EventHandler handler);

// 反例7：限制合理使用场景 - 定时器精度被强制限制在秒级
/**
 * @brief Start a periodic timer.
 *
 * @param intervalMs Timer interval in milliseconds. Must be a multiple of 1000 (1 second).
 *   Sub-second intervals are not supported.
 * @param callback Timer callback.
 * @return Timer ID on success, negative error code on failure.
 * @since 10
 */
int32_t StartTimer(uint32_t intervalMs, TimerCallback callback);
