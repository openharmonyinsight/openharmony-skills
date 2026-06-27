// Eval file for rule: 参数按逻辑关系排序
// 正例1：用户操作接口，用户标识在前
function getUserById(userId: string): User { }
function updateUserProfile(userId: string, profile: Profile): void { }
function deleteUser(userId: string): void { }
function assignRole(userId: string, roleId: string): void { }

// 正例2：文件操作接口，文件路径在前
function readFile(filePath: string): string { }
function writeFile(filePath: string, content: string): void { }
function deleteFile(filePath: string): void { }
function copyFile(sourcePath: string, targetPath: string): void { }

// 正例3：网络请求接口，URL在前
function httpRequest(url: string, options: RequestOptions): Response { }
function websocketConnect(url: string, protocols?: string[]): WebSocket { }
function fetchData(endpoint: string, params?: QueryParams): Promise<Data> { }

// 正例4：事件处理接口，事件类型在前
function onEvent(eventType: string, handler: EventHandler): void { }
function offEvent(eventType: string, handler?: EventHandler): void { }
function emitEvent(eventType: string, data?: any): void { }

// 正例5：配置相关接口，配置对象在后
function setConfig(key: string, value: any): void { }
function updateConfig(config: Config): void { }
function applySettings(settings: Settings): void { }

// 正例6：重要性排序，核心参数在前
function createUser(name: string, email: string, options?: CreateUserOptions): User { }
function sendMessage(to: string, content: string, options?: SendMessageOptions): void { }
function connect(host: string, port: number, options?: ConnectOptions): Connection { }
