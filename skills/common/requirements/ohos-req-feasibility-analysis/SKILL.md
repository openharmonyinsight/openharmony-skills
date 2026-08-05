---
name: ohos-req-feasibility-analysis
description: Use when evaluating an OHOS requirement in requirements Step 5, especially for 02-feasibility.md, capability gaps, candidate technical paths, compatibility, security, dependencies, effort, risk, or validation planning. Triggers: 02-feasibility.md, 可行性分析, capability gap, 候选技术路径, 兼容性分析, 工作量估算, 500行人月. Do NOT use for requirement intake (ohos-req-requirement-intake), architecture decision (ohos-req-arch-decision), or feature baseline (ohos-req-feature-proposal-baseline).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: feasibility-analysis
  version: 0.4.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS 可行性分析

**Announce at start:** "我正在使用 ohos-req-feasibility-analysis skill 生成 02-feasibility.md。"

## 定位

OHOS 代码证据包（kb_precheck_path）是 feasibility 的独立于用户设计方案的源码级验证——PIR #13 已证明"基于 PRD+竞品就做决策"会导致 ADR 被源码复核后推翻。feasibility 禁止选型推荐，选型决策 exclusively 属于 03-arch-decision-record.md，由用户提供。工作量估算标准固定为 500 行≈1 人月，跨所有 OHOS 领域统一。

## 输入

- `{docs_dir}/01-requirement.md`
- `{docs_dir}/_draft/feasibility-inputs.md`（Step 3 用户提供或确认不提供的本地关键代码仓路径、接口文档和前置依赖资料记录）
- 代码证据包：`{kb_precheck_path}`（由 `ohos-req-intake-orchestration` Step 4 轻量代码预检产出；未产出时按本 skill Fallback 规则降级）
- 可用的源码、架构文档、Owner 结论、竞品或 PoC 证据

## 前置输入契约

启动提醒、建议补充资料清单推导和用户确认动作由 `ohos-req-intake-orchestration` Step 3 统一定义和执行（参见 ohos-req-intake-orchestration SKILL.md），本 skill 不重复维护规则。

生成 `02-feasibility.md` 前必须满足：
- `{docs_dir}/_draft/feasibility-inputs.md` 已存在。
- 文件中记录了用户提供资料，或用户明确确认不额外提供本地关键代码仓/接口文档/Owner 结论/前置依赖资料。
- 如用户确认不额外提供或资料不可访问，`02-feasibility.md` 必须按证据受限口径标注，不得写成源码已验证或接口已确认。

## 自省提示（Mindset Prompts）

在执行关键步骤前，自问以下问题：

- **Before estimating effort, ask yourself:** 我是否已为每个候选方案独立估算工作量，还是只给了一个总量？
- **Before marking evidence as '待Phase2验证', ask yourself:** 我是否真的尝试过用 Read 工具查找证据，还是过早放弃了？
- **Before writing a GAP analysis, ask yourself:** 我是否包含了接口签名和调用链路，还是只列了 file:line 引用？

## 流程（两阶段：草稿 → 澄清 → 定稿）

### 第一阶段：草稿生成

1. 读取 `reference/feasibility.md` 和需求事实。
2. 读取 `{docs_dir}/_draft/feasibility-inputs.md`，确认用户已提供资料或明确确认不提供额外资料。
3. 确认评估范围与产品范围、FR/NFR 一致。
4. **候选路径分析**（含代码证据、子能力、可视化、估算四个子步骤）：
   - **4a 代码证据分析**：读取 `{kb_precheck_path}` 和用户提供的本地关键代码仓路径/文档/Owner 结论，提取关键接口、类、调用链，为候选路径提供代码级证据，将关键代码仓库分析写入 §2 技术可行性下的 §2.1「关键代码仓库分析」表（模板外补充子节：仓库/模块/路径/关键接口/影响类型/证据来源），供 `ohos-req-feature-proposal-baseline` §4 模块覆盖完整性校验引用。证据包和用户资料均未覆盖的接口/路径标记"证据受限，待 Phase 2 代码分析验证"，不得虚构。
   - **4b 子能力拆分**：识别是否存在多个可独立交付、独立验证或依赖不同系统能力的子能力；若存在，必须先按子能力分别评估价值、现有能力差距、候选路径、兼容性、安全、性能和依赖，再给出组合路径判断。不得只用一个整体方案掩盖子能力差异。
   - **4c 可视化方案图**：为每个候选路径绘制：
     - 流程图（Mermaid flowchart）：展示数据流转路径和模块交互顺序
     - 类图（Mermaid classDiagram）：展示新增/扩展的关键类及接口签名
     - 时序图（Mermaid sequenceDiagram）：展示跨进程/跨模块的 IPC 调用链路
   - **4d 工作量估算**：按统一评估标准折算端到端工作量，**每个候选方案必须独立给出工作量估算**，不允许只给单一总量：
     - 开发工作量：500 行代码 ≈ 1 人月（★ 本 skill 统一估算标准，后续章节引用此处）
     - 测试工作量：开发 × 0.3
     - 设计工作量：开发 × 0.1
     - UX 工作量（仅涉及 UX 时额外追加）：开发 × 0.1
     - 端到端合计 = 开发 + 测试 + 设计 + UX（如有）
     - **必须输出"各方案工作量对比汇总"表**，供 03-arch-decision-record.md 方案对比使用
