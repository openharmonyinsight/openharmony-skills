// Eval file for rule: 查询类方法，查询不到时应返回 null
// 反例1：查询容器中的值，未找到不应返回非null类型
declare function getStorageTextValue(key: string): string;
// 错误：未找到时应返回null，类型应为 string | null

// 反例2：使用undefined代替null
declare function getStorageTextValue(key: string): string | undefined;
// 错误：查询类方法应返回null而非undefined

// 反例3：next方法不应返回非null类型
declare function tryNext(): Promise<Data>;
// 错误：到达尽头应返回null，类型应为 Promise<Data | null>

// 反例4：next方法使用undefined
declare function tryNext(): Promise<Data | undefined>;
// 错误：应使用null而非undefined

// 反例5：查询方法抛出异常
function findNodeById(nodeId: string): TreeNode {
  const node = internalFind(nodeId);
  if (!node) {
    throw new Error('Node not found');  // 错误：未找到是正常场景，应返回null
  }
  return node;
}
