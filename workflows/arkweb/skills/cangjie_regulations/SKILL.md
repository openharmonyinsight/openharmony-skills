---
name: cangjie-regulations
description: 仓颉项目规范准则。包括项目结构规范、命名规范、格式化规范、错误处理规范、测试规范、并发规范、安全规范、文档规范、依赖管理规范、版本控制规范等最佳实践指导
descriptionZH: 仓颉项目规范准则。包括项目结构规范、命名规范、格式化规范、错误处理规范、测试规范、并发规范、安全规范、文档规范、依赖管理规范、版本控制规范等最佳实践指导
tags:
  - 仓颉
  - 规范
---

# 仓颉项目规范准则

本规范基于仓颉语言特性、工具链能力及业界软件工程通用规范，为仓颉项目提供编码层面和项目层面的推荐准则。

---

## 1. 项目结构规范

### 1.1 标准目录布局

```
project-root/
├── cjpm.toml              # 项目配置（必要）
├── src/                   # 源代码目录
│   ├── main.cj            # 程序入口（executable 项目在根包中有 main 函数）
│   ├── kernal/            # 子包目录，与 package 声明一致
│   │   ├── engine.cj
│   │   └── driver.cj
│   └── utils/
│       ├── shell.cj
│       └── shell_test.cj  # shell.cj 对应的单元测试程序（可选）
├── tests/                 # 集成测试/端到端测试（可选）
├── bench/                 # 基准测试（可选）
├── docs/                  # 项目文档（可选）
├── examples/              # 示例代码（可选）
├── build.cj               # 构建脚本（可选）
├── cangjie-format.toml    # 格式化配置（可选）
├── target/                # 构建输出（不提交到版本控制）
├── .gitignore
└── README.md              # 项目介绍文档（推荐）
```

### 1.2 项目初始化

- 使用 `cjpm init --name <name> --type=executable|static|dynamic` 初始化项目，确保目录结构和 `cjpm.toml` 配置正确。
- `cjpm.toml` 中的 `name`、`version`、`cjc-version`、`output-type` 为必填字段。
- 版本号遵循语义化版本（Semantic Versioning）：`MAJOR.MINOR.PATCH`。

### 1.3 包与模块组织

- 每个子目录对应一个包，包名与目录名一致。
- `package` 声明必须是文件中第一条非注释语句，且路径与 `src/` 下的目录结构匹配。
- 单一职责原则：一个包聚焦于一个功能领域，避免包内包含不相关的类型或函数。
- 公共 API 放在包的顶层文件中，内部实现可通过 `internal`/`private` 控制可见性。
- 避免循环依赖：包之间的依赖关系应形成有向无环图（DAG）。

### 1.4 源文件组织

- 每个源文件聚焦一个主要类型或一组紧密相关的功能。
- 文件内代码推荐按以下顺序组织：
  1. `package` 声明
  2. `import` 语句
  3. 常量定义
  4. 类型定义（`class`/`struct`/`enum`/`interface`）
  5. 扩展（`extend`）
  6. 顶层函数
- 单元测试文件 `xxx_test.cj` 与被测文件 `xxx.cj` 同目录放置。

---

## 2. 命名规范

### 2.1 基本命名规则

