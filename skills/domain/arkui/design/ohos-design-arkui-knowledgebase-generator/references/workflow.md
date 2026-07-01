# KB Generator Workflow Reference

Use this reference for ArkUI ace_engine new KB creation, update, and old-KB migration.

## Phase 1: Scope Gate

Confirm these before deep exploration:

1. Target component/subsystem, such as `Text`, `Slider`, `ThemeManager`, or `Pipeline`.
2. Type: public component, component family, common capability, API/SDK topic, or framework/internal mechanism.
3. Work mode: create new `docs/kb/` page, update existing new KB, migrate old KB, or repair registry/index routing.

If any item is missing, ask one concise question and wait. A quick metadata scan is allowed to identify candidate targets.

## Phase 2: KB-First Routing

Run before source exploration:

```bash
python3 docs/kb_search.py <target> --field name
```

Interpret results:

- `知识库: docs/kb/...` from registry: topic is already migrated/new. Update the new KB and registry if needed.
- `知识库: docs/pattern/...`, `docs/common/...`, `docs/layout/...`, etc. from old INDEX: topic is not migrated. For migration requests, use the old KB as context, then create a new lightweight KB.
- Both registry and old INDEX have the same target: registry wins, and the old INDEX entry is stale; remove the old INDEX entry during routing repair.
- No hit: create a new `docs/kb/` page after confirming target/type/scope.

## Phase 3: Source and API Verification

Old KB content is never authoritative. During migration, use it only to find candidate paths, classes, APIs, and behavior topics. Every retained route or factual statement must be checked against current source code, SDK/API declarations, tests, or Specs before it appears in the new KB. If verification fails or the source is missing, remove or narrow the claim instead of preserving stale content.

### Components

Inspect stable entry points:

```text
frameworks/core/components_ng/pattern/<component>/
├── *_pattern.h/cpp
├── *_model_ng.h/cpp
├── *_layout_property.h
├── *_event_hub.h
├── *_layout_algorithm.*
└── *_theme.h
```

API declarations are facts for public APIs:

| Paradigm | Path pattern |
|----------|--------------|
| Dynamic | `<OH_ROOT>/interface/sdk-js/api/@internal/component/ets/<comp>.d.ts` |
| Static | `<OH_ROOT>/interface/sdk-js/api/arkui/component/<comp>.static.d.ets` |
| Modifier Dynamic | `<OH_ROOT>/interface/sdk-js/api/arkui/<Comp>Modifier.d.ts` |
| Modifier Static | `<OH_ROOT>/interface/sdk-js/api/arkui/<Comp>Modifier.static.d.ets` |
| C API | `interfaces/native/native_node.h`, `interfaces/native/node/<comp>_native_impl.*` |

Dynamic filenames usually use snake_case; Static filenames usually use camelCase. If SDK-JS is not cloned, warn and skip API declaration coverage.

### Frameworks / Capabilities

Locate interfaces, implementations, adapters, tests, and build files with `rg`/`find`. Prefer stable directories and type names over line-numbered details.

### Specs

Specs live in a separate repo at `./specs` in this workspace. If missing:

- warn: `specs repository is not available; clone the specs repo separately at ./specs`
- skip Spec index and Feat checks
- keep KB route text conditional, such as "if available" or omit Spec tables when unverified

## Phase 4: New KB Authoring

New KBs are lightweight routing pages. They should answer: "Where do I inspect this topic next?"

Do include:

- positioning and scope
- stable source/API/test/spec routes
- external dependency entry points when relevant
- search hints for properties, events, C API enums, or adapters
- related topics

Do not include:

- line numbers or `file:line` references
- long code snippets
- large call-chain prose copied from old KBs
- stale behavior/default-value claims
- complete API behavior matrices
- old/new difference narration unless the user explicitly asks for migration history

### Suggested Component Page

```markdown
# <Name> Context

> 文档版本：v1.0
> 更新时间：YYYY-MM-DD
> 来源：`docs/context_registry.json` 主题 `<id>`

## 定位

<One or two stable paragraphs. State that behavior facts come from SDK/source/tests/Spec.>

## 快速路由

### 源码入口
| 关注点 | 稳定路径 | 说明 |

### API 入口
| 范式 | 稳定路径 | 说明 |

### API 解析实现路径
| 路径 | 入口文件 | 说明 |

### 外部依赖入口
| 依赖方向 | 本仓入口 | 外部仓路径 | 相对外部仓的头文件 / 目标路径 | 说明 |

### 测试入口
| 类型 | 稳定路径 | 用途 |

### 相关 Spec

## 常见问题定位
| 问题 | 优先查看 |

## 调试入口

## 相关主题
```

