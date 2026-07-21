
# ODK Propose

Use when writing ODK proposal.md (requirements, 8-dim N/A triage, success criteria, target_release). Default template-driven, zero plugin dependencies — use unless a bridge plugin is requested.

## Prerequisites

- `.codespec/changes/<id>/` directory exists (run `odk-init` first if not)
- `proposal.md` has YAML frontmatter (target_release, issue, author, date, status)

## Input

Read the change context from the user's request. If the user describes a requirement in plain language, extract and structure it.

## Key Rules

- Define phase input is source material, not an execution request. Implementation verbs in the user prompt such as implement, modify, refactor, update, fix, build, commit, or delete must be extracted into proposal goals, scope, non-goals, success criteria, or open questions.
- `odk-propose` may only generate or update `.codespec/changes/<id>/proposal.md` (and initialize the ODK skeleton if needed). Do not edit implementation code, tests, build scripts, knowledge documents, README files, configuration files, or other non-proposal artifacts in this phase.
- If the user asks to generate a proposal and immediately implement, refactor, or update files, finish `proposal.md` first and ask for confirmation. Do not proceed to implementation until `execution-plan.md` is approved and the user explicitly invokes an implement command.

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.proposal` (required/optional dimensions, fragments) and `agent_instructions.define` before generating content
1. Read template from `{{ODK_ASSET_ROOT}}/templates/ai/proposal.md`
2. Generate `proposal.md` per the template.
   - **Change type classification**: determine `change_type` from the requirement description and fill both the YAML frontmatter and the 初始分级判断 table row. Classification criteria:
     - `new-feature`: introduces a capability that did not previously exist (new module, new API, new user scenario)
     - `enhancement`: extends an existing feature with new parameters, options, or behavior branches
     - `optimization`: improves performance/resource metrics without changing functional behavior
     - `bugfix`: fixes behavior that deviates from expected/specification
     - `refactor`: improves internal structure without changing external behavior
     - `deprecation`: marks or removes an existing feature/API
     - When multiple types apply, choose the **primary driver** and note secondary types in the 目标 section
   - **8-dimension non-involvement confirmation**: actively evaluate each of the 8 dimensions (性能 / 安全/权限 / 兼容性 / API·SDK / IPC·跨进程 / 构建·组件 / 国际化·无障碍 / 数据迁移) and fill `是否涉及` with concrete `依据` — no blanks; a `不涉及` mark must state why. If a profile matched, pre-fill from its `required_dimensions`, then still confirm every remaining dimension individually (do not leave blanks or uniformly mark `视情况`).
   - **Security trigger declaration**: the `安全/权限` verdict is the single downstream trigger — 若 `安全/权限` 判定为「是」，design 阶段必须产出 `安全基础检查` 条件章节；命中高风险判据（敏感数据/网络暴露面/认证授权变更/合规/关键安全组件）时进一步产出 `threat-model.md`。`安全/权限` 判「是」的依据：变更跨信任边界（IPC/Binder/共享内存/Socket）、跨安全层级（用户态↔内核态、沙箱、不同 SELinux 域）、处理敏感数据、或使用加密/认证/授权/权限——命中任一即标「是」，它是 design 安全基础检查 与 threat-model 的唯一上游信号。
   - **User scenario (conditional)**: 若变更有终端用户/业务触发场景，展开 `## 用户场景与业务触发` 条件章节，每条 US 只写**业务上下文**（角色/业务触发/业务价值）——**不写可操作动作序列**（那些在 spec.md 用户故事或场景）。
   - **Success criteria**: 成功标准写**系统级能力达成**（可观察、可量化），禁内部实现 + 禁接口细节（属 spec AC）。
3. Preserve all YAML frontmatter fields (target_release, change_type, issue, author, date, status). When reading the existing `proposal.md` for these fields, read **only its YAML frontmatter** — do not load the body into context: you regenerate the body fresh from the template + requirement, and a stale body would only bias the output and waste context.

## Output

Write to `.codespec/changes/<id>/proposal.md`.

Do not generate `gates/` by default. If the user explicitly wants process evidence, record approval notes under an optional evidence directory such as `evidence/gates/`.

After generating, ask the user to confirm:
- target_release is correct
- change_type is accurate
- Triage classification is accurate
- Non-involvement items are accurate (fill in "是/否" with justification)
- Success criteria are system-level observable (no internal implementation, no interface details — those belong to spec AC)

If `issue` in frontmatter is empty, append: "The proposal content can be used as the issue description. After creating the issue, run `{{CMD_PREFIX}}link-issue <id>` to link it."

Suggest next step: run `{{CMD_PREFIX}}spec` to define acceptance criteria and business rules.
