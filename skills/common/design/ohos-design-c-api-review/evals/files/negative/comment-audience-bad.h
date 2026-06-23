// Eval file for rule: 注释的核心读者是应用开发者
// 反例1：描述内部实现细节，开发者不需要知道
/**
 * @brief Creates a file by calling the VFS layer and allocating an inode.
 *
 * This function invokes vfs_create() which then calls alloc_inode() to get a new
 * inode structure. The dentry cache is updated and the file is added to the
 * global file table. The inode mutex is held during this operation.
 * 问题：开发者不关心 VFS、inode、dentry 等内部实现细节
 *
 * @param path The file path.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int CreateFile(const char* path);

// 反例2：使用晦涩的技术术语，没有解释业务含义
/**
 * @brief Triggers an async IPC dispatch to the system server.
 *
 * The Binder transaction is marshaled with PARCEL_ENABLE_REFLECTION flag.
 * The transaction code is 0x1001 and the interface descriptor is obtained
 * from the service manager. The callback runs on the HandlerThread looper.
 * 问题：只描述了IPC机制，没说明这个API实际是做什么的
 *
 * @param callback The callback function pointer.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int RegisterCallback(void (*callback)(void));

// 反例3：参数描述过于简单，没有说明取值范围和含义
/**
 * @brief Sets the config.
 *
 * @param config The config.
 * @param size The size.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int SetConfig(const void* config, size_t size);
// 问题：没有说明 config 是什么结构，size 应该传什么值

// 反例4：使用缩写但不解释
/**
 * @brief Init the dev.
 *
 * @param id The dev id.
 * @param flags The flags.
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int InitDev(int id, int flags);
// 问题：dev 是什么设备？flags 有哪些取值？

// 反例5：返回值描述不清晰
/**
 * @brief Performs the operation.
 *
 * @param data The data.
 * @return Returns a value.
 * @retval >=0 Good
 * @retval <0 Bad
 * 问题：没有说明具体的返回值含义和错误码
 * @since 7
 */
int DoOperation(const char* data);

// 反例6：只列出错误码但不说明触发条件
/**
 * @brief Sends the data.
 *
 * @param data The data buffer.
 * @param size The data size.
 * @return Returns 0 on success, or a negative error code on failure.
 * @retval 0 Success
 * @retval -1 Error
 * @retval -2 Error
 * @retval -3 Error
 * 问题：所有错误都是 "Error"，没有说明具体原因
 * @since 7
 */
int SendData(const void* data, size_t size);

// 反例7：使用内部变量名和模块名
/**
 * @brief Calls g_service_manager->RegisterModule() with MOD_NETWORK.
 *
 * The module_info_t structure is populated with default values and then
 * passed to the registration function. The g_network_state variable is
 * set to STATE_INITIALIZED after successful registration.
 * 问题：开发者不关心 g_service_manager、MOD_NETWORK 等内部变量名
 *
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int RegisterNetworkModule(void);

// 反例8：使用过于抽象的描述，没有实际信息
/**
 * @brief Processes the thing with the stuff.
 *
 * This function does the processing. It processes the thing and returns
 * the result of the processing. The processing is done asynchronously.
 * 问题：完全没有说明这个函数是做什么的
 *
 * @param thing The thing to process.
 * @return Returns the processing result.
 * @since 7
 */
int ProcessThing(const void* thing);

// 反例9：使用"TODO"、"FIXME"等开发标记
/**
 * @brief Connects to the server.
 *
 * TODO: Implement reconnection logic.
 * FIXME: This may crash if the server is restarted.
 * NOTE: The timeout is hardcoded to 30 seconds.
 * 问题：TODO/FIXME 是开发笔记，不应该出现在公开的API文档中
 *
 * @return Returns 0 on success, or a negative error code on failure.
 * @since 7
 */
int ConnectToServer(void);

// 反例10：复制粘贴导致的注释不匹配
/**
 * @brief Reads a file from the file system.
 *
 * @param path The path of the directory to create.  <-- 错误：这是读文件不是创建目录
 * @param buffer The buffer to write the data to.  <-- 方向描述错误
 * @return Returns the number of bytes written.  <-- 应该是读取的字节数
 * @since 7
 */
int ReadFile(const char* path, char* buffer);
