---
name: cangjie-stdx-config
description: "仓颉 stdx 项目配置与构建说明。"
---

# 仓颉扩展标准库（stdx）项目配置与构建 Skill

## 1. stdx 下载与安装

### 1.1 下载

**发行版下载页面**：<https://gitcode.com/Cangjie/cangjie_stdx/releases>

根据操作系统和架构选择对应的发行版：

| 平台 | 架构 | 发行版名称示例 |
|------|------|----------------|
| Linux | x86_64 | `linux_x86_64_cjnative` |
| Linux | aarch64 | `linux_aarch64_cjnative` |
| macOS | x86_64 | `macos_x86_64_cjnative` |
| macOS | aarch64 | `macos_aarch64_cjnative` |
| Windows | x86_64 | `windows_x86_64_cjnative` |

### 1.2 目录结构

下载并解压后，目录结构如下：

```text
stdx/
├── dynamic/       # 动态库（含动态链接文件、cjo、bc 文件）
│   └── stdx/
└── static/        # 静态库（含静态链接文件、cjo、bc 文件）
    └── stdx/
```

动态库和静态库**二选一**使用。

### 1.3 获取系统架构信息

在配置前，先确认编译器目标架构，该信息用于 `cjpm.toml` 中的 `[target]` 配置：

```shell
cjc -v
# 输出示例：
# Cangjie Compiler: 0.60.5 (cjnative)
# Target: x86_64-unknown-linux-gnu
```

各平台的 target 标识：

| 平台 | target 标识 |
|------|-------------|
| Linux x86_64 | `x86_64-unknown-linux-gnu` |
| Linux aarch64 | `aarch64-unknown-linux-gnu` |
| macOS x86_64 | `x86_64-apple-darwin` |
| macOS aarch64 | `aarch64-apple-darwin` |
| Windows x86_64 | `x86_64-w64-mingw32` |

---

## 2. 动态库配置

在项目 `cjpm.toml` 中添加 `bin-dependencies` 配置，`path-option` 指向 `dynamic/stdx` 目录。

### 2.1 Linux x86_64

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = ""

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

### 2.2 Linux aarch64

```toml
[target.aarch64-unknown-linux-gnu]
  [target.aarch64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

### 2.3 macOS x86_64

```toml
[target.x86_64-apple-darwin]
  [target.x86_64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

### 2.4 macOS aarch64

```toml
[target.aarch64-apple-darwin]
  [target.aarch64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

### 2.5 Windows x86_64

```toml
[target.x86_64-w64-mingw32]
  [target.x86_64-w64-mingw32.bin-dependencies]
    path-option = ["D:\\path\\to\\stdx\\dynamic\\stdx"]
```

### 2.6 构建与运行

```shell
cjpm build
cjpm run
```

> **说明**：使用 `cjpm run` 运行时，工具会自动配置动态库依赖路径，无需额外设置环境变量，**更不必把 stdx 相关动态库复制到可执行文件所在目录**

### 2.7 独立部署运行

如果需要**独立部署运行**编译产物（即不通过 `cjpm run`，而是直接执行编译出的可执行文件），则需要手动设置动态库搜索路径：

| 操作系统 | 环境变量 | 示例 |
|----------|----------|------|
| Linux | `LD_LIBRARY_PATH` | `export LD_LIBRARY_PATH=/path/to/stdx/dynamic/stdx:$LD_LIBRARY_PATH` |
| macOS | `DYLD_LIBRARY_PATH` | `export DYLD_LIBRARY_PATH=/path/to/stdx/dynamic/stdx:$DYLD_LIBRARY_PATH` |
| Windows | `PATH` | 将 stdx 动态库目录添加到 `PATH` 中 |

---

## 3. 静态库配置

将 `path-option` 指向 `static/stdx` 目录。使用 crypto 和 net 包的静态库时，由于依赖系统符号，需要额外添加 `compile-option`。

### 3.1 Linux x86_64（静态库 + crypto/net）

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

> **注意**：Linux 下静态链接 crypto/net 模块时须添加 `compile-option = "-ldl"`，因为 OpenSSL 静态库依赖 `libdl`。如果不使用 crypto/net 模块，可省略 `-ldl`。

### 3.2 Linux aarch64（静态库 + crypto/net）

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"

[target.aarch64-unknown-linux-gnu]
  [target.aarch64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

### 3.3 macOS aarch64（静态库）

macOS 下使用静态库无需额外 `compile-option`：

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"

[target.aarch64-apple-darwin]
  [target.aarch64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

### 3.4 macOS x86_64（静态库）

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"

[target.x86_64-apple-darwin]
  [target.x86_64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

### 3.5 Windows x86_64（静态库 + crypto/net）

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-lcrypt32"

[target.x86_64-w64-mingw32]
  [target.x86_64-w64-mingw32.bin-dependencies]
    path-option = ["D:\\path\\to\\stdx\\static\\stdx"]
```

> **注意**：Windows 下静态链接 crypto/net 模块时须添加 `compile-option = "-lcrypt32"`，因为 OpenSSL 依赖 Windows 证书存储 API。如果不使用 crypto/net 模块，可省略 `-lcrypt32`。

### 3.6 构建与运行

静态库编译的产物无需设置动态库搜索路径，可直接运行：

```shell
cjpm build
cjpm run
# 或直接运行可执行文件
./target/release/bin/myproject
```

---

## 4. 静态库与动态库选择指南

| 维度 | 动态库 | 静态库 |
|------|--------|--------|
| 产物体积 | 小（运行时加载 .so/.dll/.dylib） | 大（链接进可执行文件） |
| 部署便利性 | 需随产物分发动态库或配置搜索路径 | 单文件部署，无外部依赖 |
| 额外配置 | 运行前设置 `LD_LIBRARY_PATH` 等（独立部署时） | Linux 需 `-ldl`，Windows 需 `-lcrypt32`（仅 crypto/net） |
| 适用场景 | 开发调试、多项目共享库、减小产物体积 | 生产部署、容器化、无法控制运行环境 |

---

## 5. OpenSSL 依赖

stdx 的 crypto 和 net 模块依赖 **OpenSSL 3** 库，使用前需确保系统已安装。

### 5.1 各平台安装方式

| 操作系统 | 安装方式 |
|----------|----------|
| Ubuntu/Debian | `sudo apt install libssl-dev` |
| CentOS/RHEL | `sudo yum install openssl-devel` 或 `sudo dnf install openssl-devel` |
| macOS | `brew install openssl@3` |
| Windows | 下载 OpenSSL 3 安装包并配置 PATH |

### 5.2 验证安装

```shell
# Linux/macOS
openssl version
# 应输出 OpenSSL 3.x.x

# 检查头文件
ls /usr/include/openssl/ssl.h  # Linux
ls /usr/local/opt/openssl@3/include/openssl/ssl.h  # macOS (Homebrew)
```
