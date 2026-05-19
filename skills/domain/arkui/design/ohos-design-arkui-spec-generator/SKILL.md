---
name: ohos-design-arkui-spec-generator
description: Generate ArkUI framework feature specifications by reverse-engineering the current ace_engine implementation. Use when the user asks to "generate spec", "backfill spec", "produce spec for existing feature", "document existing capability" (or Chinese equivalents like "生成规格", "补录规格"), or names a feature path like "04-common-capability/03-common-attributes/01-layout-attributes/Feat-XX-XXX". Produces a spec document under the specs directory (Feat-XX-name-spec.md) and either creates an initial design.md or incrementally updates the existing one. Handles multi-round scope clarification, source-code verification, SDK API cross-check, and incremental design-doc merging (never standalone chapters).
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: arkui
  capability: spec-generator
  version: 0.1.0
  status: trial
  tags:
    - arkui
    - spec
    - design
    - ace-engine
  related-skills:
    - ohos-req-arkui-spec-generator
---

# ArkUI Existing-Feature Spec Generator

Backfill specification documents for features **already implemented** in the ArkUI ace_engine codebase. The output feeds the SDD flow, which uses these specs to guide incremental design for future changes. Core principle: **the current implementation IS the spec** — questionable behaviors may only be annotated (as risks/notes), never modified.

## Feature taxonomy (FuncID / FeatID)

ArkUI specs live in a 3-level functional-domain tree (definition lives outside this repo and is imported incrementally). Top-level examples:

```
01-架构通用设计
   01-架构设计
      01-编译构建
      02-目录结构
      03-部件化
      04-兼容性设计
   02-架构优化
      01-产品化解耦       ← FuncID = 01-02-01
      02-新老框架拆分     ← FuncID = 01-02-02
02-跨平台适配层
   ...
```

- **FuncID** = 3-segment number (e.g. `01-02-01`), identifies a functional domain (the 3rd-level node)
- **FeatID** = `Feat-NN`, identifies one feature within that domain
- **FuncID + FeatID** uniquely identifies a feature system-wide
- Each functional domain owns **one** `design.md`; each feature owns one `Feat-NN-<name>-spec.md`
- Directory under `specs/` mirrors the tree (English-slug names — e.g. `04-common-capability/03-common-attributes/01-layout-attributes/`)

If the target feature is **not yet registered** in the local tree, add the directory path under `specs/` before doing anything else. Confirm the FuncID with the user when the mapping is ambiguous.

## Workflow (execute in order)

### Step 0: Index registration (**mandatory pre-step**)

1. **Read** `specs/index.md` — it is the single source of truth for the feature taxonomy, FuncID/FeatID assignments, and status tracking
2. **Locate or create** the FuncID entry in the "功能域层级树" table:
   - If the target functional domain already has a row → confirm FuncID matches
   - If not → add a new row (斜体 + 下划线 for uncreated) **in FuncID ascending order** and confirm with the user
3. **Determine FeatID**: look at the "已注册特性清单" section for the target FuncID, find the highest existing FeatID, assign the next one (Feat-NN)
4. **Pre-register**: add a FeatID row with status `Draft` to the特性清单 table. If adding a new FuncID section header, ensure it is placed in **FuncID ascending order** within the "已注册特性清单" section
5. Proceed to Step 1 only after the index is updated

### Step 1: Locate target and clarify scope (multi-round Q&A)

1. Parse the user-provided feature path (e.g. `04-通用能力层/03-通用属性/01-布局属性`) → derive FuncID and map to the corresponding `specs/<func-domain>/` directory
2. If the directory does not exist yet, this feature is **unregistered** — create the directory (and parent functional-domain folders) and confirm the FuncID with the user
3. Check the target directory:
   - `design.md` exists → take the **incremental merge** path
   - `design.md` missing → take the **initial design + spec** path
4. **MANDATORY — READ ENTIRE FILE**: Before asking any scope questions, read [`references/qa-checklist.md`](references/qa-checklist.md) completely. It defines the question waves and option structures.
   **Do NOT load** `spec-template.md`, `design-doc-init.md`, or `design-doc-merge.md` at this step.
5. Use `AskUserQuestion` to clarify the following dimensions (**never ask everything at once — batch by dimension**):
   - **Sub-capability scope**: which sub-properties/APIs does this feature cover? (list candidates for the user to multi-select)
   - **Coverage breadth**: cover all setting forms (e.g. x/y, edges, localizedEdges)?
   - **API version range**: do API version differences need to be annotated?
   - **Design-doc strategy** (only when `design.md` already exists): incremental merge into existing chapters vs. new standalone chapters (**strongly prefer the former**)
6. Proceed to Step 2 only after scope is confirmed

### Step 2: Source-code exploration (parallel agents)

Choose the exploration emphasis based on whether the feature is **external-facing** or **framework-internal**:

