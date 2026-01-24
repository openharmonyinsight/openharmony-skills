# ArkTS 共享容器 API 精简参考

> 源文档: js-apis-arkts-collections.md (5000+ 行)

## 导入模块

```typescript
import { collections } from '@kit.ArkTS';
```

## 核心概念

- **共享容器**: 分配在共享堆 (SharedHeap)，支持跨线程引用传递
- **非线程安全**: 需要配合 AsyncLock 使用
- **Sendable**: 所有共享容器都是 Sendable 类型

---

## collections.Array\<T>

### 创建

```typescript
// 空数组
const arr = new collections.Array<number>();

// 从元素创建
const arr = collections.Array.from<number>([1, 2, 3]);

// 指定长度和初始值
const arr = collections.Array.create<number>(100, 0);
```

### 常用方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `push(...items)` | 添加元素 | 新长度 |
| `pop()` | 移除最后元素 | 移除的元素 |
| `shift()` | 移除第一元素 | 移除的元素 |
| `unshift(...items)` | 头部添加元素 | 新长度 |
| `at(index)` | 获取元素 (支持负索引) | 元素或 undefined |
| `slice(start?, end?)` | 截取子数组 | 新 Array |
| `splice(start, deleteCount?, ...items)` | 删除/插入元素 | 删除的元素 |
| `concat(...items)` | 合并数组 | 新 Array |
| `indexOf(item)` | 查找索引 | 索引或 -1 |
| `includes(item)` | 是否包含 | boolean |
| `find(predicate)` | 查找元素 | 元素或 undefined |
| `findIndex(predicate)` | 查找索引 | 索引或 -1 |
| `fill(value, start?, end?)` | 填充元素 | this |
| `sort(compareFn?)` | 排序 | this |
| `reverse()` | 反转 | this |
| `forEach(callback)` | 遍历 | void |
| `map(callback)` | 映射 | 新 Array |
| `filter(predicate)` | 过滤 | 新 Array |
| `reduce(callback, initial?)` | 归约 | 结果值 |
| `every(predicate)` | 全部满足 | boolean |
| `some(predicate)` | 部分满足 | boolean |
| `join(separator?)` | 拼接字符串 | string |
| `shrinkTo(length)` | 缩小到指定长度 | void |
| `extendTo(length, value)` | 扩展到指定长度 | void |

### 属性

```typescript
arr.length  // 数组长度
arr[0]      // 索引访问
```

### 示例

```typescript
const arr = new collections.Array<number>();
arr.push(1, 2, 3);
arr.pop();                    // 3
arr.at(-1);                   // 2
arr.map(x => x * 2);          // [2, 4]
arr.filter(x => x > 1);       // [2]
arr.reduce((a, b) => a + b);  // 3
```

---

## collections.Map\<K, V>

### 创建

```typescript
const map = new collections.Map<string, number>();
const map = new collections.Map<string, number>([["a", 1], ["b", 2]]);
```

### 常用方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set(key, value)` | 设置键值 | this |
| `get(key)` | 获取值 | 值或 undefined |
| `has(key)` | 是否存在 | boolean |
| `delete(key)` | 删除键 | boolean |
| `clear()` | 清空 | void |
| `keys()` | 键迭代器 | IterableIterator |
| `values()` | 值迭代器 | IterableIterator |
| `entries()` | 键值对迭代器 | IterableIterator |
| `forEach(callback)` | 遍历 | void |

### 属性

```typescript
map.size  // 键值对数量
```

### 示例

```typescript
const map = new collections.Map<string, number>();
map.set("a", 1).set("b", 2);
map.get("a");     // 1
map.has("b");     // true
map.delete("a");  // true
map.size;         // 1
```

---

## collections.Set\<T>

### 创建

```typescript
const set = new collections.Set<number>();
const set = new collections.Set<number>([1, 2, 3]);
```

### 常用方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add(value)` | 添加元素 | this |
| `has(value)` | 是否存在 | boolean |
| `delete(value)` | 删除元素 | boolean |
| `clear()` | 清空 | void |
| `keys()` | 键迭代器 | IterableIterator |
| `values()` | 值迭代器 | IterableIterator |
| `entries()` | 键值对迭代器 | IterableIterator |
| `forEach(callback)` | 遍历 | void |

### 属性

```typescript
set.size  // 元素数量
```

### 示例

```typescript
const set = new collections.Set<number>();
set.add(1).add(2).add(2);  // 去重
set.has(1);   // true
set.size;     // 2
set.delete(1);
```

---

## collections.TypedArray

