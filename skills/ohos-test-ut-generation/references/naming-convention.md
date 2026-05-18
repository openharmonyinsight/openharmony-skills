# 命名规范详细说明

## 概述

OpenHarmony 测试用例命名遵循统一的规范，确保可读性和可维护性。

## 文件命名规范

### 测试源文件命名

**格式**：`[Module][SubModule]Test.cpp`

**规则**：

- 使用 CamelCase（驼峰命名）
- 以 `Test` 结尾
- 模块名对应被测模块名称

**示例**：

| 被测文件                 | 测试文件                    |
| -------------------- | ----------------------- |
| `calculator.cpp`     | `CalculatorTest.cpp`    |
| `utility.cpp`        | `UtilityTest.cpp`       |
| `state_registry.cpp` | `StateRegistryTest.cpp` |
| `dmabuf_heap.cpp`    | `DmabufHeapTest.cpp`    |
| `sensor_manager.cpp` | `SensorManagerTest.cpp` |

### 子模块命名

当模块有多个子功能时：

| 被测模块              | 测试文件                         |
| ----------------- | ---------------------------- |
| `calculator` (基础) | `CalculatorBaseTest.cpp`     |
| `calculator` (高级) | `CalculatorAdvancedTest.cpp` |
| `sensor` (管理器)    | `SensorManagerTest.cpp`      |
| `sensor` (数据处理)   | `SensorDataTest.cpp`         |

## 测试套命名规范

### HWTEST/HWTEST_F 测试套名

**格式**：`[ModuleName]Test`

**规则**：

- 与测试类名一致
- 使用 CamelCase
- 以 `Test` 结尾

**示例**：

```cpp
// 测试套名：CalculatorTest
class CalculatorTest : public testing::Test { ... };

HWTEST_F(CalculatorTest, Add_001, TestSize.Level1) { ... }

// 测试套名：UtilityTest（不使用 HWTEST_F）
HWTEST(UtilityTest, SimpleCheck_001, TestSize.Level1) { ... }
```

### 命名与被测模块对应

| 被测类/模块            | 测试套名                  |
| ----------------- | --------------------- |
| `Calculator`      | `CalculatorTest`      |
| `Utility`         | `UtilityTest`         |
| `StateManager`    | `StateManagerTest`    |
| `DmabufAllocator` | `DmabufAllocatorTest` |

## 测试用例命名规范

### 基本格式

**格式**：`[FunctionName]_[SequenceNumber]`

**规则**：

- 函数名使用 CamelCase
- 序号为 3 位数字，从 `001` 开始
- 同一函数的多个测试场景递增序号

**示例**：

```cpp
// 测试 Add 函数
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 正常情况
HWTEST_F(CalculatorTest, Add_002, TestSize.Level2)  // 边界情况
HWTEST_F(CalculatorTest, Add_003, TestSize.Level2)  // 异常情况

// 测试 Divide 函数
HWTEST_F(CalculatorTest, Divide_001, TestSize.Level1)  // 正常除法
HWTEST_F(CalculatorTest, Divide_002, TestSize.Level2)  // 除零异常
```

### 场景类型命名扩展

可在序号前添加场景标识：

```cpp
// 方式一：纯序号（推荐）
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 正常
HWTEST_F(CalculatorTest, Add_002, TestSize.Level2)  // 异常

// 方式二：场景前缀（可选）
HWTEST_F(CalculatorTest, Add_Normal_001, TestSize.Level1)
HWTEST_F(CalculatorTest, Add_Boundary_001, TestSize.Level2)
HWTEST_F(CalculatorTest, Add_Exception_001, TestSize.Level2)
```

### 多线程测试命名

多线程测试用例命名遵循相同规则：

```cpp
HWMTEST_F(CalculatorTest, ConcurrentAccess_001, TestSize.Level2, 4)
HWTEST_F(CalculatorTest, DynamicThread_001, TestSize.Level2)
```

## BUILD.gn 目标命名规范

### 测试目标命名

**格式**：`[ModuleName]Test`（小写）

**示例**：

```python
ohos_unittest("calculator_test") {  # 对应 CalculatorTest.cpp
    module_out_path = "calculator/calculator_test"
    sources = [ "CalculatorTest.cpp" ]
}

ohos_unittest("tel_state_registry_test") {  # 对应 StateRegistryTest.cpp
    module_out_path = "state_registry/tel_state_registry_test"
    sources = [ "StateRegistryTest.cpp" ]
}
```

### 输出路径命名

**格式**：`[subsystem]/[module]`

```python
module_output_path = "telephony/state_registry_test"
module_output_path = "msdp/utility_test"
module_output_path = "memory/dmabuf_heap_test"
```

## 类内方法命名

测试类中的辅助方法命名：

```cpp
class StateRegistryTest : public testing::Test {
public:
    // 辅助测试方法
    void UpdateCallState();
    void UpdateSignalInfo();
    void UpdateNetworkState();

    // 辅助方法命名规则：描述性动词 + 对象
};
```

## 常见命名错误示例

### ❌ 错误示例

```cpp
// 错误：序号不是 3 位
HWTEST_F(CalculatorTest, Add_1, TestSize.Level1)

// 错误：未使用 CamelCase
HWTEST_F(CalculatorTest, add_001, TestSize.Level1)

// 错误：测试文件命名不规范
// calculator_test.cpp（应使用 CamelCase）
// test_calculator.cpp（Test 应在末尾）

// 错误：测试套名与测试类名不一致
class CalcTest : public testing::Test { };
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 应为 CalcTest
```

### ✅ 正确示例

```cpp
// 正确：序号 3 位，CamelCase
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)

// 正确：测试文件命名
CalculatorTest.cpp
UtilityTest.cpp
StateRegistryTest.cpp

// 正确：测试套名一致
class CalculatorTest : public testing::Test { };
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
```

## 命名对照表

| 类型          | 格式                  | 示例                              |
| ----------- | ------------------- | ------------------------------- |
| 测试文件        | `[Module]Test.cpp`  | `CalculatorTest.cpp`            |
| 测试套         | `[Module]Test`      | `CalculatorTest`                |
| 测试用例        | `[Func]_[Seq]`      | `Add_001`                       |
| BUILD.gn 目标 | `[module]_test`     | `calculator_test`               |
| 输出路径        | `[subsys]/[module]` | `telephony/state_registry_test` |

## 相关文档

- [test-macro.md](test-macro.md) - 测试宏详细用法
- [comment-standard.md](comment-standard.md) - 注释标准
- [test-examples.md](test-examples.md) - 测试用例示例
