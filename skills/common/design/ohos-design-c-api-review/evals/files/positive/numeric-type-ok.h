// Eval file for rule: 合理使用数值类型
// 正例1：使用数值类型表示年龄
typedef struct {
    int age;  // 年龄，用于比较和计算
} Person;

// 正例2：使用数值类型表示金额
typedef struct {
    double price;     // 价格，用于计算
    int quantity;     // 数量，用于计算
} Product;

// 正例3：使用数值类型表示尺寸
typedef struct {
    int width;   // 宽度，用于布局计算
    int height;  // 高度，用于布局计算
} View;

// 正例4：函数参数使用数值类型
/**
 * @brief 计算总价
 * @param price 单价
 * @param count 数量
 * @return 总价
 */
double CalculateTotal(double price, int count);

// 正例5：使用数值类型表示索引
Item* GetItemByIndex(int index);

// 正例6：使用数值类型表示百分比
typedef struct {
    int percent;  // 0-100的数值
} Progress;

// 正例7：使用size_t表示大小
void* AllocateBuffer(size_t size);

// 正例8：使用uint32_t等固定宽度类型
uint32_t CalculateChecksum(const uint8_t* data, size_t len);
