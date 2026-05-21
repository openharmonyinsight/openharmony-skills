---
name: arkweb-code-gen
description: ArkWeb 代码生成全流程。按需求设计文档自动编排：需求分析 → 设计遵从性门禁 → 业务对齐 → 代码实现 → 代码检视 → 修复循环 → 设计差异对齐 → 编译-修复循环（共8个Phase）。触发词：实现需求、执行需求、开发需求、生成代码、实现功能、代码生成、写实现、按需求文档实现。
---

# ArkWeb 需求开发团队 — 实现全流程 Skill

本 Skill 作为**纯编排器**（Team Lead），调度四个 Agent Teammate 协作完成从需求到代码的全过程。
Team Lead **不参与**具体分析、编码、检视——只负责流程编排、门禁检查、用户交互。

## 团队成员与通信模型

```
                 ┌─────────────────────────────────────────┐
                 │   Team Lead: 本 Skill (SKILL.md)        │
                 │   职责: 创建团队、分配任务、汇总结果、    │
                 │         门禁检查、差异对齐、用户交互、    │
                 │         编译编排                         │
                 │   不做: 不分析需求、不写代码、不检视代码  │
                 └──────────────┬──────────────────────────┘
                                │ 创建团队 + 分配初始任务
               ┌────────────────┼────────────────┐
               ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Teammate #1  │  │ Teammate #2  │  │ Teammate #3  │
    │ requirements │◄─►│  arkweb-     │◄─►│  arkweb-     │
    │ -analysis    │  │  coder       │  │  reviewer    │
    │ [🔴 opus]    │  │ [🔵 opus]    │  │ [🟢 sonnet]  │
    │              │  │              │  │              │
    │ 需求分析专家 │  │ 代码实现工程师│  │ 代码检视工程师│
    └──────────────┘  └──────────────┘  └──────────────┘
                            ▲
                            │ 编译结果 + 报错报告
                            │
                  ┌──────────────┐
                  │ Teammate #4  │
                  │  arkweb-     │
                  │  builder     │
                  │ [🟠 sonnet]  │
                  │              │
                  │ 编译验证工程师│
                  └──────────────┘
```

