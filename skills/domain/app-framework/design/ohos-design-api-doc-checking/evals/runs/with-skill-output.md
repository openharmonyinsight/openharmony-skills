# API 文档质量检查结果（with-skill 运行输出）

- 执行 Skill：`ohos-design-api-doc-checking`（v0.1.0），规则索引 `references/index.json` v2.0.0
- 严重级别映射：critical→严重、high→高、medium→中、low→低（`priorityLabels`）
- 置信度依据各规则 JSON 中 `confidence` 字段并结合证据强度调整（参见 `scoring-guide.md`）
- 说明：按评测要求以 Markdown 表格代替 .xlsx 输出，列结构与 `reportTemplate.columns` 一致

---

## Case api_doc_planted_errors

**输入**：`evals/inputs/js-apis-demo-taskmanager.md`（81 行）

**文档类型判定**：**API 文档**。依据 SKILL.md「文档类型判断」：文件名匹配 `js-apis-*.md` 模式；内容包含 API 方法签名（createTask/queryTasks）、参数表、返回值、错误码、接口属性表。

**模块执行范围**（API 文档全部必选，共 10 个规则模块）：

| 模块 | 是否执行 | 结果 |
|------|---------|------|
| spelling | 执行 | 2 项问题（L55） |
| syntax | 执行 | 2 项问题（L46、L63-70） |
| path-consistency | 执行 | 无问题（无目录/文件创建步骤，无 srcEntry/Sample 引用） |
| semantics | 执行 | 无问题（无 bundleName/moduleName/abilityName 占位符场景） |
| project-structure | 执行 | 无问题（未涉及工程目录与配置文件名） |
| findability | 执行 | 2 项问题（L23/59 锚点、文末无相关文档章节） |
| completeness | 执行 | 2 项问题（queryTasks 缺错误码、缺设备约束说明） |
| correctness | 执行 | 2 项问题（L26 返回值逻辑矛盾、版本标记格式）；**SDK 源码一致性子检查按用户指示（"不做 SDK 源码比对"）跳过** |
| clarity | 执行 | 3 项问题（L3 取消能力、L61 完整示例、L55 描述） |
| capability | 执行 | 无新增问题（权限 L15、SystemCapability L17/57 已声明，capability-001/007 通过） |

**问题清单**（12 项，按严重级别排序）：

