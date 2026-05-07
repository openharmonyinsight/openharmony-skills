# PerfTest 模块配置

> **模块信息**
> - 所属子系统: testfwk
> - 模块名称: PerfTest（性能测试框架）
> - Kit 包: @kit.TestKit
> - API 声明文件: @ohos.test.PerfTest.d.ts
> - 版本: 2.0.0
> - 更新日期: 2026-04-02

## 一、模块概述

PerfTest 是 OpenHarmony 的性能测试框架（API 20 引入），用于测量应用和接口的性能指标。

- **SysCap**: `SystemCapability.Test.PerfTest`
- **适用设备**: Phone, Tablet, PC/2in1, Smart Screen, Vehicle
- **不支持并发调用**（错误码 32400007）

## 二、模块特有配置

### 2.1 通用配置继承

本模块继承 testfwk 子系统通用配置：
- **测试路径规范**: 见 `../_common.md` 第 2.1 节
- **导入规范**: 见 `../_common.md` 第 2.3 节
- **通用测试规则**: 见 `../_common.md` 第 2.4 节

### 2.2 模块特有规则

#### 2.2.1 状态机约束（强制）

PerfTest 有严格的调用顺序，违反顺序会触发错误码：

```
PerfTest.create(strategy) → run() → getMeasureResult(metric) → destroy()
```

| 违规操作 | 错误码 | 说明 |
|---------|--------|------|
| run() 未完成就调用 getMeasureResult() | 32400006 | 测试数据未采集完成 |
| destroy() 后调用任何方法 | 32400002 | 对象已销毁 |
| 未使用 await 调用 run() | 32400007 | 异步接口未 await 导致并发 |

#### 2.2.2 actionCode 规则（强制）

`PerfTestStrategy.actionCode` 必须调用 `finish` 回调，否则超时触发 32400004：

```typescript
let actionCode = async (finish: Callback<boolean>) => {
    // 被测代码
    finish(true);  // 必须调用
};
```

#### 2.2.3 destroy() 建议

`destroy()` 用于释放 PerfTest 对象内存。文档使用"可以"而非"必须"，建议调用但非强制。

#### 2.2.4 测试环境要求

- 必须在真实设备上执行
- 避免其他进程干扰
- 需确保目标应用进程存在（CPU/Memory 指标采集依赖应用进程）

### 2.3 PerfMetric 指标限制

| 指标 | 值 | 单位 | 限制说明 |
|------|---|------|---------|
| DURATION | 0 | ms | 无特殊限制 |
| CPU_LOAD | 1 | % | 采集前后需 app 进程存在 |
| CPU_USAGE | 2 | % | 采集前后需 app 进程存在 |
| MEMORY_RSS | 3 | KB | 含共享库的物理内存 |
| MEMORY_PSS | 4 | KB | 不含共享库的物理内存 |
| APP_START_RESPONSE_TIME | 5 | ms | 仅首次启动，场景有限 |
| APP_START_COMPLETE_TIME | 6 | ms | 仅首次启动，场景有限 |
| PAGE_SWITCH_COMPLETE_TIME | 7 | ms | 仅首次切换，仅 Router/Navigation |
| LIST_SWIPE_FPS | 8 | fps | 仅首次滑动，仅 List/Grid/Scroll/WaterFlow |

## 三、模块 API 列表

### 3.1 PerfTest 类

| API | 签名 | 返回类型 | 说明 |
|-----|------|---------|------|
| create | `static create(strategy: PerfTestStrategy): PerfTest` | PerfTest | 静态工厂方法 |
| run | `run(): Promise<void>` | Promise\<void\> | 执行性能测试（按 iterations 重复） |
| getMeasureResult | `getMeasureResult(metric: PerfMetric): PerfMeasureResult` | PerfMeasureResult | 获取测量结果（同步） |
| destroy | `destroy(): void` | void | 销毁对象释放内存（同步） |

### 3.2 PerfTestStrategy 接口

| 属性 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| metrics | Array\<PerfMetric\> | 是 | — | 要测量的指标列表 |
| actionCode | Callback\<Callback\<boolean\>\> | 是 | — | 被测代码段（必须调用 finish） |
| resetCode | Callback\<Callback\<boolean\>\> | 否 | null | 重置代码（不采集指标） |
| bundleName | string | 否 | "" | 目标应用包名 |
| iterations | number | 否 | 5 | 测试迭代次数 |
| timeout | number | 否 | 10000 | 单次 actionCode/resetCode 超时(ms) |

### 3.3 PerfMeasureResult 接口

| 属性 | 类型 | 说明 |
|------|------|------|
| metric | PerfMetric | 被测量的指标 |
| roundValues | Array\<number\> | 每轮值（失败轮为 -1） |
| maximum | number | 最大值（排除 -1） |
| minimum | number | 最小值（排除 -1） |
| average | number | 平均值（排除 -1） |

## 四、模块内 API 关联关系

### 4.1 组合关系

| 被测 API | 依赖的接口 | 依赖属性 | 测试影响 |
|---------|-----------|---------|---------|
| PerfTest.create(strategy) | PerfTestStrategy | metrics, actionCode | 必须构造完整 strategy 对象 |
| PerfTestStrategy | PerfMetric (enum) | metrics 属性 | 必须指定至少一个指标 |
| PerfTestStrategy | Callback\<Callback\<boolean\>\> | actionCode 属性 | actionCode 签名必须匹配 |

