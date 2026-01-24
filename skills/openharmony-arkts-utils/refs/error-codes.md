# 语言基础类库错误码速查表

> 源文档: `docs-OpenHarmony-v6.0-Release/zh-cn/application-dev/reference/apis-arkts/errorcode-utils.md`  
> 通用错误码请参考 `errorcode-universal.md`

---

## 错误码速查表

| 错误码 | 错误信息 | 常见原因 | 处理方法 |
|--------|----------|----------|----------|
| **10200001** | The value of ${param} is out of range | 索引越界 | 检查索引范围 |
| **10200002** | Invalid ${param} string | 字符串解析失败 | 检查字符串格式 |
| **10200003** | Worker initialization failed | Worker初始化失败 | 检查Worker数量(<8)或配置 |
| **10200004** | The Worker instance is not running | Worker已销毁 | 确保Worker运行中 |
| **10200005** | API not supported in worker thread | Worker不支持该API | 使用Worker支持的API |
| **10200006** | Serialization exception | 序列化失败 | 检查数据是否可序列化 |
| **10200007** | Invalid worker file path | Worker路径错误 | 检查Worker文件路径 |
| **10200009** | Buffer size must be multiple of ${size} | Buffer长度错误 | 确保长度为16/32/64位整数倍 |
| **10200010** | Container is empty | 容器为空 | 先向容器添加元素 |
| **10200011** | Method cannot be bound | 方法不支持bind | 不要对容器方法使用bind |
| **10200012** | Constructor cannot be directly invoked | 未用new创建 | 使用new关键字创建实例 |
| **10200013** | Property has only getter | 只读属性被修改 | 不要修改只读属性 |
| **10200014** | Function not marked as concurrent | 缺少@Concurrent | 添加@Concurrent装饰器 |
| **10200015** | Task to cancel does not exist | 取消不存在的任务 | 确保任务在任务池中 |
| **10200016** | Task to cancel is being executed | 取消执行中的任务 | 只能取消等待中的任务 |
| **10200017** | Element does not exist | 删除不存在的元素 | 确保元素存在 |
| **10200018** | Task group to cancel does not exist | 任务组不存在 | 确保任务组在任务池中 |
| **10200019** | globalCallObject not registered | 对象未注册 | 先注册对象再调用 |
| **10200020** | Method not callable/async/generator | 调用方法类型错误 | 确保方法可调用且非异步 |
| **10200021** | Global call timed out | 调用超时(默认5s) | 避免调用耗时方法 |
| **10200022** | Not called in TaskPool thread | 非TaskPool线程调用 | 确保在TaskPool线程中执行 |
| **10200023** | Not called in concurrent function | 非并发函数中调用 | 确保在并发函数内部调用 |
| **10200024** | Callback not registered on host | 回调未注册 | 先在宿主线程注册回调 |
| **10200025** | Dependent task not allowed | 串行队列中添加依赖任务 | 使用removeDependency删除依赖 |
| **10200026** | Circular dependency | 循环依赖 | 删除循环依赖关系 |
| **10200027** | Dependency does not exist | 依赖不存在 | 先addDependency再remove |
| **10200028** | delayTime is less than zero | 延时<0 | 确保延时>=0 |
| **10200029** | ArrayBuffer in both transfer and clone | 同时设置转移和克隆 | 只设置一种 |
| **10200030** | Lock does not exist | 锁不存在 | 使用正确的锁名称 |
| **10200031** | Timeout exceeded | lockAsync超时 | 检查死锁/循环依赖 |
| **10200034** | Task does not support listeners | 监听未注册 | 在执行前注册回调 |
| **10200035** | doWrite not implemented | 未实现doWrite | 实现doWrite接口 |
| **10200036** | Stream has been ended | 流已结束仍写入 | 不在end后写入 |
| **10200037** | Callback invoked multiple times | 多次调用callback | 确保callback只调用一次 |
| **10200038** | doRead not implemented | 未实现doRead | 实现doRead接口 |
| **10200039** | doTransform not implemented | 未实现doTransform | 实现doTransform接口 |
| **10200050** | Task already executed | 已执行的任务无法周期执行 | 使用新任务 |
| **10200051** | Periodic task cannot execute again | 周期任务重复执行 | 不要重复执行周期任务 |
| **10200052** | Periodic task cannot have dependency | 周期任务不能有依赖 | 不给周期任务添加依赖 |
| **10200054** | AsyncRunner task discarded | 等待队列溢出 | 增加队列容量/优化任务 |
| **10200055** | AsyncRunner task canceled | 异步任务被取消 | 捕获异常处理 |
| **10200056** | Task executed by AsyncRunner | 异步任务不能有依赖 | 不给异步队列任务添加依赖 |
| **10200057** | Task cannot be executed by two APIs | 任务被两种API执行 | 确保任务只用一种方式执行 |
| **10200060** | Precision limit exceeded | Decimal精度超限 | 使用Decimal.set设置精度 |
| **10200061** | crypto unavailable | 加密方法不可用 | Decimal.set({crypto:false}) |
| **10200062** | XML length exceeded 100000 | XML累积长度超限 | 减小参数长度 |
| **10200063** | Illegal position for xml | XML声明/属性位置错误 | 按XML标准设置位置 |
| **10200064** | Cannot be empty string | 入参字符串为空 | 传入非空字符串 |
| **10200065** | No match between start/end Element | 元素标记未匹配 | 先startElement后endElement |
| **10200066** | Incorrect encoding, only utf-8 | 编码格式错误 | 使用utf-8编码 |
| **10200068** | ArrayBuffer is null or detach | ArrayBuffer已分离 | 确保ArrayBuffer可用 |
| **10200201** | Concurrent modification error | 并发修改容器 | 使用异步锁保护 |
| **10200301** | Loading native module failed | 加载native模块失败 | 检查模块路径和内容 |

