// Eval file for rule: 模块划分合理
// 反例1：模块职责不单一
// user-manager.ts
class UserManager {
  // 用户管理
  createUser(name: string, email: string): User { }
  getUserById(id: string): User { }

  // 消息处理（不应该在这个模块）
  sendMessage(to: string, content: string): void { }
  getMessages(userId: string): Message[] { }

  // 文件操作（不应该在这个模块）
  uploadFile(file: File): string { }
  downloadFile(url: string): File { }
}

// 反例2：模块耦合度高
// database-service.ts
class DatabaseService {
  // 数据库操作
  connect(): void { }
  query(sql: string): any[] { }

  // 直接依赖HTTP客户端（高耦合）
  private httpClient: HttpClient;

  // 直接依赖日志服务（高耦合）
  private logger: Logger;

  // 直接依赖缓存服务（高耦合）
  private cache: CacheService;
}

// 反例3：模块功能过于分散
// utils.ts
class Utils {
  // 用户相关
  createUser(): User { }

  // 文件相关
  readFile(): string { }

  // 网络相关
  httpRequest(): Response { }

  // 日志相关
  log(): void { }

  // 配置相关
  getConfig(): Config { }
}

// 反例4：模块内聚度低
// data-handler.ts
class DataHandler {
  // 这些方法之间没有逻辑关联
  parseJSON(json: string): object { }
  encryptData(data: string): string { }
  sendEmail(to: string, subject: string, body: string): void { }
  validateUser(user: User): boolean { }
  generatePDF(content: string): Buffer { }
}

// 反例5：模块边界不清晰
// service.ts
class Service {
  // 用户服务功能
  getUser(): User { }

  // 订单服务功能（应在独立模块）
  createOrder(): Order { }

  // 支付服务功能（应在独立模块）
  processPayment(): Payment { }

  // 物流服务功能（应在独立模块）
  trackPackage(): TrackingInfo { }
}

// 反例6：跨层调用
// user-manager.ts
class UserManager {
  createUser(name: string, email: string): User {
    // 直接操作数据库（应通过数据访问层）
    const db = new DatabaseAccess();
    db.query('INSERT INTO users...');

    // 直接发送HTTP请求（应通过服务层）
    const http = new HttpClient();
    http.post('http://api.example.com/notify', {...});
  }
}
