# OpenHarmony 测试框架速查表

## 测试宏速查

### 宏选择决策

| 测试需求 | 选择宏 | 说明 |
|----------|--------|------|
| 无需初始化/清理 | `HWTEST` | 独立测试，不依赖 SetUp |
| 需要初始化/清理 | `HWTEST_F` | 需要测试类，使用 SetUp/TearDown |
| 多线程并发测试 | `HWMTEST_F` | 第4参数为线程数 |
| 参数化测试 | `HWTEST_P` | 多组输入数据 |

### 宏语法

| 宏 | 语法 | 示例 |
|----|------|------|
| HWTEST | `HWTEST(套名, 用例名, 等级)` | `HWTEST(MathTest, Add_001, Level1)` |
| HWTEST_F | `HWTEST_F(类名, 用例名, 等级)` | `HWTEST_F(CalculatorTest, Add_001, Level1)` |
| HWMTEST_F | `HWMTEST_F(类名, 用例名, 等级, 线程数)` | `HWMTEST_F(Test, Concurrent_001, Level2, 4)` |
| HWTEST_P | `HWTEST_P(类名, 用例名, 等级)` | `HWTEST_P(ParamTest, Add_001, Level1)` |

### 必要声明

```cpp
#include <gtest/gtest.h>
using namespace testing::ext;  // 必须，否则编译失败
```

---

## 测试等级速查

### 等级定义

| 等级 | 名称 | 门禁 | 场景 |
|------|------|------|------|
| Level0 | 冒烟测试 | ✅ 阻塞 | 系统核心功能、必须通过 |
| Level1 | 基础测试 | ✅ 阻塞 | 正常输入、高频场景 |
| Level2 | 重要测试 | ❌ 不阻塞 | 异常处理、边界条件 |
| Level3 | 一般测试 | ❌ 不阻塞 | 完整覆盖、辅助功能 |
| Level4 | 稀少测试 | ❌ 不阻塞 | 极端条件、死亡测试 |

### 等级选择决策树

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

### 常见场景等级分配

| 测试类型 | 推荐等级 |
|----------|----------|
| 系统初始化/核心服务 | Level0 |
| 正常输入验证 | Level1 |
| 空值/nullptr处理 | Level2 |
| 边界值(INT_MAX等) | Level2 |
| 错误码/异常返回 | Level2 |
| 完整功能组合 | Level3 |
| 内存耗尽/崩溃恢复 | Level4 |

---

## 测试类型速查 (@tc.type)

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| FUNC | 功能测试 | 验证功能正确性 |
| PERF | 性能测试 | 性能基准验证 |
| RELI | 可靠性测试 | 异常恢复、稳定性 |
| SECU | 安全测试 | 安全漏洞验证 |
| FUZZ | 模糊测试 | 输入鲁棒性 |

---

## 注释格式速查

### 必填注释

```cpp
/*
 * @tc.name: TestSuite_FunctionName_001
 * @tc.desc: 验证xxx功能xxx场景
 * @tc.type: FUNC
 * @tc.require: issueIxxxxx
 */
```

### 注释字段说明

| 字段 | 必填 | 格式 |
|------|------|------|
| @tc.name | ✅ | `TestSuite_FunctionName_001` |
| @tc.desc | ✅ | 描述测试场景 |
| @tc.type | ✅ | FUNC/PERF/RELI/SECU |
| @tc.require | ✅ | `issueIxxxxx` 或空 |
| @tc.author | ❌ | 作者名（可选） |

---

## 命名规范速查

| 命名对象 | 格式 | 示例 |
|----------|------|------|
| 测试文件 | `[Module]Test.cpp` | `CalculatorTest.cpp` |
| 测试类 | `[ModuleName]Test` | `CalculatorTest` |
| 测试用例 | `TestSuite_Function_001` | `CalculatorTest_Add_001` |
| 序号范围 | 001-999 | `Add_001`, `Add_002` |

---

## SetUp/TearDown速查

| 方法 | 执行时机 | 用途 |
|------|----------|------|
| SetUpTestCase() | 所有测试前一次 | 初始化共享资源 |
| TearDownTestCase() | 所有测试后一次 | 清理共享资源 |
| SetUp() | 每个测试前 | 初始化测试对象 |
| TearDown() | 每个测试后 | 清理测试对象 |

