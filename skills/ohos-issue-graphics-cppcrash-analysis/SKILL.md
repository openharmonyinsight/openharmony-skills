---
name: ohos-issue-graphics-cppcrash-analysis
description: Use when analyzing OpenHarmony cppcrash faultlogs to locate root cause of native process crashes, investigating SIGSEGV/SIGABRT signals, memory corruption patterns, or call stack anomalies.
---

# 任务与边界

## 解决的问题

分析OpenHarmony系统图形模块相关cppcrash日志文件，定位进程崩溃的根本原因。

## 输入

- cppcrash日志文件
- `code/`目录下的相关源码
- `lib.unstripped/`目录下的带符号表so文件

## 输出

- 崩溃根因分析报告
- 精确的代码行号定位
- 修复建议

## 不适用情形

- 纯ArkTS/JS层崩溃（无native调用栈）
- 无cppcrash日志文件
- 无符号表so文件（无法解栈）

# 触发信号

## 任务触发词

- 分析cppcrash
- 解析cppcrash日志
- 定位native崩溃

## 症状词

- SIGSEGV、SIGABRT
- Use-After-Free
- 野指针
- 内存踩踏
- 0x6b6b地址

## 场景词

- 图形模块崩溃
- render_service崩溃

# 前置检查

## 1. 检查输入完整性

按以下顺序检查：

1. cppcrash文件是否存在
2. `lib.unstripped/`目录是否存在
3. `code/`目录是否存在

若缺失必要输入，终止并报告用户。

## 2. 检查崩溃类型

从cppcrash头部读取`Reason`：

- 若signal为SIGSEGV：内存访问异常
- 若signal为SIGABRT：主动终止或异常
- 若地址以`0x6b6b`开头：Use-After-Free

## 3. 检查buildId匹配

解栈前必须验证so的buildId与cppcrash中一致，否则终止。

# 执行策略

## 分析流程（按顺序执行）

1. **元数据分析**：读取Device Info、Module name、Reason、LastFatalMessage
2. **调用栈解栈**：详见 `references/stack-unwinding.md`
3. **代码定位与读取**：根据解栈结果定位源码
4. **反汇编分析**：详见 `references/disassembly-analysis.md`
5. **深度数据流追踪**：详见 `references/memory-pattern-analysis.md`
6. **调用链回溯分析**：详见 `references/call-chain-backtrace.md`
7. **多线程竞争分析**：详见 `references/thread-competition-analysis.md`
8. **内存数据分析**：详见 `references/memory-data-analysis.md`
9. **特殊情况判断**：详见 `references/special-cases.md`
10. **生成分析报告**：详见 `references/report-template.md`

## 关键判断点

### 崩溃地址特征判断

- `0x6b6b...`开头 → Use-After-Free（已释放内存被访问）
- 地址为0或接近0 → 空指针或野指针
- 地址与合法地址高位字节不同 → 越界写入踩踏

### 多线程问题判断

查看`Other thread info`：
- 若其它线程持有相同锁 → 锁竞争
- 若其它线程修改相同对象 → 竞态条件
- 若崩溃线程正在遍历容器而其它线程修改 → 迭代器失效

## 代码排查重点

详见 `references/code-review-checklist.md`，重点检查：

- 多线程锁使用
- 类型强转安全
- lambda捕获生命周期
- 智能指针生命周期

# 禁止做法

## 不要猜测根因

- 禁止在没有证据的情况下推断根因
- 禁止跳过数据流追溯直接给出结论
- 禁止使用模糊表述如"可能是"、"也许是"

原因：会导致错误的修复方向，浪费调试时间。

## 不要跳过解栈验证

- 禁止使用buildId不匹配的so解栈
- 禁止不验证buildId直接解栈

原因：会导致错误的代码行号定位。

## 不要忽略多线程分析

- 禁止只分析崩溃线程而忽略其它线程
- 禁止忽略锁竞争和竞态条件

原因：多线程问题是图形模块崩溃的常见根因。

## 不要跳过地址模式匹配

- 禁止不对比崩溃地址与合法地址的差异

原因：地址模式匹配是识别内存踩踏的关键手段。

# 异常与回退

## 信息不足时

- 若无法找到对应so → 报告用户需要提供正确的符号表文件
- 若无法定位源码 → 报告用户需要提供完整的代码目录
- 若buildId不匹配 → 报告用户版本不一致，终止分析

## 证据不足时

- 若无法确定单一根因 → 列出所有可能的根因并说明判断依据
- 明确标注哪些结论是确定的，哪些是推断的
- 说明需要进一步分析的方向

## 特殊调用栈处理

- 若栈顶是abort/raise → 结合业务代码分析主动退出原因
- 若栈顶是terminate → 分析异常抛出原因，注意踩内存也可能导致异常不匹配
- 若包含`cfi_slowpath_comm` → 优先按踩内存问题分析

# 参考资料

按以下条件读取对应文件：

| 条件 | 文件 |
|------|------|
| 执行解栈步骤时 | `references/stack-unwinding.md` |
| 执行反汇编分析时 | `references/disassembly-analysis.md` |
| 执行调用链回溯分析时 | `references/call-chain-backtrace.md` |
| 执行数据流追踪或地址模式匹配时 | `references/memory-pattern-analysis.md` |
| 执行多线程竞争分析时 | `references/thread-competition-analysis.md` |
| 执行内存数据分析时 | `references/memory-data-analysis.md` |
| 判断特殊情况时 | `references/special-cases.md` |
| 排查代码问题时 | `references/code-review-checklist.md` |
| 生成分析报告时 | `references/report-template.md` |

## 前置信息

用户提供了相关源码在`code/`目录。

用户提供了相关带符号表信息的so在`lib.unstripped/`目录。

用户环境提供llvm工具（llvm-readelf/llvm-addr2line/llvm-objdump等）。

分析时使用中文交互，涉及文件均为UTF-8编码。