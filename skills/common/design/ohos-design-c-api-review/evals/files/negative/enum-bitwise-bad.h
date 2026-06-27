// Eval file for rule: 枚举型支持位运算的应该给出说明
// 反例1：FLAG枚举型缺少位运算说明
typedef enum {
    PERMISSION_READ = 1,
    PERMISSION_WRITE = 2,
    PERMISSION_EXECUTE = 4,
    PERMISSION_DELETE = 8
} PermissionFlag;
// 错误：枚举值为2的幂次方，明显支持位运算，但缺少说明

// 反例2：使用位运算枚举的函数参数缺少说明
void SetPermission(PermissionFlag flags);
// 错误：参数支持位运算组合，但缺少说明

// 反例3：返回位运算枚举的函数缺少说明
WindowFlag GetWindowFlags(void);
// 错误：返回值可能为多个枚举值的组合，但缺少说明

// 反例4：属性使用位运算枚举但缺少说明
typedef struct {
    PermissionFlag permissions;  // 错误：属性支持位运算组合，但缺少说明
} FileOptionsBad;

// 反例5：窗口标志枚举缺少说明
typedef enum {
    WINDOW_FULLSCREEN = 1,
    WINDOW_RESIZABLE = 2,
    WINDOW_ALWAYS_ON_TOP = 4,
    WINDOW_TRANSPARENT = 8
} WindowFlag;
// 错误：枚举值明显支持位运算，但缺少说明

// 反例6：位掩码宏缺少说明
#define OPTION_A 0x01
#define OPTION_B 0x02
#define OPTION_C 0x04
// 错误：位掩码定义缺少说明其支持位运算组合
