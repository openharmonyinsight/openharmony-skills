# GTest 断言使用指南

## 概述

OpenHarmony 测试框架使用 GTest (Google Test) 的断言库进行结果验证。断言是测试用例的核心，用于验证实际结果是否符合预期。

## 断言分类

| 类型 | 失败行为 | 说明 |
|------|----------|------|
| `ASSERT_*` | 终止当前测试 | 用于前置条件检查 |
| `EXPECT_*` | 继续执行测试 | 用于结果验证 |

**选择原则**：
- 前置条件失败使用 `ASSERT_*`（如指针为空）
- 结果验证使用 `EXPECT_*`（可收集多个失败）

## 常用断言列表

### 相等性断言

| 断言 | 说明 |
|------|------|
| `ASSERT_EQ(val1, val2)` | val1 == val2（终止） |
| `EXPECT_EQ(val1, val2)` | val1 == val2（继续） |
| `ASSERT_NE(val1, val2)` | val1 != val2（终止） |
| `EXPECT_NE(val1, val2)` | val1 != val2（继续） |

### 示例

```cpp
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
{
    int result = calculator_->Add(10, 5);
    EXPECT_EQ(result, 15);  // 验证结果相等
}

HWTEST_F(PointerTest, GetObject_001, TestSize.Level1)
{
    auto obj = manager->GetObject();
    ASSERT_NE(obj, nullptr);  // 指针不为空是前置条件，失败终止
    EXPECT_EQ(obj->GetValue(), 100);  // 继续验证其他结果
}
```

### 布尔断言

| 断言 | 说明 |
|------|------|
| `ASSERT_TRUE(condition)` | condition 为 true（终止） |
| `EXPECT_TRUE(condition)` | condition 为 true（继续） |
| `ASSERT_FALSE(condition)` | condition 为 false（终止） |
| `EXPECT_FALSE(condition)` | condition 为 false（继续） |

### 示例

```cpp
HWTEST_F(ConfigTest, IsEnabled_001, TestSize.Level1)
{
    bool enabled = config->IsEnabled();
    EXPECT_TRUE(enabled);  // 验证配置启用
}

HWTEST_F(ValidatorTest, IsValid_001, TestSize.Level2)
{
    bool valid = validator->CheckInvalidInput("");
    EXPECT_FALSE(valid);  // 验证无效输入返回 false
}
```

### 比较断言

| 断言 | 说明 |
|------|------|
| `ASSERT_GT(val1, val2)` | val1 > val2 |
| `EXPECT_GT(val1, val2)` | val1 > val2 |
| `ASSERT_LT(val1, val2)` | val1 < val2 |
| `EXPECT_LT(val1, val2)` | val1 < val2 |
| `ASSERT_GE(val1, val2)` | val1 >= val2 |
| `EXPECT_GE(val1, val2)` | val1 >= val2 |
| `ASSERT_LE(val1, val2)` | val1 <= val2 |
| `EXPECT_LE(val1, val2)` | val1 <= val2 |

### 示例

```cpp
HWTEST_F(PerformanceTest, ResponseTime_001, TestSize.Level2)
{
    int time_ms = MeasureResponseTime();
    EXPECT_LT(time_ms, 100);  // 响应时间小于 100ms
}

HWTEST_F(MemoryTest, Allocation_001, TestSize.Level1)
{
    int allocated = memory->GetAllocatedSize();
    EXPECT_GE(allocated, 0);  // 已分配内存 >= 0
}
```

### 字符串断言

| 断言 | 说明 |
|------|------|
| `ASSERT_STREQ(str1, str2)` | C 字符串相等 |
| `EXPECT_STREQ(str1, str2)` | C 字符串相等 |
| `ASSERT_STRNE(str1, str2)` | C 字符串不等 |
| `EXPECT_STRNE(str1, str2)` | C 字符串不等 |
| `ASSERT_STRCASEEQ(str1, str2)` | C 字符串相等（忽略大小写） |
| `EXPECT_STRCASEEQ(str1, str2)` | C 字符串相等（忽略大小写） |

### 示例

```cpp
HWTEST_F(StringTest, GetName_001, TestSize.Level1)
{
    const char* name = obj->GetName();
    EXPECT_STREQ(name, "Calculator");  // C 字符串比较
}

HWTEST_F(StringTest, GetName_002, TestSize.Level1)
{
    std::string name = obj->GetName();
    EXPECT_EQ(name, "Calculator");  // std::string 使用 EXPECT_EQ
}
```

### 浮点数断言

| 断言 | 说明 |
|------|------|
| `ASSERT_FLOAT_EQ(val1, val2)` | 浮点数近似相等 |
| `EXPECT_FLOAT_EQ(val1, val2)` | 浮点数近似相等 |
| `ASSERT_DOUBLE_EQ(val1, val2)` | 双精度近似相等 |
| `EXPECT_DOUBLE_EQ(val1, val2)` | 双精度近似相等 |
| `ASSERT_NEAR(val1, val2, abs_error)` | 差值在范围内 |
| `EXPECT_NEAR(val1, val2, abs_error)` | 差值在范围内 |

### 示例

```cpp
HWTEST_F(MathTest, Calculate_001, TestSize.Level1)
{
    float result = math->CalculateFloat(1.0f, 2.0f);
    EXPECT_FLOAT_EQ(result, 3.0f);  // 浮点数近似相等
}

HWTEST_F(MathTest, Calculate_002, TestSize.Level1)
{
    double result = math->CalculateDouble(1.5, 2.5);
    EXPECT_NEAR(result, 4.0, 0.001);  // 差值不超过 0.001
}
```

