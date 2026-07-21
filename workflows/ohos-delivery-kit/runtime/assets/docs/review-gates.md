# 阶段审视规范 (Review Gates)

本文件定义 ODK 各阶段交付件的**人工审视 checkpoints** 和**合入门禁 (hard gates)**。
目标不是把 gate 切得越细越好，而是把真正需要人工判断的节点收敛成少数几个高价值门禁。

当前推荐采用 **2 个设计阶段 gate + 1 个正式代码 gate**：

- **GA: Proposal Gate** — 冻结需求方向
- **GB: Design Baseline Gate** — 冻结 `spec/design/execution-plan` 与 `implement` 源码初稿
- **GC: Final Delivery Gate** — 正式代码评审与交付一致性确认

其中，**GB 是设计基线 PR**，不是最终代码合入 gate。它把文档交付件和源码初稿放进同一个 issue 开发上下文里，让后续真实开发、联调和代码 review 都建立在同一份设计基线之上。

## 原则

1. **角色分工，责任明确** — 每个 checkpoint 分配到一个或多个角色，不存在无人负责的检查项
2. **AI 辅助，人类决策** — AI 可自动检查格式/结构/一致性，但方向性、取舍性判断由人类做出
3. **gate 是少数高价值门禁** — spec / design / plan 不再拆成多个分散的人审 gate，而是收敛到 Design Baseline Gate
4. **gate 文件即证据** — gate 通过后记录在 `evidence/gates/`，作为阶段签批凭据
5. **例外透明** — 无法通过的项必须显式记录理由、负责人和预期解决时间
6. **源码初稿服务于设计收敛** — `odk-implement` 在 GB 阶段生成的代码是设计验证型初稿，不视为最终实现提交

## 角色定义

| 角色 | 标识 | 核心命题 | 参与 Gate |
|------|------|---------|----------|
| 产品经理 | `@pm` | 做什么、不做什么、怎么算做完 | GA |
| 系统设计 | `@se` | 怎么做、影响什么、风险是否可控 | GA, GB, GC |
| 测试设计 | `@tse` | 做得对不对、全不全、边界是否覆盖；设计蓝军 | GA, GB, GC |
| 开发人员 | `@dev` | 能否实现、粒度如何、代码是否合格 | GA, GB, GC |
| 仓库提交者 | `@committer` | 最终代码合入质量、仓库演进和提交责任 | GC |

> **角色兼任**: 同一人可兼任多个角色。在小团队中，由 Tech Lead 确认角色分配。
> **检查方式**: 各角色检查项可通过 AI 辅助（skill / rule / validator）完成，也可人工逐项核对。
> **▲ = 主审（必须签批通过）**　**△ = 参与（可提出阻塞性问题，但不主签）**　**— = 不强制参与**

---

## SDD 流程 × Gate × 角色 全景图

```text
                     @tse▲ @pm▲ @dev△ @se(owner)
                               │
  odk-propose ────→ GA ────────┘
      │
      ▼
  📄 proposal.md
      │
      ▼
  odk-spec → odk-design → odk-plan → odk-implement(源码初稿)
      │          │            │              │
      ▼          ▼            ▼              ▼
  📄 spec.md  📄 design.md  📄 execution-   💻 draft code
                            plan.md
      │          │            │              │
      └──────────┴────────────┴──────┬───────┘
                                     ▼
                          GB: Design Baseline PR
                      @tse▲ @dev▲ @se△ @pm△
                                     │
                                     ▼
                          锁定 issue 设计基线与源码初稿
                                     │
                                     ▼
                         后续真实开发 / 联调 / 修正实现
                                     │
                                     ▼
                           odk-review → evidence/reviews/
                                     │
                                     ▼
                           GC: Final Delivery Gate
                       @committer▲ @se▲ @tse△ @dev△
                                     │
                                     ▼
                      odk-validate → Level A/B/C/D pass → 正式代码合入 / 归档
```

---

## Gate ↔ SDD 实施点映射表

