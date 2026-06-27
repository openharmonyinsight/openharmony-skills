// Eval file for rule: 函数名称应该是动词或动宾/介宾结构
// 反例1：名词结构（非声明式风格）
function user(): User { }  // 应改为getUser或createUser
function message(): Message { }  // 应改为getMessage或sendMessage
function data(): Data { }  // 应改为getData或loadData

// 反例2：形容词结构
function ready(): void { }  // 应改为setReady或isReady
function active(): void { }  // 应改为setActive或isActive
function connected(): void { }  // 应改为setConnected或isConnected

// 反例3：介词错误
function connectServer(): void { }  // 应改为connectToServer
function sendQueue(): void { }  // 应改为sendToQueue
function readFile(): Data { }  // 应改为readFromFile

// 反例4：动词时态错误
function starting(): void { }  // 应改为start
function stopping(): void { }  // 应改为stop
function creatingUser(): User { }  // 应改为createUser
function sendingMessage(): void { }  // 应改为sendMessage

// 反例5：动词形式错误
function started(): void { }  // 应改为start
function stopped(): void { }  // 应改为stop
function createdUser(): User { }  // 应改为createUser
function sentMessage(): void { }  // 应改为sendMessage

// 反例6：词性搭配错误
function userCreate(): User { }  // 名词+动词，应为动词+名词：createUser
function messageSend(): void { }  // 名词+动词，应为动词+名词：sendMessage
function dataGet(): Data { }  // 名词+动词，应为动词+名词：getData
