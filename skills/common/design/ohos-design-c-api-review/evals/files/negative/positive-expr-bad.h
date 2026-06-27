// Eval file for rule: 命名使用肯定表达式
// 反例1：IsNot* 形式的否定表达
/**
 * @brief 检查功能是否未启用
 * 错误：应改为 IsDisabled
 */
bool IsNotEnabled(void);

/**
 * @brief 检查数据是否无效
 * 错误：应改为 IsInvalid
 */
bool IsNotValid(const Data* data);

/**
 * @brief 检查元素是否未显示
 * 错误：应改为 IsHidden
 */
bool IsNotShown(Element* elem);

/**
 * @brief 检查连接是否未打开
 * 错误：应改为 IsClosed
 */
bool IsNotOpen(Connection* conn);

// 反例2：IsUn* 形式可改为更清晰肯定表达的命名
/**
 * @brief 检查资源是否不可用
 * 错误：应改为 IsAvailable，语义更清晰（"是否可用"）
 */
bool IsUnavailable(const Resource* res);

/**
 * @brief 检查地址是否不可达
 * 错误：应改为 IsReachable，语义更清晰
 */
bool IsUnreachable(const Address* addr);

// 反例3：结构体成员使用否定表达
typedef struct {
    bool isNotEnabled;      // 错误：应改为 isDisabled 或 enabled
    bool isNotValid;        // 错误：应改为 isInvalid 或 valid
    bool isNotConnected;    // 错误：应改为 isDisconnected 或 connected
} FeatureState;

// 反例4：宏定义使用否定表达
#define IS_NOT_ENABLED(x)   (!((x)->enabled))   // 错误：应改为 IS_DISABLED
#define IS_NOT_VALID(x)     ((x) == NULL)        // 错误：应改为 IS_INVALID
