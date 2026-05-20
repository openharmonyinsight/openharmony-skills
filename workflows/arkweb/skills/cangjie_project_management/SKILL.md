---
name: cangjie-project-management
description: 仓颉项目管理工具 cjpm
  的用法指导，包括创建项目、项目配置(cjpm.toml)、管理依赖、构建、运行、测试、清理、安装、工作区、交叉编译、构建脚本(build.cj)、增量编译、环境变量替换等
descriptionZH: 仓颉项目管理工具 cjpm
  的用法指导，包括创建项目、项目配置(cjpm.toml)、管理依赖、构建、运行、测试、清理、安装、工作区、交叉编译、构建脚本(build.cj)、增量编译、环境变量替换等
tags:
  - 仓颉
  - 项目管理
  - cjpm
---

# 仓颉语言项目管理 Skill

## 1. cjpm 概述

cjpm（Cangjie Project Manager）是仓颉语言官方项目管理工具，负责模块初始化、依赖检查/更新、增量/并行编译、自定义构建命令等。

---

## 2. 核心命令

### 2.1 `init` — 初始化项目
```bash
cjpm init --name myapp --type=executable
cjpm init --workspace
```
- 创建 `cjpm.toml` 和 `src/` 目录；可执行类型时生成 `src/main.cj`
- 选项：
  - `--workspace` — 创建工作区配置
  - `--name <value>` — 设置根包名（默认：父目录名）
  - `--path <value>` — 模块路径（默认：当前目录）
  - `--type=<executable|static|dynamic>` — 输出类型（默认：`executable`）

### 2.2 `build` — 构建项目
```bash
cjpm build
cjpm build -V -g          # 调试模式，详细输出
cjpm build -j 4            # 4 并行任务
cjpm build --target <triple>  # 交叉编译
```
- 先检查依赖，再调用 `cjc` 编译
- 主要选项：
  - `-i`/`--incremental` — 包级增量编译
  - `-j`/`--jobs <N>` — 最大并行任务数
  - `-V`/`--verbose` — 显示编译日志
  - `-g` — 调试构建（输出到 `target/debug/bin`）
  - `--coverage` — 生成覆盖率信息
  - `-o`/`--output <value>` — 指定可执行文件名
  - `-l`/`--lint` — 运行 `cjlint` 静态分析
  - `--mock` — 启用 mock 支持
  - `--target <value>` — 交叉编译目标平台
  - `--skip-script` — 跳过构建脚本
- 中间文件 → `target/`，可执行文件 → `target/release/bin` 或 `target/debug/bin`

### 2.3 `run` — 构建并运行
```bash
cjpm run
cjpm run --run-args "arg1 arg2"
cjpm run --skip-build
```
- 自动先触发 `build`
- 选项：`--name`（二进制名）、`--build-args`、`--run-args`、`--skip-build`

### 2.4 `test` — 运行单元测试
```bash
cjpm test
cjpm test src src/koo      # 测试指定包
cjpm test --filter "MyTest*.*"
```
- 编译并运行测试用例；输出到 `target/release/unittest_bin`
- 测试文件：`xxx_test.cj` 与 `xxx.cj` 并列
- 主要选项：
  - `--filter <value>` — 过滤测试（通配符：`*`、`MyTest*.*Test`、`-*.*exclude`）
  - `--include-tags`/`--exclude-tags` — 按标签过滤
  - `--timeout-each <value>` — 单个测试超时（如 `10s`、`500millis`）
  - `--parallel <value>` — 并行执行
  - `--no-run` — 仅编译
  - `--skip-build` — 仅运行
  - `--dry-run` — 打印测试列表
  - `--report-path`/`--report-format` — 测试报告

### 2.5 `bench` — 运行基准测试
```bash
cjpm bench
cjpm bench --report-format csv
```
- 运行 `@Bench` 标注的性能测试
- 选项与 `test` 类似，额外支持 `--baseline-path`（对比基准）

### 2.6 `clean` — 清理构建产物
```bash
cjpm clean
cjpm clean --coverage
```
- 移除 `target/` 目录。`--coverage` 同时清理覆盖率文件

### 2.7 `check` — 检查依赖
- 打印有效的包编译顺序，或报告循环/缺失依赖

### 2.8 `update` — 更新 cjpm.lock
- 同步 `cjpm.toml` 到 `cjpm.lock`；记录 git 依赖版本元数据

### 2.9 `tree` — 可视化依赖树
```bash
cjpm tree -V --depth 3
```

### 2.10 `install` / `uninstall` — 安装/卸载
```bash
cjpm install --path .
cjpm install --git "https://..." --tag v1.0.0
cjpm uninstall myapp
```
- 支持本地和 git 两种安装模式

---

## 3. cjpm.toml 配置

### 3.1 `[package]` — 单模块配置
```toml
[package]
cjc-version = "0.55.3"       # 最低 cjc 版本（必填）
name = "myapp"                # 模块名和根包名（必填）
version = "1.0.0"             # 模块版本（必填）
output-type = "executable"    # 输出类型：executable|static|dynamic（必填）
description = "My app"        # 描述（可选）
compile-option = "-O2"        # 额外编译选项（可选）
link-option = ""              # 链接器选项（可选）
src-dir = "src"               # 源码目录（默认 src）
target-dir = "target"         # 输出目录（默认 target）
```

