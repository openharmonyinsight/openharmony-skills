# 线性/非线性容器 API 精简参考

> 源文档: `docs-OpenHarmony-v6.0-Release/zh-cn/application-dev/reference/apis-arkts/js-apis-*.md`  
> 本文件为 `@ohos.util.*` 容器类 API 的精简版本，仅保留核心接口和常用示例。

---

## 容器选型指南

### 线性容器对比

| 容器 | 数据结构 | 特点 | 推荐场景 |
|------|----------|------|----------|
| **ArrayList** | 动态数组 | 随机访问快，增删慢 | 频繁读取 |
| **LinkedList** | 双向链表 | 增删快，查询慢 | 频繁增删+双向操作 |
| **List** | 单向链表 | 增删快，单向遍历 | 频繁增删+单向操作 |
| **Deque** | 循环队列 | 两端增删高效 | 两端频繁增删 |
| **Queue** | 循环队列 | FIFO | 先进先出 |
| **Stack** | 数组 | LIFO | 先进后出 |

### 非线性容器对比

| 容器 | 数据结构 | 特点 | 推荐场景 |
|------|----------|------|----------|
| **HashMap** | 数组+链表+红黑树 | 查询快，无序 | 快速存取键值对 |
| **TreeMap** | 红黑树 | 有序，效率较低 | 有序键值对 |
| **HashSet** | 基于HashMap | 无序，不重复 | 去重集合 |
| **TreeSet** | 基于TreeMap | 有序，不重复 | 有序去重集合 |
| **LightWeightMap** | 哈希+线性探测 | 内存占用小 | 小数据量有序KV |
| **LightWeightSet** | 基于LightWeightMap | 内存占用小 | 小数据量有序集合 |
| **PlainArray** | 数组 | 整数key | 整数键值对 |

---

## 一、ArrayList (线性容器)

```ts
import { ArrayList } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `add` | `add(element: T): boolean` | 尾部插入 |
| `insert` | `insert(element: T, index: number): void` | 指定位置插入 |
| `has` | `has(element: T): boolean` | 判断是否包含 |
| `getIndexOf` | `getIndexOf(element: T): number` | 查找首次出现下标 |
| `remove` | `remove(element: T): boolean` | 删除首个匹配元素 |
| `removeByIndex` | `removeByIndex(index: number): T` | 按下标删除 |
| `removeByRange` | `removeByRange(from: number, to: number): void` | 删除范围 [from, to) |
| `sort` | `sort(comparator?: (a: T, b: T) => number): void` | 排序 |
| `clear` | `clear(): void` | 清空 |
| `clone` | `clone(): ArrayList<T>` | 克隆 |
| `[index]` | `[index: number]: T` | 索引访问 (API 12+) |

### 常用示例

```ts
let list = new ArrayList<number>();
list.add(2);
list.add(4);
list.insert(3, 1);       // [2, 3, 4]
list.sort((a, b) => a - b);
console.info("length:", list.length);  // 3

// 遍历
for (let item of list) {
  console.info("item:", item);
}
```

---

## 二、LinkedList (双向链表)

```ts
import { LinkedList } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `add` | `add(element: T): boolean` | 尾部插入 |
| `addFirst` | `addFirst(element: T): void` | 头部插入 |
| `insert` | `insert(index: number, element: T): void` | 指定位置插入 |
| `get` | `get(index: number): T` | 按下标获取 |
| `getFirst` | `getFirst(): T` | 获取第一个 |
| `getLast` | `getLast(): T` | 获取最后一个 |
| `removeFirst` | `removeFirst(): T` | 删除第一个 |
| `removeLast` | `removeLast(): T` | 删除最后一个 |
| `remove` | `remove(element: T): boolean` | 删除首个匹配 |
| `set` | `set(index: number, element: T): T` | 替换指定位置 |
| `clear` | `clear(): void` | 清空 |

### 常用示例

