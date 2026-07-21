---
name: ohos-req-proposal-to-sr
description: Use when every proposal associated with an OHOS IR has passed GATE A and a System Requirement baseline is needed before spec and design work begins. Triggers: 生成SR, proposal转SR, SR基线, 系统需求基线, GATE A通过, 05-proposal to SR. Do NOT use for IR generation (ohos-req-feature-to-ir), feature baseline (ohos-req-feature-baseline), or feasibility analysis (ohos-req-feasibility-analysis).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: proposal-to-sr
  version: 0.3.0
  status: draft
  tags:
    - sdd
    - requirements
  related-skills:
    - name: ohos-req-feature-to-ir
      min_version: 0.2.0
      required: true
---

# OHOS Proposal 转 SR

**Announce at start:** "我正在使用 ohos-req-proposal-to-sr skill 生成 SR.md。"

## 定位

SR.md 作为 OHOS 电子流 GA 后基线附件提交，SR 的 status=GA-Approved 是 ohos-delivery 启动 Phase 1-9 的前置条件。SR 的维度确认继承自 IR（PIR #152 P0），不重新逐条交互。SR §二责任人表的分析责任人/SE/TSE/测试责任人必须在 handoff 前指定（PIR #152 P2），缺失则阻断 Phase 1-9 启动。

## 适用边界

- ✅ 适用：Phase 0 GA 后每个 proposal 对应生成 SR 基线
- ❌ 不适用：IR 生成（ohos-req-feature-to-ir）、Feature 基线（ohos-req-feature-baseline）、可行性分析（ohos-req-feasibility-analysis）

## 输入与硬门禁

- `IR.md`
- 一个或多个 `05-proposal*.md`
- 每个 proposal 对应的 GA 记录

以下任一情况必须拒绝生成：

- proposal 状态不是 `GA-Approved`
- `gate_a` 或外部 GA 证据为空
- IR 拆解矩阵中的 proposal 未全部覆盖
- proposal 的 P0/P1 AC 无法回溯到 IR

## 模板说明

- 模板路径：`reference/SR.md`
- proposal 结构参考模板：`reference/proposal.md`（模板文件不带 `05-` 阶段编号前缀；`05-proposal*.md` 仅作为 `{docs_dir}` 下的产物文件名）
- 模板含 5 个章节：GA 通过证据 / 系统需求基线 / 接口责任与跨仓契约 / 验收与约束 / 来源追溯
- **一份 SR.md 只定义一个 SR；一个 proposal 对应一个 SR**
- 多个 SR 时各自独立文件（`SR-01.md`、`SR-02.md`...），以模板内「关联 SR」表相互引用
- 流程规则（硬门禁、追溯矩阵、维度确认等）由本 skill 控制

## 流程

1. 读取 `reference/SR.md`、`reference/proposal.md`（了解 proposal 产物结构）、IR、proposal 和 GA 证据。
2. 从 `IR.md` frontmatter 继承 `rr_id` 到 SR.md frontmatter，并在 §二 需求概要表中填写 RR单号行。
3. **按 proposal 逐个生成 SR**：每个 GA-Approved 的 proposal 对应一个独立的 SR 文件。
4. 记录该 proposal 的 GA 日期、结论、参与人和证据链接（§一）。
5. 从该 proposal 和 IR 的需求陈述中提取系统需求基线（§二），不添加 proposal 未批准的新范围。提取方法：
   - **按 FR/NFR 分类**：从 proposal §3 需求基线逐条提取，分别归入功能需求和非功能需求
   - **合并重叠需求**：同一能力在多个用户故事中出现时，合并为一条系统需求，保留各来源引用
   - **识别跨 proposal 依赖**：仅记录依赖关系（如"SR-01 依赖 SR-02 的 XX 接口"），不合并多个 proposal 的需求
    - **标注来源**：每条系统需求标注来源（proposal §X），确保可追溯
     - 填写「关联 SR」表引用其他 proposal 对应的 SR
     - **§二「责任人」表的分析责任人/SE/TSE/测试责任人必须填写**，不得留空或标"待确定"——如暂未确定，标注"⚠️ 待指定"并在 handoff 前置检查中阻断

