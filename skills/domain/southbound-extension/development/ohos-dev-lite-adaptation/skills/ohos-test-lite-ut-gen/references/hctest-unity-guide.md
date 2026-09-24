# OpenHarmony Lite 测试框架使用指南

> 本指南面向 OpenHarmony Lite（L0轻量系统 + L1小型系统）开发者，介绍如何在MCU/MPU环境中使用HCTest、iCunit和HWTest框架编写和执行驱动测试。

---

## 1. 框架总览

### 1.1 三套框架的关系

OpenHarmony Lite 测试涉及三套框架，分别服务不同系统层级：

| 框架 | 系统层级 | 语言 | 角色 | RAM开销 |
|------|---------|------|------|---------|
| **HCTest** | L0/L1 | C | 测试结构框架（套件/用例注册与调度） | ~2-4KB |
| **iCunit** | L0 | C | 断言引擎（`ICUNIT_ASSERT_*` 系列宏） | ~1KB |
| **Unity** | L0/L1 | C | 断言引擎（`TEST_ASSERT_*` 系列宏，HCTest内置） | ~2KB |
| **HWTest** | L1-Linux | C++ | 完整测试框架（`HWTEST_F` 宏 = gtest `TEST_F` + 标签注册） | ~64KB+ |

> ⚠️ **关键认知：L0存在两种断言体系的混合使用**
>
> - **HCTest提供结构**：`LITE_TEST_SUIT` / `LITE_TEST_CASE` / `RUN_TEST_SUITE`
> - **iCunit提供断言**：`ICUNIT_ASSERT_EQUAL` / `ICUNIT_ASSERT_NOT_EQUAL` 等
> - **Unity也提供断言**：`TEST_ASSERT_EQUAL_INT32` 等（HCTest内置Unity）
>
> 实际代码中，L0测试通常采用 **HCTest结构 + iCunit断言** 的混合模式（见第3节），也可使用纯Unity断言。

### 1.2 框架选择决策

| 维度 | L0轻量系统（MCU） | L1小型系统（MPU） |
|------|------------------|------------------|
| **内核** | LiteOS-M | LiteOS-A / Linux（L1-Linux 路线，kernel_family=linux） |
| **语言** | 纯C | C++（也支持C） |
| **推荐框架** | HCTest + iCunit（混合模式） | L1-Linux → HWTest（HWTEST_F + gtest断言）；L1-LiteOS-A 按平台 acts 范式确认 |
| **最小RAM** | HCTest: ~2KB | HWTest: ~64KB |
| **C++依赖** | 不需要 | 需要（gtest引擎） |
| **Mock支持** | 手动桩函数 | gmock完整支持 |
| **测试标签** | `Function \| MediumTest \| Level1` | `TestSize.Level0` |

### 1.3 三种测试写法对比

```
L0 混合模式（HCTest结构 + iCunit断言）     L0 纯Unity模式                L1-Linux HWTest模式
─────────────────────────────────────    ──────────────────────         ──────────────────────────
LITE_TEST_SUIT(Posix,Pthread,Suite);    void RunTests(void) {          class GpioTest : testing::Test {};
LITE_TEST_CASE(Suite, test001,            RUN_TEST(TestGpioOpen);
    Function|MediumTest|Level1) {         RUN_TEST(TestGpioClose);     HWTEST_F(GpioTest, TestOpen,
    int ret = GpioOpen(5);              }                                TestSize.Level0) {
    ICUNIT_ASSERT_EQUAL(ret, 0, ret);                                    int ret = GpioOpen(5);
}                                       static void TestGpioOpen(void) {  EXPECT_EQ(0, ret);
RUN_TEST_SUITE(Suite);                    int ret = GpioOpen(5);       }
                                          TEST_ASSERT_EQUAL_INT32(0,ret);
                                        }
```

---

## 2. HCTest 核心API

### 2.1 头文件引入

```c
#include "hctest.h"
```

`hctest.h` 内部引入了 `unity.h`，因此可以直接使用 Unity 的全部断言宏。

### 2.2 HCTest 套件注册宏

HCTest 提供三个核心宏，用于定义测试套件、用例和运行入口：

