---
name: ohos-req-requirement-intake
description: Use when importing an OHOS requirement into Phase 0.1, especially for 01-requirement.md, requirement intake, background, user value, scenarios, scope, FR/NFR, affected modules, or priority. Triggers: 需求导入, 01-requirement, 需求基线, RR单号. Do NOT use for feasibility analysis (ohos-req-feasibility-analysis), architecture decision (ohos-req-arch-decision), or feature baseline (ohos-req-feature-baseline).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: requirement-intake
  version: 0.3.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS 需求导入

**Announce at start:** "我正在使用 ohos-req-requirement-intake skill 生成 01-requirement.md。"

## 定位

OHOS 电子流需求管理系统的 RR单号（rr_id）是跨 Phase 0-9 的唯一追溯键，从 01-requirement.md frontmatter 继承到 IR/SR/handoff 全链路。requirement 阶段的澄清状态（Draft-NeedsClarification → Clarified）决定 feasibility 是否允许启动——电子流系统据此判定需求是否进入分析阶段。requirement 不得包含技术方案选型，确保 feasibility 的选型中立性。

## Do NOT Load

本 skill 仅在 Phase 0.1（01-requirement.md 生成）时激活。以下场景不应加载：

- 可行性分析（02-feasibility.md）→ ohos-req-feasibility-analysis
- 方案架构决策（03-arch-decision-record.md）→ ohos-req-arch-decision
- Feature 评审基线（04-feature.md）→ ohos-req-feature-baseline
- Review Ready Gate → ohos-req-review-gate
- IR 生成 → ohos-req-feature-to-ir

## ⭐ 硬规则：禁止不确定项输出

`01-requirement.md` 是 feasibility 的唯一事实输入，任何不确定项都会向后传播并放大。

**禁止出现以下任何占位符或模糊表述：**

| 禁止项 | 说明 | 原因 |
|--------|------|------|
| "待确认" | 必须在澄清环节关闭 | 占位符会传播到 feasibility 的事实输入，导致可行性分析基于假设而非事实 |
| "待分析" | 必须在澄清环节确认或排除 | feasibility 的评估范围依赖 requirement 确认的边界，待分析会导致工作量估算范围不确定 |
| "待采集" | 必须在澄清环节明确采集方案和 Owner | 无采集方案的指标在下游无法验证，电子流系统无法判定需求验收就绪 |
| "暂不设指标" | 必须在澄清环节决定：设指标还是确认不设（附理由） | 无理由的"暂不设"在 Gate 评审时无法判定是刻意决策还是遗漏 |
| " TBD / TODO / FIXME " | 任何形式的占位符 | 电子流系统将 TBD 视为未完成需求，阻断需求流转 |
| 模糊表述 | "快速""稳定""尽可能""优化""提升"等无量化锚点的描述 | feasibility 无法将模糊表述转化为可验证的技术约束，导致 AC 不可观察 |

**生成 requirement.md 时，所有字段必须填写已确认事实。如果某项事实缺失，不得写入占位符，而是在澄清环节向用户提问获取答案。**

唯一例外：用户明确说"这个我不确定，先放一下"时，可标记为 `⚠️ 用户暂缓:{用户原话}`，但必须在回传摘要中单独列出，并计入未关闭澄清项。

## ⭐ 思维准则

在 `01-requirement.md` 中写入任何字段前，自问：这是来自用户的已确认事实，还是假设？若是假设 → 写入 `clarification-questions.md`，而非正文。

Before writing a placeholder, ask yourself: 能否在输入材料（Issue/PRD/会议纪要/设计方案）中找到这个字段的答案？如果可以 → 批量确认而非逐条提问。

Before 定稿, ask yourself: 每条 NFR 是否有基线值+目标值（而非"提升XX%"）？每条 FR 是否有来源依据？RR单号是否已回填或合规标注"未立项"？

## 输入

- 用户原始描述、Issue、PRD、会议纪要或用户反馈
- 已确认的范围、版本、约束和指标口径
- RR单号（如有）：需求管理系统中的追踪编号

