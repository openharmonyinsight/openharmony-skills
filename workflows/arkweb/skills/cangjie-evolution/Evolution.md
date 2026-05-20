# 仓颉普通工程 Evolution 记录

本文件用于记录仓颉普通工程（非鸿蒙应用）开发过程中遇到的重要问题和解决方案。

## 使用说明

- 每次构建成功后，将遇到的重要问题与解决方案记录到此文件
- 每次修复报错前,先阅读此文件了解历史踩坑情况
- 遵循已有的最佳实践,避免重复犯错

## 记录格式

```markdown
## [日期] - [问题描述]

### 问题症状
[描述问题的具体表现和错误信息]

### 问题原因
[分析问题的根本原因]

### 解决方案
[列出解决该问题的具体步骤]

### 预防措施
[列出如何避免此类问题的最佳实践]
```

---

## [2026-03-09] - operator 关键字冲突

### 问题症状
代码中使用 `let operator = parts[1]` 时编译报错：
```
error: expected identifier or pattern after 'let', found keyword 'operator'
```

### 问题原因
`operator` 是仓颉语言的保留关键字，不能直接用作变量名。

### 解决方案
1. 将变量名改为非关键字，例如 `op`
2. 或使用反引号转义：`` let `operator` = parts[1] ``

### 预防措施
避免使用仓颉关键字作为变量名，常见的保留字包括：
- operator, func, class, struct, enum, interface, let, var, if, else, while, for, match, case, return 等

## [2026-04-23] - 原生后端选择不要依赖运行时平台环境变量

### 问题症状
Linux 平台已经实现了原生 backend，但 `FileMonitor` 仍然退回到了 `PollingBackend`，测试里 `monitor.getBackendType()` 显示为 `BackendType.Polling`。

### 问题原因
后端选择逻辑在非 macOS 分支里调用了运行时平台探测；而平台探测默认值偏向 macOS，环境变量不完整时会误判，导致 Linux 原生 backend 根本没有被选中。

### 解决方案
1. 原生 backend 选择改成优先走 `@When[...]` 编译期分派
2. Linux 分支直接返回 Linux 原生 backend，不再依赖运行时 `PlatformUtils`
3. 为 Linux 原生 backend 增加单元测试和 `FileMonitor` 选择测试，防止再次静默回退

### 预防措施
- 平台相关实现优先使用编译期条件编译，少依赖环境变量
- `Auto/Native` 后端选择必须有显式测试覆盖
- 原生 backend 接线完成后，至少跑一次完整测试而不是只跑 build

---

记录开始：
