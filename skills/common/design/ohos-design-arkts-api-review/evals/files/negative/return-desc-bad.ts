// Eval file for rule: 提供返回值取值说明
// 反例1：boolean类型返回值缺少true/false含义说明
/**
 * 检查状态
 * @returns 返回布尔值
 */
function checkStatus(): boolean {
  return this.status === 'active';
}

// 反例2：string类型返回值未说明空串的特殊情况
/**
 * 获取用户备注
 * @returns 用户备注
 */
function getNote(): string {
  return this.note || '';
}

// 反例3：nullable类型返回值未说明null的含义
/**
 * 获取父节点
 * @returns 父节点对象
 */
function getParent(): Node | null {
  return this.parent;
}

// 反例4：包含undefined的联合类型未说明undefined的含义
/**
 * 获取配置选项
 * @returns 配置选项
 */
function getOptions(): Options | undefined {
  return this.options;
}

// 反例5：数值类型返回值未说明极值含义
/**
 * 获取文件大小
 * @returns 文件大小（字节）
 */
function getFileSize(): number {
  if (!this.file) return -1;  // 特殊值-1未说明
  return this.file.size;
}

// 反例6：数值类型返回值未说明枚举值含义
/**
 * 获取错误码
 * @returns 错误码
 */
function getErrorCode(): number {
  return this.errorCode;
}

// 反例7：位运算结果数值类型未说明计算规则
/**
 * 获取配置标志
 * @returns 标志位组合值
 */
function getConfigFlags(): number {
  return this.flags;
}

// 反例8：枚举类型返回值未说明超出枚举本身的含义
/**
 * 获取处理结果状态
 * @returns 处理结果状态
 */
function getResultStatus(): ResultStatus {
  return this.status;
}

// 反例9：string类型返回值有特殊值但未说明
/**
 * 获取错误消息
 * @returns 错误消息字符串
 */
function getErrorMessage(): string {
  if (!this.error) return 'NONE';  // 特殊值'NONE'未说明
  return this.error.message;
}

// 反例10：数值类型返回值未说明所有可能的取值
/**
 * 获取索引位置
 * @returns 索引值
 */
function getIndex(): number {
  if (!this.isValid()) return -1;  // 特殊值-1未说明
  if (this.isDefault()) return 0;  // 特殊值0的含义未说明
  return this.index;
}
