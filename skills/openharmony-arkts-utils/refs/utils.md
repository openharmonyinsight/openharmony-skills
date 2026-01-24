# ArkTSUtils API 精简参考

> 源文档: js-apis-arkts-utils.md (1200+ 行)

## 导入模块

```typescript
import { ArkTSUtils } from '@kit.ArkTS';
```

---

## isSendable

判断对象是否为 Sendable 类型。

```typescript
ArkTSUtils.isSendable(value: Object | null | undefined): boolean
```

### 示例

```typescript
@Sendable
class MySendable {
  value: number = 0;
}

const obj = new MySendable();
console.info(ArkTSUtils.isSendable(obj));  // true
console.info(ArkTSUtils.isSendable({}));   // false
```

---

## AsyncLock 异步锁

### 创建锁

```typescript
// 方式1: 直接创建
const lock = new ArkTSUtils.locks.AsyncLock();

// 方式2: 按名称获取 (全局共享)
const lock = ArkTSUtils.locks.AsyncLock.request("myLock");
```

### 获取锁并执行

```typescript
// 基本用法
await lock.lockAsync(() => {
  // 临界区代码
});

// 指定模式
await lock.lockAsync(() => {
  // 临界区代码
}, ArkTSUtils.locks.AsyncLockMode.EXCLUSIVE);

// 带超时
const options = new ArkTSUtils.locks.AsyncLockOptions<void>();
options.timeout = 1000;  // 1秒超时

await lock.lockAsync(() => {
  // 临界区代码
}, ArkTSUtils.locks.AsyncLockMode.EXCLUSIVE, options);
```

### 锁模式

| 模式 | 值 | 说明 |
|------|----|----|
| `SHARED` | 1 | 共享锁，允许多个线程同时持有 |
| `EXCLUSIVE` | 2 | 独占锁，只允许一个线程持有 |

### 锁选项 AsyncLockOptions

| 属性 | 类型 | 说明 |
|------|------|------|
| `isAvailable` | boolean | true: 锁可用时才获取; false: 等待锁释放 |
| `signal` | AbortSignal\<T\> \| null | 中止信号 |
| `timeout` | number | 超时时间 (毫秒) |

### 查询锁状态

```typescript
// 查询指定锁
const state = ArkTSUtils.locks.AsyncLock.query("myLock");
console.info("Held:", state.held);      // 持有的锁信息
console.info("Pending:", state.pending); // 等待中的锁信息

// 查询所有锁
const states = ArkTSUtils.locks.AsyncLock.queryAll();
```

### AsyncLockState 锁状态

| 属性 | 类型 | 说明 |
|------|------|------|
| `held` | AsyncLockInfo[] | 持有的锁信息 |
| `pending` | AsyncLockInfo[] | 等待中的锁信息 |

### AsyncLockInfo 锁信息

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | string | 锁名称 |
| `mode` | AsyncLockMode | 锁模式 |

### 完整示例

```typescript
import { ArkTSUtils, taskpool } from '@kit.ArkTS';

@Sendable
class Counter {
  private count_: number = 0;
  private lock_: ArkTSUtils.locks.AsyncLock = new ArkTSUtils.locks.AsyncLock();

  async increment(): Promise<void> {
    await this.lock_.lockAsync(() => {
      this.count_++;
    });
  }

  async getCount(): Promise<number> {
    return this.lock_.lockAsync(() => {
      return this.count_;
    });
  }
}

@Concurrent
async function incrementTask(counter: Counter): Promise<void> {
  await counter.increment();
}

// 使用
const counter = new Counter();
const tasks = [];
for (let i = 0; i < 10; i++) {
  tasks.push(taskpool.execute(new taskpool.Task(incrementTask, counter)));
}
await Promise.all(tasks);
console.info(`Count: ${await counter.getCount()}`);  // 10
```

---

## ConditionVariable 条件变量 (API 13+)

用于线程间的条件同步。

### 创建

```typescript
const cv = new ArkTSUtils.locks.ConditionVariable();
```

### 方法

