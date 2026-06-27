# Advanced Reference: Combined Post-Process Implementation

This document provides advanced reference materials for Combined post-process implementation:
- **Data Flow Diagrams**: Visual representation of data transformation across layers
- **Prohibited Practices**: Critical mistakes to avoid
- **Exceptions and Fallbacks**: When this skill doesn't apply
- **Implementation Checklist**: Step-by-step completion tracking
- **Troubleshooting**: Common mistakes and validation

For code templates and detailed implementation steps, see [`code_templates.md`](code_templates.md).

---

## Data Flow Summary

Understanding data flow is critical for implementing Combined post-process effects correctly.

### Generic Data Flow

```
User Configuration (YourEffectConfiguration)
  ↓ ProcessPostProcessComponents()
PostProcessConfiguration
  ↓ RecalculatePostProcesses()
RenderDataStorePostProcess
  ├─ GetFactorYourEffect() → factors[POST_PROCESS_INDEX_YOUR_EFFECT]
  └─ userFactors[USER_INDEX_YOUR_EFFECT_PROPERTY]
  ↓ Upload to GPU
Shader Uniform
  ├─ uGlobalData.factors[POST_PROCESS_INDEX_YOUR_EFFECT]
  └─ uGlobalData.userFactors[USER_INDEX_YOUR_EFFECT_PROPERTY]
  ↓ PostProcessYourEffectBlock()
Output Color
```

### Tone Mapping Data Flow Example

```
User Configuration (TonemapConfiguration)
  ├─ tonemapType: TONEMAP_ACES
  └─ exposure: 1.0f
  ↓ ProcessPostProcessComponents()
PostProcessConfiguration
  └─ tonemapConfiguration: { tonemapType, exposure }
  ↓ RecalculatePostProcesses()
RenderDataStorePostProcess
  ├─ GetFactorTonemap() → Vec4(1.0f, 0.0f, 0.0f, 0.0f)
  └─ factors[POST_PROCESS_INDEX_TONEMAP]
  ↓ Upload to GPU
Shader Uniform (uGlobalData)
  ├─ flags.x: contains TONEMAP_BIT
  └─ factors[0]: Vec4(exposure, 0, 0, tonemapType)
  ↓ PostProcessTonemapBlock()
Output Color
  └─ outColor = TonemapAces(inColor * exposure)
```

### Data Transformation Layers

1. **User Layer (LumeScene)**
   - Effect interface classes (e.g., `ITonemap`, `IVignette`)
   - User-friendly property setters (exposure, intensity, color)
   - Stored in scene graph components

2. **Configuration Layer (Lume3D)**
   - `PostProcessComponent` stores enabled effects and parameters
   - `PostProcessConfiguration` aggregates all effect configs
   - `ProcessPostProcessComponents()` converts scene data to configuration

3. **DataStore Layer (LumeRender)**
   - `RenderDataStorePostProcess` manages GPU upload data
   - `GetFactorYourEffect()` converts config to shader-friendly Vec4
   - `factors[]` and `userFactors[]` arrays for GPU uniform binding

4. **Shader Layer**
   - `uGlobalData.factors[]` uniform array (8 Vec4 slots, indices 0-7)
   - `uGlobalData.userFactors[]` uniform array (extended parameter storage)
   - `PostProcessYourEffectBlock()` function applies effect

### Index Allocation System

The Combined system uses **index-based parameter allocation**:

**Slot Assignment:**
```
POST_PROCESS_INDEX_TONEMAP         = 0  (factors[0])
POST_PROCESS_INDEX_VIGNETTE        = 1  (factors[1])
POST_PROCESS_INDEX_DITHER          = 2  (factors[2])
POST_PROCESS_INDEX_COLOR_CONVERSION = 3  (factors[3])
POST_PROCESS_INDEX_FRINGE          = 4  (factors[4])
POST_PROCESS_INDEX_UPSCALE         = 5  (factors[5])
POST_PROCESS_INDEX_WHITE_BALANCE   = 6  (factors[6])
POST_PROCESS_INDEX_COLOR_ADJUSTMENTS = 7  (factors[7])
```

**When adding new effect:**
- Check index availability (only 8 slots in `factors[]`)
- If slot available: Register index in both shader and C++
- If >4 parameters: Use `userFactors[]` array for additional storage

---

## Prohibited Practices

### NEVER Apply to Multi-Pass Effects

**Effects requiring separate render passes** (bloom with blur, depth-of-field, motion blur, FXAA, TAA):

