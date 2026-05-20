---
name: cangjie-toolchains-cjc
description: "仓颉编译器 cjc 核心用法。"
---

# 仓颉编译器 cjc 核心用法

## 1. 基本用法

```bash
cjc [option] file...          # 编译 .cj 文件，默认生成可执行文件 main
cjc hello.cj                  # 最简编译
cjc hello.cj -o hello         # 指定输出文件名
```

- `cjc-frontend`：仅前端编译器，输出 LLVM IR（`.bc`）
- `cjc`：自动完成 前端 + 后端 + 链接

---

## 2. 核心选项速查

### 2.1 输出控制

| 选项 | 说明 |
|------|------|
| `-o <file>` | 指定输出文件路径 |
| `--output-type=[exe\|staticlib\|dylib]` | 输出类型（默认 `exe`） |
| `--output-dir <dir>` | 中间文件与输出保存目录 |

```bash
cjc tool.cj --output-type=dylib           # 生成动态库 libtool.so
cjc tool.cj --output-type=staticlib       # 生成静态库 libtool.a
```

### 2.2 包与模块

| 选项 | 说明 |
|------|------|
| `-p`, `--package` | 编译整个包目录 |
| `--module-name <name>` | 指定模块名 |
| `--import-path <dir>` | 添加 `.cjo` 文件搜索路径（同 `CANGJIE_PATH`） |

```bash
# 编译 log 包为静态库
cjc -p log --output-type=staticlib

# 使用库文件编译主程序
cjc main.cj liblog.a

# 指定模块名并编译
cjc -p src/log --module-name myModule --output-type=staticlib -o myModule/liblog.a
```

### 2.3 链接

| 选项 | 说明 |
|------|------|
| `-L <dir>` | 库文件搜索目录 |
| `-l <name>` | 链接库（搜索 `lib<name>.a/.so`） |
| `--static` | 静态链接仓颉库（仅 Linux） |
| `--static-std` / `--dy-std` | 静态/动态链接 std 模块 |
| `--static-libs` / `--dy-libs` | 静态/动态链接非 std 模块 |

```bash
# 链接 C 库
cjc main.cj -L . -l cProg

# 动态链接标准库（链接 dylib 产物时必须指定）
cjc main.cj mylib.so --dy-std --dy-libs
```

> **注意**：`--dy-std` 与 `--static-libs` 不可同时使用；`--static-std` 与 `--dy-libs` 不可同时使用。

### 2.4 调试与诊断

| 选项 | 说明 |
|------|------|
| `-g` | 生成调试信息（须配合 `-O0`） |
| `-V`, `--verbose` | 打印编译过程详细信息 |
| `-v`, `--version` | 打印编译器版本 |
| `-h`, `--help` | 打印帮助信息 |
| `--diagnostic-format=[default\|noColor\|json]` | 错误信息输出格式 |
| `--error-count-limit <N\|all>` | 限制打印错误数量（默认 8） |

### 2.5 测试

```bash
cjc a.cj --test               # 编译测试，入口变为 test_entry
cjc -p pkg --test              # 整包测试编译
cjc -p pkg --test-only -L out -l main  # 仅编译测试文件
```

### 2.6 宏

```bash
cjc --compile-macro macro.cj   # 编译宏定义，生成宏动态库
cjc main.cj --debug-macro      # 输出宏展开后的代码（用于调试）
```

### 2.7 条件编译

```bash
cjc main.cj --cfg "env=prod"   # 定义自定义条件编译变量
```

### 2.8 优化

| 选项 | 说明 |
|------|------|
| `-O0` / `-O1` / `-O2` / `-Os` / `-Oz` | 优化级别 |
| `--lto=[full\|thin]` | 链接时优化（仅 Linux） |
| `-j <N>`, `--jobs <N>` | 并行编译最大线程数 |
| `--int-overflow=[throwing\|wrapping\|saturating]` | 整数溢出策略（默认 `throwing`） |

```bash
cjc test.cj --lto=full         # Full LTO 优化
cjc test.cj -j 4               # 使用 4 线程并行编译
```

### 2.9 覆盖率与性能分析

```bash
cjc --coverage main.cj         # 编译支持覆盖率统计（须 -O0）
cjc test.cj --pgo-instr-gen    # PGO 插桩编译
cjc test.cj --pgo-instr-use=default.profdata  # 使用 profile 指导优化
```

### 2.10 交叉编译

```bash
# 指定目标平台
cjc hello.cj --target=x86_64-windows-gnu

# 使用 sysroot 简化工具链配置
cjc hello.cj --target=arch-os-env --sysroot /usr/sdk/arch-os-env
```

### 2.11 其他常用选项

| 选项 | 说明 |
|------|------|
| `--trimpath <prefix>` | 移除调试信息中的路径前缀 |
| `-s`, `--strip-all` | 删除输出文件中的符号表 |
| `--set-runtime-rpath` | 写入运行时库路径到 RPATH |
| `--disable-reflection` | 关闭反射信息生成 |
| `--no-sub-pkg` | 声明无子包以缩减 code size |
| `--stack-trace-format=[default\|simple\|all]` | 异常调用栈格式 |

---

## 3. 典型工作流

```bash
# 单文件编译运行
cjc hello.cj -o hello && ./hello

# 多包项目手动编译
cjc -p lib/utils --output-type=staticlib
cjc main.cj libutils.a -o app

# 带调试信息编译
cjc main.cj -g -O0 -o app_debug

# 发布优化构建
cjc main.cj -O2 --lto=full -s -o app_release
```

> **提示**：多文件项目推荐使用 `cjpm`（参见 `cangjie-project-management` Skill），无需手动管理编译依赖。
