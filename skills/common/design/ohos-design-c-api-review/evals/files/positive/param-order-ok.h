// Eval file for rule: 参数按逻辑关系排序
// 正例1：用户操作接口，用户标识在前
int GetUserById(const char* userId, User* outUser);
int UpdateUserProfile(const char* userId, const Profile* profile);
int DeleteUser(const char* userId);
int AssignRole(const char* userId, const char* roleId);

// 正例2：文件操作接口，文件路径在前
int ReadFile(const char* filePath, char* buffer, size_t bufferSize);
int WriteFile(const char* filePath, const char* content, size_t contentLen);
int DeleteFile(const char* filePath);
int CopyFile(const char* sourcePath, const char* targetPath);

// 正例3：网络请求接口，URL在前
int HttpRequest(const char* url, const RequestOptions* options, Response* outResponse);
int WebsocketConnect(const char* url, const char** protocols, size_t protocolCount);
int FetchData(const char* endpoint, const QueryParams* params, Data* outData);

// 正例4：事件处理接口，事件类型在前
int OnEvent(const char* eventType, EventHandler handler);
int OffEvent(const char* eventType, EventHandler handler);
int EmitEvent(const char* eventType, const void* data, size_t dataLen);

// 正例5：配置相关接口，配置对象在后
int SetConfig(const char* key, const void* value, size_t valueLen);
int UpdateConfig(const Config* config);
int ApplySettings(const Settings* settings);

// 正例6：重要性排序，核心参数在前
int CreateUser(const char* name, const char* email, const CreateUserOptions* options);
int SendMessage(const char* to, const char* content, const SendMessageOptions* options);
int Connect(const char* host, int port, const ConnectOptions* options);
