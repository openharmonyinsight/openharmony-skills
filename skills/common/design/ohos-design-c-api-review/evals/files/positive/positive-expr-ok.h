// Eval file for rule: 命名使用肯定表达式
// 正例1：使用肯定表达的函数命名
/**
 * @brief 检查连接状态
 * @return true表示已连接，false表示未连接
 */
bool IsConnected(void);

/**
 * @brief 检查功能是否启用
 * @return true表示已启用，false表示未启用
 */
bool IsEnabled(void);

/**
 * @brief 检查资源是否可用
 * @return true表示可用，false表示不可用
 */
bool IsAvailable(void);

/**
 * @brief 检查元素是否隐藏
 * @return true表示隐藏，false表示显示
 */
bool IsHidden(void);

/**
 * @brief 检查连接是否关闭
 * @return true表示已关闭，false表示打开
 */
bool IsClosed(void);

/**
 * @brief 检查数据是否无效
 * @return true表示无效，false表示有效
 */
bool IsInvalid(void);

// 正例2：使用肯定表达的宏定义
#define IS_VALID(x)        ((x) != NULL)     // 清晰：是否有效
#define IS_ENABLED(x)      ((x)->enabled)    // 清晰：是否启用
#define IS_CONNECTED(x)    ((x)->connected)  // 清晰：是否连接

// 正例3：合理的对仗函数命名（无需检出）
/**
 * @brief 订阅事件
 */
int Subscribe(EventCallback callback);

/**
 * @brief 取消订阅事件
 * 说明：与Subscribe形成对仗，无需修改
 */
int Unsubscribe(EventCallback callback);

/**
 * @brief 注册回调
 */
int Register(const char* id, Callback cb);

/**
 * @brief 注销回调
 * 说明：与Register形成对仗，无需修改
 */
int Unregister(const char* id);

// 正例4：业界通用惯例的否定前缀（无需检出）
/**
 * @brief 断开连接
 * 说明：业界通用，与Connect形成对仗
 */
int Disconnect(void);

/**
 * @brief 卸载模块
 * 说明：业界通用，与Mount形成对仗
 */
int Unmount(const char* path);

/**
 * @brief 解锁资源
 * 说明：业界通用，与Lock形成对仗
 */
int Unlock(Resource* res);
