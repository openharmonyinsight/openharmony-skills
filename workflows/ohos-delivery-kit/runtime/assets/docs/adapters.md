# Adapters

> **Source of truth**: 精确 adapter 命令、产物映射、`required_backfill` 和 fallback 声明维护在
> `core/adapters/*.yaml`。本文只解释设计意图、质量边界和无法使用桥接命令时的人工兜底方式。

ODK adapter 的目标不是替代 OpenSpec、Superpowers 或 MatrixSpec，而是把它们的阶段产物收口到统一的
`.codespec/changes/<change-id>/` 归档契约。最终交付质量仍由 ODK 模板、`core/contracts/artifacts.yaml` 和
`odk-validate` 负责。

## 当前适配器

| Adapter | 声明文件 | 状态 | 推荐命令 |
|---------|----------|------|----------|
| Superpowers | `core/adapters/superpowers.yaml` | supported | `odk-sp-*` |
| OpenSpec | `core/adapters/openspec.yaml` | supported | `odk-ops-*` |
| MatrixSpec | `core/adapters/matrixspec.yaml` | experimental | `odk-ms-*` |

`ohos-sdd` 不属于当前 kit 组合链，是独立平行方案；后续如需对齐，应单独定义 adapter 声明。

## 质量边界

Adapter 可以做三件事：

- 调用外部插件能力，例如 `/opsx:propose`、`brainstorming`、`/matspec.delta-spec`。
- 将外部产物重定向或转换到 `.codespec/changes/<change-id>/`。
- 根据 `required_backfill` 补齐 ODK 专属字段。

Adapter 不应该做三件事：

- 不宣布归档合规；合规只由 ODK validator 判断。
- 不维护 artifact 章节清单；章节契约只放在 `core/contracts/artifacts.yaml` 和模板中。
- 不把 OpenSpec/Superpowers/MatrixSpec 规则写回基础 `odk-*` 命令，避免基础命令被桥接能力污染。

这个边界与 [source-boundary-and-distribution.md](designs/source-boundary-and-distribution.md) 一致：
adapter YAML 维护桥接映射，skills/commands 维护调用和 fallback，templates 维护最终文档质量。

## 推荐使用方式

优先使用桥接命令，不手工复制外部产物。

| 场景 | 推荐路径 | 说明 |
|------|----------|------|
| 已使用 Superpowers 工作流 | `odk-sp-brainstorm` -> `odk-sp-plan` -> `odk-sp-implement` -> `odk-sp-review` | 强执行纪律和 review，但需要拆分 brainstorming 产物到 proposal/spec/design |
| 已使用 OpenSpec 结构化变更 | `odk-ops-propose` -> `odk-ops-apply` | 适合 delta spec 和 tasks 草拟，ODK 负责完整归档回填 |
| Brownfield 基线恢复 | `odk-ms-proposal` -> `odk-ms-delta-spec` -> `odk-ms-delta-design` -> `odk-ms-tasks` -> `odk-ms-validation` | 适合存量项目恢复和分层变更，当前仍为 experimental |

桥接命令必须遵守 `core/adapters/*.yaml` 中的 fallback chain。外部插件不可用时，命令应退回基础
`odk-*` 命令，并明确告知用户发生了能力降级。

## 人工兜底流程

当桥接命令不可用，只能手工迁移外部产物时，按下面流程处理：

1. 先创建 `.codespec/changes/<change-id>/` 骨架，确保目标路径符合 `core/contracts/artifacts.yaml`。
2. 根据对应 adapter YAML 的 `mapping.<artifact>.source` 找到外部源产物。
3. 将内容转换到 ODK 模板，而不是保留外部模板结构。
4. 按 `required_backfill` 补齐缺口字段；无法确认的值标记为 `TBD` 并在下一阶段解决。
5. 运行 `odk-validate` 或项目验证脚本，确认 required sections、traceability 和 evidence 路径。

人工兜底只用于恢复工作流，不应成为常规使用路径。若某个 adapter 经常需要人工兜底，应优先改桥接
skill 或 adapter YAML，而不是扩写本文档。

## Adapter 差异

### Superpowers

Superpowers 的优势是执行纪律：brainstorming、writing-plans、TDD、code review 和 completion verification。
它的主要缺口是持久化 artifact 不是 ODK 结构，所以 `odk-sp-*` 需要把会话/计划/review 结果拆分并持久化。

关键规则：

- Brainstorming 输出应先拆成 `proposal.md` 和 `spec.md`，再生成或完善 `design.md`。
- Writing-plans 的文件级任务边界应映射到 `execution-plan.md` 的 Task scope。
- Review 和 verification 结果应落到 `evidence/reviews/`，而不是只留在会话上下文中。

### OpenSpec

OpenSpec 的优势是 structured proposal、delta spec 和 tasks。它的主要缺口是 ODK 专属字段，例如
`target_release`、8 维 N/A 确认、兼容性声明、AC 编号、代码映射和 AC-to-Task 追溯。

关键规则：

- OpenSpec delta spec 可以作为 `spec.md` 的输入，但最终归档必须是 ODK 完整 spec。
- `tasks.md` 只能作为 execution plan 草稿，必须补齐 AC-to-Task、file scope 和验证实际结果。
- `/opsx:apply` 只能辅助实现，不能跳过 `execution-plan.md` 的代码范围映射和验证实际结果（actual results）回填。

### MatrixSpec

MatrixSpec 的优势是 brownfield 基线恢复、delta design 和 validation。它仍处于 experimental 状态，原因是其
任务和验证结构与 ODK 的 AC 追溯链不完全一致。

关键规则：

- `delta-spec` 中的业务规则必须转换成 ODK 的 WHEN/THEN AC。
- `tasks` 的分层任务必须补齐到文件级 scope，并建立 AC-to-Task 追溯。
- `validation` 可作为 evidence 输入，但不能替代 ODK 的 spec-compliance、code-quality、verification 结论。

## 模板注入原则

不同平台安装方式不同，因此 adapter 不直接假设同一物理路径：

- 三端 packaging 均物化 `templates/`、`contracts/`、`adapters/`（OpenCode 落在 `.opencode/ohos-delivery-kit/`，运行时由 JS 插件用 `import.meta.url` 定位）。
- OpenCode 的 bootstrap 由 JS 插件经 `messages.transform` hook 注入 `using-odk/SKILL.md`；命令层为薄包装，不再依赖 `opencode.md`。
- 所有平台的最终 artifact 仍写入 `.codespec/changes/<change-id>/`。

因此，bridge skills/commands 应只引用 `{{PLUGIN_ROOT}}` 或平台约定的插件根，不在文档中硬编码本地安装路径。

## 验证

Adapter 相关 drift 由以下脚本兜底：

```bash
bash scripts/validate-openspec-bridge.sh
bash scripts/validate-matspec-bridge.sh
bash scripts/validate-superpowers-bridge.sh
bash scripts/validate-distribution.sh --skip-determinism
```

这些脚本应读取 `core/adapters/*.yaml`，避免再维护一份独立命令清单。
