// Eval file for rule: 禁止创建空interface
// 正例1：interface定义了属性
/**
 * 用户信息接口
 */
interface UserInfo {
  userId: string;
  userName: string;
  age: number;
}

// 正例2：interface定义了方法
/**
 * 数据处理接口
 */
interface DataProcessor {
  process(data: string): void;
  validate(): boolean;
}

// 正例3：interface同时定义了属性和方法
/**
 * 服务配置接口
 */
interface ServiceConfig {
  host: string;
  port: number;

  connect(): Promise<void>;
  disconnect(): void;
}

// 正例4：interface定义了可选属性
/**
 * 分页查询参数
 */
interface PageQuery {
  page?: number;
  pageSize?: number;
  keyword?: string;
}

// 正例5：interface定义了只读属性
/**
 * 配置项接口
 */
interface ConfigItem {
  readonly key: string;
  readonly value: string;
}

// 正例6：interface定义了索引签名
/**
 * 动态属性接口
 */
interface DynamicObject {
  [key: string]: any;
}

// 正例7：interface定义了函数类型属性
/**
 * 事件处理器接口
 */
interface EventHandler {
  onClick: (event: Event) => void;
  onHover: (event: Event) => void;
}

// 正例8：interface继承并添加了新成员
/**
 * 扩展用户接口
 */
interface ExtendedUser extends UserInfo {
  avatar: string;
  isActive: boolean;
}

// 正例9：interface定义了构造签名
/**
 * 可构造接口
 */
interface Constructor {
  new (name: string): any;
}

// 正例10：有继承可以不添加任何新成员的interface
/**
 * 有继承没有任何属性和方法
 */
interface NoNewMembers extends UserInfo {
}
