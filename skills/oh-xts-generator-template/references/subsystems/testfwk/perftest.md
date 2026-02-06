# PerfTest 模块配置

> **模块信息**
> - 模块名称: PerfTest（性能测试框架）
> - 所属子系统: testfwk
> - Kit包: @kit.TestKit
> - API 声明文件: @ohos.perftest.d.ts
> - 版本: 1.0.0
> - 更新日期: 2026-02-05

## 模块概述

PerfTest 是 OpenHarmony 的性能测试框架，用于测试应用和接口的性能指标。

### 主要功能

- 应用性能测试
- 接口性能测试
- 流程性能测试
- 性能数据采集
- 性能报告生成

### 核心 API

| API 名称 | 类型 | 说明 |
|---------|------|------|
| `perfSuite` | 函数 | 性能测试套件 |
| `perfLog` | 函数 | 性能日志记录 |
| `finishBenchmark` | 函数 | 完成基准测试 |

## 测试特点

1. **关注性能指标**
   - CPU 使用率
   - 内存占用
   - 响应时间
   - 吞吐量

2. **测试环境要求**
   - 性能测试需要在真实设备上进行
   - 模拟器测试结果仅供参考
   - 注意测试环境的稳定性
   - 避免其他进程干扰

3. **数据采集**
   - 支持性能数据采集
   - 支持性能报告生成
   - 支持多次测试取平均值

## 参考资料配置

**参考文档路径**：
```
API 参考: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-test-kit/perftest.md
开发指南: ${OH_ROOT}/docs/zh-cn/application-dev/application-test/
```

**查找方式**：
```bash
# 方式1：从配置读取
使用本配置文件中指定的参考资料路径

# 方式2：在 docs 仓中查找
grep -r "perfSuite" ${OH_ROOT}/docs/
grep -r "perfLog" ${OH_ROOT}/docs/
grep -r "finishBenchmark" ${OH_ROOT}/docs/
```

## 代码模板

### 基础性能测试模板

```typescript
/**
 * @tc.name testBenchmark001
 * @tc.number SUB_testfwk_PERFTEST_BENCHMARK_001
 * @tc.desc 测试 PerfTest 性能测试功能
 * @tc.type PERFORMANCE
 * @tc.size LARGETEST
 * @tc.level LEVEL1
 */
it('testBenchmark001', TestType.PERFORMANCE | Size.LARGETEST | Level.LEVEL1, () => {
  // 1. 开始性能测试
  perfSuite('Performance Test', () => {
    // 2. 记录性能日志
    perfLog('API Call Performance');

    // 3. 执行被测试的代码
    let result = apiObject.methodName();

    // 4. 完成基准测试
    finishBenchmark('Performance Test');
  });
});
```

### 多次测试取平均值模板

```typescript
/**
 * @tc.name testAveragePerformance001
 * @tc.number SUB_testfwk_PERFTEST_AVG_001
 * @tc.desc 测试性能指标 - 多次测试取平均值
 * @tc.type PERFORMANCE
 * @tc.size LARGETEST
 * @tc.level LEVEL1
 */
it('testAveragePerformance001', TestType.PERFORMANCE | Size.LARGETEST | Level.LEVEL1, () => {
  const testRounds = 10;
  const executionTimes: number[] = [];

  for (let i = 0; i < testRounds; i++) {
    let startTime = Date.now();

    // 执行被测试的代码
    let result = apiObject.methodName();

    let endTime = Date.now();
    executionTimes.push(endTime - startTime);
  }

  // 计算平均执行时间
  let avgTime = executionTimes.reduce((sum, time) => sum + time, 0) / testRounds;

  // 验证平均执行时间符合预期
  expect(avgTime).lessThan(100); // 平均执行时间应小于 100ms
});
```

## 测试覆盖目标

| API 类型 | 最低覆盖率要求 | 推荐覆盖率 |
|---------|--------------|----------|
| PerfTest 核心 API | 85% | 95% |
| 性能测试场景 | 80% | 90% |

## 测试注意事项

1. **测试环境**
   - 性能测试需要在真实设备上进行
   - 模拟器测试结果仅供参考
   - 注意测试环境的稳定性

2. **测试设计**
   - 避免其他进程干扰
   - 多次测试取平均值
   - 设置合理的性能阈值

3. **结果分析**
   - 关注性能指标的稳定性
   - 记录测试环境信息
   - 对比历史数据

## 通用配置继承

本模块继承 testfwk/_common.md 的通用配置：
- API Kit 映射
- 测试路径规范
- 参数测试规则
- 错误码测试规则

模块级配置可以覆盖通用配置的特定部分。

## 版本历史

- **v1.0.0** (2026-02-05): 从 _common.md 拆分，初始版本
