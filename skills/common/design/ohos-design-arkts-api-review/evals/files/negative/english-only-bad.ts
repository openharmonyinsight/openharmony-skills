// Eval file for rule: 命名必须使用英语
// 反例1：使用拼音命名
function huoQuYongHuXinXi(): UserInfo { }  // 应改为getUserInfo
function faSongXiaoXi(): void { }  // 应改为sendMessage
function jiSuanZongE(): number { }  // 应改为calculateTotal
function lianJieFuWuQi(): void { }  // 应改为connectToServer

// 反例2：中英混用
function get用户Info(): UserInfo { }  // 应改为getUserInfo
function sendMessage消息(): void { }  // 应改为sendMessage
function calculate总数(): number { }  // 应改为calculateTotal

// 反例3：使用其他非英语语言
function obtenerUsuario(): UserInfo { }  // 西班牙语，应改为getUserInfo
function obtenirUtilisateur(): UserInfo { }  // 法语，应改为getUserInfo
function benutzerAbrufen(): UserInfo { }  // 德语，应改为getUserInfo
