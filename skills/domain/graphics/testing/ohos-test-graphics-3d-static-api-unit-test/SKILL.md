---
name: ohos-test-graphics-3d-static-api-unit-test
description: "Generate unit tests for ETS/ArkTS static API wrapper classes (MaterialETS, CameraETS, SceneETS) in OpenHarmony graphic_3d module using HWTEST_F + EtsTest fixture. Do NOT use for Lume engine core testing or integration/performance tests (different frameworks). Trigger keywords: ETS unit test, HWTEST_F, EtsTest fixture, graphic_3d test, SceneETS test, MaterialETS test, CameraETS test, @tc.name annotation, Destroy() cleanup."
metadata:
  author: openharmony
  scope: domain
  stage: testing
  domain: graphics-3d
  capability: static-api-unit-test
  version: 0.2.0
  status: trial
---

# Graphics 3D API Unit Test Generator

## Test Strategy by ETS Wrapper Method Type

All ETS wrappers need full engine lifecycle (EtsTest SetUp provides it) and own engine resources that must be explicitly released.

| Method Type | Required Tests | Error Paths to Cover | Example |
|-------------|---------------|---------------------|---------|
| Constructor/Create | Creation + IsValid verification | null init, double create | `MaterialETS_Create_001` |
| Load/Import | Empty path + valid path + invalid path | empty path, null, non-existent file | `SceneETS_Load_001`, `SceneETS_Load_002` |
| Getter/SetProperty | Setter→Getter roundtrip | out-of-range values, null | `MaterialETS_SetProperty_001` |
| IsValid | Valid state + invalid state | before init, after destroy | `CameraETS_IsValid_001`, `CameraETS_IsValid_002` |
| Destroy | Resource cleanup after Destroy | double destroy, destroy without init | `SceneETS_Destroy_001` |

**Rule**: Every test case MUST call `Destroy()` on the ETS object before the test body ends. EtsTest TearDown handles engine-level cleanup, but per-object cleanup is your responsibility.

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Test class name | `<Module>ETSUnitTest` | `MaterialETSUnitTest` |
| Test case name | `<Class>_<Method>_<Number>` | `MaterialETS_Create_001` |
| Test file name | `<module>_ets_unit_test.cpp` | `material_ets_unit_test.cpp` |

## Complete Test Pattern

Based on actual `SceneETSUnitTest` in codebase. This example demonstrates all mandatory conventions — annotations, `HWTEST_F` macro (not `TEST()`), `EXPECT_*` (not `ASSERT_*`), `Destroy()` cleanup, and `OHOS::Render3D` namespace:

**Test Level Selection**:

| Level | When to Use | Examples |
|-------|------------|---------|
| `TestSize.Level1` | Normal/happy-path API tests: creation, valid operations, basic getters | `Create_001`, `IsValid_001`, `SetProperty_001` |
| `TestSize.Level2` | Error/edge-path tests: invalid input, failure scenarios, boundary conditions | `Load_002` (invalid path), `Destroy_002` (double destroy) |
| `TestSize.Level3` | Full coverage / stress tests: concurrent access, repeated operations, long-running scenarios | `Load_003` (repeated load/unload cycles) |

**Rule**: Default to `Level1`. Use `Level2` when the test verifies a failure or error path. Use `Level3` only for stress/edge cases beyond normal error handling.

```cpp
#include <gtest/gtest.h>
#include <memory>
#include "common/ets_test.h"
#include "SceneETS.h"

using namespace testing;
using namespace testing::ext;
namespace OHOS::Render3D {
class SceneETSUnitTest : public EtsTest {
};

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
} // namespace OHOS::Render3D
```

## NEVER Do This

