---
name: openharmony-ut-generator
description: "为OpenHarmony C/C++代码生成单元测试用例。Use when: (1) 用户请求为子系统/模块/文件/函数生成单元测试；(2) 编写HWTEST/HWTEST_F测试用例；(3) 创建ohos_unittest BUILD.gn配置；(4) 用户提到'生成测试用例'、'写单元测试'、HWTEST、ohos_unittest。Keywords: HWTEST, ohos_unittest,  unit test, C++ testing, 单元测试生成"
---

# OpenHarmony 单元测试生成

为 OpenHarmony C/C++ 代码生成符合 testfwk_developer_test 框架规范的单元测试用例。

---

## Anti-Patterns - 绝对禁止事项

NEVER 做以下操作，否则会导致测试无法编译、运行：

| 禁止项                                          | 原因                                                | 正确做法                                            |
| -------------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| **NEVER 省略 `using namespace testing::ext;`** | HWTEST/HWTEST_F等宏定义在此命名空间，缺失会导致编译失败               | 文件头必须包含该语句                                      |
| **NEVER 使用GTest原生 `TEST()` 或 `TEST_F()`**    | OpenHarmony门禁无法识别，缺少测试等级参数                        | 统一使用 `HWTEST` 或 `HWTEST_F`                      |
| **NEVER 在HWTEST宏中忘记测试等级参数**                  | TestSize.Level1-4是门禁判断依据，缺失会被拒绝                   | 必须指定如 `TestSize.Level1`                         |
| **NEVER 省略 `import("//build/test.gni")`**    | ohos_unittest模板在此文件定义，缺失会报"template not found"    | BUILD.gn第一行必须import                             |
| **NEVER 在module_out_path使用绝对路径**             | 输出路径格式必须为 `子系统名/模块名`，GN路径会导致错误                    | 使用如 `hiviewdfx/hiview_test`                     |
| **NEVER 访问private成员时忘记cflags_cc绕过**          | private成员无法直接访问，会报"is private"错误                  | 添加 `-Dprivate=public -Dprotected=public`        |
| **NEVER 混用测试类型概念**                           | OpenHarmony有FUNC/PERF/RELI/SECU/FUZZ类型，与GTest概念不同 | 在@tc.type中使用OH定义的类型                             |
| **NEVER 在SetUp中忘记初始化测试对象**                   | 未初始化指针会导致SEGFAULT或NULL pointer错误                  | 确保SetUp中创建detector_等对象                          |
| **NEVER 省略gtest_main依赖**                     | 缺失会导致链接错误"undefined reference to main"            | deps中必须包含 `//third_party/googletest:gtest_main` |

---

## 执行流程

```
环境确认 → 分析源码 → 测试策略 → 测试设计 → 用例规划 → 编写测试文件 → BUILD.gn → 验证
```

---

## 步骤零：环境确认

**目标**：确认测试文件放置位置和编译环境配置。

**MANDATORY - READ ENTIRE FILE**: Before环境确认，MUST read [`test-framework.md`](references/test-framework.md) completely to understand:

- ohos_unittest/ohos_moduletest/ohos_fuzztest区别与选择
- API版本对应关系
- 测试框架目录结构

**Do NOT Load**: 其他reference文件暂时不需要

### 检查清单（必完成）

| 检查项        | 规范                                    | 示例                                   |
| ---------- | ------------------------------------- | ------------------------------------ |
| 测试文件位置     | 模块根目录/test/unittest/                  | base/hiviewdfx/hiview/test/unittest/ |
| Mock文件位置   | test/mock/                            | base/hiviewdfx/hiview/test/mock/     |
| BUILD.gn位置 | test/目录下                              | base/hiviewdfx/hiview/test/BUILD.gn  |
| BUILD.gn入口 | group("unittest") { testonly = true } | --                                   |
| 源码路径格式     | GN风格 //base/xxx                       | //base/hiviewdfx/hiview              |

### 输出格式

确认完成后输出：

