---
name: cangjie-toolchains-cjcov
description: "仓颉覆盖率检测工具 cjcov 使用说明。"
---

# 仓颉覆盖率统计工具 cjcov Skill

## 1. 概述

`cjcov`（Cangjie Coverage）用于生成仓颉程序的覆盖率报告，支持行覆盖率和分支覆盖率，输出 HTML、XML、JSON 格式。

---

## 2. 基本流程

### 2.1 单文件场景
```bash
# 1. 使用 --coverage 编译
cjc --coverage main.cj

# 2. 运行生成 .gcda 数据
./main

# 3. 生成 HTML 覆盖率报告
cjcov -o output --html-details
```

### 2.2 多文件/项目场景（推荐使用 cjpm）
```bash
cjpm build --coverage       # 编译带覆盖率
cjpm test --coverage        # 测试带覆盖率
cjcov -o output --html-details
```

---

## 3. 命令选项

| 选项 | 说明 |
|------|------|
| `-h` / `--help` | 显示帮助 |
| `-v` / `--version` | 显示版本号 |
| `-r ROOT` / `--root=ROOT` | gcda/gcno 文件所在根目录（默认当前目录） |
| `-o OUTPUT` / `--output=OUTPUT` | 报告输出目录（默认当前目录） |
| `--html-details` | 生成每个源文件的子 HTML 报告 |
| `-x` / `--xml` | 生成 `coverage.xml` |
| `-j` / `--json` | 生成 `coverage.json` |
| `-b` / `--branches` | 生成分支覆盖率（实验性功能） |
| `-k` / `--keep` | 保留 gcov 中间文件 |
| `-s SOURCE` / `--source=SOURCE` | 源文件路径（用于 HTML 中的相对路径） |
| `-e EXCLUDE` / `--exclude=EXCLUDE` | 排除指定路径的文件 |
| `-i INCLUDE` / `--include=INCLUDE` | 仅包含指定路径的文件 |
| `--verbose` | 输出详细解析日志 |

---

## 4. 典型使用示例

### 4.1 生成详细 HTML 报告
```bash
cjcov --root=./ -o html_output --html-details
```
生成 `index.html`（总览）和每个源文件对应的子 HTML。

### 4.2 生成 XML 报告
```bash
cjcov --root=./ -o report_dir -x
```

### 4.3 过滤源文件
```bash
# 排除测试目录
cjcov --root=./ -e "/path/to/tests" --html-details -o output

# 仅包含指定文件
cjcov --root=./ -i "/path/to/src/main.cj /path/to/src/utils" --html-details -o output
```

### 4.4 含分支覆盖率
```bash
cjcov -b --html-details -o output
```

---

## 5. 注意事项

- 不会统计行覆盖率的场景：全局变量定义、未初始化的成员变量声明、无函数体的函数声明（如 `foreign`）、枚举类型定义、class/extend 定义行
- 使用 `cjc --test` 编译时，源码中的 `main` 函数不会被执行覆盖
- 分支覆盖率为实验性功能，在 `try-catch-finally`、循环、`if-else` 场景可能不精确
- 常驻服务无法正常退出时，需通过 `gdb` 脚本（`p exit(0)`）使进程正常退出以生成 `gcda` 数据
- `gcov` 中间文件不删除会导致执行次数累加，建议默认删除（不加 `-k`）

---

## 6. 常见问题

| 问题 | 解决方案 |
|------|----------|
| 找不到 `llvm-cov` | 设置 `CANGJIE_HOME` 环境变量，或手动安装 `llvm-cov` |
| `OutOfMemoryError` | 增大堆内存：`export cjHeapSize=2GB` |