支持类型: `Int8Array`, `Uint8Array`, `Int16Array`, `Uint16Array`, `Int32Array`, `Uint32Array`, `Float32Array`, `Uint8ClampedArray`

### 创建

```typescript
// 指定长度
const arr = new collections.Int32Array(10);

// 从数组创建
const arr = collections.Int32Array.from([1, 2, 3]);

// 从 ArrayBuffer 创建
const buffer = new collections.ArrayBuffer(16);
const arr = new collections.Int32Array(buffer, 0, 4);
```

### 常用方法

| 方法 | 说明 |
|------|------|
| `at(index)` | 获取元素 |
| `fill(value, start?, end?)` | 填充 |
| `slice(start?, end?)` | 截取 |
| `subarray(begin?, end?)` | 子视图 |
| `set(array, offset?)` | 复制数据 |
| `copyWithin(target, start, end?)` | 内部复制 |
| `indexOf(value)` | 查找索引 |
| `includes(value)` | 是否包含 |
| `find(predicate)` | 查找元素 |
| `findIndex(predicate)` | 查找索引 |
| `forEach(callback)` | 遍历 |
| `map(callback)` | 映射 |
| `filter(predicate)` | 过滤 |
| `reduce(callback)` | 归约 |
| `sort(compareFn?)` | 排序 |
| `reverse()` | 反转 |
| `join(separator?)` | 拼接字符串 |

### 属性

```typescript
arr.length      // 元素数量
arr.buffer      // 底层 ArrayBuffer
arr.byteLength  // 字节长度
arr.byteOffset  // 字节偏移
arr[0]          // 索引访问
```

---

## collections.ArrayBuffer

### 创建

```typescript
const buffer = new collections.ArrayBuffer(16);  // 16 字节
```

### 方法

```typescript
// 截取
buffer.slice(begin?: number, end?: number): ArrayBuffer

// 静态方法: 判断是否为 ArrayBuffer 视图
collections.ArrayBuffer.isView(value: Object): boolean
```

### 属性

```typescript
buffer.byteLength  // 字节长度
```

---

## collections.BitVector (API 12+)

位向量，用于存储大量布尔值。

### 创建

```typescript
const bits = new collections.BitVector(100);  // 100 位
```

### 方法

| 方法 | 说明 |
|------|------|
| `push(value)` | 添加位 |
| `pop()` | 移除最后位 |
| `has(index)` | 获取位值 |
| `setBitsByRange(start, end, value)` | 批量设置 |
| `getBitsByRange(start, end)` | 批量获取 |
| `getBitCountByRange(start, end)` | 统计 1 的数量 |
| `resize(size)` | 调整大小 |
| `flipBitByIndex(index)` | 翻转位 |
| `flipBitsByRange(start, end)` | 批量翻转 |

---

## 跨线程使用示例

### 配合 AsyncLock

```typescript
import { collections, ArkTSUtils, taskpool } from '@kit.ArkTS';

@Sendable
class SharedState {
  arr: collections.Array<number> = new collections.Array<number>();
  lock: ArkTSUtils.locks.AsyncLock = new ArkTSUtils.locks.AsyncLock();

  async add(value: number): Promise<void> {
    await this.lock.lockAsync(() => {
      this.arr.push(value);
    });
  }

  async getAll(): Promise<number[]> {
    return this.lock.lockAsync(() => {
      return this.arr.slice().map(x => x);  // 返回普通数组
    });
  }
}

@Concurrent
async function addValue(state: SharedState, value: number): Promise<void> {
  await state.add(value);
}

// 使用
const state = new SharedState();
const task = new taskpool.Task(addValue, state, 100);
await taskpool.execute(task);
```

### 传递给 TaskPool

```typescript
@Concurrent
function processArray(arr: collections.Array<number>): number {
  return arr.reduce((a, b) => a + b, 0);
}

const arr = collections.Array.from([1, 2, 3, 4, 5]);
const task = new taskpool.Task(processArray, arr);
const result = await taskpool.execute(task);
console.info(`Sum: ${result}`);  // 15
```

---

## 与原生容器对比

| 特性 | collections.Array | 原生 Array |
|------|-------------------|------------|
| 跨线程传递 | 引用传递 (高效) | 拷贝传递 |
| 内存位置 | 共享堆 | 普通堆 |
| Sendable | 是 | 否 |
| 线程安全 | 否 (需 AsyncLock) | 否 |
| 使用场景 | 多线程共享 | 单线程 |

---

## 常见错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10200201 | 并发修改错误 | 使用 AsyncLock 保护 |
| 10200011 | 方法绑定错误 | 不要使用 bind |
| 10200001 | 索引越界 | 检查索引范围 |
