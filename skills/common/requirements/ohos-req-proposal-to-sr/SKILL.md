---
name: ohos-req-proposal-to-sr
description: Use when every proposal associated with an OHOS IR has passed GATE A and a System Requirement baseline is needed before spec and design work begins.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: sdd
  capability: proposal-to-sr
  version: 0.1.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS Proposal 转 SR

**Announce at start:** "我正在使用 ohos-proposal-to-sr skill 生成 SR.md。"

## 定位

SR 是 GA 后锁定的系统需求基线。它定义系统需求、接口责任和约束，但不包含详细方法签名、类设计或时序设计。

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
- 模板含 5 个章节：GA 通过证据 / 系统需求基线 / 接口责任与跨仓契约 / 验收与约束 / 来源追溯
- **一份 SR.md 只定义一个 SR；一个 proposal 对应一个 SR**
- 多个 SR 时各自独立文件（`SR-01.md`、`SR-02.md`...），以模板内「关联 SR」表相互引用
- 流程规则（硬门禁、追溯矩阵、维度确认等）由本 skill 控制

## 流程

1. 读取 `reference/SR.md`、IR、proposal 和 GA 证据。
2. 从 `IR.md` frontmatter 继承 `rr_id` 到 SR.md frontmatter，并在 §二 需求概要表中填写 RR单号行。
3. **按 proposal 逐个生成 SR**：每个 GA-Approved 的 proposal 对应一个独立的 SR 文件。
4. 记录该 proposal 的 GA 日期、结论、参与人和证据链接（§一）。
5. 从该 proposal 和 IR 的需求陈述中提取系统需求基线（§二），不添加 proposal 未批准的新范围。提取方法：
   - **按 FR/NFR 分类**：从 proposal §3 需求基线逐条提取，分别归入功能需求和非功能需求
   - **合并重叠需求**：同一能力在多个用户故事中出现时，合并为一条系统需求，保留各来源引用
   - **识别跨 proposal 依赖**：仅记录依赖关系（如"SR-01 依赖 SR-02 的 XX 接口"），不合并多个 proposal 的需求
   - **标注来源**：每条系统需求标注来源（proposal §X），确保可追溯
   - 填写「关联 SR」表引用其他 proposal 对应的 SR
6. 定义接口责任、提供方、消费方和语义约束（§三），不写实现签名。定义方法：
   - **提取涉及接口**：从 proposal 影响范围表提取涉及的接口清单
   - **标注方向**：上游->下游 / 下游->上游 / 双向
   - **标注类型**：Public（对外公开）/ System（系统级）/ Internal（仓内内部）
   - **定义责任与语义约束**：明确每个接口的职责边界和语义约束，不写方法签名、类设计或时序设计
7. 填写验收标准、系统约束和维度涉及确认（§四）。
8. 建立 `IR -> Proposal -> SR -> AC` 追溯矩阵（§五）。
9. 保存到 `{docs_dir}/SR-{NN}.md`（编号与 proposal 对应，如 `SR-01.md` 对应 `05-proposal-01.md`），状态设为 `GA-Approved`。

## 文件命名规则

| proposal 文件 | SR 文件 |
|---------------|---------|
| `05-proposal.md`（单一） | `SR.md` |
| `05-proposal-01.md` | `SR-01.md` |
| `05-proposal-02.md` | `SR-02.md` |

## 自检

- [ ] 所有关联 proposal 均有 GA 通过证据
- [ ] RR单号已从 IR.md 继承（frontmatter `rr_id` + §二 需求概要表）
- [ ] 每个 proposal 对应一个独立 SR 文件
- [ ] 系统需求没有扩大已批准范围（判定方法：逐条对比 proposal §3 用户故事与 AC，与 SR §二需求基线，确认无新增范围）
- [ ] 接口责任不依赖尚未生成的 spec/design
- [ ] P0/P1 AC 和系统约束完整
- [ ] 维度涉及确认 10 项已填写
- [ ] 关联 SR 引用表已填写（多 SR 时）
- [ ] 追溯矩阵无断链

## NEVER

- **NEVER 在 SR 中新增 proposal 未批准的需求范围**：SR 是 GA 后的基线，只能从已批准 proposal 提取，不可自行扩大范围
- **NEVER 在 SR 中写实现签名**：SR 定义接口责任和语义约束，不包含方法签名、类设计、时序设计（这些属于 spec/design 阶段）
- **NEVER 合并多个 proposal 的 SR**：一个 proposal 对应一个 SR（1:1 关系），跨 proposal 依赖仅记录依赖关系，不合并文件

## 输出

- 路径：`{docs_dir}/SR-{NN}.md`（每个 proposal 一个）或 `{docs_dir}/SR.md`（单一 proposal 时）
- 回传：SR 文件列表、各 SR ID、RR单号、GA proposal 数量、系统需求数量和追溯覆盖率
