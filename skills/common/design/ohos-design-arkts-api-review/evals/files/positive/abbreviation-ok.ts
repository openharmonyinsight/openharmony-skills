// Eval file for rule: 合理使用缩写
// 正例1：使用业界通用缩写
function getInfo(): Info { }  // Info是通用缩写
function getConfig(): Config { }  // Config是通用缩写
function getApp(): App { }  // App是通用缩写
function getUserId(): string { }  // Id是通用缩写
function parseJSON(): object { }  // JSON是全大写缩写

// 正例2：驼峰形式，首字母大写
interface UserInfo { }
interface AppConfig { }
interface AppId { }
interface HttpConfig { }  // Http首字母大写

// 正例3：缩写在复合词中
function getUserInfo(): UserInfo { }
function getAppConfig(): AppConfig { }
function parseHtmlContent(): void { }  // Html首字母大写
