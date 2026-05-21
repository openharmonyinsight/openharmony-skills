---
name: skills-index
description: "Index of available skills."
---

# Cangjie Compiler Skills Index

Available skills for working with the Cangjie compiler project and Anthropics official skills.

## Cangjie Skills

| Skill | Description |
|-------|-------------|
| [build-cangjie](./build-cangjie/SKILL.md) | 构建 Cangjie 编译器及其依赖（runtime, stdlib, stdx），以及工具（cjpm, cjfmt, cjlint, cjcov 等） |
| [run-cangjie-tests](./run-cangjie-tests/SKILL.md) | 运行 cangjie_test 仓库中的测试用例（HLT, LLT, cjcov, LSP） |
| [profile-cangjie](./profile-cangjie/SKILL.md) | 对 Cangjie 编译器进行性能分析和 profiling |
| [cangjie_compiler_knowledge](./cangjie_compiler_knowledge/SKILL.md) | 仓颉编译器知识库：概念说明、模块详情、关系图、源码导航，覆盖 18 模块 60+ 概念 |
| [cangjie_basic_concepts](./cangjie_basic_concepts/SKILL.md) | 仓颉编程语言基本概念和规则，包括关键字、标识符、程序结构、变量定义、作用域、表达式、函数等 |
| [cangjie_basic_data_type](./cangjie_basic_data_type/SKILL.md) | 仓颉语言基本数据类型：整数、浮点、布尔、字符(Rune)、字符串(String)、Unit、Nothing、元组、数组、区间等 |
| [cangjie_cffi](./cangjie_cffi/SKILL.md) | 仓颉程序与C程序互操作：foreign声明、CFunc、inout参数、unsafe块、类型映射、C回调仓颉、内存管理 |
| [cangjie_class](./cangjie_class/SKILL.md) | 仓颉语言类：类定义、抽象类、构造函数、终结器、继承、重写、重定义、成员变量、属性、访问修饰符 |
| [cangjie_collections](./cangjie_collections/SKILL.md) | 仓颉集合数据类型：Array/ArrayList/HashMap/HashSet 的使用文档 |
| [cangjie_concurrency](./cangjie_concurrency/SKILL.md) | 仓颉语言并发编程：M:N线程模型、spawn、原子操作、互斥锁、条件变量、synchronized、Future、ThreadLocal |
| [cangjie_const](./cangjie_const/SKILL.md) | 仓颉语言 const 变量与 const 函数：编译时求值、const init 构造函数 |
| [cangjie_enum](./cangjie_enum/SKILL.md) | 仓颉语言枚举类型：enum定义规则、构造器、枚举成员函数和属性、递归枚举 |
| [cangjie_error_handle](./cangjie_error_handle/SKILL.md) | 仓颉语言错误处理：异常层次、自定义异常、throw、try/catch/finally、Option类型错误处理 |
| [cangjie_extend](./cangjie_extend/SKILL.md) | 仓颉语言扩展：直接扩展、接口扩展、泛型扩展、孤儿规则、导出与导入规则 |
| [cangjie_for](./cangjie_for/SKILL.md) | 仓颉语言 for-in 迭代：Iterable/Iterator 接口、Range 区间类型、迭代控制、自定义迭代器 |
| [cangjie_full_docs](./cangjie_full_docs/SKILL.md) | 仓颉语言完整文档：语言规范、标准库、扩展标准库、工具链的原始文档 |
| [cangjie_function](./cangjie_function/SKILL.md) | 仓颉语言函数：函数定义、命名参数、默认值、函数类型、Lambda表达式、闭包、运算符重载、管道运算符 |
| [cangjie_generic](./cangjie_generic/SKILL.md) | 仓颉语言泛型：泛型函数、泛型类、泛型接口、泛型约束、型变（协变/逆变/不型变） |
| [cangjie_interface](./cangjie_interface/SKILL.md) | 仓颉语言接口：接口定义、接口实现、接口继承、默认实现、sealed接口、Any类型、菱形继承 |
| [cangjie_macro](./cangjie_macro/SKILL.md) | 仓颉语言宏与元编程：Token/Tokens类型、quote表达式、非属性宏、属性宏、std.ast包 |
| [cangjie_network](./cangjie_network/SKILL.md) | 仓颉网络编程：socket/tcp/udp/tls/http/https/websocket |
| [cangjie_option](./cangjie_option/SKILL.md) | 仓颉语言 Option 类型：?T 简写、coalescing 操作符(??)、问号操作符(?.)、if-let/while-let 解构 |
| [cangjie_package](./cangjie_package/SKILL.md) | 仓颉语言包管理：package声明、main入口、import、public import、访问修饰符 |
| [cangjie_pattern_match](./cangjie_pattern_match/SKILL.md) | 仓颉语言模式匹配：match 表达式、模式类型（常量/通配符/绑定/元组/类型/枚举）、模式守卫 |
| [cangjie_project_management](./cangjie_project_management/SKILL.md) | 仓颉项目管理工具 cjpm：项目配置(cjpm.toml)、构建、测试、交叉编译、构建脚本 |
| [cangjie_reflect_and_annotation](./cangjie_reflect_and_annotation/SKILL.md) | 仓颉语言反射与注解：整数溢出注解、自定义注解(@Annotation)、反射(TypeInfo) |
| [cangjie_regulations](./cangjie_regulations/SKILL.md) | 仓颉项目规范准则：项目结构、命名、格式化、错误处理、测试、并发、安全规范 |
| [cangjie_std](./cangjie_std/SKILL.md) | 仓颉语言标准库：类型转换、格式化字串、文件系统、IO流、命令行参数、单元测试框架 |
| [cangjie_stdx](./cangjie_stdx/SKILL.md) | 仓颉语言扩展标准库 stdx：配置构建、json编解码 |
| [cangjie_string](./cangjie_string/SKILL.md) | 仓颉标准库 String 类型：构造、搜索、替换、分割、拼接、裁剪、大小写转换、迭代 |
| [cangjie_struct](./cangjie_struct/SKILL.md) | 仓颉语言结构体：struct定义、构造函数、值语义、mut函数 |
| [cangjie_toolchains](./cangjie_toolchains/SKILL.md) | 仓颉语言工具链：cjc编译器、cjdb调试器、cjcov覆盖率、cjfmt格式化、cjlint静态检查、cjprof性能分析 |
| [cangjie_type_system](./cangjie_type_system/SKILL.md) | 仓颉语言类型系统：子类型关系、型变规则、类型转换（is/as）、Nothing/Any/Object |
| [power-gitcode](./power-gitcode/SKILL.md) | GitCode 平台全能操作：PR/Issue 管理、评论、标签、合并、模板读取、仓库 Fork/Release |
| [aceharness-spec-coding](./aceharness-spec-coding/SKILL.md) | ACEHarness Spec Coding：维护 specs/changes 正式规范制品，区分规范源与运行时结构化投影 |
| [aceflow-chat-card](./aceflow-chat-card/SKILL.md) | 通用富文本卡片渲染：12 种 Block 类型，AI 通过 JSON 动态生成可视化卡片 |
| [aceflow-workflow-creator](./aceflow-workflow-creator/SKILL.md) | 引导用户创建 AceFlow 工作流配置，提供格式规范和校验脚本 |

