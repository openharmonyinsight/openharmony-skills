// Eval file for rule: 函数入参合理使用参数封装
// 反例1：参数数量超过5个，未进行封装
function createConnection(
  host: string,
  port: number,
  timeout: number,
  retryCount: number,
  enableSSL: boolean,
  certPath: string
): Connection {
  // 错误：参数数量为6个，超过5个，建议封装为ConnectionConfig对象
  return new Connection();
}

// 反例2：参数数量过多，难以维护
function drawRectangle(
  x: number,
  y: number,
  width: number,
  height: number,
  fillColor: string,
  strokeColor: string,
  strokeWidth: number,
  opacity: number,
  borderRadius: number
): void {
  // 错误：参数数量为9个，远超5个，建议封装为RectangleOptions对象
}

// 反例3：相关参数未分组封装
function moveWindow(
  windowId: string,
  x: number,
  y: number,
  width: number,
  height: number,
  animate: boolean,
  duration: number
): void {
  // 错误：参数数量为7个，x/y和width/height可以分别封装为Position和Size对象
}

// 反例4：配置参数散乱，不易扩展
function initialize(
  appId: string,
  appSecret: string,
  serverUrl: string,
  logLevel: string,
  enableCache: boolean,
  cacheSize: number,
  timeout: number
): void {
  // 错误：参数数量为7个，配置类参数建议封装为InitConfig对象
}

// 反例5：查询参数过多
function queryData(
  table: string,
  fields: string[],
  whereClause: string,
  orderBy: string,
  limit: number,
  offset: number,
  groupBy: string
): Result {
  // 错误：参数数量为7个，建议封装为QueryOptions对象
  return new Result();
}