### 4.2 工厂关系

| 工厂方法 | 产出类型 | 所在模块 |
|---------|---------|---------|
| PerfTest.create(strategy) | PerfTest | PerfTest |
| PerfTest.getMeasureResult(metric) | PerfMeasureResult | PerfTest |

### 4.3 共享类型

| 类型名称 | 使用该类型的 API |
|---------|----------------|
| PerfMetric (enum) | PerfTestStrategy.metrics, PerfMeasureResult.metric |
| Callback\<boolean\> | PerfTestStrategy.actionCode, PerfTestStrategy.resetCode |

## 五、模块跨子系统依赖

| 本模块 API | 依赖的外部子系统 | 外部类型 | 测试处理方式 |
|-----------|----------------|---------|------------|
| PerfTest 测试代码 | @kit.BasicServicesKit | BusinessError（仅类型） | catch 中使用 `error: BusinessError` |
| PerfTest 测试代码 | @kit.BasicServicesKit | Callback（仅类型） | actionCode 签名中使用 |
| PerfTest 测试代码 | @ohos.app.ability.abilityDelegatorRegistry | getAbilityDelegator | 启动辅助应用 |
| PerfTest 测试代码 | @ohos.UiTest | Driver, ON | 操作辅助应用 perftestScene |

## 六、错误码映射

| 错误码 | 含义 | 触发条件 | 可测性 |
|-------|------|---------|--------|
| 32400001 | 初始化失败 | 无法获取测试应用包名 | ❌ 测试环境中默认可初始化 |
| 32400002 | 内部错误 | IPC 失败或对象已销毁 | ✅ destroy() 后调用方法 |
| 32400003 | 参数校验失败 | 传入非法参数 | ✅ 传入 null/undefined/无效值 |
| 32400004 | callback 执行失败 | callback 异常或超时 | ✅ actionCode 不调用 finish |
| 32400005 | 指标采集失败 | 目标应用进程不存在 | ⚠️ 需特定环境 |
| 32400006 | 获取结果失败 | run() 未完成就调用 getMeasureResult | ✅ 跳过 run() 直接调用 |
| 32400007 | 不支持并发 | 异步接口未 await | ✅ 不 await 调用 run() |

## 七、测试模板

### 7.1 标准功能测试模板

来源：`test/xts/acts/testfwk/perftest/entry/src/ohosTest/ets/test/PerfTest.test.ets`

```typescript
import { describe, beforeAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
import { Driver, ON } from '@ohos.UiTest';
import { PerfMetric, PerfTest, PerfTestStrategy, PerfMeasureResult } from '@kit.TestKit';
import { BusinessError, Callback } from '@kit.BasicServicesKit';

export default function PerfTestTest() {
  describe('PerfTestTest', () => {
    beforeAll(async (done: Function) => { done() })

    it('testPerfTestCalculate', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
      let metrics: Array<PerfMetric> = [PerfMetric.DURATION, PerfMetric.CPU_LOAD, PerfMetric.CPU_USAGE,
                                          PerfMetric.MEMORY_RSS, PerfMetric.MEMORY_PSS];
      let actionCode = async (finish: Callback<boolean>) => {
        // 被测代码
        finish(true);
      };
      let perfTestStrategy: PerfTestStrategy = {
        metrics: metrics,
        actionCode: actionCode,
        iterations: 5,
        timeout: 30000,
      };
      try {
        let perfTest: PerfTest = PerfTest.create(perfTestStrategy);
        await perfTest.run();
        let res1 = perfTest.getMeasureResult(PerfMetric.DURATION);
        perfTest.destroy();
        expect(res1.metric).assertEqual(PerfMetric.DURATION);
        expect(res1.average).assertLargerOrEqual(0);
      } catch (error) {
        expect(false).assertTrue();
      }
      done();
    })
  })
}
```

### 7.2 错误码测试模板

来源：`test/xts/acts/testfwk/perftest/entry/src/ohosTest/ets/test/PerfTestErrorCode.test.ets`

```typescript
it('testPerfTestErrorCode', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  try {
    let perfTestStrategy: PerfTestStrategy = {
      metrics: [],
      actionCode: null,
    };
    let perfTest: PerfTest = PerfTest.create(perfTestStrategy);
    expect().assertFail();
  } catch (e) {
    expect(e.code).assertEqual(32400003);
  }
});
```

## 八、辅助包

- **辅助包路径**: `${OH_ROOT}/test/xts/acts/testfwk/perftestScene/`
- **包名**: `com.uitestScene.acts`（与 uitestScene 共用）
- **页面**: Index.ets, ListPage.ets, navigation.ets
- **用途**: PerfTest 通过 UiTest 的 Driver 操作辅助包页面来测量页面切换、列表滑动等性能

## 九、版本历史

- **v2.0.0** (2026-04-02): 完全重写。修正 API 定义（旧版 perfSuite/perfLog/finishBenchmark 不存在），新增 PerfTest.create/run/getMeasureResult/destroy API、PerfMetric 枚举、PerfTestStrategy 接口、状态机描述、错误码映射、API 关联关系、跨子系统依赖
- **v1.0.0** (2026-02-05): 初始版本（API 定义错误，已废弃）
