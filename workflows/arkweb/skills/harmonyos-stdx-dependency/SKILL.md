---
name: harmonyos-stdx-dependency
description: 在鸿蒙应用（Cangjie）开发中，当需要使用 stdx 拓展库（如 crypto、encoding、net、log、actors
  等），或在构建/链接阶段出现 stdx 相关错误时，使用此 Skill 获取/解压 stdx 包，并指导在 entry/cjpm.toml 中正确配置
  bin-dependencies.path-option。
argument-hint: 描述你的 stdx 使用场景或报错信息，例如 "鸿蒙 stdx crypto 配置"、"actors 无法链接"、"x86_64-ohos stdx 找不到"
disable-model-invocation: false
descriptionZH: 在鸿蒙应用（Cangjie）开发中，当需要使用 stdx 拓展库（如 crypto、encoding、net、log、actors
  等），或在构建/链接阶段出现 stdx 相关错误时，使用此 Skill 获取/解压 stdx 包，并指导在 entry/cjpm.toml 中正确配置
  bin-dependencies.path-option。
tags:
  - 鸿蒙
  - stdx
  - 依赖配置
  - HarmonyOS
  - 仓颉
---

## 🤝 与鸿蒙开发 Skills 的协作

### 协作概述
- **本技能职责**: 专门处理 Cangjie stdx 拓展库的获取、解压路径规划与 cjpm.toml 依赖配置（面向鸿蒙应用工程）
- **调用方技能职责**: 负责鸿蒙应用整体开发流程（UI、API 查询、构建与排错），如 `harmonyos-build`、`harmonyos-doc-search-guide` 等
- **协作原因**: 当鸿蒙应用开发过程中需要使用 stdx 模块或遇到 stdx 依赖问题时，由主开发技能调用本技能处理依赖配置，确保职责分离和专业化处理

### 被调用时机
本 Skill 主要在以下场景被鸿蒙相关 Skills 调用（如 `harmonyos-build` / `harmonyos-doc-search-guide` / 需求分析流程后）：

1. **功能需求触发**
   - **触发条件**: 编码过程中发现需要某个 stdx 模块能力
   - **典型场景**: 
     - 需要使用 `crypto`（加解密、消息摘要、证书等）
     - 需要使用 `encoding`（base64/hex/json/url 编解码）
     - 需要使用 `net`（HTTP/TLS 网络能力）
     - 需要使用 `log` / `logger`（日志）
     - 需要使用 `serialization` / `unittest`（序列化 + 测试数据）
     - 需要使用 `actors` / `effect`（并发编程模型、非局部控制）
   - **接收信息**: 需要使用的 stdx 模块名称列表、构建平台信息

2. **构建错误触发**
   - **触发条件**: 构建/链接阶段出现 stdx 相关错误
   - **典型错误**: 
     - `undefined reference to stdx::...`
     - 找不到 stdx 动态库/头文件
     - 提示与 stdx 目录或 `bin-dependencies.path-option` 相关的路径问题
   - **接收信息**: 完整的构建错误信息、构建平台信息

3. **用户直接调用**
   - **触发条件**: 用户明确提出「我想在鸿蒙工程中配置/安装 stdx」这类需求
   - **接收信息**: 用户的使用场景描述或报错信息

### 处理流程
当被调用时，本 Skill 按以下流程处理：

1. **接收调用信息**: 
   - 解析调用方传递的信息（模块需求或错误信息）
   - 确定目标平台（x86_64 或 aarch64）

2. **检查当前状态**: 
   - 检查鸿蒙应用工程根目录和 `entry/cjpm.toml` 是否存在
   - 检查是否已配置 stdx 路径
   - 检查 stdx 包是否已解压

3. **执行配置操作**: 
   - 自动解压 stdx 包到 `<项目根>/cjnative/stdx` 目录
   - 自动修改 `entry/cjpm.toml` 中的 `bin-dependencies.path-option`
   - 向用户展示操作过程和最终配置

