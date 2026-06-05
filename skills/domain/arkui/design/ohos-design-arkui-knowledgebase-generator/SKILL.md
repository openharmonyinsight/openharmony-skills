---
name: ohos-design-arkui-knowledgebase-generator
description: Generate or update ArkUI knowledge base documents for ace_engine components and framework subsystems. Use when the user asks to "生成知识库", "补齐知识库", "新增 KB", "更新知识库", "写知识库文档", "generate knowledge base", "create KB", "update KB doc", or mentions creating/updating knowledge base documents under docs/. Covers both component-type KBs (Text, Slider, etc.) and framework-type KBs (ThemeManager, Pipeline, Gesture, etc.). Do NOT use for CLAUDE.md files, README updates, or code changes — this skill is documentation-only.
---

# ArkUI Knowledge Base Generator

## Hard Rules

1. **Clarify before explore** — Never start code exploration until target, type (component vs framework), and scope are confirmed through multi-round Q&A.
2. **KB-first** — Always run `python3 docs/kb_search.py <name> --field name` before any code search.
3. **Source-of-truth for API** — API information MUST come from actual SDK declaration files and source code, never from memory. See `docs/api/ArkUI_API_Paradigm_Knowledge_Base_CN.md` for paradigm paths.
4. **Template-first** — Always read `docs/knowledge_base_TEMPLATE.md` before generating output. Use component template (1A) or framework template (1B) based on type.
5. **Mermaid graphs** — All architecture/hierarchy/flow diagrams use Mermaid `graph` format, not ASCII art.
6. **Index sync** — Every KB doc must have a matching entry in `docs/knowledge_base_INDEX.json`.

## NEVER

- NEVER write API signatures from memory — always extract from actual `.d.ts`/`.static.d.ets` files. Line numbers drift across versions; re-verify with `grep -n`.
- NEVER include ace_engine internal bridge paths (e.g., `ark_modifier/`, `jsview/`) in public "API 清单" — only SDK-facing declaration files.
- NEVER copy code snippets or line numbers from existing KB docs as-is — source changes between versions; re-read the current file to verify.
- NEVER start code exploration before Phase 1 clarification completes — exploring the wrong scope is the biggest time waste.
- NEVER assume Dynamic API filenames match Static — Dynamic uses snake_case (`text_clock.d.ts`), Static uses camelCase (`textClock.static.d.ets`).
- NEVER generate a KB for a target that doesn't exist in `components_ng/pattern/` or `frameworks/core/` — verify the directory exists first.
- NEVER use ASCII box art (`┌──┐`, `│  │`) for diagrams — Mermaid `graph` only.

## Workflow

### Phase 1: Clarification (ask one question at a time)

1. What component or subsystem? (e.g., "Slider", "ThemeManager")
2. Component or framework? (has `<Name>Attribute`/`<Name>Modifier` → component; otherwise → framework)
3. New KB or update existing? If update, which sections?

Exit when all three are confirmed. Do NOT proceed without confirmation.

### Phase 2: Source Exploration

**MUST read [references/workflow.md](references/workflow.md)** before starting exploration — it contains paradigm path patterns, extraction methods, and output structure checklists not repeated here.

**Step 0: Scope check — before exploring, ask yourself:**
- Is this standalone or part of a component family? (e.g., TextInput/TextArea/Search share TextField base)
- Does it have all 5 API paradigms, or is it too new/legacy for some?
- Simple (single pattern file) or complex (10+ files with sub-patterns)?

**Step 1: KB lookup**
Run `python3 docs/kb_search.py <name> --field name`.
- **Found** → read existing KB, identify gaps, proceed to fill them.
- **Not found** → no existing KB, fall through to full code exploration below. Find a similar component/subsystem that already has a KB (e.g., Text for text-like components, Scroll for scrollable containers) and use it as structural reference.

**Component path:**
1. Source code: `frameworks/core/components_ng/pattern/<comp>/` — pattern, model, properties, events. If unfamiliar, reference a similar component's KB (from `docs/pattern/`) to understand the typical file layout and class roles.
2. API files across all paradigms (Dynamic `.d.ts`, Static `.static.d.ets`, Modifier, CAPI `NODE_<COMP>_*`)
3. Build cross-paradigm attribute comparison table

