// Eval file for rule: 禁止有争议的命名
// 正例1：中性、专业的命名
function getPrimaryNode(): Node { }  // 使用primary代替master
function getSecondaryNode(): Node { }  // 使用secondary代替slave
function getBlockList(): string[] { }  // 使用blockList代替blacklist
function getAllowList(): string[] { }  // 使用allowList代替whitelist

// 正例2：通用技术术语
function connect(): void { }
function sendMessage(): void { }
function handleEvent(): void { }
function processData(): void { }

// 正例3：使用鸿蒙特有的术语
function getHarmonyOSVersion(): string { }
function getArkUIVersion(): string { }
function getAbilityInfo(): AbilityInfo { }
