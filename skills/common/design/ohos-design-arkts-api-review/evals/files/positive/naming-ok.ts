// Eval file for rule: 符合命名规范
// 正例1：命名贴合业务场景
function connect(): void { }  // 明确表达连接功能
function disconnect(): void { }  // 明确表达断开连接功能
function sendRequest(): void { }  // 明确表达发送请求功能

// 正例2：保持业界通用命名
function toString(): string { }  // 业界通用
function toJSON(): string { }  // 业界通用
function parseJSON(): object { }  // 业界通用

// 正例3：保持存量接口风格一致
// 存量接口使用 getUserInfo，新增接口也应保持相似风格
function getUserInfo(): UserInfo { }
function setUserInfo(info: UserInfo): void { }