**Framework path:**
1. Identify interface + impl files. If unfamiliar, reference an existing framework KB (e.g., `docs/architecture/ThemeManager_Architecture_CN.md`) for structural guidance.
2. Map class hierarchy and data structures
3. Trace 2-3 core flows
4. Identify extension points

**Edge cases:**

| Situation | How to Handle |
|-----------|---------------|
| SDK-JS repo not cloned | Check `<OH_ROOT>/interface/sdk-js/`; if missing, warn user and skip API paradigm columns |
| No Dynamic API file | Some components (Sheet, LazyGrid) only have Static. Use Static as primary axis for the attribute table |
| No CAPI file | Most components lack CAPI. Mark ❌ in the table, don't leave blank |
| Multiple source dirs | Some components span directories (e.g., Flex → Row/Column/Wrap). Document all related paths |
| Component family | TextInput/TextArea/Search share `text_field/`. Decide whether to write one KB per component or one for the family, and confirm with user |

### Phase 3: Generate KB Document

1. Read `docs/knowledge_base_TEMPLATE.md` — pick 1A (component) or 1B (framework)
2. Fill every section with verified source data; cite file:line
3. Use Mermaid `graph BT` for class hierarchies, `graph TD` for flows and architecture
4. For component API tables: Dynamic API `<Comp>Attribute` as primary axis, mark ✅/❌ per paradigm

### Phase 4: Update Index & README

1. Add/update entry in `docs/knowledge_base_INDEX.json`
2. Component entries: `api_paths` with `dynamic`/`static`/`modifier`/`modifier_static`/`capi` (only existing files)
3. Framework entries: `api_paths` usually empty, `source_paths` keys by role (`interface`/`impl`/`manager`)
4. Update `docs/knowledge_base_README.md` — sync KB count, category lists, or any summary tables affected by the new/changed entry
5. Validate: `python3 -m json.tool docs/knowledge_base_INDEX.json > /dev/null`
6. Smoke test: `python3 docs/kb_search.py <name> --field name`

### Phase 5: Source Verification

Phase 3/4 output may contain non-existent file paths or incorrect API coverage marks. Verify before delivering.

**KB document checks:**
1. **Source file existence** — `ls` every source file path referenced in the KB doc
2. **Class hierarchy** — `grep "class <ClassName>" <file>` to verify Mermaid graph matches actual inheritance

**API table checks (component type):**
3. **API file existence** — For each paradigm marked ✅ in the "API declaration path" table, `ls` the file
4. **Attribute spot-check** — Pick 3-5 attributes from the attribute table, `grep` each in the corresponding paradigm file to confirm presence

**INDEX entry checks:**
5. **source_paths** — `ls` every path in the INDEX entry's `source_paths`
6. **api_paths** — `ls` every path in the INDEX entry's `api_paths`
7. **Search consistency** — `python3 docs/kb_search.py <name>` output's `file_path` points to an existing file

**README checks:**
8. **KB count** — `find docs -name "*_Knowledge_Base*.md" -type f | wc -l` matches the count stated in README
9. **Category coverage** — new KB's category is listed in README's category summary if one exists

Fix any inconsistency immediately — do not mark as "to be confirmed".

## Key Path References

| What | Path |
|------|------|
| Template | `docs/knowledge_base_TEMPLATE.md` |
| Index | `docs/knowledge_base_INDEX.json` |
| README | `docs/knowledge_base_README.md` |
| API paradigm guide | `docs/api/ArkUI_API_Paradigm_Knowledge_Base_CN.md` |
| KB search script | `docs/kb_search.py` |
| OH_ROOT | ace_engine 的 `../../../..`（即 OpenHarmony 源码根），用 `cd ../../../.. && pwd` 确认 |
| Dynamic API dir | `{OH_ROOT}/interface/sdk-js/api/@internal/component/ets/` |
| Static API dir | `{OH_ROOT}/interface/sdk-js/api/arkui/component/` |
| Modifier API dir | `{OH_ROOT}/interface/sdk-js/api/arkui/` |
| CAPI enums | `interfaces/native/native_node.h` (`NODE_<COMP>_*`) |
| Component source | `frameworks/core/components_ng/pattern/<comp>/` |
