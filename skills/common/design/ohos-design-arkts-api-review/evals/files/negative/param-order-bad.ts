// Eval file for rule: 参数按逻辑关系排序
// 反例1：用户操作接口，用户标识不在前
function getUserById(options: GetUserOptions, userId: string): User { }  // userId应在最前
function updateUserProfile(profile: Profile, userId: string): void { }  // userId应在最前
function deleteUser(options: DeleteOptions, userId: string): void { }  // userId应在最前

// 反例2：文件操作接口，文件路径不在前
function readFile(encoding: string, filePath: string): string { }  // filePath应在最前
function writeFile(content: string, filePath: string): void { }  // filePath应在最前
function deleteFile(force: boolean, filePath: string): void { }  // filePath应在最前

// 反例3：网络请求接口，URL不在前
function httpRequest(options: RequestOptions, url: string): Response { }  // url应在最前
function websocketConnect(protocols: string[], url: string): WebSocket { }  // url应在最前
function fetchData(params: QueryParams, endpoint: string): Promise<Data> { }  // endpoint应在最前

// 反例4：事件处理接口，事件类型不在前
function onEvent(handler: EventHandler, eventType: string): void { }  // eventType应在最前
function offEvent(handler: EventHandler, eventType: string): void { }  // eventType应在最前
function emitEvent(data: any, eventType: string): void { }  // eventType应在最前

// 反例5：重要性排序错误
function createUser(options: CreateUserOptions, name: string, email: string): User { }  // name和email应在前
function sendMessage(options: SendMessageOptions, to: string, content: string): void { }  // to和content应在前
function connect(options: ConnectOptions, host: string, port: number): Connection { }  // host和port应在前

// 反例6：可选参数在前，必选参数在后
function createUser(name?: string, email: string): User { }  // 可选参数应在后
function sendMessage(to: string, options?: SendMessageOptions, content: string): void { }  // content是必选，应在前
