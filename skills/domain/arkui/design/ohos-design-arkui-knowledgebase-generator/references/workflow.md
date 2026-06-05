# KB Generator Workflow Reference

## Phase 1: Clarification Loop

### Goal
Narrow down the exact scope before any exploration.

### Questions to ask (one at a time)

1. **Target identification**: What component or subsystem to document?
   - Component name (e.g., Text, Slider, Button)
   - Framework/system name (e.g., ThemeManager, Layout Framework, Pipeline)

2. **Type determination**: Is this a public UI component or an internal engine mechanism?
   - Component → use component template (1A)
   - Framework → use framework template (1B)
   - Not sure → check if `<Name>Attribute` / `<Name>Modifier` exists in SDK-JS

3. **Scope**: What content needs to be created or updated?
   - Full KB creation from scratch
   - Update existing KB (which sections?)
   - API section only
   - Architecture section only

4. **Existing state check**: Run `python3 docs/kb_search.py <name> --field name` to see if KB already exists.

### Exit condition
Proceed only when target, type, and scope are all confirmed.

---

## Phase 2: Source Exploration

### For Components (type=component)

#### Step 2a: KB-first lookup
```bash
python3 docs/kb_search.py <component> --field name
```
- **Found** → read existing KB, identify which sections are missing or outdated.
- **Not found** → no existing KB. Find a structurally similar component that already has a KB to use as reference:
  - Text-like → reference `docs/pattern/text/Text_Knowledge_Base_CN.md`
  - Container/scrollable → reference `docs/pattern/scroll/Scroll_Knowledge_Base.md`
  - Selector/picker → reference `docs/pattern/text_picker/Text_Picker_Knowledge_Base.md`
  - Use `python3 docs/kb_search.py --list-all` to browse all available KBs.

#### Step 2b: Source code exploration
```
frameworks/core/components_ng/pattern/<component>/
├── *_pattern.h/cpp      → class hierarchy, lifecycle, state
├── *_model_ng.h/cpp     → public API → property bridge
├── *_layout_property.h  → property declarations
├── *_event_hub.h        → events
├── *_layout_algorithm.*  → layout logic
└── *_theme.h            → theme defaults
```

#### Step 2c: API exploration (all paradigms)
Check each paradigm file exists, then extract method signatures:

| Paradigm | Path pattern | Extract |
|----------|-------------|---------|
| Dynamic | `interface/sdk-js/api/@internal/component/ets/<comp>.d.ts` | `TextAttribute` class methods |
| Static | `interface/sdk-js/api/arkui/component/<comp>.static.d.ets` | `TextAttribute` interface methods |
| Modifier (Dynamic) | `interface/sdk-js/api/arkui/<Comp>Modifier.d.ts` | inherits from `TextAttribute` |
| Modifier (Static) | `interface/sdk-js/api/arkui/<Comp>Modifier.static.d.ets` | implements `TextAttribute` |
| CAPI | `interfaces/native/node/<comp>_native_impl.h` + `native_node.h` `NODE_<COMP>_*` | C API enums |

Dynamic API filenames use snake_case (e.g., `text_clock.d.ts`), Static use camelCase (e.g., `textClock.static.d.ets`).

#### Step 2d: Build cross-paradigm attribute table
Use Dynamic API `<Component>Attribute` as the primary axis. For each method:
1. Check if it exists in Static API
2. Modifier inherits/implements the same interface → same coverage
3. Search `NODE_<COMP>_*` enums in `native_node.h` for CAPI coverage

### For Frameworks (type=feature)

#### Step 2a: KB-first lookup + identify entry points
```bash
python3 docs/kb_search.py <system> --field name
```
- **Found** → read existing KB, identify gaps.
- **Not found** → reference an existing framework KB for structural guidance (e.g., `docs/architecture/ThemeManager_Architecture_CN.md`). Then locate source files:
```bash
find frameworks/core -name "*<system>*" -type f | head -20
```

#### Step 2b: Map architecture
- Abstract interface (`.h`) → pure virtual methods
- Implementation class (`_impl.h/cpp`) → data structures, caching, threading
- Related modules → interaction diagram

