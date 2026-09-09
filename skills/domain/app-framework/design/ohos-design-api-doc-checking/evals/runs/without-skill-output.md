# Documentation Quality Review — Baseline (without skill)

Review date: 2026-09-08
Reviewer mode: general knowledge baseline (no skill/rule files loaded)

---

## Task api_doc_planted_errors

**文件**: `evals/inputs/js-apis-demo-taskmanager.md`（仅文档质量检查，不做 SDK 比对）

### 检查方面

- 文档结构与章节完整性（接口描述、系统能力、参数、返回值、错误码、示例）
- 术语与中英文规范（拼写、大小写、中英文混用）
- 示例代码正确性与完整性（语法、模板字符串、括号闭合）
- 内部一致性（版本标注、章节标签、锚点链接）
- 描述准确性与表述清晰度

### 问题清单

| 文件名 | 问题类型 | 问题行号 | 问题原因 | 建议修改方案 | 问题严重级别 |
| --- | --- | --- | --- | --- | --- |
| js-apis-demo-taskmanager.md | 返回值描述错误 | 26 | callback 异步接口的返回值写为 `AsyncCallback<number>`；callback 方式接口返回值应为 void/无，`AsyncCallback<number>` 是 callback 参数的类型而非返回值 | 将"**返回值**"改为"无"（或删除该行），返回值类型仅体现在 callback 参数说明中 | 高 |
| js-apis-demo-taskmanager.md | 示例代码错误（模板字符串） | 46 | `$ {err.code}` 中 `$` 与 `{` 之间有空格，模板字符串插值失效，运行时将原样输出 `$ {err.code}` | 改为 `${err.code}` | 高 |
| js-apis-demo-taskmanager.md | 示例代码不完整 | 66-70 | queryTasks 示例代码被截断：`tasks.forEach(...)` 回调未闭合，缺少 `});`、async 函数的 `}`，逻辑不完整且无法编译运行 | 补全代码：`console.info(...)` 后添加 `});` 与函数结束 `}`，并补充错误处理（try/catch 或 .catch） | 高 |
| js-apis-demo-taskmanager.md | 中英文混用/英文拼写错误 | 55 | 中文描述中夹杂英文单词 "recieve"，且拼写错误（应为 receive），不符合中文技术文档规范 | 改为中文表述，如"该接口会接收任务列表并返回给调用方" | 中 |
| js-apis-demo-taskmanager.md | 术语大小写错误 | 55 | "UiAbility" 拼写不符合官方组件名，正确写法为 "UIAbility" | 改为 "UIAbility" | 中 |
| js-apis-demo-taskmanager.md | 章节标签不一致 | 61 | queryTasks 使用"**完整示例**"标签，而 createTask（行34）使用"**示例**"，同一文档内章节标签应统一 | 统一为"**示例**：" | 低 |
| js-apis-demo-taskmanager.md | 锚点链接可能失效 | 23、59 | 链接 `[TaskInfo](#taskinfo)` 指向的标题实际为 `## TaskInfo9+`（行72），生成的锚点通常为 `#taskinfo9`，`#taskinfo` 可能无法跳转 | 核对渲染后的锚点并修正，如改为 `[TaskInfo](#taskinfo9)`，或去掉标题中的版本上标后统一锚点 | 低 |
| js-apis-demo-taskmanager.md | 章节内容缺失（错误码） | 53-59 | queryTasks 章节没有"错误码"小节，而 createTask 章节有；同类接口章节结构不一致，读者无法得知 queryTasks 可能的错误 | 为 queryTasks 补充"**错误码**"小节（至少说明有无错误码） | 中 |
| js-apis-demo-taskmanager.md | 权限说明格式不规范 | 15 | 权限要求 "需要权限 ohos.permission.RUNNING_TASKS" 混写在接口描述正文中，未按规范使用独立的"**需要权限**："条目，且未说明权限申请方式/授权级别 | 单独列出"**需要权限**：ohos.permission.RUNNING_TASKS"，并补充权限级别与申请方式说明 | 低 |
| js-apis-demo-taskmanager.md | 描述信息不足 | 55 | "任务在 UIAbility 退出后自动销毁"属于重要使用约束，但仅在 queryTasks 描述中一笔带过，未放入"使用约束/注意事项"，也未说明对 createTask 的影响 | 在模块说明或各接口下补充明确的"使用约束"说明任务生命周期 | 低 |
| js-apis-demo-taskmanager.md | 示例代码健壮性 | 67 | queryTasks 返回 Promise，示例直接 `await` 未做异常捕获，接口抛错时示例会崩溃，示范效果差 | 用 try/catch 包裹 `await demoTaskManager.queryTasks()` 并处理 `err.code`/`err.message` | 低 |

