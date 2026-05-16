# 测试宏详细用法

## 概述

OpenHarmony 在 GTest 基础上扩展了测试宏，增加了测试等级参数和多线程支持。

## 测试宏列表

| 宏                       | 基础 GTest | 参数说明                         | 适用场景               |
| ----------------------- | -------- | ---------------------------- | ------------------ |
| `HWTEST(A, B, C)`       | TEST()   | A: 测试套名, B: 用例名, C: 等级       | 不依赖 Setup/Teardown |
| `HWTEST_F(A, B, C)`     | TEST_F() | A: 测试类名, B: 用例名, C: 等级       | 需要 Setup/Teardown  |
| `HWMTEST_F(A, B, C, D)` | -        | A: 类名, B: 用例名, C: 等级, D: 线程数 | 多线程测试              |
| `HWTEST_P(A, B, C)`     | TEST_P() | A: 类名, B: 用例名, C: 等级         | 参数化测试              |

## HWTEST 基础用法

### 适用场景

- 独立的测试用例
- 不需要共享数据
- 不需要 Setup/Teardown

### 示例

```cpp
/*
 * @tc.name: SimpleTest_Add_001
 * @tc.desc: 验证基础计算功能
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST(SimpleTest, SimpleTest_Add_001, TestSize.Level1)
{
    int result = 1 + 2;
    EXPECT_EQ(result, 3);
}

/*
 * @tc.name: SimpleTest_StringLen_001
 * @tc.desc: 验证字符串操作
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST(SimpleTest, SimpleTest_StringLen_001, TestSize.Level1)
{
    std::string str = "hello";
    EXPECT_EQ(str.length(), static_cast<size_t>(5));
}
```

## HWTEST_F 详细用法

### 适用场景

- 需要在测试前后初始化/清理资源
- 多个测试用例共享测试数据
- 需要创建测试对象

### 测试类定义

```cpp
#include <gtest/gtest.h>
#include "calculator.h"

class CalculatorTest : public testing::Test {
public:
    // 所有测试前执行一次
    static void SetUpTestCase();
    // 所有测试后执行一次
    static void TearDownTestCase();

    // 每个测试前执行
    void SetUp() override;
    // 每个测试后执行
    void TearDown() override;

    // 测试数据成员
    Calculator* calculator_;
};

void CalculatorTest::SetUpTestCase()
{
    GTEST_LOG_(INFO) << "CalculatorTest SetUpTestCase";
    // 初始化共享资源
}

void CalculatorTest::TearDownTestCase()
{
    GTEST_LOG_(INFO) << "CalculatorTest TearDownTestCase";
    // 清理共享资源
}

void CalculatorTest::SetUp()
{
    calculator_ = new Calculator();
}

void CalculatorTest::TearDown()
{
    delete calculator_;
    calculator_ = nullptr;
}
```

### 测试用例编写

```cpp
/*
 * @tc.name: CalculatorTest_Add_001
 * @tc.desc: 验证加法功能正常情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_Add_001, TestSize.Level1)
{
    // Step 1: 调用函数获取结果
    int result = calculator_->Add(10, 5);

    // Step 2: 使用断言验证结果
    EXPECT_EQ(result, 15);
}

/*
 * @tc.name: CalculatorTest_Add_002
 * @tc.desc: 验证加法功能负数情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_Add_002, TestSize.Level2)
{
    int result = calculator_->Add(-3, 7);
    EXPECT_EQ(result, 4);
}

/*
 * @tc.name: CalculatorTest_Divide_001
 * @tc.desc: 验证除法功能正常情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_Divide_001, TestSize.Level1)
{
    int result = calculator_->Divide(10, 2);
    EXPECT_EQ(result, 5);
}

/*
 * @tc.name: CalculatorTest_Divide_002
 * @tc.desc: 验证除法功能除零异常
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_Divide_002, TestSize.Level2)
{
    // 除零应返回错误码或抛出异常
    int result = calculator_->Divide(10, 0);
    EXPECT_EQ(result, -1); // 假设 -1 为错误码
}
```

## HWMTEST_F 多线程测试

### 适用场景

- 测试并发安全性
- 验证多线程场景下的行为
- 性能压力测试

### 基础用法

```cpp
/*
 * @tc.name: CalculatorTest_ConcurrentAccess_001
 * @tc.desc: 验证多线程并发访问安全性
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWMTEST_F(CalculatorTest, CalculatorTest_ConcurrentAccess_001, TestSize.Level2, 4)
{
    // 4 个线程并发执行此测试体
    int result = calculator_->Add(1, 1);
    EXPECT_EQ(result, 2);
}
```

### 动态线程数

使用 `SET_THREAD_NUM` 和 `GTEST_RUN_TASK`：

