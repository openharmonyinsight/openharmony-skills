// Eval file for rule: 数据类型的名称应该是名词
// 正例1：类名使用名词
class UserManager { }
class MessageService { }
class DataService { }
class ConnectionPool { }
class EventDispatcher { }

// 正例2：接口名使用名词
interface UserInfo { }
interface AppConfig { }
interface NetworkConfig { }
interface DatabaseOptions { }
interface ConnectionParams { }

// 正例3：枚举名使用名词
enum UserType { }
enum MessageStatus { }
enum ConnectionState { }
enum LogLevel { }
enum Direction { }

// 正例4：类型别名使用名词
type UserId = string;
type UserName = string;
type UserCallback = (user: User) => void;
type EventHandler = (event: Event) => void;

// 正例5：复合名词
interface AnimationOptions { }
interface ConfigurationParams { }
interface EventHandlerRegistry { }
interface ServiceProvider { }