## HarmonyOS Skills

| Skill | Description |
|-------|-------------|
| [harmonyos-project-init](./harmonyos-project-init/SKILL.md) | 仓颉鸿蒙项目初始化：创建完整的项目模板结构和文件内容，从零开始创建可运行的仓颉鸿蒙 Hello World 项目 |
| [harmonyos-requirement-analysis](./harmonyos-requirement-analysis/SKILL.md) | 鸿蒙应用需求技术化分析：将业务需求转换为 UI 组件、数据结构和交互方式 |
| [harmonyos-build](./harmonyos-build/SKILL.md) | 鸿蒙应用构建：执行完整构建流程，包含依赖安装、仓颉预编译、资源生成、编译、打包等步骤 |
| [harmonyos-evolution](./harmonyos-evolution/SKILL.md) | 鸿蒙构建问题追踪：记录和分析构建失败日志，将重难点解决方案沉淀至 Evolution.md |
| [harmonyos-vec-retriever-guide](./harmonyos-vec-retriever-guide/SKILL.md) | 鸿蒙 L1 RAG 检索：基于向量数据库和 BM25 混合检索，快速精准检索代码片段和概念 |
| [harmonyos-doc-search-guide](./harmonyos-doc-search-guide/SKILL.md) | 鸿蒙本地文档搜索：基于本地离线官方文档进行全量检索与精读，获取权威语法和 API 用法 |
| [harmonyos-stdx-dependency](./harmonyos-stdx-dependency/SKILL.md) | 鸿蒙 stdx 依赖配置：指导 stdx 拓展库的配置和 bin-dependencies.path-option 设置 |

