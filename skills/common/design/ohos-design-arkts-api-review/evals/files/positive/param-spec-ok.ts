// Eval file for rule: 参数规格保持一致
// 正例1：同一Kit内参数命名一致
function getStartupTaskResult(startupTask: string): Object;
function isStartupTaskInitialized(startupTask: string): boolean;
function removeStartupTask(startupTask: string): void;
// 正确：所有函数使用相同的参数名 startupTask 表示同一概念

// 正例2：配置对象规格一致
interface WindowConfig {
  width: int;
  height: int;
  title: string;
}

function createWindow(config: WindowConfig): Window;
function updateWindow(windowId: string, config: WindowConfig): void;
// 正确：同一配置对象在不同API中保持一致

// 正例3：ID参数命名一致
function getUserById(userId: string): User;
function deleteUser(userId: string): void;
function updateUser(userId: string, data: Object): void;
// 正确：用户ID统一命名为 userId

// 正例4：路径参数规格一致
function readFile(filePath: string): ArrayBuffer;
function writeFile(filePath: string, data: ArrayBuffer): void;
function deleteFile(filePath: string): void;
function fileExists(filePath: string): boolean;
// 正确：文件路径统一命名为 filePath，类型统一为 string
