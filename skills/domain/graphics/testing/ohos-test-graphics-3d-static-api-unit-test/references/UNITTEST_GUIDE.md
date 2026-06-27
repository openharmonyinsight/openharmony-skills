# ETS Kit Unit Test — Setup & Development Guide

## Directory Structure

```
kits/ets/test/unittest/
├── BUILD.gn                     # GN build config
├── common/                      # Test infrastructure
│   ├── ets_test.h              # EtsTest base class header
│   └── ets_test.cpp            # EtsTest base class implementation
└── api_unit_test/              # API unit tests
    └── scene_ets_unit_test.cpp # SceneETS test cases
```

## EtsTest Base Class — Engine Lifecycle

`EtsTest` inherits `::testing::Test` and manages the complete AGP 3D engine lifecycle. **Understanding this is critical** — every ETS wrapper depends on engine context, and improper cleanup crashes subsequent tests.

### Initialization Flow (SetUp)

6 steps executed before each test case:

1. **LoadEngineLib()** — `dlopen(LIB_ENGINE_CORE)` loads `libAGPDLL.z.so`, resolves mangled C++ symbols (`CreatePluginRegistry`, `GetPluginRegister`, `IsDebugBuild`, `GetVersion`) via `dlsym`
2. **LoadPlugins()** — Registers plugin registry, loads `UID_SCENE_PLUGIN`
3. **CreateEngine()** — Creates `IEngine` via `IEngineFactory`, initializes file manager and platform paths
4. **CreateRenderContext()** — Creates `IRenderContext`, selects backend via conditional compilation:
   - `RENDER_HAS_VULKAN_BACKEND` → Vulkan backend
   - `RENDER_HAS_GLES_BACKEND` → OpenGL ES backend (default for OH devices)
5. **CreateGraphicsContext()** — Creates `IGraphicsContext` via render context factory
6. **CreateApplicationContext()** — Creates `IApplicationContext` with task queues (`ENGINE_THREAD`), resource manager (`FileResourceManager`), and registers metadata properties (EngineQueue, AppQueue, RenderContext)

### Cleanup Flow (TearDown)

Critical cleanup sequence — **wrong order causes crashes**:

1. Unregister all task queues (`UnregisterAllTaskQueues`)
2. Remove all resources via render context (`RemoveAllResources`)
3. Release application context
4. Flush render queue (`AddFutureTaskOrRunDirectly` — blocks until queued tasks complete)
5. Remove metadata properties (EngineQueue, AppQueue, RenderContext) from `ObjectRegistry`
6. Reset render/app queues and renderer
7. Reset contexts in order: applicationContext → graphicsContext3D → renderContext → engine
8. `dlclose(libHandle_)` — close engine library

**Key insight**: Steps 4-5 (flush queue + remove properties) are non-obvious. Skipping them causes the engine to crash on next test's SetUp because dangling task references remain.

### Class Definition

```cpp
class EtsTest : public ::testing::Test {
public:
    void SetUp() override;
    void TearDown() override;
private:
    void LoadEngineLib();
    void LoadPlugins(const CORE_NS::PlatformCreateInfo&);
    void CreateEngine(const CORE_NS::PlatformCreateInfo&);
    void CreateRenderContext();
    void CreateGraphicsContext();
    void CreateApplicationContext();

    void *libHandle_;
    CORE_NS::IEngine::Ptr engine_;
    BASE_NS::shared_ptr<RENDER_NS::IRenderContext> renderContext_;
    CORE3D_NS::IGraphicsContext::Ptr graphicsContext3D_;
    SCENE_NS::IApplicationContext::Ptr applicationContext_;
};
```

## Writing New Test Cases

### File Scaffold

Each test file starts with this fixed scaffold (includes + namespace + class definition):

```cpp
#include <gtest/gtest.h>
#include <memory>

#include "common/ets_test.h"
#include "<Module>ETS.h"

using namespace testing;
using namespace testing::ext;
namespace OHOS::Render3D {
class <Module>ETSUnitTest : public EtsTest {
};
```

