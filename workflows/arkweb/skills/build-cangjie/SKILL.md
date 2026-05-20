---
name: build-cangjie
description: 仓颉编译器构建技能。
descriptionZH: 仓颉编译器构建。【触发场景】build/编译
  cjc/runtime/stdlib/stdx/cjpm/cjfmt/cjlint/cjcov/cjlsp、搭建编译环境、重新编译、用 cjc
  编译。【注意】首次构建需完整步骤：1) 依次构建 runtime+stdlib+stdx 并 install；2) source
  output/envsetup.sh；3) 验证：cjc hello.cj。后续增量编译只需 ninja cjc。输出在
  cangjie_compiler/output/。支持 linux/mac x86_64/aarch64。
tags:
  - 构建
  - 编译器
  - 仓颉
  - 工具链
---

# Build Cangjie Compiler

仓颉编译器构建技能。**每当用户提到以下任何场景时，必须调用此 skill：**
- 「构建/编译 cjc/runtime/stdlib/stdx」
- 「build the compiler」「编译仓颉」「编译 toolchain」
- 「build/编译 cjpm/cjfmt/cjlint/cjcov/cjlsp/cjtrace-recover」
- 「搭建编译环境」「重新编译」「install cangjie compiler」
- **「用 cjc 编译」「cjc 编译」「帮我编译」「编译这个文件」** — 当需要使用 cjc 时，必须先确保环境已配置（source envsetup.sh）
- 在任何需要获取编译好的 `cjc` 二进制文件的场景

**构建后必须执行以下步骤，否则无法使用：**
1. **install** — 每个组件 build 后都要 install
2. **source envsetup.sh** — `source cangjie_compiler/output/envsetup.sh`
3. **验证构建** — `cjc hello.cj -o hello && ./hello`，预期输出 `Hello, Cangjie`

**首次构建**需完整步骤（runtime → stdlib → stdx → tools）。**后续增量编译**只需 `cd cangjie_compiler/build/build && ninja cjc -j$(nproc)`（使用并行编译加速）。

**构建产物路径：** `{compiler-project}/output/`（包含 envsetup.sh）

**cjc 二进制路径（直接使用，无需 find）：**
- 已构建：`{compiler-project}/output/bin/cjc`
- 构建中：`{compiler-project}/build/build/bin/cjc`
- 环境变量设置后：`source {compiler-project}/output/envsetup.sh`，之后直接用 `cjc`

## 支持平台

| Platform | Runtime Output Path | stdx Target |
|----------|--------------------|-------------|
| `linux_x86_64` | `common/linux_release_x86_64` | `linux_x86_64_cjnative` |
| `linux_aarch64` | `common/linux_release_aarch64` | `linux_aarch64_cjnative` |
| `mac_x86_64` | `common/darwin_release_x86_64` | `darwin_x86_64_cjnative` |
| `mac_aarch64` | `common/darwin_release_aarch64` | `darwin_aarch64_cjnative` |

## 仓颉项目工作区结构

工作区根目录下有若干仓颉子项目（名称不固定，编译器项目通常包含 output/ 目录和 third_party/）：

- **编译器项目** — 包含 third_party/（LLVM）、build/（构建目录）、output/（产物）
- **运行时项目** — 内含 runtime/ 和 stdlib/ 子目录
- **stdx 项目**
- **output 目录** — 构建产物，内含 envsetup.sh 和 bin/cjc

**output 目录（构建产物）示例：**
- envsetup.sh：`{compiler-project}/output/envsetup.sh`
- cjc 二进制：`{compiler-project}/output/bin/cjc`（已构建时）
- 构建中 cjc：`{compiler-project}/build/build/bin/cjc`

## 快速构建（推荐）

**使用此 skill 时必须遵循以下流程：**

1. **优先增量编译** — 若已有构建产物（存在 `cangjie_compiler/build/build` 目录），直接使用增量编译（`--incremental --component cjc`），无需询问任何参数
2. **首次构建时询问用户构建类型** — 询问用户选择 `-t` 参数：`release`/`relwithdebinfo`/`debug`，默认使用 `relwithdebinfo`
3. **检查代码仓位置** — 若未找到相关代码仓（cangjie_compiler/cangjie_runtime/cangjie_stdx），询问用户代码仓位置（使用 `--workspace` 参数）
4. **推荐跳过测试** — 构建 compiler 时推荐使用 `--no-tests` 参数（加快构建速度）

**构建类型说明：**
- `release` — 完全优化，无调试信息
- `relwithdebinfo` — 优化 + 调试信息（默认，推荐）
- `debug` — 无优化，完整调试信息

```bash
# 增量构建（仅 cjc，自动并行编译，最快，推荐）
python3 scripts/build-cangjie.py --incremental --component cjc

# 完整构建（所有组件，跳过单元测试，推荐）
python3 scripts/build-cangjie.py --platform linux_x86_64 -t relwithdebinfo --no-tests

# 指定工作区路径
python3 scripts/build-cangjie.py --workspace /path/to/workspace -t release --no-tests

# 构建时包含单元测试（耗时较长）
python3 scripts/build-cangjie.py -t debug
```

## 组件构建顺序

**首次构建：** LLVM → Compiler (cjc) → Runtime → Stdlib → stdx → Tools

**后续增量编译 cjc：** `cd {compiler-project}/build/build && ninja cjc`（无需重建 runtime/stdlib）

**每个组件构建后必须 install，否则后续组件无法找到依赖。**

## 验证构建

```bash
cd /tmp
echo 'main() { println("Hello, Cangjie") }' > hello.cj
source <workspace>/cangjie_compiler/output/envsetup.sh
cjc hello.cj -o hello && ./hello
```
预期输出：`Hello, Cangjie`