> **Before writing an interface responsibility, ask yourself:** am I adding implementation signatures (methods, classes) or just defining responsibility boundaries (direction, type)?

> Before writing a traceability matrix row, ask yourself: does this AC trace back to a proposal requirement, or am I creating an untraceable link?

> Before writing SR §二 需求基线, ask yourself: 每条系统需求是否可追溯到 proposal §X？是否新增了 proposal 未批准的范围？

> Before 维度确认, ask yourself: IR 是否已确认此维度？是否只需继承结论而非重新逐条交互？

6. 定义接口责任、提供方、消费方和语义约束（§三），不写实现签名。定义方法：
   - **提取涉及接口**：从 proposal 影响范围表提取涉及的接口清单
   - **标注方向**：上游->下游 / 下游->上游 / 双向
   - **标注类型**：Public（对外公开）/ System（系统级）/ Internal（仓内内部）
   - **定义责任与语义约束**：明确每个接口的职责边界和语义约束，不写方法签名、类设计或时序设计
7. 填写验收标准、系统约束和维度涉及确认（§四）。**维度确认继承自 IR.md**——直接引用 IR 已确认的维度结论，不再向用户逐条重新确认。仅当 proposal 范围超出 IR 覆盖的新增维度时才补充确认。
8. 建立 `IR -> Proposal -> SR -> AC` 追溯矩阵（§五）。
9. 保存到 `{docs_dir}/SR-{NN}.md`（编号与 proposal 对应，如 `SR-01.md` 对应 `05-proposal-01.md`），状态设为 `GA-Approved`。

## 文件命名规则

| proposal 文件 | SR 文件 |
|---------------|---------|
| `05-proposal.md`（单一） | `SR.md` |
| `05-proposal-01.md` | `SR-01.md` |
| `05-proposal-02.md` | `SR-02.md` |

## 自检

自检清单详见 [reference/sr-checklist.md](reference/sr-checklist.md)。核心：GA通过证据齐全、1:1 proposal→SR映射、维度继承自IR、责任人表无空值。

## NEVER

- **NEVER 在 SR 中新增 proposal 未批准的需求范围**：SR 是 GA 后的基线，只能从已批准 proposal 提取，不可自行扩大范围（原因：SR 是 GA 后锁定的基线，新增范围绕过了 GA 审批，未批准的需求会进入 Phase 1-9 实现阶段导致返工）
- **NEVER 在 SR 中写实现签名**：SR 定义接口责任和语义约束，不包含方法签名、类设计、时序设计（这些属于 spec/design 阶段）（原因：SR 是系统需求基线附件，方法签名/类设计属于 spec/design 阶段产物，提前写入会与后续设计产生冲突）
- **NEVER 合并多个 proposal 的 SR**：一个 proposal 对应一个 SR（1:1 关系），跨 proposal 依赖仅记录依赖关系，不合并文件（原因：合并会模糊 GA 审批边界，导致部分 proposal 未批准的需求混入 SR 基线，电子流无法追溯单个 proposal 的验收状态）
- **NEVER 忽略 P0/P1 AC 到 IR 的可追溯性**：每条 P0/P1 AC 必须能在 IR 矩阵中找到对应行，缺失时拒绝生成 SR（原因：断链的 AC 在 Phase 5 测试阶段无法验证，导致 SR 验收无法闭环）

## 输出

- 路径：`{docs_dir}/SR-{NN}.md`（每个 proposal 一个）或 `{docs_dir}/SR.md`（单一 proposal 时）
- 回传：SR 文件列表、各 SR ID、RR单号、GA proposal 数量、系统需求数量和追溯覆盖率
