# 测试等级详解

## 概述

OpenHarmony 定义了 5 个测试等级（Level0 - Level4），用于标识测试用例的重要程度和执行优先级。

## 测试等级定义

| 等级 | 名称 | 门禁 | 执行优先级 | 说明 |
|------|------|------|------------|------|
| Level0 | 冒烟测试 | ✅ 是 | 最高 | 核心功能，必须通过 |
| Level1 | 基础测试 | ✅ 是 | 高 | 基础功能验证 |
| Level2 | 重要测试 | ❌ 否 | 中 | 异常/边界场景 |
| Level3 | 一般测试 | ❌ 否 | 低 | 完整功能覆盖 |
| Level4 | 稀少测试 | ❌ 否 | 最低 | 极端条件 |

## 等级选择原则

### Level0 - 冒烟测试（门禁）

**适用场景**：
- 系统核心功能验证
- 必须通过的用例
- CI/CD 门禁检查

**选择依据**：
- 功能失败会导致系统不可用
- 最常用的功能路径
- 系统启动/初始化关键流程

**示例**：

```cpp
/*
 * @tc.name: Initialize_001
 * @tc.desc: 验证系统初始化成功
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(SystemTest, Initialize_001, TestSize.Level0)
{
    bool result = SystemInitialize();
    EXPECT_TRUE(result);
}

/*
 * @tc.name: CoreService_001
 * @tc.desc: 验证核心服务启动
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(ServiceTest, CoreService_001, TestSize.Level0)
{
    auto service = GetCoreService();
    EXPECT_NE(service, nullptr);
}
```

### Level1 - 基础测试

**适用场景**：
- 常用功能正常路径
- 基础 API 功能验证
- 标准输入输出场景

**选择依据**：
- 功能重要但非致命
- 用户高频使用场景
- 正常参数输入

**示例**：

```cpp
/*
 * @tc.name: Add_001
 * @tc.desc: 验证加法功能正常情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
{
    int result = calculator_->Add(10, 5);
    EXPECT_EQ(result, 15);
}

/*
 * @tc.name: GetValue_001
 * @tc.desc: 验证获取配置值正常情况
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(ConfigTest, GetValue_001, TestSize.Level1)
{
    std::string value = config->GetValue("key");
    EXPECT_EQ(value, "expected_value");
}
```

### Level2 - 重要测试

**适用场景**：
- 异常处理验证
- 边界条件测试
- 错误场景覆盖

**选择依据**：
- 异常输入处理
- 边界值验证
- 错误恢复机制

**示例**：

```cpp
/*
 * @tc.name: Divide_001
 * @tc.desc: 验证除法功能除零异常处理
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, Divide_001, TestSize.Level2)
{
    int result = calculator_->Divide(10, 0);
    EXPECT_EQ(result, -1);  // 错误码
}

/*
 * @tc.name: GetValue_002
 * @tc.desc: 验证获取配置值空键处理
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(ConfigTest, GetValue_002, TestSize.Level2)
{
    std::string value = config->GetValue("");
    EXPECT_EQ(value, "");  // 空键返回空值
}

/*
 * @tc.name: Boundary_001
 * @tc.desc: 验证数值边界溢出保护
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, Boundary_001, TestSize.Level2)
{
    int result = calculator_->Add(INT_MAX, 1);
    EXPECT_EQ(result, INT_MAX);  // 溢出保护
}
```

### Level3 - 一般测试

**适用场景**：
- 完整功能覆盖
- 辅助功能验证
- 扩展场景测试

**选择依据**：
- 非核心功能
- 低频使用场景
- 特殊参数组合

**示例**：

```cpp
/*
 * @tc.name: ComplexCalculation_001
 * @tc.desc: 验证复杂计算场景
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(CalculatorTest, ComplexCalculation_001, TestSize.Level3)
{
    int result = calculator_->ComplexOperation(100, 50, 25);
    EXPECT_EQ(result, 175);
}

/*
 * @tc.name: ExtendedFeature_001
 * @tc.desc: 验证扩展功能
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(FeatureTest, ExtendedFeature_001, TestSize.Level3)
{
    bool result = feature->ExtendedOperation();
    EXPECT_TRUE(result);
}
```

### Level4 - 稀少测试

**适用场景**：
- 极端条件验证
- 死亡测试（Death Test）
- 压力测试

**选择依据**：
- 极端参数值
- 资源耗尽场景
- 崩溃恢复测试

**示例**：

```cpp
/*
 * @tc.name: ExtremeMemory_001
 * @tc.desc: 验证内存耗尽处理
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(MemoryTest, ExtremeMemory_001, TestSize.Level4)
{
    // 分配大量内存测试
    bool result = memoryManager->HandleExhaustion();
    EXPECT_TRUE(result);
}

/*
 * @tc.name: CrashRecovery_001
 * @tc.desc: 验证崩溃恢复机制
 * @tc.type: RELI
 * @tc.require: issueI56WJ7
 */
HWTEST_F(RecoveryTest, CrashRecovery_001, TestSize.Level4)
{
    // 模拟崩溃恢复
    EXPECT_TRUE(system->RecoverFromCrash());
}
```

## 等级选择流程

```
确定测试场景
     │
     ↓
┌─────────────────────────────────────────────┐
│ 功能失败是否导致系统不可用？                    │
│   Yes → Level0                               │
│   No  → 继续                                  │
└─────────────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────────┐
│ 是否为常用功能的正常路径？                      │
│   Yes → Level1                               │
│   No  → 继续                                  │
└─────────────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────────┐
│ 是否为异常处理或边界条件？                      │
│   Yes → Level2                               │
│   No  → 继续                                  │
└─────────────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────────┐
│ 是否为完整功能覆盖或辅助功能？                   │
│   Yes → Level3                               │
│   No  → Level4                               │
└─────────────────────────────────────────────┘
```

## 测试等级与覆盖率

| 等级 | 覆盖率贡献 | 说明 |
|------|------------|------|
| Level0 | 高 | 核心路径覆盖 |
| Level1 | 高 | 主路径覆盖 |
| Level2 | 中 | 分支覆盖 |
| Level3 | 低 | 补充覆盖 |
| Level4 | 低 | 极端覆盖 |

**建议比例**：
- Level0: 10-20%（核心功能）
- Level1: 30-40%（正常场景）
- Level2: 20-30%（异常/边界）
- Level3: 10-20%（补充）
- Level4: 5-10%（极端）

## 门禁规则

### Level0 和 Level1

- 必须通过 CI 门禁
- 用例失败会阻塞提交
- 需要及时修复

### Level2 - Level4

- 不阻塞门禁
- 建议尽快修复
- 作为质量指标

## 等级分配示例

假设测试 Calculator 类：

| 函数 | 测试场景 | 等级 |
|------|----------|------|
| Initialize | 初始化成功 | Level0 |
| Initialize | 初始化失败 | Level2 |
| Add | 正常加法 | Level1 |
| Add | 边界溢出 | Level2 |
| Add | 负数相加 | Level2 |
| Divide | 正常除法 | Level1 |
| Divide | 除零异常 | Level2 |
| Power | 高精度计算 | Level3 |
| Factorial | 大数溢出 | Level4 |

## 相关文档

- [test-macro.md](test-macro.md) - 测试宏详细用法
- [comment-standard.md](comment-standard.md) - 注释标准
- [test-case-spec.md](test-case-spec.md) - 测试用例规范