Use `### 外部依赖入口` only when the component depends on external systems such as graphic rendering, typography, image framework, pasteboard, UDMF, vibrator, AI, or platform adapters.

### 外部依赖入口（通过源码调用分析补充）

组件或能力的外部依赖不能凭记忆或旧 KB 推断，必须通过源码调用链分析确认。

**分析步骤**：

1. 从 pattern 目录的核心文件（`*_pattern.cpp`、`*_model_ng.cpp`、`*_layout_algorithm.cpp`）出发，搜索跨仓 `#include` 和外部接口调用。

2. 对每个外部调用，追溯到本仓适配层入口和外部仓目标路径。

3. 填写外部依赖表格：

| 依赖方向 | 本仓入口 | 外部仓路径 | 相对外部仓的头文件 / 目标路径 | 说明 |
|----------|----------|-----------|-------------------------------|------|
| 图形渲染 | `*_paint_method.cpp` / `*_modifier.cpp` | `graphic_2d` | `rosen/modules/render_service_base/include/` | RSNode / RSCanvas 绑定 |
| 排版引擎 | `*_layout_algorithm.cpp` | `graphic_2d` | `rosen/modules/2d_engine/rosen_text/` | Typography 段落排版 |
| 图片框架 | `image_loading_context.cpp` | `multimedia_image_framework` | `interfaces/innerkits/include/` | ImageSource 解码 |
| 平台适配 | `adapter/ohos/` | 各平台仓 | — | 平台桥接层 |

以上为常见外部依赖示例，实际表格只保留通过源码分析确认存在的行，不要凭模板预填。

### API 解析实现路径（组件 KB 必填）

对组件类型 KB，`### API 解析实现路径` 是必填章节。需要区分组件是否已完成组件化改造，并列出属性解析的实际实现路径。

**判定组件化状态**：

```bash
# 检查组件是否在动态模块列表中
grep -q '"<ComponentName>"' adapter/ohos/osal/dynamic_module_helper.cpp && echo "已组件化" || echo "未组件化"

# 检查组件是否有 bridge/ 子目录（组件化标志）
ls frameworks/core/components_ng/pattern/<component>/bridge/ 2>/dev/null && echo "已组件化" || echo "未组件化"

# 检查旧 JSView 文件是否仍存在（未组件化标志）
ls frameworks/bridge/declarative_frontend/jsview/js_<component>.cpp 2>/dev/null && echo "JSView 仍存在"
```

**未组件化组件**的典型路径表：

| 路径 | 入口文件 | 说明 |
|------|----------|------|
| JSView（声明式组件） | `frameworks/bridge/declarative_frontend/jsview/js_<comp>.cpp` | `JS<Comp>::SetXxx()` → `<Comp>Model::GetInstance()->SetXxx()` |
| ArkTS Bridge（动态属性） | `frameworks/bridge/declarative_frontend/engine/jsi/nativeModule/arkts_native_<comp>_bridge.cpp` | Bridge → node_modifier → ModelNG |
| node_modifier 层 | `frameworks/core/interfaces/native/node/node_<comp>_modifier.cpp` | C++ Set/Reset/Get，bridge 和 C API 共用 |
| C API（NDK） | `interfaces/native/node/<comp>_native_impl.cpp` 或通用 `style_modifier.cpp` | 有专属 native_impl 就填，否则注明走通用框架 |
| 前端 Modifier（ArkTS 侧） | `frameworks/bridge/declarative_frontend/ark_modifier/src/<comp>_modifier.ts` | ArkTS Modifier 类 |

尾部加一句："组件化改造参考：`./组件化重构通用方案.md`。改造后 JSView 和 Bridge 双路径将统一到 `pattern/<comp>/bridge/`，并输出独立 so。"

**已组件化组件**的典型路径表：

| 路径 | 入口文件 | 说明 |
|------|----------|------|
| 前端 JS/TS 定义 | `frameworks/bridge/declarative_frontend/ark_component/components/ark<comp>.js` 或 `ark_direct_component/src/ark<comp>.ts` | 前端组件类 |
| 统一 Bridge（声明式 + 动态属性） | `frameworks/core/components_ng/pattern/<comp>/bridge/arkts_native_<comp>_bridge.cpp` | 通过 `IsJsView()` 区分模式，统一参数解析 |
| Dynamic Modifier | `frameworks/core/components_ng/pattern/<comp>/bridge/<comp>_dynamic_modifier.cpp` | 动态属性路径 |
| Static Modifier | `frameworks/core/components_ng/pattern/<comp>/bridge/<comp>_static_modifier.cpp` | 静态编译路径 |
| Dynamic Module | `frameworks/core/components_ng/pattern/<comp>/bridge/<comp>_dynamic_module.cpp` | `DynamicModule` 派生类，`libarkui_<comp>.z.so` 入口 |
| node_modifier 委托层 | `frameworks/core/interfaces/native/node/<comp>_modifier.cpp` | 通过 `DynamicModuleHelper` 转发到动态模块 |

