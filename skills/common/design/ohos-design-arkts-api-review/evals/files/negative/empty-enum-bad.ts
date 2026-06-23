// Eval file for rule: 禁止创建空枚举/常量接口
// 反例：错误码已定义但从未返回
enum ErrorCode {
  SUCCESS = 0,
  NETWORK_ERROR = 1001,
  TIMEOUT_ERROR = 1002,  // TIMEOUT_ERROR 从未被任何函数返回
  PERMISSION_ERROR = 1003,  // PERMISSION_ERROR 从未被任何函数返回
}

function connect(): ErrorCode {
  if (!isNetworkAvailable()) {
    return ErrorCode.NETWORK_ERROR;
  }
  return ErrorCode.SUCCESS;
}
// TIMEOUT_ERROR 和 PERMISSION_ERROR 是幽灵错误码，误导开发者

// 反例：枚举值从未被使用
enum UserStatus {
  ACTIVE = 0,
  INACTIVE = 1,
  SUSPENDED = 2,  // SUSPENDED 从未被引用
}

function getStatus(): UserStatus {
  if (isActive) return UserStatus.ACTIVE;
  return UserStatus.INACTIVE;
}
// SUSPENDED 从未被使用，应删除或添加使用场景
