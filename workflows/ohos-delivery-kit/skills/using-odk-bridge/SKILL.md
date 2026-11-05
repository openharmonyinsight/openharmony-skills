---
name: using-odk-bridge
description: "Loaded automatically by odk-sp-*/odk-ops-*/odk-ms-* bridge commands — not invoked directly. Provides output redirection (strict/passthrough/merge), phase-artifact mapping, and design state-ownership rules."
license: MIT
---

# Using ODK Bridge

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and obtain the effective
contract before choosing artifacts, sections or phase prerequisites.
<!-- /ODK:reference -->

## 输出模式

每个桥接命令支持三档输出模式：

| 模式 | 标识 | 行为 | 适用场景 |
|------|------|------|---------|
| 严格 | `strict` | 产出件完全按 ODK 模板格式输出 | 需通过 odk-validate 归档检查 |
| 透传 | `passthrough` | 产出件按源插件原始格式，仅归档到 codespec/ 目录 | 临时使用，不做格式转换 |
| 融合 | `merge` | 以源插件格式为基础，追加 ODK 缺失章节 | 对比审视用 |

默认 strict。切换方式：
- 在 `codespec/profile.yaml` 中设置 `output_mode: merge`
- 或在调用桥接命令时声明 "使用融合模式"

桥接命令读取此设置后决定输出处理方式。

<!-- SYNC: phase-mapping -->
## Phase-Artifact Mapping

You are the bridge between ODK artifact requirements and implementation tools. Use whatever tools are available to produce quality outputs, then write results back into `codespec/` in ODK format. Do not force the user to manually coordinate commands across plugins.

When a tool drives a phase, its ODK delivery projection must conform to the corresponding ODK template below. Identify the current phase by user intent (priority) or artifact being produced.

