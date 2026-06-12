---
name: ohos-dev-graphics-3d-combined-postprocess
description: >
  Implement OpenHarmony Graphics3D Combined post-processing effects across
  LumeRender, Lume3D, and LumeScene. Use when adding or modifying single-pass
  fullscreen effects such as tone mapping, color grading, vignette, white
  balance, color adjustments, shader factors, ECS components, or scene-facing
  post-process APIs in the Combined post-process pipeline. Triggers on:
  "Combined post-process", "post-processing effect", "fullscreen shader effect",
  "LumeRender post-process", "Combined 后处理", "后处理效果".
metadata:
  author: openharmony
  display_name: OpenHarmony Graphics3D Combined Post-Process Implementation
  scope: domain
  stage: development
  domain: graphics-3d
  capability: combined-postprocess
  version: 0.1.0
  status: stable
---

# Combined Post-Process Implementation Guide

Implement Combined post-processing effects across three modules following the dependency chain:
**LumeRender** → **Lume3D** → **LumeScene**

## Task and Boundaries

This skill guides implementation of single-pass post-processing effects in OpenHarmony Graphics3D. 

**Applicable:**
- Effects running in single fullscreen shader pass (tone mapping, color grading, vignette)
- Adding effects to Combined post-process system

**Not Applicable:**
- Effects requiring separate render passes (bloom with blur passes, depth-of-field, motion blur)

## Module Dependency Overview

```
LumeRender (AGPRender)
    ↓
Lume3D (AGP3D) 
    ↓
LumeScene
```

- **LumeRender**: Low-level rendering module, provides shader/render node infrastructure
- **Lume3D**: 3D scene module, provides ECS components, depends on LumeRender
- **LumeScene**: High-level scene module, provides user-friendly interfaces, depends on Lume3D

---

## Pre-Implementation Checklist

**Before implementing any Combined post-process effect, ask yourself:**

1. **Visual Effect Goal**: What visual effect do you want to achieve? (tone mapping, color grading, vignette, custom effect)
2. **Parameter Complexity**: ≤4 params → `factors[]` only; 5-8 → split `factors[]` + `userFactors[]`; >8 → reconsider if Combined is appropriate
3. **Render Pass Requirement**: Does the effect need intermediate framebuffers?
   - Single fullscreen pass: ✓ Use Combined post-process (this skill)
   - Blur passes, downscale/upscale, temporal: ✗ Use multi-pass system (not this skill)
4. **Index Availability**: Are indices 0-7 available in Combined system?
   - Currently used: 0 (tone), 1 (vignette), 2 (dither), 3 (color conversion), 4 (fringe), 5 (upscale), 6 (white balance), 7 (color adjustments)
   - Need unused index: Must register new index in both shader and C++

**Decision Tree:**

```
Effect needs >4 params? ─────YES──→ Split: factors[] + userFactors[]
                         │
                         NO
                         ↓
Effect needs blur/temporal? ─YES──→ Use multi-pass system (EXIT this skill)
                         │
                         NO
                         ↓
Index 0-7 available? ──────YES──→ Continue with Combined implementation ✓
                         │
                         NO
                         ↓
REJECT: Combined slots 0-7 are full. EXIT this skill.
  - Do NOT register index 8+ in Combined — indices 8+ belong to multi-pass post-process system.
  - Options: (a) free an existing 0-7 slot by removing/relocating its effect, or
             (b) implement the effect via the multi-pass post-process path (not this skill).
```

## Fallback: When Combined Doesn't Apply

When the decision tree exits (multi-pass effect or indices full), use the **multi-pass post-process system** instead:

