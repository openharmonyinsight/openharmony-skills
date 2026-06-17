---
name: ohos-issue-arkruntime-gc-debugging
description: 在诊断 ArkCompiler 运行时中的 GC 相关崩溃、缺失写屏障、悬空指针、AfterGC 校验失败或意外的长时间暂停/STW 时使用；或者在 `ecmascript/mem/**` 目录下排查问题时使用；或者当用户提到缺失屏障、AfterGC、标记-清除崩溃、CMC GC 崩溃、GC 统计、GC 暂停、弱引用 bug 时使用。
metadata:
  author: openharmony
  scope: domain
  stage: troubleshooting
  domain: arkruntime
  capability: gc-debugging
  version: 0.1.0
  status: draft
  tags:
    - arkruntime
    - gc
    - debugging
    - troubleshooting
---

# 任务与边界

诊断和修复 ArkCompiler 运行时中的 GC 相关 Bug，包括标记/清除阶段的崩溃、缺少写屏障导致的悬空指针、AfterGC 校验失败、长时间 STW 暂停以及弱引用问题。

**范围内：**
- 可达对象被错误回收（GC 后仍在使用的指针崩溃）
- 标记或清除阶段内部崩溃
- AfterGC 校验失败
- 特定测试中出现长时间暂停 / STW 尖峰
- 仅在开启 `ets_runtime_enable_cmc_gc` 时才复现的回归问题
- 弱引用返回过期（已被回收）的对象

**不在范围内：**
- 与垃圾回收无关的一般分配器/内存池问题
- 非运行时层（应用层）的内存问题
- 与 GC 行为无关的构建或配置问题

# 触发信号

- 可达对象被错误回收（仍在使用的指针在 GC 后崩溃）
- 在标记或清除阶段内部崩溃
- AfterGC 校验失败
- 特定测试中出现长时间暂停 / STW（Stop-The-World）尖峰
- 仅在开启 `ets_runtime_enable_cmc_gc` 时才复现的回归问题
- 弱引用返回了一个过期的（已被回收的）对象
- 用户提到：缺失屏障、AfterGC、标记-清除崩溃、CMC GC 崩溃、GC 统计、GC 暂停、弱引用 bug

# 初步排查

使用以下决策树对症状进行分类：

1. **"可达但被释放"** → 写屏障或 visitor 覆盖缺失。从 `ecmascript/mem/barriers.h`（审查出问题字段的写入者）以及涉及类的 visitor 开始检查，对应文件在 `ecmascript/mem/visitor.h` / `full_gc.h`。
2. **标记阶段内部崩溃** → 栈上有未根化的 handle，或者最近新增的字段缺少 visitor。参见 gc-rooting。
3. **清除/整理阶段内部崩溃** → 怀疑是指向已移动对象的过期指针。审查所有在可能的 GC 点之间持有原始指针的调用者。
4. **仅 CMC GC 回归** → 从 `ecmascript/mem/cms_mem/sweep_gc.h` 和 `ecmascript/mem/shared_heap/shared_gc.h` 中的共享 GC 交互逻辑开始排查。
5. **AfterGC 校验失败** → 校验器消息会指出违反的不变量；失败对象的类会指向缺失的 visitor / 屏障。
6. **暂停时间回归** → 通过 `Heap` 上的 GC 统计路径和 GC 日志进行测量；关联到工作量增长的遍历/收集器。

# 执行策略

## 诊断工具集

- GC 日志（GC 日志编译标志位于 `js_runtime_config.gni`；查看该文件获取当前标志名称）。捕获失败前后的 GC 事件。
- 单元测试中的强制 GC 工具；debug 构建默认启用。要在 QEMU 运行中禁用，请在 GN 参数中使用 `disable_force_gc=true`（参见 `CLAUDE.md`）。
- `Heap` 上的 AfterGC 校验钩子 —— 在排查问题时开启；它们会在违反发生的时刻立即报错，而不是延迟到后续。
- ASan / debug 构建断言 —— 始终先在 `x64.debug` 中复现。大多数"随机"GC 崩溃在 debug 模式下是确定性的。
- 已有的 `ecmascript/tests/gc_first_test.cpp` / `gc_second_test.cpp` / `gc_third_test.cpp` 和 `weak_ref_old_gc_test.cpp` 可作为编写新复现用例的脚手架。

## 常见根因

- **新增字段缺少 visitor。** 症状：对象的子引用变为悬空指针。修复：参见 gc-rooting；更新所有 visitor。
- **对标记字段进行了原始赋值。** 症状：跨区域引用对 GC 不可见。修复：通过 `Barriers::Set*` 系列方法进行赋值。
- **在 GC 触发点之间持有未根化的局部变量。** 症状：随机崩溃。修复：用 `EcmaHandleScope` + handle 包装。
- **在压缩（compaction）期间持有原始指针。** 症状：full GC 后读取到垃圾数据。修复：使用 handle，而非原始指针。
- **MachineCodeSpace 生命周期管理错误。** 症状：AOT/JIT 代码空间在仍被引用时被释放。修复：参见 compiler-overview 了解谁拥有此空间。
- **Sendable 跨区域写入缺少跨区域屏障。** 症状：仅在多 worker 环境下失败。修复：参见 sendable-debugging。

# 禁止实践

- 对标记字段使用原始赋值而非通过 `Barriers::Set*` 系列方法 —— 绕过写屏障，使引用对 GC 不可见，导致悬空指针。
- 在任何可能触发 GC 的点之间持有原始 `JSTaggedValue` 指针而不用 handle 包装 —— GC 可能移动或回收底层对象，导致原始指针失效。
- 新增标记字段但不更新所有具体 visitor —— 新的子引用不会被追踪，导致其对象被过早回收。

# 异常与回退

提交给下一级审查者时，请提供：

- 确切的复现命令（单条测试命令）。
- 失败点附近的 GC 日志。
- 使用的 GN 参数（尤其是 `ets_runtime_enable_cmc_gc`）。
- Bug 是否在 `x64.debug` 中复现（断言输出，如有）。
- AfterGC 校验输出（如果开启了校验器）。
- 涉及对象的类名（以便维护者能在数秒内审查其 visitor / 屏障）。

如果症状不符合初步排查中的六个类别，或者 bug 在 debug 构建中无法复现，应将其视为未知的 GC 交互问题，带上上述证据升级处理，而非猜测根因。

# 引用

本 skill 自身内容完整，标准 GC 调试任务无需加载额外参考文件。如需深入了解本 skill 中提及的特定子系统（gc-rooting、compiler-overview、sendable-debugging），请查阅 `ecmascript/mem/` 源码树中的对应文档或项目级 CLAUDE.md。