- **External API features** (ArkTS attributes, declarative methods): cross-verify implementation source against the **canonical SDK type definitions** under `<OpenHarmony_root>/interface/sdk-js/api/`. This is the **only** source of truth for external API contracts — never infer API signatures from internal source code or knowledge-base markdown files. Typical lookup paths:
  - **Static API**: `interface/sdk-js/api/arkui/component/<name>.static.d.ets` (e.g. `text.static.d.ets`)
  - **Dynamic API**: `interface/sdk-js/api/@internal/component/ets/<name>.d.ts` (e.g. `text.d.ts`)
  - **Dynamic Modifier**: `interface/sdk-js/api/arkui/<Name>Modifier.d.ts` (e.g. `TextModifier.d.ts`)
  - `docs/sdk/ArkUI_SDK_API_Knowledge_Base.md` and `docs/sdk/Component_API_Knowledge_Base_CN.md` serve as supplementary references only — if they disagree with the `.d.ts`/`.d.ets` files, the type definition files win
- **Framework-internal capabilities** (layout pipeline, render flow, lifecycle, internal utilities): focus exclusively on the source code; SDK type definitions typically don't cover these

Use **multiple parallel Explore agents** to cover each implementation layer. Typical layers:
- JS bridge: `frameworks/bridge/declarative_frontend/jsview/js_view_abstract.cpp`
- API layer: `frameworks/core/components_ng/base/view_abstract.cpp`
- Property layer: `frameworks/core/components_ng/property/`, `layout/layout_property.cpp`
- Render layer: `frameworks/core/components_ng/render/`, `render/adapter/rosen_render_context.cpp`
- Layout algorithm: `frameworks/core/components_ng/layout/box_layout_algorithm.cpp`
- C-API: `interfaces/native/native_node.h`, `frameworks/core/interfaces/native/node/`

Focus areas: API version differences, storage location, property change flags (`PROPERTY_UPDATE_*`), mutual exclusion, RTL/localization handling, **and any external input that affects behavior** (parent-context state, system locale, screen density, theme).

If the feature is too large for a single sweep (e.g. 10+ sub-properties or multi-layer overhaul), **split into sub-tasks** — generate one Feat-XX spec per cohesive sub-capability, share the same design.md baseline, and register all of them in the "后续 Task 拆分" table.

### Step 3: Highlight key findings, get confirmation

Present **3-7 non-obvious design decisions** to the user (e.g. storage-layer split, API version behavior changes, mutual-exclusion priority, special default values) and ask which should be emphasized in the spec. Selected items become inputs for ADRs, risks, and compatibility entries.

### Step 4: Generate the spec document

**MANDATORY — READ ENTIRE FILE**: Before writing any spec content, read [`references/spec-template.md`](references/spec-template.md) completely — the chapter skeleton has per-chapter content requirements that are NOT reproduced here.
**Do NOT load** `design-doc-init.md` or `design-doc-merge.md` at this step.

Write `specs/<func-domain>/Feat-XX-<name>-spec.md`. Required content:

- US (User Stories) + AC (Acceptance Criteria, numbered AC-X.Y)
- Business rules / functional rules / exception rules / recovery contracts
- Verification mapping (every AC has at least one verification means)
- API change analysis (ArkTS + C-API dual channel)
- Compatibility declaration (behavior differences listed by API version)
- Behavior scenarios (Gherkin Given/When/Then)

### Step 5: Handle design.md (**critical step**)

Branch based on the design.md state detected in Step 1:

#### 5A. design.md **does not exist** → generate initial design document

**MANDATORY — READ ENTIRE FILE**: Read [`references/design-doc-init.md`](references/design-doc-init.md) completely before generating any content.
**Do NOT load** `design-doc-merge.md` at this step.

When the functional domain has no design doc, create one as the baseline before producing the spec.

Key points:
- Fixed filename `design.md`, written to `specs/<func-domain>/`
- Top-level chapters must follow the "standard 13-chapter" structure
- Design ID format: `DESIGN-Func-<domain-numbers>` (e.g. `DESIGN-Func-04-03-01`)
- The current feature is the **first** Feat under this design — all ADRs / architecture diagrams / data models / detailed designs go **directly into the corresponding chapters** without `(Feat-XX)` suffixes (they're the baseline)
- Subsequent Feats use the 5B incremental-merge path

#### 5B. design.md **already exists** → incremental merge

**MANDATORY — READ ENTIRE FILE**: Read [`references/design-doc-merge.md`](references/design-doc-merge.md) completely before merging any content.
**Do NOT load** `design-doc-init.md` at this step.

New feature content **must never** open a new `## Feat-XX Detailed Design` chapter — merge each item into the corresponding existing chapter.

Merge checklist:
1. **Design metadata** — append new Feat-XX to the `Target Feature` field
2. **需求基线** — append new feature's goal to the supplementary notes
3. **Repos & modules** table — append new module rows
4. **Key design decisions** table — append `ADR-FX-N` rows (right after existing ADRs)
5. **API 签名与权限** — append new API entries with signature, d.ts location, permissions, SysCap
6. **构建系统影响** — append BUILD.gn / bundle.json changes
7. **Architecture diagram** — under the existing diagram, add a `#### XX Architecture Diagram (Feat-XX)` subsection
8. **Data model design** — under the existing data model, add a `#### XX Data Model (Feat-XX)` subsection
9. **Detailed design** — append `### <capability name>` subsections (same level as existing ones — do NOT open a new H2)
10. **Risks & open issues** table — append new risk rows
11. **后续 Task 拆分** table — append the new task row

### Step 6: Self-review and delivery

- Verify the spec file's H2/H3 structure is complete (cross-check against Feat-01's standard chapters)
- Verify design.md has no leftover standalone `## Feat-XX` chapters
- Run `grep -n "^## "` against design.md to confirm the top-level chapter sequence is correct
- **Update `specs/index.md`**: change the FeatID row status from `Draft` to `Baselined`

