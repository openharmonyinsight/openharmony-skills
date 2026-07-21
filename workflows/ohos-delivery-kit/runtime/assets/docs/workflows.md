# Workflows

## 目标

本文件定义 `ohos-delivery-kit` 与其他插件协作时的推荐使用方式。

重点不是再造一套大工作流，而是回答：

- 哪些组合成立
- 哪些组合不成立
- 插件过程输出如何与 kit 的归档要求对齐
- 如何让开发和设计在使用时更无感

## 总原则

### 模式 A：独立使用 `ohos-sdd`

如果团队已经选择 `ohos-sdd` 作为正式 OpenHarmony 插件，
理论上可以不再叠加 `ohos-delivery-kit`、`Superpowers`、`OpenSpec` 的组合链。

此时更合理的目标是：

- 让 `ohos-sdd` 的交付件规范与 kit 保持一致或高度兼容
- 而不是强迫它再走一层 kit adapter

因此：

- `ohos-sdd` 是平行方案
- `kit + other plugins` 是另一条方案

两条方案应在交付件 contract 上收敛，而不是在流程上强绑。

### 模式 B：使用 `kit + 可选插件`

这才是 `ohos-delivery-kit` 真正要覆盖的组合：

- `kit standalone`
- `kit + openspec`
- `kit + superpowers`
- `kit + openspec + superpowers`
- `kit + matspec`

在这些组合里：

- kit 定义最终 `.codespec/` 交付件 contract
- 插件负责生成、草拟、增强或恢复
- validator 负责最终收口

## 组合 0：kit standalone（纯手动）

适用场景：

- MVP 阶段，团队未接入任何第三方插件
- 只需最小交付件规范约束，不引入额外工具链
- 开发者按 kit 模板手动编写所有交付件

这是 kit 最基础的使用方式，也是其他组合模式的基线。

推荐流程：

1. `ohdk init issue-12345-slug` 创建 `.codespec/changes/issue-12345-slug/` 骨架
2. 按 kit 模板手动编写 `proposal.md`（8 必需章节）
3. 按 kit 模板手动编写 `spec.md`（9 必需章节）
4. 按 kit 模板手动编写 `design.md`（10 必需章节 + 2 条件章节）
5. 按 kit 模板手动编写 `execution-plan.md`（10 必需章节）
6. 实现代码，回填代码映射表
7. 如需要，编写可选过程证据到 `evidence/`
8. `ohdk validate .codespec/changes/<id>/` 检查合规

关键要求：

- 所有交付件必须由开发者按 kit 模板创建
- 模板只提供章节骨架，不干预写作过程
- `reviews/` 和 `gates/` 不属于最小归档 contract，默认不生成
- validator 是唯一质量门

与其他组合的关系：

- kit standalone 产出的 `.codespec/` 结构与 kit+插件组合完全一致
- 团队可以从 standalone 起步，后续随时引入 OpenSpec/Superpowers 增强特定阶段

## 组合 1：kit + OpenSpec

适用场景：

- 方案探索
- 结构化 spec 草拟
- 需要 Delta Spec 能力

推荐流程：

1. 用 kit 的 `proposal.md` 模板作为 `openspec propose` 的目标结构
2. 用 kit 的 `design.md` 模板作为 `openspec design` 的目标结构
3. 用 kit 的 `spec.md` 模板作为 `openspec spec` 的目标结构
4. OpenSpec 的中间产出如果存在私有工作区，只作为生成缓存，不作为正式归档根
5. 最终收口到 `.codespec/`

关键要求：

- OpenSpec 输出必须直接映射到 kit 模板章节
- 代码生成或代码修改若依据 OpenSpec spec，最终也必须能在 kit 的 `spec.md` 中找到对应项

## 组合 2：kit + Superpowers

适用场景：

- 需要更强的 TDD 纪律
- 需要更强的执行与 review 约束
- 但不需要强 schema spec 工具

**推荐使用桥接层命令**（`odk-sp-*`），让 ODK 自动桥接 Superpowers：

```
odk-sp-brainstorm  → Superpowers brainstorming  → proposal + spec + design
odk-sp-plan        → Superpowers writing-plans   → execution-plan
odk-sp-implement   → Superpowers TDD + subagent  → 代码 + code mapping
odk-sp-review      → Superpowers review + verify → evidence/reviews/
```

也可以分步使用基础层命令（不依赖 Superpowers）：

1. `odk-propose` / `odk-spec` / `odk-design` 模板驱动生成需求文档
2. `odk-plan` 模板驱动生成执行计划
3. `odk-implement` AI 辅助逐 Task 实现（测试先行：每 Task 先写失败测试）+ 回填 code mapping（无插件依赖）
4. `odk-review` 生成评审记录（模板驱动）

