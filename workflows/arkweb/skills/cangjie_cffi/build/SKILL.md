---
name: cangjie-cffi-build
description: "仓颉 C 互操作配置构建说明。"
---

# 仓颉C互操作配置构建指导

## 0. 各平台库文件命名对照

| 平台 | 动态库 | 静态库 |
|------|--------|--------|
| Linux | `lib<name>.so` | `lib<name>.a` |
| macOS | `lib<name>.dylib` | `lib<name>.a` |
| Windows | `lib<name>.dll` | `lib<name>.lib` |

> **注意**：Windows 平台上依赖动态库，目前 cjc 和 cjpm 实现有差异：编译时，cjc 对动态库是否有`lib`前缀不敏感，cjpm 则要求动态库必须有`lib`前缀。运行时，cjc 编出的可执行文件，依赖的动态库必须加上`lib`前缀，而 cjpm 构建出的可执行文件，依赖的动态库一定不能有`lib`前缀。请务必熟悉这个规则（实际是规格问题，未来会修复），保证能正常构建和运行。

## 1. cjc 编译器链接选项

| 选项 | 说明 |
|------|------|
| `-L <path>` / `--library-path <path>` | 指定库文件搜索目录（优先级高于 `LIBRARY_PATH` 环境变量） |
| `-l <name>` / `--library <name>` | 链接库文件，格式为 `lib[name].[extension]`（如 `-l draw` 链接 `libdraw.so/.a/.dll`） |

---

## 2. 使用 cjc 直接编译

### 2.1 Linux

```shell
# 编译 C 代码为动态库
clang -shared -fPIC -fstack-protector-all native.c -o libnative.so

# 编译 C 代码为静态库
clang -c -fstack-protector-all native.c -o native.o && ar rcs libnative.a native.o

# 编译仓颉代码并链接
cjc -L . -l native main.cj -o main

# 运行（动态库须确保在搜索路径上）
export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
./main
```

### 2.2 macOS

```shell
# 编译 C 代码为动态库
clang -shared -fPIC -fstack-protector-all native.c -o libnative.dylib

# 编译 C 代码为静态库
clang -c -fstack-protector-all native.c -o native.o && ar rcs libnative.a native.o

# 编译仓颉代码并链接
cjc -L . -l native main.cj -o main

# 运行（动态库须确保在搜索路径上）
export DYLD_LIBRARY_PATH=.:$DYLD_LIBRARY_PATH
./main
```

### 2.3 Windows

```shell
# 编译 C 代码为动态库（导出函数需加 __declspec(dllexport) 修饰）
clang -shared -fstack-protector-all native.c -o libnative.dll

# 编译仓颉代码并链接
cjc -L . -l native main.cj -o main.exe

# 运行（动态库须确保在搜索路径上）
./main.exe
```

> **注意**：Windows 平台上 C 函数需使用 `__declspec(dllexport)` 修饰以导出符号。

### 2.4 安全编译建议

编译 C 代码时**应启用栈保护选项**，防止缓冲区溢出攻击：

```shell
# 推荐选项（二选一）
clang -fstack-protector-all ...    # 全部函数开启栈保护
clang -fstack-protector-strong ... # 对含局部数组/地址操作的函数开启栈保护
```

---

## 3. 基于 cjpm 项目编译（推荐）

### 3.1 项目初始化

```shell
cjpm init          # 初始化项目
```

### 3.2 cjpm.toml 配置

在 `cjpm.toml` 中通过 `[ffi.c]` 节配置 C 库依赖：

```toml
[package]
  name = "myproject"
  cjc-version = "1.0.5"
  version = "1.0.0"
  output-type = "executable"

[ffi.c]
native = { path = "./libs/" }  # path 是 C 动态/静态库所在路径
```

### 3.3 构建与运行

```shell
cjpm build    # 构建时自动链接 [ffi.c] 设置的 C 库
cjpm run      # 构建并运行
```

### 3.4 其他相关 cjpm.toml 配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `output-type` | 输出类型 | `"executable"` / `"static"` / `"dynamic"` |
| `compile-option` | 传给 `cjc` 的额外编译选项 | `"-O1"` |
| `link-option` | 传给链接器的选项 | `"-z noexecstack -z relro -z now"` |

### 3.5 不同平台的 cjpm.toml 配置

当需要区分不同目标平台的库路径时，可使用 `[target]` 节：

**Linux x86_64**：

```toml
[ffi.c]
native = { path = "./libs/linux_x86_64/" }
```

**macOS aarch64**：

```toml
[ffi.c]
native = { path = "./libs/macos_aarch64/" }
```

**Windows x86_64**：

```toml
[ffi.c]
native = { path = ".\\libs\\windows_x86_64\\" }
```

### 3.6 链接安全加固选项

对于需要安全加固的项目，建议在 `link-option` 中添加链接器安全标志：

```toml
[package]
  link-option = "-z noexecstack -z relro -z now"
```

| 选项 | 说明 |
|------|------|
| `-z noexecstack` | 禁止栈上执行代码，防止栈溢出攻击 |
| `-z relro` | 设置 GOT 为只读，防止 GOT 覆写攻击 |
| `-z now` | 立即绑定所有符号，配合 relro 使用 |

---

## 4. 完整示例

### 4.1 Linux 完整编译流程

```shell
# 1. 编写 C 代码 (native.c)
# 2. 编译 C 代码为动态库
clang -shared -fPIC -fstack-protector-all native.c -o libnative.so

# 3. 使用 cjc 直接编译
cjc -L . -l native main.cj -o main
./main

# 或使用 cjpm 项目编译
# 将 libnative.so 放到 libs/ 目录下
# 在 cjpm.toml 中配置 [ffi.c] native = { path = "./libs/" }
cjpm build && cjpm run
```

### 4.2 Windows 完整编译流程

```shell
# 1. 编写 C 代码 (native.c)，导出函数加 __declspec(dllexport) 修饰
# 2. 编译 C 代码为动态库
clang -shared -fstack-protector-all native.c -o libnative.dll

# 3.1 使用 cjc 编译
cjc -L . -l native main.cj -o main.exe
./main.exe

# 3.2 基于 cjpm 项目构建
# 将 libnative.dll 放到 libs/ 目录下（用于编译链接）
# 基于前面提到的运行问题，libs/ 下还应放一个名为 native.dll 的副本
# 在 cjpm.toml 中配置 [ffi.c] native = { path = "./libs/" }
# 构建，依赖 libnative.dll
cjpm build
# 运行，依赖 native.dll
cjpm run
```
