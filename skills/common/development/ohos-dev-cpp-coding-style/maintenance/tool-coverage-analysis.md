# OpenHarmony C++ 规范的工具覆盖清单

## 目标
本文件只列出两类内容：

- 本规范中可以由 `clang-format` 承接的条目
- 本规范中可以由 `clang-tidy` 承接或近似承接的条目

不在本规范里的规则不纳入。

## `clang-format` 覆盖

这些规则主要是版式、缩进、空格和大括号风格，适合直接交给 `.clang-format`。

| 规范条目 | 覆盖方式 | 说明 |
|---|---|---|
| 3.1.1 行宽不超过 120 | `ColumnLimit: 120` | 直接覆盖。 |
| 3.2.1 4 空格缩进、禁 Tab | `UseTab: Never`, `IndentWidth: 4` | 直接覆盖。 |
| 3.3.1 K&R 大括号风格 | `BreakBeforeBraces: Custom` + `BraceWrapping` | 直接覆盖主要风格。 |
| 3.4.1 函数声明/定义换行对齐 | clang-format 自动处理 | 近似覆盖。 |
| 3.5.1 函数调用参数换行对齐 | clang-format 自动处理 | 近似覆盖。 |
| 3.6.2 禁止 if/else/else if 写在同一行 | `AllowShortIfStatementsOnASingleLine: Never` | 直接覆盖。 |
| 3.8.1 switch 的 case/default 缩进一层 | `IndentCaseLabels: true` | 直接覆盖。 |
| 3.9.1 表达式换行一致性 | clang-format 自动处理 | 近似覆盖。 |
| 3.11.1 初始化换行缩进/对齐 | clang-format 自动处理 | 近似覆盖。 |
| 3.14.1 水平空格规则 | `Space*` 系列选项 | 覆盖主要空格风格。 |
| 3.15.1 访问控制块与 class 对齐 | `AccessModifierOffset: -4` | 直接覆盖。 |
| 3.15.2 构造函数初始化列表排版 | `SpaceBeforeCtorInitializerColon` 等 | 覆盖主要风格。 |
| 4.4.2 注释与代码间空格/对齐 | clang-format 可整理部分样式 | 只能部分覆盖。 |

## `clang-tidy` 覆盖

这些规则适合交给 AST/静态检查。部分条目是“近似覆盖”，因为 `clang-tidy` 不能完全表达规范原文的全部语义。

| 规范条目 | 对应检查 | 说明 |
|---|---|---|
| 2.5.1 全局变量 `g_` 前缀 | `readability-identifier-naming` | 直接覆盖。 |
| 2.5.2 类成员变量后缀 `_` | `readability-identifier-naming` | 对私有/受保护成员可直接覆盖；对 `struct`/公有类成员存在局限。 |
| 2.3/2.4/2.6 命名风格相关 | `readability-identifier-naming` | 类型、函数、命名空间、枚举值、全局常量等可覆盖主要命名风格。 |
| 3.13.2 避免使用宏 | `cppcoreguidelines-macro-usage` | 近似覆盖；允许的 guard / logging 宏通过正则放行。 |
| 3.13.3 禁止使用宏表示常量 | `cppcoreguidelines-macro-usage` | 近似覆盖；常量宏会被宏使用检查抓到。 |
| 3.13.4 禁止使用函数式宏 | `cppcoreguidelines-macro-usage` | 近似覆盖；必要日志宏通过正则放行。 |
| 6.1.1 不要在头文件或 include 前 using namespace | `google-build-using-namespace` | 主要覆盖 `using namespace`。对“include 前”这一时序约束不单独区分。 |
| 9.3.1 使用 C++ 风格转换，不用 C 风格转换 | `cppcoreguidelines-pro-type-cstyle-cast` | 直接覆盖 C 风格 cast。 |
| 10.1.1 重写虚函数使用 override/final | `modernize-use-override` | 主要覆盖 `override`。`final` 仍需人工判断。 |
| 10.1.3 使用 nullptr，不用 NULL/0 | `modernize-use-nullptr` | 直接覆盖。 |

## 当前不由 clang 工具可靠覆盖的条目

这些仍应留给 skill、脚本级自定义检查、编译器告警或人工 review：

- 2.2.1 / 2.2.2 文件后缀和文件名
- 4.1 文件头版权许可
- 4.3.1 / 4.3.2 public 接口注释质量
- 5.2.1 头文件循环依赖
- 5.2.3 禁止通过 extern 偷引接口
- 5.2.4 禁止在 `extern "C"` 中包含头文件
- 5.2.1 建议 尽量避免前置声明
- 6.1.1 cpp 内部符号放匿名 namespace
- 6.2.1 / 6.3.1 命名空间组织策略
- 7.1.3 / 7.1.7 / 7.2.1 / 7.2.2 / 7.2.3 对象语义与继承设计
- 9.4.1 / 9.4.1建议 资源释放匹配与 RAII
- 9.5.1 不保存 `c_str()` 指针
- 9.8.1 禁止泛型编程
- 10.2.1 / 10.4.1 智能指针与接口所有权风格
- 10.3.1 / 10.3.2 / 10.3.3 lambda 捕获策略

## 使用方式

未来 skill 不直接解释配置细节，只调用守护脚本。以下命令以本 skill 目录为当前目录：

```bash
python3 scripts/oh_cpp_guard.py .
```

或只检查格式：

```bash
python3 scripts/oh_cpp_guard.py --format-only .
```

或只跑 tidy：

```bash
python3 scripts/oh_cpp_guard.py --tidy-only path/to/file.cpp
```
