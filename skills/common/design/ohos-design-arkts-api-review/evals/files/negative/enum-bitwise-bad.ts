// Eval file for rule: 枚举型支持位运算的应该给出说明
// 反例1：FLAG枚举型缺少位运算说明
enum PermissionFlag {
  READ = 1,
  WRITE = 2,
  EXECUTE = 4,
  DELETE = 8
}
// 错误：枚举值为2的幂次方，明显支持位运算，但缺少说明

// 反例2：使用位运算枚举的函数参数缺少说明
function setPermission(flags: PermissionFlag): void { }
// 错误：参数支持位运算组合，但缺少说明

// 反例3：返回位运算枚举的函数缺少说明
function getPermissionFlags(): PermissionFlag { }
// 错误：返回值可能为多个枚举值的组合，但缺少说明

// 反例4：属性使用位运算枚举但缺少说明
interface FileOptions {
  permissions: PermissionFlag;  // 错误：属性支持位运算组合，但缺少说明
}
