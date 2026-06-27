// Eval file for rule: 模块划分合理
// 正例1：用户管理模块（职责单一）
// user-manager.ts
class UserManager {
  createUser(name: string, email: string): User { }
  getUserById(id: string): User { }
  updateUser(id: string, data: Partial<User>): User { }
  deleteUser(id: string): void { }
}

// 正例2：消息服务模块（职责单一）
// message-service.ts
class MessageService {
  sendMessage(to: string, content: string): void { }
  getMessages(userId: string): Message[] { }
  markAsRead(messageId: string): void { }
  deleteMessage(messageId: string): void { }
}

// 正例3：数据库访问模块（高内聚）
// database-access.ts
class DatabaseAccess {
  connect(config: DatabaseConfig): void { }
  disconnect(): void { }
  query<T>(sql: string, params?: any[]): T[] { }
  execute(sql: string, params?: any[]): void { }
  transaction<T>(callback: () => T): T { }
}

// 正例4：网络请求模块（高内聚）
// http-client.ts
class HttpClient {
  get<T>(url: string, options?: RequestOptions): Promise<T> { }
  post<T>(url: string, body: any, options?: RequestOptions): Promise<T> { }
  put<T>(url: string, body: any, options?: RequestOptions): Promise<T> { }
  delete<T>(url: string, options?: RequestOptions): Promise<T> { }
}

// 正例5：配置管理模块（职责单一）
// config-manager.ts
class ConfigManager {
  loadConfig(path: string): Config { }
  saveConfig(config: Config, path: string): void { }
  get(key: string): any { }
  set(key: string, value: any): void { }
}

// 正例6：事件处理模块（高内聚）
// event-bus.ts
class EventBus {
  on(eventType: string, handler: EventHandler): void { }
  off(eventType: string, handler?: EventHandler): void { }
  emit(eventType: string, data?: any): void { }
  once(eventType: string, handler: EventHandler): void { }
}