```markdown
## 环境确认完成
- 模块根目录: base/xxx/yyy
- 测试目录: base/xxx/yyy/test/unittest/
- 测试输出路径: subsystem/module_test
- 源码GN路径: //base/xxx/yyy
```

---

## 步骤一：分析待测源码

**目标**：解析源码，提取测试所需的结构化信息。

**MANDATORY - READ ENTIRE FILE**: Continue read [`test-framework.md`](references/test-framework.md) (if not completed in step 0)

**Light Loading** (read only if needed):

- [`test-examples.md`](references/test-examples.md) - 需要参考真实代码示例时

**Do NOT Load**: build-gn-config.md, gmock-guide.md (此步骤不涉及)

### 解析要点

| 解析类别 | 关键信息           | 方法                  |
| ---- | -------------- | ------------------- |
| 类结构  | 类名、继承关系、成员变量   | 提取class定义块          |
| 公开方法 | 函数签名、返回类型、参数列表 | 分析public段函数声明       |
| 函数逻辑 | 分支条件、异常处理、边界检查 | 提取if/try/return逻辑   |
| 数据类型 | 枚举、常量、结构体定义    | 提取enum/const/struct |

### 输出格式（结构化报告）

```markdown
## 源码分析报告
### 文件信息
- 源文件: //base/xxx/src/file.cpp
- 头文件: //base/xxx/include/file.h
- 命名空间: OHOS::XXX

### 公开方法列表
| 方法 | 签名 | 分支逻辑 | 边界条件 |
| GetSectionInfo | bool GetSectionInfo(const string&, Info&) | 空字符串返回false | 空字符串 |
| ResetSection | bool ResetSection(const string&) | 空字符串返回false | 空字符串 |
```

---

## 步骤二：制定测试策略

**目标**：基于源码分析，制定测试范围、类型、优先级和覆盖率目标。

**Light Loading** (read only if needed):

- [`test-strategy-method.md`](references/test-strategy-method.md) - 需要详细了解策略制定方法论时

**Do NOT Load**: test-macro.md, build-gn-config.md

### 策略决策表

| 方法类型      | 测试范围判定      | 优先级建议         |
| --------- | ----------- | ------------- |
| public方法  | 必须测试        | 核心功能P1，辅助功能P2 |
| static方法  | 必须测试（独立可测）  | P1            |
| virtual方法 | 必须测试（覆盖派生类） | P1/P2         |
| private方法 | 不直接测试       | 通过public间接覆盖  |

| 逻辑特征 | 测试类型选择      |
| ---- | ----------- |
| 计算逻辑 | FUNC（功能测试）  |
| 性能敏感 | PERF（性能测试）  |
| 异常处理 | RELI（可靠性测试） |
| 安全检查 | SECU（安全测试）  |

### 输出格式

```markdown
## 测试策略
| 方法 | 测试判定 | 测试类型 | 优先级 |
| GetSectionInfo | 必测（核心功能） | FUNC | P1 |
| ResetSection | 必测（含状态处理） | FUNC | P1 |

### 覆盖率目标
- 语句覆盖率: ≥80%
- 分支覆盖率: ≥70%
- 函数覆盖率: 100%
```

---

## 步骤三：进行测试设计

**目标**：将测试策略转化为具体的测试场景设计。

**Light Loading** (read only if needed):

- [`test-strategy-method.md`](references/test-strategy-method.md) - 需要详细场景设计方法时

**Do NOT Load**: test-macro.md, build-gn-config.md

### 测试场景设计模板（必使用）

为每个方法填写以下表格：

```markdown
## [函数名] 测试场景设计
| 编号 | 场景类型 | 场景描述 | 输入数据 | 预期输出 | 测试等级 |
| T01 | 正常 | [具体场景] | [参数值] | [返回值/状态] | Level1 |
| T02 | 异常 | [错误场景] | [触发错误的输入] | [错误码/false] | Level2 |
| T03 | 边界 | [边界值] | [INT_MAX/空字符串等] | [预期行为] | Level2 |
| T04 | 状态 | [状态依赖] | [前置状态描述] | [状态变化结果] | Level2 |
```