**小计：11 项**

---

## Task sdk_consistency_check

**文档**: `evals/inputs/js-apis-demo-taskmanager.md`
**SDK**: `evals/inputs/sdk/api/@ohos.demo.taskmanager.d.ts`

### 检查方面

- 版本标注（@since）与文档"9+"上标/起始版本说明
- 接口签名（函数名、参数、返回值类型）
- 数据结构（TaskInfo 属性集合与类型）
- 错误码（@throws 与文档错误码表）
- 权限声明（@permission 与文档权限描述）
- 示例代码与 SDK 定义的可编译性

### 不一致清单

| 文件名 | 问题类型 | 问题行号 | 问题原因 | 建议修改方案 | 问题严重级别 |
| --- | --- | --- | --- | --- | --- |
| js-apis-demo-taskmanager.md | 版本不一致 | 7、13、53、72（对应 d.ts 5、12、47、56） | 文档标注起始版本为 9（"9+"、"起始版本为9"），而 d.ts 中 namespace、TaskInfo、createTask、queryTasks 均为 `@since 10` | 以 SDK 为准，将文档所有版本上标改为 "10+"，模块说明改为"起始版本为10"（或确认 SDK 标注错误后反向修正） | 高 |
| js-apis-demo-taskmanager.md | 数据结构属性缺失 | 78-81（对应 d.ts 37） | d.ts 中 TaskInfo 含 `priority: number` 必填属性，文档 TaskInfo 属性表只有 name、delay，缺少 priority | 在属性表中补充 `priority \| number \| 是 \| 是 \| 任务优先级`，并说明取值范围 | 高 |
| js-apis-demo-taskmanager.md | 返回值类型不一致 | 26（对应 d.ts 49） | d.ts 声明 `createTask(...): void`，文档"返回值"写为 `AsyncCallback<number>` | 文档返回值改为"无"（void） | 高 |
| js-apis-demo-taskmanager.md | 权限声明不一致 | 15（对应 d.ts 40-49） | 文档声明需要 `ohos.permission.RUNNING_TASKS`，d.ts 的 createTask 注释中没有任何 @permission 声明 | 核实实际权限要求：若确需权限，SDK 应补 @permission 注释；若不需要，文档应删除权限描述。二者必须一致 | 高 |
| js-apis-demo-taskmanager.md | 错误码缺失 | 28-32（对应 d.ts 46） | d.ts createTask 声明 `@throws 801 - Capability not supported`，文档错误码表仅列 401，缺少 801 | 在 createTask 错误码表中补充 801 及其含义（能力不支持）与处理建议 | 中 |
| js-apis-demo-taskmanager.md | 错误码章节缺失 | 53-59（对应 d.ts 55） | d.ts queryTasks 声明 `@throws 401 - Parameter error`，文档 queryTasks 章节完全没有错误码表 | 为 queryTasks 补充错误码表（401） | 中 |
| js-apis-demo-taskmanager.md | 示例代码与 SDK 不一致 | 39-42（对应 d.ts 14-38） | 示例中 TaskInfo 对象字面量只赋值 name、delay，缺少 d.ts 中必填的 priority，按 SDK 定义该示例无法通过编译 | 示例补充 `priority` 字段赋值 | 中 |
| js-apis-demo-taskmanager.md | 描述信息无法由 SDK 佐证 | 55 | "任务在 UiAbility 退出后自动销毁"在 d.ts 注释中无对应说明，无法确认是否为实现行为（且 UiAbility 拼写错误） | 与实现确认后在 d.ts 注释与文档中同步补充生命周期说明，并更正为 UIAbility | 低 |

**一致性核对通过项**（无需修改）：queryTasks 返回值 `Promise<Array<TaskInfo>>` 与 d.ts 一致（行59 vs d.ts 58）；createTask 参数名/类型与 d.ts 一致；导入方式 `import demoTaskManager from '@ohos.demo.taskmanager'` 与 `export default` 一致。

**小计：8 项**