- **Architecture**: Separate render node graph with intermediate framebuffers, not the Combined fullscreen pass
- **Index range**: Multi-pass effects use indices 8+ (outside Combined's 0-7 range)
- **Key files**: Look for `render_post_process_multipass_*` files and dedicated render node configurations
- **When to free a Combined slot**: If an existing 0-7 effect is deprecated or can be merged, free its index and re-run this skill's decision tree

> For multi-pass implementation details, consult the OpenHarmony Graphics3D multi-pass post-process documentation or the `ohos-dev-graphics-3d-multipass-postprocess` skill (if available).

## NEVER Do (Critical Anti-Patterns)

- **NEVER apply to multi-pass effects** (bloom with blur, depth-of-field, motion blur, FXAA, TAA) — Combined shader only handles indices 0-7; multi-pass effects use indices 8+ with separate framebuffers → effect silently ignored or GPU data corruption
- **NEVER mismatch shader-C++ indices** — `POST_PROCESS_INDEX_*` in GLSL must exactly match `PostProcessConfiguration::INDEX_*` in C++ across 3 files (`render_post_process_structs_common.h`, `render_data_store_render_pods.h`, `render_data_store_post_process.cpp`) → visual artifacts, wrong colors, or GPU validation error "array index out of bounds"
- **NEVER forget userFactors for >4 parameters** — Vec4 only holds 4 floats; effects with 5-8 params must define `USER_INDEX_*` constant + `GetFactorXXX()` conversion for `userFactors[]` → shader compilation error "undefined macro" or zero parameters applied
- **NEVER skip any module** — LumeRender→Lume3D→LumeScene chain must be complete (all 22 steps): skip LumeRender → shader compilation error; skip Lume3D → ECS won't propagate config → shader receives zero factors; skip LumeScene → user API missing → unusable

> Full WHY/CONSEQUENCE/VALIDATION details in [`references/advanced_reference.md`](references/advanced_reference.md#prohibited-practices) — load when troubleshooting specific issues.

---

## Workflow

**LumeRender (8 steps):**
1. Define configuration structure
2. Register metadata
3. Define shader constants
4. Implement config-to-shader conversion
5. Fill post-process stack
6. Add conversion in RenderNodeUtil
7. Implement shader processing function
8. Integrate into render pipeline

**Lume3D (5 steps):**
1. Add flag bit
2. Define component property
3. Register metadata
4. Integrate into render system
5. Integrate into Lume3D shader

**LumeScene (9 steps):**
1. Define interface
2. Add to IPostProcess interface
3. Implement API wrapper
4. Implement effect class
5. Register in PostProcess
6. Register component type
7. Register plugin type
8. Register Any type
9. Update build files

---

## LumeRender Implementation

**MANDATORY - READ ENTIRE FILE**: Before starting LumeRender steps, you MUST read [`references/code_templates.md`](references/code_templates.md#lumarender-templates) "LumeRender Templates" section (Steps 1-8, ~300 lines) completely. **Do NOT set any range limits when reading this file.**

**Do NOT load** `advanced_reference.md` yet — save for troubleshooting phase.

### Step 1: Define Configuration Structure

**File**: `api/render/datastore/render/render_data_store_render_pods.h`

Define effect configuration struct with properties and default values. Add enum indices, flag bits, and property type declaration.

**Details**: See [references/code_templates.md#step-1-define-configuration-structure](references/code_templates.md#step-1-define-configuration-structure)

---

### Step 2: Register Metadata

**File**: `src/postprocesses/render_post_process_combined_node.cpp`

Register enum values, type metadata, and configuration structure metadata for reflection system.

**Details**: See [references/code_templates.md#step-2-register-metadata](references/code_templates.md#step-2-register-metadata)

---

### Step 3: Define Shader Constants

**File**: `api/render/shaders/common/render_post_process_structs_common.h`

Define shader macro constants for effect specialization bits and indices.

**Details**: See [references/code_templates.md#step-3-define-shader-constants](references/code_templates.md#step-3-define-shader-constants)

---

### Step 4: Implement Config-to-Shader Conversion

**File**: `src/datastore/render_data_store_post_process.h`

Implement conversion functions to pack configuration into shader-friendly Vec4 factors.

**Details**: See [references/code_templates.md#step-4-implement-config-to-shader-conversion](references/code_templates.md#step-4-implement-config-to-shader-conversion)

---

### Step 5: Fill Post-Process Stack

**File**: `src/datastore/render_data_store_post_process.cpp`

Add effect to post-process stack with built-in data and factors.

**Details**: See [references/code_templates.md#step-5-fill-post-process-stack](references/code_templates.md#step-5-fill-post-process-stack)

---

### Step 6: Add Conversion in RenderNodeUtil

**File**: `src/nodecontext/render_node_util.cpp`

Add factor conversion call in `GetRenderPostProcessConfiguration()` function.

**Details**: See [references/code_templates.md#step-6-add-conversion-in-rendernodeutil](references/code_templates.md#step-6-add-conversion-in-rendernodeutil)

---

### Step 7: Implement Shader Processing Function

**File**: `api/render/shaders/common/render_post_process_blocks.h`

Implement GLSL shader processing function with effect logic.

**Details**: See [references/code_templates.md#step-7-implement-shader-processing-function](references/code_templates.md#step-7-implement-shader-processing-function)

---

### Step 8: Integrate into Render Pipeline

**Files**:
- `assets/render/shaders/shader/fullscreen_combined_post_process.frag`
- `assets/render/shaders/shader/fullscreen_combined_post_process_layer.frag` (if layer rendering is used)

Call shader processing function in fullscreen render pipeline. If your project uses layer rendering, you MUST also integrate into the layer fragment shader — see the layer template in code_templates.md Step 8.

**Details**: See [references/code_templates.md#step-8-integrate-into-render-pipeline](references/code_templates.md#step-8-integrate-into-render-pipeline)

---

## Lume3D Implementation

**MANDATORY - READ SECTION**: Now read [`references/code_templates.md`](references/code_templates.md#lume3d-templates) "Lume3D Templates" section (Steps 1-5, ~100 lines) for ECS integration examples.

**Do NOT load** `advanced_reference.md` yet — continue following workflow steps.

### Step 1: Add Flag Bit

**File**: `api/3d/ecs/components/post_process_component.h`

Add flag bit to PostProcessComponent::FlagBits enum.

**Details**: See [references/code_templates.md#lume3d-step-1-add-flag-bit](references/code_templates.md#lume3d-step-1-add-flag-bit)

---

### Step 2: Define Component Property

**File**: `api/3d/ecs/components/post_process_component.h`

Define component property with DEFINE_PROPERTY macro.

**Details**: See [references/code_templates.md#lume3d-step-2-define-component-property](references/code_templates.md#lume3d-step-2-define-component-property)

---

### Step 3: Register Metadata

**File**: `src/ecs/components/post_process_component_manager.cpp`

Register enum values and configuration metadata.

**Details**: See [references/code_templates.md#lume3d-step-3-register-metadata](references/code_templates.md#lume3d-step-3-register-metadata)

---

### Step 4: Integrate into Render System

**File**: `src/ecs/systems/render_system.cpp`

Assign configuration in `ProcessPostProcessComponents()` function.

**Details**: See [references/code_templates.md#lume3d-step-4-integrate-into-render-system](references/code_templates.md#lume3d-step-4-integrate-into-render-system)

---

### Step 5: Integrate into Lume3D Shader

**File**: `api/3d/shaders/common/3d_dm_inplace_post_process.h`

Call shader processing function in Lume3D inplace post-process.

**Details**: See [references/code_templates.md#lume3d-step-5-integrate-into-lume3d-shader](references/code_templates.md#lume3d-step-5-integrate-into-lume3d-shader)

---

## LumeScene Implementation

**MANDATORY - READ SECTION**: Read [`references/code_templates.md`](references/code_templates.md#lumescene-templates) "LumeScene Templates" section (Steps 1-9, ~400 lines) for API wrapper and registration examples.

**Do NOT load** `advanced_reference.md` yet — only load when encountering errors or need data flow diagrams.

### Step 1: Define Interface

**File**: `include/scene/interface/postprocess/intf_your_effect.h`

Define interface class with META_INTERFACE and property declarations.

**Details**: See [references/code_templates.md#lumescene-step-1-define-interface](references/code_templates.md#lumescene-step-1-define-interface)

---

### Step 2: Add to IPostProcess Interface

**File**: `include/scene/interface/intf_postprocess.h`

Add include and META_READONLY_PROPERTY for effect interface.

**Details**: See [references/code_templates.md#lumescene-step-2-add-to-ipostprocess-interface](references/code_templates.md#lumescene-step-2-add-to-ipostprocess-interface)

---

### Step 3: Implement API Wrapper

**File**: `include/scene/api/post_process.h`

Implement wrapper class with META_INTERFACE_OBJECT and property macros.

**Details**: See [references/code_templates.md#lumescene-step-3-implement-api-wrapper](references/code_templates.md#lumescene-step-3-implement-api-wrapper)

---

### Step 4: Implement Effect Class

**Files**: 
- Header: `src/postprocess/your_effect.h`
- Implementation: `src/postprocess/your_effect.cpp`

Implement effect class inheriting from PostProcessEffect template with META_OBJECT macros.

**Details**: See [references/code_templates.md#lumescene-step-4-implement-effect-class](references/code_templates.md#lumescene-step-4-implement-effect-class)

---

### Step 5: Register in PostProcess

**Files**: 
- Header: `src/postprocess/postprocess.h`
- Implementation: `src/postprocess/postprocess.cpp`

Add static property data and InitDynamicProperty handler.

**Details**: See [references/code_templates.md#lumescene-step-5-register-in-postprocess](references/code_templates.md#lumescene-step-5-register-in-postprocess)

---

### Step 6: Register Component Type

**File**: `src/component/postprocess_component.h`

Add META_TYPE registration and property macros.

**Details**: See [references/code_templates.md#lumescene-step-6-register-component-type](references/code_templates.md#lumescene-step-6-register-component-type)

---

### Step 7: Register Plugin Type

**File**: `src/plugin.cpp`

Add RegisterObjectType and UnregisterObjectType calls.

**Details**: See [references/code_templates.md#lumescene-step-7-register-plugin-type](references/code_templates.md#lumescene-step-7-register-plugin-type)

---

### Step 8: Register Any Type

**File**: `src/register_anys.cpp`

Add interface pointer type to ObjectTypes list.

**Details**: See [references/code_templates.md#lumescene-step-8-register-any-type](references/code_templates.md#lumescene-step-8-register-any-type)

---

### Step 9: Update Build Files

**Files**: 
- `include/CMakeLists.txt`
- `src/CMakeLists.txt`
- `BUILD.gn`

Add interface and source files to build targets.

**Details**: See [references/code_templates.md#lumescene-step-9-update-build-files](references/code_templates.md#lumescene-step-9-update-build-files)

---

## References

### Primary Reference Files

- **[`references/code_templates.md`](references/code_templates.md)**: Complete code templates with Generic Template and Tone Mapping Example for all 22 steps. **MANDATORY loading during implementation**.
- **[`references/advanced_reference.md`](references/advanced_reference.md)**: Advanced reference with data flow diagrams, prohibited practices, exceptions/fallbacks, implementation checklists, and troubleshooting guide. **Load ONLY when troubleshooting or need data flow understanding**.

### Loading Strategy

**Phase 1 - Initial Implementation**:
- ✅ **MANDATORY**: Load `code_templates.md` in three stages (LumeRender → Lume3D → LumeScene sections)
- ❌ **Do NOT load**: `advanced_reference.md` (save for later)

**Phase 2 - Troubleshooting**:
- ✅ **Load when needed**: `advanced_reference.md` if encountering errors, need data flow diagrams, prohibited practices, or implementation checklists
- ❌ **Do NOT reload**: `code_templates.md` if already loaded