### 场景设计要点

| 参数类型     | 正常输入设计     | 边界测试点                   |
| -------- | ---------- | ----------------------- |
| int/long | 典型正值、负值、零值 | INT_MIN, INT_MAX, 0, -1 |
| string   | 非空字符串      | 空字符串、超长字符串              |
| 指针       | 有效对象指针     | nullptr                 |
| 容器       | 非空容器       | 空容器、单元素                 |

---

## 步骤四：规划测试用例

**目标**：将测试场景映射为具体的测试用例，确定命名和等级分配。

**MANDATORY - READ ENTIRE FILE**: Before规划用例，MUST read [`naming-convention.md`](references/naming-convention.md)  to understand:

- 测试文件命名规范：`[Module]Test.cpp`
- 测试套命名规范：`[ModuleName]Test`
- 测试用例命名规范：`[FunctionName]_[001-999]`

**Do NOT Load**: build-gn-config.md, gmock-guide.md

### 用例规划模板（必使用）

```markdown
## [函数名] 用例规划
| 用例编号 | 用例名称 | 对应场景 | 测试等级 | 测试宏 |
| 001 | GetSectionInfo_001 | T01 正常获取 | Level1 | HWTEST_F |
| 002 | GetSectionInfo_002 | T02 空字符串 | Level2 | HWTEST_F |
```

### 测试宏选择决策表

| 情况        | 测试宏选择                             | 原因                   |
| --------- | --------------------------------- | -------------------- |
| 无需初始化/清理  | `HWTEST(A, B, TestSize.Level1)`   | 独立测试，无Setup/Teardown |
| 需要测试前后初始化 | `HWTEST_F(A, B, TestSize.Level1)` | 需要SetUp/TearDown     |
| 多线程测试     | `HWMTEST_F(A, B, C, D)`           | D为线程数                |
| 参数化测试     | `HWTEST_P(A, B, C)`               | 多组数据测试               |

---

## 步骤五：编写测试文件

**目标**：生成符合规范的测试代码文件。

**MANDATORY - READ ENTIRE FILE**: Before编写代码，MUST read:

- [`test-macro.md`](references/test-macro.md)  - HWTEST/HWTEST_F完整用法、SetUp/TearDown实现
- [`comment-standard.md`](references/comment-standard.md) - @tc.name/@tc.desc/@tc.type注释格式
- [`assertion-guide.md`](references/assertion-guide.md) - EXPECT_EQ/ASSERT_NE使用规则

**Do NOT Load for this step**:

- `build-gn-config.md` - 此步骤不涉及BUILD.gn
- `gmock-guide.md` - 仅需Mock时才加载（步骤五完成后再read）

**Light Loading** (read only if Mock needed):

- [`gmock-guide.md`](references/gmock-guide.md) - 测试需要Mock依赖对象时加载
- [`test-examples.md`](references/test-examples.md) - 需要参考完整示例代码时

### 测试文件结构模板（必遵循）

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
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

#include <gtest/gtest.h>
#include "被测头文件.h"

using namespace testing::ext;  // 必须包含，HWTEST宏在此命名空间

class BBoxDetectorTest : public testing::Test {
public:
    static void SetUpTestCase();     // 所有测试前执行一次
    static void TearDownTestCase();  // 所有测试后执行一次
    void SetUp() override;           // 每个测试前执行
    void TearDown() override;        // 每个测试后执行

    BBoxDetector* detector_;         // 测试对象成员
};

void BBoxDetectorTest::SetUpTestCase() {}
void BBoxDetectorTest::TearDownTestCase() {}
void BBoxDetectorTest::SetUp() { detector_ = new BBoxDetector(); }
void BBoxDetectorTest::TearDown() { delete detector_; }

/*
 * @tc.name: GetSectionInfo_001
 * @tc.desc: 验证使用有效段名获取Section信息成功
 * @tc.type: FUNC
 * @tc.require: issueNumber
 * @tc.author: authorName
 */