```typescript
// 无限等待
await cv.wait();

// 超时等待 (毫秒)
const result = await cv.waitFor(1000);
// result: true=被唤醒, false=超时

// 唤醒一个等待线程
cv.notifyOne();

// 唤醒所有等待线程
cv.notifyAll();
```

### 示例

```typescript
@Sendable
class ProducerConsumer {
  private data_: number | null = null;
  private lock_: ArkTSUtils.locks.AsyncLock = new ArkTSUtils.locks.AsyncLock();
  private cv_: ArkTSUtils.locks.ConditionVariable = new ArkTSUtils.locks.ConditionVariable();

  async produce(value: number): Promise<void> {
    await this.lock_.lockAsync(async () => {
      this.data_ = value;
      this.cv_.notifyOne();
    });
  }

  async consume(): Promise<number> {
    return this.lock_.lockAsync(async () => {
      while (this.data_ === null) {
        await this.cv_.wait();
      }
      const result = this.data_!;
      this.data_ = null;
      return result;
    });
  }
}
```

---

## SendableLruCache (API 12+)

支持跨线程共享的 LRU 缓存。

### 创建

```typescript
// 默认容量 64
const cache = new ArkTSUtils.SendableLruCache<string, number>();

// 指定容量
const cache = new ArkTSUtils.SendableLruCache<string, number>(100);
```

### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `put(key, value)` | 添加/更新 | 旧值或 undefined |
| `get(key)` | 获取 | 值或 undefined |
| `contains(key)` | 是否存在 | boolean |
| `remove(key)` | 删除 | 删除的值或 undefined |
| `clear()` | 清空 | void |
| `isEmpty()` | 是否为空 | boolean |
| `keys()` | 获取所有键 | Array |
| `values()` | 获取所有值 | Array |
| `entries()` | 获取所有键值对 | Array |

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `length` | number | 当前元素数量 (只读) |
| `capacity` | number | 最大容量 (只读) |

### 示例

```typescript
const cache = new ArkTSUtils.SendableLruCache<string, number>(3);

cache.put("a", 1);
cache.put("b", 2);
cache.put("c", 3);

console.info(cache.get("a"));  // 1, "a" 变为最近使用

cache.put("d", 4);  // "b" 被淘汰 (最久未使用)

console.info(cache.contains("b"));  // false
console.info(cache.length);  // 3
```

---

## ASON - Sendable 对象序列化 (API 12+)

用于 Sendable 对象的 JSON 序列化/反序列化。

### 导入

```typescript
import { ASON } from '@kit.ArkTS';
```

### stringify

```typescript
ASON.stringify(value: ISendable | null | undefined): string
```

### parse

```typescript
ASON.parse(text: string): ISendable | null | undefined
```

### 示例

```typescript
@Sendable
class Person {
  name: string = "";
  age: number = 0;
}

const person = new Person();
person.name = "Alice";
person.age = 30;

// 序列化
const json = ASON.stringify(person);
console.info(json);  // {"name":"Alice","age":30}

// 反序列化
const parsed = ASON.parse(json) as Person;
console.info(parsed.name);  // Alice
```

### 转换选项

```typescript
// 注册类型映射 (用于反序列化)
ASON.registerSendableClass("Person", Person);

// 带选项序列化
const options: ASON.StringifyOptions = {
  space: 2  // 缩进
};
const json = ASON.stringify(person, options);
```

---

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10200030 | 锁不存在 | 检查锁名称 |
| 10200031 | lockAsync 超时 | 检查死锁或增加超时 |
| 10200201 | 并发修改错误 | 使用 AsyncLock 保护 |

---

## 最佳实践

### 锁的使用原则

1. **最小化临界区**: 只锁必要的代码
2. **避免嵌套锁**: 防止死锁
3. **使用命名锁**: 跨模块共享时使用 `request("name")`
4. **设置超时**: 防止永久等待

### 锁的选择

| 场景 | 推荐 |
|------|------|
| 单对象保护 | 对象内部持有 AsyncLock |
| 多对象协调 | 使用命名锁 AsyncLock.request() |
| 读多写少 | 使用 SHARED 模式读，EXCLUSIVE 模式写 |
| 生产者消费者 | AsyncLock + ConditionVariable |
