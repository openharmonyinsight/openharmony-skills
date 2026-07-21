# Two-Layer Command Architecture

> **Status**: Implemented  
> **Related**: Issue #26, PR #14  
> **Replaces**: `odk-flow` (to be renamed to `odk-sp-run`), `odk-implement` (moved to bridge layer)
> **2026-06 dist note**: This design predates the `dist/*` migration. Current installable outputs are generated under `dist/claude`, `dist/codex`, and `dist/opencode`; `packaging/*` now only keeps static shell inputs.
> **2026-06 #90 方案 D note**: Code mapping (AC → file + Task + verification status) moved from `spec.md` to `execution-plan.md` (「代码范围映射」+「AC 到 Task 追溯」). All command descriptions and Implementation Plan references below reflect this.

## Motivation

PR #14 introduced Superpowers bridge wrappers (`odk-flow`, `odk-implement`, modified `odk-review`), but the design had three problems:

1. **Base layer polluted**: `odk-review` was modified to call Superpowers, breaking standalone usage.
2. **Naming opaque**: `odk-flow` doesn't convey "ODK + Superpowers full delivery" to developers.
3. **No layering**: Base commands and bridge commands were mixed at the same level, making the plugin dependency graph unclear.

This design introduces a clean two-layer architecture:

- **Base layer** (`odk-<verb>`): Standalone, template-driven, zero plugin dependencies. Every phase has a command.
- **Bridge layer** (`odk-<plugin>-<verb>`): Fuses ODK with a specific execution plugin. Command names map directly to that plugin's native concepts.

## Design Principles

1. **Base commands never depend on plugins** — they always work standalone.
2. **Bridge commands explicitly declare their plugin** — `odk-sp-*` means "ODK + Superpowers".
3. **Bridge command names mirror plugin concepts** — `odk-sp-brainstorm` maps to `/superpowers:brainstorming`.
4. **Bridge commands are not split** — one Superpowers session = one bridge command. Don't artificially split an indivisible workflow.
5. **Graceful degradation** — every bridge command falls back to base commands when the plugin is unavailable.

---

## Base Layer Commands (10 commands)

All base commands are **template-driven** and have **zero plugin dependencies**.

```
Phase 0:  odk-init              Create .codespec/changes/<id>/ skeleton
Init      odk-link-issue        Link draft directory to issue ID

Phase 1:  odk-propose           Generate proposal.md (8-dim N/A, success criteria)
Define    odk-spec              Generate spec.md (WHEN/THEN AC, verification mapping)
          odk-design            Generate design.md (Mermaid diagrams, decision comparison,
                                references spec AC numbers, resolves TBD error codes)

Phase 2:  odk-plan              Generate execution-plan.md (AC-Task traceability, dependency graph)
Plan

Phase 3:  odk-implement  [NEW]  AI-assisted Task-by-Task implementation, backfill execution-plan code scope (no plugin deps)
Implement

Phase 4:  odk-review            Generate 3 review documents from templates (standalone)
Review

Phase 5:  odk-validate          Validate Level A/B/C/D readiness
Validate

(bypass)  odk-spec-for-validation   Generate spec-for-validation.md from spec/design (validation scenarios)
                                  Optional bypass — does not block the main flow
```

### `odk-implement` (new base command)

The base `odk-implement` is an **AI-assisted implementation tracker with zero plugin dependencies**. It follows the execution plan and writes code directly, without requiring Superpowers TDD cycles or subagent-driven execution. "Without Superpowers TDD cycles" means it does not use the subagent red/green mechanism — it does **not** mean it skips tests. Base `odk-implement` still enforces test-first discipline per Task: each Task writes a failing test (or a documented reproducible evidence gap) before implementation, per the `execution-plan.md` Task template.

1. Read `spec.md` AC list and `execution-plan.md` 代码范围映射
2. Read `execution-plan.md` Task list, dependency graph, and file scope
3. For each Task (respecting dependency order):
   - Present the Task description and planned file scope
   - Implement the code changes within the declared file boundaries
   - Run the verification command and confirm it passes
   - After each Task, update `execution-plan.md` 代码范围映射 with actual files, tests, and commit references
4. If implementation reveals missing ACs or changed scope, pause and update `spec.md` / `execution-plan.md`

---

## Bridge Layer Commands (varies by plugin: SP=4, OPS=2, MS=5)

### Naming Convention

```
odk-<plugin>-<verb>

plugin = sp   (Superpowers)
         ops  (OpenSpec)
         ms   (MatrixSpec)
```

### ODK + Superpowers (`odk-sp-*`)