```ts
let linkedList = new LinkedList<number>();
linkedList.add(1);
linkedList.addFirst(0);  // [0, 1]
linkedList.add(2);       // [0, 1, 2]

console.info("first:", linkedList.getFirst());  // 0
console.info("last:", linkedList.getLast());    // 2

linkedList.removeFirst();  // [1, 2]
```

---

## 三、Deque (双端队列)

```ts
import { Deque } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `insertFront` | `insertFront(element: T): void` | 头部插入 |
| `insertEnd` | `insertEnd(element: T): void` | 尾部插入 |
| `getFirst` | `getFirst(): T` | 获取头部 |
| `getLast` | `getLast(): T` | 获取尾部 |
| `popFirst` | `popFirst(): T` | 弹出头部 |
| `popLast` | `popLast(): T` | 弹出尾部 |
| `has` | `has(element: T): boolean` | 判断是否包含 |

### 常用示例

```ts
let deque = new Deque<number>();
deque.insertFront(1);
deque.insertEnd(2);
deque.insertFront(0);  // [0, 1, 2]

console.info("first:", deque.popFirst());  // 0
console.info("last:", deque.popLast());    // 2
```

---

## 四、Queue (队列 - FIFO)

```ts
import { Queue } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `add` | `add(element: T): boolean` | 尾部入队 |
| `pop` | `pop(): T` | 头部出队 |
| `getFirst` | `getFirst(): T` | 查看队首 |

### 常用示例

```ts
let queue = new Queue<number>();
queue.add(1);
queue.add(2);
console.info("first:", queue.getFirst());  // 1
console.info("pop:", queue.pop());         // 1
```

---

## 五、Stack (栈 - LIFO)

```ts
import { Stack } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `push` | `push(item: T): T` | 压栈 |
| `pop` | `pop(): T` | 弹栈 |
| `peek` | `peek(): T` | 查看栈顶 |
| `locate` | `locate(element: T): number` | 查找元素位置 |

### 常用示例

```ts
let stack = new Stack<number>();
stack.push(1);
stack.push(2);
console.info("peek:", stack.peek());  // 2
console.info("pop:", stack.pop());    // 2
```

---

## 六、HashMap (非线性)

```ts
import { HashMap } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `set` | `set(key: K, value: V): Object` | 添加/更新 |
| `get` | `get(key: K): V` | 获取值 |
| `hasKey` | `hasKey(key: K): boolean` | 判断key存在 |
| `hasValue` | `hasValue(value: V): boolean` | 判断value存在 |
| `remove` | `remove(key: K): V` | 删除 |
| `replace` | `replace(key: K, newValue: V): boolean` | 替换 |
| `keys` | `keys(): IterableIterator<K>` | 获取所有key |
| `values` | `values(): IterableIterator<V>` | 获取所有value |
| `entries` | `entries(): IterableIterator<[K, V]>` | 获取所有键值对 |
| `clear` | `clear(): void` | 清空 |
| `setAll` | `setAll(map: HashMap<K, V>): void` | 合并另一个Map |

### 常用示例

```ts
let hashMap = new HashMap<string, number>();
hashMap.set("a", 1);
hashMap.set("b", 2);

console.info("get a:", hashMap.get("a"));     // 1
console.info("hasKey:", hashMap.hasKey("a")); // true

// 遍历
for (let [key, value] of hashMap) {
  console.info(`${key}: ${value}`);
}
```

---

## 七、TreeMap (有序KV)

```ts
import { TreeMap } from '@kit.ArkTS';
```

### 核心 API (同HashMap，额外支持)

| 方法 | 签名 | 说明 |
|------|------|------|
| `getFirstKey` | `getFirstKey(): K` | 获取最小key |
| `getLastKey` | `getLastKey(): K` | 获取最大key |
| `getLowerKey` | `getLowerKey(key: K): K` | 小于key的最大键 |
| `getHigherKey` | `getHigherKey(key: K): K` | 大于key的最小键 |

### 自定义排序

```ts
// 降序排列
let treeMap = new TreeMap<string, number>((a, b) => a > b);
treeMap.set("aa", 1);
treeMap.set("cc", 2);
treeMap.set("bb", 3);

for (let [key, value] of treeMap) {
  console.info(`${key}: ${value}`);
}
// cc: 2, bb: 3, aa: 1 (降序)
```

