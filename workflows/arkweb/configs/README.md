# ArkWeb SDD 工作流配置

本目录包含 ArkWeb SDD（Spec-Driven Development）工作流的配置文件。

## 工作流

### arkweb-sdd-code-gen.yaml

ArkWeb 全流程工作流：从需求澄清到代码生成的完整 SDD 流程。

**流程阶段：**

| Phase | 名称 | 说明 |
|-------|------|------|
| 1 | 需求澄清 | 接收需求，生成 proposal.md |
| 2 | 需求分析 | 专家团讨论 + brainstorm + code-analysis |
| 3 | 需求基线 | 追加 proposal.md 基线章节 |
| 4 | 设计文档 | 生成 requirement.md + design.md |
| 5 | 文档评审 | 技术评审 + Checklist 33 项检视 |
| 6 | 规格生成 | 生成 spec.md + task.md |
| 7a | 代码实现 | Spec 驱动代码实现 |
| 7b | 代码检视 | 8 维度检视 + 修复循环 |
| 7c | 设计差异对齐 | design.md 与实现比对 |
| 7d | 编译验证 | 编译-修复循环 |

**模式：** 状态机（state-machine），支持回退和条件分支。

## 目录结构

```
configs/
├── arkweb-sdd-code-gen.yaml   # 主工作流
├── agents/                     # Agent 配置
│   ├── arkweb-architect.yaml
│   ├── arkweb-brainstorm.yaml
│   ├── arkweb-builder.yaml
│   ├── arkweb-code-analysis.yaml
│   ├── arkweb-code-gen.yaml
│   ├── arkweb-design-doc.yaml
│   ├── arkweb-spec-gen.yaml
│   └── arkweb-spec-review.yaml
├── models/
│   └── models.yaml             # 模型配置
└── README.md
```

## Skills

工作流依赖的 skills 位于 `../skills/` 目录，包括：

- **核心 SDD skill：** arkweb-architect、arkweb-brainstorm、arkweb-code-analysis、arkweb-design-doc、arkweb-spec-review、arkweb-spec-gen、arkweb-code-gen、arkweb-committer-review、arkweb-design-alignment、arkweb-preflight
- **专家团：** 10 个 arkweb-expert-*（性能、多媒体、外设、交互安全、渲染、合成、交互运动、网络、JS 引擎、稳定性）
- **辅助：** oh-chromium-knowledge、chromium-docs、gitcode-pr
- **共享知识库：** _shared/
