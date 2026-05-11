# Advanced Reference: Combined Post-Process Implementation

This document provides advanced reference materials for Combined post-process implementation:
- **Data Flow Diagrams**: Visual representation of data transformation across layers
- **Implementation Checklist**: Step-by-step completion tracking

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

## Implementation Checklist

Use this checklist to track completion across all three modules.

### LumeRender (8 steps)

**File Locations:**
- `render_data_store_render_pods.h` - Configuration structs
- `render_post_process_combined_node.cpp` - Metadata registration
- `render_post_process_structs_common.h` - Shader constants
- `render_data_store_post_process.h/cpp` - DataStore layer
- `render_node_util.cpp` - RenderNode conversion
- `render_post_process_blocks.h` - Shader functions
- `fullscreen_combined_post_process.frag` - Pipeline integration

**Checklist:**
- [ ] **Step 1**: Define configuration structure in `render_data_store_render_pods.h`
  ```cpp
  struct YourEffectConfiguration {
      float parameter1;
      int parameter2;
      // Add more as needed
  };
  ```

- [ ] **Step 2**: Register metadata in `render_post_process_combined_node.cpp`
  ```cpp
  jsonMgr.AddMetadata<YourEffectConfiguration>("YourEffect");
  ```

- [ ] **Step 3**: Define shader constants in `render_post_process_structs_common.h`
  ```cpp
  constexpr uint32_t POST_PROCESS_INDEX_YOUR_EFFECT = 8; // Next available index
  constexpr uint32_t POST_PROCESS_SPECIALIZATION_YOUR_EFFECT_BIT = 1 << 8;
  ```

- [ ] **Step 4**: Implement `GetFactorYourEffect()` in `render_data_store_post_process.h`
  ```cpp
  Vec4 GetFactorYourEffect(const YourEffectConfiguration& config) const;
  ```

- [ ] **Step 5**: Fill post-process stack in `render_data_store_post_process.cpp`
  ```cpp
  factors[POST_PROCESS_INDEX_YOUR_EFFECT] = GetFactorYourEffect(config);
  ```

- [ ] **Step 6**: Add conversion in `render_node_util.cpp`
  ```cpp
  void RenderNodeUtil::ConvertYourEffect(const YourEffectConfiguration& config) {
      // Conversion logic
  }
  ```

- [ ] **Step 7**: Implement `PostProcessYourEffectBlock()` in `render_post_process_blocks.h`
  ```cpp
  void PostProcessYourEffectBlock(vec3 inColor, vec3 outColor) {
      // Shader processing logic
  }
  ```

- [ ] **Step 8**: Integrate into pipeline in `fullscreen_combined_post_process.frag`
  ```glsl
  if (checkBit(flags.x, POST_PROCESS_SPECIALIZATION_YOUR_EFFECT_BIT)) {
      PostProcessYourEffectBlock(inColor, outColor);
  }
  ```

### Lume3D (5 steps)

**File Locations:**
- `api/3d/ecs/components/post_process_component.h` - Component definition
- `src/ecs/components/post_process_component_manager.cpp` - Metadata registration
- `src/ecs/systems/render_system.cpp` - System integration
- `api/3d/shaders/common/3d_dm_inplace_post_process.h` - Shader integration

**Checklist:**
- [ ] **Step 1**: Add flag bit in `post_process_component.h`
  ```cpp
  enum FlagBits {
      YOUR_EFFECT_BIT = 1 << 8,
  };
  ```

- [ ] **Step 2**: Define component property in `post_process_component.h`
  ```cpp
  DEFINE_PROPERTY(yourEffectConfiguration, YourEffectConfiguration, YourEffectConfiguration);
  ```

- [ ] **Step 3**: Register metadata in `post_process_component_manager.cpp`
  ```cpp
  jsonMgr.AddMetadata<YourEffectConfiguration>("YourEffect");
  ```

- [ ] **Step 4**: Integrate into render system in `render_system.cpp`
  ```cpp
  void RenderSystem::ProcessPostProcessComponents() {
      // Your effect processing
  }
  ```

- [ ] **Step 5**: Integrate into Lume3D shader in `3d_dm_inplace_post_process.h`
  ```glsl
  PostProcessYourEffectBlock(inColor, outColor);
  ```

### LumeScene (9 steps)

**File Locations:**
- `include/scene/interface/postprocess/intf_your_effect.h` - Interface definition
- `include/scene/interface/intf_postprocess.h` - IPostProcess interface
- `include/scene/api/post_process.h` - API wrapper
- `src/postprocess/your_effect.h/cpp` - Effect implementation
- `src/postprocess/postprocess.h/cpp` - Registration
- `src/component/postprocess_component.h` - Component registration
- `src/plugin.cpp` - Plugin registration
- `src/register_anys.cpp` - Any type registration
- `CMakeLists.txt`, `BUILD.gn` - Build configuration

**Checklist:**
- [ ] **Step 1**: Define interface in `intf_your_effect.h`
  ```cpp
  META_INTERFACE(YourEffect, BASEOHOS::Scene::IPostProcessEffect)
  META_READONLY_PROPERTY(float, parameter1)
  META_READONLY_PROPERTY(int, parameter2)
  ```

- [ ] **Step 2**: Add to IPostProcess interface in `intf_postprocess.h`
  ```cpp
  #include "postprocess/intf_your_effect.h"
  META_READONLY_PROPERTY(BASEOHOS::Scene::IYourEffect, YourEffect)
  ```

- [ ] **Step 3**: Implement API wrapper in `post_process.h`
  ```cpp
  class YourEffect : public IYourEffect {
      META_INTERFACE_OBJECT(YourEffect)
      // Implementation
  };
  ```

- [ ] **Step 4**: Implement effect class in `your_effect.h/cpp`
  ```cpp
  class YourEffectImpl : public YourEffect {
      // Full implementation
  };
  ```

- [ ] **Step 5**: Register in PostProcess in `postprocess.h/cpp`
  ```cpp
  yourEffect_ = YourEffect::Ptr(new YourEffectImpl());
  ```

- [ ] **Step 6**: Register component type in `postprocess_component.h`
  ```cpp
  #include "postprocess/intf_your_effect.h"
  ```

- [ ] **Step 7**: Register plugin type in `plugin.cpp`
  ```cpp
  plugin.RegisterInterfaceType<IYourEffect>();
  ```

- [ ] **Step 8**: Register Any type in `register_anys.cpp`
  ```cpp
  RegisterAny<YourEffectConfiguration>();
  ```

- [ ] **Step 9**: Update build files
  - Add source files to `CMakeLists.txt`
  - Add source files to `BUILD.gn`

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