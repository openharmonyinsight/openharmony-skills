# Architecture

## 定位

`ohos-delivery-kit` 是 OpenHarmony 场景下的"交付件规范层"，不是新的重型工作流平台。

它解决的是一个更基础的问题：

- 业务仓最终应该沉淀哪些交付件
- 每份交付件至少必须包含哪些章节
- 不同插件如何围绕同一套交付件规范协作
- 插件过程中的输出如何和最终归档件、最终代码保持可追溯映射

## 总体分层

```text
┌─────────────────────────────────────────────┐
│ Layer 1: Core Delivery Contract             │
│ templates / rules / validators              │
│ 定义最终什么算合规交付件                    │
└─────────────────────────────────────────────┘
                      ▲
                      │ validate / materialize
                      ▼
┌─────────────────────────────────────────────┐
│ Layer 2: Adapter Layer                      │
│ openspec / superpowers / matspec / custom   │
│ 负责把不同执行风格映射到同一套交付件语义     │
└─────────────────────────────────────────────┘
                      ▲
                      │ package / invoke
                      ▼
┌─────────────────────────────────────────────┐
│ Layer 3: Platform Packaging                 │
│ codex / claude / opencode                   │
│ 负责安装、命令入口、skill 暴露、平台适配     │
└─────────────────────────────────────────────┘
```

这三层里，只有 Layer 1 可以定义正式归档契约。

Layer 2 和 Layer 3 只能帮助产出，不能改写正式归档真相源。

`ohos-sdd` 不应放进这条组合链中强行参与。

更合适的定位是：

- `ohos-sdd` 可以作为独立 OpenHarmony 插件单独使用
- `ohos-sdd` 的交付件规范应尽量与 `ohos-delivery-kit` 对齐
- 这样团队可以二选一，而不是把两者硬叠加

## Layer 1: Core Delivery Contract

这一层是仓的核心，必须保持平台无关。

建议包含：

- `contracts/`
  - `artifacts.yaml` — 交付件、章节、依赖、证据策略的声明式真相源
- `templates/`
  - `ai/` — AI 生成交付件模板（proposal、spec、design、execution-plan）
  - `review/` — 人工审核用模板（spec-compliance、code-quality、verification）
- `adapters/`
  - `superpowers.yaml` / `openspec.yaml` / `matrixspec.yaml` — 插件产物到 ODK 归档件的声明式映射
- `rules/`
  - ID 规则、校验清单
- `validators/`
  - 校验 `.codespec/` 是否满足规范

这一层只回答一个问题：

**最终归档件是否合规。**

除此之外，这一层还必须提供两类强约束：

- 模板约束：要求插件在生成过程中输出特定章节
- 映射约束：要求交付件中的 AC、Task、代码范围、验证证据之间能互相对齐

### Source Boundary

ODK 后续维护以 `core` 为唯一规范源：

| 内容 | 放置位置 | 原因 |
|------|----------|------|
| 必需产物、章节、依赖、证据策略 | `core/contracts/artifacts.yaml` | 可被校验、文档和分发脚本消费 |
| 章节正文骨架、表头、占位符 | `core/templates/` | 直接决定最终交付质量下限 |
| 阶段路由、active change 解析、fallback 行为 | `core/skills/` | 属于 agent 行为，不属于 artifact contract |
| 插件产物映射和命令回退 | `core/adapters/` | 避免在长篇 prompt 和 docs 中重复维护 |
| Claude/Codex/OpenCode 安装差异 | `packaging/*` | 平台壳只负责暴露能力，不拥有规范 |

详见 `docs/designs/source-boundary-and-distribution.md`。

## Layer 2: Adapter Layer

这一层处理"不同插件如何接入统一交付件规范"。

关键要求：

- adapter 是描述性的，不是规定性的
- adapter 记录映射关系，不拥有正式目录结构
- adapter 可以暴露缺口，但不能绕过 validator 宣布合规

每个 adapter 的职责应该很窄：

- 声明该插件能辅助哪些交付件
- 声明该插件产物如何映射到 `proposal/spec/design/plan/review`
- 声明哪些内容仍必须回填到标准文档
- 声明插件输出与代码生成或代码变更之间如何建立映射证据

这些声明现在应优先沉淀在 `core/adapters/*.yaml`。`docs/adapters.md` 只解释适配策略和人工兜底路径，不再作为精确映射的唯一维护位置。

建议支持的 adapter：

- `openspec`
  - 前期探索、通用 spec 草拟
- `superpowers`
  - TDD、review、执行纪律增强
- `matspec`
  - 基线恢复、模板化阶段推进
- `custom`
  - 业务团队本地扩展