关键要求：

- 桥接命令的产出必须重定向到 `.codespec/changes/<id>/`，不写入 `docs/superpowers/`
- Superpowers 不可用时，桥接命令自动回退到基础层对应命令
- 不允许把 Superpowers 内部笔记当作正式交付件

## 组合 3：kit + OpenSpec + Superpowers

适用场景：

- 既要结构化 spec
- 又要更强执行纪律和 review

推荐分工：

- OpenSpec 负责 `proposal/spec/design` 的结构化生成
- Superpowers 负责 `execution-plan/reviews` 的执行增强
- kit 负责章节 contract、映射 contract 和最终归档 contract

这是最平衡的一种 kit 组合。

关键要求：

- OpenSpec 和 Superpowers 都不能各自产生独立正式根目录
- 所有阶段输出最终都收口到同一份 `.codespec/`

## 组合 4：kit + MatrixSpec

适用场景：

- Brownfield 场景
- 先从现有代码库恢复基线，再逐步进入标准归档流程

推荐流程：

1. 用 MatrixSpec 做基线恢复或阶段模板输出
2. 将恢复结果转写到 kit 的 `proposal/spec/design` 等标准文件
3. 后续继续在 kit 的标准目录中推进

关键要求：

- MatrixSpec 的恢复结果只是输入，不是正式归档根
- 恢复出来的文档必须转成 kit contract

## 命令设计

采用**两层命令架构**，详见 `docs/designs/two-layer-command-architecture.md`。

精确的桥接命令、fallback 和 required backfill 现在维护在 `core/adapters/*.yaml`。本节只说明开发者如何选择路径。

### 基础层（9 个命令，零插件依赖）

独立运行，模板驱动：

```
odk-init             创建骨架
odk-link-issue       关联 issue
odk-propose          生成 proposal.md
odk-spec             生成 spec.md
odk-design           生成 design.md
odk-plan             生成 execution-plan.md
odk-implement        引导逐 Task 实现（测试先行）+ 回填 code mapping
odk-review           生成 review 证据（模板驱动）
odk-validate         校验 Level A/B/C/D
```

### 桥接层（显性插件缩写）

```
Superpowers (sp):
  odk-sp-brainstorm  brainstorming → proposal + spec + design
  odk-sp-plan        writing-plans → execution-plan
  odk-sp-implement   TDD + subagent → code + mapping
  odk-sp-review      code-review + verification → evidence/reviews

OpenSpec (ops):
  odk-ops-propose    /opsx:propose → proposal + spec + design + execution-plan
  odk-ops-apply      /opsx:apply → code + code mapping

MatrixSpec (ms):
  odk-ms-proposal      /matspec.proposal → proposal
  odk-ms-delta-spec    /matspec.delta-spec → spec
  odk-ms-delta-design  /matspec.delta-design → design
  odk-ms-tasks         matspec tasks → execution-plan
  odk-ms-validation    matspec validation → evidence/reviews
```

### 使用规则

- 无插件或仅需文档生成 → 使用基础层命令
- 有 Superpowers 且想自动桥接 → 使用 `odk-sp-*` 命令
- 桥接命令不可用时自动回退到基础层对应命令
- 开发者看到的是统一 `odk-` 前缀，基础层和桥接层通过插件缩写区分

对开发者来说，看到的是统一阶段命令；
对系统来说，背后是不同 adapter 的无感协作。

## 如何保证插件输出与 kit 归档匹配

这是设计的核心。

不能只靠"最后人工复制一下"。

必须同时做三件事：

### 1. 生成阶段就使用 kit 模板

插件在生成初稿时，目标模板就应是 kit 的模板，而不是先写通用模板。

这样定制章节从一开始就是必填项。

### 2. 中间产出与最终归档同构

过程交付件和最终归档件的章节结构应尽量一致。

这样：

- 过程输出可直接演化为归档件
- 设计和开发不用做二次改写

### 3. validator 检查交付件与代码映射

最终不只校验文件存在，还要逐步校验：

- `spec.md` 的 AC / 规则是否映射到代码范围
- `execution-plan.md` 的 Task 是否映射到代码范围
- 可选 `evidence/reviews/` 的证据是否能映射回 spec 和 task

## 如何保证过程件与最终交付件一致

这里不应把"过程件"和"归档件"设计成两套完全不同的制品。

更合理的是：

- 过程件是归档件的草稿态
- 归档件是过程件的收口态

所以本质上它们应当是同一份文档在不同阶段的版本，而不是不同文档。

这样才能保证：

- 可追溯
- 可比对
- 可映射到代码

## 是否符合原始诉求

按你现在修正后的目标，这套设计是符合的，前提是守住四条：

