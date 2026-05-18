# 注释标准（@tc.xxx）

## 概述

OpenHarmony 测试用例必须包含标准注释，用于描述测试信息、追溯需求、自动化工具解析。

## 注释格式

每个测试用例必须包含以下注释块：

```cpp
/*
 * @tc.name: TestCaseName_001
 * @tc.desc: 测试用例简要描述
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(TestSuite, TestCaseName_001, TestSize.Level1)
{
    // 测试实现
}
```

## 注释字段详解

### @tc.name

测试用例名称，必须与测试宏中的用例名一致。

**规则**：
- 格式：`[FunctionName]_[SequenceNumber]`
- 与 HWTEST 宏第二个参数一致

**示例**：

```cpp
/*
 * @tc.name: Add_001
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 一致 ✓
```

### @tc.desc

测试用例描述，说明测试验证的内容。

**规则**：
- 简明扼要，描述测试目的
- 使用中文或英文
- 包含：测试对象 + 测试场景 + 预期结果

**示例**：

```cpp
/*
 * @tc.desc: 验证加法功能正常情况
 */
/*
 * @tc.desc: 验证除法功能除零异常处理
 */
/*
 * @tc.desc: verify app info is not null
 */
```

### @tc.type

测试类型，标识测试类别。

**可选值**：

| 类型编码 | 类型名称 | 说明 |
|----------|----------|------|
| `FUNC` | 功能测试 | 验证功能正确性 |
| `PERF` | 性能测试 | 验证性能指标 |
| `RELI` | 可靠性测试 | 验证稳定性、可靠性 |
| `SECU` | 安全测试 | 验证安全性 |
| `FUZZ` | 模糊测试 | 模糊测试用例 |

**示例**：

```cpp
/*
 * @tc.type: FUNC   // 功能测试
 */
/*
 * @tc.type: PERF   // 性能测试
 */
/*
 * @tc.type: SECU   // 安全测试
 */
```

### @tc.require

需求编号或问题编号，追溯测试来源。

**可选格式**：

| 格式 | 示例 | 说明 |
|------|------|------|
| Issue 编号 | `issueI56WJ7` | Gitee Issue 编号 |
| AR 编号 | `AR0001` | 架构需求编号 |
| SR 编号 | `SR0001` | 系统需求编号 |

**规则**：
- 格式必须以 `issue`、`AR` 或 `SR` 开头
- Issue 编号格式：`issue` + Gitee Issue ID

**示例**：

```cpp
/*
 * @tc.require: issueI56WJ7    // Issue 编号
 */
/*
 * @tc.require: AR0001         // 架构需求
 */
/*
 * @tc.require: SR0001         // 系统需求
 */
```

## 文件头注释

测试文件必须包含版权和 License 注释：

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

**重要**：
- 新建文件使用当前年份
- 修改现有文件保留原有年份

## 完整注释示例

### 功能测试注释

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * ...
 */

#include <gtest/gtest.h>
#include "calculator.h"

class CalculatorTest : public testing::Test {
public:
    static void SetUpTestCase();
    static void TearDownTestCase();
    void SetUp();
    void TearDown();
};

/*
 * @tc.name: Add_001
 * @tc.desc: 验证加法功能正常输入情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
{
    int result = Add(10, 5);
    EXPECT_EQ(result, 15);
}

/*
 * @tc.name: Add_002
 * @tc.desc: 验证加法功能边界溢出情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, Add_002, TestSize.Level2)
{
    int result = Add(INT_MAX, 1);
    EXPECT_EQ(result, INT_MAX);  // 预期溢出保护
}

/*
 * @tc.name: Divide_001
 * @tc.desc: 验证除法功能除零异常处理
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, Divide_001, TestSize.Level2)
{
    int result = Divide(10, 0);
    EXPECT_EQ(result, -1);  // 预期返回错误码
}
```

### 性能测试注释

```cpp
/*
 * @tc.name: ProcessPerformance_001
 * @tc.desc: 验证数据处理性能达标
 * @tc.type: PERF
 * @tc.require: AR0001
 */
HWTEST_F(DataProcessorTest, ProcessPerformance_001, TestSize.Level2)
{
    auto start = std::chrono::high_resolution_clock::now();
    ProcessLargeData(1000);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    EXPECT_LT(duration.count(), 100);  // 预期小于 100ms
}
```

### 多线程测试注释

```cpp
/*
 * @tc.name: ConcurrentAccess_001
 * @tc.desc: 验证多线程并发访问安全性
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWMTEST_F(CalculatorTest, ConcurrentAccess_001, TestSize.Level2, 4)
{
    int result = calculator_->Add(1, 1);
    EXPECT_EQ(result, 2);
}
```

## 注释检查要点

### 必填项检查

| 字段 | 必填性 | 检查内容 |
|------|--------|----------|
| @tc.name | ✅ 必填 | 与用例名一致 |
| @tc.desc | ✅ 必填 | 描述清晰 |
| @tc.type | ✅ 必填 | 使用标准编码 |
| @tc.require | ✅ 必填 | 格式正确 |

### 常见错误

```cpp
// ❌ 错误：缺少 @tc.require
/*
 * @tc.name: Add_001
 * @tc.desc: 验证加法功能
 * @tc.type: FUNC
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)

// ❌ 错误：@tc.require 格式错误
/*
 * @tc.require: I56WJ7  // 缺少 issue 前缀
 */

// ❌ 错误：@tc.name 与用例名不一致
/*
 * @tc.name: add_001  // 小写，应大写
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)

// ❌ 错误：版权年份错误
// Copyright (c) 2021  // 新文件应使用当前年份
```

## 自动化工具解析

@tc 注释用于自动化工具解析：

- **测试报告生成**：提取 @tc.desc 生成报告
- **需求追溯**：通过 @tc.require 关联需求
- **测试分类**：通过 @tc.type 分类统计

## 相关文档

- [naming-convention.md](naming-convention.md) - 命名规范
- [test-macro.md](test-macro.md) - 测试宏详细用法
- [test-examples.md](test-examples.md) - 测试用例示例