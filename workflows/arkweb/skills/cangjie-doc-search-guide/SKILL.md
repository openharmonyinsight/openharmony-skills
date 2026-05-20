---
name: cangjie-doc-search-guide
description: "[考古层] 当基础 Skills 和 cangjie-vec-retriever-guide 的 L1
  语义检索无法给出可靠答案或终端返回 NO_RAG_RESULT 时被调用，基于本地离线官方文档进行全量检索与精读，定位权威仓颉语法、标准库与 stdx
  扩展库的规范用法。"
descriptionZH: "[考古层] 当基础 Skills 和 cangjie-vec-retriever-guide 的 L1
  语义检索无法给出可靠答案或终端返回 NO_RAG_RESULT 时被调用，基于本地离线官方文档进行全量检索与精读，定位权威仓颉语法、标准库与 stdx
  扩展库的规范用法。"
tags:
  - 仓颉
  - 文档搜索
  - 本地文档
---

# cangjie-doc-search-guide

## 目的

当基础 Skills 与 `cangjie-vec-retriever-guide` 的 L1 语义检索都无法给出足够可靠的答案时，由本 Skill 进入 **L3 官方文档“考古”阶段**，通过离线本地文档的结构化索引，精确查找：

- 语法级特性与示例；
- 标准库（`stdlib`）各模块的 API 说明与使用规范；
- 扩展库（`stdx`）组件的官方教程与示例；
- 与编译、构建、工具链相关的官方说明。

> 本 Skill 的核心目标：**严禁凭空猜测仓颉语法或 API**，所有实现与修改必须以官方文档为最终依据。

## 官方文档索引总览

所有本地官方文档索引文件位于：

```text
skills/utils/scripts/hm-docs/index/
```

根据核心技术关键词的不同，当前可用的 4 个主索引为：

1. **语言基础特性与语法** → 目标索引: `syntax.md`

   覆盖的主要内容包括（节选，与原始官方文档结构保持一致）：

   - 基本概念（标识符、程序结构、表达式、函数）
   - 基础数据类型（基本操作符、整数类型、浮点类型、布尔类型、字符类型、字符串类型、元组类型、数组类型、区间类型、Unit 类型、Nothing 类型）
   - 函数（定义函数、调用函数、函数类型、嵌套函数、Lambda 表达式、闭包、函数调用语法糖、函数重载、操作符重载、const 函数和常量求值）
   - 结构类型（定义 struct 类型、创建 struct 实例、mut 函数）
   - 枚举类型和模式匹配（枚举类型、Option 类型、模式概述、模式的 Refutability、match 表达式、其他使用模式的地方）
   - 类和接口（类、接口、属性、子类型关系、类型转换）
   - 泛型（泛型概述、泛型函数、泛型接口、泛型类、泛型结构体、泛型枚举、泛型类型的子类型关系、类型别名、泛型约束）
   - 扩展（扩展概述、直接扩展、接口扩展、访问规则）
   - Collection 类型（基础 Collection 类型概述、ArrayList、HashSet、HashMap、Iterable 和 Collections）
   - 包（包的概述、包的声明、顶层声明的可见性、包的导入、程序入口）
   - 异常处理（定义异常、throw 和处理异常、常见运行时异常、使用 Option）
   - 并发编程（并发概述、创建线程、访问线程、终止线程、同步机制、线程睡眠指定时长 sleep）
   - 基础 I/O 操作（I/O 流概述、I/O 节点流、I/O 处理流）
   - 网络编程（网络编程概述、Socket 编程、HTTP 编程、WebSocket 编程）
   - 宏（宏的简介、Tokens 相关类型和 quote 表达式、语法节点、宏的实现、编译、报错与调试、宏包定义和导入、内置编译标记、实用案例）
   - 反射和注解（动态特性、注解）
   - 跨语言互操作（仓颉-C 互操作）
   - 编译和构建（`cjc` 使用、`cjpm` 介绍、条件编译）
   - 部署和运行（部署仓颉运行时、运行仓颉可执行程序）
   - 附录（`cjc` 编译选项、Linux 版本工具链的支持与安装、runtime 环境变量使用手册、关键字、操作符、操作符函数、TokenKind 类型、仓颉包兼容性检查）

