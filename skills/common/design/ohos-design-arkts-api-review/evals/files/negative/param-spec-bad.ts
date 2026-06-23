// Eval file for rule: 参数规格保持一致
// 反例1：同一Kit内参数命名不一致
function getStartupTaskResult(task: string): Object;
function isStartupTaskInitialized(startupTask: string): boolean;
// 错误：同一概念使用了不同的参数名 task 和 startupTask

// 反例2：时间参数单位不一致
function set_timeout(int duration);   // duration单位为毫秒
function set_interval(int interval);  // interval单位为秒
// 错误：时间参数单位不一致，容易导致开发者使用错误

// 反例3：ID参数命名不一致
function getUserById(userId: string): User;
function deleteUser(id: string): void;
function updateUser(uid: string, data: Object): void;
// 错误：用户ID使用了不同的命名 userId、id、uid

// 反例4：路径参数命名不一致
function readFile(filePath: string): ArrayBuffer;
function writeFile(path: string, data: ArrayBuffer): void;
function deleteFile(file: string): void;
// 错误：文件路径使用了不同的命名 filePath、path、file

// 反例5：配置对象规格不一致
interface CreateWindowConfig {
  width: int;
  height: int;
  title: string;
}

interface UpdateWindowConfig {
  w: int;
  h: int;
  name: string;
}
// 错误：同一概念的配置对象使用了不同的属性名
