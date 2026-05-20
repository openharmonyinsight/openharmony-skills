---
name: cangjie-toolchains-cjprof
description: "仓颉性能分析工具 cjprof 使用说明。"
---

# 仓颉性能分析工具 cjprof Skill

## 1. 概述

`cjprof`（Cangjie Profile）是仓颉语言的性能分析工具，支持 CPU 热点函数采样分析和堆内存分析。仅支持 Linux 系统。

> **权限要求**：`cjprof record` 需要 `root` / `sudo` 权限，或系统 `perf_event_paranoid` 配置为 `-1`。

---

## 2. CPU 热点函数分析

### 2.1 采样（record）

```bash
# 采样正在运行的进程
cjprof record -f 10000 -p 12345 -o sample.data

# 启动新程序并采样
cjprof record -f max -- ./test arg1 arg2
```

| 选项 | 说明 |
|------|------|
| `-f` / `--freq <freq>` | 采样频率（Hz），默认 5000，`max` 取系统最大值 |
| `-o` / `--output <file>` | 输出文件名（默认 `cjprof.data`） |
| `-p` / `--pid <pid>` | 指定进程 ID |

> 采样过程中按 `Ctrl+C` 可提前结束。

### 2.2 生成报告（report）

```bash
# 文本报告
cjprof report -i sample.data

# 火焰图
cjprof report -F -i sample.data -o flame.svg
```

| 选项 | 说明 |
|------|------|
| `-F` / `--flame-graph` | 生成火焰图（SVG） |
| `-i` / `--input <file>` | 输入数据文件（默认 `cjprof.data`） |
| `-o` / `--output <file>` | 火焰图输出文件（默认 `FlameGraph.svg`） |

**报告说明**：
- 文本报告：显示函数采样总占比（含子函数）、自身占比、函数名，按总占比降序
- 火焰图：横轴=采样占比（越宽越耗时），纵轴=调用栈（父下子上）

---

## 3. 堆内存分析

### 3.1 导出堆内存（dump）
```bash
cjprof heap -d 12345 -o heap.data      # 导出进程 12345 的堆内存
```

> 导出会向进程发送 `SIG_USR1` 信号，需确认目标为仓颉程序。

### 3.2 分析对象信息
```bash
cjprof heap -i heap.data
```
输出各对象类型的实例数、浅堆大小、深堆大小：
```text
Object Type           Objects        Shallow Heap   Retained Heap
====================  =============  =============  =============
AAA                               1            80             400
BBB                               4            32             196
```

### 3.3 查看仓颉线程栈
```bash
cjprof heap --show-thread
```

### 3.4 查看对象引用关系
```bash
# 查看 AAA 和 BBB 的引用关系（引用了哪些对象）
cjprof heap --show-reference="AAA;BBB"

# 查看 CCC 的被引用关系（被哪些对象引用）
cjprof heap --show-reference="CCC" --incoming-reference

# 限制展示深度
cjprof heap --show-reference --depth 5
```

### 3.5 堆分析选项

| 选项 | 说明 |
|------|------|
| `-d` / `--dump <pid>` | 导出指定进程的堆内存 |
| `-i` / `--input <file>` | 分析的堆数据文件（默认 `cjprof.data`） |
| `-o` / `--output <file>` | 导出的堆数据文件（默认 `cjprof.data`） |
| `--show-reference[=<names>]` | 展示对象引用关系（`;` 分隔多个对象名） |
| `--incoming-reference` | 展示被引用关系（需配合 `--show-reference`） |
| `-D` / `--depth <n>` | 引用关系最大展示深度（默认 10） |
| `-t` / `--show-thread` | 展示仓颉线程栈及栈中引用的对象 |
| `-V` / `--verbose` | 打印解析日志 |

---

## 4. 术语说明

- **浅堆（Shallow Heap）**：对象自身占用的堆内存大小
- **深堆（Retained Heap）**：对象被 GC 回收后可释放的所有关联对象的浅堆大小之和
