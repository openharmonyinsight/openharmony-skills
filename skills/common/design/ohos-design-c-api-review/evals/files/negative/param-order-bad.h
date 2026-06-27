// Eval file for rule: 参数按逻辑关系排序
// 反例1：用户操作接口，用户标识不在前
int GetUserById(const GetUserOptions* options, const char* userId, User* outUser);  // userId应在最前
int UpdateUserProfile(const Profile* profile, const char* userId);  // userId应在最前
int DeleteUser(const DeleteOptions* options, const char* userId);  // userId应在最前

// 反例2：文件操作接口，文件路径不在前
int ReadFile(const char* encoding, const char* filePath, char* buffer, size_t bufferSize);  // filePath应在最前
int WriteFile(const char* content, size_t contentLen, const char* filePath);  // filePath应在最前
int DeleteFile(bool force, const char* filePath);  // filePath应在最前

// 反例3：网络请求接口，URL不在前
int HttpRequest(const RequestOptions* options, const char* url, Response* outResponse);  // url应在最前
int WebsocketConnect(const char** protocols, size_t protocolCount, const char* url);  // url应在最前
int FetchData(const QueryParams* params, const char* endpoint, Data* outData);  // endpoint应在最前

// 反例4：事件处理接口，事件类型不在前
int OnEvent(EventHandler handler, const char* eventType);  // eventType应在最前
int OffEvent(EventHandler handler, const char* eventType);  // eventType应在最前
int EmitEvent(const void* data, size_t dataLen, const char* eventType);  // eventType应在最前

// 反例5：重要性排序错误
int CreateUser(const CreateUserOptions* options, const char* name, const char* email);  // name和email应在前
int SendMessage(const SendMessageOptions* options, const char* to, const char* content);  // to和content应在前
int Connect(const ConnectOptions* options, const char* host, int port);  // host和port应在前
