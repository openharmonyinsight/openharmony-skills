# AGENTS.md

This file defines working rules for agents in `ace_engine`.

## 1. Scope and Priority

- This file applies to `OpenHarmony/foundation/arkui/ace_engine`.
- Direct user instructions take priority over this file.
- Principle: **code first, evidence first, no fabrication**.

## 2. Quick Build and Test

### Build

```bash
# Build ace_engine (from OpenHarmony root)
./build.sh --product-name rk3568 --build-target ace_engine

# Build SDK variant
./build.sh --product-name ohos-sdk --build-target ace_engine

# Build a GN target
./build.sh --product-name rk3568 --build-target //foundation/arkui/ace_engine/frameworks/core/components_ng/pattern/text:text_pattern
```

### Unit Test / Benchmark Build

```bash
./build.sh --product-name rk3568 --build-target unittest
./build.sh --product-name rk3568 --build-target benchmark_linux
```

### Run Tests

```bash
# Example unit test
./out/rk3568/tests/ace_engine/unittest/components_ng/text/text_pattern_test

# Run a single gtest case
./out/rk3568/tests/ace_engine/unittest/components_ng/text/text_pattern_test --gtest_filter=TextPatternTest.OnModifyDone

# Example benchmark
./out/rk3568/tests/ace_engine/benchmark/text/text_benchmark --benchmark_filter=TextRender
```

### C API Unit Tests

```bash
# Build C API tests
./build.sh --product-name rk3568 --build-target linux_unittest_capi --ccache
```

- Test locations:
  - ARM: `out/rk3568/tests/unittest/ace_engine/C-API-Main/components/`
  - X86: `out/rk3568/<x64 target>/tests/unittest/ace_engine/C-API-Main/components/`
- Typical executables: `capi_all_modifiers_test`, `capi_all_accessors_test`, `capi_all_utils_test`, `capi_generated_modifiers_test`.

### Build Outputs Summary

Main output dir: `out/rk3568/arkui/ace_engine/`

- Core engine libraries (`libace*.z.so`):
  - `libace_compatible.z.so`: core library for current ArkUI framework and components, still containing compatibility code paths for legacy/web-style chains
  - `libace_compatible_components.z.so`: split-out compatible components for on-demand loading
  - other examples: `libace_engine_pa_ark.z.so`, `libace_ndk.z.so`, `libace_form_render.z.so`, `libace_xcomponent_controller.z.so`
- Frontend bridge libraries:
  - `libarkts_frontend.z.so`, `libcj_frontend_ohos.z.so`
- Component libraries (`libarkui_*.z.so`):
  - per-component shared libs such as `libarkui_slider.z.so`, `libarkui_checkbox.z.so`
- ArkTS native bridge libraries (`*_ani.so`):
  - ArkTS<->Native bridge libs such as `libanimator_ani.so`, `libarkuicustomnode_ani.so`
- Functional module libraries (`lib*.z.so`):
  - module-oriented libs such as `libanimator.z.so`, `libdialog.z.so`, `libdragcontroller.z.so`
- ArkTS bytecode files (`.abc`):
  - component/runtime bytecode such as `ark*.abc`, `modifier.abc`, `node.abc`, `statemanagement.abc`, `uicontext.abc`

### Frontend Support (Quick)

| Frontend | Language | Use Case |
|----------|----------|----------|
| **Declarative Frontend** | ArkTS dynamic version | Recommended - modern declarative UI |
| **ArkTS Frontend** | ArkTS static version | Incremental engine-based frontend |
| **JavaScript Frontend** | JavaScript | Legacy web-style development |

