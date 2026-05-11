# ETS Kit Unit Test Environment Setup and Development Guide

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Environment Setup](#environment-setup)
- [Build and Compilation](#build-and-compilation)
- [Running Tests](#running-tests)
- [Test Framework Description](#test-framework-description)
- [Developing New Test Cases](#developing-new-test-cases)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)

---

## Overview

This guide is for developing and maintaining unit tests for the AGP (Ark Graphics Platform) engine ETS Kit. The test framework is built on GTest (gtest/gmock) and is used to test the ETS (Extended TypeScript) interface layer functionality of the 3D graphics engine.

### Key Features

- Built on GTest framework
- Supports multiple graphics backends (OpenGL ES / Vulkan)
- Complete engine lifecycle management
- Automated resource management and cleanup
- Modular test structure

---

## Directory Structure

```
kits/ets/test/unittest/
├── BUILD.gn                     # GN build configuration file
├── common/                      # Common test infrastructure
│   ├── ets_test.h              # Test base class header file
│   └── ets_test.cpp            # Test base class implementation
└── api_unit_test/              # API unit tests
    └── scene_ets_unit_test.cpp # SceneETS test cases
```

### File Descriptions

#### `BUILD.gn`
GN (Generate Ninja) build system configuration file that defines:
- Test target name: `SceneETSUnitTest`
- Header file search paths
- Source file list
- Compilation options and definitions
- Dependencies (internal and external)

#### `common/ets_test.h` & `common/ets_test.cpp`
Test infrastructure that provides:
- `EtsTest` base class: inherits from `::testing::Test`
- Complete engine initialization flow
- Automated resource cleanup

#### `api_unit_test/`
Contains test cases for various APIs, organized by module.

---

## Environment Setup

### Prerequisites

#### Required Components

1. **OpenHarmony Build Environment**
   - GN build tool
   - Ninja compilation tool
   - LLVM toolchain

2. **System Dependencies**
   - `ability_runtime`: Ability runtime
   - `graphic_2d`: 2D graphics library (EGL/GLES)
   - `napi`: Node.js API
   - `hilog`: Logging system
   - `googletest`: Unit test framework

3. **Engine Dependencies**
   - `3d_widget_adapter`: 3D widget adapter
   - `scene_ani`: Scene animation
   - `libKitHelper`: Helper utility library

#### Compiler Requirements

- Supports C++17 standard
- Supports OpenGL ES 3.x or Vulkan

---

## Build and Compilation

### 1. Configure Build Parameters

Before compiling, ensure the following parameters are correctly configured:

```bash
# Set target CPU architecture in build command
target_cpu = "arm64"  # or "arm"
```

The system will automatically set based on CPU architecture:
- `PLATFORM_CORE_ROOT_PATH`: Core library path
- `PLATFORM_CORE_PLUGIN_PATH`: Core plugin path
- `PLATFORM_APP_ROOT_PATH`: Application library path
- `PLATFORM_APP_PLUGIN_PATH`: Application plugin path

### 2. Build Commands

```bash
# Build entire graphic_3d module (including tests)
hb build graphic_3d

# Build only test module
hb build graphic_3d_kits_ets_test_unittest
```

### 3. Output Location

After successful compilation, the test executable is located at:
```
out/[product_name]/tests/graphic_3d/graphic_3d/kits/ets/SceneETSUnitTest
```

---

## Running Tests

### Running on Device

```bash
# Push test to device
hdc file send out/[product_name]/tests/.../SceneETSUnitTest /data/local/tmp/

# Add execute permission
hdc shell chmod 755 /data/local/tmp/SceneETSUnitTest

# Run test
hdc shell /data/local/tmp/SceneETSUnitTest
```

### Test Output Example

```
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from SceneETSUnitTest
[ RUN      ] SceneETSUnitTest.SceneETS_Load_001
[       OK ] SceneETSUnitTest.SceneETS_Load_001 (XXX ms)
[----------] 1 test from SceneETSUnitTest (XXX ms total)

[==========] 1 test from 1 test suite ran. (XXX ms total)
[  PASSED  ] 1 test.
```

---

## Test Framework Description

### EtsTest Base Class

`EtsTest` is the base class for all unit tests, responsible for initializing the complete 3D engine environment.

#### Class Definition

```cpp
class EtsTest : public ::testing::Test {
public:
    void SetUp() override;    // Executed before each test case
    void TearDown() override; // Executed after each test case

private:
    void LoadEngineLib();
    void LoadPlugins(const CORE_NS::PlatformCreateInfo&);
    void CreateEngine(const CORE_NS::PlatformCreateInfo&);
    void CreateRenderContext();
    void CreateGraphicsContext();
    void CreateApplicationContext();

    void* libHandle_;                           // Engine library handle
    CORE_NS::IEngine::Ptr engine_;              // Engine instance
    BASE_NS::shared_ptr<RENDER_NS::IRenderContext> renderContext_;
    CORE3D_NS::IGraphicsContext::Ptr graphicsContext3D_;
    SCENE_NS::IApplicationContext::Ptr applicationContext_;
};
```

#### Initialization Flow

1. **LoadEngineLib()**: Dynamically loads engine core library `libAGPDLL.z.so`
2. **LoadPlugins()**: Loads necessary plugins (such as scene plugins)
3. **CreateEngine()**: Creates engine instance and initializes file manager
4. **CreateRenderContext()**: Creates render context, supports Vulkan/GLES backend
5. **CreateGraphicsContext()**: Creates 3D graphics context
6. **CreateApplicationContext()**: Creates application context, including task queue and resource manager

#### Cleanup Flow

`TearDown()` automatically cleans up all resources, including:
- Unregisters all task queues
- Releases resources
- Closes engine library handle

### Test Case Macros

Use OpenHarmony test macros:

```cpp
HWTEST_F(TestClassName, TestCaseName, TestLevel)
```

- `HWTEST_F`: Fixed test fixture
- Test levels (per OpenHarmony Hypium framework specification):
  - `TestSize.Level0`: Smoke test - Basic functionality verification
  - `TestSize.Level1`: Basic test - Common input scenarios (most commonly used)
  - `TestSize.Level2`: Main test - Common + error scenarios
  - `TestSize.Level3`: Regular test - All functionality
  - `TestSize.Level4`: Rare test - Extreme scenarios

### Test Case Annotation Specification

Each test case must contain the following annotations:

```cpp
/**
 * @tc.name: TestCaseName_Number
 * @tc.desc: Test case description
 * @tc.type: FUNC (functional test) / PERF (performance test)
 */
```

Example:
```cpp
/**
 * @tc.name: SceneETS_Load_001
 * @tc.desc: Test SceneETS::Load with empty path
 * @tc.type: FUNC
 */
HWTEST_F(SceneETSUnitTest, SceneETS_Load_001, TestSize.Level1)
{
    // Test code
}
```

---

## Developing New Test Cases

### Step 1: Create Test File

Create a new test file in the `api_unit_test/` directory, such as `material_ets_unit_test.cpp`.

### Step 2: Include Necessary Header Files

```cpp
#include <gtest/gtest.h>
#include <memory>

#include "common/ets_test.h"
#include "MaterialETS.h"  // Header file being tested
```

### Step 3: Define Test Class

```cpp
using namespace testing;
using namespace testing::ext;

namespace OHOS::Render3D {

class MaterialETSUnitTest : public EtsTest {
    // Can add additional member variables or methods
};

} // namespace OHOS::Render3D
```

### Step 4: Write Test Cases

```cpp
/**
 * @tc.name: MaterialETS_Create_001
 * @tc.desc: Test MaterialETS creation and initialization
 * @tc.type: FUNC
 */
HWTEST_F(MaterialETSUnitTest, MaterialETS_Create_001, TestSize.Level1)
{
    // Arrange (Prepare)
    auto material = std::make_shared<MaterialETS>();

    // Act (Execute)
    bool result = material->IsValid();

    // Assert (Verify)
    EXPECT_TRUE(result);
}

/**
 * @tc.name: MaterialETS_SetProperty_001
 * @tc.desc: Test setting material properties
 * @tc.type: FUNC
 */
HWTEST_F(MaterialETSUnitTest, MaterialETS_SetProperty_001, TestSize.Level1)
{
    auto material = std::make_shared<MaterialETS>();

    // Test property setting
    material->SetAlbedoColor(1.0f, 0.0f, 0.0f); // Red color
    EXPECT_EQ(material->GetAlbedoColor(), Color(1.0f, 0.0f, 0.0f));
}
```

### Step 5: Update BUILD.gn

Add new file to the `sources` list in `BUILD.gn`:

```gni
sources = [
    "common/ets_test.cpp",
    "api_unit_test/scene_ets_unit_test.cpp",
    "api_unit_test/material_ets_unit_test.cpp",  # New
]
```

### Step 6: Build and Run Tests

```bash
# Rebuild
hb build graphic_3d_kits_ets_test_unittest

# Run tests (refer to "Running Tests" section)
```

---

## Best Practices

### 1. Naming Conventions

- **Test class name**: `<ModuleName>ETSUnitTest`, e.g., `MaterialETSUnitTest`
- **Test case name**: `<ClassName>_<MethodName>_<Number>`, e.g., `MaterialETS_Create_001`
- **File name**: `<module>_ets_unit_test.cpp`, e.g., `material_ets_unit_test.cpp`

### 2. Test Organization

- Each test class focuses on one API module
- Related test cases are placed in the same test class
- Test cases are grouped by function, distinguished by number

### 3. Assertion Usage

```cpp
// Boolean assertions
EXPECT_TRUE(condition);
EXPECT_FALSE(condition);

// Equality assertions
EXPECT_EQ(expected, actual);
ASSERT_EQ(expected, actual);  // Stops immediately after failure

// Pointer assertions
EXPECT_NE(nullptr, pointer);
EXPECT_NULL(pointer);

// Floating-point comparisons
EXPECT_FLOAT_EQ(expected, actual);
EXPECT_NEAR(val1, val2, abs_error);
```

### 4. Test Isolation

- Each test case should run independently
- Do not rely on the execution order of test cases
- Use `SetUp()` and `TearDown()` to ensure proper resource initialization and cleanup

### 5. Error Handling

```cpp
HWTEST_F(SceneETSUnitTest, SceneETS_Load_InvalidPath_001, TestSize.Level1)
{
    auto sceneETS = std::make_shared<SceneETS>();
    bool result = sceneETS->Load("/invalid/path");

    // Test error handling
    EXPECT_FALSE(result);
}
```

### 6. Performance Testing

For scenarios requiring performance validation, use `TestSize.Level2` or `TestSize.Level3`:

```cpp
/**
 * @tc.name: SceneETS_Load_LargeModel_001
 * @tc.desc: Test loading large model performance
 * @tc.type: PERF
 */
HWTEST_F(SceneETSUnitTest, SceneETS_Load_LargeModel_001, TestSize.Level2)
{
    auto start = std::chrono::high_resolution_clock::now();

    auto sceneETS = std::make_shared<SceneETS>();
    sceneETS->Load("/data/large_model.glb");

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    EXPECT_LT(duration.count(), 1000); // Expected to complete within 1 second
}
```

---

## Common Issues

### Q1: Compilation reports header file not found

**Cause**: Header file path configuration is incorrect or missing dependencies

**Solution**:
1. Check if `include_dirs` in `BUILD.gn` includes required paths
2. Confirm that related modules are correctly compiled and export header files

### Q2: Runtime reports shared library not found

**Cause**: Dynamic library path is not correctly set

**Solution**:
1. Confirm that `libAGPDLL.z.so` and other library files are deployed to device
2. Check if path macros defined during compilation match device paths

### Q3: Test case passes but engine crashes

**Cause**: Resources not properly released or thread synchronization issues

**Solution**:
1. Check if all resources are properly released before `TearDown()`
2. Ensure tasks in task queue are completed (refer to `ets_test.cpp:195`)

### Q4: How to debug test cases

**Solution**:
1. Use logging: `#include <hilog/log.h>`
   ```cpp
   OH_LOG_Print(LOG_APP, LOG_INFO, 0xFF00, "Test", "Debug info: %{public}s", info);
   ```
2. Use GDB on device:
   ```bash
   hdc shell /data/local/tmp/SceneETSUnitTest --gtest_filter=SceneETSUnitTest.SceneETS_Load_001
   ```

### Q5: How to run specific tests only

**Solution**:
Use `--gtest_filter` parameter:
```bash
# Run specific test class
hdc shell /data/local/tmp/SceneETSUnitTest --gtest_filter=SceneETSUnitTest.*

# Run specific test case
hdc shell /data/local/tmp/SceneETSUnitTest --gtest_filter=SceneETSUnitTest.SceneETS_Load_001

# Run multiple test cases
hdc shell /data/local/tmp/SceneETSUnitTest --gtest_filter=*Load_001:*Load_002
```

### Q6: How to add new compilation macro definitions

Add in `BUILD.gn`:
```gni
defines = [
    "NEW_DEFINE=1",
    "STRING_DEFINE=\"value\"",
]
```

---

## Reference Resources

- [GTest Documentation](https://google.github.io/googletest/)
- [OpenHarmony Test Specification](https://gitcode.com/openharmony/testfwk_developer_test)
- [AGP Engine Documentation](../README.md)
- [GN Build System](https://gn.googlesource.com/gn/)

---

## Appendix: Complete BUILD.gn Template

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

ohos_unittest("SceneETSUnitTest") {
  module_out_path = module_output_path

  include_dirs = [
    ".",
    "//foundation/graphic/graphic_3d/kits/ets/include",
    "//foundation/graphic/graphic_3d/kits/ets/include/property_proxy",
    "//foundation/graphic/graphic_3d/kits/ets/include/geometry_definition",
    "${LUME_BASE_PATH}/api",
    "${LUME_CORE_PATH}/api",
    "${LUME_RENDER_PATH}/api",
    "${LUME_CORE3D_PATH}/api",
  ]

  cflags = [
    "-g",
    "-O0",
    "-Wno-unused-variable",
    "-fno-omit-frame-pointer",
  ]

  sources = [
    "common/ets_test.cpp",
    "api_unit_test/scene_ets_unit_test.cpp",
    # Add new test files here
  ]

  defines = [
    "CORE_HAS_GLES_BACKEND=1",
    "CORE_HAS_VULKAN_BACKEND=1",
    "LIB_ENGINE_CORE=\"libAGPDLL.z.so\"",
  ]

  configs = [
    "//foundation/graphic/graphic_3d/kits/ets:lume3d_config",
  ]

  deps = [
    "//foundation/graphic/graphic_3d/3d_widget_adapter:lib3dWidgetAdapter",
    "//foundation/graphic/graphic_3d/kits/ets:scene_ani",
  ]

  external_deps = [
    "ability_runtime:napi_base_context",
    "c_utils:utils",
    "googletest:gmock",
    "googletest:gtest",
    "hilog:libhilog",
    "napi:ace_napi",
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