4. **返回结果**: 
   - 告知调用方配置完成
   - 提供 stdx 模块能力简介（如需要）
   - 说明后续如何在鸿蒙工程中使用已配置的 stdx 模块

### 职责边界
- **本技能负责**: 
  - ✅ stdx 能力简介和模块说明
  - ✅ stdx 本地二进制/头文件的获取和解压
  - ✅ stdx 解压路径规划（固定为 `<项目根>/cjnative/stdx`）
  - ✅ `cjpm.toml` 中 `bin-dependencies.path-option` 的配置
  - ✅ stdx 相关错误的诊断和路径问题排查
  
- **调用方技能负责**:
  - ✅ UI 开发和业务逻辑实现
  - ✅ API 查询和语法问题解答
  - ✅ 整体构建流程执行
  - ✅ 非 stdx 相关的构建错误处理

- **不重叠原则**: 
  - ❌ 本技能不负责 UI / 业务逻辑 / 整体构建流程
  - ❌ 本技能不主动触发构建，只负责配置
  - ✅ 专注于 stdx 依赖配置，确保调用方可以专注于开发流程
  - ✅ 与其它鸿蒙开发 Skills 解耦，只在 stdx 相关场景时被触发

## 📦 本 Skill 内置资源位置 & 自动解压行为

### 在 Common 仓库中的位置

- 技能目录：`skills/harmonyos-stdx-dependency/`
- 内置压缩包：`cangjie-stdx-ohos-x86_64-1.1.0-beta.10.1.zip`

> 当你将本 Skill 拷贝到具体鸿蒙工程中使用时，应将整个目录复制到项目的 `skills/harmonyos-stdx-dependency/` 下；下面的说明默认技能运行目录为 `skills/harmonyos-stdx-dependency/`。

### 在鸿蒙工程中的预期目录

- 技能目录：`skills/harmonyos-stdx-dependency/`
- 压缩包路径：`skills/harmonyos-stdx-dependency/cangjie-stdx-ohos-x86_64-1.1.0-beta.10.1.zip`

> 原则：**由 Skill 自动解压并写入 cjpm.toml，尽量避免让用户手工改路径**。

### 🛠️ 自动解压与目标目录（固定策略）

当本 Skill 被调用且检测到还未配置 stdx 依赖时，**Skill 必须按以下顺序自动执行，且不再询问用户**：

1. 确定鸿蒙应用工程根目录（例如：`C:/czc/MyApplication12`）
2. 在工程中定位 `entry/cjpm.toml`
3. 在工程根目录下创建/确认固定的 stdx 目标目录：

```text
<项目根>/cjnative/stdx
```

4. 从本 Skill 目录中的 `cangjie-stdx-ohos-x86_64-1.1.0-beta.10.1.zip` **自动解压到 `<项目根>/cjnative/stdx` 目录**：
   - 如果 `cjnative/` 或 `cjnative/stdx/` 目录不存在，先自动创建
   - 解压过程需要在回答中向用户**明确展示：目标路径、是否新建目录、解压完成信息**
5. 解压完成后，读取 `<项目根>/cjnative/stdx` 的**绝对路径**，并在 `entry/cjpm.toml` 的对应 `bin-dependencies.path-option` 中直接加入这个绝对路径（例如：`"C:/czc/MyApplication12/cjnative/stdx"`）

> 要求：整个「创建目录 → 解压 → 修改 cjpm.toml」过程，必须在回答里逐步告知用户你做了哪些具体操作，以及最终写入的绝对路径是什么。

## ⚙️ cjpm.toml 关键配置位置

在鸿蒙 Cangjie 应用中，stdx 依赖通常通过 `entry/cjpm.toml` 的 `bin-dependencies` 配置。

### 示例文件（用户提供的实际片段）

文件：`entry/cjpm.toml`

```toml
[target.x86_64-linux-ohos.bin-dependencies]
path-option = [
  "${X86_64_OHOS_LIBS}",
  "${X86_64_OHOS_MACRO_LIBS}",
  "${X86_64_OHOS_KIT_LIBS}",
  "C:/czc/linux_ohos_x86_64_cjnative/dynamic/stdx"
]
```