## Anthropics Official Skills

| Skill | Description |
|-------|-------------|
| [algorithmic-art](./algorithmic-art/SKILL.md) | Creating algorithmic art using p5.js with seeded randomness |
| [brand-guidelines](./brand-guidelines/SKILL.md) | Applies Anthropic's official brand colors and typography |
| [canvas-design](./canvas-design/SKILL.md) | Create visual art in .png and .pdf using design philosophy |
| [claude-api](./claude-api/SKILL.md) | Build apps with the Claude API or Anthropic SDK |
| [doc-coauthoring](./doc-coauthoring/SKILL.md) | Structured workflow for co-authoring documentation |
| [docx](./docx/SKILL.md) | Create, read, edit, or manipulate Word documents (.docx) |
| [frontend-design](./frontend-design/SKILL.md) | Create distinctive, production-grade frontend interfaces |
| [internal-comms](./internal-comms/SKILL.md) | Write internal communications using company formats |
| [mcp-builder](./mcp-builder/SKILL.md) | Guide for creating high-quality MCP servers |
| [pdf](./pdf/SKILL.md) | Read, create, edit, merge, split, and process PDF files |
| [pptx](./pptx/SKILL.md) | Create, read, edit PowerPoint presentations (.pptx) |
| [skill-creator](./skill-creator/SKILL.md) | Create, modify, and improve skills with eval support |
| [slack-gif-creator](./slack-gif-creator/SKILL.md) | Create animated GIFs optimized for Slack |
| [theme-factory](./theme-factory/SKILL.md) | Toolkit for styling artifacts with professional themes |
| [web-artifacts-builder](./web-artifacts-builder/SKILL.md) | Build multi-component HTML artifacts with React and shadcn/ui |
| [webapp-testing](./webapp-testing/SKILL.md) | Test web applications using Playwright |
| [xlsx](./xlsx/SKILL.md) | Create, read, edit spreadsheet files (.xlsx, .csv, .tsv) |

## Structure