## 流程（两阶段：草稿 → 澄清 → 定稿）

### 第一阶段：草稿生成

1. 读取 `reference/requirement.md`。
2. 保留需求方原意，将内容归入模板对应章节。
3. **模板保真：必须沿用模板中的 frontmatter、H1、H2 标题，参考模板的表格结构；不得新增模板外的 H1/H2 章节。**
4. `必须包含字段` 表中的 FR/NFR、受影响模块、优先级等信息，只能归入模板已有章节：
   - 功能点、用户场景、价值 → `## 4. 期望`
   - 产品、地区、设备、开发者范围 → `## 5. 适用设备/产品形态`
   - NFR、约束、版本、性能/功耗 → `## 6. 约束与期望`
   - 证据、来源、受影响仓/路径 → `## 9. 附件与证据`
   - 缺失事实和澄清项 → `{docs_dir}/_draft/clarification-questions.md`
   - RR单号 -> frontmatter `rr_id` + `## 1. 来源与背景` 表格
5. 对缺失事实，**不写入占位符**，而是记录到「待澄清问题清单」。
6. 检查功能点与 FR、场景与价值、NFR 与量化口径之间是否可追溯。
7. 输出草稿到 `{docs_dir}/01-requirement.md`（frontmatter `status: Draft-NeedsClarification`）。
8. 同时输出澄清问题清单到 `{docs_dir}/_draft/clarification-questions.md`。

   澄清问题清单格式：
   - 每个问题编号 Q-1, Q-2, ...
   - 每条包含：问题描述、优先级(P0/P1/P2)
   - 澄清后在对应问题下方追加 `**澄清结论**` 段，标注 ✅(已关闭) 或 ⚠️(条件待验证)，附结论摘要

**模板保真门禁（生成后必须自检）：**

- [ ] H1 只能是 `# 原始诉求`
- [ ] H2 只能来自 `reference/requirement.md`
- [ ] 不存在 `## 功能需求`、`## 非功能需求`、`## 受影响模块` 等模板外章节
- [ ] 模板已有表格未改名（若需调整结构应修改模板而非产物）
- [ ] 缺失事实只出现在 `_draft/clarification-questions.md`，不在正文中以占位符呈现

### 第二阶段：逐轮人工澄清 ⭐ 强制门禁

**草稿生成后，必须暂停并进入逐轮澄清对话。不允许直接进入 feasibility。**

澄清规则：

1. 主 Session 将「待澄清问题清单」逐条向用户提问
2. 每轮提问 ≤5 个问题（按 P0→P1→P2 优先级排序）
3. **批量确认已知答案（PIR #152 P2）**：对输入材料（Issue/PRD/会议纪要/设计方案）中已有明确答案的问题（如 RR 单号、交付版本、提出人等），一次性呈现全部已知答案让用户**批量确认**（✅确认/✏️修正），不逐条单独交互。仅真正不确定的问题才逐条澄清。
4. 用户回答后，更新 requirement.md 对应章节（替换为确认事实）
5. **每轮澄清后立即回填结论到 `clarification-questions.md`**：在对应问题下方追加 `**澄清结论**` 段，标注 ✅（已关闭）或 ⚠️（条件待验证/P2延后），附结论摘要和影响的下游文档章节。不允许只更新 requirement.md 而不回填 clarification-questions.md。
6. 每轮澄清后检查：
   - 是否产生新的待澄清项？→ 继续下一轮
   - 是否所有字段都有确认事实？→ 进入定稿检查
7. 澄清完成后执行定稿检查：

**定稿出口门禁（全部 ✅ 才可进入 feasibility）：**