Test case body follows SKILL.md conventions: `@tc.name/@tc.desc/@tc.type` annotations → `HWTEST_F` macro → `std::make_shared` → test logic → `EXPECT_*` assertions → `obj->Destroy()`.

### Per-Method Test Scenarios

| Method Type | Minimum Test Cases | Pattern |
|-------------|-------------------|---------|
| **Create** | 1: creation + IsValid | Create object, check IsValid, Destroy |
| **Load** | 3: empty, valid, invalid path | Create, Load(path), verify result, Destroy |
| **Getter/SetProperty** | 1: setter→getter roundtrip | Set value, Get value, compare, Destroy |
| **IsValid** | 2: valid state + invalid state | Create valid vs invalid, check IsValid, Destroy |
| **Destroy** | 1: verify cleanup | Create, Destroy, verify resources released |

**Example — Load with multiple paths**:

```cpp
/**
 * @tc.name: SceneETS_Load_001
 * @tc.desc: Test SceneETS::Load with empty path
 * @tc.type: FUNC
 */
HWTEST_F(SceneETSUnitTest, SceneETS_Load_001, TestSize.Level1)
{
    auto sceneETS = std::make_shared<SceneETS>();
    bool result = sceneETS->Load("");
    EXPECT_TRUE(result);
    sceneETS->Destroy();
}

/**
 * @tc.name: SceneETS_Load_002
 * @tc.desc: Test SceneETS::Load with invalid path
 * @tc.type: FUNC
 */
HWTEST_F(SceneETSUnitTest, SceneETS_Load_002, TestSize.Level2)
{
    auto sceneETS = std::make_shared<SceneETS>();
    bool result = sceneETS->Load("/invalid/path/to/file.glb");
    EXPECT_FALSE(result);
    sceneETS->Destroy();
}
```

**Example — Property roundtrip**:

```cpp
/**
 * @tc.name: MaterialETS_SetProperty_001
 * @tc.desc: Test MaterialETS albedo color setter/getter roundtrip
 * @tc.type: FUNC
 */
HWTEST_F(MaterialETSUnitTest, MaterialETS_SetProperty_001, TestSize.Level1)
{
    auto material = std::make_shared<MaterialETS>();
    material->SetAlbedoColor(1.0f, 0.0f, 0.0f);
    EXPECT_EQ(material->GetAlbedoColor(), Color(1.0f, 0.0f, 0.0f));
    material->Destroy();
}
```

### ASSERT vs EXPECT — Critical for ETS Tests

In ETS tests, `ASSERT_*` stops the test immediately and **skips your Destroy() call**. This leaves engine resources dangling.

- Use `EXPECT_*` for assertions in test body — test continues to Destroy() even on failure
- Only use `ASSERT_*` in SetUp/TearDown (EtsTest already uses it there) or when Destroy() would be meaningless anyway (e.g., object creation itself failed)

```cpp
// BAD — skips Destroy() on failure
HWTEST_F(SceneETSUnitTest, SceneETS_Load_001, TestSize.Level1)
{
    auto sceneETS = std::make_shared<SceneETS>();
    ASSERT_TRUE(sceneETS->IsValid());  // Fails here → Destroy() never called
    sceneETS->Destroy();
}

// GOOD — Destroy() always reached
HWTEST_F(SceneETSUnitTest, SceneETS_Load_001, TestSize.Level1)
{
    auto sceneETS = std::make_shared<SceneETS>();
    EXPECT_TRUE(sceneETS->IsValid());  // Failure logged but continues
    sceneETS->Destroy();
}
```

## BUILD.gn Configuration

### Updating for New Test Module

When adding a new `<module>_ets_unit_test.cpp`, update `BUILD.gn`:

**1. Add source file**:
```gni
sources = [
    "common/ets_test.cpp",
    "api_unit_test/scene_ets_unit_test.cpp",
    "api_unit_test/<module>_ets_unit_test.cpp",  # New
]
```

**2. Add header include path** (if new module has its own headers):
```gni
include_dirs += [
    "//foundation/graphic/graphic_3d/kits/ets/include/<module>",
]
```

**3. Add new deps** (if module depends on additional libraries):
```gni
deps += [
    "//foundation/graphic/graphic_3d/<adapter>:<library>",
]
```

