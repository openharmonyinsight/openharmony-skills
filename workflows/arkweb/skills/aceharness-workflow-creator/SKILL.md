---
name: aceharness-workflow-creator
description: Aceharness 工作流配置文件创建技能。
descriptionZH: AceHarness 工作流配置文件创建技能。【触发场景】每当用户提到：创建工作流、配置
  workflow、新建工作流、写工作流配置、设置 agent 执行流程、state-machine/phase-based 工作流。生成前必须用验证脚本校验
  YAML 格式和 agent 引用有效性，不要跳过验证直接生成。
tags:
  - 工作流
  - 配置
  - 创建
  - 对话
---

# Aceharness Workflow Creator

Aceharness 工作流配置文件创建技能。**每当用户提到以下任何场景时，必须调用此 skill：**
- 「创建一个工作流」「配置一个 workflow」「新建工作流」
- 「帮我写个工作流配置」「生成工作流 yaml」
- 「设置 agent 执行流程」「配置 agent 步骤」
- 「创建 state-machine 工作流」「创建 phase-based 工作流」
- 工作流模式选择（状态机 vs 阶段式）
- 修改已有工作流配置时的格式检查

**生成工作流配置前必须用验证脚本校验格式，确保 YAML 语法正确、agent 引用存在于运行时 `configs/agents/` 目录、状态机/阶段模式结构完整。不要在没有调用此 skill 的情况下直接生成工作流配置文件。**

## 工作流模式

**除非用户提出要求，否则尽量帮助用户创建state-machine（状态机模式）的工作流**
**除非用户明确拒绝或场景不适用，否则尽量在方案中启用红蓝对抗机制（红队产出、蓝队挑战、裁判仲裁）**

## 建模原则

- 默认把复杂研发流程建模为 `state-machine`
- 一个 node（即一个 state）表示一个业务阶段，例如“设计”“实施”“测试”“构建”
- 红队、蓝队、黄队（judge）在默认设计里是**同一个 node 内的多个 steps**，不是拆成多个 node
- 不要把“设计蓝队”“设计红队”“设计裁判”各自拆成独立状态；正确做法是一个“设计”状态下包含多个步骤
- 不要把“实施蓝队”“实施红队”“实施裁判”各自拆成独立状态；正确做法是一个“实施”状态下包含多个步骤
- `requireHumanApproval` 是 state 级能力，应该挂在需要人工把关的 state 上，而不是某个单独 step 上
- 默认情况下，“设计”与“代码实施/实施”都应设置 `requireHumanApproval: true`
- `context.workspaceMode` 用于决定执行前是否创建工作区副本：`in-place` 表示直接在 `context.projectRoot` 指向的工作区执行，`isolated-copy` 表示先复制一份隔离工程再执行
- 若用户没有明确要求隔离副本，新建工作流时优先推荐 `context.workspaceMode: in-place`；只有用户明确要求隔离执行、避免污染原目录时才使用 `isolated-copy`

推荐结构示意：

```yaml
workflow:
  mode: state-machine
  states:
    - name: 设计
      requireHumanApproval: true
      steps:
        - name: 方案设计
          role: defender
        - name: 方案挑战
          role: attacker
        - name: 设计评审
          role: judge
    - name: 实施
      requireHumanApproval: true
      steps:
        - name: 编码实施
          role: defender
        - name: 代码审查
          role: attacker
        - name: 实施评审
          role: judge
```

### state-machine（状态机模式）
- 有且仅有一个 `isInitial: true` 的初始状态
- 至少有一个 `isFinal: true` 的最终状态
- 所有 `transition.to` 必须指向已定义的状态名
- 关键阶段优先按“一个状态 + 多个步骤”的方式建模
- 设计类状态、代码实施类状态默认开启 `requireHumanApproval: true`

### phase-based（阶段模式）
- 至少一个 phase，每个 phase 至少一个 step
- step 中的 agent 引用必须在运行时 `configs/agents/` 中存在
- 如果用户坚持使用 phase-based，也应沿用“一个 phase 承载该阶段的多步骤协作”的思路，不要为了红蓝黄角色拆碎阶段

## 并发设计元数据

并发、多 Agent 多实例、channel、join policy 属于 workflow YAML / workflow 设计层。它们用于表达编排意图和未来运行调度元数据，不能在当前执行器尚未支持真实并发时承诺实际并行执行。

