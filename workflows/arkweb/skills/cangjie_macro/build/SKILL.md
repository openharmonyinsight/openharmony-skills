---
name: cangjie-macro-build
description: "仓颉宏包编译构建说明。"
---

# 仓颉宏包编译构建 Skill

## 1. 宏包编译规则

### 1.1 包规则
- 宏须在 `macro package` 声明的包中
- 宏包中仅宏定义可为 `public`；其他声明为包内部可见
- 宏包**可以**重新导出宏包和非宏包的符号。非宏包**不能**重新导出宏包符号
- 宏定义和调用**须**在不同包中

---

## 2. 使用 cjc 编译

宏包须**先编译**，使用 `--compile-macro` 标志，然后编译调用包并链接宏包。

### 2.1 基本编译流程

```shell
# 步骤 1：编译宏包
cjc macros/m.cj --compile-macro --output-dir ./target

# 步骤 2：编译调用包并链接宏包
cjc src/demo.cj -o demo --import-path ./target
```

### 2.2 多模块场景

当宏包依赖其他非宏包时，须按依赖顺序编译：

```shell
cjc A.cj --compile-macro                    # 编译宏包
cjc B.cj --output-type=dylib -o libB.so     # 编译依赖库（Linux）
cjc C.cj --compile-macro -L. -lB            # 编译带依赖的宏包
cjc main.cj -o main -L. -lB                 # 编译主程序
```

### 2.3 不同平台的注意事项

| 平台 | 动态库扩展名 | 示例 |
|------|-------------|------|
| Linux | `.so` | `cjc B.cj --output-type=dylib -o libB.so` |
| macOS | `.dylib` | `cjc B.cj --output-type=dylib -o libB.dylib` |
| Windows | `.dll` | `cjc B.cj --output-type=dylib -o B.dll` |

---

## 3. 使用 cjpm 构建（推荐）

### 3.1 项目结构

```text
my_project/
├── cjpm.toml              # 主项目配置
├── src/
│   └── main.cj            # 调用宏的代码
└── macros/                 # 宏模块
    ├── cjpm.toml           # 宏模块配置
    └── src/
        └── my_macros.cj    # 宏定义
```

### 3.2 宏模块 cjpm.toml

宏模块的 `cjpm.toml` 必须设置 `compile-option = "--compile-macro"`：

```toml
[package]
cjc-version = "0.55.3"
name = "macros"
version = "1.0.0"
output-type = "static"
compile-option = "--compile-macro"
```

### 3.3 主项目 cjpm.toml

在主项目 `cjpm.toml` 中以本地路径依赖方式引用宏模块：

```toml
[package]
cjc-version = "0.55.3"
name = "my_project"
version = "1.0.0"
output-type = "executable"

[dependencies]
macros = { path = "./macros" }
```

### 3.4 构建与运行

```bash
cjpm build      # 自动按依赖顺序编译宏包和主包
cjpm run        # 构建并运行
cjpm test       # 运行测试
```

### 3.5 多宏模块项目结构

当项目包含多个宏模块时，可以组织为：

```text
my_project/
├── cjpm.toml
├── src/
│   └── main.cj
├── macro_a/
│   ├── cjpm.toml          # compile-option = "--compile-macro"
│   └── src/
│       └── macro_a.cj
└── macro_b/
    ├── cjpm.toml          # compile-option = "--compile-macro"
    └── src/
        └── macro_b.cj
```

主项目 `cjpm.toml`：

```toml
[dependencies]
macro_a = { path = "./macro_a" }
macro_b = { path = "./macro_b" }
```

---

## 4. 并行宏展开

- 使用 `--parallel-macro-expansion` 标志启用并行宏展开
- **警告**：使用全局变量的宏在并行展开时不安全
- 可通过 `cjpm.toml` 中 `compile-option` 添加：

```toml
[package]
compile-option = "--parallel-macro-expansion"
```

---

## 5. 调试模式

- `--debug-macro` 生成 `.macrocall` 临时文件显示完全展开的宏代码
- 用于开发阶段排查宏展开结果是否符合预期

```shell
# cjc 直接使用
cjc src/demo.cj --debug-macro --import-path ./target

# cjpm 中通过 compile-option 使用
# cjpm.toml
[package]
compile-option = "--debug-macro"
```

---

## 6. 常见问题

### 6.1 编译顺序错误
- **现象**：编译调用包时报找不到宏定义
- **原因**：宏包未先编译或 `--import-path` 未正确指向宏包输出目录
- **解决**：确保先用 `--compile-macro` 编译宏包，再编译调用包。使用 cjpm 时工具会自动处理编译顺序

### 6.2 宏包中非宏符号导出
- **现象**：宏包中的辅助函数在外部不可见
- **原因**：宏包中仅宏定义可为 `public`
- **解决**：将辅助函数放到独立的非宏包中，宏包和调用包分别依赖该非宏包
