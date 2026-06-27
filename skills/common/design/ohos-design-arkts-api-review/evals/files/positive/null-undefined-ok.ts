// Eval file for rule: 显式声明所有 null/undefined
// Note: The reference file has TODO placeholders for examples.
// This eval file provides basic positive examples based on the rule description.

// 正例1：通过可选参数声明 undefined
interface UserOptions {
  name?: string;  // 可选参数，显式声明可能为undefined
  age?: number;
}

// 正例2：通过显式 undefined 联合类型声明
function getConfig(key: string): string | undefined {
  // 返回值显式声明可能为undefined
  return this.configMap.get(key);
}

// 正例3：返回值显式声明 null
function findUser(id: string): User | null {
  // 返回值显式声明可能为null
  const user = this.users.get(id);
  return user ?? null;
}

// 正例4：属性显式声明可选与 null 联合类型
interface SearchResult {
  data: string | null;  // 显式声明可能为null
  error?: string;       // 显式声明可选
}