Teammates 之间可以直接通信（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`），不需要经过 Team Lead 中转。

| Teammate | 角色 | 只做 | 禁止 |
|----------|------|------|------|
| requirements-analysis | 需求分析专家 | 需求理解、架构分析、代码探查、输出步骤报告、回答队友业务疑问 | 编写业务代码、修改 BUILD.gn |
| arkweb-coder | 代码实现工程师 | 按报告实现代码、修复检视问题、向需求专家请教业务疑问 | 自行分析需求、偏离报告方案 |
| arkweb-reviewer | 代码检视工程师 | 8维度检视、生成 Fix Step、向需求专家确认业务上下文 | 直接修改任何代码文件 |
| arkweb-builder | 编译验证工程师 | 执行编译、分析报错、生成结构化报告 | 修改代码、修复错误、clean/reset |

## Team 初始化

```
Teammate #1: requirements-analysis  (model: opus)
Teammate #2: arkweb-coder           (model: opus)
Teammate #3: arkweb-reviewer        (model: sonnet)
Teammate #4: arkweb-builder         (model: sonnet)
```

共享上下文：需求设计文档路径、分析报告路径、检视报告路径、编译报错报告路径、Teammate 标识。

Team Lead 职责：创建 Team + 传递共享上下文、Phase 2/7/8 的执行与编排、全局进度追踪、异常处理。

## 流程总览

| Phase | 名称 | 执行者 | 输出 |
|-------|------|--------|------|
| 0 | 开发环境预检 | Team Lead | 环境检查报告 |
| 1 | 需求分析 | requirements-analysis | 分析报告 |
| 2 | 设计遵从性门禁 | Team Lead | 遵从性检查结果 |
| 3 | 业务对齐 | arkweb-coder ↔ requirements-analysis | 业务对齐确认 |
| 4 | 代码实现 | arkweb-coder | 代码变更 |
| 5 | 代码检视 | arkweb-reviewer | 检视报告 |
| 6 | 修复循环 | arkweb-coder ↔ arkweb-reviewer | 修复后代码 |
| 7 | 设计差异对齐 | Team Lead（交互式） | 差异对齐结果 |
| 8 | 编译-修复循环 | Team Lead + builder + coder + reviewer | 编译通过确认 |

## Phase 交接协议

```
Phase 0 → 1:  环境预检全部通过（Agent Teams 可用、Agent 文件齐全、Claude Code 版本满足）
Phase 1 → 2:  分析报告已生成（含"五、实现步骤"且至少 1 个 Step）
Phase 2 → 3:  无未确认的 [偏离-需用户确认] 项
Phase 3 → 4:  arkweb-coder 声明"业务对齐完成" + requirements-analysis 确认
Phase 4 → 5:  arkweb-coder 输出变更文件清单
Phase 5 → 6:  检视报告已生成
Phase 6 → 7:  BLOCKER/CRITICAL 清零，或达到 5 轮上限
Phase 7 → 8:  所有代码变更已最终确定（设计差异已对齐）
Phase 8 → 完成:  编译成功（exit code 0）或达到 10 轮上限
```

> **注意**：在 `.claude/skills` 目录中，设计差异对齐已提取为独立 skill（`arkweb-design-alignment`），由 `arkweb-architect` 全流程调度执行。在 `arkweb-sdd` 目录中，Phase 6 逻辑内嵌于本文件（见下方 Phase 5 完整内容），因为 `arkweb-design-alignment` skill 不存在于 arkweb-sdd。

**Spec 驱动：** 优先依据结构化 Spec（spec.md）生成代码，设计文档作为上下文补充。

## 知识库驱动规则（离线 + DeepWiki）

通用规则统一引用：`../_shared/KB_RULES.md`。
本 skill 的增量要求如下：

- 代码实现前必须产出候选子系统/部件/API 证据包。
- 外部接口落地前必须对照离线 `apis/*/*.json` 与本地头文件，避免接口口径漂移。
- 若实现偏离证据包，必须在输出中说明偏离原因与风险。

## 输入

用户需提供一个**需求设计文档路径**（必需），可选提供：
- **Spec 文件路径**（推荐，优先于纯文档驱动）
- 需求分析报告输出路径（默认 `{DOCS_REPO}/tmp/arkweb_requirements_analysis.md`）
- 检视报告输出路径（默认 `{DOCS_REPO}/tmp/arkweb_review_report.md`）
- 编译报错报告路径（默认 `{DOCS_REPO}/tmp/arkweb_build_error_report.md`）

## 执行步骤

### Phase 0: 开发环境预检

执行者：Team Lead 直接执行（不启动 Agent）
知识：→ Read [reference/env-check.md](reference/env-check.md)

在启动任何 Teammate 之前，执行环境预检。按 `reference/env-check.md` 中的检查清单逐项验证（Agent Teams 环境变量、Agent 定义文件、Reference 文件、编译脚本、Claude Code 版本）。未通过项按参考文档中的自动修复流程处理。

**输出内容（强制）**：
- 候选子系统（1~3）
- 候选部件（3~10）
- 候选 API（5~30）
- 每条证据附来源、路径/URL、命中原因、置信度

**【强制持久化】** 证据包 Write 到 `{DOCS_REPO}/tmp/`，详见 `_shared/KB_RULES.md` 第 10 节。

**Phase 0 完成判定**：
- 已按标准顺序完成离线检索
- 已形成候选证据包并写入后续分析上下文
- **证据包已持久化到 `{DOCS_REPO}/tmp/` 目录**（Write 工具完成，文件存在且内容完整）
- 全部环境检查项 PASS。FAIL 时报告阻断原因，停止流程。

---

### Phase 1: 需求分析

执行者：`requirements-analysis` Agent

指令：
```
请分析以下需求设计文档，按照你的标准流程执行 Phase 0 ~ Phase 3，
生成完整的实现步骤清单。

需求文档路径：{用户提供的文档路径}
分析报告输出路径：{分析报告路径，默认 {DOCS_REPO}/tmp/arkweb_requirements_analysis.md}

【强制要求】必须先 Read 需求设计文档全文，提取其中的架构方案、技术路径、
接口定义、错误码、参数校验规则等强制约束项，然后基于设计文档的方案
（而非代码库中已有的类似模式）来规划实现步骤。

【知识库要求】需求分析报告必须新增"知识库证据包"章节，包含：
1. 候选子系统、部件、API（含分数与命中原因）
2. 每条证据的来源类型（按 `_shared/KB_RULES.md` 的 source_type）与路径
3. 低置信度项标注"推断项"


请先 Read 需求文档，然后按 Phase 1→2→3 顺序执行，
最终将报告 Write 到指定输出路径。
```

**Phase 1 完成判定**：
- 使用 Read 检查分析报告文件已生成
- 报告中包含"五、实现步骤"章节且至少有 1 个 Step
- 报告中"六、自检清单"所有项不为空
- 报告中包含"知识库证据包"章节且存在 LOCAL_KB 主证据
- **证据包已持久化到 `{DOCS_REPO}/tmp/` 目录**（Phase 0 的证据包文件存在）

**如果 Phase 1 失败**（报告未生成或内容不完整）：
- 停止流程
- 向用户说明分析失败的原因
- 展示已获取的部分分析结果

---

### Phase 2: 设计遵从性门禁

执行者：Team Lead 直接执行（不启动 Agent）
知识：→ Read [reference/design-conformance-check.md](reference/design-conformance-check.md)

并行 Read 设计文档和分析报告，按 `reference/design-conformance-check.md` 中的 5 个维度逐项比对，按 3 级规则分类偏离项。存在 `[偏离-需用户确认]` 时暂停流程请用户决策（A 接受/B 退回/C 逐项决定）。

完成判定：无未确认的 `[偏离-需用户确认]` 项。

---

### Phase 3: 业务对齐

执行者：`arkweb-coder` Agent

指令：
```
请先完整阅读需求分析报告，整理出所有不确定的业务疑问。

需求设计文档路径：{用户提供的文档路径}
需求分析报告路径：{分析报告路径}

【Phase 3: 业务对齐 — 编码前必做】
1. Read 需求设计文档全文
2. Read 分析报告全文
3. 整理出所有不确定的业务疑问，逐一向 requirements-analysis 请教
4. 等待所有疑问得到解答后，声明"业务对齐完成"
5. 如果阅读后确认无疑问，直接声明"业务对齐完成，无待确认疑问"

有疑问不猜测，宁可多问不要猜错。
完成后报告业务对齐结果（已提问数量 + 已解答数量）。
```

完成判定：arkweb-coder 声明"业务对齐完成"且 requirements-analysis 确认。
超时时 Team Lead 介入汇总未决问题，请用户一次性解答。

---

### Phase 4: 代码实现

执行者：`arkweb-coder` Agent

指令：
```
业务对齐已完成，请按分析报告中的实现步骤逐 Step 执行代码实现。

需求设计文档路径：{用户提供的文档路径}
需求分析报告路径：{分析报告路径}

【强制要求】
1. 需求设计文档是最高优先级的参考，分析报告是执行指南
2. 设计文档中指定的技术路径不可自行替换
3. 设计文档要求修改的所有层级/仓库都必须实现，包括 deps_code/ 目录

【代码规范】严格遵循你内置的代码生成规范和项目模板执行。

请按你的内部 Phase 1→2→3→4 顺序执行。
完成后输出变更文件清单和验证报告。
```

完成判定：Agent 报告所有 Step 已完成（或部分完成）。
部分失败时记录失败的 Step，继续 Phase 5 检视已完成部分。

---

### Phase 5: 代码检视

执行者：`arkweb-reviewer` Agent

指令：
```
请对所有变更文件进行完整的代码检视。

需求设计文档路径：{用户提供的文档路径}
需求分析报告路径：{分析报告路径}

【检视过程中】如果在 H 维度（设计遵从性）有疑问，直接向 requirements-analysis 确认。
【检视报告要求】每个 Issue 给出代码修改建议 + 测试验证建议。

变更文件来源：分析报告中"四、代码探查结果"列出的文件 + git diff 获取的变更文件。

请按你的内部 Phase 1→2→3→4 顺序执行：
1. 收集变更范围
2. 逐文件检视（A~H 共 8 个维度，含 H-设计遵从性）
3. 交叉验证
4. 生成检视报告到 {检视报告路径，默认 {DOCS_REPO}/tmp/arkweb_review_report.md}

特别注意 H 维度：检查实现是否忠实于设计文档的架构方案、错误码定义、实现范围和参数校验规则。
```

完成判定：检视报告已生成，包含"问题清单"章节和检视摘要。

---

### Phase 6: 修复循环

执行者：arkweb-coder ↔ arkweb-reviewer 直接沟通（Team Lead 不参与细节）

循环逻辑：max_rounds = 5，每轮 coder 修复 → reviewer 复检 → 统计 BLOCKER/CRITICAL。清零则通过，超限则向用户报告剩余问题。分歧涉及业务逻辑时请 requirements-analysis 仲裁。

给 coder 的指令：
```
请根据代码检视报告中的"附录: 修改指引"章节，逐个 Fix Step 执行修复。
检视报告路径：{检视报告路径}
仅修复报告中列出的问题，不做额外改动。修复完成后直接通知 arkweb-reviewer 复检。
这是第 {current_round}/{max_rounds} 轮修复。
```

给 reviewer 的指令：
```
arkweb-coder 已完成第 {current_round} 轮修复，请复检。
上轮修复的文件：{修复轮次变更的文件列表}
检视报告输出路径：{检视报告路径}
```

---

### Phase 7: 设计差异对齐

执行者：Team Lead 主导（交互式）
知识：→ Read [reference/design-diff-alignment.md](reference/design-diff-alignment.md)

循环逻辑：max_diff_rounds = 5。按 `reference/design-diff-alignment.md` 中的 10 个维度比对设计文档与实际实现，逐一向用户展示差异并请求决策（A 接受/B 重做/C 搁置），执行回写或重做操作。重做后重新比对，无新差异则退出。

完成判定：所有差异已处理（通过或达到最大轮次）。

---

### Phase 8: 编译-修复循环

执行者：Team Lead 编排 + arkweb-builder + arkweb-coder + arkweb-reviewer
知识：→ Read [reference/build-verification.md](reference/build-verification.md)

循环逻辑：max_rounds = 10。按 `reference/build-verification.md` 中的流程，builder 编译 → 失败则 coder 修复 → reviewer 检视（内层最多 3 轮）→ 重新编译。编译通过则完成。

2. Read 需求分析报告（{DOCS_REPO}/tmp/arkweb_requirements_analysis.md）
   → 提取：实现步骤清单、代码探查结果、自检清单

3. Read 检视报告（{DOCS_REPO}/tmp/arkweb_review_report.md）
   → 提取：修复过程中产生的技术决策、接口变更、架构调整
```

**比对维度**：

```
设计要素              比对方法                              差异类型
─────────────────────────────────────────────────────────────────────
接口/API 签名         设计文档的 API 定义 vs 实际代码的头文件   签名差异
数据结构/枚举         设计文档的字段定义 vs 实际 struct/enum    字段差异
类/继承关系           设计文档的类图 vs 实际 class 定义         结构差异
方法列表              设计文档的方法列表 vs 实际方法列表         增减差异
参数/返回值           设计文档的参数描述 vs 实际参数类型         类型差异
流程/状态机           设计文档的流程图 vs 实际控制流             逻辑差异
错误码/异常           设计文档的错误定义 vs 实际错误处理         异常差异
Feature Flag          设计文档的开关规划 vs 实际 flag 定义       配置差异
多语言绑定范围        设计文档的绑定要求 vs 实际绑定覆盖         范围差异
模块划分              设计文档的模块边界 vs 实际文件组织         架构差异
```

**执行方式**：对设计文档中描述的每个接口/类/方法，使用 Grep + Read 在实际代码中
查找对应实现，逐项对比。

将所有差异收集为列表，准备进入用户决策环节。

#### Step 5.2: 逐一向用户展示差异并请求决策

对每个差异点，使用 AskUserQuestion 工具向用户展示并请求决策。
**每次仅展示一个差异点**，等待用户明确回复后再处理下一个。

**展示格式**：

```
差异 {N}/{Total}: {差异标题}

设计文档描述：
  {设计文档中的原始描述，包含章节引用}

实际实现：
  {代码中实际的实现情况}

差异分析：
  {简要说明差异的原因和影响}

请选择处理方式：
  A) 接受实现 — 将设计文档修改为与实现一致（回写设计文档）
  B) 要求重做 — 按设计文档的要求重新实现代码（启动 coder+reviewer）
  C) 暂时搁置 — 记录为遗留事项，后续处理
```

**用户决策选项说明**：

| 选项 | 含义 | 后续操作 |
|------|------|---------|
| A) 接受实现 | 实现合理，设计文档需要更新 | 直接 Edit 设计文档原始章节 |
| B) 要求重做 | 实现偏离设计意图，需修正代码 | 启动 coder → reviewer 循环 |
| C) 暂时搁置 | 无法立即决策，后续处理 | 记录到遗留事项列表 |

#### Step 5.3: 根据用户决策分类处理

收集所有差异点的用户决策，按处理方式分组：

```
决策 A（接受实现）的差异数量: {a_count}
决策 B（要求重做）的差异数量: {b_count}
决策 C（暂时搁置）的差异数量: {c_count}
```

#### Step 5.4: 执行用户决策

##### 对决策 A（接受实现）的差异：直接回写设计文档

**关键原则：直接修改设计文档的原始章节，而不是在末尾追加说明。**

对每个决策 A 的差异：

1. 使用 Read 定位设计文档中对应的原始章节
2. 使用 Edit **就地修改**原始描述，使其与实际实现一致
3. **不在末尾追加汇总章节**，仅在修改处标注修改来源

**修改原则**：
- 仅修改与实现不一致的段落/章节，不改动文档整体结构
- 保持原文档的写作风格和术语
- 使用 Edit 精确替换，不覆盖整个文档
- 每处修改通过行内注释标注变更来源和原因

**修改示例**：

```
原设计文档（3.1 节）：

**不追加末尾总结章节**——所有修改直接体现在原始章节中。

##### 对决策 B（要求重做）的差异：启动 coder+reviewer 重做循环

将所有决策 B 的差异整合为重做需求，传递给 arkweb-coder Agent：

```
请根据以下用户决策，重新实现代码以对齐设计文档。

需求设计文档路径：{用户提供的文档路径}
检视报告路径：{检视报告路径}

用户要求重做的差异点：

差异 1: {差异标题}
  设计文档要求：{设计文档的原始描述}
  当前实现：{当前代码的实现}
  需要修改为：{与设计文档一致}

差异 2: ...

请按以下步骤执行：
1. 读取需求设计文档中对应的章节
2. 使用 TodoWrite 创建修复任务列表
3. 逐个修改代码文件以对齐设计文档
4. 修改完成后输出变更文件清单
```

重做完成后，启动 arkweb-reviewer Agent 仅检视重做涉及的文件：

```
请仅检视以下重做涉及的文件，确认代码已正确对齐设计文档。

需求设计文档路径：{用户提供的文档路径}
重做的文件：{重做变更的文件列表}
检视报告输出路径：{检视报告路径}

重点关注：
1. 用户指出的差异是否已修正
2. 修正是否引入了新问题
3. 代码是否与设计文档一致
```

如果检视仍有 BLOCKER/CRITICAL 问题，按 Phase 4 的修复循环逻辑继续
（最多 3 轮）。

##### 对决策 C（暂时搁置）的差异：记录到遗留事项

不修改设计文档，不修改代码。仅在最终总结中列出。

#### Step 5.5: 差异对齐循环检查

```
如果有决策 B 的差异触发了重做：
    → 重新执行 Step 5.1（重新收集信息并比对）
    → 检查重做是否引入了新的差异
    → 如果有新差异 → 回到 Step 5.2（向用户展示新差异）
    → 如果无新差异 → 退出循环

如果无决策 B 的差异：
    → 直接退出循环，所有差异已处理完毕
```

**循环保护**：
```
max_diff_rounds = 5
如果差异对齐循环超过 5 轮：
    → 向用户报告仍有未对齐的差异
    → 列出剩余差异
    → 建议人工介入
```

#### Step 5.6: 差异处理总结

完成所有差异处理后，向用户输出总结：

```
═══════════════════════════════════════════
  Phase 5: 设计差异对齐完成
═══════════════════════════════════════════
需求文档: {原始需求文档路径}

本轮差异统计:
  总差异点: {N}

用户决策分布:
  接受实现（已回写设计文档）: {A_count} 处
  要求重做（已重新实现）:     {B_count} 处
  暂时搁置（记录为遗留）:     {C_count} 处

已直接修改的设计文档章节:
  - {章节1} ({差异标题}): {修改摘要}
  - {章节2} ({差异标题}): {修改摘要}

已重新实现的代码文件:
  - {文件1}: {修改说明}
  - {文件2}: {修改说明}

遗留事项（用户选择搁置）:
  - [ ] {差异标题}: {设计要求 vs 实际实现}
═══════════════════════════════════════════
```

---

## 流程状态追踪

使用 TodoWrite 维护全局进度：

```
Phase 1:   需求分析          [pending / in_progress / completed]
Phase 2:   设计遵从性门禁    [pending / in_progress / completed / blocked]
Phase 3:   业务对齐          [pending / in_progress / completed]
Phase 4:   代码实现          [pending / in_progress / completed]
Phase 5:   代码检视          [pending / in_progress / completed]
Phase 6:   修复循环 (1~5)    [pending / in_progress / completed]
Phase 7:   设计差异对齐      [pending / in_progress / completed]
  └─ 差异决策轮次 (1~5)      [追踪当前轮次]
Phase 8:   编译-修复循环 (1~10)  [pending / in_progress / completed]
  └─ 内层检视循环 (1~3)         [追踪当前轮次]
```

## 异常处理

### Phase 1 失败（需求无法分析）
- 停止流程
- 向用户展示错误信息
- 建议检查需求文档格式和内容

### Phase 1.5 阻断（设计遵从性检查未通过）
- 停止流程，不进入 Phase 2
- 向用户输出偏离详情（设计文档要求 vs 分析报告方案）
- 提供三个选项：A) 接受偏离继续 B) 退回重新分析 C) 逐项决定
- 等待用户确认后继续或退回

### Phase 1.5 退回（用户选择重新分析）
- 将偏离详情作为反馈传递给 requirements-analysis Agent
- 重新执行 Phase 1，在指令中明确要求修正偏离项
- 重新执行 Phase 1.5 验证

### Phase 2 部分失败（某些 Step 无法实现）
- 记录失败的 Step
- 继续执行后续可完成的 Step
- 在 Phase 4 检视时标注未完成的步骤
- 设计差异对齐（Phase 6）处理时标注 INCOMPLETE

### Phase 4 达到最大轮次仍有问题
- 停止修复循环
- 向用户报告剩余的 BLOCKER/CRITICAL 问题
- 建议人工介入处理
- Phase 5（设计差异对齐）正常执行，标注 PASS_WITH_ISSUES

### Phase 5 差异对齐循环超过最大轮次
- 停止差异对齐循环
- 向用户报告仍有未对齐的差异
- 列出剩余差异及建议处理方式
- 保留已完成的差异处理结果

### Agent 执行超时或无响应
- 记录当前进度
- 向用户报告已完成的阶段和当前卡住的位置
- 保留已生成的中间文件（分析报告、检视报告）

---

## 代码生成规范

以下规范在 Phase 2 调度 `arkweb-coder` Agent 时，**必须作为强制指令传递**。

### 命名规范

```
类名：     PascalCase       例：WebGPUContext
方法名：   camelCase        例：initializeContext
成员变量： m_ 前缀           例：m_contextId
常量：     k 前缀           例：kMaxTextureSize
文件名：   snake_case       例：webgpu_context.h
命名空间： OHOS::ArkWeb::*  例：OHOS::ArkWeb::WebGPU
```

### 代码结构（每个 C++ 文件）

```cpp
// Copyright (c) 2026 Huawei Device Co., Ltd.
// Licensed under the Apache License, Version 2.0

#ifndef {GUARD_NAME}
#define {GUARD_NAME}

#include <memory>
// ... 依赖头文件

namespace OHOS::ArkWeb::{Module} {

class {ClassName} : public {BaseClass} {
public:
    {ClassName}();
    ~{ClassName}() override;

    // 接口方法（来自设计文档）
    int32_t Initialize(const {Config}& config) override;
    void Destroy() override;

private:
    // 成员变量
    std::unique_ptr<{Impl}> impl_;
};

} // namespace OHOS::ArkWeb::{Module}

#endif // {GUARD_NAME}
```

### 关键约束（coder Agent 必须遵守）

1. **版权头** — 每个源文件必须包含 Apache 2.0 版权头
2. **namespace** — 必须使用 `OHOS::ArkWeb::*` 命名空间包裹
3. **RAII** — 必须遵循资源获取即初始化原则
4. **裸指针** — 禁止裸指针传递所有权，使用 `std::unique_ptr` / `std::shared_ptr`
5. **错误码** — 使用 `int32_t` 返回错误码（ArkWeb 约定，0 表示成功）
6. **日志** — 使用 `WEBGPU_LOGI/LOGE/LOGW` 或对应的模块日志宏
7. **设计文档优先** — 所有接口、类名、参数必须与 requirement.md 一致
8. **最小修改** — 能新增文件解决的，不修改已有文件

### 单元测试规范

**覆盖要求：**
- 正常路径（Happy Path）：至少 2 个用例
- 边界条件：空输入、最大值、零值
- 错误路径：无效参数、资源不足
- 设备差异：不同设备类型的行为差异（如适用）

**测试结构：**
```cpp
// Copyright (c) 2026 Huawei Device Co., Ltd.

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "{header_path}"

using namespace testing;
using namespace OHOS::ArkWeb::{Module};

class {ClassName}Test : public testing::Test {
protected:
    void SetUp() override { /* 初始化 */ }
    void TearDown() override { /* 清理 */ }
};