| 宏 | 作用 | 参数 |
|----|------|------|
| `LITE_TEST_SUIT(subsystem, module, suite_name)` | 声明并注册一个测试套件 | 子系统名、模块名、套件名（均为标识符，非字符串） |
| `LITE_TEST_CASE(suite_name, case_name, test_flag)` | 定义一个测试用例函数 | 套件名、用例名、测试标签（位域OR组合） |
| `RUN_TEST_SUITE(suite_name)` | 注册套件运行入口（系统启动时自动执行） | 套件名 |

**测试标签**（可位域OR组合）：

| 标签 | 含义 |
|------|------|
| `Function` | 功能测试 |
| `MediumTest` | 中等规模 |
| `Level1` ~ `Level4` | 测试优先级等级 |

### 2.3 Unity 断言宏（HCTest内置）

HCTest 内置了 Unity 断言引擎，以下是最常用的宏：

| 断言宏 | 说明 | 示例 |
|--------|------|------|
| `TEST_ASSERT_EQUAL_INT32(expected, actual)` | 验证int32_t相等 | `TEST_ASSERT_EQUAL_INT32(0, ret)` |
| `TEST_ASSERT_EQUAL_UINT8(expected, actual)` | 验证uint8_t相等 | `TEST_ASSERT_EQUAL_UINT8(1, val)` |
| `TEST_ASSERT_EQUAL_UINT32(expected, actual)` | 验证uint32_t相等 | `TEST_ASSERT_EQUAL_UINT32(100000, freq)` |
| `TEST_ASSERT_NOT_EQUAL(expected, actual)` | 验证不相等 | `TEST_ASSERT_NOT_EQUAL(0, ret)` |
| `TEST_ASSERT_TRUE(condition)` | 验证条件为真 | `TEST_ASSERT_TRUE(val == 0 \|\| val == 1)` |
| `TEST_ASSERT_FALSE(condition)` | 验证条件为假 | `TEST_ASSERT_FALSE(ptr == NULL)` |
| `TEST_ASSERT_NULL(pointer)` | 验证指针为NULL | `TEST_ASSERT_NULL(handle)` |
| `TEST_ASSERT_NOT_NULL(pointer)` | 验证指针非NULL | `TEST_ASSERT_NOT_NULL(handle)` |
| `TEST_ASSERT_GREATER_THAN(threshold, actual)` | 验证大于阈值 | `TEST_ASSERT_GREATER_THAN(0, readLen)` |
| `TEST_ASSERT_UINT32_WITHIN(delta, expected, actual)` | 验证在误差范围内 | `TEST_ASSERT_UINT32_WITHIN(5, 100, elapsed)` |

> Unity 提供 380+ 个 `TEST_ASSERT_*` 宏，完整列表见 `resources/unity-framework/src/unity.h`。

---

## 3. iCunit 断言引擎与混合模式（L0）

### 3.1 iCunit 概述

iCunit 是 LiteOS-M 内核自带的 C 单元测试框架，在 OpenHarmony Lite 测试中主要作为**断言引擎**使用，与 HCTest 的套件结构配合形成混合模式。

```c
#include "iCunit.h"     // 或直接包含 osTest.h（osTest.h 已包含 iCunit.h）
```

### 3.2 iCunit 断言宏

| 断言宏 | 返回值 | 说明 |
|--------|--------|------|
| `ICUNIT_ASSERT_EQUAL(param, value, retcode)` | `return 1`（失败时） | 验证相等，失败则记录错误行号并返回1 |
| `ICUNIT_ASSERT_NOT_EQUAL(param, value, retcode)` | `return 1` | 验证不相等 |
| `ICUNIT_ASSERT_EQUAL_VOID(param, value, retcode)` | `return`（失败时） | 验证相等，失败时返回void（用于void函数） |
| `ICUNIT_ASSERT_NOT_EQUAL_VOID(param, value, retcode)` | `return` | 验证不相等，void版 |
| `ICUNIT_ASSERT_WITHIN_EQUAL(param, min, max, retcode)` | `return 1` | 验证在范围内 |
| `ICUNIT_ASSERT_WITHIN_EQUAL_VOID(param, min, max, retcode)` | `return` | 范围验证，void版 |
| `ICUNIT_ASSERT_STRING_EQUAL(str1, str2, retcode)` | `return 1` | 字符串相等（strcmp） |
| `ICUNIT_ASSERT_STRING_NOT_EQUAL(str1, str2, retcode)` | `return 1` | 字符串不相等 |
| `ICUNIT_ASSERT_SIZE_STRING_EQUAL(str1, str2, size, retcode)` | `return 1` | 定长字符串比较（strncmp） |
| `ICUNIT_GOTO_EQUAL(param, value, retcode, label)` | `goto label` | 验证相等，失败跳转到label |
| `ICUNIT_GOTO_NOT_EQUAL(param, value, retcode, label)` | `goto label` | 验证不相等，失败跳转 |
| `ICUNIT_TRACK_EQUAL(param, value, retcode)` | 无（仅记录） | 验证相等，仅记录不返回 |
| `ICUNIT_TRACK_NOT_EQUAL(param, value, retcode)` | 无（仅记录） | 验证不相等，仅记录 |