| 文件名 | 问题类型(规则ID) | 问题行号 | 问题原因 | 建议修改方案 | 问题严重级别 | 置信度 |
|--------|-----------------|---------|---------|-------------|------------|--------|
| js-apis-demo-taskmanager.md | 示例代码不完整/语法错误 (correctness-002, syntax-002, syntax-003) | 63-70 | queryTasks 示例代码块被截断：L66 `async function queryAll() {` 与 L68 `tasks.forEach((task) => {` 打开的 2 个大括号、`forEach(` 等 2 个圆括号均未闭合，代码在 L69 后直接结束，无法编译运行 | 补全代码：`});`（闭合 forEach）、`}`（闭合 queryAll），并补充 `queryAll()` 调用入口及 try-catch/err 错误处理 | 严重 | 95% |
| js-apis-demo-taskmanager.md | 代码语法 (syntax-001) | 46 | 模板字符串 `` `createTask failed, code is $ {err.code}, ...` `` 中 `$` 与 `{` 之间有空格，不构成插值语法，运行时将输出字面量 "$ {err.code}" 而非错误码 | 将 `$ {err.code}` 改为 `${err.code}`（同行 `${err.message}` 写法正确，可对照） | 高 | 100% |
| js-apis-demo-taskmanager.md | 拼写错误-鸿蒙专有名词 (spelling-002) | 55 | `UiAbility` 大小写错误，HarmonyOS 标准名词为 `UIAbility`（glossary AbilityFramework.UIAbility 的 variants 明确列出 UiAbility 为错误形式） | 将 `UiAbility` 改为 `UIAbility` | 高 | 95% |
| js-apis-demo-taskmanager.md | 清晰易懂-标题与内容不符 (clarity-001) | 61 | 小节标注 "**完整示例**：" 但其下代码（L63-70）不完整、被截断，命中 badPattern「标题为'完整示例'但代码不完整」 | 补全示例代码使其真正完整，或将标题改为「示例」 | 高 | 85% |
| js-apis-demo-taskmanager.md | 清晰易懂-标题与内容不符 (clarity-001) | 3 | 模块简介声称「用于创建、查询和取消后台任务」，但全文仅文档化 createTask（创建）与 queryTasks（查询）两个 API，不存在任何「取消」相关章节，描述与内容不符 | 若确有取消能力则补充 cancelTask API 章节（含参数/返回值/错误码/示例）；否则从简介中删除「和取消」 | 高 | 85% |
| js-apis-demo-taskmanager.md | 正确性-JSDOC/描述错误 (correctness-003) | 26 | createTask 为 AsyncCallback 回调风格 API，L24 已声明第二个参数类型为 `AsyncCallback<number>`，而 L26「返回值」又写 `AsyncCallback<number>`，回调参数类型被误作返回值类型，逻辑矛盾（回调风格 API 返回值应为 void） | 将 L26 改为「**返回值**：void」或按回调风格 API 文档规范删除返回值小节 | 高 | 80% |
| js-apis-demo-taskmanager.md | 完整性-关键说明缺失 (completeness-002) | 53-70 | queryTasks 章节缺少「错误码」小节（apiDoc 必备章节为 参数/返回值/示例/错误码，本章节仅有返回值与示例）；Promise 风格接口拒绝时的 BusinessError 错误码无处可查 | 在 queryTasks 章节补充「**错误码**」表（至少覆盖 401 Parameter error） | 高 | 85% |
| js-apis-demo-taskmanager.md | 拼写错误 (spelling-001) | 55 | `recieve` 为常见拼写错误，应为 `receive`（commonMisspellings 明确收录）；且中文描述中混用英文动词，表达不规范 | 改为 `receive`；建议整体改写为中文「该接口会获取任务列表并返回给调用方」 | 中 | 95% |
| js-apis-demo-taskmanager.md | 格式问题/正确性 (correctness-001) | 13, 53, 72 | API 版本标记未按规范使用 `<sup>` 上标格式，直接写作 `createTask9+`、`queryTasks9+`、`TaskInfo9+`（versionPatterns 期望 `<sup>\d+\+?</sup>`），渲染后版本号与 API 名粘连 | 改为 `## demoTaskManager.createTask<sup>9+</sup>`、`## demoTaskManager.queryTasks<sup>9+</sup>`、`## TaskInfo<sup>9+</sup>` | 中 | 85% |
| js-apis-demo-taskmanager.md | 资源易找性-交叉引用失效 (findability-003, clarity-003) | 23, 59 | 页内链接 `[TaskInfo](#taskinfo)` 无法跳转：因标题 L72 为 `## TaskInfo9+`（未用 `<sup>` 包裹版本号），Markdown 生成的实际锚点为 `#taskinfo9`，与链接目标 `#taskinfo` 不匹配 | 修复 L72 标题为 `## TaskInfo<sup>9+</sup>` 后锚点 `#taskinfo` 自动生效；或将两处链接改为 `#taskinfo9` | 中 | 80% |
| js-apis-demo-taskmanager.md | 完整性-规格约束说明缺失 (completeness-003) | 5-11 | 模块说明块仅声明起始版本与导入方式，未说明支持的设备类型（phone/tablet/2in1 等）；queryTasks 章节也未说明是否需要权限（createTask 在 L15 有权限说明，形成不对称） | 在说明块补充设备支持范围；核实并说明 queryTasks 的权限要求 | 中 | 70% |
| js-apis-demo-taskmanager.md | 资源易找性-可发现性 (findability-003) | 81 | 文档末尾（L81 之后）缺少「相关文档/参见」章节，未链接对应开发指南或 Sample 工程，信息发现链路不完整 | 文末添加「相关文档」章节，链接任务管理开发指南与示例代码仓库 | 中 | 70% |

---

## Case sdk_consistency_check

**输入**：
- 文档：`evals/inputs/js-apis-demo-taskmanager.md`
- SDK：`evals/inputs/sdk/api/@ohos.demo.taskmanager.d.ts`（61 行，相当于 `INTERFACE_SDK_JS_PATH=evals/inputs/sdk`）

**文档类型判定**：API 文档（同 Case 1）。

