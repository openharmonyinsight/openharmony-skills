# @ohos.test.PerfTest

**模块**: PerfTest
**API 版本**: 20+
**导入方式**: `import { PerfTest, PerfMetric, PerfTestStrategy, PerfMeasureResult } from '@kit.TestKit';`

## 概述

白盒性能测试框架。自动执行测试代码段并收集性能指标：
- 执行耗时
- CPU 负载/使用率
- 内存（RSS/PSS）
- 应用启动延迟
- 页面切换延迟
- 列表滚动 FPS

**重要提示**：
- 只能在 JsUnit 上下文中使用
- 不支持并发调用
- 始终在 actionCode 中调用 `finish(boolean)` 回调
- 始终调用 `destroy()` 清理资源

## PerfMetric 枚举

可收集的性能指标。

| 值 | 名称 | 描述 | 单位 |
|-------|------|-------------|------|
| 0 | DURATION | 代码执行时间 | 毫秒 |
| 1 | CPU_LOAD | 进程 CPU 负载 | 百分比 |
| 2 | CPU_USAGE | 进程 CPU 使用率 | 百分比 |
| 3 | MEMORY_RSS | 物理内存（含共享库） | KB |
| 4 | MEMORY_PSS | 物理内存（不含共享库） | KB |
| 5 | APP_START_RESPONSE_TIME | 应用启动响应延迟 | 毫秒 |
| 6 | APP_START_COMPLETE_TIME | 应用启动完成延迟 | 毫秒 |
| 7 | PAGE_SWITCH_COMPLETE_TIME | 页面切换完成延迟 | 毫秒 |
| 8 | LIST_SWIPE_FPS | 列表滚动帧率 | fps |

## PerfTestStrategy

性能测试配置对象。

```typescript
interface PerfTestStrategy {
  metrics: Array<PerfMetric>;              // 必需：要收集的指标
  actionCode: Callback<Callback<boolean>>; // 必需：测试代码段
  resetCode?: Callback<Callback<boolean>>; // 可选：清理代码
  bundleName?: string;                     // 可选：目标应用包名
  iterations?: number;                     // 可选：迭代次数（默认：5）
  timeout?: number;                        // 可选：单次执行超时（默认：10000ms）
}
```

### 字段说明

- **metrics**（必需）：要测试的指标数组
- **actionCode**（必需）：测试代码段。必须调用 `finish(boolean)` 回调。
- **resetCode**（可选）：测试完成后的清理代码。框架运行时不执行。
- **bundleName**（可选）：目标应用包名。默认为当前应用。
- **iterations**（可选）：测试迭代次数。默认为 5。
- **timeout**（可选）：actionCode/resetCode 执行超时时间（毫秒）。默认为 10000。

## PerfTest 类

性能测试的入口点。

### static create()

```typescript
static create(strategy: PerfTestStrategy): PerfTest
```

创建 PerfTest 实例。

**参数**：
- `strategy: PerfTestStrategy` - 测试配置

**返回值**: `PerfTest` 实例

**示例**：
```typescript
import { PerfTest, PerfMetric, PerfTestStrategy } from '@kit.TestKit';

let metrics: Array<PerfMetric> = [PerfMetric.DURATION];
let actionCode = async (finish: Callback<boolean>) => {
  // 测试代码
  finish(true);
};

let strategy: PerfTestStrategy = {
  metrics: metrics,
  actionCode: actionCode,
  iterations: 10
};

let perfTest = PerfTest.create(strategy);
```

### run()

```typescript
run(): Promise<void>
```

运行性能测试，迭代执行代码并收集指标。

**示例**：
```typescript
await perfTest.run();
```

### getMeasureResult()

```typescript
getMeasureResult(metric: PerfMetric): PerfMeasureResult
```

获取指定指标的测量数据。

**参数**：
- `metric: PerfMetric` - 要查询的指标

