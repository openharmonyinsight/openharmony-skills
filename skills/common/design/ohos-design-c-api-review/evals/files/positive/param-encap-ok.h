// Eval file for rule: 函数入参合理使用参数封装
// 正例1：参数数量不超过5个，无需封装
/**
 * @brief 连接服务器
 */
int Connect(const char* host, int port, int timeout);

// 正例2：使用结构体封装多个相关参数
typedef struct {
    const char* host;
    int port;
    int timeout;
    int retry_count;
    bool enable_ssl;
    const char* cert_path;
} ConnectionConfig;

/**
 * @brief 使用配置结构体创建连接
 */
int ConnectWithConfig(const ConnectionConfig* config);

// 正例3：使用Options结构体封装可选参数
typedef struct {
    int width;
    int height;
    const char* background_color;
    int border_radius;
    float opacity;
    int z_index;
} ViewOptions;

/**
 * @brief 创建视图
 */
View* CreateView(const ViewOptions* options);

// 正例4：将相关参数分组封装
typedef struct {
    int x;
    int y;
} Position;

typedef struct {
    int width;
    int height;
} Size;

typedef struct {
    const char* fill_color;
    const char* stroke_color;
    int stroke_width;
} Style;

/**
 * @brief 绘制矩形
 * 参数分组封装后，参数数量为3个，符合规范
 */
int DrawRectangle(const Position* pos, const Size* size, const Style* style);

// 正例5：初始化配置结构体
typedef struct {
    const char* app_id;
    const char* app_secret;
    const char* server_url;
    const char* log_level;
    bool enable_cache;
    size_t cache_size;
    int timeout;
} InitConfig;

/**
 * @brief 初始化SDK
 */
int Initialize(const InitConfig* config);

// 正例6：查询参数封装
typedef struct {
    const char* table;
    const char** fields;
    size_t field_count;
    const char* where_clause;
    const char* order_by;
    int limit;
    int offset;
    const char* group_by;
} QueryOptions;

/**
 * @brief 查询数据
 */
int QueryData(const QueryOptions* options, Result* result);