// 正常路径
TEST_F({ClassName}Test, InitializeSuccess) {
    // Arrange
    {ClassName} obj;
    {Config} config = {.width = 1024, .height = 768};
    // Act
    int32_t result = obj.Initialize(config);
    // Assert
    EXPECT_EQ(result, 0);
}

// 边界条件
TEST_F({ClassName}Test, InitializeWithZeroSize) { /* ... */ }

// 错误路径
TEST_F({ClassName}Test, InitializeWithNullConfig) { /* ... */ }
```

### BUILD.gn 规范

新增源文件时按以下格式修改 BUILD.gn：

```gn
import("//build/ohos.gni")

ohos_shared_library("{module_name}") {
  sources = [
    "{new_source}.cpp",
    # ... 新增文件
  ]

  include_dirs = [
    "//foundation/arkui/ace_engine/interfaces",
    "//base/web/webview/interfaces",
  ]

  deps = [
    "//third_party/googletest:gtest_main",
  ]

  external_deps = [
    "c_utils:utils",
    "hilog:libhilog",
  ]
}
```

### 自验证清单（coder Agent 完成编码后必须执行）

1. **命名一致性** — 类名与文件名对应、方法名与设计文档一致、命名空间正确
2. **接口完整性** — 设计文档中所有接口都已实现、参数类型和返回值与设计文档一致
3. **测试覆盖** — 每个公共方法至少 1 个测试、包含正常 + 边界 + 错误路径
4. **规范检查** — 版权头完整、namespace 包裹、无裸指针所有权传递、日志使用正确宏
5. **头文件包含** — 所有 `#include` 正确，无遗漏、无冗余

