// Eval file for rule: 参数规格保持一致
// 反例1：同一文件内参数命名不一致
TaskResult* GetStartupTaskResult(const char* task);
bool IsStartupTaskInitialized(const char* startupTask);
// 错误：同一概念使用了不同的参数名 task 和 startupTask

// 反例2：时间参数单位不一致
void SetTimeout(int duration);   // duration单位为毫秒
void SetInterval(int interval);  // interval单位为秒
// 错误：时间参数单位不一致，容易导致开发者使用错误

// 反例3：ID参数命名不一致
User* GetUserById(const char* userId);
void DeleteUser(const char* id);
void UpdateUser(const char* uid, const void* data, size_t dataLen);
// 错误：用户ID使用了不同的命名 userId、id、uid

// 反例4：路径参数命名不一致
Byte* ReadFileBad(const char* filePath, size_t* dataLen);
void WriteFileBad(const char* path, const Byte* data, size_t dataLen);
void DeleteFileBad(const char* file);
// 错误：文件路径使用了不同的命名 filePath、path、file

// 反例5：配置结构体规格不一致
typedef struct {
    int width;
    int height;
    const char* title;
} CreateWindowConfig;

typedef struct {
    int w;
    int h;
    const char* name;
} UpdateWindowConfig;
// 错误：同一概念的配置结构体使用了不同的属性名