### 3.3 iCunit 与 Unity 断言对比

| 维度 | iCunit (`ICUNIT_ASSERT_*`) | Unity (`TEST_ASSERT_*`) |
|------|---------------------------|------------------------|
| **失败行为** | 记录 `__LINE__` + retcode，`return 1` | 记录失败，`TEST_FAIL()` |
| **错误信息** | `[Failed]-caseID-[Errline: %d RetCode:0x%lx]` | `FAIL: Expected X Was Y` |
| **void函数支持** | `*_VOID` 后缀宏（`return;`） | `TEST_ASSERT_*` 不返回（但也不return） |
| **goto支持** | `ICUNIT_GOTO_*` 宏 | 无 |
| **类型安全** | 参数为 `unsigned long`，无类型检查 | 有 `INT32`/`UINT8`/`UINT32` 类型区分 |
| **适用场景** | L0内核测试、XTS兼容性测试 | 通用单元测试 |

### 3.4 混合模式：HCTest + iCunit（L0主流写法）

这是 OpenHarmony Lite 官方测试代码（kernel_liteos_m testsuites）中最常见的模式：

```c
#include "hctest.h"          /* HCTest 套件结构 */
#include "cmsis_os2.h"       /* 被测接口 */

/* 1. 声明测试套件 */
LITE_TEST_SUIT(Cmsis, Cmsistask, CmsisTaskFuncTestSuite);

/* 2. 套件级 SetUp / TearDown */
static BOOL CmsisTaskFuncTestSuiteSetUp(void) {
    return TRUE;
}
static BOOL CmsisTaskFuncTestSuiteTearDown(void) {
    return TRUE;
}

/* 3. 定义测试用例 — HCTest结构 + iCunit断言 */
LITE_TEST_CASE(CmsisTaskFuncTestSuite, testOsThreadNew001,
               Function | MediumTest | Level1) {
    osThreadId_t id = osThreadNew(threadFunc, NULL, &attr);
    ICUNIT_ASSERT_NOT_EQUAL(id, NULL, id);        /* ← iCunit断言 */

    osStatus_t status = osThreadTerminate(id);
    ICUNIT_ASSERT_EQUAL(status, osOK, status);     /* ← iCunit断言 */
}

/* 4. 注册运行入口 */
RUN_TEST_SUITE(CmsisTaskFuncTestSuite);
```

**为什么混合使用？**
- `LITE_TEST_CASE` 宏将用例注册到 HCTest 的 `TestSuiteManager`，由系统启动时自动调度执行
- `ICUNIT_ASSERT_EQUAL` 宏在失败时记录行号和错误码，格式为 `[Failed]-caseID-[Errline: %d RetCode:0x%lx]`
- HCTest 的 `RUN_TEST_SUITE` 在 `OHOS_SystemInit()` 后自动触发，无需手动创建任务

### 3.5 混合模式中的注意事项

| 注意项 | 说明 |
|--------|------|
| **ICUNIT_ASSERT_EQUAL 的第三个参数** | 是 `retcode`（错误码），不是 message。失败时以十六进制输出 |
| **`_VOID` 后缀** | 在 `void` 返回类型的函数中使用 `ICUNIT_ASSERT_EQUAL_VOID`，否则编译报错 |
| **SetUp/TearDown** | 套件级 SetUp 函数命名规则：`{SuiteName}SetUp`，返回 `BOOL` |
| **不要混用断言** | 同一测试函数内不要混用 iCunit 和 Unity 断言，失败行为不同 |

---

## 4. HWTest 框架（L1-Linux）

### 4.1 框架定位

HWTest 是 OpenHarmony L1 小型系统的测试框架，基于 Google Test (gtest) 引擎，通过 `HWTEST_F` 宏扩展了测试标签注册能力（本包实证于 L1-Linux 路线；L1-LiteOS-A 可用性按平台确认）。