| Gate | SDD 节点 | 输入交付件 | 输出交付件 | 主审 | 参与 | 审视主题 |
|------|---------|-----------|-----------|------|------|---------|
| **GA** | `odk-propose` 完成 | — | proposal.md | @tse ▲ + @pm ▲ | @dev △ + @se △ | 需求方向正确性 |
| **GB** | `odk-spec` + `odk-design` + `odk-plan` + `odk-implement` 初稿完成 | proposal.md | spec.md + design.md + execution-plan.md + draft code | @tse ▲ + @dev ▲ | @se △ + @pm △ | 设计基线与源码初稿一致性 |
| **GC** | 真实开发/联调后 `odk-review` 完成 | code + spec.md + design.md + execution-plan.md + evidence/reviews/ | 正式代码提交结论 | @committer ▲ + @se ▲ | @tse △ + @dev △ | 最终交付一致性 |
| — | `odk-validate` 完成 | 全部 | Level A/B/C/D pass | 自动化 | — | 机器校验 |
| *(旁路)* | `odk-spec-for-validation` | spec.md + design.md | spec-for-validation.md | @tse | @se △ + @dev △ | 验证规格 |
| *(旁路)* | `odk-security-threat-model` | design.md + proposal.md | threat-model.md | @se | @tse △ + @dev △ | 高风险深度威胁分析（STRIDE + 合规） |

---

## Gate A: Proposal Gate — 需求方向正确性

**SDD 节点**: `odk-propose` 生成 `proposal.md` 后
**主 owner**: `@se`
**主审**: `@tse` ▲ + `@pm` ▲
**参与**: `@dev` △ + `@se` △
**目标**: 确认 "做什么、不做什么、怎么算做完" 在所有角色间对齐。

### 产物与 PR 语义

- 产物：`proposal.md`
- 推荐 PR：**Proposal PR**
- 合入语义：需求方向基线合入，可继续进入 `spec/design/plan`

### @pm — 需求方向 (▲ 主审)

| # | Checkpoint | 类型 |
|---|-----------|------|
| A1 | `target_release` 与发布计划一致，不是占位符 | `[人工]` |
| A2 | 分级判断 (L0-L4) 有事实支撑：复杂度 / 仓库数 / API 影响 / 安全关键路径 / 跨 SIG | `[人工]` |
| A3 | 非目标至少列出 1 项明确不做的事情（防止范围蔓延） | `[人工]` |
| A4 | 每条成功标准有可观测外部指标 + 验证方式（不能写 "功能可用" 或 "代码写完"） | `[人工]` |
| A5 | 需求范围和 issue 描述一致，无主观扩写的额外范围 | `[人工]` |

### @tse — 可测性与验收口径 (▲ 主审)

| # | Checkpoint | 类型 |
|---|-----------|------|
| A6 | 成功标准可测试，无 "体验更好"、"基本可用" 一类不可测表述 | `[人工]` |
| A7 | 8 维不涉及项全部填写，每项有 "是/否" + 一句话理由 | `[AI]` |
| A8 | proposal 中的成功标准已为后续 spec AC 留出可验证空间，不是纯宣言式目标 | `[人工]` |

### @dev — 可行性预判 (△ 参与)

| # | Checkpoint | 类型 |
|---|-----------|------|
| A9 | 需求在目标仓库技术栈中可实现，无明显不可行风险 | `[人工]` |

### @se — 影响范围预判 (△ 参与 / owner)

| # | Checkpoint | 类型 |
|---|-----------|------|
| A10 | 影响范围中子系统 / 仓库 / 模块准确，无明显遗漏 | `[人工]` |
| A11 | 如涉及公开 API / SDK 变更，已在 proposal 中明确标出，供 GB 重点审视 | `[人工]` |

---

## Gate B: Design Baseline Gate — 设计基线与源码初稿

**SDD 节点**: `odk-spec`、`odk-design`、`odk-plan` 完成，且 `odk-implement` 已生成源码初稿后
**主审**: `@tse` ▲ + `@dev` ▲
**参与**: `@se` △ + `@pm` △
**目标**: 冻结当前 issue 的 `spec/design/execution-plan` 基线，并用 implement 源码初稿反向暴露设计和规格问题。

