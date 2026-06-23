// Eval file for rule: 数据类型的名称应该是名词
// 反例1：类名使用动词
class ManageUser { }  // 应改为UserManager
class SendMessage { }  // 应改为MessageService或MessageSender
class ConnectToServer { }  // 应改为ServerConnector

// 反例2：接口名使用动词
interface GetUserInfo { }  // 应改为UserInfo
interface SendData { }  // 应改为DataSender或DataTransmitter
interface HandleEvent { }  // 应改为EventHandler

// 反例3：枚举名使用动词
enum GetUserType { }  // 应改为UserType
enum SendMessageStatus { }  // 应改为MessageStatus
enum ConnectState { }  // 应改为ConnectionState

// 反例4：类型别名使用动词
type GetUserId = string;  // 应改为UserId
type SendCallback = (msg: Message) => void;  // 应改为MessageSender或MessageCallback
type HandleEvent = (event: Event) => void;  // 应改为EventHandler

// 反例5：形容词作为类型名
class Active { }  // 应改为ActiveUser或Activity
interface Running { }  // 应改为RunningState或Runtime
enum Connected { }  // 应改为ConnectionStatus

// 反例6：动词短语作为类型名
class CreateUser { }  // 应改为UserCreator或UserFactory
interface GetData { }  // 应改为DataRetriever或DataProvider
enum StartService { }  // 应改为ServiceStarter或ServiceType
