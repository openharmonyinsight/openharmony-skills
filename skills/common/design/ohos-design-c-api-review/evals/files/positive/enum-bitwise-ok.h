// Eval file for rule: 枚举型支持位运算的应该给出说明
// 正例1：FLAG枚举型带有位运算说明
/**
 * @brief 权限标志位枚举。
 * 该枚举支持位运算，可通过按位或(|)组合多个权限。
 * @example
 * int permissions = PERMISSION_READ | PERMISSION_WRITE;
 */
typedef enum {
    PERMISSION_READ = 1,       // 读取权限
    PERMISSION_WRITE = 2,      // 写入权限
    PERMISSION_EXECUTE = 4,    // 执行权限
    PERMISSION_DELETE = 8      // 删除权限
} PermissionFlag;

// 正例2：使用位运算枚举的函数参数带有说明
/**
 * @brief 设置文件权限。
 * @param flags 权限标志位，支持通过按位或组合多个权限，
 *              如 PERMISSION_READ | PERMISSION_WRITE
 */
void SetPermission(PermissionFlag flags);

// 正例3：窗口标志枚举
/**
 * @brief 窗口标志枚举。
 * 该枚举支持位运算，可通过按位或(|)组合多个标志。
 * @example
 * int flags = WINDOW_FULLSCREEN | WINDOW_RESIZABLE;
 */
typedef enum {
    WINDOW_FULLSCREEN = 1,
    WINDOW_RESIZABLE = 2,
    WINDOW_ALWAYS_ON_TOP = 4,
    WINDOW_TRANSPARENT = 8
} WindowFlag;

// 正例4：返回位运算枚举的函数带有说明
/**
 * @brief 获取当前窗口标志。
 * @return 窗口标志位，可能为多个标志的按位或组合
 */
WindowFlag GetWindowFlags(void);

// 正例5：属性使用位运算枚举带有说明
typedef struct {
    /**
     * 文件权限标志，支持通过按位或组合多个权限
     */
    PermissionFlag permissions;
} FileOptions;

// 正例6：枚举值虽符合2的幂次方，但最大枚举值<4，且不存在多个枚举值"逻辑或"的组合关系，无需添加用法说明
/**
 * Describes types of trace collection threads, including the main thread and all threads.
 */
typedef enum {
    Default = 0,
    MAIN_THREAD = 1,
    ALL_THREADS = 2
} TraceFlag;
