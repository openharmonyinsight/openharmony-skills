# OpenHarmony真实仓库示例（标注历史格式）

本文档收录来自OpenHarmony hiviewdfx仓库的真实测试代码，**标注历史命名格式以供存量分析参考**。

---

## 示例一：BBoxDetector插件测试

**来源路径**：`base/hiviewdfx/hiview/plugins/bbox_detector/test/unittest/`

**⚠️ 历史命名格式标注**：
- 测试类名：`BBoxDetectorUnitTest`（符合推荐规则）
- 用例命名：`BBoxDetectorUnitTest001`（**历史格式**，不推荐新生成模仿）
- 推荐：应使用 `BBoxDetectorPlugin_001` 或 `CanProcessEvent_001`

### 测试源码

```cpp
/*
 * Copyright (c) 2022 Huawei Device Co., Ltd.
 * ...
 */
#include <gtest/gtest.h>
#include "bbox_detector_unit_test.h"
#include "bbox_detector_plugin.h"

using namespace testing::ext;  // ✓ OpenHarmony门禁要求

namespace OHOS {
namespace HiviewDFX {

void BBoxDetectorUnitTest::SetUpTestCase(void) {}
void BBoxDetectorUnitTest::TearDownTestCase(void) {}

void BBoxDetectorUnitTest::SetUp(void)
{
    FileUtil::ForceCreateDirectory("/data/test/bbox/panic_log/");
}

void BBoxDetectorUnitTest::TearDown(void)
{
    FileUtil::ForceRemoveDirectory("/data/test/bbox/");
}

/**
 * @tc.name: BBoxDetectorUnitTest001          // ⚠️ 历史格式：TestSuiteFunction001
 * @tc.desc: check bbox config parser
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(BBoxDetectorUnitTest, BBoxDetectorUnitTest001, TestSize.Level1)
{
    SysEventCreator sysEventCreator("KERNEL_VENDOR", "PANIC", SysEventCreator::FAULT);
    auto sysEvent = make_shared<SysEvent>("test", nullptr, sysEventCreator);
    auto testPlugin = make_shared<BBoxDetectorPlugin>();
    EXPECT_EQ(testPlugin->CanProcessEvent(event), true);
}

/**
 * @tc.name: BBoxDetectorUnitTest002          // ⚠️ 历史格式
 * @tc.type: FUNC
 */
HWTEST_F(BBoxDetectorUnitTest, BBoxDetectorUnitTest002, TestSize.Level0)  // ✓ Level0冒烟测试
{
    GenerateFile("/data/test/bbox/panic_log/test_file", 1);
    EXPECT_TRUE(FileUtil::FileExists("/data/test/bbox/panic_log/test_file"));
}
```

### 对应BUILD.gn

```python
import("//build/test.gni")  # ✓ 第一行必须import

module_output_path = "hiview/bbox_detector"

ohos_unittest("BBoxDetectorUnitTest") {
    sources = [ "unittest/bbox_detector_unit_test.cpp" ]
    cflags_cc = [ "-Dprivate=public" ]  # ✓ 访问私有成员
    external_deps = [
        "googletest:gmock",      # ✓ 使用Mock
        "googletest:gtest_main",  # ✓ 必填
        "hilog:libhilog",
    ]
    module_out_path = module_output_path
}
```

### 要点说明

1. **历史命名格式**：`BBoxDetectorUnitTest001` 是历史存量格式，生成新测试应使用 `[FunctionName]_[001]`
2. **SetUp/TearDown**：每个用例前后执行目录创建与清理
3. **TestSize.Level0**：冒烟测试，门禁阻塞级别
4. **cflags_cc**：访问私有成员必须配置

---

## 示例二：TraceStrategy策略测试

**来源路径**：`base/hiviewdfx/hiview/framework/native/unified_collection/collector/impl/trace/test/`

**⚠️ 历史命名格式标注**：
- 用例命名：`TraceStrategyTest001`（**历史格式**，不推荐新生成模仿）
- 推荐：应使用 `TraceFlowControlStrategy_001` 或 `HandleTrace_001`

### 测试源码

```cpp
using namespace testing::ext;

class TraceStrategyTest : public testing::Test {
public:
    void SetUp() override
    {
        if (!FileUtil::FileExists(TEST_DB_PATH)) {
            FileUtil::ForceCreateDirectory(TEST_DB_PATH);
        }
    };

    void TearDown() override
    {
        if (FileUtil::FileExists(TEST_DB_PATH)) {
            FileUtil::ForceRemoveDirectory(TEST_DB_PATH);
        }
    };

    static void SetUpTestCase()
    {
        CreateTraceFile("/data/test/trace_src/test_traces/trace.sys");
    }
};

/**
 * @tc.name: TraceStrategyTest001             // ⚠️ 历史格式：TestSuiteTest001
 * @tc.desc: used to test TraceFlowControlStrategy
 * @tc.type: FUNC
 */
HWTEST_F(TraceStrategyTest, TraceStrategyTest001, TestSize.Level1)
{
    StrategyParam strategyParam {0, 0, ...};
    auto flowControlStrategy = std::make_shared<TraceFlowControlStrategy>(...);
    // 验证逻辑
}
```