2. **标准库 (stdlib)** → 目标索引: `stdlib.md`

   覆盖的主要模块包括（节选）：

   - `std.core`（函数、类型别名、内置类型、接口、类、枚举、结构体、异常类）
   - `std.argopt`（函数、类、枚举、结构体、异常类）
   - `std.ast`（函数、接口、类、枚举、结构体、异常类）
   - `std.binary`（接口）
   - `std.collection`（函数、接口、类、异常类）
   - `std.collection.concurrent`（类型别名、接口、类）
   - `std.console`（类）
   - `std.convert`（接口）
   - `std.crypto.cipher`（接口）
   - `std.crypto.digest`（函数、接口）
   - `std.database.sql`（接口、类、枚举、异常类）
   - `std.deriving`（宏）
   - `std.env`（函数、类、异常类）
   - `std.fs`（函数、类、枚举、结构体、异常类）
   - `std.io`（函数、接口、类、枚举、异常类）
   - `std.math`（接口、函数、枚举）
   - `std.math.numeric`（函数、枚举、结构体）
   - `std.net`（接口、类、枚举、结构体、异常类）
   - `std.objectpool`（类）
   - `std.overflow`（接口、异常类）
   - `std.posix`（常量&变量、函数）
   - `std.process`（函数、类、枚举、异常类）
   - `std.random`（类）
   - `std.ref`（类、枚举）
   - `std.reflect`（函数、类型别名、类、枚举、异常类）
   - `std.regex`（类、枚举、结构体、异常类）
   - `std.runtime`（函数、结构体）
   - `std.sort`（函数、接口）
   - `std.sync`（常量&变量、接口、类、枚举、结构体、异常类）
   - `std.time`（类、枚举、结构体、异常类）
   - `std.unicode`（接口、枚举）
   - `std.unittest` 系列（包括 `mock`、`mockmacro`、`testmacro`、`common`、`diff`、`prop_test` 等）

3. **扩展库 (stdx)** → 目标索引: `stdx.md`

   覆盖的主要模块包括（节选）：

   - `stdx.aspectCJ`（类，示例教程：AOP 开发示例）
   - `stdx.compress.zlib`（类、枚举、异常类，示例教程：Deflate/Gzip 数据的压缩和解压）
   - `stdx.crypto.crypto`（类、结构体、异常类，示例教程：SecureRandom/SM4 使用）
   - `stdx.crypto.digest`（类、结构体、异常类，示例教程：digest 使用）
   - `stdx.crypto.keys`（类、枚举、结构体，示例教程：keys 使用）
   - `stdx.crypto.x509`（类型别名、接口、类、枚举、结构体、异常类，示例教程：x509 使用）
   - `stdx.encoding.base64`（函数，示例教程：Byte 数组和 Base64 互转）
   - `stdx.encoding.hex`（函数，示例教程：Byte 数组和 Hex 互转）
   - `stdx.encoding.json`（接口、类、枚举、异常类，示例教程：JsonArray 使用示例 / JsonValue 与 String 互转 / JsonValue 与 DataModel 的转换）
   - `stdx.encoding.json.stream`（接口、类、枚举、结构体，示例教程：使用 Json Stream 进行反序列化/序列化、WriteConfig 使用示例）
   - `stdx.encoding.url`（类、异常类，示例教程：Form 构造与 URL 解析）
   - `stdx.fuzz.fuzz`（常量&变量、类、异常类，示例教程：fuzz 使用与覆盖率处理等）
   - `stdx.log` / `stdx.logger`（类型别名、函数、接口、类、结构体、异常类，示例教程：日志打印示例）
   - `stdx.net.http`（函数、接口、类、枚举、结构体、异常类，示例教程：client/cookie/log/server/webSocket/h1_gzip 等）
   - `stdx.net.tls`（类、枚举、结构体、异常类，示例教程：客户端/服务端示例、证书热更新等）
   - `stdx.serialization.serialization`（函数、接口、类、异常类，示例教程：class/HashSet/HashMap 序列化）
   - `stdx.unittest.data`（函数、类）

