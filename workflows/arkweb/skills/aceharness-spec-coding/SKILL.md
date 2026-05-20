---
name: aceharness-spec-coding
description: ACEHarness Spec Coding skill for spec-first planning and implementation. Turns rough requirements into structured requirements, design, and implementation plans. Creates requirements.md (user stories + WHEN/THEN acceptance criteria), design.md (architecture + interfaces + pseudocode), and tasks.md (multi-level nested task lists with requirement tracing).
descriptionZH: ACEHarness Spec Coding 规范编码技能。将粗需求转化为结构化的需求文档、设计文档和实现计划。生成 requirements.md（用户故事 + WHEN/THEN 验收标准）、design.md（架构 + 接口 + 伪代码）和 tasks.md（多级嵌套任务列表 + 需求追溯）。
tags:
  - ACEHarness Spec Coding
  - Requirements
  - Design
  - Tasks
  - Planning
---

# ACEHarness Spec Coding

将粗需求转化为可审查、可实现、可验证的正式规范制品，并在实现阶段按规范推进。

## 制品体系

| 制品 | 用途 | 质量标准 |
| --- | --- | --- |
| `requirements.md` | 用户故事 + 验收标准 | 每个需求有用户故事 + WHEN/THEN 验收标准 |
| `design.md` | 架构 + 接口 + 伪代码 | 至少 1 个架构图 + 组件接口 + 关键决策表 |
| `tasks.md` | 多级嵌套实现计划 | 多级 checkbox + 需求追溯 + 检查点 |

## 工作流程

### 阶段 1：需求文档 (requirements.md)

**输入：** 用户需求描述、已有代码上下文

**过程：**
1. 从用户输入和代码中提取已知事实
2. 针对会改变实现和验收的关键问题进行访谈
3. 将需求结构化为用户故事 + WHEN/THEN 验收标准

**输出：** `requirements.md`

**质量标准：**
- 每个需求包含用户故事（作为<角色>，我希望<目标>，以便<价值>）
- 每个需求包含 WHEN/THEN 格式的验收标准
- 包含术语表，统一关键概念定义

**示例：**

```markdown
### 需求 1：多语言构建支持

**用户故事：** 作为文档维护者，我希望通过一条命令同时构建多个语言版本，以便减少重复操作。

#### 验收标准

1. WHEN 用户传入逗号分隔的配置文件路径 THEN 系统解析为多个独立配置
2. WHEN 任一配置缺少 i18n.target 字段 THEN 系统报错并停止构建
3. WHEN 所有配置验证通过 THEN 系统为每个语言生成独立输出目录
```

### 阶段 2：设计文档 (design.md)

**输入：** `requirements.md`

**过程：**
1. 确定核心设计原则
2. 绘制架构图（Mermaid）
3. 定义组件接口和伪代码
4. 记录关键决策及理由

**输出：** `design.md`

**质量标准：**
- 包含 Mermaid 架构图或数据流图
- 每个核心组件有接口定义和伪代码
- 关键决策表包含选择、理由和替代方案

### 阶段 3：实现计划 (tasks.md)

**输入：** `requirements.md` + `design.md`

**过程：**
1. 将设计拆解为可执行的多级任务
2. 每个子任务引用对应需求编号
3. 在关键节点插入检查点

**输出：** `tasks.md`

**质量标准：**
- 使用多级嵌套 checkbox（顶层任务 → 子任务 → 步骤描述）
- 每个子任务通过 `_需求：x.x_` 引用对应需求
- 包含检查点任务用于增量验证

**示例：**

```markdown
- [ ] 1. 更新命令行参数解析
  - [ ] 1.1 修改 CLI 参数解析器
    - 更新 --config 参数以接受逗号分隔的文件路径
    - 实现路径分割和空白字符修剪逻辑
    - _需求：1.1, 1.2_

  - [ ] 1.2 添加参数验证
    - 检查配置文件数量限制
    - 验证文件路径存在性
    - _需求：1.3_

- [ ] 2. 检查点 - 确保参数解析测试通过
  - 确保所有测试通过，如有问题请询问用户。
```

## 需求访谈

在写制品之前，先从上下文推断已知事实，再针对性提问。

**核心维度：**
1. **目标与价值：** 谁需要这个变化，成功后可观察结果是什么
2. **当前行为与目标行为：** 现在如何运行，目标如何变化
3. **范围与非目标：** 本次包含和排除什么
4. **兼容与迁移：** 旧数据、旧配置是否需要继续可用
5. **验证方式：** 用什么命令、测试或人工验收证明完成

**提问原则：**
- 先吸收用户已说过的内容，不重复提问
- 只问会影响实现策略或验收标准的问题
- 给具体选项并允许补充，避免空泛问题

## 目录结构

```
specs/<domain>/
├── requirements.md
├── design.md
└── tasks.md
```

## 模板

- `skills/aceharness-spec-coding/templates/requirements.md`
- `skills/aceharness-spec-coding/templates/design.md`
- `skills/aceharness-spec-coding/templates/tasks.md`

## 校验

```bash
node skills/aceharness-spec-coding/scripts/validate-spec-coding.mjs <spec-root>
```

校验内容：
- `requirements.md` 包含需求标题和 WHEN/THEN 验收标准
- `design.md` 包含架构图、组件接口和关键决策
- `tasks.md` 包含多级嵌套 checkbox 和需求引用

## 持久化 Spec 模式

当工作流配置 `specCoding.persistMode: 'repository'` 时，spec 制品持久化到仓库 `specCoding.specRoot` 指定的目录（默认 `<workingDirectory>/.spec`）。

### 目录结构
- `<specRoot>/spec.md` — 总 spec（master，输入文件）
- `<specRoot>/checklist.md` — 预存问题清单（输入文件）
- `<specRoot>/specs/<workflowName>-<runId>/` — 每次运行的 delta 快照（requirements.md、design.md、tasks.md）

### AI 规则

- **审查时**：检查 `<specRoot>/checklist.md`，所有未回答问题（`- [ ]`）需要在人工审批或 supervisor 审查时提出；已回答的问题以 `- [x]` 表示
- **修订制品时**：直接更新 requirements/design/tasks 对应 artifacts 的正文，保持三份制品之间的术语、范围和需求追溯一致
- **制品格式**：checklist.md 使用 `- [ ] 问题内容` 格式，每行一个问题
