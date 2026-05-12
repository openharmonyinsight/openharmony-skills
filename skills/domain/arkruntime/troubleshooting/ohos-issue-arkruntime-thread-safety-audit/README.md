# OH ArkRuntime Thread Safety Audit

## 概述

本 Skill 用于审计、审查或修复 ArkCompiler Runtime Core 中的线程安全问题，特别是 `static_core/plugins/ets` 目录下的 ArkTS-Sta ETS stdlib 和插件代码。

## 目标范围

- ETS stdlib 文件：`static_core/plugins/ets/stdlib/**/*.ets`
- ETS runtime/plugin 支持代码：`static_core/plugins/ets/**`
- 测试代码：`static_core/plugins/ets/tests/`
- 相关 native C++ 代码（仅当 ETS API 跨越 native 边界或 TSAN 报告指向时）

## 核心能力

### 1. 静态可变状态检测

识别 ETS/TS 文件中的静态字段、全局可变对象、缓存、锁和原子变量：

- 静态字段和单例
- 共享 Map/Array/StringBuilder
- ConcurrentHashMap/Mutex/QueueSpinlock/Atomic 类型

### 2. 并发入口点分析

判断候选状态是否可从并发路径访问：

- 公共 API 和导出函数
- taskpool.execute / EAWorker
- runtime 或 stdlib 回调
- 声明为 native 的 ETS 方法

### 3. 风险分级评估

根据四个条件识别有意义的风险：

- 共享可变状态
- 并发入口
- 缺失或不完整的同步
- 具体影响

风险等级：High / Medium / Low / Candidate / No risk

### 4. 常见问题模式识别

- 延迟单例初始化竞争
- 共享输出缓冲区
- 共享 Map get-or-create
- 未同步计数器
- 未同步布尔标志
- 成对缓存字段
- 复合状态槽

### 5. 修复方案选择

根据问题类型选择最窄的同步方案：

| 问题类型 | 推荐修复方案 |
|---------|-------------|
| 单数值计数器 | AtomicInt / AtomicLong |
| 单布尔标志 | AtomicBoolean |
| 需要匹配的多字段 | 一个互斥锁保护所有读写 |
| 单例延迟初始化 | 锁保护的 check-then-act |
| 共享键值注册表 | ConcurrentHashMap + 锁保护的 get-or-create |
| 每键可变复合状态 | 每槽锁 |
| 全局输出行构建 | 一个输出锁保护构建和发送 |

## 使用场景

### 触发条件

- 审计 ArkRuntime ETS stdlib 代码的线程安全性
- 审查涉及 taskpool/EAWorker 的代码变更
- 跟进 TSAN 报告的线程安全问题
- 设计新的并发测试

### 典型工作流程

1. **检测阶段**：扫描静态可变状态
2. **分析阶段**：识别并发入口点
3. **分类阶段**：根据风险标准评估候选问题
4. **修复阶段**：选择合适的同步方案
5. **验证阶段**：使用仓库工具验证修复

## API 引用

所有建议的 API 都有源码支撑：

- `AtomicInt`, `AtomicLong`, `AtomicBoolean` - `static_core/plugins/ets/stdlib/std/concurrency/Atomics.ets`
- `ConcurrentHashMap` - `static_core/plugins/ets/stdlib/std/containers/ConcurrentHashMap.ets`
- `Mutex`, `QueueSpinlock` - `static_core/plugins/ets/stdlib/std/core/SyncPrimitives.ets`
- `ConcurrencyHelpers.mutexCreate`, `ConcurrencyHelpers.lockGuard` - `static_core/plugins/ets/stdlib/std/core/ConcurrencyHelpers.ets`
- `taskpool.execute` - `static_core/plugins/ets/stdlib/std/concurrency/taskpool.ets`
- `EAWorker` - `static_core/plugins/ets/stdlib/std/core/EAWorker.ets`

## 测试策略

- 功能并发测试：参考现有仓库测试模板
- TSAN 测试：简明说明竞争的变量/函数
- 针对性测试：覆盖共享状态的并发访问场景

## 验证命令

```bash
# 检查变更
git diff --check -- <changed-files>

# 构建标准库
ninja -C static_core/build plugins/ets/etsstdlib.abc

# 编译测试文件
static_core/build/bin/es2panda --extension=ets \
  --stdlib=static_core/build/plugins/ets/etsstdlib.abc \
  --output=/tmp/test.abc <test.ets>

# 运行测试
static_core/build/bin/ark \
  --boot-panda-files=static_core/build/plugins/ets/etsstdlib.abc \
  --load-runtimes=ets \
  --verification-mode=ahead-of-time \
  /tmp/test.abc <entrypoint>
```

## 相关 Skills

暂无正式关联的 Skills。未来可考虑与崩溃日志分析、内存泄漏分析等 troubleshooting 类 Skill 关联。

## 维护说明

### 更新频率

- 当 ArkRuntime 并发模型发生变化时更新
- 当新增同步原语或 API 时更新
- 当发现新的线程安全模式时更新

### 贡献指南

1. 所有代码示例必须有源码位置引用
2. 新增模式需提供 Bad/Fix 对照
3. 风险分级标准需有实际案例支撑
4. 测试策略需引用现有仓库测试

### 参考资料

- OpenHarmony ArkRuntime 官方文档
- ArkTS 并发编程指南

## 版本历史

- **v0.1.0** (draft) - 初始版本，包含核心线程安全审计能力
