# OpenHarmony Template Source

本目录是 OpenHarmony SDD 公共交付模板真相源，包含 4 阶段主工作流、通用条件旁路模板 + CLAUDE.md + manifest.md。Profile 专属格式放在 `openharmony/profiles/<name>/templates/`。

运行时 `{{ASSET_ROOT}}/templates/` 由打包工具从本目录生成；如存在差异，以本目录为准。

## 模板列表

| 模板 | 用途 | 阶段 |
|------|------|------|
| `proposal.md` | 需求澄清与基线（三合一） | Phase 1: 定义 |
| `spec.md` | 特性规格 | Phase 2: 规格说明 |
| `scenario-library.md` | Gherkin 场景库 | Phase 2: 规格说明 |
| `design.md` | 架构设计 | Phase 3: 设计 |
| `execution-plan.md` | 执行计划 + 交接 | Phase 4: 计划 |
| `task.md` | 任务规格 | Phase 4: 计划 |
| `epic.md` | Epic 规格（跨 SIG/跨仓） | Phase 1-2 |
| `bugfix.md` | 缺陷修复规格 | Define/Plan 跨阶段旁路 |
| `test-spec.md` | 集成/系统测试规格 | Plan 期测试设计旁路 |
| `regression-test.md` | 回归测试 | Plan 之后的验证动作 |
| `review.md` | 统一审查（四合一） | Plan 之后的审查动作 |
| `gate-checklist.md` | 阶段检查清单 | 阶段切换 |
| `CLAUDE.md` | AI Agent 指令模板 | 全局 |
| `manifest.md` | 工作项清单 | 全局 |

## 同步源

公共模板以 `openharmony/templates/` 为唯一源；Profile 专属模板以 `openharmony/profiles/<name>/templates/` 为唯一源。更新后运行 `bash packaging/build.sh` 刷新运行时模板。