4. **编译构建与命令行工具** → 目标索引: `tools.md`

   覆盖的内容主要包括：

   - 项目管理工具
   - 调试工具
   - 格式化工具
   - 静态检查工具
   - 覆盖率统计工具
   - 语言服务器工具
   - CHIR 反序列化工具
   - 异常堆栈信息还原工具
   - 性能分析工具

在任何情况下，你都**不得**臆测文档路径，必须按照下面的分步流程通过索引文件查找到真实文档路径。

## L3：官方文档全量检索兜底流程

### 目的

在仓颉通用基础检索与 L1 的 RAG 检索都没查到有用的知识情况下，通过读取本地索引文件定位目标 API 文档，随后读取完整文档以获取官方标准实现和上下文，用官方文档来兜底，**严禁凭空想象仓颉代码**。

### 核心原则

根据分析出的核心技术关键词，首先锁定合适的索引文件，再从索引中提取真实文档路径，最后阅读全文获取官方实现细节。整个过程必须依赖索引与文档内容本身，不能凭经验猜测路径或 API。

### 核心检索逻辑说明

**必须严格遵守此推理顺序：**

1. 提取前面阶段未检索到的“核心技术关键词”；
2. 扫描上方的**分类大纲目录**，寻找与关键词最相关的“知识点/模块”（例如：关键词有 HTTPS，对应找到 `stdx.net.http` 模块）；
3. 确定该知识点属于哪一个具体的“目标索引文件”（例如：属于 `hm-docs/index/stdx.md`）；
4. 使用 `Read` 工具全文读取这个索引文件；
5. 在索引文件中，利用刚刚确定的“知识点/模块”定位，找出具体文档的相对路径（例如：`libs_stdx/net/http/http_package_overview.md`）；
6. 根据索引来源拼接为完整路径，并再次使用 `Read` 工具读取目标文档，学习其中的标准写法与注意事项。

### 步骤 1：提取核心技术关键词

在开始 L3 检索前，你应从当前上下文中提炼出 **最关键的 1~2 个技术关键词**，例如：

- API 或模块名：`std.fs`, `stdx.net.http`, `JsonArray`, `WebSocket`；
- 概念类关键词：`异常处理`, `并发`, `反射`, `宏`；
- 工具与构建相关：`cjc`, `cjpm`, `cjcov`, `cjfmt`, `cjlint`, `cjprof`, `cjdb` 等。

> 尽量避免使用含糊的自然语言句子，例如 “怎么写 http server”，而是提炼出 “`stdx.net.http` + server” 这样的组合。

### 步骤 2：锁定目标索引文件（Determine Target Index）

根据提取到的关键词，将其映射到 4 个索引中的其中一个：

- 对应 **语言基础特性与语法** 的关键词（如“泛型、枚举、模式匹配、宏、I/O、并发”等）：
  - 使用索引：`skills/utils/scripts/hm-docs/index/syntax.md`
- 对应 **标准库 stdlib** 的关键词（如 `std.fs`, `std.io`, `std.net`, `std.regex` 等）：
  - 使用索引：`skills/utils/scripts/hm-docs/index/stdlib.md`
- 对应 **扩展库 stdx** 的关键词（如 `stdx.net.http`, `stdx.encoding.json`, `stdx.log` 等）：
  - 使用索引：`skills/utils/scripts/hm-docs/index/stdx.md`