| 元素 | 规则 | 示例 | 规则编号 |
|------|------|------|----------|
| 包名 | 全小写，可含数字和下划线 | `network`, `http_client` | G.NAM.01 |
| 源文件名 | 全小写加下划线，`.cj` 后缀 | `http_client.cj`, `user_service.cj` | G.NAM.02 |
| 类/接口/struct/枚举/类型别名 | 大驼峰（PascalCase） | `HttpClient`, `UserService` | G.NAM.03 |
| 函数名 | 小驼峰（camelCase） | `getData`, `parseResponse` | G.NAM.04 |
| 全局 `let` 和 `static let` 常量 | 全大写下划线分隔（SCREAMING_SNAKE_CASE） | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` | G.NAM.05 |
| 变量名 | 小驼峰（camelCase） | `itemCount`, `userName` | G.NAM.06 |
| 泛型类型参数 | 大写单字母或 PascalCase | `T`, `K`, `V`, `Element` | — |

### 2.2 命名最佳实践

- 名称应具有描述性和自文档性，避免使用无意义的缩写。
- 布尔类型变量/函数使用 `is`/`has`/`can`/`should` 等前缀，如 `isValid`、`hasPermission`。
- 集合类型变量使用复数形式，如 `users`、`orderItems`。
- 工厂方法使用 `create`/`from`/`of` 前缀，如 `createUser`、`fromJson`。
- 转换方法使用 `toXxx` 形式，如 `toString`、`toJson`。
- 避免使用保留关键字作为标识符；如必须使用，用反引号转义（如 `` `type` ``），但应优先选择替代名称。

---

## 3. 格式化规范

### 3.1 工具强制规则

使用 `cjfmt` 自动格式化，确保团队代码风格一致。推荐配置：

```toml
# cangjie-format.toml
indentWidth = 4
linelimitLength = 120
lineBreakType = "LF"
allowMultiLineMethodChain = false
```

### 3.2 核心格式规则

- **缩进**：统一使用 4 个空格，禁止使用 Tab。
- **行长度**：不超过 120 个字符。
- **大括号**：K&R 风格——左大括号在行末（前置 1 个空格），右大括号独占一行。`else`/`catch`/`finally` 与前一个右大括号同行。
- **空格**：
  - 冒号后加空格（类型声明、返回类型、命名参数）。
  - 二元操作符两侧各留一个空格。
  - 一元操作符与操作数之间不留空格。
  - 圆括号和方括号内部不留空格。
  - 区间操作符（`..`、`..=`）两侧不留空格。
- **空行**：移除多余的连续空行和大括号内首尾的空行。
- **修饰符排序**：`public` → `open`/`abstract` → `override`/`redef` → `static`。

### 3.3 代码组织格式

- 顶层声明之间保留一个空行。
- 函数体内通过空行分隔逻辑段落，增强可读性。
- `import` 语句分组：标准库导入在前，第三方库导入在后，组间用空行分隔。

---

## 4. 编码规范

### 4.1 变量与常量

- 优先使用 `let` 声明不可变变量，仅在需要修改时使用 `var`（G.VAR.01）。
- 编译期常量使用 `const` 声明。
- 避免变量遮盖（shadow），防止同名变量在嵌套作用域中造成混淆（G.DCL.01）。
- `public` 变量和函数必须显式声明类型（G.DCL.02）。
- 减少全局可变状态的使用（G.VAR.03）。

### 4.2 函数设计

- 单一职责：每个函数只完成一个明确的任务（G.FUN.01）。
- 禁止未使用的参数（G.FUN.02）；如确实需要占位，使用 `_` 命名。
- 函数参数数量建议不超过 5 个；参数过多时考虑使用结构体封装。
- 命名参数（`param!: Type`）用于提升可读性，尤其当参数含义不明确时。
- 合理使用默认参数值减少重载。
- 使用管道操作符（`|>`）和函数组合（`~>`）提升数据处理链的可读性。

### 4.3 类型设计

- **struct（值类型）**：用于轻量、不可变的数据对象，如坐标、颜色、配置项。
- **class（引用类型）**：用于需要继承、多态或共享引用的场景。
- **interface**：定义行为契约，支持多实现；优先面向接口编程。
- **enum**：表示有限的状态集合；利用参数化构造器携带关联数据。
- 类的继承层次不宜过深（建议不超过 3 层），优先使用组合而非继承。
- 使用 `sealed` 修饰 `class`/`interface` 限制继承范围到同一包内，增强可控性。
- 充分利用 `@Derive` 自动生成 `Equatable`、`Hashable` 等实现。

### 4.4 属性与访问控制

- 使用属性（`prop`/`mut prop`）替代公开字段，便于后续添加校验逻辑。
- 遵循最小可见性原则：默认使用 `private`，按需提升到 `internal` → `protected` → `public`。
- 安全检查方法禁止声明为 `open`，防止子类绕过安全逻辑（G.SEC.01）。

### 4.5 表达式与控制流

- 利用仓颉的表达式特性（`if`/`match`/`try` 均为表达式），简化赋值逻辑。
- `match` 表达式应覆盖所有分支，或显式使用 `_` 通配分支。
- 避免过深的嵌套（建议不超过 4 层），通过提前返回（early return）简化逻辑。
- `for-in` 循环优先使用 `where` 子句过滤，替代循环体内的 `if` 判断。

### 4.6 扩展（extend）

- 扩展用于为已有类型添加新方法或实现新接口，不用于修改已有行为。
- 遵守孤儿规则：扩展类型和扩展接口至少有一个在当前包中定义。
- 扩展中不能添加存储型成员变量。

---

## 5. 错误处理规范

### 5.1 异常使用原则

- 自定义异常继承自 `Exception`，禁止继承 `Error`（`Error` 仅用于系统级故障）。
- 异常用于真正的异常情况，不用于正常的控制流。
- `catch` 块应处理具体异常类型，避免裸 `catch (_)` 吞掉所有异常。
- `finally` 块用于资源清理，不在其中抛出新异常或执行业务逻辑。
- 实现了 `Resource` 接口的对象使用 `try-with-resources` 自动管理生命周期。

### 5.2 Option 类型使用

- 对于可预期的「无值」场景，优先使用 `Option<T>` 而非异常。
- 使用 `??` 提供默认值，使用 `?.` 安全链式访问。
- 使用 `if-let`/`while-let` 进行条件解包。
- 避免滥用 `getOrThrow()`，仅在确定值存在时使用。

### 5.3 错误传播

- 函数若无法处理异常，应让异常自然传播给调用者。
- 在 API 边界层统一捕获和转换异常，提供用户友好的错误信息。
- 日志记录异常时包含完整上下文信息，但禁止记录敏感数据（G.OTH.01）。

---

## 6. 并发编程规范

### 6.1 线程安全

- 仓颉采用 M:N 线程模型（语言线程调度到 OS 线程），使用 `spawn` 创建轻量级线程。
- 共享可变状态必须使用同步机制保护：`Mutex`、`synchronized`、原子操作。
- 优先使用 `synchronized` 块自动管理锁的获取和释放，避免手动 `lock`/`unlock` 遗漏。
- `Condition` 变量必须在持有对应 `Mutex` 锁时创建和使用。
- 禁止暴露内部锁对象到外部（G.CON.01），防止外部代码破坏同步逻辑。

### 6.2 并发最佳实践

- 使用不可变数据（`let`）减少共享可变状态的需求。
- 使用 `Future<T>` 获取异步任务的执行结果。
- 使用 `SyncCounter` 协调多线程的完成顺序。
- 使用 `ThreadLocal` 存储线程局部数据，避免不必要的锁竞争。
- 合理使用协作式取消（`Thread.currentThread.requestCancel()`）实现线程的优雅终止。
- 使用并发集合（`std.collection.concurrent` 中的 `ConcurrentHashMap`、`NonBlockingQueue` 等）替代手动加锁的普通集合。

---

## 7. 测试规范

### 7.1 测试组织

- 单元测试文件命名为 `xxx_test.cj`，与被测文件 `xxx.cj` 同目录放置。
- 使用 `@Test` 标注测试函数或测试类。
- 测试类中使用 `@TestCase` 标注每个测试用例方法。
- 测试名称应清晰描述被测行为，如 `addPositiveNumbers`、`throwOnInvalidInput`。

### 7.2 断言使用

- `@Expect`（软断言）：断言失败后继续执行后续断言，用于收集多个失败信息。
- `@Assert`（硬断言）：断言失败后立即停止当前测试。
- `@AssertThrows[ExType](expr)`：验证特定异常类型的抛出。
- `@PowerAssert`：在复杂表达式断言失败时显示中间值，便于调试。
- 每个测试用例至少包含一个断言。

### 7.3 测试最佳实践

- 测试遵循 AAA 模式：Arrange（准备）→ Act（执行）→ Assert（断言）。
- 每个测试用例独立，不依赖其他测试的执行顺序或状态。
- 使用 `@BeforeEach`/`@AfterEach` 进行测试前后的初始化和清理。
- 使用参数化测试（`@Test[x in ...]`）覆盖多组输入数据，减少重复代码。
- 使用 Mock 框架（`mock<T>()`/`spy<T>()`、`@On`、`@Called`）隔离外部依赖。
- 使用 `cjpm test --filter "pattern"` 运行特定测试。
- 使用 `cjcov` 生成覆盖率报告，关注分支覆盖率，目标覆盖率 ≥ 80%。

### 7.4 基准测试

- 使用 `@Bench` 标注基准测试函数。
- 基准测试放在独立文件或目录中，与功能测试分离。
- 使用 `cjpm bench` 运行基准测试。

---

## 8. 文档规范

### 8.1 代码注释

- 公共 API（`public` 类型、函数、属性）必须编写文档注释。
- 注释说明「为什么」而非「做了什么」——代码本身应表达意图。
- 多行注释中 `*` 保持对齐（`cjfmt` 会自动格式化）。
- 使用 `@Deprecated[message: "...", since: "版本号"]` 标注废弃的 API，并提供替代方案说明。

### 8.2 项目文档

- `README.md`：项目简介、快速开始、构建与运行方法、依赖说明。
- `CHANGELOG.md`（可选）：记录版本变更历史。
- `docs/`（可选）：存放详细的设计文档、API 文档、架构说明。
- 示例代码放在 `examples/` 目录中，保持可编译和可运行。

---

## 9. 依赖管理规范

### 9.1 依赖声明

- 所有外部依赖在 `cjpm.toml` 的 `[dependencies]` 中显式声明。
- 测试专用依赖在 `[test-dependencies]` 中声明，不打包到正式产物中。
- 指定明确的版本或版本范围，避免使用不固定版本。

```toml
[dependencies]
http_lib = { git = "https://example.com/http_lib.git", tag = "v1.2.0" }
utils = { path = "./libs/utils" }

