// Eval file for rule: 查询类方法，查询不到时应返回 null
// 正例1：查询容器中的值，未找到返回null
declare function getStorageTextValue(key: string): string | null;

// 正例2：通过next方式查找下一个，到达尽头返回null
declare function tryNext(): Promise<Data | null>;

// 正例3：查询缓存数据
declare function getFromCache(key: string): CacheData | null;

// 正例4：查询UI树节点
declare function findNodeById(nodeId: string): TreeNode | null;

// 正例5：数据库查询
declare function queryUserById(userId: number): User | null;

// 正例6：游标获取下一个元素
declare function cursorNext(): CursorResult | null;
