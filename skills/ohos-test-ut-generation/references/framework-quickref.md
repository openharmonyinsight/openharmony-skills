# OpenHarmony 测试框架速查表

---

## 一、测试宏选择决策

| 需求场景             | 选择宏                           | OpenHarmony特有要求              |
| ---------------- | ----------------------------- | ---------------------------- |
| 无需初始化/清理         | `HWTEST(套名, 用例名, 等级)`         | **门禁仅识别HWTEST**，NEVER用TEST() |
| 需要SetUp/TearDown | `HWTEST_F(类名, 用例名, 等级)`       | **必须指定等级参数**，否则门禁拒绝          |
| 多线程并发测试          | `HWMTEST_F(类名, 用例名, 等级, 线程数)` | 第4参数为线程数                     |
| 参数化测试            | `HWTEST_P(类名, 用例名, 等级)`       | 多组输入数据                       |

**门禁强制要求**：

```cpp
#include <gtest/gtest.h>
using namespace testing::ext;  // NEVER省略，HWTEST宏在此命名空间
```

---

## 二、测试等级选择（门禁判定依据）

| 等级         | 门禁行为  | 适用场景                 | 失败影响   |
| ---------- | ----- | -------------------- | ------ |
| **Level0** | ✅阻塞提交 | 冒烟测试：系统核心功能          | 系统不可用  |
| **Level1** | ✅阻塞提交 | 正常输入、高频场景            | 常用功能失败 |
| **Level2** | ❌不阻塞  | 异常处理、边界条件、空值/nullptr | 辅助功能失败 |
| **Level3** | ❌不阻塞  | 完整功能、辅助功能、集成测试       | 覆盖不足   |
| **Level4** | ❌不阻塞  | 极端条件、死亡测试、内存耗尽       | 极端场景   |

**等级选择决策树**：

```
功能失败导致系统不可用？ → Level0
↓ 否
常用功能的正常路径？ → Level1
↓ 否
异常处理或边界条件？ → Level2
↓ 否
完整功能或辅助功能？ → Level3
↓ 否
极端条件或死亡测试 → Level4
```

**常见场景等级分配**：

- 正常输入验证 → **Level1**
- 空值/nullptr处理 → **Level2**
- 边界值(INT_MAX等) → **Level2**
- 错误码/异常返回 → **Level2**
- 完整功能组合 → **Level3**

---

## 三、@tc 注释规范（门禁解析要求）

**必填注释格式**：

```cpp
/*
 * @tc.name: FunctionName_001        // 必填：与HWTEST宏第2参数一致
 * @tc.desc: 验证xxx功能xxx场景       // 必填：描述测试目的
 * @tc.type: FUNC                    // 必填：FUNC/PERF/RELI/SECU/FUZZ
 * @tc.require: issueI56WJ7          // 选填：issue/AR/SR编号
 */
HWTEST_F(TestSuite, FunctionName_001, TestSize.Level1)
```

**@tc.type 测试类型**（OpenHarmony特有，区别于GTest）：
| 类型编码 | 适用场景 |
|----------|----------|
| **FUNC** | 功能正确性验证 |
| **PERF** | 性能基准验证 |
| **RELI** | 异常恢复、稳定性 |
| **SECU** | 安全漏洞验证 |
| **FUZZ** | 输入鲁棒性验证 |

**@tc.require 格式要求**：

- Issue编号：`issueI56WJ7`（Gitee Issue ID）
- 架构需求：`AR0001`
- 系统需求：`SR0001`

**常见错误**：

```cpp
// ❌ 错误：缺少issue前缀
@tc.require: I56WJ7

// ❌ 错误：缺少等级参数
HWTEST_F(Test, Func_001)  // 门禁拒绝

// ❌ 错误：使用GTest原生宏
TEST(Test, Func)  // 门禁无法识别
```

---

## 四、命名规范速查

### 推荐新生成规则（标准格式）

| 类型         | 格式                         | 示例                   |
| ---------- | -------------------------- | -------------------- |
| 测试文件       | `[Module]Test.cpp`         | `CalculatorTest.cpp` |
| 测试套/类      | `[Module]Test`             | `CalculatorTest`     |
| 测试用例       | `[FunctionName]_[001-999]` | `Add_001`            |
| BUILD.gn目标 | `[module]_test`（小写）        | `calculator_test`    |

**命名示例**（推荐新代码遵循）：

```cpp
class CalculatorTest : public testing::Test { };

HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 正常情况
HWTEST_F(CalculatorTest, Add_002, TestSize.Level2)  // 边界情况
HWTEST_F(CalculatorTest, Add_003, TestSize.Level2)  // 异常情况
```

### 兼容历史存量风格（不推荐新生成）

历史存量代码可能使用以下命名格式，**生成新测试时不要模仿**：

| 历史格式                              | 示例                          | 说明              |
| --------------------------------- | --------------------------- | --------------- |
| `[TestSuite][FunctionName]_[Seq]` | `BBoxDetectorUnitTest001`   | 历史hiviewdfx仓库格式 |
| `[TestSuite]Test[Seq]`            | `TraceStrategyTest001`      | 历史trace测试格式     |
| `Test[FunctionName]_[Seq]`        | `TestSysEventDaoInsert_001` | 历史数据库测试格式       |

**分析存量代码时**：使用 `scripts/analyze-existing-tests.py` 检测命名风格。

---

## 五、文件头版权注释

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
```

**重要**：新文件使用当前年份，修改现有文件保留原有年份。

---

## 相关文档

- [build-rules.md](build-rules.md) - BUILD.gn配置规则
- [error-matrix.md](error-matrix.md) - 错误排查矩阵
- [real-patterns.md](real-patterns.md) - 真实仓库示例
- [test-strategy.md](test-strategy.md) - 测试策略设计方法