---

## 八、HashSet (去重集合)

```ts
import { HashSet } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `add` | `add(value: T): boolean` | 添加元素 |
| `has` | `has(value: T): boolean` | 判断存在 |
| `remove` | `remove(value: T): boolean` | 删除元素 |
| `values` | `values(): IterableIterator<T>` | 获取所有值 |
| `clear` | `clear(): void` | 清空 |

### 常用示例

```ts
let hashSet = new HashSet<number>();
hashSet.add(1);
hashSet.add(2);
hashSet.add(1);  // 重复，不会添加

console.info("length:", hashSet.length);  // 2
console.info("has 1:", hashSet.has(1));   // true
```

---

## 九、TreeSet (有序去重)

```ts
import { TreeSet } from '@kit.ArkTS';
```

### 核心 API (同HashSet，额外支持)

| 方法 | 签名 | 说明 |
|------|------|------|
| `getFirstValue` | `getFirstValue(): T` | 获取最小值 |
| `getLastValue` | `getLastValue(): T` | 获取最大值 |
| `getLowerValue` | `getLowerValue(value: T): T` | 小于value的最大值 |
| `getHigherValue` | `getHigherValue(value: T): T` | 大于value的最小值 |

### 自定义排序

```ts
// 升序排列 (默认)
let treeSet = new TreeSet<number>((a, b) => a < b);
treeSet.add(3);
treeSet.add(1);
treeSet.add(2);

for (let value of treeSet) {
  console.info("value:", value);
}
// 1, 2, 3 (升序)
```

---

## 十、LightWeightMap / LightWeightSet

轻量级容器，适合小数据量场景，内存占用更小。

```ts
import { LightWeightMap, LightWeightSet } from '@kit.ArkTS';
```

### LightWeightMap 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `set` | `set(key: K, value: V): Object` | 添加/更新 |
| `get` | `get(key: K): V` | 获取值 |
| `getIndexOfKey` | `getIndexOfKey(key: K): number` | 获取key的下标 |
| `getKeyAt` | `getKeyAt(index: number): K` | 按下标获取key |
| `getValueAt` | `getValueAt(index: number): V` | 按下标获取value |
| `setValueAt` | `setValueAt(index: number, value: V): boolean` | 按下标设置value |

---

## 十一、PlainArray

key为number类型的简化容器。

```ts
import { PlainArray } from '@kit.ArkTS';
```

### 核心 API

| 方法 | 签名 | 说明 |
|------|------|------|
| `add` | `add(key: number, value: T): void` | 添加 |
| `get` | `get(key: number): T` | 获取 |
| `getIndexOfKey` | `getIndexOfKey(key: number): number` | 获取key下标 |
| `getKeyAt` | `getKeyAt(index: number): number` | 按下标获取key |
| `getValueAt` | `getValueAt(index: number): T` | 按下标获取value |
| `remove` | `remove(key: number): T` | 删除 |
| `removeAt` | `removeAt(index: number): boolean` | 按下标删除 |

---

## 通用注意事项

1. **不要在遍历中修改容器**: 在 `forEach`、`entries`、`[Symbol.iterator]` 中使用 `set`/`remove` 会导致死循环等风险
2. **使用 for 循环修改**: 需要在遍历中增删时，使用普通 for 循环
3. **构造函数不能直接调用**: 必须使用 `new` 关键字创建实例
4. **方法不支持 bind**: 容器方法不能使用 `bind` 绑定到其他对象
5. **索引范围**: index 需 <= `int32_max` (2147483647)

```ts
// 正确: 使用 for 循环删除
let hashMap = new HashMap<string, number>();
for (let i = 0; i < 10; i++) {
  hashMap.set("key" + i, i);
}
for (let i = 0; i < 10; i++) {
  hashMap.remove("key" + i);
}

// 错误: 在 forEach 中删除 (可能死循环)
// hashMap.forEach((v, k) => hashMap.remove(k));
```
