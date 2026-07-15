---
name: ohos-req-feature-to-ir
description: Use when an OHOS Feature has completed the Phase 0 Review Ready Gate and an Initial Requirement baseline is needed before proposal creation or cross-repository requirement splitting. Activation keywords: "IR.md baseline", "AC reference inheritance", "rr_id", "extension dimension confirmation". Do NOT use for requirement intake (ohos-req-requirement-intake), feasibility analysis (ohos-req-feasibility-analysis), or SR generation (ohos-req-proposal-to-sr).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: feature-to-ir
  version: 0.2.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS Feature 转 IR

**Announce at start:** "我正在使用 ohos-req-feature-to-ir skill 生成 IR.md。"

## 定位

IR 是 Phase 0 的正式出口。一个 Feature 只生成一个平台级 `IR.md`，随后按仓库或独立交付单元拆成一个或多个 proposal。

## 适用边界

- ✅ 适用：Phase 0 Step 0.5 Gate 通过后生成平台级 IR.md
- ✅ 适用：Feature Gate 为 Ready 或 Conditional Ready 时生成 IR（Conditional Ready 时条件项写入 IR 并标注 status=Conditional）
- ❌ 不适用：需求导入（ohos-req-requirement-intake）、可行性分析（ohos-req-feasibility-analysis）、SR 生成（ohos-req-proposal-to-sr）
- ❌ 不适用：Feature 评审就绪检查（ohos-req-review-gate）、Feature 基线生成（ohos-req-feature-baseline）

## 输入与前置

- `01-requirement.md`
- `02-feasibility.md`
- `03-arch-decision-record.md`
- `04-feature.md`
- Feature Gate 必须是 `Ready` 或 `Conditional Ready`

仅在 Gate=Not Ready 时拒绝生成。Gate=Conditional Ready 时允许生成，但必须把条件项（conditions）、Owner、关闭动作和关闭时点写入 IR，生成 `status: Conditional` 的 IR。`Conditional Ready` 不是失败状态，不得误判为拒绝。

IR.md 引用 01-04 的结论而非重复内容，AC 直接引用 04-feature.md 的编号，不重新编号。

## 引用式而非重复

IR.md 的 AC 清单直接引用 04-feature.md 的 AC 编号（如 AC-01~AC-10），不重新编号或重复描述。

## 模板说明

- 模板路径：`reference/IR.md`
- 模板与 sdd-pilot IR.md 完全一致：13节扁平结构 + HTML注释占位，skill 生成时按需填充各章节内容
- 流程规则（扩展维度确认交互、AC引用规则、评估8项填写要求、Proposal拆解等）由本 skill 控制

## Before generating IR, ask yourself...

- Before writing an AC reference, ask: am I re-numbering or referencing 04-feature.md's original numbers?
- Before inheriting rr_id, ask: did I copy it exactly from 04-feature.md frontmatter, including format?
- Before marking status, ask: is the Gate Ready (→ Baseline) or Conditional Ready (→ Conditional with conditions written to IR)?
- Before confirming extension dimensions, ask: am I pausing for user confirmation on all 6 dimensions, or skipping/synthesizing answers?
- Before filling metrics, ask: do I have a reliable baseline for this number, or should I mark "待采集"/"暂不设指标"?
- Before splitting proposals, ask: am I keeping cross-repo dependencies in one IR appendix, not duplicating IR per repo?

## 流程

1. 读取 `reference/IR.md` 和 01-04。
2. 从 `04-feature.md` frontmatter 继承 `rr_id` 到 IR.md frontmatter，并填写 §0 需求追踪表（RR单号、Feature ID、IR ID）。
3. §1 需求价值：从 Feature 提取核心需求、范围和非目标。
4. §2 详细描述：从 Feature 提取场景分析（场景编号、触发条件、用户操作、预期结果、当前问题）。
5. §3 验收目标：AC 直接引用 04-feature.md 的编号，不重新编号。
6. §4 验收平台：明确 OS版本/设备/API Level。
7. §5-§13 平台级评估各项：适用产品差异/OS规格/性能功耗/UX/资料变更/API/依赖子系统/Sample。
8. **⭐ 扩展维度确认（安全与权限/性能与功耗/兼容性/API/IPC/构建组件）生成后，必须暂停并向用户逐条确认**。操作步骤：
   - 向用户逐条呈现 6 个维度，每维度呈现格式：`维度: 是否涉及? 依据: [当前分析]`
   - 6 个维度依次为：① 安全与权限 ② 性能与功耗 ③ 兼容性 ④ API ⑤ IPC ⑥ 构建组件
   - 用户回答后，将确认结果回填到 IR.md 对应章节（§8-§13）
   - L1+ 需逐维度确认（每维度独立呈现、独立回答）；L0 可简化为批量确认（一次性呈现全部 6 个维度）
   - 以用户判断为准，AI 不代行决策
9. Proposal拆解和跨仓依赖作为附件或 IR 末尾补充章节，不按仓复制多份 IR。
10. 对没有可靠基线的指标标记"待采集"或"暂不设指标"，禁止补造数值。
11. 保存到 `{docs_dir}/IR.md`。

## 输出要求

- `status`：`Baseline` 或 `Conditional`
- §1 需求价值明确核心需求和范围、非目标
- §2 场景分析覆盖核心用户场景
- §3 每条 AC 可观察、可验证，引用 04-feature AC 编号
- §4 验收平台明确 OS 版本/设备形态/API Level
- §5-§13 各项全部填写
- Proposal拆解和跨仓依赖作为附件或补充章节
- 扩展维度确认已与用户逐条确认（L1+ 逐维度，L0 可简化）

## 自检

- [ ] Feature Gate 满足前置条件（Ready 或 Conditional Ready；Conditional Ready 时条件项已写入 IR 并标注 status=Conditional）
- [ ] RR单号已从 04-feature.md 继承（frontmatter `rr_id` + §0 需求追踪表）
- [ ] 一个 Feature 只生成一个 IR
- [ ] §1 核心需求和范围、非目标已明确
- [ ] §2 场景分析覆盖核心用户场景
- [ ] §3 P0/P1 AC 全部进入验收基线，引用 feature AC 编号
- [ ] §4 验收平台已明确（OS版本/设备/API Level）
- [ ] §5-§13 各项已填写
- [ ] Proposal拆解没有丢失跨仓依赖
- [ ] 扩展维度确认已与用户确认
- [ ] 所有生成内容有来源或明确未知状态

## NEVER

- **NEVER 重新编号 AC**：必须引用 04-feature.md 的 AC 编号（如 AC-01~AC-10），不重新编号或重复描述
- **NEVER 在 IR 中包含 proposal 级别的设计细节**：IR 是平台级需求基线，不包含单个 proposal 的设计级细节（接口签名、类设计等）
- **NEVER 虚构指标数值**：无可靠基线时标注"待采集"或"暂不设指标"，禁止编造性能/功耗等量化数值
- **NEVER 按仓生成多份 IR**：一个 Feature 只生成一个平台级 IR，跨仓需求拆分在 proposal 层完成

## 输出

- 路径：`{docs_dir}/IR.md`
- 回传：IR ID、RR单号、状态、AC 数量、proposal 数量和条件项
