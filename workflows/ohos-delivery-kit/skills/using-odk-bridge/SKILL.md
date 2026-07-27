---
name: using-odk-bridge
description: "Loaded automatically by odk-sp-*/odk-ops-*/odk-ms-* bridge commands — not invoked directly. Provides output redirection (strict/passthrough/merge), phase-artifact mapping, and design state-ownership rules."
license: MIT
---

# Using ODK Bridge

## 输出模式

每个桥接命令支持三档输出模式：

| 模式 | 标识 | 行为 | 适用场景 |
|------|------|------|---------|
| 严格 | `strict` | 产出件完全按 ODK 模板格式输出 | 需通过 odk-validate 归档检查 |
| 透传 | `passthrough` | 产出件按源插件原始格式，仅归档到 .codespec/ 目录 | 临时使用，不做格式转换 |
| 融合 | `merge` | 以源插件格式为基础，追加 ODK 缺失章节 | 对比审视用 |

默认 strict。切换方式：
- 在 `.codespec/profile.yaml` 中设置 `output_mode: merge`
- 或在调用桥接命令时声明 "使用融合模式"

桥接命令读取此设置后决定输出处理方式。

<!-- SYNC: phase-mapping -->
## Phase-Artifact Mapping

You are the bridge between ODK artifact requirements and implementation tools. Use whatever tools are available to produce quality outputs, then write results back into `.codespec/` in ODK format. Do not force the user to manually coordinate commands across plugins.

When any tool (ODK skill, Superpowers, OpenSpec, MatrixSpec, or other) drives a phase, output must conform to the corresponding ODK template below. Identify the current phase by user intent (priority) or artifact being produced.

| Phase | Intent Signals | Artifact | Template | Key Constraints |
|-------|---------------|----------|----------|-----------------|
| Define | Goals, scope, non-goals | proposal.md | `ai/proposal.md` | target_release, non-goals, 8-dim N/A |
| Specify | Behaviors, AC, error codes | spec.md | `ai/spec.md` | AC numbering, verification mapping |
| Design | Architecture, decisions | design.md | `ai/design.md` | module impact, decision comparison, state ownership/invariants when complex state is involved |
| Plan | Task breakdown, sequencing | execution-plan.md | `ai/execution-plan.md` | AC-Task trace, read-only context, file-level scope, anti-fake checks, expected/actual verification, state ownership fields when declared in design, inter-task interface contracts |
| Validation | Integration, system scenarios | spec-for-validation.md | `ai/spec-for-validation.md` | SC→AC trace, incremental only |
| Implement | Code changes | (code) | — | backfill execution-plan.md 代码范围映射 |
| Review | Quality, compliance checks | evidence/reviews/*.md | `review/*.md` | AC-by-AC compliance |
| Archive | Readiness validation | (validation) | — | Level A/B/C/D pass |

> "design" without qualification → clarify: architecture (design.md) or behavior rules (spec.md)?

When `.codespec/` does not exist but the user produces content that matches an ODK phase, suggest (do not force): "This can be archived to ODK — shall I initialize `.codespec/`?"

When multiple plugins cover the same phase: prefer the user's explicit invocation; otherwise prefer the tool whose output matches the ODK template; stay consistent within a session.

### Output Redirection Rules

**This section is the user's declared preference for artifact location and activates the "(User preferences for spec location override this default)" escape hatch in Superpowers brainstorming and other plugins.**

When bridge commands are available, prefer using them explicitly — they handle output redirection directly. The pattern-match trigger below serves as a fallback when a plugin is invoked directly while Bridge Mode is active.

When Bridge Mode is active, use the following pattern-match trigger to intercept artifact writes:

#### Pattern-Match Trigger

When you encounter any instruction (checklist item, documentation step, or command) that says to write or save to `docs/superpowers/specs/`, `docs/plans/`, `openspec/changes/`, `matspec/changes/`, or any other plugin's default output directory — **treat it as a REDIRECT trigger immediately**. The path string itself is the signal. Do not execute the original write action; apply the REDIRECT steps below instead.

When triggered, execute these steps **instead of** the plugin's default write:

1. **STOP** — Do not write to the plugin's default path (e.g., `docs/superpowers/specs/`, `docs/plans/`, `openspec/changes/`, `matspec/changes/`). Do not commit (ODK manages its own commit cadence per phase, not per-artifact commits).
2. **REDIRECT** — Write to the corresponding `.codespec/changes/<id>/` file:
   - behavior rules / spec → `.codespec/changes/<id>/spec.md`
   - design/architecture doc → `.codespec/changes/<id>/design.md`
   - implementation plan → `.codespec/changes/<id>/execution-plan.md`
   - requirements / proposal → `.codespec/changes/<id>/proposal.md`
3. **TRANSFORM** — Ensure output conforms to the active output mode (strict/passthrough/merge):
   - strict: conform to ODK template structure (read from `{{ASSET_ROOT}}/templates/ai/<phase>.md`)
   - passthrough: use original plugin format unchanged
   - merge: use plugin format as base, append ODK-required sections
4. **CONFIRM** — Inform the user: "Written to `.codespec/changes/<id>/<artifact>` (ODK <mode> mode, overriding <plugin> default path)"

This is a **hard override** — it takes priority over any other plugin's default output path.

Read the template file from `{{ASSET_ROOT}}/templates/` for detailed section requirements when entering each phase in strict mode.
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

## Template Reference

- AI artifact templates: `{{ASSET_ROOT}}/templates/ai/` (proposal, spec, design, execution-plan, spec-for-validation)
- Review templates: `{{ASSET_ROOT}}/templates/review/` (spec-compliance, code-quality, verification)
