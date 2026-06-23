// Eval file for rule: 合理使用缩写
// 反例1：使用非熟知缩写
function getUsrInf(): UserInfo { }  // 应使用getUserInfo
function getConf(): Config { }  // 应使用getConfig或getConfiguration
function getApl(): App { }  // 应使用getApp

// 反例2：缩写格式错误（非驼峰形式）
function getUSERInfo(): UserInfo { }  // USER应改为User
function getAPP(): App { }  // APP应改为App
function get_info(): Info { }  // 下划线命名，应使用驼峰

// 反例3：缩写首字母未大写
interface userInfo { }  // Info首字母应大写
interface appConfig { }  // App和Config首字母应大写
interface httpConfig { }  // Http首字母应大写

// 反例4：全大写缩写在驼峰中使用不当
interface JSONParser { }  // 可接受
function parseJSON(): void { }  // 正确
function parsejson(): void { }  // 错误，JSON应大写
function parseJson(): void { }  // 可接受，但parseJSON更通用

// 反例5：过度缩写
function getUsr(): User { }  // User不应缩写
function getNm(): Name { }  // Name不应缩写
function getAddr(): Address { }  // Addr可接受，但Address更清晰