### 异常断言

| 断言 | 说明 |
|------|------|
| `ASSERT_THROW(stmt, exception_type)` | 语句抛出指定异常 |
| `EXPECT_THROW(stmt, exception_type)` | 语句抛出指定异常 |
| `ASSERT_NO_THROW(stmt)` | 语句不抛出异常 |
| `EXPECT_NO_THROW(stmt)` | 语句不抛出异常 |
| `ASSERT_ANY_THROW(stmt)` | 语句抛出任意异常 |
| `EXPECT_ANY_THROW(stmt)` | 语句抛出任意异常 |

### 示例

```cpp
HWTEST_F(ExceptionTest, Divide_001, TestSize.Level2)
{
    EXPECT_THROW(calculator_->Divide(10, 0), std::runtime_error);
}

HWTEST_F(ExceptionTest, SafeOperation_001, TestSize.Level1)
{
    EXPECT_NO_THROW(calculator_->Add(1, 2));  // 正常操作不抛异常
}
```

## 断言使用场景

### 前置条件检查

使用 `ASSERT_*` 确保前置条件满足：

```cpp
HWTEST_F(DatabaseTest, Query_001, TestSize.Level1)
{
    // 前置条件：连接必须成功
    ASSERT_TRUE(db->Connect());
    
    // 前置条件：指针必须有效
    auto result = db->Query("SELECT * FROM table");
    ASSERT_NE(result, nullptr);
    
    // 结果验证：检查查询结果
    EXPECT_EQ(result->Count(), 100);
    EXPECT_TRUE(result->IsValid());
}
```

### 多结果验证

使用 `EXPECT_*` 验证多个结果：

```cpp
HWTEST_F(ObjectTest, Create_001, TestSize.Level1)
{
    auto obj = factory->CreateObject();
    
    // 验证多个属性（失败不终止）
    EXPECT_NE(obj, nullptr);
    EXPECT_EQ(obj->GetType(), "Calculator");
    EXPECT_TRUE(obj->IsValid());
    EXPECT_GT(obj->GetVersion(), 0);
}
```

### 边界值验证

```cpp
HWTEST_F(BoundaryTest, Range_001, TestSize.Level2)
{
    int min = obj->GetMinValue();
    int max = obj->GetMaxValue();
    
    EXPECT_EQ(min, 0);
    EXPECT_EQ(max, 100);
    EXPECT_GE(max, min);  // max >= min
}
```

### 空值检查

```cpp
HWTEST_F(NullTest, HandleNull_001, TestSize.Level2)
{
    auto result = processor->Process(nullptr);
    
    // 空输入应返回错误
    EXPECT_FALSE(result.IsValid());
    EXPECT_EQ(result.GetErrorCode(), ERROR_NULL_INPUT);
}
```

## 自定义失败消息

断言可附加自定义消息：

```cpp
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
{
    int result = calculator_->Add(10, 5);
    EXPECT_EQ(result, 15) << "Add function failed for inputs 10 and 5";
}
```

## 断言最佳实践

### 1. 前置条件用 ASSERT

```cpp
// ✓ 正确
ASSERT_NE(obj, nullptr);  // 空指针后续操作无意义
EXPECT_EQ(obj->GetValue(), 100);

// ❌ 错误
EXPECT_NE(obj, nullptr);  // 即使为空也继续执行，可能导致崩溃
obj->GetValue();  // 空指针崩溃
```

### 2. 结果验证用 EXPECT

```cpp
// ✓ 正确：收集所有失败
EXPECT_EQ(value1, expected1);
EXPECT_EQ(value2, expected2);
EXPECT_EQ(value3, expected3);

// ❌ 不推荐：只看到第一个失败
ASSERT_EQ(value1, expected1);  // 失败后终止
EXPECT_EQ(value2, expected2);  // 不执行
```

### 3. 每个测试至少一个断言

```cpp
// ✓ 正确
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
{
    int result = calculator_->Add(1, 2);
    EXPECT_EQ(result, 3);  // 有断言验证
}

// ❌ 错误：无断言
HWTEST_F(CalculatorTest, Add_002, TestSize.Level1)
{
    calculator_->Add(1, 2);  // 无结果验证
}
```

### 4. 断言顺序合理

```cpp
HWTEST_F(DatabaseTest, Insert_001, TestSize.Level1)
{
    // 1. 前置条件
    ASSERT_TRUE(db->Connect());
    
    // 2. 执行操作
    bool inserted = db->Insert(data);
    
    // 3. 验证结果
    EXPECT_TRUE(inserted);
    
    // 4. 验证副作用
    EXPECT_EQ(db->Count(), oldCount + 1);
}
```

## 断言速查表

| 验证内容 | 推荐断言 |
|----------|----------|
| 数值相等 | `EXPECT_EQ(a, b)` |
| 数值不等 | `EXPECT_NE(a, b)` |
| 条件为真 | `EXPECT_TRUE(cond)` |
| 条件为假 | `EXPECT_FALSE(cond)` |
| 大于 | `EXPECT_GT(a, b)` |
| 小于 | `EXPECT_LT(a, b)` |
| 字符串相等 | `EXPECT_STREQ(s1, s2)` |
| 浮点近似 | `EXPECT_FLOAT_EQ(a, b)` |
| 指针非空（前置） | `ASSERT_NE(p, nullptr)` |
| 抛出异常 | `EXPECT_THROW(stmt, ex)` |

## 相关文档

- [test-macro.md](test-macro.md) - 测试宏详细用法
- [test-examples.md](test-examples.md) - 测试用例示例