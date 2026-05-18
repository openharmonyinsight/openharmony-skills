# OpenHarmony 测试代码真实示例

本文档收录来自 OpenHarmony hiviewdfx 仓库的真实测试代码，涵盖基础 HWTEST_F 测试、复杂 SetUp/TearDown、gmock 数据库测试以及 Mock 文件编写模式。

---

## 示例一：基础 HWTEST_F 测试（BBoxDetector 插件测试）

**来源路径：** `base/hiviewdfx/hiview/plugins/bbox_detector/test/unittest/`

### 测试源码

```cpp
/*
 * Copyright (c) 2022 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <fstream>
#include "bbox_detector_unit_test.h"
#include "bbox_detector_plugin.h"
#include "bbox_detectors_mock.h"
#include "hisysevent_util_mock.h"
#include "sys_event.h"
using namespace std;

namespace OHOS {
namespace HiviewDFX {
using namespace testing;
using namespace testing::ext;

void BBoxDetectorUnitTest::SetUpTestCase(void) {}
void BBoxDetectorUnitTest::TearDownTestCase(void) {}

void BBoxDetectorUnitTest::SetUp(void)
{
    FileUtil::ForceCreateDirectory("/data/test/bbox/panic_log/");
    FileUtil::ForceCreateDirectory("/data/test/bbox/ap_log/");
}

void BBoxDetectorUnitTest::TearDown(void)
{
    FileUtil::ForceRemoveDirectory("/data/test/bbox/");
}

/**
 * @tc.name: BBoxDetectorUnitTest001
 * @tc.desc: check bbox config parser whether it is passed.
 *           1.parse bbox config;
 *           2.check result;
 * @tc.type: FUNC
 * @tc.require:
 * @tc.author: liuwei
 */
HWTEST_F(BBoxDetectorUnitTest, BBoxDetectorUnitTest001, TestSize.Level1)
{
    SysEventCreator sysEventCreator("KERNEL_VENDOR", "PANIC", SysEventCreator::FAULT);
    auto sysEvent = make_shared<SysEvent>("test", nullptr, sysEventCreator);
    auto testPlugin = make_shared<BBoxDetectorPlugin>();
    shared_ptr<Event> event = dynamic_pointer_cast<Event>(sysEvent);
    EXPECT_EQ(testPlugin->CanProcessEvent(event), true);
}

/**
 * @tc.name: BBoxDetectorUnitTest002
 * @tc.desc: check whether fault is processed
 * @tc.type: FUNC
 * @tc.require:
 * @tc.author: liuwei
 */
HWTEST_F(BBoxDetectorUnitTest, BBoxDetectorUnitTest002, TestSize.Level0)
{
    // 测试文件创建和故障处理逻辑
    GenerateFile("/data/test/bbox/panic_log/test_file", 1);
    // ... 验证逻辑
    EXPECT_TRUE(FileUtil::FileExists("/data/test/bbox/panic_log/test_file"));
}
```

### 对应 BUILD.gn

```gn
import("//base/hiviewdfx/hiview/hiview.gni")
import("//build/test.gni")

module_output_path = "hiview/bbox_detector"

config("bbox_detector_test_config") {
  visibility = [ ":*" ]
  include_dirs = [
    "../",
    "../include",
    "mock",
    "unittest",
  ]
}

ohos_unittest("BBoxDetectorUnitTest") {
  sources = [ "unittest/bbox_detector_unit_test.cpp" ]
  sources += bbox_detector_test_source
  configs = [ ":bbox_detector_test_config" ]
  cflags_cc = [ "-Dprivate=public" ]
  cflags_cc += [ "-Dprotected=public" ]
  external_deps = [
    "c_utils:utils",
    "googletest:gmock",
    "googletest:gtest_main",
    "hilog:libhilog",
    "hisysevent:libhisysevent",
  ]
  deps = [
    "$hiview_base:hiviewbase_static_lib_for_tdd",
    "$hiview_base/event_store:event_store_source",
  ]
  module_out_path = module_output_path
}
```

### 要点说明

- 使用 `HWTEST_F` 宏注册测试用例，这是 OpenHarmony 基于 gtest 的扩展宏。
- `SetUp` / `TearDown` 在每个测试用例前后执行目录创建与清理。
- `SetUpTestCase` / `TearDownTestCase` 为静态方法，在整个测试套件前后各执行一次。
- BUILD.gn 中使用 `ohos_unittest` 模板，通过 `cflags_cc` 中的 `-Dprivate=public` 和 `-Dprotected=public` 绕过访问控制进行白盒测试。

---

## 示例二：带复杂 SetUp/TearDown 的测试（TraceStrategy 策略测试）

**来源路径：** `base/hiviewdfx/hiview/framework/native/unified_collection/collector/impl/trace/test/`

### 测试源码