> **关键定义**
>
> GB 对应的是**Design Baseline PR**，不是最终代码合入 gate。
> 这里的 `implement` 代码属于**设计验证型源码初稿**：
>
> - 用于检验 spec / design / plan 是否闭环、是否可实现
> - 可作为后续真实开发和联调的输入
> - 不代表“已经完成正式开发”
> - 后续真实实现可以重新提交正式 PR，并对比 GB 初稿持续改进

### 产物与 PR 语义

- 必选产物：
  - `spec.md`
  - `design.md`
  - `execution-plan.md`
  - `odk-implement` 生成的源码初稿
- 可选产物：
  - `spec-for-validation.md`
  - `evidence/gates/gate-b-design-baseline.md`
- 推荐 PR：**Design Baseline PR**
- 合入语义：锁定本 issue 的设计基线与源码初稿，后续真实开发在此基础上继续推进

### @tse — 规格闭环与蓝军审视 (▲ 主审)

| # | Checkpoint | 类型 |
|---|-----------|------|
| B1 | proposal 成功标准均能在 `spec.md` 中找到对应 AC | `[AI]` |
| B2 | AC 使用 `WHEN [condition] THEN [verifiable result]` 格式，编号和分组正确 | `[AI]` |
| B3 | 异常/边界规则表覆盖本次变更相关维度：输入边界 / 超时 / 并发冲突 / 资源不足 | `[人工]` |
| B4 | `design.md` 的关键设计决策均至少引用 1 条 spec AC 编号 | `[AI]` |
| B5 | 设计没有遗漏关键失败路径：spec 里要求的行为，在设计中都有异常/恢复/降级考虑 | `[人工]` |
| B6 | 如已生成源码初稿，初稿未暴露出新的未记录规格空洞；如暴露，spec/design/plan 已同步修订或显式留痕 | `[人工]` |
| B7 | 如生成 `spec-for-validation.md`，其关键场景与 spec/design 一致，无明显验证盲区 | `[人工]` |
| B7.1 | 如生成 `threat-model.md`，P0/P1 风险均有缓解措施并关联 Task（缓解措施可追溯到 execution-plan） | `[人工]` |

### @dev — 可执行性与源码初稿质量 (▲ 主审)

| # | Checkpoint | 类型 |
|---|-----------|------|
| B8 | `execution-plan.md` 的 AC-Task 追溯表 `Covered?` 列全部为 "是" | `[AI]` |
| B9 | 每个 Task 有文件级代码范围、完成判据和验证命令 | `[AI]` |
| B10 | Task 粒度适合后续真实开发推进，单个 Task 不应过大或跨越多个不相关子系统 | `[人工]` |
| B11 | 源码初稿覆盖了关键实现路径，足以验证 design 决策的可落地性 | `[人工]` |
| B12 | 源码初稿与 execution-plan 声明的文件范围基本一致；如有超出，已在 plan 或备注中解释 | `[AI]` |
| B13 | 初稿未引入明显违反红线的实现（如公开 API 误改、新三方依赖、关键性能预算失控） | `[人工]` |

### @se — 架构 owner 审视 (△ 参与)

| # | Checkpoint | 类型 |
|---|-----------|------|
| B14 | 关键设计决策有推荐方案 + 至少 1 个替代方案 + 取舍理由 | `[人工]` |
| B15 | 模块影响表覆盖所有受影响子系统/仓库，尤其注意间接依赖 | `[人工]` |
| B16 | `代码事实基线` 的关键约束在设计和源码初稿中得到处理 | `[AI]` |
| B17 | 如适用，`状态归属与不变量` 无模糊表述，且初稿没有直接违背这些约束 | `[人工]` |

### @pm — 需求一致性确认 (△ 参与)

| # | Checkpoint | 类型 |
|---|-----------|------|
| B18 | 设计和源码初稿没有偏离 proposal 的需求边界；如有超出，已显式说明是预留还是偏差 | `[人工]` |
| B19 | 兼容性影响、用户可见行为变化在 spec/design 中有清楚表达 | `[人工]` |

---

