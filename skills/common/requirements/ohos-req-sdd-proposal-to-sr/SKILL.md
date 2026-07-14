---
name: ohos-req-sdd-proposal-to-sr
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
5. 从该 proposal 和 IR 的需求陈述中提取系统需求基线（§二），不添加 proposal 未批准的新范围。填写「关联 SR」表引用其他 proposal 对应的 SR。
6. 定义接口责任、提供方、消费方和语义约束（§三），不写实现签名。
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
- [ ] 系统需求没有扩大已批准范围
- [ ] 接口责任不依赖尚未生成的 spec/design
- [ ] P0/P1 AC 和系统约束完整
- [ ] 维度涉及确认 10 项已填写
- [ ] 关联 SR 引用表已填写（多 SR 时）
- [ ] 追溯矩阵无断链

## 输出

- 路径：`{docs_dir}/SR-{NN}.md`（每个 proposal 一个）或 `{docs_dir}/SR.md`（单一 proposal 时）
- 回传：SR 文件列表、各 SR ID、RR单号、GA proposal 数量、系统需求数量和追溯覆盖率