```cpp
#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include "trace_utils.h"
#include "trace_handler.h"
#include "trace_strategy.h"

using namespace testing::ext;
using namespace OHOS::HiviewDFX;

class TraceStrategyTest : public testing::Test {
public:
    void SetUp() override
    {
        if (!FileUtil::FileExists(TEST_DB_PATH)) {
            FileUtil::ForceCreateDirectory(TEST_DB_PATH);
        }
        if (!FileUtil::FileExists(TEST_SHARED_PATH)) {
            FileUtil::ForceCreateDirectory(TEST_SHARED_PATH);
        }
    };

    void TearDown() override
    {
        if (FileUtil::FileExists(TEST_DB_PATH)) {
            FileUtil::ForceRemoveDirectory(TEST_DB_PATH);
        }
        if (FileUtil::FileExists(TEST_SHARED_PATH)) {
            FileUtil::ForceRemoveDirectory(TEST_SHARED_PATH);
        }
    };

    static void SetUpTestCase()
    {
        if (!FileUtil::FileExists(TEST_SRC_PATH)) {
            FileUtil::ForceCreateDirectory(TEST_SRC_PATH);
            CreateTraceFile("/data/test/trace_src/test_traces/trace_20170928220220@75724-2015.sys");
        }
    }

    static void TearDownTestCase()
    {
        if (FileUtil::FileExists(TEST_SRC_PATH)) {
            FileUtil::ForceRemoveDirectory(TEST_SRC_PATH);
        }
    }
};

/**
 * @tc.name: TraceStrategyTest
 * @tc.desc: used to test TraceFlowControlStrategy uc error
 * @tc.type: FUNC
*/
HWTEST_F(TraceStrategyTest, TraceStrategyTest001, TestSize.Level1)
{
    StrategyParam strategyParam {0, 0, EnumToString(UCollect::TraceCaller::XPOWER), TEST_DB_PATH, TEST_CONFIG_PATH};
    auto flowControlStrategy = std::make_shared<TraceFlowControlStrategy>(strategyParam, TraceScenario::TRACE_COMMON,
        std::make_shared<TraceZipHandler>(TEST_SHARED_PATH, strategyParam.caller, 3));
    TraceRetInfo testInfo {
        .errorCode = TraceErrorCode::OUT_OF_TIME
    };
    // ... 验证逻辑
}
```

### 对应 BUILD.gn

```gn
import("//base/hiviewdfx/hiview/hiview.gni")
import("//build/test.gni")

config("trace_unified_collection_test_config") {
  visibility = [ ":*" ]
  include_dirs = [
    "include",
    "$hiview_framework/native/unified_collection/collector/impl/trace/include",
    "$hiview_framework/native/unified_collection/collector/impl/trace/strategy/include",
  ]
  cflags = [
    "-D__UNITTEST__",
    "-frtti",
  ]
}

ohos_unittest("TraceStrategyTest") {
  module_out_path = hiview_module + "/ucollection/trace"
  configs = [ ":trace_unified_collection_test_config" ]
  sources = [
    "trace_strategy_test.cpp",
    "$hiview_framework/native/unified_collection/collector/impl/trace/strategy/src/trace_handler.cpp",
    "$hiview_framework/native/unified_collection/collector/impl/trace/strategy/src/trace_strategy.cpp",
  ]
  deps = [
    "$hiview_base:hiviewbase",
    "$hiview_framework/native/unified_collection/trace_manager:libtrace_manager",
  ]
  external_deps = [
    "googletest:gtest_main",
    "hilog:libhilog",
    "ffrt:libffrt",
    "c_utils:utils",
  ]
  defines = [
    "TRACE_STRATEGY_UNITTEST",
  ]
  resource_config_file = "$hiview_framework/native/unified_collection/collector/impl/trace/test/resource/ohos_test.xml"
}
```

### 要点说明

- `SetUpTestCase` 在套件开始时一次性创建源目录和 trace 文件，适用于所有用例共享的昂贵初始化。
- `SetUp` / `TearDown` 管理每个用例独立的数据库路径和共享路径，保证用例间隔离。
- BUILD.gn 中通过 `defines` 添加 `TRACE_STRATEGY_UNITTEST` 宏，用于在源码中区分测试和正式编译。
- `resource_config_file` 指定测试资源描述文件，用于打包测试所需的额外资源。
- `cflags` 中的 `-frtti` 启用运行时类型信息，供 `dynamic_cast` 等特性使用。

---

## 示例三：带 gmock 的数据库测试（SysEventDao）

**来源路径：** `base/hiviewdfx/hiview/framework/native/unified_collection/database/test/`

### 测试源码