**返回值**: 包含测量数据的 `PerfMeasureResult`

**示例**：
```typescript
let result = perfTest.getMeasureResult(PerfMetric.DURATION);
console.info(`平均耗时: ${result.average}ms`);
console.info(`最小: ${result.minimum}ms, 最大: ${result.maximum}ms`);
```

### destroy()

```typescript
destroy(): void
```

销毁 PerfTest 实例并释放资源。

**示例**：
```typescript
perfTest.destroy();
```

## PerfMeasureResult

指标的测量结果数据。

```typescript
interface PerfMeasureResult {
  metric: PerfMetric;       // 被测量的指标
  roundValues: number[];    // 每轮的原始值（失败则为 -1）
  maximum: number;          // 最大值（不包括 -1）
  minimum: number;          // 最小值（不包括 -1）
  average: number;          // 平均值（不包括 -1）
}
```

## 完整示例

### 基础耗时测试

```typescript
import { PerfTest, PerfMetric, PerfTestStrategy } from '@kit.TestKit';

async function testDuration() {
  let num = 0;
  let actionCode = async (finish: Callback<boolean>) => {
    // 要测试的代码
    for (let i = 0; i < 10000; i++) {
      num++;
    }
    finish(true);  // 必须调用 finish！
  };

  let strategy: PerfTestStrategy = {
    metrics: [PerfMetric.DURATION],
    actionCode: actionCode,
    iterations: 10
  };

  let perfTest = PerfTest.create(strategy);
  await perfTest.run();

  let result = perfTest.getMeasureResult(PerfMetric.DURATION);
  console.info(`平均执行时间: ${result.average}ms`);
  console.info(`最小: ${result.minimum}ms, 最大: ${result.maximum}ms`);

  perfTest.destroy();
}
```

### 多指标测试带清理

```typescript
async function testWithCleanup() {
  let data = new Array(1000);

  let actionCode = async (finish: Callback<boolean>) => {
    // 执行操作
    for (let i = 0; i < 1000; i++) {
      data[i] = i * i;
    }
    finish(true);
  };

  let resetCode = async (finish: Callback<boolean>) => {
    // 测试后清理
    data.length = 0;
    finish(true);
  };

  let strategy: PerfTestStrategy = {
    metrics: [
      PerfMetric.DURATION,
      PerfMetric.CPU_USAGE,
      PerfMetric.MEMORY_PSS
    ],
    actionCode: actionCode,
    resetCode: resetCode,
    iterations: 5
  };

  let perfTest = PerfTest.create(strategy);
  await perfTest.run();

  // 获取每个指标的结果
  let duration = perfTest.getMeasureResult(PerfMetric.DURATION);
  let cpu = perfTest.getMeasureResult(PerfMetric.CPU_USAGE);
  let memory = perfTest.getMeasureResult(PerfMetric.MEMORY_PSS);

  console.info(`耗时: ${duration.average}ms`);
  console.info(`CPU: ${cpu.average}%`);
  console.info(`内存: ${memory.average}KB`);

  perfTest.destroy();
}
```

### 应用启动延迟

```typescript
async function testAppStartup() {
  let actionCode = async (finish: Callback<boolean>) => {
    // 触发应用启动的代码
    // 框架将收集 APP_START_RESPONSE_TIME 和 APP_START_COMPLETE_TIME
    finish(true);
  };

  let strategy: PerfTestStrategy = {
    metrics: [
      PerfMetric.APP_START_RESPONSE_TIME,
      PerfMetric.APP_START_COMPLETE_TIME
    ],
    actionCode: actionCode,
    bundleName: 'com.example.app',  // 目标应用
    iterations: 3
  };

  let perfTest = PerfTest.create(strategy);
  await perfTest.run();

  let responseTime = perfTest.getMeasureResult(PerfMetric.APP_START_RESPONSE_TIME);
  let completeTime = perfTest.getMeasureResult(PerfMetric.APP_START_COMPLETE_TIME);

  console.info(`响应时间: ${responseTime.average}ms`);
  console.info(`完成时间: ${completeTime.average}ms`);

  perfTest.destroy();
}
```