| ❌ Wrong | ✅ Right | Reason |
|----------|----------|--------|
| `MaterialETS_Test` | `MaterialETSUnitTest` | OH requires `UnitTest` suffix |
| `MaterialETS_Create` | `MaterialETS_Create_001` | MUST include `_Number` suffix |
| Skip `@tc.name` | Always add annotation block | Missing breaks test discovery |
| Use `TEST()` macro | Use `HWTEST_F` | OH framework requires HWTEST_F |
| Skip `Destroy()` call | Always call `obj->Destroy()` | Unreleased engine resources crash subsequent tests |
| Assume engine persists | EtsTest SetUp/TearDown resets | Full engine lifecycle re-initialized per case |
| Use `ASSERT_*` in test body carelessly | Use `EXPECT_*` for non-critical checks | ASSERT stops test immediately, skips cleanup code before Destroy() |
| Forget namespace | Wrap in `OHOS::Render3D` | Tests must match production namespace |

## Implementation Workflow

1. **Create test file**: `api_unit_test/<module>_ets_unit_test.cpp`
2. **Write test cases**: Follow test strategy table above, always include `Destroy()`
3. **Update BUILD.gn**: Add file to `sources` list, add header `include_dirs` if needed

**For BUILD.gn details and environment setup**: See UNITTEST_GUIDE.md (load only when blocked or setting up new module).

## When to Load References

### ✅ Load UNITTEST_GUIDE.md when:

- Setting up **new test module** (first-time setup) → **MANDATORY**: Read ["Directory Structure"](references/UNITTEST_GUIDE.md#directory-structure) + ["EtsTest Base Class — Engine Lifecycle"](references/UNITTEST_GUIDE.md#etstest-base-class--engine-lifecycle) sections for engine lifecycle internals
- Need **complete BUILD.gn template** (copy-paste ready) → **MANDATORY**: Read ["Complete BUILD.gn Template"](references/UNITTEST_GUIDE.md#complete-buildgn-template) section completely. **Do NOT set any range limits when reading this file.**
- Troubleshooting **build/run errors** → Read ["BUILD.gn Configuration"](references/UNITTEST_GUIDE.md#buildgn-configuration) + ["Troubleshooting"](references/UNITTEST_GUIDE.md#troubleshooting) sections
- Need **EtsTest fixture implementation details** → Read ["EtsTest Base Class — Engine Lifecycle"](references/UNITTEST_GUIDE.md#etstest-base-class--engine-lifecycle) section for SetUp/TearDown lifecycle

### ❌ Do NOT Load when:

- **Quick test generation** (SKILL.md has all patterns needed)
- **Simple naming queries** (conventions in SKILL.md)
- **Familiar scenarios** (standard patterns known)

**Rule**: Start with SKILL.md. Load UNITTEST_GUIDE.md only when blocked or setting up new environment. Load specific sections, not the entire file.

**Link**: [UNITTEST_GUIDE.md](references/UNITTEST_GUIDE.md)

## Common Issues

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Header not found | Missing `include_dirs` in BUILD.gn | Add header path to `include_dirs` list |
| `libAGPDLL.z.so` not found | Engine library not deployed | Ensure library deployed to device `/system/lib64/` |
| Test passes but engine crashes | Skipped `Destroy()` or TearDown failure | Always call `Destroy()` before test ends |
| Platform path macros wrong | `target_cpu` mismatch in BUILD.gn | Check `arm` vs `arm64` conditional defines |
| Tests interfere with each other | Engine state leaking across cases | EtsTest TearDown resets full lifecycle — trust it |

## References

| Document | Description |
|----------|-------------|
| [UNITTEST_GUIDE.md](references/UNITTEST_GUIDE.md) | Complete BUILD.gn template, EtsTest internals, environment setup, troubleshooting Q&A |

## Evaluation Assets

When improving or validating this skill itself:

1. Start from [`evals/evals.json`](evals/evals.json).
2. See [`evals/README.md`](evals/README.md) for coverage map, success criteria, and benchmark workflow.
3. Keep qualitative review focused on whether the skill changes OpenHarmony-specific test decisions (annotations, HWTEST_F, Destroy(), namespace), not whether generic GTest output merely looks reasonable.
