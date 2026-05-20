---
name: cangjie-toolchains-cjdb
description: "仓颉调试器 cjdb 使用说明。"
---

# 仓颉调试工具 cjdb Skill

## 1. 概述

`cjdb` 是基于 `lldb` 开发的仓颉程序命令行调试工具，位于 SDK 的 `cangjie/tools/bin` 路径下。支持 Windows、Linux、macOS 平台。

### 1.1 前提条件
- 被调试程序须以 `debug` 模式编译：`cjc -g test.cj -o test`
- 保证 `cjdb` 和编译器来自同一版本工具链

---

## 2. 启动调试

### 2.1 launch 方式
```bash
# 方式一：启动时加载程序
cjdb ./test

# 方式二：先启动再加载
cjdb
(cjdb) file test
```

### 2.2 attach 方式
```bash
cjdb
(cjdb) attach <pid>    # 附加到正在运行的进程
```

---

## 3. 断点

### 3.1 源码断点
```text
(cjdb) b test.cj:4                                  # 简写
(cjdb) breakpoint set --file test.cj --line 4        # 完整写法
```

### 3.2 函数断点
```text
(cjdb) b test                                        # 简写
(cjdb) breakpoint set --name test                    # 完整写法
```

### 3.3 条件断点
```text
(cjdb) breakpoint set --file test.cj --line 4 --condition a==12
```

### 3.4 继续执行
```text
(cjdb) c    # 运行到下一个断点
```

---

## 4. 单步执行

| 命令 | 简写 | 说明 |
|------|------|------|
| `thread step-over` | `n` / `next` | 单步跳过（不进入函数） |
| `thread step-in` | `s` / `step` | 单步进入（进入有调试信息的函数） |
| `finish` | — | 执行完当前函数并返回上层 |

---

## 5. 变量查看与修改

### 5.1 查看变量
```text
(cjdb) locals              # 查看所有局部变量
(cjdb) globals             # 查看所有全局变量
(cjdb) p variableName      # 查看单个变量（简写 print）
(cjdb) p array[1..3]       # 查看数组区间（左闭右开）
```

支持类型：基础类型、String、struct/class、Array、CString、Enum。

### 5.2 修改变量
```text
(cjdb) set a=30            # 仅支持基础数值类型
(cjdb) set b=0             # Bool: 0=false, 非0=true
(cjdb) set c=0x41          # Rune: 使用 ASCII 码
```

---

## 6. 表达式计算

```text
(cjdb) expr 3              # 字面量
(cjdb) expr a + b          # 算术表达式
(cjdb) expr a > b          # 关系表达式
(cjdb) expr value.member   # 成员访问
(cjdb) expr array[2]       # 索引访问
```

> **注意**：不支持带命名参数的函数调用、互操作、扩展、属性、插值字符串。Windows 不支持 Float16 和异常抛出。

---

## 7. 观察点

```text
(cjdb) wa s v -w read a           # 读观察点
(cjdb) wa s v -w write a          # 写观察点
(cjdb) wa s v -w read_write a     # 读写观察点
```

仅支持基础类型。

---

## 8. 仓颉线程

```text
(cjdb) cjthread list              # 列出所有仓颉线程
(cjdb) cjthread backtrace 1       # 查看指定线程调用栈
```

---

## 9. 日志

```text
(cjdb) log enable                 # 启用日志
(cjdb) log list                   # 查看支持的日志列表
```

---

## 10. 常见问题

| 问题 | 解决方案 |
|------|----------|
| Docker 下报 `packet returned an error: 8` | 创建容器时加 `--cap-add=SYS_PTRACE --security-opt seccomp=unconfined` |
| 持续报 `signal SIGABRT` | `process handle --pass true --stop false --notify true SIGBUS` |
| 无法通过 `next/s` 进入 `catch` 块 | 在 `catch` 块内打断点 |
| 泛型变元名显示为 T0, T1 | 仓颉 ABI 兼容设计，非错误 |