```
skills/
├── SKILL.md                              # This index file
│
├── 编译器工具链 (Compiler Toolchain)
├── build-cangjie/
│   ├── SKILL.md                          # 构建说明
│   ├── REFERENCE.md                      # 平台配置、参数、环境变量
│   ├── LICENSE
│   └── scripts/
│       └── build-cangjie.py              # 自动化构建脚本
├── run-cangjie-tests/
│   ├── SKILL.md                          # 测试运行说明
│   ├── REFERENCE.md                      # 测试框架参数
│   ├── LICENSE
│   └── scripts/
│       └── run-cangjie-tests.py          # 测试运行辅助脚本
├── profile-cangjie/
│   ├── SKILL.md                          # 性能分析指南
│   ├── REFERENCE.md                      # 性能分析工具和参数
│   ├── LICENSE
│   └── scripts/
│       └── profile-cangjie.py            # 性能分析辅助脚本
├── cangjie_compiler_knowledge/
│   ├── SKILL.md                          # 编译器知识库使用指南
│   ├── REFERENCE.md                      # 检索命令、知识库结构
│   ├── LICENSE
│   ├── knowledge-base/                   # 知识库数据
│   │   ├── descriptions/                 # 概念描述文档
│   │   ├── modules/                      # 模块信息
│   │   ├── graphs/                       # 概念关系图
│   │   ├── search-index.json            # 搜索索引
│   │   └── cross-references.json        # 交叉引用
│   └── scripts/
│       └── search.py                     # 知识库检索脚本
│
├── 仓颉语言技能 (Cangjie Language Skills)
├── cangjie-evolution/
│   ├── SKILL.md                          # 普通工程问题追踪指南
│   └── Evolution.md                      # 问题记录文件
├── cangjie-vec-retriever-guide/
│   ├── SKILL.md                          # 混合检索指南
│   └── scripts/
│       └── ask_cangjie.py                # 向量+BM25混合检索脚本
├── cangjie-doc-search-guide/
│   ├── SKILL.md                          # 本地文档搜索指南
│   └── kernel/                           # 仓颉官方文档
│       └── source_zh_cn/                 # 中文文档
├── cangjie_basic_concepts/SKILL.md        # 仓颉基本概念
├── cangjie_basic_data_type/SKILL.md      # 基本数据类型
├── cangjie_cffi/SKILL.md                 # C/C++ 互操作
├── cangjie_class/SKILL.md                # 类
├── cangjie_collections/SKILL.md           # 集合类型
├── cangjie_concurrency/SKILL.md           # 并发编程
├── cangjie_const/SKILL.md                # const 变量与函数
├── cangjie_enum/SKILL.md                 # 枚举类型
├── cangjie_error_handle/SKILL.md         # 错误处理
├── cangjie_extend/SKILL.md               # 扩展
├── cangjie_for/SKILL.md                  # for-in 迭代
├── cangjie_full_docs/SKILL.md            # 完整文档
├── cangjie_function/SKILL.md             # 函数
├── cangjie_generic/SKILL.md              # 泛型
├── cangjie_interface/SKILL.md             # 接口
├── cangjie_macro/SKILL.md                # 宏与元编程
├── cangjie_network/SKILL.md              # 网络编程
├── cangjie_option/SKILL.md               # Option 类型
├── cangjie_package/SKILL.md               # 包管理
├── cangjie_pattern_match/SKILL.md        # 模式匹配
├── cangjie_project_management/SKILL.md   # 项目管理 cjpm
├── cangjie_reflect_and_annotation/SKILL.md  # 反射与注解
├── cangjie_regulations/SKILL.md          # 项目规范准则
├── cangjie_std/SKILL.md                  # 标准库
├── cangjie_stdx/SKILL.md                 # 扩展标准库 stdx
├── cangjie_string/SKILL.md               # String 类型
├── cangjie_struct/SKILL.md               # 结构体
├── cangjie_toolchains/SKILL.md           # 工具链
├── cangjie_type_system/SKILL.md          # 类型系统
│
├── 鸿蒙应用技能 (HarmonyOS Skills)
├── base-skill/
│   └── SKILL.md                          # 强制前置入口（仓颉/鸿蒙项目）
├── harmonyos-project-init/
│   └── SKILL.md                          # 鸿蒙项目初始化
├── harmonyos-requirement-analysis/
│   └── SKILL.md                          # 需求技术化分析
├── harmonyos-build/
│   ├── SKILL.md                          # 鸿蒙构建流程
│   └── scripts/
│       └── build.py                      # Python 构建脚本
├── harmonyos-evolution/
│   ├── SKILL.md                          # 构建问题追踪
│   └── Evolution.md                      # 问题记录文件
├── harmonyos-vec-retriever-guide/
│   └── SKILL.md                          # L1 RAG 检索
├── harmonyos-doc-search-guide/
│   └── SKILL.md                          # L3 本地文档搜索
├── harmonyos-stdx-dependency/
│   ├── SKILL.md                          # stdx 依赖配置
│   └── stdx/                             # stdx 拓展库
│
├── 平台集成 (Platform Integration)
├── power-gitcode/
│   ├── SKILL.md                          # GitCode 操作指南
│   ├── PROMPT.md                         # 系统提示词注入
│   ├── REFERENCE.md                      # API 接口文档
│   └── scripts/
│       └── power-gitcode.py              # GitCode CLI 工具
│
├── 工作流与卡片 (Workflow & Cards)
├── aceflow-chat-card/
│   ├── SKILL.md                          # 富文本卡片渲染
│   ├── PROMPT.md                         # 系统提示词注入
│   ├── REFERENCE.md                      # Block 类型速查
│   └── scripts/
│       └── validate-card.mjs             # 卡片校验脚本
├── aceflow-workflow-creator/
│   ├── SKILL.md                          # 工作流创建
│   ├── PROMPT.md                         # 系统提示词注入
│   └── scripts/
│       └── ...                           # 其他技能脚本
│
├── Anthropics 官方技能 (Official Skills)
├── algorithmic-art/SKILL.md              # 算法艺术
├── brand-guidelines/SKILL.md             # 品牌指南
├── canvas-design/SKILL.md                # 画布设计
├── claude-api/SKILL.md                  # Claude API
├── doc-coauthoring/SKILL.md              # 文档协作
├── docx/SKILL.md                         # Word 文档
├── frontend-design/SKILL.md              # 前端设计
├── internal-comms/SKILL.md                # 内部通信
├── mcp-builder/SKILL.md                  # MCP 服务器构建
├── pdf/SKILL.md                          # PDF 处理
├── pptx/SKILL.md                         # PowerPoint
├── skill-creator/SKILL.md                # 技能创建
├── slack-gif-creator/SKILL.md            # Slack GIF
├── theme-factory/SKILL.md                # 主题工厂
├── web-artifacts-builder/SKILL.md        # Web 构建
├── webapp-testing/SKILL.md               # Web 测试
└── xlsx/SKILL.md                         # 表格处理
```