当 workflow step 之间相互独立、没有共享写冲突、没有人工审批依赖时，可以在 workflow YAML 中表达并发设计：

- workflow 级：`workflow.concurrency.agentInstances`、`workflow.concurrency.channels`、`workflow.concurrency.joinPolicies`
- step 级：`step.parallelGroup`、`step.concurrency.groupId`、`step.concurrency.branchId`、`step.concurrency.joinPolicy`、`step.agentInstanceId`、`step.channelIds`
- spec 追踪：`step.specTaskBinding` 仅用于把 workflow step 绑定到已有 spec task，便于运行态追踪和审查

依赖关系不清晰、有共享写冲突、需要人工审批先后顺序，或任务之间存在明确产物依赖时，保持串行建模。

## 验证脚本

```bash
node /absolute/path/to/skills/aceharness-workflow-creator/scripts/validate-workflow.mjs <config.yaml>
```

验证内容：YAML 语法、agent 引用存在性、状态机/阶段模式结构完整性。

## 核心流程

1. **收集需求** — 了解要解决的问题、涉及模块、验收标准
2. **查询资源** — `agent.list` 查看可用 Agent，`config.list` 参考已有工作流
3. **确认关键信息** — 工作目录、需求描述、代码目录（用户确认后再设计）
   - 必须确认 `context.workspaceMode`：是直接在工作目录执行（`in-place`），还是先复制副本再执行（`isolated-copy`）
4. **设计方案** — 默认优先给出“按阶段建模的红蓝对抗”版本：每个关键阶段先定义 node/state，再在该 node 内放入红队、蓝队、裁判多个步骤；“设计”和“实施”默认开启人工审批；如用户要求简化再降级为普通流程；用 card 展示方案预览，确认后再写入
5. **写入 + 验证** — 必须运行验证脚本，优先使用脚本绝对路径；配置文件参数优先传运行时根目录下的相对路径，例如：`node /absolute/path/to/skills/aceharness-workflow-creator/scripts/validate-workflow.mjs configs/{filename}.yaml`

**绝对不要在展示方案的同一条回复中创建文件，必须等用户确认。**
**当不确定某个工作流或步骤应该挂哪些 `skills` 时，优先保持 `context.skills` 或 `step.skills` 为空，让运行时自动获得工作区可用的全部 skill 能力，而不是猜测性地填错 skill。**

## Agent 团队

- **defender（红队）** — 建设者：设计、实现、测试、文档
- **attacker（蓝队）** — 挑战者：攻击方案、寻找缺陷、压力测试
- **judge（裁判）** — 仲裁者：评审和判定

## 红蓝对抗（默认优先）

- 创建工作流时，默认优先提供带红蓝对抗机制的方案，但不是强制；若用户明确不需要，可切换为普通流程
- 红蓝黄的正确建模单位是“同一阶段内的多步骤协作”，不是“按角色拆多个 node”
- 推荐最小闭环是在单个关键阶段内组织 `defender -> attacker -> judge`，需要修复时再回到同一阶段或上游阶段
- “设计”阶段推荐结构：`defender(方案设计) -> attacker(方案挑战) -> judge(设计评审)`，并设置 `requireHumanApproval: true`
- “实施”阶段推荐结构：`defender(编码实施) -> attacker(代码审查/攻击实现) -> judge(实施评审)`，并设置 `requireHumanApproval: true`
- 如需补充修复动作，应作为同一 state 内的后续步骤或通过 transition 回到该 state，而不是为了红蓝黄角色扩张状态数量
- 适用场景：复杂需求、质量门禁、上线前评审；简单脚本类任务可在用户确认后简化

## 示例模板

以下模板是业务无关的通用骨架，可直接参考。完整 YAML 见 `templates/` 目录。

### 功能开发（红蓝对抗）

**文件：** `templates/feature-dev.yaml.md`

适用于新功能开发、重构、迁移等需要设计→实施→验证的场景。

```
状态流：设计 → 实施 → 验证 → 完成（异常 → 终止）
```

### Bug 修复

**文件：** `templates/bug-fix.yaml.md`

适用于 bug 修复、crash 分析、性能问题排查。

```
状态流：复现确认 → 根因分析 → 修复实现 → 回归验证 → 完成（异常 → 终止）
```

### 分析审计

**文件：** `templates/analysis-audit.yaml.md`

适用于代码审计、安全分析、技术调研。

```
状态流：数据收集 → 深度分析 → 交叉验证 → 报告输出 → 完成
```
