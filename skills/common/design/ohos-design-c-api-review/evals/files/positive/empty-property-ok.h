// Eval file for rule: 禁止创建空属性接口
// 正例1：结构体所有成员有明确的类型定义和实际用途
typedef struct {
    const char* userId;     // 用户唯一标识，用于业务逻辑
    const char* userName;   // 用户名称，显示用途
    const char* avatarUrl;  // 可选属性，用户可能未设置头像
} UserInfo;

// 正例2：支付结果所有字段类型明确，可选字段有合理的业务场景
typedef struct {
    const char* orderId;    // 订单ID
    double amount;          // 支付金额
    int64_t timestamp;      // 支付时间戳
    const char* promotionId; // 可选，关联的促销活动ID（可为NULL）
} PaymentResult;

// 正例3：配置选项所有可选字段都有明确的类型和合理的默认行为
typedef struct {
    int timeout;      // 超时时间，有默认值
    int retries;      // 重试次数，有默认值
    bool enableCache; // 是否启用缓存，有默认值
} ConfigOptions;

// 正例4：响应数据有明确的类型定义
typedef struct {
    int code;            // 响应状态码
    const char* message; // 响应消息
    UserData data;       // 响应数据，有明确的类型定义
} ApiResponse;

// 正例5：联合类型属性有明确的用途和类型定义
typedef struct {
    int status;          // 状态：0=success, 1=failed, 2=pending
    ResultData* result;  // 结果数据，根据状态有不同含义
} ResponseData;
