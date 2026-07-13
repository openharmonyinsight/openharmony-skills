---
name: ohos-req-sdd-feat-to-ir
description: Use when an OHOS Feature has completed the Phase 0 Review Ready Gate and an Initial Requirement baseline is needed before proposal creation or cross-repository requirement splitting.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: sdd
  capability: feat-to-ir
  version: 0.1.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS Feature 转 IR

**Announce at start:** "我正在使用 ohos-feat-to-ir skill 生成 IR.md。"

## 定位

IR 是 Phase 0 的正式出口。一个 Feature 只生成一个平台级 `IR.md`，随后按仓库或独立交付单元拆成一个或多个 proposal。

## 输入与前置

- `01-requirement.md`
- `02-feasibility.md`
- `03-decision.md`
- `04-feature.md`
- Feature Gate 必须是 `Ready` 或 `Conditional Ready`

`Not Ready` 时必须拒绝生成。`Conditional Ready` 时必须把条件项、Owner 和关闭时点写入 IR。

IR.md 引用 01-04 的结论而非重复内容，AC 直接引用 04-feature.md 的编号，不重新编号。

## 引用式而非重复

IR.md 的 AC 清单直接引用 04-feature.md 的 AC 编号（如 AC-01~AC-10），不重新编号或重复描述。

## 模板说明

- 模板路径：`reference/IR.md`
- 模板与 sdd-pilot IR.md 完全一致：13节扁平结构 + HTML注释占位，skill 生成时按需填充各章节内容
- 流程规则（扩展维度确认交互、AC引用规则、评估8项填写要求、Proposal拆解等）由本 skill 控制

## 流程

1. 读取 `reference/IR.md` 和 01-04。
2. §1 需求价值：从 Feature 提取核心需求、范围和非目标。
3. §2 详细描述：从 Feature 提取场景分析（场景编号、触发条件、用户操作、预期结果、当前问题）。
4. §3 验收目标：AC 直接引用 04-feature.md 的编号，不重新编号。
5. §4 验收平台：明确 OS版本/设备/API Level。
6. §5-§13 平台级评估各项：适用产品差异/OS规格/性能功耗/UX/资料变更/API/依赖子系统/Sample。
7. **⭐ 扩展维度确认（安全与权限/性能与功耗/兼容性/API/IPC/构建组件）生成后，必须暂停并向用户逐条确认**：将每维度的"是否涉及"和"依据"向用户呈现，以用户判断为准。L1+ 需完整填写每维度，L0 可简化为一句话。
8. Proposal拆解和跨仓依赖作为附件或 IR 末尾补充章节，不按仓复制多份 IR。
9. 对没有可靠基线的指标标记"待采集"或"暂不设指标"，禁止补造数值。
10. 保存到 `{docs_dir}/IR.md`。

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

- [ ] Feature Gate 满足前置条件
- [ ] 一个 Feature 只生成一个 IR
- [ ] §1 核心需求和范围、非目标已明确
- [ ] §2 场景分析覆盖核心用户场景
- [ ] §3 P0/P1 AC 全部进入验收基线，引用 feature AC 编号
- [ ] §4 验收平台已明确（OS版本/设备/API Level）
- [ ] §5-§13 各项已填写
- [ ] Proposal拆解没有丢失跨仓依赖
- [ ] 扩展维度确认已与用户确认
- [ ] 所有生成内容有来源或明确未知状态

## 输出

- 路径：`{docs_dir}/IR.md`
- 回传：IR ID、状态、AC 数量、proposal 数量和条件项