**文件映射**：按 `correctness-rules.json → sdkSourceCheck.mappingRules` 顺序匹配，命中规则 `^js-apis-(?<name>[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\.md$ → api/@ohos.{name}.d.ts`，捕获 `name=demo-taskmanager`，经 `transforms.name = hyphen-to-dot` 转换为 `demo.taskmanager`，得到 `api/@ohos.demo.taskmanager.d.ts`；`mappingRules.assertions` 中登记了同一期望值，文件存在性校验通过，映射成功。

**模块执行范围**：仅执行 `correctness.sdkSourceCheck` 的 10 个检查点（api-since-version-match / param-count-match / param-name-match / param-type-match / return-type-match / systemapi-mark-match / stagemodelonly-mark-match / error-code-match / enum-values-complete / interface-fields-complete）。

**不一致清单**（7 项，按严重级别排序）：

| 文件名 | 问题类型(规则ID) | 问题行号 | 问题原因 | 建议修改方案 | 问题严重级别 | 置信度 |
|--------|-----------------|---------|---------|-------------|------------|--------|
| js-apis-demo-taskmanager.md | API起始版本不一致 (api-since-version-match) | 7, 13, 53, 72 | 文档标注模块及全部 API 起始版本为 9（L7「起始版本为9」、L13 `createTask9+`、L53 `queryTasks9+`、L72 `TaskInfo9+`）；SDK 中 namespace（d.ts L5）、TaskInfo（L12）、createTask（L47）、queryTasks（L56）均为 `@since 10`，版本全面不一致 | 以 SDK `@since 10` 为准，将说明块改为「起始版本为10」，各标题版本标记改为 `<sup>10+</sup>`（若文档正确则应推动 SDK 修正，二者必须统一） | 严重 | 95% |
| js-apis-demo-taskmanager.md | 返回值类型不一致 (return-type-match) | 26 | createTask 文档「返回值」为 `AsyncCallback<number>`；SDK 声明 `function createTask(taskInfo: TaskInfo, callback: AsyncCallback<number>): void;`（d.ts L49），实际返回类型为 `void` | 将 L26 改为「**返回值**：void」 | 高 | 90% |
| js-apis-demo-taskmanager.md | 文档描述SDK中不存在的能力 (SDK中未找到对应API / correctness-001) | 3 | 文档简介称「用于创建、查询和取消后台任务」；SDK namespace 仅导出 `TaskInfo`、`createTask`、`queryTasks`（d.ts L7-59），不存在任何取消（cancel）类 API | 从简介中删除「和取消」；若取消能力确在其他模块/版本提供，补充准确出处链接 | 高 | 90% |
| js-apis-demo-taskmanager.md | 示例代码与SDK接口不一致-无法编译 (interface-fields-complete 衍生 / correctness-002) | 39-42 | 示例中 `let taskInfo: demoTaskManager.TaskInfo = { name: 'demoTask', delay: 1000 };` 仅赋值 2 个字段；SDK 的 TaskInfo 含 3 个必填字段 name、delay、`priority: number`（d.ts L31-37，非可选），缺少 priority 在 ArkTS 严格类型检查下编译失败 | 示例对象补充 `priority` 字段赋值（如 `priority: 1`，并说明取值含义） | 高 | 90% |
| js-apis-demo-taskmanager.md | 错误码缺失 (error-code-match) | 30-32 | createTask 文档错误码表仅列 401；SDK `@throws` 声明 401（d.ts L45）与 `801 - Capability not supported.`（d.ts L46）两个错误码，文档缺失 801 | 在错误码表补充 801 行，并说明触发条件（设备不支持该系统能力），与「能力由系统提供」及设备支持范围呼应 | 中 | 85% |
| js-apis-demo-taskmanager.md | 错误码缺失 (error-code-match) | 53-70 | queryTasks 章节无错误码表；SDK queryTasks 声明 `@throws {BusinessError} 401 - Parameter error.`（d.ts L55），文档未列出 | 为 queryTasks 补充错误码表并列入 401 | 中 | 85% |
| js-apis-demo-taskmanager.md | 接口字段缺失 (interface-fields-complete) | 78-81 | TaskInfo 属性表仅列 name、delay 两个字段；SDK interface TaskInfo 含 name（d.ts L21）、delay（L29）、`priority: number`（L37，Task priority）三个字段，文档缺失 priority | 在属性表补充一行：priority \| number \| 是 \| 是 \| 任务优先级 | 中 | 85% |

**通过的检查点**：