注明独立 so 名称，如 `libarkui_<comp>.z.so`。

## Phase 5: Registry and Old INDEX

### Add/update `docs/context_registry.json`

Use stable IDs and docs-relative KB path:

```json
{
  "id": "Text",
  "name": "Text",
  "name_cn": "文本组件",
  "kind": "component",
  "category": "basic",
  "keywords": ["Text", "文本", "font", "selection"],
  "aliases": ["Text组件", "文本", "文字组件"],
  "kb": "docs/kb/components/basic/text.md",
  "spec_domain": "specs/05-ui-components/09-text-components/04-text",
  "func_id": "05-09-04",
  "spec_status": "active",
  "source_paths": { "pattern": "frameworks/core/components_ng/pattern/text/text_pattern.cpp" },
  "api_paths": { "dynamic": "<OH_ROOT>/interface/sdk-js/api/@internal/component/ets/text.d.ts" },
  "test_paths": ["test/unittest/core/pattern/text/"],
  "status": "active",
  "last_verified": "YYYY-MM-DD"
}
```

Do not add `legacy_kb` for migrated topics.

Look up `func_id` and `spec_domain` from `specs/registry/functions.yaml`:

```bash
grep -A 10 'title: <ComponentName>' specs/registry/functions.yaml
# Extract id (e.g. 05-09-04) and path (e.g. 05-ui-components/09-text-components/04-text/)
# spec_domain = "specs/" + path (without trailing slash)
```

Set `spec_status` based on whether the `spec_domain` directory exists:

- `active` — spec directory exists. Validator errors if path is missing.
- `pending` — registered in `functions.yaml` but directory not yet created. Validator warns instead of erroring.

### Maintain `docs/knowledge_base_INDEX.json`

This file indexes old KBs that have not migrated.

For new `docs/kb/` topics:

- do not add them to the old INDEX
- add them to `context_registry.json`

For migrations:

- remove only the migrated topic entry from old INDEX
- remove the migrated topic name from category `components`
- keep all unrelated old KB entries intact
- ensure every remaining `file_path` exists under `docs/`

## Phase 6: Migration Procedure

1. Run `python3 docs/kb_search.py <target> --field name`.
2. Read the old KB if present. Treat it as hints, not as truth.
3. Build a verification checklist from old-KB claims that will be retained: source paths, class/type names, API declarations, test paths, Spec links, and external dependencies.
4. Verify each checklist item against current source/API/test/Spec files before writing. Do not carry forward old line numbers, code snippets, behavior claims, or default values unless re-verified.
5. Analyze source code call chains to identify external dependencies (see Phase 4 "外部依赖入口" section for grep/rg commands). Only include dependencies confirmed by actual `#include` or API calls in current source — do not copy dependency lists from old KBs.
6. Create new KB under `docs/kb/` using only verified stable routes and scoped statements, including the external dependency table populated from step 5.
7. Update `docs/context_registry.json`.
8. Remove the migrated topic from `docs/knowledge_base_INDEX.json` only.
9. Update links that referenced the old KB path.
10. Delete the old KB file.
11. Update `docs/kb/README.md` and `docs/knowledge_base_README.md` if counts/rules changed.
12. Validate.

Never delete unrelated old KB files or remove unrelated old INDEX entries.

## Phase 7: Validation Checklist

Always run:

```bash
python3 -m json.tool docs/context_registry.json > /dev/null
python3 -m json.tool docs/knowledge_base_INDEX.json > /dev/null
python3 docs/validate_context.py --quiet
python3 docs/kb_search.py <target> --field name
```

For migration, additionally run:

```bash
rg -n "<Old_KB_File_Name>|<old/kb/path>" docs
```

Check manually:

- New KB file exists and contains only source/API/test/Spec-verified routes or explicitly scoped statements.
- Old KB file is deleted only for migrated target.
- Old INDEX does not contain the migrated target.
- Old INDEX still contains unrelated old KBs.
- `kb_search.py` finds the migrated target via `context_registry.json`.
- `validate_context.py` has zero errors. Existing warnings may remain if they are unrelated placeholders or missing Specs.
