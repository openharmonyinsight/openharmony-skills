// Eval file for rule: 禁止出现语法词法错误
// 反例1：词法错误（拼写错误）
function getUserInfor(): UserInfo { }  // Infor应为Info
function sendMesage(): void { }  // Mesage应为Message
function calculateTotall(): number { }  // Totall应为Total
function conectToServer(): void { }  // conect应为connect

// 反例2：语法错误（词性错误）
function userGet(): UserInfo { }  // 名词+动词，语法错误，应为getUser
function messageSend(): void { }  // 名词+动词，语法错误，应为sendMessage
function totalCalculate(): number { }  // 名词+动词，语法错误，应为calculateTotal

// 反例3：语法错误（时态错误）
function gettingUserInfo(): UserInfo { }  // 进行时，应为原形getUserInfo
function sendingMessage(): void { }  // 进行时，应为原形sendMessage
function calculatedTotal(): number { }  // 过去式，应为原形calculateTotal

// 反例4：不符合业界惯例的错误命名
function stringTo(): string { }  // 与业界通用toString不一致
function JSONParse(): object { }  // 大小写与业界惯例parseJSON不一致
function convertToJSON(): string { }  // 与业界通用toJSON不一致