### Platform-Specific Defines

BUILD.gn uses conditional `target_cpu` defines for library paths. These are **mandatory** — without them, engine can't find libraries on device:

```gni
if (target_cpu == "arm") {
    defines += [
        "PLATFORM_CORE_ROOT_PATH=/system/lib/",
        "PLATFORM_CORE_PLUGIN_PATH=/system/lib/graphics3d",
        "PLATFORM_APP_ROOT_PATH=/system/lib/",
        "PLATFORM_APP_PLUGIN_PATH=/system/lib/graphics3d",
    ]
}

if (target_cpu == "arm64") {
    defines += [
        "PLATFORM_CORE_ROOT_PATH=/system/lib64/",
        "PLATFORM_CORE_PLUGIN_PATH=/system/lib64/graphics3d/",
        "PLATFORM_APP_ROOT_PATH=/system/lib64/",
        "PLATFORM_APP_PLUGIN_PATH=/system/lib64/graphics3d/",
    ]
}
```

The engine library macro uses a variable (not hardcoded):
```gni
defines += [ "LIB_ENGINE_CORE=\"${LIB_ENGINE_CORE}.z.so\"" ]
```

### Multiple Test Targets

For multiple independent test modules, create separate `ohos_unittest` targets and add them to the `group("unittest")` deps:

```gni
ohos_unittest("SceneETSUnitTest") {
    # ... config for SceneETS tests ...
}

ohos_unittest("MaterialETSUnitTest") {
    # ... config for MaterialETS tests ...
}

group("unittest") {
    testonly = true
    deps = [
        ":SceneETSUnitTest",
        ":MaterialETSUnitTest",
    ]
}
```

## Build & Run

```bash
# Build entire graphic_3d module (including tests)
hb build graphic_3d

# Build only test module
hb build graphic_3d_kits_ets_test_unittest

# Push to device
hdc file send out/[product]/tests/.../SceneETSUnitTest /data/local/tmp/
hdc shell chmod 755 /data/local/tmp/SceneETSUnitTest

# Run all tests
hdc shell /data/local/tmp/SceneETSUnitTest

# Run specific test case
hdc shell /data/local/tmp/SceneETSUnitTest --gtest_filter=SceneETSUnitTest.SceneETS_Load_001

# Debug with hilog
# In test code: OH_LOG_Print(LOG_APP, LOG_INFO, 0xFF00, "Test", "Debug: %{public}s", info);
```

## Troubleshooting

### Compilation: header file not found

Check `include_dirs` in BUILD.gn. Common missing paths:
- `//foundation/graphic/graphic_3d/kits/ets/include/<subdir>`
- `//foundation/graphic/graphic_3d/3d_scene_adapter/include`
- `//foundation/graphic/graphic_3d/3d_widget_adapter/core/include`

### Runtime: shared library not found

`libAGPDLL.z.so` must be deployed to device. Check:
- `PLATFORM_CORE_ROOT_PATH` / `PLATFORM_APP_ROOT_PATH` defines match device path (`/system/lib64/` for arm64)
- `${LIB_ENGINE_CORE}.z.so` resolve correctly

### Test passes but engine crashes on next test

**Root cause**: Resources not properly released in previous test.

**Fix**: Ensure every test calls `obj->Destroy()` before test body ends. Never skip Destroy() — it releases the wrapper's engine-side resources that EtsTest TearDown doesn't know about.

### Test hangs or times out

**Root cause**: Task queue not flushed. Engine async operations may still be queued.

**Fix**: EtsTest TearDown flushes render queue via `AddFutureTaskOrRunDirectly`. If your test triggers async operations, ensure they complete before test body ends. Never manually modify engine task queues in test code.

## Complete BUILD.gn Template

