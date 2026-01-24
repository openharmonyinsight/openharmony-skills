# TaskPool API 精简参考

> 源文档: js-apis-taskpool.md (2700+ 行)

## 导入模块

```typescript
import { taskpool } from '@kit.ArkTS';
```

## 核心 API 速查表

### 任务执行

| API | 说明 | 版本 |
|-----|------|------|
| `execute(func, ...args)` | 直接执行函数 | 9+ |
| `execute(task, priority?)` | 执行 Task 对象 | 9+ |
| `execute(group, priority?)` | 执行 TaskGroup | 10+ |
| `executeDelayed(delay, task, priority?)` | 延时执行任务 | 11+ |
| `executePeriodically(period, task, priority?)` | 周期执行任务 | 12+ |

### 任务控制

| API | 说明 | 版本 |
|-----|------|------|
| `cancel(task)` | 取消任务 | 9+ |
| `cancel(group)` | 取消任务组 | 10+ |
| `terminateTask(task)` | 终止长时任务 | 12+ |
| `isConcurrent(func)` | 检查函数是否有 @Concurrent | 12+ |
| `getTaskPoolInfo()` | 获取线程池信息 | 10+ |

---

## Task 类

### 构造函数

```typescript
// 基本构造
new taskpool.Task(func: Function, ...args: Object[])

// 命名任务
new taskpool.Task(name: string, func: Function, ...args: Object[])

// 泛型任务 (API 13+)
new taskpool.GenericsTask<A, R>(func: (...args: A) => R, ...args: A)
```

### Task 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `taskId` | number | 任务 ID (只读) |
| `name` | string | 任务名称 |
| `totalDuration` | number | 总耗时 (只读, API 12+) |
| `ioDuration` | number | IO 耗时 (只读, API 12+) |
| `cpuDuration` | number | CPU 耗时 (只读, API 12+) |

### Task 方法

```typescript
// 设置转移列表 (零拷贝，转移所有权)
task.setTransferList(list: ArrayBuffer[]): void

// 设置拷贝列表 (复制数据)
task.setCloneList(list: ArrayBuffer[]): void

// 添加/移除依赖 (API 11+)
task.addDependency(task: Task): void
task.removeDependency(task: Task): void

// 注册回调
task.onReceiveData(callback: Function): void  // 接收数据
task.onExecutionSucceeded(callback: Function): void  // 成功回调 (API 12+)
task.onExecutionFailed(callback: Function): void     // 失败回调 (API 12+)

// 静态方法 - 向宿主线程发送数据
Task.sendData(...args: Object[]): void
```

---

## TaskGroup 类 (API 10+)

```typescript
// 创建任务组
const group = new taskpool.TaskGroup();
const group = new taskpool.TaskGroup("groupName");

// 添加任务
group.addTask(func: Function, ...args: Object[]): void
group.addTask(task: Task): void

// 执行
taskpool.execute(group, taskpool.Priority.HIGH).then((results: Object[]) => {
  // results 是所有任务结果的数组
});
```

---

## SequenceRunner 串行队列 (API 11+)

```typescript
// 创建串行队列
const runner = new taskpool.SequenceRunner();
const runner = new taskpool.SequenceRunner("runnerName");

// 执行任务 (按顺序)
runner.execute(task: Task): Promise<Object>
```

---

## AsyncRunner 异步队列 (API 18+)

```typescript
// 创建异步队列: 名称, 并发数, 队列大小
const asyncRunner = new taskpool.AsyncRunner("camera", 5, 10);

// 执行任务
asyncRunner.execute(task: Task): Promise<Object>

// 取消任务
asyncRunner.cancel(task: Task): void
```

---

## LongTask 长时任务 (API 12+)

```typescript
// 创建长时任务
const longTask = new taskpool.LongTask(func, ...args);

// 执行
taskpool.execute(longTask);

// 终止
taskpool.terminateTask(longTask);
```

**注意**: 长时任务仅支持执行一次

---

## Priority 优先级枚举

| 优先级 | 值 | 说明 |
|--------|----|----|
| `HIGH` | 0 | 高优先级，优先执行 |
| `MEDIUM` | 1 | 中优先级 (默认) |
| `LOW` | 2 | 低优先级 |
| `IDLE` | 3 | 后台任务，所有线程空闲时执行 |

