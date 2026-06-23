// Eval file for rule: 禁止创建空枚举/常量接口
// 正例：错误码都有对应的返回场景
enum ErrorCode {
  SUCCESS = 0,
  NETWORK_ERROR = 1001,
  TIMEOUT_ERROR = 1002,
}

function connect(): ErrorCode {
  if (!isNetworkAvailable()) {
    return ErrorCode.NETWORK_ERROR;  // NETWORK_ERROR 有对应的返回
  }
  return ErrorCode.SUCCESS;
}

function requestWithTimeout(): ErrorCode {
  try {
    return doRequest();
  } catch (timeout) {
    return ErrorCode.TIMEOUT_ERROR;  // TIMEOUT_ERROR 有对应的返回
  }
}