### 代码生成原则

1. **设计文档是唯一真理** — 所有接口、类名、参数必须与 requirement.md 一致
2. **最小修改** — 能新增不修改，能改小不改大
3. **先计划后编码** — 先列文件清单，再逐个生成
4. **测试先行** — 每个公共接口必须有测试
5. **自验证闭环** — 生成后必须自检，不通过要自动修复
6. **遵循现有规范** — 读取 analysis.md 中的命名和结构规范，不另起炉灶

---

## 使用示例

### 示例 1: 完整流程（含差异交互）
```
用户: 实现需求 /path/to/requirement_design.md

助手: 好的，我将启动需求实现全流程。
      需求文档: /path/to/requirement_design.md
      分析报告: {DOCS_REPO}/tmp/arkweb_requirements_analysis.md
      检视报告: {DOCS_REPO}/tmp/arkweb_review_report.md

      Phase 1: 启动需求分析...
      → [requirements-analysis Agent 执行]
      → 分析完成：8 个功能点，12 个实现步骤

      Phase 2: 设计遵从性门禁...
      → 比对设计文档与分析报告
      → 3 项一致，0 项偏离 → 检查通过

      Phase 2: 启动代码实现...
      → [arkweb-coder Agent 执行]
      → 实现完成：12/12 Step 已完成，变更 18 个文件

      Phase 3: 启动代码检视...
      → [arkweb-reviewer Agent 执行]
      → 检视完成：2 CRITICAL，5 MAJOR，3 MINOR

      Phase 4: 修复循环 (Round 1/5)...
      → [arkweb-coder 执行修复]
      → [arkweb-reviewer 再次检视]
      → Round 1 完成：0 BLOCKER，0 CRITICAL → 检视通过

      Phase 5: 设计差异对齐（交互式）...

      → 比对设计文档与实际实现，发现 3 处差异

      差异 1/3: 接口方法签名扩展

### 示例 1.5: 设计遵从性门禁拦截
```
助手: Phase 2: 设计遵从性门禁...
      → 比对设计文档与分析报告

      ⚠ Phase 1.5: 设计遵从性检查未通过

      偏离 1: 技术路径偏离
      设计文档要求：使用 C++ DOM API (SetValueForUser)
      分析报告方案：使用 JS 注入 (ExecuteJavaScript)

      偏离 2: 实现范围缺失
      设计文档要求：修改 arkui_ace_engine 入口层参数校验
      分析报告方案：未涉及 ACE Engine 层修改

      偏离 3: 错误码体系未对齐
      设计文档要求：定义 -1 至 -10 的专项错误码
      分析报告方案：复用已有错误码 102/131/132/133

      请确认：
      A) 接受偏离，按分析报告方案继续
      B) 拒绝偏离，退回 Phase 1 重新分析
      C) 逐项决定（告知每项选择）