| Phase | Intent Signals | Artifact | Template | Key Constraints |
|-------|---------------|----------|----------|-----------------|
| Define | Goals, scope, non-goals | proposal.md | `ai/proposal.md` | target_release, non-goals, `1+8 设备差异规格`, `外部依赖`, 8-dim N/A |
| Specify | Behaviors, AC, error codes | spec.md | `ai/spec.md` | AC numbering, verification mapping |
| Design | Architecture, decisions | design.md | `ai/design.md` | module impact, decision comparison, state ownership/invariants when complex state is involved |
| Plan | Task breakdown, sequencing | execution-plan.md | `ai/execution-plan.md` | AC-Task trace, read-only context, file-level scope, anti-fake checks, expected/actual verification, state ownership fields when declared in design, inter-task interface contracts |
| Validation | Integration, system scenarios | spec-for-validation.md | `ai/spec-for-validation.md` | SC→AC trace, incremental only |
| Implement | Code changes | (code) | — | backfill execution-plan.md 代码范围映射 |
| Review | Quality, compliance checks | evidence/reviews/*.md | `review/*.md` | AC-by-AC compliance |
| Archive | Readiness validation | (validation) | — | Level A/B/C/D pass |

> "design" without qualification → clarify: architecture (design.md) or behavior rules (spec.md)?

When `codespec/` does not exist but the user produces content that matches an ODK phase, suggest (do not force): "This can be archived to ODK — shall I initialize `codespec/`?"

When multiple plugins cover the same phase: prefer the user's explicit invocation; otherwise prefer the tool whose output matches the ODK template; stay consistent within a session.

### OpenSpec native-workspace exception

<!-- ODK:reference contracts/skill-guides/router/openspec-state.md -->
Read `contracts/skill-guides/router/openspec-state.md` for OpenSpec. Its native
workspace, delta specs and tracked task file are never redirected. Native state
is captured and the ODK delivery projection is reconciled separately.
<!-- /ODK:reference -->

### Output Redirection Rules

**This section is the user's declared preference for artifact location and activates the "(User preferences for spec location override this default)" escape hatch in Superpowers brainstorming and other plugins.**

When bridge commands are available, prefer using them explicitly — they handle output redirection directly. The pattern-match trigger below serves as a fallback when a plugin is invoked directly while Bridge Mode is active.

When Bridge Mode is active, use the following pattern-match trigger to intercept artifact writes:

#### Pattern-Match Trigger

When you encounter any instruction (checklist item, documentation step, or command) that says to write or save to `docs/superpowers/specs/`, `docs/plans/`, `matspec/changes/`, or any other plugin's default output directory — **treat it as a REDIRECT trigger immediately**. The path string itself is the signal. Do not execute the original write action; apply the REDIRECT steps below instead.

When triggered, execute these steps **instead of** the plugin's default write:

1. **STOP** — Do not write to the plugin's default path (e.g., `docs/superpowers/specs/`, `docs/plans/`, `matspec/changes/`). Do not commit (ODK manages its own commit cadence per phase, not per-artifact commits).
2. **REDIRECT** — Write to the corresponding `codespec/changes/<repo-name>/<proposal-id>/` file:
   - behavior rules / spec → `codespec/changes/<repo-name>/<proposal-id>/spec.md`
   - design/architecture doc → `codespec/changes/<repo-name>/<proposal-id>/design.md`
   - implementation plan → `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md`
   - requirements / proposal → `codespec/changes/<repo-name>/<proposal-id>/proposal.md`
3. **TRANSFORM** — Ensure output conforms to the active output mode (strict/passthrough/merge):
   - strict: conform to ODK template structure (read from `templates/ai/<phase>.md`)
   - passthrough: use original plugin format unchanged
   - merge: use plugin format as base, append ODK-required sections
4. **CONFIRM** — Inform the user: "Written to `codespec/changes/<repo-name>/<proposal-id>/<artifact>` (ODK <mode> mode, overriding <plugin> default path)"

This override applies to stateless document outputs. The OpenSpec native-workspace exception above takes precedence; it must not change CLI-owned state paths.

Read the template file from `templates/` for detailed section requirements when entering each phase in strict mode.
<!-- /SYNC: phase-mapping -->

## Design State Ownership Rules

When strict or merge mode produces `design.md`, keep the base template minimal for simple changes.

<!-- SYNC: state-ownership -->
For changes involving runtime state, caches, lifecycle cleanup, hot paths, compatibility behavior, or cross-module
ownership, append a `状态归属与不变量` section after `关键设计决策` and before `时序设计`.

Only declare dimensions that apply to the change:

- **Ownership:** each new or changed state has one explicit owner, key/index, creation timing, cleanup trigger, and
  read-only consumers. Do not write ambiguous phrases such as "owned or delegated", "handled by relevant modules",
  "由相关模块处理", or "TBD".
- **Lifecycle:** state creation, cleanup, error recovery, and rollback triggers are paired.
- **Concurrency safety:** multi-thread or cross-process access declares its synchronization model, such as lock,
  atomic, CAS, or message passing.
- **Compatibility:** existing state formats, APIs, configuration, or default behavior do not change silently.
- **Performance:** hot paths declare constraints for allocation, logging, scans, and lock hold time.
- **Capacity:** growing state declares its bounds and limit behavior.
- **Migration:** versioned state schemas declare upgrade, downgrade, and compatibility requirements.

Each declared invariant must be checkable with a verification method and traceable to an `execution-plan.md` Task.
The owner and lifecycle rules in `design.md` must match the state ownership fields later generated in
`execution-plan.md`. Profiles may inject additional dimensions or domain-specific requirements.
<!-- /SYNC: state-ownership -->

Project-specific concepts such as lazy allocation should come from a profile or project instructions, not from the
base bridge rule.

## Session ID 追踪（桥接规则）

桥接命令（如 `odk-sp-propose` / `odk-ops-apply` / `odk-ms-proposal` 等）在交付件落盘时**必须**执行会话追踪，覆盖 strict、passthrough、merge 三种输出模式。**不能假设基础 skill 内部已完成追踪**——桥接正常路径常调用外部插件再转换写入交付件，并不完整执行对应基础 skill 的全部步骤，存在漏记风险。

### 桥接追踪为交付件落盘的公共步骤

无论桥接以何种模式（strict / passthrough / merge）输出交付件，落盘后**必须**追加执行：

1. **获取当前 session ID**：按 `using-odk` 的「Session ID 获取（多平台）」从当前对话提取；获取不到则用 `unavailable`。
2. **调用脚本更新 sidecar**：

   ```sh
   python3 "runtime/executables/update-sessions-sidecar.py" \
     "<变更目录绝对路径>" "<交付件文件名>" "<当前session ID>" "<桥接skill名>" "<action>"
   ```

3. **从脚本 `---MIRROR---` 段提取镜像**，写入交付件 frontmatter `sessions` 字段和 body `## 会话记录` 表格。

**与基础 skill 追踪的关系**：
- 若桥接完整执行了基础 skill（strict 模式且基础 skill 已调用脚本），基础 skill 的追踪已生效，桥接的追加调用会被脚本去重（同一 session ID 不重复进 `sessions`，但 `log` 会追加一条桥接记录），不会产生冲突。
- 若桥接通过外部插件生成再转换写入（passthrough / merge 模式），基础 skill 的追踪步骤被跳过，**必须由桥接命令补做**。
- 桥接命令不手动操作 JSON，一律通过脚本完成。

## Template Reference

- AI artifact templates: `templates/ai/` (proposal, spec, design, execution-plan, spec-for-validation)
- Review templates: `templates/review/` (spec-compliance, code-quality, verification)
