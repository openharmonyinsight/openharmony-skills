# 测试文件完整结构（OpenHarmony要求）

---

## 一、测试文件标准结构

### HWTEST_F结构（带SetUp/TearDown）

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * ...
 */
#include <gtest/gtest.h>
#include "被测模块头文件.h"
using namespace testing::ext;  // NEVER省略，HWTEST宏在此命名空间

// 测试类定义
class ModuleTest : public testing::Test {
public:
    static void SetUpTestCase();      // 所有测试前执行一次
    static void TearDownTestCase();   // 所有测试后执行一次
    void SetUp() override;            // 每个测试前执行
    void TearDown() override;         // 每个测试后执行

    Module* module_;                  // 测试对象成员（NEVER忘记初始化）
};

void ModuleTest::SetUpTestCase() {}
void ModuleTest::TearDownTestCase() {}

void ModuleTest::SetUp() {
    module_ = new Module();  // NEVER忘记初始化，否则SEGFAULT
}

void ModuleTest::TearDown() {
    delete module_;  // 资源清理
}

/*
 * @tc.name: FunctionName_001
 * @tc.desc: 验证xxx功能xxx场景
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(ModuleTest, FunctionName_001, TestSize.Level1)
{
    GTEST_LOG_(INFO) << "FunctionName_001 start";
    // 测试实现
    GTEST_LOG_(INFO) << "FunctionName_001 end";
}
```

### HWTEST结构（无SetUp/TearDown）

```cpp
#include <gtest/gtest.h>
using namespace testing::ext;

/*
 * @tc.name: SimpleCheck_001
 * @tc.desc: 简单功能验证
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST(SimpleTest, SimpleCheck_001, TestSize.Level1)
{
    EXPECT_EQ(1 + 1, 2);
}
```

---

## 二、Anti-Patterns禁止清单

| 禁止项                                         | 原因                                    | 正确做法                                           |
| ------------------------------------------- | ------------------------------------- | ---------------------------------------------- |
| **NEVER省略 `using namespace testing::ext;`** | HWTEST宏在此命名空间，缺失导致编译失败                | 文件头必须包含                                        |
| **NEVER使用GTest原生 `TEST()` 或 `TEST_F()`**    | OpenHarmony门禁无法识别，缺少测试等级参数            | 统一使用 `HWTEST` 或 `HWTEST_F`                     |
| **NEVER在HWTEST宏中忘记测试等级参数**                  | TestSize.Level1-4是门禁判断依据，缺失被拒绝        | 必须指定如 `TestSize.Level1`                        |
| **NEVER在SetUp中忘记初始化测试对象**                   | 未初始化指针导致SEGFAULT或NULL pointer错误       | SetUp中创建detector_等对象                           |
| **NEVER访问private成员时忘记cflags_cc绕过**          | private成员无法直接访问，报"is private"错误       | BUILD.gn添加 `-Dprivate=public`                  |
| **NEVER省略gtest_main依赖**                     | 缺失导致链接错误"undefined reference to main" | deps必须包含 `//third_party/googletest:gtest_main` |
| **NEVER硬编码绝对路径**                            | 不可移植，测试失败                             | 使用相对路径或配置文件                                    |
| **NEVER使用真实外部服务**                           | 测试不稳定、依赖环境                            | 使用Mock或测试专用实现                                  |
| **NEVER无断言测试**                              | 无法验证结果                                | 每个测试至少一个EXPECT/ASSERT                          |

---

## 三、检查清单

编写测试用例后逐项检查：

- [ ] 文件头包含 `using namespace testing::ext;`
- [ ] 使用HWTEST/HWTEST_F而非TEST/TEST_F
- [ ] HWTEST宏包含测试等级参数（TestSize.Level1-4）
- [ ] @tc注释四项完整（name/desc/type/require）
- [ ] @tc.name与HWTEST宏第2参数一致
- [ ] SetUp正确初始化测试对象（new Module()）
- [ ] TearDown正确释放资源（delete module_）
- [ ] 每个测试至少一个断言（EXPECT_*或ASSERT_*）
- [ ] BUILD.gn配置正确：
  - [ ] sources包含测试文件
  - [ ] deps包含gtest_main
  - [ ] external_deps包含gmock（如使用Mock）
  - [ ] cflags_cc包含 `-Dprivate=public`（如测试私有成员）

---

## 四、命名规范要点

### 推荐新生成规则

| 类型       | 格式                     | 示例                   |
| -------- | ---------------------- | -------------------- |
| 测试文件     | `[Module]Test.cpp`     | `CalculatorTest.cpp` |
| 测试套/类    | `[Module]Test`         | `CalculatorTest`     |
| 测试用例     | `[FunctionName]_[001]` | `Add_001`, `Add_002` |
| @tc.name | 与用例名一致                 | `Add_001`            |

**生成新测试时遵循**：

```cpp
class CalculatorTest : public testing::Test { };

HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 正常
HWTEST_F(CalculatorTest, Add_002, TestSize.Level2)  // 边界
HWTEST_F(CalculatorTest, Add_003, TestSize.Level2)  // 异常
```

### 兼容历史存量风格（仅分析时参考）

历史存量代码可能使用不同命名格式，**生成新测试时不要模仿**：

- `BBoxDetectorUnitTest001`（历史hiviewdfx格式）
- `TraceStrategyTest001`（历史trace格式）
- `TestSysEventDaoInsert_001`（历史数据库格式）

使用 `scripts/analyze-existing-tests.py` 分析存量命名风格。

---

## 五、BUILD.gn配置要点

```python
import("//build/test.gni")  # 第一行必须import

module_output_path = "subsystem/module_test"  # 格式：子系统/模块

config("test_config") {
    visibility = [ ":*" ]
    include_dirs = [
        "//base/xxx/include",
    ]
}

ohos_unittest("ModuleTest") {
    module_out_path = module_output_path
    sources = [ "unittest/module_test.cpp" ]
    configs = [ ":test_config" ]

    deps = [
        "//third_party/googletest:gtest_main",  # 必填
        "//base/xxx:module",  # 被测模块
    ]

    external_deps = [
        "googletest:gmock",  # 使用Mock时必填
        "hilog:libhilog",
    ]

    cflags_cc = [
        "-Dprivate=public",  # 测试私有成员时必填
        "-Dprotected=public",
    ]
}

group("unittest") {
    testonly = true
    deps = [":ModuleTest"]
}
```

**关键配置项**：
| 配置项 | 说明 | 必填性 |
|--------|------|--------|
| `import("//build/test.gni")` | ohos_unittest模板定义 | **第一行必填** |
| `module_out_path` | 测试输出路径（子系统/模块） | **必填** |
| `deps` 包含gtest_main | 提供main函数入口 | **必填** |
| `external_deps` 包含gmock | gmock库依赖 | **使用Mock时必填** |
| `cflags_cc` | 访问控制绕过 | **测试私有成员时必填** |

---

## 相关文档

- [framework-quickref.md](framework-quickref.md) - 测试框架速查表（宏+等级+注释）
- [build-rules.md](build-rules.md) - BUILD.gn决策规则
- [error-matrix.md](error-matrix.md) - 错误排查矩阵
- [real-patterns.md](real-patterns.md) - 真实仓库示例