## Supported Platforms

All skills support:
- `linux_x86_64`
- `linux_aarch64`
- `mac_x86_64`
- `mac_aarch64`
- `windows_x64`

**CRITICAL**: 当用户要求**创建或生成**仓颉/鸿蒙项目时，必须**首先**调用 `base-skill`。

### 鸿蒙应用开发 Skill 触发条件

仅当用户请求明确包含以下意图时触发：

**技术关键词**（任选其一）：

- 仓颉 / Cangjie / cangjie
- 鸿蒙 / HarmonyOS / harmonyos

**动作关键词**（必须包含）：

- 创建 / 生成 / 初始化 / 新建 / 开发一个新项目

**触发示例**：

| 用户输入                     | 是否触发             |
| ---------------------------- | -------------------- |
| "创建一个仓颉项目"           | ✓                    |
| "生成鸿蒙应用"               | ✓                    |
| "帮我开发一个仓颉命令行工具" | ✓                    |
| "初始化 HarmonyOS 项目"      | ✓                    |
| "查询 ArkUI 组件用法"        | ✗ 仅查询，不触发     |
| "修改 module.json5"          | ✗ 仅修改，不触发     |
| "添加依赖"                   | ✗ 仅配置修改，不触发 |

### 执行流程

1. 检测到项目生成需求 → 调用 `skill({ name: "base-skill" })`
2. 阅读 `base-skill` 内容 → 按流程执行

### 其他操作

对于**非项目生成**的操作（如查询、修改配置等），直接执行对应操作，无需调用 base-skill。

## 关键约束

1. **严禁猜语法**: 遇到不确定的 API/语法，必须通过 Skills 或官方文档确认
2. **禁止修改 stdx**: stdx 本地库已预编译，严禁修改其内任何文件