Adapter 不拥有最终真相源。

最终真相源始终是：

- `.codespec/changes/<id>/` 目录下的标准交付件

推荐每个 adapter 固定四段内容：

1. 适用场景
2. 映射表
3. 缺口说明
4. 最小回填要求
5. 代码映射要求

## Layer 3: Platform Packaging

这一层只处理平台安装和调用入口，不承载交付件规范真相。

建议目录：

```text
packaging/
├── codex/
├── claude/
└── opencode/
```

每个平台只做三件事：

1. 暴露入口
2. 引用 `core/` 和 `adapters/` 的能力
3. 把结果写回业务仓 `.codespec/`

为做到"无缝无感"，平台层不应要求开发者显式理解 adapter 细节。

更合理的做法是：

- slash command 只暴露阶段语义
- adapter 选择由命令或配置自动完成
- 模板强制章节在生成时自动注入

不允许：

- 把平台特定 prompt 写成唯一规范来源
- 让某个平台独有的目录结构替代标准交付件结构
- 让平台包内文档成为业务归档件

## 数据流

```text
User / Team Choice
  -> select adapter(s)
  -> invoke platform package
  -> generate or update .codespec/
  -> run validator
  -> archive compliant artifacts
```

关键控制点：

- 只有一个正式交付规范
- 可以有多个辅助插件
- 适配器之间允许并存，但只能有一个归档真相源
- 最终必须通过统一 validator

## 统一验证口

`ohos-delivery-kit` 必须把验证定义成唯一耦合点。

这意味着：

- 插件可以不同
- 生成过程可以不同
- 文风可以不同
- 但最终归档前必须经过同一个 validator

同时，validator 不能只看"文件是否存在"，还要逐步看：

- 过程交付件是否已回填到最终归档件
- 归档件中的 AC / Task / code_refs / evidence 是否能对应到实现结果

如果 validator 未通过，就不能把交付件视为正式完成。

这条规则比任何 prompt 或命令约定都更重要。

## OpenHarmony 定制点

相较于通用交付规范，OpenHarmony 额外关注以下字段：

- `target_release`
- `code_refs`

这些约束应由 validator 强制，而不是靠写作者自觉。

### 安全两层模型

安全不在主链之外另起流程，而是随 SDD 自然产生：Tier 1 为 `design.md` 的条件章节「安全基础检查」，Tier 2 为高风险变更按需生成的 `threat-model.md`，二者由 propose 的 `安全/权限` 维度裁定作为单一触发源驱动。设计详见 `docs/designs/security-design.md`，操作层清单见 `docs/security-guide.md`。

## 过程件与归档件一致性

这是 `ohos-delivery-kit` 相对普通模板仓的核心差异。

本仓不只是定义"最终归档长什么样"，还要求：

- 插件过程中的阶段输出和最终归档件内容语义一致
- 最终归档件不是事后总结，而是过程输出的收口版本
- 代码生成或代码变更必须能追溯回 `spec.md` 和 `execution-plan.md`

换句话说：

```text
过程输出 ≈ 归档输出 ≈ 代码实现依据
```

这三者不能彼此脱节。

## 设计开发者无感接入

要做到无缝无感，重点不是减少约束，而是把约束前置到模板和命令层。

建议做法：

- 在 kit 模板里直接内置 OpenHarmony 必需章节
- 在 slash command 或 skill 包装层里自动选用对应模板
- 在每个阶段生成时自动带出上一阶段关键信息
- 在实现和评审阶段自动要求回填 `code_refs`、验证证据

这样开发者看到的是熟悉的插件命令，
但插件生成内容从一开始就已经带有 OpenHarmony 定制章节。

## 设计取舍

### 选择"轻模板 + 强校验"，不选择"重模板 + 强流程"

原因：

- 用户希望开发者可自选不同插件
- 不同插件的强项在行为引导，而不是最终目录结构
- 统一交付件需要收敛的是结构契约，不是写作风格

### 选择"单一真相源"，不选择"双主线"

原因：

- 一个需求同时维护 OpenSpec 正式 spec 和 OHOS 正式 spec，追溯必然破裂
- 不同插件可以共存，但正式归档必须只认一套输出结构

### 选择"adapter 映射"，不选择"插件改造"

原因：

- 你无法要求所有插件接受同一种内部工作流
- 但你可以要求它们的最终输出映射到同一套归档 contract
- 这样能保留插件自由度，同时避免双主线

### 选择"先设计 core，再补 platform shells"

原因：

- 先做平台壳子容易把规范绑死在某个平台机制上
- 当前仓的关键风险不是"装不上"，而是"规范边界不清"