## Gate C: Final Delivery Gate — 正式代码评审与交付一致性

**SDD 节点**: 后续真实开发 / 联调完成，`odk-review` 生成 `evidence/reviews/` 后
**主审**: `@committer` ▲ + `@se` ▲
**参与**: `@tse` △ + `@dev` △
**目标**: 确认最终代码实现、验证证据和交付件一致，可以正式合入代码仓。

> GC 对应的是**正式代码 PR**。
> 它延续传统代码 review gate，同时允许与 GB 的源码初稿 PR 做对比，审视真正实现相对设计基线的改进和偏差。

### 产物与 PR 语义

- 必选产物：
  - 最终代码
  - `evidence/reviews/spec-compliance.md`
  - `evidence/reviews/code-quality.md`
  - `evidence/reviews/verification.md`
- 推荐 PR：**Final Delivery PR**
- 合入语义：正式实现合入

### @committer — 最终代码合入质量 (▲ 主审)

| # | Checkpoint | 类型 |
|---|-----------|------|
| C1 | `code-review` 中标记为阻塞 (blocking) 的 Issues 已全部解决 | `[人工]` |
| C2 | 实际变更代码文件与 execution-plan 声明范围一致；如有扩展，已补充说明 | `[AI]` |
| C3 | 最终代码相对 GB 的源码初稿，如有关键偏离，已解释原因并同步更新交付件 | `[人工]` |
| C4 | 正式提交满足仓库提交质量要求，可承担最终合入责任 | `[人工]` |

### @se — 架构与设计一致性 (▲ 主审)

| # | Checkpoint | 类型 |
|---|-----------|------|
| C5 | 最终实现与 design.md 的关键决策一致；如偏离，design.md 或 review 证据已显式记录 | `[人工]` |
| C6 | 模块边界、状态约束、关键技术路线未被实现过程无意破坏 | `[人工]` |
| C7 | 如涉及架构性偏差，已有明确的设计回写或后续收敛计划 | `[人工]` |

### @tse — 规格符合性与验证证据 (△ 参与)

| # | Checkpoint | 类型 |
|---|-----------|------|
| C8 | `spec-compliance` 表中所有 AC 有实现证据（file:line 或测试结果），无空行 | `[证据]` |
| C9 | 验证记录有具体证据（命令输出 / 日志摘录 / 人工检查记录），不得仅有 "通过" / "PASS" | `[证据]` |
| C10 | 验证覆盖异常/边界场景，不限于 happy path 验证 | `[人工]` |
| C11 | `spec-for-validation.md` 中的关键场景（如已生成）均已执行并有结果记录 | `[证据]` |
| C11.1 | `threat-model.md`（如已生成）中 P0/P1 风险的缓解措施已在代码 / 测试中落实，并有结果记录 | `[证据]` |

### @dev — 正式实现交底 (△ 参与)

| # | Checkpoint | 类型 |
|---|-----------|------|
| C12 | 最终代码与 spec 一致性结论明确：只能是 "一致" 或 "不一致（已记录偏差）" | `[AI]` |
| C13 | 无未解释的超范围实现；如有新增能力，已补充到交付件或拆为新需求 | `[人工]` |

---

## 跨阶段规则

### Proposal PR / Design Baseline PR / Final Delivery PR 的关系

推荐拆分为三类 PR：

1. **Proposal PR**
   - 聚焦 `proposal.md`
   - 冻结需求方向
2. **Design Baseline PR**
   - 聚焦 `spec.md`、`design.md`、`execution-plan.md` 与 `implement` 源码初稿
   - 锁定需求开发过程中的设计基线和初稿实现
3. **Final Delivery PR**
   - 聚焦联调后的正式实现、review 证据和最终一致性
   - 与传统代码提交 review 兼容

允许的协作方式：

- Proposal PR 合入后，再开启 Design Baseline PR
- Design Baseline PR 合入后，后续真实开发可新开 Final Delivery PR
- Final Delivery PR 可引用 Design Baseline PR 作为“设计基线 / 初稿对照 PR”

### 角色缺席处理