[test-dependencies]
test_helper = { path = "./libs/test_helper" }
```

### 9.2 依赖管理实践

- 使用 `cjpm check` 检查依赖状态，使用 `cjpm update` 更新依赖。
- 使用 `cjpm tree` 查看依赖树，排查间接依赖冲突。
- 定期审查依赖的安全性和版本更新。
- 最小化外部依赖数量，优先使用标准库（`std.*`）和扩展标准库（`stdx.*`）提供的功能。

---

## 10. 安全规范

### 10.1 输入校验

- 跨信任边界的数据必须进行校验（G.CHK.01），包括外部输入、文件内容、网络数据。
- 使用 `Option` 类型和模式匹配安全地处理可能缺失的数据。

### 10.2 敏感信息保护

- 禁止在源代码中硬编码敏感信息（密码、密钥、Token 等）（G.OTH.02）。
- 禁止在日志中保存敏感数据（G.OTH.01）。
- 敏感配置通过环境变量或安全配置管理系统注入。

### 10.3 FFI 安全

- FFI 调用限制在 `unsafe` 块中，最小化 `unsafe` 代码范围。
- 对 C 函数传入的数据进行严格校验。
- 使用 `CPointerResource`/`CStringResource` 等 RAII 类型管理 FFI 内存，避免内存泄漏。
- `@FastNative` 仅用于不阻塞、不回调仓颉、执行时间短的 C 函数。

### 10.4 并发安全

- 遵循第 6 节并发规范，避免数据竞争和死锁。
- 安全检查方法禁止声明为 `open`（G.SEC.01）。

---

## 11. 工具链集成规范

### 11.1 持续集成流程

推荐在 CI/CD 流程中依次执行以下步骤：

```bash
cjpm build               # 1. 编译构建
cjfmt -d src/            # 2. 代码格式化（格式化后检查是否有变更，有则说明代码未预先格式化）
cjlint -f src/           # 3. 静态代码检查
cjpm test                # 4. 运行测试
cjcov --format html      # 5. 生成覆盖率报告
```

### 11.2 工具配置

- 项目根目录维护 `cangjie-format.toml` 统一格式化配置。
- 使用 `config/cjlint_rule_list.json` 定义启用的检查规则集合。
- 启用 G.FMT.13 规则时，在源文件头添加版权注释。
- 使用构建脚本 `build.cj` 的 `pre-build`/`post-build` 钩子集成自定义检查。

### 11.3 调试与性能分析

- 使用 `cjdb` 进行断点调试和变量检查。
- 使用 `cjprof` 进行 CPU 采样和堆内存分析，定位性能瓶颈。
- 使用 `cjcov` 的分支覆盖率模式（`--branch`）检查测试覆盖质量。