```
odk-sp-brainstorm     brainstorming → proposal.md + spec.md + design.md
                      Single session: clarification → approach selection → design approval
                      Output redirected to .codespec/ via Output Redirection Rules

odk-sp-plan           writing-plans → execution-plan.md
                      Task decomposition + dependency analysis + file boundaries
                      → Convert to ODK format + AC-Task traceability

odk-sp-implement      TDD + subagent-driven-development → code + backfill
                      RED-GREEN-REFACTOR cycle + Task-level execution + file scope constraint

odk-sp-review         requesting-code-review + verification-before-completion
                      → evidence/reviews/
                      Review + verification results as ODK evidence source, then persist

> `odk-sp-run` was removed — no full-flow orchestrator. Each plugin manages its own workflow.
> Users invoke bridge commands individually for better context management.
```

### ODK + OpenSpec (`odk-ops-*`)

```
odk-ops-propose       /opsx:propose → proposal.md + spec.md + design.md + execution-plan.md
                      Single OpenSpec command covers Define+Specify+Design+Plan; ODK bridge
                      splits into 4 artifacts with ODK-required chapters.

odk-ops-apply         /opsx:apply → code + execution-plan code scope backfill
                      Implements code and backfills execution-plan.md code scope.
```

### ODK + MatrixSpec (`odk-ms-*`)

```
odk-ms-proposal       /matspec.proposal → proposal.md
odk-ms-delta-spec     /matspec.delta-spec → spec.md (delta format)
odk-ms-delta-design   /matspec.delta-design → design.md (delta format)
odk-ms-tasks          /matspec.tasks → execution-plan.md
odk-ms-validation     /matspec.validation → evidence/reviews/
```

> MatrixSpec stage order (proposal → delta-spec → delta-design → tasks) is the same as ODK's
> default (proposal → spec → design → plan). Both put spec before design. Bridge commands
> follow the source plugin's native workflow — this is by design. See adapters.md for detail.

### Mapping table

```
Superpowers native concept          ODK bridge command     ODK artifact
─────────────────────────           ──────────────         ─────────────────────
brainstorming                       odk-sp-brainstorm      proposal + spec + design
writing-plans                       odk-sp-plan            execution-plan
TDD + subagent-driven-dev           odk-sp-implement       code + execution-plan code scope
requesting-code-review              odk-sp-review          evidence/reviews/
+ verification-before-completion
(all of the above)                  (removed)             —
```

> `odk-sp-run` was removed because Superpowers' natural skill flow already provides phase-to-phase transitions, and a full-flow orchestrator accumulated context across all phases. OpenSpec and MatrixSpec have their own workflow management and don't need ODK-level orchestration.
```

### Extending to other plugins

```
              Superpowers           OpenSpec              MatrixSpec
              ──────────            ────────              ──────────
explore:      (direct /opsx:explore)                      (direct /opsx:explore)
define:       odk-sp-brainstorm     odk-ops-propose       odk-ms-proposal
specify:      (in brainstorm)       (in propose)          odk-ms-delta-spec
design:       (in brainstorm)       (in propose)          odk-ms-delta-design
plan:         odk-sp-plan           (in propose)          odk-ms-tasks
implement:    odk-sp-implement      odk-ops-apply         (matspec state machine)
review:       odk-sp-review         (direct /opsx:verify) odk-ms-validation
```

> Commands map 1:1 to source plugin native concepts. No `odk-*-run` orchestrators — each plugin manages its own workflow.

---

## Full Command Mapping

| Phase | Base (`odk-*`) | SP Bridge | OPS Bridge | MS Bridge | ODK Artifact |
|-------|---------------|-----------|------------|-----------|--------------|
| Init | `odk-init` / `odk-link-issue` | — | — | — | `.codespec/changes/<id>/` |
| Define | `odk-propose` | `odk-sp-brainstorm` | `odk-ops-propose` | `odk-ms-proposal` | `proposal.md` |
| Specify | `odk-spec` | (in brainstorm) | (in propose) | `odk-ms-delta-spec` | `spec.md` |
| Design | `odk-design` | (in brainstorm) | (in propose) | `odk-ms-delta-design` | `design.md` |
| Plan | `odk-plan` | `odk-sp-plan` | (in propose) | `odk-ms-tasks` | `execution-plan.md` |
| Implement | `odk-implement` | `odk-sp-implement` | `odk-ops-apply` | (state machine) | code + tests + execution-plan code scope |
| Review | `odk-review` | `odk-sp-review` | (direct verify) | `odk-ms-validation` | `evidence/reviews/` |
| Validate | `odk-validate` | — | — | — | Level A/B/C/D pass |

Base commands are template-driven and work standalone. Bridge commands map 1:1 to source plugin native concepts and fall back to base commands when the plugin is unavailable. No `odk-*-run` orchestrators — each plugin manages its own workflow.

### Usage Decision

```
Has Superpowers installed?
  ├── Yes → Use odk-sp-* for process discipline + automatic ODK output
  └── No  → Use odk-* for template-driven generation + AI-assisted implementation
