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

When the user is describing or discussing a requirement, feature idea, or non-trivial change — and no `proposal.md` exists yet in the active change directory — load `odk-brainstorm` first instead of going straight to `odk-propose`. This matches Superpowers `brainstorming` trigger strength: any requirement articulation, not just specific keywords. Trigger does not require the user to say "brainstorm", "帮我梳理需求", "I have an idea", or any fixed phrase — the mere act of describing what they want to build is enough. **The escape conditions below take priority over the trigger — check them first:** only fire the trigger when none of the escapes apply. Skip `odk-brainstorm` when any of these hold: (a) `proposal.md` already exists, (b) the user explicitly says their requirement is fully-formed and wants to go straight to `odk-propose`, (c) the change is a self-contained bug fix with a single clear root cause (e.g. "null check missing", "off-by-one in index", "wrong return value"), (d) the user is doing ordinary coding, debugging, refactoring, or a revert with no new feature scope, or (e) the user is already mid-spec or mid-design and `proposal.md` exists. `odk-brainstorm` conducts a one-question-at-a-time interview across the ODK proposal dimensions and outputs a decision summary that feeds `odk-propose`.

### Deactivation

ODK bridge does **not** activate when:
- `codespec/` exists but the user has not invoked any `{{CMD_PREFIX}}*` command in this session
- The user is doing ordinary coding, debugging, build, or review tasks
- The user explicitly says "不用ODK" / "skip ODK" / "don't use ODK"

After activation, follow the Context Loading rules below to determine the active change.

### Resource Self-Check

<!-- ODK:reference contracts/skill-guides/router/resource-check.md -->
On first activation, locate and read `contracts/skill-guides/router/resource-check.md` before checking resources. Run this bootstrap with the **absolute path of the SKILL.md actually loaded**, replacing the example argument. It resolves file/directory symlinks first (including flat host skills pointing into source or plugin caches), then probes source/native, neutral and SkillHub layouts. `OHOS_PLUGIN_ROOT` is an optional fallback; no environment variable is required. Use the first existing guide; do not guess relative to the business repository or search unrelated caches.

```sh
python3 - /absolute/path/to/loaded/using-odk/SKILL.md <<'PY'
import os
from pathlib import Path
import sys

loaded = Path(sys.argv[1]).absolute()
suffix = Path('contracts/skill-guides/router/resource-check.md')
roots = [loaded.resolve().parents[2], loaded.parents[2]]
if os.environ.get('OHOS_PLUGIN_ROOT'):
    roots.append(Path(os.environ['OHOS_PLUGIN_ROOT']).expanduser())
candidates = []
for root in roots:
    for base in (root, root / 'runtime/assets', root / 'assets', root / 'core'):
        candidate = base / suffix
        if candidate not in candidates:
            candidates.append(candidate)
for candidate in candidates:
    if candidate.is_file():
        print(candidate.resolve())
        break
else:
    sys.exit('ODK resource guide missing; inspected:\n' + '\n'.join(map(str, candidates)))
PY
```

Read the returned guide path and resolve subsequent resources from its actual location. If the command fails, report its inspected paths and stop phases that need those resources. Reuse a successful check in this session unless the installation changes.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/workflow.md -->
## Workflow (on activation)

After ODK activates, read `contracts/skill-guides/router/workflow.md` before selecting a phase, archive, or base/bridge command. It defines the unchanged archive layout, phase order, available commands, plugin preference and fallback. Do not load it for ordinary coding or when ODK is disabled.
<!-- /ODK:reference -->
## Configuration

Before configuration-dependent work, run `python3 runtime/executables/lib/odk_repository.py --effective-config` (source checkout: `python3 scripts/lib/odk_repository.py --effective-config`). Use the returned `config` values and `user_config_path`; a config error stops the phase.

<!-- ODK:reference contracts/skill-guides/router/configuration.md -->
Read `contracts/skill-guides/router/configuration.md` for same-directory user overrides, upgrade preservation, precedence and empty-value semantics. Reload at the start of each phase; implementation reuses the commands already confirmed in its execution plan unless the user requests a change.
<!-- /ODK:reference -->

