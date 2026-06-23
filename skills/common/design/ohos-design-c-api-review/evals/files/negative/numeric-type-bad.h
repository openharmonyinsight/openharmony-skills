// Eval file for rule: 合理使用数值类型
// 反例1：使用字符串表示年龄
typedef struct {
    char age[16];  // 错误：年龄需要比较和计算，应使用 int
} PersonBad;

// 反例2：使用字符串表示金额
typedef struct {
    char price[32];  // 错误：价格需要计算，应使用 double
} ProductBad;

// 反例3：使用字符串表示尺寸
typedef struct {
    char width[16];   // 错误：宽度需要布局计算，应使用 int
    char height[16];  // 错误：高度需要布局计算，应使用 int
} ViewBad;

// 反例4：函数参数使用字符串表示数值
double CalculateTotalBad(const char* price, const char* count);
// 错误：数值参数应使用 double 和 int 类型

// 反例5：使用字符串表示索引
Item* GetItemByIndexBad(const char* index);
// 错误：索引应使用 int 类型

// 反例6：使用字符串表示大小
void* AllocateBufferBad(const char* size);
// 错误：大小应使用 size_t 类型