| 检查点 | 结论 | 证据 |
|--------|------|------|
| param-count-match | 通过 | createTask 文档 2 个参数（L23-24）= SDK 2 个形参（d.ts L49） |
| param-name-match | 通过 | taskInfo、callback 与 SDK 形参名逐一一致 |
| param-type-match | 通过 | taskInfo: TaskInfo（doc L23 = d.ts L49）；callback: AsyncCallback&lt;number&gt;（doc L24 = d.ts L49） |
| return-type-match (queryTasks) | 通过 | doc L59 `Promise<Array<TaskInfo>>` = d.ts L58 |
| systemapi-mark-match | 通过 | 文档文件名无 `-sys` 后缀，SDK 无 `@systemapi` 标记，二者一致（L7「能力由系统提供」为 SystemCapability 标准样板文字，非系统接口标记） |
| stagemodelonly-mark-match | 通过 | 文档未标注 Stage 模型约束，SDK 无 `@stagemodelonly`，一致 |
| enum-values-complete | 不适用 | 文档与 SDK 均无枚举定义 |

---

## Case dev_guide_scope_and_rules

**输入**：`evals/inputs/application-dev-guide-demo-task.md`（41 行）

**文档类型判定**：**开发指南**。依据 SKILL.md「文档类型判断」：文件名包含 `guide` 关键词（application-dev-guide-*），内容为概述、开发步骤、相关文档等指导性章节，无系统性 API 签名/参数表/错误码结构。

**模块执行范围说明**（按 SKILL.md「检查项选择 → 开发指南（选择性执行）」）：

*执行的模块（必选 8 个）*：

| 模块 | 结果 |
|------|------|
| spelling | 执行，1 项问题（L32） |
| syntax | 执行，1 项问题（L26）；子规则 syntax-006（missing-semicolon）因 `enabled:false` 未执行 |
| path-consistency | 执行，无问题（无目录/文件创建步骤；L40 链接 `./js-apis-demo-taskmanager.md` 目标文件存在于同目录） |
| clarity | 执行，2 项问题（L7 模糊表述、L34-36 标题不符） |
| semantics | 执行，无问题（无 bundleName/abilityName/moduleName/packageName 占位符场景；semantics-004 因 `enabled:false` 未执行） |
| project-structure | 执行，无问题（未涉及工程目录名、配置文件名或扩展名） |
| findability | 执行，2 项问题（L34 关键词不符、L41 失效链接） |
| correctness | 执行，1 项问题（L41 链接有效性归入此项交叉验证）；无敏感信息（correctness-005 通过） |

*执行的模块（可选 2 个，本次选择执行）*：

| 模块 | 执行理由 | 结果 |
|------|---------|------|
| completeness | 该文档为场景型开发指南，步骤完整性与约束说明直接决定开发者能否跑通流程，且规则在 index.json 中 enabled=true | 2 项问题（L32 步骤缺示例、缺「约束限制」章节） |
| capability | 指南涉及权限/系统能力等使用前提，需评估约束条件与示例实用性 | 1 项问题（L24-29 示例缺成功分支，与 completeness 约束缺失合并核查） |

*跳过的模块*：

| 模块/检查 | 跳过原因 |
|-----------|---------|
| SDK 源码一致性检查（correctness.sdkSourceCheck 的 10 个检查点） | SKILL.md 对开发指南明确规定「不执行：SDK源码一致性检查（不适用）」——开发指南不与单一 .d.ts 文件建立映射关系 |
| syntax-006、semantics-004 | 规则文件中 `enabled: false`，全局停用 |

**问题清单**（9 项，按严重级别排序）：