- ArkTS dynamic version (Declarative Frontend):
  - Path: `frameworks/bridge/declarative_frontend/`
  - Main mode for most apps; uses ArkTS/TS declarative syntax with state management (`@Watch`, `@Link`, `@Prop`) and modifier-based property updates.
  - Corresponds to the dynamic version pipeline (Dynamic API): runtime bridge dispatch in `declarative_frontend`, mainly through `jsview/`, `ark_modifier/`, and `engine/jsi/nativeModule/`.
  - Dynamic API artifacts are typically `*.d.ts` (component APIs) and `*Modifier.d.ts` (modifier APIs), in parallel with static APIs.
- ArkTS static version (ArkTS Frontend):
  - "Static" means ArkTS syntax hardened with static-compilation-friendly constraints (strong typing, fully statically analyzable), executed on the new static ArkTS Runtime.
  - For the static version, ArkUI rebuilds the frontend and state management on top of the koala_projects incremental engine, replacing the dynamic version's `declarative_frontend` runtime-dispatch model.
  - Path: `frameworks/bridge/arkts_frontend/`
  - Static frontend pipeline is based on `koala_projects/` + `arkoala_generator/`, bridged by `libarkts_frontend.z.so`.
  - `frameworks/bridge/arkts_frontend/arkoala_generator/BUILD.gn` provides `idlize_gen`, which installs generated ArkUI static bridge files into `frameworks/bridge/arkts_frontend/koala_projects/arkoala-arkts/arkui-ohos/generated/`.
  - `frameworks/bridge/arkts_frontend/koala_projects/arkoala-arkts/BUILD.gn` depends on `../../arkoala_generator:idlize_gen` and uses `generate_static_abc("components_compile_abc")` to produce static `.abc` artifacts (e.g. `components.abc`).

## 3. Knowledge Base

Use the KB as the first-stop context before any deep code analysis, and follow the authoring rules below when adding or updating entries. Always treat the KB as context — **then verify against real source code**.

### 3.1 Lookup First

**MANDATORY: Before any code search or analysis on components, architecture, APIs, or patterns, you MUST run a KB query first. Do NOT skip this step and jump straight to source code.**

- Prefer `docs/kb_search.py` for KB lookup:
  - `python3 docs/kb_search.py <keyword>`
- Use KB query results to precisely locate files for follow-up code inspection.
- Use `rg` in `docs/` as a fallback when script results are insufficient.
- Entry points: `docs/knowledge_base_README.md`, `docs/knowledge_base_INDEX.json`, and KB directories under `docs/` (for example: `pattern/`, `common/`, `layout/`, `api/`, `sdk/`, `architecture/`).

#### 3.1.1 Task Routing Rules (KB-first)

- Keep this section rule-based, not an exhaustive scenario catalog.
- Run `python3 docs/kb_search.py <keyword>` with 1-2 core keywords and read the top matching 1-3 KB docs first.
- If KB hits are weak or ambiguous, refine query (`--field`, second keyword) and fallback to `rg -n "<keyword>" docs`.
- After KB routing, verify only in real source code and tests (typically `frameworks/`, `interfaces/`, `test/`) before concluding.

### 3.2 Authoring Standard (Minimal)

- Naming/location: use `XXX_Knowledge_Base.md` or `XXX_Knowledge_Base_CN.md`; place under `docs/pattern/<component>/`, `docs/sdk/`, `docs/architecture/`, `docs/common/`, `docs/layout/`, `docs/api/`, `docs/accessibility/` (choose by topic).
- Index metadata (`docs/knowledge_base_INDEX.json`) must include: `name`, `name_cn`, `category`, `type`, `file_path`, `last_updated`, `keywords` (5-15), `aliases` (2-5); recommend `source_paths` and `api_paths`.
- Allowed categories: `basic`, `container`, `selector`, `shape`, `media`, `data_display`, `rich_text`, `advanced`, `sdk`, `system`.
- Required sections in each KB doc: 概述, 目录结构, 核心类继承关系, Pattern层详解, Model层详解, 完整API清单, 关键实现细节, 使用示例, 调试指南, 常见问题.

Quick checks:

```bash
find docs -name "*_Knowledge_Base*.md" -type f | wc -l
python3 -m json.tool docs/knowledge_base_INDEX.json > /dev/null && echo "Valid JSON"
python3 docs/kb_search.py --list-categories
```

Detailed templates/rules: `docs/knowledge_base_README.md`.

## 4. Core Working Principles (Must Follow)

### 4.1 Actual Code Only

- Always read real code via search/read tools before concluding behavior.
- Always cite file path and line when giving code-level conclusions.
- If code is missing, explicitly state: **"此代码在 ace_engine 中未找到"**.
- Do not write hypothetical implementation as fact.

### 4.2 Speculation Management

- Any unverified statement must be labeled **"推测"**.
- Try to verify first; only keep speculation when verification is impossible.

### 4.3 Code-First Verification

- User suggestions may be wrong; verify with source before accepting.
- Resolve disagreements with evidence from implementation.

### 4.4 Error Learning

- If a user correction reveals a doc error, update relevant knowledge base docs.
- Record root cause and prevention in the knowledge base when appropriate.

## 5. Project Map

- `adapter/`: platform adaptation (`ohos/`, `preview/`)
- `advanced_ui_component/`, `advanced_ui_component_static/`: advanced/composite components for the dynamic and static paradigms (counterparts of `@ohos.arkui.advanced.*`).
- `frameworks/base/`: base utilities
- `frameworks/bridge/`: frontend bridge (`declarative_frontend`, `arkts_frontend`, `js_frontend`, `cj_frontend`)
- `frameworks/core/components_ng/`: new-generation component framework (preferred for new development), centered on `FrameNode` + `Pattern` + property/modifier pipelines.
- `frameworks/core/components/`: legacy component framework (DOM/Component/Element/Render style), mainly for historical compatibility and older implementation paths.
- `frameworks/core/pipeline_ng/` (+ legacy `pipeline/`): rendering pipeline, frame scheduling, and task dispatch for `components_ng`.
- `interfaces/native/node/`: C API for components — entry point of the Modifier bridge consumed by NDK scenario (covered by `linux_unittest_capi`).
- `interfaces/napi/kits/`: NAPI implementations for `@ohos.*` modules such as `router`, `promptAction`, `mediaquery`, `animator`, `font`, `measure`, `curves`, `matrix4` (31 subdirectories).
- `test/unittest`, `test/benchmark`: tests

## 6. Component Development Guidance

- Prefer `components_ng` over legacy `components`.
- Typical component files:
  - `*_pattern.*`, `*_model.*`, `*_layout_property.*`, `*_paint_property.*`, `*_event_hub.*`
- Register new components in `frameworks/core/components_ng/components.gni` when needed.
- Keep platform-specific logic in `adapter/`, not in core business logic.

## 7. Testing Guidance

- Test path should mirror source layout.
- Run targeted unit tests for changed modules first, then broader regression tests if impact is large.
- For C API related changes:
  - Build `linux_unittest_capi`
  - Run relevant `capi_*` test executables
  - Ensure host binaries are correct architecture (`file <test_binary>`)

## 8. Hard Boundaries (Do not / Ask before)

Do not (without explicit user confirmation):

- Change public API signatures/semantics/error codes/struct layout under `interfaces/native/` or `interfaces/napi/` (including ABI-risk changes).
- Manually edit generated files under `**/generated/`.
- Add dependencies on other OpenHarmony system modules outside `adapter/` (including `BUILD.gn` `deps/public_deps/data_deps` dependency entries).
- Run destructive or hard-to-recover commands (for example `rm -rf`, `git reset --hard`).

Ask before:

- Any API/ABI compatibility-impacting change or default behavior change.
- Any new/updated/replaced dependency: `bundle.json` dependency changes; new `deps/public_deps/data_deps` in any `BUILD.gn`.
- Regenerating static ArkTS generated files (must edit `frameworks/bridge/arkts_frontend/arkoala_generator/` first).
