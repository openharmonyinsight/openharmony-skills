// Eval file for rule: 禁止有争议的命名
// 反例1：种族歧视相关词汇
function getMasterNode(): Node { }  // 应使用primary/main
function getSlaveNode(): Node { }  // 应使用secondary/replica
function getBlackList(): string[] { }  // 应使用blockList
function getWhiteList(): string[] { }  // 应使用allowList

// 反例2：宗教争议词汇
function jihadProcess(): void { }  // 宗教相关
function crusadeTask(): void { }  // 宗教相关

// 反例3：人物姓名词汇
function adamProcess(): void { }  // 人物姓名
function eveThread(): void { }  // 人物姓名
function bobAlice(): void { }  // 人物姓名（密码学示例除外）

// 反例4：侮辱性词汇
function stupidHandler(): void { }  // 侮辱性
function dumbProcess(): void { }  // 侮辱性
function idiotFunction(): void { }  // 侮辱性

// 反例5：品牌名称
function getIOSVersion(): string { }  // iOS是苹果品牌
function getAndroidInfo(): any { }  // Android是Google品牌
function getWindowsConfig(): any { }  // Windows是微软品牌
function getMicrosoftService(): any { }  // Microsoft是品牌
function getGoogleAPI(): any { }  // Google是品牌
function getAppleService(): any { }  // Apple是品牌

// 反例6：注册商标
function getSwiftVersion(): string { }  // Swift是苹果商标
function getKotlinInfo(): any { }  // Kotlin是JetBrains商标
function getReactNativeConfig(): any { }  // React Native是Facebook商标

// 反例7：其他OS或生态专有名词
function getActivityInfo(): any { }  // Android专有名词，鸿蒙应使用Ability
function getIntentData(): any { }  // Android专有名词
function getUIViewController(): any { }  // iOS专有名词
function getNSManagedObject(): any { }  // iOS专有名词
