// Eval file for rule: 函数入参合理使用参数封装
// 反例1：参数数量超过5个，未进行封装
/**
 * @brief 创建连接
 * 错误：参数数量为6个，超过5个，建议封装为ConnectionConfig结构体
 */
int CreateConnection(const char* host, int port, int timeout,
                     int retry_count, bool enable_ssl, const char* cert_path);

// 反例2：参数数量过多，难以维护
/**
 * @brief 绘制矩形
 * 错误：参数数量为9个，远超5个，建议封装为RectangleOptions结构体
 */
int DrawRectangleEx(int x, int y, int width, int height,
                    const char* fill_color, const char* stroke_color,
                    int stroke_width, float opacity, int border_radius);

// 反例3：相关参数未分组封装
/**
 * @brief 移动窗口
 * 错误：参数数量为7个，x/y和width/height可以分别封装为Position和Size结构体
 */
int MoveWindow(const char* window_id, int x, int y,
               int width, int height, bool animate, int duration);

// 反例4：配置参数散乱，不易扩展
/**
 * @brief 初始化
 * 错误：参数数量为7个，配置类参数建议封装为InitConfig结构体
 */
int Init(const char* app_id, const char* app_secret, const char* server_url,
         const char* log_level, bool enable_cache, size_t cache_size, int timeout);

// 反例5：网络请求参数过多
/**
 * @brief 发送HTTP请求
 * 错误：参数数量为8个，建议封装为RequestConfig结构体
 */
int SendRequest(const char* url, const char* method,
                const char* headers, const char* body,
                int timeout, int retry_count,
                bool verify_ssl, Response* response);