```cpp
#include <gtest/gtest.h>          // gtest 引擎
#include <gtest/hwext/gtest-ext.h> // HWTEST_F 扩展宏（通常通过 gtest.h 间接引入）
```

### 4.2 HWTEST_F 宏

```cpp
// HWTEST_F = regist(test_flags) + TEST_F(test_case_name, test_name)
#define HWTEST_F(test_case_name, test_name, test_flags) \
    bool GTEST_TEST_UNIQUE_ID_(test_case_name, test_name, __LINE__) = \
        testing::ext::TestDefManager::instance()->regist( \
            #test_case_name, #test_name, test_flags, testing::ext::Fixtured); \
    TEST_F(test_case_name, test_name)
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `test_case_name` | 测试套件类名（继承 `testing::Test`） | `GpioTest` |
| `test_name` | 用例名 | `TestGpioOpenClose` |
| `test_flags` | 测试等级标签 | `TestSize.Level0` |

**测试等级标签**：

| 标签 | 含义 | 对应 L0 标签 |
|------|------|-------------|
| `TestSize.Level0` | 冒烟测试（最核心） | `Level1` |
| `TestSize.Level1` | 基础功能测试 | `Level2` |
| `TestSize.Level2` | 扩展功能测试 | `Level3` |
| `TestSize.Level3` | 全量测试 | `Level4` |
| `TestSize.Level4` | 压力/性能测试 | 无对应 |

### 4.3 gtest 常用断言

| 断言 | 说明 | 对应 iCunit | 对应 Unity |
|------|------|------------|-----------|
| `EXPECT_EQ(expected, actual)` | 相等（非致命） | `ICUNIT_ASSERT_EQUAL` | `TEST_ASSERT_EQUAL_INT32` |
| `ASSERT_EQ(expected, actual)` | 相等（致命，终止当前用例） | `ICUNIT_ASSERT_EQUAL` | `TEST_ASSERT_EQUAL_INT32` |
| `EXPECT_NE(val1, val2)` | 不相等 | `ICUNIT_ASSERT_NOT_EQUAL` | `TEST_ASSERT_NOT_EQUAL` |
| `EXPECT_TRUE(condition)` | 条件为真 | — | `TEST_ASSERT_TRUE` |
| `EXPECT_FALSE(condition)` | 条件为假 | — | `TEST_ASSERT_FALSE` |
| `EXPECT_NULL(ptr)` | 指针为空 | — | `TEST_ASSERT_NULL` |
| `EXPECT_NOT_NULL(ptr)` | 指针非空 | — | `TEST_ASSERT_NOT_NULL` |
| `EXPECT_GT(val1, val2)` | 大于 | — | `TEST_ASSERT_GREATER_THAN` |
| `EXPECT_NEAR(val1, val2, abs_error)` | 近似相等 | `ICUNIT_ASSERT_WITHIN_EQUAL` | `TEST_ASSERT_UINT32_WITHIN` |

> **EXPECT_ vs ASSERT_**：`EXPECT_` 失败后继续执行后续断言；`ASSERT_` 失败后立即终止当前用例。L1驱动测试推荐使用 `EXPECT_`。

### 4.4 HWTest 标准写法

```cpp
#include <gtest/gtest.h>
#include "gpio_if.h"

using namespace testing::ext;

namespace OHOS {

class GpioTest : public testing::Test {
public:
    static void SetUpTestCase(void) {
        // 套件级初始化（仅执行一次）
    }
    static void TearDownTestCase(void) {
        // 套件级清理（仅执行一次）
    }
    void SetUp() override {
        // 每个用例前的初始化
    }
    void TearDown() override {
        // 每个用例后的清理
    }
};

/**
 * @tc.name: GpioTestOpenClose
 * @tc.desc: 验证GPIO正常打开和关闭
 * @tc.type: FUNC
 */
HWTEST_F(GpioTest, TestGpioOpenClose, TestSize.Level0)
{
    int32_t ret = GpioOpen(5);
    EXPECT_EQ(0, ret);

    ret = GpioClose(5);
    EXPECT_EQ(0, ret);
}

/**
 * @tc.name: GpioTestInvalidPin
 * @tc.desc: 验证无效引脚号返回错误
 * @tc.type: FUNC
 */
HWTEST_F(GpioTest, TestGpioInvalidPin, TestSize.Level0)
{
    int32_t ret = GpioOpen(999);
    EXPECT_NE(0, ret);
}

} // namespace OHOS
```

### 4.5 HWTest 条件编译

L1 测试使用条件编译控制测试范围：

```cpp
#if defined(LOSCFG_USER_TEST_SMOKE)    // 仅冒烟测试
HWTEST_F(GpioTest, TestBasic, TestSize.Level0) { ... }
#endif