> **注意**：`GTEST_RUN_TASK` 只接受函数名（无参数的可调用对象）作为参数。
> 如果需要在任务中访问测试类的成员变量，应通过全局变量或 lambda 捕获来传递。

```cpp
// 全局指针，用于在 GTEST_RUN_TASK 中访问测试对象
static Calculator* g_calculator = nullptr;

// 定义测试函数（无参数，由 GTEST_RUN_TASK 调用）
void ConcurrentTestFunc()
{
    // 通过全局变量访问测试对象
    int result = g_calculator->Add(1, 1);
    EXPECT_EQ(result, 2);
}

/*
 * @tc.name: CalculatorTest_DynamicThread_001
 * @tc.desc: 验证动态线程数设置
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_DynamicThread_001, TestSize.Level2)
{
    g_calculator = calculator_; // 将成员指针赋给全局变量
    SET_THREAD_NUM(6); // 设置线程数为 6
    GTEST_LOG_(INFO) << "CalculatorTest_DynamicThread_001 BEGIN";
    GTEST_RUN_TASK(ConcurrentTestFunc); // 启动多线程执行
    GTEST_LOG_(INFO) << "CalculatorTest_DynamicThread_001 END";
}
```

### 使用 Lambda 替代全局变量

如果不想使用全局变量，可以利用 `GTEST_RUN_TASK` 结合 lambda 的方式（需要通过包装函数间接调用）：

```cpp
// 定义一个 std::function 全局变量来捕获上下文
static std::function<void()> g_task;

void TaskWrapper()
{
    g_task(); // 调用捕获了上下文的 lambda
}

/*
 * @tc.name: CalculatorTest_LambdaThread_001
 * @tc.desc: 使用 lambda 捕获测试对象进行多线程测试
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_LambdaThread_001, TestSize.Level2)
{
    Calculator* calc = calculator_;
    g_task = [calc]() {
        int result = calc->Add(2, 3);
        EXPECT_EQ(result, 5);
    };
    SET_THREAD_NUM(4);
    GTEST_RUN_TASK(TaskWrapper);
}
```

### 任务注册模式

使用 `MTEST_ADD_TASK` 和 `MTEST_POST_RUN`：

```cpp
/*
 * @tc.name: CalculatorTest_RegisterTasks_001
 * @tc.desc: 验证任务注册和统一执行
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, CalculatorTest_RegisterTasks_001, TestSize.Level2)
{
    // 注册多个线程任务（不立即执行）
    MTEST_ADD_TASK(0, TaskFuncA);
    MTEST_ADD_TASK(1, TaskFuncB);
    MTEST_ADD_TASK(RANDOM_THREAD_ID, TaskFuncC); // 随机线程ID

    // 统一执行所有注册的任务
    MTEST_POST_RUN();
}
```

## HWTEST_P 参数化测试

### 适用场景

- 同一逻辑，不同输入参数
- 批量验证多种输入组合

### 定义参数化测试类

```cpp
#include <gtest/gtest.h>
#include "calculator.h"

// 参数结构
struct TestParams {
    int input1;
    int input2;
    int expected;
};

class ParamTest : public testing::TestWithParam<TestParams> {
public:
    static void SetUpTestCase() {}
    static void TearDownTestCase() {}
};
```

### 参数实例化

#### INSTANTIATE_TEST_SUITE_P（推荐，GTest 1.11+）

`INSTANTIATE_TEST_SUITE_P` 是 GTest 1.11 及以上版本推荐的方式：

```cpp
INSTANTIATE_TEST_SUITE_P(
    ParamValues,
    ParamTest,
    testing::Values(
        TestParams{1, 2, 3},
        TestParams{10, 5, 15},
        TestParams{-3, 7, 4}
    )
);
```

#### INSTANTIATE_TEST_CASE_P（已废弃但仍广泛使用）

> **注意**：`INSTANTIATE_TEST_CASE_P` 在 GTest 1.11+ 中已被标记为废弃（deprecated），
> 推荐使用 `INSTANTIATE_TEST_SUITE_P`。但 OpenHarmony 当前代码库中仍大量使用
> `INSTANTIATE_TEST_CASE_P`，两种写法在功能上完全等价，编译器均支持。
> 新代码建议优先使用 `INSTANTIATE_TEST_SUITE_P`。

```cpp
// 旧写法（OpenHarmony 现有代码中常见）
INSTANTIATE_TEST_CASE_P(
    ParamValues,
    ParamTest,
    testing::Values(
        TestParams{1, 2, 3},
        TestParams{10, 5, 15},
        TestParams{-3, 7, 4}
    )
);

// 新写法（GTest 1.11+ 推荐）
INSTANTIATE_TEST_SUITE_P(
    ParamValues,
    ParamTest,
    testing::Values(
        TestParams{1, 2, 3},
        TestParams{10, 5, 15},
        TestParams{-3, 7, 4}
    )
);
```

