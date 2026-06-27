// Eval file for rule: 符合命名规范
// 反例1：命名不贴合业务场景
function doSomething(): void { }  // 命名模糊，无法表达功能
function process(): void { }  // 命名过于泛化
function handle(): void { }  // 命名不明确

// 反例2：违背业界通用命名
function convertToString(): string { }  // 业界通用的是toString
function stringify(): string { }  // 业界通用的是toJSON，容易混淆

// 反例3：与存量接口风格不一致
// 存量接口使用 getUserInfo，新增接口不应使用不同风格
function fetchUserInfo(): UserInfo { }  // 应保持与getUserInfo风格一致
function queryUserInfo(): UserInfo { }  // 应保持与getUserInfo风格一致