### BUILD.gn配置

```python
ohos_unittest("TraceStrategyTest") {
    configs = [ ":trace_unified_collection_test_config" ]
    sources = [
        "trace_strategy_test.cpp",
        "$hiview_framework/.../trace_handler.cpp",
    ]
    defines = [
        "TRACE_STRATEGY_UNITTEST",  # ✓ 条件编译宏
    ]
    cflags = [ "-frtti" ]  # ✓ 启用dynamic_cast
}
```

### 要点说明

1. **SetUpTestCase**：一次性创建源目录和trace文件，所有用例共享
2. **SetUp/TearDown**：每个用例独立的数据库路径，保证隔离
3. **defines**：添加测试专用宏，源码中区分测试和正式编译
4. **cflags `-frtti`**：启用运行时类型信息，供dynamic_cast使用

---

## 示例三：SysEventDao数据库测试

**来源路径**：`base/hiviewdfx/hiview/framework/native/unified_collection/database/test/`

**⚠️ 历史命名格式标注**：
- 用例命名：`TestSysEventDaoInsert_001`（**历史格式**，不推荐新生成模仿）
- 推荐：应使用 `Insert_001` 或 `SaveEvent_001`

### 测试源码

```cpp
namespace OHOS {
namespace HiviewDFX {
namespace {
const char TEST_LEVEL[] = "MINOR";
}

void SysEventDaoTest::SetUpTestCase()
{
    HiviewPlatform &platform = HiviewPlatform::GetInstance();
    platform.InitEnvironment("/data/test/test_data/hiview_platform_config");
}

/**
 * @tc.name: TestSysEventDaoInsert_001        // ⚠️ 历史格式：TestFunctionName_001
 * @tc.desc: save event to doc store
 * @tc.type: FUNC
 * @tc.require: AR000FT2Q3
 */
HWTEST_F(SysEventDaoTest, TestSysEventDaoInsert_001, testing::ext::TestSize.Level3)
{
    std::string jsonStr = R"~({"domain_":"demo", "name_":"SysEventDaoTest_001"})~";
    // 验证插入逻辑
}
```

### 要点说明

1. **SetUpTestCase**：初始化HiviewPlatform单例环境，提供基础设施
2. **匿名命名空间**：定义测试常量，避免符号污染
3. **@tc.require**：关联需求编号（如`AR000FT2Q3`），与需求管理系统联动
4. **TestSize.Level3**：集成级测试，耗时较长

---

## 示例四：Mock文件编写模式

### 类继承Mock模式

```cpp
// mock/bbox_detectors_mock.h
#include <gmock/gmock.h>
#include "plugin.h"

namespace OHOS {
namespace HiviewDFX {
class MockHiviewContext : public HiviewContext {
public:
    MOCK_METHOD0(GetSharedWorkLoop, std::shared_ptr<EventLoop>());
};

class MockEventLoop : public EventLoop {
public:
    MockEventLoop() : EventLoop("testEventLoop") {};
    uint64_t AddTimerEvent(...) override;  // 手动实现
    MOCK_METHOD0(GetMockInterval, uint64_t());  // gmock宏
};
}
}
```

### 单例Mock模式

```cpp
// mock/hisysevent_util_mock.h
#include <gmock/gmock.h>

namespace OHOS {
namespace HiviewDFX {
class MockHisyseventUtil {
public:
    static MockHisyseventUtil& GetInstance();
    MOCK_METHOD0(IsEventProcessed, bool());

private:
    MockHisyseventUtil() = default;
    MockHisyseventUtil& operator=(const MockHisyseventUtil&) = delete;
};
}
}
```

### BUILD.gn配置（使用Mock时）

```python
ohos_unittest("BBoxDetectorUnitTest") {
    sources = [
        "unittest/bbox_detector_unit_test.cpp",
        "mock/bbox_detectors_mock.cpp",  # ✓ Mock cpp必须加入sources
    ]
    external_deps = [
        "googletest:gmock",  # ✓ Mock时必填
    ]
}
```

---

## 附录：命名格式对照表

### 推荐新生成规则

| 类型 | 格式 | 示例 |
|------|------|------|
| 测试文件 | `[Module]Test.cpp` | `CalculatorTest.cpp` |
| 测试用例 | `[FunctionName]_[001]` | `Add_001` |
| @tc.name | 与用例名一致 | `Add_001` |

### 历史存量格式（仅分析时参考）

| 历史格式 | 示例 | 说明 |
|----------|------|------|
| `[TestSuite]Function_[Seq]` | `BBoxDetectorUnitTest001` | hiviewdfx仓库历史 |
| `[TestSuite]Test_[Seq]` | `TraceStrategyTest001` | trace测试历史 |
| `Test[Function]_[Seq]` | `TestSysEventDaoInsert_001` | 数据库测试历史 |

**重要**：生成新测试时遵循推荐规则，不要模仿历史格式。

---

## 相关文档

- [framework-quickref.md](framework-quickref.md) - 测试框架速查表
- [naming-convention.md](naming-convention.md) - 命名规范（推荐新规则）
- [assertion-gmock-guide.md](assertion-gmock-guide.md) - Mock配置详情