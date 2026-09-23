## Archive Structure

All delivery artifacts are archived under:

```
codespec/changes/<repo-name>/<req-id>/
codespec/changes/<repo-name>/draft-<yyyymmdd>-<english-slug>/
```

Resolve `<repo-name>` from the Git `origin` URL basename without `.git`; if `origin` is unavailable, use the Git worktree root directory name. A formal directory leaf is exactly `req-id`; the English slug exists only while the change is a draft.

Each change directory is **populated by phase** — `odk-init` only seeds `proposal.md` as a frontmatter stub; the other main docs appear when their phase first runs (a missing main doc before its phase is expected, not an error):
- `proposal.md` — (`odk-init` stub → `odk-propose` fills) requirements proposal with triage, 1+8 device variation, external dependencies, success criteria, and impact scope (YAML frontmatter with `target_release`)
- `spec.md` — (`odk-spec`) functional specification with WHEN/THEN AC, error codes, and verification mapping
- `design.md` — (`odk-design`) architecture design with Mermaid diagrams and decision comparison (references spec ACs)
- `execution-plan.md` — (`odk-plan`) implementation plan with AC-Task traceability and task details
- `spec-for-validation.md` — optional validation specification with integration/system scenarios derived from spec.md (parallel bypass, does not block main flow)
- `threat-model.md` — optional deep threat analysis (bypass; high-risk security/privacy/compliance changes; produced by `odk-security-threat-model`)
- `metadata_tracking.yaml` — generated or refreshed by `odk-submit-design-docs` when the formal five-base-file bundle plus required conditional evidence is submitted to design-docs; it may use `pull_requests: []` before a business-code PR exists

The recommended phase order is **Propose → Specify → Design → Plan → Implement**. Spec defines WHAT (behavior, ACs, business rules); Design defines HOW (architecture, error code values, interface signatures). Design references specific AC numbers from Spec, strengthening the traceability chain. After design, review and update spec's error codes and interfaces if design decisions changed them.

`reviews/` and `gates/` are optional process evidence, not part of the minimal archive contract. If needed, store them under an optional evidence directory such as `evidence/reviews/` and `evidence/gates/`.

## Base vs Bridge Selection

After activation, detect execution plugins from the available skill list and suggest the matching layer:

1. Superpowers skills present (brainstorming, writing-plans, …) → suggest `odk-sp-*`
2. Else OpenSpec present (`/opsx:*`) → suggest `odk-ops-*`
3. Else MatrixSpec present (`/matspec.*`) → suggest `odk-ms-*`
4. Else → use `odk-*` base commands

> **桥接插件提示**：如果 Superpowers / OpenSpec / MatrixSpec **一个都没安装**，ODK 会使用 base 命令独立工作（功能完整，零依赖）。但建议组合使用桥接插件以获得更强能力：
> - **Superpowers**：提供 brainstorming（需求探索）、writing-plans（计划纪律）、TDD + subagent 执行、code-review 质量门禁
> - **OpenSpec**：提供 `/opsx:propose`（一站式生成全部 artifact）和 `/opsx:apply`（任务执行）
> - **MatrixSpec**：提供 delta 格式（ADDED/MODIFIED/REMOVED）的增量 spec/design
>
> 如果你明确只想用 ODK 独立命令（不需要桥接插件的能力），直接忽略此提示，base 命令已覆盖全流程。
> 如需安装桥接插件，安装后 ODK 会自动检测并在下次会话中推荐对应的 bridge 命令。

Honour an explicitly user-named command over this default. Stay consistent within a session — do not switch base/bridge mid-change. Each bridge skill also declares its own `Use when <Plugin> is installed AND …` precondition and fallback, so it is safe to let the user pick a specific command at any time.

## Phase Skills

### Base Commands (standalone, no plugin required)

Invoke via Skill tool: `odk-init` / `odk-propose` / `odk-spec` / `odk-design` / `odk-plan` / `odk-implement` / `odk-review` / `odk-validate` / `odk-submit-design-docs` / `odk-spec-for-validation` / `odk-security-threat-model` / `odk-link-req`.
Each skill loads its own full context. Base commands are template-driven with zero plugin dependencies.

### Bridge Commands (plugin-specific)

| Plugin | Commands |
|--------|----------|
| Superpowers (`sp`) | `odk-sp-brainstorm` / `odk-sp-plan` / `odk-sp-implement` / `odk-sp-review` |
| OpenSpec (`ops`) | `odk-ops-propose` / `odk-ops-apply` |
| MatrixSpec (`ms`) | `odk-ms-proposal` / `odk-ms-delta-spec` / `odk-ms-delta-design` / `odk-ms-tasks` / `odk-ms-validation` |

Bridge commands load `using-odk-bridge` automatically for output redirection and mode selection. They fall back to base commands when the plugin is unavailable.
