# Worker API 精简参考

> 源文档: js-apis-worker.md (2500+ 行)

## 导入模块

```typescript
import { worker } from '@kit.ArkTS';
```

## 核心概念

- **宿主线程**: 创建 Worker 的线程 (通常是 UI 线程)
- **Worker 线程**: 独立的后台线程，不能操作 UI
- **最大数量**: 同一进程最多 64 个 Worker 线程

---

## ThreadWorker 类 (API 9+)

### 构造函数

```typescript
// 基本创建
const workerInstance = new worker.ThreadWorker("entry/ets/workers/Worker.ets");

// 带选项创建
const workerInstance = new worker.ThreadWorker("entry/ets/workers/Worker.ets", {
  name: "MyWorker",
  type: "classic",  // 'classic' | 'module'
  priority: worker.ThreadWorkerPriority.MEDIUM  // API 18+
});
```

### 文件路径规则

| 场景 | 路径格式 |
|------|----------|
| 同模块 | `entry/ets/workers/Worker.ets` |
| HSP 模块 | `hsp/ets/workers/Worker.ets` |
| HAR 模块 | `@ohos/library/ets/workers/Worker.ets` |

**注意**: Worker 文件需在 `build-profile.json5` 中配置

---

## 宿主线程 API

### 发送消息

```typescript
// 拷贝数据
workerInstance.postMessage(message: Object): void

// 转移 ArrayBuffer 所有权
workerInstance.postMessage(message: Object, transfer: ArrayBuffer[]): void

// 共享 Sendable 对象 (API 12+)
workerInstance.postMessageWithSharedSendable(message: Object, transfer?: ArrayBuffer[]): void
```

### 事件回调

```typescript
// 接收 Worker 消息
workerInstance.onmessage = (event: MessageEvents) => {
  console.info("Received:", event.data);
};

// 捕获所有异常 (推荐, API 18+)
workerInstance.onAllErrors = (error: ErrorEvent) => {
  console.error(`Error: ${error.message}`);
  // Worker 线程继续运行
};

// 捕获 onmessage 同步异常 (旧版)
workerInstance.onerror = (error: ErrorEvent) => {
  console.error(`Error: ${error.message}`);
  // Worker 线程进入销毁流程
};

// Worker 退出回调
workerInstance.onexit = (code: number) => {
  console.info(`Worker exited with code: ${code}`);
  // code: 0=正常, 1=异常
};

// 接收无法序列化的消息
workerInstance.onmessageerror = (event: MessageEvents) => {
  console.error("Message serialization error");
};
```

### 销毁 Worker

```typescript
// 销毁 Worker
workerInstance.terminate(): void
```

### 事件监听

```typescript
// 添加事件监听 (可多次执行)
workerInstance.on(type: string, listener: WorkerEventListener): void

// 添加一次性事件监听
workerInstance.once(type: string, listener: WorkerEventListener): void

// 移除事件监听
workerInstance.off(type: string, listener?: WorkerEventListener): void

// 触发事件
workerInstance.dispatchEvent(event: Event): boolean
```

### 全局调用 (API 11+)

```typescript
// 注册对象 (宿主线程)
workerInstance.registerGlobalCallObject("calculator", {
  add: (a: number, b: number) => a + b,
  subtract: (a: number, b: number) => a - b
});

// 取消注册
workerInstance.unregisterGlobalCallObject(instanceName: string): void
```

---

## Worker 线程 API

### workerPort 属性

```typescript
import { worker } from '@kit.ArkTS';

const workerPort = worker.workerPort;
```

### 接收/发送消息

```typescript
// 接收宿主线程消息
workerPort.onmessage = (event: MessageEvents) => {
  const data = event.data;
  // 处理数据...
  
  // 发送结果回宿主线程
  workerPort.postMessage({ result: "done" });
};

// 共享 Sendable 对象 (API 12+)
workerPort.postMessageWithSharedSendable(message: Object, transfer?: ArrayBuffer[]): void
```

### 错误处理

```typescript
workerPort.onerror = (err: ErrorEvent) => {
  console.error("Worker error:", err.message);
};

workerPort.onmessageerror = (event: MessageEvents) => {
  console.error("Message error");
};
```

### 关闭 Worker

```typescript
// 从 Worker 内部关闭
workerPort.close(): void
```