### 参数化测试用例

```cpp
/*
 * @tc.name: ParamTest_ParamAdd_001
 * @tc.desc: 验证加法功能参数化测试
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_P(ParamTest, ParamTest_ParamAdd_001, TestSize.Level1)
{
    TestParams params = GetParam();
    int result = params.input1 + params.input2;
    EXPECT_EQ(result, params.expected);
}
```

## 测试等级参数

### testing::ext 命名空间

OpenHarmony 的测试等级常量定义在 `testing::ext` 命名空间中。使用时需要：

- 在文件开头声明 `using namespace testing::ext;`，或
- 使用完整限定名 `testing::ext::TestSize.Level1`

推荐在测试文件中使用 `using namespace testing::ext;` 声明：

```cpp
#include <gtest/gtest.h>
#include <gtest/hwext/gtest-ext.h>  // OpenHarmony 扩展头文件

using namespace testing::ext;

// 之后可直接使用 TestSize.Level1
HWTEST(MyTest, MyTest_Foo_001, TestSize.Level1)
{
    EXPECT_TRUE(true);
}
```

如果不使用 `using namespace` 声明，则需要完整限定名：

```cpp
// 不使用 using namespace 时的完整写法
HWTEST(MyTest, MyTest_Foo_001, testing::ext::TestSize.Level1)
{
    EXPECT_TRUE(true);
}
```

### TestSize 定义

```cpp
testing::ext::TestSize.Level0  // 冒烟测试（门禁）
testing::ext::TestSize.Level1  // 基础测试
testing::ext::TestSize.Level2  // 重要测试
testing::ext::TestSize.Level3  // 一般测试
testing::ext::TestSize.Level4  // 稀少测试
```

> 注：使用 `using namespace testing::ext;` 后可简写为 `TestSize.Level0` 等。

### 选择原则

| 等级     | 选择依据           |
| ------ | -------------- |
| Level0 | 核心功能，必须通过门禁    |
| Level1 | 常用功能，正常输入场景    |
| Level2 | 异常处理、边界条件、错误场景 |
| Level3 | 完整功能覆盖、辅助功能    |
| Level4 | 极端条件、死亡测试      |

详见 [test-level.md](test-level.md)。

## 命名规范

### 测试套命名

- 匹配被测模块/类名
- 使用 CamelCase 风格
- 示例：`CalculatorTest`, `UtilityTest`, `StateRegistryTest`

### 测试用例命名

- 格式：`ClassName_MethodName_SequenceNumber`
- 序号：3 位数字，从 001 开始
- 示例：`CalculatorTest_Add_001`, `CalculatorTest_Divide_001`

> 注：对于 HWTEST（无类名），使用 `SuiteName_MethodName_SequenceNumber` 格式，
> 如 `SimpleTest_Add_001`。

详见 [naming-convention.md](naming-convention.md)。

## 注意事项

1. **必须添加注释**：每个测试用例必须有 @tc 注释
2. **等级必须填写**：测试等级是必填参数
3. **断言必须有**：每个测试至少有一个断言验证结果
4. **版权年份**：新文件版权年份为当前年份
5. **头文件引用**：系统头文件使用 `<>` 引用（如 `<gtest/gtest.h>`），项目头文件使用 `""` 引用（如 `"calculator.h"`）
6. **避免 using namespace std**：统一使用 `std::` 前缀，不要在文件中写 `using namespace std;`

### GTEST_LOG_ 日志宏

GTest 提供了 `GTEST_LOG_` 宏用于在测试中输出日志信息，支持三个级别：

```cpp
// 信息级别 - 用于输出测试流程信息
GTEST_LOG_(INFO) << "TestCase start";

// 警告级别 - 用于输出非预期但非致命的情况
GTEST_LOG_(WARNING) << "Unexpected value";

// 错误级别 - 用于输出严重问题
GTEST_LOG_(ERROR) << "Critical failure";
```

使用建议：

- 在 `SetUpTestCase` / `TearDownTestCase` 中使用 `GTEST_LOG_(INFO)` 记录生命周期事件
- 在测试体中使用 `GTEST_LOG_(INFO)` 记录关键步骤
- 避免过度使用日志，以免影响测试输出的可读性
- 不要使用 `printf` 或 `std::cout`，统一使用 `GTEST_LOG_`

## 相关文档

- [comment-standard.md](comment-standard.md) - 注释标准
- [test-level.md](test-level.md) - 测试等级详解
- [assertion-guide.md](assertion-guide.md) - 断言使用指南
- [test-examples.md](test-examples.md) - 测试用例示例