- 对应 **工具链 & 构建 & 调试 & 静态检查** 的关键词（如 `cjfmt`, `cjlint`, `cjcov`, `性能分析` 等）：
  - 使用索引：`skills/utils/scripts/hm-docs/index/tools.md`

**操作要求：**

1. 必须使用 `Read` 工具 **全文**读取被选中的索引文件；
2. 在索引文件中，找到与你的关键词最匹配的“知识点/模块”条目；
3. 从该条目的 Markdown 链接中提取出真实的 **相对路径片段**（即 `(... )` 括号中的路径）。

### 步骤 3：拼接真实文档路径并读取目标文档

根据索引来源不同，将刚刚提取到的相对路径拼接为**实际文件路径**：

- `syntax.md` 索引 → 拼接到：
  - `skills/utils/scripts/hm-docs/syntax/{相对路径}`
- `stdlib.md` 索引 → 拼接到：
  - `skills/utils/scripts/hm-docs/stdlib/{相对路径}`
- `stdx.md` 索引 → 拼接到：
  - `skills/utils/scripts/hm-docs/stdx/{相对路径}`
- `tools.md` 索引 → 拼接到：
  - `skills/utils/scripts/hm-docs/tools/{相对路径}`

**重要限制（防 payload 过大）：**

1. 每次调用 `Read` 工具，**最多只能读取 1~2 个最核心的文档文件**；
2. 尽量**优先**选择名称包含：
   - `_samples.md`（示例代码）
   - `_overview.md`（概览与基本用法）
3. 尽量避免直接读取：
   - 名称包含 `_classes.md`
   - `_funcs.md`
   - `_interfaces.md`
   
   这类文件通常体积巨大，只在极端情况下作为最后选择。

读取完目标文档后，你应当：

- 提取其中的 `import` 声明；
- 标出关键 API 的完整签名（函数名、参数、返回值）；
- 关注官方给出的示例代码及注意事项；
- **严格以文档为准**设计/修改仓颉代码。

### 步骤 4：基于官方文档执行开发与排错

在完成文档阅读后，你需要：

- 将当前工程中的代码实现，对照官方示例逐条检查：
  - 包导入是否正确；
  - 类型/泛型参数是否匹配；
  - 错误处理是否符合推荐模式（异常 vs `Option`）；
  - 网络/IO/并发等敏感模块是否按照推荐模式使用；
- 在引用 API 时，**不得**擅自更改签名或臆测重载版本；
- 如遇到版本差异（文档示例与实际 SDK 不完全一致）：
  - 应以当前 SDK 中的实际报错信息为线索，再次回到 L3 文档中查找“变更说明/弃用说明”等章节。

### 自我检查与回溯（Self-Reflection）

每次使用本 Skill 进行 L3 检索后，你应回答以下问题：

1. 当前修改/实现的代码，是否可以在官方文档中找到**直接或高度相似**的示例？
2. 是否存在任何一处“凭感觉写的语法”或“凭记忆写的 API 名称”？如果有，应重新回到文档确认。
3. 是否遗漏了文档中强调的“注意事项/警告/边界条件处理”？

只有在上述问题都得到肯定回答后，才可以认为本次 L3 检索任务完成。

## 与其它 Skills 的协作关系

- 与 `cangjie-vec-retriever-guide`：
  - 当前 Skill 用于 **L3 官方文档兜底层**；
  - 如果 L1 语义检索已经给出足够清晰且与官方文档一致的结果，可优先使用 L1 输出；
  - 当 L1 返回 `NO_RAG_RESULT` 或结果质量不足时，必须转入本 Skill。
- 与 `cangjie-kernel`：
  - `cangjie-kernel` 提供“目录化”的仓颉基础知识与常用场景；
  - 当 L1/L3 得到的结论与 `cangjie-kernel` 存在明显冲突时，应以 **官方文档（本 Skill）为最终裁决依据**，并可将新发现记录到 `cangjie-evolution/Evolution.md` 中，优化未来体验。

