// Eval file for rule: 枚举型支持位运算的应该给出说明
// 正例1：FLAG枚举型带有位运算说明
/**
 * 权限标志位枚举。
 * 该枚举支持位运算，可通过按位或(|)组合多个权限。
 * @example
 * const permissions = PermissionFlag.READ | PermissionFlag.WRITE;
 */
enum PermissionFlag {
  READ = 1,       // 读取权限
  WRITE = 2,      // 写入权限
  EXECUTE = 4,    // 执行权限
  DELETE = 8      // 删除权限
}

// 正例2：使用位运算枚举的函数参数带有说明
/**
 * 设置文件权限。
 * @param flags 权限标志位，支持通过按位或组合多个权限，如 PermissionFlag.READ | PermissionFlag.WRITE
 */
function setPermission(flags: PermissionFlag): void { }

// 正例3：返回位运算枚举的函数带有说明
/**
 * 获取文件权限。
 * @returns 权限标志位，可能为多个标志的按位或组合
 */
function getPermissionFlags(): PermissionFlag { }

// 正例4：枚举值虽符合2的幂次方，但是最大枚举值＜4，且不存在多个枚举值"逻辑或"的组合关系，因而无需添加用法说明
/**
 * Describes types of trace collection threads, including the main thread and all threads.
 */
enum TraceFlag {
    Default = 0,
    MAIN_THREAD = 1,
    ALL_THREADS = 2
}
