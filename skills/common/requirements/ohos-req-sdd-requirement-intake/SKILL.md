---
name: ohos-req-sdd-requirement-intake
description: Use when importing an OHOS requirement into Phase 0.1, especially for 01-requirement.md, requirement intake, background, user value, scenarios, scope, FR/NFR, affected modules, or priority.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: sdd
  capability: requirement-intake
  version: 0.1.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS 需求导入

**Announce at start:** "我正在使用 ohos-requirement skill 生成 01-requirement.md。"

## 定位

`01-requirement.md` 是需求事实输入，不是技术方案或可行性报告。它回答谁提出、为何提出、谁受益、需要什么、适用于哪里以及优先级是什么。

不得在本阶段选择技术方案、估算 ROI、下可行性结论或补造指标。

## ⭐ 硬规则：禁止不确定项输出

`01-requirement.md` 是 feasibility 的唯一事实输入，任何不确定项都会向后传播并放大。

**禁止出现以下任何占位符或模糊表述：**

| 禁止项 | 说明 |
|--------|------|
| "待确认" | 必须在澄清环节关闭 |
| "待分析" | 必须在澄清环节确认或排除 |
| "待采集" | 必须在澄清环节明确采集方案和 Owner |
| "暂不设指标" | 必须在澄清环节决定：设指标还是确认不设（附理由） |
| " TBD / TODO / FIXME " | 任何形式的占位符 |
| 模糊表述 | "快速""稳定""尽可能""优化""提升"等无量化锚点的描述 |

**生成 requirement.md 时，所有字段必须填写已确认事实。如果某项事实缺失，不得写入占位符，而是在澄清环节向用户提问获取答案。**

唯一例外：用户明确说"这个我不确定，先放一下"时，可标记为 `⚠️ 用户暂缓:{用户原话}`，但必须在回传摘要中单独列出，并计入未关闭澄清项。

## 输入

- 用户原始描述、Issue、PRD、会议纪要或用户反馈
- 已确认的范围、版本、约束和指标口径

## 流程（两阶段：草稿 → 澄清 → 定稿）

### 第一阶段：草稿生成

1. 读取 `reference/requirement.md`。
2. 保留需求方原意，将内容归入模板对应章节。
3. **模板保真：必须沿用模板中的 frontmatter、H1、H2 标题，参考模板的表格结构；不得新增模板外的 H1/H2 章节。**
4. `必须包含` 中的 FR/NFR、受影响模块、优先级等信息，只能归入模板已有章节：
   - 功能点、用户场景、价值 → `## 4. 期望`
   - 产品、地区、设备、开发者范围 → `## 5. 适用设备/产品形态`
   - NFR、约束、版本、性能/功耗 → `## 6. 约束与期望`
   - 证据、来源、受影响仓/路径 → `## 9. 附件与证据`
   - 缺失事实和澄清项 → `{docs_dir}/_draft/clarification-questions.md`
5. 对缺失事实，**不写入占位符**，而是记录到「待澄清问题清单」。
6. 检查功能点与 FR、场景与价值、NFR 与量化口径之间是否可追溯。
7. 输出草稿到 `{docs_dir}/01-requirement.md`（frontmatter `status: Draft-NeedsClarification`）。
8. 同时输出澄清问题清单到 `{docs_dir}/_draft/clarification-questions.md`。

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
3. 用户回答后，更新 requirement.md 对应章节（替换为确认事实）
4. **每轮澄清后立即回填结论到 `clarification-questions.md`**：在对应问题下方追加 `**澄清结论**` 段，标注 ✅（已关闭）或 ⚠️（条件待验证/P2延后），附结论摘要和影响的下游文档章节。不允许只更新 requirement.md 而不回填 clarification-questions.md。
5. 每轮澄清后检查：
   - 是否产生新的待澄清项？→ 继续下一轮
   - 是否所有字段都有确认事实？→ 进入定稿检查
6. 澄清完成后执行定稿检查：

**定稿检查清单（全部 ✅ 才可进入 feasibility）：**

- [ ] 每个章节所有字段有确认事实，无占位符
- [ ] 所有 FR 有来源依据
- [ ] 所有 NFR 有量化口径（"提升XX%"不算量化，必须有基线和目标值）
- [ ] 优先级(P0/P1/P2)每项有判定依据
- [ ] 受影响模块有具体仓/路径（不是"待确定"）
- [ ] 用户痛点有影响描述和严重程度（不是笼统"体验差"）
- [ ] 无模糊表述（"快速""稳定""尽可能"等）

**任何一项不通过 → 继续澄清，不允许进入 feasibility。**

6. 定稿检查全部通过后，更新 frontmatter `status: Clarified`，输出最终版。

### 澄清状态检测（输入材料已有澄清结论时）

当用户提供的输入材料已包含澄清结论时（如标记为"已完成 P0 澄清"或包含 Q-1~Q-N 全部 ✅ 结论），skill 应：

1. 检测输入材料中的澄清状态标记或澄清结论覆盖度
2. 若已澄清完成且覆盖所有必填字段，只做格式归一化和定稿检查
3. 若定稿检查通过，直接输出 `status: Clarified`，跳过逐轮对话
4. 若定稿检查不通过（仍有不确定项），仍需逐轮澄清
5. 在回传摘要中标注"澄清状态: 已完成/需补充/无标记"

## 必须包含

- 需求方、提出时间、来源、触发场景、现状和问题
- 用户痛点（有影响描述和严重程度）
- 功能点、用户场景、价值和可量化目标（有基线和目标值）
- 产品、地区、设备、开发者范围和期望版本
- FR（有来源依据）、NFR（有量化口径）、受影响模块（有仓/路径）
- 约束、优先级（有判定依据）和证据

## 禁止包含

- 候选方案和推荐方案
- 技术架构、接口设计和代码路径
- 无依据的精确成本、ROI、性能或成功率
- 可行/不可行或批准/拒绝结论
- 任何占位符或模糊表述（"待确认""待分析""TBD""尽可能"等）

## 输出

- 路径：`{docs_dir}/01-requirement.md`（`status: Clarified`）
- 澄清问题清单：`{docs_dir}/_draft/clarification-questions.md`（澄清完成后保留，每个问题必须回填 `**澄清结论**`段；仅当全部问题已回填且 status 标记为"已完成"时才可考虑删除）
- 回传：路径、需求方、目标版本、FR/NFR 数量、澄清轮次、未关闭项数量（必须为 0）