1. `ohos-sdd` 作为独立方案，不强行纳入 kit 组合链
2. kit 只管归档 contract、模板 contract、映射 contract
3. 插件过程件和最终归档件尽量同构
4. 代码实现必须能反向追溯到 kit 的交付件

## 模板注入触发点

每个组合模式下，OH 定制模板在什么时候注入到插件工作流中：

### kit + OpenSpec

| 阶段 | 触发点 | 注入内容 | 机制 |
|------|--------|---------|------|
| 初始化 | `ohdk init <id>` | `.codespec/changes/<id>/` 骨架（proposal/spec/design/execution-plan） | ohdk CLI |
| propose | `openspec instructions proposal` | kit proposal 模板（8 必需章节）+ context/rules | ohos-spec-driven schema |
| spec | `openspec instructions specs` | kit spec 模板（9 必需章节）+ rules | ohos-spec-driven schema |
| design | `openspec instructions design` | kit design 模板（10 必需章节 + 2 条件章节）+ context/rules | ohos-spec-driven schema |
| plan | `openspec instructions tasks` | kit execution-plan 模板（10 必需章节） | ohos-spec-driven schema |

### kit + Superpowers

| 阶段 | 桥接命令 | 注入内容 | 机制 |
|------|---------|---------|------|
| 初始化 | `odk-init` | `.codespec/changes/<id>/` 骨架 | CLI / Skill |
| 会话启动 | SessionStart | ODK_ROUTER 轻量路由 | Hook |
| brainstorming | `odk-sp-brainstorm` | kit proposal/spec/design 章节清单 + AC 编号要求 | Wrapper skill |
| writing-plans | `odk-sp-plan` | kit execution-plan 章节清单 + AC-Task 追溯表头 | Wrapper skill |
| implement | `odk-sp-implement` | TDD + subagent 执行 + execution-plan 代码范围映射回填 | Wrapper skill |
| review | `odk-sp-review` | code review + verification → evidence/reviews/ 持久化 | Wrapper skill |

### kit + OpenSpec + Superpowers

可混合使用：Define 阶段用 OpenSpec 的结构化能力，Plan/Implement/Review 阶段用 Superpowers 的执行能力。桥接命令各自独立，可自由组合。

| 阶段 | 选项 A（OpenSpec） | 选项 B（Superpowers） |
|------|-------------------|----------------------|
| proposal/spec/design/execution-plan | `odk-ops-propose`（Schema Override + artifact split） | `odk-sp-brainstorm` + `odk-sp-plan` |
| implement | `odk-ops-apply` | `odk-sp-implement` |
| review | `odk-review`（OpenSpec 无专用 bridge） | `odk-sp-review` |

### kit + MatrixSpec

| 阶段 | 触发点 | 注入内容 | 机制 |
|------|--------|---------|------|
| 初始化 | `ohdk init <id>` | `.codespec/changes/<id>/` 骨架（proposal/spec/design/execution-plan）+ 覆盖模板配置 | ohdk CLI + .matspec-cli/config.yaml |
| 基线恢复 | `matspec generate` | 无额外注入（基线恢复用原生模板） | — |
| proposal | `matspec start` → agent 阶段 | 覆盖模板（含不涉及项确认） | .matspec-cli/config.yaml 模板路径覆盖 |
| delta-spec | `matspec go` → agent 阶段 | 覆盖模板（含兼容性声明 + 验证映射） | 模板路径覆盖 |
| delta-design | `matspec go` → agent 阶段 | 覆盖模板（含验证思路） | 模板路径覆盖 |
| tasks | `matspec go` → agent 阶段 | 覆盖模板（含 AC-Task 追溯 + 代码范围列） | 模板路径覆盖 |
| validation | `matspec go` → agent 阶段 | 覆盖模板（含代码一致性检查） | 模板路径覆盖 |

## 追溯回填时机

每个组合模式下，代码映射追溯链何时回填：

| 追溯项 | kit+OpenSpec | kit+Superpowers | kit+OpenSpec+Superpowers | kit+MatrixSpec |
|--------|-------------|----------------|------------------------|----------------|
| AC 编号创建 | spec 阶段 (OpenSpec spec) | spec 阶段 (wrapper 转写时) | OpenSpec spec 阶段 | delta-spec 阶段 |
| 预期实现范围 | plan 阶段 (execution-plan 代码范围映射预填) | spec 阶段 | OpenSpec spec 阶段 | delta-spec 阶段 |
| AC-Task 关联 | plan 阶段 (tasks.md) | plan 阶段 (writing-plans) | Superpowers plan 阶段 | tasks 阶段 |
| 代码范围（文件级） | plan 阶段 (tasks.md 补充) | plan 阶段 (writing-plans 已有) | Superpowers plan 阶段 | tasks 阶段 (补充) |
| 实际实现文件 | implement 阶段 (回填 spec.md) | implement 阶段 | implement 阶段 | implement 阶段 |
| review 验证证据 | review 阶段 (可选回填 evidence/reviews/) | review 阶段 (可选持久化) | review 阶段 | validation 阶段 (原生) + review 阶段补充 |
| 追溯交叉检查 | validator Phase 2 | validator Phase 2 | validator Phase 2 | validation.md 原生 + validator 补充 |