```

---

## Responsibilities

| Layer | Scope | Dependency | Fallback |
|-------|-------|-----------|----------|
| Base (`odk-*`) | Document generation, validation, AI-assisted implement tracking | None | N/A |
| Bridge (`odk-sp-*`) | Plugin delegation, format conversion, archive backfill | Target plugin | Corresponding base command(s) |

### Degradation strategy

Every bridge command MUST declare in its Preconditions:

```markdown
If Superpowers skills are unavailable, fall back to the corresponding base ODK
command(s) and clearly report the degradation.
```

| Bridge command | Fallback |
|---------------|----------|
| `odk-sp-brainstorm` | `odk-propose` + `odk-spec` + `odk-design` |
| `odk-sp-plan` | `odk-plan` |
| `odk-sp-implement` | `odk-implement` (base) |
| `odk-sp-review` | `odk-review` |
| `odk-ops-propose` | `odk-propose` + `odk-spec` + `odk-design` + `odk-plan` |
| `odk-ops-apply` | `odk-implement` |
| `odk-ms-proposal` | `odk-propose` |
| `odk-ms-delta-spec` | `odk-spec` |
| `odk-ms-delta-design` | `odk-design` |
| `odk-ms-tasks` | `odk-plan` |
| `odk-ms-validation` | `odk-review` |

---

## Implementation Plan

> **Status**: This section records the original implementation steps. Steps 1–12 have been completed. Subsequent changes:
> - `odk-sp-run` was **removed** — no full-flow orchestrator; users invoke bridge commands individually for better context management.
> - `using-odk` was **split** into `using-odk` (base, ~98 lines) + `using-odk-bridge` (output redirection + mode selection, ~46 lines) for context cost reduction.
> - Bridge commands now map **1:1 to source plugin native concepts** (not ODK phase decomposition). OpenSpec has `odk-ops-propose`/`odk-ops-apply`; MatrixSpec has 5 stage-aligned commands.
> - Output mode selection (strict/passthrough/merge) was added to `using-odk-bridge`.

### Step 1: Create base `odk-implement`

**New file**: `core/skills/odk-implement/SKILL.md`

This is a standalone command that reads `execution-plan.md`, implements each Task with AI assistance, and backfills `execution-plan.md` code scope (代码范围映射). No plugin dependency.

### Step 2: Rename `odk-flow` → `odk-sp-run`

**Rename** (git mv):
```
core/skills/odk-flow/SKILL.md  →  core/skills/odk-sp-run/SKILL.md
```

**Update** internal references:
- Frontmatter `name:` → `odk-sp-run`
- Section `# ODK Flow` → `# ODK SP Run`
- All `{{CMD_PREFIX}}flow` → `{{CMD_PREFIX}}sp-run`
- All `odk-flow` → `odk-sp-run`
- All `/odk-validate` → `{{CMD_PREFIX}}sp-review` references → update accordingly

**Update** the flow references within `odk-sp-run`:
- Step 3 "Invoke `odk-implement`" → "Invoke `odk-sp-implement`"
- Step 4 "Invoke `odk-review`" → "Invoke `odk-sp-review`"

### Step 3: Create `odk-sp-brainstorm`

**New file**: `core/skills/odk-sp-brainstorm/SKILL.md`

Extract the Define & Explore phase from `odk-sp-run` as a standalone command:

- Invoke Superpowers `brainstorming`
- Apply Output Redirection Rules to intercept writes to `docs/superpowers/specs/`
- Generate `proposal.md` + `spec.md` + `design.md` using ODK templates
- Preserve ODK-required fields (target_release, non-goals, 8-dim N/A, AC numbering, verification mapping)

### Step 4: Create `odk-sp-plan`

**New file**: `core/skills/odk-sp-plan/SKILL.md`

Extract the Plan phase from `odk-sp-run` as a standalone command:

- Invoke Superpowers `writing-plans`
- Redirect plan output to `.codespec/changes/<id>/execution-plan.md`
- Transform into ODK format, add AC-Task traceability
- Populate `execution-plan.md` AC-Task 追溯 (AC / Task / verification status)

### Step 5: Rename `odk-implement` → `odk-sp-implement`

**Rename** (git mv):
```
core/skills/odk-implement/SKILL.md  →  core/skills/odk-sp-implement/SKILL.md
```

**Update** internal references:
- Frontmatter `name:` → `odk-sp-implement`
- Section `# ODK Implement` → `# ODK SP Implement`
- All `{{CMD_PREFIX}}implement` → `{{CMD_PREFIX}}sp-implement`

### Step 6: Create `odk-sp-review`

**New file**: `core/skills/odk-sp-review/SKILL.md`

