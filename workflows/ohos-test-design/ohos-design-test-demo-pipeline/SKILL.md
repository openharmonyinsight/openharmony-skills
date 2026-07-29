---
name: ohos-design-test-demo-pipeline
description: Use when 需要把测试点设计转化为可编译的 HarmonyOS NEXT Demo 应用——Demo UI 设计、ArkUI 代码编写、编译验证与修复三阶段。当用户需要生成测试 Demo 应用、将测试点映射为可交互 ArkUI 界面、生成真机可部署的测试验证 Demo，或提及 demo app / ArkUI code 时使用。Do NOT use without an existing test-point design（先跑 ohos-design-test-coordinator），或当 HarmonyOS SDK/hvigor 不可用且无需 Demo 编译验证时。
---

# Demo 流水线编排器

## 平台工具映射（三平台）

本 skill 同样发布到 Claude / Codex / OpenCode。文中 `AskUserQuestion`、`spawn Agent`、`Task`、`Read`、`Edit`、`Glob` 为 **Claude 工具记法别名**，运行时按当前平台映射到对应工具；无对应工具时降级，不得因别名不存在而无法启动或忽略强制约束。完整映射表见 `ohos-design-test-coordinator/SKILL.md`「平台工具映射与降级」。

- **独立调用**：用户确认用本平台提问工具；子阶段执行若无子Agent能力则本 skill 自身顺序执行，`parallel_limit=1`。
- **协调器调用**：**禁止**自行发起用户确认，将需确认项写入返回摘要由协调器统一发起。
- **降级**：能力探测在启动时进行；降级状态（`parallel_limit=1`、`mcp=none` 等）写入返回摘要，不得静默降质。

## 执行约束

- 本文件是编排器，仅定义流程控制和用户交互逻辑
- 各阶段的详细指令（执行逻辑、输出格式、自检清单、编码规范）存储在 `phases/` 目录下的独立文件中
- 每个阶段通过 Agent 子代理执行，实现上下文隔离
- 阶段间通过文件路径传递数据，Agent 通过 Read 工具按需读取上游输出文件
- 全程不生成 JSON 数据块，仅使用 Markdown 表格

**路径约定：**
- `{技能目录}` 指本 skill 所在的根目录
- **共享资源目录**：`reference/`（即 `{技能目录}/reference/`）
  - `reference/api-reference/` — **外部数据依赖，不随仓发布**（见 `reference/api-reference/README.md`、`install.sh`）；各领域 API 参考目录（ArkWeb/、ArkUI/、Ability/ 等）
  - `reference/domains.yaml` — 领域配置文件
- **API 参考搜索（完整模式）**：当 `reference/api-reference/{选定领域}/index.json` 已安装时，通过其索引定位 API（读取 index.json 的 `modules[].files[]` 匹配 `name` 字段获取对应文件名），再 Read 该文件获取详情。**禁止 Grep/Glob 搜索目录下所有 .json 文件**
- **API 参考降级模式**：当 `index.json` 未安装或未通过 `install.sh` 完整性校验（schema + 引用文件存在且为合法 JSON）时，跳过 index 查找，所有 API 标注 `⚠️ 无 API 参考`，代码生成采用最佳努力 + ⚠️ 标记，由门禁决定是否继续。此时 Demo Pipeline **不宣称可独立运行**（完整模式需先安装并通过完整性校验）。

## NEVER

- NEVER 在 ArkUI 声明式语法中使用命令式 DOM 操作——ArkUI 无 `document.getElementById`，必须用 `@State`/`@Link` 响应式绑定
- NEVER 生成不包含 `id()` 修饰符的可交互控件——无 `id()` 的控件无法被测试框架定位
- NEVER 硬编码字符串到代码中——必须使用 `$r('app.string.xxx')` 资源引用
- NEVER 编译修复超过 5 轮后继续修改业务代码——超过 5 轮说明设计阶段 API 选型有误，应回退阶段1重新评估
- NEVER 在编译修复时修改 `reference/template/` 下的工程模板文件——模板文件是固定的构建配置，问题出在生成的页面代码
- NEVER 为单个测试点生成超过 3 个页面——测试点粒度过细会导致 Demo 碎片化，应合并到同一页面不同操作模式
- 完整模式下 NEVER 凭记忆编写 API 调用代码——必须通过 index.json 索引定位到对应 JSON 文件，获取准确的 importPath、参数签名和示例。降级模式（index.json 未安装）下：API 标注 `⚠️ 无 API 参考`，最佳努力生成，由门禁决定，不宣称可独立运行
- 完整模式下 NEVER 使用 Grep/Glob 搜索 api-reference 目录下所有 .json 文件来查找 API——必须先 Read index.json 索引定位文件，再 Read 目标文件。降级模式下不进行 index 查找（数据本就不存在）
- NEVER 跳过阶段3编译验证——未编译的代码无法保证 Demo 可运行