---

## 断言速查

### ASSERT vs EXPECT

| 类型 | 失败行为 | 使用场景 |
|------|----------|----------|
| ASSERT_* | 立即终止 | 前置条件检查 |
| EXPECT_* | 继续执行 | 结果验证 |

### 常用断言

| 断言 | 说明 | 示例 |
|------|------|------|
| ASSERT_TRUE(cond) | 条件必须为真 | `ASSERT_TRUE(ptr != nullptr)` |
| ASSERT_FALSE(cond) | 条件必须为假 | `ASSERT_FALSE(result)` |
| ASSERT_EQ(a, b) | 必须相等 | `ASSERT_EQ(size, 10)` |
| ASSERT_NE(a, b) | 必须不等 | `ASSERT_NE(ptr, nullptr)` |
| EXPECT_TRUE(cond) | 期望为真 | `EXPECT_TRUE(success)` |
| EXPECT_FALSE(cond) | 期望为假 | `EXPECT_FALSE(failed)` |
| EXPECT_EQ(a, b) | 期望相等 | `EXPECT_EQ(result, 15)` |
| EXPECT_NE(a, b) | 期望不等 | `EXPECT_NE(value, 0)` |
| EXPECT_STREQ(a, b) | 字符串相等 | `EXPECT_STREQ(str, "hello")` |

---

## 日志速查

| 宏 | 级别 | 用途 |
|----|------|------|
| GTEST_LOG_(INFO) | 信息 | 测试流程信息 |
| GTEST_LOG_(WARNING) | 警告 | 非预期情况 |
| GTEST_LOG_(ERROR) | 错误 | 严重问题 |

```cpp
GTEST_LOG_(INFO) << "Test case start";
```

---

## 快速模板

### HWTEST 模板（无SetUp）

```cpp
#include <gtest/gtest.h>
using namespace testing::ext;

HWTEST(MathTest, SimpleAdd_001, TestSize.Level1)
{
    EXPECT_EQ(1 + 2, 3);
}
```

### HWTEST_F 模板（有SetUp）

```cpp
#include <gtest/gtest.h>
#include "calculator.h"
using namespace testing::ext;

class CalculatorTest : public testing::Test {
public:
    static void SetUpTestCase() {}
    static void TearDownTestCase() {}
    void SetUp() override { calculator_ = new Calculator(); }
    void TearDown() override { delete calculator_; }
    Calculator* calculator_;
};

HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
{
    EXPECT_EQ(calculator_->Add(10, 5), 15);
}
```

### HWTEST_P 模板（参数化）

```cpp
#include <gtest/gtest.h>
using namespace testing::ext;

struct Params { int a; int b; int expected; };

class ParamTest : public testing::TestWithParam<Params> {};

INSTANTIATE_TEST_SUITE_P(
    Values,
    ParamTest,
    testing::Values(Params{1,2,3}, Params{10,5,15})
);

HWTEST_P(ParamTest, Add_001, TestSize.Level1)
{
    auto p = GetParam();
    EXPECT_EQ(p.a + p.b, p.expected);
}
```

### HWMTEST_F 模板（多线程）

```cpp
HWMTEST_F(ConcurrencyTest, ThreadSafe_001, TestSize.Level2, 4)
{
    EXPECT_EQ(obj_->ThreadSafeOp(), true);
}
```

---

## 常见错误速查

| 错误 | 原因 | 解决 |
|------|------|------|
| `'HWTEST' was not declared` | 缺少命名空间 | 添加 `using namespace testing::ext;` |
| `TestSize not found` | 缺少命名空间 | 添加 `using namespace testing::ext;` |
| `undefined reference to SetUp` | SetUp未实现 | 实现所有声明的SetUp/TearDown |
| 编译通过但无测试运行 | 用例名不规范 | 检查命名是否符合规范 |

---

## 相关文档

- [build-gn-config.md](build-gn-config.md) - BUILD.gn决策规则
- [naming-convention.md](naming-convention.md) - 命名规范详解
- [comment-standard.md](comment-standard.md) - 注释标准详解
- [assertion-gmock-guide.md](assertion-gmock-guide.md) - 断言与Mock指南