#if defined(LOSCFG_USER_TEST_FULL)     // 冒烟 + 完整测试
HWTEST_F(GpioTest, TestAdvanced, TestSize.Level1) { ... }
#endif

#if defined(LOSCFG_USER_TEST_PRESSURE) // 压力测试
HWTEST_F(GpioTest, TestStress, TestSize.Level4) { ... }
#endif
```

---

## 5. 测试输出格式

### 5.1 HCTest 输出格式（L0）

HCTest 基于 Unity 引擎输出，格式为：

```
Start to run test suite:CmsisTaskFuncTestSuite
CmsisTaskFuncTestSuite::testOsThreadNew001:PASS
CmsisTaskFuncTestSuite::testOsThreadNew002:PASS
CmsisTaskFuncTestSuite::testOsThreadGetId001:FAIL
-----------------------
14 Tests 1 Failures 0 Ignored
```

**失败详情**（Unity 格式）：
```
  testOsThreadGetId001 cmsis_task_func_test.c:156
  :FAIL: Expected 0 Was 1
```

### 5.2 iCunit 输出格式（L0混合模式）

当使用 iCunit 断言时，失败输出格式为：

```
[Passed]-testOsThreadNew001
[Failed]-testOsThreadGetId001-[Errline: 156 RetCode:0x1]
```

### 5.3 HWTest 输出格式（L1-Linux）

HWTest 基于 gtest 引擎，格式为：

```
[==========] Running 5 tests from 1 test suite.
[----------] Global test environment set-up.
[----------] 5 tests from GpioTest
[ RUN      ] GpioTest.TestGpioOpenClose
[       OK ] GpioTest.TestGpioOpenClose (2 ms)
[ RUN      ] GpioTest.TestGpioInvalidPin
[       OK ] GpioTest.TestGpioInvalidPin (1 ms)
[----------] 5 tests from GpioTest (10 ms total)
[==========] 5 tests from 1 test suite ran. (10 ms total)
[  PASSED  ] 5 tests.
```

---

## 6. 测试任务创建与运行

### 6.1 L0 自动运行机制（推荐）

使用 `LITE_TEST_SUIT` + `RUN_TEST_SUITE` 宏注册的测试套件，会在 `OHOS_SystemInit()` 完成后**自动运行**，无需手动创建任务：

```c
/* 只需这三个宏，测试会在系统启动后自动执行 */
LITE_TEST_SUIT(Cmsis, Cmsistask, CmsisTaskFuncTestSuite);
LITE_TEST_CASE(CmsisTaskFuncTestSuite, test001, Function | MediumTest | Level1) { ... }
RUN_TEST_SUITE(CmsisTaskFuncTestSuite);
```

> ⚠️ 前提：在 `config.json` 中配置了 XTS 子系统，或在链接选项中链接了 `-lhctest -lbootstrap -lbroadcast`。

### 6.2 L0 手动创建测试任务（备选）

对于不使用 XTS 框架的独立测试，需要手动创建 LiteOS-M 任务：

```c
#include "hctest.h"
#include "los_task.h"

extern void RunGpioTests(void);
extern void RunI2cTests(void);

static void TestTaskEntry(void) {
    printf("\n========================================\n");
    printf("  OpenHarmony Lite Driver Test Suite\n");
    printf("========================================\n\n");

    RunGpioTests();
    RunI2cTests();

    printf("\n  All tests completed.\n");
}

void TestMain(void) {
    TSK_INIT_PARAM_S taskAttr = {0};
    taskAttr.pfnTaskEntry = (TSK_ENTRY_FUNC)TestTaskEntry;
    taskAttr.uwStackSize = 4096;
    taskAttr.pcName = "TestTask";
    taskAttr.usTaskPrio = 10;

    uint32_t taskId;
    LOS_TaskCreate(&taskId, &taskAttr);
}
```

### 6.3 栈大小建议

| 测试复杂度 | 建议栈大小 | 说明 |
|-----------|-----------|------|
| 简单接口测试 | 2KB | 仅基础断言 |
| 含缓冲区操作 | 4KB | 包含局部数组 |
| 复杂集成测试 | 8KB | 多层调用+大缓冲 |
| 含CMSIS测试 | 4-8KB | CMSIS API可能有较大栈消耗 |

---

## 7. BUILD.gn 编译配置模板

### 7.1 L0 HCTest 标准模板

```gn
import("//build/lite/config/component/lite_component.gni")

