---
name: cangjie-toolchains-cjfmt
description: "仓颉代码格式化工具 cjfmt 使用说明。"
---

# 仓颉格式化工具 cjfmt Skill

## 1. 概述

`cjfmt`（Cangjie Formatter）是基于仓颉语言编程规范的代码自动格式化工具。

---

## 2. 基本用法

### 2.1 单文件格式化
```bash
cjfmt -f test.cj                          # 格式化并覆盖源文件
cjfmt -f test.cj -o output.cj             # 输出到新文件
```

### 2.2 目录格式化
```bash
cjfmt -d src/                             # 格式化目录下所有 .cj 文件（覆盖）
cjfmt -d src/ -o ./formatted/             # 输出到指定目录
```

### 2.3 片段格式化
```bash
cjfmt -f a.cj -o b.cj -l 10:25            # 仅格式化第 10~25 行
```
> `-l` 仅适用于单文件（`-f`），与 `-d` 搭配时无效。

---

## 3. 命令选项

| 选项 | 说明 |
|------|------|
| `-h` | 显示帮助信息 |
| `-v` | 显示版本号 |
| `-f <file>` | 指定格式化文件（支持相对/绝对路径） |
| `-d <dir>` | 指定格式化目录 |
| `-o <value>` | 输出文件或目录 |
| `-c <value>` | 指定格式化配置文件 |
| `-l <start:end>` | 指定格式化行范围（仅 `-f`） |

---

## 4. 配置文件

通过 `-c` 指定自定义配置文件，或使用 `CANGJIE_HOME/tools/config/cangjie-format.toml` 默认配置。

```toml
indentWidth = 4                            # 缩进宽度 [0, 8]
linelimitLength = 120                      # 行长度限制 [1, 120]
lineBreakType = "LF"                       # 换行类型："LF" 或 "CRLF"
allowMultiLineMethodChain = false          # 允许多行方法链
multipleLineMethodChainLevel = 5           # 多行方法链最小层级 [2, 10]
multipleLineMethodChainOverLineLength = true  # 超过行长度时自动多行方法链
```

> 配置读取优先级：`-c` 指定文件 → `CANGJIE_HOME` 默认文件 → 内置默认值。

---

## 5. 格式化规则摘要

### 5.1 缩进
- 统一使用 4 个空格缩进

### 5.2 大括号
- 非空块使用 K&R 风格：左大括号在行末，前置 1 空格；右大括号独占一行
- `else`/`catch` 与右大括号同行

### 5.3 空格
- 冒号后有空格（类型声明、命名参数、返回类型）
- 二元操作符两侧留空格
- 一元操作符与操作数之间不留空格
- 圆括号/方括号内部不留空格
- `range` 操作符（`..`）两侧不留空格

### 5.4 空行与分号
- 移除多余连续空行和大括号内首尾空行
- 移除包声明和导入语句末尾的冗余分号

### 5.5 修饰符排序
- 顶层：`public` → `open`/`abstract`
- 成员函数：`public`/`protected`/`private` → `open` → `override`
- 静态函数：`public`/`protected`/`private` → `static` → `redef`

### 5.6 注释
- 以 `*` 开头的多行注释中 `*` 会自动对齐，多余空格被删除

---

## 6. 注意事项

- 暂不支持语法错误代码的格式化
- 暂不支持元编程（宏）代码的格式化
