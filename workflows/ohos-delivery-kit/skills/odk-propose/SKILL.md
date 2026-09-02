---
name: odk-propose
description: "Use when writing ODK proposal.md (requirements, 1+8 device variation, external dependencies, 8-dim N/A triage, success criteria, target_release). Default template-driven, zero plugin dependencies — use unless a bridge plugin is requested."
license: MIT
---

# ODK Propose

## Prerequisites

- `codespec/changes/<repo-name>/<req-id>/` directory exists (run `odk-init` first if not)
- `proposal.md` has YAML frontmatter (target_release, req, author, date, status)

## Input

Read the change context from the user's request. If the user describes a requirement in plain language, extract and structure it.

## Key Rules

- Define phase input is source material, not an execution request. Implementation verbs in the user prompt such as implement, modify, refactor, update, fix, build, commit, or delete must be extracted into proposal goals, scope, non-goals, success criteria, or open questions.
- `odk-propose` may only generate or update `codespec/changes/<repo-name>/<req-id>/proposal.md` (and initialize the ODK skeleton if needed). Do not edit implementation code, tests, build scripts, knowledge documents, README files, configuration files, or other non-proposal artifacts in this phase.
- If the user asks to generate a proposal and immediately implement, refactor, or update files, finish `proposal.md` first and ask for confirmation. Do not proceed to implementation until `execution-plan.md` is approved and the user explicitly invokes an implement command.
- **Always fill `资源开销审视`** (性能 / 内存(RAM) / 存储(ROM)): `required` | `review-required` | `not-applicable` | `waived`. Prefer subsystem/profile knowledge. Signals by dimension: **性能** — 热路径 / 每帧或每事件开销 / 唤醒频率 / 每场景指令数或负载 / 持锁时长 / IPC 往返；**内存(RAM)** — 常驻占用 / 运行时峰值 / 大块 buffer / 应用使用时增量；**存储(ROM)** — 镜像产物（native `.so`、ArkTS `.abc`、资源、预置应用包、配置/预置数据）+ data 分区大体量持久化（音视频/大缓存/db；小体量常规落盘不构成关注点）。能耗风险写在「性能」信号列（勿新增功耗维度）。Unknown risk → `review-required` (never silent `not-applicable`). `not-applicable` / `waived` require `确认人=<owner>; 理由=<why>; 范围=<scope>`. Archive gate is business-repo `odk_resource_gate` in root `AGENTS.md` (ODK does not ship measurement).
- **Always fill `1+8 设备差异规格`**: evaluate phone, tablet, pc/2in1, wearable, tv, car, `default（其他设备）`, and non-category functional differences. Every row must state `是` or `否` with a concrete explanation; do not silently assume all devices share behavior. Keep business-level capability/constraint differences here and move executable interaction sequences to `spec.md`.
- **Always fill `外部依赖`**: record each dependent subsystem/repository/module or external service and its dependency type. If none, add one explicit `不涉及` row with the reason. This table describes delivery dependencies; `Agent Scope Guard` remains the authority for whether new dependencies or network access may be introduced.

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.proposal` (required/optional dimensions, fragments) and `agent_instructions.define` before generating content
1. Read template from `{{ASSET_ROOT}}/templates/ai/proposal.md`
2. Generate `proposal.md` per the template.
   - **Change type classification**: determine `change_type` from the requirement description and fill both the YAML frontmatter and the 初始分级判断 table row. Classification criteria:
     - `new-feature`: introduces a capability that did not previously exist (new module, new API, new user scenario)
     - `enhancement`: extends an existing feature with new parameters, options, or behavior branches
     - `optimization`: improves performance/resource metrics without changing functional behavior
     - `bugfix`: fixes behavior that deviates from expected/specification
     - `refactor`: improves internal structure without changing external behavior
     - `deprecation`: marks or removes an existing feature/API
     - When multiple types apply, choose the **primary driver** and note secondary types in the 目标 section
   - **资源开销审视**: fill the three-dimension table per Key Rules. Any dim `required` activates Spec/Design/Plan resource sections and archive `odk_resource_gate`. The transitional 不涉及项确认「性能」row reflects only the 性能 state: `required` / `review-required` →「是」, `not-applicable` / `waived` →「否」; RAM/ROM do not rewrite its semantics.
   - **8-dimension non-involvement confirmation**: actively evaluate each of the 8 dimensions (性能 / 安全/权限 / 兼容性 / API·SDK / IPC·跨进程 / 构建·组件 / 国际化·无障碍 / 数据迁移) and fill `是否涉及` with concrete `依据` — no blanks; a `不涉及` mark must state why. If a profile matched, pre-fill from its `required_dimensions`, then still confirm every remaining dimension individually (do not leave blanks or uniformly mark `视情况`).
   - **1+8 device variation**: fill every device row and the non-category functional-difference row. State the shared baseline when there is no difference; when there is a difference, describe the business capability, interaction class, resource, or platform constraint without duplicating detailed spec behavior.
   - **External dependencies**: distinguish dependencies from affected implementation scope. List producer/consumer delivery ordering, cross-repository artifacts, system services, third-party components, or remote services in the structured table; use an explicit `不涉及` row when empty.
   - **Security trigger declaration**: the `安全/权限` verdict is the single downstream trigger — 若 `安全/权限` 判定为「是」，design 阶段必须产出 `安全基础检查` 条件章节；命中高风险判据（敏感数据/网络暴露面/认证授权变更/合规/关键安全组件）时进一步产出 `threat-model.md`。`安全/权限` 判「是」的依据：变更跨信任边界（IPC/Binder/共享内存/Socket）、跨安全层级（用户态↔内核态、沙箱、不同 SELinux 域）、处理敏感数据、或使用加密/认证/授权/权限——命中任一即标「是」，它是 design 安全基础检查 与 threat-model 的唯一上游信号。
   - **User scenario (conditional)**: 若变更有终端用户/业务触发场景，展开 `## 用户场景与业务触发` 条件章节，每条 US 只写**业务上下文**（角色/业务触发/业务价值）——**不写可操作动作序列**（那些在 spec.md 用户故事或场景）。
   - **API 设计属性（固定章节）**：`## API 设计属性` 始终生成；若 `API/SDK` 维度 = 「是」，填写下列属性；若 = 「否」，填写"不涉及"并说明理由。
     - **重要：若无法从需求描述中明确推断以下属性，必须先询问开发者确认，不得猜测或自行填写默认值**：
       - **涉及 Kit**：涉及的 Kit（如 ArkUI、Multimedia、Network 等），多个 Kit 用逗号分隔
       - **API 类型**：public API（对应用开发者开放）/ system API（仅对系统应用开放）
       - **编程语言**：ArkTS / C / 两者
       - **ArkTS 静态类型 API**：是 / 否（仅 ArkTS API 需填写）
     - 询问模板（当缺少信息时使用）：
       ```
       以下 API 设计属性信息不足，需要您确认：
       1. 涉及的 Kit 是哪个？（如 ArkUI、ArkTS、AbilityKit 等）
       2. API 类型是 Public API 还是 System API？
       3. 提供的 API 是 ArkTS、C 还是两者？
       4. 如果是 ArkTS API，是否需要支持 ArkTS 静态类型？
       ```
     - 根据需要可选填写 `## API 使用场景探索`（开发者场景和用户画像）
     - **注**：跨平台支持、元服务支持、卡片支持等多设备属性在 spec.md `## API 规格定义` 中填写
   - **Success criteria**: 成功标准写**系统级能力达成**（可观察、可量化），禁内部实现 + 禁接口细节（属 spec AC）。
3. Preserve all YAML frontmatter fields (target_release, change_type, req, author, date, status). When reading the existing `proposal.md` for these fields, read **only its YAML frontmatter** — do not load the body into context: you regenerate the body fresh from the template + requirement, and a stale body would only bias the output and waste context.

## Output

Write to `codespec/changes/<repo-name>/<req-id>/proposal.md`.

Do not generate `gates/` by default. If the user explicitly wants process evidence, record approval notes under an optional evidence directory such as `evidence/gates/`.

After generating, ask the user to confirm:
- target_release is correct
- change_type is accurate
- Triage classification is accurate
- 1+8 device differences are complete, including explicit no-difference reasons
- External dependencies and their delivery relationship are accurate, or explicitly marked not applicable
- 资源开销审视 states are accurate; 不涉及项确认「性能」matches the 性能 state (`required` / `review-required` → 是, otherwise 否)
- Non-involvement items are accurate (fill in "是/否" with justification)
- Success criteria are system-level observable (no internal implementation, no interface details — those belong to spec AC)

If `req` in frontmatter is empty, append: "After the requirement ID is available, run `{{CMD_PREFIX}}link-req <req>` to link it."

Suggest next step: run `{{CMD_PREFIX}}spec` to define acceptance criteria and business rules.