---

## 0. 启动

### 调用模式判断

启动时检查是否存在运行时上下文（输出目录、输入文件路径）：

- **协调器调用**：运行时上下文由协调器 Agent prompt 传入，直接进入阶段 1
- **独立调用**：无运行时上下文，执行下方启动流程

### 独立调用启动流程

使用 AskUserQuestion 询问用户：

| 问题 | 选项 |
|------|------|
| 输入目录 | 当前目录 / 指定路径 |
| 输出目录 | 当前目录 / 指定路径 |

启动动作：
1. 扫描输入目录，识别输入文件：
   - 测试点设计：`demo_test_points.md`（必需，仅包含非XTS执行方式的测试点；协调器调用时由协调器生成）或 `test_point_design.md`（独立调用时使用）
   - 需求分析：`requirement_analysis.md`（可选，补充上下文）
   - Demo 设计：`demo_design.md`（可选，跳过阶段 1 直接进入阶段 2）
2. 用 ls 验证输入目录可读、输出目录可写（不存在则创建）
3. 确定起始阶段：
   - 存在 demo_design.md → 询问用户从阶段 2（代码生成）开始
   - 不存在 demo_design.md → 从阶段 1（UI 设计）开始
4. 显示扫描结果及起始阶段

---

## 阶段执行模式

每个阶段按以下统一模式执行：

### 标准执行流程

1. Read `{技能目录}/phases/phase{N}_xxx.md` 获取阶段完整指令
2. 构造 Agent prompt：
   - 指令部分：phase 文件的完整内容
   - 运行时上下文：输入文件路径、输出目录等
   - 通用约束和返回格式（见下方模板）
3. 使用 Agent 工具 foreground 模式执行
4. Agent 返回摘要后，展示给用户
5. **确认策略**：
   - **协调器调用**：所有子阶段自动执行，不暂停确认；仅编译验证阶段检测到 SDK 缺失 API 时暂停等待用户处理
   - **独立调用**：阶段1、阶段2、阶段3 正常编译通过后均不确认，自动执行下一阶段；仅编译验证阶段检测到 SDK 缺失 API 时暂停等待用户处理
6. 如需增量优化（仅独立调用时用户主动要求）→ 重新 spawn Agent 执行增量修改

### Agent prompt 通用模板

```
你是 Demo 流水线系统的阶段执行器。

{phase 文件的完整内容}

## 运行时上下文
{阶段特有的输入文件路径和参数}

## 通用约束
- 全程不生成 JSON 数据块，仅使用 Markdown 表格
- 输出文件写入磁盘后返回摘要
- 摘要必须包含具体数字，不含占位符

## 返回格式
完成后请返回以下摘要信息：
{阶段特有的摘要字段列表}
```

### 增量优化 Agent prompt 模板

```
你是 Demo 流水线系统的阶段增量优化执行器。

{phase 文件的完整内容}

## 任务
用户对 {输出文件名} 提出以下优化建议：
{用户的具体建议}

请读取 {输出文件路径}，根据用户建议进行增量修改。
修改后重新执行该阶段自检清单，然后返回变更摘要（修改了哪些内容）。
```

---

## 1. 阶段 1：Demo UI 设计

- **指令文件**：`{技能目录}/phases/phase1_ui_design.md`
- **输入**：`{输出目录}/test_point_design.md`（仅包含非XTS执行方式的测试点） + `{输出目录}/requirement_analysis.md`（可选）
- **输出**：`{输出目录}/demo_design.md`
- **运行时上下文**：
  ```
  - 测试点设计文件：{输出目录}/demo_test_points.md（仅包含非XTS执行方式的测试点）
  - 需求分析文件：{输出目录}/requirement_analysis.md（可选）
  - 领域配置文件：{技能目录}/reference/domains.yaml
  - API 参考目录：{技能目录}/reference/api-reference/
  - 输出目录：{输出目录}

  **API 查找提醒**：必须通过 index.json 索引定位 API，禁止 Grep/Glob 搜索 api-reference 目录，详见 phase1 指令步骤 5a-5d
  ```
