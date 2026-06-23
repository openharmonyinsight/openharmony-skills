// Eval file for rule: 显式声明所有 null/undefined
// Note: The reference file has TODO placeholders for examples.
// This eval file provides basic negative examples based on the rule description.

// 反例1：返回值可能为null但未显式声明
function findUser(id: string): User {
  // 错误：实际可能返回null，但类型声明中未体现
  const user = this.users.get(id);
  if (!user) {
    return null;  // 运行时返回null，但类型声明为User
  }
  return user;
}

// 反例2：属性可能为null但未显式声明
interface Config {
  value: string;  // 错误：实际可能为null/undefined，但类型声明中未体现
}

// 反例3：参数可能接收null但未显式声明
function processValue(value: string): void {
  // 错误：实际可能传入null/undefined，但参数类型声明为string
  if (value === null) {
    return;
  }
}
