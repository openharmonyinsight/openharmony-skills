---
name: using-odk
description: "Use when the user mentions ODK, ohos-delivery-kit, `codespec`, or OpenHarmony delivery artifacts (proposal/spec/design/execution-plan/review/validate). Main router: loads phase skills and detects which bridge plugin (Superpowers/OpenSpec/MatrixSpec) is installed."
license: MIT
---

# Using ohos-delivery-kit

You are working in a project that uses **ohos-delivery-kit** — a lightweight delivery artifact specification layer for OpenHarmony.

## Activation

### Bridge Mode (session-scoped)

Once the user invokes any `{{CMD_PREFIX}}*` command in the current session, ODK bridge activates for the remainder of the session: Output Redirection Rules (see Phase-Artifact Mapping below) override all other plugins' default output paths. Ends when the session ends.

ODK also activates when the user explicitly mentions ODK, ohos-delivery-kit, `codespec`, or ODK artifact names/actions (proposal, spec, design, execution-plan, spec-for-validation, threat-model, metadata_tracking, review, validate, submit design docs).

### Deactivation

ODK bridge does **not** activate when:
- `codespec/` exists but the user has not invoked any `{{CMD_PREFIX}}*` command in this session
- The user is doing ordinary coding, debugging, build, or review tasks
- The user explicitly says "不用ODK" / "skip ODK" / "don't use ODK"

After activation, follow the Context Loading rules below to determine the active change.

<!-- ODK:reference contracts/skill-guides/router/workflow.md -->
## Workflow (on activation)

After ODK activates, read `{{ASSET_ROOT}}/contracts/skill-guides/router/workflow.md` before selecting a phase, archive, or base/bridge command. It defines the unchanged archive layout, phase order, available commands, plugin preference and fallback. Do not load it for ordinary coding or when ODK is disabled.
<!-- /ODK:reference -->
## Key Rules

- **target_release** is the single source of truth for version, stored in `proposal.md` YAML frontmatter
- Traceability chain: `proposal → spec AC → execution-plan Task → code → commit → review`. Any broken link fails validation.
- **GitCode submission reminder**: when implementation is complete and the user is about to commit, push, or open a GitCode PR, remind them that documents under `codespec/` must be submitted to the separate design-docs repository. Read its address from developer-owned `codespec/profile.yaml` key `design_docs_repository`. If the key is absent or empty, show it as “待开发者填写” and ask the developer to provide it; never guess a repository or automatically push across repositories. This reminder does not by itself block the business-code submission. When the user explicitly requests design-document submission, invoke `odk-submit-design-docs`: generate `metadata_tracking.yaml`, validate the five-base-file bundle plus required conditional evidence, and submit `proposal.md`, `spec.md`, `design.md`, `execution-plan.md`, and `metadata_tracking.yaml` together.
- **Phase Gate**: Artifact phases (propose, spec, design, plan) produce documents for approval. When the user confirms an artifact ("没问题", "looks good", etc.), it means the document is approved — it does NOT authorize skipping to implementation. After each artifact is approved, suggest the next phase command explicitly and wait for the user to invoke it. Do not write implementation code until `execution-plan.md` is approved and the user explicitly invokes an implement command (`{{CMD_PREFIX}}implement`, `{{CMD_PREFIX}}sp-implement`, etc.). This applies regardless of perceived simplicity.

## Context Loading

For actual design-document submission, `odk-submit-design-docs` resolves and confirms the destination first: retain an explicit `design_docs_repository`; otherwise offer `https://gitcode.com/OpenHarmonyAI/design-docs` for a business `origin` whose host is exactly `gitcode.com`, and require a user-provided address for other/missing origins. No answer is not consent; the reminder alone never authorizes cross-repository writes.

- If `codespec/` does not exist, the project is not yet initialized — guide the user to run `odk-init`
- Resolve the current `<repo-name>` and inspect only `codespec/changes/<repo-name>/`
- If that repository directory has exactly one change directory, treat it as the active change
- If it has multiple change directories, ask the user which one to operate on before proceeding
- Once determined, read `target_release` from the active change's `proposal.md` frontmatter
- Do not load full documents into context — use summaries (≤15 lines) when passing between phases
- Two distinct read cases, do not conflate them:
  - **Regenerating your own target file** (e.g. `odk-propose` reading an existing `proposal.md`): read **only its YAML frontmatter** to preserve fields — never load the body, since you regenerate it fresh from the template + inputs; a stale body only biases the output and wastes context.
  - **Reading an upstream artifact for context** (e.g. `odk-spec` ← filled `proposal.md`, `odk-design` ← `spec.md`, `odk-plan` ← `design.md`): the body carries the requirements/AC/state you depend on — read the relevant sections in full (still prefer summaries ≤15 lines when only passing between phases).
- When spawning subagents (e.g. via bridge commands), run them in isolated contexts — never fork the main session history; the main session only dispatches tasks and receives summaries
- Pass evidence by file path, not by content — artifacts land on disk once (`evidence/`, `pr-diff.txt`, `findings.json`); later references pass the path, not the full text
- Cap parallel fan-out at ≤4 subagents per layer; batch or narrow task scope if more are needed
- Template files are located at `{{ASSET_ROOT}}/templates/` (installed with the plugin)

<!-- ODK:reference contracts/skill-guides/router/profiles.md -->
## Profile Detection

When generating ODK artifacts for a module, read `{{ASSET_ROOT}}/contracts/skill-guides/router/profiles.md` before applying profile overrides; resolve its relative paths from that guide's directory. It defines profile selection, phase mappings, fragment composition and conflict precedence. Routing-only requests do not need this reference.
<!-- /ODK:reference -->
## Bypass Documents (Design Phase)

ODK supports bypass documents that supplement main artifacts for complex scenarios:

| Bypass Document | Trigger Condition | Relation to Main Artifact | Production Skill |
|----------------|-------------------|---------------------------|-------------------|
| `threat-model.md` | High-risk security/privacy/compliance (see `odk-security-threat-model` trigger conditions) | `design.md` 基础检查 → 深度分析独立存档 | `odk-security-threat-model` |
| `spec-for-validation.md` | Integration/system scenarios needed for validation | Derived from `spec.md`; parallel bypass, does not block main flow | `odk-spec-for-validation` |

**Drift direction rule**: When upstream proposal/spec content changes, re-run the bypass skill to sync (e.g., `threat-model.md` security triggers expand → re-run `odk-security-threat-model` to refresh analysis).

When using bridge commands, `using-odk-bridge` is loaded automatically and provides output mode selection and redirection rules.

## Template Reference

- AI artifact templates: `{{ASSET_ROOT}}/templates/ai/` (proposal, spec, design, execution-plan, spec-for-validation, threat-model)
- Review templates: `{{ASSET_ROOT}}/templates/review/` (spec-compliance, code-quality, verification)
- Design-docs submission metadata: `{{ASSET_ROOT}}/templates/metadata_tracking.yaml`