- **返回摘要**：Demo 页面数、UI 控件数、操作模式数、测试点覆盖率（X/X XX%）
- **自动执行**（不暂停确认）

### Demo 设计质量评估

阶段1 Agent 返回后、进入阶段2前，评估 Demo 设计质量：

| 评估维度 | 达标标准 | 不达标时 |
|---------|---------|---------|
| 测试点覆盖 | 每个非XTS测试点至少关联一个UI控件或操作 | 标记未覆盖测试点，提示 Agent 补充 |
| 页面复杂度 | 单页面 ≤ 15个控件 | 超出时建议拆分为多页面或分步操作 |
| 操作可达性 | 每个操作模式可从首页导航到达 ≤ 3步 | 提示简化导航层级 |
| API 完整性 | 设计中引用的每个 API 都在 api-reference 中找到对应条目 | 未找到的 API 标记为 ⚠️ 无参考，代码生成时需格外注意 |

---

## 2. 阶段 2：Demo 代码生成

- **指令文件**：`{技能目录}/phases/phase2_code_generation.md`
- **输入**：`{输出目录}/demo_design.md`
- **输出**：`{输出目录}/TestDemo/` + `{输出目录}/demo_code_manifest.md`（`rag_demo_experience.json` 为编排器前置写入的中间缓存，非交付物，流水线结束时清理）
- **返回摘要**：源文件数、控件 ID 数、权限声明项数、MCP知识库查询结果（控件专项查询数 + 通用知识条目数；MCP不可用时返回"未执行（环境无MCP）"）
- **自动执行**（不暂停确认）

### 编排器前置步骤：MCP 知识库查询（编排器直接执行，不委托子 Agent）

**目的**：将 MCP 查询从子 Agent 任务中剥离，由编排器直接执行并写入文件，确保查询步骤可靠执行，避免子 Agent 上下文丢失导致跳过。

**执行时机**：阶段1完成、阶段2 Agent 启动前。

**执行步骤**：

1. **探针检测**：调用 `search_knowledge({ query: "ArkUI", domain: "common", category: "demo_experience", top_k: 1 })`
   - 调用成功 → MCP 可用，执行步骤2-3
   - 工具不存在或调用失败 → MCP 不可用，在 `{输出目录}/rag_demo_experience.json` 写入 `{"status": "MCP不可用，已跳过知识库查询"}`，跳到步骤4

2. **第一轮：控件驱动专项查询**（优先级最高）
   - 读取 `{输出目录}/demo_design.md`，从各页面「控件清单」的「控件类型」列提取所有不重复的 ArkUI 组件类型
   - 对每个组件类型，调用 `search_knowledge` 查询用法和代码示例：
     | 控件类型 | 查询关键字 |
     |---------|-----------|
     | Select | "ArkUI Select 组件 用法 示例" |
     | Button | "ArkUI Button 组件 用法 示例" |
     | TextInput | "ArkUI TextInput 组件 用法 示例" |
     | Toggle | "ArkUI Toggle 组件 用法 示例" |
     | Text/Result/Status | "ArkUI Text 组件 样式 装饰" |
     | List/Log | "ArkUI Scroll List 组件 滚动列表" |
     | 其他 | "ArkUI {控件类型} 组件" |
   - 参数：`domain: "common"`, `category: "demo_experience"`, `top_k: 10`

3. **第二轮：通用开发知识查询**
   - 按需查询以下类别（每个类别一次查询）：
     - "装饰器用法 状态管理 页面跳转"
     - "ArkTS 命名规范 工程目录 资源规范"
   - 参数：`domain: "common"`, `category: "demo_experience"`