HWTEST_F(BBoxDetectorTest, GetSectionInfo_001, TestSize.Level1)
{
    GTEST_LOG_(INFO) << "GetSectionInfo_001 start";
    std::string sectionName = "section1";
    SectionInfo info;

    bool result = detector_->GetSectionInfo(sectionName, info);

    EXPECT_TRUE(result);
    GTEST_LOG_(INFO) << "GetSectionInfo_001 end";
}
```

### 断言使用规则（必遵循）

| 断言类型                       | 使用场景        | 失败行为    |
| -------------------------- | ----------- | ------- |
| `ASSERT_NE(ptr, nullptr)`  | 前置条件：指针非空检查 | 失败后终止测试 |
| `ASSERT_TRUE(condition)`   | 前置条件：状态检查   | 失败后终止测试 |
| `EXPECT_EQ(val, expected)` | 结果验证：值相等    | 失败后继续执行 |
| `EXPECT_TRUE(condition)`   | 结果验证：条件为真   | 失败后继续执行 |

---

## 步骤六：编写 BUILD.gn

**目标**：配置测试目标编译规则。

**MANDATORY - READ ENTIRE FILE**: Before编写BUILD.gn，MUST read [`build-gn-config.md`](references/build-gn-config.md) (~650 lines) to understand:

- ohos_unittest完整配置项
- deps与external_deps区别
- cflags_cc访问控制绕过
- module_out_path格式要求

**Do NOT Load for this step**:

- `test-macro.md`, `test-examples.md` - 此步骤不涉及测试代码
- `gmock-guide.md` - 仅配置gmock依赖时参考external_deps部分

### BUILD.gn模板（必遵循）

```python
import("//build/test.gni")  # 第一行必须import

module_output_path = "hiviewdfx/hiview_test"  # 格式：子系统名/模块名

config("module_private_config") {
    visibility = [ ":*" ]  # 仅本BUILD.gn可见
    include_dirs = [
        "//base/hiviewdfx/hiview/include",
        "//base/hiviewdfx/hiview/core",
    ]
}

ohos_unittest("BBoxDetectorUnitTest") {
    module_out_path = module_output_path

    sources = [
        "unittest/bbox_detector/bbox_detector_test.cpp",
    ]

    configs = [ ":module_private_config" ]

    deps = [
        "//third_party/googletest:gtest_main",  # 必须包含
        "//base/hiviewdfx/hiview:hiview_core",  # 被测模块
    ]

    external_deps = [
        "hiviewdfx_hilog_native:libhilog",  # 外部依赖
        "googletest:gmock",  # Mock支持（如需要）
    ]

    # 访问控制绕过：测试private/protected成员
    cflags_cc = [
        "-Dprivate=public",
        "-Dprotected=public",
    ]

    defines = [
        "HILOG_ENABLE",
        "UNIT_TEST",
    ]
}