| 情况 | 处理方式 |
|------|---------|
| 角色在小团队中不存在 | Tech Lead 兼任，在 gate 文件中明确记录 "该角色职责由 @xxx 代行" |
| 某个 Gate 的参与角色 `△` 缺席 | 不阻塞 gate，但在 gate 文件中记录 "未参与" |

### 例外处理

如某个硬 gate 确实无法通过：

1. 在 gate 文件中显式记录未通过的 checkpoint + 理由
2. 指定负责人和预期解决时间
3. 获得主审角色批准
4. 在下一 Gate 开头首先回顾上一 Gate 的例外是否已解决

### gate 文件模板

Gate 通过后，可选记录到 `evidence/gates/gate-<name>.md`：

```markdown
# Gate <Name>

- **SDD 节点**: odk-<command> 完成
- **日期**: YYYY-MM-DD
- **通过**: 是 / 否
- **PR 类型**: Proposal PR / Design Baseline PR / Final Delivery PR

## 角色签批

| 角色 | 人名 | 签批 | 备注 |
|------|------|------|------|
| @pm | | 通过 / 例外 / — | |
| @se | | 通过 / 例外 / — | |
| @tse | | 通过 / 例外 / — | |
| @dev | | 通过 / 例外 / — | |

## Checkpoints

- [x] A1 ...
- [x] A2 ...
- [ ] B6 ... — ⚠️ 例外：<理由>，预期 <日期> 前由 <负责人> 解决

## 例外记录

| Checkpoint | 理由 | 负责人 | 预期解决 |
|------------|------|--------|---------|
| B6 | ... | @name | YYYY-MM-DD |

## 备注

<讨论结论、遗留事项、后续关注点>
```

---

## 扩展指南

本文档是最小基线。后续可根据需要扩展：

### 新增角色

在角色表中追加行，在对应 Gate 下追加 checkpoints。示例：

| 新角色 | 标识 | 核心命题 | 参与 Gate |
|--------|------|---------|----------|
| 安全审计 | `@sec` | 安全漏洞、权限模型、CVE 策略、沙箱隔离 | GA(参与), GB(审视), GC(验证) |
| 性能工程 | `@perf` | 性能基准、退化检测、热路径设计、资源预算 | GA(参与), GB(审视), GC(验证) |

### 新增子系统专项检查

在对应 Gate 下追加专项小节。示例：

```markdown
### ArkUI 专项 — Gate B 追加

| # | Checkpoint | 类型 | 角色 |
|---|-----------|------|------|
| B.A1 | 是否满足 60fps 硬约束（渲染管线设计不得引入主线程阻塞） | `[证据]` | @se |
| B.A2 | 多设备适配 (Phone/Tablet/Watch/TV) 是否在设计和源码初稿中论述 | `[人工]` | @tse |
```

### 新增 Checkpoint 类型

| 标签 | 含义 | 举例 |
|------|------|------|
| `[AI]` | AI agent 可自动检查（skill / validator） | AC 格式合规、章节完整性、文件范围一致性 |
| `[人工]` | 必须人类判断 | 分级是否偏低、架构是否过度设计、初稿是否真的帮助设计收敛 |
| `[证据]` | 必须有文档/数据支撑 | 测试通过记录、日志、review 结论 |
| `[工具]` | 可通过外部工具自动化（CI / 静态分析） | Lint 检查、覆盖率报告 |

---

## 与现有文档的关系

| 文档 | 关系 |
|------|------|
| `using-odk` Phase Gate 规则 | 约束 AI 行为（何时等待用户进入下一阶段）；本文件约束人工 gate **检查什么** |
| `docs/contracts.md` | 定义产物**结构**；本文件定义 Proposal / Design Baseline / Final Delivery 的**人工判断标准** |
| `odk-validate` Level A/B/C/D | 机器执行的自动结构校验；本文件定义人工语义审视 checkpoints |
| `core/templates/review/` | 提供 review 文档模板；本文件定义这些文档的通过标准 |
| `docs/code-traceability.md` | 定义可追溯链的数据要求；本文件定义在 GB / GC 阶段如何判断追溯链是否足够支撑评审 |