lite_component("{{test_target_name}}") {
  features = [
    ":{{test_target_name}}_bin",
  ]
}

executable("{{test_target_name}}_bin") {
  sources = [
    "{{TEST_SOURCE_FILE}}",
  ]

  include_dirs = [
    "//kernel/liteos_m/kal/cmsis",
    "//drivers/lite/include",
    "//device/soc/{{VENDOR}}/{{CHIP}}/include",
    "//foundation/lite/interfaces/kits",
    "//test/xts/acts/kernel_lite/kernelcmsis_hal",
  ]

  deps = [
    "//drivers/lite/{{PERIPHERAL_TYPE}}:{{peripheral_lib}}",
    "//kernel/liteos_m:liteos_m",
  ]

  cflags = [
    "-Os",
    "-ffunction-sections",
    "-fdata-sections",
  ]
  ldflags = [ "-Wl,--gc-sections" ]
}
```

### 7.2 L0 XTS 集成方式

如果测试要作为 XTS 兼容性测试套件运行，需在 `vendor/xxx/xxx/config.json` 中添加：

```json
{
  "subsystem": "test",
  "components": [
    { "component": "xts_acts", "features": [] },
    { "component": "xts_tools", "features": [] }
  ]
}
```

链接选项中必须包含（在 `-Wl,--whole-archive` 和 `-Wl,--no-whole-archive` 之间）：

```
"-lhctest",
"-lbootstrap",
"-lbroadcast",
"-lmodule_ActsXxxTest",   // 你的测试模块
```

### 7.3 L1-Linux HWTest 标准模板

```gn
import("//build/lite/config/component/lite_component.gni")

local_flags = [
  "-fpermissive",
  "-O2",
  "-fbuiltin",
  "-Wno-narrowing",
  "-fPIE",
  "-Wno-error",
]

config("public_config_for_smoke") {
  cflags = [ "-DLOSCFG_USER_TEST_SMOKE" ]
  cflags += local_flags
  cflags_cc = cflags
}

config("public_config_for_all") {
  cflags = [
    "-DLOSCFG_USER_TEST_SMOKE",
    "-DLOSCFG_USER_TEST_FULL",
  ]
  cflags += local_flags
  cflags_cc = cflags
}