- **WHY**: Combined post-process shader (`fullscreen_combined_post_process.frag`) only handles indices 0-7. Multi-pass effects use indices 8+ with separate shaders and intermediate framebuffers.
- **CONSEQUENCE**: Attempting Combined approach causes `factors[INDEX_BLOOM]` (index 9) to be ignored in Combined shader. Effect won't render, or may read garbage data from wrong memory offset.
- **VALIDATION**: Check if effect needs intermediate render passes (blur passes, downscale/upscale). If yes → use multi-pass system, not Combined.
- **CORRECT**: Use dedicated multi-pass post-process implementation with separate render node graph.

---

### NEVER Mismatch Shader-C++ Indices

**Index consistency between GLSL constants and C++ enums**:

- **WHY**: Shader accesses `uGlobalData.factors[POST_PROCESS_INDEX_TONEMAP]` directly. If shader defines `POST_PROCESS_INDEX_TONEMAP 0` but C++ defines `INDEX_TONEMAP 1`, shader reads wrong Vec4 from factors array.
- **CONSEQUENCE**: Visual artifacts (wrong colors, parameters not applied) or GPU validation error "array index out of bounds" if index exceeds `POST_PROCESS_GLOBAL_VEC4_FACTOR_COUNT (14)`.
- **VALIDATION**: Cross-check three files:
  1. Shader: `render_post_process_structs_common.h` → `POST_PROCESS_INDEX_*` values
  2. C++ config: `render_data_store_render_pods.h` → `PostProcessConfiguration::INDEX_*` values
  3. DataStore conversion: `render_data_store_post_process.cpp` → `factors[INDEX_*]` assignment
- **CORRECT**: Ensure all three locations use same numeric value. File comment explicitly states: "needs to match api/core/render/render_data_store_render_pods.h".

---

### NEVER Forget userFactors for >4 Parameters

**Effects needing more than 4 float parameters**:

- **WHY**: Vec4 only holds 4 floats. GlobalPostProcessStruct has `factors[14]` (Vec4 array) and `userFactors[16]` (Vec4 array). If effect has 5+ parameters, must split into factors + userFactors.
- **CONSEQUENCE**: Shader tries to read `uGlobalData.userFactors[USER_INDEX_*]` but constant undefined → compilation error "undefined macro". Or if defined but not filled → shader reads zero Vec4 → effect parameters wrong.
- **VALIDATION**: Count effect parameters. If >4, verify:
  1. `USER_INDEX_*` constant defined in `render_data_store_render_pods.h`
  2. `GetFactorXXX()` function for userFactors in `render_data_store_post_process.h`
  3. Shader uses correct userFactors index: `uGlobalData.userFactors[POST_PROCESS_USER_INDEX_*]`
- **CORRECT**: For 5-8 parameters: use factors[0-3] + userFactors[0-3]. Define `USER_INDEX_*` constant, implement conversion function, call in FillDefaultPostProcessData.

---

### NEVER Skip LumeRender/Lume3D/LumeScene Consistency

**All three modules must be updated**:

- **WHY**: Combined post-process flows through three modules: LumeRender defines shader constants → Lume3D integrates into ECS → LumeScene wraps API. Skipping one module breaks the chain.
- **CONSEQUENCE**: 
  - Skip LumeRender: Shader can't find `PostProcessXXXBlock()` function → compilation error
  - Skip Lume3D: `PostProcessComponent` missing property → ECS system won't propagate configuration → shader receives zero factors
  - Skip LumeScene: User API missing → developers can't configure effect → unusable
- **VALIDATION**: Use implementation checklist (22 steps across 3 modules). Check each module's key files exist and are modified.
- **CORRECT**: Follow all 22 steps. LumeRender (8) → Lume3D (5) → LumeScene (9) in sequence.

---

## Exceptions and Fallbacks

### Effect Requires Multiple Render Passes

**Symptom**: Effect needs blur passes, downscale/upscale, temporal accumulation.

- **Fallback**: This skill doesn't apply. Use dedicated multi-pass post-process system with separate render node graph.
- **Evidence**: Check if shader needs `uImgSampler` + `uBloomSampler` + intermediate framebuffers (like bloom). If yes → multi-pass.

### Shader Compilation Error

**Symptom**: "undefined macro POST_PROCESS_INDEX_XXX" or "array index out of bounds".

- **Diagnosis**: Index mismatch or missing constant definition.
- **Fix**: Check shader constant matches C++ enum value. Verify index < 14 (POST_PROCESS_GLOBAL_VEC4_FACTOR_COUNT).