### 3.2 `[workspace]` — 工作区配置（与 `[package]` 互斥）
```toml
[workspace]
members = ["module_a", "module_b"]
build-members = ["module_a"]
test-members = ["module_a"]
compile-option = ""
target-dir = "target"
```

### 3.3 `[dependencies]` — 依赖配置
```toml
[dependencies]
# 本地依赖
pro0 = { path = "./pro0" }
# Git 依赖（优先级：commitId > branch > tag）
pro1 = { git = "https://...", tag = "v1.0.0" }
pro2 = { git = "https://...", branch = "dev" }
pro3 = { git = "https://...", commitId = "abc123" }
# 覆盖依赖输出类型
pro4 = { path = "./pro4", output-type = "dynamic" }
```

### 3.4 `[test-dependencies]` — 测试专用依赖
- 格式同 `[dependencies]`，仅在 `xxx_test.cj` 文件中可用

### 3.5 `[script-dependencies]` — 构建脚本依赖
- 格式同 `[dependencies]`，仅用于 `build.cj` 脚本

### 3.6 `[replace]` — 依赖替换
- 替换间接（传递）依赖：`pro0 = { path = "./local_pro0" }`
- 仅入口模块的 `replace` 生效

### 3.7 `[ffi.c]` — C 库 FFI 依赖
```toml
[ffi.c]
hello = { path = "./src/" }
```
- 开发者须预编译 `.so`/`.a` 文件到指定路径

### 3.8 `[profile]` — 配置

#### profile.build
```toml
[profile.build]
lto = "full"                  # 链接时优化：full|thin
incremental = true            # 增量编译
```

#### profile.test
```toml
[profile.test]
filter = "MyTest*"
timeout-each = "10s"
parallel = "4"

[profile.test.build]
compile-option = ""
mock = "on"                   # on|off|runtime-error

[profile.test.env]
MY_VAR = { value = "abc", splice-type = "replace" }
```

#### profile.bench
```toml
[profile.bench]
report-path = "bench_report"
report-format = "csv"
baseline-path = "old_report"
```

#### profile.customized-option — 自定义选项
```toml
[profile.customized-option]
feature_x = "--cfg=\"feature=x\""
optimize = "-O2"
```
启用：`cjpm build --feature_x --optimize`

### 3.9 `[target]` — 平台/后端特定配置
```toml
[target.x86_64-unknown-linux-gnu]
compile-option = ""
link-option = ""

[target.x86_64-unknown-linux-gnu.dependencies]
pro0 = { path = "./pro0_linux" }

[target.x86_64-unknown-linux-gnu.bin-dependencies]
path-option = ["./libs/"]
```

#### bin-dependencies — 二进制库依赖
```toml
[target.name.bin-dependencies]
path-option = ["./path1", "./path2"]   # 自动导入路径下的仓颉库
[target.name.bin-dependencies.package-option]
"pro0.xoo" = "./test/pro0/pro0.xoo.cjo"  # 精确映射
```

### 3.10 `package-configuration` — 子包配置
```toml
[package.package-configuration.sub_pkg]
output-type = "executable"    # 子包可独立生成可执行文件
compile-option = "-O1"
```

### 3.11 环境变量替换
- 语法：`${ENV_VAR}`
- 支持字段：`compile-option`、`link-option`、`target-dir`、`members`、`path` 等

---

## 4. 包管理规则

### 4.1 有效源包
- 目录须直接包含至少一个 `.cj` 文件
- 所有父包（直到根包）也须为有效源包
- 无 `.cj` 文件的目录及其子目录被忽略（带警告）

### 4.2 循环依赖检测
- cjpm 报告循环路径
- 解决方案：移除多余导入、重构依赖顺序、拆分模块

### 4.3 cjpm.lock
- `build` 时自动创建，用于可复现构建
- `cjpm update` 手动刷新

---

## 5. 构建脚本（build.cj）

### 5.1 位置
- 项目根目录（与 `cjpm.toml` 同级），不由 `init` 创建

### 5.2 模板
```cangjie
import std.process.*

main() {
    match (Process.current.arguments[0]) {
        case "pre-build" => 0
        case "post-build" => 0
        case "pre-test" => 0
        case "post-test" => 0
        case _ => 0
    }
}
```

### 5.3 钩子规则
- 返回 `0` = 成功；非零 = 失败（中止命令）
- 支持的钩子：`pre-build`/`post-build`、`pre-test`/`post-test`、`pre-bench`/`post-bench`、`pre-run`/`post-run`、`pre-clean`（无 `post-clean`）
- `--skip-script` 跳过所有构建脚本

### 5.4 依赖
- 通过 `[script-dependencies]` 配置（独立于 `[dependencies]` 和 `[test-dependencies]`）

---

## 6. 命令扩展

- 将可执行文件命名为 `cjpm-xxx(.exe)` 并放入 `PATH`
- 通过 `cjpm xxx [args]` 调用（等价于 `cjpm-xxx [args]`）
- 内置命令优先级高于扩展命令

---

## 7. 典型工作流

```bash
# 1. 创建项目
cjpm init --name myapp

# 2. 创建子包
mkdir src/utils

# 3. 创建依赖模块
mkdir mylib && cd mylib && cjpm init --name mylib --type=static

# 4. 配置依赖（编辑 cjpm.toml）
# [dependencies]
# mylib = { path = "mylib" }

# 5. 构建
cjpm build

# 6. 运行
cjpm run

# 7. 编写测试（xxx_test.cj 文件）
cjpm test

# 8. 清理
cjpm clean
```
