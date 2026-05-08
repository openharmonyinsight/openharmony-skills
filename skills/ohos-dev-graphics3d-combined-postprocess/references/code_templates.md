# Code Templates for Combined Post-Process Implementation

This file contains detailed code templates for implementing combined post-processing effects across LumeRender, Lume3D, and LumeScene modules.

**Table of Contents:**
- [LumeRender Templates](#lumarender-templates) (Steps 1-8)
- [Lume3D Templates](#lume3d-templates) (Steps 1-5)
- [LumeScene Templates](#lumescene-templates) (Steps 1-9)

---

## LumeRender Templates

### Step 1: Define Configuration Structure

**File**: `api/render/datastore/render/render_data_store_render_pods.h`

**Generic Template:**
```cpp
/** Render your effect */
RENDER_YOUR_EFFECT = N,

/** User factor index for YourEffect property */
static constexpr uint32_t USER_INDEX_YOUR_EFFECT_PROPERTY { M };

/** Your effect configuration. */
struct YourEffectConfiguration {
    /** Property 1 description */
    type1 property1 { defaultValue1 };

    /** Property 2 description */
    type2 property2 { defaultValue2 };
};

/** Enable your effect */
ENABLE_YOUR_EFFECT_BIT = (1 << N),

INDEX_YOUR_EFFECT = N,

/** Your effect configuration */
YourEffectConfiguration yourEffectConfiguration;

DECLARE_PROPERTY_TYPE(RENDER_NS::YourEffectConfiguration);
```

**Tone Mapping Example:**
```cpp
/** Render tonemap post process */
RENDER_TONEMAP = 0,

/** Tonemap post process configuration. */
struct TonemapConfiguration {
    /** Tonemap type enum */
    enum TonemapType {
        /** ACES */
        TONEMAP_ACES = 0,
        /** ACES 2020 */
        TONEMAP_ACES_2020 = 1,
        /** Filmic */
        TONEMAP_FILMIC = 2,
        /** PBR Neutral */
        TONEMAP_PBR_NEUTRAL = 3,
    };

    /** Tonemap type (Default: TONEMAP_ACES) */
    TonemapType tonemapType { TonemapType::TONEMAP_ACES };
    /** Exposure (Default: 1.0f) */
    float exposure { 1.0f };
};

/** Enable tonemap post process */
ENABLE_TONEMAP_BIT = (1 << 0),

INDEX_TONEMAP = 0,

/** Tonemap configuration */
TonemapConfiguration tonemapConfiguration;

DECLARE_PROPERTY_TYPE(RENDER_NS::TonemapConfiguration);
```

---

### Step 2: Register Metadata

**File**: `src/postprocesses/render_post_process_combined_node.cpp`

**Generic Template:**
```cpp
ENUM_VALUE(ENABLE_YOUR_EFFECT_BIT, "Your Effect")

DATA_TYPE_METADATA(RENDER_NS::YourEffectConfiguration,
    MEMBER_PROPERTY(property1, "Property 1", 0),
    MEMBER_PROPERTY(property2, "Property 2", 0))

MEMBER_PROPERTY(yourEffectConfiguration, "Your Effect Configuration", 0)
```

**Tone Mapping Example:**
```cpp
ENUM_VALUE(ENABLE_TONEMAP_BIT, "Tonemap")

ENUM_TYPE_METADATA(RENDER_NS::TonemapConfiguration::TonemapType, 
    ENUM_VALUE(TONEMAP_ACES, "Aces"),
    ENUM_VALUE(TONEMAP_ACES_2020, "Aces 2020"), 
    ENUM_VALUE(TONEMAP_FILMIC, "Filmic"),
    ENUM_VALUE(TONEMAP_PBR_NEUTRAL, "Neutral"))

DATA_TYPE_METADATA(RENDER_NS::TonemapConfiguration, 
    MEMBER_PROPERTY(tonemapType, "Tonemap Type", 0),
    MEMBER_PROPERTY(exposure, "Exposure", 0))

MEMBER_PROPERTY(tonemapConfiguration, "Tonemap Configuration", 0)
```

---

### Step 3: Define Shader Constants

**File**: `api/render/shaders/common/render_post_process_structs_common.h`

**Generic Template:**
```glsl
#define POST_PROCESS_SPECIALIZATION_YOUR_EFFECT_BIT (1 << N)
#define POST_PROCESS_INDEX_YOUR_EFFECT N
#define POST_PROCESS_USER_INDEX_YOUR_EFFECT_PROPERTY M
```

**Tone Mapping Example:**
```glsl
#define POST_PROCESS_SPECIALIZATION_TONEMAP_BIT (1 << 0)
#define POST_PROCESS_INDEX_TONEMAP 0

#define CORE_POST_PROCESS_TONEMAP_ACES 0
#define CORE_POST_PROCESS_TONEMAP_ACES_2020 1
#define CORE_POST_PROCESS_TONEMAP_FILMIC 2
#define CORE_POST_PROCESS_TONEMAP_PBR_NEUTRAL 3
```

---

### Step 4: Implement Config-to-Shader Conversion

**File**: `src/datastore/render_data_store_post_process.h`

**Generic Template:**
```cpp
static inline BASE_NS::Math::Vec4 GetFactorYourEffect(const PostProcessConfiguration& input)
{
    return { input.yourEffectConfiguration.property1,
             input.yourEffectConfiguration.property2, 0.0f, 0.0f };
}

static inline BASE_NS::Math::Vec4 GetFactorYourEffectProperty(const PostProcessConfiguration& input)
{
    return input.yourEffectConfiguration.property3;
}
```

**Tone Mapping Example:**
```cpp
static inline BASE_NS::Math::Vec4 GetFactorTonemap(const PostProcessConfiguration& input)
{
    return { 
        input.tonemapConfiguration.exposure,
        0.0f,
        0.0f,
        static_cast<float>(input.tonemapConfiguration.tonemapType)
    };
}
```

---

### Step 5: Fill Post-Process Stack

**File**: `src/datastore/render_data_store_post_process.cpp`

**Generic Template:**
```cpp
ppStack.postProcesses.push_back(
    FillBuiltInData(PostProcessConstants::RENDER_YOUR_EFFECT,
        PostProcessConstants::RENDER_YOUR_EFFECT,
        defUserIdx,
        PostProcessConversionHelper::GetFactorYourEffect(ppConfig),
        {}));

ppStack.globalFactors.userFactors[PostProcessConstants::USER_INDEX_YOUR_EFFECT_PROPERTY] =
    PostProcessConversionHelper::GetFactorYourEffectProperty(ppConfig);
```

**Tone Mapping Example:**
```cpp
ppStack.postProcesses.push_back(
    FillBuiltInData(PostProcessConstants::RENDER_TONEMAP,
        PostProcessConstants::RENDER_TONEMAP,
        defUserIdx,
        PostProcessConversionHelper::GetFactorTonemap(ppConfig),
        {}));
```

---

### Step 6: Add Conversion in RenderNodeUtil

**File**: `src/nodecontext/render_node_util.cpp`

**Function**: `GetRenderPostProcessConfiguration(const PostProcessConfiguration& input)`

**Generic Template:**
```cpp
output.factors[PostProcessConfiguration::INDEX_YOUR_EFFECT] =
    PostProcessConversionHelper::GetFactorYourEffect(input);
```

**Tone Mapping Example:**
```cpp
output.factors[PostProcessConfiguration::INDEX_TONEMAP] = 
    PostProcessConversionHelper::GetFactorTonemap(input);
```

---

### Step 7: Implement Shader Processing Function

**File**: `api/render/shaders/common/render_post_process_blocks.h`

**Generic Template:**
```glsl
void PostProcessYourEffectBlock(
    in uint postProcessFlags,
    in vec4 factor,
    in vec3 inCol,
    out vec3 outCol)
{
    outCol = inCol;
    if ((postProcessFlags & POST_PROCESS_SPECIALIZATION_YOUR_EFFECT_BIT) ==
        POST_PROCESS_SPECIALIZATION_YOUR_EFFECT_BIT) {
        const float param1 = factor.x;
        const float param2 = factor.y;
        outCol = YourEffectLogic(outCol, param1, param2);
    }
}
```

**Tone Mapping Example:**
```glsl
#include "render_color_conversion_common.h"
#include "render_post_process_structs_common.h"
#include "render_tonemap_common.h"

void PostProcessTonemapBlock(
    in uint postProcessFlags, 
    in vec4 tonemapFactor, 
    in vec3 inCol, 
    out vec3 outCol)
{
    outCol = inCol;
    
    if ((postProcessFlags & POST_PROCESS_SPECIALIZATION_TONEMAP_BIT) == 
        POST_PROCESS_SPECIALIZATION_TONEMAP_BIT) {
        
        const float exposure = tonemapFactor.x;
        const uint tonemapType = uint(tonemapFactor.w);
        const vec3 x = outCol * exposure;
        
        if (tonemapType == CORE_POST_PROCESS_TONEMAP_ACES) {
            outCol = TonemapAces(x);
        } else if (tonemapType == CORE_POST_PROCESS_TONEMAP_ACES_2020) {
            outCol = TonemapAcesFilmRec2020(x);
        } else if (tonemapType == CORE_POST_PROCESS_TONEMAP_FILMIC) {
            const float exposureEstimate = 6.0f;
            outCol = TonemapFilmic(x * exposureEstimate);
        } else if (tonemapType == CORE_POST_PROCESS_TONEMAP_PBR_NEUTRAL) {
            outCol = TonemapPbrNeutral(x);
        }
    }
}
```

---

### Step 8: Integrate into Render Pipeline

**File**: `assets/render/shaders/shader/fullscreen_combined_post_process.frag`

**Generic Template:**
```glsl
PostProcessYourEffectBlock(
    uGlobalData.flags.x,
    uGlobalData.factors[POST_PROCESS_INDEX_YOUR_EFFECT],
    outColor.rgb,
    outColor.rgb);
```

**Tone Mapping Example:**
```glsl
#version 460 core
#extension GL_ARB_separate_shader_objects : enable
#extension GL_ARB_shading_language_420pack : enable

#include "render/shaders/common/render_post_process_structs_common.h"
#include "render/shaders/common/render_post_process_blocks.h"

layout(set = 0, binding = 0, std140) uniform uGlobalStructData
{
    GlobalPostProcessStruct uGlobalData;
};

layout(set = 1, binding = 0) uniform sampler2D uImgSampler;
layout(location = 0) in vec2 inUv;
layout(location = 0) out vec4 outColor;

void main(void)
{
    outColor = textureLod(uImgSampler, inUv, 0);
    
    PostProcessTonemapBlock(
        uGlobalData.flags.x,
        uGlobalData.factors[POST_PROCESS_INDEX_TONEMAP],
        outColor.rgb,
        outColor.rgb);
}
```

**File**: `assets/render/shaders/shader/fullscreen_combined_post_process_layer.frag` (if layer rendering is used)

**Generic Template:**
```glsl
PostProcessYourEffectBlock(
    uGlobalData.flags.x,
    uGlobalData.factors[POST_PROCESS_INDEX_YOUR_EFFECT],
    outColor.rgb,
    outColor.rgb);
```

---

## Lume3D Templates

### Step 1: Add Flag Bit

**File**: `api/3d/ecs/components/post_process_component.h`

**Generic Template:**
```cpp
YOUR_EFFECT_BIT = (1 << N),
```

**Tone Mapping Example:**
```cpp
TONEMAP_BIT = (1 << 0),
```

---

### Step 2: Define Component Property

**File**: `api/3d/ecs/components/post_process_component.h`

**Generic Template:**
```cpp
/** Your effect configuration.
 */
DEFINE_PROPERTY(RENDER_NS::YourEffectConfiguration, yourEffectConfiguration,
    "Your Effect Configuration", 0, ARRAY_VALUE())
```

**Tone Mapping Example:**
```cpp
/** Tonemap configuration. */
DEFINE_PROPERTY(
    RENDER_NS::TonemapConfiguration, 
    tonemapConfiguration, 
    "Tonemap Configuration", 
    0, 
    ARRAY_VALUE())
```

---

### Step 3: Register Metadata

**File**: `src/ecs/components/post_process_component_manager.cpp`

**Generic Template:**
```cpp
using RENDER_NS::YourEffectConfiguration;

ENUM_VALUE(YOUR_EFFECT_BIT, "Your Effect")

DATA_TYPE_METADATA(RENDER_NS::YourEffectConfiguration,
    MEMBER_PROPERTY(property1, "Property 1", 0),
    MEMBER_PROPERTY(property2, "Property 2", 0))
```

**Tone Mapping Example:**
```cpp
using RENDER_NS::TonemapConfiguration;

ENUM_VALUE(TONEMAP_BIT, "Tonemap")

ENUM_TYPE_METADATA(RENDER_NS::TonemapConfiguration::TonemapType, 
    ENUM_VALUE(TONEMAP_ACES, "Aces"),
    ENUM_VALUE(TONEMAP_ACES_2020, "Aces 2020"), 
    ENUM_VALUE(TONEMAP_FILMIC, "Filmic"),
    ENUM_VALUE(TONEMAP_PBR_NEUTRAL, "Neutral"))

DATA_TYPE_METADATA(RENDER_NS::TonemapConfiguration, 
    MEMBER_PROPERTY(tonemapType, "Tonemap Type", 0),
    MEMBER_PROPERTY(exposure, "Exposure", 0))
```

---

### Step 4: Integrate into Render System

**File**: `src/ecs/systems/render_system.cpp`

**Function**: `ProcessPostProcessComponents(const Entity& mainCameraEntity)`

**Generic Template:**
```cpp
ppConfig.yourEffectConfiguration = pp.yourEffectConfiguration;

ppConfig.userFactors[RENDER_NS::PostProcessConstants::USER_INDEX_YOUR_EFFECT_PROPERTY] =
    ppConfig.yourEffectConfiguration.property3;
```

**Tone Mapping Example:**
```cpp
ppConfig.tonemapConfiguration = pp.tonemapConfiguration;
```

---

### Step 5: Integrate into Lume3D Shader

**File**: `api/3d/shaders/common/3d_dm_inplace_post_process.h`

**Generic Template:**
```glsl
PostProcessYourEffectBlock(
    uPostProcessData.flags.x,
    uPostProcessData.factors[POST_PROCESS_INDEX_YOUR_EFFECT],
    uPostProcessData.userFactors[POST_PROCESS_USER_INDEX_YOUR_EFFECT_PROPERTY],
    color.rgb,
    color.rgb);
```

**Tone Mapping Example:**
```glsl
#include "render/shaders/common/render_post_process_blocks.h"

#ifdef VULKAN

void InplacePostProcess(in vec2 fragUv, inout vec4 color)
{
    PostProcessTonemapBlock(
        uPostProcessData.flags.x,
        uPostProcessData.factors[POST_PROCESS_INDEX_TONEMAP],
        color.rgb,
        color.rgb);
}

#endif
```

---

## LumeScene Templates

### Step 1: Define Interface

**File**: `include/scene/interface/postprocess/intf_your_effect.h`

**Generic Template:**
```cpp
SCENE_BEGIN_NAMESPACE()

class IYourEffect : public IPostProcessEffect {
    META_INTERFACE(IPostProcessEffect, IYourEffect, "UUID")
public:
    META_PROPERTY(type1, Property1)
    META_PROPERTY(type2, Property2)
};

SCENE_END_NAMESPACE()

META_INTERFACE_TYPE(SCENE_NS::IYourEffect)
```

**Tone Mapping Example:**
```cpp
SCENE_BEGIN_NAMESPACE()

class ITonemap : public IPostProcessEffect {
    META_INTERFACE(IPostProcessEffect, ITonemap, "b902a0b0-3c2d-4e5f-8a9b-0c1d2e3f4a5b")
public:
    META_PROPERTY(TonemapType, TonemapType)
    META_PROPERTY(float, Exposure)
};

SCENE_END_NAMESPACE()

META_TYPE(SCENE_NS::ITonemap::TonemapType)
META_INTERFACE_TYPE(SCENE_NS::ITonemap)
```

---

### Step 2: Add to IPostProcess Interface

**File**: `include/scene/interface/intf_postprocess.h`

**Generic Template:**
```cpp
#include <scene/interface/postprocess/intf_your_effect.h>

/**
 * @brief Camera postprocessing settings, your effect
 */
META_READONLY_PROPERTY(IYourEffect::Ptr, YourEffect)
```

**Tone Mapping Example:**
```cpp
#include <scene/interface/postprocess/intf_tonemap.h>

/**
 * @brief Camera postprocessing settings, tonemap
 */
META_READONLY_PROPERTY(ITonemap::Ptr, Tonemap)
```

---

### Step 3: Implement API Wrapper

**File**: `include/scene/api/post_process.h`

**Generic Template:**
```cpp
class YourEffect : public PostProcessEffect {
public:
    META_INTERFACE_OBJECT(YourEffect, PostProcessEffect, IYourEffect)
    META_INTERFACE_OBJECT_PROPERTY(type1, Property1)
    META_INTERFACE_OBJECT_PROPERTY(type2, Property2)
};

META_INTERFACE_OBJECT_READONLY_PROPERTY(SCENE_NS::YourEffect, YourEffect)
```

**Tone Mapping Example:**
```cpp
class Tonemap : public PostProcessEffect {
public:
    META_INTERFACE_OBJECT(Tonemap, PostProcessEffect, ITonemap)
    META_INTERFACE_OBJECT_PROPERTY(TonemapType, TonemapType)
    META_INTERFACE_OBJECT_PROPERTY(float, Exposure)
};

META_INTERFACE_OBJECT_READONLY_PROPERTY(SCENE_NS::Tonemap, Tonemap)
```

---

### Step 4: Implement Effect Class

**Header File**: `src/postprocess/your_effect.h`

**Generic Template:**
```cpp
META_REGISTER_CLASS(YourEffect, "UUID", META_NS::ObjectCategoryBits::NO_CATEGORY)

class YourEffect : public Internal::PostProcessEffect<IYourEffect,
    CORE3D_NS::PostProcessComponent::YOUR_EFFECT_BIT> {
    META_OBJECT(YourEffect, ClassId::YourEffect, PostProcessEffect)
public:
    META_BEGIN_STATIC_DATA()
    SCENE_STATIC_DYNINIT_PROPERTY_DATA(IPostProcessEffect, bool, Enabled, "")
    SCENE_STATIC_DYNINIT_PROPERTY_DATA(IYourEffect, type1, Property1, "property1")
    SCENE_STATIC_DYNINIT_PROPERTY_DATA(IYourEffect, type2, Property2, "property2")
    META_END_STATIC_DATA()

    META_IMPLEMENT_PROPERTY(bool, Enabled)
    META_IMPLEMENT_PROPERTY(type1, Property1)
    META_IMPLEMENT_PROPERTY(type2, Property2)

private:
    BASE_NS::string_view GetComponentPath() const override;
};
```

**Tone Mapping Example:**
```cpp
META_REGISTER_CLASS(Tonemap, "b902a0b0-3c2d-4e5f-8a9b-0c1d2e3f4a5c", META_NS::ObjectCategoryBits::NO_CATEGORY)

class Tonemap : public Internal::PostProcessEffect<ITonemap,
    CORE3D_NS::PostProcessComponent::TONEMAP_BIT> {
    META_OBJECT(Tonemap, ClassId::Tonemap, PostProcessEffect)
public:
    META_BEGIN_STATIC_DATA()
    SCENE_STATIC_DYNINIT_PROPERTY_DATA(IPostProcessEffect, bool, Enabled, "")
    SCENE_STATIC_DYNINIT_PROPERTY_DATA(ITonemap, TonemapType, TonemapType, "tonemapType")
    SCENE_STATIC_DYNINITINIT_PROPERTY_DATA(ITonemap, float, Exposure, "exposure")
    META_END_STATIC_DATA()

    META_IMPLEMENT_PROPERTY(bool, Enabled)
    META_IMPLEMENT_PROPERTY(TonemapType, TonemapType)
    META_IMPLEMENT_PROPERTY(float, Exposure)

private:
    BASE_NS::string_view GetComponentPath() const override;
};
```

**Implementation File**: `src/postprocess/your_effect.cpp`

**Generic Template:**
```cpp
BASE_NS::string_view YourEffect::GetComponentPath() const
{
    static constexpr BASE_NS::string_view p("PostProcessComponent.yourEffectConfiguration.");
    return p;
}
```

**Tone Mapping Example:**
```cpp
BASE_NS::string_view Tonemap::GetComponentPath() const
{
    static constexpr BASE_NS::string_view p("PostProcessComponent.tonemapConfiguration.");
    return p;
}
```

---

### Step 5: Register in PostProcess

**Header File**: `src/postprocess/postprocess.h`

**Generic Template:**
```cpp
SCENE_STATIC_DYNINIT_PROPERTY_DATA(IPostProcess, IYourEffect::Ptr, YourEffect, "")
META_IMPLEMENT_READONLY_PROPERTY(IYourEffect::Ptr, YourEffect)
```

**Tone Mapping Example:**
```cpp
SCENE_STATIC_DYNINIT_PROPERTY_DATA(IPostProcess, ITonemap::Ptr, Tonemap, "")
META_IMPLEMENT_READONLY_PROPERTY(ITonemap::Ptr, Tonemap)
```

**Implementation File**: `src/postprocess/postprocess.cpp`

**Generic Template:**
```cpp
#include "your_effect.h"

if (name == "YourEffect") {
    return InitEffect<IYourEffect>(p, ClassId::YourEffect);
}
```

**Tone Mapping Example:**
```cpp
#include "tonemap.h"

if (name == "Tonemap") {
    return InitEffect<ITonemap>(p, ClassId::Tonemap);
}
```

---

### Step 6: Register Component Type

**File**: `src/component/postprocess_component.h`

**Generic Template:**
```cpp
META_TYPE(RENDER_NS::YourEffectConfiguration)

META_PROPERTY(RENDER_NS::YourEffectConfiguration, YourEffect)

SCENE_STATIC_PROPERTY_DATA(
    IInternalPostProcess, RENDER_NS::YourEffectConfiguration, YourEffect,
    "PostProcessComponent.yourEffectConfiguration")

META_IMPLEMENT_PROPERTY(RENDER_NS::YourEffectConfiguration, YourEffect)
```

**Tone Mapping Example:**
```cpp
META_TYPE(RENDER_NS::TonemapConfiguration)

META_PROPERTY(RENDER_NS::TonemapConfiguration, Tonemap)

SCENE_STATIC_PROPERTY_DATA(
    IInternalPostProcess, RENDER_NS::TonemapConfiguration, Tonemap,
    "PostProcessComponent.tonemapConfiguration")

META_IMPLEMENT_PROPERTY(RENDER_NS::TonemapConfiguration, Tonemap)
```

---

### Step 7: Register Plugin Type

**File**: `src/plugin.cpp`

**Generic Template:**
```cpp
#include "postprocess/your_effect.h"

META_NS::RegisterObjectType<YourEffect>();

META_NS::UnregisterObjectType<YourEffect>();
```

**Tone Mapping Example:**
```cpp
#include "postprocess/tonemap.h"

META_NS::RegisterObjectType<Tonemap>();

META_NS::UnregisterObjectType<Tonemap>();
```

---

### Step 8: Register Any Type

**File**: `src/register_anys.cpp`

**Generic Template:**
```cpp
IYourEffect::Ptr,
```

**Tone Mapping Example:**
```cpp
ITonemap::Ptr,
```

---

### Step 9: Update Build Files

**include/CMakeLists.txt**: Add interface file to API target
```cmake
scene/interface/postprocess/intf_your_effect.h
```

**src/CMakeLists.txt**: Add source files to private target
```cmake
postprocess/your_effect.cpp
postprocess/your_effect.h
```

**BUILD.gn**: Add source files to lume_scenewidget_src
```gn
"src/postprocess/your_effect.cpp",
"src/postprocess/your_effect.h",
```

**Tone Mapping Example:**

include/CMakeLists.txt:
```cmake
scene/interface/postprocess/intf_tonemap.h
```

src/CMakeLists.txt:
```cmake
postprocess/tonemap.cpp
postprocess/tonemap.h
```

BUILD.gn:
```gn
"src/postprocess/tonemap.cpp",
"src/postprocess/tonemap.h",
```