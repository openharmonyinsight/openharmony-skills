// Eval file for rule: 说明和其他API配合制约关系
// 反例1：创建实例未说明释放资源
/**
 * @return Returns the pointer to the device manager.
 */
DeviceManager* CreateDeviceManager(void);

// 反例2：申请资源未说明释放
/**
 * @param resourceId Resource ID.
 * @return 0 on success.
 */
int32_t RequestResource(int32_t resourceId);

// 反例3：开始操作未说明结束
/**
 * Starts recording.
 * @return 0 on success.
 */
int32_t StartRecording(void);

// 反例4：创建连接未说明关闭
/**
 * @param url Server URL.
 * @return Connection handle.
 */
ConnectionHandle CreateConnection(const char* url);

// 反例5：分配缓冲区未说明释放
/**
 * @param size Buffer size.
 * @return Buffer pointer.
 */
void* AllocateBuffer(size_t size);