---

## 常见场景错误处理

### TaskPool 相关 (10200014-10200028, 10200050-10200057)

```ts
import { taskpool } from '@kit.ArkTS';

// 错误: 函数未标记 @Concurrent (10200014)
// function myTask() { ... }

// 正确:
@Concurrent
function myTask(): string {
  return "result";
}

// 取消任务需捕获异常 (10200015/10200016)
let task = new taskpool.Task(myTask);
taskpool.execute(task);
try {
  taskpool.cancel(task);
} catch (e) {
  console.error("Cancel failed:", e.code);
}
```

### Worker 相关 (10200003-10200007)

```ts
import { worker } from '@kit.ArkTS';

// 错误: Worker数量超过8个 (10200003)
// 正确: 及时销毁空闲Worker
let w = new worker.ThreadWorker("entry/ets/workers/Worker.ets");
// 使用完毕后
w.terminate();

// 路径错误 (10200007)
// 确保路径格式正确，参考API文档
```

### 容器相关 (10200010-10200012, 10200017, 10200201)

```ts
import { ArrayList, HashMap } from '@kit.ArkTS';

// 错误: 容器为空时操作 (10200010)
let list = new ArrayList<number>();
// list.removeByIndex(0);  // Error!

// 正确: 先添加元素
list.add(1);
list.removeByIndex(0);

// 错误: 并发修改 (10200201)
// 正确: 使用异步锁保护共享容器
import { ArkTSUtils } from '@kit.ArkTS';
let lock = new ArkTSUtils.locks.AsyncLock();
await lock.lockAsync(() => {
  // 安全操作容器
});
```

### 异步锁相关 (10200030-10200031)

```ts
import { ArkTSUtils } from '@kit.ArkTS';

// 超时处理 (10200031)
let lock = new ArkTSUtils.locks.AsyncLock();
try {
  await lock.lockAsync(() => {
    // 操作
  }, ArkTSUtils.locks.AsyncLockMode.EXCLUSIVE, { timeout: 5000 });
} catch (e) {
  if (e.code === 10200031) {
    console.error("Lock timeout - possible deadlock");
  }
}
```

---

## 通用错误码 (401)

| 错误信息 | 说明 |
|----------|------|
| Mandatory parameters are left unspecified | 必填参数缺失 |
| Incorrect parameter types | 参数类型错误 |
| Parameter verification failed | 参数校验失败 |

```ts
// 示例: 参数错误 (401)
let list = new ArrayList<number>();
// list.insert("string", 0);  // 类型错误
list.insert(1, 0);  // 正确
```
