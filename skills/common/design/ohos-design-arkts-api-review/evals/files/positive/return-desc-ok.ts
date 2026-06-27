// Eval file for rule: 提供返回值取值说明
// 正例1：boolean类型返回值有明确的true/false含义说明
/**
 * 检查用户是否已登录
 * @returns 返回true表示用户已登录，返回false表示用户未登录（Return true if user is logged in, false otherwise）
 */
function isLoggedIn(): boolean {
  return this.session !== null;
}

// 正例2：string类型返回值说明了空串的特殊情况
/**
 * 获取用户显示名称
 * @returns 用户显示名称。如果用户未设置显示名称，返回空字符串
 */
function getDisplayName(): string {
  return this.displayName || '';
}

// 正例3：nullable类型返回值说明了null的含义
/**
 * 获取用户头像URL
 * @returns 用户头像URL。如果用户未设置头像，返回null
 */
function getAvatarUrl(): string | null {
  return this.avatarUrl;
}

// 正例4：包含undefined的联合类型说明了undefined的含义
/**
 * 获取用户偏好设置
 * @returns 用户偏好设置对象。如果用户从未设置过偏好，返回undefined
 */
function getUserPreference(): Preference | undefined {
  return this.preference;
}

// 正例5：数值类型返回值说明了极值含义
/**
 * 获取用户积分
 * @returns 用户积分值。新用户返回0，积分达到上限时返回MAX_POINTS(10000)
 */
function getPoints(): number {
  if (this.isNewUser) return 0;
  return Math.min(this.points, MAX_POINTS);
}

// 正例6：数值类型返回值说明了枚举值含义
/**
 * 获取连接状态
 * @returns 连接状态码：0表示断开，1表示连接中，2表示已连接，3表示连接失败
 */
function getConnectionState(): number {
  return this.state;
}

// 正例7：位运算结果数值类型说明了计算规则
/**
 * 获取文件权限标志
 * @returns 权限标志位运算结果。多个权限可通过位或运算组合，
 * 例如：可读(1) | 可写(2) = 3表示同时拥有读写权限
 */
function getFilePermissions(): number {
  return this.permissions;
}

// 正例8：枚举类型返回值说明了超出枚举本身的含义
/**
 * 获取任务执行结果
 * @returns 任务执行结果枚举值。SUCCESS表示任务成功完成；
 * FAILED表示任务执行失败，需查看error字段获取详细信息；
 * TIMEOUT表示任务超时，通常需要重试
 */
function getTaskResult(): TaskResult {
  return this.result;
}

// 正例9：string类型返回值说明了多种特殊值
/**
 * 获取系统日志路径
 * @returns 日志文件路径。如果未配置日志路径返回空字符串；
 * 如果日志文件不存在返回"NOT_FOUND"
 */
function getLogPath(): string {
  if (!this.config.logPath) return '';
  if (!fs.existsSync(this.config.logPath)) return 'NOT_FOUND';
  return this.config.logPath;
}

// 正例10：boolean类型返回值说明了多种业务含义
/**
 * 检查文件是否可访问
 * @returns 返回true表示文件可正常访问；
 * 返回false表示文件不可访问，可能是权限不足或文件不存在
 */
function canAccessFile(): boolean {
  try {
    fs.accessSync(this.filePath);
    return true;
  } catch {
    return false;
  }
}