#### Step 2c: Trace core flows
Pick 2-3 most important operations and trace call chains from entry to result.

#### Step 2d: Identify extension points
How does external code extend or plug into this framework?

---

## Phase 3: Document Generation

### Read the template
```bash
# Always read the latest template before writing
cat docs/knowledge_base_TEMPLATE.md
```

### Component KB output structure
```
## 概述
## 目录结构
## 核心类继承关系          → Mermaid graph BT
## Pattern层详解
## Model层详解
## API 清单
  ### API 声明路径         → 6-paradigm table
  ### 属性接口清单         → cross-paradigm comparison table
  ### 构造参数
  ### 关联的 @ohos.arkui.* 模块 API
## 关键实现细节
## 使用示例               → ArkTS Dynamic + Static
## 调试指南
## 常见问题
```

### Framework KB output structure
```
## 概述
  ### 定位与职责
  ### 设计目标
  ### 与其他模块的交互关系  → Mermaid graph TD
## 架构设计
  ### 类继承关系            → Mermaid graph BT
  ### 核心接口
  ### 核心数据结构
## 核心流程                 → Mermaid graph TD per flow
## 关键特性
## 代码组织
## 性能与优化
## 调试指南
## 常见问题
## 扩展指南
```

### Mermaid conventions
- Class hierarchy: `graph BT` (bottom-to-top, children point to parents)
- Flows/architecture: `graph TD` (top-to-bottom)
- Node labels: `NodeId["Display Text<br/>subtitle"]`
- Inheritance edge: `Child --> Parent`
- Virtual inheritance: `Child -->|"virtual"| Parent`
- Composition: `Owner --- Part`

---

## Phase 4: Index & README Update

After writing the KB doc, update `docs/knowledge_base_INDEX.json` and `docs/knowledge_base_README.md`:

### Component entry
```json
{
  "name": "<ComponentName>",
  "name_cn": "<中文名>",
  "category": "<category>",
  "type": "component",
  "keywords": ["5-15 keywords"],
  "aliases": ["2-5 aliases"],
  "file_path": "pattern/<component>/<Component>_Knowledge_Base_CN.md",
  "source_paths": { "pattern": "...", "model": "..." },
  "api_paths": {
    "dynamic": "...",  "static": "...",
    "modifier": "...", "modifier_static": "...",
    "capi": "..."
  },
  "last_updated": "YYYY-MM-DD"
}
```

### Framework entry
```json
{
  "name": "<SystemName>",
  "name_cn": "<中文名>",
  "category": "system",
  "type": "feature",
  "keywords": ["5-15 keywords"],
  "aliases": ["2-5 aliases"],
  "file_path": "architecture/<System>_Architecture_CN.md",
  "source_paths": { "interface": "...", "impl": "..." },
  "api_paths": {},
  "last_updated": "YYYY-MM-DD"
}
```

### Validation
```bash
python3 -m json.tool docs/knowledge_base_INDEX.json > /dev/null && echo "Valid JSON"
python3 docs/kb_search.py <name> --field name
```

---

## Phase 5: Source Verification

After generating the KB doc and updating the index, verify all references against actual source.

### KB document checks
1. **Source file existence** — `ls` every source file path referenced in the KB doc
2. **Class hierarchy** — `grep "class <ClassName>" <file>` to verify Mermaid graph matches actual inheritance

### API table checks (component type)
3. **API file existence** — For each paradigm marked ✅ in the "API declaration path" table, `ls` the file
4. **Attribute spot-check** — Pick 3-5 attributes from the attribute table, `grep` each in the corresponding paradigm file to confirm presence

### INDEX entry checks
5. **source_paths** — `ls` every path in the INDEX entry's `source_paths`
6. **api_paths** — `ls` every path in the INDEX entry's `api_paths`
7. **Search consistency** — `python3 docs/kb_search.py <name>` output's `file_path` points to an existing file

### README checks
8. **KB count** — `find docs -name "*_Knowledge_Base*.md" -type f | wc -l` matches the count stated in README
9. **Category coverage** — new KB's category is listed in README's category summary if one exists

Fix any inconsistency immediately — do not mark as "to be confirmed".
