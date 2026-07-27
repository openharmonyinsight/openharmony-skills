---
name: using-odk
description: "Use when the user mentions ODK, ohos-delivery-kit, `.codespec`, or OpenHarmony delivery artifacts (proposal/spec/design/execution-plan/review/validate). Main router: loads phase skills and detects which bridge plugin (Superpowers/OpenSpec/MatrixSpec) is installed."
license: MIT
---

# Using ohos-delivery-kit

You are working in a project that uses **ohos-delivery-kit** — a lightweight delivery artifact specification layer for OpenHarmony.

## Activation

### Bridge Mode (session-scoped)

Once the user invokes any `{{CMD_PREFIX}}*` command in the current session, ODK bridge activates for the remainder of the session: Output Redirection Rules (see Phase-Artifact Mapping below) override all other plugins' default output paths. Ends when the session ends.

ODK also activates when the user explicitly mentions ODK, ohos-delivery-kit, `.codespec`, or ODK artifact names (proposal, spec, design, execution-plan, spec-for-validation, threat-model, review, validate).

### Deactivation

ODK bridge does **not** activate when:
- `.codespec/` exists but the user has not invoked any `{{CMD_PREFIX}}*` command in this session
- The user is doing ordinary coding, debugging, build, or review tasks
- The user explicitly says "不用ODK" / "skip ODK" / "don't use ODK"

After activation, follow the Context Loading rules below to determine the active change.

## Archive Structure

All delivery artifacts are archived under:

```
.codespec/changes/issue-<issue-number>-<english-slug>/
```

Each change directory is **populated by phase** — `odk-init` only seeds `proposal.md` as a frontmatter stub; the other main docs appear when their phase first runs (a missing main doc before its phase is expected, not an error):
- `proposal.md` — (`odk-init` stub → `odk-propose` fills) requirements proposal with triage, success criteria, and impact scope (YAML frontmatter with `target_release`)
- `spec.md` — (`odk-spec`) functional specification with WHEN/THEN AC, error codes, and verification mapping
- `design.md` — (`odk-design`) architecture design with Mermaid diagrams and decision comparison (references spec ACs)
- `execution-plan.md` — (`odk-plan`) implementation plan with AC-Task traceability and task details
- `spec-for-validation.md` — optional validation specification with integration/system scenarios derived from spec.md (parallel bypass, does not block main flow)
- `threat-model.md` — optional deep threat analysis (bypass; high-risk security/privacy/compliance changes; produced by `odk-security-threat-model`)

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

Invoke via Skill tool: `odk-init` / `odk-propose` / `odk-spec` / `odk-design` / `odk-plan` / `odk-implement` / `odk-review` / `odk-validate` / `odk-spec-for-validation` / `odk-security-threat-model` / `odk-link-issue`.
Each skill loads its own full context. Base commands are template-driven with zero plugin dependencies.

### Bridge Commands (plugin-specific)

| Plugin | Commands |
|--------|----------|
| Superpowers (`sp`) | `odk-sp-brainstorm` / `odk-sp-plan` / `odk-sp-implement` / `odk-sp-review` |
| OpenSpec (`ops`) | `odk-ops-propose` / `odk-ops-apply` |
| MatrixSpec (`ms`) | `odk-ms-proposal` / `odk-ms-delta-spec` / `odk-ms-delta-design` / `odk-ms-tasks` / `odk-ms-validation` |

Bridge commands load `using-odk-bridge` automatically for output redirection and mode selection. They fall back to base commands when the plugin is unavailable.

## Key Rules

- **target_release** is the single source of truth for version, stored in `proposal.md` YAML frontmatter
- Traceability chain: `proposal → spec AC → execution-plan Task → code → commit → review`. Any broken link fails validation.
- **Phase Gate**: Artifact phases (propose, spec, design, plan) produce documents for approval. When the user confirms an artifact ("没问题", "looks good", etc.), it means the document is approved — it does NOT authorize skipping to implementation. After each artifact is approved, suggest the next phase command explicitly and wait for the user to invoke it. Do not write implementation code until `execution-plan.md` is approved and the user explicitly invokes an implement command (`{{CMD_PREFIX}}implement`, `{{CMD_PREFIX}}sp-implement`, etc.). This applies regardless of perceived simplicity.

## Context Loading

- If `.codespec/` does not exist, the project is not yet initialized — guide the user to run `odk-init`
- If `.codespec/changes/` has exactly one change directory, treat it as the active change
- If `.codespec/changes/` has multiple directories, ask the user which one to operate on before proceeding
- Once determined, read `target_release` from the active change's `proposal.md` frontmatter
- Do not load full documents into context — use summaries (≤15 lines) when passing between phases
- Two distinct read cases, do not conflate them:
  - **Regenerating your own target file** (e.g. `odk-propose` reading an existing `proposal.md`): read **only its YAML frontmatter** to preserve fields — never load the body, since you regenerate it fresh from the template + inputs; a stale body only biases the output and wastes context.
  - **Reading an upstream artifact for context** (e.g. `odk-spec` ← filled `proposal.md`, `odk-design` ← `spec.md`, `odk-plan` ← `design.md`): the body carries the requirements/AC/state you depend on — read the relevant sections in full (still prefer summaries ≤15 lines when only passing between phases).
- When spawning subagents (e.g. via bridge commands), run them in isolated contexts — never fork the main session history; the main session only dispatches tasks and receives summaries
- Pass evidence by file path, not by content — artifacts land on disk once (`evidence/`, `pr-diff.txt`, `findings.json`); later references pass the path, not the full text
- Cap parallel fan-out at ≤4 subagents per layer; batch or narrow task scope if more are needed
- Template files are located at `{{ASSET_ROOT}}/templates/` (installed with the plugin)

## Profile Detection

When generating ODK artifacts for a specific OpenHarmony module, apply subsystem-specific constraints:

1. If `.codespec/profile.yaml` exists, use the declared profile IDs (e.g., `profiles: ["arkui"]`)
2. Otherwise, infer profile from module keywords in the change path or user description (see `{{ASSET_ROOT}}/profiles/README.md` for activation rules)
3. Read the matching profile(s) from `{{ASSET_ROOT}}/profiles/<id>.yaml`
4. Apply `template_overrides` to adjust dimensions and sections per phase:
   - Proposal: `required_dimensions` → mark those rows as "是" in the 8-dim N/A table; all others default to "视情况"
   - Design: `additional_sections` → append to required sections list
   - Spec: `additional_ac_categories` → add to user story AC categories
   - Execution-plan: `additional_prohibitions` → append to 禁止项

   Dimension mapping: perf→性能, security→安全/权限, compatibility→兼容性, api-sdk→API/SDK, ipc→IPC/跨进程, build→构建/组件, i18n→国际化/无障碍, data-migration→数据迁移
5. Apply `agent_instructions` for the current phase (define/specify/design/plan) to add domain-specific constraints
6. If a profile provides `fragments` with a composition strategy (prepend/append/wrap), apply to the generated artifact

Profiles compose additively — they add required sections and constraints, never remove from the base template. When multiple profiles match, lower `priority` values take precedence for dimension conflicts, while sections and instructions are merged by union. See `{{ASSET_ROOT}}/profiles/README.md` for available profiles and their activation rules.

When using bridge commands, `using-odk-bridge` is loaded automatically and provides output mode selection and redirection rules.

## Template Reference

- AI artifact templates: `{{ASSET_ROOT}}/templates/ai/` (proposal, spec, design, execution-plan, spec-for-validation, threat-model)
- Review templates: `{{ASSET_ROOT}}/templates/review/` (spec-compliance, code-quality, verification)