executable("{{test_target_name}}") {
  sources = [
    "{{TEST_SOURCE_FILE}}",
  ]

  configs = [ ":public_config_for_smoke" ]

  include_dirs = [
    "//kernel/liteos_a/utils",
    "//kernel/liteos_a/testsuites/include",
    "//test/xts/acts/startup_lite/syspara_hal",
  ]

  deps = [
    "//kernel/liteos_a:liteos_a",
  ]

  cflags_cc = [ "-std=c++14" ]
}
```

---

## 8. 测试覆盖率目标

| 指标 | 定义 | 最低目标 | 推荐目标 |
|------|------|---------|---------|
| **行覆盖率** | 被执行到的代码行数 / 总代码行数 | ≥ 70% | ≥ 85% |
| **接口覆盖率** | 被测试的接口数 / 总接口数 | 100% | 100% |
| **错误码覆盖率** | 被触发的错误码 / 定义的总错误码 | ≥ 60% | ≥ 80% |
| **边界值覆盖率** | 被测试的边界点 / 识别的总边界点 | ≥ 70% | ≥ 90% |
| **RAM开销** | 测试框架额外占用的RAM | ≤ 4KB（L0） | ≤ 2KB（L0） |

> ⚠️ **注意**：L0系统上的代码覆盖率采集较为困难（gcov需要额外的RAM和文件系统支持）。建议在开发机上使用QEMU或主机编译模式进行覆盖率采集，真机上仅执行功能验证。

---

## 9. 测试类型全景

### 9.1 测试金字塔

```
┌─────────────────────────────────────────────────────┐
│          OpenHarmony Lite 驱动测试金字塔              │
│                                                     │
│                    ┌───────┐                         │
│                   │ 验收测试 │  ← CMSIS/HAL兼容性     │
│                  ┌┴───────┴┐                        │
│                 │  集成测试   │ ← 驱动+IoT子系统联调   │
│                ┌┴─────────┴┐                        │
│               │  单元测试     │ ← HCTest / HWTest     │
│              ┌┴───────────┴┐                        │
│             │  性能/压力测试  │ ← 自定义benchmark      │
│            └───────────────┘                        │
└─────────────────────────────────────────────────────┘
```

### 9.2 各测试类型详情

| 测试类型 | 目标 | L0框架 | L1-Linux框架 | 执行环境 |
|---------|------|--------|--------|---------|
| **单元测试** | 验证单个函数逻辑 | HCTest+iCunit | HWTest | MCU/MPU真机 |
| **集成测试** | 验证驱动与子系统交互 | HCTest+iCunit | HWTest | 真机 |
| **兼容性测试** | 验证CMSIS/HAL接口合规 | HCTest+iCunit | HWTest | 真机 |
| **性能测试** | 测量延迟、吞吐量 | 自定义+HCTest | 自定义+HWTest | 真机 |
| **压力测试** | 高负载稳定性 | 自定义 | HWTEST_F Level4 | 真机 |

---

## 10. 测试生成策略引擎

### 10.1 策略分类

```
测试生成策略（Lite版）
├── 正向测试策略 (Positive Test)
│   ├── 基本功能验证：每个HAL接口的正常调用路径
│   ├── 参数遍历：有效参数的组合覆盖
│   └── 序列测试：按生命周期顺序的完整业务流程
├── 边界测试策略 (Boundary Test)
│   ├── 数值边界：最小值、最大值、临界值±1
│   ├── 引脚号边界：0、最大引脚号、超出范围
│   └── 缓冲区边界：空缓冲、满缓冲
├── 异常测试策略 (Negative Test)
│   ├── 空指针传入
│   ├── 无效参数值
│   ├── 未初始化状态调用
│   ├── 重复操作（双重打开、双重关闭）
│   └── 资源耗尽模拟
├── 中断安全测试策略 (ISR Safety Test)
│   ├── ISR中调用非ISR-safe接口检测
│   ├── ISR与任务间共享数据保护验证
│   └── 中断嵌套场景
├── 低功耗测试策略 (Low Power Test)
│   ├── Sleep模式下驱动状态保持
│   ├── Stop模式下唤醒后驱动恢复
│   └── 低功耗进出时的驱动行为
└── CMSIS兼容性测试策略 (CMSIS Compatibility) [仅L0]
    ├── CMSIS-RTOS2接口一致性
    ├── CMSIS-Driver接口一致性
    └── POSIX接口一致性
```

### 10.2 接口元数据提取格式

从驱动源码和HAL头文件中提取的结构化信息：

```json
{
  "driver_name": "hi3861_gpio",
  "hal_interface": "gpio_if.h",
  "system_level": "L0",
  "target_chip": "Hi3861",
  "test_pattern": "hybrid_hctest_icunit",
  "methods": [
    {
      "name": "GpioSetDir",
      "return_type": "int32_t",
      "params": [
        {"name": "pin", "type": "uint16_t", "constraints": "0-21 for Hi3861"},
        {"name": "dir", "type": "enum GpioDir", "valid_values": ["GPIO_DIR_IN", "GPIO_DIR_OUT"]}
      ],
      "error_codes": ["0 (success)", "-1 (invalid param)", "-2 (not init)"],
      "preconditions": ["GPIO已初始化", "pin在有效范围内"],
      "postconditions": ["GPIO方向已设置为指定值"],
      "isr_safe": false
    }
  ],
  "hardware_constraints": {
    "max_pins": 22,
    "supported_directions": ["IN", "OUT"],
    "pull_modes": ["NONE", "UP", "DOWN"],
    "ram_footprint_estimate": "256 bytes"
  }
}
```

### 10.3 L1 接口元数据扩展

```json
{
  "driver_name": "rk3568_gpio",
  "system_level": "L1",
  "test_pattern": "hwtest_gtest",
  "test_fixture_class": "GpioTest",
  "test_namespace": "OHOS",
  "compilation": {
    "language": "C++",
    "std": "c++14",
    "compile_flags": ["-DLOSCFG_USER_TEST_SMOKE"]
  }
}
```