5. 为风险和未知项指定验证动作、Owner、关闭时点和阻塞性。
6. 给出每个方案的可行、有条件可行、待证据或不可行判断（见强制规则"禁止选型推荐"）。
7. 不生成 ROI 章节（详见 NEVER §禁止生成ROI）。
8. 输出草稿到 `{docs_dir}/02-feasibility.md`（frontmatter `status: Draft-NeedsClarification`）。
9. 同时输出澄清问题清单到 `{docs_dir}/_draft/feasibility-clarification-questions.md`。

### 第二阶段：逐轮人工澄清 ⭐ 强制门禁

**草稿生成后，必须暂停并进入逐轮澄清对话。不允许直接进入 decision。**

澄清规则：

1. 主 Session 将「待澄清问题清单」逐条向用户提问
2. 每轮提问 ≤5 个问题（按对决策影响优先级排序）
3. **批量确认已知答案**：对需求文档或设计方案中已有明确答案的问题，一次性呈现全部已知答案让用户**批量确认**（✅确认/✏️修正），不逐条单独交互。仅真正不确定的问题才逐条澄清。
4. 用户回答后，更新 feasibility.md 对应章节（替换为确认事实）
5. 每轮澄清后检查：
   - 是否产生新的待澄清项？→ 继续下一轮
   - 是否所有字段都有确认事实？→ 进入定稿检查
6. 澄清完成后执行定稿检查：

**定稿检查清单（全部 ✅ 才可进入 decision）：**

- [ ] 目标与范围边界已明确
- [ ] feasibility-inputs.md 已存在且用户已确认（提供资料或明确不提供）
- [ ] 证据受限项已显式标注（不得写成源码已验证或接口已确认）
- [ ] 多子能力时按子能力分别分析候选路径、工作量、风险和可行性
- [ ] **代码分析分支判定**（二选一，满足其一即可）：
  - **源码级场景**（代码仓可访问或预检证据包已覆盖）：代码分析已完成（关键模块、接口、依赖已检索），技术可行性基于实际代码评估
  - **证据受限场景**（用户确认不额外提供资料或代码仓不可访问）：① 证据免责声明已在文档中显式标注（"证据受限，待 Phase 2 验证"）；② 未验证接口/路径清单完整（逐条列出）；③ 每条未验证项有 Owner、验证动作和 Phase 2 关闭时点；满足后允许以条件状态（`status: Conditional`）完成，不得标记为源码已验证
- [ ] 竞品参考有具体做法和可借鉴点，且每条竞品有来源链接（无链接视为不可信）
- [ ] 工作量估算有代码行数依据（见 Step 4d 估算标准），且每个方案独立估算
- [ ] 各方案工作量对比汇总表完整
- [ ] 收益量化优先
- [ ] 风险矩阵覆盖关键风险
- [ ] 结论与数据一致
- [ ] 无 ROI 章节（详见 NEVER §禁止生成ROI）
- [ ] 未包含选型推荐内容（详见 NEVER §1）
- [ ] 结论章节为各方案可行性判断表，不含选定方案
- [ ] 不含自审清单（详见 NEVER §禁止自审清单写入文档）

**任何一项不通过 → 继续澄清，不允许进入 decision。**

7. 定稿检查全部通过后，更新 frontmatter `status: Clarified`，输出最终版。

