// Eval file for rule: 声明式风格的函数名称可以使用名词
// 反例1：非声明式风格使用名词
class UserService {
  function user(): User { }  // 应改为getUser或createUser
  function message(): Message { }  // 应改为getMessage或sendMessage
}

// 反例2：普通函数使用名词
function data(): Data { }  // 应改为getData或loadData
function config(): Config { }  // 应改为getConfig或loadConfig

// 反例3：命令式风格使用名词
class ProcessManager {
  function process(): void { }  // 应改为runProcess或startProcess
  function task(): void { }  // 应改为executeTask或runTask
}

// 反例4：非链式返回使用名词
interface Calculator {
  function result(): number;  // 应改为getResult
  function sum(): number;  // 应改为getSum或calculateSum
}

// 反例5：非Builder模式使用名词
class UserFactory {
  function user(): User { }  // 应改为createUser
  function profile(): Profile { }  // 应改为createProfile
}
