# ohos-delivery-kit

`ohos-delivery-kit` (ODK) 是一个面向 OpenHarmony 的轻量化交付件规范层。它定义最终归档产物的最小章节契约，同时允许选择不同插件来生成这些产物。

**核心理念**：先定义必须沉淀什么，再决定用什么工具生成。

## 设计目标

- 提供轻量、稳定、插件无关的 OpenHarmony 交付件规范
- 业务仓输出统一收敛到 `.codespec/`
- 保留 OpenHarmony 特有约束（`target_release`、8 维 N/A 确认）
- 允许 Superpowers / OpenSpec / MatrixSpec 等插件与 ODK 组合使用

## 非目标

- 不重新实现完整的流程编排器
- 不绑定特定 Agent、平台或 slash command 体系
- 不要求所有团队采用同一种写作风格

## 快速上手

参见 [docs/quick-start.md](docs/quick-start.md)

## 安装与分发

- **开发仓本地安装**：`scripts/install-{claude,codex,opencode}.sh`（三端持久化；Claude 亦支持会话级 `claude --plugin-dir dist/claude`，活跃开发 live-reload）。
- **发布仓安装**（[`ohos-marketplace`](https://gitcode.com/oshunter/ohos-marketplace)——当前为测试/过渡发布仓，正式发布仓与路径待定）：Claude/Codex 走 `plugin marketplace add` + `plugin install`；OpenCode 走 clone 发布仓 + `./scripts/install-opencode.sh <target>`。三端产物已同步 0.6.5。

详见 [quick-start.md](docs/quick-start.md)。

## 仓内结构

```
ohos-delivery-kit/
├── README.md
├── HANDOFF.md                         # 会话交接：当前状态 + 技术债 + TODO
│
├── core/                              # 平台无关的核心
│   ├── contracts/                     # 交付件契约声明（artifact 真相源）
│   │   └── artifacts.yaml             # 必需产物、章节、依赖、证据策略
│   ├── adapters/                      # 插件桥接声明（映射 + fallback）
│   │   ├── superpowers.yaml
│   │   ├── openspec.yaml
│   │   └── matrixspec.yaml
│   ├── templates/                     # 交付件模板（章节和表头定义）
│   │   ├── ai/                        # AI 生成模板: proposal/spec/design/execution-plan
│   │   └── review/                    # 评审模板: spec-compliance/code-quality/verification
│   ├── skills/                        # 阶段技能（canonical source）
│   │   ├── using-odk/SKILL.md        # ODK 路由 + Phase-Artifact Mapping + Profile Detection
│   │   ├── odk-*/SKILL.md              # 基础层命令（模板驱动，零插件依赖）
│   │   └── odk-{sp,ops,ms}-*/SKILL.md  # 桥接层命令（对接外部插件）
│   ├── rules/delivery/                # 规则: ID 格式、OH 元数据、校验清单
│   └── profiles/                      # 子系统分层定制（arkui/arkgraphic/arkweb/arkruntime）
│       ├── <id>.yaml                  # Profile 声明
│       └── fragments/                 # 按 phase 加载的模板片段
│
├── docs/                              # 设计文档
│   ├── architecture.md                # 三层架构设计
│   ├── contracts.md                   # 最小交付件契约
│   ├── adapters.md                    # 适配器映射（OpenSpec/Superpowers/MatrixSpec）
│   ├── workflows.md                   # 插件组合模式
│   ├── template-injection.md          # 模板注入机制
│   ├── code-traceability.md           # 代码追溯链
│   ├── validator.md                   # 统一校验器设计
│   ├── quick-start.md                 # 快速上手指南
│   ├── user-guide.md                  # 端到端使用指南
│   ├── security-guide.md              # 安全检查与威胁建模指南
│   ├── mvp-plan.md                    # MVP 实施计划
│   └── designs/                       # 设计决策记录
│
├── packaging/                         # 三平台静态安装壳
│   ├── claude/                        # Claude Code manifest/hooks/README
│   ├── codex/                         # Codex CLI manifest/hooks/README
│   └── opencode/                      # OpenCode package.json/plugins/ohos-delivery-kit.js/README 静态输入
│
├── dist/                              # 生成的安装产物（由 distribute-skills.sh 重建，不提交）
│   ├── claude/                        # Claude Code 可安装插件包
│   ├── claude-marketplace/            # 本地 Claude marketplace（install-claude.sh 持久化安装用）
│   ├── codex/                         # Codex CLI 可安装/手动复制包
│   └── opencode/                      # OpenCode project-local 拷贝源
│
├── scripts/                           # 分发和安装脚本
│   ├── distribute-skills.sh
│   ├── install-{claude,codex,opencode}.sh
│   ├── uninstall-{claude,codex,opencode}.sh
│   ├── validate-*.sh
│   └── test-*-install.sh
│
└── examples/                          # 完整样例
    └── issue-12345-arkui-focus/
```

## 维护边界

`core/` 是规范真相源：

- `core/contracts/artifacts.yaml` 定义最终归档件、必需章节、依赖和证据策略
- `core/templates/` 定义交付件正文骨架和表头
- `core/profiles/` 只做 OpenHarmony 子系统的加法式扩展
- `core/adapters/` 定义 Superpowers / OpenSpec / MatrixSpec 到 ODK 的映射和回退
- `core/skills/` 只负责阶段路由、上下文加载、桥接调用和平台无关行为约束

`packaging/` 是平台静态安装壳。Claude、Codex、OpenCode 的安装形态不同，生成后的 skills/templates/profiles/contracts/adapters 由 `scripts/distribute-skills.sh` 输出到 `dist/`，不应成为契约或模板的人工维护真相源。

## 最终业务仓输出

```
.codespec/changes/issue-<number>-<slug>/
├── proposal.md
├── spec.md
├── design.md
└── execution-plan.md
```

`reviews/` 和 `gates/` 属于过程证据，不属于最小归档合同。如需保留，建议放在 `evidence/reviews/` 和 `evidence/gates/`。

## 相关文档

| 文档 | 内容 |
|------|------|
| [quick-start.md](docs/quick-start.md) | 安装、命令、与 Superpowers/OpenSpec/MatrixSpec 融合 |
| [user-guide.md](docs/user-guide.md) | 新需求端到端使用说明、命令分层、插件组合选择 |
| [architecture.md](docs/architecture.md) | 三层架构设计 |
| [contracts.md](docs/contracts.md) | 最小交付件契约 |
| [adapters.md](docs/adapters.md) | 适配器映射（章节覆盖度、缺口回填） |
| [workflows.md](docs/workflows.md) | 插件组合模式 |
| [security-guide.md](docs/security-guide.md) | 安全基础检查、STRIDE、合规与安全最佳实践 |
| [template-injection.md](docs/template-injection.md) | 模板注入机制（Mode A/B/C） |
| [code-traceability.md](docs/code-traceability.md) | AC→Task→code→commit→review 追溯链 |
| [validator.md](docs/validator.md) | 统一校验器（Level A/B/C/D） |
| [core/profiles/README.md](core/profiles/README.md) | Profile 系统文档 |