---

## Task dev_guide_scope_and_rules

**文件**: `evals/inputs/application-dev-guide-demo-task.md`

### 检查方面

1. **文档结构完整性**：概述、前提条件/约束、开发步骤、高级用法、相关文档等章节是否齐全、标题与内容是否匹配
2. **内容准确性**：步骤描述、代码示例是否正确可运行
3. **代码质量**：示例语法、模板字符串、错误处理、与 API 定义的匹配
4. **关键信息覆盖**：权限申请、错误码处理、生命周期约束等开发者必需信息
5. **语言规范**：中英文混用、拼写、模糊表述
6. **链接有效性**：相对链接指向的文件是否存在

### 问题清单

| 文件名 | 问题类型 | 问题行号 | 问题原因 | 建议修改方案 | 问题严重级别 |
| --- | --- | --- | --- | --- | --- |
| application-dev-guide-demo-task.md | 章节标题与内容不匹配/内容空洞 | 34-36 | "高级用法"章节内容却是"本节介绍任务管理的基础导入方式，参见上文开发步骤第 1 步"——标题为高级用法、内容为基础导入且只是循环引用上文，无任何实质内容 | 删除该章节，或补充真正的高级用法（如任务优先级设置、任务生命周期管理、错误码 801 处理等） | 高 |
| application-dev-guide-demo-task.md | 关键信息缺失（权限） | 17-30 | 创建任务步骤未说明需要申请权限（API 文档标注 createTask 需要 ohos.permission.RUNNING_TASKS），开发者按指南操作会因缺权限而失败 | 在开发步骤前增加"前提条件/权限申请"章节，说明所需权限及在 module.json5 中申请的方式 | 高 |
| application-dev-guide-demo-task.md | 链接失效 | 41 | 相关文档链接 `./background-task-guide.md` 指向的文件在同目录下不存在 | 修正为有效链接，或删除该条目 | 中 |
| application-dev-guide-demo-task.md | 示例代码错误（模板字符串） | 26 | `$ {err.code}` 中 `$` 与 `{` 之间有空格，插值失效，错误日志将原样输出占位文本 | 改为 `${err.code}` | 中 |
| application-dev-guide-demo-task.md | 中英文混用/拼写错误 | 32 | 中文句子中夹杂拼写错误的英文 "recieve"（应为 receive） | 改为纯中文表述："查询任务列表，接口会返回当前所有任务" | 中 |
| application-dev-guide-demo-task.md | 步骤不完整（缺示例） | 32 | 步骤 3"查询任务列表"只有一句描述，没有代码示例，与前两个步骤的呈现方式不一致，开发者无法照做 | 补充 queryTasks 的调用示例（含 await 与异常处理） | 中 |
| application-dev-guide-demo-task.md | 模糊表述 | 7 | "开发者大概需要注意任务的生命周期"中"大概"语义模糊，且"某些情况下任务会被系统自动回收"未说明具体条件，指导性差 | 删除"大概"，明确说明任务回收/销毁的具体条件（如 UIAbility 退出后任务自动销毁）及应对建议 | 中 |
| application-dev-guide-demo-task.md | 示例代码错误处理不完整 | 24-29 | createTask 回调仅在 err 分支打印日志，成功分支无任何处理（taskId 未使用），且未说明可能的错误码（401/801）及含义 | 补充成功分支示例与错误码说明，或链接到 API 参考的错误码表 | 低 |
| application-dev-guide-demo-task.md | 概述与指南范围不匹配 | 3、5-7 | 首段称指南面向"希望了解任务管理基本用法的开发者"，但正文未覆盖查询结果的使用、约束与限制等基本信息，概述提到的"自动回收"也未在步骤中体现 | 概述与正文章节对齐，补充"约束与限制"说明 | 低 |
| application-dev-guide-demo-task.md | 示例与 API 定义疑似不一致 | 20-23 | TaskInfo 字面量只含 name、delay；若 SDK 中 priority 为必填（见 SDK 一致性检查），此示例无法编译 | 与 API 参考/SDK 核对 TaskInfo 必填字段后补全示例 | 中 |

**小计：10 项**

---

## 总计

| 任务 | 发现数 |
| --- | --- |
| api_doc_planted_errors | 11 |
| sdk_consistency_check | 8 |
| dev_guide_scope_and_rules | 10 |
| **合计** | **29** |