### Visual Artifacts or Effect Not Applied

**Symptom**: Wrong colors, parameters ignored, effect invisible.

- **Diagnosis**: Wrong factors index, or GetFactorXXX() not called in DataStore.
- **Fix**: Verify conversion function called in both `render_data_store_post_process.cpp` (Step 5) and `render_node_util.cpp` (Step 6).

---

## Implementation Checklist

Use this checklist to track completion across all three modules.

### LumeRender (8 steps)

**Checklist:**
- [ ] **Step 1**: Define configuration structure in `api/render/datastore/render/render_data_store_render_pods.h`
- [ ] **Step 2**: Register metadata in `src/postprocesses/render_post_process_combined_node.cpp`
- [ ] **Step 3**: Define shader constants in `api/render/shaders/common/render_post_process_structs_common.h`
- [ ] **Step 4**: Implement config-to-shader conversion in `src/datastore/render_data_store_post_process.h`
- [ ] **Step 5**: Fill post-process stack in `src/datastore/render_data_store_post_process.cpp`
- [ ] **Step 6**: Add conversion in `src/nodecontext/render_node_util.cpp`
- [ ] **Step 7**: Implement shader processing function in `api/render/shaders/common/render_post_process_blocks.h`
- [ ] **Step 8**: Integrate into render pipeline in `assets/render/shaders/shader/fullscreen_combined_post_process.frag`

### Lume3D (5 steps)

**Checklist:**
- [ ] **Step 1**: Add flag bit in `api/3d/ecs/components/post_process_component.h`
- [ ] **Step 2**: Define component property in `api/3d/ecs/components/post_process_component.h`
- [ ] **Step 3**: Register metadata in `src/ecs/components/post_process_component_manager.cpp`
- [ ] **Step 4**: Integrate into render system in `src/ecs/systems/render_system.cpp`
- [ ] **Step 5**: Integrate into Lume3D shader in `api/3d/shaders/common/3d_dm_inplace_post_process.h`

### LumeScene (9 steps)

**Checklist:**
- [ ] **Step 1**: Define interface in `include/scene/interface/postprocess/intf_your_effect.h`
- [ ] **Step 2**: Add to IPostProcess interface in `include/scene/interface/intf_postprocess.h`
- [ ] **Step 3**: Implement API wrapper in `include/scene/api/post_process.h`
- [ ] **Step 4**: Implement effect class in `src/postprocess/your_effect.h` and `src/postprocess/your_effect.cpp`
- [ ] **Step 5**: Register in PostProcess in `src/postprocess/postprocess.h` and `src/postprocess/postprocess.cpp`
- [ ] **Step 6**: Register component type in `src/component/postprocess_component.h`
- [ ] **Step 7**: Register plugin type in `src/plugin.cpp`
- [ ] **Step 8**: Register Any type in `src/register_anys.cpp`
- [ ] **Step 9**: Update build files in `include/CMakeLists.txt`, `src/CMakeLists.txt`, `BUILD.gn`

---

## Troubleshooting Reference

### Common Mistakes

**1. Index Mismatch**
- **Symptom**: Effect parameters affect wrong effect
- **Cause**: `POST_PROCESS_INDEX_*` != `PostProcessConfiguration::INDEX_*`
- **Fix**: Ensure indices match across shader and C++ code

**2. Flag Bit Collision**
- **Symptom**: Effect doesn't enable/disable correctly
- **Cause**: `POST_PROCESS_SPECIALIZATION_*_BIT` != `FlagBits::*_BIT`
- **Fix**: Use `1 << N` where N matches enum position

**3. Missing Dual Path**
- **Symptom**: Effect works in some scenarios but not all
- **Cause**: Only implemented in DataStore OR RenderNodeUtil
- **Fix**: Implement conversion in BOTH paths (Steps 5 and 6)

**4. UserFactor Index Overflow**
- **Symptom**: GPU data corruption
- **Cause**: `userFactors[]` index collision
- **Fix**: Coordinate index allocation across all effects

### Validation Checklist

After implementation, verify:

- [ ] Effect compiles across all three modules
- [ ] Effect appears in scene graph interface
- [ ] Effect parameters update correctly in real-time
- [ ] Effect enables/disables without crashing
- [ ] Effect works with other Combined effects simultaneously
- [ ] GPU uniform data matches configuration (use RenderDoc/Snapdragon Profiler)
- [ ] Shader specialization constants correct (check SPIR-V reflection)