```cpp
#include "sys_event_dao_test.h"
#include <chrono>
#include <thread>
#include <gmock/gmock.h>
#include "sys_event.h"
#include "sys_event_dao.h"

namespace OHOS {
namespace HiviewDFX {
namespace {
const char TEST_LEVEL[] = "MINOR";
constexpr int32_t TEST_INT32_VALUE = 1;
constexpr int64_t TEST_INT64_VALUE = 1;
constexpr double TEST_DOU_VALUE = 123.456;
const std::string TEST_STR_VALUE = "test";
}

void SysEventDaoTest::SetUpTestCase()
{
    OHOS::HiviewDFX::HiviewPlatform &platform = HiviewPlatform::GetInstance();
    std::string defaultDir = "/data/test/test_data/hiview_platform_config";
    if (!platform.InitEnvironment(defaultDir)) {
        std::cout << "fail to init environment" << std::endl;
    }
}

void SysEventDaoTest::TearDownTestCase() {}
void SysEventDaoTest::SetUp() {}
void SysEventDaoTest::TearDown() {}

/**
 * @tc.name: TestSysEventDaoInsert_001
 * @tc.desc: save event to doc store
 * @tc.type: FUNC
 * @tc.require: AR000FT2Q3
 * @tc.author: zhouhaifeng
 */
HWTEST_F(SysEventDaoTest, TestSysEventDaoInsert_001, testing::ext::TestSize.Level3)
{
    std::string jsonStr = R"~({"domain_":"demo", "name_":"SysEventDaoTest_001", "type_":1, "tz_":8,
        "time_":1620271291188, "pid_":6527, "tid_":6527})~";
    // ... 创建事件并验证插入
}
```

### 要点说明

- `SetUpTestCase` 中初始化 `HiviewPlatform` 单例环境，为数据库操作提供基础设施。这是需要全局平台的测试常见模式。
- 匿名命名空间（`namespace { ... }`）中定义测试常量，避免符号污染。
- `@tc.require` 字段关联需求追踪编号（如 `AR000FT2Q3`），与 OpenHarmony 需求管理系统联动。
- `TestSize.Level3` 表示较低的测试级别，通常用于耗时较长的集成级测试。

---

## 示例四：Mock 文件编写模式

**来源路径：** `base/hiviewdfx/hiview/plugins/bbox_detector/test/mock/`

### 类继承 Mock 模式

```cpp
// bbox_detectors_mock.h
#ifndef MOCK_BBOX_DETECTORS_MOCK_H_
#define MOCK_BBOX_DETECTORS_MOCK_H_
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
    uint64_t AddTimerEvent(std::shared_ptr<EventHandler> handler,
                           std::shared_ptr<Event> event, const Task &task,
                           uint64_t interval, bool repeat) override;
    MOCK_METHOD0(GetMockInterval, uint64_t());
};
}
}
#endif
```

### 单例 Mock 模式

```cpp
// hisysevent_util_mock.h
#ifndef MOCK_HISYSEVENT_UTIL_MOCK_H_
#define MOCK_HISYSEVENT_UTIL_MOCK_H_
#include <gmock/gmock.h>
#include "hisysevent_util.h"

namespace OHOS {
namespace HiviewDFX {
class MockHisyseventUtil {
public:
    static MockHisyseventUtil& GetInstance();
    MOCK_METHOD0(IsEventProcessed, bool());
private:
    MockHisyseventUtil() = default;
    ~MockHisyseventUtil() = default;
    MockHisyseventUtil& operator=(const MockHisyseventUtil&) = delete;
    MockHisyseventUtil(const MockHisyseventUtil&) = delete;
};
}
}
#endif
```

### 要点说明

**类继承 Mock：**

- 继承目标类并使用 `MOCK_METHOD` 宏生成模拟方法。
- 适用于接口类或虚函数较多的类，可直接替换真实实现。
- `MockEventLoop` 同时混合了手动覆写（`AddTimerEvent`）和 gmock 宏（`MOCK_METHOD0`），适合部分方法需要自定义行为的场景。

**单例 Mock：**

- 通过 `GetInstance()` 静态方法提供全局唯一实例，与真实单例模式保持一致。
- 构造函数、析构函数设为 `private`，拷贝和赋值操作显式 `delete`，确保单例语义。
- 测试中通过替换 `GetInstance()` 的返回值来注入 Mock 对象，无需修改被测代码。

---

## 附录：测试注解规范

OpenHarmony 测试用例统一使用以下注释格式：

```cpp
/**
 * @tc.name:   测试用例名称（唯一标识）
 * @tc.desc:   测试用例描述（含测试步骤和预期）
 * @tc.type:   测试类型（FUNC / PERF / RELI / SECURITY / ...）
 * @tc.require: 关联需求编号（可选）
 * @tc.author:  用例作者（可选）
 */
```

**TestSize 级别说明：**

| 级别     | 含义     | 适用场景         |
| ------ | ------ | ------------ |
| Level0 | 冒烟测试   | 关键路径验证，快速执行  |
| Level1 | 基础功能测试 | 核心功能验证       |
| Level2 | 扩展功能测试 | 边界条件、异常场景    |
| Level3 | 集成测试   | 涉及多模块协作、耗时较长 |
| Level4 | 完整测试   | 全量回归验证       |
