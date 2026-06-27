// Eval file for rule: 参数规格保持一致
// 正例1：同一文件内参数命名一致
TaskResult* GetStartupTaskResult(const char* startupTask);
bool IsStartupTaskInitialized(const char* startupTask);
void RemoveStartupTask(const char* startupTask);
// 正确：所有函数使用相同的参数名 startupTask 表示同一概念

// 正例2：配置结构体规格一致
typedef struct {
    int width;
    int height;
    const char* title;
} WindowConfig;

Window* CreateWindow(const WindowConfig* config);
void UpdateWindow(int windowId, const WindowConfig* config);
// 正确：同一配置结构体在不同API中保持一致

// 正例3：ID参数命名一致
User* GetUserById(const char* userId);
void DeleteUser(const char* userId);
void UpdateUser(const char* userId, const void* data, size_t dataLen);
// 正确：用户ID统一命名为 userId

// 正例4：路径参数规格一致
Byte* ReadFile(const char* filePath, size_t* dataLen);
void WriteFile(const char* filePath, const Byte* data, size_t dataLen);
void DeleteFile(const char* filePath);
bool FileExists(const char* filePath);
// 正确：文件路径统一命名为 filePath，类型统一为 const char*