A new bridge command (NOT a modification of base `odk-review`):

- Invoke Superpowers `requesting-code-review`
- Invoke Superpowers `verification-before-completion`
- Generate 3 ODK review documents using Superpowers results as primary evidence
- Degradation: if Superpowers unavailable, fall back to base `odk-review`

### Step 7: Revert `odk-review` modifications

PR #14 modified `core/skills/odk-review/SKILL.md` to call Superpowers. **Revert this** — base `odk-review` must remain standalone.

The original steps (pre-PR #14) were:
```
1. Read spec.md AC list
2. Read execution-plan.md Task list and code scope
3. Read review templates
4. Generate 3 review documents from templates
5. Backfill execution-plan code scope (代码范围映射)
```

Restore this. No Superpowers calls in the base `odk-review`.

### Step 8: Update `using-odk/SKILL.md`

Update the Phase Skills section to reflect the two-layer structure:

```markdown
## Phase Skills

### Base Commands (standalone, no plugin required)

Invoke via Skill tool: `odk-init` / `odk-propose` / `odk-spec` / `odk-design` /
`odk-plan` / `odk-implement` / `odk-review` / `odk-validate` / `odk-link-issue`.
Each skill loads its own full context.

### Bridge Commands (plugin-specific)

| Plugin | Commands |
|--------|----------|
| Superpowers (`sp`) | `odk-sp-brainstorm` / `odk-sp-plan` / `odk-sp-implement` / `odk-sp-review` |
```

### Step 9: Update `packaging/codex/README.md`

Update the workflow diagram and command table to reflect new names:
- `odk-flow` → `odk-sp-run`
- `odk-implement` → `odk-sp-implement`
- Add new commands: `odk-sp-brainstorm`, `odk-sp-plan`, `odk-sp-review`
- Add base `odk-implement` to the workflow

### Step 10: Update `validate-superpowers-bridge.sh`

Update the script to check for the new file names:
```
core/skills/odk-sp-run/SKILL.md
core/skills/odk-sp-brainstorm/SKILL.md
core/skills/odk-sp-plan/SKILL.md
core/skills/odk-sp-implement/SKILL.md
core/skills/odk-sp-review/SKILL.md
```

And their generated distribution counterparts under `dist/*`.

### Step 11: Run distribute-skills.sh

Run `scripts/distribute-skills.sh` to regenerate all installable distribution files under `dist/*`.

### Step 12: Verify

1. `bash scripts/validate-superpowers-bridge.sh` passes
2. `bash scripts/validate-codex-hooks.sh` passes
3. `bash scripts/validate-codex-package.sh` passes
4. All `wc -l` counts are within context budget

---

## File Change Summary

```
NEW:
  core/skills/odk-implement/SKILL.md             (base layer)
  core/skills/odk-sp-run/SKILL.md                (formerly odk-flow, renamed)
  core/skills/odk-sp-brainstorm/SKILL.md          (new bridge command)
  core/skills/odk-sp-plan/SKILL.md                (new bridge command)
  core/skills/odk-sp-implement/SKILL.md           (formerly odk-implement, renamed)
  core/skills/odk-sp-review/SKILL.md              (new bridge command)

DELETE:
  core/skills/odk-flow/SKILL.md                   (renamed to odk-sp-run)
  core/skills/odk-implement/SKILL.md              (renamed to odk-sp-implement)

MODIFY (revert):
  core/skills/odk-review/SKILL.md                 (remove Superpowers calls)
  core/skills/using-odk/SKILL.md                  (update Phase Skills section)

MODIFY:
  packaging/codex/README.md                       (update command names)
  scripts/validate-superpowers-bridge.sh           (update file paths)

REGENERATE (via distribute-skills.sh):
  dist/claude/skills/odk-*/SKILL.md
  dist/claude/skills/odk-sp-*/SKILL.md
  dist/claude/skills/using-odk/SKILL.md
  dist/codex/skills/odk-*/SKILL.md
  dist/codex/skills/odk-sp-*/SKILL.md
  dist/codex/skills/using-odk/SKILL.md
  dist/opencode/commands/odk-*.md
  dist/opencode/commands/odk-sp-*.md
```

---

## Context Budget Check

Each new skill file:
- `odk-sp-brainstorm`: ~45 lines
- `odk-sp-plan`: ~35 lines
- `odk-sp-review`: ~35 lines
- `odk-sp-run`: ~75 lines (from odk-flow)
- `odk-sp-implement`: ~40 lines (from odk-implement)
- `odk-implement` (base): ~40 lines

Total core skill additions: ~270 lines across 6 files (each loaded independently, not all at once).

`using-odk/SKILL.md` Phase Skills section update: net +~5 lines.

All within acceptable limits.