### Skill 在回答时的步骤

当用户问「stdx 怎么配置 / 链接不到 / undefined reference」时，按以下顺序引导：

1. **定位配置文件**
   - 提示用户打开：`entry/cjpm.toml`
   - 重点关注：
     - `[target.aarch64-linux-ohos.bin-dependencies]`
     - `[target.x86_64-linux-ohos.bin-dependencies]`
2. **确认 stdx 解压路径**
   - 询问用户 stdx 解压到了哪里（例如：`C:/czc/linux_ohos_x86_64_cjnative/dynamic/stdx`）
   - 如果用户尚未解压，提示先解压本 Skill 目录下的 zip 包：
     - `skills/harmonyos-stdx-dependency/cangjie-stdx-ohos-x86_64-1.1.0-beta.10.1.zip`
3. **给出路径配置示例**
   - 如果用户走「集中目录方案」：
     - 直接给出类似：`".../dynamic/stdx"` 这种绝对路径写法
   - 如果用户走「项目内相对目录方案」：
     - 建议路径形如：`"<项目根>/cjnative/stdx"`，并在 `cjpm.toml` 中写相对路径
4. **平台区分**
   - 如果错误出现在 **真机 / 模拟器 (aarch64-linux-ohos)**：
     - 需要在 `[target.aarch64-linux-ohos.bin-dependencies]` 中追加对应的 stdx 路径
   - 如果错误出现在 **PC x86_64-linux-ohos 运行**：
     - 在 `[target.x86_64-linux-ohos.bin-dependencies]` 中追加 stdx 路径

## 📚 stdx 能力速查（用于回答时简要介绍）

当用户问「stdx 是什么 / 某个模块大概干嘛」时，可以用本节的简要说明，**不要胡编 API 细节**，API 细节仍需查官方文档。

- **整体定义**  
  拓展库 stdx 是仓颉语言提供的官方扩展模块集合（非核心 stdlib，但由官方维护），主要提供以下能力：

- **模块概览**：
  - `aspectCJ`: 面向切面编程相关注解
  - `compress`: 压缩/解压缩能力
  - `crypto`: 安全能力（对称/非对称加解密、签名、消息摘要、证书处理等）
  - `encoding`: 基础编解码能力（base64/hex/json/url 等）
  - `fuzz`: 模糊测试框架
  - `log`: 统一日志 API
  - `logger`: 文本/JSON 格式日志打印
  - `net`: 网络通信与 TLS 安全传输
  - `serialization`: 序列化/反序列化框架
  - `unittest`: 在单测中使用序列化输入数据的支持
  - `actors`: 并发编程模型（Actor 模型）
  - `effect`: 非局部控制操作（Effect 系统）

> 回答准则：**只概括能力，不虚构方法名/类型签名**。如需 API 级别文档，请提醒用户查官方 stdx 文档或 hm-docs 中的 `./hm-docs/stdx/libs_stdx/`。

## 🧭 回答策略总结（鸿蒙场景）

当本 Skill 被调用时，优先遵循下面的决策树：

1. **用户是否已经说明平台？**
   - aarch64 / x86_64 / Windows 交叉编译？  
   - 若未说明，先让用户补充运行/构建的平台。
2. **检查 cjpm.toml 是否已配置 stdx 路径**
   - 若无：指导如何追加 `path-option` 项
   - 若有：检查路径是否指向实际解压目录
3. **检查 stdx 物理路径是否存在**
   - 若用户未解压：指导其从 `skills/harmonyos-stdx-dependency/cangjie-stdx-ohos-x86_64-1.1.0-beta.10.1.zip` 解压
4. **仍然报错时**
   - 让用户贴出完整构建/链接错误信息
   - 根据错误信息判断是「路径问题 / 版本不匹配 / 缺少符号」等，再给出下一步建议

本 Skill 不会主动触发构建，只负责让用户在 **正确位置配置正确的 stdx 路径**，并理解各个 stdx 模块大致提供的能力。