group("unittest") {
    testonly = true
    deps = [":BBoxDetectorUnitTest"]
}
```

### 关键配置项说明

| 配置项               | 说明                 | 必填性 |
| ----------------- | ------------------ | --- |
| `module_out_path` | 测试输出路径，格式 `子系统/模块` | 必填  |
| `sources`         | 测试源文件列表            | 必填  |
| `deps`            | 内部依赖，包含gtest_main  | 必填  |
| `external_deps`   | 外部依赖库              | 按需  |
| `cflags_cc`       | 访问控制绕过（测试private时） | 按需  |

---

## 步骤七：验证与调试

**目标**：确认测试用例可以正确编译和运行。

**MANDATORY - READ ENTIRE FILE**: Before验证，MUST read [`troubleshooting.md`](references/troubleshooting.md)  to understand:

- 常见编译错误与解决方案
- 链接错误排查方法
- 访问控制绕过注意事项

**Do NOT Load**: 其他reference文件已在前步骤加载

### 编译命令

```bash
./build.sh --product-name <product> --build-target BBoxDetectorUnitTest
```

### 常见编译错误快速排查

| 错误                                   | 原因             | 解决方案                               |
| ------------------------------------ | -------------- | ---------------------------------- |
| `fatal error: xxx.h: No such file`   | include_dirs缺失 | 在config块中添加include_dirs            |
| `undefined reference to xxx`         | deps缺失         | 检查deps和external_deps               |
| `'xxx' is private`                   | 访问控制           | 添加cflags_cc: `-Dprivate=public`    |
| `template 'ohos_unittest' not found` | 缺少import       | 第一行添加 `import("//build/test.gni")` |

---

## 快速参考

### 测试等级速查

| 等级     | 用途       | 执行频率      |
| ------ | -------- | --------- |
| Level0 | 冒烟测试（门禁） | 必须通过，高频执行 |
| Level1 | 基础测试     | 常用功能，正常输入 |
| Level2 | 重要测试     | 异常处理，边界条件 |
| Level3 | 一般测试     | 完整功能覆盖    |
| Level4 | 稀少测试     | 极端条件      |

### 测试宏速查

| 宏                       | 适用场景            | 参数格式                       |
| ----------------------- | --------------- | -------------------------- |
| `HWTEST(A, B, C)`       | 无Setup/Teardown | A:测试套名, B:用例名, C:等级        |
| `HWTEST_F(A, B, C)`     | 需Setup/Teardown | A:测试类名, B:用例名, C:等级        |
| `HWMTEST_F(A, B, C, D)` | 多线程测试           | D:线程数                      |
| `HWTEST_P(A, B, C)`     | 参数化测试           | 配合INSTANTIATE_TEST_SUITE_P |

---

## References导航

详细文档位于 `references/` 目录，按步骤需求加载：

| 文件                        | 内容                  | 加载时机                   |
| ------------------------- | ------------------- | ---------------------- |
| `test-framework.md`       | 测试框架概述、API版本对应      | **步骤0 MANDATORY**      |
| `test-macro.md`           | HWTEST/HWTEST_F详细用法 | **步骤5 MANDATORY**      |
| `naming-convention.md`    | 文件/用例命名规范           | **步骤4 MANDATORY**      |
| `comment-standard.md`     | @tc注释格式             | **步骤5 MANDATORY**      |
| `assertion-guide.md`      | 断言使用规则              | **步骤5 MANDATORY**      |
| `build-gn-config.md`      | BUILD.gn完整配置        | **步骤6 MANDATORY**      |
| `troubleshooting.md`      | 编译错误排查              | **步骤7 MANDATORY**      |
| `test-strategy-method.md` | 测试策略与设计方法           | 步骤2-3 Light Loading    |
| `test-examples.md`        | 真实测试代码示例            | 步骤1-5 Light Loading    |
| `gmock-guide.md`          | gmock使用指南           | 步骤5 Mock时Light Loading |
| `test-level.md`           | 测试等级详解              | 可选参考                   |
| `test-case-spec.md`       | 测试用例完整规范            | 可选参考                   |

---

## 输入信息要求

| 信息           | 必需性 | 说明                   |
| ------------ | --- | -------------------- |
| 源码位置         | 必需  | 文件路径或函数名称            |
| 需求编号         | 可选  | @tc.require填写内容，默认留空 |
| 测试等级         | 可选  | 默认Level1             |
| 是否生成BUILD.gn | 可选  | 默认生成                 |

---

## 开始使用

当用户请求生成测试时，按工作流程执行：

1. 环境确认 → read test-framework.md
2. 分析源码 → 输出源码分析报告
3. 测试策略 → 输出策略表格
4. 测试设计 → 输出场景设计表格
5. 用例规划 → read naming-convention.md → 输出用例规划
6. 编写测试文件 → read test-macro.md + comment-standard.md + assertion-guide.md → 生成.cpp
7. 编写BUILD.gn → read build-gn-config.md → 生成.gn
8. 验证 → read troubleshooting.md → 提供编译命令