## Key Rules

- **target_release** is the single source of truth for version, stored in `proposal.md` YAML frontmatter
- Traceability chain: `proposal → spec AC → execution-plan Task → code → commit → review`. Any broken link fails validation.
- **Post-implementation**: completed Tasks automatically enter review and validation through the implementation skill's shared handoff. Source PR submission waits for an explicit user trigger after a reminder; confirmed PR results drive local metadata, followed by separate design-docs confirmation. Do not auto-merge or recursively restart the handoff from review/validate.
- **GitCode submission reminder**: when implementation is complete and the user is about to commit, push, or open a GitCode PR, remind them that documents under `codespec/` must be submitted to the separate design-docs repository. Resolve its address using priority order: `codespec/profile.yaml` if present → `odk_config_ext.yaml` → `odk_config.yaml`. Do not warn if `codespec/profile.yaml` is absent. If no address can be resolved, show “待开发者填写” and ask the developer to provide it; never guess a repository or automatically push across repositories. This reminder does not by itself block the business-code submission. When the user explicitly requests design-document submission, invoke `odk-submit-design-docs`: generate `metadata_tracking.yaml`, validate the five-base-file bundle plus required conditional evidence, and submit `proposal.md`, `spec.md`, `design.md`, `execution-plan.md`, and `metadata_tracking.yaml` together.
- **Phase Gate**: Use the interaction mode below. In interactive mode, artifact approval approves only that document: suggest the next command and wait. Implementation requires an approved execution plan and a user request to implement (natural language or an implement command). In autonomous mode, an explicit end-to-end request authorizes sequential phases within its stated scope: generate and self-check each artifact, summarize decisions, then continue to the authorized next phase. Never infer implementation authorization solely from document approval. TDD remains the default for implementation; untestable Tasks must declare degradation.

## Interaction Mode

Default to **interactive** mode. If the user asks to automate, use recommended options, or run through the workflow ("自动", "全选推荐", "跑完"), use **autonomous** mode within the requested endpoint. Record the mode, authorized endpoint and assumptions at the start; summarize artifact changes, selected recommendations and validation results at every phase, then invoke the next phase without requiring another slash command. "全选推荐" changes how choices are made; it authorizes code changes only when the task also includes implementation. A request to finish design stops at design; an explicit request to implement and deliver may continue through plan, implementation, review and validation.

Self-check every generated artifact and run the packaged validator after each artifact phase (missing downstream artifacts before their phases are expected; report those findings separately). Fix issues in available artifacts before continuing. Stop for missing essential facts, conflicting requirements, failures that cannot be resolved, or a material scope expansion. Previously granted authorization stays effective; neither mode authorizes new publication destinations, merging, destructive operations or separate design-docs submission. Follow the shared delivery handoff for those steps and honor any source-PR submission already requested by the user.


## Context Loading

For actual design-document submission, `odk-submit-design-docs` resolves and confirms the destination first: for an exact `gitcode.com` business origin retain configured `design_docs_repository` or offer `https://gitcode.com/OpenHarmonyAI/design-docs`; other/missing origins require the user to supply the address for this submission, not silently reuse a profile. No answer is not consent; the reminder alone never authorizes cross-repository writes. Confirmation of the document PR authorizes commit/push/PR creation, not merging.

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
- Template files are located at `templates/` (installed with the plugin)

<!-- ODK:reference contracts/skill-guides/router/profiles.md -->
## Profile Detection

When generating ODK artifacts for a module, read `contracts/skill-guides/router/profiles.md` before applying profile overrides; resolve its relative paths from that guide's directory. It defines profile selection, phase mappings, fragment composition and conflict precedence. Routing-only requests do not need this reference.
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

- AI artifact templates: `templates/ai/` (proposal, spec, design, execution-plan, spec-for-validation, threat-model)
- Review templates: `templates/review/` (spec-compliance, code-quality, verification)
- Design-docs submission metadata: `templates/metadata_tracking.yaml`