---

## @Concurrent 装饰器

```typescript
@Concurrent
function myTask(arg1: number, arg2: string): number {
  // 任务逻辑
  return arg1;
}
```

### 装饰器约束

| 约束 | 说明 |
|------|------|
| 函数类型 | async 函数或普通函数。禁止箭头函数、类方法 |
| 变量访问 | 仅允许局部变量、入参、import 引入的变量 |
| 闭包 | **禁止使用闭包变量** |
| 使用场景 | 仅 Stage 模型 .ets 文件 |

---

## 常用代码示例

### 基本任务执行

```typescript
@Concurrent
function add(a: number, b: number): number {
  return a + b;
}

// 方式1: 直接执行函数
taskpool.execute(add, 1, 2).then((result) => {
  console.info(`Result: ${result}`); // 3
});

// 方式2: 创建 Task 对象
const task = new taskpool.Task(add, 1, 2);
taskpool.execute(task, taskpool.Priority.HIGH).then((result) => {
  console.info(`Result: ${result}`);
});
```

### 任务组并行执行

```typescript
@Concurrent
function process(data: number): number {
  return data * 2;
}

const group = new taskpool.TaskGroup();
group.addTask(process, 10);
group.addTask(process, 20);
group.addTask(process, 30);

taskpool.execute(group).then((results: Object[]) => {
  console.info(`Results: ${results}`); // [20, 40, 60]
});
```

### 延时执行

```typescript
@Concurrent
function delayedTask(): void {
  console.info("Delayed task executed");
}

const task = new taskpool.Task(delayedTask);
taskpool.executeDelayed(2000, task); // 2秒后执行
```

### 周期执行

```typescript
@Concurrent
function periodicTask(): void {
  console.info("Periodic: " + Date.now());
}

const task = new taskpool.Task(periodicTask);
taskpool.executePeriodically(1000, task); // 每秒执行

// 取消周期任务
taskpool.cancel(task);
```

### 任务间通信

```typescript
@Concurrent
function taskWithCallback(): void {
  // 向宿主线程发送数据
  taskpool.Task.sendData("progress", 50);
  taskpool.Task.sendData("progress", 100);
}

const task = new taskpool.Task(taskWithCallback);
task.onReceiveData((data1: string, data2: number) => {
  console.info(`Received: ${data1} - ${data2}`);
});
taskpool.execute(task);
```

### ArrayBuffer 转移/拷贝

```typescript
@Concurrent
function processBuffer(buf: ArrayBuffer): number {
  return buf.byteLength;
}

const buffer = new ArrayBuffer(1024);
const task = new taskpool.Task(processBuffer, buffer);

// 转移 (零拷贝，原 buffer 不可用)
task.setTransferList([buffer]);

// 或拷贝 (原 buffer 仍可用)
// task.setCloneList([buffer]);

taskpool.execute(task);
```

### 任务依赖

```typescript
@Concurrent
function taskA(): string { return "A done"; }

@Concurrent
function taskB(): string { return "B done"; }

const a = new taskpool.Task(taskA);
const b = new taskpool.Task(taskB);

// B 依赖 A (A 先执行)
b.addDependency(a);

taskpool.execute(a);
taskpool.execute(b); // 等待 A 完成后执行
```

---

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10200006 | 序列化异常 | 检查参数是否可序列化 |
| 10200014 | 函数未标记 @Concurrent | 添加 @Concurrent 装饰器 |
| 10200015 | 取消的任务不存在 | 确保任务已提交且未完成 |
| 10200016 | 任务正在执行 | 无法取消执行中的任务 |
| 10200028 | 延时时间 < 0 | 设置 delayTime >= 0 |
| 10200029 | ArrayBuffer 冲突 | 不能同时设置 transfer 和 clone |
| 10200050 | 周期任务已执行 | 周期任务只能执行一次 |
| 10200051 | 周期任务重复执行 | 创建新 Task 对象 |

---

## 性能约束

| 约束 | 限制值 | 说明 |
|------|--------|------|
| 任务执行时长 | < 3 分钟 | 不含 async/await 耗时 |
| 数据传输大小 | 16 MB | 序列化传输限制 |
| 线程数量 | CPU 核数 | 自动扩缩容 |
| 任务开销 | 1-2 ms/任务 | 小任务建议批量处理 |