4. **写入结果文件**：将所有查询结果（第一轮+第二轮）按以下结构写入 `{输出目录}/rag_demo_experience.json`，使用 Glob 验证文件存在

   **写入格式（强制）**：必须保留每条结果的 `content_preview` 字段（含代码示例），供阶段2 Agent 直接参考。禁止仅写入元数据索引。

   ```json
   {
     "status": "MCP可用",
     "round1_component_queries": [
       {
         "component": "Select",
         "query": "ArkUI Select 组件 用法 示例",
         "results": [
           {
             "rank": 1,
             "doc_id": "test_exp_common_demo_experience_xxx",
             "title": "ArkUI基础组件精简参考",
             "relevance_score": 0.664,
             "content_preview": "（完整保留 search_knowledge 返回的 content_preview 内容，含代码示例）",
             "content_length": 762,
             "content_full_length": 16352,
             "content_truncated": true,
             "metadata": { "entry_code": "KP-DEMO-002" }
           }
         ]
       }
     ],
     "round2_general_queries": [
       {
         "query": "装饰器用法 状态管理 页面跳转",
         "results": [
           {
             "rank": 1,
             "doc_id": "...",
             "title": "...",
             "relevance_score": 0.80,
             "content_preview": "（完整保留）",
             "content_length": 105,
             "content_full_length": 6290,
             "content_truncated": true,
             "metadata": { "entry_code": "KP-DEMO-004" }
           }
         ]
       }
     ],
     "summary": {
       "total_queries_executed": 8,
       "unique_documents_retrieved": 5,
       "mcp_available": true
     }
   }
   ```

   **关键约束**：
   - `content_preview` 字段必须完整保留 search_knowledge 返回的原始内容，不得截断或省略
   - 每条结果的 `metadata.entry_code` 必须保留（如 KP-DEMO-002），用于阶段2 Agent 按 entry_code 去重和引用
   - `content_truncated` 为 `true` 时表示该条目有完整文档，阶段2 Agent 可通过 `get_document(doc_id)` 获取更多内容

5. **构造阶段2 Agent 运行时上下文**：
   ```
   - Demo 设计文件：{输出目录}/demo_design.md
   - 工程模板目录：{技能目录}/reference/template/
   - API 参考目录：{技能目录}/reference/api-reference/
   - MCP 查询结果文件：{输出目录}/rag_demo_experience.json（编排器已预先查询并写入）
   - 输出目录：{输出目录}
   - MCP 可用状态：是/否
   ```

---

## 3. 阶段 3：编译验证与修复

- **指令文件**：`{技能目录}/phases/phase3_compile_verify.md`
- **输入**：`{输出目录}/TestDemo/` + `{输出目录}/demo_code_manifest.md` + `{输出目录}/demo_design.md`
- **输出**：`{输出目录}/demo_code_manifest.md`（更新）
- **运行时上下文**：
  ```
  - Demo 工程目录：{输出目录}/TestDemo/
  - Manifest 文件：{输出目录}/demo_code_manifest.md
  - Demo 设计文件：{输出目录}/demo_design.md（用于提取基准 API 清单）
  - ArkTS 修复参考：{技能目录}/reference/arkts-more-cases.md
  - 输出目录：{输出目录}
  ```
- **返回摘要**：编译状态（BUILD SUCCESSFUL/FAILED/SDK版本过低/HVIGORW_NOT_FOUND）、修复次数、缺失 API 清单（如有）、环境缺失详情（如有，仅 HVIGORW_NOT_FOUND 时）、环境缺失处理建议（如有）
- **自动执行**（正常编译通过不暂停确认）
- **hvigorw 未安装处理（按调用模式分支）**：检测到 hvigorw 命令不存在于系统 PATH 时，根据调用模式执行不同策略：
  - **独立调用**：使用 AskUserQuestion 询问用户：
    - 问题："未在系统 PATH 中找到 hvigorw 命令，请安装 HarmonyOS command-line-tools 并配置 PATH"
    - 选项1："我已安装，重新检查" → 重新执行环境检查
    - 选项2："终止阶段3" → 执行中间文件清理（见阶段4），返回摘要（编译状态：HVIGORW_NOT_FOUND），结束阶段3
  - **协调器调用**：**禁止使用 AskUserQuestion**。改为将缺失信息写入返回摘要：
    - 编译状态：`HVIGORW_NOT_FOUND`
    - 环境缺失详情：`未在系统 PATH 中找到 hvigorw 命令，需安装 HarmonyOS command-line-tools`
    - 环境缺失处理建议：`需协调器询问用户：安装 command-line-tools 后重试 或 终止`
    - 执行中间文件清理（见阶段4），返回摘要，结束阶段3