### 调用宿主线程方法 (API 11+)

```typescript
// 同步调用宿主线程注册的方法
const result = workerPort.callGlobalCallObjectMethod(
  instanceName: string,
  methodName: string, 
  timeout: number,
  ...args: Object[]
): Object
```

---

## 线程优先级 (API 18+)

```typescript
enum ThreadWorkerPriority {
  HIGH = 0,      // 用户触发任务，几秒内完成
  MEDIUM = 1,    // 默认优先级
  LOW = 2,       // 下载等后台任务
  IDLE = 3,      // 数据同步等不可见任务
  DEADLINE = 4,  // 页面加载等关键任务 (API 20+)
  VIP = 5        // UI/动画渲染任务 (API 20+)
}
```

---

## 完整示例

### 宿主线程 (Index.ets)

```typescript
import { worker, MessageEvents, ErrorEvent } from '@kit.ArkTS';

@Entry
@Component
struct Index {
  private workerInstance: worker.ThreadWorker | null = null;

  aboutToAppear() {
    // 创建 Worker
    this.workerInstance = new worker.ThreadWorker("entry/ets/workers/Worker.ets");

    // 接收消息
    this.workerInstance.onmessage = (event: MessageEvents) => {
      console.info("Result:", event.data);
    };

    // 错误处理
    this.workerInstance.onAllErrors = (err: ErrorEvent) => {
      console.error("Worker error:", err.message);
    };

    // 退出回调
    this.workerInstance.onexit = (code: number) => {
      console.info("Worker exited:", code);
    };
  }

  aboutToDisappear() {
    // 销毁 Worker
    this.workerInstance?.terminate();
  }

  build() {
    Button("Send Task")
      .onClick(() => {
        this.workerInstance?.postMessage({ type: "compute", data: 100 });
      })
  }
}
```

### Worker 线程 (Worker.ets)

```typescript
import { worker, MessageEvents, ErrorEvent } from '@kit.ArkTS';

const workerPort = worker.workerPort;

workerPort.onmessage = (event: MessageEvents) => {
  const msg = event.data;
  
  if (msg.type === "compute") {
    const result = msg.data * 2;
    workerPort.postMessage({ type: "result", value: result });
  }
};

workerPort.onerror = (err: ErrorEvent) => {
  console.error("Worker error:", err.message);
};
```

### ArrayBuffer 转移

```typescript
// 宿主线程
const buffer = new ArrayBuffer(1024);
workerInstance.postMessage(buffer, [buffer]);
// buffer 现在不可用

// Worker 线程
workerPort.onmessage = (event: MessageEvents) => {
  const buffer: ArrayBuffer = event.data;
  const view = new Int8Array(buffer);
  // 处理数据...
};
```

### Sendable 对象共享 (API 12+)

```typescript
// sendable.ets
@Sendable
export class SharedData {
  value: number = 0;
}

// 宿主线程
import { SharedData } from './sendable';

const data = new SharedData();
data.value = 100;
workerInstance.postMessageWithSharedSendable(data);

// Worker 线程
workerPort.onmessage = (event: MessageEvents) => {
  const data: SharedData = event.data;
  console.info("Shared value:", data.value); // 100
};
```

---

## onAllErrors vs onerror

| 特性 | onAllErrors (API 18+) | onerror |
|------|----------------------|---------|
| 捕获范围 | Worker 生命周期内所有异常 | 仅 onmessage 同步异常 |
| 异常后行为 | Worker 继续运行 | Worker 进入销毁 |
| 推荐程度 | **推荐使用** | 旧版兼容 |

---

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10200003 | Worker 初始化失败 | 检查数量限制和路径 |
| 10200004 | Worker 未运行 | 确保未销毁 |
| 10200005 | API 不支持 | 使用 Worker 支持的 API |
| 10200006 | 序列化异常 | 检查数据类型 |
| 10200007 | 文件路径无效 | 检查路径格式 |
| 10200019 | 对象未注册 | 先调用 registerGlobalCallObject |
| 10200020 | 方法类型错误 | 确保是同步可调用方法 |
| 10200021 | 调用超时 | 避免耗时方法 |

---

## build-profile.json5 配置

```json5
{
  "buildOption": {
    "sourceOption": {
      "workers": [
        "./src/main/ets/workers/Worker.ets"
      ]
    }
  }
}
```