## Diagram rules

- **All diagrams must use Mermaid syntax** — Mermaid renders natively on most Markdown viewers.
- Diagram types: `graph TB` (layered architecture), `graph TD` (pipeline/flow), `sequenceDiagram` (cross-component timing), `subgraph` (containment/nesting).
- Keep diagrams **flat enough to render well** — avoid nesting subgraphs more than 2 levels deep. Use `<br/>` for multi-line labels inside nodes.
- Applies to both `design.md` (architecture diagrams, constraint pipeline, layout flow, paint rect flow) and `Feat-XX-spec.md` (if any diagrams are needed).

## Anti-patterns (forbidden)

❌ Opening a new `## Feat-XX 详细设计` top-level chapter in design.md — always merge into existing chapters (see merge mapping in `design-doc-merge.md`)
❌ Naming first-Feat decisions `ADR-F1-N` — first Feat uses baseline `ADR-1, ADR-2, ...`; only subsequent Feats use `ADR-FX-N`
❌ Proposing fixes or improvements when source behavior is questionable — annotate as risk/note only ("the current implementation IS the spec")
❌ Asking all scope questions in a single `AskUserQuestion` call — batch by dimension across 2-4 waves
❌ Writing spec content without reading the template — the chapter skeleton is non-negotiable
❌ Creating one design.md per Feat — one functional domain owns exactly one design.md shared by all Feats
❌ Inventing custom Design ID formats — must be `DESIGN-Func-XX-XX-XX`
❌ Skipping `## 不涉及项承接` or `## 设计审批` chapters in design.md
❌ Using ASCII box art for diagrams — all diagrams must use Mermaid syntax
❌ Silently reconciling SDK-vs-source discrepancies — the deviation must be visible in both spec and risks table
❌ Inferring API signatures from internal C++ source, JS bridge files, or knowledge-base markdown instead of reading the canonical `.d.ts` / `.d.ets` / `.static.d.ets` files under `interface/sdk-js/api/`

## Conflict resolution

When source code behavior and SDK type definitions disagree:

1. **SDK type definition is the contract** for external APIs — the `.d.ts` / `.d.ets` / `.static.d.ets` files under `interface/sdk-js/api/` define the authoritative API surface. Document the SDK-defined behavior in the spec's API chapter
2. **Source deviation is a risk** — add a row to the spec's compatibility / risks table: "Source implements X, SDK defines Y"
3. **Never silently reconcile** — the discrepancy must be visible to downstream SDD consumers
4. For **framework-internal** capabilities, source code IS the truth — no SDK cross-check needed

## Freedom calibration

- **Format & structure** → zero freedom: chapter skeleton, ID formats, file naming, merge mapping are all fixed — deviation produces invalid output
- **Exploration & analysis** → high freedom: choose agents, layers, and depth based on feature complexity
- **Scope & emphasis** → user-driven: ask in waves, let the user decide breadth and highlights

## Hard constraints

- **Implementation IS the spec**: if source behavior is questionable, write a risk/note — do NOT propose fixes
- **All claims need file:line references**: every assertion must trace back to ace_engine source
- **APIs must be SDK-verified from canonical type definitions**: for external APIs, read the actual `.d.ts` / `.d.ets` / `.static.d.ets` files under `<OpenHarmony_root>/interface/sdk-js/api/` — these are the single source of truth for API signatures, parameter types, return types, and `@since` versions. Do NOT infer API signatures from internal C++ source, JS bridge files, or knowledge-base markdown. `docs/sdk/*.md` files are supplementary only; when they disagree with type definitions, type definitions win. Framework-internal capabilities don't need SDK cross-check.
- **Incremental first**: when design.md exists, never open a new `## Feat-XX` top-level chapter
- **No fabricated ACs**: every AC must map to existing source behavior or tests
- **Don't over-batch AskUserQuestion**: ask in waves — scope first, then strategy, then highlight confirmation
- **Cover every external input**: parent state, system locale, density/scale, theme, API version, lifecycle stage — anything that can change behavior must be enumerated, especially anything that could become a future **compatibility risk**
- **Split large features into sub-tasks**: if scope grows beyond a single coherent spec, generate multiple Feat-XX specs sharing one design.md
- **Spec consumers are the SDD flow**: downstream SDD flow reads these specs to plan incremental changes — be exhaustive on observable behavior and version differences, since omissions become silent regressions