### 页面切换延迟

```typescript
async function testPageSwitch() {
  let actionCode = async (finish: Callback<boolean>) => {
    // 导航到页面
    // 框架收集 PAGE_SWITCH_COMPLETE_TIME
    finish(true);
  };

  let strategy: PerfTestStrategy = {
    metrics: [PerfMetric.PAGE_SWITCH_COMPLETE_TIME],
    actionCode: actionCode,
    iterations: 5
  };

  let perfTest = PerfTest.create(strategy);
  await perfTest.run();

  let result = perfTest.getMeasureResult(PerfMetric.PAGE_SWITCH_COMPLETE_TIME);
  console.info(`页面切换时间: ${result.average}ms`);

  perfTest.destroy();
}
```

### 列表滚动 FPS

```typescript
async function testListScroll() {
  let actionCode = async (finish: Callback<boolean>) => {
    // 触发列表滚动
    // 框架收集 LIST_SWIPE_FPS
    finish(true);
  };

  let strategy: PerfTestStrategy = {
    metrics: [PerfMetric.LIST_SWIPE_FPS],
    actionCode: actionCode,
    iterations: 3
  };

  let perfTest = PerfTest.create(strategy);
  await perfTest.run();

  let result = perfTest.getMeasureResult(PerfMetric.LIST_SWIPE_FPS);
  console.info(`列表滚动 FPS: ${result.average}`);

  perfTest.destroy();
}
```

## 指标说明

### CPU 和内存指标
- 仅收集指定应用进程的数据
- 在代码执行前后收集 CPU 和内存数据
- 确保测试期间应用进程存在

### 启动延迟指标
- 受系统日志上报影响
- 起始时间：点击事件上报时
- 响应时间结束：点击后首帧显示时
- 完成时间结束：应用启动后首帧显示时
- 延迟与用户感知不同
- 每次测试仅收集首次启动延迟
- 场景：主屏幕图标、dock 栏图标、应用中心图标

### 页面切换延迟
- 受系统日志上报影响
- 起始时间：点击事件上报时
- 结束时间：页面切换后首帧显示时
- 适用于 Router 和 Navigation 组件
- 每次测试仅收集首次页面切换延迟

### 列表滚动 FPS
- 滚动时每秒渲染/更新的帧数
- 支持：List、Grid、Scroll、WaterFlow 组件
- 每次测试仅收集首次滚动 FPS

## 错误码

| 代码 | 消息 | 原因 |
|------|---------|-------|
| 32400001 | 初始化失败 | 初始化 PerfTest 失败 |
| 32400002 | 内部错误 | IPC 连接失败或对象不存在 |
| 32400003 | 参数验证失败 | 参数无效 |
| 32400004 | 回调执行失败 | 回调异常或超时 |
| 32400005 | 指标数据收集失败 | 数据收集失败 |
| 32400006 | 获取测量结果失败 | 结果获取失败 |
| 32400007 | API 不支持并发调用 | 检测到并发 API 调用 |

## 最佳实践

1. **始终调用 finish()**：必须调用回调以通知完成
2. **成功使用 finish(true)**，失败使用 `finish(false)`
3. **使用 destroy() 清理**：始终释放 PerfTest 资源
4. **选择合适的迭代次数**：更多迭代 = 更准确的数据，但测试时间更长
5. **处理超时**：根据预期执行时间设置适当的超时
6. **检查 -1 值**：表示 roundValues 中的数据收集失败

```typescript
// 示例：处理失败
let result = perfTest.getMeasureResult(PerfMetric.DURATION);
let successCount = result.roundValues.filter(v => v !== -1).length;
console.info(`成功测量: ${successCount}/${result.roundValues.length}`);
```