### 澄清状态检测

当用户提供的输入材料已包含澄清结论时，skill 应：
1. 检测输入材料中的澄清状态标记或澄清结论覆盖度
2. 若已澄清完成且覆盖所有必填字段，只做格式归一化和定稿检查
3. 若定稿检查通过，直接输出 `status: Clarified`，跳过逐轮对话
4. 在回传摘要中标注"澄清状态: 已完成/需补充/无标记"

## 强制规则

> **加载策略（Progressive Disclosure）**：本节保留 5 条顶层不变式（核心红线，始终生效）。生成 `02-feasibility.md` §2-§6 各章节时的详细判定口径（证据约束/单方案降级/锚点链接/竞品链接/Mermaid/GAP/工作量标准等 11 类细则）见 [`reference/feasibility-rules.md`](reference/feasibility-rules.md)，**在第一阶草稿生成步骤按需加载**。

**顶层不变式（始终生效，违反即阻断）：**

1. **证据为本**：技术判断必须有源码、文档、PoC 或 Owner 证据，否则标记待验证；代码事实验证优先用 `{kb_precheck_path}` 证据包，未覆盖标记"待 Phase 2 验证"，Read 不可用降级为 `warn` 不硬 fail（详见 reference §1）。
2. **启动前软前置确认**：必须存在 `{docs_dir}/_draft/feasibility-inputs.md` 且记录用户资料或明确不提供，未完成不得生成 `02-feasibility.md`（详见 reference §2）。
3. **禁止选型推荐**：不允许"推荐/最优/建议选择"等决策倾向性表述，只给可行性判断（✅/⚠️/❌），选型决策属 03-arch-decision-record.md（详见 NEVER §1）。
4. **按方案独立估算工作量**：每个候选方案独立给代码行数+人月折算，必须输出"各方案工作量对比汇总"表，统一标准 500行≈1人月（详见 reference §6）。
5. **多子能力分开分析**：多个独立子能力时按子能力分别输出候选路径/依赖/工作量/风险/可行性，工作量表和风险表带子能力归属（详见 reference §7）。

> 以下细则按章节加载 `reference/feasibility-rules.md` 对应小节：§6 结论填写约束与锚点链接(§8) · 性能/竞品链接出处(§9) · Mermaid 可视化与 GAP 接口签名(§10) · ROI/自审清单禁令(§11) · 单方案降级(§4) · 证据受限标注(§3)。

## NEVER

1. **禁止选型推荐**：feasibility 不允许出现"推荐"列、"建议选择XX方案"、"XX方案最优"等决策倾向性表述。方案选型决策 exclusively 属于 03-arch-decision-record.md，由用户提供。每个方案只给出可行性判断（✅可行/⚠️有条件可行/❌不可行）和事实依据，不做推荐排序。
2. **禁止生成 ROI 章节**：模板已去除 ROI 分析章节，只保留收益量化（原因：虚构的接口/路径在 Phase 2 代码分析阶段被证伪，导致 feasibility 结论失效需返工）
3. **禁止虚构代码证据**：证据包和用户资料未覆盖的接口/路径必须标注"证据受限，待 Phase 2 验证"（原因：电子流系统将"源码已验证"的需求直接进入分析阶段，标注不足会导致未经源码验证的需求被误判为已确认）
4. **禁止硬 fail 单方案**：客观上只有一条可行路径时允许单方案，标注 warn 并写明不可行证据（原因：禁止硬 fail 单方案避免迫使 AI 虚构垃圾方案凑数，单方案场景需标注 warn 并写明不可行证据）
5. **禁止自审清单写入文档**：自审结果输出到控制台回传摘要（原因：选型决策 exclusively 属于 03-arch-decision-record.md，由用户提供；feasibility 提前选型会跳过用户决策门禁）
6. **禁止无出处竞品引用**：无来源链接的竞品记录视为不可信证据，不得作为可行性判断依据

## 输出

- 路径：`{docs_dir}/02-feasibility.md`（`status: Clarified`）
- 澄清问题清单：`{docs_dir}/_draft/feasibility-clarification-questions.md`（澄清完成后保留，每个问题必须回填 `**澄清结论**`段）
- 回传：路径、各方案可行性判断、候选路径数量、各方案工作量（代码行数+端到端人月）、高风险项、阻塞条件、自审检查结果