| 文件名 | 问题类型(规则ID) | 问题行号 | 问题原因 | 建议修改方案 | 问题严重级别 | 置信度 |
|--------|-----------------|---------|---------|-------------|------------|--------|
| application-dev-guide-demo-task.md | 代码语法 (syntax-001) | 26 | 模板字符串 `` `createTask failed: $ {err.code}` `` 中 `$` 与 `{` 之间有空格，不构成插值，运行时输出字面量 "$ {err.code}" 而非错误码，导致示例排错信息失效 | 改为 `${err.code}` | 高 | 100% |
| application-dev-guide-demo-task.md | 清晰易懂-功能描述不准确 (clarity-002) | 7 | 一句话连用 3 个规则命中的模糊表述：「某些情况下」（未指明何种情况）、「可能会影响」（未说明触发条件与必然性）、「大概需要注意」（不确定语气）。任务回收条件与生命周期应对恰是本节关键信息，模糊化后开发者无法据此设计业务 | 明确写出：任务被系统回收的具体触发条件（如应用退到后台超时、内存回收）、对业务的确定性影响、以及开发者应采取的措施（如持久化任务数据、查询任务状态） | 高 | 85% |
| application-dev-guide-demo-task.md | 清晰易懂-标题与内容不符 (clarity-001) | 34-36 | 「## 高级用法」章节内容仅为「本节介绍任务管理的基础导入方式，参见上文开发步骤第 1 步」，复述基础导入且无任何高级内容，命中 badPattern「标题为'高级用法'但只讲基础」；且与 L3「基本用法」的文档定位自相矛盾 | 补充真正的高级内容（如批量任务管理、异常恢复、任务生命周期处理），或删除本章节 | 高 | 85% |
| application-dev-guide-demo-task.md | 完整性-示例代码缺失 (completeness-001) | 32 | 开发步骤 3「查询任务列表」仅一句文字描述，无 queryTasks 示例代码；步骤 1、2 均配有代码块，指导在步骤 3 出现断点，不满足「step by step 完整指导、无操作断点」要求 | 补充可运行示例：`let tasks = await demoTaskManager.queryTasks();` 及结果遍历与错误处理（完整闭合的代码块） | 高 | 85% |
| application-dev-guide-demo-task.md | 完整性-关键说明缺失/约束条件缺失 (completeness-002, capability-001) | 9-32 | 指南缺少「约束限制」章节（guideDoc 必备章节：概述/开发步骤/示例代码/约束限制）；全文未提及调用 createTask 所需权限 `ohos.permission.RUNNING_TASKS`、系统能力 `SystemCapability.Demo.TaskManager` 及起始版本要求，开发者按指南操作将在首次调用即遇权限/能力错误 | 在「开发步骤」前或文末增加「约束限制」章节，说明所需权限（含 module.json5 申请方式与授权步骤）、系统能力、API 起始版本 | 高 | 85% |
| application-dev-guide-demo-task.md | 资源易找性-描述关键字不准确 (findability-001) | 34 | 章节标题关键词「高级用法」与文档实际内容（仅基础导入）不符，命中 badPattern「标题使用'高级用法'但内容仅包含基础示例」，误导以「任务管理 高级用法」为关键词检索的开发者 | 使标题与内容一致：改标题为「导入方式说明」并合并入开发步骤，或补充高级内容 | 高 | 80% |
| application-dev-guide-demo-task.md | 拼写错误 (spelling-001) | 32 | `recieve` 为常见拼写错误，应为 `receive`（commonMisspellings 收录）；中文语境混用英文动词亦不规范 | 改为 `receive`，建议改写为「接口会获取所有任务并返回」 | 中 | 95% |
| application-dev-guide-demo-task.md | 资源易找性-交叉引用失效 (findability-003, correctness 链接有效性) | 41 | 链接 `[后台任务开发指导](./background-task-guide.md)` 的目标文件在被检文档所在目录中不存在（目录内仅有 application-dev-guide-demo-task.md、js-apis-demo-taskmanager.md、sdk/），开发者点击后 404 | 核实并修正为实际存在的文档相对路径；若该文档尚未编写，先移除链接或标注「即将上线」 | 中 | 85% |
| application-dev-guide-demo-task.md | 能力易用性-示例代码不实用 (capability-005) | 24-29 | createTask 示例回调仅处理错误分支，形参 `taskId` 声明后从未使用，无成功处理逻辑，未展示完整调用流程（对照 API 文档版示例含成功分支，指南版被简化丢失） | 补充成功分支，使用 taskId 完成日志输出或后续业务处理，体现完整工作流 | 中 | 75% |

---

## 汇总统计

| Case | 文档类型 | 问题总数 | 严重 | 高 | 中 | 低 |
|------|---------|---------|------|----|----|----|
| api_doc_planted_errors | API 文档 | 12 | 1 | 6 | 5 | 0 |
| sdk_consistency_check | API 文档（SDK 一致性） | 7（另 7 个检查点通过/不适用） | 1 | 3 | 3 | 0 |
| dev_guide_scope_and_rules | 开发指南 | 9 | 0 | 6 | 3 | 0 |