## 无缝无感实现路径

### 使用基础层（无插件依赖）

```
开发者输入： "实现 ArkUI 组件 XYZ 的焦点管理能力"
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  odk-init + odk-propose                                 │
│  背后：模板驱动，按 proposal.md 模板逐项填写             │
│  开发者看到：proposal.md 已生成（含 8-dim N/A）          │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  odk-spec                                               │
│  背后：模板驱动，按 spec.md 模板生成                     │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  odk-design                                             │
│  背后：模板驱动，按 design.md 模板生成                   │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  odk-plan                                               │
│  背后：模板驱动，按 execution-plan.md 模板生成           │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  odk-implement                                          │
│  背后：AI 辅助逐 Task 实现，回填 code mapping             │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  odk-review + odk-validate                              │
│  背后：模板驱动 review + Level A/B/C/D 校验             │
└─────────────────────────────────────────────────────────┘
```

### 使用桥接层（ODK + Superpowers，一条命令）

```
开发者输入： "使用 ODK 完成 ArkUI 焦点管理"
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  ODK + Superpowers 桥接工作流                            │
│                                                         │
│  Step 1: odk-sp-brainstorm → Superpowers brainstorming  │
│          → proposal + spec + design 写入 .codespec/     │
│                                                         │
│  Step 2: odk-sp-plan → Superpowers writing-plans        │
│          → execution-plan + AC-Task 追溯                 │
│                                                         │
│  Step 3: odk-sp-implement → Superpowers TDD + subagent  │
│          → 代码实现 + code mapping 回填                  │
│                                                         │
│  Step 4: odk-sp-review → Superpowers review + verify    │
│          → evidence/reviews/ 持久化                     │
│                                                         │
│  Step 5: odk-validate → Level A/B/C/D 校验              │
└─────────────────────────────────────────────────────────┘
```

### 开发者不需要感知的内容

- 底层用的是 Superpowers 还是仅模板驱动
- 模板是如何注入到阶段产物中的
- 桥接命令内部的重定向和格式转换
- AC-Task 追溯表何时被回填

### 开发者必须显式确认的内容

| 确认项 | 时机 | 原因 |
|--------|------|------|
| target_release | proposal 阶段 | 需人类判断版本规划 |
| 不涉及项确认（8 维度 N/A） | proposal 阶段 | 需人类逐项确认 |
| 各阶段审批 | 每阶段出口 | 需人类判断质量 |

## 插件间产物合并规则

当多个插件产出同一文档的不同部分时：

### 合并优先级

| 文档 | 结构来源 | 内容优先级 | 说明 |
|------|---------|-----------|------|
| proposal.md | OpenSpec（若启用） | 两者合并：OpenSpec 主导 Why/What，Superpowers 补充边界探索 | OpenSpec 结构更完整 |
| design.md | OpenSpec（若启用） | 两者合并：OpenSpec 主导 Decisions，Superpowers 补充风险/验证 | OpenSpec 有方案对比表 |
| spec.md | OpenSpec（若启用） | OpenSpec 主导业务规则，Superpowers 补充边缘场景 | OpenSpec 结构更系统 |
| execution-plan.md | Superpowers（若启用） | Superpowers 主导（Task 粒度和文件边界更精确） | Superpowers plan 结构更强 |
| evidence/reviews/ (optional) | Superpowers（若启用） | Superpowers 主导（code review + verification 更系统） | Superpowers review 纪律更强 |

### 合并冲突解决

1. **同章节不同结论**: 以人工确认的 kit 归档件为准
2. **不同粒度**: 以更细粒度为准（Superpowers plan 的 Task 粒度通常优于 OpenSpec tasks）
3. **不同格式**: 以 kit 模板格式为准，插件差异在转换阶段消除

### 禁止的合并模式

- 两个插件各自维护独立归档根（OpenSpec `openspec/` + Superpowers `docs/superpowers/` 同时存在作为正式归档）= 双主线，禁止
- 同一 Task 在两个插件中有不同完成判据 = 分歧，合并到 kit 文档时必须有唯一结论
- 两个插件的 review 结论不一致 = 必须人工裁决，不可各自保留