```gni
# Copyright (c) 2025 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import("//build/config/features.gni")
import("//build/test.gni")
import("//build/ohos.gni")
import("//foundation/graphic/graphic_3d/lume/lume_config.gni")

module_output_path = "graphic_3d/graphic_3d/kits/ets"

# Engine core library name (without extension). Default: "libAGPDLL".
# Override via gn args or parent scope if your build uses a different engine binary.
LIB_ENGINE_CORE = "libAGPDLL"

ohos_unittest("SceneETSUnitTest") {
  module_out_path = module_output_path

  include_dirs = [
    ".",
    "//foundation/graphic/graphic_3d/kits/ets/include",
    "//foundation/graphic/graphic_3d/kits/ets/include/property_proxy",
    "//foundation/graphic/graphic_3d/kits/ets/include/geometry_definition",
    "//foundation/graphic/graphic_3d/3d_scene_adapter/include",
    "//foundation/graphic/graphic_3d/3d_widget_adapter/core/include",
    "//foundation/graphic/graphic_3d/3d_widget_adapter/include/ohos",
    "${LUME_BASE_PATH}/api",
    "${LUME_CORE_PATH}/api",
    "${LUME_RENDER_PATH}/api",
    "${LUME_CORE3D_PATH}/api",
    "${LUME_META_PATH}/include",
    "${LUME_SCENE_PATH}/include",
  ]

  if (current_os == "ohos") {
    include_dirs += [ "${LUME_CORE_PATH}/api/platform/ohos" ]
  }

  cflags = [
    "-g",
    "-O0",
    "-Wno-unused-variable",
    "-fno-omit-frame-pointer",
  ]

  sources = [
    "common/ets_test.cpp",
    "api_unit_test/scene_ets_unit_test.cpp",
  ]

  defines = [
    "CORE_HAS_GLES_BACKEND=1",
    "CORE_HAS_VULKAN_BACKEND=1",
  ]

  defines += [ "LIB_ENGINE_CORE=\"${LIB_ENGINE_CORE}.z.so\"" ]

  if (target_cpu == "arm") {
    defines += [
      "PLATFORM_CORE_ROOT_PATH=/system/lib/",
      "PLATFORM_CORE_PLUGIN_PATH=/system/lib/graphics3d",
      "PLATFORM_APP_ROOT_PATH=/system/lib/",
      "PLATFORM_APP_PLUGIN_PATH=/system/lib/graphics3d",
    ]
  }

  if (target_cpu == "arm64") {
    defines += [
      "PLATFORM_CORE_ROOT_PATH=/system/lib64/",
      "PLATFORM_CORE_PLUGIN_PATH=/system/lib64/graphics3d/",
      "PLATFORM_APP_ROOT_PATH=/system/lib64/",
      "PLATFORM_APP_PLUGIN_PATH=/system/lib64/graphics3d/",
    ]
  }

  configs = [
    "//foundation/graphic/graphic_3d/kits/ets:lume3d_config",
    "//foundation/graphic/graphic_3d/3d_scene_adapter:scene_adapter_config",
    "//foundation/graphic/graphic_3d/3d_widget_adapter:widget_adapter_config",
  ]

  deps = [
    "//foundation/graphic/graphic_3d/3d_widget_adapter:lib3dWidgetAdapter",
    "//foundation/graphic/graphic_3d/kits/ets:scene_ani",
    "//foundation/graphic/graphic_3d/kits/js:libKitHelper",
  ]

  external_deps = [
    "ability_runtime:ability_manager",
    "ability_runtime:app_context",
    "ability_runtime:data_ability_helper",
    "ability_runtime:napi_base_context",
    "ability_runtime:napi_common",
    "bundle_framework:appexecfwk_base",
    "bundle_framework:appexecfwk_core",
    "c_utils:utils",
    "googletest:gmock",
    "googletest:gtest",
    "graphic_2d:EGL",
    "graphic_2d:GLESv3",
    "graphic_2d:librender_service_base",
    "graphic_2d:librender_service_client",
    "graphic_surface:surface",
    "graphic_surface:sync_fence",
    "hilog:libhilog",
    "hitrace:hitrace_meter",
    "init:libbegetutil",
    "input:libmmi-client",
    "napi:ace_napi",
    "vulkan-headers:vulkan_headers",
  ]

  part_name = "graphic_3d"
  subsystem_name = "graphic"
}

group("unittest") {
  testonly = true
  deps = [
    ":SceneETSUnitTest",
  ]
}
```