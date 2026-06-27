// Eval file for rule: 禁止出现语法词法错误
// 正例1：语法正确
function getUserInfo(): UserInfo { }  // 动词+名词，语法正确
function sendMessage(): void { }  // 动词+名词，语法正确
function calculateTotal(): number { }  // 动词+名词，语法正确
function isConnected(): boolean { }  // be动词+形容词，语法正确

// 正例2：符合业界通用惯例的例外
function toString(): string { }  // 业界通用，虽语法略有不妥但可接受
function parseJSON(): object { }  // 业界通用
function toJSON(): string { }  // 业界通用
function log(): void { }  // 业界通用简写

// 正例3：专业术语
function parseHTML(): object { }  // HTML是专业术语
function parseXML(): object { }  // XML是专业术语
function parseURL(): object { }  // URL是专业术语