用户: B

助手: 退回 Phase 1 重新分析，将偏离详情作为反馈...
      → Phase 1 重新执行（已指示修正 3 项偏离）
      → Phase 1.5 重新检查 → 检查通过
      → 继续 Phase 2...
```

### 示例 2: 指定文档和自定义输出路径
```
用户: 按照设计文档 docs/snapshot_api_design.md 实现功能，
      分析报告输出到 {DOCS_REPO}/tmp/snapshot_analysis.md

助手: 好的，启动需求实现全流程。
      需求文档: docs/snapshot_api_design.md
      分析报告: {DOCS_REPO}/tmp/snapshot_analysis.md
      ...（同上流程）
```

### 示例 3: 达到最大修复轮次
```
助手: Phase 4: 修复循环 (Round 5/5)...
      → [arkweb-coder 执行修复]
      → [arkweb-reviewer 再次检视]
      → Round 5 完成：仍有 1 CRITICAL 问题

      ⚠️ 已达到最大修复轮次(5轮)，以下问题尚未解决：
      - Issue 3: [CRITICAL] nweb_snapshot_impl.cc:87 异步回调中
        使用 shared_ptr 可能导致循环引用

      建议人工介入处理此问题。
      Phase 5 将正常执行，状态标注为 PASS_WITH_ISSUES。
```

### Phase 8 超限（编译验证达到最大轮次）
- 报告最后一轮编译错误摘要
- 建议人工介入
- 保留已生成的所有中间文件

### Phase 8 内层超限（coder 修复轮次耗尽）
- 直接进入下一轮编译
- 让编译器验证当前代码状态