- [ ] 「必须包含字段」表中所有"定稿必填"字段均有确认事实（逐项对照表格自检）
- [ ] 正文中无任何占位符（"待确认""待分析""TBD""FIXME"等任何形式）
- [ ] 正文中无模糊表述（"快速""稳定""尽可能""优化""提升"等无量化锚点）
- [ ] RR单号已回填或合规标注"未立项"并附依据
- [ ] clarification-questions.md 所有问题已回填 `**澄清结论**`，无未关闭项
- [ ] frontmatter `status` 已更新为 `Clarified`
- [ ] 模板保真：H1/H2 仅来自模板，无模板外章节，表格结构未改名
- [ ] 功能点↔FR、场景↔价值、NFR↔量化口径 之间可追溯

**任何一项不通过 → 继续澄清，不允许进入 feasibility。**

8. 定稿检查全部通过后，更新 frontmatter `status: Clarified`，输出最终版。

### 澄清状态检测（输入材料已有澄清结论时）

当用户提供的输入材料已包含澄清结论时（如标记为"已完成 P0 澄清"或包含 Q-1~Q-N 全部 ✅ 结论），skill 应：

1. 检测输入材料中的澄清状态标记或澄清结论覆盖度
2. 若已澄清完成且覆盖所有必填字段，只做格式归一化和定稿检查
3. 若定稿检查通过，直接输出 `status: Clarified`，跳过逐轮对话
4. 若定稿检查不通过（仍有不确定项），仍需逐轮澄清
5. 在回传摘要中标注"澄清状态: 已完成/需补充/无标记"

## 必须包含字段（草稿/定稿对照）

| 字段 | 草稿必填 | 定稿必填 | 说明 |
|------|---------|---------|------|
| 需求方/提出时间/来源/触发场景/现状和问题 | ✅ | ✅ | 归入 §1 来源与背景 |
| RR单号 | ✅ | ✅ | frontmatter `rr_id` + §1 表格；无 RR单号时标注"未立项"并附依据 |
| 用户痛点 | ✅ | ✅ | 必须有影响描述和严重程度（不是笼统"体验差"） |
| 功能点/用户场景/价值 | ✅ | ✅ | 归入 §4 期望 |
| 可量化目标 | ✅ | ✅ | 必须有基线和目标值（"提升XX%"不算量化） |
| 产品/地区/设备/开发者范围/期望版本 | ✅ | ✅ | 归入 §5 适用设备/产品形态 |
| FR | ✅ | ✅ | 必须有来源依据 |
| NFR | ✅ | ✅ | 必须有量化口径（基线+目标值） |
| 受影响模块 | ✅ | ✅ | 必须有具体仓/路径（不是"待确定"） |
| 约束 | ✅ | ✅ | 归入 §6 约束与期望 |
| 优先级 | ✅ | ✅ | P0/P1/P2 每项有判定依据 |
| 证据 | ✅ | ✅ | 归入 §9 附件与证据 |

## 禁止包含

- 候选方案和推荐方案（原因：requirement 是 feasibility 的唯一事实输入，混入技术方案会污染可行性分析的选型中立性）
- 技术架构、接口设计和代码路径（原因：requirement 阶段的架构决策会在 03-arch-decision-record.md 被 feasibility 推翻，提前写入会导致文档冲突）
- 无依据的精确成本、ROI、性能或成功率（原因：requirement 阶段无源码验证能力，编造的数值会被下游 feasibility 的代码证据包证伪）
- 可行/不可行或批准/拒绝结论（原因：可行性判断属于 02-feasibility.md，批准/拒绝属于 03-arch-decision-record.md，提前下结论会跳过 Gate 门禁）
- 任何占位符或模糊表述（"待确认""待分析""TBD""尽可能"等）（原因：见上方「禁止项」表的原因列）

## 输出

- 路径：`{docs_dir}/01-requirement.md`（`status: Clarified`）
- 澄清问题清单：`{docs_dir}/_draft/clarification-questions.md`（澄清完成后保留，每个问题必须回填 `**澄清结论**`段；仅当全部问题已回填且 status 标记为"已完成"时才可考虑删除）
- 回传：路径、需求方、RR单号、目标版本、FR/NFR 数量、澄清轮次、未关闭项数量（必须为 0）