- **SDK 缺失处理（按调用模式分支）**：检测到 demo_design.md API 清单中的 API 在当前 SDK 不存在时，根据调用模式执行不同策略：
  - **独立调用**：使用 AskUserQuestion 询问用户：
    - 问题："以下 API 在当前 SDK 中未找到：{缺失 API 列表}，请选择处理方式："
    - 选项1："我已替换 SDK，重新编译" → 重新 spawn Agent 从步骤1开始执行阶段3
    - 选项2："跳过，继续后续流程" → 标注未验证，继续完成
  - **协调器调用**：**禁止使用 AskUserQuestion**。改为将缺失信息写入返回摘要：
    - 编译状态：`SDK版本过低`
    - 缺失 API 清单：列出所有缺失 API 的完整名称
    - SDK 缺失处理建议：`需协调器询问用户：替换 SDK 后重试 或 跳过继续`
    - 标注 Demo 编译验证为"未验证（SDK 缺失）"，执行中间文件清理（见阶段4），返回摘要，结束阶段3

---

## 4. 阶段 4：完成

`demo_code_manifest.md` 的完整输出格式（含文件清单、控件ID汇总、权限声明、API调用记录、自检结果、编译验证结果）定义在 `{技能目录}/phases/phase2_code_generation.md` 的执行步骤10中。

### 确认机制

**自动执行完成**：所有子阶段自动执行完毕后，显示摘要（页面数/源文件数/控件数/权限/编译状态），自动结束流水线返回最终摘要。
- **独立调用**：在编译验证阶段检测到 SDK 缺失 API 时暂停等待用户处理（替换 SDK 或跳过）。
- **协调器调用**：编译验证阶段检测到 SDK 缺失 API 时不暂停，将缺失 API 清单和处理建议写入返回摘要，由协调器负责向用户询问。

### 中间文件清理

流水线结束前（无论阶段4 正常完成还是阶段3 异常终止），编排器清理已消费的中间缓存：

- **删除** `{输出目录}/rag_demo_experience.json`（MCP 知识库查询缓存，阶段2 已消费，非交付物）
- **跨平台命令**（编排器直接执行，不委托子 Agent）：
  - **Windows（PowerShell）**：`Remove-Item -LiteralPath "{输出目录}/rag_demo_experience.json" -ErrorAction SilentlyContinue`
  - **Linux/macOS（Bash）**：`rm -f "{输出目录}/rag_demo_experience.json"`
- **错误处理**：文件不存在时静默跳过（MCP 不可用时编排器写入的状态文件同样清理）；删除失败仅记录警告，不阻塞流水线结束
- **保留文件**（交付物或上游输入，禁止删除）：`demo_test_points.md`、`requirement_analysis.md`、`demo_design.md`、`TestDemo/`、`demo_code_manifest.md`

### 流水线完成摘要

```
Demo 流水线执行完成：
- Demo 页面：X 个 | UI 控件：X 个 | 操作模式：X 种 | 测试点覆盖率：X/X (XX%)
- 源文件数：X 个 | 控件 ID 数：X 个 | 权限声明：X 项
- 编译验证：BUILD SUCCESSFUL（修复 X 次）/ BUILD FAILED (SDK 版本过低)（缺失 API：XXX, YYY）
- 输出文件：demo_design.md, TestDemo/, demo_code_manifest.md
```

## 错误处理

### 文件操作重试

- 文件读取失败：最多重试 3 次
- 文件写入失败：最多重试 3 次
- 单个页面代码生成失败：最多重试 2 次
- 重试间隔：1s → 2s → 4s（指数退避）

### 编译错误分型处理

| 错误类型 | 识别特征 | 处理策略 | 最大轮次 |
|---------|---------|---------|---------|
| 语法错误 | `SyntaxError`、`Expected`、类型不匹配 | 自动修复 ArkTS 语法 | 3轮 |
| API 调用错误 | `Cannot find name`、`Property does not exist` | 搜索 api-reference 修正 importPath 或参数 | 3轮 |
| SDK 版本缺失 | API 在 api-reference 中存在但 SDK 报错 | **独立调用**：暂停问用户（替换SDK或跳过）；**协调器调用**：写入返回摘要，由协调器询问用户 | 0轮 |
| 模板配置错误 | `hvigor`、`build-profile`、`oh-package` 相关 | **不修复模板文件**，检查生成代码是否覆盖了模板配置 | 1轮 |
| 资源引用错误 | `$r()` 找不到资源 | 自动补充 string.json / color.json 条目 | 2轮 |
